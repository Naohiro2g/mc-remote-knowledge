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
- build state：各connection／streamが持つworldとorigin。
- project設定：`param_mc_remote.py` が持つ接続先と初期 `BUILD_ORIGIN`。

`1 Minecraft instance = 1 connection = 1 build state`です。`setPlayer()` は削除され、次を使います。

```python
mc.setWorld("overworld")
mc.setBuildOrigin(ORIGIN.x, ORIGIN.y, ORIGIN.z)
```

建築座標はorigin相対で、絶対座標は `origin + relative` です。Y座標にも暗黙offsetはありません。`setWorld()` と `setBuildOrigin()` はsession中に変更できます。

b3の主要APIは次のとおりです。

| Python API | 役割 |
| --- | --- |
| `postToChat(message)` | chatへ投稿 |
| `setBlock(x, y, z, ref)` | ブロックを1個設置 |
| `setBlocks(x0, y0, z0, x1, y1, z1, ref)` | 直方体を設置 |
| `getBlock(x, y, z)` | canonical-fullなblock stateを取得 |
| `setWorld(world)` | このstreamのbuild worldを変更 |
| `setBuildOrigin(x, y, z)` | このstreamのoriginを変更 |
| `getPos()` | paired playerのworldとorigin相対位置を取得 |
| `setPos(world, x, y, z)` | paired playerを明示worldのorigin相対位置へ移動 |

state付きblock refは文字列で直接書くか、client-side helperを使えます。

```python
from mc_remote.catalog import block_ref

mc.setBlock(0, 0, 0, block_ref("oak_log", axis="z"))
```

## 6. catalog／projectionの失敗

`Minecraft.create()` による自動projectionはbest-effortです。fetch、validate、cache、generate、publish等で失敗すると `CatalogProjectionWarning` を出しますが、認証済みbuild streamは維持し、接続済みclientを返します。

warningには失敗stage、接続と建築は成功していること、補完だけが更新されなかったこと、再試行方法が含まれます。token、pair code、credential内容は含めません。

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

token、pair code、player UUIDをsource、URL、通常log、Git管理fileへ書かないでください。`param_mc_remote.py` にcredentialを置かないでください。

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
- `streams[].hello` は初期 handshake の記録です。`hello.world`／`hello.origin` を後続の
  `build.setWorld`／`build.setOrigin` による現在値で上書きしません。現在の可変 build state は
  schema v1へ未宣言 fieldとして追加せず、次の schema sliceで `current_build_state` と lifecycle／fixtureを
  共に固定してから追従します。現在値を得るためだけの25ms pollingも行いません。
- adapter は Scratch lifecycle fixture と schema validator に対する conformance を満たし、
  generation-side allowlist で hello、permissions、world constants と許可された建築／world／player
  frame・payloadだけを生成します。任意の Python object、無制限な履歴、内部 transport 状態を
  observer feedへ直列化しません。
- `auth.*`、token、pair code、player UUID、credential／device情報を生成せず、history、grant、
  observer sessionをproject fileやcredential storeへ永続化しません。observerへ認証・操作権限も
  渡しません。

共通appとの接続は[WireScope deployment設計](../15-wirescope/wirescope-deployment-design_ja.md)と
[station attach設計](../15-wirescope/wirescope-station-attach-design_ja.md)に従います（`2026-08-10-02`、
`2026-08-11-02`／`2026-08-11-03`）。最初に実装するのはsource／station／browserが同じnetwork namespaceに
あるbrowser-loopback profileだけです。station roleをsource processへ融合し、`127.0.0.1`のephemeral portで
共通appを提供します。UDS、named pipe、cross-process relay、LAN、VPSを初期sliceへ含めません。

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
79件、全回帰159件、`uv lock --check`、sdist／wheel build、`git diff --check`がPASSした。これはcodecと
fixture境界の到達点であり、実loopback HTTP server、attach code再発行trigger、browser起動、real-browser E2Eは
未実装である。

schema v1 adapterとconformance fixtureは合格済みですが、current mainとconformance branchはdivergeしています。
observerだけを移植せず、b3 catalog／projection／CLI／adapter一式をcurrent mainへ統合し、全test済みの新しい
固定SHAを実装起点とします。引数なしの`mcremote wirescope`はcross-process transport決定まで予約のままです。
AGPLの共通appをwheelへ同梱する前にPEP 639 metadata、license files、component notice、対応source導線を配布
gateで確認します。consumerはdetached manifestとdeterministic ZIPの双方をwheel `RECORD`でpinし、外側の
manifest hash、archive hash、manifest内archive hashを照合します。dirty checkout由来artifactを正式packageへ
同梱しません。Python追従でMcRemote wire protocol、Bridge、pluginの変更が必要になった場合は、既存schema v1への
単純追従として進めず別の横断決定へ戻します。
