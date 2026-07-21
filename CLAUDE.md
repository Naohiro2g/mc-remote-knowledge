# CLAUDE.md — mc-remote-knowledge

この public repository は、マイクラリモコン（mc-remote / Code2CreateClub）の設計記録・横断決定・現行 contract を管理する SSOT です。コードは各 dev repository に置きます。

## 動作原理

- 教材開発から実開発・検証・運用まで、同じ観察と自己判定の原理で地続きに扱う。ただし gate と委譲境界は「テーマ × 現在地 × 作業」に合わせて投影する。
- 「観察 → 痕跡を残す → 言語化 → 比較・検証 → 自己判定 → 共有・再検証」を正典順序とする。言語化を最初の入場条件にしない。
- agent は合意範囲で起草・生成・実行・検証を担う。未検証の正しさと設計判断を人間に代わって確定しない。
- 主張のスコープを証拠のスコープから越境させず、誰も結果を検証できないことは確約しない（決定 `2026-07-19-05`）。

## このリポの役割

- 結論もの（設計記録・決定ログ・現行 contract）の唯一の真実の源。
- 会話の生ログや秘密の実値を置かない。
- private archive / backstage を通常参照せず、公開 contributor にアクセスを要求しない。
- archive を例外参照したら `00-hub/NOTES_ja.md` に carry-forward 欠落として記録し、このリポだけで判断できる状態にして閉じる（`2026-07-21-01`）。

## 最優先の価値：判断理由を残す

- 決定には結論、理由、却下案を残す。
- 変更時は古い行を消さず、新しい決定を追記し、前後を参照でつなぐ。
- 横断決定は `00-hub/DECISIONS_ja.md`、未確定の芽は `00-hub/NOTES_ja.md` に置く。

## ハブ & スポーク

```text
00-hub/            全体原理・索引・横断決定・agent contract
10-protocol/       plugin と client 間の通信 contract
11-plugin/         server plugin の設計
12-python-client/  Python client の設計
13-scratch-client/ Scratch client の設計
14-evidence/       公開可能な evidence policy / sanitized records
20-教材/           学習支援・教材設計
30-広告宣伝/        公開戦略
```

公開 server package / runbook は `mc-remote-stack`、private ops は `mc-remote-backstage` が正本です。本リポへ private ops を戻しません（`2026-07-21-03`）。

## ファイル命名

- 構造ファイル（`README` / `DECISIONS` / `INDEX` / `NOTES` / `CLAUDE.md` / `AGENTS.md` / `LICENSE*` / `CONTRIBUTING.md` / `SECURITY.md`）は慣用名を使う。
- それ以外の文書は `<topic>-<genre>_ja.md`。topic-first、小文字 kebab-case、genre suffix（`design` / `guide` / `plan` / `notes` / `roadmap` / `instructions`）。
- 日付と番号はファイル名へ入れない。日付は本文、番号接頭辞はディレクトリだけに使う。

## 作業規律

- token、API key、password、private key 等の秘密の実値を書かない。raw log に秘密が混ざる場合は Git 外へ置く。
- 自分が編集した path だけを明示 stage する。`git add -A` / `git add .` は使わない。
- commit 前に `git diff --staged` を確認する。commit は stage 済み index を `git commit`（pathspec なし）で確定する。
- ユーザーや他 agent の未関連変更を触らない。競合する場合は止めて確認する。
- 意味のある小さい単位で commit する。
- 設計、命名、public/private 境界、確定/起案の別は着地前に人間レビューを通す。合意済み内容の verbatim / mechanical な投影だけは確認なしで進めてよい。
- 文書は日本語（`_ja`）を基本とする。

## セッションと evidence

- 現在地の問い合わせには `00-hub/claude-ai-guide_ja.md` の `セッションループ現在地` 形式を使う。
- 固定票三種の本文は `00-hub/dev-repo-protocol_ja.md` を唯一の正本とする（`2026-07-21-08`）。
- 人間参加・横断型実機テストを正式根拠にするときは `14-evidence/` に sanitized record を置く。秘密実値を含む raw は公開 commit しない（`2026-07-06-03` / `2026-07-21-04`）。

## トークン衛生

冗長ログはファイルへ残し、会話には失敗箇所だけを出す。理由と定型は [token-hygiene-guide_ja.md](token-hygiene-guide_ja.md) を参照する。

## 実行境界

権限境界（してよいか）、実行能力境界（できるか）、検証能力境界（確かめられるか）を分ける。できると確証のない外部操作を推測で進めない。詳細は [LLM agent boundary guide](00-hub/llm-agent-boundary-guide_ja.md) を参照する。

## @import（Claude Code）

常時 preload は、小さく高密度で、ほぼ毎セッション必要な規則だけに限る。当面 `@import` はゼロとし、設計記録は task に応じて on-demand で読む。
