# Protocol Inventory（E1の表）

Protocolの各methodと、methodでない能力を、どのcomponentが投影しているかを1つの表にまとめる
（`2026-10-23-01`、進め方は[Phase E／Fの案](polyglot-phase-ef-plan_ja.md)の「E1」）。各列は、その担当が確認票で返した
ものを写す。coordinatorは実装を調べない。

- 行：`api-reference-metadata.json`の32 methodと、auth節の5 method、methodでない能力
- セル：「あり」「部分」「なし」。「あり」はClient APIへの投影があることで、全reasonや実機の全経路を確かめたことでは無い
- 未返却の列は「—」
- 分類（E2）はまだしていない

## 返却の状況

| 列 | 状態 | 出典 |
| --- | --- | --- |
| McRemote | 未返却 | — |
| Python | 未返却 | — |
| Java | 2026-11-06 返却 | `Naohiro2g/minecraft-remote-java` `6bfea96c4c189c3a1eb56f07cc1bd26b7ad18917`の`docs/polyglot-e1_ja.md`（基準はstable `2321.0.0`、protocol `23.2.1`） |
| Scratch | 未返却 | — |
| 共有fixture | 未返却 | minecraft-remote-tooling |

## method

| method | 分類 | McRemote | Python | Java | Scratch | 共有fixture |
| --- | --- | --- | --- | --- | --- | --- |
| `hello` | 接続 | — | — | あり（`Builder.connect()`） | — | — |
| `connection.flush` | 接続 | — | — | なし | — | — |
| `build.setDimension` | 建築の文脈 | — | — | なし | — | — |
| `build.setOrigin` | 建築の文脈 | — | — | あり（`setOrigin`） | — | — |
| `world.setBlock` | ブロック | — | — | あり（`setBlock`／`BlockSpec`） | — | — |
| `world.setBlocks` | ブロック | — | — | あり（`setBlocks`） | — | — |
| `world.getBlock` | ブロック | — | — | あり（`getBlock`→`BlockValue`） | — | — |
| `world.getBlocks` | ブロック | — | — | なし | — | — |
| `world.getHeight` | ブロック | — | — | なし | — | — |
| `world.getSign` | 看板 | — | — | あり（`getSign`） | — | — |
| `world.setSign` | 看板 | — | — | あり（`setSign`） | — | — |
| `world.updateSignLine` | 看板 | — | — | あり（`updateSignLine`） | — | — |
| `player.getPos` | プレイヤー | — | — | なし | — | — |
| `player.setPos` | プレイヤー | — | — | なし | — | — |
| `player.getPose` | プレイヤー | — | — | あり（`getPlayerPose`） | — | — |
| `player.setPose` | プレイヤー | — | — | あり（`setPlayerPose`。liveでの移動は未主張） | — | — |
| `player.getDirection` | プレイヤー | — | — | なし | — | — |
| `player.setDirection` | プレイヤー | — | — | なし | — | — |
| `world.spawnEntity` | エンティティ | — | — | なし | — | — |
| `world.getNearbyEntities` | エンティティ | — | — | なし | — | — |
| `entity.getPose` | エンティティ | — | — | なし | — | — |
| `entity.setPose` | エンティティ | — | — | なし | — | — |
| `entity.getDirection` | エンティティ | — | — | なし | — | — |
| `entity.setDirection` | エンティティ | — | — | なし | — | — |
| `entity.remove` | エンティティ | — | — | なし | — | — |
| `world.spawnParticle` | 演出 | — | — | 部分（dataの要らないparticleだけ。typed dataとreceiverはなし） | — | — |
| `world.playSound` | 演出 | — | — | なし | — | — |
| `world.playBlockSound` | 演出 | — | — | なし | — | — |
| `world.strikeLightning` | 演出 | — | — | なし | — | — |
| `chat.post` | チャット | — | — | あり（`postToChat`） | — | — |
| `events.poll` | イベント | — | — | あり（`pollEvents`） | — | — |
| `catalog.get` | カタログ | — | — | あり（`getCatalog`。生成定数は無い） | — | — |

## auth（metadataのauth節）

| method | McRemote | Python | Java | Scratch | 共有fixture |
| --- | --- | --- | --- | --- | --- |
| `auth.pairBegin` | — | — | あり（接続の処理の中） | — | — |
| `auth.pairPoll` | — | — | あり（接続の処理の中） | — | — |
| `auth.listCredentials` | — | — | なし | — | — |
| `auth.revoke` | — | — | なし（`--forget`はlocalの削除） | — | — |
| `auth.logout` | — | — | なし | — | — |

## methodでない能力

| 能力 | McRemote | Python | Java | Scratch | 共有fixture |
| --- | --- | --- | --- | --- | --- |
| TCPのframing／JSON-RPC | — | — | あり | — | — |
| WebSocket／browser | — | — | なし | — | — |
| protocol negotiation | — | — | あり（majorの一致、serverのminorが同じか上、patchは見ない） | — | — |
| authentication／pairing | — | — | あり | — | — |
| session credentialのUX | — | — | あり（examplesでOSのstoreを選ぶ。long-livedは別） | — | — |
| request／notification／flushと順序 | — | — | 部分（同期requestと順序だけ。notification、flush、DEBUG／TRACE／FASTは無い） | — | — |
| events cursor／loss | — | — | あり | — | — |
| error reason | — | — | あり（code、message、data、reasonを保つ。全reasonの経路は未主張） | — | — |
| build context | — | — | 部分（originだけ変えられる） | — | — |
| BlockValue／BlockSpec | — | — | あり | — | — |
| catalog／constants | — | — | 部分（catalogとhashを取る。生成定数とcacheは無い） | — | — |
| helloの`world_constants` | — | — | 部分（Mapのまま渡す） | — | — |
| epoch／reconnect | — | — | 部分（つなぎ直すとhelloから。entity handleは無い） | — | — |
| WireScopeのobserver | — | — | なし | — | — |

## 共有fixtureの使い方

tooling `6447f6e8cbfbeeb9d229990b5c4f6e82a5875666`の`packages/protocol/test/fixtures/`の10本に対して、各clientがどれを
testへつないでいるか。

| client | つないでいるもの | つないでいないもの |
| --- | --- | --- |
| Java | `chat-event-compat-v23.2.1.json`、`events-v23.json`、`sign-v23.json`、`spawn-v22.json` | `block-value-v22.json`（F1で使う予定）、`dimensions-v22.json`、`direction-lightning-v23.1.json`、`entity-particle-v23.2.1.json`（それぞれ対応する機能のsliceで）、`chat-event-compat-v23.2.json`、`entity-particle-v23.2.json`（履歴の版） |

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
