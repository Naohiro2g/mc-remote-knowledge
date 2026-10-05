# WireScope列幅の表示調整

- 元の表示確認: b8統一実施票segment 3。human ownerがWireScope画像の4点を確認済み。
- 依頼: 時刻列を詰め、方向列は通知表示の2行折り返しを許容して詰める。
- 参照SSOT: knowledge `396326def73d99aae91dca4de9416f4eca6d2aea`、dev runtime、INDEX、WireScope deployment design §13・14。b8 exact setは`691576f`のまま。
- 実装案: 時刻・方向をtableの内容に必要な幅へ変更し、通知ラベルの区切りにwbrを置く。表示文言、時刻の内容／tooltip、wire、observer schemaは維持。
- 状態: human ownerが調整後画像を承認。`agent/b8-compatibility@01cdb0bfee3a681697ffa44db5b890045b74b01c`としてcommit／pushし、GitHub ref一致を確認。後続WireScope ZIP／manifestを別素材として作成した。human ownerの判断でb9へ持ち越し（2026-10-03）。b8の凍結source `691576f`、成果物と正式live画像は維持する。
- 持ち越しのSSOT確認: knowledge remote main `3f0c14ab9e41e469a23f865b3e7a313744bdcdc7`のruntime／INDEX／release gate節を読んだ。「b8には入れず、b9で出す」の記録と一致。
- 引継ぎ先: b9のWireScope担当。上記commit、patch、検証素材とZIP／manifestを保持し、b9のgateを開くときに取り込み状況とrelease identityを確認する。現成果物は引継ぎ用で、b9のrelease identityは未確定。
- 検証: `npm test --workspace=@mc-remote/live`（lint／Prettier＋13 suites／142 tests）PASS。Viteによる別outDirのプレビューbuild PASS。`preview-columns.cjs`による独立ChromeのJA／EN／ja-Hira、1280px／600pxの6表示PASS。時刻の全文・tooltip・方向の全文を維持し、通知が2行、ペイロードが拡大、狭い画面でも時刻が切れないことを確認。既存の横scrollは維持。
- 日本語の実測: 時刻104→60.1px、方向139.1→72.0px、ペイロード499.3→610.3px。before／after画像を実見して折り返しと文字切れを確認。
- full package build（web／lib／tsc）もPASS。標準builderが生成したZIP83993 bytes／SHA-256 `7d66aa0d1cdf41ea98669185a988c046b736c4fa6a871b427e81f60e6e74e579`、manifest2321 bytes／`5588cdb1abd8d65004a393bc91b83cc6e947ef425125c0ec18c84a5ca2508fb4`を6 assetと照合。元の5成果物とfixture不変も再照合PASS。
- 素材: `materials/`の画像・測定JSON・preview script・patch・test／full-build log・ZIP／manifest・artifact-identities.json。ナレッジへの返信は`GATE-ADDENDUM_ja.md`。shared配置、正式exact set更新、tag／release公開なし。
