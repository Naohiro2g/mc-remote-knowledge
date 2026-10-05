## Release gate 確認票（b9実機試験・Scratch segment 3追記）

- 対象 repo: `Naohiro2g/scratch-editor`（移管済みBridge／WireScopeの配布元は`Naohiro2g/minecraft-remote-tooling`）
- 対象 branch/commit: Scratch `agent/b9-tooling`／`develop`、凍結source `7fbbf034488760d8fc7e034bf23f3e08e6e1807d`。tooling凍結source `dc1ab834183e29f2eb03059b07e99d2b463776ee`
- release / channel: `2320.0.0b9`／beta candidate、protocol `23.2.0`
- gate coordinator: knowledge担当session
- human release owner: プロジェクトオーナー
- current phase: 凍結済み・実機試験。Scratch segment 3の新規pairing、代表ブロック、独立ChromiumのWireScope frame確認、時刻列／方向列の幅のhuman確認がPASS。Bridgeの実行形態の採否はcoordinator判断待ち
- contract maturity / required test tier: 批准済み契約。凍結後のTier 3、変更箇所の代表往復
- knowledge contract path: `00-hub/b9-gate-live-test-sheet_ja.md`「共通」・§3、`00-hub/release-gate-notes_ja.md`「確認票」・2026-10-04の節
- knowledge contract commit: `561de98b5c15864ac9b86cb6dcaeef1f20ce635b`（実際に読んだpush済みSHA。取得時remote mainも一致）
- gate manifest identity: 独立したgate manifestは未提示。凍結根拠は上記gateの節。使用candidate manifestは1,821 bytes／SHA-256 `239f7f94cf31e732eff173744da105408b00b182d0aad73507623ea09b43bc6b`
- change cone: 移管したBridge／WireScope、`chat.post`の成功result `null`、未知eventへの対応、WireScopeの列幅。手元の凍結candidate配信、接続、統一実施票§3の代表往復を実施。公開sourceは変更なし
- reused PASS / rationale: 実施票の方針どおり、APIを変えない部分のb8 live PASSを再利用する。今回は代表往復とobserver表示を確認し、Minecraft画面上の粒子描画・音の聴取・receiver差のhuman試験は繰り返していない。未知eventは実サーバーから出せないため、既存deterministic testを使う。今回、unit suiteの再実行はしていない
- exact compatibility set / freeze status: `b9-integrated-artifact-set-1`、凍結済み。使用GUI／Bridge／WireScopeとcandidate manifestは凍結identityに一致。稼働JARのSHA-256は本担当では採取していない
- target deployment / profile / lock: dev通常環境。Scratch／Bridge／WireScopeは手元端末。取得pinは`mc-remote/tooling-lock.json`。GUI／WireScopeは静的配信。Bridgeは凍結OCIのlinux/amd64 `/app`を展開し、host-native Node `24.19.0`で実行
- authorized next action: 実施結果をcoordinatorへ本票で返す。shared設定変更、他repoの試験、tag／Release公開の権限は今回の票に含まれない
- test class: `live-auto`（認証前transport確認、独立Chromiumの実Blockly blockとScratch VMを使った代表往復、独立WireScopeのDOM・画像確認）、`live-human`（human ownerの既存token接続、新規pairing承認、列幅目視確認）
- 実行した command / 手順: `materials/prepare-runtime.py`でcandidate ZIPと使用artifactのbytes／SHA-256、OCI source label・layer digestを照合して展開。HTTP file hash照合とWebSocketの`hello`→one-shot `auth.pairBegin`を実行。human ownerの保存済みtoken接続を記録。`node materials/open-validation-browser.cjs`で独立Chromium（headless、Playwright、ja-JP、Asia/Tokyo、viewport1600×1100、新規browser context）を起動し、human ownerが新規pairingを承認。`node materials/check-representative-blocks.cjs`で実Blockly blockをworkspaceへ作成し、Scratch VM経由で代表往復・pickerのclick／検索／適用を実施。`node materials/finalize-browser-check.cjs`で既に完了した22 frameを独立WireScopeのDOMへ照合し、sanitized記録と画像を保存。この最終照合で追加のMinecraft操作は送信していない
- 結果: 下表。代表ブロック12回の実行と、対象22 frameの表示がPASS。human ownerが画像を確認し「画像確認しました。オッケーです。」と返答したため、時刻列／方向列の幅もPASS。Bridgeの実行形態についてはcoordinatorへ判断を求める
- evidence record / artifact: 搬送素材 `handoff-materials/2026-10-05-b9-scratch-dev/`。`materials/user-b9-hello.json`にhuman提示の2行、`materials/independent-browser-hello.json`に新規pairingと版照合、`materials/representative-results.json`に代表往復・検索・表示・cleanup、`materials/wirescope-b9.png`／`wirescope-b9-columns.png`と`picker-gold.png`／`picker-door.png`に画面。準備段階の`materials/readiness.json`は当時の観測として保持。`materials/runtime-identity.json`に使用artifactと展開fileのidentity。bytes／SHA-256は`INVENTORY.json`と`SHA256SUMS`。正式evidenceは未着地。knowledge側での収容先案は`14-evidence/artifacts/2026-10-05-b9-scratch-live/scratch/`、record案は`14-evidence/records/2026-10-05-b9-scratch-live_ja.md`
- 未検証の境界: OCI container実行、実サーバーJARのexact digest・Paper／Java・credential healthの本担当による採取。b9でMinecraft画面上の描画や音を再確認したとは主張しない。他segmentの完了と横断判定も本担当では行わない
- security / compatibility / rollback の確認: devの認証設定を変更していない。通常browserのprofileと保存済みtokenに触れず、独立Chromiumの新規sessionはScratch自身が保存・使用。実tokenの読出し・コピー・エクスポートなし。認証なしhelloは`auth_required`、humanの保存済みtoken接続と独立browserの新規pairing接続は成功。private実値・token・pairing_id・player UUIDを票に含めず、取得frameも再sanitize。試験位置は事前にairを確認し、gold_block設置後に元のairへ復元・読戻し一致。生成したarmor_standは削除成功。b8 source／tagと手元runtimeを保持。戻し作業そのものは未試験
- 判定を求める事項: Docker daemonが無いため、Bridgeは凍結OCI内のコードをhost-native Nodeで実行した。この観測を移管後Bridgeの検証材料として採れるか、OCI container実行を別途要するかをcoordinatorへ返す。横断GREEN／HOLD／REDや公開可否は判定しない

| 項目 | 結果・根拠 |
| --- | --- |
| 凍結candidate／使用artifactのidentity | PASS。bytes／SHA-256を再照合 |
| b8 Scratch→b9 pluginの既存token継続 | PASS。human ownerの報告。独立transcriptは未採取 |
| b9 Scratch→b9 pluginの既存token接続 | PASS。再ペアリングなしで成功したとのhuman報告 |
| 最初の認証済みhelloの版照合 | PASS。08:02:10のWireScope提示でclient `2320.0.0b9`、protocol `23.2.0`、MC `1.21.11`、成功result |
| WireScopeのhello要求／応答表示 | PASS。human提示の2行で確認。独立Chromium確認とは区別 |
| 移管Bridgeのone-shot `auth.pairBegin` | PASS。6桁pair code発行。調査socketは正常切断 |
| 新規pairingの承認／`auth.pairPoll`／再hello | PASS。独立Chromiumでpair code発行、human owner承認後にconnected。認証済みhelloのprotocol23.2.0／MC1.21.11一致 |
| チャット | PASS。実ブロックから`chat.post`、成功result `null` |
| ブロック設置／読戻し | PASS。無印`gold_block`で設置、`world.getBlock`は`minecraft:gold_block`。事前のairへ復元後、読戻しが元の情報と一致 |
| entity | PASS。`armor_stand`生成のhandleをScratch変数へ格納し、`entity.getPose`成功、最後に`entity.remove`成功 |
| particle | PASS。dust reporterを実ブロックへ差込み、RGB255/0/0・size1・receiver self、count10の要求にaccepted10 |
| sound | PASS。soundOptions reporterを差込み、`block.note_block.harp`、volume0.25／N12→note12／receiver self、成功result `null` |
| カタログID一覧 | PASS。blockの1166件がリストへ入り、完全修飾ID・整列・`minecraft:gold_block`含有を確認。取得済みcacheを使用 |
| picker検索／適用 | PASS。`gold`5件、`金ブロック`1件、`Block of Gold`2件、`door`42件。日英名とID表示、gold_blockの適用を確認 |
| 独立Chromiumで代表frameが落ちずに表示されること | PASS。9 methodの要求／応答がDOMに存在。代表実行の22 frameをsequence・method・directionで全件照合。画像の「古いフレーム26件省略」は過去の履歴に対する表示で、今回の対象22 frameは全件残っている。認証methodと`catalog.get`はScratch observerのallowlist外のため表示対象に含めない |
| WireScope時刻列／方向列の幅のhuman確認 | PASS。1600×1100の独立Chromiumで時刻約60.1px／方向約60.8px。`wirescope-b9-columns.png`をhuman ownerが確認し「画像確認しました。オッケーです。」（2026-10-05）。記録は`human-width-review.json` |

自動試験helperでの失敗と修正は、凍結candidateのFAILと区別して記録した。空のtext shadowにfieldを補う処理の不足、前のreporter吹き出しを閉じずに次を実行したことによるfocus例外、observerの表示対象にない認証／catalog通信を必須としていた判定が該当する。サーバーの失敗応答はなく、helperだけを修正した。元の失敗結果3件は`representative-results-*-failure.json`へ保持。最後の再照合ではMinecraft操作を繰り返していない。

使用した配布物は次のとおり。GUIのindex／gui.jsとWireScope ZIP内の全6 fileは、HTTP配信したbytesも照合済み。

| 配布物 | bytes | SHA-256 |
| --- | ---: | --- |
| `scratch-gui.tar.gz` | 138376671 | `c0d08c26b0d016c7cf4f57661022c631be0f2aa3d1d7d517ce97fd75e118c75d` |
| `bridge.oci.tar` | 114628096 | `b6a6feec07e8d7ae9805a81e8dc370e6220e91af145ef3117ce5ed12e703b100` |
| `wirescope-app.zip` | 83854 | `da3da0b6cf4d05265bc0c11abaa4913208c7cfc3600b0c3e78c93a356fc431ad` |
| `wirescope-app.manifest.json` | 2339 | `c654f7d1f0be2773d6737e889279b2587317088717f162b082c82be9cff910d7` |

Bridge OCI index: `sha256:5828304c9bb1d60df8672f9189f503790050e09358bd375f39e4d59d190eb84f`。
配布元はScratch candidate run `37232396741`、tooling run `37220882228`。
humanの列幅確認は`materials/human-width-review.json`へ記録。試験専用Chromiumは終了済みで、通常browserは未操作。localhostのScratch／WireScope配信はHTTP200で継続を確認し、結果を`materials/completion.json`へ記録した。
`private/`と稼働中の`runtime/`は公開evidence収容対象にせず、稼働serviceが参照中なので削除しない。
