# ブロック値・状態・多言語投影設計

## 1. この設計が決めること

McRemote protocol 22.0.0では、Minecraftのブロックを一体化した文字列ではなく、
`block_id`と`state`を分けた構造として扱う。

```json
{
  "block_id": "minecraft:oak_log",
  "state": {
    "axis": "z"
  }
}
```

この形をplugin、Python、Scratch、WireScope、将来の他言語clientが共有する。利用者が
`oak_log[axis=z]`を組み立てたり分解したりすることを、共通APIの前提にしない。

分離する理由は三つある。

1. `gold_block`のようにstate propertyを持たないブロックがある。
2. IDとstateは意味が異なり、検索、翻訳、補完、検証、文字列操作の前に分かれている方がよい。
3. Scratchだけへ文字列の合成・分解を負わせず、各言語が同じschemaとfixtureを使える。

本書は人間向けの説明正本である。JSON-RPCの厳密なmethod／error契約は
[wire-format-design](wire-format-design_ja.md)、版境界は
[versioning-design](versioning-design_ja.md)を正とする（決定`2026-08-19-02`／`03`）。

## 2. 一つの形、二つの役割

set入力を`BlockSpec`、get出力を`BlockValue`と呼ぶ。両者は同じcontainer shapeを持ち、
stateの完全性だけが異なる。

```text
BlockSpec  = { block_id: string, state: object }
BlockValue = { block_id: string, state: object }
```

- `BlockSpec.block_id`はvanillaの短縮IDを受理する。非vanillaは完全修飾IDを使う。
- `BlockSpec.state`は部分指定を受理する。空objectはMinecraftの既定stateを使う。
- `BlockValue.block_id`は常に完全修飾IDで返す。
- `BlockValue.state`はそのブロックが持つ全propertyを返す。
- 最上位fieldは`block_id`と`state`の2つを必須とし、欠落fieldと未知fieldは`invalid_params`にする。
- stateのkeyはcatalog／registryのproperty名、valueはboolean／number／stringのJSON scalarに限る。

state propertyを持たないブロックも、`state`を欠落、`null`、空文字にせず、空objectへ
正規化する。

```json
{
  "block_id": "minecraft:gold_block",
  "state": {}
}
```

これにより、各言語はfieldの有無で分岐せず、常にobjectとしてstateを扱える。

## 3. setの意味

`world.setBlock`は座標と`BlockSpec`を受け取る。

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "world.setBlock",
  "params": [
    0,
    0,
    0,
    {
      "block_id": "oak_log",
      "state": {
        "axis": "z"
      }
    }
  ]
}
```

`world.setBlocks`も末尾に同じ`BlockSpec`を置く。

```json
{
  "jsonrpc": "2.0",
  "id": 2,
  "method": "world.setBlocks",
  "params": [
    0,
    0,
    0,
    9,
    9,
    9,
    {
      "block_id": "gold_block",
      "state": {}
    }
  ]
}
```

空のstateは、既に置かれているブロックのstateとのmergeではない。指定したblock IDから、
Minecraftの既定stateを使った新しいblock dataを作る。部分stateも同様に、指定しなかった
propertyをMinecraftの既定値で補う。

id付き`world.setBlock`／`world.setBlocks`の成功resultは`null`とする。idなしnotificationはresponseを
返さない。setterは副作用command、getterは観察queryとして分離し、適用後の状態が必要なら
`world.getBlock`／`world.getBlocks`を明示的に呼ぶ（決定`2026-08-20-03`）。

これは`2026-08-19-03`が却下した`null`を明示的に改訂する。当時はsetが常にid付きrequestで、set成功、get、
eventを`BlockValue`へ揃える利点があった。DEBUG／TRACE／FAST導入後はFASTがresponse自体を持たず、同期modeだけ
`BlockValue`を返すとclient setterの戻り型がmode依存になる。全modeの公開setterを値なしへ揃え、観察をgetへ
分ける利益が、set成功値の共通codecより上回る。

stateを持たないblockの`state:{}`は`BlockSpec`／`BlockValue`内の型不変条件であり、値を返さないcommandの
`result:null`と衝突しない。意味のない将来予約`{}`、入力echo、`{applied:N}`を成功resultにしない。

## 4. getの意味

`world.getBlock`は一つの`BlockValue`を返す。

```json
{
  "jsonrpc": "2.0",
  "id": 3,
  "result": {
    "block_id": "minecraft:oak_log",
    "state": {
      "axis": "z"
    }
  }
}
```

getとsetを同じ構造にすることで、読み取った値を別座標へ渡せる。入力側は短縮IDと部分stateを
受け入れ、出力側は完全修飾IDとfull stateを返す。既存の「入力は寛容、出力は正準」という
原則は維持する。

JSON objectのmember順序に意味はない。fixtureやScratch内部tokenのdeterministic serializationでは、
最上位を`block_id`、`state`の順、state propertyを名前の昇順で出力する。

`world.getBlocks`は複数座標を有界に読むmethodである。6個のorigin相対integer座標を受け、
各軸をmin／maxへ正規化し、両端を含む領域をx外側・y中間・z内側（z最速）の昇順で走査する。
resultは同じ順序の`BlockValue` arrayで、座標を各要素へ重複収録しない。各軸のinclusive長は10以下、
全体は最大1000件とする。一軸でも上限を超えればworld走査前に`work_limit_exceeded`、shape／integer
違反は`invalid_params`とする。

旧`world.getBlockWithData`はfull-state `world.getBlock`に包含されるためprotocol 22で廃止し、
`method_not_found`とする。

## 5. 検証とerror

構造やJSON型が不正な場合は`invalid_params`とする。文字列refの構文解析が無くなるため、
`malformed_ref`はprotocol 22では使用しない。

| reason | 意味 | 主なdata |
| --- | --- | --- |
| `invalid_params` | object shape、field、JSON型、座標等が不正 | `path`を出せる場合は原因fieldを示す |
| `unknown_block` | 補完後のblock IDがregistryに無い | `block_id` |
| `unknown_property` | blockに存在しないstate property | `block_id`, `property` |
| `invalid_property_value` | property値が許容外 | `block_id`, `property`, `value`, `allowed` |

原因fieldを特定できる`invalid_params`は、任意の`data.path`を返せる。pathは`params`をrootとし、
array indexを`[n]`、object fieldを`.name`で連結する（例`params[3].state.axis`）。pathで表現できない
入力や原因fieldが一つに定まらない場合は省略し、入力全体を文字列化して代用しない。

catalogのJSON numberは十進数値としてscale非依存で比較する。`3`、`3.0`、`3e0`は同じnumberであり、
string`"3"`とは異なる。出力はMinecraft registryの正準型に戻し、整数stateはJSON integerとして返す。

最終受理はserver registryを読むpluginが所有する。clientのresource catalog検証は入力支援であり、
server validationの代替ではない。

## 6. Pythonへの投影

Pythonの公開入力は`block_id`と`state`を分ける。

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

```python
def setBlock(
    x: int,
    y: int,
    z: int,
    block_id: str,
    *,
    state: Mapping[str, str | int | bool] | None = None,
) -> None:
    ...
```

API上の`None`は送信前に空objectへ正規化する。state propertyを`**kwargs`だけで受ける形は、
Python identifierにできないmod propertyや将来のoption名との衝突を避けるため、主APIにしない。

`getBlock()`はimmutableな`BlockValue`を返す。

```python
value = mc.getBlock(0, 0, 0)

print(value.block_id)
print(value.state)
print(value.state.get("axis"))
```

`setBlock()`／`setBlocks()`はDEBUG／TRACE／FASTの全modeで`None`を返す。`getBlocks()`はwire順序を保つ
immutableな`BlockValue` sequenceを返す。Pythonは各要素へ座標を捏造せず、呼出し側が入力領域と
規定のz最速順から対応を導く。

公開helperとしての`block_ref()`はprotocol 22の正準APIに含めない。protocol 21のコードには、
恒久shimでなく現行記法への書き換え例を提供する。

## 7. Scratchへの投影

Scratchはrecordを第一級値として持たないため、通信と表示を分ける。一回の通信でブロック情報を
snapshotとして取得し、専用reporterがfieldを取り出す。

```text
([x] [y] [z] のブロック情報)

([ブロック情報] のブロックID)

([ブロック情報] の状態 [property])
```

利用例は次のとおり。

```text
[調べたブロック v] を ([0] [0] [0] のブロック情報) にする

もし <([調べたブロック] のブロックID) = [minecraft:oak_log]> なら
  ([調べたブロック] の状態 [axis]) と言う
end
```

`ブロック情報`は同じ観察時点のIDとstateを持つimmutable snapshotである。ID用とstate用に
別々の`world.getBlock`を送らない。Scratch-visibleなStateText／BlockInfoText、予約ErrorText、
Pickerと多言語表示の詳細は
[Scratch block value投影設計](../13-scratch-client/scratch-block-value-projection-design_ja.md)を正とする
（決定`2026-08-19-04`）。これらの文字列をwireやPythonへ逆流させない。

### 7.1 スプライトごとの利用

reporter定義は全targetで共通だが、呼出しと保存はScratchのtarget／thread規則に従う。

- 取得結果を「このスプライトのみ」の変数へ保存できる。
- extension全体で共有する「最後のブロック情報」を作らない。
- Stageのグローバル変数へ入れた場合だけ、利用者の明示操作として共有する。
- cloneはScratchの通常のsprite-local variable複製規則に従う。
- block valueへsprite ID、stream ID、credential、capabilityを埋め込まない。

b4では各spriteからのcommandは同じmain streamを使う。将来spriteをsubstreamへ写像する場合も、
呼出元`target`からtransportを選ぶだけで、block valueのshapeとreporter面を変更しない。

通信reporterをmonitor表示する場合はthrottleと同一引数のin-flight coalescingを持たせる。
明示的なscript callは毎回実行し、disconnect時にcacheを破棄する。

## 8. ID、表示名、検索

`gold_block`、`axis`、`north`等はmachine tokenであり、自然言語の英語表示名とは別である。
wire値は翻訳しない。日本語と英語はresource catalogから導く表示・検索metadataとして扱う。

```text
金ブロック / Gold Block / gold_block
オークの原木 / Oak Log / oak_log
軸 / Axis / axis
縦方向 / Y axis / y
```

Pickerは日本語表示名、英語表示名、canonical ID、登録済みaliasを正規化し、空白区切りの
AND検索を行う。選択後に保存・送信するのは`block_id`とmachine state valueであり、日本語名を
wireへ送らない。

初学者向け教材は、`gold_block`、`iron_block`、`diamond_block`、`sea_lantern`等、輪郭や個数を
確認しやすくstate propertyを持たないblockから始める。教材の対比表は日本語名、表示用英語名、
canonical ID、Python定数を並べる。state editorは必要になるまで詳細面へ置く。

## 9. 共通fixtureと実装gate

各実装は、同じ機械可読fixtureを固定hashで照合する。最低限、次を含める。

1. state propertyを持たないblockの`state: {}`
2. stateful blockへの空state入力とdefault補完
3. 部分state入力とfull state出力
4. boolean、number、stringのJSON native型
5. vanilla短縮ID入力と完全修飾出力
6. non-vanilla完全修飾ID
7. `invalid_params`、`unknown_block`、`unknown_property`、`invalid_property_value`
8. set→getの意味的round-trip
9. set成功result、event内block、scale非依存number、`data.path`
10. bounded `getBlocks`の順序／反転端点／軸・総数上限と`getBlockWithData`拒否
11. Scratch block information tokenとaccessor
12. sprite-local保存、並行thread、clone、disconnect時cache回収

plugin fixture、Python codec／API、Scratch codec／block、WireScope method validator、教材例を一つの
compatibility setとして更新する。片側だけで旧文字列と新objectを混在させない。

## 10. version境界と移行

構造化block valueはprotocol `22.0.0`で導入する。protocol `21.0.0`のb4 artifactは文字列
`block_state_ref`を使う当時の事実として残す。

| scope | protocol | artifact |
| --- | --- | --- |
| b4 | `21.0.0` | `2100.0.0b4` |
| b5 | `22.0.0` | `2200.0.0b5` |
| b6 | `22.0.0` | `2200.0.0b6` |

protocol 21 clientとprotocol 22 plugin、またはその逆はhelloで`protocol_mismatch`として拒否する。
旧文字列refのin-band互換受付、新旧を自動判定するunion schema、恒久的な`block_ref()` shimは設けない。
利用者が保存したコードには、現行正準記法への書き換え方法を提供する。

## 11. 採用しない形

- `oak_log[axis=z]`を公開block valueとして維持する。
- `state`なしを言語ごとの`null`、field欠落、空文字で表す。
- setだけ構造化し、getは一体文字列のままにする。
- `world.getBlockId`と`world.getBlockState`を別wire methodにする。
- ScratchでIDとstateを別々の通信reporterから取得する。
- extension全体で共有する「最後のブロック情報」を作る。
- 日本語表示名をblock IDやstate valueとして送る。
- protocol 21と22のshapeを同じprotocol番号の下で混在させる。
- `world.getBlocks`をcomma区切り文字列、無制限領域、端点入力順依存で返す。
- full-state `world.getBlock`と重複する`world.getBlockWithData` aliasを残す。
- DEBUG／TRACEだけsetterから`BlockValue`を返し、公開戻り型をmode依存にする。
- FAST notificationへsyntheticな成功responseを作る。
- set成功に意味のない空object、入力echo、自明または部分成功を誤解させる`{applied:N}`を返す。
