# 公式ホームページ（mc-remote.com）情報アーキテクチャ・導線設計

## 1. 目的と位置づけ

`mc-remote.com` は、マイクラリモコン（mc-remote / Code2CreateClub）の**「正面玄関（Showcase / Projection Layer）」**です。8歳から80歳までの初学者、保護者、教育関係者、および導入検討者が最初に訪れる場であり、難解な内部事情や契約文書を押し付けず、直感的にプロジェクトの魅力・始め方・全体像を伝える役割を担います。

設計記録や判断理由の唯一の真実の源（SSOT）である本ナレッジリポジトリ（`mc-remote-knowledge`）に対し、ホームページは**「SSOTから合意事項を抽出し、利用者の目線に合わせて平易に投影した表現層」**として位置づけられます。

---

## 2. ドメイン集約とサブドメインの規律（`github.mc-remote.com` の扱い）

- **完全手動の独立した別サイトは作成しない**:
  過去の初期メモに存在した「プロジェクトのリポジトリハブ（`github.mc-remote.com`）」について、独立した手動Webサイトとしての運用は廃止・却下する。リポジトリやリリースの変更に伴う手動更新の二重管理（ドリフト）を防ぎ、利用者の導線分断を解消するため、エコシステム案内は `mc-remote.com` 本体内に統合する。
- **サブドメインのエイリアス化**:
  `github.mc-remote.com` は独立Webサイトを配置せず、GitHubのプロジェクトトップ（`https://github.com/Naohiro2g`）への直リダイレクト（エイリアス）として扱う。

---

## 3. ホームページ（`mc-remote.com`）の6大構成要素

```text
mc-remote.com
├── ① ヒーロー & 最短接続ガイド（Scratch / Python / 箱庭サーバー接続の第一歩）
├── ② プロジェクトの起源とミッション（先人の功績・学びの支援哲学）
├── ③ 学習カリキュラムの全体像（使う側から、OSSを創る・開発する側へ）
├── ④ 各リポ案内 / エコシステム（Scratch, Python, Plugin, WireScope, Java, C#, Stack, Knowledge）
├── ⑤ 開発ロードマップ & 進捗状況（現在地 R3/b7、2027年春までの時間軸）
└── ⑥ 横断リリースノート & 互換性情報（動作確認マトリクス、過去のb1〜b6変遷）
```

### ① ヒーロー & 最短接続ガイド（First View）
- **キャッチコピー**: 「マインクラフトの世界を、コードで動かそう。」
- **Scratch版**: Web版エディタ（`https://scratch-beta.mc-remote.com/`）への直接リンクと、箱庭サーバー（`sb-beta.mc-remote.com`）の接続手順（推奨Java版1.21.1、統合版ポート`25565`、統合版更新直後の注意）を併記。
- **Python版**: `pip install minecraft-remote-api` と、建築原点（`setBuildOrigin`）・位置設定（`setPos`）・ブロック設置（`setBlock(5, 67, 5)`）を含む最小3ステップコード。

### ② プロジェクトの起源とミッション（About & Mission）
- **先人の功績への敬意**:
  - `RaspberryJuice` (zhuowei氏)
  - `mcpi` (Martin O'Hanlon氏)
  - `JuicyraspberryPie` (wensheng氏)
- **教育哲学**: 知識注入型の「教育（EDUCATION）」ではなく、学習者が自ら探究し創り出す「学びの支援（SUPPORT LEARNING）」。MITメディアラボ ライフロング・キンダーガーテン（Dr. Mitchel Resnick）の精神を継承。
- **明確なミッション**: 初学者の自立的な探究学習アプローチの獲得支援。
  - コーディングの本質概念と技術
  - Git/GitHubを活用したオープンソース開発技術
  - 自分のアイデアを実現・表現する力

### ③ 学習カリキュラムの全体像（使う人から、創る人へ）
- **Level 1（体験と観察）**: Scratchでブロック設置・チャット送信、WireScopeで通信パケット観察
- **Level 2（論理と自動化）**: Scratchでループ・条件分岐・関数化による自動建築
- **Level 3（本格開発への跳躍）**: Pythonコードへの移行、環境アダプターと自動補完の獲得
- **Level 4（空間・数理・応用）**: 3D幾何学、パーティクル、ミニゲーム、AI・画像認識連携
- **Level 5（開発者・貢献者へ）**: **`minecraft-remote-api`（クライアント）や `McRemote`（プラグイン）自体の機能拡張・不具合修正（OSSコントリビューション）**

### ④ 各リポ案内 / エコシステム
- `scratch-editor`: ブラウザ完結ビジュアルプログラミング
- `minecraft-remote-api`: 型補完と標準APIを備えた公式Pythonライブラリ
- `McRemote`: PaperMCサーバー対応のJSON-RPC 2.0接続エンジン
- `wirescope`: 通信内容を可視化する観察・学習ツール
- `minecraft-remote-java`: Javaクライアント
- `csharp-client`: Unity等の3D環境向けC#クライアント（※旧プロトコル対応）
- `mc-remote-stack`: 教室・VPS向けサーバー自動構築・運用パッケージ
- `mc-remote-knowledge`: システム全体の真実の源（SSOT）

### ⑤ 開発ロードマップ & 進捗状況
- 現在地: **R3（学べる・教えられる）進行中 / b7 公開中**
- タイムライン:
  - 2026年9月: b7 / b8（機能拡充、月末API freeze）
  - 2026年10月: RC（外部テスター検証、Paper 26.2/26.3対応）
  - 2026年11月: 初回 Stable リリース
  - 2027年春: 新学年・教室本番導入

### ⑥ 横断リリースノート & 過去の履歴
- 動作確認済みバージョン対照表（Plugin × Python × Scratch × WireScope × Paper/Minecraft）。
- 過去のリリース変遷（アコーディオン形式で展開可能）：
  - b7: direction、lightning、WireScope detached ZIP同梱
  - b6: 看板API、ツルハシイベント（pickaxe_poke）
  - b5: 構造化ブロック値（block_idとstate分離）、DimensionKey統一
  - b4: 建築原点とプレイヤー識別の完全分離（setWorld / setBuildOrigin）、paired pose
  - b3: 生きたカタログ補完（mc_constants生成）
  - b2: トークン認証・ペアリング機構（/mcremote pair）
  - b1: JSON-RPC 2.0ワイヤ形式確定

---

## 4. ナレッジリポ（SSOT）との連携・反ドリフト規律

1. **真実の源はナレッジリポ**: ホームページ上で新しい仕様・決定を直接作らない。必ずナレッジリポで合意・決定（DECISIONS）された内容を要約・投影する。
2. **Deep-hidingの徹底**: SHA-256ハッシュ値、内部のライセンス論争、過渡期の失敗や試行錯誤はナレッジリポに留め、ホームページには表出させない。
3. **更新フロー**:
   - 新しいリリースや方針確定時、ナレッジリポの `00-hub/DECISIONS_ja.md` や `release-gate-notes_ja.md` を更新後、ホームページの対応セクション（リリース表、ロードマップ）を追従更新する。
