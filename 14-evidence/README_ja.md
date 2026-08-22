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

raw は `14-evidence/raw/` に一時配置できるが gitignore 対象であり、public commit しません。公開 record は token、`pairing_id`、private host、UUID 等を必要に応じて redact し、redaction が主張を壊していないことを確認します（`2026-07-06-03` / `2026-07-21-04` / `2026-08-22-01`）。pair codeと表示用`/mcremote pair NNN-NNN`は通常log、transcript、公開evidenceへ収録でき、必須redaction対象ではありません。

新 public 正本世代は過去 evidence を carry せず、空の索引から始めます。

b5／b6 plugin APIの横断的な検証範囲は
[b5／b6 横断検証設計](b5-b6-verification-design_ja.md)を参照します。これは未実施の結果を
evidence化する文書ではなく、実行後にrecordへ残す主張とtest classの境界です。
