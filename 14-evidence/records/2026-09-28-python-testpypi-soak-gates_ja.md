# Python API TestPyPI soak：遷移ゲート①〜④の記録

> status: ①②③④は実施（④のWindowsを除く）。mature判定は未実施（human ownerが行う）。

## Record

- test ID: `2026-09-28-python-testpypi-soak-gates`
- test class: `unit/deterministic` + `live-auto`（①④、agent）＋ `live-human`（②、報告ベース）
- observed date: `2026-09-26`〜`2026-09-28` JST
- result: ①②③④ **PASS**（Windows未検証）
- artifact: minecraft-remote-api `2301.0.0b7.post3`（tag `v2301.0.0b7.post3`→`1ea043b`、annotated）
- decisions: `2026-06-25-04`（遷移ゲート）、`2026-09-26-03`、`2026-09-27-01`、`2026-09-27-05`
- 指示: `12-python-client/pypi-soak-uv-readme-instructions_ja.md`
- 出典: Python担当の確定搬送票（2026-09-28、`main@c213674`）

## 公開identity

| 面 | identity |
| --- | --- |
| wheel | `minecraft_remote_api-2301.0.0b7.post3-py3-none-any.whl`、184,468 bytes、SHA-256 `76e56f9eacbddcdee0c7a5558d7a941f2c735f48c93866de955a3ad03b55fc62` |
| sdist | `minecraft_remote_api-2301.0.0b7.post3.tar.gz`、178,281 bytes、SHA-256 `c883b2764698a0035cc0fe3f4bec0a381af29ed9f3639da5265277209e8dec0b` |
| GitHub Release | 「minecraft-remote-api 2301.0.0b7.post3」、prerelease、`manifest.json`添付 |
| TestPyPI | https://test.pypi.org/project/minecraft-remote-api/2301.0.0b7.post3/ |

coordinatorはRelease assetとTestPyPIのdigestが一致することを2026-09-28に照合した。

## 遷移ゲート

1. **再現可能なpublish**：固定trigger run `36283409414`でpromoteとpublish-testpypiがsuccess。mainからworkflow_dispatchでpublishだけを再実行したrun `36357356599`では、2 fileとも`already exists, skipping`で、upload-timeは変わらなかった。runbookは`PUBLISHING.md` §1〜§4。
2. **soak／yankの1サイクル**：humanがTestPyPIからexact-pinで入れたpost3で、sb-beta.mc-remote.comへのhello.pyとpairingに成功し、yank／unyankを複数回操作した（報告ベース。transcriptと時刻はない）。agentの観測（2026-09-28）：yank中は範囲指定と`--prerelease allow`で解決に失敗し、exact-pinは警告付きで取得できた。unyank後（08:07 JST、simple index serial `8372336`）は範囲指定でpost3に解決し、exact-pinは警告なしで取得できた。TestPyPIから無指定で取ると`1214.10.2`になった。
3. **退避手順**：`PUBLISHING.md` §5.3（yankでも版番号は消費されたまま、`==`なら取得可、出し直しは`.postN`、確認は範囲指定と`--prerelease allow`）。TestPyPIの2FAは確認済み（2026-09-26）。ownerは`nao2g`の1名で、2人目のmaintainerはいない（human owner記入、2026-09-28）。
4. **利用目的ごとのexact-pin**：学習者はRelease wheel URLと`--dev jupyterlab`（agentがLinux、humanがUbuntuで確認）。beta testerはTestPyPIのindex設定（explicitとsources、依存はPyPI.orgから取得、agentとhumanが確認）。OSS開発者はtagをclone→`uv sync --frozen`→pytest 253/253。PyPI.orgの無指定取得は`1214.10.13`のまま（2026-09-26、2026-09-28）。**未検証**：Windows（クリーンインストール直後からの手順とあわせて検証する予定）。

## non-claim

- PyPI.orgへのpublishはしていない。
- mature判定はしていない。
- Windowsでは検証していない。
- ②のhuman観察は報告ベースで、transcriptと時刻を持たない。
- 「コードはpost2と同一」はPython担当の報告で、coordinatorは照合していない。
