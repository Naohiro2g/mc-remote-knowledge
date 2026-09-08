# マイクラリモコン (mc-remote) ナレッジベース

> **人間とLLMが「学びながら開発し、共創する」ためのナレッジベース型開発システム**

マイクラリモコン（mc-remote / Code2CreateClub）は、Minecraft（Java版）をScratchやPythonからプログラミング・遠隔操作できるオープンソース環境です。

このリポジトリ（`mc-remote-knowledge`）は、プロジェクト全体の**設計記録、横断決定、現行規約を公開・管理する唯一の真実の源（SSOT: Single Source of Truth）**です。実装コードは各開発リポジトリに置き、このリポでは「何を、なぜ、どの境界で決めたか」を記録しています。

また、マイクラリモコンは**「LLM支援ナレッジベース型開発システム」**の実践例でもあります。ソフトウェアを使う学習者だけでなく、**「人間とAIがどう協調して大規模なシステムを破綻なく共創・学習していくか」という開発システム自体も学習パス（学びの対象）**として位置づけられています。

---

## 🚀 あなたの目的に合わせた最短入口

### 1. マイクラをプログラミングで動かしたい（学習者・子ども・教育関係者）
- 🐱 **Scratchで動かす**: ブラウザから即座にブロックプログラミングでマイクラの世界を動かせます。  
  👉 [scratch-editor (GitHub)](https://github.com/Naohiro2g/scratch-editor) / [Web版エディタ](https://scratch-beta.mc-remote.com/)
- 🐍 **Pythonで動かす**: わずか3行のコードでブロック設置やチャット送信ができます。  
  👉 [minecraft-remote-api (GitHub)](https://github.com/Naohiro2g/minecraft-remote-api)
- 🎮 **作品サンプル・作例を見る**: 建築、ドット絵、ミニゲームなどの動くコード集。  
  👉 [mc_remote_samples (GitHub)](https://github.com/Naohiro2g/mc_remote_samples)
- 🏰 **サーバーを立てたい**: 教室や自宅でサーバーを構築・運用するパッケージ。  
  👉 [mc-remote-stack (GitHub)](https://github.com/Naohiro2g/mc-remote-stack) / [McRemote Plugin (GitHub)](https://github.com/Naohiro2g/McRemote)

### 2. 人間×LLMの開発システムを学びたい（エンジニア・開発者・AI共創学習者）
「AIに丸投げして破綻するのではなく、人間が意思決定の主権を握りながら、LLMの爆発的な推論・実装力を活かす仕組み」を学べます。
- 📖 **学習と開発の思想**: なぜ言語化より先に「観察」から入るのか？  
  👉 [AIアシストと学習支援 (ai-learning-design_ja.md)](20-教材/ai-learning-design_ja.md)
- 🏗️ **ナレッジベース構造**: ハブ＆スポーク構造、文書三層モデル（拘束・説明・投影）  
  👉 [ナレッジリポジトリ設計 (knowledge-repo-design_ja.md)](00-hub/knowledge-repo-design_ja.md)
- 📜 **意思決定の記録（SSOT）**: 結論・理由・却下案を消さずに残す「追記只進」の規律  
  👉 [横断決定ログ (DECISIONS_ja.md)](00-hub/DECISIONS_ja.md)
- 🧭 **ドキュメントの書き方**: 「文書は説明し、台帳が拘束する」  
  👉 [説明文書の様式ガイド (document-style-guide_ja.md)](00-hub/document-style-guide_ja.md)

---

## 💡 システムの最上位動作原理（エッセンス）

本システムは、教材開発から実開発・検証・運用まで、一貫して以下の原理で運用されています。

1. **正典順序：観察 → 痕跡を残す → 言語化 → 比較・検証 → 自己判定 → 共有・再検証**  
   言語化を最初の入場条件にしません。まず動かし、観察し、痕跡を残すことから始めます。
2. **委譲と責任：未検証の正しさや設計判断をLLMに代行させない**  
   コード生成はAIに委譲しても、判断・検証・統合の責任は人間が握ります。証拠のスコープを超えて確約しません。
3. **判断理由を残す：結論・理由・却下案をセットで記録する**  
   方針変更時も過去の判断を上書きで消さず、新しい決定を追記して参照で繋ぎます。
4. **メタ判断と跳躍：疑う規律と跳ぶ直感の両方を置く**  
   過去の決定が今も最適かを常に問い直す（メタ判断）と同時に、根拠が薄くても直感で踏み出す跳躍を排除しません。
5. **不要な禁止ルールを作らない（`2026-09-04-05`）**  
   局所最適による禁止ルールの増殖を防ぎ、誤りと判明したルールは判断履歴を残したまま現行拘束から外します。

> より深い運用哲学や設計背景は [knowledge repository design](00-hub/knowledge-repo-design_ja.md) および [CLAUDE.md](CLAUDE.md) を参照してください。

---

## 📂 リポジトリの構造（ハブ & スポーク）

```text
00-hub/            全体原理・索引・横断決定・開発プロトコル
10-protocol/       サーバープラグインとクライアント間の通信仕様（Protocol）
11-plugin/         Paper サーバープラグイン（McRemote）の設計
12-python-client/  Python クライアントライブラリの設計
13-scratch-client/ Scratch エディタ拡張・Bridge の設計
14-evidence/       実機テスト・検証ログ
15-wirescope/      通信パケットをリアルタイム可視化する観察UI
16-java-client/    Java クライアントライブラリの設計
20-教材/           学習支援・教育設計・チュートリアル設計
30-広告宣伝/        公開戦略・発信
```

## 🗺️ 主な案内（入口）

- [INDEX](00-hub/INDEX_ja.md) — 全ドキュメントの総合目録
- [DECISIONS](00-hub/DECISIONS_ja.md) — プロジェクトの横断決定ログ（SSOT）
- [NOTES](00-hub/NOTES_ja.md) — 未確定の芽・未解決の課題
- [グランドデザイン](00-hub/grand-design-roadmap_ja.md) — プロジェクト全体の長期展望
- [README・sample近代化ロードマップ](00-hub/readme-sample-modernization-roadmap_ja.md) — 各リポの人間向け入口整備方針
- [CONTRIBUTING](CONTRIBUTING.md) — コントリビューションの手引き
- [SECURITY](SECURITY.md) — セキュリティ報告窓口

---

## 📦 関連リポジトリ一覧

| リポジトリ | 役割 | リンク |
| --- | --- | --- |
| **`minecraft-remote-api`** | Python クライアント（`pip install minecraft-remote-api`） | [GitHub](https://github.com/Naohiro2g/minecraft-remote-api) |
| **`scratch-editor`** | Scratch 3.0 ベースのマイクラプログラミング環境 | [GitHub](https://github.com/Naohiro2g/scratch-editor) |
| **`mc_remote_samples`** | 多言語対応の作例・サンプルコード集 | [GitHub](https://github.com/Naohiro2g/mc_remote_samples) |
| **`McRemote`** | Minecraft Paper サーバー用プラグイン | [GitHub](https://github.com/Naohiro2g/McRemote) |
| **`mc-remote-stack`** | サーバー環境デプロイ・Dockerパッケージ | [GitHub](https://github.com/Naohiro2g/mc-remote-stack) |
| **`minecraft-remote-java`** | Java 向けクライアントライブラリ | [GitHub](https://github.com/Naohiro2g/minecraft-remote-java) |

---

## ライセンス

オリジナルの文書・図・教育資料は [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/)、プロジェクト所有コードは原則 [MIT License](LICENSE.md) です。
Scratch Editor や WireScope 等の個別コンポーネント固有のライセンスについては各リポジトリの `LICENSE` を参照してください。詳細は [LICENSE.md](LICENSE.md) を確認してください。
