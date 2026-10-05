# b8確認票の追記：human目視の完了とWireScope列幅のb9持ち越し

- 作成日: 2026-10-03
- 搬送元: scratch-editor／WireScope
- knowledge contract path: `00-hub/dev-repo-protocol_ja.md` runtime、`00-hub/release-gate-notes_ja.md`のb8節。表示実装の根拠は`15-wirescope/wirescope-deployment-design_ja.md` §13・14。liveのbaselineは`00-hub/b8-gate-live-test-sheet_ja.md`「共通」「3. Scratch」。
- knowledge contract commit: b9持ち越しの更新時に`3f0c14ab9e41e469a23f865b3e7a313744bdcdc7`をremote mainと照合し、runtime／INDEX／gateの該当記述を実参照。表示実装時の参照は`396326def73d99aae91dca4de9416f4eca6d2aea`、live baselineは指定済み`749ba60dc8c18938e50ce66b8e820aac4401c69e`。
- branch／push済みcommit: `agent/b8-compatibility@01cdb0bfee3a681697ffa44db5b890045b74b01c`。GitHub APIのbranch refとローカルHEADの一致をpush後に確認。
- 方針: 列幅修正はb9へ持ち越す（human owner「b9に送ります」、2026-10-03）。b8は凍結source `691576f`と既存成果物を維持する。

## human目視の完了

凍結source `691576f`で撮ったWireScope画像について、entityのmethod／送受信、typed particle、sound2 method、IDなしparticle通知の「送信済み・結果未確認」の4点を具体的に提示し、human ownerから「４点、オッケー。」を受領。segment 3のhuman目視をPASSへ更新した。

返却票は`../2026-10-03-b8-scratch-live-gate/RESULT_ja.md`、返答の捕捉は同素材の`materials/human-review.json`／`live-results.json`。server backpressureの実機案内、二人目player・描画／聴感等のsegment 4は未検証のまま。

## 表示調整の実装と確認

human ownerの列幅改善希望を受け、時刻列・方向列を内容幅へ詰め、通知ラベルの区切りに`wbr`を入れた。日本語では時刻104→60.1px、方向139.1→72.0px、ペイロード499.3→610.3px。表示文字列と時刻全文／tooltipは同じ。

保存済みフレームによる別プレビューを提示し、human ownerから「確認しました。オッケーです。」を受領。2ファイルだけの変更を1 commitにまとめ、pushした。

- 変更: `mc-remote/live/src/main.ts`、`mc-remote/live/src/styles.css`のみ。GUI／VM／Bridge／Protocol／fixture／observer schema／sanitizer／wire認識のsourceに差分なし。
- 検証: `npm test --workspace=@mc-remote/live`（lint／Prettier、13 suites／142 tests）PASS。`npm run build --workspace=@mc-remote/live`（web app／observer lib／tsc）PASS。コミット対象と検証したコードは一致。
- browser: 独立Chrome、JA／EN／ja-Hira、1280px／600pxの6表示PASS。通知が2行、方向と時刻全文・tooltipが一致、ペイロード幅が増加、狭幅で時刻切れなし。保存済みlive frameをMessageChannelで渡す表示確認であり、新たなMinecraft接続やlive PASSの再実施には数えない。
- commitlint PASS。stageなし、追跡済みworktreeはclean。ユーザーの未追跡作画素材等は変更していない。

## b9への引継ぎ素材のartifact identity

push済みsourceのpackage buildから標準`build-artifact.mjs --source-commit`で作成。6 asset、source commit、package.json／lock、各bytes／SHA-256を実ファイルと照合してPASS。

| file | bytes | SHA-256 |
| --- | ---: | --- |
| wirescope-app.zip | 83993 | 7d66aa0d1cdf41ea98669185a988c046b736c4fa6a871b427e81f60e6e74e579 |
| wirescope-app.manifest.json | 2321 | 5588cdb1abd8d65004a393bc91b83cc6e947ef425125c0ec18c84a5ca2508fb4 |

- source: `01cdb0bfee3a681697ffa44db5b890045b74b01c`。ZIP／manifestは本票の`materials/`に保存。
- 元の凍結5成果物はbytes／SHA-256を再照合して全件一致。`b8-integrated-artifact-set-1`のWireScope ZIP（83746 bytes／`4cb34989…70a07`）とmanifest（2321 bytes／`6ea468f5…24d0`）は置き換えていない。
- B8 fixture: `entity-particle-v23.2.json`、owner commit `054a3af017f1abb8cc01cf85b3bc83181e648e19`、36481 bytes／111 case／SHA-256 `ca636b4a2685ea67f24d8e7931e3d30a84e7cec872bb5c5d2eadd178cdac39f2`で不変。
- 根拠素材: `materials/artifact-identities.json`、`verify-artifacts.py`、`full-build.log`、`test.log`、`column-measurements.json`、`columns-before.png`／`columns-after.png`、`column-width.patch`。

## b9への持ち越し

human ownerの判断で列幅修正はb9へ持ち越す。knowledge `3f0c14ab9e41e469a23f865b3e7a313744bdcdc7`のgate節にも「b8には入れず、b9で出す」と記録されていることを確認した。b8のexact setとPython同梱WireScopeは既存identityを維持する。

引継ぎ先はb9のWireScope担当。実装commit `01cdb0bfee3a681697ffa44db5b890045b74b01c`、patch、表示確認と上記ZIP／manifestを参照素材として保持する。b9のgateを開くときに取り込み状況、release source／artifact、Python同梱物を確認する。現ZIP／manifestはb9への引継ぎ素材であり、b9のrelease identityは未確定。

元のlive観測はsource691576fと旧ZIPに結び付けたまま維持する。shared／devへの配置、他repo作業の依頼、正式exact setの変更、tag／Release／OCI公開、component／横断GREENの主張は行っていない。
