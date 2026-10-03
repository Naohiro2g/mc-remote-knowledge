# Python後続への引継ぎ — b8 closeからb9

- 種別: ②後続sliceへの引継ぎ素材。実装の着手票ではない。
- knowledge: `2a8c3eae4e489e67f044111b0d1e6cdd22ead86a`。b8 CLOSED、hub NOTESの移管／Windows／READMEの残件を参照。
- Python公開起点: `main`／`v2320.0.0b8` → `52d35f5304e62f465c1f47ab47c00fe9bcf62470`。protocol `23.2.0`。
- 引継ぎ先: Python b9 tooling移管担当＋knowledge coordinator。Windows実機はhuman owner。

## fixtureと同梱WireScope

- B8 consumerの正本fileはPython `tests/fixtures/entity-particle-v23.2.json`と`.source.json`、使用箇所は`tests/test_b8_fixture.py`。発行元はScratch `mc-remote/protocol/test/fixtures/entity-particle-v23.2.json`、source `054a3af017f1abb8cc01cf85b3bc83181e648e19`、36,481 bytes、111 cases、SHA-256 `ca636b4a2685ea67f24d8e7931e3d30a84e7cec872bb5c5d2eadd178cdac39f2`。JSONはowner発行のexact bytesを取り込み、source sidecarとconsumerのidentity assertionを同時更新する。
- Python同梱WireScopeはScratch `df34849d2502a498a06c5fe07a91d03e925124eb`の`mc-remote/live`から再生成したもの。ZIP 83,746 bytes／`4cb349894b71d61d7ca143d8362a5b79deb1810e1d7a9e31ad30e29bfe370a07`、manifest 2,321 bytes／`45d56d5012c2c0b21631597e160363d93bcf3e736b74cc0b8a1041afc8101413`。Scratch公開source `691576f`へPythonのpinを黙って変更しない。
- 移管時に点検するScratch直参照: `tests/fixtures/entity-particle-v23.2.source.json`、`display-alias-v1.source.json`、`station-attach-v1.source.json`、`mc_remote/_wirescope_artifact.py`の`SOURCE_REPOSITORY`、`pyproject.toml`のWireScope Source、`scripts/check_wirescope_wheel.py`のsource URL／artifact digest。これは自repoの参照一覧であり、Scratch repoへの変更ではない。
- `.github/workflows/ci.yml`は同梱manifestのsource commitを読み、CI release manifestの`bundled_wirescope_source_commit`へ投影する。b9で所有先が変わる場合も、取り込んだartifactの実際のsource commitを記録する。
- 次の一手: coordinatorからowner／repo／fixture発行方式／同梱appの生成元を受領してから上記の取得元・source metadata・hash・source URL／licenseを揃えて変更し、対象consumerとwheel同梱検査を行う。b8の公開物を再生成・差し替えない。

## sound surfaceの局所決定

- 原票: `handoff-materials/2026-10-01-b8-python-successor/materials/sound-surface-handoff_ja.md`。
- `playSound`／`playBlockSound`のvolume／pitch／note／receiverはkeyword-only。数値引数の既定Noneはwire field省略、receiver既定world。pitchとnoteの両指定はValueError。両方なしはserver既定を保持し、0は省略しない。音名換算はユーザーコード。
- 次の一手: knowledge `12-python-client/`とsound notesへの説明の着地をcoordinatorに確認し、移管後も同じsurfaceを維持する。wire契約にPython固有のNone規則を混ぜない。

## Windowsと利用者向け文書

- human ownerの入口ルート試験: tracked `docs/windows-b8-entry_ja.md`。クリーンWindows 11でGitなし、uv導入→Python3.13でinit→公開wheel URLでadd→import→JupyterLab add→起動。公開wheel URLは `https://github.com/Naohiro2g/minecraft-remote-api/releases/download/v2320.0.0b8/minecraft_remote_api-2320.0.0b8-py3-none-any.whl`。
- wheel 195,068 bytes、SHA-256 `dcedff010feac0d5df24ff85dd84b321fb819f78563c39431ac32d9d75bc0180`。匿名取得で同一digestは確認済み。Windows実機PASSはまだ受領していない。
- 次の一手: human ownerの結果を受領し、失敗した手順・Windows／uv版・Gitなしの前提を記録する。通らない場合は通常ルート（Git for Windows）へ進む。b9のPyPI登録判断材料としてcoordinatorへ返す。
- README残件はhub NOTESの2026-08-28 priorityに従う。starter READMEの旧記述、更新／rollback導線、Windows、cold-reader確認が残る。3D graphのデモ効果の改善は観測として残し、今回のcloseでsampleを変更しない。
