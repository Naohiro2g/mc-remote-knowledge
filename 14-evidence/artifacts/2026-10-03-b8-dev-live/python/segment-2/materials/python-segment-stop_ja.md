## Python segment 2 停止票（run 1）

- knowledge contract: `749ba60dc8c18938e50ce66b8e820aac4401c69e`、`00-hub/b8-gate-live-test-sheet_ja.md`「共通」「2. Python — 代表往復」。
- exact set: `b8-integrated-artifact-set-1`。Python `52d35f5304e62f465c1f47ab47c00fe9bcf62470`、CI wheel SHA-256 `dcedff010feac0d5df24ff85dd84b321fb819f78563c39431ac32d9d75bc0180`。candidate変更なし。
- test class: frozen wheelのlive-autoと、human ownerのreal-browser WireScope表示確認。
- segment結果: **FAIL、停止済み**。block soundの準備でtest runner自身がTypeError。server RPC error／reasonではない。
- 原因: Minecraft.getBlock()のpublic戻り値はimmutable BlockValue。runnerがoriginal_block["block_id"]と辞書扱いした。serverはworld.getBlock [3,1,0]に{block_id:minecraft:air,state:{}}を正常応答し、clientもBlockValueへdecodeした。
- 実施済みPASS: 短いimport、認証済みhello23.2.0／MC1.21.11、build context、無印cow spawn→nearby（2件、spawned handleあり）→getPose→setPose→remove、dust／block各world／self、無印flame、無印block.bell.useのpitch world、harpのnote self。
- human観測: ownerがWireScopeからsequence1〜34を貼り付け。上記代表操作のframe表示を確認。最後のgetBlock受信payloadは貼り付けで空のため、そのUI payload表示は未確認。
- 未実施: playBlockSoundの既定／pitch／note、3D graph、最後のhuman checkpoint。2-player、描画／聴取／定位もこのsegmentでは未判定。
- cleanup: cowは停止前にremove済み。仮blockは未設置。追加world callは行わず、connection／stationを閉じた。保存tokenは変更・破棄していない。
- evidence素材: run-1/python_representative.py SHA-256 `ca10db9691f2a097046abcfa2d4796b4a41bbefa8d87a8d69a16ba92ccb0fa8b`、run-1/representative_frames.jsonl（34 frames）SHA-256 `2a2296fe91dc5a55afa1f9b49b46f992539866ccb322b69a51738707794b95ba`、run-1/representative_summary.json SHA-256 `77de431e58a9d459de0811c18a9e57d3cd7d363805243d952eceff95e67b8247`、owner-observation_run1_ja.md。
- 補正準備: Git外runnerの2箇所だけをoriginal_block.block_id／original_block.stateへ補正。frozen package、source、wheel、server、設定は変更しない。再接続／再実施はまだ行っていない。
- 判定を求める事項: 同じ凍結identityで補正runnerによるsegment 2再実施を許可するか。PASS再利用や再凍結の要否はcoordinatorが判断する。Python側で横断GREENを判定しない。

