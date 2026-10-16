# b10 Scratch pre-release返却票（2026-10-14）

- Release：<https://github.com/Naohiro2g/scratch-editor/releases/tag/v2320.0.0b10>
- tag `v2320.0.0b10` target：`0809eb5e49e4b83c17a4e91b435d151b9d1b0655`（annotated tagのpeelをoriginで照合）
- `develop`先頭：`0809eb5e49e4b83c17a4e91b435d151b9d1b0655`（旧`7fbbf034488760d8fc7e034bf23f3e08e6e1807d`からstrict fast-forward、originで照合）
- Release状態：`prerelease=true`、`draft=false`、title `mc-remote Scratch 2320.0.0b10`。作成時に`--latest=false`を指定した。
- Release本文：指示された`RELEASE_NOTES_DRAFT_ja.md`（SHA-256 `90f8957f81ce73136a7b1cb87338985f5033ee3c944f041e1b6bb0c4c6a83f2e`）で作成。作成後、human ownerが本文冒頭の重複タイトルを削除した。こちらは再編集していない。
- repository variables：`SCRATCH_LOCAL_CANDIDATE_ARTIFACT_ID=11862469927`、`SCRATCH_LOCAL_CANDIDATE_ARTIFACT_DIGEST=sha256:6576a64d75f7eb46f2245ea5d38b336e18388131c79b0db869e693edc3a1fb23`（GitHub APIで読み戻し一致）。
- 公開workflow：[run 38525643511](https://github.com/Naohiro2g/scratch-editor/actions/runs/38525643511)、release event、head `0809eb5e49e4b83c17a4e91b435d151b9d1b0655`、success。
- 公開`manifest.json`：schema `mc-remote.release-manifest` v2、2,105 bytes、SHA-256 `7c90c4b0041447f132a1da4bb20bdbdd259eed8a4023d79993f4976295708741`、契約validator PASS。
- Scratch OCI：`ghcr.io/naohiro2g/mc-remote-scratch:v2320.0.0b10`、digest `sha256:1c7bccb32444e7263841ce87add0547cf798f95df2b47971b9be78db847d3be5`（Release manifestとGHCRのtagを独立に照合）。Bridge OCIはmanifest上`sha256:5828304c9bb1d60df8672f9189f503790050e09358bd375f39e4d59d190eb84f`。

| Release asset／manifest role | bytes | SHA-256 |
| --- | ---: | --- |
| `mc-remote-scratch-LAN-2320.0.0b10-windows-x64.zip`／`scratch-local` | 261,590,008 | `00e73b71d63859f088595257abdec7ce204a09282d79f26daa8d851e0f4af1e8` |
| `mc-remote-scratch-LAN-2320.0.0b10-macos-arm64.zip`／`scratch-local` | 265,941,672 | `edcc757b931d8b89fc18487ee385c20d9ecbdc398b7f34f017e2137fe26c12d2` |
| `mc-remote-scratch-LAN-2320.0.0b10-linux-x64.zip`／`scratch-local` | 271,197,726 | `b69e5b1118dba284604c217b0f3b06ea40b9876014166461705fdc400f647526` |
| `wirescope-app.zip`／`wirescope` | 83,854 | `da3da0b6cf4d05265bc0c11abaa4913208c7cfc3600b0c3e78c93a356fc431ad` |
| `wirescope-app.manifest.json`／`wirescope-manifest` | 2,339 | `c654f7d1f0be2773d6737e889279b2587317088717f162b082c82be9cff910d7` |
| `contracts.tar.gz`／`contracts` | 1,908 | `48948ba47d55409f02a8ff8e0d44021b07859e11ffa5ca0f8598e6ef06082390` |
| `manifest.json`／公開identity | 2,105 | `7c90c4b0041447f132a1da4bb20bdbdd259eed8a4023d79993f4976295708741` |

照合：7 assetすべて、GitHub Release APIの`size`と`digest`がダウンロードした実体のbytes／SHA-256に一致。3 ZIPはcandidate run `38495047680`のローカル保存実体と`cmp`でbyte一致。candidateの3 ZIP identityもknowledge gateの固定値と一致。

未実施：3 OSのpre-release配布ページからの人間参加試験、shared deploy、pre-release解除。Windowsの「許可する」画像はhuman ownerの添付予定で、現時点のRelease asset一覧にはない。
