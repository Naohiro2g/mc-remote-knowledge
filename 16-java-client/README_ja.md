# Minecraft Remote for Java

現行Minecraft Remote ProtocolをJavaへ投影する、一般用途Client Libraryの設計スポーク。

## 現在地

`2026-08-29-06`でPhase Aを開始し、`2026-08-29-07`で既存McRemote／C2CC配下へJava namespaceを改訂した。

- repository: `Naohiro2g/minecraft-remote-java`
- bootstrap元commit: `862fa363274e314b28454c662d48b757c8134cee`
- bootstrap実装commit: `4300c5de42cfb8c731361de463f5e4a8a15f402e`
- C2CC namespace改訂commit: `19ebccbcca2d0eba1d197ab9cb2e7512797907df`
- Java root package: `club.code2create.mcremote.client`
- Gradle logical group: `club.code2create.mcremote`
- build: Gradle wrapper／`java-library`
- Java target: 21
- Java bootstrap baseline: protocol 23.0.0／artifact 2300.0.0b6

Gradle clean build、unit test、Java 21 classfile確認と
[GitHub Actions CI](https://github.com/Naohiro2g/minecraft-remote-java/actions/runs/33250749563)はPASSしている。

Classic `Naohiro2g/minecraft_remote_java`は現行化せず履歴として温存する。

## 正本境界

- wire／versioning／authentication等のProtocol contract: `10-protocol`
- 多言語展開の進行: `10-protocol/polyglot-client-roadmap_ja.md`
- Classic温存、baseline、判断順位、最小縦slice: `2026-08-29-04`
- repository、Phase A開始: `2026-08-29-06`
- C2CC／Minecraft Remote／Client Libraryのnamespace分離: `2026-08-29-07`
- 実装、build、Javaに閉じるClient API判断: `Naohiro2g/minecraft-remote-java`

Java実装の判断順位は次である。

1. 現行Protocol SSOT
2. Java bootstrap baseline上のPython Client Library外部挙動
3. Python内部実装

Protocolまたは複数Client Libraryへ波及する発見は、Java repositoryのlocal `NOTES_ja.md`からsession／slice終端の
escalation sweepでhub `00-hub/NOTES_ja.md`へ運ぶ。

## Buildとpublicationの境界

Gradle project名`minecraft-remote-java`はrepository／local build identityであり、Maven artifactIdを確定しない。
bootstrapには`maven-publish`、公開repository、signing、release versionを入れない。

未確定の公開事項は次である。

- artifactId: `minecraft-remote`／`minecraft-remote-client`
- Maven Centralの親namespace `club.code2create`の検証状態
- Maven向けrelease version表記

Maven Centralの[現行namespace規則](https://central.sonatype.org/register/namespace/)ではDNS由来namespaceはdomainを
exact reverseし、検証済み親namespaceのpublisherはその子groupIdも利用できる。
したがって`code2create.club`に対応する`club.code2create`をCentral Portalで検証できれば、
project group `club.code2create.mcremote`を公開に利用できる。現時点ではownership／Portal verificationを確認済みとは主張しない。

Pluginは既存package `club.code2create.mcremote`を維持する。Client Libraryはその下の
`club.code2create.mcremote.client`を使い、同じproject familyを示しながらPluginとのsplit packageを避ける。

## 次の縦slice

Phase BはJava bootstrap baselineに対して次を一本通す。

1. 既存shared fixtureをJavaから消費できるか確認する
2. TCP＋line-delimited JSON-RPC 2.0
3. `hello`／protocol negotiation
4. authenticationと初回pairing path
5. `world.setBlock`／`world.getBlock`
6. 実Minecraft worldでwrite／readを確認する

DEBUG／TRACE／FAST、`connection.flush`、catalog、event、player／entity等の追加順序は、この縦slice後にJava側で決める。
