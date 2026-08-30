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

次はPhase Cとして、単独利用可能なClient Libraryへsurfaceを広げる。追加順序はJava repoの局所計画で決め、
Pythonのmethod数を機械的に埋めず、Protocol capabilityとJavaに自然なAPIを較正する。

DEBUG／TRACE／FAST、`connection.flush`、catalog、event、player／entity等の追加順序は、この縦slice後にJava側で決める。

Client repoの最小examplesと`mc_remote_samples`の多言語比較面の役割分離は`2026-08-30-01`および
`20-教材/client-sample-learning-ux_ja.md`を正とする。
