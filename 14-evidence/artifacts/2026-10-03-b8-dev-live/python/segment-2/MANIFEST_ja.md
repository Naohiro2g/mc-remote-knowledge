# B8 通常devのtoken継続試験準備

- 搬送用ZIP: `python-segment-2-return.zip`、44,012 bytes／SHA-256 `ed283f90f068043dac53375053e1d5061a38aa109e80c852a38200de34e21f03`。確認票、run1／run2／run3のsanitized素材、runnerとgraphを19ファイルの明示allowlistで収録。各entryのbytes／SHAを同梱handoff-manifest.jsonに記録。private設定／credential state／token store／cache／表示codeは収録せず、実tokenと実private endpointが全entryに含まれないことを値を出力せず照合済み。

- 2026-10-03 最新結果: **残りのPython試験PASS（run 3、exit0）**。同じ凍結CI wheel／保存tokenのhello23.2.0 MC1.21.11、getBlock取得／仮stone／元airへ復元readback、playBlockSound5kind×省略/pitch/noteとPython既定呼出の計16往復、凍結graph81往復が成功。212frames／106RPC／21PASS行。human ownerがWireScope frame1〜50とgraph113〜212をpayload付きで貼り付け、表示を確認。仮blockなし、station／connection正常close、session86468終了。
- 最新返却票: `materials/handoff_ja.md` と同一の `materials/run-3/return_ja.md`（Release gate確認票形式）。以前の統合票は `materials/run-1/handoff_ja.md` へ保存。knowledge396326dの許可／PASS再利用、userの再開承認、run 2準備停止を区別して記録。formal evidence authoringはknowledge担当へ返す。
- 実runner SHA-256 `c001bd5cbc8ab8b5151133c995dec4f226d82f4b9ac83f786a2e9797574a5c7c`、frames `35922a3de2bb5c8d36e7162c98e68b5ea886f965edc2b2ed8b401da1552646a8`、summary `ad90cddaef3a62a3a4cc41eb364e6479b2d50bd36e1fd4cdfa4971582452f7de`。human観測はrun-3/owner-observation_ja.md。基準runner15c5c2cf…1003・run 2 runner46b4b61f…0271は不変。再発行対応を追加したrun 3では最初のattachで成立し、再発行操作は使わなかった。
- 非主張: server内部のSoundGroup数値、描画、聴取・定位、2-player receiver差、Windows。既定は値を省略したwireと正常ACKまで。次のgate進行・formal evidence着地はcoordinator担当。frozen identity／tracked candidate／server配置・設定／保存tokenに変更なし。
- 以下は過去段階の経過記録であり、準備済み・未実施・回答待ちの記載は当該時点の状態。


- 2026-10-03 最新状態: knowledge `396326def73d99aae91dca4de9416f4eca6d2aea` のcoordinator回答を受領。token継続とrun 1のPASSを再利用し、同じ凍結identityで残りのみ実施。userは「残り専用runnerで実施し、新しいSHAを返す」を選択した。
- run 2: **FAIL・接続準備で停止、本体未実施**。実runner SHA-256 `46b4b61f85eef5679114223755eea9ad4ac8f3fb5de2aca2ed0258348da90271`。同じ保存tokenのhello `23.2.0`／MC `1.21.11` はPASS、human ownerがWireScope attachについて「時間切れ」と回答したためcheckpointを中止。world操作0回、仮blockなし、session73255／station／connection終了。停止票と実素材は `materials/run-2/return_ja.md`／`summary.json`／`frames.jsonl`（2frames）。以前の統合搬送票へ、この停止票を追記として併せて渡す。
- run 3準備済み・未起動: `materials/run-3/python_remaining.py`、SHA-256 `c001bd5cbc8ab8b5151133c995dec4f226d82f4b9ac83f786a2e9797574a5c7c`。開始前readiness入力、既存productのbounded attach code再発行、実attach成立確認を追加。凍結CI wheelでoffline load PASS。本体は5kind×省略／pitch／noteとPython既定呼出、getBlock／復元、graph81往復で同じ。基準runner15c5c2cf…1003、run 2 runnerは変更なし。再開確認をhuman ownerへ質問中。回答なしで再接続しない。
- 次のcheckpoint: 再開許可・human準備後に起動し `start`、新stationのattach／MCログイン確認後に `ready`。表示code失効時は `reissue` を入力し既存bounded再発行を使う。getBlock payload／playBlockSound frame確認後 `graph`、graph frame確認後 `finish`。表示用attach codeを永続素材へ保存しない。
- SoundGroup数値そのものはRPC result:nullから直接観測できず、既定の確認はwireでvolume／pitch／noteを省略した正常往復の範囲とする。描画・聴取・定位・2-playerはsegment 4の範囲。
- 以下は以前の段階を含む経過記録。未許可／未実施の記載は当該時点の状態であり、最新状態は上記を参照。

- 統合搬送票: `materials/handoff_ja.md`。token継続PASS、Python run 1のrunner停止、補正、未実施、再実施判断依頼を一枚へ統合。以前の各段階票より、現在地の搬送にはこの統合票を使用する。

## 現在地

- b7 phase: **PASS**。新規session pairingをhuman ownerが承認。local token storeへ保存後に読み直し、認証付きhelloがprotocol`23.1.0`／mc_version`1.21.11`で成功。
- b7前段: token無しhelloは`auth_required`。auth.enforcementやserver設定は変更していない。pair code表示は`/mcremote pair 037-474`。
- b7 evidence素材: `materials/b7_summary.json`。要求はauth.tokenをREDACTED、応答はprotocol／mc_versionだけを保存。private address、player UUID、pairing_id、token実値を出力していない。
- runner: 凍結B8 CI wheelのtransportからb7のprotocol23.1.0を明示して実施。frozen packageは変更していない。world書き込み0回。
- b8 phase: **PASS**。user「差し替え完了」後に同じendpoint・保存tokenをprivate stateで照合し、認証付きhelloを1回送信。protocol`23.2.0`／mc_version`1.21.11`で成功。pairing_started=false、world書き込み0回、保存token削除／上書きなし。
- b8 evidence素材: `materials/b8_summary.json`。b7／b8両summaryとrunnerはknowledge正式evidence化の搬送素材。失敗reasonなし（hello成功）、MC版はhello広告に基づく。
- Python代表往復run 1: **FAIL、停止済み**。human ownerのWireScope attach／MC再ログイン確認後、entity lifecycle、dust／block各world／self、無印flame／cow／block.bell.use、playSound pitch／noteがPASS。block sound準備のgetBlock正常応答後、runnerがBlockValueを辞書扱いしてTypeError。playBlockSound／graphは未実施。cow削除済み、仮block未設置。station／connectionは閉じた。
- human ownerの実browser観測: WireScope sequence1〜34を貼り付け。最後のgetBlock受信payloadは貼り付けでは空で、そのUI payload表示は未確認。その他の操作frame表示を確認。描画／聴取／2-playerは主張しない。
- run 1原本を`materials/run-1/`に保存。停止票は`materials/python-segment-stop_ja.md`。runnerのみ2箇所をBlockValue.block_id／stateへ補正、凍結wheelでoffline decode／set引数とrunner loadを確認。再実施は許可待ち。candidate／wheel／server／tokenは不変。
- Frozen graph: source52d35f5の`examples/particle_graph.py`を`materials/particle_graph_frozen.py`へGitから取得。SHA-256 `e3824c3800aea4acc3ca1141a289e5a04d34c52cb2492af25b38f050bfe824d3`。未push worktreeのsampleを使用しない。
- 観測素材: product observerのsanitized frame consumerを、同じstation sinkとJSONL素材保存へ分岐。token／player UUID／pairing_id／endpointを含むraw frameは保存しない。runnerのcheckpointと操作ごとのPASS／FAILをsummary化する。
- 再実施時のcheckpoint: human ownerがWireScopeへattachしMC通常devへログインしたことを確認後に`ready`。entity／particle／soundのframe表示確認後に`graph`。81点graphのframe確認後に`finish`。userの確認なしで進めない。

- knowledge: `749ba60dc8c18938e50ce66b8e820aac4401c69e`。最新mainのruntimeをmarker抽出して読み、INDEX、release-gate-notesの凍結exact set、統一実施票の共通／2.Python、wire §5.8.3を確認。
- exact set: `b8-integrated-artifact-set-1`。Python `52d35f5304e62f465c1f47ab47c00fe9bcf62470`、CI wheel SHA-256 `dcedff010feac0d5df24ff85dd84b321fb819f78563c39431ac32d9d75bc0180`。取得済みwheel／sdist／manifestを再照合。
- 最新user指定: 通常devをb7にして新規pair→local保存→同じ保存tokenでb7 hello→Backstageがb8へ戻した後に同じtokenでb8 hello。b8側は再pairしない。token実値は出力しない。
- 接続先確認中: examplesのlocal設定は非loopback、testsのlocal設定はloopback。通常devに対応する設定と現在のb7起動状態をuserへ確認中。値は票や出力へ転記しない。未接続。
- user追記: 「サーバーはdev」。対象は通常devと確認できた。手元の2設定のどちらが対応するか未確定のため、dev用host／portまたは設定ファイル、および現在b7起動済みかを確認中。localhostはこの試験に使わない。
- 接続先確定: userが通常devのhost aliasとport25575を指定。Git外`materials/param_dev.py`へ設定。b7のprotocolでtoken無しhelloを試し、auth_requiredなら新規pairへ進む。不一致／失敗なら停止して返す。
- 接続設定補正: 指定aliasのDNS解決がgaierrorとなったため、TCP接続／server RPC前で停止。ローカル`ssh -G`でaliasの実接続先を取得し、Git外設定へ反映（値は出力せず）。candidate変更／server変更なし。初回出力は`materials/endpoint-resolution-failure.json`へ保持するが、hello_request欄は予定要求であり実送信ではない。
- 実施runner: `materials/token_upgrade.py`。凍結CI wheelの隔離環境から実行。b7はtransportでprotocol23.1.0のhelloを明示、b8は23.2.0を明示。client artifactの変更はしない。
- b7 token: userのMinecraft承認後にauthのlocal token storeへ専用profile keyで保存。通常devの設定とtoken digestをprivate continuity stateに記録し、b8で同じ保存tokenであることを照合。raw token／private endpoint／player UUID／pairing_idをsummaryへ出さない。
- b8: 同じtargetのverified b7 stateとtokenがなければ停止。失敗時にcredentialを削除せず、再pairせず、そのsegmentのFAIL／reasonを返す。MC版がhello errorで取得できなければnullとし、推測しない。
- 開始待ち: 通常devのtarget確認とb7起動連絡。b8段階はBackstage／human ownerの切り戻し完了連絡後のみ。deployment／rollbackはこのrepoで操作しない。
- 後続: Python代表往復は統一実施票通りに実施。認証済みhelloのprotocol23.2.0／MC1.21.11を確認してからentity、particle、sound、無印ID、graphへ進む。WireScopeのframe表示はhuman ownerが確認する。通常devの開始条件を満たすまで接続しない。
- evidence: ここはGit外搬送素材。正式record／artifactのauthoringはknowledge担当。試験未実施でPASSは主張しない。
- 準備検証: runnerのpy_compileと--helpを隔離CI wheel環境で実行済み。サーバー接続／pairing／token store書き込みは未実施。
