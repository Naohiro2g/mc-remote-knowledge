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

## 2026-08-07 Scratch editor `2100.0.0b3`

- candidate: `release/b3@3f1a10a366bfbe76e32b5a31c54da19eddd56e56`
- contract: `13-scratch-client/scratch-roadmap_ja.md` §2.3 / knowledge `3dfbf57c07f2b7985c65edc5564b879f9e67e122`
- CI: run `31145335984`、exact candidate、全job success
- evidence: `14-evidence/records/2026-08-07-scratch-b3-release-gate_ja.md`
- status: **GREEN — tag `v2100.0.0b3`とGitHub prerelease作成を承認**
- release条件: tag targetは上記candidate完全SHA、prerelease ON、draft OFF、Latest非対象
- rollback: `v2100.0.0b2@e19247069d1ae55037c0e9ffc52ea88cde612ac3`
- scope boundary: hosted surface更新は含めない。更新時はdeploy smoke / rollback / re-deployを別gateで確認する
- deferred: catalog picker / WireScope miniはb4、独立WireScopeは`2026-08-06-03`どおりb3非blocker
