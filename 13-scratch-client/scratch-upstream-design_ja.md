# 設計記録: Scratch upstream 追従と貢献の分離

> 状態: 現行運用として確定（DECISIONS `2026-07-20-06`。`2026-07-18-02` を改訂）
> 出自: 2026-07-18 `Naohiro2g/scratch-editor` 作業セッションの検討素材（確定搬送票でない旨明示あり）を、knowledge 側で §2.9・リリースチャンネル決定群・contrib clone 実機と突き合わせて再構成。2026-07-19、contrib セッション bootstrap と貢献パイプライン（探索→起票→運搬→戻し）を補強
> 関連: hub DECISIONS `2026-07-20-06`（upstream contribution の一方向弁）／`2026-07-20-03`（agent configuration topology）。旧 `scratch-plan` の volatile な実装計画は public seed 初回から除外し、本書を現行 upstream 方針の入口とする。

---

## 1. 収容境界（この文書の前提原則）

- **収容の基準は関連性でなく管轄（出自）**。ナレッジリポが正典を持つのは、判断権を持つ**界面**まで＝追従方針・handoff 様式・watch 仕様・境界規律。
- **upstream 内部の正本は upstream の venue に住む**。バグ分析・修正の設計理由・PR の中身の正典は Scratch Foundation の Issue / PR（翻訳は Transifex）。こちらには URL 参照のみを置き、複製しない（管轄外の複製は、原本が動いても自分で正せない drift 源）。
- **「地続きだが、同一管轄ではない」**。方法論（観察 → 痕跡を残す → 言語化 → 比較・検証 → 自己判定 → 共有・再検証）は人と共に携行するが、作業記録は現地の正典形式へ着地させる。こちらへ帰るのは界面の決定と、自分たちの方法論についての学び（evidence は merged PR への参照＝born-public なポインタ）。
- 消費（Minecraft 本体・GitHub・XServer 等）ではこの境界は自明だったが、**貢献**では作業が自分たちのもので venue が向こうのものになるため、記録がナレッジへ「帰りたがる」張力が初めて生じる。本節はその明文化。
- 本原則は Scratch 固有でなく**汎用側候補**（外部系との界面規律）。汎用フレームワーク起案時に昇格を検討する。

## 2. 二トラックの分離

### A. upstream 追従（McRemote 側）

- 目的: McRemote 版 `Naohiro2g/scratch-editor` を公式へ継続追従させ、upstream 差分と McRemote 固有変更の競合・回帰リスクを評価し、追従候補を alpha/beta 等で検証可能な状態へ運ぶ。
- 作業場所: 既存 McRemote 開発 clone `scratch-editor/`（repository: `Naohiro2g/scratch-editor`）。
- 担当範囲: upstream 差分確認（ahead/behind・commit・変更ファイル分類）／McRemote 変更箇所との重複確認／追従用 branch・PR／McRemote 固有 build・test／alpha/beta 回帰確認。
- 扱わないもの: 公式向け一般バグ修正 PR、upstream 貢献のための実装、全体リリース計画の決定。

### B. upstream 貢献（公式側）

- 目的: **Scratch コミュニティへの貢献を第一義とする**。l10n（ローカライゼーション。翻訳は Transifex 経由・基盤はツーリング PR＝二経路、§7）と、公式で再現する一般バグの修正を Scratch Foundation へ返す。McRemote fork の差分縮小は副次的に得られる効果であり、第一義ではない。
- 作業場所: 独立 clone `scratch-editor-upstream-contrib/`（§4）。
- 担当範囲: 公式 Issue の再現確認／公式 `develop` からの branch 作成／failing test の追加／一般化された最小修正／公式向け PR／公式 contributor policy・AI-assisted development policy への準拠。
- 扱わないもの: McRemote 固有実装、McRemote の release 期限、McRemote private SSOT を根拠とした公式設計変更、McRemote 版への直接統合。

## 3. トラック間の関係（一方向）

```text
upstream貢献
  → Scratch Foundation公式へマージ
  → upstream追従が公式変更として検知
  → McRemote側で統合・検証
  → 全体リリース計画へ準備状態を報告（報告のみ）
```

- 貢献 PR の commit は、**原則として McRemote 版へ先行 cherry-pick しない**。公式マージ後に通常の追従として取り込む。緊急先行採用は別途の例外判断とし、本方針では決めない。
- 全体リリース計画へ渡すのは準備状態の報告のみ。リリース時期・bN の内容・release freeze・channel 昇格条件は本文書からは決めない（`2026-06-25-02`〜`-06` のまま）。

## 4. サーフェスと環境

### 貢献用 clone（2026-07-18 実機検証済み）

- 場所: `AA_KNOWLEGE_BASED_DEV_SYSTEM/scratch-editor-upstream-contrib/`（clone 元: `scratchfoundation/scratch-editor`、作成時 HEAD `bb4337a` / `develop` / clean / full clone）
- push 安全設計（検証済み）: `origin` push URL `DISABLED`／`fork`＝`Naohiro2g/scratch-editor`／`remote.pushDefault=fork`／`push.default=simple`／`branch.develop.pushRemote=origin`。**貢献 branch は fork へ明示 push、`develop` は push 先が無効化 origin のためどこへも push 不能**＝誤 push を構造的に防ぐ。

### セッション規律

- 貢献 clone は**専属セッション**で扱う。同一セッションで2つの clone を往復しない（remote・branch・AGENTS・設計目的の混同を招く）。
- **contrib セッションはナレッジリポを読まない**。作業根拠は handoff 票（§5）の記載事項のみ＝一方向弁。読むのは公式の AGENTS.md・contributor policy。
- 運用者ローカルの指示書・NOTES は置いてよいが**非コミット**。除外は `.git/info/exclude` で行う（`.gitignore` 編集は upstream との diff になるため不可）。公式 AGENTS.md は改変・複製しない。
- 公式 contributor policy / AI-assisted development policy は**PR 提出の直前に毎回**最新版を確認する（policy は動く）。
- 専用の別 AI モデルは不要。同一モデルでよいが、作業ディレクトリと会話セッションを分離する。

### contrib セッション bootstrap（正本はここ・投影は非コミット）

contrib セッションは設計上ナレッジリポを読まない＝**構造的に無知で開始する**。知識を渡す唯一の経路は「人間が運ぶ投影」で、その実体が本テンプレート。正本は本節、投影は contrib clone 直下の `local-bootstrap_ja.md`（非コミット・`.git/info/exclude` 登録・投影日付入り）。内容を変えるときは正本を直してから再投影する。

公式 AGENTS.md は改変できないため、bootstrap は自動では読まれない。人間がセッション開始時に次の定型文を最初に貼る:

```text
local-bootstrap_ja.md を読んでから、以下の貢献作業票を処理して。
```

テンプレート（投影時に日付を更新）:

```markdown
# contrib セッション bootstrap（投影: YYYY-MM-DD・正本: mc-remote-knowledge/13-scratch-client/scratch-upstream-design_ja.md §4）

- 任務: Scratch コミュニティへの貢献（l10n・一般バグ修正）。ここは Scratch Foundation の管轄で、あなたは客。
- 読むもの: 公式 AGENTS.md・CONTRIBUTING・渡された貢献作業票。読まないもの: mc-remote-knowledge・McRemote の clone。
- 根拠は貢献作業票の記載のみ。McRemote の事情を修正理由にしない。
- 環境: origin＝scratchfoundation 公式（push 無効化済み）／fork＝Naohiro2g/scratch-editor。branch は develop から作成し、push は fork へ明示。develop へは commit しない。
- 初回セットアップ: 公式ドキュメント（README / AGENTS.md）に従う。手順をこのファイルへ複製しない。実施結果（npm ci 済み等）は作業票の「環境メモ」へ書く。
- PR 提出の直前に contributor policy / AI-assisted development policy の最新版を毎回確認する。
- 成果は公式 venue（Issue コメント・PR・Transifex）へ。セッション終了時に作業票の「戻し報告」を埋める。
- このファイルの投影日付が古い（目安2週間超）場合は、人間に正本からの再投影を求める。
```

## 5. 貢献パイプラインと handoff 様式（トラック間の唯一の情報経路）

### パイプライン全体像（探索 → 検討 → 起票 → 運搬 → 実行 → 戻し）

```text
[McRemote側 scratch-editor セッション]（knowledge 可読）
  探す（公式 Issue・§7 の入口リスト・自分が遭遇したバグ）
  → 検討（公的価値・難度・policy 適合。private 文脈は票に書かない）
  → 貢献作業票を起票
[人間]＝一方向弁の担い手。票を contrib セッションへ運ぶ
[contrib セッション]（bootstrap＋票のみが根拠）
  実行（再現確認／修正＋PR／翻訳候補のローカル検証）
  → 成果は公式 venue へ（Issue コメント・PR・Transifex）
  → 票の「戻し報告」を追記
[人間] 票を持ち帰る → McRemote 側は学びと evidence ポインタだけ収容
```

- 探索は contrib 側でも可能（公式 venue は public なので一方向弁に触れない）が、優先順位の検討には文脈が要るため既定は McRemote 側。第一義がコミュニティ貢献なので、探索の起点は自分のバグより公式 Issue トラッカーを既定とする。

### 貢献作業票（汎用の運搬単位）

確認系・翻訳検証・調査も運べる汎用の票。修正+PR の場合は後述の「upstream貢献handoff」ブロックを背景に添付する。

```markdown
## 貢献作業票
- 票ID: C-YYYYMMDD-NN（人間採番）
- 対象: 公式 Issue URL / Transifex 対象 / その他
- 作業種別: 再現確認 / 修正+PR / 翻訳候補検証 / 調査報告
- 背景（public-safe のみ）:
- 期待する成果物: Issue コメント / PR / ローカル検証レポート
- 制約: policy 最新確認・branch は develop から・push は fork へ明示
- 完了条件:

### 戻し報告（contrib セッションが追記し、人間が持ち帰る）
- 実施内容:
- 成果物リンク:
- 未完・次の一手:
- 環境メモ（npm ci 実施等、次セッションが知るべきこと）:
```

### McRemote → 貢献（一般バグの引き渡し）

```markdown
## upstream貢献handoff
- 公式Issue URL:
- 公式developでの再現手順:
- Expected / Actual:
- ブラウザ・OS:
- 関係しそうなpackage:
- McRemote固有変更なしでも再現する根拠:
```

渡さないもの: McRemote の release 期限／McRemote 固有の実装案／private SSOT の設計理由／McRemote でだけ成立する期待挙動。

### 貢献 → 追従（公式マージ後の戻し）

```markdown
## 追従戻しhandoff
- upstream PR URL:
- merge commit:
- 変更package:
- 回帰リスク:
- McRemote側で確認すべき項目:
```

## 6. upstream watch（起案・実装は dev 側）

- 置き場所: **McRemote fork（`Naohiro2g/scratch-editor`）のみ**。貢献 clone・全体リリース計画側には置かない（watch は外部事実の観測記録であり、ナレッジの決定ではない）。
- トリガー: McRemote 版 Release 公開後／月2回／`workflow_dispatch`。
- 処理: 公式 `develop` fetch → ahead/behind・upstream HEAD・merge-base・新規 commit 一覧（bot/human 区別）・変更ファイル一覧・McRemote 変更箇所との重複・high-risk 領域検出（root package/lockfile・`.github/workflows`・scratch-gui/scratch-vm・serialization/.sb3・Blockly/spork・SVG/paint・localization・monorepo package 追加）。
- 出力: **単一 tracking Issue を更新し続ける**（毎回新 Issue は spam 化、Actions Summary は流れて参照不能）。
- 権限: `contents: read`＋`issues: write` のみ。`contents: write`／`pull-requests: write`／`deployments: write` は与えない。
- しないこと: **upstream の自動マージは不採用**（CI では live/browser 検証と採用タイミングを判断できない。ゲートは人間）。candidate branch の自動 push・Draft PR の自動作成・deploy・release 作成もしない。Draft PR 自動作成のみ、watch 運用と CI が安定した後に別途検討。

## 7. 貢献候補の入口（外部事実・鮮度注意）

Issue 番号は外部管轄の生き物。着手前に現況を必ず再確認する。分析の正典は各 Issue / PR 側に置き、ここは入口リストに留める。

- 低リスクの入口: scratch-editor #649（sprite duplication の code loss 解消確認）／#650（spork 期旧 project の load-time repair 後動作確認）
- 次の候補: #643（block input 内 Ctrl+A/C/V）／#547（angle picker 後に block が pointer へ張り付く）／#648（New Broadcast の表示順）
- 初回には重い: #601（local variable rename / data loss）／#633（backpack import 後の blank variable input）
- l10n は二経路を混同しない（2026-07-18 確認）:
  - **翻訳コンテンツ**: Scratch Foundation は翻訳を直接 PR で受け付けず、**Transifex 経由・言語ごとのチーム制・Scratch 側からの招待制**で受ける。運用者（Naohiro2g）は Transifex アカウント既保有で、2026-07-18 に Scratch チームへ参加済み＝翻訳貢献が可能な状態。contrib 環境でできるのはレポート収集と翻訳候補のローカル検証まで、提出は Transifex 側で行う。
  - **基盤ツーリング**: scratch-l10n #792 の follow-up（daily pull timeout・Transifex 並列数制限・translation key の ID 化）。認証情報・定期運用に関わるため、**実装前に maintainer へ外部 PR 可否を確認**。

## 8. 実装バックログ（dev 側へ戻す候補）

- McRemote 側: `.github/workflows/upstream-watch.yml` 実装／権限・Issue 出力の検証／初回 watch 実行／repo 固有指示の必要最小限の更新／追従 branch・PR 運用の実装。
- 貢献側: bootstrap 投影の設置（`local-bootstrap_ja.md` 書き込み・`.git/info/exclude` 登録）／専属セッション開始（開始定型文の運用）／#649・#650 の再現確認／Issue への結果報告／maintainer へ次候補の着手可否確認／公式 `develop` 基準の test・修正・PR。
- 全体リリース計画側: 本文書からは変更しない。追従側から準備状態が報告された時点で、既存計画に従い採用時期だけを判断する。

## 9. scratch-plan §2.9 との関係

§2.9 の本質——追従困難の原因は経過時間でなく**衝突する変更量**、「upstream と同じ場所を触らない設計」が本質で頻度はその次、改造の3カテゴリ管理（純粋追加／マーカー付き最小パッチ／改変の最小化）——を全面継承する。§2.9 の機構（branch 表・月1回定例フロー）は本文書へ委譲。branch 表の `upstream/main` は monorepo 移行後の実態（公式既定 branch `develop`）に合わせて本文書側で読み替え、追従 branch 運用の詳細は §8 の dev 側実装で確定する。
