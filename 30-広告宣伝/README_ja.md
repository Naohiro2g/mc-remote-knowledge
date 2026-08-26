# 30-広告宣伝（スポーク）

役割: 広告・マーケティング・公開戦略の記録・決定ログ。記事の公開シーケンス、ビルド・イン・パブリックの方針、ターゲット読者の設計などを扱う。

このディレクトリは mc-remote-knowledge のスポーク。`00-hub/` の方針（全体計画・理念・全体アーキテクチャ）に従う。

横断的な影響を持つ決定（複数ワークストリームに波及するもの）は、ここに書くと同時に `00-hub/DECISIONS_ja.md` に1行追記する。

## 2027年4月までの公開準備track

広告宣伝はproduct releaseやR3と別の並走trackです。ただし、外部testerが自力で検証を開始するための
情報は単なる宣伝ではなく利用可能性の一部です（`2026-08-26-09`）。

### Homepage

2026年9月から次を段階的に整えます。

- 基本情報: McRemoteとは何か、対象者、できること、できないこと
- project詳細: 構成component、Python／Scratch、WireScope、機能実現の三層モデル
- roadmap: beta／rc／stable、Minecraft／Paper対応、2027年4月までの粗い時間軸
- release情報: exact version、対応版、導入、update／rollback、既知制約、feedback入口

10月rcの外部test開始時点では、少なくともrelease情報と検証参加導線を会話履歴なしで辿れる状態にします。
homepage全体の完成、SEO、記事本数はrc／stable blockerにしません。

### Release notes

Gemini Notebook等を使う場合は、knowledge SSOTのsource commit、release差分、正式evidenceを入力にした
半自動の草稿生成として扱います。生成物を独立正本にせず、同じsourceから再生成できる投影とし、対応版、
breaking change、既知制約、non-claimを人間が確認してから公開します。AI出力を無確認で公開しません。

### 技術記事

release告知と技術解説を分けます。記事候補は、protocol majorを正直に上げた理由、機能実現の三層モデル、
Scratch browser保存、WireScopeによる観察、ケータリングPCのupdate／rollback経験です。記事公開は
build-in-publicと学習支援の入口ですが、本数をproduct completionへ換算しません。
