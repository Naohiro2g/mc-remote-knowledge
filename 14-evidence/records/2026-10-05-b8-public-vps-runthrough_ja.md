# b8の公開VPS配備と独立ランスルー（2026-10-03、2026-10-05）

> test class: `live-auto`（Stack担当と独立担当の実施報告）+ `live-human`（human ownerの報告とtranscript）。release gateの再判定ではなく、
> 公開したb8を公開VPS（official-public-beta、ケータリング方式）へ配備した後の検証。Stack担当の確定搬送票（mc-remote-stack、
> 2026-10-05）による。coordinatorは素材を要約しただけで、配備を照合していない。

## 素材

`14-evidence/artifacts/2026-10-05-b8-public-vps-runthrough/`。Stack担当が選んだ素材5件（`materials-index.json`のSHA-256と一致）と
搬送票。private host、token、UUID、world／credential／TLSの実データ、画像、raw server logは含まない。

## 2026-10-03：初回配備（Stack担当）

- 入力: knowledge `2a8c3ea`、preset `public-web-paper@12`、公開b8のmanifest（McRemote `v1.21.11-2320.0.0b8`、Scratch `v2320.0.0b8`、
  Python `v2320.0.0b8`）。JARは公開した`fdffaf0c…80c6`
- 旧deploymentの停止時の入力と3 volumeを保存し、world、LuckPermsのDB、McRemoteのsnapshotとauthority、TLSを一組で新しいdeploymentへ
  引き継いだ。全source fileの内容一致を確かめて公開入口を切り替えた
- live-auto（報告）: operatorとdoctorが正常、artifactのidentityが一致、credential `HEALTHY`、LuckPerms使用、外部のHTTPS、Java版の
  status、Bedrock UDP 25565。UDPの入口はhost filterの19132を25565へ直して永続化した（human owner）。backupのZIPのCRCと収録、
  off-hostへの転送と再取得のhash一致
- live-human: Scratch b8からpairingし、`23.2.0`の`hello`と`chat.post`が成功。認証前の`hello`は`auth_required`。iPadからworldへ
  入れた（human ownerの報告）
- 2026-10-04: homepageをknowledge `ceba530`（全79 file、`api/scratch`を含む）へ更新し、公開HTTPSの取得内容をsourceのGit blobと照合

## 2026-10-05：会話履歴を共有しない別セッションでの再構築

- mainの公開手順、SSOT、private opsの情報だけから、別deploymentを作って同じ公開入口へ切り替えた（Stack main `6cdbe6e`、knowledge
  `561de98`）。最初はStack #66が未統合で`unknown_preset_revision`となり、サービスを止めずに報告し、統合後に同じ地点から完走した
- live-auto（独立担当の報告）: profile `vps-server@12`／preset `public-web-paper@12`、公開b8のidentityが一致。3 volumeの全fileを
  cmp、tar header、SHA-256で照合して引き継いだ。McRemoteのsnapshotは保存時と起動後とも39件、authorityは不変で、domainの
  再初期化やtokenの期限延長はしていない。旧deploymentの停止要求からdoctor正常まで1分53秒。外部のHTTPS、Java TCP 25565、
  Bedrock UDP 25565、McRemote TCP 25575（認証前は`auth_required`）。ServerBackupの生成は、既定のuserで拒否された後、実行時の
  UID:GIDに合わせて成功し、暗号化、転送、off-hostの再取得のhash一致まで
- live-human: 保存tokenの`hello`は`token_expired`、その後の`hello`が`23.2.0`／`1.21.11`で成功し、`chat.post`も成功
- 実行漏れ: 配備の前に製品noticeと運用者noticeを人間へ見せて選んでもらう段階を漏らした。停止と起動の報告も分かりにくかった。
  Stack #65（main `68b8d45`、368 tests PASS）で、noticeの事前の選択、停止と起動の進行の報告、ServerBackupの生成時のUIDの確認を
  手順へ足した。直した手順での新たな実機の切り替えはしていない

## 主張しない範囲

10月5日の`auth.*`の中間transcript、ゲームのeditionごとの参加、WireScopeの全画面の操作。10月5日にiPadの参加を再試験したとは
扱わない。backupの復号、worldの復元、旧setへの切り戻し。b9の配備（Bridge OCIのcontainerとしての起動の確認を含む）はこの記録の
範囲外。
