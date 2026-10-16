## Release gate 確認票（Scratch Local：WireScope同梱candidateの追記）

- 対象 repo: `Naohiro2g/scratch-editor`
- 対象 branch/commit: `agent/b10-scratch-local@ec29372dadac9c51b2812c746e72032d48d987b6`（push済み）
- release / channel: `2320.0.0b10`／candidate、未公開
- gate coordinator: knowledge coordinator
- human release owner: human owner
- current phase: 新candidateの生成・identity固定完了。横断setの凍結と次操作の許可待ち
- contract maturity / required test tier: DECISIONS `2026-10-09-01`確定。今回の実装はunit/deterministicとCIの実ZIP試験。次段の3 OSはlive-human
- knowledge contract path: `00-hub/DECISIONS_ja.md` `2026-10-09-01`、`00-hub/release-gate-notes_ja.md` b10「初回のlive-human」「次の操作（2026-10-09）」、`00-hub/b10-gate-live-test-instructions_ja.md`、`15-wirescope/wirescope-deployment-design_ja.md` §5・§6
- knowledge contract commit: `8c3a31a967731a81c91645b08ecff62f620d0fe4`（remote main一致、runtime・決定・gateを実読）
- gate manifest identity: `materials/candidate-manifest.json`（新candidate、全artifactのbytes／SHA-256を本体で照合。横断gate manifestは未発行）
- change cone: Scratch LocalのZIP builder、launcher、Linux実ZIP試験と案内。固定済み共通WireScope appを無変更で同梱、別loopback originで配信し`wirescope_url`を設定。Scratch VM／GUI、protocol、common tooling sourceとwireは変更なし
- reused PASS / rationale: 初回live-humanの観測は引き継がない（coordinatorの指示）。NodeとBridgeの同一性は旧ZIPとのbyte比較で確認したが、人間参加試験の代替とはしない
- exact compatibility set / freeze status: Scratch componentの新source／3 ZIPを下記identityで固定。横断setの凍結はcoordinatorへ返す
- target deployment / profile / lock: 1台構成とLAN構成のScratch Local、全listenerは`127.0.0.1`のみ。Scratch8601／Bridge8602／WireScope8603。`mc-remote/tooling-lock.json`（tooling `dc1ab834183e29f2eb03059b07e99d2b463776ee`）とNode runtime lockは変更なし
- authorized next action: Scratch同梱修正、新candidate CI生成、identity返却まで実施。tag／Release、shared deploy、人間参加試験は次の許可が出るまで実施しない
- test class: unit/deterministic（CIのWS→TCP peerは模擬サーバー。live-auto／live-humanとは数えない）
- 実行した command / 手順: `npm run local:test`、`npm run local:lint`、固定WireScope pair／6 assetの生成関数での照合、固定workflow `mc-remote-candidate.yml`のdispatch、API metadata取得、artifact本体の取得・全candidate manifest hash照合
- 結果: 手元Node13＋Python8＝21 PASS、lint PASS。CIのmanifest93＋consumer Node19＋Python8 PASS、manifest/local lint PASS、本番build PASS。CIのLinux実ZIPは日本語・空白pathで起動、GUIとconfig、別originのWireScopeと全assetの配信hash、固定BridgeのWS→TCP往復、終了と3 port解放PASS
- evidence record / artifact: 本packetはdev観測素材。`materials/CONFIRMATION_ja.md`、`ZIP_IDENTITIES.json`、`artifact-verification.json`、`provider-run.json`、`provider-artifact.json`、`ci-linux-zip-test.log`、`ci-consumer-tests.log`、local test／lint log。正式recordのauthoring／収容はknowledge coordinatorへ返す
- 未検証の境界: 新ZIPのWindows11／macOS／Linuxでの取得・OS警告・認証ONの実McRemote接続・ペアリング・ScratchからのクリックによるWireScope handoff・実画面・再起動・LAN。McRemoteのWindows credential障害は他担当の調査対象。横断GREENは主張しない
- security / compatibility / rollback の確認: 共通appのLICENSE／NOTICE、detached manifestと固定ZIPを保持。配信用6 fileも全て固定manifestと一致。Node／Bridgeの各fileは旧candidateの同OS ZIPとbyte一致。port競合時は既存serviceを維持して起動失敗、Scratch listenerを解放。静的fileは各root内のみ配信、WireScope側に設定POSTを置かず、openerを切断するheaderも追加しない。ブラウザのcredential保存originを維持。credential storeやserver configは変更していない。`microee`の原BSD表記と参照本文は承認どおり保持
- 判定を求める事項: McRemote新candidateがそろった後のexact setと、3 OS再実施の許可・実施票更新。初回観測は新candidateへ引き継がず履歴として保持

### CIとartifactのidentity

- CI run: [37933218014](https://github.com/Naohiro2g/scratch-editor/actions/runs/37933218014)、source `ec29372dadac9c51b2812c746e72032d48d987b6`、status completed／conclusion success
- Actions artifact: `scratch-candidate-ec29372dadac9c51b2812c746e72032d48d987b6`、ID `11616819485`、1362315280 bytes
- provider digest: `sha256:f747f3b537b060aacfa24bbcdbc1e42575169d7cd11b5d3219fdb6a7c0767159`。ダウンロードした外側ZIPのSHA-256も一致
- source／run／name／期限と外側digest、candidate manifestの全artifact、3 ZIPのsidecar／内部identity／source archive hash／Node architecture／補完license hashを照合PASS
- 新3 ZIPの実体: `candidate/ci-37933218014/`（git管理外、正式evidenceではない）

### Scratch Local ZIP（role `scratch-local`、kind `file`）

| OS／arch | file | bytes | SHA-256 |
| --- | --- | ---: | --- |
| windows-x64 | `mc-remote-scratch-local-2320.0.0b10-windows-x64.zip` | 260532718 | `f9d09ee84eb8cc54324c6b9d83dc3ab9371d7592ec0535346cf527d3db931a77` |
| macos-arm64 | `mc-remote-scratch-local-2320.0.0b10-macos-arm64.zip` | 264884384 | `16e20e5b2ecbfe1a7070d18f3700739bf2d4d567920347398e7ff82d1a40edc0` |
| linux-x64 | `mc-remote-scratch-local-2320.0.0b10-linux-x64.zip` | 270120781 | `3717f4dd55c0996c8e35ce121f293b06ed78e1a1c1bd7e4dad8c1a297fc186fc` |

全ZIPの`working_tree_dirty`は`false`、versionは`2320.0.0b10`、sourceは`ec29372dadac9c51b2812c746e72032d48d987b6`。3 OSすべてで固定WireScope pairと配信用6 assetを再照合した。

### 変更していない共通WireScope入力

- `wirescope-app.zip`: 83854 bytes／SHA-256 `da3da0b6cf4d05265bc0c11abaa4913208c7cfc3600b0c3e78c93a356fc431ad`
- `wirescope-app.manifest.json`: 2339 bytes／SHA-256 `c654f7d1f0be2773d6737e889279b2587317088717f162b082c82be9cff910d7`

共通sourceは`dc1ab834183e29f2eb03059b07e99d2b463776ee`。3 ZIPの中に同じbytesのpair、LICENSE／NOTICEを含む配信用fileとsource参照を収めた。WireScopeのsourceもartifactも作り直していない。
