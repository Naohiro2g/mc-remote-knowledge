# 10-protocol（スポーク）

役割: protocol（プラグイン ↔ 各クライアントの通信契約）の設計記録・決定ログ。**この契約の SSOT**。バージョニング方式、protocol v1 仕様（hello / pair / 実行コマンド）、コマンド・エラーコード表を扱う。

protocol は plugin・python-client・scratch-client の3つにまたがる共有契約なので、各実装スポークから独立させてここに一本化する。実装側の決定は各スポーク（`11-plugin` / `12-python-client` / `13-scratch-client`）に置き、契約そのものはここを正とする。

このディレクトリは mc-remote-knowledge のスポーク。`00-hub/` の方針（全体計画・理念・全体アーキテクチャ）に従う。

横断的な影響を持つ決定（複数ワークストリームに波及するもの）は、ここに書くと同時に `00-hub/DECISIONS_ja.md` に1行追記する。
