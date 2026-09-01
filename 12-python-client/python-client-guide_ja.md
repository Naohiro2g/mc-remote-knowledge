# マイクラリモコン Python API セットアップと使い方

このガイドは Python API `2100.0.0b3`、wire protocol `21.0.0` の現行導線を説明します。対象実装は `Naohiro2g/minecraft-remote-api` の tag `v2100.0.0b3`、commit `af2d11d66a16e3085f569241406a703a1c28c348` です。

`2100.0.0b3` は GitHub prerelease のみで、PyPIには公開していません。素の `pip install minecraft-remote-api` は旧stableを選ぶため、b3を試す場合はsource checkoutまたはGitHub tagへのexact pinを使います。

## 1. starterを準備する

source repositoryのstarterを使う場合は次の順です。

```bash
git clone https://github.com/Naohiro2g/minecraft-remote-api.git
cd minecraft-remote-api
git checkout v2100.0.0b3
uv sync
cd starter
cp param_mc_remote.template.py param_mc_remote.py
```

既存projectへdependencyとして追加する場合はtagを明示します。

```bash
uv add "minecraft-remote-api @ git+https://github.com/Naohiro2g/minecraft-remote-api@v2100.0.0b3"
```

`param_mc_remote.py` はディレクトリ固有のenvironment adapterです。starterのtemplateが持つ設定は次の3つだけです。

```python
from mc_remote.vec3 import Vec3

ADRS_MCR = "sb.mc-remote.com"
PORT_MCR = 25575
BUILD_ORIGIN = Vec3(2000, 0, 2000)
```

- `ADRS_MCR`：McRemote socketの接続先。公式sandboxを使う場合は変更不要です。
- `PORT_MCR`：McRemote socketのport。Minecraftへ入るportとは別です。
- `BUILD_ORIGIN`：このディレクトリの建築座標系の原点です。

`PLAYER_NAME` と `PLATFORM` は使いません。player identityはpairing、Minecraft versionとregistryは認証済みhelloとcatalogで確定します。tokenもこのファイルには書きません。

`param_mc_remote.py` はGit管理外です。privateな接続先やディレクトリ固有の原点を共有コードへ埋め込まないでください。

## 2. 最初の接続とpairing

starterの `hello.py` は、最初の接続前には存在しない `mc_constants` をimportせずに動きます。

```python
import param_mc_remote as param
from param_mc_remote import BUILD_ORIGIN as ORIGIN
from mc_remote.minecraft import Minecraft

mc = Minecraft.create(address=param.ADRS_MCR, port=param.PORT_MCR)
mc.setBuildOrigin(ORIGIN.x, ORIGIN.y, ORIGIN.z)

mc.postToChat("Hello, Minecraft from Python!")
mc.setBlock(5, 62 + 5, 5, "sea_lantern")
```

実行します。

```bash
uv run python hello.py
```

認証が必要な初回接続では、Python側に次の形のcommandが表示されます。

```text
/mcremote pair NNN-NNN
```

pair codeの有効時間内に、接続対象のMinecraftへ入り、このcommandを実行します。pairingしたMinecraft playerが認証済みidentityになります。Pythonコードからplayer名を送る必要はありません。

`Minecraft.create()` は保存済みtokenがあれば先にhelloを試し、必要な場合だけpairingへ進みます。公開既定のcredentialは短命な `session` です。`permission_denied` は認可拒否でありtokenを破棄しません。

CIやbatchなどpairing待機を許さない環境では `pair=False` を指定します。credentialが無ければ `PairingRequiredError` になり、pairing commandは発行しません。

```python
mc = Minecraft.create(
    address=param.ADRS_MCR,
    port=param.PORT_MCR,
    pair=False,
)
```

## 3. 接続後に補完を獲得する

認証済みhelloでserverが `catalogHash` を返すと、`Minecraft.create()` は既定で次を行います。

1. PC global cacheに同じhashのcatalogがあれば再利用する。
2. cache missなら、建築用とは別の短命な認証済みstreamで `catalog.get` を呼ぶ。
3. block／entity／particle schemaとSHA-256 `catalogHash`を検証する。
4. 現在の作業ディレクトリへ `mc_constants.py` と `mc_constants.manifest.json` をatomicに公開する。

raw catalog cacheのrootは次の優先順です。

1. `$MCREMOTE_CACHE_DIR`
2. `$XDG_CACHE_HOME/mcremote`
3. `~/.cache/mcremote`

project-localな生成物は接続先から得る一時projectionであり、packageには同梱されず、Gitにもcommitしません。manifestは少なくとも `catalogHash`、projection key、generator version、projection schema version、`mc_constants.py` のSHA-256を持ちます。

starter以外のGit projectでは、最初の接続前にignore規則を用意します。

```bash
mcremote init
```

このcommandは `.gitignore` へ `param_mc_remote.py`、`mc_constants.py`、manifest、一時lock／staging fileの規則を冪等追加するだけです。templateの作成、接続、pairing、projection生成は行いません。

Git管理下でprojectionが安全にignoreされていない場合、生成は拒否されます。ただし接続済み `Minecraft` objectは返り、建築は継続できます。

## 4. 生成された定数を使う

最初の接続後は、通常のPython moduleとしてimportできます。旧設計のように「先に `mc_remote` をimportするとimport時に生成される」という順序規則はありません。

```python
import param_mc_remote as param
from param_mc_remote import BUILD_ORIGIN as ORIGIN
from mc_constants import block, entity, particle, world_info
from mc_remote.minecraft import Minecraft

mc = Minecraft.create(address=param.ADRS_MCR, port=param.PORT_MCR)
mc.setBuildOrigin(ORIGIN.x, ORIGIN.y, ORIGIN.z)
mc.setBlock(6, world_info.Y_SEA + 5, 5, block.GOLD_BLOCK)
```

- `block`、`entity`、`particle` は接続先serverの現在のregistryから一括生成されます。
- `world_info` はhelloの `world_constants` から生成され、b3では `Y_SEA` を利用できます。
- `MC_VERSION` と `CATALOG_HASH` もmoduleに含まれます。
- `PLATFORM` による版選択や、カテゴリごとに旧版へfallbackする仕組みはありません。

fresh cloneでは、同じcatalogがPC cacheにあっても、そのproject自身の認証済みhelloが成功するまでprojectionを作りません。補完が無い状態は、まだその環境で接続を成立させていないことを観察する入口です。

## 5. build stateとplayer identity

player identityとbuild stateは別の層です。

- identity：pairingしたplayer。`getPos()`／`setPos()`の対象になります。
- build state：各connection／streamが持つ正準DimensionKeyとorigin。
- project設定：`param_mc_remote.py` が持つ接続先と初期 `BUILD_ORIGIN`。

`1 Minecraft instance = 1 connection = 1 build state`です。`setPlayer()` は削除され、次を使います。

```python
mc.setDimension("overworld")
mc.setBuildOrigin(ORIGIN.x, ORIGIN.y, ORIGIN.z)
```

建築座標はorigin相対で、絶対座標は`origin + relative`です。Y座標にも暗黙offsetはありません。`setDimension()`と`setBuildOrigin()`はsession中に変更できます。入力は完全修飾DimensionKeyまたは`minecraft` namespaceを省略したpathで、出力と保持値は常に完全修飾します。`setWorld()` aliasは作りません。

b3の主要APIは次のとおりです。

| Python API | 役割 |
| --- | --- |
| `postToChat(message)` | chatへ投稿 |
| `setBlock(x, y, z, block_id, *, state=None)` | 1個設置し、全build modeで`None`を返す（protocol 22／b5） |
| `setBlocks(x0, y0, z0, x1, y1, z1, block_id, *, state=None)` | 直方体を設置し、全build modeで`None`を返す（protocol 22／b5） |
| `getBlock(x, y, z)` | `BlockValue(block_id, state)`を取得（protocol 22／b5） |
| `getBlocks(x0, y0, z0, x1, y1, z1)` | 各軸10／最大1000件をz最速順の`BlockValue` sequenceで取得 |
| `setDimension(dimension)` | このstreamのbuild dimensionを変更し、serverの正準resultから現在contextを更新 |
| `setBuildOrigin(x, y, z)` | このstreamのoriginを変更 |
| `getPos()` | paired playerのdimensionとorigin相対位置を取得 |
| `setPos(dimension, x, y, z)` | paired playerを明示dimensionのorigin相対位置へ移動 |

protocol 22ではblock IDとstateを分ける。state propertyを持たないblockやMinecraft既定stateを
使う場合は、stateを指定しない。

```python
mc.setBlock(0, 0, 0, block.GOLD_BLOCK)

mc.setBlock(
    0,
    0,
    0,
    block.OAK_LOG,
    state={"axis": "z"},
)
```

`None`は送信前に空state objectへ正規化される。公開helperとしての`block_ref()`はprotocol 22の
正準APIに含めず、propertyを`**kwargs`だけで受ける形も主APIにしない。mod由来propertyがPython
identifierにならない場合や、将来option名と衝突する場合にも`state` mappingなら同じ形を保てる。

`getBlock()`はimmutableな値を返す。

```python
value = mc.getBlock(0, 0, 0)

print(value.block_id)           # minecraft:oak_log
print(value.state)              # {"axis": "z"}
print(value.state.get("axis"))  # z
```

`setBlock()`／`setBlocks()`は全build modeで`None`を返す。適用後の状態を観察する場合は`getBlock()`／
`getBlocks()`を明示的に呼ぶ。`getBlocks()`は端点方向に依存せずmin／maxへ
正規化したx→y→z（z最速）順を保つ。各要素へ座標を重複させず、旧`getBlockWithData()`は提供しない。

state propertyを持たないblockは`state == {}`となる。入力の短縮vanilla ID／部分stateと、出力の
完全修飾ID／full stateという正準化はpluginが所有し、Python側で別の文字列表現へ戻さない。
共通値モデルは[ブロック値・状態・多言語投影設計](../10-protocol/block-value-design_ja.md)を参照する。

### build execution mode

`world.setBlock`／`world.setBlocks`は単一APIのまま、connection単位のclient execution policyを持つ。

```python
from mc_remote.minecraft import BuildMode, Minecraft

mc = Minecraft.create(
    build_mode=BuildMode.TRACE,
    trace_delay=0.25,
)

mc.setBuildMode(BuildMode.FAST)
mc.setBuildMode(BuildMode.TRACE, trace_delay=1.0)
mc.flush()
```

- DEBUGはid付きrequestを送りresponseまで待つ。library既定modeである。
- TRACEはid付きrequestの成功後、呼出元を`trace_delay`秒待たせる。既定は`0.25`秒、許容範囲は
  有限な`0`〜`2.0`秒（両端を含む）で、範囲外をclampせず、error時は待たない。
- FASTはnotificationを送り、個別server responseを待たない。finite bufferのbackpressureには従う。
- modeとdelayはconnection／stream個別のclient stateで、wire paramsやhelloへ追加しない。
- mode切替は同じ送信sequencerへtransition fenceとして登録し、`connection.flush`成功後に原子的に反映する。
  flush失敗時は旧modeを維持する。
- 各setterは登録時点のmodeとdelayを保持する。後のmode変更で成立済みTRACE待機を変更しない。
- 正常な`close()`／context manager終了は自動flushする。flush失敗は完了保証失敗として通知したうえで
  connectionを回収する。context manager本体の例外とclose／flush失敗が重なる場合は本体例外をprimaryに
  維持し、close／flush失敗をexception chainまたはnoteへ残す。本体例外が無い場合はclose／flush失敗を
  呼出元へ送出する。この優先順位と、いずれの場合もconnectionを回収することをfixtureで固定する。

`mc.flush()`はworldを読まない明示barrierであり、先行FAST notificationの個別成功を復元しない。同一connectionの
後続get requestもFIFO上は先行commandを追い越さないが、教材では完了確認に`flush()`を使う。
flushは通常のconnection request timeoutを共用する。timeout時は先行処理の成否を確定せず、自動retryせず、
mode切替を成立させずにconnectionを回収する。timeout実値はcandidate fixture／lockへ固定し、protocol定数にしない。

## 6. catalog／projectionの失敗

`Minecraft.create()` による自動projectionはbest-effortです。fetch、validate、cache、generate、publish等で失敗すると `CatalogProjectionWarning` を出しますが、認証済みbuild streamは維持し、接続済みclientを返します。

warningには失敗stage、接続と建築は成功していること、補完だけが更新されなかったこと、再試行方法が含まれます。token、`pairing_id`、credential内容は含めません。pairing進行の通常logはpair codeと表示用commandを記録できます。

修正後は明示的に再試行できます。

```python
mc.sync_constants(force=True)
```

明示した `sync_constants()` はstrictで、失敗時に `CatalogProjectionError` を送出しますが、既存build streamはcloseしません。catalog処理自体を省く場合は次を使います。

```python
mc = Minecraft.create(
    address=param.ADRS_MCR,
    port=param.PORT_MCR,
    sync_catalog=False,
)
```

## 7. 困ったときは

| 症状 | 確認と対処 |
| --- | --- |
| `mc_constants` が見つからない | 最初のprogramではimportせず、認証済みhelloを一度成功させる |
| `stage=ignore` のwarning | project rootで `mcremote init` を実行し、再接続または `mc.sync_constants(force=True)` |
| projection warningが出た | 建築は継続可能。stageを直して明示syncを再試行する |
| pair codeが期限切れ | `Minecraft.create()` をもう一度実行して新しいcodeを取得する |
| `PairingRequiredError` | 対話環境で `pair=True` として一度接続するか、対象token namespaceへcredentialを用意する |
| `permission_denied` | tokenを消さず、server operatorへLuckPerms設定を確認する |
| 別接続先のtokenを使ってしまう | `token_key`を明示する。互換引数`sandbox`もlocal token keyとしてだけ働き、wireへ送られない |
| VS Codeで違う場所へ生成される | starterの`.vscode`設定を使うか、実行時CWDをscriptのディレクトリへ合わせる |
| Jupyterで古い定数が残る | kernelを再起動し、projection生成後に最初からcellを実行する |

## 8. credentialの保存と公開gate

token storeは `$MCREMOTE_CONFIG_DIR`、`$XDG_CONFIG_HOME/mcremote`、`~/.config/mcremote` の優先順で解決し、`token.json` を接続先namespace別に保持します。`token_key`を省略した既定namespaceは `"{address}:{port}"` です。

token、`pairing_id`、player UUIDをsource、URL、通常log、Git管理fileへ書かないでください。`param_mc_remote.py` にcredentialを置かないでください。pair codeは約120秒・一回限りの表示・操作用コードなので、console、通常log、test transcript、Git管理の公開evidenceへ残して構いません。ただし再利用可能な設定値やcredentialとして保存しません。

現行のinstalled CLIが持つsubcommandは `mcremote init` だけです。`login`、`status`、`devices`、`revoke`、`logout` は未実装であり、現行手順として案内しません。

long-lived credentialの公開gateは閉じています。Pythonの既定を `long_lived` へ切り替えず、実利用で需要が確認されるまでcredential-lifecycle sliceを後続へ送ります。再開後の順序は正式list／revoke／logout API、checkpoint＋doctor、secret-safe live runner、snapshot rollback transaction、reset／災害復旧です。正本は [認証ロードマップ](../00-hub/authentication-roadmap_ja.md) と決定 `2026-08-07-01` です。

## 9. WireScope（Python追従条件）

現行の `mcremote` に `wirescope` subcommandはありません。Scratch参照実装は共通
`@mc-remote/live` appと observer contract を先行固定済みであり、Pythonは完成UIを再解釈せず、
次の schema v1 入力条件へ追従します（`2026-08-06-03` の2026-08-07追記）。

- top-level は `schema=mcremote.observer`、`schema_version=1`、`emitted_at`、`target`、`streams[]`。
  Python source は `target.source_kind=python` とし、target ID と stream ID を同一化しません。
- 初版は `Minecraft.create()` で成立した main connection 1件を `kind=main` として投影します。
  `1 stream = 1 connection = 1 build state` を維持し、将来の明示 substream を schema 破壊なしで
  `streams[]` へ追加できる形にします。
- `streams[].hello`は初期handshakeの記録です。protocol 22では`hello.dimension`／`hello.origin`を後続の
  `build.setDimension`／`build.setOrigin`による現在値で上書きしません。現在の可変build stateは
  schema v1へ未宣言 fieldとして追加せず、次の schema sliceで `current_build_state` と lifecycle／fixtureを
  共に固定してから追従します。現在値を得るためだけの25ms pollingも行いません。
- adapter は Scratch lifecycle fixture と schema validator に対する conformance を満たし、
  generation-side allowlistでhello、permissions、world constantsと許可された建築／dimension／player
  frame・payloadだけを生成します。任意の Python object、無制限な履歴、内部 transport 状態を
  observer feedへ直列化しません。
- `auth.*`、token、pair code、player UUID、credential／device情報を生成せず、history、grant、
  observer sessionをproject fileやcredential storeへ永続化しません。observerへ認証・操作権限も
  渡しません。
- 新規targetの`display_alias`は共通alias contract v1（`2026-08-12-03`）へ従います。正本fixtureはScratch
  `develop@3b3d1f1c8a0dd66d265c5c6ea515cc5ac291209b`の
  `mc-remote/live/test/fixtures/display-alias-v1.json`です。Pythonの現行8桁uppercase hex生成器は移行対象で、
  canonical `WORD-WORD-NNNNNN`、connection epoch固定、再接続時新規生成、active衝突時再生成をfixture／testで
  閉じるまで共通alias conformance完了としません。observer schema v1の受理shapeは狭めません。

共通appとの接続は[WireScope deployment設計](../15-wirescope/wirescope-deployment-design_ja.md)と
[station attach設計](../15-wirescope/wirescope-station-attach-design_ja.md)に従います（`2026-08-10-02`、
`2026-08-11-02`／`2026-08-11-03`）。最初に実装するのはsource／station／browserが同じnetwork namespaceに
あるbrowser-loopback profileだけです。station roleをsource processへ融合し、`127.0.0.1`のephemeral portで
共通appを提供します。UDS、named pipe、cross-process relay、LAN、VPSを初期sliceへ含めません。

公式cross-origin browser handoffの`wirescope[-channel].mc-remote.com`はScratch等のbrowser source用surfaceであり、
Python browser-loopbackは使用しません。Python wheelが共有するのはexact app artifact／manifest／schema／UIで、
public originやresponse headerではありません。Python初期profileのsource ingressはsource process内のin-process
callbackであり、public pageからloopbackへfetch／WebSocketを伸ばす構成やnetwork source ingressへ変更しません
（`2026-08-20-01`／`02`）。

APIは`wirescope=None | bool | WireScopeStation`を受け、`None`／`False`ではstation、artifact検証、browser、
observer hookを開始しません。`True`は恒久的に`WireScopeStation.local()`のlow-floor省略形です。初期sliceは
`local()`だけを実装し、将来profileを追加しても`True`の意味を変えません。

stationはbrowser attachを待たず、通常のMinecraft接続、pairing、authenticated helloを進めます。TTY、
artifact、stationのpreflightに失敗した場合はWireScopeだけをactionable warning付きで開始せず、Minecraft接続を
継続します。observer hookはMinecraft RPC thread上でnetwork待機やsnapshot serializeをせず、有限のingress
queueへ渡します。rolling windowの省略はobserver session envelopeで可視化し、backpressureと単一frame超過は
observerだけを終了します。件数、byte数、code表現、期限、試行、再発行、cooldownはPython fixture／testで
機械化します。session protocol v1のserialized conformance入力はScratch参照実装の
`mc-remote/live/test/fixtures/observer-session-lifecycle.ndjson`とし、Python固有shapeを別に作りません。
HTTP stationは同じ参照実装commit `192d1e3ccd213fb5012b92655e51b779270e15be`の
`mc-remote/live/test/fixtures/station-attach-v1.json`（SHA-256
`b50ce8e0cb8a6bb06f75d9bdad59b83006c92683bd73ced84a18223dde21fa81`）へconformanceします。
bootstrap、attach request、error status／attempt消費、byte上限、security header、NDJSON framingを
Python側で独自解釈しません。機械的conformanceは
`Naohiro2g/minecraft-remote-api@14a662e173e3805870987691a938292a5de6e456`へ固定した。targeted tests
79件、全回帰159件、`uv lock --check`、sdist／wheel build、`git diff --check`がPASSした。

後続の内部runtimeは実装commit `d4899f1ed4d139d579174527f6014677d78c4fbb`、merge済みmain
`973c7f44211ad0fc2f87e1d119dcdbf04983a52f`へ固定した。`127.0.0.1`のephemeral portだけへbindする
strict HTTP station、observer worker／NDJSON stream／lifecycle cleanup、detached manifest・archive・全assetを
検証してmemory上から配信するconsumerを実装し、全回帰165件、sdist／wheel build、`git diff --check`がPASSした。
wheel `RECORD`によるmanifest外部pinは合成artifactで検証したが、AGPL共通appはpackageへ同梱していない。
このmain時点ではpublic起動、実artifact配布、automatic browser launch、attach code再発行の外部trigger、
real-browser E2Eは未実装だった。後続branchの到達点は下記delivery unit節で更新する。

schema v1 adapter、b3 catalog／projection／CLI、station contract／runtimeは上記mainへ統合済みである。
引数なしの`mcremote wirescope`はcross-process transport決定まで予約のままです。
AGPLの共通appをwheelへ同梱するときは、PEP 639 metadata、license files、component notice、対応source導線を
配布gateで確認する。consumerはdetached manifestとdeterministic ZIPの双方をwheel `RECORD`でpinし、外側の
manifest hash、archive hash、manifest内archive hashを照合する。dirty checkout由来artifactを正式packageへ
同梱しない。このpackage実装は下記固定branchで合格したが、main mergeと公開releaseは別状態として扱う。
Python追従でMcRemote wire protocol、Bridge、pluginの変更が必要になった場合は、既存schema v1への単純追従として
進めず別の横断決定へ戻す。

Scratchから受領するartifact delivery unitは、bytesとcanonical filenameを変えない
`wirescope-app.zip`／`wirescope-app.manifest.json`のexact 2-file pairである（`2026-08-12-02`）。Pythonは
これを別archiveへ再包装せず、第三のgenerated lock fileも要求しない。両fileを個別package dataとしてwheelへ
収録し、build inputで両hashをpinしたうえでwheel `RECORD`とpackage inventoryを再検証する責務を持つ。
Scratch実装は`09ccd563c93048f8a1d0a3dc1cee2d1f0ffb4681`へ固定済みだが、Python wheelへの実同梱・PEP 639
metadata・license files・notice・exact source導線のdistribution-level実装は、その後
`codex/wirescope-wheel-browser-e2e@8c2360abffe64d3d0b84e2a8b3e1c5da7d25d018`へ固定した。canonical
filename／bytesのまま両fileをpackage dataへ収録し、固定hash／byte数／asset inventory／wheel `RECORD`を
検証する。distributionのPEP 639 license expressionは`MIT AND AGPL-3.0-only`、license filesはMIT本文、
AGPL本文、WireScope NOTICEとし、対応source URLをmetadataへ持つ。全回帰168件、`uv lock --check`、sdist／
wheel build、wheel metadata／license gate、clean wheelからのartifact検証→実loopback station→標準browser
launcher→NDJSON lifecycleがPASSした。top-level URLにsecretを含めず、browser起動失敗時はstationを回収して
Minecraft側をfail openに保つ。

後続のb4 candidate `codex/b4-player-pose@4d510442db58a94f8b249ddcd9d959381f97276c`では、同じ
delivery／launcher基盤に`player.getPose`／`player.setPose`を載せ、candidate wheelをfresh venvへinstallして
automatic browser launch、main stream 1件のWireScope UI操作、origin相対座標、yaw正規化、pitch境界、
`invalid_params`時のpose不変、`mc.close()`後の終了表示までlive-humanでPASSした。全回帰175件と
distribution／license gateもPASSした。正式根拠は
[b4 Python pose／WireScope live-human evidence](../14-evidence/records/2026-08-16-b4-python-pose-wirescope-live-human_ja.md)とする。

この到達点はPython component candidateのPASSであり、main merge、公開release、Scratch common app／
MessageChannel regressionとの横断real-browser E2E、home alpha、rollback実操作は未完である。attach code再発行の
外部triggerも推測実装しない。

## 10. protocol 22／b5とprotocol 23／b6のAPI投影

Python clientはpluginのepoch-scoped event／entity contractを隠さず、Python側だけのqueue、identity、
retry規則を作らない（DECISIONS `2026-08-16-04`〜`07`）。b5はprotocol 22、b6は
`block_right_click`を`pickaxe_poke`へ置換するprotocol 23のcompatibility setとして分ける（`2026-08-26-06`）。

### Event cursor

- connectionごとに一つのcursorを持ち、`events.poll` responseを正常受理した後だけ
  `through_sequence`まで進める。
- `events.poll`は`[after_sequence]`または`[after_sequence,{"max_events":N}]`を使う。Python既定は
  server既定へ委ねられ、利用者が指定した正integerはserver上限を拡張しない希望上限として扱う。
- response喪失時は同じ`after_sequence`で再取得し、destructive dequeueとして実装しない。
- overflow／capacity／明示破棄の累積値を利用者から確認可能にし、event gapを空batchへ畳まない。
- reconnect時はcursor、event cache、entity handleを全て破棄し、旧epochのreplayやhandle再利用を行わない。
- filter採用後も非一致eventをloss扱いせず、serverが返す`through_sequence`と`filtered_out`を正とする。

### Entity handleとretry

handleはopaque stringとして保持し、UUIDへ変換・解析しない。operationごとにserver errorをそのまま投影し、
foreign／unknownをclient側で区別しない。`backpressure`だけを「後で同一要求をretry可能」と説明し、
`work_limit_exceeded`、`entity_capacity_exhausted`、`permission_denied`、`internal_error`を自動retryしない。
特に`world.spawnEntity`のresponse喪失は結果不明であり、重複spawnを避けるため再送しない。

### Wrapperとobserver projection

b5では`events.poll`、`world.getHeight`、`world.spawnParticle`、`world.spawnEntity`を同じwire contractへ
薄く投影する。b6は`pickaxe_poke`とsign三操作、b7はplayer／entityのdirection get／set、b8は
`world.getNearbyEntities`と`entity.getPose`／`setPose`／`remove`を概念別の縦sliceとして追加する。
さらにb7はdamage-capableな`world.strikeLightning`を投影し、旧`world.strikeLightningEffect`は公開しない。
clientは専用rate値をローカル保証として複製せず、`backpressure`を既存の一時拒否として扱い、非冪等な
`internal_error`を自動retryしない。particleのPaper `ParticleBuilder`内部移行はPython surfaceを
変えない。b8はreceiver選択と有限typed particle dataをPythonへ追加し、3D graphのapplication sampleを受入入力に
する。条件付きb9はb8と同じparticle specを使うbounded batchだけを候補とし、単点`FAST`で十分なら追加しない。
Scratchの学習者向けsurfaceは別trackで追従でき、Python実装の完了条件へ含めない。exact Python method signatureと
戻り型は共通wire fixtureとplugin実装を入力に固定し、knowledgeだけからkwargsや独自型を推測しない。

Pythonのb6 surfaceは`codex/b6-protocol23-python@0ba22e80b9b1b339dfd11085b1b24cef646599b2`で
push済み実装candidateになった。protocol／packageを`23.0.0`／`2300.0.0b6`へ上げ、`pickaxe_poke`、
sign三操作、protocol 23の`mcr_eh_` handle検証とobserver／fixture投影を実装した。Scratch ownerの
`sign-v23.json`／`events-v23.json`をexact bytesで配置し、handle suffix長をclient共通contractにせず、
`mceh_`とのaliasは作らない。対象18/18、全242/242件PASSを報告し、三repo共有fixture gateもPASSした。
live-auto／live-human、default branch統合、正式evidence、統合artifact／releaseは未完・未主張である。これはPython component
surfaceの局所実装完了であり、b6 method集合全体の`implemented`／`released`状態への昇格ではない。

後続のdefault branch統合は`main@a30a37b15658da655fe1e3535a73fb0e80c06f56`で完了した。candidateとの
全source tree差分はなく、clean main tarballで242/242件をPASSした。mainから再生成したwheel／sdistも
candidate artifactとbyte-for-byte一致した。これはPython componentの統合完了であり、最終横断artifact set、
公開、b6 releaseの完了を意味しない。

Pythonのb7 surfaceは`codex/b7-python-pass-a@c9e0c19925a56dbcece409982df1b707d41f51ae`で
push済みcomponent candidateになった。protocol／packageは`23.1.0`／`2301.0.0b7`で、公開APIは次のexact shapeを持つ。

- `getDirection() -> tuple[int | float, int | float, int | float]`
- `setDirection(x, y, z) -> tuple[int | float, int | float, int | float]`
- `getEntityDirection(handle: str) -> tuple[int | float, int | float, int | float]`
- `setEntityDirection(handle: str, x, y, z) -> tuple[int | float, int | float, int | float]`
- `strikeLightning(x, y, z) -> None`

`DirectionValue`はimmutableな3要素tupleへdecodeする。serverが返した有限値とnorm toleranceを検証するが、Python側で
再正規化、再丸め、signed zero置換を行わない。入力も有限性と既存の型境界だけを確認してwireへ渡し、zero vectorを
別方向へ補正しない。`zero_direction`、`player_offline`、entity handle lifecycle、permission／build、rate／work、
`internal_error`を含むserver reasonは`McRpcError`で変更せず保持する。`strikeLightningEffect` aliasと新しい自動retry規則は
持たない。

Scratch owner `agent/b7-protocol-owner-fixture@607cda40588ec4579c503d457c3784385419ac65`の
`direction-lightning-v23.1.json` 14,179 bytes／SHA-256
`faad66c93d2c8ee8eb541f6b7297163cb681054b3de05ba3d130ac4288c1046a`をexact bytesで配置し、81 case IDをfixture ledgerとして
消費する。変更coneはwrapper、DirectionValue decoder、protocol negotiation、Python observer projection、deterministic
observer fixture、package metadata、README、starterである。b6 `spawnParticle`、receiver／typed data、sign／event fixture
bytesは変更しない。

担当報告では対象b7／b6／observer 47/47、全252/252、starterのfake roundtrip／direction復元／lightning opt-in、
lint／format／`git diff --check`、`uv lock --check`、sdist／wheel build、wheel metadataをPASSした。local build artifactは
wheel SHA-256 `ec0d032d7c75c14ea804b0a7bca4c723458a1224b8b8b00a4b9b50869f24caf2`、sdist SHA-256
`05547cd1fdbb1a448758c13f5793ae10563a65bee1101da242ebe72cf001d7b2`と報告されたが、durable artifact／公開releaseとは
扱わない。実plugin代表往復、live-auto／live-human、shared deploy、bundled WireScopeのb7 real-browser E2E、tag／releaseは
未実施・未主張である。

後続`codex/b7-permission-contract-followup@8f4bc4b96ae74fb5370a3d804676cd07e5352346`はsuccessor fixture
20,367 bytes／93件をexact再消費し、`mcr.lightning`前提を除去した。targeted 48件、全253件、build／metadataが
PASSし、wheel／sdistはSHA-256 `cc5842b79501fd103f1e7d2e3a4ea1cc72029e6969265591f60c9324338d3094`／
`6be3db058cc1aff7cf5375b58dc11737e5d471f0f67a6cdaa28a869d0c12c236`になった。同commitへ`main`をstrict
fast-forwardし、統合後main再生成物もcandidateとbyte一致した。これによりPython b7 source integrationは完了した。
公開artifact、tag、GitHub release、PyPI公開は未完である。

ただしwire paramsの順序はb5共通fixtureとして先に固定する。`world.spawnParticle`は
`[x,y,z,offset_x,offset_y,offset_z,particle,speed,count,(force)]`、`world.spawnEntity`は
`[x,y,z,entity]`とする。force省略時は`true`である。Python APIを追加するときもparticle-first／
entity-firstのshim、union、自動判定を作らない（DECISIONS `2026-08-21-01`）。

Minecraft由来の連続位置・角度はpluginが正準化したJSON numberをそのまま返す（DECISIONS
`2026-08-19-01`）。Python wrapperは座標3桁、角度2桁へ再roundせず、yawの再wrap、pitchのclampも
行わない。set系は入力精度を保って送信する。block setterは成功時`None`であり、適用後状態の観察には
明示的なget系を使う。
block座標、height、count、sequence等のinteger fieldをfloatから黙って丸めない。

WireScope observer projectionはmethod allowlist、method別params／result validator、plugin fixture、
Scratch adapter、common app artifactと一つのmethod-observation compatibility set v1.1で更新する。
この`v1.1`はcompatibility setの改訂番号であり、observer snapshotのtop-levelは引き続き
`schema_version=1`とする。`schema_version=1.1`や未宣言fieldを生成しない。Python wheelは
exact app artifact versionをpinし、plugin wire conformanceとreal-browser E2Eを別gateとして通す。
