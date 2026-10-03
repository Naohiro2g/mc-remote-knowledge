# B8 Python successor candidate

正式release evidenceではなく、coordinatorへの追記と再開のための素材。Git管理外。

- repo: minecraft-remote-api
- branch/commit: `codex/b8-python-entity-particle@52d35f5304e62f465c1f47ab47c00fe9bcf62470`（push済、GitHub branch API一致）
- knowledge contract commit: `fd29db757c07f993155842ecc88b1c39558611a9`（gateとwireを実際に読んだ）
- runtime／sound surface参照: `4f0b46f27a1f1e31a47b7a1f9aa79254e3b153a6`（sound notes §3.3、wireはfd29db7とbyte-for-byte同一）
- change cone: Pythonサウンドのkeyword-only引数／None省略／pitch-note排他、shared fixture successor取り込み、coordinator指定同梱WireScopeの再生成・pin更新。
- source: Scratch `df34849d2502a498a06c5fe07a91d03e925124eb`。`/tmp/mcr-b8-source`はread-onlyな使い捨てclone、pushurl無効。WireScopeだけをbuild。Scratch実装は変更しない。
- fixture source: Scratch `054a3af017f1abb8cc01cf85b3bc83181e648e19`。111 cases、36,481 bytes、SHA-256 `ca636b4a2685ea67f24d8e7931e3d30a84e7cec872bb5c5d2eadd178cdac39f2`。
- CI: https://github.com/Naohiro2g/minecraft-remote-api/actions/runs/36860299749 （Python3.10〜3.13／build-candidate全job success）
- [返却追記・close票](materials/return_ja.md)
- [Python surfaceの局所決定](materials/sound-surface-handoff_ja.md)
- 素材: `materials/mcr-b8-df34849-build.log`、`materials/mcr-b8-df34849-test.log`、`materials/mcr-b8-successor-python-snapshot.json`（79frame、共通appのproduction validator受理）。
- 後続owner: knowledge coordinatorがgateへ反映・exact setを凍結し、live実施票を発行する。Python担当は追加修正依頼を受けて対応。
- 旧fc6c700 artifactsは現candidate入力として使わない。2026-09-30 handoff directoryは変更履歴の参照用。b8 release close時に現materialsを正式記録へ昇格／後続移管／非参照失効のいずれかに整理する。
