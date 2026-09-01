# Protocol／WireScope／Bridge移管評価計画

> 状態: `2026-09-01-03`でpark。b7 release後に再開し、b8前に実施するかb8後へ送るかを人間レビューで決める。
>
> 人間向けの意味、非許可境界、再開手順は
> [人間向け固定文](protocol-tooling-migration-human-guide_ja.md)をそのまま確認する。b7完了は自動開始条件ではない。

## 現在地

公開repository `Naohiro2g/minecraft-remote-protocol`は2026-09-01に先行作成された。

- bootstrap import: `b570d2292131f825e4766ed9ebb43a2260cfe583`
- pre-park operational head: `72567606f81370710fb53f00e61041e189c73d2e`
- parked head: `3f7c3586eeee3a1f05d371ba2f5d3bcfcac61a1d`
- source snapshot: `scratch-editor@607cda40588ec4579c503d457c3784385419ac65:mc-remote/protocol`
- predecessor fixture: `test/fixtures/direction-lightning-v23.1.json`
- bytes／SHA-256: `14179`／`faad66c93d2c8ee8eb541f6b7297163cb681054b3de05ba3d130ac4288c1046a`
- standalone lint／Prettier、Vitest `27/27`、build、GitHub Actions: PASS

これは移管candidateの実物検討材料であって、owner cutoverではない。現行の実行可能Protocol投影／shared fixture ownerは
`2026-08-27-02`に従いscratch-editor内の`@mc-remote/protocol`とする。park中のrepositoryからsuccessor fixture、package、
releaseを発行せず、McRemote、Python、Scratch、Javaの参照先を変更しない。

## なぜb7中に進めないか

b7はdirection、full lightning、permission snapshot、handle lifecycle、artifact、live、releaseを閉じる作業中である。
repository ownershipの変更には、ProtocolだけでなくWireScope、Bridge、TCP／WebSocket、distribution、consumer build、
version、artifact、securityの判断が伴う。公開bootstrapが存在することを追加作業の根拠にせず、b7の完了と分離する。

## 再開時に評価する範囲

### Protocol projection／conformance

- `@mc-remote/protocol`、method／reason mirror、型、定数、shared fixture、owner testの配置
- knowledgeの人間可読SSOTとexecutable projectionの批准順序
- npm、Git commit pin、source vendor、generated artifactの取得方式
- consumerごとのexact commit／path／bytes／digest固定
- Scratchから編集可能なowner copyを除く完全移行と、一時hybridの終了条件

### WireScope

WireScopeはScratchとPythonが既に同じbrowser appを利用し、将来のJava、TypeScript、C# sourceも同じ観察面へ接続する共通
productである。browser UIだけでなくobserver schema／session、station attach、固有fixture、artifact generator、
Scratch MessageChannel adapter、station adapterを持つ。

再開時は、Scratch／Python固定の表示や`source_kind`を増やし続けず、言語非依存source identity、表示名、adapter profile、
capabilityを分離できるかを評価する。Scratchにはframe生成、handoff開始、起動UI等のScratch固有source側だけを残し、
common appをconsumerとして利用する完全移行を第一候補とする。

### BridgeとTCP接続

BridgeはWebSocketとMcRemoteのnewline-delimited TCPを接続するtransport adapterであり、現在はScratch browser接続を起点に
している。将来の一般TypeScript browser利用、WireScope station、direct TCP Client Libraryとの関係を比較し、次を決める。

- Bridgeを共通componentとして維持／一般化する
- Scratch専用adapterへ縮小する
- stationまたは別transportへ役割を移して廃止する
- McRemoteのdirect TCPを維持する範囲と、browserからTCPへ到達する正規経路
- Origin、target allowlist、TLS終端、routing、credentialをどのdeploymentが所有するか

Bridgeの現状維持を前提にせず、廃止も正規候補に含める。TCP自体の廃止やwire変更をこの計画から先取りしない。

## 有力なtopology

### 共通TypeScript tooling monorepo

Protocol、conformance、WireScope、必要ならBridgeを一つの中立repositoryへ置く。package境界と依存方向を保ち、
`@mc-remote/protocol`はdependency-free leaf、WireScope／Bridgeはconsumerとする。同一repoであることからversion／release同期を
推測しない。

Scratch monorepo内で既に一緒に育ち、Protocol変更、observer allowlist、fixture、artifactを横断検証できた価値を、Scratch
製品所有から切り離して維持できる点が強い。現時点の有力案とする。ただし公開bootstrap名
`minecraft-remote-protocol`を共通tooling全体の名前として使うかは再批准する。

### Protocol repo＋WireScope repo

Protocol projection／fixtureとobserver productを別repositoryへ置き、それぞれ独立version、artifact、security reviewを持つ。
責務とrelease cadenceが実際に分かれる場合に有力である。最初から分けるcostと、monorepoから後で分けるcostを比較する。

### Hybrid

移行中だけScratchへvendor copyを残し、外部owner commit／digestとの一致をCIで検証する。双方向編集を許さず、終了条件を
先に固定する。恒久的な二重ownerにはしない。

## 再開gateと完了条件

b7 release後に、b8の規模と開始時期を見て「b8前に実施」または「b8後へ送る」を人間が決める。公開bootstrapの存在や
投入済み工数だけで前者を選ばない。

b7完了は検討再開の最早時点であって、repository操作、source移動、owner変更、distribution変更の実行許可ではない。
coordinatorは実装／依存、候補、推奨、工数、影響repository、外部操作、knowledge決定文を先に会話へ提示し、exactな方向と
実行範囲の人間批准後にだけ作業へ進む。

移管を選ぶ場合の完了は、SSOT改訂、target topology、package／artifact取得、owner test、全consumer切替、Scratch側の旧owner
撤去、provenance、rollback、CIを一組で確認した時点とする。repository作成またはcopy一致だけをcutover完了と呼ばない。
