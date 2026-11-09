# Scratch 2321.1.0 公開の返却

- 実際に読んだknowledge commit：`2f337180c919a80aa80200e9f9d959d64812543e`（remote main）。
- knowledge contract path：`00-hub/23211-gate-release-instructions_ja.md`の「共通」「Scratch editor」。最新runtimeとgate notesの人間試験の判断も実読。
- coordinator確認済み本文に対するhuman ownerの2026-11-09の指示を受領。「Minecraft 1.21.11・26.2・26.3の公式の日本語・英語カテゴリ名に対応しています。」を「Minecraftの公式の日本語・英語のカテゴリ名に対応しています。」へ1回だけ置換して開始した。

## 公開先・branch・tag

- Release：[mc-remote Scratch 2321.1.0](https://github.com/Naohiro2g/scratch-editor/releases/tag/v2321.1.0)、ID `438573011`。
- 公開時刻：`2026-11-08T22:44:58Z`（JST 2026-11-09 07:44:58）。
- `draft=false`、`prerelease=false`、**Latest**。`releases/latest`のIDも同じことを確認。
- 既定branch：`develop`。公開後の先頭は**`57fb7691bb5d9a5895785b200ae78734240ebfa6`**。開始時点で既に凍結sourceと同じ先頭だったため、branchの移動はしていない。公開直前・直後・返却前に同SHAを確認。
- tag：**`v2321.1.0` → `57fb7691bb5d9a5895785b200ae78734240ebfa6`**。
- annotated tag object：`1b62f8b0eddd62dad007b00f5a6979e89fd83174`。Git refのtypeはtagで、commitへの参照とtagからの解決結果を照合。
- `v2321.0.0`のtagとReleaseは保持。旧tag targetは`ffb496ed50d751d307f685f2ae555c94c893fae5`のまま、Release IDも変更なし。

## runとRunner Image

- 生成run：[42350684690](https://github.com/Naohiro2g/scratch-editor/actions/runs/42350684690)（success）、head_sha `57fb7691bb5d9a5895785b200ae78734240ebfa6`。
- job `128337960170`、Runner Image **`ubuntu-24.04` / `20261101.360.1`**。
- 凍結artifact：`13565862576`、digest `sha256:47a4f4601dbec0c2e8fc58d9359f69290fda4c1f4f2f58bb387e73590a172050`。
- 今回の公開は指示どおり手動昇格で、新しい公開用build runは無い。生成済みのfileとOCIを使い、新しいビルドはしていない。

## Release assetと凍結値の照合

| file | bytes | SHA-256 | 照合結果 |
| --- | ---: | --- | --- |
| `contracts.tar.gz` | 1,908 | `48948ba47d55409f02a8ff8e0d44021b07859e11ffa5ca0f8598e6ef06082390` | 候補からそのまま一致 |
| `manifest.json` | 2,093 | `bd66f04446bdd37f221dba52df968d4d04e74886b9d6eddc59bf7e0be49171e6` | 公開形式へ変換・schema検証済み |
| `mc-remote-scratch-LAN-2321.1.0-linux-x64.zip` | 272,115,968 | `52f1f4b3eff59cec44c634c8974d5b41cfb18ee873d1348021e7e1831a2cbe42` | 候補からそのまま一致 |
| `mc-remote-scratch-LAN-2321.1.0-macos-arm64.zip` | 266,859,915 | `d9bb5976f62ad5043130c911551f23b0f4b127a5f0a80a6465ff8cd7decb768e` | 候補からそのまま一致 |
| `mc-remote-scratch-LAN-2321.1.0-windows-x64.zip` | 262,508,252 | `8edf5c1890df3550b3d4ffdd8d39dfbc1cbd35509531266ebd5e80103cab7ad6` | 候補からそのまま一致 |
| `scratch-gui.tar.gz` | 139,262,746 | `0f0b2597a8694863fb264340c1b3b89685849c85ce7c32e9f4b210e645fbdff8` | 候補からそのまま一致 |
| `wirescope-app.manifest.json` | 2,339 | `3dd668a236463809a4cdc6d19375f3e6d75eea0c8089a616d2b761d3a4a05235` | 候補からそのまま一致 |
| `wirescope-app.zip` | 83,854 | `da3da0b6cf4d05265bc0c11abaa4913208c7cfc3600b0c3e78c93a356fc431ad` | 候補からそのまま一致 |

凍結Actions archive全体と全13 fileを公開前に再hashし、一致を確認した。7つの既存fileを同じbytesで添付し、manifestだけを既存の公開用生成器で作った。8 assetすべてについて、公開前のdraftと公開後のGitHub serverの`size`／`digest`を照合し、上の値と一致した。manifestは公開URLからも取り直し、bytes／SHA-256と内容の一致を確認。大容量assetの公開後の照合はserver digestによるもので、全件をHTTPで再ダウンロードした結果とは区別する。

## OCI

- 公開tag：`ghcr.io/naohiro2g/mc-remote-scratch:v2321.1.0`。
- 公開後index digest：**`sha256:f3bcf6a6e9ae939e8a8781628ad1e9b40507286da34224f91dfba711a4920c67`**。凍結値と一致。
- 凍結入力`scratch.oci.tar`：326,605,824 bytes、SHA-256 `c1dc8dc79a4e7dd351af728aa5e80677ce3aa08a84f8a4583dc9b4d9d84d7e10`。
- archiveをローカルOCI layoutへimportした時点でもdigestを照合し、`regctl image copy --force-recursive`で全platform・attestationを含めてそのまま転送した。転送後とRelease公開後にもregistry側のdigestが一致。
- versionラベルは凍結物の`v2321.1.0`、revisionは57fb769。mtimeも凍結archiveのまま保持。追加の時刻正規化やラベル変更はしていない（凍結時の全ファイルを共通epochへ揃え直したという意味ではない）。
- Bridgeは既存の`ghcr.io/naohiro2g/mc-remote-bridge` index `sha256:305d6e38b36e195a0e158522f32f3a8c45d39da2aeec7b7e46f785c920406acf`を再利用し、registry上でも一致を確認。toolingの新しいtag／Release／buildは行っていない。
- 転送tool：公式regctl v0.11.7、binary SHA-256 `3737fbbdd791e04e7a831640b681f3397a376498e80e2ad9b1b2d27296f239bc`を公開元digestと照合してから使用。

## manifestの候補からの差分

- 入力のcandidate manifest：2,664 bytes、SHA-256 `19aec7258f726f11ce497783b0e3c9b97f39be4fc4d8ccd7f25cfdc084061d47`。
- 公開manifest：**2,093 bytes、SHA-256 `bd66f04446bdd37f221dba52df968d4d04e74886b9d6eddc59bf7e0be49171e6`**。
- 既存`build-mcremote-release-manifest.mjs`で生成し、固定している公開manifest contractでschema／semanticsを検証した。
- `schema`はcandidateからreleaseへ、`schema_version`は1から2へ、`version`は`release_tag: v2321.1.0`へ変換。
- 候補の`source.commit`を公開の`source_commit`へ変換。値は57fb769の全桁SHAで同じ。`source.repository`と候補用の`tooling`記録は公開schemaに収録しない。
- OCIはarchiveのfile／bytes／SHAではなく、registry locatorと同じindex digestで記録する。通常fileのkindはfile→https-fileに変わり、bytes／SHAは不変。
- 既存の公開生成器に従いartifactは9→8項目。`scratch-gui.tar.gz`のroleは公開manifestには収録されないが、Release assetには凍結bytesのまま添付した。manifestの8項目はScratch OCI／Bridge OCI／WireScope 2 file／contracts／LAN 3 file。
- 原因は公開用の形式への変換であり、配布物を作り直した差ではない。詳細は`MANIFEST_DIFF.json`、公開された実物は添付`manifest.json`。

## 本文・workflow

- 元の確認済み本文：4,763 bytes、SHA-256 `468f0d1e2811d85ee4ed2fee6f3069652bd4543a0aa1ee8913e6a36cc3580e5b`。
- 指定1文だけを差し替えた公開本文：**4,744 bytes、SHA-256 `6ecf13d711589af52a832c82a96fba4bdad42b692097523af516c159de118e66`**。GitHubの公開本文が同じであることを確認。ほかの箇所は変更なし。
- image workflow `312664341`（`.github/workflows/mc-remote-images.yml`）はactive→disabled_manuallyとして公開し、finallyでactiveへ戻した。workflowのsource fileは編集していない。
- 公開前後と返却前のimage run一覧が一致し、今回の`release:published`による新しいimage runは**0件**。

## 確認の範囲と次の工程

- 凍結値と異なるasset／OCIは出ていない。branch・tag・Latest・本文・asset・OCI・workflow復帰・旧release保持の照合は完了。
- Stack／ホームページ／箱庭の切り替え、共有環境の変更は行っていない。公開物のcoordinatorによる独立照合と、その後のStackへの指示は別工程。
- 返却の小さなJSON／本文／manifestをこのpacketへ保存。分類②：coordinatorの独立照合と正式recordへの収容、release closeへ引き継ぐために保持し、固有参照が無くなれば破棄可。大容量転送cacheとregctl binaryは公開照合後に破棄可の③で、公開asset／registry／Actionsが配布物の正本。
