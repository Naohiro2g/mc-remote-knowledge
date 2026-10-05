# human ownerによるWireScope表示の観測

- 日付: 2026-10-05 JST
- test class: `live-human`
- 観測者: プロジェクトオーナー
- source: 実際のWireScope表示から、human ownerがこのPython sessionへ貼り付けたframe 1〜22
- human操作: 新規pairing承認、WireScope attach、Minecraftで`b9-python-live`を送信、下記frameを提示
- 判定範囲: 全代表操作の送受信frameとpayloadが表示された。音の聴取・定位、particleの描画品質は今回の主張に含めない
- agentはブラウザーを自動操作していない。実際に表示された内容の根拠は以下のhuman提示

```text
1	08:29:29	送信	hello	{"params":{"protocol":"23.2.0"}}
2	08:29:29	受信	hello	{"result":{"protocol":"23.2.0","mc_version":"1.21.11","supported_mc_versions":["1.21.11"],"catalog_hash":"6d0f8524b70e37fb8d7b34d0fdb45c2b058dcfea82920d86ca9aaabb9fcadc83","dimension":"minecraft:overworld","origin":[200,0,200],"world_constants":{"y_sea":62},"permissions":{"online":true,"offline":true,"build_range":1000}}}
3	08:42:17	送信	chat.post	{"params":["[b9 Python] representative round trip"]}
4	08:42:17	受信	chat.post	{"result":null}
5	08:42:17	送信	events.poll	{"params":[0,{"max_events":32}]}
6	08:42:17	受信	events.poll	{"result":{"events":[{"sequence":1,"type":"chat_posted","dimension":"minecraft:overworld","origin":[200,0,200],"message":"b9-python-live"}],"through_sequence":1,"latest_sequence":1,"filtered_out":0,"overflow_dropped_total":0,"capacity_dropped_total":0,"explicitly_discarded_total":0}}
7	08:42:17	送信	player.getPos	{"params":[]}
8	08:42:17	受信	player.getPos	{"result":{"dimension":"minecraft:overworld","pos":[-16.538,120.499,12.869]}}
9	08:42:17	送信	build.setDimension	{"params":["minecraft:overworld"]}
10	08:42:17	受信	build.setDimension	{"result":{"dimension":"minecraft:overworld","origin":[200,0,200]}}
11	08:42:17	送信	build.setOrigin	{"params":[183,120,212]}
12	08:42:17	受信	build.setOrigin	{"result":{"dimension":"minecraft:overworld","origin":[183,120,212]}}
13	08:42:17	送信	world.spawnEntity	{"params":[2,1,2,"cow"]}
14	08:42:17	受信	world.spawnEntity	{"result":"mcr_eh_x09LV9iBC8PC7BIsGESkig"}
15	08:42:17	送信	entity.getPose	{"params":["mcr_eh_x09LV9iBC8PC7BIsGESkig"]}
16	08:42:17	受信	entity.getPose	{"result":{"dimension":"minecraft:overworld","pos":[2,1,2],"yaw":0,"pitch":0}}
17	08:42:17	送信	entity.remove	{"params":["mcr_eh_x09LV9iBC8PC7BIsGESkig"]}
18	08:42:17	受信	entity.remove	{"result":null}
19	08:42:17	送信	world.spawnParticle	{"params":[0,2,2,0.2,0.2,0.2,{"particle_id":"dust","receiver":"self","data":{"color":[64,160,255],"size":1}},0,8]}
20	08:42:17	受信	world.spawnParticle	{"result":8}
21	08:42:17	送信	world.playSound	{"params":[0,1,1,"block.note_block.harp",{"volume":0.5,"note":18,"receiver":"self"}]}
22	08:42:17	受信	world.playSound	{"result":null}
```
