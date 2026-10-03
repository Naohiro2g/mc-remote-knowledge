# Human ownerのWireScope観測（run 1）

- 起動前の回答: 「両方確認できました」。質問対象はWireScopeのPython source表示と、Minecraftでの通常devログイン。
- ownerが実browserからhelloの送受信2行を貼り付け。protocol23.2.0／mc_version1.21.11、auth.tokenを含まない表示だった。
- 代表操作の後、ownerがWireScopeのsequence1〜34を貼り付け。entityのspawn→nearby→pose get／set→remove、ParticleSpecのdust／block各world／self、無印flame、playSoundのpitch／noteの送受信を表示した。
- 最後のsequence34のworld.getBlock受信は、owner貼り付けではpayloadが空。Pythonのsanitized loggerにはsequence34、result={block_id:minecraft:air,state:{}}がある。最後のUI payload表示までPASSとはしない。
- 視覚・聴覚について: player間のreceiver差、dust／blockの描画、音を聞けたか／定位の観測は、この貼り付けだけから主張しない。
- runnerがBlockValueの扱いで停止して終了したため、stationは閉じた。停止後の表示状態は未確認。

