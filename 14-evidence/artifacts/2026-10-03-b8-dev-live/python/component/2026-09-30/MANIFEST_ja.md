> 2026-10-01更新: 現candidateは`52d35f5304e62f465c1f47ab47c00fe9bcf62470`。このdirectoryは旧fc6c700の履歴素材。現返却は`handoff-materials/2026-10-01-b8-python-successor/MANIFEST_ja.md`。旧artifactを現gate inputに使わない。

# B8 Python component candidate

正式release evidenceではなく、candidateの搬送・再開用素材です。Git管理外。

- repo: minecraft-remote-api
- branch/commit: `codex/b8-python-entity-particle@fc6c700b1588a1d052499314f47e8e7e5b06ae27`（commit/push済、GitHub API照合済）
- knowledge contract commit: `16668c5e5152d593c4b184939c9a9e723529d6e9`
- contract: wire §5.0.2／§5.8.3、DEC `2026-09-28-01/02`、`2026-09-30-01/02/06`
- 現在の返却: [candidate追記](materials/candidate-addendum_ja.md)
- 履歴: [初期実装票](materials/return_ja.md)（fc208b8b・442件・未commit時点。現在値として使わない）
- CI artifact: `materials/ci-36718297434/`（run `36718297434`全job成功、artifact `11097400766`、manifest照合済み。返却する主identity）
- local artifact: `materials/candidate-fc6c700/`（clean commit archiveからPEP 517 build、先行buildとbyte-for-byte一致）
- 同梱WireScope: Scratch `5aaa9c59acc393cd0a0de5cb45a5e619a5e87abe`
- fixture: Scratch `0735a9c957d069f719bee9c91e8be0f9322f4920`、59 cases／Python投影54 test
- 残件: Scratch successor fixture／WireScope発行→Python取り込み。Windows実機、補完表示、shared/live-humanはcoordinatorが別票で進める。移管はb9。
- 後続owner: Python担当。successor取り込みでcandidate identityが変われば旧identityをcoordinatorへ差し戻す。
