# mc-remote-knowledge public SSOT 運用設計

> 状態: 2026-07-21 public epoch baseline

## 1. 解く問題

会話、コード、運用、教材が複数リポと複数 LLM surface に分散すると、結論だけが残り「なぜ」が失われる。逆に全ログを一箇所へ集めると、秘密・揮発情報・古い判断が現行 contract と混ざる。本リポは、公開可能な結論ものをハブ & スポークで結び、判断理由と却下案を検証可能な形で残す。

## 2. 正本世代と trust boundary

2026-07-21、private 履歴を public 履歴へ持ち込まないために、履歴非継承の新しい正本世代を開始した。旧リポは private frozen archive として完全保存し、新 public が名前、通常作業、依存先を継承する（`2026-07-21-01`）。

これは履歴の削除や要約置換ではなく、trust boundary をまたぐ cutover である。同一世代・同一 trust boundary の内部では、append-only と生成投影優先（`2026-07-20-05`）を維持する。

archive は通常依存にしない。例外参照で欠落を見つけたら NOTES に登録し、公開可能な interface と why を current SSOT へ carry する。公開できない行を同じ decision ID の redacted 版として作らない。

## 3. ハブ & スポーク

`00-hub` は横断原理、決定、索引、agent contract を持つ。`10`–`30` は対象別の設計を持つ。通信 contract は `10-protocol` を正本とし、plugin / Python / Scratch は実装固有の判断だけを持つ。横断変更はスポークだけで閉じず DECISIONS に残す。

公開 server package / runbook は `mc-remote-stack`、private ops は `mc-remote-backstage` が正本であり、knowledge に実環境の実値を戻さない（`2026-07-21-03`）。

## 4. Surface と同期

Git repository が system of record。claude.ai Project や NotebookLM は snapshot / projection であり、食い違えば repository が正しい。snapshot から確定が生まれた場合は固定搬送票で repository 側へ戻し、ID 採番・stage・commit は live repository を所有する surface が行う。

projection は読者、テーマ、現在地、作業に合わせて生成する。projection 自体を第二の正本にしない。

## 5. 公開境界

- public knowledge: 設計思想、現行 contract、sanitized evidence、公開 release summary
- private backstage: provider / account / cost / inventory / internal incident 等の運営情報。ただし秘密実値は置かない
- Git 外: token、password、private key、秘密を含む raw log / capture / dump

不明な権利物は fail closed で seed へ入れない。文書は CC BY-SA 4.0、独立 tool / code は MIT（`2026-07-21-02`）。

## 6. Contribution gate

archive / backstage へのアクセスを contributor に要求しない。private 資料だけを根拠に reject せず、公開可能な理由を返す。設計・命名・public/private 境界は human review、合意済みの機械変更は maintainer direct-main を許す。security-sensitive な報告は public Issue に誘導しない（`2026-07-21-05`）。

## 7. 最小限の保険

- 意味単位の小さい commit
- 自分の path だけを明示 stage
- DECISIONS は append-only、改訂は新旧を双方向に接続
- evidence は再現コストと visibility の両方で分類
- INDEX のリンクを全て解決可能に保つ
- default branch の force push / 削除を禁止
