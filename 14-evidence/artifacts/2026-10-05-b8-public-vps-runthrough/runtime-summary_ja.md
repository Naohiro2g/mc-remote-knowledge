# 正式b8の公開VPS配備と独立ランスルー：収録用要約

この文書はKnowledge担当へ渡す選択済み素材で、正式evidence recordではない。出所はStack担当の初回配備報告、独立担当のCOMPLETE、元Stack担当の後続read-onlyレビュー。

## 2026-10-03：初回配備

正式b8を別deploymentに構築し、旧停止時の入力と3volumeを保存、world・LuckPerms DB・McRemote snapshot＋authority・TLSを一組で引き継いだ。全source fileの内容一致を確認して公開入口を切り替えた。引継ぎconfigの内容保持でmtimeを更新したのは次volumeのconfigのみ。

live-auto（実施報告）: operator／doctor正常、正式artifact identity一致、credential HEALTHY、LuckPerms使用、creative、外部HTTPS／Java status／Bedrock UDP25565が成功。UDP入口は既存host filterの19132から25565への訂正と永続化を人間が実行した。backup ZIPのCRC・world／plugin収録を確認し、secret参照のnamespace引継ぎ後に定期転送・off-host再取得hash照合／download-verifiedが成功した。

live-human（人間報告・transcript）: Scratch b8からペアリング、protocol23.2.0のhelloとchat.post「Hello, Minecraft!」が成功。認証前helloはauth_required。追加で人間からiPadのworld参加成功を報告された。

10月4日14:12 JSTにはKnowledge `ceba53099fa001fea6b83d68deadc1eb9e0038fe`のapi/scratchを含むhomepage全79ファイルを反映し、配置と公開HTTPS取得内容をsource Git blobへ照合した。

## 2026-10-05：会話履歴を共有しない別セッション

最初のmainのpreset確認はunknown_preset_revisionで停止。必要な#66が未統合で、サービスを停止せず元セッションへ報告した。#66のmain統合後、`6cdbe6e2f8bc654a3d21a6119de6c4154a559afc`へ更新して同じ地点から再開・完走した。b9公開後でも、要求された正式b8のexact identityを使った。

live-auto（独立担当の実施報告）:

- profile／presetは`vps-server@12`／`public-web-paper@12`。McRemote／Scratch／Bridge／WireScopeの正式release identity一致。Pythonはrelease照合のみ
- 入力検査・artifact fetch・render・plan・SETUP_ONLY・Caddy検査に成功。旧停止時の入力と3volumeを新たに保存し、別3volumeへ全source fileをコピーしてcmp・tar header・SHA-256を照合した
- world3dimension、LuckPerms DB、McRemote snapshot＋authority、TLSを引き継いだ。snapshotは保存時・起動後とも39件、authority内容不変、domain整合。検査時点で期限内保存recordは0件。domain再初期化・token期限延長は実施していない
- 旧停止要求14:19:19 JST、次起動処理開始14:20:38 JST、doctor正常14:21:12 JST。停止要求からdoctor正常まで1分53秒。起動処理開始は全service稼働確認の時刻ではない
- 4service稼働、Minecraft healthy、doctor全OK。11JARの入力／lock一致、config内容保持、auth enforcement、credential HEALTHY、LuckPerms使用を確認
- 外部HTTPS各入口200、Java TCP25565、Bedrock UDP25565、McRemote TCP25575の認証前helloにauth_requiredを確認
- ServerBackup生成はexec既定userで拒否された後、実runtimeのUID:GIDに合わせて成功。ZIPのCRCとworld3dimension・権限DB・snapshot／authority収録を確認し、既存timerによる暗号化・転送・off-host再取得hash一致／download-verifiedを確認
- homepageはsyncを再実行せず既存配信directoryを新Caddyでも利用。後続Stack担当のread-only観測でも全79ファイルのceba530とのGit blob一致、operator／doctor正常を確認

live-human（人間transcript・担当の画像確認報告）: 14:40:35のhelloはtoken_expired、14:40:46のhelloはprotocol23.2.0／MC1.21.11で成功し、14:42:18のchat.post「hello again from b8」も成功。画像に関する担当報告はScratch2320.0.0b8、notice表示、WireScope mini接続OK。元画像はこの素材に含めていない。

## 実行漏れと後続の手当

独立ランスルーは配備前に製品noticeと既存運用者noticeを人間へ提示し、継承／編集／追加／削除を選んでもらう段階を漏らした。配信JSON・画面一致の成功で事前確認を実施済みにはしない。旧停止・次起動・正常確認の会話での報告も分かりにくかった。

後続Stack担当は#65で、構築準備からnotice事前選択へ接続し、準備完了・旧稼働中／旧停止直前／停止確認／次起動直前／doctor正常の報告と、ServerBackup生成時のruntime UID確認・console入口を補った。全368pytest／Ruff PASSのheadをmain `68b8d45af743cd56b70efe67a42e1e162b04c50c`へ統合済み。修正手順を使う新たな実機切替は行っていない。

## 未試験・未提供

10月5日のauth.*中間transcript、ゲームedition別のworld参加内訳、フルWireScope操作は未提供。初回配備のiPad参加を10月5日に再試験したとは扱わない。復号・world復元・旧セットへの切戻しは未試験。手順書があらゆる障害へ自動対処できることを示す検証ではなく、確認した構成・経路・実行範囲の記録である。
