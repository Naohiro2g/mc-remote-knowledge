# 周辺プラグインの互換性調査（knowledgeへ移管）

- 日付: 2026-10-18
- repo／surface: mc-remote-stack／Claude Code（Stack担当）
- 内容: 公開VPSで使っている10個の周辺プラグインとOtterLibについて、Paper 26.3対応の作者申告、公式JARのJava要件、26.3複製worldでの起動試験。dogfoodingの結果としてOSS利用者へ公開する情報で、private値は含まない
- 移管先: knowledge（公開）。正式なrecord／artifact／配置はknowledge担当が決める
- 入口: `materials/2026-10-17/PLUGIN_RESEARCH_ja.md`（最新）、`materials/2026-10-13/PLUGIN_COMPATIBILITY_ja.md`（作者申告の詳細と運用案）、`materials/2026-10-12/`（Java要件のJAR検査）
- 作成元: `handoff-materials/2026-10-12-b9-plugin-latest-check`、`2026-10-12-b9-plugin-update`、`2026-10-13-homepage-paper263`、`2026-10-17-b10-deployment`から非秘密の素材だけを複写。`preview-result.json`は`container_id`を除いた
- 含めないもの: 第三者のJAR本体（identityはSHA-256で各JSONに記録）、VPSのpath・host、backup ZIP、credential
- test class: author metadata／static（10/12、10/13）、live-auto（10/17の複製world試験）。live-humanは未実施
- 非確認: 実playerのlogin／pairing、DirectionHUDの実表示、backupからのrestore、各pluginのゲーム中の操作、XServer GAMEsの実機
- 全素材: `SHA256SUMS`
- 移管後: knowledgeで着地したら、この packet と作成元4件のうち調査部分は破棄してよい（private opsはbackstageへ収容済み）
