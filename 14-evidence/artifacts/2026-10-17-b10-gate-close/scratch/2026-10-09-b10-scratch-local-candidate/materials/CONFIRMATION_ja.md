## Release gate 確認票（Scratch Local candidateの固定）

- 対象 repo: `Naohiro2g/scratch-editor`
- 対象 branch/commit: `agent/b10-scratch-local@c717d0c2ed9b045b8c3bb925b0e1fcd8ee33010b`。commit／push済み、GitHub branch ref一致。前の`2592b64d280d85daa1730c59a1d89948cada826a`は承認済みお知らせ整理を分けたcommit
- release / channel: `2320.0.0b10`／prerelease準備、tag／Release未作成
- gate coordinator: knowledge担当session
- human release owner: プロジェクトオーナー
- current phase: 簡易版をcommitし、CI candidateを生成、3 ZIPのidentityを実体で照合して固定済み。人間参加の実施票待ち
- contract maturity / required test tier: b10ケータリング型簡易版の配布形・manifest v2は確定。本票の検証はunit/deterministic。3 OSの操作と配布前ライセンスの最終確認は後続
- knowledge contract path: `00-hub/release-gate-notes_ja.md` b10「次の操作」（2026-10-08）／「release manifest v2の形」。ライセンスはDEC `2026-08-11-01`
- knowledge contract commit: `5e248a9cd9243c1ca654abfbed65ee2646087316`（remote mainからruntime・INDEX・該当gate・DECを実読）
- gate manifest identity: 横断exact setを本票では作成していない。component candidateは下のActions artifact ID／digestと3 ZIPのbytes／SHA-256で固定
- change cone: Scratch Localランチャー・setup／案内、3 OSの公式Node入力lock、ZIP生成・取得・検査、manifest v2契約consumer、candidate／公開workflow、GUIのclient診断版。wire API、Bridge／WireScopeのsource・artifact pinは不変。お知らせの承認済み削除は別commit
- reused PASS / rationale: 旧dirty試作ZIPを入力にせず、上のsourceからCIで全workspaceをビルドし3 ZIPを生成。旧Linux観測をこのZIPの観測へ付け替えない。今回のLinux ZIPはCIで新たに模擬peerと決定論的に検査した
- exact compatibility set / freeze status: Scratch component candidateのidentityを固定。横断setの凍結と公開判定はcoordinator。3 OS実施前
- target deployment / profile / lock:
  - 各PCのHTTP／WSはlocalhost、認証ON・従来のペアリングを維持。人間の接続・pairingは今回していない
  - `mc-remote/local-runtime-lock.json`: 745 bytes／`86fed4a5cd301779bcbac9d5bd94bcc29794e0d5b326f0ab24f30091ada6d923`
  - `mc-remote/tooling-lock.json`: 3763 bytes／`5bd219b9c68eb804f0ff5ce5dd0973b5d38d68c4dfcb941e2fb9dd0772cb6c3c`
  - `mc-remote/release-manifest-lock.json`: 1411 bytes／`c7de38a3316656d183632b4ca58e8904d67ae722cc9e9959a03fff626ab39298`
  - Bridge／WireScopeのtooling source `dc1ab834183e29f2eb03059b07e99d2b463776ee`、manifest専用source `5f567f14adaa24603e9dee3c0ec9909d428b7c4b`は維持
- authorized next action: human ownerが許可した実装commit、license135件の分類、CI candidate生成・3 ZIP固定を実施。Windows11／macOS／Linuxの実施はcoordinatorの実施票を待つ
- test class: unit/deterministic。GitHub APIと取得したartifact本体によるidentity確認
- 実行した command / 手順:
  - Scratch VM: `npx tap --disable-coverage test/unit/extension_mcremote.js`
  - GUI: config-contract／runtime-config／notice-overlayの3 suiteをJest `--runInBand --runTestsByPath`で実行
  - Node: ランチャー／ローカルartifact選択と収集／既存tooling取得／candidate生成の5 fileを`node --test --test-isolation=none`で実行
  - `npm run release-manifest:test`、`python3 scripts/build-mcremote-local.test.py`、`npm run local:lint`、`npm run release-manifest:lint`
  - workflowのYAML parseと20 run bodyの`bash -n`。新しいライセンスguardは先に3 failureを再現してから実装
  - `gh workflow run mc-remote-candidate.yml --repo Naohiro2g/scratch-editor --ref agent/b10-scratch-local`
  - GitHubのrun／artifact metadataと外側ZIPを取得し、raw digestを照合。全candidate manifest artifact、ZIP sidecar、内部identity、source archive、Node binary arch、補完license fileを照合
- 結果:
  - 手元の対象tests 687 PASS（VM532／GUI39／Node17／manifest93／Python6）、local／manifest lint、workflow構文、補完license hash PASS
  - 初回VM sandboxは全skipだったため制限外で532 PASSを確認。GUI初回1 suiteはfile path誤りを実fileへ修正し3 suite39 PASSを確認。skip／path誤りをPASSへ数えない
  - CI [run 37808012407](https://github.com/Naohiro2g/scratch-editor/actions/runs/37808012407) success、source SHA一致。全workspace production build、consumer／launcher／archive test、Bridge digest維持、3 ZIP生成、Linux ZIP模擬接続、Scratch OCI生成、収集・uploadが全成功
  - 3 ZIPのhashはCI producer log／sidecar／candidate manifest／取得したraw bytesで一致。全て`working_tree_dirty:false`
  - Node binaryはWindows PE x64、macOS Mach-O arm64、Linux ELF x64を実体で確認。Node `24.19.0`は公式archiveから変更せず抽出
  - 3 ZIPの同梱Scratch source archiveは全てSHA-256 `ba5af6dcb7ad0b7e93255e66b7eb629463eabfdab7f2cd1357544df675e44cfb`。Node／Scratch／Bridge／wsの本文、Scratch商標案内、補完本文・noticeと出典、対応source導線を確認
  - LinuxのCI試験は日本語・空白を含む展開pathでランチャーを起動し、HTTP配信・GUI/config・固定BridgeのWS→模擬TCP hello・終了・ポート解放を確認。実MC・pairing・OS download警告ではない
- evidence record / artifact: 本packetの`CI_RUN.json`／`CI_ARTIFACT.json`／`CANDIDATE_VERIFICATION.json`／`candidate-manifest.json`／`logs/`、license照合2表と補完出典、`SOURCE_INPUTS.json`。dev捕捉素材であり、正式evidence配置・authoringはknowledge担当
- 未検証の境界: Windows11／macOS／Linuxの初回取得・展開・起動警告・実行権限・firewall・接続先・実MC・pairing・再起動・1台/LAN構成、実browserによるScratch操作、公開workflow・tag／Release・shared deploy。microee原BSD本文・条項数は未確定
- security / compatibility / rollback の確認: localhostのみ待受け、設定はhost／portのみでtokenを保存しない。HTTP Host／POST Origin／path境界をunitで確認。固定manifest／tooling／runtime入力のbytes・hashを照合。公開workflowは指定artifactから同一ZIPを収集し、dirty／source／digest不一致を拒否。既存b8/b9サービス・shared・user未追跡2件は変更なし
- 判定を求める事項: 固定した下の3 ZIPで、Windows11／macOS／Linuxの実施票を出す段階へ進めるか。公開前license確認としてmicroee1件を返す。OS実施・公開許可・横断GREENを本票では判定しない

## 固定したCI artifact

- workflow file: `.github/workflows/mc-remote-candidate.yml`
- run: `37808012407`、run attempt `1`、conclusion `success`
- artifact name: `scratch-candidate-c717d0c2ed9b045b8c3bb925b0e1fcd8ee33010b`
- artifact ID: `11563852835`
- outer bytes: `1361803350`
- outer SHA-256 / provider digest: `sha256:75b1df3df6d659514ee6eb3a2913a7d9bf6e062a449316c352e9a59078a89aea`（取得した外側ZIPと一致）
- expire状態: provider取得時`expired:false`。Releaseへはまだ添付していない
- GitHubのrunのArtifactsから取得、またはCLIで同じIDを指定。公開収集workflowの`local_candidate_artifact_id`／`local_candidate_artifact_digest`へ将来渡す値

## 固定した3 ZIP

| OS/arch | file | bytes | SHA-256 |
| --- | --- | ---: | --- |
| windows-x64 | mc-remote-scratch-local-2320.0.0b10-windows-x64.zip | 260361934 | `08340c801c1196c30a1227a7e495feb32131a95e4816ffbb29278557cadab9c1` |
| macos-arm64 | mc-remote-scratch-local-2320.0.0b10-macos-arm64.zip | 264713598 | `60d69479079eb5f7b7022547d417abc5dc31b237eb12766354885e4db53e6908` |
| linux-x64 | mc-remote-scratch-local-2320.0.0b10-linux-x64.zip | 269950028 | `245d83aeab8f6a10bc3703547e0f897b3e82a8c9152c1a131378454f0debdf8b` |

照合済みの実fileとsidecarはscratch-editorの`candidate/ci-37808012407/`に保持。
このdirectoryはGit管理外の配布入力です。公開時に再buildして同じversion名で置き換えないでください。

## ライセンス135件の分類と充足

- 元135件をname/versionの出現数で全件照合。元票にinstallation locationが無いため、特定の旧pathの同一性は主張しない
- 手元入力は132件（runtime26／buildのみ106）。同梱した最終CI入力は130件（runtime26／buildのみ104）。ZIP内`licenses/review.json`を正とする
- 元135→CI130で減った5 instanceはbuild入力。`@rolldown/binding-linux-x64-gnu@1.0.0-beta.53`3 instance、`@napi-rs/wasm-runtime@1.1.1`1、`@tybys/wasm-util@0.10.1`1が不足表から減った。具体的な旧installation locationは元票からは復元できない
- runtime26: 全て本文／publisher attributionを補完し出典とhashを固定。同梱の補完fileを全3 ZIPで照合。元bundleのLICENSE.txtとソース内noticeを維持
- buildのみ104: 配布codeに入ったという主張をせず、root本文が無いものは`not-distributed`として記録。ソースは同梱せず、名前・版・宣言・分類をinventoryに残す
- 補完の出典: 対応公開sourceの本文10 component、公式projectの固定した後続本文6、宣言に対応するSPDX標準本文7、元README内の本文2、BSD条項未確定1。原作者の情報はpackage metadataで保持しcopyrightを創作しない
- 未確定1: `microee 0.0.6`の原表記「BSD」。公式sourceに原本文／条項数が見つからず、BSD-3-Clause標準本文は参照用として収容。このcomponentをBSD-3-Clauseへ変更したという主張や、配布前license gateのPASSはしない。noticeと`open_reviews`に明記
- 判定入力: `ORIGINAL_135_CI_RECONCILIATION.json`（135全件）、`CI_LICENSE_REVIEW.json`（最終CI130件）、`LICENSE_SUPPLEMENTS.json`（26 componentの本文／notice／出典／hash）。手元時点の`LICENSE_CLASSIFICATION.json`は132件の旧入力として保持

## その他のcandidate同梱物

全て取得したraw bytesをmanifestと照合しました。Bridge／WireScopeは既存lockで固定した入力です。

| role | file | bytes | SHA-256 | OCI digest（ある場合） |
| --- | --- | ---: | --- | --- |
| scratch-gui | scratch-gui.tar.gz | 138368101 | `21efc8831c839d86afafb4c89bc8e9e8adad0cee4764b085c819854137135256` | — |
| scratch | scratch.oci.tar | 322935808 | `29767113dab795dbda1ff3c404c13a2b4392386a1f32b44879e95877f23b2eac` | `sha256:78be826b8802ae72b5f23d713b35d8330735eef85b4c47957f012a0c7c247314` |
| bridge | bridge.oci.tar | 114628096 | `b6a6feec07e8d7ae9805a81e8dc370e6220e91af145ef3117ce5ed12e703b100` | `sha256:5828304c9bb1d60df8672f9189f503790050e09358bd375f39e4d59d190eb84f` |
| wirescope | wirescope-app.zip | 83854 | `da3da0b6cf4d05265bc0c11abaa4913208c7cfc3600b0c3e78c93a356fc431ad` | — |
| wirescope-manifest | wirescope-app.manifest.json | 2339 | `c654f7d1f0be2773d6737e889279b2587317088717f162b082c82be9cff910d7` | — |
| contracts | contracts.tar.gz | 1908 | `48948ba47d55409f02a8ff8e0d44021b07859e11ffa5ca0f8598e6ef06082390` | — |
