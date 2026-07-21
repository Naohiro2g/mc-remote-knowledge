# mc-remote-knowledge INDEX

public 正本世代の入口です。ここに載る path は、このリポ内で解決できる現行文書です。

## ハブ

| Path | 役割 |
| --- | --- |
| `00-hub/DECISIONS_ja.md` | 公開可能で現行判断に必要な横断決定。旧世代から carry した行は同じ ID・同じ本文 |
| `00-hub/NOTES_ja.md` | 未確定の芽と archive carry-forward 欠落 |
| `00-hub/knowledge-repo-design_ja.md` | public SSOT の構造・trust boundary・運用理由 |
| `00-hub/grand-design-roadmap_ja.md` | 低 drift な粗い相マーカーと横断優先 |
| `00-hub/dev-repo-protocol_ja.md` | 4 dev リポの bootstrap、runtime marker、固定票三種 |
| `00-hub/claude-ai-guide_ja.md` | session loop と surface 間の着地方法 |
| `00-hub/claude-ai-instructions_ja.md` | claude.ai instructions |
| `00-hub/llm-agent-boundary-guide_ja.md` | agent の権限・実行・検証境界 |
| `00-hub/release-gate-notes_ja.md` | 新世代で使う空の release gate template |
| `00-hub/terms-glossary_ja.md` | 横断語彙 |

## 現行 contract / client design

| Path | 役割 |
| --- | --- |
| `10-protocol/versioning-design_ja.md` | protocol version と release compatibility の contract |
| `10-protocol/wire-format-design_ja.md` | wire envelope、hello/auth、command/error の contract |
| `11-plugin/platform-design_ja.md` | server plugin / loader の設計境界 |
| `12-python-client/python-client-guide_ja.md` | Python client の公開利用面 |
| `12-python-client/mc-constants-design_ja.md` | constants / catalog の生成・配布設計 |
| `13-scratch-client/debug-session-design_ja.md` | debug / observation session の設計 |
| `13-scratch-client/scratch-execution-model-design_ja.md` | Scratch 実行モデルと stream の前提 |
| `13-scratch-client/scratch-upstream-design_ja.md` | upstream 追従と contribution の一方向弁 |

## 耐久層

| Path | 役割 |
| --- | --- |
| `20-教材/ai-learning-design_ja.md` | 学習支援の哲学、AI 委譲境界、Scratch / Python の並列ビークル論 |
| `token-hygiene-guide_ja.md` | 情報を失わず context token を減らす運用 |

## Evidence

| Path | 役割 |
| --- | --- |
| `14-evidence/README_ja.md` | public / private / Git 外の visibility policy |
| `14-evidence/INDEX_ja.md` | public sanitized record の索引。新世代開始時点では空 |

## 初回 seed に含めないもの

- 旧 `NOTES`、session memo、過去 release 固有の gate notes
- 過去の evidence / raw artifact
- private ops、provider / account / cost / host の実値
- superseded または移行中の protocol / API / wire 詳細
- 公開可否・ライセンスが未確認の資料

必要になって archive を参照した場合は、archive link を恒久依存にせず `00-hub/NOTES_ja.md` へ carry-forward 欠落を登録します。
