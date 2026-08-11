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

- LAN／public profileのsource discoveryとsource-to-station transport
- source登録能力とbrowser attach能力のdeployment実装
- grant発行前frameを後発observerへ見せるか
- target／display alias列挙capability
- multi-user／multi-target isolation
- LAN／public station認証、rate limit、multi-user buffer分離
- schema v1.1のpayload summary、gap marker、recording／replay loss表現
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
