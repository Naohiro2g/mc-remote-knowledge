# mc-remote-knowledge INDEX

public 正本世代の入口です。ここに載る path は、このリポ内で解決できる現行文書です。

## ハブ

| Path | 役割 |
| --- | --- |
| `00-hub/DECISIONS_ja.md` | 公開可能で現行判断に必要な横断決定。旧世代から carry した行は同じ ID・同じ本文 |
| `00-hub/NOTES_ja.md` | 未確定の芽と archive carry-forward 欠落 |
| `00-hub/knowledge-repo-design_ja.md` | public SSOT の構造・trust boundary・運用理由 |
| `00-hub/document-style-guide_ja.md` | 拘束／説明／投影の三層と、骨格→柵→拘束層への錨という説明文書の様式 |
| `00-hub/grand-design-roadmap_ja.md` | 低 drift な粗い相マーカーと横断優先 |
| `00-hub/readme-sample-modernization-roadmap_ja.md` | 各public repoの人間向けREADMEと実行可能sampleをb7〜stableへ整える横断track |
| `00-hub/authentication-roadmap_ja.md` | 認証現在地、Client Library共通session credential UX、long-lived公開gate、credential-lifecycle再開順序 |
| `00-hub/deployment-interface-design_ja.md` | Scratch product/runtime config、Scratch–Stack contract handoff、一order＋apply／doctorの通常deployment経路 |
| `00-hub/dev-repo-protocol_ja.md` | 4 dev リポの bootstrap、runtime marker、固定票三種 |
| `00-hub/claude-ai-guide_ja.md` | session loop と surface 間の着地方法 |
| `00-hub/claude-ai-instructions_ja.md` | claude.ai instructions |
| `00-hub/llm-agent-boundary-guide_ja.md` | agent の権限・実行・検証境界 |
| `00-hub/release-operations-responsibility-design_ja.md` | 公開runbook、物理host、deployment、component担当、gate coordinator、人間release ownerの責務、test tier／change cone／常設dev harness／gate manifest／release close |
| `00-hub/release-gate-notes_ja.md` | 公開release gateの確認票、coordinator、phase、exact set、許可済み次操作の状態集約 |
| `00-hub/terms-glossary_ja.md` | 横断語彙 |
| `00-hub/external-facts_ja.md` | 決定が `F-<topic>` で参照する外部事実の生きた台帳（調査日・状態・次回確認を更新する） |
| `00-hub/domain-knowledge-modules-design_ja.md` | 起案。領域知識を domain knowledge module として分離する方式（`2026-07-02-01` の起案正本） |
| `00-hub/world-constants-facts_ja.md` | 旧世代 archive から carry。次元×世代別の世界定数実値表（`y_ground`/`y_sea`/`y_lava`/`y_cloud`/`steve_min_y`/`steve_max_y`）。domain knowledge の最初の実体候補 |
| `00-hub/world-constants-provision-notes_ja.md` | 旧世代 archive から carry。世界定数・catalog をサーバーからクライアントへ配る動機（VS Code 自動補完のための実ファイル化・環境スイッチング構想）を記した設計メモ |

## 現行 contract / client design

| Path | 役割 |
| --- | --- |
| `10-protocol/versioning-design_ja.md` | protocol version と release compatibility の contract |
| `10-protocol/beta-to-stable-release-roadmap_ja.md` | method成熟状態、b6 sign／b7 direction／b8 entity lifecycle、WireScope companion、Paper 26.x pulse、初回stableまでの現行roadmap |
| `10-protocol/polyglot-client-roadmap_ja.md` | Java bootstrapを起点に、developer experience評価、Python／Java比較、既存conformance資産の一般化、TypeScript／browser／C#展開へ進む多言語Client Libraryロードマップ |
| `10-protocol/wire-format-design_ja.md` | wire envelope、hello/auth、command/error の contract |
| `10-protocol/dimension-key-design_ja.md` | protocol 22のDimensionKey入力／出力、build context、surface投影、protocol 21非互換境界 |
| `10-protocol/block-value-design_ja.md` | protocol 22の構造化block value、set／get対称性、多言語・Scratch投影の説明正本 |
| `11-plugin/platform-design_ja.md` | server plugin / loader の設計境界、availability guard、認証設定lifecycle、credential 永続化と失効耐性（§9） |
| `11-plugin/b7-live-gate-followup-instructions_ja.md` | b7 handle reason／session permission修正とtargeted再検証のMcRemote担当向け確定指示 |
| `12-python-client/python-client-guide_ja.md` | Python client の公開利用面 |
| `12-python-client/b7-permission-contract-followup-instructions_ja.md` | b7 successor fixtureとpermission説明へ追従するPython担当向け確定指示 |
| `12-python-client/mc-constants-design_ja.md` | constants / catalog の生成・配布設計 |
| `13-scratch-client/debug-session-design_ja.md` | debug / observation session の設計 |
| `13-scratch-client/scratch-execution-model-design_ja.md` | Scratch 実行モデルと stream の前提 |
| `13-scratch-client/scratch-upstream-design_ja.md` | upstream 追従と contribution の一方向弁 |
| `13-scratch-client/scratch-roadmap_ja.md` | Scratch の現行 release scope、検収基線、R3 作業束 |
| `13-scratch-client/scratch-block-value-projection-design_ja.md` | protocol 22 block値のStateText／BlockInfoText／Picker／ErrorText投影 |
| `13-scratch-client/b7-permission-fixture-amendment-instructions_ja.md` | b7 session permission contractのsuccessor fixtureを発行するScratch protocol owner向け確定指示 |
| `13-scratch-client/scratch-project-storage-transfer-design_ja.md` | 作品共有の責任分界、ブラウザ／ファイル保存、スプライト・ブロックの移送モデル |
| `13-scratch-client/scratch-plan_ja.md` | **原点文書（完全保存・改訂しない）**。再始動の起点。現行 contract の正本ではなく、食い違う場合は 10-protocol が優先（`2026-07-26-01`） |
| `16-java-client/README_ja.md` | 現行Java Client Libraryのrepository、group／root package、build境界、Java bootstrap baseline、次の縦slice |

## WireScope

| Path | 役割 |
| --- | --- |
| `15-wirescope/README_ja.md` | source／station／browser三役モデルから入る人間向け入口 |
| `15-wirescope/wirescope-deployment-design_ja.md` | public browser hostname、browser source handoff、station、deployment profile、capability、LNA、failure semantics、長期ビジョンの説明正本 |
| `15-wirescope/wirescope-station-attach-design_ja.md` | 共通appのadapter、observer session、artifact、Python browser-loopback参照profile、Stack gateの説明正本 |

## 耐久層

| Path | 役割 |
| --- | --- |
| `20-教材/ai-learning-design_ja.md` | 学習支援の哲学、AI 委譲境界、Scratch / Python の並列ビークル論 |
| `20-教材/client-sample-learning-ux_ja.md` | Client repoのREADME隣接examplesと`mc_remote_samples`のconcept-first多言語比較面のowner・学習UX |
| `20-教材/environment-guide_ja.md` | 教材・OSS の想定実行環境、uv 統一、deployment profile とケータリング型の区別 |
| `20-教材/jupyter-notes_ja.md` | デモ .ipynb の autoreload / CWD / 実行順序依存の注意点 |
| `token-hygiene-guide_ja.md` | 情報を失わず context token を減らす運用 |

## 広告宣伝

| Path | 役割 |
| --- | --- |
| `30-広告宣伝/README_ja.md` | homepage、半自動release notes、技術記事とproduct gateの境界 |

## Evidence

| Path | 役割 |
| --- | --- |
| `14-evidence/README_ja.md` | public / private / Git 外の visibility policy |
| `14-evidence/beta-verification-design_ja.md` | b5〜b8 event・sign・direction・entity・WireScope compatibilityのassertion inventory、test class／tier、横断検証境界 |
| `14-evidence/INDEX_ja.md` | public sanitized record の索引。新世代開始時点では空 |

## 初回 seed に含めないもの

- 旧 `NOTES`、session memo、過去 release 固有の gate notes
- 過去の evidence / raw artifact
- private ops、provider / account / cost / host の実値
- superseded または移行中の protocol / API / wire 詳細
- 公開可否・ライセンスが未確認の資料

必要になって archive を参照した場合は、archive link を恒久依存にせず `00-hub/NOTES_ja.md` へ carry-forward 欠落を登録します。
