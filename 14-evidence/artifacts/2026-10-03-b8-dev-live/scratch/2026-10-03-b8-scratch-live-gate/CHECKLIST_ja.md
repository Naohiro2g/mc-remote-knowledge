# Scratch segmentの確認項目

実施結果は`RESULT_ja.md`。本一覧は開始前に用意した項目で、PASS／未実施の判定は結果票を参照する。

実施根拠: knowledge `749ba60dc8c18938e50ce66b8e820aac4401c69e`、統一実施票「共通」「3. Scratch」。
exact set `b8-integrated-artifact-set-1`、Scratch `691576f60b7f0824e1753bd6823901d01fbe2422`。
human ownerのJAR差し替え連絡前には接続しない。試験位置はdevのhelloと人間の目視に合わせて選ぶ。

## 開始判定

- 凍結成果物を使い、接続先を確認する。過去のローカルMCへ接続しない。
- 最初の認証済みhelloのprotocolが23.2.0、mc_versionが1.21.11。違えば本体を実行せずFAILとして返す。
- auth.enforcementはONのまま。必要なpairingはhuman ownerが承認する。
- 以後、失敗時はそのsegmentで止める。要求・応答・reason・identityを記録し、source／artifactを差し替えて続けない。

## entity／particleの新規9ブロック

entityは試験用に1体生成し、そのhandleを使う。削除の確認もこの試験用entityを対象にする。

| ID | ブロック | 確認すること | WireScopeで見るmethod |
| --- | --- | --- | --- |
| E01 | 近くのentityをリストへ入れる | 範囲内の試験用entityが入り、指定上限を超えない | world.getNearbyEntities |
| E02 | entity情報の項目 | リスト項目からhandle・type・座標を読める。accessorだけでは追加通信しない | E01の結果と照合 |
| E03 | entityのpose | 生成したhandleからposeを取得できる | entity.getPose |
| E04 | entity poseの項目 | 取得したposeから座標・向きを読める。accessorだけでは追加通信しない | E03の結果と照合 |
| E05 | entityのposeを設定 | 小さな位置・向きの変更が反映され、再取得結果とも一致する | entity.setPose／getPose |
| E06 | entityを削除 | 試験用entityが削除される | entity.remove |
| P01 | 通常particleの設定値 | flameなどの設定値を生成ブロックへ渡し、typed paramsが送られる | world.spawnParticle |
| P02 | dust particleの設定値 | 色・sizeを含む設定値が送られ、dustが描画される | world.spawnParticle |
| P03 | block particleの設定値 | block ID・stateを含む設定値が送られ、block particleが描画される | world.spawnParticle |

既存のentity生成ブロックでhandleを受け取る操作と、particle生成ブロックへ設定値を差し込む操作も含めて確認する。
particleは通常の要求に加え、試験用のIDなし通知frameがWireScopeから落ちないことを確認する。wire §3.5の建築モードFASTはsetBlock／setBlocksだけに適用し、particle learner blockの通知化は要求しない。

## sound／catalog／picker

| ID | 対象 | 確認すること |
| --- | --- | --- |
| S01 | 音IDで再生 | block.glass.breakなどの有効ID、音の設定ブロック、pitch／N0〜N24のnote入力を使い、world.playSoundの往復と音を確認 |
| S02 | 置かれたblockの音 | 実際にblockがあると確認した座標でworld.playBlockSoundの往復と音を確認 |
| C01 | カタログID一覧をリストへ | block／entity／particleの各ID一覧が指定リストへ入り、kindと内容が対応する |
| C02 | pickerの名前と検索 | 日本語名・英語名・IDで検索でき、適用後の値はmachine IDとStateTextになる |
| C03 | pickerの既定値省略 | 選択肢はcatalog順で重複せず、既定値に「（デフォルト）」が付き、選ぶと結果から省略される |
| C04 | 名前空間省略 | BlockInfoTextのID／状態／property／property有無がoak_log[axis=z]等の入力を受け、ID出力を完全修飾する |

## WireScope／b7後の是正

- Scratch sourceの独立WireScopeを独立Chromiumで開く。E01／E03／E05／E06、typed particle、particle FAST通知、soundのframeをDOMと実画面で確認する。human ownerも目視する。
- 空のevents.pollが続いても有用な履歴が押し出されないことを確認する。
- 数値入力欄でCtrl+C／Ctrl+Vがネイティブ編集として動作することを確認する。
- server backpressureが観測された場合は「接続停止」と誤案内せず、接続を維持して再試行を案内することを確認する。再現できなければ未実施として記載し、実機PASSとしない。発生のために凍結candidateやserver設定を変えない。

## 結果の返し方

- 各項目をPASS／FAIL／未実施で記録する。準備のdigest照合をブロック実動作のPASSへ流用しない。
- screenshotはGit外に保存し、token・pairing_id・private address・player UUIDが写る部分を公開素材から除く。pair codeは収録してよい。
- identity、観測、要求・応答、失敗reason、未実施範囲を一枚で返す。component／横断GREENを宣言しない。
