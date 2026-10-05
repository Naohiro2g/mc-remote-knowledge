## Release gate 確認票（b9公開再開・tooling公開済み／ScratchのCOPY layer不一致で停止）

- 対象 repo: `Naohiro2g/minecraft-remote-tooling`、`Naohiro2g/scratch-editor`
- 対象 branch/commit: tooling `main@dc1ab834183e29f2eb03059b07e99d2b463776ee`、Scratch `develop@7fbbf034488760d8fc7e034bf23f3e08e6e1807d`。公開前buildのworkflowは隔離branch `agent/b9-release-preflight@9ed22a4a14cb10974940ed93060b7b14b0113996`、CI比較は同branchの`027424e90fd0957808478d6fcb52a38447f8f960`。製品sourceは双方とも7fbbへpinして照合
- release / channel: `2320.0.0b9`／GitHub prerelease。toolingは公開済み、Scratchはtag／Release／registry未操作
- gate coordinator: knowledge担当session
- human release owner: プロジェクトオーナー
- current phase: tooling先行公開完了。Scratch公開前のOCI比較で停止
- contract maturity / required test tier: 批准済み。公開artifactのidentity確認と、packaging例外の条件に従う新旧OCI比較
- knowledge contract path: `00-hub/dev-repo-protocol_ja.md`のruntime、`00-hub/release-gate-notes_ja.md`のb9節「release authorization」「Scratch OCIのversionラベル」
- knowledge contract commit: `ede3d0fc8d548e76eefadc93b6dd415f9dce7b1b`（remote mainから実読、取得時一致）
- gate manifest identity: `b9-integrated-artifact-set-1`。凍結Scratch candidate manifest 1,821 bytes／SHA-256 `239f7f94cf31e732eff173744da105408b00b182d0aad73507623ea09b43bc6b`
- change cone: Release用version label／生成metadata／OCI packaging。sourceとfixtureは不変。追加した比較workflowとhelperは隔離branchにだけ置き、developへは入れていない
- reused PASS / rationale: knowledgeのsegment 0〜3 PASS／GREENと、今回のラベル差に対する実機PASS再利用の許可を参照。live／製品unit suiteは再実行していない。公開前buildで固定sourceのbuildと取得consumerの既存検査を実行
- exact compatibility set / freeze status: 製品sourceとtooling artifactは凍結値のまま。新Scratch OCIは許可条件を満たしておらず、公開setのidentityへ採用していない
- target deployment / profile / lock: toolingのGitHub Release。ScratchのGHCR／GitHub Releaseは未操作。dev／localhostの稼働設定にも変更なし
- authorized next action: 指示の「layerが違えば止めて返す」に従い、本票をcoordinatorへ返す。COPY layer内のmtime差を独自に採用せず、Scratchを公開しない
- test class: artifact identity inspection／static comparison。公開前のbuild・OCI構造・filesystem entryの検査。実機試験ではない
- 実行した command / 手順: toolingのannotated tag作成→draft Releaseと3 asset添付→providerのbytes／SHA-256照合→prerelease公開→tag target／公開状態のAPI照合。Scratchは隔離workflowで凍結7fbbをcheckoutし、固定公開workflowと同じDocker build引数（version=`v2320.0.0b9`、revision=7fbb）・provenance mode=max・SBOM=trueでOCI export、push=false。run `37266780367`はsuccess。新旧ZIPのSHAを固定したCI比較run `37267805360`で、全OCI blob hash・amd64／arm64のlayer／configを照合。手元でもartifact ZIPを再hashし、`compare-scratch-oci.py`と`inspect-copy-layer.py`で再照合と原因調査
- 結果: tooling公開はPASS。Scratch比較はSTOP。amd64／arm64とも先頭9 layerは同じで、最後のGUI COPY layerだけ異なる。最後のlayer内の各1,746 entryについて、path・内容SHA・size・type・link先はすべて一致、追加／削除なし。差は各1,743 entryのmtimeだけで、mode／uid／gid等も同じ。正規化済みGUI tarのbytes／SHA-256も凍結値と一致
- evidence record / artifact: 搬送素材 `handoff-materials/2026-10-05-b9-release/`。本票、`scratch-oci-comparison.json`、`copy-layer-inspection.json`、CIの原判定`scratch-oci-comparison-ci.json`、provider metadata、操作request／response、監査script。bytes／SHA-256は`INVENTORY.json`／`SHA256SUMS`。正式authoringはknowledge側。収容先案は`14-evidence/artifacts/2026-10-05-b9-release/scratch/`
- 未検証の境界: Scratch固定workflowの公開trigger自体は実行していない。公開前buildは生成物の比較用で、registryにはpushしていない。Bridge registry copyとcontainer起動も今回未実施。新Scratch OCIを実機へ配置していない。mtime差だけで安全に採用できるという横断判定は本担当では行わない
- security / compatibility / rollback の確認: token／credential／private接続先の読出し・変更なし。tooling tag targetは凍結dc1ab83、main不変。Scratch developも凍結7fbbのまま、公開tag未作成。既存b8 tagと手元b9サービス、userの未追跡2件を保持
- 判定を求める事項: GUI COPY layerのmtimeだけの差を追加のpackaging差として受け入れるか。受け入れる場合は、公開経路・公開するScratch OCIのexact identity・実機PASS再利用の扱いをcoordinatorが確定して指示する。現在の「全layer digest一致」条件のままでは再開しない

toolingの公開identity:

- Release: https://github.com/Naohiro2g/minecraft-remote-tooling/releases/tag/v2320.0.0b9 （ID `403384824`）
- tag target: `dc1ab834183e29f2eb03059b07e99d2b463776ee`（annotated tagをAPIでdereferenceして一致）
- prerelease=true、draft=false、make_latest=falseで公開。mainのsourceは不変
- Bridge OCIの置き場所: 上記Releaseの`bridge.oci.tar` asset。OCI indexは凍結`sha256:5828304c9bb1d60df8672f9189f503790050e09358bd375f39e4d59d190eb84f`。registry locatorを発行したとは主張しない

| Release asset | bytes | SHA-256 |
| --- | ---: | --- |
| `wirescope-app.zip` | 83854 | `da3da0b6cf4d05265bc0c11abaa4913208c7cfc3600b0c3e78c93a356fc431ad` |
| `wirescope-app.manifest.json` | 2339 | `c654f7d1f0be2773d6737e889279b2587317088717f162b082c82be9cff910d7` |
| `bridge.oci.tar` | 114628096 | `b6a6feec07e8d7ae9805a81e8dc370e6220e91af145ef3117ce5ed12e703b100` |

Scratchの新旧identity（新しい値は公開identityではない）:

| 項目 | 凍結 | 公開前build |
| --- | --- | --- |
| source | `7fbbf034488760d8fc7e034bf23f3e08e6e1807d` | 同一 |
| OCI index | `sha256:6702b112ad53b48efa2bf99fc0145fc7b23d24a1d20743018582f781f61c9e34` | `sha256:da7c9622f18ad7d6e45782b57c470605cebc978271c41280240192625de8ff27` |
| OCI archive | 322922496 bytes／`48f4d808ff3d5a992c09101d075dfcd7d5c4ce4e91b907691fbf393db0b1f390` | 324857856 bytes／`00f1b4afd50663bb2cf975d7e7bb0db9e409a283493853651b9d14c90e648f23` |
| GUI tar | 138376671 bytes／`c0d08c26b0d016c7cf4f57661022c631be0f2aa3d1d7d517ce97fd75e118c75d` | bytes／SHAとも同一 |
| amd64 最後のlayer | `sha256:cdb149aa0817af22517e725c7d8c76498451ba9070dbc4b4ed2a20ede2c8b37f` | `sha256:44162b9203117753ac6d1dc2af36d0718b0dd2a177911e907d5b5f4084b280f1` |
| arm64 最後のlayer | `sha256:ac2c682b5f6bb4f60976b08da483049a762425f9fa7ce7e4b33bb87d34e6ec85` | `sha256:2898029c1cadfd00c089acbf3359b11bce903b88ac4b2780ad9d08fbab559055` |

OCI configではversionラベル、version引数／LABELの生成履歴、作成時刻、EXPOSE生成履歴のhex表記、COPY layerに対応する`rootfs.diff_ids[9]`が異なる。他のruntime config差は無かった。CI比較helperの最初のmetadata分類はARG／EXPOSEの履歴差も厳しく拒否したため、そのraw結果を別fileで保持し、手元の再照合でversion由来のARGとEXPOSE履歴のhex表記差を生成metadataとして分類し直した。layer／rootfsのdigest不一致という停止根拠は変わらない。

比較run: https://github.com/Naohiro2g/scratch-editor/actions/runs/37267805360 。結果artifact ID `11326788484`、2,312 bytes／SHA-256 `0aa3c57bd68c213cb78c867b6b53aa38411ea71e8bf5b39f8bda5410bf480dac`。公開前build run: https://github.com/Naohiro2g/scratch-editor/actions/runs/37266780367 。artifact ID `11327285872`、575,032,028 bytes／SHA-256 `846a09c29f1c19b6fee793c80863ced6950bed0c33b4207c318b8b05eec1ce1b`。
