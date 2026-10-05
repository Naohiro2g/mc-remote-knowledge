## Release gate 確認票（b9公開完了・追記）

- 対象 repo: `Naohiro2g/scratch-editor`、担当する共通tooling `Naohiro2g/minecraft-remote-tooling`
- 対象 branch/commit: Scratch `develop@7fbbf034488760d8fc7e034bf23f3e08e6e1807d`、tooling `main@dc1ab834183e29f2eb03059b07e99d2b463776ee`。照合helperは隔離branch `agent/b9-release-preflight@dfebdfebd6aad8fd1e3246ca1566653f6b198b95` に保持
- release / channel: `2320.0.0b9`／GitHub prerelease。両repoともprerelease=true、draft=false、make_latest=falseで公開
- gate coordinator: knowledge担当session
- human release owner: プロジェクトオーナー
- current phase: 担当するtoolingとScratchの公開・identity照合完了。本票を返却。横断gateの閉鎖判断はcoordinatorへ
- contract maturity / required test tier: 批准済み。固定workflowによる公開と、承認されたpackaging差の範囲でartifact identityを比較
- knowledge contract path: `00-hub/dev-repo-protocol_ja.md` runtime、`00-hub/release-gate-notes_ja.md` b9節「release authorization」「Scratch OCIのversionラベル」「Scratch OCIのCOPY layer」
- knowledge contract commit: `7eec4255e1b820cf996dc71c42b34d672dea44f8`（remote mainと一致を確認し実読）
- gate manifest identity: `b9-integrated-artifact-set-1`。凍結source／tooling／fixture不変。公開Scratch OCI digestは下記。Release manifestは1,168 bytes／`cbc6af558a0633cd252d2f6e2192523e4d92f2602c629e9092677e2f2cb920da`
- change cone: Scratch OCIのversionラベル、mtime、configの生成metadata。固定workflowを凍結sourceで実行。製品sourceとfixtureを変更していない
- reused PASS / rationale: knowledge記録のsegment 0〜3の実機PASSを、human ownerのCOPY layer包装差受入れ指示に従って再利用。実機・製品unit suiteは再実行していない
- exact compatibility set / freeze status: sourceは凍結値のまま。公開Scratch OCIの内容が凍結OCIと一致し、差が許可されたmtime／config生成metadataの範囲内であることを照合。Bridge、WireScope、contractsは凍結identityと一致
- target deployment / profile / lock: GitHub ReleaseとGHCRへの公開。shared／dev環境や手元サービスへ新OCIをdeployしていない
- authorized next action: 承認された公開と公開後の照合を完了し、identityをcoordinatorへ返す。判定待ちの事項は本担当には無い
- test class: build／artifact identity inspection／static filesystem comparison。live-humanは既存PASSの再利用
- 実行した command / 手順: annotated tag→prerelease公開→固定workflow `37270517123`→Release実体の`verify-published-release.py`→読み取り専用比較workflow `37271363905`。比較helperは凍結candidate ZIPの外側SHAを固定して取得し、GHCRから公開digestのOCIを`--all --preserve-digests`で取得。全OCI blob hash、runtime layer／configを検査。digestの異なるlayerは全entryのpath／内容SHA／size／type／link先／mode／uid／gid／所有者名／pax headersを照合。mtimeだけの差を認める。等しいdigestのlayerはbyte同一。比較helperのmode・所有者・型・内容・link・path、runtime config変更拒否の境界も確認
- 結果: 固定公開workflow success。公開OCI比較 success／amd64・arm64ともPASS。各architectureで先頭9 layerはdigest同一。最後のCOPY layerの各1,746 entryは内容・属性一致、追加／削除なし、1,743 entryのmtimeのみ相違。config差はversionラベル、作成時刻、version由来のARG／LABEL履歴、EXPOSE履歴の生成hex表記、対応する最終layerのdiff_idのみ。WireScope ZIP、detached manifest、contractsはbytes／SHA-256一致。Bridge registry indexは凍結値と一致
- evidence record / artifact: `handoff-materials/2026-10-05-b9-release/`。本票、公開操作request／response、provider metadata、実体asset、`artifacts/published-comparison/published-oci-comparison.json`（7,469 bytes／`12417d60f77bf724448ddc1b3ed75418eec22d60ce38bb5b5a32dd8071d62520`）、監査script。全file inventoryは`INVENTORY.json`／`SHA256SUMS`。正式evidenceのauthoringはknowledge側
- 未検証の境界: 新OCIのcontainer起動・deployと再度の実機試験は未実施。Bridge containerとしての起動は、knowledgeに記録されたVPSベータへのdeploy時のhuman確認へ委ねる。provenance／SBOMは生成metadataとして扱い、同一bytesとは主張しない。他repoの公開を実行していない
- security / compatibility / rollback の確認: token／credential／private接続先を読出し・変更していない。user未追跡2件とlocalhostサービス不変。旧b8 tag／Release不変。公開sourceは既にdefault branch developへ統合済み。比較branchはevidence収容確認まで保持し、製品へ統合しない
- 判定を求める事項: なし。横断公開完了／gate closeはcoordinatorが他repoの事実と合わせて判断する

公開先とsource:

- Scratch: https://github.com/Naohiro2g/scratch-editor/releases/tag/v2320.0.0b9 （Release ID `403409264`、title `mc-remote Scratch 2320.0.0b9`）。tag target／developは `7fbbf034488760d8fc7e034bf23f3e08e6e1807d`
- tooling: https://github.com/Naohiro2g/minecraft-remote-tooling/releases/tag/v2320.0.0b9 （Release ID `403384824`）。tag targetは `dc1ab834183e29f2eb03059b07e99d2b463776ee`
- 固定公開workflow: https://github.com/Naohiro2g/scratch-editor/actions/runs/37270517123 （release event、head source7fbb、success）
- 公開OCI比較workflow: https://github.com/Naohiro2g/scratch-editor/actions/runs/37271363905 （helper source dfebdfeb、success）。結果artifact ID `11327683955`、92,127 bytes／`a5481e7599121513faec2a8c730216372b7b430ed7ffc100cee43862361bd4fc`

Release manifestのrole:

| role | kind | 公開identity |
| --- | --- | --- |
| scratch | oci | `ghcr.io/naohiro2g/mc-remote-scratch@sha256:f44e7a6c1a3b041aba787eba5e052a3ae78ce4ce733732bc7213207a3b17f607` |
| bridge | oci | `ghcr.io/naohiro2g/mc-remote-bridge@sha256:5828304c9bb1d60df8672f9189f503790050e09358bd375f39e4d59d190eb84f` |
| wirescope | https-file | `wirescope-app.zip`、83,854 bytes／`da3da0b6cf4d05265bc0c11abaa4913208c7cfc3600b0c3e78c93a356fc431ad` |
| wirescope-manifest | https-file | `wirescope-app.manifest.json`、2,339 bytes／`c654f7d1f0be2773d6737e889279b2587317088717f162b082c82be9cff910d7` |
| contracts | https-file | `contracts.tar.gz`、1,908 bytes／`48948ba47d55409f02a8ff8e0d44021b07859e11ffa5ca0f8598e6ef06082390` |

Scratchのmanifest.json: 1,168 bytes／`cbc6af558a0633cd252d2f6e2192523e4d92f2602c629e9092677e2f2cb920da`（asset ID `611690856`）。各assetはproviderのsize／digestとdownloadした実体のhashを照合。registryのtagを読み取ったraw indexもmanifestのdigestと一致（Scratch index1,611 bytes、Bridge index1,609 bytes）。OCI indexのbytesはimage archive／展開後のsizeではない。

tooling Releaseの3 assetは先行公開票の値から不変: WireScope ZIPとmanifestは上記と同じ。`bridge.oci.tar`は114,628,096 bytes／`b6a6feec07e8d7ae9805a81e8dc370e6220e91af145ef3117ce5ed12e703b100`。今回、固定workflowがBridgeをregistryへ同一index digestでコピーした。

handoff分類:

- ① 本票、公開操作・provider metadata、比較結果、監査script、asset identityはknowledge正式evidenceへ移す候補（案: `14-evidence/artifacts/2026-10-05-b9-release/scratch/`）。旧停止票は経緯として保持。本票を現在の返却とする
- ② 大きい公開前build ZIP、比較用隔離branch／worktree、凍結candidate ZIPの元directoryは、coordinatorの収容・失効確認まで公開close担当へ引き継ぐ。参照identityは上記。branch／大archiveを恒久保管先とはしない
- ③ 今回は削除していない。公開Releaseで取れるfileと参照不要の比較素材は、正式収容をcoordinatorが確認した後に処理する
