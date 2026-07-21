# mc-remote-knowledge

マイクラリモコン（mc-remote / Code2CreateClub）の設計記録、横断決定、現行 contract を公開する knowledge repository です。実装は各 dev repository に置き、このリポは「何を、なぜ、どの境界で決めたか」の SSOT を担います。

## 最上位の動作原理

- 教材開発、実装、検証、運用を、同じ観察と自己判定の原理でつなぐ。
- 学びと開発は **観察 → 痕跡を残す → 言語化 → 比較・検証 → 自己判定 → 共有・再検証** の順で進める。言語化を最初の入場条件にせず、観察前に原因説明を要求しない。
- AI / agent は支援役であり実行者でもあるが、未検証の正しさや設計判断を人間に代わって確定しない。
- 生成を委譲しても、判断・検証・統合は人間が握る。主張のスコープを証拠のスコープから越境させない。
- 結論だけでなく、理由と却下案を残す。後から変えるときも古い判断を消さない。

教育観の詳説は [AIアシストと学習支援](20-教材/ai-learning-design_ja.md)、運用原理は [knowledge repository design](00-hub/knowledge-repo-design_ja.md) を参照してください。

## 入口

- [INDEX](00-hub/INDEX_ja.md) — 現行文書の地図
- [DECISIONS](00-hub/DECISIONS_ja.md) — 横断決定ログ
- [NOTES](00-hub/NOTES_ja.md) — 未確定の芽と archive carry-forward 欠落
- [dev-repo protocol](00-hub/dev-repo-protocol_ja.md) — 4 dev リポが on-demand 取得する runtime contract
- [CONTRIBUTING](CONTRIBUTING.md) — contribution の入口
- [SECURITY](SECURITY.md) — security-sensitive な報告

## 正本世代

この public リポは、private 履歴を継承せず 2026-07-21 に開始した新しい正本世代です。旧リポは `mc-remote-knowledge-archive` として private / frozen に保管されますが、通常作業や contribution に archive へのアクセスは要りません。archive を例外参照して欠落が見つかった場合は、[NOTES](00-hub/NOTES_ja.md) に記録し、この public リポだけで同じ判断ができる状態まで carry-forward して閉じます（決定 `2026-07-21-01`）。

## 関連リポ

- `McRemote` — Paper plugin
- `minecraft-remote-api` — Python client
- `scratch-editor` — McRemote extension を含む Scratch editor fork
- `mc-remote-stack` — 公開 server package / bootstrap / runbook の SSOT
- `mc-remote-backstage` — private ops の SSOT。公開 contributor は参照しません

## ライセンス

オリジナルの文書・図・教育資料は CC BY-SA 4.0、独立して利用できるコード・ツールは MIT です。第三者由来のものは原ライセンスに従います。詳細は [LICENSE.md](LICENSE.md) と `LICENSES/` を参照してください。
