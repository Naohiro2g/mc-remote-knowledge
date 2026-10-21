# Minecraft Remote for Java

現行Minecraft Remote ProtocolをJavaへ投影する、一般用途Client Libraryの設計スポーク。

## 現在地

`2026-08-29-06`でPhase Aを開始し、`2026-08-29-07`で既存McRemote／C2CC配下へJava namespaceを改訂、
`2026-08-29-08`でMaven artifactIdを確定した。

- repository: `Naohiro2g/minecraft-remote-java`
- bootstrap元commit: `862fa363274e314b28454c662d48b757c8134cee`
- bootstrap実装commit: `4300c5de42cfb8c731361de463f5e4a8a15f402e`
- C2CC namespace改訂commit: `19ebccbcca2d0eba1d197ab9cb2e7512797907df`
- Maven artifactId確定commit: `1c7512ed53550caa55596e0c3caf973efaad7431`
- Phase B／examples commit: `f259b396bfbde6e37e65b3c7916c25af37dc6a29`
- session credential UX commit: `af95e9ce5202926533d053d9e6d97befc7d006ee`
- Phase C代表capability commit: `20c47bd2c862b100084ef713ee52f72759fa2d0e`
- README・APIリファレンス・作例の先行準備commit: `66814b992e629deec60028d4af0d978212477526`
- Java root package: `club.code2create.mcremote.client`
- Maven / Gradle group: `club.code2create.mcremote`
- Maven artifactId: `minecraft-remote-client`
- build: Gradle wrapper／`java-library`
- Java target: 21（build・test・実行はmiseで選ぶJDK 21か25）
- Java bootstrap baseline: protocol 23.0.0／artifact 2300.0.0b6

Gradle clean build、unit test、Java 21 classfile確認、`minecraft-remote-client.jar`／sources JAR生成と
[GitHub Actions CI](https://github.com/Naohiro2g/minecraft-remote-java/actions/runs/33253559318)はPASSしている。

Phase BのTCP、改行区切りJSON-RPC 2.0、`hello`／protocol negotiation、authentication／初回pairing、
`world.setBlock`／`world.getBlock`、closeはJava bootstrap baselineの実serverまで通った。unit 8件とbuildがPASSし、
Minecraft 1.21.11でpairing、chat、AxisFlat、block write／readを確認した。README連動の`examples/`は同じGradle buildで
検証され、`MyWorld`、Hello、Set and Read、AxisFlatを持つ。

Classic `Naohiro2g/minecraft_remote_java`は現行化せず履歴として温存する。

## 正本境界

- wire／versioning／authentication等のProtocol contract: `10-protocol`
- 多言語展開の進行: `10-protocol/polyglot-client-roadmap_ja.md`
- Classic温存、baseline、判断順位、最小縦slice: `2026-08-29-04`
- repository、Phase A開始: `2026-08-29-06`
- C2CC／Minecraft Remote／Client Libraryのnamespace分離: `2026-08-29-07`
- Maven artifactId: `2026-08-29-08`
- 実装、build、Javaに閉じるClient API判断: `Naohiro2g/minecraft-remote-java`

Java実装の判断順位は次である。

1. 現行Protocol SSOT
2. Java bootstrap baseline上のPython Client Library外部挙動
3. Python内部実装

Protocolまたは複数Client Libraryへ波及する発見は、Java repositoryのlocal `NOTES_ja.md`からsession／slice終端の
escalation sweepでhub `00-hub/NOTES_ja.md`へ運ぶ。

## Buildとpublicationの境界

Gradle project名`minecraft-remote-java`はrepository／local build identityであり、Maven artifactIdとは別である。
Maven coordinateの確定部分は次とする。

```text
club.code2create.mcremote:minecraft-remote-client
```

bootstrap buildではarchive名も`minecraft-remote-client`へ固定するが、`maven-publish`、公開repository、signing、
release versionはまだ入れない。

未確定の公開事項は次である。

- Maven向けrelease version表記
- POM metadata／Javadoc JAR／signing／publish手段のexact設定

Maven Centralの[現行namespace規則](https://central.sonatype.org/register/namespace/)ではDNS由来namespaceはdomainを
exact reverseし、検証済み親namespaceのpublisherはその子groupIdも利用できる。
`code2create.club`に対応する親namespace `club.code2create`は、2026-08-29にCentral Portalのbadgeが`Verified`であることを
人間確認した。このnamespace権限により、project group `club.code2create.mcremote`を公開に利用できる。
`io.github.naohiro2g`も既存のverified namespaceだが、採用済みのproject family identityは変更しない。
Maven Centralへのdeployment／公開はまだ実施していない。

Pluginは既存package `club.code2create.mcremote`を維持する。Client Libraryはその下の
`club.code2create.mcremote.client`を使い、同じproject familyを示しながらPluginとのsplit packageを避ける。

## release trainとの関係（`2026-09-30-04`）

Javaは横断release trainへ同期せず、公開済みのreleaseを固定して追従する。追従の対象は公開tag／commit、protocol
version、fixture／artifact identityで固定する。Javaの機能充足、同期release、Maven公開、Java公開API全体のfreezeを、
横断releaseの完了条件にしない。b8にもb9にもJavaを含めない。

b9までは、freezeと移管に役立つ準備を先に進める。契約の疑問点の棚卸しとb9 freeze前の返却、consumerとしての依存の
明示、再現できる検証の入口、README／examples／対応範囲の整合である。初回stable（GitHubのLatest）の後、b9で移管した
新しいownerと取得経路で実装を追従し、移管を再検証する（[移管評価計画](../10-protocol/protocol-tooling-migration-plan_ja.md)）。

初回stableの後は、公開tag、解決先commit、protocolを固定し、契約、wire、fixtureを`66814b9`の時点の参照値と照合する。
差分が無いと確かめた範囲は、下の「README・APIリファレンス・作例の先行準備」のPASSを使い回し、同じ試験を自動では
やり直さない。版番号の文字列が同じだけでは差分なしとしない。fixtureの取得元をminecraft-remote-toolingへ切り替えることと、
まだつないでいない共有fixtureをtestへつなぐことは残っており、必要なtestを実行して仕上げてからPhase Cの機能追加へ進む。
Phase Cの順序はJava repoの局所案（`docs/post-latest-plan_ja.md`）のままとし、横断contractへ固定しない。Javaの再検証を、
移管全体の完了判定や横断releaseの条件にしない。

## Phase B後の進行

Phase Bの最小縦sliceは`f259b396bfbde6e37e65b3c7916c25af37dc6a29`で成立した。

Phase Cとして、単独利用可能なClient Libraryへsurfaceを広げる。追加順序はJava repoの局所計画で決め、
Pythonのmethod数を機械的に埋めず、Protocol capabilityとJavaに自然なAPIを較正する。

DEBUG／TRACE／FAST、`connection.flush`、catalog、event、player／entity等の追加順序は、この縦slice後にJava側で決める。

Client repoの最小examplesと`mc_remote_samples`の多言語比較面の役割分離は`2026-08-30-01`および
`20-教材/client-sample-learning-ux_ja.md`を正とする。

### Phase C代表capability projection（実装済み）

`20c47bd2c862b100084ef713ee52f72759fa2d0e`で、Javaに自然な型付きAPIとして次を代表投影した。

- server-authoritativeな`catalog.get`
- `player.getPose`／`player.setPose`
- protocol 23 event unionと`events.poll`
- `world.spawnParticle`
- 二面signの`world.getSign`／`world.setSign`／`world.updateSignLine`

Demo 02 Protocol 23 Tourは、catalog、player pose、有限event pollをterminalへ表示し、signとparticleをMinecraftで
観察できる入口を持つ。demoは`player.setPose`を実行して学習者を不意にteleportせず、event監視を自動常駐させない。

Java wire testは、Scratch owner commit `df9264ec355dd722a848df46e96d4b0fc9340ca2`の
`mc-remote/protocol/test/fixtures/`から次のfixtureをbyte-for-byteで取り込み、SHA-256を固定して消費する。

| fixture | SHA-256 |
| --- | --- |
| `events-v23.json` | `31760d267f3c2641042fbe8595fda9c259134a1c05423271a99cb74da1efa9aa` |
| `sign-v23.json` | `7ffb63c264602cba56117eefff1f9604b955df04c5cc655e877772b8ff7cd30e` |
| `spawn-v22.json` | `1120e6c8d41b05b65c916fa96f496b02884123ec7ef59b0a226eea48bebf3abd` |

fixture copyはtest入力であり、新しいProtocol正本ではない。protocol 22のparticle shapeはprotocol 23でも変更せず使う。

Gradle wrapperのclean build、core 20件＋examples 12件のunit／deterministic test、Javadoc生成、Java 21 classfile
major 65、[GitHub Actions build](https://github.com/Naohiro2g/minecraft-remote-java/actions/runs/33386956086)はPASSした。
搬送票では、Minecraft 1.21.11／protocol 23.0.0実serverへ保存済みsession tokenからpairingなしで接続し、catalog
blocks 1166／entities 157／particles 115とhash、player pose read、sign set→line update→get、particle
accepted 30、空event ringの`events.poll`を確認したと報告された。看板はtest worldの絶対座標`(304,96,304)`に残し、
[live-human追補画像](https://github.com/Naohiro2g/mc-remote-knowledge/issues/3#issuecomment-5477701392)でfront faceの4行、
gold＋bold、aquaを含むtext／color／decoration投影を確認した。particleは一時表示のため画像から追加主張しない。
`player.setPose`はdeterministic testだけで確認し、live playerを移動していない。

この到達はPhase Cの代表projectionであり、Phase C／Milestone C全体の完了を意味しない。Java bootstrap baselineの
protocol 23.0.0／artifact 2300.0.0b6を維持し、b7以降のdirection、Protocol wire、Python／Scratch API、artifact
coordinate、公開version／publish flowを変更しない。

### 認証UX slice（実装済み）

`af95e9ce5202926533d053d9e6d97befc7d006ee`で、starter／examples向けsession credential UXを実装した。
Javaの`CredentialStore` SPI、`none()`、`inMemory()`は維持し、core libraryへOS依存、GUI prompt、暗黙のfile作成を
持ち込まない。OS資格情報store adapterはexamples moduleへ隔離し、macOS Keychain、Windows Credential Manager、Linux
Secret Serviceから利用可能な保護storeを選ぶ。利用不能時は平文fileへfallbackせずin-memoryへ戻し、次回もpairingが
必要になることを秘密なしで警告する。

Java learner runnerの投影は次である。

- 初回は保存／memoryを既定回答なしで明示選択する
- `--no-save`は永続storeをread／write／clearせず、今回のprocessだけmemoryで動く
- `--forget`は選択targetのlocal tokenを削除して接続せず終了し、server revoke／logoutとは呼ばない
- logical credential scopeへJava application identity、session、TCP、`ServerTarget`を含める
- 物理keyはlogical scope全体のSHA-256 hashとし、private targetを通常logやOS backend labelへ露出しない

OS backendにはMicrosoft `credential-secure-storage` 1.0.3をexamples限定で使う。同libraryはarchive済みであり、古い
transitive JNA 5.9.0を使わないよう、公式Maven CentralのJNA 5.19.1へ明示固定した。

Gradle wrapperのclean build、core 15件＋examples 12件のunit／deterministic test、
[GitHub Actions build](https://github.com/Naohiro2g/minecraft-remote-java/actions/runs/33379032295)はPASSした。
保存／別instanceからの再読込、target分離、認証reasonでの該当entry削除、認可／版／network errorでのtoken温存、
backend利用不能時のmemory縮退、secret-free warningを確認している。GNOME Secret Service非接続時のread probeもPASSした。
搬送票では、Minecraft 1.21.11実serverで初回pairing後にOSへ保存し、別processの`--save hello`がpairing表示なしで期限内
session tokenを再利用して`chat.post`に成功したと報告された。macOS／Windowsの実機確認は未実施・未主張である。

このsliceはsession tokenの再利用であり、long-lived credentialを公開しない。横断意味は`2026-08-30-03`と
`00-hub/authentication-roadmap_ja.md` §1.1を正とする。

### README・APIリファレンス・作例の先行準備（2026-10-21）

`66814b992e629deec60028d4af0d978212477526`で、初回stableの前にJavaの入口を整えた。protocolが変わらない予定なので、
README、API、作例と既存機能のconsumer確認を先に済ませた。

- README：Pythonの「最初の成功→編集→作例→API」の導線にならい、JDKの選び方、接続先、ペアリング、tokenの保存を実行の
  順に案内する。pair codeは120秒、session tokenは発行から2時間
- APIリファレンス（`docs/java-api-reference_ja.md`）：JDKのdoclet APIで、公開メソッドの署名、recordの要素、enumの値を
  抜き出し、日本語の説明を付けて生成する。buildが生成結果と文書の一致を確かめる
- 作例：接続、block state、catalog、看板、event cursorの短い作例（`docs/java-examples_ja.md`）。実行できるサンプルに、
  読み取りだけの`inspect`と、時間を区切った`events`を足した。menuはサーバーに操作を拒否されても接続を保ち、`r`で同じ
  tokenを使って接続し直す。書き込みの自動再試行はしない
- JDK：build、test、サンプルの実行は、miseで選ぶJDK 21か25（既定は`mise.toml`の21）。classfileのtargetは21のまま。CIは
  21と25のmatrix（[GitHub Actions](https://github.com/Naohiro2g/minecraft-remote-java/actions/runs/39596340985)、両方PASS）
- 変えていないもの：core library、要求protocol 23.0.0、vendor fixture、Maven coordinate、公開versionとpublishの流れ

JDK 21と25のそれぞれで、core 23件＋examples 20件の43件がPASSし、core／examplesの全classfileがmajor 65だった。examplesの
20件には、サンプル本体をloopback TCPの23.2.1のpeerで動かす互換test 8件（request形、cursor、整地の分割、拒否の後の継続、
同じtokenでの再接続）を含む。rc1のtooling `6447f6e8cbfbeeb9d229990b5c4f6e82a5875666`から取った既存fixture 3本は、vendor copyと
bytes、SHA-256が一致した。

搬送票では、箱庭（公開VPSのベータ、rc1、Minecraft 1.21.11／protocol 23.2.1）で、ペアリングの後にchat、catalog（blocks 1166／
entities 157／particles 115）、pose read、AxisFlat、金ブロックのwrite／read、看板のset／update／get、particle accepted 30、
空event ringの有限poll、cleanupと再実行が成功し、別processの`--save hello`がペアリングなしで接続してchatを送ったと
報告された。稼働JARのdigestを固定した試験ではない。非空event、axis-flat-clearのlive、Minecraft 26.3、macOS／Windowsの
保護storeは確かめていない。

途中でsetBlockが`build_denied`になったのは、箱庭のLuckPermsに`mcr.build.blocks`が無かったためだった。LuckPermsがある
環境ではmetaが無いと上限0になる（b10からの仕様、[platform design](../11-plugin/platform-design_ja.md) §8.2）。human ownerが
playerとdefault groupに設定し、接続し直して直った。認証やchatが通っても、ブロックを置く量の上限を満たしているとは限らない。
