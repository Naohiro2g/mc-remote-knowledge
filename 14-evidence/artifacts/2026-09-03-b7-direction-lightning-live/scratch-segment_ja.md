# Scratch／WireScope live-human素材

## 観測済みRPC

- `player.getDirection`: request `{"params":[]}`、result `[-0.962763,0.26892,0.027733]`
- `player.setDirection`: request `{"params":[1,0,0]}`、post-read result `[1,0,0]`
- entity setup initial attempt: `unknown_entity`
- entity setup retry: `world.spawnEntity` request `[55.108,121,0.883,"minecraft:armor_stand"]`、opaque handle取得成功
- `entity.getDirection`: spawn結果のopaque handleをbyte-for-byte同じ文字列でrequestへ渡し、result `[0,0,1]`
- `entity.setDirection`: request `["mcr_eh_TxRj_TNICzGN_J1XUfuGPA",1,0,0]`、post-read result `[1,0,0]`
- `world.strikeLightning`: request `[55.108,121,0.883]`、result `null`。人間が雷の実発生を視聴覚確認した。

## 人間によるMinecraft側確認

- player `[1,0,0]` の向き変化を再実施で目視確認した。
- armor stand `[0,0,1]` → `[1,0,0]` の向き変化を再実施で目視確認した。
- player入力 `[1,0.5,0]` の方向変化も追加確認した。
- armor standのY成分変化は外見から判別できず、目視確認を主張しない。
- armor stand位置への落雷を追加実施し、3回目で着火を確認した。fireは毎回の成功条件ではなく、full lightningがfireを含み得ることの観測とする。

## b7後follow-up — WireScope保持window

- `events.poll`の50往復が、request／response各1 frameとして100-frame保持windowを占有することをreal-browserで観測した。
- filter表示では送受を1 unitとして原子的に扱い、method group `events` 50件とevent class `empty` 50件は同じ50 unitの重複集計である。
- `empty`を非表示にしてもraw frame保持から除外されないため、有用なframeが約50 poll後にwindow外へ押し出される。
- b7 candidate中は変更しない。release後のWireScope是正対象として搬送する。

## b7後follow-up — Scratch数値入力欄のclipboard

- real-browserで、数値入力欄間のキーボード`Ctrl+C`が機能しないことを観測した。
- 右クリックcontext menuからのcopyはclipboardへ入り、同menuからのpasteは成功した。
- b7 candidate中は変更せず、release後にkeyboard event経路とBlockly入力欄の既存挙動を切り分ける。

## b7後follow-up — server backpressureの誤案内

- lightning連続実行時、`world.strikeLightning`のserver responseとしてcode `-32000`、message／reason `backpressure`を4回観測した。同じ接続の人間による再実行で落雷に成功した。
- exact sequence: `358/360` success `result:null`、`363/364`、`365/366`、`369/370`、`371/373`はserver `backpressure`。
- 現行GUIはreason `backpressure`を一律`mcremoteBuildDeliveryFailed`へ写像し、「接続を停止したため再接続」と案内する。
- client outbound transportのbackpressureではVMがsocketをcloseするため再接続案内が正しい。一方、serverからの一時的なadmission拒否`backpressure`ではsocketをcloseせず、再接続を要求する根拠がない。
- source上で両者が同じreason／alertへ合流している。b7 candidate中は変更せず、release後に発生源を区別した案内へ是正する。
- automatic retryは観測していない。成功した再試行は人間による明示的なblock再実行である。
- screenshot: `images/server-backpressure-reconnect-alert.png`、32,300 bytes、SHA-256 `dffd51bc76e48ef5ce09646ffb609c6722402b1e5a36ac9347fcdef43c27eb67`。
- screenshotは再接続後の再現、exact server framesはその前の再現であり、同一発生の同期captureとは主張しない。

## 接続contract観測

- hello request: protocol `23.1.0`、client `scratch-mcremote`、version `2301.0.0b7`、locale `ja`。
- hello response: protocol `23.1.0`、Minecraft `1.21.11`、permissions snapshot `online:true`、`offline:true`、`build_range:1000`。

## Non-claim

- 本素材はb7 artifact/source、observer schema、station transport、server event ringを変更しない。
- 保持方式の是正案とrelease番号は未決定。
