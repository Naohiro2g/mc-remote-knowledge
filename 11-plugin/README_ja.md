# 11-plugin（スポーク）

役割: McRemote プラグイン（`Naohiro2g/McRemote`、PaperMC サーバー側本体）の設計記録・決定ログ。mod 展開（NeoForge / Forge / Fabric、Architectury、モノリポ構想）、認可（LuckPerms / PermissionProvider）、pair / token のサーバー側正本を扱う。

通信契約（protocol）そのものは `10-protocol/` を正とし、ここはサーバー側の実装・判断を置く。

このディレクトリは mc-remote-knowledge のスポーク。`00-hub/` の方針（全体計画・理念・全体アーキテクチャ）に従う。

横断的な影響を持つ決定（複数ワークストリームに波及するもの）は、ここに書くと同時に `00-hub/DECISIONS_ja.md` に1行追記する。
