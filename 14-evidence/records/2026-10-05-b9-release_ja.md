# b9の移管、公開、gate closeの素材（2026-10-05）

> test class: `unit/deterministic`（artifactの照合、OCIの比較）と公開identityの照合。b9横断release gate（`00-hub/release-gate-notes_ja.md`の
> 2026-10-04の節）のclose分類（`00-hub/b9-gate-close-instructions_ja.md`）で、各担当が①とした素材を収容した。公開identityの要約と
> coordinatorの照合はgateの節にある。この記録は素材の置き場所と、収容のときに変えたものを示す。

## 収容した素材

| 収容先（`14-evidence/artifacts/`） | 中身 | 搬送元 |
| --- | --- | --- |
| `2026-10-05-b9-tooling-migration/scratch/` | 移管の前後の照合、追加fixtureの発行、consumerのpin、CI log。`initial-confirmation/`は10/4の確認票と移管評価の別紙 | scratch-editor `2026-10-05-b9-tooling-migration`、`2026-10-04-b9-scratch-confirmation` |
| `2026-10-05-b9-release/scratch/` | 公開前の停止（OCIのversionラベル、COPY layerのmtime）、原因の調査、公開したOCIと凍結したOCIの比較、toolingとScratchの公開操作。`close/`はclose分類票 | scratch-editor `2026-10-05-b9-release`、`2026-10-05-b9-close` |
| `2026-10-05-b9-mcremote-release/` | 公開前の凍結JARとの照合、tagのCI、公開assetとmanifest、API snapshot | McRemote `2026-10-05-b9-mcremote-release` |
| `2026-10-05-b9-mcremote-close/` | close分類票、収容済み素材の全文照合 | McRemote `2026-10-05-b9-mcremote-close` |
| `2026-10-05-b9-python-release/` | PyPI.orgへの初公開：公開の許可、tagのCI、GitHub Release、PyPI.orgとTestPyPI、新しいuv環境での取得 | minecraft-remote-api `2026-10-05-b9-python-release` |
| `2026-10-05-b9-python-close/` | close分類票、収容済み素材の全文照合 | minecraft-remote-api `2026-10-05-b9-python-close` |
| `2026-10-05-b9-dev-live/scratch/segment-3/materials/` | 画面のPNG 4枚（pickerの検索、WireScopeの全体と列幅） | scratch-editor `2026-10-05-b9-scratch-dev` |
| `2026-10-03-b8-dev-live/scratch/` | b8から残していたもののうちb9で用が済んだもの：pickerの名前表示と検索の初期観測、ローカル試運転、WireScopeの列幅の元観測 | scratch-editor `2026-09-30-block-picker-names`、`2026-10-01-b8-local-playtest`、`2026-10-03-wirescope-column-width` |

Scratchの151 fileは、搬送元の一覧（`2026-10-05-b9-release/scratch/close/materials/EVIDENCE_FILES.tsv`）のbytesとSHA-256で照合してから
収容した（不一致0）。

## 収容のときに変えたもの、収容しなかったもの

- home directoryのpathを`~`へ置き換えた: `2026-10-03-b8-dev-live/scratch/2026-09-30-block-picker-names/materials/browser-smoke.log`と、
  `2026-10-03-b8-dev-live/scratch/2026-10-03-wirescope-column-width/materials/`の`artifact-build.log`、`build.log`、`test.log`。
  この4 fileは搬送元の一覧のdigestと一致しない
- 収容しなかった: McRemoteの公開素材にあったJARの複製2つ（公開assetと同じ261,016 bytes／`4feb90db…a58e`）、`__pycache__`。
  Scratchが③とした大きなarchive（candidate ZIP、公開前build、Release assetの複製）
- 点検: token、pairing_id、private address、player UUIDの値は見つからなかった。CI logにあるUUIDはGitHub Actionsのworker、一時
  directory、artifactのblobの識別子

## 照合の要点

- 収容済みの素材は、3担当とも全文とSHA-256が収容先と一致した（McRemote 19 file、うち2 fileはpathの置き換えだけ、Python 12 file、
  Scratch 18 file）
- Scratchのb8の公開物の残り2 file（`contracts.tar.gz`、`wirescope-app.zip`）は、公開b8のRelease assetと一致した（③）
