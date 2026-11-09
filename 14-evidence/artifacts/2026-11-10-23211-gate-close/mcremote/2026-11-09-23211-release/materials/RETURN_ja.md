# McRemote 2321.1 公開の返却

**McRemote 2321.1.0をstable・Latestで公開し、公開した5 assetの実物とmanifestを照合した。すべてPASS。**
公開日時：2026-11-09 05:26:59 JST。横断gateの判定と、他component／Stackの作業はcoordinatorの進行による。

## 共通の返却

- 実際に読んだknowledge commit：`2f337180c919a80aa80200e9f9d959d64812543e`。remote mainと一致を確認し、runtime、INDEX、
  `00-hub/23211-gate-release-instructions_ja.md`の共通／McRemote、gate notesのset-2と人間の試験の判断を読んだ
- human ownerの着手許可：2026-11-09「これで進めてください」
- 検証記録の追加指示：同日「凍結JARで1.21.11だけ自動確認を追加して」。この指示に従い、1.21.11の添付を新しい実測記録へ替えた。
  候補のsourceとJARは変えていない。26.3は#244での既存記録をそのまま使った
- exact set：`2321.1-set-2`。McRemoteのsource：`feat/coordinate-time-hud@5b78ded96d1ad6d45160b67c5f8a13e14adb3fc8`
- 既定branchの新しい先頭：`main@5b78ded96d1ad6d45160b67c5f8a13e14adb3fc8`。旧`77b77c61235ba80f335d141e236126bbe8faad90`からfast-forwardしてpush。
  追加の製品commitは作成していない
- tagが指すSHA：annotated tag `v2321.1.0` → `5b78ded96d1ad6d45160b67c5f8a13e14adb3fc8`。
  annotated tag objectは`57fc4fec5e03835d7d53b27d67dfd773f1ba1127`。GitHubのAPIでmainとtag objectの参照先を確認した
- Release URL：<https://github.com/Naohiro2g/McRemote/releases/tag/v2321.1.0>
- Release ID：`438498551`、title：`McRemote 2321.1.0 (Minecraft 1.21.11, 26.3)`
- 公開状態：`prerelease=false`、`draft=false`、Latest。GitHub APIの`releases/latest`でも`v2321.1.0`を確認
- 旧`v2321.0.0`のtagとReleaseは保持。旧Release ID `430007998`が公開されたまま存在し、Latestは新しい版へ移った
- 共通の返却に求められたrun ID／Runner Image、assetのbytes／SHA-256と照合結果は次の表のとおり

## runとRunner Image

| 用途 | run ID | job ID | 結果 | Runner Image | 版 |
| --- | --- | --- | --- | --- | --- |
| 凍結候補の生成 | [42291740554](https://github.com/Naohiro2g/McRemote/actions/runs/42291740554) | 128147688359（build-only） | success | ubuntu-24.04 | 20261101.360.1 |
| tagのCI | [42519567217](https://github.com/Naohiro2g/McRemote/actions/runs/42519567217) | 128850384204（build-only） | 全7 jobs success | ubuntu-24.04 | 20261101.360.1 |
| 公開前dry-run | [42519953779](https://github.com/Naohiro2g/McRemote/actions/runs/42519953779) | 128851057451（promote） | success | ubuntu-24.04 | 20261101.360.1 |
| 公開・添付 | [42520172238](https://github.com/Naohiro2g/McRemote/actions/runs/42520172238) | 128851734383（promote） | success | ubuntu-24.04 | 20261101.360.1 |

各jobの実logの「Runner Image」を読んだ。抜粋は`validation/`の`*-runner-image.log`。
タグCIの3 OS × Java 21／25のcredentialの6 jobsもすべてsuccess。[tag-ci-jobs.json](tag-ci-jobs.json)

凍結候補artifact `13540651077`のZIPは317,670 bytes、
`9dd6d88106b3415f96cd51c34064d39bbda362411390594462ab3644eb140803`。
公開workflowは既存の手順どおりtag CIのartifact `13633241102`から昇格した。このZIPは317,670 bytes、
`9179051e38783f9f66e57afe3048285e8f98a16c0363651a7647bcf9efdb65de`。
ZIP外側のdigestは異なるが、**JARと宣言の中身が凍結候補と同じbytes**であることを公開前に確認した。
[source／実物の比較](tag-ci-comparison.json)。公開workflow自身はJARを再buildしていない。

## 公開assetの照合

公開後、全5 fileをGitHub Releaseからダウンロードし、準備したfileとのbytes一致、providerのdigest、manifestのSchemaと参照内容を検証した。

| file | bytes | SHA-256 | 凍結値／添付予定値との照合 |
| --- | ---: | --- | --- |
| `manifest.json` | 2,063 | `994e4a7d210ba329c9b9e538a2f636756f07cb0865b736fe96ab51432d865389` | 一致 |
| `mc-remote-2321.1.0.jar` | 340,193 | `cd1fff723b2b8349f45184b940cd5da1ca3cdcacc9bad988fa71cd00ea960112` | 一致 |
| `mc-remote-verification-1.21.11.json` | 63,279 | `45c0b5e6d7254a83d820ed7702ad3e67a1540f1d1c7a4ea1dc1aef4ce6c550e1` | 一致 |
| `mc-remote-verification-26.3.json` | 63,801 | `9c3492739c8088d413f8d3aafad0b733d732db3a1c159363a0e5eb4d5c72b1b5` | 一致 |
| `minecraft-targets.json` | 126 | `8e830732decd6bcde13f91eb6c071d062ba6993342a7edb52e6ea543b9e0c361` | 一致 |

- JAR：凍結値340,193 bytes／`cd1fff723b2b8349f45184b940cd5da1ca3cdcacc9bad988fa71cd00ea960112`と全桁一致
- 宣言：凍結CI artifact、source、JAR内の`minecraft-targets.json`と同じbytes
- verification：下記の実測した記録と同じbytes
- manifest：既存の固定Schema／semantic／reference content検証にPASS。公開前のローカル生成物、dry-run、公開物も同じbytes
- 公開本文：human ownerの原稿を基に、指示の「統合版ではFで切り替えられない」、APIと通信は2321.0.0と同じこと、feedbackの入口を追加。
  protocolは23.2.1のまま。公開workflowが末尾の改行を1つ加えた以外は準備済み本文と同じで、本文の内容に差は無い

[公開assetの実物照合](public-assets-verification.json)、[Release／LatestのAPI記録](public-release-metadata.json)、
[main／tagのAPI記録](published-git-identity.json)、[公開本文の準備済みfile](release-body_ja.md)

## 添付した検証記録の実測対象

両対象とも、実際に使用したMcRemoteは凍結source `5b78ded96d1ad6d45160b67c5f8a13e14adb3fc8`、JAR SHA-256
`cd1fff723b2b8349f45184b940cd5da1ca3cdcacc9bad988fa71cd00ea960112`。

| 対象 | Paper JARのbytes／SHA-256 | Java | 自動確認 |
| --- | --- | --- | --- |
| 1.21.11 #132（2026-11-09に追加） | 54,846,016／`5ffef465eeeb5f2a3c23a24419d97c51afd7dbb4923ff42df9a3f58bba1ccfba` | Temurin 21.0.13+9 | 通常8／再起動後4 groups、両回lifecycle・正常終了、欠落toggle_on_swap補完PASS |
| 26.3 #244（2026-11-07の実測を維持） | 55,279,049／`9601f9a26a2a52a0f2c807cf1abf691f96ee4fb287878313b601cebc2c51eabf` | Temurin 25.0.5+8 | 通常8／再起動後4 groups、両回lifecycle・正常終了、欠落toggle_on_swap補完PASS |

今回の1.21.11追加は新規の隔離world、合成credential、認証有効、LuckPermsなしで実行。看板の表裏、named／hex色、装飾、1行更新もPASS。
両回の起動logはERROR／FATAL 0件、exit 0。終了後の試験ポート解放も確認。
記録と再現recipeは[verification-1.21.11/](verification-1.21.11/)、統合記録は
[mc-remote-verification-1.21.11.json](verification-1.21.11/mc-remote-verification-1.21.11.json)。
旧db7f7dbの観測原本は元packetに保持し、今回のJARの測定として付け替えていない。

今回の追加試験はlive-autoで、人間の画面／Fキーの試験は再実施していない。人間の合格報告は実読knowledgeのgate notesのとおり。
公開VPSの更新、Stackのpreset、他componentの公開、横断gateのcloseは今回の操作に含めていない。

## 保持と戻り先

- mainへ統合済み。feature branchは同じ凍結sourceのまま保持。rootのユーザー所有の未追跡`mise.toml`は変更していない
- 次はcoordinatorがこの返却を照合し、他component／Stack／closeを進行する
- 本packetは分類②としてMcRemote担当で保持。knowledgeの必要な観測の収容と照合、gate close分類と必要な移管が済み、参照用途が終われば整理できる
- raw runtime／合成credentialはローカル限定。素材は正式な14-evidenceではなく搬送用で、正式記録の配置はknowledge側で行う
