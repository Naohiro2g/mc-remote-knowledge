# betaから初回stableまでのreleaseロードマップ

> 2026-08-26確定。DECISIONS `2026-08-26-08`の説明とmethod／surface capability台帳です。
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

| release | protocol／artifact core | concept slice | 目標時期 |
| --- | --- | --- | --- |
| b6 | `23.0.0`／`2300.0.0b6` | sign、`pickaxe_poke`、Scratch browser保存、protocol 23 cleanup | 2026-08-31 |
| b7 | `23.1.0`／`2301.0.0b7` | direction | 2026-09前半 |
| b8 | `23.2.0`／`2302.0.0b8` | entity lifecycle | 2026-09後半 |
| 条件付きb9 | `23.3.0`／`2303.0.0b9` | stable必須の自己完結slice一つだけ | 2026-09末まで |
| rc | b8またはb9と同じcore | API freeze、capacity、soak、rollback | 2026-10 |
| 初回stable | rcと同じcore | 全component mature、配布・運用説明を固定 | 2026-11 |

b9を使わない場合のstable coreは`2302.0.0`、使う場合は`2303.0.0`です。b9はevent filter／clear、typed
particle、保存、legacy整理の残件箱にしません。9月末で新API追加を止めます。

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
追加し、deterministic real-browserまでPASSしました。表示停止はframe収集／poll／`dropped_frames`を止めず、
wireやserver filterを変えません（`2026-08-28-01`）。

現行の未公開artifact入力は`b6-artifact-candidate-set-3`です。McRemote／Python／Bridgeはset 1、GUIはdropdown
修正版set 2からexact bytesを再利用し、WireScope ZIP／manifestだけを`24077ef…`から生成したbytesへ置換しました。
完全identityとset 1／2の失敗履歴は[`b6 artifact candidate記録`](b6-artifact-candidate-record_ja.md) §7、
実browserの観測範囲は
[`2026-08-28-b6-scratch-wirescope-live-human`](../14-evidence/records/2026-08-28-b6-scratch-wirescope-live-human_ja.md)
を正とします。`pickaxe_poke`の一操作一eventと腕振り、Scratch→WireScopeの現行allowlist method、filter安定化は
PASSしましたが、Scratch sign／browser保存のexact integrated artifact確認、Bridge package境界、default branch統合、
公開releaseが残るためb6横断gateはOPENです。表示filter／pause単独の未確認はb6 coreのHOLD条件にしません。

### 3.2 b7 — direction

次のget／setを分割せず、実装・fixture・教材を一つの縦sliceへ閉じます。

- `player.getDirection`
- `player.setDirection`
- `entity.getDirection`
- `entity.setDirection`

getは現在の向きを正規化した単位vectorとして返します。setは有限な非zero vectorを受け、その大きさを
捨てて向きだけへ正規化して適用します。位置とdimensionは変更しません。entity AI等が後から向きを変え得るため、
方向lockとは説明しません。exact params、result shape、zero vector error、出力精度はcontract lockで固定します。

`getRotation`／`setRotation`、`getPitch`／`setPitch`、`getYaw`／`setYaw`の六methodは採りません。
`lookAt(target)`はclient APIまたはユーザーコードで`target - current_position`を組み、`setDirection`へ渡せます。
これは機能実現の三層モデルを観察する3D turtle graphicsの基礎になります。

### 3.3 b8 — entity lifecycle

次をread／writeへ分けず、handle取得、状態観察、移動、終端まで一つの縦sliceへ閉じます。

- `world.getNearbyEntities`
- `entity.getPose`
- `entity.setPose`
- `entity.remove`

nearbyの一覧は、探索後すぐ使えるsnapshotとして少なくともopaque `handle`、canonical `type`、`pos`を返す
方向とします。yaw／pitch／direction／full poseは一覧へ重ねず個別getterに任せます。player除外、bounded検索、
chunk loadなし、request全体のhandle capacity事前確認を維持します。exact params、radius／件数上限、terminal
error、set失敗の原子性はb8 contract lockで固定します。

### 3.4 条件付きb9と後続

`events.poll` filter、`events.clear`、typed particle dataはb9または後続minor候補です。9月中旬に、初回stableの
学習・運用体験へ不可欠で、かつ一つの自己完結sliceとして閉じられるかを判定します。該当しなければrc後へ送ります。

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
