# 接続の生存確認、回収、pairingの途中の接続について、今の振る舞いを返す依頼（McRemote）

> 多言語Client LibraryのE2で、clientの待ち方とつなぎ直しを決めた（`2026-11-11-01`③⑤、`2026-11-12-05`）。clientは既定で長く
> 待ち、接続が切れたら次の呼び出しで自動でつなぎ直す。各clientへは、それを入れる票（`00-hub/polyglot-e2-reconnect-instructions_ja.md`）
> を出した。検討メモ（`10-protocol/connection-liveness-notes_ja.md`）では、serverの側にも確かめることが残っている。いちばん重いのは、
> clientが黙って消えたときにserverに残る接続（メモの「3」の2）。そうした接続が枠を使っていると、つなぎ直したclientが入れない
> おそれがある。coordinatorは、McRemoteが今どうしているかを調べていない。この票は、今の振る舞いを返してもらう依頼です。
> codeは変えない。参照するknowledge commitは、この依頼が入ったmainのcommitです。

## 前提

- 決まっていること：
  - 認証前の資源制限（同時connection、accept rate、frame size、idle／hello timeout、pair begin／poll rate、pending pair数）に
    当たった接続は、transportを閉じるだけにする。どれに当たったかは、serverの理由別の集計で見る（`2026-10-07-02`）
  - 同一UUIDの並行セッションの上限は16（`2026-07-04-03`）
  - pairingのpollは`pairing_id`で対応させるので、`auth.pairBegin`と`auth.pairPoll`で同じTCPを保たなくてよい（wire「6.5」）。
    pairingの途中で接続が切れたら、clientは期限内なら同じ`pairing_id`の次のpollを新しい接続で送る（`2026-11-12-05`）
- 決まっていないこと：serverの側の生存確認と回収の要否、値。この票の返却を見て決める
- PR #18（`protocol_mismatch`と`expected_hello`のcode）とは別の依頼。PR #18とそのreleaseを待たせない

## 返してほしいこと

答えるときは、読んだMcRemoteのcommit（`main`の先頭）を書く。codeの場所（classやmethod）と、確かめたtestがあればそれも書く。

1. **認証後の接続の生存確認**：clientが黙って消えたとき（電源断、Wi-Fiの切断、IPアドレスの変化）、McRemoteはその接続を見つけて
   閉じるか。TCPのkeepalive（`SO_KEEPALIVE`など）、読み取りのidleの上限、ほかの仕組みのどれを使っているか。既定の値と、設定の
   名前
2. **残った接続と上限**：見つけられずに残った接続は、同一UUIDの並行セッションの上限16と、ほかの接続数の上限（全体、IPごと
   など）に数えられるか。上限に当たったとき、新しい接続はどうなるか（拒む、古いものを閉じる、など）。そのときclientには何が
   届くか
3. **観測**：開いている接続の数、最後に受信してからの時間、回収した接続の数を、operatorが見られるか。認証前の理由別の集計
   （`2026-10-07-02`）と同じ形で見られるか
4. **pairingの途中の認証前の接続**：C#が実McRemote（`2321.1.0`）で、承認を待つ間に認証前のTCPが閉じられたのを見た。どの上限に
   当たったと考えられるか（idle／hello timeoutなど）。その既定の値と、pairingの期限（`expires_in`、約120秒）との関係
5. **`ok`の後のpoll**：`auth.pairPoll`がtokenつきの`ok`を返した後に、同じ`pairing_id`でもう一度pollが来たら、何を返すか
   （`pair_not_found`など）。`2026-11-12-05`は、これを確かめずに決めた
6. **つなぎ直しが重なるとき**：serverの再起動の後などに、多くのclientが続けてつなぎ直すと、認証前の上限（accept rate、pair
   begin／poll rateなど）に当たりうるか。既定の値
7. 1〜6のうち、直した方がよいと思うものがあれば、案を返す（codeは変えない）

## 返却

- 実際に読んだknowledge commitと、McRemoteのcommit
- 1〜7の答え。値は既定の値と設定の名前で書く
- 確かめられなかったことと、その理由
- token、`pairing_id`、host、IP、player名、UUID、座標を書かない

## coordinatorがすること

- 返却を、検討メモと突き合わせる。serverの側の生存確認と回収を決める案を作り、human ownerに見せる
- 5の答えを`2026-11-12-05`の記録に足す
