# tools

独立して利用できる tool / test は MIT License です。

## DECISIONS checker

```bash
python3 tools/check-decisions.py
python3 -m unittest tools/test_check_decisions.py
```

次を検査します。

- decision ID の重複
- `改訂→<ID>` の参照先不存在
- `起案` / `保留` が未確定 dashboard 外に残ること
- 再開 trigger のない `保留`
