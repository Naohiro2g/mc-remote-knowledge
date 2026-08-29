# 10-protocol（スポーク）

役割: protocol（プラグイン ↔ 各クライアントの通信契約）の設計記録・決定ログ。**この契約の SSOT**。バージョニング方式、protocol v1 仕様（hello / pair / 実行コマンド）、コマンド・エラーコード表を扱う。

protocol は plugin・python-client・scratch-client の3つにまたがる共有契約なので、各実装スポークから独立させてここに一本化する。実装側の決定は各スポーク（`11-plugin` / `12-python-client` / `13-scratch-client`）に置き、契約そのものはここを正とする。

このディレクトリは mc-remote-knowledge のスポーク。`00-hub/` の方針（全体計画・理念・全体アーキテクチャ）に従う。

横断的な影響を持つ決定（複数ワークストリームに波及するもの）は、ここに書くと同時に `00-hub/DECISIONS_ja.md` に1行追記する。

ブロックID／stateの構造化値、set／get対称性、Python／Scratch／将来言語への投影は
[ブロック値・状態・多言語投影設計](block-value-design_ja.md)を人間向け説明正本とする。

旧b6 scopeの概念別分割、method成熟状態、Paper 26.x対応、rc／初回stableへの日程は
[betaから初回stableまでのreleaseロードマップ](beta-to-stable-release-roadmap_ja.md)を参照する
（DECISIONS `2026-08-26-08`）。

Java bootstrapを起点に、developer experience評価、Python／Java比較、既存conformance資産の一般化、
TypeScript／browser／C#展開へ進む横断順序は
[多言語Client Library / Protocol-firstロードマップ](polyglot-client-roadmap_ja.md)を参照する
（DECISIONS `2026-08-29-05`）。

b6 source candidateのTier 2入口で使うcanonical case、三repoの既存test対応、fixture化前のgapは
[b6 compatibility fixture計画](b6-compatibility-fixture-plan_ja.md)を参照する。

共有fixture収束後に生成した未公開candidate artifactのexact name／size／SHA-256、source、再現性、
non-claimは[b6 artifact candidate記録](b6-artifact-candidate-record_ja.md)を参照する。
