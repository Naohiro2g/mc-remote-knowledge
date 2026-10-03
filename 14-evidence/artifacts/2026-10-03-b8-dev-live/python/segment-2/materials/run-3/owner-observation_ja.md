# Python segment 2 残り専用run 3のhuman WireScope観測

- 日付: 2026-10-03
- 観測者: human release owner（プロジェクトオーナー）
- 方法: Python同梱WireScopeをownerの実browserで開いて確認。agentのbrowser自動操作／screenshotは使用していない。
- identity: exact set `b8-integrated-artifact-set-1`、Python `52d35f5304e62f465c1f47ab47c00fe9bcf62470`、CI wheel SHA-256 `dcedff010feac0d5df24ff85dd84b321fb819f78563c39431ac32d9d75bc0180`。runner SHA-256 `c001bd5cbc8ab8b5151133c995dec4f226d82f4b9ac83f786a2e9797574a5c7c`。
- ownerは「準備できた。新runnerで再開」と回答。起動後にWireScopeからhello frame 1〜2を貼り付け。runnerでもbrowser attach成立を確認してからbodyへ進んだ。
- 続いてownerがWireScope frame 1〜50をpayload付きで貼り付け。以下のgetBlock受信payloadと、playBlockSound 5kindの各3制御・Python既定呼出の送受信を確認できた。対応するsanitized observer原本は同directoryの`frames.jsonl`。

| WireScope frame | ownerの貼り付けで確認した内容 |
| --- | --- |
| 1〜2 | hello protocol23.2.0／MC1.21.11 |
| 9〜10 | 元block取得。`{"result":{"block_id":"minecraft:air","state":{}}}` |
| 11〜14 | 無印stoneを設置し、`{"result":{"block_id":"minecraft:stone","state":{}}}`を読み戻し |
| 15〜20 | kind=place、options省略／pitch=0.75・self／note=18・world、各result:null |
| 21〜26 | kind=hit、同3制御、各result:null |
| 27〜32 | kind=break、同3制御、各result:null |
| 33〜38 | kind=step、同3制御、各result:null |
| 39〜44 | kind=fall、同3制御、各result:null |
| 45〜46 | Python既定呼出hit。optionsはreceiver:worldのみ、volume／pitch／noteなし、result:null |
| 47〜50 | 元のairへ復元し、`{"result":{"block_id":"minecraft:air","state":{}}}`を読み戻し |

送信optionsの代表（owner貼り付け）:

```json
{"params":[3,1,0,"place"]}
{"params":[3,1,0,"place",{"pitch":0.75,"receiver":"self"}]}
{"params":[3,1,0,"place",{"note":18,"receiver":"world"}]}
```

- graph: 凍結sampleの81往復（frame51〜212）はrunnerでPASS。ownerが実browserからframe113〜212をpayload付きで貼り付け、dust／receiver:selfの送信と各result:1の受信表示を確認できた。human貼り付けが示す範囲は113〜212であり、51〜112の全行をhumanが個別に確認したとは主張しない。sanitized observer原本には81往復すべてを保持。
- 終了: 上記表示確認後にfinish checkpointを通し、runnerはPASS・exit0で終了。仮blockは元のairへ復元／読み戻し済み、station／Minecraft connectionは正常close。
- 非主張: SoundGroupのserver内部数値、2-playerのreceiver差、描画、聴取、音の定位。WireScopeのframe表示確認と、これらの意味・知覚の試験を混同しない。
- token、pairing_id、private endpoint、player UUID、表示用attach codeをこの素材へ保存していない。正式evidenceのauthoring／配置はknowledge担当。
