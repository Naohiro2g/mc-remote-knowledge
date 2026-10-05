# b8公開VPS配備・独立ランスルーと手順補強

## 確定搬送票

- 搬送元 repo: Naohiro2g/mc-remote-stack
- 搬送元 surface: Codex
- 搬送元 branch/commit: 配備・ランスルーに使ったmainは`6cdbe6e2f8bc654a3d21a6119de6c4154a559afc`（Stack #66 merge）。手順補強は`agent/scratch-notice-runbook`／`ae3288a390d73292d3fe396cf9e27ff1dbaadae0`、mainへのmergeは`68b8d45af743cd56b70efe67a42e1e162b04c50c`（#65）。検証済みheadとmergeのtreeは一致
- 作成日: 2026-10-05
- 種別: その他（release後の配備検証結果と手順への反映。release gateの再判定ではない）
- 決定: 正式b8を10月3日に公開VPSへ配備。10月5日には会話履歴を共有しない別セッションがmainの公開手順・SSOT・private ops情報から別deploymentを構築して同じ公開入口へ切り替えた。停止時保存・データ引継ぎ・doctor・外部接続・実backup転送・人間提供結果を確認した。実行漏れと未試験範囲を区別し、漏れに対応する手順をStack #65へ収容した
- 理由: 会話中に共有した認識だけで配備が成立していないかを別セッションの実作業で確認するため。何が起きたか、どの段階が成功したか、人間に確認すべき内容を手順から追えるようにするため
- 却下案（3件まで）: なし
- 影響: Stack公開runbook、Knowledgeのrelease後検証要約、private operationsの現在地。ホームの未統合PRとプラグイン管理は後続Stack担当の別作業
- 根拠/検証: 初回配備のKnowledgeは`2a8c3eae4e489e67f044111b0d1e6cdd22ead86a`、独立ランスルーは`561de98b5c15864ac9b86cb6dcaeef1f20ce635b`。今回はremote main `099c40b0c312694712653885200f3114ea4bed33`のruntime／INDEX／release責務／deployment interfaceとevidence INDEXを確認。live-autoは担当の実施報告、live-humanは人間のtranscript・報告を素材にする。後続read-only観測でoperator／doctor正常、homepage全79source一致。#65最終headのuv sync／全368pytest／Ruff／diff check PASS。正式Knowledge record／artifactとそのcommitは未作成
- 既に変更した実装/文書: Stack #66と#65はmainへ統合済み。#65はnotice一時ファイル編集、準備でのnotice事前提示・選択、停止／起動の進行報告、ServerBackup生成時のruntime UID確認とconsole入口を収容。自動復旧やプラグイン管理機構は追加していない。private opsはBackstage #18と#19へ統合済み。#19 mergeは`17024231378265b9cca0d79ec8e448295483198c`、homepageは10月4日ceba530・79ファイルへ訂正済み
- ナレッジ着地希望: 10月3日の配備と10月5日の独立ランスルーを実施日・参照commit・test classで区別して収録する。既存b8-dev-liveとの重複はKnowledge担当が照合する。noticeのユーザー確定方針は下記を既存deployment interfaceと照合して捕捉する。正式record／artifact／INDEX／redactions.jsonのauthoring・配置・commitはKnowledge担当
- 捕捉 cleanup: 公開可能な選択済み素材を[knowledge-materials](knowledge-materials/materials-index.json)へまとめた。既存16handoffは[review第5節](review_ja.md#5-このセッションの素材分類)で①Knowledge昇格素材／②後続担当と参照identityを伴う移管へ分類済み。private opsの現在地はBackstageのマージ済み記録を入口とする。元のignored資料を正式evidenceとして引用しない。素材破棄は今回行っていない
- 着地後の確認戻り先: Stack担当。この票、[completion-checks.json](completion-checks.json)、[CLOSE_ja.md](CLOSE_ja.md)、root NOTESの「2026-10-05 残件の実施・マージとKnowledge搬送」へ、push済みKnowledge commitとrecord／artifact／INDEXの着地先を返す

## 選択済み素材

- [runtime-summary_ja.md](knowledge-materials/runtime-summary_ja.md): 初回配備と独立ランスルーの確認範囲、実行漏れ、未試験範囲、手順への反映
- [2026-10-03-human-check_ja.md](knowledge-materials/2026-10-03-human-check_ja.md): 初回配備のペアリング／hello／chat、人間のiPad world参加報告
- [2026-10-05-human-check_ja.md](knowledge-materials/2026-10-05-human-check_ja.md): 独立ランスルーのhello／chat transcript。画像記載は担当報告の要約で、画像実物は含めていない
- [release-intake.json](knowledge-materials/release-intake.json): 取得・照合した正式b8 manifestと配布物の公開identity。Pythonはrelease照合のみ
- [validation-summary_ja.md](knowledge-materials/validation-summary_ja.md): 後続の文書・記録訂正の検証
- [materials-index.json](knowledge-materials/materials-index.json): 上記素材のSHA-256・size・出所。private host、token、UUID、world／credential／TLSの実データ、未確認画像、raw server logは選択素材へ含めていない

正式evidenceの命名提案: `14-evidence/records/2026-10-05-b8-public-vps-runthrough_ja.md`、対応する`14-evidence/artifacts/2026-10-05-b8-public-vps-runthrough/`。初回配備との分割・既存evidenceへの接続を含めKnowledge担当が確定する。未作成のpathであり正式証拠へのリンクではない。

## noticeのユーザー確定方針

製品noticeと運用者noticeの二系統を維持する。b8配布製品noticeは継続する。ユーザーは開発元noticeをテンプレート／サンプルに近いものとして考えていたが、必要時に開発元から固定表示できる仕組みを残すことを確認した。b9では製品versionとreleaseページへのリンクを持つ一entryに絞る方針をScratch担当へ渡し、追加topicは運用者がデプロイ時の編集phaseで用意する。

この票はb9製品内容を再検証したものではない。初回b8配備では承認文面を採用済み。10月5日の再構築は既存文面を引き継いだが、人間へ提示して選んでもらう段階を漏らした。事後表示成功で事前確認を実施済みに置き換えない。後続#65で準備段階へ明示的に接続した。

## 未試験・未提供

10月5日のauth.*中間transcript、ゲームedition別の参加内訳、フルWireScope操作は未提供。初回配備のiPad参加を独立ランスルーで再試験したとは扱わない。backupは生成・CRC・内容検査・暗号化・off-host再取得hash一致／download-verifiedまでで、復号・world復元・切戻しは未試験。修正手順を使う新たな実機ランスルーは行っていない。
