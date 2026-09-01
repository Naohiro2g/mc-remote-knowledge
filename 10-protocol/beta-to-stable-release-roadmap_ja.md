# betaから初回stableまでのreleaseロードマップ

> 2026-08-26確定。DECISIONS `2026-08-26-08`の説明とmethod／surface capability台帳です。
> `2026-08-28-02`により短期betaを軽量に反復し、`2026-08-29-02`でb7〜b9のparticle／world effect配置を
> 精密化しました。
> 日々の作業記録や実施済みevidenceではありません。exact wireは
> [wire contract](wire-format-design_ja.md)、release番号と互換性は
> [versioning design](versioning-design_ja.md)を正とします。

## 1. 三つの軸

次の三軸を混ぜません。

| 軸 | 表すもの |
| --- | --- |
| R1／R2／R3 | 利用者価値と成熟段階 |
| b6／b7／b8／rc／stable | product release train |
| ケータリング／教材／広報 | releaseをまたいで並走する実行track |

betaは旧b6へ集めていたAPIを一度に完成させる箱ではなく、contractと実装を観察可能な概念別の
縦sliceへ分けて公開するpulseです。初回stableはハードフォーク前methodの全復帰ではなく、rcでfreezeした
一貫したmethod集合を対象にします。

## 2. Methodの開発状態

状態は実装率ではなく、次に許可できる作業を表します。machine keyを`method_state`とし、methodごとに
一つを正とします。根拠をcandidate、fixture、gate manifestまたはevidenceへ接続します。

| 状態 | 意味 | 次へ進む条件 |
| --- | --- | --- |
| `inventory` | 旧実装、要求またはregistry上で存在を確認しただけ | 復帰価値、owner、重複／代替を判定する |
| `candidate` | 復帰・追加候補。shapeやPaper挙動に未確定を残す | params／result／error／上限／副作用を起案する |
| `contracted` | 人間批准済みcontractと共有fixtureがある | component実装とTier 0〜2へ進む |
| `implemented` | 必要componentがcontractへ適合したcandidateを持つ | exact setとchange coneを固定する |
| `released` | beta exact setで必要tierを通過し、公開identityを確認した | rc採用または後続観察を判定する |
| `frozen` | rc対象としてAPIとwireをfreezeした | fix、capacity、soak、rollbackだけを進める |
| `deferred` | 初回stableの対象外として後続release trainへ送った | 新しいcore／minorのscope決定で再開する |
| `removed` | 対象protocol registryへ収容しないと判断した | 新要求とversioning判断なしに復帰しない |

`candidate`を実装開始許可と読まず、`implemented`を横断互換やrelease済みと読みません。contractに影響する
発見があれば前の状態へ戻し、過去の観測事実は消しません。

## 3. Release train

| release | protocol／artifact core | concept slice(s) | 目標時期 |
| --- | --- | --- | --- |
| b6 | `23.0.0`／`2300.0.0b6` | sign、`pickaxe_poke`、Scratch browser保存、protocol 23 cleanup | 2026-08-31 |
| b7 | `23.1.0`／`2301.0.0b7` | direction、damage-capableな`world.strikeLightning`、ParticleBuilder内部移行 | 2026-09前半 |
| b8 | `23.2.0`／`2302.0.0b8` | entity lifecycle、particle receiver／typed data、Python surface | 2026-09後半 |
| 条件付きb9 | `23.3.0`／`2303.0.0b9` | 同じparticle specを使うbounded batch | 2026-09末まで |
| rc | b8またはb9と同じcore | API freeze、capacity、soak、rollback | 2026-10 |
| 初回stable | rcと同じcore | 全component mature、配布・運用説明を固定 | 2026-11 |

b9を使わない場合のstable coreは`2302.0.0`、使う場合は`2303.0.0`です。b9はb8の3D graph prototypeで
単点RPCが実際の律速になり、batchが初回stableに必要と観察された場合だけ使います。event filter／clear、
追加particle type、追加receiver、保存、legacy整理の残件箱にしません。9月末で新API追加を止めます。

この表のb7 direction、b8 entity lifecycle、条件付きb9は、2026-08-26時点で概念別縦sliceを作るための
有力な計画仮説であり、method名を固定した不変のscope freezeではありません。Paper APIとmcpiから見つかるAPI、
3D turtle graphics、agent型建築、別言語展開を学習パスと実装単位の両面で比較し、人間レビューを通してb7〜b9を
自己完結した縦sliceへ組み替えられます。短期betaは`2026-08-28-02`の軽量release modeで早く公開し、問題が
見つかった場合は観測を残してchange coneまで戻り、通常は次のbetaへroll forwardします。

組み替え可能であることを、無関係なAPIを一つのbetaへ押し込む理由、b9を残件箱へ戻す理由、9月末のAPI freezeを
暗黙に後ろへ動かす理由にはしません。新候補は「できる」だけでなく、どの位置でprototypeし何をpluginへ
昇格するか、どの学習経路を開くか、一つのfixture／実機pulseで閉じられるかを示して採否と配置を決めます。

### 3.1 b6 — sign、poke、保存、cleanup

b6は次を一つのprotocol 23 compatibility setとして閉じます。

- `world.getSign`／`world.setSign`／`world.updateSignLine`。exact contractは`2026-08-26-05`。
- `block_right_click`を削除した`pickaxe_poke`。b5／protocol 22の履歴は変更しない。
- Scratch作品／スプライトのbrowser保存。OS clipboard移送は`deferred`。
- protocol 23で発行するentity handle prefixを`mcr_eh_`へ変更する。protocol 22の`mceh_`はb5履歴にだけ残し、
  alias受理やmigrationは作らない。
- 未批准legacy entity methodをb6 registryへ出さない。対象は`world.getNearbyEntities`、
  `entity.getPos`／`setPos`、`entity.getRotation`／`setRotation`、`entity.getPitch`／`setPitch`、
  `entity.getYaw`／`setYaw`、`entity.remove`。後続で採用する概念は新contractとして戻す。

McRemoteのsign、`pickaxe_poke`、`mcr_eh_`化とlegacy entity method除去、scratch-editorのbrowser保存、
sign、`pickaxe_poke`、Pythonのprotocol 23／sign／`pickaxe_poke`／`mcr_eh_`投影にはpush済み実装candidateが
あります。2026-08-27に三repoがScratch ownerの`sign-v23.json`／`events-v23.json`をexact bytesで消費し、
sign errorの`data.allowed`順も`2026-08-27-03`で収束したため、共有fixture gateをPASSしました。現行source setは
McRemote `88d818703be5e7314bc1e45597a66237796db641`、Python
`0ba22e80b9b1b339dfd11085b1b24cef646599b2`、Scratch
`104f194deddc9c244e6e07c4223965c792551f9d`です。このsetから未公開の
`b6-artifact-candidate-set-1`を再現可能なbytesとして固定しました。exact artifact identityは
[`b6 artifact candidate記録`](b6-artifact-candidate-record_ja.md)を正とします。通常devでの実plugin接続、
正式evidence、default branch統合、公開releaseは別gateです。

scratch-editor `agent/b6-wirescope-display-filter@3c199b08645306fc77441f59e89d5ebacbb9d836`は、Scratch VM、
WireScope source adapter、`@mc-remote/live`のhandle検証を`mcr_eh_`へ揃え、旧`mceh_`を受けず、protocol
22の歴史fixture `spawn-v22.json`を現行protocol fixtureへ読み替えず残したpush済みcleanup candidateです。
同commitはtest harnessのprotocol major直書きを現行`PROTOCOL_VERSION`参照へ改めています。対象test／lint／
buildは搬送元でPASSしましたが、default branch統合、実plugin接続、横断fixture、正式evidence、releaseは別gateです。

WireScope表示側filterはclient-onlyの独立companionです。b6に間に合わなければb7以降へ送り、b6をHOLDに
しません。server側`events.poll` filterとは別物です。scratch-editor
`agent/b6-wirescope-display-filter@c720341a2cee4b01f2b2a227cf6379ac0ac92db2`には表示filterと
`dropped_frames`修正のpush済み実装candidateがあります。`2026-08-27-01`で現行のmethod／event分類、pair、
検索、件数、保存state、UI表示集合をclient-only UX v1として受理しました。wire／server filter／observer allowlistは
変更せず、exact表示挙動は`15-wirescope/wirescope-deployment-design_ja.md` §14を正とします。

2026-08-27時点のScratch b6 component入力は、上記の個別candidateと作品／スプライトbrowser保存を合流した
`agent/b6-integration@040f06617c80e54cdba9421b6c69445efdf099ba`から、protocol mirror／owner fixture／診断versionを
補った`agent/b6-source-refresh@104f194deddc9c244e6e07c4223965c792551f9d`へ進みました。統合時点のscratch-vmは4217/4220件をPASSし、
残る3件は既知の並列cascading timeoutとして単独118/118件をPASSしました。scratch-vm／scratch-gui build、
変更範囲lint、`@mc-remote/live` 124/124件もPASS報告済みです。このidentityをScratch component candidateとして
変更凍結しました。refreshではprotocol 22/22、対象VM 416/416、build／lintをPASSし、三repo共有fixture gateも
PASSしました。exact candidate artifactは後続set 1として固定済みですが、実plugin接続、shared環境deploy、
default branch統合、releaseは未実施・未主張です。
個別candidateの履歴は実装由来として残し、共有fixture／protocol 23 coreの基準identityにはrefresh identityを使います。

同source setから固定した`b6-artifact-candidate-set-1`は2026-08-27の通常dev Tier 2で、server runtime、
exact Python wheelのsign三操作／`mcr_eh_`、exact Bridgeのone-shot実plugin一往復までPASSしました。
[formal record](../14-evidence/records/2026-08-27-b6-tier2-integration-pulse_ja.md)はScratch実ブラウザ、
WireScope、`pickaxe_poke`を未実施として分離しており、b6横断gateはOPENのままです。Bridgeの`dist/` tarが
production dependencyを同梱しない点も、公開配布形態のartifact gateへ残しています。

その後のreal-browserで、mini dropdownのclipと、pending `events.poll`の一瞬表示＋全table再構築によるcopy阻害を
発見しました。前者はGUI source `1d1b21d5acdbabdb596476c087c14033d5c33d32`、後者はWireScope source
`7b4f71d71e8ecd665d402682e677dc4e425d160f`で閉じ、後者は実plugin接続でも非点滅、copy維持、poke pair、
player pair切替をPASSしました。さらに`24077ef005e4969bf3a7434b45532ae53cefbc28`でclient-onlyの表示一時停止を
追加し、実plugin接続browserでtable固定、新着件数、copy、一括再開をPASSしました。表示停止はframe収集／poll／
`dropped_frames`を止めず、wireやserver filterを変えません（`2026-08-28-01`）。

Tier 2実証へ投入した未公開artifact入力は`b6-artifact-candidate-set-3`です。McRemote／Python／Bridgeはset 1、GUIはdropdown
修正版set 2からexact bytesを再利用し、WireScope ZIP／manifestだけを`24077ef…`から生成したbytesへ置換しました。
完全identityとset 1／2の失敗履歴は[`b6 artifact candidate記録`](b6-artifact-candidate-record_ja.md) §7、
実browserの観測範囲は
[`2026-08-28-b6-scratch-wirescope-live-human`](../14-evidence/records/2026-08-28-b6-scratch-wirescope-live-human_ja.md)
を正とします。`pickaxe_poke`、Scratch sign text-only v1、作品／スプライトbrowser保存、WireScopeの現行allowlist
method、filter安定化／pauseまでTier 2 requested sliceをPASSしました。観測target変更とlive `dropped_frames`はb6 coreの
HOLD条件にしません。Bridgeの3,052-byte tarは`ws`をexternal importする中間buildで、release packageへ昇格させません。

2026-08-28、McRemote `main@4e8f1ff1bd48bfa28c465f2dc24060fbb419317f`、Python
`main@a30a37b15658da655fe1e3535a73fb0e80c06f56`、scratch-editor
`develop@df9264ec355dd722a848df46e96d4b0fc9340ca2`へのdefault branch統合を完了し、
`b6-integrated-source-set-1`として固定しました。Python／Scratchはcandidateとの機能差分がありません。
McRemoteはmainにあったb4／b5実証済みsession token永続化fixを保持したため、統合JARはset 3のJARと異なる
SHA-256 `0ec8d4c0b105f3034361b260fc39fcb78013e932e684d34d5ca95c9a6c6a87a6`になりました。
したがってset 3のTier 2 PASSは消さずに再利用しますが、旧JARを最終artifactへ流用しません。統合sourceからの
最終artifact固定、既決のOCI境界によるScratch／Bridge生成、公開releaseが残るため、この時点のb6横断gateはOPENでした。

同日、Scratch／Bridge OCIを除く六artifactを`b6-integrated-artifact-input-1`としてclean再生成・durable stagingへ固定しました。
McRemote統合JARは通常devで起動、credential `HEALTHY`、auth否定4 path、新規session、同じJARの正常再起動後に
pairingなしで行う期限内session再利用と認証済み`catalog.get`までPASSしました。正式記録は
[`2026-08-28-b6-integrated-artifact-smoke`](../14-evidence/records/2026-08-28-b6-integrated-artifact-smoke_ja.md)
を正とします。残件はScratch ownerのexact test集計、明示承認後のScratch／Bridge multi-arch OCI生成／push／container smoke、
最終artifact set固定、release判定です。artifact identityの詳細は
[`b6 artifact candidate記録`](b6-artifact-candidate-record_ja.md) §8／§9を正とします。

同日、明示承認後のmanual workflowでScratch／Bridge multi-arch OCIをGHCRへpushし、index／platform／attestation
identityを照合しました。六artifactとOCIを`b6-artifact-candidate-set-4`として固定し、McRemote
`v1.21.11-2300.0.0b6`、Python／Scratch `v2300.0.0b6`のGitHub prereleaseを公開しました。三tag target、
prerelease／draft、Latest非対象、McRemote JAR asset、release notes digestをAPIで確認し、b6横断gateをCLOSEDとします。
公開identityとnon-claimは[`b6 artifact candidate記録`](b6-artifact-candidate-record_ja.md) §10／§11を正とします。

### 3.2 b7 — direction、world effect、ParticleBuilder Stage 1

次のget／setを分割せず、実装・fixture・教材を一つの縦sliceへ閉じます。

- `player.getDirection`
- `player.setDirection`
- `entity.getDirection`
- `entity.setDirection`

getは現在の向きを正規化した`[x,y,z]`として返します。setは有限な非zero vectorをscale-safeに正規化し、
位置とdimensionを変えずrotationだけへ適用してpost-read値を返します。zeroは`zero_direction`、出力は最大6桁
`HALF_UP`、wire norm toleranceは`1.5e-6`です。entity AI等が後から向きを変え得るため方向lockとは説明しません。
params／result、handle lifecycle、work順序を含むexact contractはwire §5.8.2を正とします。

`getRotation`／`setRotation`、`getPitch`／`setPitch`、`getYaw`／`setYaw`の六methodは採りません。
`lookAt(target)`はclient APIまたはユーザーコードで`target - current_position`を組み、`setDirection`へ渡せます。
これは機能実現の位置と昇格モデルを観察する3D turtle graphicsの基礎になります。

同じb7へ`world.strikeLightning`を置きます。旧`world.strikeLightningEffect`候補は実装入力から除外し、
damage-capableなPaper full lightningをorigin相対のexact targetへ要求します。hello時のsession admission snapshot、
X／Z build range、専用rate、cost 256のwork admission、chunk load、`World#strikeLightning` exactly onceまでを副作用順として固定し、
成功resultは`null`です。damage／fire／rod／copper／entity変化は起こり得ますが個別結果を返さず、視覚／音響や
後続tickもbarrier保証しません。exact contract、fixture、live／non-claimはwire §5.8.2を正とします。

既存`world.spawnParticle`のplugin内部実装はPaper `ParticleBuilder`へ移します。これはStage 1であり、wire、
既定receiver、`particle`／offset／speed／count／force、result、errorを変更しません。Paper APIの置換だけを
理由にprotocolを上げず、b7が新method追加で`23.1.0`になるreleaseへ内部移行を同梱します。Paper 1.21.11と
26.2で同じ既存fixtureと代表描画を確認し、Stage 2のreceiver／typed dataを載せる足場にします。

McRemote `codex/b7-direction-lightning-particle@893baa917500770b00119dbfe85ccf236f5755af`は2026-09-01に
server-side `implemented` candidateへ到達した。Paper 1.21.11全189 tests、build、Paper 26.2／Java 25 compileと
対象41 tests、candidate JAR digestをknowledge側でも再照合した。Scratch ownerは
`agent/b7-protocol-owner-fixture@607cda40588ec4579c503d457c3784385419ac65`で81 caseのfixtureを発行済みで、
SHA-256は`faad66c93d2c8ee8eb541f6b7297163cb681054b3de05ba3d130ac4288c1046a`である。McRemote
`9db95e8af0bcc9feaf66c1bbbffc05b9fb8304e0`は同じfixture bytesを消費し81 caseをproduction pathへ対応付けたため、
protocol owner／server間の横断shape確認はCLOSEDである。Pythonも
`codex/b7-python-pass-a@c9e0c19925a56dbcece409982df1b707d41f51ae`でfixture exact bytesと81 case ledgerを消費し、
direction四method、full lightning、observer、README／starterを含むcomponent candidateへ到達した。対象47/47、全252/252、
buildとmetadataのPASSが報告され、Pythonのfixture消費gateもCLOSEDである。Scratch学習者向けsurfaceを待たない。次のserver
gateはcoordinatorが許可したtargetでの短いlive-auto／live-humanであり、Python実plugin代表往復は同じexact setへ接続する。
candidate sourceとfixtureだけからdamage／fire／entity変化等のlive結果、学習者向けclient surface、artifact統合、
公開releaseを推測しない。

その後のliveで、外部dimension移動後のhandle reason不一致と、online playerに`mcr.online`があっても旧
`mcr.lightning`不足で拒否する権限設計の問題を確認した。`2026-09-01-02`は後者を改訂し、`mcr.online`／
`mcr.offline`を独立した状態別permissionとしてhello時に一度snapshotし、個別`mcr.lightning`を削除する。
したがって上記fixture SHA-256 `faad66c93d2c8ee8eb541f6b7297163cb681054b3de05ba3d130ac4288c1046a`と
三componentの消費PASSは旧contractを満たした履歴であり、新contractの完成根拠ではない。b7 gateは、successor owner
fixture、McRemoteのsession admission／handle reason修正、各consumerのexact fixture再消費、対象live-autoが揃うまで
**HOLD**とする。Scratch学習者向けsurfaceは引き続き開始条件にしない。

### 3.3 b8 — entity lifecycle、ParticleBuilder Stage 2

次をread／writeへ分けず、handle取得、状態観察、移動、終端まで一つの縦sliceへ閉じます。

- `world.getNearbyEntities`
- `entity.getPose`
- `entity.setPose`
- `entity.remove`

nearbyの一覧は、探索後すぐ使えるsnapshotとして少なくともopaque `handle`、canonical `type`、`pos`を返す
方向とします。yaw／pitch／direction／full poseは一覧へ重ねず個別getterに任せます。player除外、bounded検索、
chunk loadなし、request全体のhandle capacity事前確認を維持します。exact params、radius／件数上限、terminal
error、set失敗の原子性はb8 contract lockで固定します。

particle Stage 2では、既存のdata不要particle文字列とworld全体への既定配送を壊さず、receiver選択と有限なtyped
dataを後方互換な追加としてcontractします。最初のreceiver候補は既定の`world`と呼出playerだけの`self`に絞り、
任意player一覧、UUID、距離指定は同じsliceへ入れません。typed data候補はdustの色＋sizeとblock particleの
`BlockSpec`に絞り、任意Java object、item、transition、trail、vibrationを受けません。exact wire shape、methodを
既存`world.spawnParticle`の拡張にするか別methodにするか、result／error、capはb8 contract lockで固定します。

Python surfaceと3D graphの小さいapplication sampleをb8 acceptanceへ含めます。receiverが実際に対象playerだけへ
届く2-player確認、dust／blockの描画、1.21.11／26.2のdual-target pulseをchange coneに入れます。Scratchは
protocol mirrorと互換認識を先に揃えられますが、学習者向けblockは別trackで追従し、b8 plugin／Python releaseを
自動的にHOLDしません。

### 3.4 条件付きb9 — ParticleBuilder Stage 3

b9は、b8と同じreceiver／typed data specを複数点へ適用するbounded batchだけを候補にします。全入力を検証してから
一括accept／rejectし、point数、入力byte、work、receiver fan-outを有限にします。costは少なくとも
`points × receivers`を反映し、成功resultは受理point／配送規模を観察できる方向でcontract lockします。
新しいparticle typeやreceiver modeをb9へ便乗させません。

b8のPython 3D graphを単点`FAST`で描いて十分ならb9を使わず、Stage 3をrc後へ送って`23.2.0`をfreezeします。
RPC／再描画負荷が実測上の問題で、bounded batchが初回stableに必要な一つの自己完結sliceと判定できた時だけ
`23.3.0`として実装します。`events.poll` filter／`events.clear`はこのb9へ入れません。

### 3.5 2026-08-29時点の新API候補pool

次はscope lockでなく、Paper 1.21.11 APIと学習用途から発掘した`candidate`です。b7〜b9へ入れる場合も、exact
params／result／error、有限性、副作用、client surface、sampleを一つの縦sliceとして人間レビューします。

| 候補概念 | Paper側の足場 | 主な価値 | contract lock前の中心論点 |
| --- | --- | --- | --- |
| `lookAt` | `Entity.lookAt(position, anchor)`／`Player.lookAt(entity, …)` | walkthrough、playerを使う3D turtle、目標点への注視 | 座標targetとhandle targetを一methodにするか、anchor、dimension、AIによる後続変更 |
| marker／waypoint | server-only `Marker` entity、または別の可視entity | 移動可能な基準点、entity target、後続agentの足場 | 座標`lookAt`の前提にはしない。不可視Markerか可視markerか、spawn／setPos／remove、handle lifecycle、method名 |
| `rayTraceBlocks` | precise collision shapeを使う`World.rayTraceBlocks` | HUD、照準先、空間理解、相対／絶対座標の橋渡し | max distance、build／query許可範囲、chunk生成cost、fluid／passable、miss、hit位置／block／faceの正準result |
| block preview | `Player.sendBlockChange`／`sendMultiBlockChange` | 非破壊の建築preview、確認してから実配置 | player限定表示、bounded batch、client view範囲、復元／disconnect／chunk resend、実world stateとの区別 |
| output target | real world／player別preview／pygame | 同じ建築codeを実配置、非破壊preview、画面描画へ向ける | `DEBUG`／`TRACE`／`FAST`と別軸、preview lifecycle、collisionを伴わないこと、cleanup |

Paper 1.21.11では`Player`も`Entity`から座標指定`lookAt`を継承するため、座標targetだけを理由にmarker entityを
経由しません。`Marker`はserver内だけに存在し、人間に見える目印ではありません。marker候補は移動するhandleや
agent／waypointとして別に評価します。`rayTraceBlocks`は一request一rayを基本にし、現行block queryと同じく
許可された範囲で必要なchunkをload／generateし得ます。必要chunkを見ずに確定missを返す`loaded-only`意味論は
採りません。v0候補は最大距離100未満かつbuild／query許可範囲内とし、要求distanceをworkへ計上します。多数rayで
風景画を作る用途はRPCへ押し込まず、bounded `getBlocks`結果を下流で解析します。

block previewは実worldとcollisionを変えないplayer限定描画です。通常clearは触れた座標を記録し、clear時点の
実`BlockData`を読み直して同じplayerへ再送します。`World.refreshChunk`は全viewerへchunkを再送する重い操作なので
通常APIにしません。clientがchunk dataを再受信するteleport／dimension change／reconnectで見え方が戻る場合はあっても、
それを正式なclear契約にしません。実world、preview、pygameの出力先切替は下流prototypeから始め、共通lifecycleや
性能保証が必要になった時に昇格を検討します。

### 3.6 初回stable後の3D turtle／agent track

本格的な3D turtle graphicsは独自Mobと独自AIを使う2027年春以降のtrackとする。教育版Minecraftのagent式建築を
そのまま複製せず、移動、向き、建築、観察、AIの一部をMcRemoteの学習pathとして再構成する。Scratchでは必要に応じて
extensionを機能群へ分割し、Python／別言語では同じ概念をその言語に自然なAPIとsampleで示す。この将来trackを
b7〜b9や初回stableのcompletion条件にはしません。

## 4. Minecraft／Paper target

b6は1.21.11で閉じ、直後にPaper 26.2 compatibility pulseを独立実施します。Java 25 build、plugin
enable／disable、通常再起動、DimensionKey、resource registry、block／sign、entity、event、scheduler、
認証済みhelloと代表read／write／event／handleを確認します。protocol、client、observer schemaが不変なら
全client受入を再実施せず、change cone外のPASSを根拠付きで再利用します。

初回stableは1.21.11を維持し、加えてplatform target freeze時点で採用可能なPaper 26.xを一つsupportします。
既定候補は26.2です。26.3はMojang正式releaseとPaper stableが成立し、同じpulseを通過した場合だけ26.2と
置き換えられます。26.3の9月予測をsupport確約にしません。

plugin compatibility pulseと公開serverのworld migrationを同じgateにしません。公開server移行はclone上の
world upgrade、旧runtime＋旧world snapshotへのrollback、credential store非包含、Stack lock更新、
public beta先行soak、人間批准、doctorを別途要求します。

## 5. Release gateの強さ

実装中はTier 0／1、通常dev integration harnessでTier 2を反復します。candidate freeze後だけchange cone内の
Tier 3へ進み、10月rcでTier 4、capacity、soak、rollbackを閉じます。各betaでfull soakを繰り返しません。

初回stableは次を満たします。

- rcで`frozen`になったmethod集合がplugin／Python／Scratch／WireScopeの必要surfaceで一致する。
- exact source／artifact identity、shared fixture、formal evidence、rollback先がある。
- 1.21.11と採用Paper 26.xのsupport gateを分けて通す。
- install／update／rollback／既知制約の利用者向け入口がある。

stable後の小変更は、同じstable coreへbeta suffixを足さず、次coreの`bN → rc → stable`で進めます。

## 6. 却下案

- 旧b6 scopeを8月末へ一括投入する。
- getをb7、setをb8へ機械的に分ける。
- b9を9月残件の無条件な受け皿にする。
- ハードフォーク前の全method復帰を初回stable条件にする。
- raw UUID／comma-separated resultをprotocol 23へ持ち越す。
- `mceh_`と`mcr_eh_`をprotocol 23で両方受ける。
- 26.3の予測日をsupport確約にする。
- plugin pulse合格だけで公開serverのworld migrationを許可する。

## 7. 外部入力

時点依存の外部事実は[external-facts](../00-hub/external-facts_ja.md)の
`F-mojang-release-cadence`／`F-paper-support-flags`を正とします。exact Paper buildは変動値として
gate manifestへ取得し、本ロードマップへ固定しません。
