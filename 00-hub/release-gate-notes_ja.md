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
- knowledge contract path:
- knowledge contract commit:
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

## 2026-08-21 b5横断release gate（進行中）

- gate coordinator: knowledge担当session。人間による明示handoffなしに他担当へ移さない
- human release owner: プロジェクトオーナー
- current phase: **host-native通常devのbootstrap差分修正を許可**。初回smokeで検出したMcRemote runtime data所有権とcredential domain明示bootstrapだけをrunbookへ加え、クリーン再構築→health→正常再起動まで一巡する。製品live-auto／live-humanはenvironment返却後に統一実施票で開始する
- contract: 技術scopeはDECISIONS `2026-08-21-01`／`2026-08-21-02`およびknowledge `f50ebb13f00facfc2e73163a24f002f4c8b77d43`、進行責任は`2026-08-21-03`／`2026-08-21-04`およびknowledge `575ce310048525f38e11815c8a38d01658b843b3`
- exact compatibility set / freeze status: **全体setは失効・未凍結**。McRemote、Scratch／Bridge、WireScope、Python、Paper、runtime policy／schemaの固定済み入力は再利用候補として保持するが、Docker OCI／container内Javaを含むruntime topologyが人間意図と異なったため、runtime／Java／deploymentを含む一組としての凍結を解除した。host-native runtime identityを確定するまでexact setと称しない
- landing verification: `2026-08-21-03`／`2026-08-21-04`の責務契約はMcRemote、Python、Scratch、Stack、backstageの全担当で一致。Pythonの下記schema差分は責務契約の着地差分でなくb5 component実装差分
- component readiness:
  - McRemote: **決定論的component candidate準備済み**。remote branch `codex/b5-reproducible-jar@ef025ce511e12bf2e8a111e3a8c15ac561ca2be9`は旧candidate `6214a6a5…`へarchive timestamp非保存／reproducible file orderの2設定だけを加えたbuild-only変更。JARは191,625 bytes／SHA-256 `17cdc457a886dd1d37c8e969e5406016460599636f55fdeb584af0012c61aeb6`、85 tests PASS、独立clean build一致。旧`f293…`との110 entriesの名前／展開payload／CRC一致を担当が確認し、coordinatorもGitHub差分、recipe／toolchain／build-input digest、handoff JARを照合したうえで独立clean checkoutから85 tests PASS、同一JAR SHAを再確認。git-build provenanceはrepository `https://github.com/Naohiro2g/McRemote.git`、source subdirectory `.`、recipe SHA-256 `61a4999e31c2b29703836ba5d1e8917de1042ac2ff02cd6142b59862d8280e34`、toolchain SHA-256 `88e5d8ed9b5f3be3b812813971fa4f339d48eec4ab14512a142aae74df35883c`、build input SHA-256 `f8ee956984904870990e062ace5d920f1f7b34497f1885c9ac19c46a5a298eee`。旧`f293…`は原因観測でありexact setへ含めない。live未実施
  - Scratch／WireScope: **決定論的component candidate準備済み**。remote branch `agent/b5-protocol22-block-value@602ecdf809f87a7e33e50d7c465b7248429e26dc`、protocol `22.0.0`／artifact `2200.0.0b5`。CI run `32504972088`はexact headのBuild／Scratch VM／Scratch GUI／Test Resultsが全てsuccess。GUI build artifact ID `9455095975`／digest `sha256:4b8186a32cdeba62dfaf69a58e95c909dcd0351559b6b30459aba4e0b72c9592`、Bridge artifact ID `9455099784`／digest `sha256:cab330cabf38351699bca92e3c22a6299cb23ddaecd7c9c39788f998df284950`。common WireScope ZIPは59,340 bytes／SHA-256 `f3ffaa1c55122b21acaccf9467bbd39c775c44d7e982fa3b11658d10a14b0f49`、detached manifestは2,321 bytes／SHA-256 `b7565dd7f4883020737bbe5f5dfb28819862d0edc54bb4b4d5503d99c5d65780`。manifestはsource commit、Node `24.19.0`、`npm ci && npm run build:artifact --workspace=@mc-remote/live -- --source-commit 602ecdf809f87a7e33e50d7c465b7248429e26dc`、observer schema／session／handoff／station attach version `1`を固定。専用CI uploadはなくlocal `/tmp`を取得元にはしないため、Pythonがpush済みsourceから独立再生成して両SHAへ一致させる。live未実施
  - Python: **決定論的component candidate準備済み**。remote branch `codex/b5-structured-block-value@af2b19dd4a4f0404c4bde439021ca7e017904a04`、protocol `22.0.0`／artifact `2200.0.0b5`。push済みsource内のWireScope ZIP／manifest blobをknowledge coordinatorが再hashし、ScratchのSHAと一致。wheelは167,478 bytes／SHA-256 `a3dacff46027108a6216ded320ad7b75f9b42b4dbdb3e424059c49e0935fcf0c`、sdistは172,944 bytes／SHA-256 `e6684f15197d165203c8b5b9f99669b16893de19f95cfe2456074359e43403fd`。clean commitからのbuild再現、52 focused tests／216全決定論的tests、compileall、metadata／RECORD／license／corresponding source検査PASSと担当報告。observer schema／session／handoff／station attachはversion `1`、compatibility revision `v1.1`は別管理。Actions workflow／runはなく、wheel／sdistはsource commitとexact digestから再生成・照合する。live未実施
- frozen runtime policy / schema: protocol `22.0.0`、artifact `2200.0.0b5`、Minecraft `1.21.11`。plugin command FIFO `1024`、response queue `64` frames、event ring `256` events／`262144` bytes、event poll default／server max `64`／`64`、entity handles `256`、particle count `1000`、work request／session／player／global `4096`／`4096`／`8192`／`32768`、compact poll response最大`61440` bytes。Python send queue `1024`、request／flush timeout `60.0`秒（timeout時は完了不明、自動retryなし、connection回収）、TRACE delay既定`0.25`秒／範囲`0.0`〜`2.0`秒。observer schema、observer session、Scratch handoff、station attachはversion `1`、compatibility set revisionは`v1.1`、observer session frame最大`65536` bytes
- environment preparation correction: プロジェクトオーナーのいう「通常dev環境」は、ケータリング型でないだけでなく、**Docker／Composeを使わずm720s2のhost上でPaper／McRemoteを直接動かすhost-native環境**を指す。knowledge coordinatorがこれを「非ケータリングの永続環境」とだけ解釈して`home-server@5`／`compose@5`を採用したのは誤り。knowledge commit `e854039646a84468b506c2c286bc5314f1e10d20`によるapply／doctor許可を撤回する
- invalidated Docker path: Stack PR `#26`／`#27`／`#28`とその検証事実は履歴として保持するが、本gateの通常dev targetとして`home-server@5`、container runtimeを内包する`mcremote-paper@7`、OCI index `sha256:7f69fd6688e03495c8a8f5a46e8a8e82001b4465f4b55bdcd024c02c3624d8c8`、container内Java `jdk-21.0.11+10`、adapter `compose@5`を採用しない。order semantic `97561f1b49aa8f4d96e59ab24647ff2fb3ef93dab670178c33dc9867f13c708d`、lock identity `sha256:b5840f077f0a6fd55221be1795751cad809da00a033933df3f461ca2292ab705`、render manifest `6cd55bd02b6ed52958e6ee163ab852ec809bc0c01541f571e3943e75d3778ea6`はこのgateへapplyしてはならない
- reusable preparation: Stackのreview済みartifact import、標準port `25565`／`25575`、未知listener時のreadiness取消、Paper `1.21.11-132`（54,846,016 bytes／SHA-256 `5ffef465eeeb5f2a3c23a24419d97c51afd7dbb4923ff42df9a3f58bba1ccfba`）、McRemote JAR `17cdc457…aeb6`のCAS照合結果はhost-native案でも再利用候補とする。ただし再利用可否は新profile／renderer／service contractと新lockで再確認する
- environment staging result: 訂正前のknowledge commit `e854039646a84468b506c2c286bc5314f1e10d20`による許可とHOLD訂正が入れ違いになり、Stackは旧lockを用いたDocker applyを一回実行した。containerはrunning／healthy、Paper／McRemoteのread-only mountと3 managed volumes、OCI index、order／lock／compose／render bindingは旧setと一致したが、doctorはgit-build artifactの`output_filename`／`output_sha256`を共通mount検査が`filename`／`sha256`として読まない実装差分により`doctor_artifact_mount_mismatch`でFAILした。order／lock／generated file／containerの手修正、再apply、rollback、製品live試験は行っていない。この失敗をhost-native gateの失敗へ読み替えず、Docker経路の観測として保持する。runtimeは停止確認が返るまで**意図しない稼働中state**であり、通常dev readinessを取り下げる
- host-native first smoke: knowledge `b84e9901265f15bb9e0ccd30a74be5a2bdc130c5`により旧Docker runtimeを停止し、OpenJDK `21.0.11+10`、Paper `1.21.11-132`、McRemote `1.21.11-2200.0.0b5`をsystemdで直接起動した。Docker container非稼働、port解放後のhost-native listen、workstation LAN到達、tokenなしhelloの`auth_required`はPASS。一方、root所有のMcRemote configへpluginがb5既定値を追記できず`Permission denied`、credential snapshot／revocation authorityが未初期化でcredential domainが`UNHEALTHY`となったためPARTIAL PASSで停止した。serviceはinactive、port `25565`／`25575`解放、追加手修正・再起動・製品試験なし。これはcandidate不具合でなくbootstrap手順の不足として扱う
- runbook cleanup: Stack PR `#28`はreview済みhead `94b86b6f4142024a443a77bcfb1a39c8107aace9`／merge commit `e3d73a5dae44086bde60f36d0fdfa3630d330b28`でmerge済み。通常dev guideとrunbook testの2 filesだけを変更し、orderの既存acknowledgement 2 scalarを具体的なgate理由で設定して再validate、`resolve --allow-unverified`、plan review、後続`apply --allow-unverified`へ進むdurable＋one-shot境界、成功条件、`acknowledgement_reason_required`／`unverified_not_acknowledged`からの戻り先を記載する。lock／generated treeの手編集は禁止したまま。coordinatorはremote main一致、reviewed head包含、外部check 0件をGitHub APIで確認した。担当報告は452 tests／ruff／diff check PASSで、preset／order／lock／artifact／render identity不変。CLI変更なし
- input correction: McRemote作業票のknowledge SHA `f50ebb17…`は存在せず、実在する`f50ebb13f00facfc2e73163a24f002f4c8b77d43`を参照。契約差分なし
- target deployment / profile / lock: logical deploymentは`dev-integration`、physical hostはbackstage管理下の`m720s2`、channel=`dev`、exposure=`lan-only`、purpose=`integration`、標準server portはJava `25565`／McRemote `25575`を維持する。Paper／McRemoteをhost Javaで直接起動するhost-native／non-Docker構成とし、service managerはsystemdを使う。host Java exact identity、service unit、filesystem inventory、host-native order／lock相当は今回の実bootstrapで固定する。ケータリング型とDocker／Compose型はいずれも本gate対象外
- authorized next action:
  - McRemote: source `ef025ce511e12bf2e8a111e3a8c15ac561ca2be9`、JAR `17cdc457…`、review済みhandoff／provenanceを変更せず待機する。tag／release／asset、deploy、live試験は行わない
  - Scratch: source `602ecdf809f87a7e33e50d7c465b7248429e26dc`と上記artifact identityを変更せず待機する。candidate deploy／liveを開始しない
  - Python: source `af2b19dd4a4f0404c4bde439021ca7e017904a04`と上記artifact identityを変更せず待機する。candidate deploy／liveを開始しない
-  - Stack: **二つのbootstrap差分を直ちに修正し再実行する**。①McRemote JARはimmutable／read-onlyのまま、plugin runtime data directoryと生成・更新されるconfigを専用service account所有・非公開権限にする。credential snapshotとrevocation authorityの分離resourceも同accountが必要な書込みを行えるようにする。②Stackが内部JSONを生成せず、candidateが提供するplugin所有console commandのexact名称・成功条件を実装／helpから確認してrunbookへ固定し、空のsnapshot／authorityに対してcredential domainを明示bootstrapする。初回PARTIAL PASSのtreeは直接chownして合格扱いにせず退避して、修正版runbookから新しい空runtime stateを構築する。起動→明示bootstrap→credential health `HEALTHY`→tokenなしhello `auth_required`→正常停止・再起動→同一domainで`HEALTHY`→artifact hash、listener、LAN到達、未知service／listenerなしを確認する。Java `21.0.11+10`と既存Paper／McRemote digestは変更しない。汎用renderer、Docker doctor、製品API live試験へscopeを広げず、失敗時はその場の追加手修正をせずreasonを返す
  - backstage: Stackの停止・host-native起動に合わせ、Docker container非稼働、host-native service／listenerの所有者・用途・起動主体、標準port、service account／directory、未知service／listenerなしをprivate inventoryで一巡照合する。必要なinventory更新は日本語PRとして分離し、秘密実値をknowledge／Stackへ複製しない。旧Docker managed dataとDocker installationは観測事実として保持し、削除しない
- live-auto / live-human: **未許可**。exact set凍結とenvironment readiness確認後にcoordinatorが統一実施票を発行する
- non-claim: component GREEN、b5横断GREEN、通常dev環境完成、release承認をまだ主張しない

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
