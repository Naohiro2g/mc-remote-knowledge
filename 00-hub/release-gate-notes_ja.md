# Release gate notes — public baseline

> 新public正本世代の単一template／状態集約。旧世代のrelease固有履歴はcarryしない。

release判定は、実装repo側が事実と根拠を記入し、単一のgate coordinatorがknowledge側で
contractと照合します。shared環境へのcandidate deployと人間参加試験は、coordinatorがexact setと
許可済みの次操作を示した後に行います。責務と正準進行は
[release運用と責務分担](release-operations-responsibility-design_ja.md)を参照します。
秘密実値、private inventory、未sanitized raw logはここへ貼りません。

## 確認票

```markdown
## Release gate 確認票

- 対象 repo:
- 対象 branch/commit:
- release / channel:
- gate coordinator:
- human release owner:
- current phase:
- contract maturity / required test tier:
- knowledge contract path:
- knowledge contract commit:
- gate manifest identity:
- change cone:
- reused PASS / rationale:
- exact compatibility set / freeze status:
- target deployment / profile / lock:
- authorized next action:
- test class: unit/deterministic / live-auto / live-human
- 実行した command / 手順:
- 結果:
- evidence record / artifact:
- 未検証の境界:
- security / compatibility / rollback の確認:
- 判定を求める事項:
```

`live-human` や高い再現コストを持つ検証は `14-evidence/` の sanitized record を参照します。private evidence は `mc-remote-backstage`、秘密を含む raw は Git 外です（`2026-07-06-03` / `2026-07-21-04`）。

repo担当は自repoの事実と根拠を返し、他repoの着手、shared環境へのdeploy、人間参加試験、横断判定を
開始しません。candidate identityが変わった場合は旧exact setを失効させ、gate coordinatorへ戻します。
ただし旧setの観測事実まで自動的に破棄せず、`2026-08-23-01`のchange coneとPASS再利用条件で再評価します。
仕様形成中はTier 0〜2を既定とし、人間参加・全回帰・capacity／soakをrelease候補より前へ自動的に持ち込みません。

## 2026-08-27 b6横断release gate（OPEN）

- gate coordinator: knowledge担当session。人間による明示handoffなしに他担当へ移さない
- human release owner: プロジェクトオーナー
- current phase: **未公開artifact candidate set 1のTier 2製品pulse進行中／partial PASS**。通常devのruntime readiness、exact Python wheelによるsign三操作／`mcr_eh_`、exact Bridgeによるprotocol 23 plugin一往復までPASSした。Scratch実ブラウザ／WireScope、`pickaxe_poke`人間操作、default branch統合、release判定は未着手で、横断gateはOPENを維持する
- contract maturity / required test tier: b6 wire contract、共有fixture、candidate bytes、target、server runtime identityは固定・照合済みで、根本仕様へ戻さない。workstation側exact artifactを起動し、最小横断pulseへ進む。横断`GREEN`やTier 3完了は主張しない
- knowledge contract: `10-protocol/versioning-design_ja.md` §10.11.4、`10-protocol/wire-format-design_ja.md` §5.4／§5.8／§7.3、`10-protocol/beta-to-stable-release-roadmap_ja.md` §3.1、`10-protocol/b6-compatibility-fixture-plan_ja.md`、`15-wirescope/wirescope-deployment-design_ja.md` §14。DECISIONS `2026-08-26-05`／`2026-08-26-06`／`2026-08-26-08`／`2026-08-27-01`／`2026-08-27-02`／`2026-08-27-03`。core b6 contract baselineは`b47d979c6779842e9eea892e90f69f0bdbd4dc4b`
- gate manifest identity: `b6-artifact-candidate-set-1`。`b6-source-candidate-set-3`から生成した未公開candidate bytesを指す。人間可読のbinding recordは`10-protocol/b6-artifact-candidate-record_ja.md`であり、machine-readable gate manifest完成や公開releaseを意味しない
- exact compatibility set / freeze status: **Tier 2投入用candidate setとして凍結**。McRemote `codex/b6-protocol23-cleanup@88d818703be5e7314bc1e45597a66237796db641`、Python `codex/b6-protocol23-python@0ba22e80b9b1b339dfd11085b1b24cef646599b2`、Scratch `agent/b6-source-refresh@104f194deddc9c244e6e07c4223965c792551f9d`。protocol `23.0.0`、artifact version `2300.0.0b6`。七artifactのexact name／size／SHA-256はcandidate記録を正とする。いずれかのsource、fixtureまたはartifact bytesが変わればset 1を失効させる。公開release artifact freezeは未実施
- component readiness:
  - McRemote: source `88d818…`からJAR `mc-remote-1.21.11-2300.0.0b6.jar`（204,341 bytes、SHA-256 `4e28603caefa4273fabfe325e1c75a28239a6fa9eb44fb5a2b49da7be79870e8`）を生成した。全143/143 PASS、独立clean build三回一致。通常devへ配置し、runtime identity／credential health／auth否定パスと、Python／Bridgeからの実接続をPASSした。poke人間操作、rollback、releaseは未実施
  - Python: source `0ba22e…`からwheel（173,301 bytes、SHA-256 `0887807f0d00f71fcb543caf16c3963b70580bf073b6a7576d7f274399a1877b`）とsdist（178,483 bytes、SHA-256 `0507a10cbd6b31c2dd84ebff0034c5f72625ff1142d30f1c0d41e14d0ce2da3b`）を生成した。全242/242 PASS、別venv install smoke、独立二build一致。exact wheelをisolated Python `3.11.5`へinstallし、人間pairing後のhello、sign full-style get／set、1行PATCH、`mcr_eh_` handle、試験block復元を実pluginでPASSした。公開、default branch統合、releaseは未実施
  - Scratch: source `104f194…`からGUI tar（234,622,982 bytes、SHA-256 `3ba9940ebd2d60f70e20a45a5a29f1d2614caf79b5c87f13236139994d40f617`）、Bridge tar（3,052 bytes、`11199a8e…31c72`）、WireScope ZIP（73,525 bytes、`06a6fb44…b7d`）とmanifest（2,321 bytes、`a4440a27…cad7`）を生成した。GUI unit 471/472（既知skip 1）、Bridge 30/30、lint error 0、各artifact複数回生成一致。exact GUI／Bridge／WireScopeをloopback起動し、deployment-owned b6 configとHTTP到達性を確認、Bridge one-shotから実pluginの`auth_required`までPASSした。Scratch／WireScope実ブラウザE2E、公開、default branch統合、releaseは未実施
- change cone: b6必須はsign三操作、`pickaxe_poke`、Scratch project／sprite browser保存、protocol 23 cleanup。WireScope表示filter／`dropped_frames`／mini配置改善は同じScratch sourceに含まれるclient-only companionであり、server wireを変更しない
- reused PASS / rationale: 上記component PASSは各申告sourceの局所事実として保持する。共有contract適合、candidate artifact、実plugin接続の代用には使わない。Scratch全体並列実行3件は全件PASSと書き換えず、単独再実行結果と既知flakinessの主張範囲を分けて保持する
- canonical case audit: `10-protocol/b6-compatibility-fixture-plan_ja.md`。protocol／artifact identity、handle、sign、`pickaxe_poke`、legacy method不在をcase IDへ分け、set 1のgap、set 2のowner発行と投影、`data.allowed`追補、set 3のPASSまで記録した。根本wire shapeの再設計を要求する差分はない
- shared fixture owner: Scratch `agent/b6-source-refresh@104f194d…`の`@mc-remote/protocol/test/fixtures/`。`sign-v23.json`はSHA-256 `7ffb63c264602cba56117eefff1f9604b955df04c5cc655e877772b8ff7cd30e`、`events-v23.json`は`31760d267f3c2641042fbe8595fda9c259134a1c05423271a99cb74da1efa9aa`。三repoの配置bytes、case接続、McRemote productionのsign error順を照合し、共有fixture gate PASS
- target and preflight: 人間承認により論理deployment `dev-integration`、物理host `m720s2`、host-native `run.sh`＋Screen runtimeを再利用する。2026-08-27のread-only preflightでは旧systemd版はinactive、`Minecraft server` Screen sessionと標準port `25565`／`25575`が稼働中で、Paper JARはb5と同じSHA-256 `5ffef465eeeb5f2a3c23a24419d97c51afd7dbb4923ff42df9a3f58bba1ccfba`、現行b5 McRemote JARは公開releaseと同じ`f7ddbcb5a92acadfe1adb7a9f6a4f50a05707e2eefbd1c01ff9aeeebe0a36547`だった。private address、player UUID等のraw log値は本票へ収録しない
- staging and runtime result: workstationのdurable gate stagingへ七artifactを置き、全size／SHA-256を再照合した。server側はconsoleの`stop`でb5を正常停止し、b5 JARを`plugins`外へ二copy保持、McRemote JAR一件だけをb6へ交換した。Paper JARは同一digest、world／config／credential backendは変更していない。`run.sh`再起動後、Paper `1.21.11-132`、McRemote `1.21.11-2300.0.0b6`、credential `HEALTHY`、Screen、両listenerを確認した。workstationからprotocol `23.0.0`でtokenなし=`auth_required`、bogus／旧`mcrp_`=`token_not_found`、malformed=`token_invalid`をPASSした。最初のSSH aliasを通常DNS名として使ったprobe失敗は接続前の名前解決差で、SSH設定からaddressを解決した再試験でPASSした。rawのprivate address／UUIDは収録しない
- authorized next action: 同じset 1と起動済みruntimeを使い、実ブラウザでScratch pairing、text-only sign surface、browser保存の代表操作、WireScope mini／表示filter／`dropped_frames`を確認する。その後、人間がMinecraftへ参加できる時に`pickaxe_poke`一操作一eventと腕振りを確認する。Bridge tarが`dist/`だけでproduction dependencyを含まない点は、Tier 2ではexact source installの`ws 8.18.3`をruntime入力として固定したが、公開配布形態のartifact gateで閉じる。公開release、tag、registry upload、default branch統合は行わない。source修正が必要になればset 1を失効させ、新SHAでgateへ戻す
- resolved human decision: `2026-08-27-01`で現行WireScope表示filterをb6のclient-only UX v1として受理した。このfilter判断自体はScratch source変更を要求しない。後続のcontract監査で見つかった別gapによりset 2へのrefreshを要求するが、method／event分類、pair、検索、件数、保存stateは変更せず、正本を`15-wirescope/wirescope-deployment-design_ja.md` §14とする
- resolved observer boundary: 現行observer allowlistがb6 sign三操作を含まない点は、`2026-08-27-01`がallowlist拡張を含めないと明記した範囲どおり、b6では**WireScope v1の非必須観測範囲**と判定する。signの互換性はScratch APIと実worldで確認し、WireScope E2Eはhello／`pickaxe_poke`／現行allowlist method／`dropped_frames`を使う。filterの`world`分類からsign frame観測済みと推測せず、本判定を理由にScratch SHAを変えない
- evidence: `14-evidence/records/2026-08-27-b6-tier2-integration-pulse_ja.md`。server readiness、Python sign／handle、Bridge one-shotをformalに記録し、Scratch実ブラウザ／WireScope／poke未実施を同じrecordで明示した
- non-claim: Scratch／WireScope実ブラウザE2E、`pickaxe_poke`人間操作、Bridge dependency-complete公開package、公開release artifact freeze、default branch統合、b6 `GREEN`／releaseを主張しない
- rollback: 公開済みb5 exact release set。b6 rollback実操作は未実施

## 2026-08-21 b5横断release gate（CLOSED）

- gate coordinator: knowledge担当session。人間による明示handoffなしに他担当へ移さない
- human release owner: プロジェクトオーナー
- current phase: **b5 prerelease identity確認完了／技術gate close**。3 componentのGitHub prereleaseがexact setへ固定され、tag target、公開状態、Latest非対象、asset／release notes digestをAPIで確認した
- contract: 技術scopeはDECISIONS `2026-08-21-01`／`2026-08-21-02`／`2026-08-22-02`、進行責任は`2026-08-21-03`／`2026-08-21-04`。DimensionKeyの説明正本は`10-protocol/dimension-key-design_ja.md`
- exact compatibility set / freeze status: **凍結**。McRemote `bbbb53602a9c375e2ead3ee4c22174d5cf424f55`／JAR 195,998 bytes・SHA-256 `f7ddbcb5a92acadfe1adb7a9f6a4f50a05707e2eefbd1c01ff9aeeebe0a36547`、Scratch `1a11c46bac5696afd3f494caac56ae682ed00fb0`／CI run `32574020556`／GUI build artifact ID `9476135596`・digest `sha256:a5fef95460d2e07accd5eb82276def9eafa36692166e1db34e833447e6f6865e`／Bridge artifact ID `9476136894`・digest `sha256:2b84bf753ac67ea4906c9beb590cdb63d03da282015e40995ec129e3697b8e7b`／common WireScope ZIP `407031d5…a6964`・manifest `15d0c6b9…5bda`、Python `64b0f8831fa33e74f1b70b9102b3f29ec99b8e14`／wheel 170,271 bytes・SHA-256 `370f0fef3d5124a1024cbea8dfb4c65f2080cb545ab342086a827287d0f3f195`／sdist 175,715 bytes・SHA-256 `4337c6502f2be58e2bbf526d657c3f41d962bab08dd5a68eeb9527d66c9896b6`を一組とする。protocol `22.0.0`、artifact `2200.0.0b5`、observer schema／session／handoff／station attach version `1`、compatibility revision `v1.1`。いずれかのsourceまたはartifact identityが変わればこのfreezeを失効させる
- landing verification: `2026-08-21-03`／`2026-08-21-04`の責務契約は全担当で一致。McRemote、Python、Scratch／WireScopeはknowledge `f9d5dc7780ab2673b8872dc7481d230e10ca95d9`とremote mainの一致、`2026-08-22-02`との設計差分なしを確認した。各返却で列挙された差分はknowledge契約の不一致ではなく、旧world契約candidateの未追従実装である。設計再検討へ戻さず、3担当の実装とpush済みidentity返却を許可する
- DimensionKey component refresh:
  - McRemote: **candidate入力固定済み**。remote branch `codex/b5-reproducible-jar@bbbb53602a9c375e2ead3ee4c22174d5cf424f55`。共通DimensionRef codec／resolver、`Bukkit.getWorld(NamespacedKey)`、`build.setDimension`、hello／build context／player／event／entity handleの`dimension`、`unknown_dimension`／`entity_dimension_changed`を実装し、旧method／field／alias／fallbackを撤去した。Java 95 tests、runner 4 tests、clean build、構文検査、diff check PASS。独立clean checkout 2件のJARはbyte-for-byte一致。JARは195,998 bytes／SHA-256 `f7ddbcb5a92acadfe1adb7a9f6a4f50a05707e2eefbd1c01ff9aeeebe0a36547`
  - Scratch／WireScope: **candidate入力固定済み**。remote branch `agent/b5-protocol22-block-value@1a11c46bac5696afd3f494caac56ae682ed00fb0`。DimensionKey command／DTO／build context、標準menuと一般namespace自由入力、validator／adapter／表示を同時更新し、旧union／alias／shimを撤去した。CI run `32574020556`は全job PASS。GUI build artifact ID `9476135596`／digest `sha256:a5fef95460d2e07accd5eb82276def9eafa36692166e1db34e833447e6f6865e`、Bridge artifact ID `9476136894`／digest `sha256:2b84bf753ac67ea4906c9beb590cdb63d03da282015e40995ec129e3697b8e7b`。common WireScope ZIPは59,836 bytes／SHA-256 `407031d5e64279d90572f0843c788d2e4d9daac5b1ad12ffa121fa7f9fca6964`、manifestは2,321 bytes／SHA-256 `15d0c6b9a46ee68ac93dc850c9c5014c46476f7af1a49c7e98b2397cd7f95bda`。同一commitから2回生成してbyte-for-byte一致。observer schema／session、Scratch handoff、station attachはversion `1`
  - Python: **candidate入力固定済み**。remote branch `codex/b5-structured-block-value@64b0f8831fa33e74f1b70b9102b3f29ec99b8e14`。`setDimension()`、canonical build contextの原子的同期、player／event／guard、observer／stationをDimensionKeyへ更新し、旧world API／field／unionを撤去した。Scratch exact sourceからNode `24.19.0`で独立再生成したcommon WireScopeとPython同梱物はbyte-for-byte一致。Python 3.11／3.13で各225 tests、lock／compile／fixture／metadata／RECORD／license検査PASS。独立clean checkout 2件のwheel／sdistはそれぞれbyte-for-byte一致。wheelは170,271 bytes／SHA-256 `370f0fef3d5124a1024cbea8dfb4c65f2080cb545ab342086a827287d0f3f195`、sdistは175,715 bytes／SHA-256 `4337c6502f2be58e2bbf526d657c3f41d962bab08dd5a68eeb9527d66c9896b6`
- component readiness（以下の旧candidate PASSは影響外の観測履歴として保持し、DimensionKey sliceの合格には使わない）:
  - McRemote: **live-auto segment PASS**。source `fc84c8fd5e41c07c5d89671f193fdb7012eabd36`／JAR SHA-256 `7f9bf3616accc27cac100c705aa3bfc722024978a76a5505015d80047054012f`をhost-native `dev-integration`で実行し、runner全項目PASS。修正対象の`world.spawnParticle`は未ロードchunkのload／generate後にaccepted count `1`、`world.spawnEntity`は256 unique handles、257件目`entity_capacity_exhausted`、別epoch独立を実機確認した。structured block、`getBlocks`、`getHeight`、FIFO／flush、1041 notification burst、`events.poll`、validationもPASS。serverは試験後もactiveで標準portを待受。旧source `ef025ce5…`／JAR `17cdc457…aeb6`は修正前candidateとして失効する。試験で生成したentity／blockは再生成可能なruntime stateであり清掃を後続segmentの開始条件にしない。stale／latest cursor、server poll上限縮小、reconnect後cursor失効、3種eventの人間操作は本segmentのnon-claimとして後続へ送る
  - Scratch／WireScope: **決定論的component candidate準備済み**。remote branch `agent/b5-protocol22-block-value@602ecdf809f87a7e33e50d7c465b7248429e26dc`、protocol `22.0.0`／artifact `2200.0.0b5`。CI run `32504972088`はexact headのBuild／Scratch VM／Scratch GUI／Test Resultsが全てsuccess。GUI build artifact ID `9455095975`／digest `sha256:4b8186a32cdeba62dfaf69a58e95c909dcd0351559b6b30459aba4e0b72c9592`、Bridge artifact ID `9455099784`／digest `sha256:cab330cabf38351699bca92e3c22a6299cb23ddaecd7c9c39788f998df284950`。common WireScope ZIPは59,340 bytes／SHA-256 `f3ffaa1c55122b21acaccf9467bbd39c775c44d7e982fa3b11658d10a14b0f49`、detached manifestは2,321 bytes／SHA-256 `b7565dd7f4883020737bbe5f5dfb28819862d0edc54bb4b4d5503d99c5d65780`。manifestはsource commit、Node `24.19.0`、`npm ci && npm run build:artifact --workspace=@mc-remote/live -- --source-commit 602ecdf809f87a7e33e50d7c465b7248429e26dc`、observer schema／session／handoff／station attach version `1`を固定。専用CI uploadはなくlocal `/tmp`を取得元にはしないため、Pythonがpush済みsourceから独立再生成して両SHAへ一致させる。live未実施
  - Python: **決定論的component candidate準備済み**。remote branch `codex/b5-structured-block-value@af2b19dd4a4f0404c4bde439021ca7e017904a04`、protocol `22.0.0`／artifact `2200.0.0b5`。push済みsource内のWireScope ZIP／manifest blobをknowledge coordinatorが再hashし、ScratchのSHAと一致。wheelは167,478 bytes／SHA-256 `a3dacff46027108a6216ded320ad7b75f9b42b4dbdb3e424059c49e0935fcf0c`、sdistは172,944 bytes／SHA-256 `e6684f15197d165203c8b5b9f99669b16893de19f95cfe2456074359e43403fd`。clean commitからのbuild再現、52 focused tests／216全決定論的tests、compileall、metadata／RECORD／license／corresponding source検査PASSと担当報告。observer schema／session／handoff／station attachはversion `1`、compatibility revision `v1.1`は別管理。Actions workflow／runはなく、wheel／sdistはsource commitとexact digestから再生成・照合する。live未実施
- frozen runtime policy / schema: protocol `22.0.0`、artifact `2200.0.0b5`、Minecraft `1.21.11`。plugin command FIFO `1024`、response queue `64` frames、event ring `256` events／`262144` bytes、event poll default／server max `64`／`64`、entity handles `256`、particle count `1000`、work request／session／player／global `4096`／`4096`／`8192`／`32768`、compact poll response最大`61440` bytes。Python send queue `1024`、request／flush timeout `60.0`秒（timeout時は完了不明、自動retryなし、connection回収）、TRACE delay既定`0.25`秒／範囲`0.0`〜`2.0`秒。observer schema、observer session、Scratch handoff、station attachはversion `1`、compatibility set revisionは`v1.1`、observer session frame最大`65536` bytes
- environment preparation correction: プロジェクトオーナーのいう「通常dev環境」は、ケータリング型でないだけでなく、**Docker／Composeを使わずm720s2のhost上でPaper／McRemoteを直接動かすhost-native環境**を指す。knowledge coordinatorがこれを「非ケータリングの永続環境」とだけ解釈して`home-server@5`／`compose@5`を採用したのは誤り。knowledge commit `e854039646a84468b506c2c286bc5314f1e10d20`によるapply／doctor許可を撤回する
- invalidated Docker path: Stack PR `#26`／`#27`／`#28`とその検証事実は履歴として保持するが、本gateの通常dev targetとして`home-server@5`、container runtimeを内包する`mcremote-paper@7`、OCI index `sha256:7f69fd6688e03495c8a8f5a46e8a8e82001b4465f4b55bdcd024c02c3624d8c8`、container内Java `jdk-21.0.11+10`、adapter `compose@5`を採用しない。order semantic `97561f1b49aa8f4d96e59ab24647ff2fb3ef93dab670178c33dc9867f13c708d`、lock identity `sha256:b5840f077f0a6fd55221be1795751cad809da00a033933df3f461ca2292ab705`、render manifest `6cd55bd02b6ed52958e6ee163ab852ec809bc0c01541f571e3943e75d3778ea6`はこのgateへapplyしてはならない
- reusable preparation: Stackのreview済みartifact import、標準port `25565`／`25575`、未知listener時のreadiness取消、Paper `1.21.11-132`（54,846,016 bytes／SHA-256 `5ffef465eeeb5f2a3c23a24419d97c51afd7dbb4923ff42df9a3f58bba1ccfba`）の照合結果は再利用できる。旧McRemote JAR `17cdc457…aeb6`のCAS照合結果は履歴として保持するが、現行live setのartifact identityには使わない
- environment staging result: 訂正前のknowledge commit `e854039646a84468b506c2c286bc5314f1e10d20`による許可とHOLD訂正が入れ違いになり、Stackは旧lockを用いたDocker applyを一回実行した。containerはrunning／healthy、Paper／McRemoteのread-only mountと3 managed volumes、OCI index、order／lock／compose／render bindingは旧setと一致したが、doctorはgit-build artifactの`output_filename`／`output_sha256`を共通mount検査が`filename`／`sha256`として読まない実装差分により`doctor_artifact_mount_mismatch`でFAILした。order／lock／generated file／containerの手修正、再apply、rollback、製品live試験は行っていない。この失敗をhost-native gateの失敗へ読み替えず、Docker経路の観測として保持する。runtimeは停止確認が返るまで**意図しない稼働中state**であり、通常dev readinessを取り下げる
- host-native first smoke: knowledge `b84e9901265f15bb9e0ccd30a74be5a2bdc130c5`により旧Docker runtimeを停止し、OpenJDK `21.0.11+10`、Paper `1.21.11-132`、McRemote `1.21.11-2200.0.0b5`をsystemdで直接起動した。Docker container非稼働、port解放後のhost-native listen、workstation LAN到達、tokenなしhelloの`auth_required`はPASS。一方、root所有のMcRemote configへpluginがb5既定値を追記できず`Permission denied`、credential snapshot／revocation authorityが未初期化でcredential domainが`UNHEALTHY`となったためPARTIAL PASSで停止した。serviceはinactive、port `25565`／`25575`解放、追加手修正・再起動・製品試験なし。これはcandidate不具合でなくbootstrap手順の不足として扱う
- host-native readiness: knowledge `5400560225f4a329fd0f40725c91b5465187d872`の最小差分後、systemd serviceは専用accountでactive、boot enableはdisabled、credential domainは`HEALTHY`、通常再起動後も同一domainで`HEALTHY`。Paper／McRemote exact SHA、port `25565`／`25575`、workstation LAN到達、tokenなしprotocol 22 helloの`auth_required`、Docker container 0、未知service／listenerなしを確認。Stack PR `#29` head `8e65214d766a4448b3fc294b794262f294c2679a`は454 tests／ruff／ShellCheck／self-test PASS、backstage PR `#5` head `c91d82d816cb17569ddda621adbab9d8f8df117b`はTOML parse／secret scan／diff check PASS。両PRはdraft／clean。製品API liveは未実施
- Stack PR review: `#29`のhost-native経路とreadiness barrierは採用可能。ただし`data/plugins`がservice account所有のため、root所有JAR fileでもserviceがunlink／置換でき、「immutable入力」という主張と不一致。merge前に`data/plugins`をroot所有・非書込み、`data/plugins/McRemote`だけをservice所有とし、service accountがJARを置換できずconfig／credential backendへ書ける回帰testを追加する。この修正は製品artifact／runtime policyを変えないためlive試験と並行する。backstage `#5`はdraft解除・merge可
- McRemote first segment attempt: candidate `b5_live_auto.py`はtoken／credential入力とpairingを持たず、tokenなしhelloの成功を要求したため、exact auth-enforced serverの正しい`auth_required`でrunner preflight FAIL。plugin不具合とAPI FAILは未観測で、world／entity／origin変更なし。source／JAR／server readinessは維持する。これは製品candidateを失効させず、test harness identityだけを追加固定するgapとする
- runbook cleanup: Stack PR `#28`はreview済みhead `94b86b6f4142024a443a77bcfb1a39c8107aace9`／merge commit `e3d73a5dae44086bde60f36d0fdfa3630d330b28`でmerge済み。通常dev guideとrunbook testの2 filesだけを変更し、orderの既存acknowledgement 2 scalarを具体的なgate理由で設定して再validate、`resolve --allow-unverified`、plan review、後続`apply --allow-unverified`へ進むdurable＋one-shot境界、成功条件、`acknowledgement_reason_required`／`unverified_not_acknowledged`からの戻り先を記載する。lock／generated treeの手編集は禁止したまま。coordinatorはremote main一致、reviewed head包含、外部check 0件をGitHub APIで確認した。担当報告は452 tests／ruff／diff check PASSで、preset／order／lock／artifact／render identity不変。CLI変更なし
- input correction: McRemote作業票のknowledge SHA `f50ebb17…`は存在せず、実在する`f50ebb13f00facfc2e73163a24f002f4c8b77d43`を参照。契約差分なし
- target deployment / profile / lock: logical deploymentは`dev-integration`、physical hostはbackstage管理下の`m720s2`、channel=`dev`、exposure=`lan-only`、purpose=`integration`、標準server portはJava `25565`／McRemote `25575`。現在の試験runtimeは`/home/tsuji/MINECRAFT_SERVERS/PaperMC`を`run.sh`から名前付きScreen session `Minecraft server`で起動するhost-native／non-Docker環境。旧systemd版はinactive。Paper `1.21.11-132`、McRemote `2200.0.0b5`／JAR `f7ddbcb5…36547`、credential domain `HEALTHY`、両port LISTEN、tokenなしhello `auth_required`を確認済み。起動方式とrunbookの恒久改訂は進行中の製品試験へ混ぜず、試験完了後の別作業とする
- authorized next action:
  - unified test ID: `2026-08-22-b5-dimension-key-live`
  - Python segment: **PASS**。exact source `64b0f8831fa33e74f1b70b9102b3f29ec99b8e14`／wheel `370f0fef…f195`、McRemote `bbbb5360…`／JAR `f7ddbcb5…36547`、WireScope `407031d5…a6964`／manifest `15d0c6b9…5bda`を使用した。authenticated hello、shorthandからcanonical DimensionKeyへの正準化、両build setterのcontext一体同期、pose、旧alias不採用、一般namespaceのserver到達、旧method拒否、失敗時context不変、3 event DTO、same-context guard、意図的mismatch拒否、WireScope schema version `1`／`world` fieldなし、real-browser終了表示をすべてPASS。初期2停止は試験runnerの過剰なerror値固定とbrowserによるsnapshot slot消費で、candidate不具合ではない。最終runは正常終了しcandidate／server／config変更なし
  - Scratch segment: **PASS**。exact source `1a11c46b…`／CI run `32574020556`を使い、標準3dimension menuと完全修飾result、一般namespaceのserver到達、旧`world` alias不在、pose、3 event hat、canonical dimension／origin／loss `0`、real-browser WireScopeのbuild／player／event frameと`world` field不在を確認した。poll frameが履歴を押し流すため操作ごとの分割runを使い、初回旧localhost cacheはfresh originで同じexact artifactを表示して解消。candidate／server設定変更なし、接続終了、worktree clean
  - 省略範囲: standalone McRemote live runner、spawn capacity、block／height、FIFO／1041 notification burst、poll上限、全回帰、試験前後の重複readiness、world／entity清掃を実施しない。既存PASSを再利用する
  - 進行規則: Python PASS後にScratchを開始する。失敗時はそのsegmentで停止し、exact request／response、reason、candidate identityだけを返す。candidate、server配置、config、起動方式を試験中に変更しない。人間操作の取り直しは失敗した操作だけに限定する
  - 返却: 各担当は実行したexact artifact、PASS／FAIL一覧、WireScope確認、未実施範囲、candidate変更なし、接続終了だけを一枚で返す。component GREENや横断GREENを主張しない
- live-auto / live-human: **完了**。追加試験を行わない。正式recordは`14-evidence/records/2026-08-22-b5-dimension-key-live_ja.md`
- gate result: **GREEN — b5横断技術gate完了／prerelease identity確認完了**。exact compatibility setと技術evidenceを変更せず、3 componentのprereleaseを受理する
- release authorization: プロジェクトオーナーの明示承認（2026-08-23）。McRemoteは`v1.21.11-2200.0.0b5`を`bbbb53602a9c375e2ead3ee4c22174d5cf424f55`へ、Pythonは`v2200.0.0b5`を`64b0f8831fa33e74f1b70b9102b3f29ec99b8e14`へ、Scratchは`v2200.0.0b5`を`1a11c46bac5696afd3f494caac56ae682ed00fb0`へ固定する。各releaseはprerelease ON、draft OFF、Latest非対象とし、作成後にtag target、公開状態、asset／release notesのSHA-256をGitHub APIで確認する。McRemote JAR assetを登録し、Pythonはwheel／sdistのSHA-256をrelease notesへ記載する。ScratchはCI／Bridge artifact ID、common WireScope ZIP／manifest SHAをrelease notesへ記載する
- release identity verification: McRemote [v1.21.11-2200.0.0b5](https://github.com/Naohiro2g/McRemote/releases/tag/v1.21.11-2200.0.0b5)はtag target `bbbb53602a9c375e2ead3ee4c22174d5cf424f55`、prerelease ON、draft OFF、Latest非対象、JAR asset 195,998 bytes／SHA-256 `f7ddbcb5…36547`、release notes SHA-256 `64f2cedd…a364`。Python [v2200.0.0b5](https://github.com/Naohiro2g/minecraft-remote-api/releases/tag/v2200.0.0b5)はtag target `64b0f8831fa33e74f1b70b9102b3f29ec99b8e14`、prerelease ON、draft OFF、Latest非対象、assetsなし、release notes SHA-256 `c0375238…0dc04`。Scratch [v2200.0.0b5](https://github.com/Naohiro2g/scratch-editor/releases/tag/v2200.0.0b5)はtag target `1a11c46bac5696afd3f494caac56ae682ed00fb0`、prerelease ON、draft OFF、Latest非対象、追加assetsなし、CI／Bridge digestとWireScope SHAをnotesへ記載。各repo worktreeはclean
- authorized next action: release identity確認をもってb5 gateをcloseする。PyPI／TestPyPI、registry publish、public deploy、runtime／server変更、b6実装はこのrelease確認に含めない。次の作業は別途b5後・b6前の保存entry gateまたはb6 scopeとして起票する
- non-claim: Scratch browser保存、b6 API、full load／soak、capacity本較正、custom loaded dimension成功、他Minecraft／Paper版、通常dev環境runbook改訂、public deploymentを主張しない

### b5から次gateへ持ち越す方法論

- decision: `2026-08-23-01`
- b5の厳密検証でspawn、runner認証、DimensionKeyの問題を発見したことは有効であり、試験項目を破棄しない。
- 手戻りの主因は、仕様形成中の毎回へrelease gate級の固定・環境準備・全検証を適用したこと、通常dev harnessとdeploymentを混同したこと、identityを手転記したことである。
- b6／b7／b8はTier 0〜2でcontractを収束させ、RC候補までTier 4を自動要求しない。capacity／soakは実装が載った後の実測へ送る。
- 次の横断候補前に、常設通常dev integration harnessの正準入口とmachine-readable gate manifestをStack／backstage／knowledgeの各責務に従って実装する。
- b5で実施した非影響PASSは、change coneと元identity／non-claimを明示できる場合に限り後続gateへ再利用できる。

### b5 public deploy 実施記録（2026-08-23）

- decision: `2026-08-23-02`
- 対象 repo: mc-remote-stack（協調: McRemote, scratch-editor）
- gate coordinator: mc-remote-stackリポのClaude Codeセッション。human release ownerが本セッション内でpublic VPS beta（official-public-beta）へのb5 exact set適用を明示承認し、実行した
- 実施日: 2026-08-23
- exact compatibility set遷移: `public-web-paper@5` → `@6`（Stack PR `#31`、merge `7cb0168`）→ `@7`（Stack PR `#34`、merge `a58f51d`）。`vps-server@8` → `@12`
- 適用先: official-public-beta VPS、lock `sha256:a2e93aaf512f895f4ec5482c443a0763ff534f68f611dd14ca58fb49b109bb92`
- credential永続化regressionと修正: 適用直後にMcRemote CredentialServiceが`UNHEALTHY`（`Unknown persisted credential type: session`）となった。`git log --graph`によるcommit history比較で、b5ブランチが共有merge-base `9df8c46`（b4 player pose commits）から、b4側のsession token永続化fix `3496db9`（2026-08-18、`2026-08-02-08`実装、evidence `2026-08-18-b4-session-persistence-home-alpha`）がマージされる前に分岐しており、b5独自のprotocol-22作業が同じcredential関連fileを独立に書き換えたためこの修正が欠落していたと判明した。意図的なb5設計変更ではなく並行branch間の取り込み漏れであり、既存on-disk `session`型recordを読込み時に黙って捨てるだけのshimは、b4で実機検証済みの同一runtime再起動を跨ぐsession token継続を回復しない不完全な対応として不採用とし、`3496db9`をcherry-pickして修正した。McRemote `v1.21.11-2200.0.1b5`（JAR SHA-256 `b20705899e3d352a434640b2b075845e34bdac9bda895ee8d1a768f8d232a844`、独立clean checkout 2件でbyte-for-byte一致、`./gradlew check` 101 tests PASS、うちsession-persistence関連6 tests）としてVPSへ適用した
- live doctor結果: 適用時点で接続player 0名・直近backup 1時間以内の低リスクな窓だった。修正適用後、`docker logs`で`[McRemote] Credential domain health: HEALTHY (healthy)`を確認。`mcrctl doctor`はruntime／lock／network／protocol／homepage／scratch-runtime／wirescope全項目OKで、`compatibility=unverified`のみ既存の想定内WARN（regressionと無関係）
- non-claim: capacity較正、soak、rollback実演、公開向け人間参加試験は本follow-upで実施しない
- 関連決定: `2026-08-23-02`（「b5後・b6前の保存entry gate」という語は時期を示すだけで、public deploy可否を制限する条件ではないという訂正を含む）

## 2026-08-07 Scratch editor `2100.0.0b3`

- candidate: `release/b3@3f1a10a366bfbe76e32b5a31c54da19eddd56e56`
- contract: `13-scratch-client/scratch-roadmap_ja.md` §2.3 / knowledge `3dfbf57c07f2b7985c65edc5564b879f9e67e122`
- CI: run `31145335984`、exact candidate、全job success
- evidence: `14-evidence/records/2026-08-07-scratch-b3-release-gate_ja.md`
- status: **GREEN — tag `v2100.0.0b3`とGitHub prerelease作成を承認**
- release条件: tag targetは上記candidate完全SHA、prerelease ON、draft OFF、Latest非対象
- rollback: `v2100.0.0b2@e19247069d1ae55037c0e9ffc52ea88cde612ac3`
- scope boundary: hosted surface更新は含めない。更新時はdeploy smoke / rollback / re-deployを別gateで確認する
- deferred: catalog picker / WireScope miniはb4、独立WireScopeは`2026-08-06-03`どおりb3非blocker

## 2026-08-07 b3 横断 milestone close

- status: **CLOSED — b3の横断スコープを完了扱いとし、b4の利用者向け機能へ進む**
- decision: `2026-08-07-01`
- Python API: `v2100.0.0b3@af2d11d66a16e3085f569241406a703a1c28c348`、GitHub prerelease、PyPI非公開。正式live根拠は `14-evidence/records/2026-08-06-b3-python-catalog-projection-live-human_ja.md`
- McRemote: `v1.21.11-2100.0.0b3@a3dab998b710f65f42f95058a68ec51d419b097c`、GitHub prerelease、JAR SHA-256 `aeb190705bd9957ce73557dc1be0fe15efe7250ba9bc688945e6f537e00ef78e`
- Scratch editor: `v2100.0.0b3@3f1a10a366bfbe76e32b5a31c54da19eddd56e56`、GitHub prerelease。正式gate根拠は `14-evidence/records/2026-08-07-scratch-b3-release-gate_ja.md`
- scope: versioning §10.11.1項14のcatalog一式、Scratch現行roadmapのb3 scope、各componentのb3 prereleaseを区切りとして閉じる。component番号の永久同期やstable releaseを主張しない
- deferred: long-lived credentialの公開gate、checkpoint＋doctor、end-to-end snapshot rollback、reset／災害復旧は閉じたまま後続へ送る。既定は`session`のまま
- non-claim: Stackの一般profile公開、hosted surface更新、long-lived公開可否をGREENとする記録ではない。これらをb3完了へ遡及混入しない

## 2026-08-16 Python `2100.0.0b4` candidate

- candidate: `codex/b4-player-pose@4d510442db58a94f8b249ddcd9d959381f97276c`
- contract: DECISIONS `2026-08-16-08` / knowledge `b747fa2b3b6c278f1a8e920ba8e02b45e2cf2b47`
- evidence: `14-evidence/records/2026-08-16-b4-python-pose-wirescope-live-human_ja.md`
- status: **PYTHON CANDIDATE PASS — tag／releaseは未承認**
- verified: candidate wheel、main stream 1件、`player.getPose`／`player.setPose`、origin相対座標、automatic browser launch、WireScope UI、終了表示、distribution／license gate
- compatibility set: McRemote `9df8c46d600ff9605dc1822b304715de713e6767` / JAR SHA-256 `ab3b87c38b6876ec4ba26112eff35d7cb016395a1dae1661578fd3690e1dbc46` / WireScope source `56011f71291f47ced69cc4e3c377734f501b6081` / ZIP SHA-256 `1a56617c78c283332f1afe3bdd3797ab37f0cdc3455c86c73c926c751721657f`
- rollback candidate: `v2100.0.0b3@af2d11d66a16e3085f569241406a703a1c28c348`。rollback実操作と再復帰は未実施
- remaining: Scratch／Pythonの順次横断real-browser E2E、home alpha、plugin artifactを含むexact compatibility set最終批准、release後identity確認
- non-claim: 本項だけでPython tag、GitHub prerelease、横断b4 milestoneをGREENにしない

## 2026-08-16 Scratch editor `2100.0.0b4` candidate

- candidate: `release/b4@56011f71291f47ced69cc4e3c377734f501b6081`
- contract: DECISIONS `2026-08-16-08` / knowledge `b747fa2b3b6c278f1a8e920ba8e02b45e2cf2b47`
- CI: run `31934776981`、exact candidate、全job success
- evidence: `14-evidence/records/2026-08-16-scratch-b4-release-gate_ja.md`
- status: **SCRATCH COMPONENT GREEN — tag／releaseは横断gateまで保留**
- verified: Catalog Picker、`player.getPose`／`player.setPose`、Scratch main stream 1件のMessageChannel観察、pose対応common app、clean artifact reproduction、unit／build／CI
- common artifact: ZIP SHA-256 `1a56617c78c283332f1afe3bdd3797ab37f0cdc3455c86c73c926c751721657f` / manifest SHA-256 `f3ec11496b595bbca4ba27a6e938a1149336eb5a2da55e742d60e1681cf4d154`。Python candidateと一致
- rollback target: `v2100.0.0b3@3f1a10a366bfbe76e32b5a31c54da19eddd56e56`。hosted deploy／rollback実操作／再復帰は未実施
- remaining: Scratch／Pythonの順次横断real-browser E2E、plugin artifactを含むexact compatibility set、home alpha、release後identity確認
- non-claim: 本項からPython／plugin／home alphaまたは横断b4 milestoneのGREENを推測しない

## 2026-08-17 b4 home-alpha pre-auth transport correction（初回観測）

- decision: `2026-08-17-01`
- evidence: `14-evidence/records/2026-08-17-b4-home-alpha-integration_ja.md`
- status: **PARTIAL PASS — one-shot認証とb4機能統合はPASS、session token再起動耐性はBLOCKED**
- observed gap: McRemote `dab6908494290c894d8efbe6828707e544860fa1`のclose-after-flushでもresponseからEOF観測まで約41msあり、Bridge経由で`auth_required`直後0msに送る`auth.pairBegin`はtimeoutする。100ms待機では成功し、直接新TCPでは成功したが、固定delayは解決として採用しない
- McRemote input: close-after-flush JAR SHA-256 `f902ed360ac1674143d8e79a49c8e109968f2c38dc36656c91a50dec89082aa8`。plugin追加変更は要求しない
- implemented set: Scratch／Bridge one-shot `8b69ecefc9771a47e2eac8bea242cf96c09d36f3`、pagehide lifecycle `1d2f18785d260564ad4bc30a26a45ef33fc813d6`、McRemote JARは上記digest、Python `4d510442db58a94f8b249ddcd9d959381f97276c`、WireScope ZIP `1a56617c78c283332f1afe3bdd3797ab37f0cdc3455c86c73c926c751721657f`
- passed: `auth_required`直後0msのone-shot pairing、Scratch／Python／WireScope実機一巡、canonical b3 rollback、corrected b4再適用
- failed: 同一corrected b4 runtimeの通常再起動後、期限内session tokenが`auth_required`。candidateはsession tokenをin-memoryだけに保持し、`2026-08-02-08`のhash-only snapshot永続化と不一致
- doctor gap: credential domain `UNINITIALIZED`を現行doctorが検出せずPASS。`2026-08-06-02`のcredential checkpoint／doctor contractは未実装
- next gate: McRemote session record永続化→artifact再固定→同一b4再起動とb3→b4再適用でtoken再利用→Stack credential health／doctor再照合
- non-claim: 既存のPython candidate PASS／Scratch component GREENと今回の機能統合PASSは維持するが、認証再起動FAILが閉じるまでhome-alpha認証、credential継続を含むrollback／再適用、b4 releaseはGREENにしない。100ms待機、EOF依存、自動再送をfixture／runbookへ残さない
- resolution: このFAIL観測は削除しない。後続McRemote `3496db9293baa6e1d4f79439cacbd239ba15e2b7`と`2026-08-18-b4-session-persistence-home-alpha`でsame-b4再起動とb4再適用後のtoken再利用がPASSし、最終判定は下記2026-08-18項へ移った

## 2026-08-18 b4 横断 release gate

- decision: `2026-08-16-08`／`2026-08-17-01`／`2026-08-18-01`
- status: **CLOSED — exact b4 compatibility setのGitHub prerelease公開identityを確認し、b4 milestoneを閉じる**
- protected value: Scratch／Pythonの保存済み建築コード。復旧基準はコード保存→空環境再構築→再pairing→必要なら書き換え→再実行
- exact set:
  - McRemote `3496db9293baa6e1d4f79439cacbd239ba15e2b7`／JAR SHA-256 `331633ef15a729658496e89fe49cb8a5eb5ebcb2ec86937b7e5313528d7ec997`
  - Python `4d510442db58a94f8b249ddcd9d959381f97276c`／wheel SHA-256 `eeed6261972987946b5e22dd8ff8d3533a758c7db57472d1d82766fbf964e7d0`
  - Scratch／Bridge one-shot `8b69ecefc9771a47e2eac8bea242cf96c09d36f3`、pagehide lifecycle `1d2f18785d260564ad4bc30a26a45ef33fc813d6`
  - WireScope ZIP SHA-256 `1a56617c78c283332f1afe3bdd3797ab37f0cdc3455c86c73c926c751721657f`／manifest SHA-256 `f3ec11496b595bbca4ba27a6e938a1149336eb5a2da55e742d60e1681cf4d154`
  - Stack `780d99291d669fd1ec98c513245bf6fdbac36271`／runtime implementation `cd3ff18e31534f394e5fc7ad63af1f164ce54f15`／`home-server@3`／`mcremote-paper@6`
- passed:
  - Scratch Catalog Picker、player pose、Scratch／Python main stream各1件の共通WireScope観察
  - pre-auth one-shot pairing、固定delay・自動再送なし
  - same-b4通常再起動後の期限内session token認証
  - b4再適用後の同token認証。b3はb4 session recordを読めずfail closedし、snapshotを破損しなかった
  - 新規world／credential環境でのScratch `.sb3`／Python source再pairing・再実行とserver側独立照合
  - b3 artifact rollback／b4再適用、exact artifact／lock照合
- formal evidence:
  - `2026-08-16-scratch-b4-release-gate`
  - `2026-08-16-b4-python-pose-wirescope-live-human`
  - `2026-08-17-b4-home-alpha-integration`（初回PASS／FAILを保持）
  - `2026-08-18-b4-session-persistence-home-alpha`
  - `2026-08-18-b4-code-preservation-recovery-live-human`
- release identities（GitHub API再確認済み）:
  - [Python `v2100.0.0b4`](https://github.com/Naohiro2g/minecraft-remote-api/releases/tag/v2100.0.0b4): target=`4d510442db58a94f8b249ddcd9d959381f97276c`、prerelease=true、draft=false、Latest非対象。binary assetなし、release notesにwheel／sdist digestを固定、PyPI／TestPyPI非公開
  - [Scratch `v2100.0.0b4`](https://github.com/Naohiro2g/scratch-editor/releases/tag/v2100.0.0b4): target=`1d2f18785d260564ad4bc30a26a45ef33fc813d6`、release ID `372338711`、prerelease=true、draft=false、Latest非対象、追加assetなし
  - [McRemote `v1.21.11-2100.0.0b4`](https://github.com/Naohiro2g/McRemote/releases/tag/v1.21.11-2100.0.0b4): annotated tag target=`3496db9293baa6e1d4f79439cacbd239ba15e2b7`、prerelease=true、draft=false、Latest非対象。asset=`mc-remote-1.21.11-2100.0.0b4.jar`／140,712 bytes／SHA-256 `331633ef15a729658496e89fe49cb8a5eb5ebcb2ec86937b7e5313528d7ec997`
- non-blocking observations:
  - b3はb4の`session` recordを理解せず`unknown_persisted_credential_type_session`となる。b3をcredential継続付きdowngrade runtimeとしては承認しない
  - checkpoint projectionは未実装で、Stack doctorは`doctor_credential_health_unsupported`としてfail closedする。これをdoctor PASSへ読み替えない
- deferred / non-claim: long-lived credential一般公開、checkpoint／doctor完成、world backup／restore、一般Stack profile、public hosted deployment、PyPI／Modrinth公開、substream／multi-stream、b5以降。これらをb4 GREENから推測しない
