## Release gate 確認票（b9実装・移管の追記）

- 対象 repo: `Naohiro2g/scratch-editor`、依頼で明示許可された移管先 `Naohiro2g/minecraft-remote-tooling`
- 対象 branch/commit: Scratch `agent/b9-tooling`／`develop` = `7fbbf034488760d8fc7e034bf23f3e08e6e1807d`（push済み）。tooling `main` = `dc1ab834183e29f2eb03059b07e99d2b463776ee`（push済み）
- release / channel: `2320.0.0b9`／beta candidate。protocol `23.2.0`。tag／Release未公開
- gate coordinator: knowledge coordinator
- human release owner: human owner
- current phase: 契約修正・owner移管・Scratch consumer切替・candidate生成
- contract maturity / required test tier: 批准済み契約、決定論的unit／共有fixture／build／artifact identity検査。凍結後の実機試験は別指示
- knowledge contract path: `00-hub/b9-gate-work-instructions_ja.md`、`00-hub/release-gate-notes_ja.md`、`00-hub/DECISIONS_ja.md`（2026-10-03-01／02、2026-10-05-01／02）、`10-protocol/protocol-tooling-migration-plan_ja.md`、wire §4／§5.4
- knowledge contract commit: `900f6f4b8027d265a62ba7f139d4f3b1bbe78100`（実参照したpush済みSHA）
- gate manifest identity: 未提示
- change cone: 未知eventとchat.post nullの契約対応、WireScope列幅、b9 client identity、共通tooling ownershipと取得・CI・公開collector。learner API／wire method／protocol version追加なし
- reused PASS / rationale: 公開b8のfixture12件はbyte不変。機能修正後・移管前のScratch `c7505c`と移管後toolingのruntime／fixture／index HTML 44 file、およびWireScope ZIP内6 assetがbyte一致。source URL／commitを記すdetached manifestとOCI metadataは比較対象外。b8のlive-humanをb9の実機試験済みとはしない
- exact compatibility set / freeze status: b9のexact set未提示・未凍結。Scratch担当による横断判定なし
- target deployment / profile / lock: shared環境は未操作。consumer pinは `mc-remote/tooling-lock.json`（固定Git SHA、fixture bytes／SHA-256、GitHub artifact ID／digest、Bridge OCI digest）
- authorized next action: 今回の実装・push・candidate生成と確認票返却まで。consumer各担当への取り込みと凍結・deploy・liveはcoordinatorの進行
- test class: `unit/deterministic`。実サーバー接続／live-auto／live-humanなし
- 実行した command / 手順: 下の検証表、commit分離、repo rename／設定readback、13 fixtureとWireScope asset比較、固定sourceのActions生成・取得・identity照合
- 結果: 契約fixture発行、tooling source投入、Scratch旧owner撤去とconsumer取得元切替を実施。10/6確認点の「fixture発行と移管先source投入」は両方そろっている。candidateのidentityは下表
- evidence record / artifact: 確定搬送素材 `handoff-materials/2026-10-05-b9-tooling-migration/`。正式evidence案: `14-evidence/artifacts/2026-10-05-b9-tooling-migration/scratch/`。正式record／配置／INDEXのauthoringはknowledge担当。素材一覧はMANIFESTとSHA256SUMS
- 未検証の境界: 他consumer（McRemote／Python）の取得元切替と相互接続、sharedへの配置、real-browser／live-human、registryへのBridgeコピー、公開workflowの実際のRelease実行。candidate内のOCI archiveを公開registry imageとして扱わない
- security / compatibility / rollback の確認: 認証・origin/grant/transport機能は維持。未知eventは共通fieldのみ観測へ渡す。取得時の改変／長さ違い／浮動ref／別owner／path traversalは拒否。元のrepo historyと公開b8 tag／setを保持。Actions read、main strict Build and test、force/delete禁止、admin例外あり。rollbackは `691576f60b7f0824e1753bd6823901d01fbe2422`／`v2320.0.0b8` と公開b8 set。world等のrestoreはしていない
- 判定を求める事項: b9候補としての取り込みと次のgate進行。picker aliasはhuman ownerの登録語未選択で非blockerとして保持。移管そのものの最終判定は置かず、他consumerと初回stable後のJava追従による再検証へ続く

### commitの分離

| Scratch commit | 内容 |
| --- | --- |
| `62e46fd156a55c57794227d370a72f3558aa43d8` | 契約対応、ChatPostResult、共有fixture発行 |
| `c7505c887c5c71a942d9f1f190b32a5da00544bc` | 保持していたWireScope列幅（01cdb0b）をdevelopへ取り込み |
| `688b1b1c338e1216bf0a798ffd99c253a39f7025` | client identityをb9へ |
| `ea796dcd1bb4d0086e58a632efc82cb708b44a56` | GUI観測feedの未知event／chat.post契約追従 |
| `3e5ac5fcdb2817cf03b70f7618d25d3e0c923f76` | Scratch consumer切替、旧owner撤去、lock／CI／collector／docs |
| `7fbbf034488760d8fc7e034bf23f3e08e6e1807d` | 実在VMをvirtual mockしていたGUI unitの指定修正（製品code無変更） |

移管を外す場合は契約対応とfixtureを単独で採れる。公開b8 source／tagと旧branch履歴を変更していない。

### 新shared fixture

- 初回発行: `scratch-editor@62e46fd156a55c57794227d370a72f3558aa43d8:mc-remote/protocol/test/fixtures/chat-event-compat-v23.2.json`
- 現owner: `minecraft-remote-tooling@dc1ab834183e29f2eb03059b07e99d2b463776ee:packages/protocol/test/fixtures/chat-event-compat-v23.2.json`
- schema: `mcremote.chat-event-compat.v23.2`
- bytes／SHA-256: **32382**／`670b0a86df1956c0e44c6986a0a2598caab32c7328804f9c703190e62e9dd727`
- case数: **33**（chat.post 7、event batch 22、stateful rejection 4）。keysと適用範囲は `NEW_FIXTURE_ja.md`。全13 fixture identityは `FIXTURE_IDENTITIES_ja.md`

### 検証

| command／対象 | 結果 |
| --- | --- |
| tooling root `npm ci`、`npm test`、`npm run build` | 独立lockからPASS。Protocol39／Bridge30／WireScope144、計213 test |
| Scratch `npm install --package-lock-only --ignore-scripts` | PASS、残る依存のresolved version変更なし |
| `npm run refresh-gh-workflow` | workspace8、filter再生成、publish workflow変更なし |
| VM `node test/unit/extension_mcremote.js` | 532 PASS |
| VM `node test/unit/mcremote_event.js` | 55 PASS |
| VM sign／block-value fixture consumer | 37／94 PASS |
| VM `npm run lint` | PASS、0 error（既存warning718） |
| GUI `npx jest --runInBand --runTestsByPath test/unit/util/mcremote-wirescope-source.test.js` | 22 PASS |
| GUI `npx jest --runInBand test/unit` | 72 suite／530 PASS、既存skip1 |
| GUI変更source／testのESLint | 0 error |
| root Node取得／candidate identity tests | 6 PASS。改変された取得物・浮動sourceの拒否を含む |
| Scratch `npm run build` | 全workspace PASS（既存compiler warningあり） |
| fixture byte比較 | 公開b8 12件＋新規1件すべて一致 |
| WireScope移管前後比較 | ZIP内6 assetとZIP全体が一致 |
| workflow YAML、`git diff --check` | PASS |
| tooling Actions run37220882228 | success。WireScope pair・multi-platform Bridge OCI生成 |
| Scratch CI run37232360354 | success。全workspace build、GUI lint 0 error（既存warning1075）、unit530 PASS＋skip1、integration127 PASS＋skip7、Playwright8 PASS |
| Scratch candidate run37232396741 | success。fixed tooling取得、Bridge OCI digest保持copy、全workspace build、Scratch multi-platform OCI生成 |

GUI全unitでruntime config3件とnotice overlay2件のFAILを再現した。実在dependencyに対するvirtual mock指定だけを除去後に全件PASS。失敗logも履歴として保存し、最終PASSへ置き換えて隠していない。

### owner candidate identity

- source: `minecraft-remote-tooling@dc1ab834183e29f2eb03059b07e99d2b463776ee`
- run: https://github.com/Naohiro2g/minecraft-remote-tooling/actions/runs/37220882228 （success）
- Actions artifact: `11310203564`／`tooling-dc1ab834183e29f2eb03059b07e99d2b463776ee`
- outer ZIP: 114134029 bytes／`f68527816c0e5e9a6457612d2efc3770fcdb647c7ff452853a7edd4a0d38c307`

| file | bytes | SHA-256 |
| --- | ---: | --- |
| wirescope-app.zip | 83854 | `da3da0b6cf4d05265bc0c11abaa4913208c7cfc3600b0c3e78c93a356fc431ad` |
| wirescope-app.manifest.json | 2339 | `c654f7d1f0be2773d6737e889279b2587317088717f162b082c82be9cff910d7` |
| bridge.oci.tar | 114628096 | `b6a6feec07e8d7ae9805a81e8dc370e6220e91af145ef3117ce5ed12e703b100` |
| candidate-manifest.json | 972 | `e18f3a07afee3586259845bc6ff5755ea6d6974990929c97f3ff52e9e115a77d` |

Bridge OCI index digest: `sha256:5828304c9bb1d60df8672f9189f503790050e09358bd375f39e4d59d190eb84f`（linux/amd64／linux/arm64）。archiveのfile hashとは区別する。

### Scratch candidate identity

- source: `scratch-editor@7fbbf034488760d8fc7e034bf23f3e08e6e1807d`
- run: https://github.com/Naohiro2g/scratch-editor/actions/runs/37232396741 （success）
- CI: https://github.com/Naohiro2g/scratch-editor/actions/runs/37232360354 （success）
- Actions artifact: `11314795242`／`scratch-candidate-7fbbf034488760d8fc7e034bf23f3e08e6e1807d`
- outer ZIP: **574809291 bytes**／`27ade4f9b3d6a1e4b0cf814ef346b75613df8e8d446c82793b345665be9c4d7c`
- local archive: `artifacts/scratch-candidate-7fbbf03448.zip`（この搬送directory内、Git管理外）

| role／file | bytes | SHA-256 |
| --- | ---: | --- |
| scratch-gui／`scratch-gui.tar.gz` | 138376671 | `c0d08c26b0d016c7cf4f57661022c631be0f2aa3d1d7d517ce97fd75e118c75d` |
| scratch／`scratch.oci.tar` | 322922496 | `48f4d808ff3d5a992c09101d075dfcd7d5c4ce4e91b907691fbf393db0b1f390` |
| bridge／`bridge.oci.tar` | 114628096 | `b6a6feec07e8d7ae9805a81e8dc370e6220e91af145ef3117ce5ed12e703b100` |
| wirescope／`wirescope-app.zip` | 83854 | `da3da0b6cf4d05265bc0c11abaa4913208c7cfc3600b0c3e78c93a356fc431ad` |
| wirescope-manifest／`wirescope-app.manifest.json` | 2339 | `c654f7d1f0be2773d6737e889279b2587317088717f162b082c82be9cff910d7` |
| contracts／`contracts.tar.gz` | 1908 | `48948ba47d55409f02a8ff8e0d44021b07859e11ffa5ca0f8598e6ef06082390` |
| candidate manifest／`candidate-manifest.json` | 1821 | `239f7f94cf31e732eff173744da105408b00b182d0aad73507623ea09b43bc6b` |

- scratch OCI digest: `sha256:6702b112ad53b48efa2bf99fc0145fc7b23d24a1d20743018582f781f61c9e34`
- bridge OCI digest: `sha256:5828304c9bb1d60df8672f9189f503790050e09358bd375f39e4d59d190eb84f`

すべてのfile hashをダウンロードした実体と照合した。WireScope pairとBridge archiveはtooling lockに一致。OCIのindex digest・両CPUのconfig label（source repository／commit／version）を検査した。Scratchは上記Scratch commit／2320.0.0b9、Bridgeはtooling commit／sha-dc1ab834183e29f2eb03059b07e99d2b463776ee。両方のplatformはlinux/amd64とlinux/arm64。

GUI archiveのindex、product/runtime config schema_version 1と、既定connection_enabled falseを確認。contracts archiveは公開b8の1908 bytes／48948ba47d55409f02a8ff8e0d44021b07859e11ffa5ca0f8598e6ef06082390と一致。

これらはActions candidate archiveであり、OCIのregistry locatorはまだ発行していない。正式release manifestの5 role（scratch／bridge／wirescope／wirescope-manifest／contracts）は維持し、公開collectorの実行は別のrelease authorizationを受けてから行う。

