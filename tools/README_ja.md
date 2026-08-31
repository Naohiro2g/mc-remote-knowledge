# tools

独立して利用できる tool / test は MIT License です。

## DECISIONS checker

```bash
python3 tools/check-decisions.py
python3 -m unittest tools/test_check_decisions.py
```

次を検査します。

- decision ID の重複
- 新規の短縮 decision ID 参照（public epoch前の歴史行6件だけ互換入力）
- DECISIONS内の参照先不存在（`NOTES_ja.md`に登録されたcarry-forward gap・解決経緯は許容）
- `改訂→<ID>` の参照先不存在
- 改訂先から旧 decision ID への参照欠落
- 日付見出しの重複
- `起案` / `保留` が未確定 dashboard 外に残ること
- 再開 trigger のない `保留`

## dev agent runtime block checker

```bash
python3 -m unittest tools/test_dev_repo_protocol.py
```

`00-hub/dev-repo-protocol_ja.md` の marker 間だけを抽出し、dev リポへ実際に渡る runtime block に
ローカル `CLAUDE.md`／`NOTES_ja.md` の非追跡境界が含まれることを検査します。marker 外の説明にだけ
規則が存在する bootstrap 欠落を防ぎます。

### `--meta`（局面の宣言候補）

```bash
python3 tools/check-decisions.py --meta
```

影響欄の領域数が 6 以上で、状態セルに `局面` の記載が無い決定を列挙します。**判定はせず候補を
出すだけ**で、exit code は常に 0 です。横断度は機械的に測れますが、重要度と時間軸は人間との
対話で決めるためです（`2026-07-25-05`）。範囲を示して編集する流れの中で「今回は影響範囲が
広い」と気づくための補助として使います。

`2026-07-25` より前の行は対象外です。過去の決定へ重みの札を貼らないという同決定の方針に
従い、遡って埋めません。FAIL にしないのは、FAIL にすると「局面＝当面」と書いて通す最短経路が
でき、同決定の却下③が警告した形骸化になるためです。

## Gemini Notebook 用ソースバンドル generator

`build-notebooklm-bundle.py` は、指定した Git commit tree の Markdown を
Gemini Notebook（旧 NotebookLM）取り込み用のソースバンドルへ束ねます。working tree
の未commitファイルは読みません。

無修飾の「バンドル」は配備バンドル（deployment bundle）を指します。本 generator の
出力は `Gemini Notebook 用ソースバンドル` と修飾して呼びます（`2026-07-25-04`）。
script 名と test 名は `2026-07-23-05` で固めた生成経路の参照を動かさないため変更しません。

```bash
# 全体を dist/notebooklm/ へ生成
python3 tools/build-notebooklm-bundle.py

# 小さいスコープを一時出力へ生成
python3 tools/build-notebooklm-bundle.py 00-hub 10-protocol --out /tmp/notebooklm-check

# tag / commitを投影元として固定
python3 tools/build-notebooklm-bundle.py --source-ref notebooklm/2026-07-23

# 生成器の回帰・再現性検査
python3 -m unittest tools/test_build_notebooklm_bundle.py
```

出力は `00-current-state-capsule.md` と、トップ階層単位の連結Markdownです。
現在地カプセルは次のpublic正本セクションを原文のまま投影します。

- `00-hub/grand-design-roadmap_ja.md` の `## 現在地`
- 同文書の `## 4. 現在の横断優先`

指定見出しの欠落・重複・空、存在しないsource ref、未知のMarkdownが出力先に
残る場合は生成を停止します。同じcommitと引数からは同じbytesを生成します。

Notebookへアップロードするときは、cleanなsource commitから一時生成して検証し、
そのcommitへannotated tag `notebooklm/YYYY-MM-DD[-NN]` を作成します。tagから本生成し、
事前生成と同一であることを確認してからtagをpushします。通常の文書更新では
ソースバンドルを生成・追跡しません。

`dist/` は使い捨て生成物でありGit管理しません。根拠は
`2026-07-01-07`、現在のpublic投影経路は`2026-07-23-05`です。
