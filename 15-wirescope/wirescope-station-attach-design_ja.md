# WireScope station attach 設計

> 状態: `2026-08-11-02`／`2026-08-11-03` の説明正本。配置とcapabilityの上位原則は
> [WireScope deployment設計](wirescope-deployment-design_ja.md)、observer snapshotのschema v1は
> `2026-08-06-03`を参照する。

## 1. 一つの画面へ、異なる入口から接続する

ScratchとPythonは同じ`@mc-remote/live` browser appを使う。共通にするのはschema検証、observer session、
view state、UIであり、sourceやdeploymentに固有のattach方法はadapterとして分ける。

```text
Scratch opener ── MessageChannel adapter ─┐
                                          ├─ observer session core ── common UI
loopback station ── HTTP attach adapter ──┘
```

Scratch固有のhandoffをPythonへ移植せず、Python専用UIも作らない。将来のconsoleは第三のbrowser adapterでは
なく、自前のpairingとcontrol capabilityを持つ独立sourceである（`2026-08-10-03`）。

## 2. Adapterの選択

browser appは、次の状態遷移で一つのadapterだけを選ぶ。

1. openerとdistinct absolute referrerがあればScratch adapterの**候補**にする。この時点では確定しない。
2. Scratch selection window内に、exact source／origin、protocol version、MessagePort数を満たすattachを
   受理した時点でScratch adapterを確定する。
3. selection window終了前にport／grant処理が始まらなかった場合だけScratch listenerを破棄し、same-origin
   station bootstrapを確認する。
4. 一度MessagePortを受理した後はstation adapterへfallbackしない。
5. station bootstrapが無い、または検証に失敗したdirect navigationには観察能力を与えない。

selection windowの具体値はScratch contractとtestで固定し、source側のlaunch待機時間およびgrant発行後
15秒の寿命とは別定数にする。

## 3. Same-origin station attach protocol

初版endpointは次とする。

```text
GET  /__mcremote/wirescope/bootstrap/v1
POST /__mcremote/wirescope/attach/v1
```

bootstrapは、station attach version、observer session version、observer schema name／version、artifact
identity、station readinessだけを返す。target一覧、display alias、grant、attach code、Minecraft接続情報を
返さない。target未成立時は`readiness=false`である。

attach codeは`POST`のJSON bodyだけで受け取る。URL、fragment、cookie、Web Storage、IndexedDB、
BroadcastChannel、referrerへ置かない。target／code未成立時はboundedな`target-not-ready` errorとし、codeの
試行回数を消費しない。malformed codeも消費せず、canonical形式だが不一致のcodeだけを試行上限へ数える。
redeemは並行request間でもatomicとする。成功時は新しいsession tokenやcookieを発行せず、単一の
`application/x-ndjson` responseをobserver sessionとして返す。

両endpointでexact authorityを検証する。bootstrapの`Origin`は省略可能だが、存在する場合はexact originを
要求する。attachではexact `Origin`を必須とし、exact `Host`、loopback bind、`Content-Type`、request byte
上限も検証する。CORSとredirectを許可せず、responseは`Cache-Control: no-store`とする。profileはCSP、
`Referrer-Policy`、`X-Content-Type-Options`を応答headerで保証する。

## 4. Observer schemaとsession envelope

`mcremote.observer` schema v1はsanitized snapshotのshapeを所有し、strict validatorと現行method allowlistを
維持する。`catalog.get`は初期sliceへ追加せず、helloの`catalog_hash`だけを観察できる。transport、履歴窓、
終了理由をschema v1の未知fieldとして加えない。

外側のversioned observer session envelopeが次を所有する。

- `snapshot`: schema v1 snapshotと、同じ時点の`history-window` metadata
- `end`: station／sourceが送信できるobserver終了
- envelopeのline順序、size上限、終端規律

`history-window`とsnapshotは同じenvelopeで原子的に適用する。snapshotの`frames[]`は、そのenvelopeが示す
retained windowそのものである。`dropped_frames`はobserver session内で単調増加し、target／session開始時に
resetする。snapshot coalescingは欠落ではなく、rolling windowから実際に退去したframeだけを数える。

wireで送れるend reasonは次である。

- `target-ended`
- `source-closed`
- `backpressure`
- `capacity-exhausted`

`transport-lost`はwire reasonではない。正常なendを受ける前のEOF、fetch rejection、NDJSON framing error、
message上限違反では、browser coreがlocal terminal stateとして合成する。

## 5. Rolling historyと処理能力境界

初期Python profileの調整可能な既定値は、100 framesかつUTF-8 compact JSONのencoded合計256 KiBである。
古いframeから退去させ、`history-window`で省略を可視化する。通常の小さいframeが続く大量建築ではobserverを
終了しない。

単一encoded frameが64 KiBを超える場合は、黙ってdrop／truncate／summary化せず
`capacity-exhausted`でobserverだけを終了する。Minecraft RPCと利用者codeは継続する。summary、gap marker、
recording／replay向けloss表現は後続schema sliceで同時に設計する。

Python sourceのobserver hookはMinecraft RPC thread上でnetwork待機やsnapshot serializeを行わず、有限の
in-process ingress queueへ`put_nowait`する。ingress overflowは`backpressure`でobserver sessionだけを終了
する。station workerはrolling windowを更新し、未送信snapshot envelopeを最大1件だけ最新状態へ置換できる。
terminal end envelopeは置換しない。

初期outbound queueの調整可能な既定値は16 envelopesかつencoded合計1 MiBである。ingress queueの具体上限、
rolling window、frame、outbound queueの数値はPython spokeとfixture／testで固定し、横断不変条件は有限・
非永続・沈黙したloss禁止・Minecraft側fail openとする。

## 6. Immutable artifact

共通appは次のdetachedな二artifactとして生成する。

```text
wirescope-app.zip
wirescope-app.manifest.json
```

manifestは少なくとも、manifest／archive format version、archive SHA-256、Scratch source repository／commit／
subdirectory、build recipe／toolchain／入力identity、observer schema／session version、Scratch handoff version、
station attach version、asset inventoryと各hash、component license expression、対応source URLを持つ。
runtime portやattach codeをassetへ埋め込まない。

consumerはarchiveだけでなくmanifest自身のSHA-256も外側の信頼境界で固定する。Python wheelはwheel
`RECORD`、Stackはdeployment lockでmanifestとarchiveの双方をpinし、manifest内のarchive hashとも照合する。
archiveには`AGPL-3.0-only`本文とcomponent noticeを含め、asset inventoryへ登録する。

## 7. Python browser-loopback参照profile

初版はsource、station、browserが同じnetwork namespaceにあるprofileだけを実装し、station roleをPython
source processへ融合する。

```python
from mc_remote.wirescope import WireScopeStation

mc = Minecraft.create(wirescope=WireScopeStation.local())
```

`wirescope=None`は無効である。`wirescope=True`はlow-floor APIとして恒久的に
`WireScopeStation.local()`の省略形とし、将来profileを追加しても意味を変えない。初期sliceで実装するdescriptor
は`local()`だけであり、LAN／VPS descriptorと`connect()`は後続決定まで作らない。

stationは`127.0.0.1`のephemeral portだけへbindする。`localhost`の名前解決、固定port、`0.0.0.0`、LAN
addressを使わない。attach codeを非永続のinteractive TTYへ安全に表示できない環境ではWireScopeだけを
actionable warning付きで開始せず、Minecraft接続を継続する。Jupyter等の非TTY attach経路は後続profileとして
parkする。

起動順序は次である。

1. TTY、artifact、stationをpreflightする。
2. loopback stationを起動する。
3. secretを含まないtop-level URLでbrowserを開く。
4. observer hookを接続し、通常の`Minecraft.create()`接続、pairing、authenticated helloを進める。
5. browser attachを待たない。
6. authenticated hello成功後にtarget ID、display alias、target-scoped attach codeを生成する。
7. attach後にmain streamのlive observationを開始する。
8. `mc.close()`、connection epoch終了、create失敗時にtarget、observer、thread、socketを回収する。

preflight失敗またはWireScope無効時はobserver hook自体を接続しない。station起動、browser起動、attach、observer
送信の失敗はactionable warningとし、Minecraft connectionと利用者codeへ伝播させない。

## 8. Attach codeとlifecycle

attach codeはMinecraft pair codeやcredentialとは別物で、初期profileでは次を満たす。

- 暗号学的乱数による40 bit、ambiguity-free base32のcanonical 8文字
- target 1件へbinding、120秒有効、atomicな一回redeem
- canonical形式の不一致を最大5回まで許し、失効時はboundedな回数だけcooldown付きで再発行
- 新code発行時に旧codeをatomicに無効化
- terminalとbrowser入力欄だけに表示し、URL、通常log、exception、project file、credential store、browser
  storageへ保存しない

alphabet、大小文字正規化、表示区切り、malformed／well-formed判定、clock境界、再発行回数とcooldownは
Python fixtureで機械化する。

attach前に保持するのはsanitized authenticated hello summaryとallowlist済みhello request／responseだけで
ある。pairing frame、未認証hello、`auth.*`、catalog body、一般frame履歴は保持しない。

Python lifecycleからsession endへの写像は次である。

- authenticated connection epochのclose、remote EOF、reconnect: `target-ended`
- WireScope sourceだけの正常停止: `source-closed`
- ingress／outbound処理能力の超過: `backpressure`
- 単一frame admission上限超過: `capacity-exhausted`

初期profileは1 target、1 browser、main stream 1本に限定し、自動reattach、複数browser、複数targetを実装
しない。引数なし`mcremote wirescope` subcommandはcross-process transport決定まで予約のままにする。

## 9. Python実装起点とStack gate

Pythonのconformance branch `d3c221c27c6af3db89bbc28f9965ea4e01a42353` とcurrent main
`4a83e81c51aaa252ac5d92cdd5403ff0ab0b86f6` はdivergeしている。observerだけを移植せず、b3 catalog、
projection、CLI、adapter一式をcurrent mainへ統合し、全test済みの新しい固定SHAを実装起点にする。

Python wheelへAGPL componentを同梱する前に、distribution-level license expression、license files、component
notice、対応source導線をPEP 639 metadataと配布物で確定する。projectのlicense原則`2026-08-11-01`は
2026-08-11に人間批准済みである。未完なのは方針の批准でなく、各distributionが同原則を満たすことの実装・
検証gateである。

初期Python profileは`mc-remote-stack`をruntime dependencyにしない。StackがLAN／public HTTPS stationを
実装するのは、共通artifact／session／attach contractとPython loopback real-browser E2Eが合格し、source
ingress、multi-user／multi-target isolation、TLS、rate limitが別途批准された後である。

Stackではapp artifact、station runtime、browser endpoint、source ingressを別capabilityとして扱う。同一
service／portへ載せてもpath、credential、rate limit、request schemaを分離し、最初のmessage種別だけで権限を
分岐しない。McRemote credentialを再利用しない。変更・rollback後もartifact、runtime、schema、session、attach、
ingress、profileを完全なcompatibility setとしてlock・検証する。未批准fieldを先にprofile schemaへ追加しない。

## 10. 実装順序とpark

実装は次の順で進める。

1. 共通observer session envelopeとclient core
2. Scratch adapter選択の状態機械と既存handoff regression
3. detached app artifact／manifest
4. Python main統合と新しい固定SHA
5. Python in-process station、有限queue、attach code
6. Python fixture／unit／conformance
7. 共通appとのreal-browser loopback E2E
8. 人間批准済みの`2026-08-11-01`に従うlicense／artifact配布実装の確認
9. Stack後続gateの再判定

次は今回確定しない。

- schema v1.1のgap marker、oversized frame summary、recording／replay loss表現
- 非TTY／Jupyter向けattach
- cross-process、LAN、public stationのsource ingress
- multi-user／multi-target isolation、LAN CA、公開rate limit
- artifact signing
- consoleのprotocol、pairing、command scope、教材gate
