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

## 13. protocol 22／b5 method観察とschema v1.1 compatibility set

b5ではobserver schema／app artifact contractをv1.1へ進め、`events.poll`、`world.getHeight`、
`world.spawnParticle`、`world.spawnEntity`と新しいreasonを観察できるようにする（DECISIONS
`2026-08-16-07`）。加えて、protocol 22の`world.setBlock`／`world.setBlocks`／`world.getBlock`は、
`block_id`と`state`を分離した構造化`BlockSpec`／`BlockValue`として観察する（`2026-08-19-02`）。
これはschema v1へ未知fieldを追加する変更ではない。

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

`world.setBlock`／`world.setBlocks`の`BlockValue` result、`world.getBlocks`の有界array、
`block_right_click.block`、`projectile_hit.target.block`も同じvalidatorへ収容する。WireScopeは
Scratch StateText／BlockInfoTextへ再結合せず、partial request、full result、event snapshot、errorの
`data.path`を構造化frameのまま観察する（`2026-08-19-03`／`04`）。

連続位置・角度はpluginがDECISIONS `2026-08-19-01`の正準numberへ変換した後のframeを観察する。
observer validatorと共通UIは座標や角度を別値へ再round／wrap／clampしない。UIが可読性のため末尾ゼロを
補う場合も、raw frame、copy、fixture比較はserverから受けたJSON numberを正とする。Scratch／Pythonで
同じframeを異なる桁へ変換しないことをcompatibility setで検査する。

本sliceで確定するv1.1はmethod観察のcompatibility境界である。payload summary、gap marker、
recording／replayのloss表現はv1.1へ含めず、後続version／sliceとして別に固定する。
