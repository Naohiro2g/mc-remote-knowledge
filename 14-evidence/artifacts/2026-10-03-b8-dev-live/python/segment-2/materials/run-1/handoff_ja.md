## 確定搬送票

- 搬送元 repo: `Naohiro2g/minecraft-remote-api`
- 搬送元 surface: Python担当session（Codex）
- 搬送元 branch/commit: `codex/b8-python-entity-particle@52d35f5304e62f465c1f47ab47c00fe9bcf62470`
- 作成日: 2026-10-03
- 種別: その他（b8通常dev試験結果・Python segment停止報告）
- 決定: b7→b8の同一保存tokenによるhello継続はPASS。Python代表往復segment 2はtest runnerのTypeErrorでFAILとして停止。runnerのみ補正・オフライン確認済み。再実施は未許可・未実施で、横断gate判定はcoordinatorへ返す。
- 理由: `getBlock()`はimmutable `BlockValue`を返すが、runnerが辞書として`["block_id"]`で参照した。serverはairの正常応答、clientも正常decodeしており、例外はrunner側で発生した。統一実施票「共通」の「失敗したらそのsegmentで止め」「その場で直して続けない」に従って停止した。
- 却下案: なし。
- 影響: frozen source／wheel／同梱WireScopeのidentityは不変。plugin配置やserver設定はPython担当から変更していない。通常devの新規pairingはhuman owner承認で実施。b8側で再pair／保存tokenの削除・上書きはしていない。失敗後の再接続／world callもしていない。
- 根拠/検証: knowledge `749ba60dc8c18938e50ce66b8e820aac4401c69e`のruntime、release-gate-notes凍結節、`00-hub/b8-gate-live-test-sheet_ja.md`「共通」「2. Python — 代表往復」。exact set=`b8-integrated-artifact-set-1`。CI run36860299749のwheel2320.0.0b8、SHA-256 `dcedff010feac0d5df24ff85dd84b321fb819f78563c39431ac32d9d75bc0180`を使用。下記結果・sanitized素材を参照。
- 既に変更した実装/文書: packageのtracked変更なし。Git外runnerの2箇所だけを`original_block.block_id`／`original_block.state`へ補正。凍結wheelでBlockValueのdecode、復元用BlockSpecの組立、補正runnerのloadをオフライン確認しPASS。失敗時runner／frames／summaryはrun-1に原本保存。
- ナレッジ着地希望: b8 gateへtoken継続PASSとsegment 2停止を記録。live-human／live-auto素材をknowledge担当で正式evidence化。同じ凍結identityでの補正runner再実施可否、既存PASSの再利用範囲、再凍結の要否をcoordinatorが判断する。Python側では横断GREENを出さない。
- 捕捉 cleanup: local NOTESへ結果と未完了を反映。spawnしたcowは停止前にremove済み。仮blockは未設置。connection／WireScope stationは終了。token storeは継続試験後も保存tokenを保持。Git外素材は正式evidence着地後に昇格／移管／非参照失効を分類する。
- 着地後の確認戻り先: Python担当sessionへknowledge着地SHA、evidence参照、同一candidateでの再実施対象と許可済み次操作を返してほしい。

### 試験結果

| 対象 | 結果・観測 |
| --- | --- |
| b7新規pairing・local保存 | PASS。Minecraftでhuman ownerが承認。凍結wheelのtransportからprotocol23.1.0を明示 |
| 保存tokenでb7 hello | PASS。protocol23.1.0／mc_version1.21.11 |
| 同じ保存tokenでb8 hello | PASS。protocol23.2.0／mc_version1.21.11。private digestで同一tokenを照合、再pairなし、reasonなし |
| 短いimport・代表往復のhello | PASS。`from mc_remote import Minecraft`、protocol23.2.0／MC1.21.11 |
| entity lifecycle | PASS。無印cow spawn→nearby（2件、spawned handleあり）→pose get／set→remove |
| ParticleSpec | PASS。dust／block各world／self、result各8。無印flameもresult4で成功 |
| playSound | PASS。無印block.bell.useのpitch=0.75／world、harpのnote=18／self、各result:null |
| playBlockSound・3D graph | 未実施。block sound準備中のrunner TypeErrorで停止 |
| real-browser WireScope | human ownerがPython source接続とframe1〜34を貼り付け。上記操作のframe表示を確認。最後のgetBlock受信payloadは貼り付けで空のため、そのUI payload表示は未確認 |

失敗直前のRPCは`world.getBlock [3,1,0]`。sanitized loggerでは受信`{block_id: "minecraft:air", state: {}}`まで記録されている。server error／reasonは返っていない。

2-player receiver差、dust／blockの実描画、音の聴取／定位、graph、Windowsはこの票でPASSを主張しない。token、pairing_id、private address、player UUIDは票・summary・observer素材へ出力していない。

### 搬送素材

Git外の`handoff-materials/2026-10-03-b8-dev-token-upgrade/materials/`に保存。正式evidenceではなく、knowledge担当がauthoring／配置するための素材。接続先設定とprivate credential stateは搬送対象に含めない。

| 素材 | SHA-256 |
| --- | --- |
| b7_summary.json | `f1c5d7e812c080f4dc7a26a90c3cae8656a4eef1bf650accdb2f87ecdb41bd06` |
| b8_summary.json | `81da6bb092cf4d59f5df6c81905651653d048384ffe5f50f918b3082334e45ef` |
| run-1/representative_frames.jsonl（34 frames） | `2a2296fe91dc5a55afa1f9b49b46f992539866ccb322b69a51738707794b95ba` |
| run-1/representative_summary.json | `77de431e58a9d459de0811c18a9e57d3cd7d363805243d952eceff95e67b8247` |
| run-1/python_representative.py（失敗時原本） | `ca10db9691f2a097046abcfa2d4796b4a41bbefa8d87a8d69a16ba92ccb0fa8b` |
| python_representative.py（補正版） | `15c5c2cfa1ace74b03fd21c54d0ac575b656f75a39315754f283d8255fbf1003` |

追加素材: `token_upgrade.py`、`owner-observation_run1_ja.md`、`python-segment-stop_ja.md`。b7→b8のtoken継続は完了。Python代表往復の残りはcoordinatorの再実施指示待ち。

