# LLM agent 境界ガイド（権限・実行能力・検証能力）

## 1. 三種類の境界

```text
権限境界:       してよいか。credential、書き込み先、外部作用。
実行能力境界:   できるか。tool、environment、実行手段。
検証能力境界:   確かめられるか。test、再現、比較、照合。
```

これらを人や model 名へ固定しない。「主体 × テーマ × 現在地 × 作業 × 利用可能な道具」ごとに観測する。自己申告や自信でなく、成果物と反証可能な test で判定する（`2026-07-19-05`）。

## 2. 作業領域

```text
public knowledge repo:
  判断理由、横断決定、現行 contract、sanitized evidence。

dev repos:
  実装、test、release 作業。

private backstage:
  provider / account / cost / inventory / internal ops。

Git 外:
  token、password、private key、秘密を含む raw log。
```

repo は共同作業場であり、credential store ではない。private repo であっても秘密実値を commit しない。

## 3. Repository write

agent は依頼された repo / path だけを編集する。同じ GitHub credential が複数 repo に write できても、CWD は安全境界にならない。技術的な分離が必要なら repo 別 deploy key、fine-grained PAT、GitHub App、machine user 等で actor を分ける。

public contributor に archive / backstage access を要求しない。公開範囲の判断は公開 knowledge で検証可能にする。

## 4. 外部領域

外部サービス、server、account、課金、公開設定への作用は、依頼された scope と credential の境界を確認する。agent に許可する場合は human 用と分けた OS user / SSH key / server user / limited token を使う。

同じ OS user から読める credential は、その user で動く agent も利用できる。鍵の filename を変えるだけでは境界にならない。

## 5. 検証不能を確約しない

権限と実行能力があっても、誰も結果を検証できない作業は確約へ落とさない。scope 縮小、evidence 追加、別主体への委譲、捕捉への park、工房での試行へ振り分ける。

確約するときは、検証した scope、evidence、未検証の境界を明示する。主張の scope を evidence の scope から越境させない。
