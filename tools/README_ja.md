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
