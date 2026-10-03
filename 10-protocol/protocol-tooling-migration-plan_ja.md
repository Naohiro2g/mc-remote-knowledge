# Protocol／WireScope／Bridge移管評価計画

> 状態: `2026-09-01-03`でpark。`2026-09-13-02`によりb8前に実施せずb8後へ送ることを確定。b8期間中は現行owner・依存方向を維持し、repository操作・source移動・owner変更・distribution変更を開始しない。`2026-09-30-03`でb9に実施すると決めた（b9はAPIを変えない）。Java以外のconsumerで行い、初回stableの後にJavaの追従で再検証する（`2026-09-30-04`、下の「Javaの位置づけ」）。topologyとexactな実行範囲は、b9の前に別途批准する。
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
- owner移管の成否に依存せず、現ownerの人間可読contract、批准済みmetadata、production registry／surface、共有fixtureから、
  release別API referenceの人間可読版と機械可読版を同じ入力で生成できるか

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

b7 release後の評価において、B8のentity lifecycle／particle Stage 2の変更と共通tooling ownership変更を同じchange coneへ重ねないため、b8前に実施せず「b8後へ送る」ことを確定した（`2026-09-13-02`）。b8期間中は現行ownerと依存方向を維持し、repository操作、source移動、owner変更、distribution変更を開始しない。

b7完了は検討再開の最早時点であって、repository操作、source移動、owner変更、distribution変更の実行許可ではない。
coordinatorは実装／依存、候補、推奨、工数、影響repository、外部操作、knowledge決定文を先に会話へ提示し、exactな方向と
実行範囲の人間批准後にだけ作業へ進む。

b9の移管では、SSOT改訂、target topology、package／artifact取得、owner test、Java以外のconsumer（McRemote、Python、
Scratch）の切替、Scratch側の旧owner撤去、provenance、rollback、CIを一組で行う。repository作成またはcopy一致だけを
移管と呼ばない。

移管に「完了」の判定は置かない。完璧な移管は無く、何をもって完了とするかは誰も判定しきれないからである
（`2026-09-30-04`、`2026-07-19-05`）。初回stableの後、Javaが新しいownerと取得経路だけを使って実装を追従し、
移管を再検証する。見つかった問題は通常の修正として扱う。以前のこの段落にあった「全consumer切替を含む一組の確認を
完了とする」は、この形へ置き換えた。

release別API referenceの生成はowner移管の実行許可や完了条件ではない。移管を選ばなくても現ownerから生成できることを
評価し、移管待ちをreference提供の前提にしない（`2026-09-04-06`）。人間向けのAPI一覧は公開分をknowledgeが持ち、
ホームページ配下に置く（`2026-09-30-05`）。

## b8時点の起点

b9の移管の起点は、公開したb8のScratch source `691576f`時点のfixture 12件（Protocol 7、WireScope 4、Bridge 1）である。path、bytes、
SHA-256、case数、consumerは[b8 closeのfixture一覧](../14-evidence/artifacts/2026-10-03-b8-dev-live/scratch/2026-10-03-b8-close-inventory/FIXTURES_ja.md)を正とし、移した後のownerはこれとbyte一致で再現する。

## Javaの位置づけ（`2026-09-30-04`）

Javaはb8にもb9にも含めない。b9までは、移管とfreezeに役立つ準備を先に進める。契約の疑問点の棚卸しとfreeze前の
返却、consumerとしての依存の明示、再現できる検証の入口、README／examples／対応範囲の整合である。

初回stableの後、Javaは新しいownerと取得経路で実装を追従し、移管の再検証を担う。Scratchのruntime／buildに依存しない
Java consumerが、新しいownerと取得経路だけから実装・検証できるかを確かめる（いまのJavaのtest fixtureはScratchの
owner由来なので、「Scratchに一度も依存していない」とは書かない。Java着地確認の指摘、2026-09-30）。
