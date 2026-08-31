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
- Java root package: `club.code2create.mcremote.client`
- Maven / Gradle group: `club.code2create.mcremote`
- Maven artifactId: `minecraft-remote-client`
- build: Gradle wrapper／`java-library`
- Java target: 21
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
