# Release gate 確認票（追記：Scratch b8公開完了）

- 対象 repo: Naohiro2g/scratch-editor。
- 対象 branch/commit: tag `v2320.0.0b8`のpeeled targetとdevelopはともに`691576f60b7f0824e1753bd6823901d01fbe2422`。agent/b8-compatibilityは`01cdb0bfee3a681697ffa44db5b890045b74b01c`で保持。
- release / channel: mc-remote Scratch 2320.0.0b8 / prerelease。draft OFF、Latest非対象。
- gate coordinator: knowledge coordinator。
- human release owner: human owner（公開承認2026-10-03）。
- current phase: Scratch repoの公開と公開後identity照合が完了。横断gateのcloseはcoordinatorへ返す。
- contract maturity / required test tier: 凍結b8、横断技術gate GREENと公開承認を受けた公開後のidentity照合。
- knowledge contract path: 00-hub/release-gate-notes_ja.mdの2026-09-30節「release authorization」、00-hub/release-operations-responsibility-design_ja.md §10・§12。
- knowledge contract commit: `fd7cad78564dd96ee91831d284abf1560fdf65b0`。remote mainと一致を確認し実参照。
- gate manifest identity: b8-integrated-artifact-set-1。
- change cone: 承認済みタグ・developのfast-forward・prerelease公開。製品コード／fixtureは変更なし。
- reused PASS / rationale: 凍結sourceのCI run36996656694はsuccess、公開前のtitle test1件PASS。公開workflowのproduction buildとartifact生成もsuccess。候補を変更せず既存のgate結果を使用。
- exact compatibility set / freeze status: 691576fの凍結成果物を維持。01cdb0bのWireScope列幅変更はtag／develop／b8成果物に含めずb9へ残した。
- target deployment / profile / lock: GitHub prereleaseとGHCRのみ。dev、public server、hosted Scratch等への配置は行っていない。
- authorized next action: 公開指示票の1〜5を実行し、identityを返す。他repoへの着手・公開指示なし。
- test class: 公開後のprovider／artifact identity照合。新たなlive-auto／live-human試験は行っていない。
- 実行した command / 手順: annotated tag作成とpush → developのstrict fast-forward → gh release create（--verify-tag、--prerelease、--latest=false、指定title、notes-file） → releaseイベントの固定workflowを監視 → GitHub API／Release assetの実体／GHCRタグのdigestを照合。手動artifact build・手動asset upload・npm publishなし。
- 結果: 全操作完了、以下の公開状態・identity照合はPASS。指定WireScope ZIPにbytes／SHA-256の不一致なし。
- evidence record / artifact: materials/provider-identities.json、asset-verification.json、oci-identities.json、Releaseから取得した4 asset。素材digestはmaterials/export-identities.json。正式evidenceの配置はknowledge担当が行う。
- 未検証の境界: 今回はOCIのregistry identityとamd64／arm64の存在を確認。公開OCIの起動・pull全layerの検証、deploy、capacity／soak／rollbackは実施していない。b8の既知のBedrock dustサイズ制限・backpressure実機NOTRUNはSSOTのgate記録を維持。
- security / compatibility / rollback の確認: 私的接続値・credentialを票や公開release notesへ含めない。tracked worktree／stageに変更なし。ユーザー未追跡素材は保持。rollback／shared環境変更なし。
- 判定を求める事項: 指示票どおりの公開後照合としてcoordinatorへ返す。横断gateの正式closeと後続sliceの移管はcoordinatorが扱う。

## 公開状態とGit identity

- Release: [mc-remote Scratch 2320.0.0b8](https://github.com/Naohiro2g/scratch-editor/releases/tag/v2320.0.0b8)。id `402440419`、published_at `2026-10-03T09:42:03Z`。prerelease true／draft false。作成時--latest=false、公開前後のLatest APIは404でLatest Releaseは存在しない。
- tag target: `691576f60b7f0824e1753bd6823901d01fbe2422`（annotated tagをpeeledしたcommitをGitHub APIとlocal Gitで照合）。
- develop: `691576f60b7f0824e1753bd6823901d01fbe2422`。旧develop `0fc2cccde4d331edd01cda4eae0340601b44020c`からstrict fast-forward。
- b9保持branch: `agent/b8-compatibility@01cdb0bfee3a681697ffa44db5b890045b74b01c`。
- 固定workflow: [run 37113933602](https://github.com/Naohiro2g/scratch-editor/actions/runs/37113933602)、attempt 1、event release、head_sha `691576f60b7f0824e1753bd6823901d01fbe2422`、completed／success。

## Release assets

| file / role | bytes | SHA-256 |
| --- | ---: | --- |
| [contracts.tar.gz](https://github.com/Naohiro2g/scratch-editor/releases/download/v2320.0.0b8/contracts.tar.gz) / contracts | 1908 | `48948ba47d55409f02a8ff8e0d44021b07859e11ffa5ca0f8598e6ef06082390` |
| [manifest.json](https://github.com/Naohiro2g/scratch-editor/releases/download/v2320.0.0b8/manifest.json) / 収集入口（5 role） | 1168 | `122846bd6624b80718a905b49dde749e6d283a1ae1cee2ff6daa5826e9cd2887` |
| [wirescope-app.manifest.json](https://github.com/Naohiro2g/scratch-editor/releases/download/v2320.0.0b8/wirescope-app.manifest.json) / wirescope-manifest | 2321 | `6ea468f50d50b52722b8f34145743df86cebc60865fe0e827be5632c26b024d0` |
| [wirescope-app.zip](https://github.com/Naohiro2g/scratch-editor/releases/download/v2320.0.0b8/wirescope-app.zip) / wirescope | 83746 | `4cb349894b71d61d7ca143d8362a5b79deb1810e1d7a9e31ad30e29bfe370a07` |

WireScope ZIPは83746 bytes／4cb349894b71d61d7ca143d8362a5b79deb1810e1d7a9e31ad30e29bfe370a07で、指示票の期待値と一致。detached manifestのsourceは691576f、ZIP内6 assetのbytes／SHA-256をすべて照合。contractsもcandidateのidentityと一致。

## manifestのOCI role

| role | locator | OCI digest |
| --- | --- | --- |
| scratch | `ghcr.io/naohiro2g/mc-remote-scratch` | `sha256:d595992e05feb891ead10860a14eb292228968d8ca9460505a34fa1d24a1d8c0` |
| bridge | `ghcr.io/naohiro2g/mc-remote-bridge` | `sha256:0d7802aba4af418a634afb74c52813810d3b9224ee1ae8e97a485551cf9d79dc` |

両OCIのv2320.0.0b8タグをGHCRへ読み取り照合し、上のdigestとの一致を確認。各indexは1611 bytesで、linux/amd64とlinux/arm64、attestation manifestを含む。このbytesはimage全layerの総量ではない。

## release close時の素材分類

全14のローカルhandoff directoryへ後続担当とentryのSHA-256、次の一手を指定した。HANDOFF-INVENTORY_ja.md／materials/handoff-inventory.jsonを参照。b9の列幅修正は01cdb0bとその素材をWireScope担当へ引き継ぐ。b8 liveの正式summaryはknowledgeの14-evidence/records/2026-10-03-b8-dev-live_ja.mdへ着地済み。詳細artifactの配置・非参照確認と、private素材のbackstage移管は担当へ返し、当repoから削除・外部送信はしていない。
