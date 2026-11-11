# F1に、待ち方、つなぎ直し、clientが判断する終わりのcaseを足す依頼（tooling）

> F1をE2の決定（`2026-11-11-01`）に合わせる票（`00-hub/polyglot-f1-e2-fixture-instructions_ja.md`）で、toolingは48 caseを返し
> （minecraft-remote-tooling `36ebe9e63e4f0afcf949eae998832f68209b8119`）、③④⑤⑧と互換判定の後のcloseは、今の`steps`と`expected`
> では表せないとして案を返した（同じcommitの`packages/protocol/F1_E2_PROPOSALS_ja.md`）。互換判定の後のcloseは`2026-11-12-01`で
> 決めた。この票は、その案を形にして、caseを足す依頼です。TypeScriptが③⑤を入れ、C#が最初の縦sliceを作るときに使う。
> 参照するknowledge commitは、この依頼が入ったmainのcommitです。

## 決まったこと

- `2026-11-12-01`（wire「6.2 応答 `result`」、versioning「8.3 不一致時」）：clientが、成功したhelloの応答の版を互換でないと
  判定したら、次のrequestを送らずに接続を閉じ、applicationへ失敗を返す
- `2026-11-11-01`の②（閉じたら応答待ちをすべてlocalな「完了不明」の失敗にする。相手のEOF、socketのerror、自分で閉じた
  とき、timeoutで回収したときを含む）、③（最後に受信してからの時間で見る。生存確認は別）、④（自動で再送しない）、⑤（次の
  呼び出しで自動でつなぎ直す。条件はDECISIONSの⑤のA〜G）、⑧（clientが判断したpairingの期限切れは`pair_expired`と同じ意味。
  serverのerrorの形は作らない。どちらが判断したかが分かる）
- 値と設定の仕方（timeoutの長さ、backoffの値）は言語ごと。fixtureで値を決めない

## PRを2つに分ける

1. **今のopsで表せるもの（先に）**：C#が最初の縦sliceで使うので、先にmergeする
   - 互換判定の後のclose：成功形のhelloの応答をclientが互換でないと判定し、次のrequestを送らずに閉じ、applicationへ失敗を
     返す。今のF1-HE-04、05のexpectedへ足すか、新しいcaseにするかは、toolingが選び、理由を返す
   - ②の残り：JSONは閉じているがLFの無い末尾のままEOFになり、応答にしない（F1-FR-05とF1-CL-03を合わせた形）。socketの
     errorと、自分で閉じたときの、応答待ちの回収。今のopsで表せないものがあれば、2へ回す
2. **新しいopsが要るもの**：`F1_E2_PROPOSALS_ja.md`の「追加案の返却」の表を形にする
   - applicationの呼び出しと、その結果（request idを持たない呼び出しの「未送信」を含む）の表し方
   - clientのtimeoutの設定に結びつく仮想の時計（期限の直前と到達を、値を決めずに表す）
   - 「送らないこと」を確かめる区間（④、⑤の旧requestの自動の再送）
   - notification（FASTの`world.setBlock`）と、接続ごとの観測（どの接続の互換判定か、どの接続の設置まで`connection.flush`が
     保証するか）
   - clientが判断して終わるpairing（⑧）。F1-AU-02は、serverが期限切れを返す経路として今のまま残す
   - caseは、③の期限と途中の受信、④、⑤の`build`の復元、つなぎ直せなかった呼び出し、旧FASTとflush、つなぎ直した
     helloでの非互換、⑧。⑤のA〜Gの残り（handleとcursorの失効、eventを失った知らせ、`auth_required`で止まる、一回の
     つなぎ直しへまとめる、backoffのばらつき、生存確認）は、表せるものを足し、表せないものは理由を返す
   - schemaの版を上げるか（`client-bootstrap-v1.schema.json`を広げるか、v2にするか）は、toolingが選び、理由を返す。
     今のconsumerが読めなくなるなら、そう書く

## 進め方

- 既定のbranchへのPRにして、CIが通ったら、担当がmergeしてよい。tag、Release、公開のworkflowの実行はしない
- 今の48 caseは変えない。直したいところが見つかったら、変えずに返す（1で、F1-HE-04、05を直すと選んだときは除く）
- 決まっていないことは、fixtureで決めない。決める必要が出たら、決めずに返す
- 足したcaseのfileの`knowledge_contract.commit`は、この依頼が入ったknowledgeのcommitにする

## 返却

PRごとに：

- 実際に読んだknowledge commit、PRの番号、merge commit、CIのrun ID
- 変えたfileの一覧（bytes、SHA-256）、足したcaseのIDとcaseの数
- 足したopsと`expected`の欄（2）と、そう決めた理由。schemaの版の扱い
- 表せずに残したことと、その理由

## coordinatorがすること

- 返却をGitHubのAPI（PR、merge commit、CI、fileのbytes）で照合し、Protocol Inventoryの共有fixtureの行を直す
- 1のmerge commitをC#へ、2のmerge commitをTypeScriptへ伝える。ほかのclientへは、固定し直しの票を作る
