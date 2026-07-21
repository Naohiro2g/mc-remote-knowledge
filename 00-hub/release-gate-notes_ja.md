# Release gate notes — public baseline

> 新 public 正本世代の空テンプレート。旧世代の release 固有履歴は carry しない。

release 判定は、実装 repo 側が事実と根拠を記入し、knowledge 側が contract と照合します。秘密実値、private inventory、未 sanitized raw log はここへ貼りません。

## 確認票

```markdown
## Release gate 確認票

- 対象 repo:
- 対象 branch/commit:
- release / channel:
- knowledge contract path:
- knowledge contract commit:
- test class: unit/deterministic / live-auto / live-human
- 実行した command / 手順:
- 結果:
- evidence record / artifact:
- 未検証の境界:
- security / compatibility / rollback の確認:
- 判定を求める事項:
```

`live-human` や高い再現コストを持つ検証は `14-evidence/` の sanitized record を参照します。private evidence は `mc-remote-backstage`、秘密を含む raw は Git 外です（`2026-07-06-03` / `2026-07-21-04`）。
