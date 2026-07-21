# AGENTS.md — mc-remote-knowledge

このファイルは Codex 等の coding agent 向けの薄い入口です。

## 正典は CLAUDE.md

このリポの運用ルール・哲学・構成の唯一の正典は [CLAUDE.md](CLAUDE.md) です。作業前に全文を読み、そこに従ってください。本ファイルへルール本文を複製しません。

特に次を効かせます。

- 判断理由と却下案を残し、過去の決定を上書きで消さない
- 自分が編集した path だけを明示 stage する
- 秘密の実値を書かない
- 横断決定は `00-hub/DECISIONS_ja.md` に残し、着地前に人間レビューを通す
- 文書は日本語、topic-first kebab-case と `_ja` suffix を基本にする

Claude Code 固有の `@import`、hooks、surface 能力の説明は、他の agent へそのまま適用しなくて構いません。
