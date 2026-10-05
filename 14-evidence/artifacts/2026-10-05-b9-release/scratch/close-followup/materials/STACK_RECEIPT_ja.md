# Stack受領結果：設定契約・WSS検査

- 作成日: 2026-10-06。
- 搬送元: Scratch `2026-10-06-stack-backstage-handoff/materials/STACK_ja.md`。
- 搬送先: Stack／Codex、`agent/home-luckperms@a30aa8b1b230e88ed92c515b357a088d97ddb0da`。
- knowledge contract path: `00-hub/deployment-interface-design_ja.md` §3・4・7・8、`00-hub/dev-repo-protocol_ja.md` runtime、`00-hub/b9-gate-close-instructions_ja.md`。
- knowledge contract commit: `5beaad2557abbc6e90ada03edf7d0a2918fa7a52`（remoteから取得・実読）。
- 結果: 設定生成、直接Bridge／外側WSS検査ともに対応済み。今回新たな製品修正は不要。

## 受領と収容

元6fileすべてのbytes／SHA-256が [Scratchのinventory](incoming-stack-source-inventory.json) と一致した。
収容後にも全文の一致を確認した。全fileの元path、収容先path、bytes／SHA-256は
[受領inventory](received-inventory.json) にある。今回の受領素材はすべてGit管理外・未commit。

| 元directory／file | Stack側の収容先（repoルート基準） | 処理 |
| --- | --- | --- |
| home-scratch-contract-reply／MANIFEST_ja.md | handoff-materials/2026-10-06-stack-backstage-handoff/materials/scratch-contract-reply/MANIFEST_ja.md | コピー |
| home-scratch-contract-reply／materials/reply_ja.md | handoff-materials/2026-10-06-stack-backstage-handoff/materials/scratch-contract-reply/materials/reply_ja.md | コピー |
| stack-wss-reply／MANIFEST_ja.md | handoff-materials/2026-10-06-stack-backstage-handoff/materials/scratch-wss-reply/MANIFEST_ja.md | コピー |
| stack-wss-reply／materials/probe-result.json | handoff-materials/2026-10-06-stack-backstage-handoff/materials/scratch-wss-reply/materials/probe-result.json | コピー |
| stack-wss-reply／materials/probe-subprotocol.mjs | handoff-materials/2026-10-06-stack-backstage-handoff/materials/scratch-wss-reply/materials/probe-subprotocol.mjs | コピー |
| stack-wss-reply／materials/reply_ja.md | handoff-materials/2026-10-02-home-wss-subprotocol/materials/scratch-reply_ja.md | 既存全文を再利用・一致確認 |

WSSの元probeは移管前のScratch内Bridge sourceを相対importする。元の再現用source identityは回答にある
`df34849d2502a498a06c5fe07a91d03e925124eb`、調査対象の公開b7.post2 sourceは
`f133fc95ed7b23109cc1908dc4f0dae066510258`。Stackの単独実行scriptとして扱わず、今回は再実行していない。

## 設定生成：対応済み

- 通常のホーム経路 `home-alpha-full@2`〜`@4` は共通deployment interfaceを使い、`schema_version: 1` を生成し、`release_identity` を設定JSONへ入れない。render時・配信結果のdoctor時ともに固定したScratch schemaを検査する。
- source: `src/mc_remote_stack/deployment_interface.py` の `prepare_interface_deployment`、`src/mc_remote_stack/scratch_contract.py`。回帰test: `tests/test_home_deployment_interface.py` の `test_home_post2_uses_the_published_contract_and_shared_target_generation`、`test_home_doctor_validates_the_served_runtime_against_the_locked_schema`（schema_version欠落／release_identity追加の両ケース）。
- 実装commit: `dece1a3`、提出head `ac2506a4d0d27a19943759d259056023f5da49a4`、[PR #61](https://github.com/Naohiro2g/mc-remote-stack/pull/61)は2026-10-02にmainへ統合済み（`cafb16bcd7636d19f321ab6164fdd21a46dfd599`）。現在のremote mainは `68b8d45af743cd56b70efe67a42e1e162b04c50c`。
- contract: source `f133fc95ed7b23109cc1908dc4f0dae066510258`、directory tree `ecb669a02ac6c8e502b44850e6dd28260c5adad4`、schema SHA-256 `4e1f8489dc6ea03800f5cf0fefd2f078fd6d71c8efda581f1711f68e384f99e4`。公開元GitHub APIのtreeとStackの固定値が一致。
- 今回のunit/deterministic確認: `uv run --no-sync --cache-dir /tmp/mc-remote-stack-confirmation-uv-cache pytest -q tests/test_deployment_interface.py tests/test_home_deployment_interface.py`、60件PASS、exit 0。sandbox内ではUDP socket生成が拒否され、同一suiteをsandbox外で再実行して全成功。製品の失敗ではない。
- 既存記録: `handoff-materials/2026-10-02-home-b7-post2-preparation/MANIFEST_ja.md`、`handoff-materials/2026-10-02-home-runtime-permissions/MANIFEST_ja.md`、ローカル `NOTES_ja.md` の10月2日該当節。実機dry-run・配信schema・apply／doctorの成功記録を保持している。
- この結論の対象は正式schemaを使う通常ホーム経路。元問い合わせにあった旧 `home-server@6`／`compose@14` の生成処理そのものを修正したという主張はしない。
- Scratch側の設定異常専用UIの当時の未対応は、Scratchの担当範囲。今回の受領確認で現行ScratchのUIを再検証していない。

## WSS検査：対応済み（実環境101の既存記録あり）

- 2026-10-02の回答を当日に受領し、検査要求へ `mcremote.bridge.probe.v1, mcremote.bridge.one-shot.v1` を追加済み。
- 直接Bridge検査: `handoff-materials/2026-10-02-home-wss-subprotocol/materials/probe-direct-bridge.js`。修正前401、修正後101・one-shot選択、exit 0は同directoryの `direct-before-fix.log`／`direct-after-fix.log` に記録。
- 外側WSS検査: 同directoryの `probe-wss.py`。TLS証明書を通常検証し、HTTP 101、Sec-WebSocket-Accept、responseの `mcremote.bridge.one-shot.v1` を確認。修正前401、修正後成功は `wss-before-fix.log`／`wss-after-fix.log` に記録。
- 当時のStack code／実機commitは `19c8afa68a3133addf82f308ab642d8ca4e51e15`。検査scriptと記録はGit管理外・未commitで、WSSの修正による製品codeのcommitはない。既存MANIFESTとローカルNOTESへ記録済み。
- 401解消のためのallowlist緩和・Bridge実装変更は不要だった。doctorへのWSS upgrade検査組込みは未実装だが、回答が求めた直接Bridge／外側WSS検査は完了している。公開手順 `docs/home-catering-guide_ja.md` はdoctorの検査範囲を明記している。
- [PR #62](https://github.com/Naohiro2g/mc-remote-stack/pull/62) と [PR #63](https://github.com/Naohiro2g/mc-remote-stack/pull/63) は現在未マージ。前者はホーム起動確認・WireScope配信、後者は標準plugin配置等の別残件であり、今回の受領を理由に統合しない。
- 今回は過去のsourceと結果を照合した。稼働環境へ再接続せず、pairing・ゲーム操作・現時点のサービス状態・b9 gate判定を主張しない。

## Scratch側の元資料の処理可否

| 元directory | Stackから返す処理可否 | 理由・終了条件 |
| --- | --- | --- |
| 2026-10-02-home-scratch-contract-reply | 削除可（受領結果をScratch側で確認後） | 全2fileをStackへ引取り・全文hash照合済み。設定生成は対応済み。今回の返却をScratchの②追跡へ反映した後、Scratch担当が処理できる |
| 2026-10-02-stack-wss-reply | 削除可（受領結果をScratch側で確認後） | 全4fileを引取りまたは既存全文参照として確保しhash照合済み。直接Bridge／外側WSSの101まで既存記録がある。返却をScratchの②追跡へ反映した後、Scratch担当が処理できる |

Scratch側で別の正本・evidenceから参照されている場合は、その参照の更新／引継ぎも確認してから処理する。
Stack担当は元資料を移動・削除していない。本packetはStack側②として保持し、引継ぎ先・参照identity・終了条件は親MANIFESTに記載。

knowledge正式着地: 今回なし。正式path／push済みknowledge SHAは該当なし。
human owner経由でこの票をScratch担当へ戻し、b9 close追跡へ受領と処理可否を反映してもらう。
Stack側で新しい横断仕様決定は行っていない。

## 必須確認・セッションクローズ

- uv sync --extra dev: PASS（20 packages解決、19 packages確認）。
- uv run pytest: 391件PASS、exit 0（391.29s）。実行commitは `a30aa8b1b230e88ed92c515b357a088d97ddb0da`。ローカルsocketを使うtestを含むためsandbox外で実行。commandには `/tmp` のuv cache指定を追加した。
- uv run ruff check .: PASS。
- repo／surface／branch: mc-remote-stack／Codex／agent/home-luckperms、commitは冒頭のSHA。
- 作業範囲／今回やったこと: 回答2件の全文受領・hash照合、現在の生成・検査sourceと既存結果の照合、元資料の処理可否を返却票へ収容。
- 変更ファイル: Git管理外の本packetとローカルNOTESのみ。追跡済み製品source・test・runbookの変更なし。
- 未完了／次の一手: human ownerからScratchへ受領票を戻し、Scratch側の②追跡・b9 close追跡へ反映。Stackの関連PR統合は別作業。
- 次に読むもの: 本受領票、received-inventory.json、既存2026-10-02-home-wss-subprotocol/MANIFEST_ja.md。
- 未着地の搬送物: 本受領票（外部送信・knowledge正式着地なし）。
- NOTES/DECISIONS: StackのローカルNOTESへ受領先を追記。新しいDECISIONなし。
- 注意点: 受領素材は正式evidenceではない。今回実機操作・Scratch元資料の削除なし。
