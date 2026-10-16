# b10 Scratch Local：WireScope同梱candidate

- knowledge contract commit: `8c3a31a967731a81c91645b08ecff62f620d0fe4`
- 根拠: DECISIONS `2026-10-09-01`、release-gate-notes b10「初回のlive-human」「次の操作（2026-10-09）」、b10-after-first-live.md
- source: `agent/b10-scratch-local@ec29372dadac9c51b2812c746e72032d48d987b6`（push済み）
- CI run `37933218014`、artifact ID `11616819485`、1362315280 bytes、`sha256:f747f3b537b060aacfa24bbcdbc1e42575169d7cd11b5d3219fdb6a7c0767159`
- 内容: 固定版WireScope appとdetached manifest／ライセンスを3 OS ZIPへ同梱。別loopback originで配信しruntime configへURLを設定
- 検証: local:test Node13＋Python8＝21 PASS、local:lint PASS。CI全工程PASS、Linux実ZIP試験PASS。artifact本体と全manifest hash、3 OSの内包identity／WireScope／Node・Bridgeの同一性を照合PASS
- 返却: `materials/CONFIRMATION_ja.md`。機械identityは`materials/ZIP_IDENTITIES.json`
- 正式evidenceのauthoring／収容と横断gate判定はknowledge coordinatorへ返す。tag／Release／shared deploy／人間参加試験なし
