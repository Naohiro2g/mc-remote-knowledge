# Minecraft Remote 多言語 Client Library / Protocol-first ロードマップ

> Minecraft Remoteを、Python中心の実装から、言語非依存Protocolを中心に複数のClient Libraryが
> 対等に参加する構造へ発展させるための説明ロードマップ。
>
> 本文書は説明層である。名称・互換性・bootstrap方針などの拘束は`00-hub/DECISIONS_ja.md`、
> 正典語は`00-hub/terms-glossary_ja.md`、wireとversioningのcontractは本ディレクトリの各文書を正とする。
>
> 起点となる横断決定:
>
> - `2026-08-29-03` — Client Library／Client API語彙と多言語命名
> - `2026-08-29-04` — Classic温存＋新Java Client Library bootstrap
> - `2026-08-29-05` — 本ロードマップの進行、配置、既存fixture／test語彙／developer experienceとの接続

---

## 1. 何を目指すロードマップか

Minecraft Remoteは、PythonからMinecraftを外部操作する仕組みとして発展してきた。

b6で固定された実行可能なPython Client Libraryは、単純なsocket wrapperではない。接続、`hello`、protocol
version negotiation、authentication、block value、build context、catalog、event、error、build execution mode、
WireScope観察など、Minecraft Remoteを利用するための広いsurfaceを持つ。

一方、Minecraft Remote Protocol自体も既に存在する。

したがって、これから行うことは、

> PythonライブラリからProtocolを新しく発明する

ことではない。

目標は、

> **既に存在するMinecraft Remote Protocolを、Python実装の背後にある通信仕様から、複数のClient Libraryが
> 対等に実装する第一級の製品境界へ育てる**

ことである。

最終像は次の形になる。

```text
                       Minecraft Remote Protocol
                    ─────────────────────────────
                    method / type / error / state
                    lifecycle / ordering / version
                       /       |       |       \
                      /        |       |        \
                 Python      Java   TypeScript    C#
                  Client     Client    Client    Client
                 Library    Library   Library   Library
                      \        |       |        /
                       \       |       |       /
                        ─── McRemote Plugin ───
                                  │
                              Minecraft
```

Pythonは中心から追い出されるのではない。

Python、Java、TypeScript、C#が、

> **同じProtocolを各言語へ投影するClient Library**

として並ぶ構造へ移行する。

---

## 2. 正典語とレイヤ

本ロードマップでは`2026-08-29-03`と用語集に従い、次の語を使う。

### Protocol

言語によらず共通でなければならない通信上の契約。

例:

- method名
- params／result
- error
- request／notification
- `hello`
- authentication
- version negotiation
- connection-scoped state
- ordering
- `connection.flush`
- block／entity／event等のwire上の値
- serverが保証すること／保証しないこと

Protocolの正本は`10-protocol`に置く。

### Transport

Protocol messageを運ぶ経路。

現行では主に、

```text
TCP
  └─ 1行 = 1 JSON

WebSocket
  └─ 1 message = 1 JSON
```

がある。

TCP／WebSocketのframing、socket open／close、WSS deploymentはProtocolの意味論と区別する。Bridgeは
WebSocketとTCPを接続するproxy／transport adapterであり、TCP／WebSocketと並ぶ第三transportではない。

### Client Library

あるプログラミング言語からMinecraft Remote Protocolを利用するための成果物。

例:

- Minecraft Remote for Python
- Minecraft Remote for Java
- Minecraft Remote for TypeScript
- Minecraft Remote for C#

### Client API

Client Libraryがconstructors、methods、types、errors等として利用者へ見せるprogramming面。

Client APIは各言語に自然な形でよい。

たとえば同じProtocol操作であっても、

```text
Python       mc.getBlock(...)
Java         mc.getBlock(...)
TypeScript   await mc.getBlock(...)
C#           await mc.GetBlockAsync(...)
```

のように表現が違ってよい。

統一するのはsyntaxではなくsemanticsである。

### Application / user code

Client APIを利用して作品や処理を作る層。

たとえば、

- pyramidを建築する
- 迷路を生成する
- MinecraftとUnityを連動させる
- eventを使ってゲームを作る

といった処理はこちらに属する。

`buildPyramid`のような便利な処理を、複数言語で欲しいという理由だけでProtocol commandへ昇格させない。

---

## 3. Protocol-firstは「最初に仕様書を全部作る」という意味ではない

このロードマップでいうProtocol-firstは、開発作業の時間順序ではなく**最終的な責任構造**を表す。

```text
Protocol-first
≠
すべてのProtocol仕様・schema・fixtureを先に完成させる
```

である。

むしろ最初は、

```text
b6で固定された実行可能なPython Client Library
       ↓
新しいJava実装
       ↓
二つを比較
       ↓
Protocol境界を精密化
```

という順序を採る。

これはProtocol-firstと矛盾しない。

Pythonを参考にしてJavaを作る過程で、

- 本当に言語共通であるもの
- Pythonだけの実装判断
- Javaでは別表現が自然なもの
- Protocol文書に不足しているもの

が具体物として見えてくるからである。

Protocol-firstとは、

> 最後にPythonやJavaのどちらかを正本にするのではなく、発見した共通意味をProtocol側へ戻す

という開発循環を持つことである。

---

## 4. 現在地

現在は次の状態にある。

```text
McRemote Protocol       存在する
McRemote Plugin         存在する
Python Client Library   b6で固定された実行可能な実装が存在する
Scratch Client          存在する
共有Protocol fixture    部分的に実働している
Java Classic            旧Protocol世代として存在する
新Java Client Library   未着手
一般TypeScript Library  未着手
C# Client Library       未着手
```

Classic Javaは現行版へ改造せず履歴として保存する。

新しいJava Client Libraryは別repositoryで現行Protocolを対象として作る。

拘束は`2026-08-29-04`を正とする。

また、b6 protocol 23では既に`@mc-remote/protocol/test/fixtures/`が共有fixtureのownerとして使われ、
複数componentが同じmachine-readable caseへ投影する仕組みが動いている。

したがって本ロードマップは、conformanceをゼロから発明する計画でもない。

---

## 5. 全体の進行

ロードマップ全体は次の流れで進める。

```text
Phase A  Java bootstrap準備
   ↓
Phase B  Javaの最小縦slice
   ↓
Phase C  Javaを単独利用可能なClient Libraryへ
   ↓
Phase D  Polyglot developer experience checkpoint
   ↓
Phase E  Python / Java / Protocol比較
   ↓
Phase F  既存executable contract / conformance資産の一般化
   ↓
Phase G  TypeScript Node実装
   ↓
Phase H  Browser / WebSocketによるTransport独立性検証
   ↓
Phase I  C# / Unity展開
   ↓
Phase J  多言語Client Libraryの通常運用
```

これは`2026-08-29-05`で確定した2026-08-29時点の最適な進行である。不変の未来予測ではなく、各Phaseで得た
観察によって前提が変われば、append-onlyの後続決定で改訂する。

未固定なのはロードマップ全体ではなく、各Phaseが所有するexact API、wire shape、registry name、実装slice等の
局所contractである。各段階はコード量ではなく、**得られた保証と次に観察可能になった境界**で進行を判断する。

---

## 6. Java bootstrap baseline

`2026-08-29-04`は、Java bootstrapで比較に使うprotocol 23.0.0／artifact 2300.0.0b6の固定一式を
定めている。

本文書では、このJava固有の固定比較基線を**Java bootstrap baseline**と呼ぶ。

これは一般語彙`compatibility set`と書き分ける。

- compatibility set:
  app artifact、runtime、schema、protocol、profile等を互換な一組としてlock・検証する横断概念。
- Java bootstrap baseline:
  新Java Client Libraryがmoving targetを追わず、Python外部挙動とProtocolを比較するために固定したb6基線。

exact source／artifact／digestは`2026-08-29-04`とrelease evidenceを正とし、本文書へ重複固定しない。

---

## 7. Phase A — Java bootstrap準備

最初に新Java repositoryを作るための最小限のidentityを確定する。

repository名は`2026-08-29-03`／`2026-08-29-04`に従う。

一方、Java root packageはsource fileを書き始めると即座にコードへ焼き込まれるため、repositoryのsource
scaffoldより前に決める。

現在未確定のexact candidateと再開条件はhub NOTESを正とする。

ここではMaven公開を完成させる必要はない。

必要なのは、

> **後で変更するとJava source全体へ影響するroot packageだけは、最初のpackage declarationより前に
> 人間レビューで固定する**

ことである。

### Phase A 完了条件

- Java repository identityが決まっている
- root packageが決まっている
- build systemの最小scaffoldがある
- Java bootstrap baselineが固定されている
- Classic repositoryを変更していない

---

## 8. Phase B — 最初の「目に見えるJava」を作る

このPhaseでは、多機能なClient Libraryを目指さない。

最初の目標は、

> **Javaコードを書き、それを実行すると、現行Minecraft Remoteへ接続してMinecraft世界が実際に変わる**

ところまで一本通すこと。

最初の縦sliceは、認証状態により次のように分岐する。

```text
Java application
     ↓
Java Client API
     ↓
JSON-RPC over TCP
     ↓
hello（保存tokenがあれば付与）
     ├─ success
     │    └─ protocol negotiation＋authentication成立
     │          └─ world.setBlock / world.getBlock
     │
     ├─ protocol_mismatch
     │    └─ 停止
     │
     └─ auth_required／token認証reason
          └─ auth.pairBegin
                ↓
             人間pairing
                ↓
             auth.pairPoll
                ↓
             必要に応じて再接続
                ↓
             token付きhello
```

writeだけでなくreadまで通すことで、

> 送信できた

ではなく、

> 同じProtocolで世界を読み書きできた

ことを確認する。

### 既存fixtureを使う

Javaのcodec／value／error testをすべて独自に書き始める前に、既存の
`@mc-remote/protocol/test/fixtures/`をJavaから消費できるか確認する。

b6では既に、共有fixtureをMcRemote／Python／Scratchへ投影して同じcaseを確認する仕組みが成立している。

Javaをこの消費者へ追加できるなら、それが第一候補である。

Java固有のtestが必要な場合も、同じProtocol assertionを別fixtureへ複製しない。

### pairing

初回pairing pathは実際に一度確認する。

一方、反復開発のたびに人間pairingを要求する必要はない。

credential再利用やnon-interactive testの具体方式はJava repository側の局所計画とし、新しいProtocol
contractへ早期昇格させない。

### Phase B 完了条件

Javaから最低限、

- connect
- `hello`
- protocol negotiation
- authentication
- 初回pairing path一回
- block write
- block read
- close

が成立し、実Minecraftで観察できる。

この時点で、Minecraft Remote for Javaの**実行可能な縦slice**が目に見える形で存在する。

単独利用可能なClient Libraryとしての到達はPhase Cで判定する。

---

## 9. Java実装中の判断順位

Java bootstrap中に不明点が出た場合は、次の順で判断する。

```text
1. 現行Protocol SSOT
2. Java bootstrap baseline上のPython外部挙動
3. Python内部実装
```

Python sourceを翻訳すること自体を目的にしない。

たとえばPythonに、

- thread
- lock
- tuple
- helper
- cache
- Python固有exception
- context manager

が存在していても、それだけではJavaへコピーする理由にならない。

Java側ではJavaに自然な形を選べる。

一方、

- wire method
- resultの意味
- error reason
- connection state
- ordering

が違えば、単なる言語差とは扱わない。

---

## 10. 発見を捨てない

Java実装の大きな目的の一つは、Protocolの未記述部分を発見することである。

疑問が出た場合は、まず現行SSOT、既存fixture、既決のfailure semanticsを照合する。その後にも意味が決まらず、
JavaとPythonで外部挙動の選択が分かれ得る事項だけをProtocol未確定点として捕捉する。

これをJava実装内だけで解決しない。

低摩擦の作業メモはJava repository localのNOTESへ置いてよい。

ただしsession／slice終端では、

```text
Java local NOTES
       ↓ escalation sweep
hub NOTES
       ↓ review
Protocol decision / contract
```

と運ぶ。

後段のProtocol-first強化では、この発見群が重要な入力になる。

---

## 11. Phase C — Javaを単独利用可能なClient Libraryへ育てる

最小縦sliceが成立した後、Javaのsurfaceを広げる。

追加順序をこの横断ロードマップでは固定しない。

機能面はwire namespaceに近い次の分類で考える。

### Connection / execution

- request
- notification
- error
- timeout
- `connection.flush`
- DEBUG／TRACE／FAST

### Build

- dimension
- build origin
- build contextに関係するclient操作

### World

- block
- multiple blocks
- sign
- particle等のworld操作

### Chat

- `chat.post`

### Authentication

- pairing
- credential
- session
- permissions

#### Session credentialの共通UX

各Client Libraryは、期限内session tokenをtarget単位で再利用し、必要な場合だけ一接続試行につき一度pairingする共通意味を
持つ。認証reasonでは該当tokenだけを破棄し、`permission_denied`、`protocol_mismatch`、network errorでは温存する。

ただし保存backendや対話UIをcore libraryへ統一しない。native starterは利用可能な保護されたOS資格情報storeを利用者の
明示同意のもとで使い、利用不能時は平文fileへ自動fallbackせずin-memoryへ縮退する。browser／Scratchはorigin隔離された
browser保存を使い、projectへtokenを含めない。credential scopeにはclient／application、credential type、transport、targetを
含め、異なる言語やapplicationが同じtokenを暗黙共有しない。exact API／CLI／backendは各言語へ自然に投影する。横断正本は
`00-hub/authentication-roadmap_ja.md` §1.1と`2026-08-30-03`である。

### Catalog

- block
- entity
- particle resource catalog

### Player

- position
- direction
- pose等

### Entity

- handle
- query
- pose
- lifecycle等

### Events

- event polling
- event cursor
- event value

どのsliceから実装するかは、その時点のProtocol surface、教材価値、実装依存、Java利用要求を見てJava repository側で
決める。

ロードマップが固定するのは機能順ではなく、

> **Pythonのmethod数を埋める作業ではなく、Protocol capabilityをJavaへ投影する**

という方向である。

---

## 12. DEBUG / TRACE / FASTは境界を理解する好例

build execution modeは、ProtocolとClient Libraryを分ける代表例になる。

概念的には、

```text
DEBUG
  → request

TRACE
  → request + client-side delay

FAST
  → notification
```

である。

DEBUG／TRACE／FASTという利用者向け概念そのものをwireへ送る必要はない。

Protocolが持つ、

- request
- notification
- ordering
- flush

をClient Libraryが利用者に分かりやすく投影している。

Javaを作るときにも、

> PythonにBuildModeというenumがあるからコピーする

ではなく、

> 同じ利用意味をJavaでどう自然に表現するか

から考える。

---

## 13. Phase D — Polyglot developer experience checkpoint

Client Libraryはsocketで接続できれば完成、とはしない。

Minecraft Remoteは学習環境でもあるため、

> **その言語で余計な落とし穴にはまらず、Minecraft固有resourceや型を発見し、補完や支援を受けながら
> コードを書けるか**

を評価する。

Pythonではcatalogから`mc_constants.py`をprojectionし、IDE補完へ接続する仕組みがある。

しかし、この方式そのものをJava、TypeScript、C#へ強制しない。

各言語で、

- catalogの取得
- resource IDの発見
- 型安全性
- IDE補完
- generated source／constants／types
- documentation
- LLMが現在serverのresourceを把握できる導線

などをどう実現するのが自然かを評価する。

### 旧「採用見送り」方針との関係

`00-hub/world-constants-provision-notes_ja.md`には、他言語でも自動補完を含む快適な環境を提供できなければ
採用を見送る、という旧展望がある。

`2026-08-29-05`はこの自動的な採用見送り規則を改訂する。Polyglot developer experience checkpointで体験を
必ず評価するが、不足だけを理由にClient Libraryまたは言語を廃棄しない。不足があれば、たとえば
「単独利用可能だが推奨教材surfaceには未昇格」と状態を明示し、言語nativeな改善へ進む。

Phase Dの完了は全gapの解消ではない。評価対象、観察結果、推奨状態、改善先を記録し、Phase E以降がその事実を
利用できる状態にすることである。

### Phase Dの意味

Phase C:

> Java Client Libraryとして利用できる

Phase D:

> Minecraft Remoteが推奨する学習・開発環境として十分に快適かを評価し、現在の状態を裁く

を分ける。

---

## 14. Phase E — Python / Java / Protocolを比較する

Javaが単独利用可能になり、developer experienceの現在地を評価した段階で、本格的なProtocol抽出レビューを行う。

比較するのは、

```text
Protocol SSOT
Python Client Library
Java Client Library
McRemote Plugin
共有fixture
```

である。

各機能を次の分類へ分ける。

| 分類 | 意味 |
| --- | --- |
| Protocol | 全言語で同じ意味でなければならない |
| Client共通意味論 | wireそのものではないがClient Library群で共通に持つ価値がある |
| Python固有 | Pythonに自然な投影 |
| Java固有 | Javaに自然な投影 |
| Application／sample | Protocolへ入れる必要がない構成 |
| 未確定 | SSOTへ戻って判断が必要 |

重要なのは、

> 同じコード構造か

ではなく、

> 同じ外部意味か

を見ることである。

---

## 15. Phase EでProtocol Inventoryを作る

この段階で体系的なProtocol Inventoryを作る。

形式は次のように、意味のownerと各surfaceの投影状態を並べる。以下は列構成の例であり、現時点の実装statusを
事前記入した表ではない。

| Capability | Protocol | Plugin | Python | Java | Scratch |
| --- | --- | --- | --- | --- | --- |
| hello | 要確認 | 要確認 | 要確認 | 要確認 | 要確認 |
| auth | 要確認 | 要確認 | 要確認 | 要確認 | 要確認 |
| getBlock | 要確認 | 要確認 | 要確認 | 要確認 | 要確認 |
| flush | 要確認 | 要確認 | 要確認 | 要確認 | 要確認 |
| events | 要確認 | 要確認 | 要確認 | 要確認 | 要確認 |
| catalog | 要確認 | 要確認 | 要確認 | 要確認 | 要確認 |

この表の目的はfeature競争ではない。

目的は、

> **どこに意味が定義され、どのClient Libraryがどこまでそれを投影しているか**

を見えるようにすることである。

---

## 16. Phase F — 既存executable contractを一般化する

Minecraft Remoteには既にmachine-readableな共有fixtureが存在する。

`@mc-remote/protocol/test/fixtures/`は、b6 protocol 23で共有compatibility caseのownerとして使われ、

- `events-v23.json`
- `sign-v23.json`

等をMcRemote／Python／Scratchへ投影する仕組みが実働している。

したがってPhase Fは、

> machine-readable contractを新しく作り始める

段階ではない。

目標は、

> **既存の部分的なshared fixture／contractを、Java、TypeScript、C#等の独立実装追加にも耐えるProtocol
> conformance基盤へ一般化する**

ことである。

構成は一つの巨大schemaへ畳まず、

```text
human-readable contract
        +
machine-readable fixture / metadata
        +
executable conformance
```

の組合せを基本とする。

---

## 17. Machine-readable化するもの

machine-readable化に向くものから広げる。

例:

- protocol version metadata
- method name
- request／notification可否
- params shape
- result type
- error reason
- value schema
- canonical examples
- negative case
- compatibility fixture

一方、

- lifecycle
- timeout後のcompletion unknown
- ordering
- flush barrier
- authentication遷移
- event cursor

などは単純なJSON Schemaだけで完全に表せない。

すべてを一つのIDLへ入れること自体を目標にしない。

---

## 18. Conformance testと既存test taxonomy

新しい`Level A／B／C`のような分類軸は作らない。

既存のtest classを使う。

### `unit/deterministic`

この中で、

- codec test
- shared fixture test
- value encode／decode
- scripted peer

等を行う。

`scripted peer`はtest classではなく、fake server／fake clientを使ってProtocol会話を再現する**test technique**で
ある。

例:

```text
client → hello
peer   → protocol_mismatch
```

```text
client → request
peer   → unexpected id
```

```text
client → request
peer   → connection close
```

など。

### `live-auto`

実McRemote／Paperを相手に、人間操作なしで確認できる部分を検証する。

### `live-human`

pairing、browser UI、物理入力等、人間操作を必要とする部分を検証する。

### test tier

Tier 0〜4は、これらtest classとは別軸で、仕様成熟度と必要な主張強度を表す。

たとえば、

```text
Tier 2で
unit/deterministic shared fixture
+
短いlive-auto pulse
```

のように組み合わせる。

---

## 19. Conformanceは内部実装の統一ではない

Pythonがthreadを使い、Javaが別のconcurrency mechanismを使い、TypeScriptがPromiseを使ってもよい。

見るべきものは、

```text
同じProtocol input
       ↓
同じwire semantics
       ↓
同じserver-visible behavior
       ↓
言語に自然な結果
```

である。

Client Libraryの内部構造を一致させることをconformanceとは呼ばない。

---

## 20. Protocol専用repositoryは急いで作らない

Protocol SSOTは現在`mc-remote-knowledge/10-protocol`にある。

ここを維持する。

TypeScript側の`@mc-remote/protocol`は、型、定数、method identity、error reason、およびb6 protocol 23の
machine-readable shared fixture等を持つ実行可能なProtocol投影／限定ownerである。

しかし、knowledge SSOTそのものや、全Protocol version／全contractの包括ownerを置き換えるものではない。

将来、

- Maven
- npm
- NuGet
- CI
- 外部contributor

から共通Protocol artifactを直接取得する必要が強くなった場合は、生成artifactや独立distributionを検討できる。

正本を二つにはしない。

---

## 21. Phase G — TypeScriptを第三の独立実装にする

Javaの次は一般用途TypeScript Client Libraryへ進む。

Scratch Clientとは別物である。

最初はNode.jsを対象にする。

```text
TypeScript Client Library
          ↓
       TCP Transport
          ↓
      McRemote Plugin
```

とし、browser特有の問題を入れずにProtocol実装だけを試す。

ここで重要なのは、TypeScript版を、

> JavaコードをTypeScriptへ翻訳する

方式にしないことである。

Protocol contract＋shared fixture＋conformance materialを主入力として実装する。

Python／Javaは調査材料として使えるが、正本にはしない。

---

## 22. TypeScriptはProtocol独立性の試験になる

PythonとJavaはいずれも、

```text
native process
   ↓
TCP
```

という比較的近い環境にいる。

TypeScriptではNode.js版を作った後、

```text
Minecraft Remote Client API
        ↓
     Protocol
      /     \
     /       \
TCP Transport WebSocket Transport
   Node            Browser
```

へ広げられる。

これが成立すれば、

> ProtocolとTransportが本当に分離されているか

を強く試せる。

---

## 23. Phase H — Browser / WebSocket

Browser版では直接TCPを使えないため、既存Bridge／WSS経路を利用する。

```text
Browser TypeScript
       ↓ WSS
     Bridge
       ↓ TCP
 McRemote Plugin
```

このときClient APIから見えるMinecraft Remoteの意味を、Node TCP版と可能な範囲で共有する。

ただし、

- WebSocket lifecycle
- browser storage
- browser security
- Bridge routing

までProtocol本体へ逆流させない。

### Bridge Origin / allowlist

現行BridgeはScratch等の既存source／originを前提にした許可境界を持つ。

一般用途TypeScript browser clientを別originから提供する場合、そのoriginを無条件に既存許可へ乗せない。

Phase Hの実装前に、

- 利用origin
- Origin検証
- allowlist
- stable／beta／dev等のenvironment境界
- unknown originの拒否

を既存Bridge security boundaryと照合する。

---

## 24. Scratchとの関係

Scratch ClientはTypeScript／JavaScriptで実装されていても、一般用途TypeScript Client Libraryとは別のsurfaceで
ある。

したがって、

```text
@mc-remote/client
       ↓
Scratch extension
```

を自動的な目標にはしない。

Scratchには、

- block programming model
- project serialization
- fork内build-time bake
- Scratch runtime lifecycle

という固有条件がある。

共有すべきなのはコードそのものではなく、Protocolの意味である。

---

## 25. Phase I — C# / Unity

C# Client Libraryは一般用途の.NET／C#成果物とし、Unity専用品にはしない。

Protocol独立性の検証だけならJava／TypeScriptほど急がない一方、Unityを主要consumer／sampleとして
Minecraft Remoteの利用世界を大きく広げられる。

```text
Minecraft
    ↑
Minecraft Remote Protocol
    ↑
C# Client Library
    ↑
Unity application
```

が成立すれば、

- Unity内のobject状態をMinecraftへ送る
- Minecraft世界をUnity側で観察する
- 二つの3D environmentを同じcodeから操作する

といった教材・作品が可能になる。

C#対応は単なる言語数追加ではなく、

> **Minecraft Remoteが異なるconstruction environment同士を接続するProtocolになる**

ことを示す段階と位置づける。

---

## 26. Pythonへのback projection

多言語化の途中で、

> Java／TypeScriptを作った結果、Python内部の責任分離を直した方がよい

という発見が出る可能性がある。

その場合もPythonを全面rewriteしない。

必要な部分だけ、

- Protocol codec
- transport
- model
- Client API
- convenience layer

等の責任分離を改善する。

ここでの分類は**Client Library内部の責務面**である。

Phase Cで用いたBuild、World、Chat、Catalog、Player、Events等は**機能面**の分類であり、別軸である。

二つを同じ階層表現として混同しない。

---

## 27. 高水準機能をProtocolへ上げる基準

多言語化すると、

> 全Client Libraryで同じhelperを書くならserver commandにすればよい

という誘惑が生まれる。

これは自動規則にしない。

たとえば`buildPyramid`がPython、Java、TypeScriptに存在しても、それだけでProtocolへ昇格しない。

Protocol／pluginへ上げる主な理由は、既存の「機能実現の位置と昇格モデル」に従い、

- server-only capability
- atomicity
- permission／authorization
- shared-state concurrency
- finite work／performance
- 複数言語で共通に必要な意味
- lifecycle／recovery保証

などである。

便利さやコード重複だけでは足りない。

---

## 28. 共通sampleを多言語比較面にする

Client Libraryが増えたら、同じconceptを複数言語で実装したsampleを用意できる。

`2026-08-30-01`により、各Client Library開発repoは現行Client APIと一緒にbuild／testするREADME隣接の最小examplesを
所有し、`mc_remote_samples`はconcept-firstな言語間比較面を所有する。後者は前者を置き換える共通実装repoではない。
配置と学習UXの正本は[Client sampleの配置と多言語学習UX](../20-教材/client-sample-learning-ux_ja.md)とする。

例:

```text
00_hello
01_set_block
02_get_block
03_build_line
04_build_wall
05_build_pyramid
06_events
```

重要なのはコード構造を同じにすることではない。

各言語らしく書く。

そうすると、

> 同じMinecraft Remote capabilityを各言語ではどう表現するか

そのものが教材になる。

---

## 29. WireScopeをpolyglot観察面として使う

この方向はhub NOTES 2026-08-08で既に捕捉されていた候補を継承する。

WireScopeを将来、

```text
Python
Java
TypeScript
C#
```

が、

> 同じ操作をwire上でどう表現しているか

を見る共通観察面として使える。

これは単なるdebug用途ではない。

たとえば学習者が、

```text
Javaの setBlock
Pythonの setBlock
```

を実行し、どちらも最終的には同じ`world.setBlock`へ投影されることを観察できる。

Client APIとProtocolの違いを目で見られるため、多言語化とWireScopeは教育上も相性がよい。

ただし、本ロードマップから現行WireScope schema、station transport、保存境界を変更しない。

必要なobserver projectionは実際のJava／TypeScript source実装時に既存WireScope contractへ照合する。

---

## 30. OSS contributorに新しい入口を作る

Protocol contractとconformanceが育つと、新しい言語Client Libraryの追加そのものをOSS contributionにできる。

たとえばRust版を作りたいcontributorに、

> Pythonを読んで同じものを作ってください

と言う必要がなくなる。

代わりに、

```text
1. Protocol contractを読む
2. shared fixture / conformanceを読む
3. Client Libraryを実装する
4. unit/deterministicを通す
5. 必要なLive McRemote検証を行う
```

という明確な課題にできる。

LLM coding agentに対しても、

> この実装を真似せよ

より、

> このcontractとfixtureを満たせ

の方が逸脱を検出しやすい。

---

## 31. Versioningと各Client Libraryの進度

全Client Libraryを常に同じfeature levelへ揃える必要はない。

たとえば将来、

```text
Plugin       protocol 24.3
Python       requires 24.3
Java         requires 24.2
TypeScript   requires 24.1
C#           requires 24.0
```

のような状態があり得る。

互換判定はProtocol version negotiationが担う。

したがって、

> 新Protocol featureを追加するたび全言語実装を同時releaseする

ことを原則にしない。

これは多言語化の保守コストを有限にするために重要である。

---

## 32. 新機能開発の循環

Protocol-first化が進んだ後の新機能は、概ね次の循環へ寄せる。

```text
利用要求 / prototype
        ↓
意味を観察
        ↓
実現位置を比較
        ↓
Protocol変更が必要か判断
        ↓
必要ならcontract
        ↓
plugin
        ↓
必要なClient Libraryへ投影
        ↓
sample / 教材
        ↓
利用者観察
        ↓
次の改訂
```

必ずProtocolから始める必要はない。

prototypeから発見してよい。

重要なのは、

> prototypeの偶発的な形をそのまま横断契約にしない

ことである。

---

## 33. このロードマップが作らないもの

当面、次は目標にしない。

### Multi-language Client Library generator

一つのschemaからPython／Java／TypeScript／C#を全自動生成する仕組み。

Protocol semanticsがまだ実装比較から学ぶ段階なので早い。

### 全Client APIの形状統一

言語らしさを失うため採らない。

### Transport一本化

TCPとWebSocketには別々の存在理由がある。

### Python全面rewrite

既存価値を壊す。

### 全言語同時release

Protocol version negotiationの意味を失う。

### Client Libraryを増やすこと自体をKPIにする

Go、Rust、Kotlin等は要求やcontributorが現れたときに評価する。

言語数ではなく、

> 新しい利用世界、学習経路、Protocol検証価値が増えるか

で判断する。

---

## 34. マイルストーン

### Milestone A — Java bootstrap ready

- repository準備
- root package確定
- Java bootstrap baseline固定
- build／test skeleton成立

### Milestone B — Visible Java

Javaから、

- connect
- hello
- protocol negotiation
- auth
- setBlock
- getBlock

が実Minecraftで動く。

ここを最初の目に見える成果とする。

### Milestone C — Usable Java Client Library

主要なProtocol capabilityをJavaから利用でき、独立したsample applicationを書ける。

Python sourceを直接参照しなくても、利用者がJava版だけで始められる。

### Milestone D — Polyglot developer experience checkpoint

Javaの、

- catalog
- resource discovery
- types
- IDE completion
- documentation
- LLM支援

を含む開発体験を評価し、gap、推奨状態、改善先を記録する。

Pythonの実装方式をそのまま複製することは条件にしない。全gapの解消をMilestone E開始の条件にもしない。

### Milestone E — Two independent general-purpose implementations

PythonとJavaの二つが存在し、Protocol SSOTとの横断比較を完了する。

### Milestone F — Existing executable contract generalized

既存shared fixtureをJavaを含む独立Client Library群へ広げ、human-readable contractとmachine-readable
fixture／conformanceが相互に接続される。

### Milestone G — TypeScript Node

TypeScriptの第三実装がTCP経由で動く。

Javaコードの翻訳ではなくProtocol contractとshared fixtureを主入力に実装できることを確認する。

### Milestone H — Transport independence

同じ一般TypeScript Client Libraryの意味をbrowser／WebSocket経路へ投影できる。

必要なBridge Origin／allowlist境界も明示される。

### Milestone I — C# / Unity

一般用途C# Client Libraryを主要consumerであるUnityからも利用し、UnityとMinecraftを同じProtocolで接続できる。

### Milestone J — Polyglot normal operation

複数Client Libraryが異なる進度でProtocolへ追従し、

- compatibility matrix
- shared fixture／conformance
- sample
- documentation

によって利用可能範囲を判断できる。

---

## 35. 完了像

最終的なMinecraft Remoteは、

```text
PythonからMinecraftを操作するAPI
```

だけではなく、

```text
Minecraftを外部のプログラミング環境へ接続するProtocol
```

として説明できる。

そのProtocolへ、

```text
Scratch
Python
Java
TypeScript
C#
```

という異なるprogramming environmentが参加する。

それぞれの環境には、それぞれの学び方がある。

```text
Scratch       block programming
Python        programming / science / AI
Java          Minecraft plugin / mod / JVM
TypeScript    Web / Node / browser
C#            .NET / Unity / game development
```

しかしMinecraft世界へ向かう途中では、

```text
Client API
   ↓
Minecraft Remote Protocol
   ↓
McRemote Plugin
   ↓
Minecraft
```

という共通構造を見ることができる。

この共通構造そのものを、Minecraft Remoteの製品価値と学習価値の両方へ育てる。

---

## 36. 直近の一手

現在の次の一手はProtocol Inventoryを先に完成させることではない。

`2026-08-29-04`に従い、

```text
1. Java root packageを人間レビューで固定
2. 新Java repositoryを作る
3. library-firstの最小scaffoldを作る
4. Java bootstrap baselineへ接続する
5. 既存shared fixtureをJavaから利用できるか確認する
6. hello / protocol negotiationを通す
7. 必要ならpairingしてtoken付きhelloを通す
8. setBlock / getBlockを通す
9. 実Minecraftで確認する
```

である。

ここで得られた具体物と発見を持って、次のsliceを決める。

---

## 37. 一文で表す

> **b6で固定された実行可能なPython Client Libraryを比較対象として、まずJava bootstrap baseline上に現行Protocolの
> Java Client Libraryを一つ作り切る。その第二実装からProtocolと各言語固有surfaceの境界を抽出し、既に存在する
> 共有machine-readable fixture／conformance資産を多言語へ一般化したうえで、TypeScriptによって言語・Transport
> 独立性を検証し、一般用途C# Client LibraryとUnityへ利用世界を広げる。最終的にはPythonを含む各Client Libraryが、
> Minecraft Remote Protocolから対等に投影される構造へ移行する。**
