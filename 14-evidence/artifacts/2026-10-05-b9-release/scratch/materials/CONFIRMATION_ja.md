## Release gate 確認票（b9公開・事前照合で停止）

- 対象 repo: `Naohiro2g/scratch-editor`、公開順序の先行対象 `Naohiro2g/minecraft-remote-tooling`
- 対象 branch/commit: Scratch `develop@7fbbf034488760d8fc7e034bf23f3e08e6e1807d`、tooling `main@dc1ab834183e29f2eb03059b07e99d2b463776ee`。remote refをGitHub APIで照合し、ともに凍結sourceと一致
- release / channel: `2320.0.0b9`／GitHub prerelease、予定tag `v2320.0.0b9`。公開操作は未実施
- gate coordinator: knowledge担当session
- human release owner: プロジェクトオーナー
- current phase: 公開承認済み。公開前の入力照合で停止
- contract maturity / required test tier: 批准済み。凍結artifactと公開artifactのidentity照合
- knowledge contract path: `00-hub/dev-repo-protocol_ja.md`のDEV-AGENT-RUNTIME、`00-hub/release-gate-notes_ja.md`のb9節「exact set凍結」「実機試験」「判定」「release authorization」
- knowledge contract commit: `d6d59d91032230a959b7288807179e1bd8100041`（remote mainから取得し、実際に読んだpush済みSHA）
- gate manifest identity: `b9-integrated-artifact-set-1`。Scratch candidate manifest 1,821 bytes／SHA-256 `239f7f94cf31e732eff173744da105408b00b182d0aad73507623ea09b43bc6b`
- change cone: 公開workflowのScratch OCI build引数。製品code、fixture、Bridge、WireScopeへの変更なし
- reused PASS / rationale: knowledgeのsegment 0〜3 PASS／GREENの記録を参照。Bridgeのhost-native観測はhuman ownerが採用し、container起動はVPSベータdeployで確認するとの判断も参照した。今回live／unitは再実行していない
- exact compatibility set / freeze status: 凍結済み。Scratch OCI `sha256:6702b112ad53b48efa2bf99fc0145fc7b23d24a1d20743018582f781f61c9e34`、Bridge OCI `sha256:5828304c9bb1d60df8672f9189f503790050e09358bd375f39e4d59d190eb84f`、WireScope ZIP `da3da0b6cf4d05265bc0c11abaa4913208c7cfc3600b0c3e78c93a356fc431ad`、detached manifest `c654f7d1f0be2773d6737e889279b2587317088717f162b082c82be9cff910d7`
- target deployment / profile / lock: GitHub Release／GHCRの公開。sharedやlocalhostの稼働サービスには変更なし
- authorized next action: 指示票の「一致しないものが出たら、公開せずに止めてcoordinatorへ返す」に従い、本票を返す。固定workflowの変更やexact setの置換は実施しない
- test class: static／artifact identity inspection。公開workflowの実行試験ではない
- 実行した command / 手順: 凍結sourceのcandidate／release workflowをGitHub Contents APIで取得し、local sourceとの一致を確認。`python3 materials/audit-release-inputs.py`でCI candidate内のScratch OCI archiveのbytes／SHA-256、凍結index blob、amd64／arm64両configのdigest・revision・version label、remote source refsを照合。GitHubのtag refと直近Release一覧を読み取り
- 結果: 事前照合でSTOP。candidateは`RELEASE_VERSION=2320.0.0b9`、公開workflowは`RELEASE_VERSION=${{ steps.release.outputs.tag }}`で予定tagから`v2320.0.0b9`になる。Dockerfileはこの引数を`org.opencontainers.image.version`へ入れる。両configのラベルが変わるため、凍結Scratch OCIの同じdigestにはならない
- evidence record / artifact: 搬送素材 `handoff-materials/2026-10-05-b9-release/`。`materials/release-input-audit.json`、凍結workflow2件、remote ref4件、監査script。bytes／SHA-256は`INVENTORY.json`と`SHA256SUMS`。正式evidence authoringはknowledge側
- 未検証の境界: 新しいOCIはbuildしておらず、新digestの実測値は無い。tag、Release、registry upload、固定workflowの公開実行は未実施。再buildの時刻／provenance等がもたらす差は今回測定していない。version引数のprefixだけを修正すれば全体digestが再現できるとは主張しない
- security / compatibility / rollback の確認: token、credential、private接続先を読出し／変更していない。公開repo source／branch／tagに変更なし。APIのtag照合結果は両repoとも空、直近Release一覧に予定b9 tagは無かった。通常devやlocalhostサービスにも変更なし
- 判定を求める事項: 凍結Scratch OCI archiveをそのままregistryへ移す公開経路にするか、公開workflowによる再buildをpackaging差として扱い、生成後の新identityをcoordinatorが採用するか。前者ならBridgeと同様にdigestを維持したcopyを使う案。いずれも公開手順とfreezeの扱いをcoordinatorが確定してから再開する。repo側では横断判定を変更しない

具体的な不一致:

| 対象 | 凍結candidate | 公開workflowの入力 |
| --- | --- | --- |
| source revision | `7fbbf034488760d8fc7e034bf23f3e08e6e1807d` | 同一sourceを指定する |
| `RELEASE_VERSION` | `2320.0.0b9` | `v2320.0.0b9` |
| `org.opencontainers.image.version` | archiveのamd64／arm64両configで`2320.0.0b9`を実測 | Dockerfileにより`v2320.0.0b9`になる |
| OCI index digest | `sha256:6702b112ad53b48efa2bf99fc0145fc7b23d24a1d20743018582f781f61c9e34` | 未生成。同じconfig digestは維持できない |

今回、tooling→Scratchという順序の公開操作を開始する前に検出したため、両repoのtag／Release／registryには書き込んでいない。
