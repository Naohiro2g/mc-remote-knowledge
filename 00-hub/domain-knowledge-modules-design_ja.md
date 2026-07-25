# 設計起案: domain knowledge modules

> 状態: 起案（DECISIONS `2026-07-02-01`）
> 対象: Minecraft / pygame 等の領域知識を、McRemote 固有設計から分離して扱う方式。

---

## 1. 問題

McRemote の knowledge repo には、次の3層が混ざり始めている。

1. knowledge repo の運用規律（DECISIONS、SSOT、投影、agent gate）
2. McRemote 固有の設計（protocol、plugin、Python client、Scratch client、サービス運用）
3. Minecraft の実用常識（世界定数、superflat、block の癖、Paper/Geyser 差、教材で発見した落とし穴）

このまま Minecraft 知識を McRemote 文書へ直接足すと、pygame など他領域へ広げるときに構造が崩れる。逆に、Minecraft 知識を切り出しすぎると、McRemote protocol や教材から参照しにくくなる。

方針は、領域知識を domain knowledge module として扱うこと。

---

## 2. 採用候補の形

将来は、領域ごとに公開リポを分ける。

```text
knowledge-system/          汎用の知識運用・SSOT・投影・agent gate
minecraft-knowledge/       Minecraft の機械可読データと実用ナレッジ
pygame-knowledge/          pygame の機械可読データと実用ナレッジ
mc-remote-knowledge/       McRemote 固有設計。必要な domain repo を submodule で参照
```

利用側では submodule として pinned snapshot を取り込む。

```text
mc-remote-knowledge/
  modules/
    minecraft-knowledge/   # git submodule
    pygame-knowledge/      # 必要になったら追加
```

submodule は普通のサブディレクトリとして読めるため、LLM のローカル参照運用と相性がよい。Git が記録するのは submodule の commit pointer なので、NotebookLM bundle や release gate でも「どの知識 snapshot を読んだか」を固定できる。

短期では、まだ repo を分けず、この文書で形を起案し、最初の実体候補を `world_constants.json` とする。

---

## 3. Minecraft knowledge の収集方針

白紙から「知っていることを書いて」と集める運用は採らない。子どもたちや教材から集めるには、先に seed card が必要。

Minecraft knowledge は次の3層で作る。

| 層 | 役割 | 例 |
| --- | --- | --- |
| 生成・公式寄りデータ | ベースライン。版差・ID・定数の候補を作る | Mojang version manifest、server.jar data generator、Paper API、実機 smoke test |
| OSS 参照データ | 抜け確認・差分比較・seed 作成 | misode/mcmeta、PrismarineJS minecraft-data |
| 実用観察 | 本プロジェクト固有の価値。検索しにくい常識・教材上のつまずき | 子どもたちの発見、授業ログ、教材から抽出した落とし穴、Paper/Geyser/ViaVersion 実機差 |

misode/mcmeta は、Mojang の generated data / assets を version-controlled に扱っており、Minecraft knowledge の seed として使いやすい。ただし Mojang 公式品ではないため、利用時は出典と取得時点を残す。

PrismarineJS minecraft-data は有用な比較・補助ソースだが、主ベースにはしない。README 上は更新と対応版リストが見える一方、一部データの出典・ライセンス caveat があるため、まずは欠損確認・比較・古い版の参考に限定する。

---

## 4. 子どもたちから集めるための seed card

子どもたちに求めるのは分類体系の設計ではなく、観察・再現・言語化。

そのため、投稿単位は自由メモではなく seed card にする。

```json
{
  "id": "mc.world.overworld.superflat.y_sea",
  "topic": "world-constants",
  "question": "スーパーフラットの海面レベルは通常ワールドと同じ意味を持つか",
  "edition": "java",
  "version": "1.21.11",
  "server": "Paper",
  "dimension": "overworld",
  "world_type": "superflat",
  "observed_value": null,
  "how_to_check": [
    "superflat world を作る",
    "水面が自然生成されるか見る",
    "Paper API / McRemote hello の値と照合する"
  ],
  "result": "未検証",
  "notes": ""
}
```

seed card の元は3つ。

- mcmeta 等から抽出した「調べる候補」
- McRemote / Python / Scratch の教材から抽出した「つまずき候補」
- 授業・質問・失敗例から抽出した「実際に迷った候補」

この形なら、子どもたちは「何を見ればよいか」が分かり、知識ベース側は構造化された fact として取り込める。

---

## 5. fact record の最小形

最終的な knowledge は、読み物だけでなく機械可読 fact として残す。

```json
{
  "id": "mc.world.overworld.modern.y_sea",
  "statement": "Java Edition の通常 overworld では、海面を表す情報値は 62 として扱う",
  "edition": "java",
  "version_range": "1.18..1.21.x",
  "dimension": "overworld",
  "world_type": "normal",
  "value": 62,
  "evidence": [
    {
      "type": "smoke-test",
      "target": "Paper 1.21.11",
      "date": "2026-07-01"
    }
  ],
  "source_refs": [],
  "confidence": "verified",
  "license": "own-observation"
}
```

読み物は fact の背景を説明する。機械可読データは、IDE 補完・LLM context・教材生成・protocol/client の実装補助に使う。

---

## 6. `world_constants.json` の位置づけ

`world_constants.json` は、Minecraft domain module の最初の候補 artifact。

McRemote protocol 側で hello に `world_constants` を載せるかどうかは protocol の問題だが、値そのものは Minecraft domain knowledge の問題。ここを分ける。

```text
Minecraft domain:
  world_constants.json の値・根拠・版差・world_type 差を管理する

McRemote protocol:
  hello でどの key / slice を配るかを決める

Python / Scratch client:
  受け取った値や bundled json から IDE 補完・UI 表示・教材表示へ投影する
```

LLM にとっても、`world_constants.json` は検索不要で参照できる project-local context になる。これは VS Code 補完の代替ではなく、同じ SSOT を別の投影先へ配ること。

---

## 7. ライセンスと出典のガード

既存サイトやコミュニティ wiki から、本文・表・画像・説明文をそのまま取り込まない。

扱う単位は次の順に安全側へ寄せる。

1. 自分たちの実機観察・教材観察・smoke test
2. Mojang / Paper 等の公開 API や runtime から抽出できる事実
3. OSS データを seed / 比較に使い、必要な場合だけ license と attribution を確認して取り込む
4. 集約サイトは topic seed と出典リンクに留め、文章や編集済み表現は写さない

子どもたち由来の投稿は、個人情報・サーバー名・座標の実値・チャットログをそのまま保存しない。公開リポ化する場合は、投稿の扱い、保護者同意、ライセンス同意を別途設計する。

---

## 8. pygame への展開

pygame knowledge も同じ形にできる。

- 画面座標・Rect・event loop・clock/tick 等の実用常識
- 初学者が詰まりやすいパターン
- 教材から抽出した seed card
- LLM が検索なしで参照する機械可読 fact / guide

Minecraft 固有の分類を知識運用に混ぜず、domain module の中だけに閉じ込めることで、pygame へ展開しても McRemote 固有設計を汚さない。

---

## 9. 未決事項

- `minecraft-knowledge` をいつ別リポ化するか。
- 短期に `50-domains/` をこの repo 内に作るか、別リポ化まで設計文書だけに留めるか。
- `world_constants.json` の正式置き場と schema。
- 子どもたちからの投稿フォーム、匿名化、公開時の license / consent。
- mcmeta を submodule / fetch script / seed snapshot のどの形で参照するか。
- pygame knowledge の最初の seed card。
