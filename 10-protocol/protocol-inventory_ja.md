# Protocol Inventory（E1の表）

Protocolの各methodと、methodでない能力を、どのcomponentが投影しているかを1つの表にまとめる
（`2026-10-23-01`、進め方は[Phase E／Fの案](polyglot-phase-ef-plan_ja.md)の「E1」）。各列は、その担当が確認票で返した
ものを写す。coordinatorは実装を調べない。

- 行：`api-reference-metadata.json`の32 methodと、auth節の5 method、methodでない能力
- セル：「あり」「部分」「なし」。「あり」はClient APIへの投影があることで、全reasonや実機の全経路を確かめたことでは無い
- 共有fixtureの列：「あり」はそのmethodや能力の入力と期待値のcaseがあること。「部分」は値や一部の状態遷移だけ。
  値ベクトルがあってもmethodのparams／resultが無ければ「なし」。10本とも静的な入力と期待値で、送受信の順を再生する
  scripted peerのcaseは無い
- 未返却の列は「—」
- 分類（E2）はまだしていない

## 返却の状況

| 列 | 状態 | 出典 |
| --- | --- | --- |
| McRemote | 未返却 | — |
| Python | 2026-11-06 返却 | `Naohiro2g/minecraft-remote-api` `ac8969f9113afd18f5878068fa8806e89c21f5df`の`docs/polyglot-e1_ja.md`（基準はstable `v2321.0.0`の`fac0313`、protocol `23.2.1`。2321.1の候補`09bbda4`にも同じbytesで入る） |
| Java | 2026-11-06 返却 | `Naohiro2g/minecraft-remote-java` `6bfea96c4c189c3a1eb56f07cc1bd26b7ad18917`の`docs/polyglot-e1_ja.md`（基準はstable `2321.0.0`、protocol `23.2.1`） |
| Scratch | 未返却 | — |
| 共有fixture | 2026-11-06 返却 | `Naohiro2g/minecraft-remote-tooling` `1286eb486bcaea93c4195c11e94304bdb51f53ba`の`packages/protocol/FIXTURE_INVENTORY_ja.md`（基準は`21a2a9a`の10本。PR 2で`main`へmerge） |

## method

| method | 分類 | McRemote | Python | Java | Scratch | 共有fixture |
| --- | --- | --- | --- | --- | --- | --- |
| `hello` | 接続 | — | あり（`create()`／`hello()`） | あり（`Builder.connect()`） | — | 部分（認可のsnapshotだけ。helloのrequest／responseは無い） |
| `connection.flush` | 接続 | — | あり（`flush()`。timeoutは接続を回収し、再送しない） | なし | — | なし |
| `build.setDimension` | 建築の文脈 | — | あり（`setDimension()`） | なし | — | なし（dimensionの値ベクトルだけ） |
| `build.setOrigin` | 建築の文脈 | — | あり（`setBuildOrigin()`） | あり（`setOrigin`） | — | なし（build contextの値例だけ） |
| `world.setBlock` | ブロック | — | あり（`setBlock()`。DEBUG／TRACE／FAST） | あり（`setBlock`／`BlockSpec`） | — | なし（StateText／BlockValueの値ベクトルだけ） |
| `world.setBlocks` | ブロック | — | あり（`setBlocks()`） | あり（`setBlocks`） | — | なし |
| `world.getBlock` | ブロック | — | あり（`getBlock()`→`BlockValue`） | あり（`getBlock`→`BlockValue`） | — | なし（BlockValueの値例だけ） |
| `world.getBlocks` | ブロック | — | あり（`getBlocks()`） | なし | — | なし |
| `world.getHeight` | ブロック | — | あり（`getHeight()`） | なし | — | なし |
| `world.getSign` | 看板 | — | あり（`getSign()`） | あり（`getSign`） | — | あり（`sign-v23`） |
| `world.setSign` | 看板 | — | あり（`setSign()`） | あり（`setSign`） | — | あり（`sign-v23`） |
| `world.updateSignLine` | 看板 | — | あり（`updateSignLine()`） | あり（`updateSignLine`） | — | あり（`sign-v23`） |
| `player.getPos` | プレイヤー | — | あり（`getPos()`。dictで返す） | なし | — | なし |
| `player.setPos` | プレイヤー | — | あり（`setPos()`） | なし | — | なし |
| `player.getPose` | プレイヤー | — | あり（`getPose()`。dictで返す） | あり（`getPlayerPose`） | — | なし |
| `player.setPose` | プレイヤー | — | あり（`setPose()`） | あり（`setPlayerPose`。liveでの移動は未主張） | — | なし |
| `player.getDirection` | プレイヤー | — | あり（`getDirection()`） | なし | — | あり（`direction-lightning-v23.1`） |
| `player.setDirection` | プレイヤー | — | あり（`setDirection()`） | なし | — | あり（`direction-lightning-v23.1`） |
| `world.spawnEntity` | エンティティ | — | あり（`spawnEntity()`→EntityHandle） | なし | — | なし（履歴の`spawn-v22`だけ。handleは旧形式） |
| `world.getNearbyEntities` | エンティティ | — | あり（`getNearbyEntities()`） | なし | — | あり（`entity-particle-v23.2.1`） |
| `entity.getPose` | エンティティ | — | あり（`getEntityPose()`） | なし | — | あり（`entity-particle-v23.2.1`） |
| `entity.setPose` | エンティティ | — | あり（`setEntityPose()`） | なし | — | あり（`entity-particle-v23.2.1`） |
| `entity.getDirection` | エンティティ | — | あり（`getEntityDirection()`） | なし | — | あり（`direction-lightning-v23.1`） |
| `entity.setDirection` | エンティティ | — | あり（`setEntityDirection()`） | なし | — | あり（`direction-lightning-v23.1`） |
| `entity.remove` | エンティティ | — | あり（`removeEntity()`） | なし | — | あり（`entity-particle-v23.2.1`） |
| `world.spawnParticle` | 演出 | — | あり（`spawnParticle()`。typed data、receiver、force） | 部分（dataの要らないparticleだけ。typed dataとreceiverはなし） | — | あり（`entity-particle-v23.2.1`、`direction-lightning-v23.1`） |
| `world.playSound` | 演出 | — | あり（`playSound()`） | なし | — | あり（`entity-particle-v23.2.1`） |
| `world.playBlockSound` | 演出 | — | あり（`playBlockSound()`） | なし | — | あり（`entity-particle-v23.2.1`） |
| `world.strikeLightning` | 演出 | — | あり（`strikeLightning()`） | なし | — | あり（`direction-lightning-v23.1`） |
| `chat.post` | チャット | — | あり（`postToChat()`） | あり（`postToChat`） | — | あり（`chat-event-compat-v23.2.1`） |
| `events.poll` | イベント | — | あり（`pollEvents()`） | あり（`pollEvents`） | — | あり（`events-v23`、`chat-event-compat-v23.2.1`） |
| `catalog.get` | カタログ | — | あり（`getCatalog()`／`sync_constants()`。別のstreamで取る） | あり（`getCatalog`。生成定数は無い） | — | なし（block 4つのcatalog例だけ） |

## auth（metadataのauth節）

| method | McRemote | Python | Java | Scratch | 共有fixture |
| --- | --- | --- | --- | --- | --- |
| `auth.pairBegin` | — | あり（`create()`／`authenticate()`の中） | あり（接続の処理の中） | — | なし |
| `auth.pairPoll` | — | あり（同じ処理の中） | あり（接続の処理の中） | — | なし |
| `auth.listCredentials` | — | なし | なし | — | なし |
| `auth.revoke` | — | なし（`auth.clear_token()`はlocalの削除） | なし（`--forget`はlocalの削除） | — | なし |
| `auth.logout` | — | なし | なし | — | なし |

## methodでない能力

| 能力 | McRemote | Python | Java | Scratch | 共有fixture |
| --- | --- | --- | --- | --- | --- |
| TCPのframing／JSON-RPC | — | あり | あり | — | なし |
| WebSocket／browser | — | なし | なし | — | なし |
| protocol negotiation | — | 部分（23.2.1を申告し、`protocol_mismatch`を運ぶ。応答の版はPythonでは比べない） | あり（majorの一致、serverのminorが同じか上、patchは見ない） | — | なし |
| authentication／pairing | — | あり | あり | — | 部分（認可とauth_requiredだけ。pairingの送受信は無い） |
| session credentialのUX | — | あり（接続先ごとのlocal token。config下のJSONで、OSのstoreではない） | あり（examplesでOSのstoreを選ぶ。long-livedは別） | — | なし |
| request／notification／flushと順序 | — | あり（DEBUG／TRACE／FAST、`flush()`、closeのときのflush） | 部分（同期requestと順序だけ。notification、flush、DEBUG／TRACE／FASTは無い） | — | 部分（雷のrequest／notificationとmode別の失敗だけ。flushは無い） |
| events cursor／loss | — | あり | あり | — | あり（`events-v23`、`chat-event-compat-v23.2.1`） |
| error reason | — | あり（code、message、data、reasonを保つ。全reasonの経路は未主張） | あり（code、message、data、reasonを保つ。全reasonの経路は未主張） | — | 部分（methodごとのreason／data。JSON-RPC errorの外枠は無い） |
| build context | — | あり | 部分（originだけ変えられる） | — | 部分（値ベクトルだけ。context変更の対話は無い） |
| BlockValue／BlockSpec | — | あり | あり | — | 部分（値のencode／decodeだけ。setBlock／getBlockの対話は無い） |
| catalog／constants | — | あり（catalogHashをkeyにしたcacheと、`.py`／`.pyi`の生成） | 部分（catalogとhashを取る。生成定数とcacheは無い） | — | 部分（resource IDとblock 4つの例。catalogHashの照合と完全なcatalogは無い） |
| helloの`world_constants` | — | あり（`world_constants`と`y_sea`。生成では`world_info`） | 部分（Mapのまま渡す） | — | なし |
| epoch／reconnect | — | 部分（`reconnect()`は新しいepoch。自動の再認証と再開は無い。handleのstaleはserverが判定） | 部分（つなぎ直すとhelloから。entity handleは無い） | — | 部分（session状態とhandleの失効。新しいTCPと再helloの対話は無い） |
| WireScopeのobserver | — | あり（`create(wirescope=True)`。TTYが前提） | なし | — | 部分（未知eventのobserver投影だけ） |

## 共有fixtureの使い方

tooling `6447f6e8cbfbeeb9d229990b5c4f6e82a5875666`の`packages/protocol/test/fixtures/`の10本に対して、各clientがどれを
testへつないでいるか。MITのLICENSEを置いた`21a2a9a0aed8b4d9c715da46616aad86f1174b4c`の10本も同じbytes。

| client | つないでいるもの | つないでいないもの |
| --- | --- | --- |
| Java | `chat-event-compat-v23.2.1.json`、`events-v23.json`、`sign-v23.json`、`spawn-v22.json` | `block-value-v22.json`（F1で使う予定）、`dimensions-v22.json`、`direction-lightning-v23.1.json`、`entity-particle-v23.2.1.json`（それぞれ対応する機能のsliceで）、`chat-event-compat-v23.2.json`、`entity-particle-v23.2.json`（履歴の版） |
| Python | `chat-event-compat-v23.2.1.json`、`direction-lightning-v23.1.json`、`entity-particle-v23.2.1.json`、`events-v23.json`、`sign-v23.json`。`chat-event-compat-v23.2.json`と`entity-particle-v23.2.json`は履歴としてbytesを比べるだけ | `block-value-v22.json`（F1で検討）、`dimensions-v22.json`（F1／build contextで検討）、`spawn-v22.json`（E2／F1で採否）。どれも時期は未定 |

### fixtureの中身（toolingの返却）

| file | 対象protocol | case | 現行か履歴か |
| --- | --- | ---: | --- |
| `block-value-v22.json` | 22系 | 18 | 現行に続けて使う値ベクトル |
| `dimensions-v22.json` | 22.0.0 | 17 | 現行に続けて使う |
| `direction-lightning-v23.1.json` | 23.1.0 | 93 | 現行に続けて使う |
| `entity-particle-v23.2.1.json` | 23.2.1 | 111 | 現行 |
| `entity-particle-v23.2.json` | 23.2.0 | 111 | 履歴 |
| `chat-event-compat-v23.2.1.json` | 23.2.1 | 33 | 現行 |
| `chat-event-compat-v23.2.json` | 23.2.0 | 33 | 履歴 |
| `events-v23.json` | 23.0.0 | 13 | 現行に続けて使う |
| `sign-v23.json` | 23.0.0 | 18 | 現行に続けて使う |
| `spawn-v22.json` | 22.0.0 | 5 | 履歴（entityのhandleが旧形式） |

toolingの見立てでは、今の10本だけでは、新しいclientがhelloからsetBlock／getBlockまでを独立に作れない。値の型、正準化、
reasonの一部は使えるが、最初の接続を成り立たせる対話が足りない。足りないのは、framing、hello／negotiation、
authentication／pairing、`world.setBlock`／`world.getBlock`の対話、JSON-RPC errorの外枠、close。追加の案はF1の入力で、
F1の範囲や新しいwireの契約は決めていない（返却の「3. F1の不足と追加案」）。

## Phase D：開発体験

`2026-10-23-01`の判断bで、Phase Dを独立したgateにせず、E1の中で見る。

### Java（2026-11-06）

sourceのcheckoutで代表的な機能を使い、型とcatalogを調べられる段階。評価はsource、README、生成したAPI、examplesの
静的な確認と、build／testで、IDEの操作や学習者の操作は見ていない。

| 観点 | いまの状態 | 次に見るもの |
| --- | --- | --- |
| resourceの発見 | examplesでcatalogのblock／entity／particleとblockのstateを読める | catalogのpropertyと許容値から入力を作る短い例 |
| 型 | `BlockSpec`／`BlockValue`、`PlayerPose`、看板、eventの型がある。block IDとpropertyは文字列で、コンパイル時には確かめない | 生成したsourceやbuilderが要るか（E2で分類） |
| 補完 | Javaの型とメソッドは補完できる。serverのresource IDとstateは補完できない | IDEでの実際の操作、catalogからの生成 |
| 編集と実行 | README→MyWorld→menu→作例→API。miseでJDKを選ぶ | 学習者の実際の操作。Maven artifactからの導入はまだ無い |
| 文書／LLM | 公開signatureからAPIの表を生成し、buildが一致を確かめる | catalogを安全にexportするか |

### Python（2026-11-06）

stableのsourceとREADME、既存のunitを静的に確かめた評価で、IDEの操作、cold reader、Jupyterの操作は見ていない。

| 観点 | いまの状態 | 次に見るもの |
| --- | --- | --- |
| resourceの発見 | `getCatalog()`と、生成したblock／entity／particle／`block_state`からIDとstateの候補を調べられる | 実際に探す操作 |
| 型 | `BlockValue`、`BlockId`、stateのTypedDict／Literal、看板、方向、entity、eventの型がある。player poseはdict。型だけではserverのregistryにあることを保証しない | type checkerとIDEでの実際の操作 |
| 補完 | 接続先のcatalogから`.pyi`を生成し、ID、property、許容値を補完できる。生成先はCWDで、Gitのignoreが要る。soundとdimensionは生成の対象外 | IDEで候補が出ること |
| 編集と実行 | README→uvで導入→`.py`を実行。starterのlocal設定。Notebookはmoduleのcacheと再接続を説明する | cold readerとJupyterの操作。WireScopeの起動はTTYが前提 |
| 文書／LLM | 公開signatureからAPIの参照を生成し、CIで一致を確かめる。catalogのLLM向けexportは無い | LLMの利用者の評価 |
