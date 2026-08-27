# WireScope deployment 設計

> 状態: `2026-08-10-02` の配置に関する説明正本。共通appのattach／session／artifact契約とPython
> browser-loopback参照profileは[station attach設計](wirescope-station-attach-design_ja.md)および
> `2026-08-11-02`／`2026-08-11-03`を参照する。

## 1. 三役と共通責務

WireScopeは、sourceがallowlist済みの観察データを差し出し、stationが配り、browserが読むsystemである。

```text
source client
  └─ generation-side allowlist
        └─ source-specific transport
              └─ WireScope station
                    ├─ app artifact提供
                    ├─ source ingress
                    ├─ target／observer session broker
                    ├─ browser endpoint
                    └─ finite non-persistent buffer role
                          └─ browser observer session
```

`WireScope station`は、あるdeploymentにWireScopeを提供する論理runtime境界である。物理PC、単一process、
source transport、artifact registryのいずれとも同義ではない。Scratchでは複数roleをopener、MessagePort、
別origin appへ融合でき、LAN／VPSではingress、broker、artifact serverを分離できる。

## 2. 固定するものと固定しないもの

共通に固定するものは次である。

- `mcremote.observer` schemaと共通UI
- generation-side allowlistと秘密境界
- target／stream lifecycle
- read-only observer capability
- observer dataを永続化しない境界
- 全bufferが有限であること
- observer障害がMinecraft connectionを壊さないfailure semantics

次はdeployment／sourceごとに選べるため、一種類へ固定しない。

- source discovery
- source-to-station transport
- roleを一processへ融合するか分離するか
- loopback、LAN、public HTTPS等のtopology
- finite bufferのprocess上の所有者と具体上限

## 3. Capabilityとデータ境界

- publish主体は、自分がpublishするtargetに限りattach grant発行を起動または要求できる。
- publish主体は他targetの一覧・alias・観察資格を得ない。
- attach capabilityからpublish capabilityを導出しない。
- observer dataをpublishする能力と、Minecraftへcommandを送るcontrol capabilityを同一視しない。
- display aliasは発見、列挙、接続、認可、player識別に使わない。
- target一覧とdisplay alias一覧も無認可の公開情報にしない。
- operatorはdeployment runtimeとbufferへ到達できる信頼主体として明示する。
- McRemote token、pair code、credential、UUID、内部transport状態をobserver認証へ流用しない。
- sanitized observer dataもpublic dataでなくtarget-scoped confidentialを既定とする。

### 3.1 Display alias contract v1

人間がtargetを目視照合する`display_alias`はsource種別に依存しない共通生成contractとする
（`2026-08-12-03`）。canonical vocabularyは次の16語である。

```text
MIND STORM SOCIETY PAPERT RESNICK PIAGET MINSKY LIFE
DNA MUSIC WAVE BRAIN SELF APPLE ORANGE LEMON
```

canonical表示は`WORD-WORD-NNNNNN`で、ASCII hyphenとゼロ埋め6桁のASCII数字を使う。例は
`MIND-STORM-000027`である。単語と数値の選び方はsource固有でよいが、語彙、表示形式、target lifecycle、
active alias衝突時の再生成、安全境界は共通とする。機械可読正本はScratch
`develop@3b3d1f1c8a0dd66d265c5c6ea515cc5ac291209b`の
`mc-remote/live/test/fixtures/display-alias-v1.json`（SHA-256
`85c8159a8b74788c0cf978078094d23a3cdae83c0be5e9aa9552bb820c8389ca`）である。

aliasはauthenticated hello後のtarget成立時に生成し、connection epoch中は固定する。再接続で新targetが
成立したら新しく生成し、同じtargetを複数observerで見る場合は同じaliasを使う。同一stationでactive aliasが
衝突した場合は再生成する。aliasは非秘密の表示専用情報であり、target／stream ID、discovery／search key、
attach capability、認可、player識別に使わず、UUID、接続先、credential、session／target IDを符号化しない。
`source_kind`は別metadataとする。

observer schema v1の`display_alias`は引き続きnon-empty stringを受理し、旧sessionや移行中sourceを拒否しない。
canonical formatは新規・更新sourceのgeneration-side conformanceで検査する。alias contractのversion交換方式は、
必要になるまで固定しない。

source ingressとbrowser attachを同一network endpointへ載せる場合、最初のmessage種別だけで権限を分岐せず、
型付きcapabilityまたは同等の分離を必要とする。具体方式は未確定である。

## 4. Profileの分類軸

profileは「個人」「教室」等の利用者属性でなく、source、station、browser三者のaddress spaceとnetwork
namespaceの関係で分類する。

| 関係類型 | top-level WireScope | sourceからstation | 例 |
| --- | --- | --- | --- |
| browser-loopback到達 | browser自身のloopback origin | 同一namespaceまたは明示的IPC／bridge | native Python、同一OS |
| deployment LAN到達 | deploymentのLAN origin | deployment内IPCまたはsource発outbound | 教室、VPN、閉域網 |
| public HTTPS到達 | public HTTPS origin | 認証済みsource発outbound | 公式VPS、公開beta／stable |
| Scratch handoff | 別origin WireScope | opener＋`MessageChannel` | Scratch参照実装 |

Jupyter、WSL、Docker、SSH、remote notebookでは「個人利用」でもbrowser loopbackとsource loopbackが同じとは
限らない。profile判定は実際のnamespaceと到達関係から行う。

### 4.1 公開browser surfaceのhostname

公式のcross-origin browser source handoff用WireScope appには、source非依存でchannel-boundな
public canonical hostnameを与える（決定`2026-08-20-01`）。

| channel | public canonical hostname |
| --- | --- |
| stable | `wirescope.mc-remote.com` |
| beta | `wirescope-beta.mc-remote.com` |
| alpha | `wirescope-alpha.mc-remote.com` |
| dev | なし |

stableは無接尾辞、beta／alphaは`<surface>-<channel>.mc-remote.com`とする。旧`scope.mc-remote.com`は、
起動導線がruntime config／linkとなって手入力の短さが利点でなくなり、完全なWireScopeブランド名の識別性が
上回ったため改訂する。channelからexposureは導出せず、public canonical hostnameを提供するenvironmentだけが
上記名を使う。

このhostnameは利用者が開く共通WireScope browser app surfaceを表す。station process、物理host、provider、
source ingress、source kind、protocol／schema／artifact version、target／stream identityを表さない。
`wirescope-station-*`や`wirescope-scratch-*`等のrole／source別public hostnameを作らず、内部service名だけに
`wirescope-station`、`wirescope-app`、`wirescope-ingress`等を使える。

b4の公開Scratch betaは次のorigin関係を取る。

```text
https://scratch-beta.mc-remote.com
        └─ cross-origin MessageChannel handoff
           └─> https://wirescope-beta.mc-remote.com
```

Python browser-loopbackは同じapp artifactを`http://127.0.0.1:<ephemeral-port>/`から提供し、public hostnameを
使わない。共通なのはartifact bytes、detached manifest、schema、session envelope、UI、validator、artifact
identityであり、deployment originとresponse headerではない。public pageからloopback stationへfetch／WebSocketを
伸ばさない。

cross-origin handoffの成立は、source originとWireScope origin双方のresponse header／runtime configを一組で
検証する。source側は現行adapterが要求するdistinct absolute referrer originをselection window中に渡せること、
WireScope側はopenerを同window中に切断しないことをbrowser smokeで確認する。Python loopback stationの
`Cross-Origin-Opener-Policy: same-origin`をpublic handoff originへ流用せず、逆方向にも流用しない。同一URLを
query parameterや未認証入力で異なるsecurity profileへ切り替えない。exact CSP／COOP／Referrer-Policy／cacheは
deploy fixtureで固定する。

LAN-only／isolated profileはpublic canonical hostname規則の対象外である。operator管理下のDNS namespaceを使い、
scheme、hostname、port、TLS／local CA、browser origin、station authority、certificate identityをprofile／lockへ
exactに固定する。`.local`はmDNSと衝突するため通常DNS suffixとして無条件に正典化しない。official public
same-origin stationが同じcanonical hostnameを使うかは、source ingressとheader profileを伴う後続決定で扱う。

## 5. LNAとbootstrap

- browserはtop-level WireScopeよりprivateなaddress spaceへobserver endpointを伸ばさない。
- loopback profileではWireScope自体をloopback top-level pageとして開く。
- LAN profileではdeploymentのLAN originをtop-levelとして開く。
- public profileではpublic HTTPS originをtop-levelとして開く。
- main-frame navigationへの現在のLNA例外をsecurity boundaryにしない。
- QRは対象deploymentのtop-level URLを直接示す。
- public bouncerを使う場合もnavigationだけとし、local addressへfetch／WebSocketを行わない。
- same-originだけでtargetの観察認可が成立したとは扱わない。

same-originはscheme、host、portの一致で判定する。loopbackはaddress-space分類であり、`localhost`、
`127.0.0.1`、`[::1]`が同じoriginという意味ではない。

## 6. Source別の初期形

### Scratch

現在の別origin WireScope、送信元windowとexact originの検証、exact `targetOrigin`、`MessageChannel`、
15秒有効・一回限りのgrantを維持する。Scratch adapterとして有効なhandoffを得ないbrowserには、Scratch targetの
観察能力を与えない。same-origin station bootstrapが成立する別profileまで禁止する意味ではない。

### Python

schema v1 adapter、generation-side allowlist、main connection lifecycle fixtureは合格済みである。launcher、
station、browser attachは未実装である。最初の参照profileはsource／station／browserが同じnetwork namespaceに
あるbrowser-loopbackへ限定し、station roleをPython source processへ融合する。UDS、named pipe、cross-process
relay、LAN／VPSはこの初期profileへ含めない。詳細は[station attach設計](wirescope-station-attach-design_ja.md)を
参照する。

### Cross-origin browser source handoffの一般化方向

Scratchはb4で検証済みの最初のbrowser source profileである。第二のbrowser-based sourceが具体化したときは、
source固有のWireScope app／hostname／stationをforkせず、共通appのcross-origin browser source handoff familyへ
登録済みsource profileとして追加する（決定`2026-08-20-02`）。browser adapterの大分類は、cross-origin browser
source handoffとsame-origin station attachの二つを維持する。

各browser source profileはregistered `source_kind`、source application identity、exact allowed source origin、
handoff protocol version、schema／session compatibility、MessagePort数、selection window、readiness、grant delivery、
target lifecycle、generation-side allowlist、failure semantics、artifact compatibility setをfixtureで固定する。未知profile、
source自己申告origin、`targetOrigin: "*"`を受理しない。openerやreferrerだけで認可せず、event source／originをexactに
照合し、grantをURL、cookie、storageへ置かない。port／grant処理後はstation attachへfallbackしない。

このhandoffはobserver dataを渡すsource-specific transportであり、Minecraft command、pairing、credential、他targetの
探索／一覧、公開source registration能力へ昇格させない。browser JavaScriptでなくbackend processが観測元なら、frontend
browserへ代理publishさせず、後続の認証済みsource ingressを使う。source種別追加とmulti-target／multi-source UI、station
federationを同じsliceにしない。

局面は第二のbrowser sourceが具体化する前の共通境界である。具体sourceがMessageChannelのsecurity／lifecycle条件を満たせない
場合は、Scratchを偽装させたり無理に同transportへ押し込まず本決定を再吟味する。exact envelopeとprofile registryは後続fixture
まで未確定であり、b4へ遡及せずb5へも自動追加しない。

## 7. Failure semanticsとbuffer

- grant不正、Origin不一致、schema不正はobserver側でfail closedとする。
- station停止、transport障害、backpressure、capacity超過はMinecraft connectionと利用者codeに対してfail openとする。
- observer処理はmain connectionへ無制限の待機、queue、同期serializeを持ち込まない。
- adapter、transport、station、browserの各bufferは有限かつ非永続とする。
- lossが生じ得る境界では、欠落を沈黙させず利用者が認識できる表現を必要とする。

schema v1にはgap、truncated、per-frame byte limitのfieldがなく、strict validatorは未知fieldを拒否する。
初期station attachでは外側のobserver session envelopeがrolling historyの省略数とendを所有し、schema v1を
変更しない。payload summaryやrecording／replay向けgap markerは後続schema version／sliceをfixtureと
Scratch／Python conformance付きで固定する。schema v1のframe windowを完全な通信記録とは主張しない。

scratch-editor `agent/b6-wirescope-display-filter@c720341a2cee4b01f2b2a227cf6379ac0ac92db2`は、Scratch VMの
`FRAME_LOG_LIMIT=100`超過trim件数をconnection単位で累積し、source adapterからsession envelopeの
`history_window.dropped_frames`へ渡す実装candidateである。累積値はframe logと同じconstructor／connection
reset境界で0へ戻り、UI filterによる非表示件数を加えない。対象unit／deterministic testと、105／125 frameを
投入して5／25を表示するdeterministic sourceの実browser確認はPASS報告済みだが、実plugin E2Eと正式evidenceは
未実施である。この局所修正は既存のloss可視化原則を実装するもので、observer frame schemaを変更しない。

## 8. Artifactと互換性

stationは固定identityを持つ`@mc-remote/live` artifactを提供する。初期artifactはarchiveとdetached manifestに
分け、consumerの外側の信頼境界が双方のhashをpinする。manifestはsource commit、build identity、observer
schema／session、handoff／attach protocol、asset inventory、license、対応sourceを記録する。runtime portや
attach codeをimmutable assetへ埋め込まない。詳細は[station attach設計](wirescope-station-attach-design_ja.md)を
参照する。

deploymentではobserver schema、session envelope、WireScope app artifact、station runtime、source ingress、
profileを完全なcompatibility setとしてlock・検証する。source ingressを含むLAN／public setは未確定である。

## 9. Lifecycleの次slice

初期observer sessionは、次の意味論を共通endへ写像する。

```text
target activated
snapshot changed
target ended
source closed
```

wire end reasonは`target-ended`、`source-closed`、`backpressure`、`capacity-exhausted`とする。
`transport-lost`はstationが送れないためbrowserがlocal terminal stateとして合成する。自動reconnect、同じ
browserを新targetへattachする方法は未確定である。observer presenceをsource／学習者へ見せるかも、privacyと
教材設計を含む別判断とする。

## 10. 未確定事項

- public handoffの両origin response header fixture、DNS／TLS／deploy／rollback／health check
- common browser handoffのexact envelope、source application identity encoding、source profile registry
- backend source ingress transport／hostname、official public same-origin station origin、dual-profile origin
- LAN／public profileのsource discoveryとsource-to-station transport
- source登録能力とbrowser attach能力のdeployment実装
- grant発行前frameを後発observerへ見せるか
- target／display alias列挙capability
- multi-user／multi-target isolation
- LAN／public station認証、rate limit、multi-user buffer分離
- payload summary、gap marker、recording／replay loss表現の後続schema version／slice（b5 schema v1.1のmethod validator拡張とは分離）
- Python非TTY／Jupyter向けattach
- artifact signing、公開deploy、rollback運用
- LAN HTTP簡易modeとHTTPS／local CAの境界
- Docker、WSL、SSH、Jupyter等のnetwork namespace差

## 11. 採らない構成

- public WireScopeから利用者のlocalhost／LANへ接続する。
- Python版を常にlocalhost relayとして定義する。
- Scratchの`MessageChannel`契約をPythonへ直輸入する。
- stationからsourceを探してpullすることを既定にする。
- stationまたはbrowserからBridge／Minecraftへ直接接続する。
- alias、target ID、session IDを観察能力として使う。
- McRemote credentialをstation認証へ流用する。
- LANを信頼済みとしてOrigin、grant、利用者隔離を省略する。
- adapterまたはstationへ無制限履歴を持たせる。

長期ビジョンは `2026-08-10-03` と本書の次節へ置く。現行observerのread-only境界を、将来のcontrol機能を
先取りする理由で緩めない。

## 12. 長期ビジョン：見る道具から創作を支える道具へ

WireScopeの発達段階を次のように置く。

```text
見る → 選んで見る・比べる → つつく → 組む
```

最初の二段はbrowser observerのread-only projectionを育てる。filter、追跡、比較、再生等を増やしても、
Minecraft control capabilityは必要ない。

「つつく」以降もbrowser observerをsourceへ変えない。同じ画面にconsole UIを置く場合、consoleは別roleの
sourceとして自前でMcRemoteへpairingし、独立したcontrol capabilityを得る。console自身のrequest／responseは
allowlistを通した別streamとしてstationへobserver publishする。

```text
console source ── McRemote command ──> Minecraft
       └─ allowlist済みの自stream ──> station ──> browser observer
```

attach、observer publish、Minecraft controlを別capabilityとして維持する。Scratch等のopenerが持つconnectionを
browserへ貸して代理送信しない。console streamと既存source streamを不可逆にmergeせず、同時表示が必要なら
出自を持つ複数streamからUIで再導出する。

この原則は、loopback web app、教室station、VPS、Electron等の梱包が変わっても同じである。場の名前は
WireScopeのまま保ち、増えたroleやcomponentを個別に命名する。consoleのtransport、pairing、command scope、
教材gateは実装着手前に別決定とする。

## 13. protocol 22／b5 method観察とschema v1／compatibility revision v1.1

b5ではobserver top-level schema version `1`を維持したままcompatibility revision／app artifact contractをv1.1へ進め、`events.poll`、`world.getHeight`、
`world.spawnParticle`、`world.spawnEntity`と新しいreasonを観察できるようにする（DECISIONS
`2026-08-16-07`）。加えて、protocol 22の`world.setBlock`／`world.setBlocks`／`world.getBlock`は、
`block_id`と`state`を分離した構造化`BlockSpec`／`BlockValue`として観察する（`2026-08-19-02`）。
ここでいう`v1.1`はmethod allowlist、validator、adapter、artifactを一組にするcompatibility setの
改訂番号である。observer snapshotのtop-level wire fieldは引き続き`schema_version=1`とし、
`schema_version=1.1`へ変更したりschema v1へ未宣言fieldを追加したりしない。

spawn系params validatorは`world.spawnParticle`の座標先行9／10 params
`[x,y,z,offset_x,offset_y,offset_z,particle,speed,count,(force)]`と、`world.spawnEntity`の座標先行4 params
`[x,y,z,entity]`だけを受理する。旧順序をunion受理せずraw frameを再配列しない。particleのforce省略と
明示booleanはraw frame上の差を保って観察し、省略値のsynthetic fieldをframeへ追加しない
（`2026-08-21-01`）。

次を一つのcompatibility setとして更新する。

- pluginのwire fixture
- observer method allowlist
- method別params／result／error validator
- Python observer projection
- Scratch source adapter
- common app artifact／manifest
- Python wheelのexact artifact pin

plugin wire fixtureのconformance完了と、共通UIおよびreal-browser E2Eの完了を別gateにする。
fixtureが通ってもUI表示・loss可視化・Scratch／Python両sourceの実browser動作が確認されるまでは
WireScope b5 gateを完了扱いにしない。

block valueのvalidatorとUIは`block_id`／`state`を文字列refへ再結合せず、同じobject shapeのまま扱う。
stateが無いblockも`state:{}`を表示・copy・fixture比較の正とし、getのfull stateとsetの部分stateを
method別validatorで区別する。protocol 21の文字列frameとprotocol 22のobject frameを一つのunion schemaで
黙って受理せず、plugin、Python、Scratch、observer validator、common app artifactのprotocol identityを
一つのcompatibility setとして固定する。

`world.setBlock`／`world.setBlocks`の部分`BlockSpec` request、`result:null`、FAST notification、
`connection.flush` request／response、`world.getBlocks`の有界array、
`block_right_click.block`、`projectile_hit.target.block`も同じvalidatorへ収容する。WireScopeは
Scratch StateText／BlockInfoTextへ再結合せず、partial request、getterのfull result、event snapshot、errorの
`data.path`を構造化frameのまま観察する（`2026-08-19-03`／`04`）。

protocol 22では`build.setDimension`、hello／player position・pose／eventの`dimension`、
`unknown_dimension`、`entity_dimension_changed`をmethod validatorとadapterへ同時投影する。DimensionKeyは
完全修飾`namespace:path`のraw fieldとして表示し、Bukkit world nameへ変換しない。旧`build.setWorld`、
`world` identity field、旧reasonとのunionを受理せず、`world.*`操作namespaceと`world_constants`は別概念として
維持する（`2026-08-22-02`）。

FASTはid省略をmachine token `sent-unconfirmed`として扱い、日本語「送信済み・結果未確認」、英語
`Sent · unconfirmed`と表示して、success／error responseを合成しない。この状態はframeのid欠落とresponse不在から
導出し、mode名、TRACE delay、synthetic status responseをobserver schemaへ追加しない。DEBUG／TRACEは
wire上では同じid付きrequestなので、frame間隔からmode名を推測しない。`connection.flush`は先行commandの
barrierとして表示するが、notificationごとの成功集約とは説明しない。mode名とTRACE delayはobserver schemaへ
追加せず、plugin、Python、Scratch、validator、common appを`2026-08-20-03`のcompatibility setで更新する。

`events.poll`のcompact response上限60 KiBは、最大合法responseをschema v1（compatibility revision v1.1）frameとsession envelopeへ通した
UTF-8 encoded bytesで検証する。escape量の多い文字列を含めても単一frame上限64 KiBを越えないことをb5 fixtureで
確認し、full load／rolling historyの本較正はb8実装後・API freeze前に行う（`2026-08-21-02`を`2026-08-26-08`で配置改訂）。

連続位置・角度はpluginがDECISIONS `2026-08-19-01`の正準numberへ変換した後のframeを観察する。
observer validatorと共通UIは座標や角度を別値へ再round／wrap／clampしない。UIが可読性のため末尾ゼロを
補う場合も、raw frame、copy、fixture比較はserverから受けたJSON numberを正とする。Scratch／Pythonで
同じframeを異なる桁へ変換しないことをcompatibility setで検査する。

本sliceで確定するv1.1はmethod観察のcompatibility境界である。payload summary、gap marker、
recording／replayのloss表現はv1.1へ含めず、後続version／sliceとして別に固定する。

## 14. protocol 23／b6の表示filter — client-only UX v1

WireScope表示filterは、sourceが既に観察してbrowserの現在windowへ保持したframeから表示対象だけを選ぶ
client-only capabilityである。wire、server event ring、`events.poll`の頻度／params／result、frame payload、
observer schemaを変更しない。server側`events.poll` filter／`events.clear`とは別sliceであり、未達でもb6を
HOLDにしない（`2026-08-26-08`）。`2026-08-27-01`はscratch-editorの現行実装をb6へ含める
**client-only UX v1**として批准した。ここでいうUX v1は表示挙動の識別であり、protocol、observer schema、
station sessionまたはartifact coreへ新しいversionを追加しない。

### 14.1 methodグループ

内部分類は次の8種＋`other`で固定する。methodはobserver validatorを通過した後、一つのgroupへ入る。

| 内部token | 写像 | 現行`OBSERVED_METHODS`の対象 | UI |
| --- | --- | --- | --- |
| `connection` | `hello`、`connection.*` | `hello`、`connection.flush` | 表示「接続」 |
| `auth` | `auth.*` | なし | 非表示 |
| `build` | `build.*` | `build.setDimension`、`build.setOrigin` | 表示「建築」 |
| `catalog` | `catalog.*` | なし | 非表示 |
| `chat` | `chat.*` | `chat.post` | 表示「チャット」 |
| `events` | `events.*` | `events.poll` | 表示「イベント」 |
| `player` | `player.*` | `player.getPos`／`setPos`／`getPose`／`setPose` | 表示「プレイヤー」 |
| `world` | `world.*` | `world.setBlock`／`setBlocks`／`getBlock`／`getBlocks`／`getHeight`／`spawnParticle`／`spawnEntity` | 表示「ワールド」 |
| `other` | 上記に一致しないmethod | なし | 表示「その他」 |

`auth`／`catalog`は将来の分類tokenとして内部stateへ保持するが、現行allowlistから到達せず常に0件なのでswitchを
描画しない。理由付きdisabled表示も作らない。`other`も現行strict allowlist下では0件だが、将来または予期しない
methodのcatch-allという役割を優先し、通常switchとして表示する。この例外を含む現行挙動をUX v1として受理する。

この表はobserver allowlist自体を拡張しない。特にb6 sign三操作`world.getSign`／`world.setSign`／
`world.updateSignLine`は現行`OBSERVED_METHODS`に含まれず、`world` filterで表示できるとは主張しない。
signを観測対象へ加える場合は、validator／adapter／fixtureの別changeとして扱う。

### 14.2 `events.poll`のevent分類

| 内部token | 意味 | UI |
| --- | --- | --- |
| `pickaxe_poke` | responseに同typeが一件以上ある | 表示「ツルハシでつつく」 |
| `chat_posted` | responseに同typeが一件以上ある | 表示「チャット投稿」 |
| `projectile_hit` | responseに同typeが一件以上ある | 表示「発射物ヒット」 |
| `empty` | responseの`events`が空配列 | 表示「空振り」、既定OFF |
| `other` | 上記以外のtype | 非表示 |

現行`parseEvent()`は未知typeを分類へ渡す前にsnapshot全体を拒否するため、実データのevent `other`は到達不能である。
内部stateと防御的分類は残すが、switchは描画しない。parserを未知event許容へ変える場合はUI表示集合を再吟味する。

### 14.3 pair、判定、検索、件数

同じstream内の`events.poll` request／responseは`request_id`でpairにし、一つのfilter unitとして同じ表示判定を
適用する。sendだけを観測しresponseがまだ無いunitは、空振りか非空かを判定できない**pending request**として、
method switchやOR検索の一致を含む全条件より先に表示を保留する。response到着後に初めてpair全体を表示判定し、
空振りOFFなら一度もrequestを先行表示しない。receiveだけのorphanは既に判定材料を持つため防御的表示対象に残す。
responseが複数typeを含む場合は該当classのいずれかがONならpair全体を表示する。非poll frameは一frameで一unitである。

判定式は次で固定する。

```text
基本通過 = method groupがON
           AND（events.pollとして分類不能 OR 該当event classのいずれかがON）
表示 =（基本通過 OR（or検索がON AND or欄が一致））
       AND（and検索がOFF OR and欄が一致）
```

検索対象はunit内各frameのmethod名とJSON payloadを連結した文字列で、大文字小文字を区別しない部分一致とする。
一つの欄へcomma区切りで入力した複数keywordは、そのいずれかが一致すれば欄全体を一致とする。keywordが空なら
一致しないため、空のor欄をONにしても効果はなく、空のand欄をONにすると全unitが非表示になる。

件数は現在保持windowに対してfilter stateと独立に計算する。methodはunitごとに一回、eventはpairが含むclassごとに
一回を数え、同じclassのeventが複数あってもそのpairでは一回とする。表示から除外したunitを`dropped_frames`へ
加えず、保持windowから実際に退去したframeのlossと表示選好を混ぜない。

### 14.4 既定値と保存

初期stateは全method group ON、event classは`empty`だけOFF、or／and検索はOFFかつ空文字である。UIに描画しない
`auth`／`catalog`／event `other`も内部stateではONを保持する。選好stateは`localStorage` key
`mcremote.wirescope.frame-filter`、version 1、
`{version,methodGroups,eventClasses,orSearch,andSearch}`へbest-effortで保存する。現在入力中のor／and文字列は
各search stateの一部として保存するが、過去の検索履歴一覧は作らない。frameとpayloadは保存しない。欠損／型違反fieldは
field単位で既定値へ戻し、壊れたJSON、異なるversion、storage read失敗はfilter UIを壊さず全既定値へ戻す。
storage write失敗は例外を外へ出さず、現在のmemory上の選好を保ったまま永続化だけを行わない。

### 14.5 表示安定化と一時停止

frame tableはsnapshot到着ごとに全DOMを作り直さない。filter後の表示frameを順序付き`sequence`列として比較し、
表示集合が変わらないsnapshotではtable bodyを置換しない。これにより、非表示のpending／空振りpollが約1秒ごとに
到着しても、既存payloadの選択範囲とcopy操作を維持する。filter変更とlocale変更は利用者が意図した再投影なので、
同じ表示signatureでも一回再描画できる。件数、接続状態、`dropped_frames`等の周辺表示更新を、table bodyの
再構築理由にはしない。

各streamはclient-onlyの「表示を一時停止」／「表示を再開」を持つ。停止時点の保持frame配列を表示snapshotとして
固定し、その後もsourceからのframe収集、`events.poll`、保持windowのtrim、`dropped_frames`累積を止めない。
停止中はlive frameとの差から新着件数をbadge表示し、filter／検索は停止時点のsnapshotへ即時適用する。再開時は
最新の保持windowへ一度だけ切り替え、中間snapshotを再生しない。観測targetが変わるとstream cacheごと停止状態を
破棄し、通常表示へ戻す。一時停止状態、停止snapshot、frame、payloadは`localStorage`へ保存しない。

この機能を「観測停止」と呼ばない。WireScope source、Scratch observer、Bridge、plugin、server event ring、poll頻度を
止めるcontrolではなく、read-only observer UIの投影だけを固定する機能だからである。表示停止は§14.3のpending pair
保留や通常時のDOM安定化の代替ではなく、建築中など表示対象そのものが多い局面で利用者が明示的に静止させる追加UXである
（`2026-08-28-01`）。

### 14.6 実装identityと検証境界

実装基準はscratch-editor `agent/b6-wirescope-display-filter@c720341a2cee4b01f2b2a227cf6379ac0ac92db2`、
UI表示集合の後続は`46919addc071c3607864672854190c1bbeb7047e`、b6統合sourceは
`agent/b6-integration@040f06617c80e54cdba9421b6c69445efdf099ba`である。搬送元は`@mc-remote/live` 124件、
lint／build、deterministic sourceによる実browserで、switch表示集合、pair連動、件数、and／or検索、
`dropped_frames`、reload後の選好復元を確認した。実McRemote plugin E2E、and／or全組合せ、iPad／Safari、
default branch統合、正式evidence、releaseは未実施・未主張である。

後続のscratch-editor `agent/b6-wirescope-poll-pair-stability@7b4f71d71e8ecd665d402682e677dc4e425d160f`は、
pending `events.poll` requestを無条件に保留し、pair完成後に原子的表示判定する。また、表示frameの`sequence`列が
変わらないsnapshotではtable bodyを再構築しない。搬送元は`@mc-remote/live` 130/130件、lint／buildをPASSし、
実protocol 23 plugin＋local Bridgeのreal-browser確認で、空振りpoll中の選択／copy維持、非空poke pairの同時表示、
player groupによる`player.getPos` request／responseの一体表示／非表示を確認した。

その子`24077ef005e4969bf3a7434b45532ae53cefbc28`は§14.5の表示停止を追加した。130/130件、lint／buildを維持し、
deterministic sourceの実browserでtable固定、新着badge、copy、停止snapshotへのfilter／検索、最新windowへの一括再開を
確認した。観測target変更後の自動再開と、実plugin接続中の表示停止は未確認である。生成した
`wirescope-app.zip`は79,169 bytes／SHA-256
`b3d6270299195d2c3db93c9d122938be6ae20d23e0f10e19afe3b0e99e3ca315`、detached manifestは2,321 bytes／
SHA-256 `5fafdc54af45d8f498cd48b13590797eaaa6316adaf017a40595566f0f507b2e`である。GUI／Bridge、wire、observer
schemaは変更していない。
