# 13-scratch-client（スポーク）

役割: Scratch クライアントの設計記録・決定ログ。改造版 Scratch Editor（`Naohiro2g/scratch-editor`）・wss ブリッジ・認証（pair / token）・作品保存／移送・追従戦略を扱う。

このディレクトリは mc-remote-knowledge のスポーク。`00-hub/` の方針（全体計画・理念・全体アーキテクチャ）に従う。

横断的な影響を持つ決定（複数ワークストリームに波及するもの）は、ここに書くと同時に `00-hub/DECISIONS_ja.md` に1行追記する。

現行の Scratch release scope と R3 作業束は
[scratch-roadmap_ja.md](scratch-roadmap_ja.md) を正本とする。
[scratch-plan_ja.md](scratch-plan_ja.md) は原点文書であり、現行 scope の根拠には使わない。

Scratch imageのproduct config、deployment runtime config、Stackへのcontract handoff、通常operator経路は
[Scratch–Stack deployment interface設計](../00-hub/deployment-interface-design_ja.md)を正とする。Scratch担当は
Stack内部を調査せず、Stack担当はscratch-editorが公開するcontract directoryだけを入力にする。

作品共有の責任分界、ブラウザ保存作品／スプライト、`.sb3`／`.sprite3`、OS clipboardによる
ブロック移送は [Scratch作品の保存・移送設計](scratch-project-storage-transfer-design_ja.md) を参照する。
McRemoteは一般UGC hostingと一般利用者accountを所有しない（`2026-08-16-01`〜`03`）。

protocol 22の構造化block valueと、スプライトごとの`ブロック情報`／ID／state reporterは
[ブロック値・状態・多言語投影設計](../10-protocol/block-value-design_ja.md)を参照する。
Scratch-visibleなStateText／BlockInfoText、Picker、`⟦mcr-error:<reason>⟧`は
[Scratch block value投影設計](scratch-block-value-projection-design_ja.md)を正とする。
