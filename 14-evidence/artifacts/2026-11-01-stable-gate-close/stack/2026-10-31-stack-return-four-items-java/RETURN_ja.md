# Stack返却票：10/28追補の4点とJava記録（2026-10-31統合版）

10/28追補の「返してほしいこと」4点と、10/29追補のJava記録への一括回答です。今回の最新版による最終確認と、安定版のヒープをXms=Xmx=3Gにするhuman ownerの指定も反映しました。これまでの素材が未受領なら、本票を回答本文として受け取ってください。

- 搬送元：mc-remote-stack／Codex
- branch/commit：main@488475f2b3dfeeb3252bddda2d87b4fca39fb2a6
- knowledge contract path：00-hub/stable-gate-work-instructions_ja.md「Stack」4／5、00-hub/release-gate-notes_ja.mdの初回stable節、DECISIONS 2026-10-29-01
- knowledge contract commit：d012c910f16d8c89921c8265124049a8c732ab1d。今回remote mainからruntimeと対象本文を読取
- 観測日：事前確認は10/29、採用#231の配布物照合と最新版・3Gの最終確認および公開Javaの再読取は10/31
- test class：起動・RPC・Geyser応答・通常再起動はlive-auto。新たなlive-humanは実施していない
- 返却範囲：実施結果、凍結・切替の手順と見積、未完了。横断gateの最終判定ではない

| 依頼 | 返却 |
| --- | --- |
| 1. rc2＋26.3で新セットを先に起動したか | 10/29に実施済み。加えて10/31にstable候補＋#231＋25.0.5＋3Gで自動確認PASS |
| 2. 新セットのb1273で/v1/joinが26.60を返すか | b1273の確認は10/29にPASS。最新版b1279でも10/31に26.60／2225を確認 |
| 3. 凍結手順と所要時間 | 下記の手順・条件付き見積を返却。製品presetへの組込みと凍結完了はまだ |
| 4. 11/1に残る作業順 | 下記へ明記。公開切替はまだ |
| Java・heap・上限・flags | 公開側の再読取と新環境の実測を下記へ記録。採用heapは3G／3G |

## 1. rc2＋26.3の新セットの事前起動と、最新版での最終確認

10/29、profile vps-server@16／preset public-web-paper@16で、McRemote2321.0.0rc2＋Paper26.3#203＋Temurin25.0.3+9を、完成済みbackupから復元した専用volumeで起動しました。3次元を継承し、worldのリセットはありません。公開portは持たず、検査後に停止しています。

- McRemote source：7960a913a11c621d85e6120ee412b696fe125457
- rc2 JAR SHA-256：ce66abaf41a94800217a11161145b9f868333b7bfa605fd1f77b888878620e50
- b1273構成のlock：sha256:5cce2872e0dd6bee102293193ad11715d739ce73226fd627522e6163f48be5c5、起動29.733秒
- 当時の最新plugin構成のlock：sha256:fb33ef807c6f7a5f519d2a730d0912d633d1cbfbf3b535cf5283ea22d2271f77、起動46.474秒
- plan：新規projectを対象にしたmcrctl plan。CLIは上記lock identityを表示する方式で、同一volume更新のdeployment update plan_idは対象外。planの出力はprivateに保持
- WorldEdit7.4.2を維持した初回は互換性エラー。7.4.6への更新後は起動し、McRemote credential HEALTHY、tokenなしhelloはauth-required

human ownerの追加依頼「最新バージョンで最終確認してください」を受け、10/31に次の構成で改めて試験しました。McRemoteは公開済み最新版rc2だけでなく、SSOT指定のstable候補の実JARを使用しています。候補のsourceとbranchをGitHub APIで、JAR本体をSHA-256で照合しました。

| 対象 | 最終確認した値 |
| --- | --- |
| Paper | 26.3 #231、STABLE |
| Paper JAR | paper-26.3-231.jar、55,258,607 bytes |
| Paper SHA-256 | a836a016be7ac52352eb3a1efb6857bb42ee73a6c78d46e292f7e87742edb0e6 |
| McRemote | 2321.0.0 stable候補、source 525c31823a8efb736463aec471c2756089546391 |
| McRemote JAR SHA-256 | e3f7cc2ab9ee9b3130f927935634e32e8ddffe7d7603b6d873973968f68db4ab |
| Java | Eclipse Adoptium、Temurin-25.0.5+8、runtime25.0.5+8-LTS |
| 実Javaのheap指定 | -Xms3G -Xmx3G |
| 検査用ComposeのSHA-256 | e145a3e5256dcc7f9aaa8bf43feb39f82c71b78fd3426c65d646d7bc00fe6a23 |

10/31に公式metadataと照合した周辺pluginは次のとおりです。

- WorldEdit：7.4.6
- ViaVersion：5.12.2
- ViaBackwards：5.12.2
- Geyser：2.12.1-b1279
- LuckPerms：5.5.88
- DirectionHUD：1.8.4.0+26.2
- OtterLib：0.4.0.1+26.2
- AdvancedPortals：2.8.0
- DiscordSRV：1.30.5
- Floodgate：2.2.5-b141
- ServerBackup：2.10.0

DirectionHUD／OtterLibのPaper向け最新版は26.2表記です。26.3向けFabric版とは分けて選定しました。確認済みはPaper26.3での起動・有効化で、HUDの実画面やportalの人間操作は今回の範囲に含めません。

この最終試験は、新しい製品preset／lockの作成とは分けた、専用コピーでの検査用構成です。既存の生成物を公開配備済みという扱いにはしません。RPC接続はloopbackだけに限定し、ゲームの公開portは持ちません。

認証は有効なまま、コピーの既存credential domainを保ち、短期の試験用sessionを1件だけ追加しました。試験用UUIDにだけLuckPerms権限を付けています。公開側の認証DB・権限DBを変更せず、試験コピーを公開worldへ戻すこともありません。これは新しい実プレイヤーのペアリング試験ではありません。

producerのcompatibility_pulse.pyを同じ候補JARに対して実行し、次を確認しました。

- 認証したhello、protocol23.2.1、Minecraft26.3、同梱の対応版一覧とcatalog
- 構造化blockの設置・読取、32768ブロックの処理とnotification後のflush、上限超過の拒否
- 看板の設置・読取・行更新、entity handleの取得・pose・remove
- event poll、particle、chat
- 通常の停止・再起動後も、同じ試験用sessionで認証・読取・書込が継続すること
- tokenなしhelloはauth_requiredで拒否されること

通常pulseは8群、再起動後pulseは4群がPASS。3Gでの起動は34.304秒、通常再起動は29.703秒でした。容量・授業負荷・長時間運転の測定結果ではありません。

Paper #231は公式API・取得JAR・実起動logで照合。各pluginも実際に配置されたJAR全件のhashと実行時versionを確認しました。検査用にDiscordSRVのBotTokenだけを空にして二重接続を避けたため、DiscordSRVは無効、ほかの対象pluginは有効でload errorはありません。

検証スクリプトの依存ファイル不足と再開時の変数不足を修正して再実行しました。アプリケーションのJARは変更していません。途中の失敗記録とraw logはprivateに保持し、最終のPASSと混同しません。

## 2. Geyser b1273と既定config、最新版での26.60応答

10/29の新しい26.3セットで、Geyser b1273と当時の最新版b1276の両方がGET /v1/joinに26.60／protocol2225を返しました。公開sb-betaの古い応答の流用ではありません。

- b1273 JAR SHA-256：218f57088fd7a147f670c489377da2341fc51f1867b2c36ed181f39c9f379b59
- b1273生成の既定configを未編集で使用。config-version11、nethernet、19132、webrtc-port0、builtin HTTP、実行時FLOODGATE。identityはbackupと同hash

10/31は公式metadataの最新版がb1279だったため、これを取得・hash照合して採用し、上記#231／25.0.5／3Gの構成で次を確認しました。

- 実行時：2.12.1-b1279 (git-master-a651d60)
- JAR SHA-256：234fa467a32bbc780bd495296eb18fa0fbd7af8dab41f137ed5f7a45aabfbb90
- GET /v1/join：version26.60、protocol2225
- 生成された既定config：config-version11、nethernet、19132、webrtc-port0、builtin HTTP。実行時FLOODGATE
- nethernet/identity.pem：backupから継承したものとhash不変。鍵の本文は搬送しない

このHTTP応答を、外部のiPhone／Windows／Androidからの実参加や、UDP到達性の新しいPASSには広げません。b1273の結果は#203／25.0.3、今回の最新構成の結果はb1279／#231／25.0.5として残します。

## 3. 10/31の凍結手順と所要時間

Paperの選定待ちは解消しました。採用は#231で、公式APIと取得物のbytes／SHA-256が一致しています。以後、番号が進んだことだけを理由に自動変更しません。

1. coordinatorのexact component setと正式なrelease tag／manifestを受領し、JAR・宣言・verification record・OCI参照を照合する。stableの正式配布物は今回の候補JARとbytes／hashを比較する
2. Paper #231、Temurin25.0.5+8の再取得可能なruntime image参照、今回確認したplugin JAR群、heap3G／3Gを同じ組へ固定する
3. 新しいimmutable stable preset／必要なprofileを追加し、catalogを再生成する。既存revisionを上書きしない
4. 停止中の次projectでoperator check→resolve→validate→artifact fetch→render→plan。world継承、旧キー不在、Geyser、2組のWeb名、各組のconnection_targetsと既定、heapとflagsを照合する
5. 変更を含むcommitでuv sync --extra dev、uv run pytest、uv run ruff check .、catalog／差分検査を行う。生成したexact setと実際の起動条件を照合し、identityと結果を返す
6. 凍結した候補と公開後のrelease assetを再照合し、公開まで環境を保持する。差替が必要ならcoordinatorへ戻す

入力・必要な実装・runtime参照が揃ってからのpreset反映とrepo検査は30〜45分の見込みです。前回の同じStack commitのpytestは598件／879.59秒で、約15分でした。これは凍結全体の完了時間の保証ではありません。

正式なruntime imageの配布参照、stable presetへの組込み、heap3Gの正式な生成・更新経路への反映が残っています。本票作成後、(a)の組別一覧・既定の生成をvps-server@17で実装し、618件の検査がPASSしました。https://github.com/Naohiro2g/mc-remote-stack/pull/81（source 392c29a343dc4106645d5ca557f503f307fdbebd）に提出済みで、PR統合と11/1セットへの適用が残ります。詳細は2026-10-31-web-pair-target-selectionsの返却票を参照してください。これらの実装・検査・公開物待ちは、上の30〜45分に含めません。

## 4. 11/1に残る作業順と人間の操作

1. 停止前に、公開されたexact set、#231、Temurin25.0.5+8、Xms=Xmx=3G、追加GC tuningなしを照合する。volume・port・filter・backup先、2組のWeb設定、接続先の既定、登録済みMOTDを準備する
2. human ownerと停止開始を合わせ、旧Minecraftを正常停止。旧project、world、plugin設定、権限DB、認証状態、TLSをprivateへ退避する
3. 停止直後の3次元と必要dataを新volumeへ複製し、worldを継承する。今回の試験用world・合成session・試験用権限は公開せず、健全な認証backendを再初期化しない
4. config／seed／旧キー不在、Geyser既定configとidentity、Discord本来の設定、MOTD、backupのnamespaceを確認する
5. 新セットを起動し、実argvの3G／3G、Java実体、doctor、Java status、Geyserの/v1/joinと必要なTCP／UDP19132、2組のScratch／WireScope／Bridgeを照合する。DNSはhuman owner
6. 新projectに向いたbackup・systemd・JST設定を確認し、実backupとoff-host download-verifiedを確認する。必要なsudo操作は具体的な差分を用意してhuman ownerへ渡す
7. 結果と未確認をcoordinatorへ返す。告知と横断判定はcoordinator／human ownerが行う。旧データ削除は別作業とする

必要な準備を終えた後の、停止から新セットの機械的確認までは従来の2〜5分を目安とします。10/20の切替は約2分、今回の新環境の通常起動は約30秒ですが、11/1切替そのものの実測ではありません。DNS・転送待ち・不具合対応は別です。

人間の参加確認をやり直さないという既存指定は維持します。今回も新たなlive-humanは追加していません。既存の人間試験の再利用範囲はcoordinatorが整理します。

## 5. Javaの実体・image・heap・container上限・flags

公開側を10/31に再読取しました。SSOTにある「公開VPSは25.0.3」という記述は訂正をお願いします。25.0.3は旧26.3事前試験のJavaであり、公開中のrc1はJava21です。

| 対象 | vendor／full version | 実heap／上限 |
| --- | --- | --- |
| 公開rc1／Paper1.21.11（10/31再読取） | Eclipse Adoptium、Temurin-21.0.11+10、runtime21.0.11+10-LTS | -Xms1G -Xmx1G。Docker memory／swap上限0＝未指定、cgroup memory.maxはmax |
| 10/29のrc2／#203事前試験 | Eclipse Adoptium、Temurin-25.0.3+9、runtime25.0.3+9-LTS | Xms512M／Xmx1536M、一時的な動作確認設定 |
| 10/31のstable候補／#231最終確認 | Eclipse Adoptium、Temurin-25.0.5+8、runtime25.0.5+8-LTS | 実argvで-Xms3G -Xmx3G。Docker memory上限未指定。起動・代表操作・通常再起動PASS |

- 公開sourceのimage：docker.io/itzg/minecraft-server:2026.7.2-java21@sha256:7f69fd6688e03495c8a8f5a46e8a8e82001b4465f4b55bdcd024c02c3624d8c8
- 旧#203試験のimage：docker.io/itzg/minecraft-server:2026.7.2-java25@sha256:6ec1110e4d9236d00ae9436a3e4a5929583e5b19cc94b756a7c603f7cf647a77
- 今回の25.0.5 image tag：mc-remote/paper-runtime:temurin-25.0.5-8-20261029
- 今回の実image ID：sha256:df6898c45b2decc621a320f09e79dcc700cc6f8852e219a38294269525f6ac1c

このimageは固定したitzgのjava25 imageをbaseに、公式Temurin JRE25.0.5+8だけを差し替えたものです。公式JREの61,736,206 bytes／SHA-256 6fac98f0c8202efc3135a9e9e42aa61963ec42d1c5cbb40caf231e7b14a24ef6を照合済み。起動のEnv／Entrypoint／Cmd等はbaseと同じで、正式なPaper公式コンテナという扱いではありません。

上のimage IDはDockerのconfig digestです。registryへ発行したmanifest digestや、別hostからpull可能な参照としては主張しません。最終preset用の正式な配布参照の確定は残ります。

公開中はrendererがheapを指定せず、image既定の1Gを使っています。安定版の採用値はhuman owner指定の3G／3Gへ変更しました。最初の最新版試験は512M／1536Mでしたが、その結果だけで済ませず、3G／3Gへ変えて代表操作と通常再起動を再確認したのが本票の最終結果です。公開側の1Gはまだ変更していません。

公開側・最終試験側とも、実argvに追加の-XX／-Xlogはなく、nogui引数もありません。今回の変更はheap指定であり、18項目のGC tuningを新しく追加していません。G1を既定から始める方針は[Java25の公式G1 tuning guide](https://docs.oracle.com/en/java/javase/25/gctuning/garbage-first-garbage-collector-tuning.html)とも整合します。3GはJavaヒープの量であり、Java全体・container全体の使用量の上限ではありません。

## 終了状態、添付、未完了

試験containerは停止済み、OOMなし。公開sourceのcontainer ID／StartedAt／lockは不変、source doctorは正常でした。公開環境の更新・停止・再起動は行っていません。

添付はfinal-result.json、final-pulse.json、restart-pulse.json、source-runtime-final.json、最新pluginの選定表とmetadata照合結果、b1273と旧#203の記録、Paper #231配布物照合、Java image準備記録とDockerfileです。旧記録は当時の条件のまま残しています。raw log、world、認証DB、試験tokenはprivateに保持し、本票へ秘密の値・実IP・プレイヤー名は含めません。

未完了は、製品preset／profileとheap3Gの正式反映、runtime imageの正式配布参照、connection_targets(a)の11/1セットへの適用（実装・検査済み、PR統合待ち）、exact setの凍結、11/1の公開切替です。授業相当の負荷・swap／GC分布・長時間容量試験は未実施で、今回の機能確認PASSを代用しません。

正式evidenceのrecord／artifact／INDEXへの配置はknowledge側でお願いします。10/28の4点とJava記録の受領、公開Javaの訂正、#231／25.0.5／3Gの新しい実績と上記未完了を、stable gateの現在地へ反映してください。
