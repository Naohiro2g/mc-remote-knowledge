# catalog block tag設計

> 状態: 採用（`2026-09-30-08`）。実装は初回stable後。exact条項は実装に入るときにwire §7.2.1へ書く。
>
> 出典: scratch-editor確定搬送票2と添付の仕様案・担当別作業案（`agent/b8-compatibility@5aaa9c59acc393cd0a0de5cb45a5e619a5e87abe`、
> `handoff-materials/2026-09-30-catalog-list-and-block-tags/`、git管理外）。素材が初回stable後まで残る保証が無いので、
> 中身をこの文書へ移した。

## 1. 利用者ができること

「丸太に属するブロックIDを集める」「datapackの建材グループから順番に選ぶ」を、Scratchのリスト操作（反復、検索、
ランダム選択）につなげる。ブロックは複数のタグに所属できる。分類名は`minecraft:logs`などのタグIDを使い、
各Minecraft版・サーバーのdatapackにある所属を配送する。

クリエイティブインベントリーのタブ名・表示順・アイコン・日本語分類名は対象外。タグには`minecraft:mineable/axe`
など機能上の分類も含まれるため、画面上の教材向け分類が要るときは別の投影として扱う。

b8に入れるカタログのID一覧ブロック（`13-scratch-client/scratch-roadmap_ja.md`）とは独立した、McRemoteのproducerと
各clientにまたがる拡張である。

## 2. wire shape

既存`catalog.get`の各`block[blockId]`に、追加field `tags: string[]`を置く。top-levelの`block`／`entity`／`particle`と
既存`states`／`default_state`、methodとparams `[]`は変えない。次の例はshapeの説明用で、実サーバーの所属全体を
表すものではない。

```json
{
  "catalogHash": "<本体から算出したSHA-256>",
  "block": {
    "minecraft:oak_log": {
      "states": {"axis": ["x", "y", "z"]},
      "default_state": {"axis": "y"},
      "tags": ["minecraft:logs", "minecraft:oak_logs", "school:building_materials"]
    },
    "school:untagged_block": {
      "states": {},
      "default_state": {},
      "tags": []
    }
  },
  "entity": {},
  "particle": {}
}
```

- タグに対応したproducerは、**すべてのblock entry**に`tags`を付ける。所属の無いブロックも`[]`を付ける
- タグIDは完全修飾の`namespace:path`で、`#`を付けない。入力側の補い方はwire §5.0.2（`2026-09-30-06`）に従う
- 配列は重複なし、文字列の辞書順。ASCIIのIDなので言語固有のlocale順は使わない
- 値は「catalogを作った時点で、そのブロックが所属するブロックタグの集合」。block stateによる所属の分岐は設けない
- vanillaに加え、ロード済みdatapackのnamespaceも配送する。タグ参照を含むdatapackの生JSONは配送せず、サーバーが
  解決した所属を使う
- itemタグ、entityタグ、particleの分類は対象外

## 3. 取得元と生成

Paper 1.21.11では`Bukkit.getTags(Tag.REGISTRY_BLOCKS, Material.class)`でサーバーに定義されたブロックタグを列挙できる。
各タグの`getKey()`と`getValues()`を読み、既存のblock mapのIDへ所属を足す
（[Bukkit公式API](https://jd.papermc.io/paper/1.21.11/org/bukkit/Bukkit.html#getTags(java.lang.String,java.lang.Class))、
[Tag公式API](https://jd.papermc.io/paper/1.21.11/org/bukkit/Tag.html#getValues())）。

タグごとの要素を一度ずつ走査し、ブロック→タグへ反転する。全block entryの空配列を先に作り、所属を足してから重複を
除いて並べる。タグの値が既存のblock mapに無い場合は配送対象から除き、producerの検証で差を確認する。タグの取得に
失敗した状態を「所属なし」の`[]`として出さない。snapshotの生成に失敗したら、既存のcatalog取得失敗と同じ扱いにする。

このAPIで1.21.11／26.xのcustomタグ・タグ参照・reloadが実際にどう反映されるかは、McRemote側の実機確認事項である。
APIの確認をlive PASSとして扱わない。

## 4. 互換性とcache

現行のwire §7.2.1は、block entryの未知の追加fieldを許し、hashの対象を`block`／`entity`／`particle`の3 mapの全内容と
している。`tags`をblock entryの下へ置けば、既存のhash algorithmのままで所属の変更がhashへ反映される。**配列はhashの
処理でsortされない**ので、producerでIDの順を固定する。

対応前のcatalogでは、`tags`を省略した形を引き続き受ける。省略は「タグ情報を提供していない」、`[]`は「タグ情報は
提供済みで、所属なし」であり、clientは両者を区別する。

- 全entryで省略: 従来のcatalog。ID一覧や建築は使える。タグの操作は「接続先がタグ情報を提供していません」と案内し、
  出力リストを保持する
- 全entryで正しい配列: タグの操作を使える
- 一部だけ省略、`null`、重複、無効なID、順の違反: 拡張に対応したclientは`invalid_catalog`として扱う案。旧clientは
  未知fieldとして従来どおり扱う
- block mapが空: 所属の一覧は空で、タグに対応しているかはこのshapeからは判定できない。対応を推定した表示はしない

IndexedDB等には追加fieldを含む本体を保存し、helloで広告されたhashと一致した後だけ使う。オフライン用のcatalogや
固定のタグ表は同梱しない。Pythonの投影にタグを足す場合は、既存のgenerator／projection schemaの版を上げる。

## 5. 生成と更新の範囲

registryとdatapackのロード完了後に、タグを含むcatalogのsnapshotを作る。サーバーの稼働中は同じ本体とhashを使い、
helloと後続の`catalog.get`を一致させる。タグ配列はPaperの可変なregistryへの参照を持たず、snapshotの値としてコピーする。

datapackを変えたら**サーバーの再起動でcatalogを更新**し、Scratchも接続し直してhelloのhashで再検証する。稼働中の
datapack reloadやScratchの再接続だけではタグのcatalogは更新しない。コピー済みのScratchのリストも自動では更新しない。

再起動の後に所属が変われば、hashも変わる。内容が同じなら同じhashになる。広告済みのhashのまま本体だけ差し替える
実装は採らない。稼働中のreload、connection epochごとの新旧snapshotの保持、新しいpush通知・RPCは後続の起案とする。

## 6. Scratchへの投影

| ブロック | 結果 |
| --- | --- |
| カタログの［ブロックタグ］を［リスト］に入れる | 各block entryの`tags`の和集合を、重複なし・辞書順でコピーする。b8のID一覧ブロックのメニューを広げる |
| ブロックID［ID］のタグを［リスト］に入れる | そのブロックの`tags`をコピーする |
| タグ［TAG］のブロックIDを［リスト］に入れる | そのタグに所属するblock IDを辞書順でコピーする |

- どの操作もCURRENTのcatalogだけを使い、追加の通信なしで出力リスト全体を置き換える。取得中は既存の取得の完了を待つ
- 切断、接続の切り替え、未提供、不正な入力では、元のリストを保持して案内する
- IDとTAGは文字列入力・変数・reporterを受ける。TAGは`#`なし。補い方はwire §5.0.2。IDやタグIDは翻訳しない
- 逆引きのindexはclient内で導き、wireで二重に配送しない
- このshapeでは、所属ブロックがゼロのタグは現れない。タグの一覧は「catalogのブロックが所属するタグ」の一覧で、
  サーバーの全定義タグの一覧とは呼ばない。正しい形式のTAGに所属が無ければ空リスト。未知のブロックIDは入力エラーとして
  リストを保持する
- 英語・日本語・ひらがなを用意する
- 所属ブロックの無いタグの存在を確かめる必要が出たら、定義タグの一覧の独立した配送を別に起案する

## 7. shared fixture

形と規則を合成データで固定する。特定のMC版のvanillaタグの一覧を正本として固定しない。実際のタグの値の正本は
live producerである。

- case案: TAG-C01旧shape、02全件tags、03複数所属、04空配列、05customタグ、06部分提供、07重複、08無効ID、09未整列、
  10所属だけ変えたhash、11同じ集合の生成順差、12 hello／本体のhash不一致。空block mapの扱いも足す
- file名とschema名（Scratch案は`catalog-block-tags-vNEXT.json`、`mcremote.catalog-block-tags.vNEXT`）とcaseのkeyは、
  実装に入るときに版と合わせて決める

## 8. 担当別の作業案（実装に入るときに渡す）

### McRemote（producer）

1. registryとdatapackのロード完了後に、Paperのブロックタグを列挙する。既存adapterと生成タイミングの適合を確かめる
2. 全block entryに`tags`を付ける。取得失敗を空配列に置き換えない
3. vanillaとロード済みdatapackの、サーバーが解決した所属を配送する
4. タグIDを完全修飾で`#`なしにし、重複を除いて辞書順に固定する。既存のblock mapに無いブロックは除く
5. 配列を含む本体をsnapshotとして保持する
6. 現行のhash algorithmで、タグを含む3 map全体をhash化し、helloの広告と`catalog.get`の本体を一致させる
7. 稼働中のreloadでは本体を更新しない。再起動の後に所属だけ変わった場合もhashが変わることを確かめる

受け入れの目安: 複数所属、未所属、custom namespace、解決済みの所属、完全な配列、重複除去と並び、生成順が違っても
同じhash、所属の変更でhashが変わること、helloと本体の一致をunitで確かめる。shared fixtureのconsumer testを足す。
liveはcustom datapackを含む所属、タグ参照の解決、変更後の再起動でのhashの差を見る。工数の目安は3〜5時間。

### Scratch（validatorと学習面）

- validatorに`tags`の受理規則（§4）を足す
- §6の3つの操作を足す（ID一覧ブロックのメニュー拡張と、command 2つ）。引数LISTは既存の`ArgumentType.LIST`を使う
- 和集合と逆引きindexはCURRENTの本体から導き、接続の境界で無効にして新しいcatalogで作り直す
- 英語・日本語・ひらがなの案内を足す

受け入れの目安: 3操作、辞書順と重複なし、空集合、複数所属、namespaceの補い、不正ID、catalog配列との分離、選んだ
リストの一括置換、追加RPCなしをunitで確かめる。cacheのhit、取得待ち、取得失敗、接続世代の変更、未提供と空配列の区別、
空block map、snapshot変更後の新しいhashも見る。工数の目安はScratch投影4〜6時間、fixtureとconsumer test 3〜5時間。

全体の工数の見込みは12〜20時間（Scratch担当の概算）。

## 9. 実装に入るときに決めること

- protocolのversion（追加fieldの互換性とminorの要否）とartifactのidentity
- `invalid_catalog`の受理規則をwireへどう書くか
- shared fixtureのownerとfile名。b9でProtocol／fixtureのownerがScratchから移る（`2026-09-30-03`）ので、実装時点の
  ownerが発行する
- 各担当の分担の最終形
