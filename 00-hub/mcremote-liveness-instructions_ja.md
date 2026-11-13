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

## 返却と照合（2026-11-13）

McRemoteは、knowledge `f05f2a1440cbf2aed0841689bd0c3fc60d4ada03`（この依頼が入ったcommit）と、McRemoteのmain
`cdafcfd804614def19a35b099bedc93697ca4899`（PR 17のmerge）を読んだ。coordinatorはGitHubのAPIで、このcommitが今もmainの先頭で
あることと、出荷tag `v2321.1.0`がcommit `5b78ded96d1ad6d45160b67c5f8a13e14adb3fc8`を指すことを確かめた。McRemoteは、関わる
7つのclassがこのtagと同じだと返した。code、test、configは変えていない。既存のtestを6 class 17件走らせ、すべて通った。

1. **認証後の生存確認**：TCP keepaliveは有効（`RemoteSession.init`）だが、待ち、間隔、回数はOSに任せる。認証後の読み取りに
   期限は無い（helloの後は`setSoTimeout(0)`）。最後の受信で回収する仕組みも、heartbeatも無い。EOFや読み書きのerrorなら閉じ、
   tickで枠を返す。設定の名前は無い
2. **残った接続と上限**：気づけない接続は、同一UUIDの16枠（`auth.max_sessions_per_uuid`）と全体の枠を使い続ける。古い接続を
   閉じて入れる処理は無い。16枠に当たると、helloに`too_many_sessions`（code `-32000`、dataに`limit`と`current`）を返して閉じる。
   全体の枠、hello前の枠、accept rateに当たると、transportを閉じるだけ。全体の枠とrateは、Paperの`max-players`で選ぶ内部の
   profileで決まり、設定の名前は無い（旧`connection.*`などのkeyは廃止）

| Paperの`max-players` | 全体の枠 | hello前の枠 | accept／秒 | pairBegin／秒 | pairPoll／秒 | pendingのpairing |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| 16以下 | 64 | 32 | 80 | 20 | 64 | 32 |
| 17〜24 | 96 | 48 | 112 | 28 | 96 | 48 |
| 25以上 | 128 | 64 | 144 | 36 | 128 | 64 |

3. **観測**：開いている接続の今の数、最後の受信からの時間、回収した接続の数は、どれも見られない。見られるのは、起動時の
   profile、最高値（`connection_peak`など）、認証前の理由別の拒否（`ConnectionLimitStats`）
4. **pairingの途中の認証前の接続**：無通信30秒（`IDLE_TIMEOUT`）と、接続から数えるhelloの期限180秒（`HELLO_DEADLINE`。
   pairingの期限＋60秒以上で、pollでは延びない）。pairingの期限は120秒（`auth.pair_code_ttl_seconds`、beginから）。C#が見た
   切断がどれだったかは、渡された情報では決められない。TCPが切れてもpendingのpairingは消えず、期限内なら新しいTCPから続けられる
5. **`ok`の後のpoll**：`pair_not_found`（code `-32000`）を返す。`ok`を返す時にpendingを消し、応答が届いたかは待たない。`ok`を
   もう一度渡す仕組みは無い。`2026-11-12-05`の状態の欄と、wire「6.5」に足した
6. **つなぎ直しが重なるとき**：上の表のrateはplugin全体で共有するので、当たりうる。当たるとtransportを閉じるだけ
7. **案**（採っていない）：観測を足す。認証後のkeepaliveの実効値と回収を較正する（長く静かな正常な接続は切らない）。古い接続を
   閉じて入れるかは、観測を見て決める。5の意味を記録する

返却が別に見つけたこと：BANで拒む経路で、接続の枠（lease）が返らない。codeを読んだだけで、実行しては確かめていない。human
ownerが直すと決めた（下の「追加の依頼：BANで拒む経路の枠と、認証後の接続の回収（2026-11-13）」）。

確かめられなかったこと：電源断やWi-Fiの切断の実機での再現、稼働OSのkeepaliveの値、C#の切断の原因、16枠を埋めた実機での拒否。
稼働OSの値は、Stackの返却で、公開VPSのMinecraftのcontainerの既定が7200秒、75秒、9回と分かった（`00-hub/stack-liveness-instructions_ja.md`
の「返却と照合（2026-11-13）」）。McRemoteは値を指定しないので、黙って消えたclientに気づくまで約2時間11分の計算になる。

serverの側の回収は、`2026-11-13-02`で決めた。黙って消えたclientの認証後の接続を、数分（目安5分）で見つけて閉じ、枠を返す。
観測の追加と古い接続の追い出しは、今はしない。

## 追加の依頼：BANで拒む経路の枠と、認証後の接続の回収（2026-11-13）

> 上の返却を受けた直しの依頼です。human owner 2026-11-13：「McRemoteが別に見つけた不具合を治す」。続けて、coordinatorの振り返り
> の案（BANの直しと、socketごとのkeepaliveを1つのPRにする）を採った。PR #18とは別のPRにする。参照するknowledge commitは、
> この依頼が入ったmainのcommitです。

### 前提

- 返却の観察：`ServerListenerThread`は枠（lease）を取ってsessionを作る。`McRemote.handleConnection`は、BANで拒むときにkickして、
  リストに登録する前にreturnする。今の`kick`は、playerに結びついていなければ何もせず、どちらの場合も`RemoteSession.close()`を
  呼ばない。tickの`close()`にも進まないので、全体の枠とhello前の枠が返らない
- 認証前の資源の上限に当たった接続は、transportを閉じるだけにする（`2026-10-07-02`）
- `2026-11-13-02`①：McRemoteは、黙って消えたclientの認証後の接続を、数分（目安5分）で見つけて閉じ、枠を返す。静かでも応答する
  接続は切らない。手段は、socketごとのTCP keepaliveの値の指定（Java Client Libraryが`jdk.net.ExtendedSocketOptions`でしている形）

### すること：BANで拒む経路

1. BANで拒んだ接続の後に、全体の枠とhello前の枠が戻ることを見るtestを書き、直す前に意図した理由で落ちるのを見る
2. BANで拒む経路でも、socketを閉じて枠を返すように直す。BANの判定と、拒む条件は変えない
3. 直す前と後で、BANで拒まれたclientに何が届くか（kickの文、errorの応答、閉じるだけ、閉じない）を返す。届くものを新しく
   決める必要が出たら、決めずに返す
4. BANで拒んだ件数が、認証前の理由別の集計（`ConnectionLimitStats`）に入るか、今と直した後を返す。新しい理由は足さない
5. 同じ形で枠が返らない経路がほかに見つかったら、直さずに返す

### すること：認証後の接続の回収

6. 接続のsocketに、TCP keepaliveの待ち、間隔、回数を指定する。値は、目安5分で回収できるもの（例：60秒、30秒、8回）から選び、
   選んだ値と理由を返す。socketを作るときに付けるので、認証前の接続にも付く。認証前の期限（`2026-10-07-02`）は変えない
7. JDKやOSが値の指定を受け付けない環境では、今のまま（SO_KEEPALIVEとOSの既定）にし、起動時のlogで分かるようにする
8. 値を指定したことを見るtest（socketのoptionを読む）を書き、直す前に落ちるのを見る。実際の回線の切断での回収は、実機では
   試さない
9. operatorの設定（config key）は足さない。要ると思えば、案で返す
10. 認証後の読み取りの期限、heartbeat、古い接続の追い出し、接続の観測は足さない（`2026-11-13-02`）

### 進め方

- 1〜10を1つのPRにし、既定のbranchへ出す。localとCIの検査を通す。mergeはhuman ownerが判断する。tag、Release、公開の
  workflowの実行はしない。releaseの版と時期は、human ownerが決める
- 実機でBANを使う試験はしない。要るとhuman ownerが判断したときは、その前で止めて手順を返す

### 返却

- 実際に読んだknowledge commit、PRの番号とhead、CIのrun ID
- 落ちるのを見たtestと落ち方、直した後
- 3、4、5の答え。6で選んだ値と理由、7の環境の扱い
- token、`pairing_id`、host、IP、player名、UUID、座標を書かない

### coordinatorがすること

- PRの差分、test、CIをGitHubのAPIで照合する
- human ownerにmergeとreleaseの時期を聞き、hub NOTES 2026-11-12の「McRemoteの次のrelease」の行に足す
