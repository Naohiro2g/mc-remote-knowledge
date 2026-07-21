# 14-evidence（公開 evidence）

人間参加・複数 repo 横断など、再現コストが高い検証を後から監査できる形で残します。

## Test class

- `unit/deterministic`: test code + PASS command + commit で足りる
- `live-auto`: 実 server smoke。release gate の根拠に使う回は transcript を保存する
- `live-human`: pairing 等の人間操作・実機状態を含む。正式根拠は record + sanitized artifact を作る

## Visibility

- public knowledge: policy、sanitized record / artifact、public contract の検証結果
- `mc-remote-backstage`: private inventory / internal ops / 非秘密だが非公開の evidence
- Git 外: token、password、private key、秘密実値を含む raw log / capture / dump

raw は `14-evidence/raw/` に一時配置できるが gitignore 対象であり、public commit しません。公開 record は token、pair code、private host、UUID 等を必要に応じて redact し、redaction が主張を壊していないことを確認します（`2026-07-06-03` / `2026-07-21-04`）。

新 public 正本世代は過去 evidence を carry せず、空の索引から始めます。
