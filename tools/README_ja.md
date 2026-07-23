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

## Gemini Notebook bundle generator

`build-notebooklm-bundle.py` は、指定した Git commit tree の Markdown を
Gemini Notebook（旧 NotebookLM）取り込み用に束ねます。working tree の未commit
ファイルは読みません。

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
バンドルを生成・追跡しません。

`dist/` は使い捨て生成物でありGit管理しません。根拠は
`2026-07-01-07`、現在のpublic投影経路は`2026-07-23-05`です。
