# b9契約修正・tooling移管：確定搬送素材

- handoff ID: `2026-10-05-b9-tooling-migration`
- 依頼: knowledge `00-hub/b9-gate-work-instructions_ja.md`
- knowledge contract commit: `900f6f4b8027d265a62ba7f139d4f3b1bbe78100`
- Scratch source: `7fbbf034488760d8fc7e034bf23f3e08e6e1807d`（develop／agent/b9-tooling、push済み）
- 新owner source: `minecraft-remote-tooling@dc1ab834183e29f2eb03059b07e99d2b463776ee`（main、push済み）
- 現在地: 実装・CI・candidate生成・最終candidateの実体照合まで実施済み。
- 正式evidence配置案: `14-evidence/artifacts/2026-10-05-b9-tooling-migration/scratch/`
- authoring境界: このdirectoryはdev側の素材。knowledge担当がrecord／配置／INDEXを確定する。

## 入口

- `materials/CONFIRMATION_ja.md`: 確認票形式の返却本文
- `materials/NEW_FIXTURE_ja.md`: 新fixtureの発行identity、schema／caseの適用範囲
- `materials/FIXTURE_IDENTITIES_ja.md`: 新ownerの13 fixture一覧
- `materials/source-move-comparison.json`: 機能修正後・移管前sourceと新ownerのfile比較
- `materials/wirescope-final-asset-comparison.json`: WireScope ZIP内6 assetのbyte一致
- `materials/tooling-lock.json`: Scratchの固定consumer入力
- `materials/consumer-source-identity.json`: exact source、固定URL、旧owner source撤去の確認
- `materials/tooling-*.json`: 新ownerの設定readbackとActions／artifact identity
- `materials/scratch-*.json`: 最終Scratch CI／candidate／artifactのidentityと照合結果
- `materials/verify-candidate.py`: ダウンロード済みcandidateの再検証。outer／inner file hash、owner pin、OCI source／version／amd64・arm64、GUI configを検査
- `materials/logs/`: unit／build／lint／CIログ。手元の絶対pathを`~`へ置換。修正前のFAILログも保持
- `materials/before-migration/`: 純粋な移管比較の起点になるWireScope ZIPとdetached manifest（source c7505c）

## 保持と境界

全fileのbytesとSHA-256は同directoryの`SHA256SUMS`／`INVENTORY.json`へ記した。generated cacheは `mc-remote/tooling/` にありGit管理外。candidateの元archiveはActions run／artifact IDで取得でき、`artifacts/scratch-candidate-7fbbf03448.zip`として手元にも保持する。大きなarchiveの正式収容はknowledge担当の分類による。

公開repoへこの素材をstage／commit／pushしない。shared環境変更、人間参加試験、他consumerの編集、tag／Release／registry公開はしていない。protocol `23.2.0`、learner APIの追加なし。
