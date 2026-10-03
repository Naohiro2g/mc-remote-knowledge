# b8統一実施票：Scratch segment 3 の返却

- 実施日: 2026-10-03。human ownerからdev JAR差し替え済み、接続先、Python segment 2の残り完了を受領して開始。pairingはhuman ownerが承認。
- knowledge contract commit: `749ba60dc8c18938e50ce66b8e820aac4401c69e`。統一実施票の「共通」「3. Scratch」、wire §3.3・3.5・5.8.3、Scratch projection／roadmapを実参照。最新進捗とruntimeは`396326def73d99aae91dca4de9416f4eca6d2aea`も参照したが、凍結setは変更していない。
- exact set: `b8-integrated-artifact-set-1`。branch `agent/b8-compatibility`、Scratch source `691576f60b7f0824e1753bd6823901d01fbe2422`。
- 実行: 凍結GUI／Bridge／WireScope archiveを展開し、privateなdeployment設定だけを重ねた。独立Google Chromeで、実ScratchブロックをVM sequencerから実行。試験用Chromeは通常利用中のChromeとは別context。内蔵Browserの初期接続が失敗したため独立Chromeを使用。
- 最初の認証済みhello: `protocol:23.2.0`、`mc_version:1.21.11`で一致。auth.enforcementはONを維持。

## ブロック別の結果

以下のPASSはブロック実行・wire応答・Scratch値の確認。Minecraftの描画や聞こえ方はsegment 4へ残し、ここでは合格を主張しない。

| 対象 | 結果 | 観測 |
| --- | --- | --- |
| getNearbyEntities | PASS | 指定リストへsnapshotを格納。試験用armor_standを含み、削除後はそのhandleが消えた |
| entityInfo | PASS | handle／type／x・y・zが取得済みsnapshotと一致 |
| getEntityPose | PASS | pose取得と移動後の再取得が成功 |
| entityPoseInfo | PASS | dimension／座標／yaw／pitchをsnapshotと照合 |
| setEntityPose | PASS | xを1増やしyawを90へ変更。再取得で一致。dimension_refの無印`overworld`を使用 |
| removeEntity | PASS | result:null。今回生成したentityだけを削除し、nearbyの再取得で不在を確認 |
| particleSpec | PASS | 無印`flame`のtyped object、world／selfを生成ブロックへ渡し、各result:8 |
| dustParticleSpec | PASS | RGB[255,64,0]／size:1、world／self。各result:8 |
| blockParticleSpec | PASS | 無印`stone`／state:{}、world／self。各result:8 |
| playSound | PASS | `block.glass.break`＋note:12、`block.note_block.harp`＋pitch:1／self。各result:null |
| playBlockSound | PASS | getBlockでstoneを確認した位置のbreak音、volume:0.5／note:12。result:null |
| soundOptions | PASS | N12→note:12、数字1→pitch:1、receiver:selfの生成を確認 |
| catalogToList | PASS | block1166件／entity157件／particle115件。完全修飾ID、昇順、空でない一覧を実Scratchリストへ格納 |
| pickerの名前・検索 | PASS | `gold_block 金ブロック`／`Block of Gold`。gold5件、日本語名1件、Block of Gold2件、door42件 |
| pickerの既定値省略・適用 | PASS | catalog順の選択肢を維持し、デフォルトを重複させず表示。選択でStateTextから省略。適用値はacacia_button＋空StateText |
| pickerの表示調整 | PASS | 左424.8px／右283.2pxで60:40。結果17.6px／選択13.6px。modal実画面を確認 |
| BlockInfoTextのnamespace省略 | PASS | oak_log[axis=z]からID=minecraft:oak_log、状態=axis=z、axis=z、存在=true |

## WireScopeとb7後の是正

| 対象 | 結果 | 根拠・境界 |
| --- | --- | --- |
| entityの4 method、typed particle、soundの表示 | PASS | Scratch sourceを独立WireScopeへ接続し、実DOMとscreenshotで全7 methodを確認 |
| particleのIDなし通知の表示 | PASS | 凍結extensionの既存outbound transportから実通知を送信。WireScopeで「送信済み・結果未確認」。個別応答はなく、後続flushは成功 |
| 空events.pollが履歴を押し出さない | PASS | 無操作3.5秒で内部frame sequenceが3756→3767と進む間、WireScope tbody全文が不変 |
| 数値欄のCtrl+C／Ctrl+V | PASS | 実Blockly数値欄で123.5をコピーし、0へ変えてから貼り付け。入力と確定したfield値が123.5 |
| server backpressureの案内 | NOTRUN | volume:0の32要求を一度だけ送ったが、backpressureは0件。設定変更や追加負荷による強制再現はせず、実機PASSに数えない |
| human ownerによるWireScope目視 | PASS | method／送受信、particle種別、sound2 method、IDなし通知表示の4点を具体的に示し、human ownerから「４点、オッケー。」を受領 |

### 試験スクリプトの修正とFASTの境界

初回スクリプトでsetBuildModeのTRACE_DELAYを省略し、localの`invalid_trace_delay`を受けた。この試行は製品PASSに数えない。TRACE_DELAY:0へ修正後のflushは成功した。
WireScope画像のstreamの「エラー」badgeはこのlocal errorの保持によるもの。観測schemaの拒否や接続停止ではなく、後続のブロック試験中はconnectedを維持した。

また、建築モードFASTがparticleブロックにも適用されると想定したassertionは誤りだった。wire §3.5はsetBlock／setBlocksだけに適用する規定で、実装のspawnParticleがID付きrequestを送るのは契約どおり。これを製品FAILとして搬送しない。
統一実施票のparticle通知の観測は、同じ認証済みScratch接続の既存transportからIDなしworld.spawnParticleを実送信する独立probeに変更した。observer frameの捏造、製品へのpatch、candidate変更はない。これはlearner blockがFAST通知を生成するという主張には使わない。

## 凍結identity

| 使用成果物 | bytes | SHA-256 |
| --- | ---: | --- |
| scratch-image-inputs.tar.gz | 138375344 | c7318efdfb22076c2d40501a526d7ca16a121510f7685d875fff34cdc4404843 |
| bridge-image-inputs.tar.gz | 38138 | fd43f714c77d2bc184bf882460dfc05a1ce345dc6d4f5b52505a6a9d2850908f |
| wirescope-app.zip | 83746 | 4cb349894b71d61d7ca143d8362a5b79deb1810e1d7a9e31ad30e29bfe370a07 |
| wirescope-app.manifest.json | 2321 | 6ea468f50d50b52722b8f34145743df86cebc60865fe0e827be5632c26b024d0 |
| contracts.tar.gz | 1908 | 48948ba47d55409f02a8ff8e0d44021b07859e11ffa5ca0f8598e6ef06082390 |

B8 fixtureはowner commit `054a3af017f1abb8cc01cf85b3bc83181e648e19`、`entity-particle-v23.2.json`、36481 bytes／111 case／SHA-256 `ca636b4a2685ea67f24d8e7931e3d30a84e7cec872bb5c5d2eadd178cdac39f2`のまま。Python同梱WireScopeの凍結identityは変更を求めていない。

## 素材・終了・未検証

- `materials/live-results.json`: 57回のVM block／observer probeの実行値、要求・応答、runner修正、終了結果。token／pairing_id／private address／player UUIDを含まないことをexport時に検査。
- `materials/wirescope-final.png`、`wirescope-final-dom.txt`: 全対象methodとIDなし通知の表示。agentが実画像を確認。
- `materials/picker-gold.png`、`picker-door.png`、`picker-default-state.png`: 実devカタログの表示。`image-identities.json`に4画像のbytes／SHA-256。
- 本素材はGit管理外。`private/`は運用設定と非公開logなので搬送しない。正式evidenceの配置はknowledge coordinatorが行う。
- 今回のentityは削除済み、建築モードはDEBUGへ戻し、ScratchのWebSocketをclient側code1000で正常終了。最終connection statusはclosed。元の別試運転サービスは維持。
- 本票のlive試験ではsource／fixture／candidate更新・server設定変更・他repo変更・tag／release公開はなし。後続の列幅調整は別票`../2026-10-03-wirescope-column-width/GATE-ADDENDUM_ja.md`へ捕捉し、本票の実行identityを変えない。
- 未検証: server backpressureの実機表示、segment 4の二人目player・receiverの見え方・dust／block描画・音の定位／減衰／音階／5 kind。component／横断GREENやrelease可否は主張しない。
- human目視で列幅への改善希望を受領：時刻列を詰め、方向列の「送信済み・結果未確認」は2行表示を許容して詰める。調整後画像も承認され、後続source01cdb0bfeeと別ZIPを作成。human ownerの判断でb9へ持ち越し（2026-10-03）。上記b8の凍結candidate identityを維持する。
