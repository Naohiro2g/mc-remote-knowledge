# Minecraft dimension key 設計

> 現行正本：protocol 22.0.0／artifact 2200.0.0b5以後
> 拘束層：DECISIONS `2026-08-22-02`、[wire format](wire-format-design_ja.md)
> protocol 21／b4以前のBukkit world name契約とは互換にしない。

## 1. 一つのidentity

McRemoteが建築先、player位置、event発生先、entity所在先をwireへ出すとき、そのidentityは
Minecraft dimension keyとする。Bukkit world folder名や`World#getName()`をwire identityに使わない。

```text
DimensionKey = namespace:path
```

例：

```text
minecraft:overworld
minecraft:the_nether
minecraft:the_end
myworld:world
myplugin:moon
```

出力は常にnamespaceを含む完全修飾形である。pluginは`World#getKey().toString()`を一度だけ正準化の
ownerとし、Python、Scratch、WireScopeは受信値を短縮・別名化しない。

## 2. 入力と解決

入力の`DimensionRef`は完全修飾DimensionKey、または`minecraft` namespaceだけを省略したpathである。

```text
overworld             -> minecraft:overworld
the_nether            -> minecraft:the_nether
the_end               -> minecraft:the_end
minecraft:overworld   -> minecraft:overworld
myworld:world         -> myworld:world
```

namespaceを省略した入力へだけ`minecraft:`を補う。case変換、trim、Environment走査、folder名検索、
最初に見つかったworldへのfallbackは行わない。`world`、`normal`、`nether`、`end`を標準dimensionの
aliasとして扱わない。例えば`world`は`minecraft:world`というkeyとしてだけ解釈され、
`minecraft:overworld`へ読み替えない。

pluginは構文検証後に`Bukkit.getWorld(NamespacedKey)`でloaded dimensionを解決する。解決できないkeyは
`unknown_dimension`とし、error dataで入力全体を反射せず、安全に特定できる場合だけ`data.dimension`
へDimensionRefを置ける。

既定dimensionは`minecraft:overworld`であり、`Bukkit.getWorld("world")`やloaded world一覧の先頭へ
fallbackしない。

## 3. wire vocabulary

dimension identityを運ぶ公開語彙は`dimension`へ統一する。

| surface | protocol 22の現行形 |
| --- | --- |
| build setter | `build.setDimension [dimension_ref]` |
| hello request | `build.dimension` |
| hello result | `dimension` |
| build setter result | `{dimension, origin}` |
| player position／pose | params／resultの`dimension` |
| event DTO | `dimension` |
| b6 entity pose | params／resultの`dimension` |
| 解決失敗 | `unknown_dimension` |
| entity外部移動 | `entity_dimension_changed` |

`build.setDimension`と`build.setOrigin`は、成功時にserver正準値による同じbuild contextを返す。

```json
{
  "dimension": "minecraft:overworld",
  "origin": [200, 0, 200]
}
```

clientはsetter入力を現在値として保存せず、認証済みhelloまたは成功resultをstrictに検証した後だけ、
connection／streamの現在dimensionとoriginを一体更新する。失敗、不正shape、結果不明では以前のcontextを
維持する。event context guardもserver由来のDimensionKeyとcapture済みoriginだけを比較する。

## 4. surface投影

### McRemote

- DimensionRefを共通codecで一度だけparse／resolveする。
- `Bukkit.getWorld(NamespacedKey)`を使い、`Bukkit.getWorld(String)`をこのAPI経路で使わない。
- hello、build result、player result、event DTO、entity resultは`World#getKey()`を出力する。
- right-click相関とentity handle registryの内部所在比較もDimensionKeyで行う。

### Python

- 公開APIは`setDimension()`とし、`setWorld()`を残さない。
- `_dimension`はhello／build resultだけから更新する。
- position、pose、event、context mismatchのfield／属性名を`dimension`へ統一する。
- 任意namespaceを保持できるstringとして扱い、標準3dimensionのclient allowlistを作らない。

### Scratch

- commandは「建築する次元を [DIMENSION] にする」とし、opcode／wireは`build.setDimension`を使う。
- 初期menuは標準3dimensionを提示できるが、plugin wireの許容集合をmenuへ閉じない。
- menuのmachine valueは`overworld`／`the_nether`／`the_end`、server由来値は完全修飾形で保持する。
- event／player reporterのpropertyは`dimension`へ揃える。

### WireScope

- raw requestのDimensionRefを再配列・短縮しない。
- hello、result、eventのDimensionKeyは完全修飾grammarを検証する。
- `build.setDimension`／`build.setOrigin`のbuild context resultを同じvalidatorで扱う。
- observer schema top-levelはversion `1`、compatibility set revisionは`v1.1`のままとする。

## 5. `world`として残すもの

次はdimension identityではないため改名しない。

- `world.setBlock`等、Minecraft worldへ作用するmethod namespace
- Javaの`org.bukkit.World`型と実装内の通常の局所変数
- Minecraft worldの保存directory、volume、backup、lineage
- Stack／backstageのdeployment上のworld identity
- `world_constants`。これは選択中world／profileの情報定数bucketで、identity fieldではない

この区別により、「保存対象としてのworld」と「wire上のdimension identity」を同じ文字列規則へ
誤って束縛しない。

## 6. protocol 21／b4以前

protocol 21のb4 prerelease、evidence、当時の`build.setWorld`、`world` field、短縮値は履歴として保持する。
protocol 22では次を作らない。

- `build.setWorld` alias
- `setWorld()` wrapper
- `world`／`dimension` union field
- Bukkit world nameとDimensionKeyの自動判定
- `world`／`normal`／`nether`／`end` alias
- `.sb3`／Python作品migration

protocol 22の最初のexact compatibility setがGREENになる前の全面改訂であり、b4以前との相互運用を
設計条件にしない。

## 7. fixture

最低限、次をplugin／Python／Scratch／WireScopeの共通fixtureへ置く。

1. namespace省略の`overworld`を`minecraft:overworld`へ正準化
2. 完全修飾`minecraft:the_nether`／`minecraft:the_end`
3. loaded custom key `myworld:world`
4. unloaded keyの`unknown_dimension`
5. `world`／`normal`／`nether`／`end`をaliasにしない
6. 大文字、空白、malformed keyの`invalid_params`
7. default dimensionがexact `minecraft:overworld`
8. hello、両build setter、player position／pose、3 eventの完全修飾出力
9. build setter成功resultによるcontext一体更新
10. setter失敗／不正resultでclient context不変
11. actual eventのsame-context guard成功と、dimension／origin変更後のguard失敗
12. entity handleのdimension移動判定
13. WireScopeがrequestの短縮入力とresponseの完全修飾出力をそのまま観察
