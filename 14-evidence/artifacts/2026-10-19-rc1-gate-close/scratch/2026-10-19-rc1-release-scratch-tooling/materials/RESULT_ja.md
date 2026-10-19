# rc1 公開結果 — tooling / Scratch

- knowledge contract path: `00-hub/rc1-gate-release-instructions_ja.md`。
- knowledge contract commit: `32fd7d4892a410ef9d38f90320a511f383aaa9f9`（remote main から実読）。
- 凍結セット: `rc1-integrated-artifact-set-1`。protocol `23.2.1`、artifact `2321.0.0rc1`。
- 指定の順番で tooling → Scratch を公開。候補の再ビルドなし。公開物に凍結値との不一致なし。
- 公開操作は CLI による凍結生成物の昇格。新しい Actions 公開 run ID はなし。下記 run ID は公開物の元になった成功済み owner candidate run。
- Release はともに `prerelease=true`、`draft=false`、`make_latest=false` で公開。公開後、GitHub API で latest の tag が rc1 でないことも確認（stable latest が存在しない場合は 404）。

## Naohiro2g/minecraft-remote-tooling

- 既定 branch / 新先頭: `main@6447f6e8cbfbeeb9d229990b5c4f6e82a5875666`（fast-forward）。
- tag / 指す commit: `v2321.0.0rc1@6447f6e8cbfbeeb9d229990b5c4f6e82a5875666`。
- Release URL: https://github.com/Naohiro2g/minecraft-remote-tooling/releases/tag/v2321.0.0rc1
- Release ID / 公開時刻: `417032717` / `2026-10-19T07:53:33Z`。
- 候補生成 run ID: `39053886890`。
- 凍結 Actions artifact: `12109060950` / `sha256:5b644de44ae2f9a2fb9de09d221c2930218f6c317baffee3b5c7f817309555fa`。

| 公開 asset | bytes | SHA-256 | 凍結値との照合 |
| --- | ---: | --- | --- |
| `bridge.oci.tar` | 114626048 | `3982876466fb860dca250438d73e18e441a2a85d67d9f149f537a7a8d1a1c44c` | 全桁一致 |
| `wirescope-app.manifest.json` | 2339 | `3dd668a236463809a4cdc6d19375f3e6d75eea0c8089a616d2b761d3a4a05235` | 全桁一致 |
| `wirescope-app.zip` | 83854 | `da3da0b6cf4d05265bc0c11abaa4913208c7cfc3600b0c3e78c93a356fc431ad` | 全桁一致 |

## Naohiro2g/scratch-editor

- 既定 branch / 新先頭: `develop@f20e55eb53f192eab6cdc4f0d5aae4f52b2dc8db`（fast-forward）。
- tag / 指す commit: `v2321.0.0rc1@ec79b3b0e364e722d6926a0932eb4bf088ddd3a1`。
- Release URL: https://github.com/Naohiro2g/scratch-editor/releases/tag/v2321.0.0rc1
- Release ID / 公開時刻: `417042836` / `2026-10-19T08:21:05Z`。
- 候補生成 run ID: `39072595749`。
- 凍結 Actions artifact: `12116296168` / `sha256:259ca91e68616035a81deb49bb1060300138c85942597a2b11c7b7f5133d66e8`。

| 公開 asset | bytes | SHA-256 | 凍結値との照合 |
| --- | ---: | --- | --- |
| `contracts.tar.gz` | 1908 | `48948ba47d55409f02a8ff8e0d44021b07859e11ffa5ca0f8598e6ef06082390` | 全桁一致 |
| `manifest.json` | 2320 | `776e0d51a8d8db14cb5ace23f2a41f9d6a56e7eacb0a51e88463bd6bf076c68c` | 新規の公開metadata。manifest v2 schema・semantics・内容照合 PASS |
| `mc-remote-scratch-LAN-2321.0.0rc1-linux-x64.zip` | 271455727 | `b76b574803c58403e38438d2569917bd72ca95f039026f12ed3a294edfcfba54` | 全桁一致 |
| `mc-remote-scratch-LAN-2321.0.0rc1-macos-arm64.zip` | 266199673 | `bdfff47b8c1210a359ed65a8be6fca26624546e3c04add125063968acc091412` | 全桁一致 |
| `mc-remote-scratch-LAN-2321.0.0rc1-windows-x64.zip` | 261848009 | `86bbaf9a278683315ffe2ebd4f19d56ba53f5501289e4cddfc22f284d8d4e209` | 全桁一致 |
| `scratch-gui.tar.gz` | 138835708 | `2dafb257c511989946da021591191cc1501e0d1a9211cc559373ed7de30f19c2` | 全桁一致 |
| `wirescope-app.manifest.json` | 2339 | `3dd668a236463809a4cdc6d19375f3e6d75eea0c8089a616d2b761d3a4a05235` | 全桁一致 |
| `wirescope-app.zip` | 83854 | `da3da0b6cf4d05265bc0c11abaa4913208c7cfc3600b0c3e78c93a356fc431ad` | 全桁一致 |

## OCI の結果

| OCI | 公開 locator | 公開 index digest | 凍結との照合 |
| --- | --- | --- | --- |
| Bridge | `ghcr.io/naohiro2g/mc-remote-bridge:v2321.0.0rc1` | `sha256:305d6e38b36e195a0e158522f32f3a8c45d39da2aeec7b7e46f785c920406acf` | 完全一致 |
| Scratch | `ghcr.io/naohiro2g/mc-remote-scratch:v2321.0.0rc1` | `sha256:75e76edb6b8a1de4fb896184b5c26bed7cb1791296f82903e6b1ec4a1a5ab840` | 完全一致 |

- `skopeo copy --all --preserve-digests` で凍結OCI archiveを直接転送。公開後、匿名で取得したregistry indexのSHA-256を独立計算し、両方とも凍結digestと照合した。provenance / SBOM の参照も同じindexに含まれる。
- Scratch の amd64 / arm64 のplatform manifestとraw configも匿名で取得し、凍結archive内のbytesと一致。全layer descriptorも一致。例外条件による差の受け入れは使っていない。
- Scratch の凍結OCI archiveは 325822464 bytes / SHA-256 `88d81fba1aca0194c85f638cf19c66a1a2087748f32ff501bdb1dd283ea1d0c5`。archive全体も取得して凍結値と独立照合した。

### version label と mtime

- version label: 揃えている。凍結sourceのcandidate / 公開workflowはどちらも `RELEASE_VERSION=v2321.0.0rc1` を渡す。公開済みの両architectureの実際のlabelも `v2321.0.0rc1`、revisionは `ec79b3b0e364e722d6926a0932eb4bf088ddd3a1`。
- created: 両workflowは凍結sourceの `SOURCE_DATE_EPOCH=1792273800` を渡す構成。凍結・公開の実configは `2026-10-17T21:50:00Z` で一致。
- COPY layerのmtime: ビルド入力を一定時刻へ正規化する実装は入っていない。凍結したGUIファイルにはbuild時刻 `1792274146` / `1792274147` がある。今回は凍結OCIを直接転送したため、公開物も同じmtimeを保持し、index / layer / configの全digestが一致。新しいbuildによってmtimeが揃うことは未検証。

## 検証と運用状態

- 凍結Actions外側ZIPは両方とも全体を取得してSHA-256を検査。内側の全ファイルを独立hashし、公開指示のbytes / SHA-256と照合した。
- shared fixture 2件も凍結sourceのGit blobからbytes / SHA-256を照合。詳細は `frozen-verification.json`。
- 公開直前と公開後に全assetのsizeとGitHub providerが計算したdigestを照合。公開済み `manifest.json` は実体も取得してSHA-256 / v2 schema / semanticsを検証。
- ScratchのRelease公開イベントによる再ビルドを防ぐため `mc-remote-images.yml` を一時停止し、公開後に `active` へ戻した。新規の公開workflow runが起動していないことを確認。
- tooling PR #1、Scratch PR #26 はfast-forward反映によりMERGED。指定どおりScratchのdevelop先頭とtagのcommitは異なる。
- 一時registry認証情報は削除。作業ツリーの既存未追跡ファイルは変更していない。build / human test / deployは実行していない。

## 引き継ぎ

- 引き継ぎ先: knowledge の gate coordinator。Release URL、tag、default branch先頭、上記digestを参照identityとして、公開後照合とホームページ・API一覧・rc1ブロック一覧snapshotの取り込みを進められる。
- このdirectoryはローカル搬送素材で、正式evidenceではない。knowledge側への配置・採番・commitは行っていない。
- 今回参照したknowledgeの公開指示の範囲は完了。公開VPSへの切り替えなど後続作業はcoordinatorの担当。
