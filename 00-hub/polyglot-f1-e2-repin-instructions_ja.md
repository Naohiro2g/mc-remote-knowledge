# F1の固定し直しと、E2の決定との違いを返す依頼（Python・Java・Scratch・TypeScript）

> 多言語Client LibraryのE2で、接続の振る舞いを`2026-11-11-01`①〜⑧と`2026-11-12-01`で決めた。toolingがF1をその決定に合わせ、
> minecraft-remote-tooling `36ebe9e63e4f0afcf949eae998832f68209b8119`（PR #7、48 case）で返した（照合は
> `00-hub/polyglot-f1-e2-fixture-instructions_ja.md`の「返却と照合（2026-11-11）」）。この票は、F1の取得元をそのcommitへ固定し直し、
> 各clientの今の振る舞いと決定との違いを返してもらう依頼です。human owner 2026-11-10：「クライアントの多言語化を最優先とする。
> その先のUnity版マイクラリモコンを急ぐため」。参照するknowledge commitは、この依頼が入ったmainのcommitです。各担当は
> 「共通」と、自分の節を読んでください。

## 共通

### 決まったこと

- `2026-11-11-01`（wire「3.4 id 規律」「6.5 認証：ペアリングフロー」）
  - ①承認を拒む専用の応答は今は持たない。承認されなければ`pair_expired`になる
  - ②接続が閉じたら（相手のEOF、socketのerror、自分で閉じたとき。timeoutで回収したときを含む）、応答待ちのrequestを
    すべて、localな「完了不明」の失敗にする。serverのerrorとしては扱わず、reasonを作らない。LFの無い末尾は応答にしない。
    例外の型は言語ごと
  - ③応答は既定で長く待つ。その接続で最後に受信してからの時間で見て、超えたら「完了不明」で接続を回収する。生存確認は
    別に持つ。値と設定の仕方は言語ごと
  - ④自動で再送しない
  - ⑤接続が切れた後の次の呼び出しで、自動でつなぎ直す（既定で有効）。条件はDECISIONSの⑤のA〜G（「未送信」と
    「完了不明」を分ける、FASTとflushの境界、版と`catalogHash`の照合をやり直す、pairingは自動で進めない、一回に
    まとめる、backoffのばらつき、生存確認で切れたと分かる）。helloの`build`で、最後に成功を確かめたdimensionとoriginを戻す
  - ⑥serverが不正な行にerrorを返すかは契約にしない
  - ⑦認証reason（`token_expired`、`token_revoked`、`token_not_found`、`token_invalid`）でtokenを捨てたら、tokenなしのhelloへ
    戻り、`auth_required`のときだけpairingに入る。pairingは一接続試行につき一度（`2026-08-30-03`）
  - ⑧clientが`expires_in`を過ぎたと判断したpairingの期限切れは、`pair_expired`と同じ意味で扱い、serverのerrorの形（code
    とreason）は作らない。serverが言ったのか、clientが判断したのかが分かるようにする
- `2026-11-12-01`（wire「6.2 応答 `result`」）：clientが、成功したhelloの応答の版を互換でないと判定したら、次のrequestを
  送らずに接続を閉じ、applicationへ失敗を返す

### F1の取得元

- tooling `36ebe9e`の`packages/protocol/test/fixtures/`の、F1の6本（`client-bootstrap-{framing,hello,pairing,blocks,errors,close}-v23.2.1.json`、
  48 case）、`client-bootstrap-v1.schema.json`、`block-value-v22.json`（blocksの`value_refs`の範囲）。形の説明は同じcommitの
  `packages/protocol/README.md`
- `131f315`から変わったのは、close（F1-CL-03、05に`local_failures`と`pending_ids`）、pairing（F1-AU-07の前提、F1-AU-08〜10を
  追加。`pairing_attempts`）、schemaの3 file。ほかのfileとLICENSE（1,070 bytes、SHA-256
  `aa329a0bafc839b95124306141db13a381de45818bf629e983c44ea55ab5a7fb`）は同じbytes
- copyで持つときは、fileごとのbytesとSHA-256をtestで確かめる（F2、`2026-10-22-07`）

### すること

1. 取得元を`36ebe9e`へ固定し直し、CIでF1の48 caseをすべて通す。skipを残したら済みにしない
2. ②④⑦⑧と`2026-11-12-01`のそれぞれについて、今の振る舞いと決定との違いを表にする。違うものは直す。直すときは、そのcase
   （F1に無ければ担当のunit test）が、直す前に意図した理由で落ちることを見てから直す
3. ③⑤：今の振る舞い（timeout、生存確認、つなぎ直し）を書き、決定のとおりに入れるためのAPIの形（timeoutの設定、つなぎ
   直しの有効と無効、つなぎ直したことの知らせ、「未送信」と「完了不明」の失敗の型）を案にして返す。入れるのは次の票
   （TypeScriptは下の節のとおり、この票で入れる）。F1の③⑤のcaseは、toolingに頼んでいる
   （`00-hub/polyglot-f1-e2-ops-fixture-instructions_ja.md`）
4. caseが契約と違う、または読み方が決まらないと思ったら、そのcaseのIDと理由を返す。決まっていないことは、clientで新しく
   決めない
5. 認証の流れを変えたら、実McRemoteとのpulse（hello → `world.setBlock` → `world.getBlock`）を1本通す。相手は担当の手元の
   Paperと、公開のMcRemote `2321.1.0`（`protocol_mismatch`はcode `-32600`で届くが、reasonで判定するので通る）。Minecraftの中
   での承認など、人の操作が要るなら、その前で止めて手順を返す（human ownerが行う）。「live-auto相当」で、scriptとPASSの
   summaryを残す
6. 既定のbranchへのPRにして、CIが通ったら、担当がmergeしてよい（権限で拒まれたら、human ownerが行う）。tag、Release、
   公開のworkflowの実行はしない
- token、`pairing_id`、private endpoint、host、IP、player名、座標を、返却と公開のartifactへ書かない

## Python

- `2026-11-12-01`：応答の版の不一致は、F3で`Minecraft.create()`の失敗にした。接続を閉じているかを確かめる
- ⑦：認証reasonの後の流れが、F1-AU-08〜10のとおりかを確かめる

## Java

- ⑦：TypeScriptの返却（2026-11-11）で、Javaは認証reasonでtokenを捨てた後、すぐpairingへ進むと見えた。tokenなしのhelloへ
  戻す（F1-AU-08〜10）
- ⑧：Javaは、clientが判断したpairingの期限切れを、serverのerrorと同じ形（`-32000`、`pair_expired`）で作ると見えた。serverの
  errorの形を作らずに、同じ意味で扱い、どちらが判断したかが分かるようにする
- 既定の申告protocolは`23.0.0`のまま（human owner「24.0.0で揃えば問題ない」）。F1のcaseは`23.2.1`の申告を使ってよい

## Scratch

- Scratchは、F1をtestにつないでいない（Protocol Inventoryの「共有fixtureの使い方」）。1は、F1をtestにつなぐかを案にして
  返す（つなぐなら、どの層で、何caseか。F1は直接のTCPが基準で、browserのWebSocketの境界とは分ける）
- 2は、blockやUIの振る舞いを変えずに直せるものを直す。block、ペアリングのhat、表示を変えるものは、直さずに案を返す
  （human ownerが決める）

## TypeScript

- `2026-11-12-01`、②⑦⑧は、最初の縦sliceで今の形のまま合っている（照合は`00-hub/polyglot-typescript-start-instructions_ja.md`の
  「返却と照合（2026-11-11）」）。1で`36ebe9e`へ固定し直す
- ③⑤を、この票で決定のとおりに入れる。APIの形は担当が案にして返す。F1の③⑤のcaseが届くまでは、担当のunit testで持つ。
  toolingのcaseが届いたら、coordinatorが伝えるので、取得元を固定し直す
- ⑤のpairingは自動で進めない（D）。`onPairing`を渡していても、つなぎ直しで`auth_required`になったら止めて知らせる

## 返却

- 実際に読んだknowledge commit、PRの番号、merge commit、CIのrun ID
- fixtureの取得元の前と後（commit、copyならfileごとのbytesとSHA-256）と、fileごとのcase数とPASS数
- 2の表（決定ごとに、前の振る舞い、決定との違い、直したか、直したなら落ちたcaseと前と後）
- 3：今の振る舞いと、APIの形の案（TypeScriptは、入れた形とtest）
- pulse（したなら）：日付、Paperの版、McRemoteの版、手順、結果、認証の方法、片付けの方法
- 違うと思ったcase、決めずに残したこと
- Protocol Inventoryの「共有fixtureの使い方」の自分の行の、前と後
- Scratchだけ：F1をtestにつなぐかの案。直さなかったblockやUIの振る舞いの案

## coordinatorがすること

- 返却を、GitHubのAPI（PR、merge commit、CI、fixtureのbytes）で照合し、Protocol Inventoryへ写す
- 3の案を突き合わせ、③⑤を入れる票を作る
- toolingの③⑤のcaseのmerge commitを伝える
