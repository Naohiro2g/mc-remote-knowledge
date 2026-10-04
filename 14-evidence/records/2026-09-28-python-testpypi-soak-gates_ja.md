# Python API TestPyPI soak：遷移ゲート①〜④の記録

> status: ①②③④は実施（④のWindowsを除く）。mature判定は未実施（human ownerが行う）。
> 2026-10-05: ④のWindowsは、b8のRelease wheelで入口ルートが成功した（[Windows入口の記録](2026-10-05-python-windows-entry_ja.md)、報告ベース）。

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

## Artifacts

「後から再現できない一次観測」（yankの状態、保持期限のあるrun log）だけを収録した。Python担当がsanitizeし（一時フォルダのパスを`<scratch>`へ置換、抜粋ログのBOMを除去）、coordinatorが全文を読んでSHA-256を照合した（2026-09-28）。run log全体、`manifest.json`（Releaseから再取得可）、dev側のMANIFESTは収録しない。

| file | 内容 | SHA-256 |
| --- | --- | --- |
| [dispatch-run-36357356599-publish-excerpt.log](../artifacts/2026-09-28-python-testpypi-soak-gates/dispatch-run-36357356599-publish-excerpt.log) | ①：mainからの再実行で2 fileとも`already exists, skipping` | `f01f76d83ea242b93d28546d730e35812f5801fd0b524558d0730a2bd2a9ca4a` |
| [g2-default-testpypi.log](../artifacts/2026-09-28-python-testpypi-soak-gates/g2-default-testpypi.log) | ②：TestPyPIから無指定で取ると`1214.10.2` | `bda8dbd5dd21df2e23644ceb279eab79efb206820f0bd0fe49ff6e62494f2428` |
| [g2-exact-unyanked.log](../artifacts/2026-09-28-python-testpypi-soak-gates/g2-exact-unyanked.log) | ②：unyank後、exact-pinは警告なしで取得 | `23ace346b37194626006b0349248578c2bfaa900931cb6d4067d75ec46159e41` |
| [g2-range-unyanked.log](../artifacts/2026-09-28-python-testpypi-soak-gates/g2-range-unyanked.log) | ②：unyank後、範囲指定でpost3に解決 | `5488447bc61b0972f9f0752929a778ca69b75f60736e813a897c6d63e4fb2f89` |
| [g2-yanked-exact-pin.log](../artifacts/2026-09-28-python-testpypi-soak-gates/g2-yanked-exact-pin.log) | ②：yank中、exact-pinは警告付きで取得 | `7c2533d5ad462b6eba66088681037a47513b730b2dd9477b6d2183853515eb8c` |
| [g2-yanked-range-prerelease.log](../artifacts/2026-09-28-python-testpypi-soak-gates/g2-yanked-range-prerelease.log) | ②：yank中、範囲指定＋`--prerelease allow`で解決に失敗 | `9b7d3cbb8b22e3b5d46b3acd02701ca5fd8d292b05c305b251635dccf50a8cf0` |
| [testpypi-simple-post3-unyanked-2026-09-28T0807JST.json](../artifacts/2026-09-28-python-testpypi-soak-gates/testpypi-simple-post3-unyanked-2026-09-28T0807JST.json) | ②：unyank後のsimple index（serial `8372336`） | `f5b1127c321c622fd426315b410682cf6404e51cf47fc0d423eaa12209e8c640` |
| [testpypi-simple-post3-yanked-2026-09-28T0803JST.json](../artifacts/2026-09-28-python-testpypi-soak-gates/testpypi-simple-post3-yanked-2026-09-28T0803JST.json) | ②：yank中のsimple index（該当file分の抜粋） | `01ed05786d4758a678f50e14f1810f7835125e4a6b4385998267a050872dcd19` |

`g2-yanked-exact-pin.log`には、このときの必須依存`pygame-ce`が現れる（`2026-09-28-02`でb8に外す前の状態）。

## non-claim

- PyPI.orgへのpublishはしていない。
- mature判定はしていない。
- Windowsでは検証していない。
- ②のhuman観察は報告ベースで、transcriptと時刻を持たない。
- 「コードはpost2と同一」はPython担当の報告で、coordinatorは照合していない。
