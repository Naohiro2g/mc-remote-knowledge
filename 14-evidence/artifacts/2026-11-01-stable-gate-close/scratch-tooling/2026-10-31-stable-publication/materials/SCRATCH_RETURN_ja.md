# Scratch stable公開の返却（2026-11-01）

- 実読した公開契約：knowledge `9dee6881a414a2b1fd4a37fa4fe26ddbedd9d8a5`、`00-hub/stable-gate-release-instructions_ja.md`「共通」「minecraft-remote-tooling」「Scratch editor」。
- Scratch着手時に最新runtime／INDEXを実読：`10fe11cfd437ab45f8c000517595598229e1011e`。公開依頼本文の変更がないことをcompare APIで確認した。
- 着手条件：user経由でcoordinatorのtooling v2321.0.0照合完了（2026-11-01）を受領してから実施。
- 公開日時：2026-11-01 00:32:16 JST（2026-10-31T15:32:16Z）。
- Release：https://github.com/Naohiro2g/scratch-editor/releases/tag/v2321.0.0
- Release ID：430018752。`draft=false`、`prerelease=false`。GitHub `/releases/latest`が同じIDを返すことを確認。
- 既定branch：`develop@bee41dc9629ee3225c19ef1d6be1299b6b4bf7d1`。公開前後で不変。local developも進めていない。
- tag：`v2321.0.0` → `ffb496ed50d751d307f685f2ae555c94c893fae5`（凍結source、完全一致）。
- annotated tag object：`f5b93fcc12d22979d4e299f55f97f270af24443b`。
- 公開run ID：なし。GitHub API／CLIとregctlで手動公開し、buildを起動していない。
- 凍結候補run ID：`39744827621`、artifact ID：`12410683112`。外側artifactは1370347310 bytes／`sha256:9f0a148a286c8bc3528f1b0e4f948f2d5b9d0da141ac9d393e610e3615d81a6c`と一致。

## Release asset（8件）

ローカル実fileのbytes／SHA-256を凍結値と照合後、そのfileをそのままuploadした。
GitHubのasset size／digestが全件一致することを公開前後に確認した。
この返却は、公開URLから全fileを再downloadした独立照合を主張するものではない。

| file | bytes | SHA-256 | 凍結値 |
| --- | ---: | --- | --- |
| scratch-gui.tar.gz | 138834579 | `fa4a1939843a83b453d882dda54ad2713ff3d53f0e1a16458e0bfc731947947a` | 一致 |
| wirescope-app.zip | 83854 | `da3da0b6cf4d05265bc0c11abaa4913208c7cfc3600b0c3e78c93a356fc431ad` | 一致 |
| wirescope-app.manifest.json | 2339 | `3dd668a236463809a4cdc6d19375f3e6d75eea0c8089a616d2b761d3a4a05235` | 一致 |
| contracts.tar.gz | 1908 | `48948ba47d55409f02a8ff8e0d44021b07859e11ffa5ca0f8598e6ef06082390` | 一致 |
| mc-remote-scratch-LAN-2321.0.0-windows-x64.zip | 261870138 | `262f67442e9699a06afb39d2259fda7f429a1a16524539e2ba51b52ceddd9525` | 一致 |
| mc-remote-scratch-LAN-2321.0.0-macos-arm64.zip | 266221800 | `8cacff36c64adf8a9a6570e76db564bc81a54d1ace180e0042dbd1836f77b92f` | 一致 |
| mc-remote-scratch-LAN-2321.0.0-linux-x64.zip | 271477855 | `e3361bf69036417c8f9d03db7087d00b46e680f0f0fca1360994f16cbadba581` | 一致 |
| manifest.json | 2093 | `95b7cf9d997c9da144a5050b30560da311668dcfd35940c32eb012938d8de364` | 一致 |

`manifest.json`は凍結した`manifest.stable-draft.json`の内容をそのまま使用。差分なし。
pinned ownerの公開manifest v2契約によるschema／semantics／content検証も通過。
公開本文は準備した本文と一致。内部source／run情報やSHA-256表は公開本文に入れていない。

## OCI

- Scratch：`ghcr.io/naohiro2g/mc-remote-scratch:v2321.0.0`
- index：`sha256:d85e37291ef75e4d64ab7f0c52b9a496889205071d3afc51b796dbcc1161903c`。凍結値と完全一致。公開後のregistry HEADで再確認。
- archive：`scratch.oci.tar`、325819392 bytes／`373effd2c5da766d64077b1bcf1a70f258d59970ee5dacb15fc51b8d9bcdd491`。凍結archiveをimportしたlocal OCI layoutからindex全体を直接copyし、再buildしていない。
- amd64／arm64とも、versionラベルは`v2321.0.0`、revisionは凍結source `ffb496ed50d751d307f685f2ae555c94c893fae5`、createdは`2026-10-22T08:02:15Z`。今回ラベルやmtimeを変更せず、凍結した内容を維持した。
- Bridge：`ghcr.io/naohiro2g/mc-remote-bridge:v2321.0.0`、index `sha256:305d6e38b36e195a0e158522f32f3a8c45d39da2aeec7b7e46f785c920406acf`。先行tooling公開で凍結値一致、今回のScratch着手前にcoordinator照合済み。Scratch公開でBridgeの内容を変更していない。

## 再build防止と復帰

- workflow `312664341`（`mc-remote-images.yml`）を`active → disabled_manually`にしてから公開した。
- `release:published`で生成し直していない。公開確認後に`enable`し、`active`への復帰をAPIで確認した。
- 復帰後もrun一覧は公開前と同一。最新runは`38525643511`（2026-10-14）で、今回の新しいimage runは0件。
- 機械可読の照合記録：`SCRATCH_PUBLISHED.json`。
- これでScratchの公開返却とする。公開URLからの独立照合と横断gate判定はcoordinatorの工程。homepage／Stackの切替は変更していない。

