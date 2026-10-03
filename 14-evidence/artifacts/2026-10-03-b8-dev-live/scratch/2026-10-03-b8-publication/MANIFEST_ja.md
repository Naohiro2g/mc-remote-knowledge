# Scratch b8公開（公開・identity照合完了）

- 指示元: knowledge coordinator、human ownerの公開承認2026-10-03。
- knowledge contract commit: fd7cad78564dd96ee91831d284abf1560fdf65b0。remote mainと一致を確認し、runtime、INDEX、release-gate-notesのrelease authorizationとrelease operationsを参照。
- exact set: b8-integrated-artifact-set-1。tag v2320.0.0b8とdevelopのtargetは691576f60b7f0824e1753bd6823901d01fbe2422。
- 保持branch: agent/b8-compatibility@01cdb0bfee3a681697ffa44db5b890045b74b01c。列幅修正はb9へ残す。
- 事前確認: frozen commitのCI run36996656694はsuccess。origin/developの0fc2cccde4d331edd01cda4eae0340601b44020cはfrozenの祖先、strict fast-forward可能。remoteのtagとReleaseは未存在、stableのLatest Releaseも存在しない。
- 公開状態: prerelease ON、draft OFF、Latest非対象。titleはmc-remote Scratch 2320.0.0b8。release notesはRELEASE-NOTES_ja.md。
- 成果物の生成・添付: .github/workflows/mc-remote-images.ymlをpublishedイベントで起動。手動build・手動asset upload・npm publishは行わない。
- 照合対象: workflowのWireScope ZIP 83746 bytes／SHA-256 4cb349894b71d61d7ca143d8362a5b79deb1810e1d7a9e31ad30e29bfe370a07。manifestの5 roleとOCI digest、Release assetのbytes／SHA-256を実体から採取して返す。
- 本directoryはローカルの搬送素材。正式evidenceの配置と横断gateのcloseはknowledge担当。private運用値は含めない。
- 完了した操作: annotated tagを作成・push、remote developとlocal developを691576fへstrict fast-forward。GitHub APIでtagのpeeled target、develop、保持branchのSHAを照合済み。
- GitHub Release: https://github.com/Naohiro2g/scratch-editor/releases/tag/v2320.0.0b8 、id402440419、published_at2026-10-03T09:42:03Z。title、draft:false、prerelease:true、target_commitishの一致を確認。作成時--latest=falseを指定。
- 固定workflow: run37113933602、https://github.com/Naohiro2g/scratch-editor/actions/runs/37113933602 、event:release、head_sha691576f60b7f0824e1753bd6823901d01fbe2422。completed／success。
- 照合: ダウンロードした4 assetはGitHub APIのbytes／digest、release manifestのhttps-file roleとすべて一致。WireScope ZIPは83746 bytes／指定SHA-256で一致。detached manifestのsourceと6 assetを実ZIPへ照合。GHCRのScratch／Bridgeタグはrelease manifestのOCI digestと一致し、linux/amd64・linux/arm64を確認。公開後もLatest APIは404で、b8はLatest非対象。
- 返却: RESULT_ja.md。provider-identities.json、asset-verification.json、oci-identities.jsonと取得したRelease assetsはmaterialsへ保存。保存素材のdigest一覧も同directoryへ作成。
- 素材分類: HANDOFF-INVENTORY_ja.mdとmaterials/handoff-inventory.jsonで全14 directoryの後続担当、entryのidentity、次の一手を指定。b8の正式live summaryはfd7cad7の14-evidence/records/2026-10-03-b8-dev-live_ja.mdに着地済み。詳細素材の正式配置確認と非参照確認前の破棄は行わず、private素材は公開搬送対象外。
