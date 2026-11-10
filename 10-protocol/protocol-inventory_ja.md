# Protocol Inventory（E1の表）

Protocolの各methodと、methodでない能力を、どのcomponentが投影しているかを1つの表にまとめる
（`2026-10-23-01`、進め方は[Phase E／Fの案](polyglot-phase-ef-plan_ja.md)の「E1」）。各列は、その担当が確認票で返した
ものを写す。coordinatorは実装を調べない。

- 行：`api-reference-metadata.json`の32 methodと、auth節の5 method、methodでない能力
- セル：「あり」「部分」「なし」。「あり」はClient APIへの投影があることで、全reasonや実機の全経路を確かめたことでは無い
- 共有fixtureの列：「あり」はそのmethodや能力の入力と期待値のcaseがあること。「部分」は値や一部の状態遷移だけ。
  値ベクトルがあってもmethodのparams／resultが無ければ「なし」。2026-11-06の10本は静的な入力と期待値。2026-11-10にF1の
  6本（44 case）が加わり、送受信の順を再生するcase（scripted peer）ができた（下の「F1のfixture」）
- McRemoteの列は、serverがそのmethodや能力を受けて処理すること。Scratchの列は、blockや拡張機能への投影があること
- 分類（E2）はまだしていない

## 返却の状況

| 列 | 状態 | 出典 |
| --- | --- | --- |
| McRemote | 2026-11-10 返却 | `Naohiro2g/McRemote` `a38beaf121ce06594391237cb09745ec0da7649d`の`docs/polyglot-e1_ja.md`（PR 15。基準は公開の`v2321.1.0`の`5b78ded`、protocol `23.2.1`） |
| Python | 2026-11-06 返却 | `Naohiro2g/minecraft-remote-api` `ac8969f9113afd18f5878068fa8806e89c21f5df`の`docs/polyglot-e1_ja.md`（基準はstable `v2321.0.0`の`fac0313`、protocol `23.2.1`。2321.1の候補`09bbda4`にも同じbytesで入る） |
| Java | 2026-11-06 返却 | `Naohiro2g/minecraft-remote-java` `6bfea96c4c189c3a1eb56f07cc1bd26b7ad18917`の`docs/polyglot-e1_ja.md`（基準はstable `2321.0.0`、protocol `23.2.1`） |
| Scratch | 2026-11-10 返却 | `Naohiro2g/scratch-editor` `dc2840ba3c5c9d6938555ed737bc199acca2586e`の`docs/polyglot-e1_ja.md`（PR 32。基準は公開の`v2321.1.0`の`57fb769`、protocol `23.2.1`） |
| 共有fixture | 2026-11-06 返却 | `Naohiro2g/minecraft-remote-tooling` `1286eb486bcaea93c4195c11e94304bdb51f53ba`の`packages/protocol/FIXTURE_INVENTORY_ja.md`（基準は`21a2a9a`の10本。PR 2で`main`へmerge） |
| 共有fixture（F1） | 2026-11-10 返却 | `Naohiro2g/minecraft-remote-tooling` `8264c3881bb4128c14cda6d122641ebcfa67d9c5`（PR 4）の`packages/protocol/test/fixtures/client-bootstrap-*`。形の説明は`packages/protocol/README.md`の「F1：client bootstrap の対話データ」 |

## method

| method | 分類 | McRemote | Python | Java | Scratch | 共有fixture |
| --- | --- | --- | --- | --- | --- | --- |
| `hello` | 接続 | あり（`RemoteSession.handleHello`。拒否は応答をflushして閉じる） | あり（`create()`／`hello()`） | あり（`Builder.connect()`） | あり（「接続する」`connect`） | あり（F1のhello 9 case。10本には認可のsnapshot） |
| `connection.flush` | 接続 | あり（`ConnectionCommands.handleFlush`。先行commandの終端まで） | あり（`flush()`。timeoutは接続を回収し、再送しない） | なし | あり（「送ったブロック設置が終わるまで待つ」`flushBuildCommands`、`setBuildMode`） | なし |
| `build.setDimension` | 建築の文脈 | あり（`BuildStateCommands.handleSetDimension`） | あり（`setDimension()`） | なし | あり（「建築する次元を…にする」`setDimension`） | なし（dimensionの値ベクトルだけ） |
| `build.setOrigin` | 建築の文脈 | あり（`BuildStateCommands.handleSetOrigin`） | あり（`setBuildOrigin()`） | あり（`setOrigin`） | あり（「建築原点…にする」`setBuildOrigin`。Yは0に固定） | なし（build contextの値例だけ） |
| `world.setBlock` | ブロック | あり（`BlockEditCommands.handleSetBlock`。成功は`null`、notificationも受ける） | あり（`setBlock()`。DEBUG／TRACE／FAST） | あり（`setBlock`／`BlockSpec`） | あり（「…に ブロックID … 状態 … を置く」`setBlock`。StateTextをcatalogの型で解決） | あり（F1のblocks 12 case。set→getと拒否。10本にはStateText／BlockValueの値ベクトル） |
| `world.setBlocks` | ブロック | あり（`BlockEditCommands.handleSetBlocks`。tickで分けて実行） | あり（`setBlocks()`） | あり（`setBlocks`） | あり（「…から…まで…を置く」`setBlocks`） | なし |
| `world.getBlock` | ブロック | あり（`BlockQueryCommands.handleGetBlock`。正準のBlockValue） | あり（`getBlock()`→`BlockValue`） | あり（`getBlock`→`BlockValue`） | あり（「…のブロック情報」`getBlock`。BlockInfoText） | あり（F1のblocks 12 case。10本にはBlockValueの値例） |
| `world.getBlocks` | ブロック | あり（`BlockQueryCommands.handleGetBlocks`。各軸10 blockまで） | あり（`getBlocks()`） | なし | あり（「…から…までのブロック情報を…に入れる」`getBlocks`） | なし |
| `world.getHeight` | ブロック | あり（`WorldB5Commands.handleGetHeight`） | あり（`getHeight()`） | なし | あり（「…の地面の高さ」`getHeight`、上限つきの`getHeightBelow`） | なし |
| `world.getSign` | 看板 | あり（`SignCommands.handleGetSign`） | あり（`getSign()`） | あり（`getSign`） | あり（「看板…の情報」`getSign`） | あり（`sign-v23`） |
| `world.setSign` | 看板 | あり（`SignCommands.handleSetSign`） | あり（`setSign()`） | あり（`setSign`） | あり（「看板…の…を…にする」`setSign`） | あり（`sign-v23`） |
| `world.updateSignLine` | 看板 | あり（`SignCommands.handleUpdateSignLine`） | あり（`updateSignLine()`） | あり（`updateSignLine`） | あり（「看板…の…行を…にする」`updateSignLine`） | あり（`sign-v23`） |
| `player.getPos` | プレイヤー | あり（`PlayerCommands.handleGetPosStructured`） | あり（`getPos()`。dictで返す） | なし | あり（「プレイヤーの…」`playerAttribute`） | なし |
| `player.setPos` | プレイヤー | あり（`PlayerCommands.handleSetPosStructured`） | あり（`setPos()`） | なし | あり（「プレイヤーを…へ移動する」`setPlayerPos`、`setPlayerXYZ`） | なし |
| `player.getPose` | プレイヤー | あり（`PlayerCommands.handleGetPoseStructured`） | あり（`getPose()`。dictで返す） | あり（`getPlayerPose`） | あり（「プレイヤーの…」`playerAttribute`） | なし |
| `player.setPose` | プレイヤー | あり（`PlayerCommands.handleSetPoseStructured`） | あり（`setPose()`） | あり（`setPlayerPose`。liveでの移動は未主張） | あり（「プレイヤーを…水平方向…上下方向…へ移動する」`setPlayerPose`） | なし |
| `player.getDirection` | プレイヤー | あり（`DirectionCommands`） | あり（`getDirection()`） | なし | あり（「プレイヤーの向き…」`playerDirection`） | あり（`direction-lightning-v23.1`） |
| `player.setDirection` | プレイヤー | あり（`DirectionCommands`。非ゼロの方向を正準化） | あり（`setDirection()`） | なし | あり（「プレイヤーの向きを…にする」`setPlayerDirection`） | あり（`direction-lightning-v23.1`） |
| `world.spawnEntity` | エンティティ | あり（`WorldB5Commands.handleSpawnEntity`） | あり（`spawnEntity()`→EntityHandle） | なし | あり（「エンティティ…を…に生成し ハンドルを…に入れる」`spawnEntity`） | なし（履歴の`spawn-v22`だけ。handleは旧形式） |
| `world.getNearbyEntities` | エンティティ | あり（`EntityLifecycleCommands.handleGetNearbyEntities`。playerを除く） | あり（`getNearbyEntities()`） | なし | あり（「…の半径…以内のエンティティを…に入れる」`getNearbyEntities`） | あり（`entity-particle-v23.2.1`） |
| `entity.getPose` | エンティティ | あり（`EntityLifecycleCommands`） | あり（`getEntityPose()`） | なし | あり（「エンティティ…の姿勢」`getEntityPose`） | あり（`entity-particle-v23.2.1`） |
| `entity.setPose` | エンティティ | あり（`EntityLifecycleCommands`） | あり（`setEntityPose()`） | なし | あり（「エンティティ…を…へ移動する」`setEntityPose`） | あり（`entity-particle-v23.2.1`） |
| `entity.getDirection` | エンティティ | あり（`DirectionCommands`） | あり（`getEntityDirection()`） | なし | あり（「エンティティ…の向き…」`entityDirection`） | あり（`direction-lightning-v23.1`） |
| `entity.setDirection` | エンティティ | あり（`DirectionCommands`） | あり（`setEntityDirection()`） | なし | あり（「エンティティ…の向きを…にする」`setEntityDirection`） | あり（`direction-lightning-v23.1`） |
| `entity.remove` | エンティティ | あり（`EntityLifecycleCommands`） | あり（`removeEntity()`） | なし | あり（「エンティティ…を取り除く」`removeEntity`） | あり（`entity-particle-v23.2.1`） |
| `world.spawnParticle` | 演出 | あり（`WorldB5Commands.handleSpawnParticle`。typed data、receiver、force） | あり（`spawnParticle()`。typed data、receiver、force） | 部分（dataの要らないparticleだけ。typed dataとreceiverはなし） | あり（`spawnParticle`と、receiver、ダスト、ブロックのparticleの指定block） | あり（`entity-particle-v23.2.1`、`direction-lightning-v23.1`） |
| `world.playSound` | 演出 | あり（`SoundCommands`） | あり（`playSound()`） | なし | あり（「音…を…で鳴らす」`playSound`、`soundOptions`） | あり（`entity-particle-v23.2.1`） |
| `world.playBlockSound` | 演出 | あり（`SoundCommands`） | あり（`playBlockSound()`） | なし | あり（「…のブロックの…音を鳴らす」`playBlockSound`） | あり（`entity-particle-v23.2.1`） |
| `world.strikeLightning` | 演出 | あり（`LightningCommands`） | あり（`strikeLightning()`） | なし | あり（「雷を…に落とす」`strikeLightning`） | あり（`direction-lightning-v23.1`） |
| `chat.post` | チャット | あり（`MiscCommands.handleChatPost`。成功は`null`、notificationは応答なし） | あり（`postToChat()`） | あり（`postToChat`） | あり（「チャットに…と言う」`postToChat`） | あり（`chat-event-compat-v23.2.1`） |
| `events.poll` | イベント | あり（`EventCommands.handlePoll`、`EventRing`。filtered pollとclearは無い） | あり（`pollEvents()`） | あり（`pollEvents`） | あり（3つのhat、`eventValue`、`eventStatus`。pollerは1つ） | あり（`events-v23`、`chat-event-compat-v23.2.1`） |
| `catalog.get` | カタログ | あり（`CatalogCommands.handleGet`、`CatalogService`） | あり（`getCatalog()`／`sync_constants()`。別のstreamで取る） | あり（`getCatalog`。生成定数は無い） | あり（「カタログの…を…に入れる」`catalogToList`。hashの照合とcache） | なし（block 4つのcatalog例だけ） |

## auth（metadataのauth節）

| method | McRemote | Python | Java | Scratch | 共有fixture |
| --- | --- | --- | --- | --- | --- |
| `auth.pairBegin` | あり（`AuthCommands.handlePairBegin`、`PairingManager.begin`。`client`の情報は保存も表示もしない） | あり（`create()`／`authenticate()`の中） | あり（接続の処理の中） | あり（「接続する」、`pairCode`、`pairCommand`） | あり（F1のpairing 7 case） |
| `auth.pairPoll` | あり（`AuthCommands.handlePairPoll`。pendingは成功のresult） | あり（同じ処理の中） | あり（接続の処理の中） | あり（「接続する」、`whenPaired`） | あり（F1のpairing 7 case） |
| `auth.listCredentials` | あり（`AuthCommands.handleListCredentials`。自分のlong-livedだけ） | なし | なし | なし（管理のblockは無い） | なし |
| `auth.revoke` | あり（`AuthCommands.handleRevoke`。失効したcredentialの全sessionを閉じる） | なし（`auth.clear_token()`はlocalの削除） | なし（`--forget`はlocalの削除） | なし（管理のblockは無い） | なし |
| `auth.logout` | あり（`AuthCommands.handleLogout`。long-livedだけ） | なし | なし | なし（管理のblockは無い） | なし |

## methodでない能力

| 能力 | McRemote | Python | Java | Scratch | 共有fixture |
| --- | --- | --- | --- | --- | --- |
| TCPのframing／JSON-RPC | あり（`BoundedLineReader`、`CommandParser`。LFのほかCRLF／CRも区切り。batchは扱わない） | あり | あり | 部分（JSON-RPCのidの照合とerrorの処理。TCPと改行の区切りはBridgeが持つ） | あり（F1のframing 7 case。clientが受ける側） |
| WebSocket／browser | 部分（WebSocketは受けない。BridgeがWebSocketのmessageをTCPの行に変える） | なし | なし | あり（browserのWebSocket→Bridge→McRemoteのTCP。Bridgeのsubprotocolを確かめる） | なし |
| protocol negotiation | あり（`ProtocolInfo.isCompatible`。majorの一致、serverのminorが同じか上、patchは見ない。拒否の後は切断） | 部分（23.2.1を申告し、`protocol_mismatch`を運ぶ。応答の版はPythonでは比べない） | あり（majorの一致、serverのminorが同じか上、patchは見ない） | あり（majorの一致、serverのminorが同じか上、patchは見ない） | あり（F1のhello。応答の版5つの互換判定と`protocol_mismatch`） |
| authentication／pairing | あり（`AuthCommands`、`PairingManager`、`PairCommand`。helloの前のpairとtokenつきhelloを分ける） | あり | あり | あり（接続、ペアコード、ペアリングのhat。long-livedの管理のUIは無い） | あり（F1のpairing 7 case。承認を拒む専用の応答は契約に無い。10本には認可と`auth_required`） |
| session credentialのUX | あり（serverの側：コードの承認、期限つきのsession token、long-livedの一覧と失効） | あり（接続先ごとのlocal token。config下のJSONで、OSのstoreではない） | あり（examplesでOSのstoreを選ぶ。long-livedは別） | あり（localStorageを接続先のsandboxごとに分ける。認証のerrorでtokenを捨てる） | 部分（F1のpairing。tokenの再利用と、無効なtokenを捨てること） |
| request／notification／flushと順序 | あり（`ConnectionCommandQueue`。notificationにはerrorも返さない。DEBUG／TRACEはclientの方針） | あり（DEBUG／TRACE／FAST、`flush()`、closeのときのflush） | 部分（同期requestと順序だけ。notification、flush、DEBUG／TRACE／FASTは無い） | あり（DEBUG／TRACEは応答を待つ、FASTの設置はnotification、flushが境界） | 部分（雷のrequest／notificationとmode別の失敗だけ。flushは無い） |
| events cursor／loss | あり（`EventRing`。有限のring、through／latestのcursor、loss。pushは無い） | あり | あり | あり（未知のeventでもcursorを進め、hatを作らない） | あり（`events-v23`、`chat-event-compat-v23.2.1`） |
| error reason | あり（`RemoteSession.respondError`がcode、message、`data.reason`を包む。想定外の例外は切断で、errorを返すとは限らない） | あり（code、message、data、reasonを保つ。全reasonの経路は未主張） | あり（code、message、data、reasonを保つ。全reasonの経路は未主張） | 部分（code、message、data、reasonは保つが、表示はallowlistのErrorTextで、未知のreasonは`remote_error`へまとめる） | あり（F1のerrors 3 case。JSON-RPC errorの外枠と、未知のreasonを保つ例。10本にはmethodごとのreason／data） |
| build context | あり（`BuildStateCommands`。dimensionとoriginは接続ごと） | あり | 部分（originだけ変えられる） | 部分（原点のYは0に固定） | 部分（値ベクトルだけ。context変更の対話は無い） |
| BlockValue／BlockSpec | あり（`BlockCodec`。wireの`block_id`とstateを受けて正準化する） | あり | あり | あり（StateTextとBlockInfoTextの文字列、picker） | あり（F1のblocks。10本の`block-value-v22`の値を参照する） |
| catalog／constants | あり（registryからcatalogとhashを作る） | あり（catalogHashをkeyにしたcacheと、`.py`／`.pyi`の生成） | 部分（catalogとhashを取る。生成定数とcacheは無い） | 部分（catalogHashの照合とIndexedDBのcache、ID一覧、名前とカテゴリの検索。生成した定数は無い） | 部分（resource IDとblock 4つの例。catalogHashの照合と完全なcatalogは無い） |
| helloの`world_constants` | 部分（`y_sea`だけ。ほかの世界定数は2400へ） | あり（`world_constants`と`y_sea`。生成では`world_info`） | 部分（Mapのまま渡す） | 部分（`world_constants`を保持し、observerへは`y_sea`だけ。読むblockは無い） | なし |
| epoch／reconnect | あり（接続ごとにepoch、handle、ringを作り、closeで捨てる。新しいTCPはhelloから） | 部分（`reconnect()`は新しいepoch。自動の再認証と再開は無い。handleのstaleはserverが判定） | 部分（つなぎ直すとhelloから。entity handleは無い） | 部分（closeで状態を捨て、次の「接続する」でtokenを使い直してhelloから。自動の再認証、再送、scriptの再開は無い） | 部分（F1のclose 6 case。新しい接続でhelloをやり直す。応答待ちのrequestの扱いと自動の再送は未確定。10本にはsession状態とhandleの失効） |
| WireScopeのobserver | なし（observerはclientとtoolingの側） | あり（`create(wirescope=True)`。TTYが前提） | なし | あり（WireScope miniと独立のwindow。credentialを伏せる） | 部分（未知eventのobserver投影だけ） |

### 担当が足した行

McRemoteとScratchが、表に無い能力として返したもの。Scratchの3行は、clientの使い勝手と言語に固有の投影で、新しい
Protocolの能力の提案ではない。

| 能力 | 担当 | 内容 |
| --- | --- | --- |
| 接続の前の有限の資源とadmission | McRemote | あり（`PreAuthAdmission`、`BoundedLineReader`、`ConnectionFrameQueue`。接続数、期限、frameとqueueの量。上限を超えるとtransportを閉じることがある） |
| tickの実行量と公平さ | McRemote | あり（`WorkAdmission`、`BlockEditCursor`。全methodの重さを一律には数えない） |
| 失効を永続させるcredential | McRemote | あり（`CredentialService`、`SqliteCredentialStore`。storeの障害ではfail-close） |
| resource IDの入力と出力の正準化 | McRemote | あり（`ResourceIds`、`BlockCodec`、`DimensionResolver`。namespaceを省いた入力と正準の出力） |
| ゲーム内の座標・時刻HUD | McRemote | あり（protocolの外。Client Libraryへ投影するものではない） |
| 変数やリストへの結果の投影 | Scratch | あり（`spawnEntity`、`getNearbyEntities`、`getBlocks`、`catalogToList`） |
| 名前とカテゴリの検索、stateの入力の補助 | Scratch | あり（GUIのblock picker。block IDを保存し、表示名とカテゴリは検索だけに使う） |
| reporterのモニターのpollを抑える | Scratch | あり（モニターの重複と頻度を抑え、明示した呼び出しとは分ける） |

## 共有fixtureの使い方

tooling `6447f6e8cbfbeeb9d229990b5c4f6e82a5875666`の`packages/protocol/test/fixtures/`の10本に対して、各clientがどれを
testへつないでいるか。MITのLICENSEを置いた`21a2a9a0aed8b4d9c715da46616aad86f1174b4c`の10本も同じbytes。
McRemote、Python、Java、Scratchとも、取得元は`21a2a9a`。F1の6本は、まだどのclientもtestへつないでいない（F3）。

| client | つないでいるもの | つないでいないもの |
| --- | --- | --- |
| Java | `chat-event-compat-v23.2.1.json`、`events-v23.json`、`sign-v23.json`、`spawn-v22.json` | `block-value-v22.json`（F1で使う予定）、`dimensions-v22.json`、`direction-lightning-v23.1.json`、`entity-particle-v23.2.1.json`（それぞれ対応する機能のsliceで）、`chat-event-compat-v23.2.json`、`entity-particle-v23.2.json`（履歴の版） |
| Python | `chat-event-compat-v23.2.1.json`、`direction-lightning-v23.1.json`、`entity-particle-v23.2.1.json`、`events-v23.json`、`sign-v23.json`。`chat-event-compat-v23.2.json`と`entity-particle-v23.2.json`は履歴としてbytesを比べるだけ | `block-value-v22.json`（F1で検討）、`dimensions-v22.json`（F1／build contextで検討）、`spawn-v22.json`（E2／F1で採否）。どれも時期は未定 |
| McRemote | `chat-event-compat-v23.2.1.json`、`direction-lightning-v23.1.json`、`entity-particle-v23.2.1.json`、`events-v23.json`、`sign-v23.json`（5本、6つのtest class）。`chat-event-compat-v23.2.json`と`entity-particle-v23.2.json`は履歴としてcopyだけ | `block-value-v22.json`、`dimensions-v22.json`、`spawn-v22.json`（copyも無い。McRemote独自のfixtureとは別） |
| Scratch | 10本すべて（履歴の版も、observerの投影などで使う）。どのfileも全caseを再生しているわけではない | なし |

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

### F1のfixture（2026-11-10、toolingの返却）

依頼は`00-hub/polyglot-f1-fixture-instructions_ja.md`。protocol `23.2.1`で、新しいclientがhelloからsetBlock／getBlockまでを
独立に作るためのもの。各caseは`steps`（`connect`、`client_send`、`peer_send`、`peer_bytes`、`peer_eof`、`client_close`、
`connect_error`、`approve_pairing`、`advance_time`）と`expected`を持ち、根拠のknowledgeの節を`basis`に書く。直接のTCPが基準で、
browserのWebSocketの境界とは分ける。tokenはfixture用の値。

| file | case | 範囲 |
| --- | ---: | --- |
| `client-bootstrap-framing-v23.2.1.json` | 7 | UTF-8の1行、文字の途中での分割、複数行の一括受信、未完の末尾、LFまでは未完、JSONでない行、idの対応 |
| `client-bootstrap-hello-v23.2.1.json` | 9 | tokenつきhello、最小のhello、完全なparams、応答の版5つの互換判定、`protocol_mismatch`の受信 |
| `client-bootstrap-pairing-v23.2.1.json` | 7 | `auth_required`→pending→承認→tokenつきhello、`pair_expired`、`pair_not_found`、知らない`token_type`、helloの`permission_denied`、tokenの再利用、無効なtoken |
| `client-bootstrap-blocks-v23.2.1.json` | 12 | set→get（namespace、state）、`unknown_block`、`unknown_property`、`invalid_property_value`、`invalid_params` |
| `client-bootstrap-errors-v23.2.1.json` | 3 | JSON-RPC errorの外枠、dataを保つこと、未知のreason |
| `client-bootstrap-close-v23.2.1.json` | 6 | 正常なclose、応答の後のEOF、行の途中のEOF、つながらない、応答待ちのrequestがあるEOF、新しい接続でのhello |

- 既存の10本とLICENSEはbytesが変わっていない。`client-bootstrap-v1.schema.json`とtoolingのowner test（52件）が、形と参照を確かめる
- toolingが「未確定」とした点：承認を拒む専用の応答（`pair_denied`）は契約に無い。`protocol_mismatch`のdataの欄の名前、
  messageの文言、codeの番号。EOFの時の末尾の扱い、応答待ちのrequestの例外の型とtimeout、自動の再送
- 実際のclientで44 caseを流すことと、実McRemoteとのpulseはF3

## E2への入力（2026-11-10）

E1の5列とF1の返却で見えた、E2で分類や判断が要るもの。coordinatorが返却どうしを突き合わせて挙げた。

- `protocol_mismatch`のerror：McRemoteはcode `-32600`、dataに`reason`、`server`、`client_requires`を返す。F1のfixtureは
  code `-32000`、dataは`reason`だけで、版はmessageに書き、dataの欄の名前とcodeの番号は「未確定」とした。契約は、codeを
  `-32000`番台とし（`wire-format-design_ja.md`の「6.3 失敗」）、errorにserverとclientの版を入れるとする
  （`versioning-design_ja.md`の「8.3 不一致時」）が、欄の名前は書いていない
- 応答の版の互換判定（`versioning-design_ja.md`の「8.2 互換判定（クライアント側）」）：Java、Scratchはする。Pythonは
  しない（23.2.1を申告するだけ）。F1のhelloの5 caseは、clientが判定することを期待する
- McRemoteの振る舞いで、F1が仮定しないもの：壊れたJSONや不正なidは、JSON-RPC errorを返さずに捨てるか、helloの前なら
  切断する。notificationにはerrorも返さない。想定外の例外と資源の上限は、応答なしで閉じることがある。serverはLFのほか
  CRLF／CRも区切りとして読む
- pairing：承認を拒む専用の応答は無く、承認されなければpendingから期限切れになる。`auth.pairBegin`の`client`の情報は、
  McRemoteが保存も表示もしない
- F1が「未確定」とした残り：EOFの時の末尾の扱い、応答待ちのrequestの例外の型とtimeout、自動の再送
- Scratch：原点のYは0に固定。errorの表示はallowlistで、未知のreasonは`remote_error`にまとめる。公開のブロック一覧
  （`/api/scratch/`の`blocks.json`とindex.html）は、`setDimension`と`setBuildOrigin`のmethodを`connection.setBuildContext`と
  書いているが、VMは`build.setDimension`と`build.setOrigin`を送る（hub NOTES 2026-11-10の行）
- 学習者が直し方まで分かるエラーと、適用中の権限と上限の照会（2026-11-10の相談、human owner「polyglotプロジェクトにも関わる」）：
  対処が違う原因をreasonで分け、入力箇所、値、上限をdataで伝える案と、送信前のローカル検証に原因と候補を持たせる案。
  検討メモ[learner-error-diagnostics-notes_ja.md](learner-error-diagnostics-notes_ja.md)

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

### Scratch（2026-11-10）

公開のsourceとtestの静的な確認で、学習者、タブレット、IDEでの操作は見ていない。

| 観点 | いまの状態 | 次に見るもの |
| --- | --- | --- |
| resourceの発見 | catalogからIDの一覧とstateの候補。同梱した公式の名前とカテゴリで検索 | 学習者が実際に探す操作 |
| 型 | ID、StateText、BlockInfoText、SignInfoTextで投影し、catalogで値の型を解決 | 文字列の投影と、型のあるAPIの使いやすさの比較 |
| 補完 | stateのpickerとメニュー。生成した定数は無い | IDEの補完との比較 |
| 編集と実行 | blockを選ぶ→script→接続とペアリング→実行。作品はbrowserかsb3へ保存 | cold readerとタブレットでの一連の操作 |
| 文書／LLM | 版ごとのブロック一覧（opcodeと表示名） | LLMの利用者の評価 |
