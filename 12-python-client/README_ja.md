# 12-python-client（スポーク）

役割: Python API クライアント（`Naohiro2g/minecraft-remote-api`）の設計記録・決定ログ。`param_mc_remote` / `mc_constants.py` 自動生成、版依存リソース（世界定数・block/entity/particle の ID カタログ）の生成・フォールバック・配布方式を扱う。

通信契約（protocol）そのものは `10-protocol/` を正とし、ここはクライアント側の設計・判断を置く。実装の正本は `Naohiro2g/minecraft-remote-api` dev リポとし、本リポへスナップショットを複製しない。

このディレクトリは mc-remote-knowledge のスポーク。`00-hub/` の方針（全体計画・理念・全体アーキテクチャ）に従う。

横断的な影響を持つ決定（複数ワークストリームに波及するもの）は、ここに書くと同時に `00-hub/DECISIONS_ja.md` に1行追記する。
