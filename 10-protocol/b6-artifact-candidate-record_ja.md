# b6 artifact candidate記録

> 2026-08-27時点の`b6-artifact-candidate-set-1`を、人間が照合できる形で固定する記録です。
> 公開release manifest、machine-readable gate manifest、配布済みartifactの主張ではありません。
> Tier 2で生じたset 2／3は§7へ、official-public-beta適用時の後続修正は§12へ追記し、
> set 1〜4とGitHub prereleaseの原記録を上書きしません。

## 1. 状態と用途

三repo共有fixture gateをPASSした`b6-source-candidate-set-3`から、sourceを変更せず未公開artifactを生成した。
この七ファイルを一組として、protocol `23.0.0`／artifact `2300.0.0b6`の通常dev Tier 2横断pulseへ
投入する。component単独のbuild再現性とtestは確認済みだが、実plugin接続、shared環境deploy、正式evidence、
default branch統合、公開releaseはまだ行っていない。

## 2. Exact source set

| component | branch／source SHA |
| --- | --- |
| McRemote | `codex/b6-protocol23-cleanup@88d818703be5e7314bc1e45597a66237796db641` |
| Python | `codex/b6-protocol23-python@0ba22e80b9b1b339dfd11085b1b24cef646599b2` |
| Scratch／Bridge／WireScope | `agent/b6-source-refresh@104f194deddc9c244e6e07c4223965c792551f9d` |

共有fixtureはScratch `@mc-remote/protocol`をownerとし、`sign-v23.json`のSHA-256は
`7ffb63c264602cba56117eefff1f9604b955df04c5cc655e877772b8ff7cd30e`、
`events-v23.json`は`31760d267f3c2641042fbe8595fda9c259134a1c05423271a99cb74da1efa9aa`である。

## 3. Exact artifact set

| component | artifact | size（bytes） | SHA-256 |
| --- | --- | ---: | --- |
| McRemote | `mc-remote-1.21.11-2300.0.0b6.jar` | 204,341 | `4e28603caefa4273fabfe325e1c75a28239a6fa9eb44fb5a2b49da7be79870e8` |
| Python | `minecraft_remote_api-2300.0.0b6-py3-none-any.whl` | 173,301 | `0887807f0d00f71fcb543caf16c3963b70580bf073b6a7576d7f274399a1877b` |
| Python | `minecraft_remote_api-2300.0.0b6.tar.gz` | 178,483 | `0507a10cbd6b31c2dd84ebff0034c5f72625ff1142d30f1c0d41e14d0ce2da3b` |
| Scratch | `scratch-gui-build.tar.gz` | 234,622,982 | `3ba9940ebd2d60f70e20a45a5a29f1d2614caf79b5c87f13236139994d40f617` |
| Bridge | `mc-remote-bridge-dist.tar.gz` | 3,052 | `11199a8e6966e8a5160411104934498657f4befd3d27a8fc25c88f51afa31c72` |
| WireScope | `wirescope-app.zip` | 73,525 | `06a6fb44009cee27a355ad38f7a3c554445fb98b31d3073afc04381fa5574b7d` |
| WireScope | `wirescope-app.manifest.json` | 2,321 | `a4440a27ebb5ecb3918be33a253211c78a668e645e3df63130296ce61fa6cad7` |

## 4. Build、test、再現性

### McRemote

- `./gradlew clean test jar`。Gradle `8.14`、Java toolchain `21`、実行JVM Corretto `25.0.3`
- Paper API `1.21.11-R0.1-SNAPSHOT`、plugin API／Minecraft `1.21.11`
- Linux `7.0.0-30-generic` x86_64。JAR taskはtimestamp非保持、file order再現可能設定
- unit／deterministic `143/143` PASS
- 独立したclean build三回でJARがbyte-for-byte一致

### Python

- `uv build`。uv `0.11.7`、`uv_build>=0.11.7,<0.12.0`、build host Python `3.11.9`
- 独立export上で`242/242` PASS
- wheelを別venvのPython `3.11.6`へinstallし、package version、protocol、sign surfaceを確認
- `git archive`から作った独立二directoryでwheel／sdistがbyte-for-byte一致

### Scratch／Bridge／WireScope

- Scratch GUIはNode `24.19.0`、npm `11.12.1`、webpack `5.109.2`で`npm ci`後に
  `NODE_ENV=production npm run build`
- GUI tarはpath順、mtime `UTC 1980-01-01`、owner／group `0`、numeric ownerへ固定して生成
- Bridgeは`npm run build --workspace=mc-remote/bridge`。TypeScript `5.9.3`、rolldown-vite `7.3.1`で
  buildし、`npm test`を`30/30` PASS
- WireScopeは`npm run build:artifact --workspace=@mc-remote/live -- --source-commit 104f194deddc9c244e6e07c4223965c792551f9d`
- Scratch GUI unitは`471/472` PASS（残り一件は既知のskip）、lintはerror `0`
- GUI三回、Bridge二回、WireScope三回の生成で、それぞれbyte-for-byte一致
- WireScope detached manifestのsource commitと内部ZIP digestを照合済み

各component担当はclean sourceからの生成と再現性を報告した。coordinatorはローカルに返された七ファイルを
再hashし、上表のsize／SHA-256、source branchのremote HEAD、JAR／wheel／WireScope manifestの埋め込みidentityを
照合した。build／testそのものをcoordinatorが再実行したという主張には広げない。

## 5. 固定境界と失効条件

`b6-artifact-candidate-set-1`は、次の通常dev横断pulseに使う**未公開candidate bytesの固定**である。
公開release artifact freeze、tag、registry upload、default branch統合、shared環境への配置完了を意味しない。
現物はdev repoと一時領域にあり、公開配布元や永続CASをまだ持たない。

次のいずれかが変わればset 1を失効させ、新しいsource／artifact setとして再申告する。

- §2のsource SHAまたは共有fixture bytes
- §3のartifact bytes、ファイル名または埋め込みversion
- Tier 2で見つかった修正により生成元sourceが変わる場合

build環境の差だけでbyte列が変わった場合も、既存digestへ一致するまで同一setとして扱わない。

## 6. 次のgate

人間承認により通常dev integration targetを`m720s2`のhost-native `dev-integration`へ固定した。server側は
既存のPaper `1.21.11-132`、world、config、credential backendを維持し、現行b5 JARをrollback入力として
`plugins`外へ保持してb6 JARだけを交換する。§3のworkstation側artifactも同じset identityでstageする。

2026-08-27、七artifactをworkstationのdurable gate stagingへ配置して全digestを再照合し、server側は
上記境界でb6 JAR一件へ交換した。Paper／McRemote version、credential `HEALTHY`、標準port、protocol 23の
tokenなし／無効token hello否定パスをPASSした。これはserver runtime readinessであり、sign、poke、handle、
Scratch／WireScopeの製品API横断PASSではない。

runtime readiness後、exact Python wheelによる認証済みhello、sign三操作、`mcr_eh_` handleと、exact Bridge
buildによるone-shotから実plugin未認証境界までをPASSした。結果と未実施境界は
[`2026-08-27-b6-tier2-integration-pulse`](../14-evidence/records/2026-08-27-b6-tier2-integration-pulse_ja.md)
へ着地した。Bridge tarは`dist/`だけでproduction dependencyを含まないため、Tier 2ではexact source installの
`ws 8.18.3`を外部runtime入力として固定した。単独deploy可能artifactとは扱わず、公開配布形態のartifact gateで閉じる。

残る最小pulseは、Scratch実ブラウザのpairing／sign／browser保存、WireScope表示filterと`dropped_frames`、
`pickaxe_poke`の一操作一eventと腕振りである。人間参加結果をrelease根拠へ使う場合は、同recordへsanitized結果を
追補するか、scopeを分けたformal evidenceを`14-evidence/`へ作る。

公開release、tag、registry upload、default branch統合は、このTier 2 pulseの結果をgate coordinatorへ返すまで
行わない。

## 7. Scratch／WireScope後続set

Tier 2実browserで二件のclient-only UX不具合を観測したため、set 1の観測事実を消さず、Scratch側だけを
change coneに沿って更新した。

### 7.1 set 2 — mini dropdown修正

`b6-artifact-candidate-set-2`は、Scratch GUIを
`agent/b6-source-refresh@1d1b21d5acdbabdb596476c087c14033d5c33d32`から生成した
234,620,525 bytes／SHA-256
`1757f665b9c327985fdbd101a356a82926daa4a00361694ce5b059f78dda7ef5`へ置換した。tab行へ移したminiの
dropdownが親panelの`overflow: hidden`でclipされる不具合を直し、Code／Costumes／Sounds、折りたたみ、palette
非干渉をreal-browserでPASSした。plugin、Python、Bridge、旧WireScope artifactはset 1からexact bytesで再利用した。

set 2の実接続中、空振りOFFでもpending `events.poll` requestが一瞬表示され、約1秒周期の全table再構築がpayloadの
選択／copyを壊す不具合を観測した。したがってset 2を公開release候補へ進めず、失敗を次setの入力として保持する。

### 7.2 set 3 — poll pair安定化＋表示一時停止

`b6-artifact-candidate-set-3`はset 2からMcRemote、Python、GUI、Bridgeをexact bytesで再利用し、WireScopeだけを
scratch-editor `agent/b6-wirescope-poll-pair-stability@24077ef005e4969bf3a7434b45532ae53cefbc28`の
artifactへ置換した。共有fixture、protocol、observer schema、Bridge、Scratch VM／GUI本体は変えていない。

| component | artifact | size（bytes） | SHA-256 | source／再利用 |
| --- | --- | ---: | --- | --- |
| McRemote | `mc-remote-1.21.11-2300.0.0b6.jar` | 204,341 | `4e28603caefa4273fabfe325e1c75a28239a6fa9eb44fb5a2b49da7be79870e8` | set 1再利用 |
| Python | `minecraft_remote_api-2300.0.0b6-py3-none-any.whl` | 173,301 | `0887807f0d00f71fcb543caf16c3963b70580bf073b6a7576d7f274399a1877b` | set 1再利用 |
| Python | `minecraft_remote_api-2300.0.0b6.tar.gz` | 178,483 | `0507a10cbd6b31c2dd84ebff0034c5f72625ff1142d30f1c0d41e14d0ce2da3b` | set 1再利用 |
| Scratch | `scratch-gui-build.tar.gz` | 234,620,525 | `1757f665b9c327985fdbd101a356a82926daa4a00361694ce5b059f78dda7ef5` | set 2再利用／GUI source `1d1b21d5ac…` |
| Bridge | `mc-remote-bridge-dist.tar.gz` | 3,052 | `11199a8e6966e8a5160411104934498657f4befd3d27a8fc25c88f51afa31c72` | set 1再利用 |
| WireScope | `wirescope-app.zip` | 79,169 | `b3d6270299195d2c3db93c9d122938be6ae20d23e0f10e19afe3b0e99e3ca315` | source `24077ef005…` |
| WireScope | `wirescope-app.manifest.json` | 2,321 | `5fafdc54af45d8f498cd48b13590797eaaa6316adaf017a40595566f0f507b2e` | source `24077ef005…` |

coordinatorは七fileを新しいdurable stagingへcopyし、全size／SHA-256を再照合した。WireScope manifest内のsource、
archive digest、package／lock identityも表と一致する。set 1／2のdirectoryとbytesは履歴として残し、上書きしていない。

直前commit `7b4f71d71e8ecd665d402682e677dc4e425d160f`は実plugin＋local Bridgeのreal-browserで、pending pollの
非点滅、空振りpoll継続中の選択／copy、非空poke pairの原子的表示、player groupのrequest／response一体切替を
PASSした。後続`24077ef…`のcurrent checkoutでは、表示一時停止、Scratch sign text-only v1、作品／スプライトbrowser
保存を同じ実plugin接続browserでPASSした。観測target変更後の自動再開とlive `dropped_frames`は未確認である。

Bridge tarは`dist/config-*.js`からexternal dependency `ws`をimportする中間buildであり、単独deploy可能なrelease
artifactではない。配布境界は新規設計せず、`2026-07-14-04`と既存Dockerfile／manual workflowどおり、`dist/`、
`package.json`、lock済み`node_modules/ws/`だけを非root runtimeへ入れるmulti-arch OCIを正とする。したがって残件は
tarへdependencyを足すことではなく、統合後のexact source identityからOCI index／platform digest、SBOM／provenanceを
生成・固定し、container smokeを通すことである。

Tier 2 requested sliceはPASSした。Scratch／Bridge OCI生成、default branch統合、正式release artifact freeze、公開releaseは
引き続き未完である。観測target変更後の自動再開とlive `dropped_frames`はclient-only補足で、b6 coreをHOLDにしない。

## 8. Default branch統合後のsource set

2026-08-28、三repoのcandidateをdefault branchへ統合し、次を`b6-integrated-source-set-1`として固定した。
これは**source identityの固定**であり、`b6-artifact-candidate-set-4`の成立や公開release artifact freezeを
意味しない。set 1〜3のbytesとTier 2観測は履歴として保存し、統合後artifactへ黙って読み替えない。

| component | default branch／統合後SHA | candidateとの関係 |
| --- | --- | --- |
| McRemote | `main@4e8f1ff1bd48bfa28c465f2dc24060fbb419317f` | `88d818703be5e7314bc1e45597a66237796db641`を包含。b6機能差分なし。main独自のsession token永続化fixを保持 |
| Python | `main@a30a37b15658da655fe1e3535a73fb0e80c06f56` | `0ba22e80b9b1b339dfd11085b1b24cef646599b2`を包含し、全source tree差分なし |
| Scratch／Bridge／WireScope | `develop@df9264ec355dd722a848df46e96d4b0fc9340ca2` | `24077ef005e4969bf3a7434b45532ae53cefbc28`をno-ff merge。conflict、手動編集、機能差分なし |

McRemoteのcandidateとの差分は`CredentialService`／`CredentialStore`／`TokenStore`と関連test二件だけである。
これはPR #6の`2978db56a93301cd85ed0393f1d0b985933d0096`で回復したsession token永続化で、
`CredentialService.java`のblobは、b4で実機PASSした`3496db9293baa6e1d4f79439cacbd239ba15e2b7`、
`2978db5…`、統合後mainの三者で同一である。統合後は`./gradlew clean test jar`を149/149件PASSし、
JAR `mc-remote-1.21.11-2300.0.0b6.jar`のSHA-256
`0ec8d4c0b105f3034361b260fc39fcb78013e932e684d34d5ca95c9a6c6a87a6`をcomponent担当が報告した。
set 3のJAR `4e28603c…70e8`とはbyte列が異なるため、旧JARを最終artifactへ再利用しない。この新JARは
source set固定時点ではcoordinatorのdurable stagingへの返却と実runtime smokeをまだ終えていなかった。

Pythonはmerge後mainのclean tarballで242/242件をPASSし、wheel／sdistを再生成した。生成物はset 1〜3の
SHA-256 `0887807f…1877b`／`0507a10c…da3b`とbyte-for-byte一致した。最終setへ収容するときは、統合後mainからの
再生成事実とbytesを結び直す。

Scratchはprotocol 22/22、WireScope 130/130、Bridge 30/30、GUI 471件PASS＋既知1 skip、各lint／buildを
PASSした。scratch-vmのaggregate報告は4003件中3998件PASSで、担当は残る2件を既知の並列resource競合、
isolated 283/283件PASSと判定した。一方、総数との差5件のうち残り3件のstatus内訳が返却にないため、
最終artifact freeze前にpassed／failed／skipped等のexact集計だけを補う。これは現時点で新規regressionを
示すものとは扱わない。Scratch／WireScope artifactはsource set固定時点では統合後developから未生成だった。

次のartifact gateは、統合後sourceからJAR、wheel／sdist、GUI、WireScope ZIP／manifestを生成・durable stagingへ
固定し、Scratch／Bridgeは既決のmulti-arch OCIとして生成することである。GHCR pushを伴う現行workflowの実行は人間承認を
待つ。McRemoteはcredential実装の既存PASSをchange cone外として再利用する一方、新JARでserver起動、credential
`HEALTHY`、期限内session tokenの再起動継続、代表protocol 23呼出しを最小統合smokeする。sign／poke／browser保存／
WireScopeの全Tier 2試験は繰り返さない。

## 9. 統合後artifact入力（pre-OCI）

coordinatorは`b6-integrated-source-set-1`の三default branchを個別のclean export／isolated checkoutへ固定し、
Scratch／Bridge OCIを除く次の六artifactを再生成した。これを`b6-integrated-artifact-input-1`としてdurable stagingへ置き、
全fileをcopy後に再hashした。入力manifestは2,127 bytes、SHA-256
`1a3b40fc3747359bd2a206f37aa4b8508989b97aedc6b6d584d8cfd49b3c4a4b`である。

| component | artifact | size（bytes） | SHA-256 |
| --- | --- | ---: | --- |
| McRemote | `mc-remote-1.21.11-2300.0.0b6.jar` | 204,463 | `0ec8d4c0b105f3034361b260fc39fcb78013e932e684d34d5ca95c9a6c6a87a6` |
| Python | `minecraft_remote_api-2300.0.0b6-py3-none-any.whl` | 173,301 | `0887807f0d00f71fcb543caf16c3963b70580bf073b6a7576d7f274399a1877b` |
| Python | `minecraft_remote_api-2300.0.0b6.tar.gz` | 178,483 | `0507a10cbd6b31c2dd84ebff0034c5f72625ff1142d30f1c0d41e14d0ce2da3b` |
| Scratch | `scratch-gui-build.tar.gz` | 234,620,525 | `1757f665b9c327985fdbd101a356a82926daa4a00361694ce5b059f78dda7ef5` |
| WireScope | `wirescope-app.zip` | 79,169 | `b3d6270299195d2c3db93c9d122938be6ae20d23e0f10e19afe3b0e99e3ca315` |
| WireScope | `wirescope-app.manifest.json` | 2,321 | `8570d3eed8024d32324806a28d4b7a40da1d2774d39e6e95bcb2c43206e6296f` |

McRemoteはclean exportで149/149件と`clean test jar`をPASSし、component返却digestを独立再現した。
Pythonは242/242件をPASSし、wheel／sdistが旧setと同一bytesになることを再確認した。Scratchはisolated checkoutで
Node `24.19.0`／npm `11.12.1`、`npm ci`、全workspace production buildをPASSした。GUI tarは旧set 3と
byte-for-byte同一である。WireScope artifact scriptは二回とも同じZIP／manifestを生成し、ZIPは旧setと同一、
manifestだけがsource commitを統合後`df9264ec…`へ更新したため新digestになった。

coordinatorが追加で実行したscratch-vm full TAPは、assertion-levelの4003件集計を返さず、file-level
`132 total／11 fail／121 skip`となった。失敗は並列renderer初期化、SIGKILL、timeoutを含み、ownerが報告した
isolated PASSと同型のrunner／resource診断である。この実行を4003件のPASS／FAIL内訳へ読み替えず、ownerから
exact passed／failed／skipped集計が返るまで§8の確認事項を維持する。

通常devではオンラインplayer 0、旧candidate JARのrollback入力を確認してからJAR一件だけを統合後bytesへ交換した。
Paper、world、config、credential backendを維持し、起動、version、標準listener、credential `HEALTHY`、auth否定
4 path、新規sessionの認証済みhello＋`catalog.get`をPASSした。さらに同じJARを正常停止・再起動し、pairingなしで
同じ期限内session tokenを再利用して認証済み`catalog.get`をPASSした。正式記録は
[`2026-08-28-b6-integrated-artifact-smoke`](../14-evidence/records/2026-08-28-b6-integrated-artifact-smoke_ja.md)
を正とする。

既存`run.sh`が自身で名前付きScreenを作るため、別Screenで包んだ最初の起動操作はserver開始前に終了した。
listenerは作られず、dead outer sessionを除去して`run.sh`を直接実行するとPASSした。JAR、world、config、credential
backendはこの訂正で変更していない。この運用観測を製品artifactのFAILへ読み替えない。

本identityは**pre-OCI input**である。Scratch ownerのexact test集計、Scratch／Bridge multi-arch OCI、最終artifact set、
公開releaseはまだ主張しない。

## 10. 統合後OCIと最終artifact candidate

プロジェクトオーナーの明示承認後、scratch-editorのmanual workflow
[`Build McRemote OCI Images`](https://github.com/Naohiro2g/scratch-editor/actions/runs/33136505029)を、
統合source `develop@df9264ec355dd722a848df46e96d4b0fc9340ca2`から一回実行した。run
`33136505029`はScratch／Bridgeのmulti-arch build、source stamp検証、GHCR push、identity JSON生成、
artifact uploadをすべてPASSした。identity JSONのSHA-256は
`f7229cf2484858867a52b782f8de89c358b6920532555f06e955f05e08413634`である。

| image | identity |
| --- | --- |
| Scratch index | `ghcr.io/naohiro2g/mc-remote-scratch@sha256:fecd0b46b287be37038e7dfa82f926fbc1c55fea6811522ef33539373452d851` |
| Scratch `linux/amd64` | `sha256:61ea9f2ad719a85e4c39e97f7db30cf9be72b8b87da67bd29e0323ad8cb9f613` |
| Scratch `linux/arm64` | `sha256:6d5ad4eabdee00c96a2222f47671421501e29191721aedab6ce77116fc68bd38` |
| Bridge index | `ghcr.io/naohiro2g/mc-remote-bridge@sha256:a115d1e62bcde78580515a88d564b0871049a999386c6cb33703b300389d14f8` |
| Bridge `linux/amd64` | `sha256:676c960fd1c72a6490cb6a12928c816de0ce19e42f935aaa5e01ea98eae99617` |
| Bridge `linux/arm64` | `sha256:bd7a40dc94ed6428781c30b7e56a8fa63197d8f415751054404203fd458e0ed6` |

workflow artifactだけでなく、registryに対する独立した`docker buildx imagetools inspect`でも両index、
platform digest、各platformに付随するattestation manifestの一致を確認した。Docker daemonやMinecraft
serverの変更は伴わない。

§9の六artifactと本節の二OCI indexを`b6-artifact-candidate-set-4`として固定する。Scratch VMのaggregate
報告には総数と内訳の表記差が残るため「full suite exact集計PASS」とは主張しない。一方、component担当のpackage別
PASS、失敗対象のisolated PASS、production build、Tier 2実ブラウザ、統合後sourceからの再現buildは成立しており、
新規regressionを示す観測はない。この集計表記だけを目的とした再実行はb6 release blockerにしない。

b6の横断機能検証はhost-native通常devと実ブラウザで完了している。OCIはScratch／Bridgeの配布形態であり、
Minecraft serverをDocker／ケータリング構成へ置き換えて横断試験を反復しない。OCI runtimeを実配備する際の
start／health／routing確認はdeployment gateで行い、本artifact gateではindex／platform／attestation identityの
固定までを採用する。これはOCI runtime smokeを実施済みとする主張ではない。

本setは公開前の最終artifact candidateである。Git tag、GitHub prerelease、McRemote JAR asset、release notes、
公開後identity確認はまだ実施していない。

## 11. GitHub prerelease identity

2026-08-28のプロジェクトオーナー承認後、set 4を次のGitHub prereleaseへ公開した。

| component | release | tag target | asset／notes identity |
| --- | --- | --- | --- |
| McRemote | [`v1.21.11-2300.0.0b6`](https://github.com/Naohiro2g/McRemote/releases/tag/v1.21.11-2300.0.0b6) | `4e8f1ff1bd48bfa28c465f2dc24060fbb419317f` | JAR 204,463 bytes／SHA-256 `0ec8d4c0b105f3034361b260fc39fcb78013e932e684d34d5ca95c9a6c6a87a6`／notes `731f491b8defecad3ecb3f0498646b85747e5bc171deda5eb549be0249a62059` |
| Python | [`v2300.0.0b6`](https://github.com/Naohiro2g/minecraft-remote-api/releases/tag/v2300.0.0b6) | `a30a37b15658da655fe1e3535a73fb0e80c06f56` | assetsなし／notes `d7e8293cd513e71a376034edcbef781bb0803d02a412f2423e8f73eb317ba55c` |
| Scratch | [`v2300.0.0b6`](https://github.com/Naohiro2g/scratch-editor/releases/tag/v2300.0.0b6) | `df9264ec355dd722a848df46e96d4b0fc9340ca2` | assetsなし／notes `a81a0bed45edb9c42da01b1483788ca9c5f043ac3e61c4cfd4af24e75752842a` |

三件とも`prerelease=true`、`draft=false`、Latest非対象である。Pythonのwheel／sdist、ScratchのOCI／GUI／
WireScopeはrelease notesのdigest declarationを正とし、追加assetを添付しない。PyPI、Modrinth、public server
deployment、OCI runtime deployment smokeは本公開に含めない。これをもってb6 GitHub prerelease identityを固定する。

## 12. official-public-beta適用時のScratch／Bridge後続修正

2026-08-29、mc-remote-stackの`public-web-paper@8`をofficial-public-betaへ適用する準備中、公開Scratch clientの
notice pane footerがdeploymentの`release_identity`を人間向けversion labelへ変換せず、OCIのraw
`sha-<commit>` tagとして表示する不具合を発見した。Scratchの正式GitHub prereleaseとset 4は
`develop@df9264ec355dd722a848df46e96d4b0fc9340ca2`で既に固定済みだったが、直後の
`5df50144da13b1a1c8c23b01f2d0138ffd17b953`に当該footer／notice label修正があったため、
official-public-betaには後続commitから再生成したScratch／Bridge OCIを使用した。

| image／artifact | official-public-beta適用identity | set 4との関係 |
| --- | --- | --- |
| Scratch index | `ghcr.io/naohiro2g/mc-remote-scratch@sha256:84499b1b9874daa08fde4b485338b42830470f5787ce0ab7d9cc46a2b86e2d95` | sourceを`5df50144…`へ進めた後続修正版 |
| Bridge index | `ghcr.io/naohiro2g/mc-remote-bridge@sha256:6641766b3558185ea2af78e3bfdf3e173c990a26ed997bee268e852178edd72b` | Bridge機能差分はないが、同じsource commitから再生成 |
| WireScope ZIP | SHA-256 `b3d6270299195d2c3db93c9d122938be6ae20d23e0f10e19afe3b0e99e3ca315` | byte-for-byte不変 |
| WireScope manifest | SHA-256 `cee0c3c852ab719f141ee941e914c451af28fa664af08675d50b658e541df5b1` | source commit stampだけを`5df50144…`へ更新 |

適用presetはmc-remote-stack
[`main@23521199701ceb2081de8af3ad64ac6da9682a17`](https://github.com/Naohiro2g/mc-remote-stack/commit/23521199701ceb2081de8af3ad64ac6da9682a17)
の`public-web-paper@8`である。Scratch／Bridge index digestはregistryに対する独立した
`docker manifest inspect`で照合し、判断経緯と再生成は
[PR #35](https://github.com/Naohiro2g/mc-remote-stack/pull/35)のcommit履歴、適用記録は
[PR #36](https://github.com/Naohiro2g/mc-remote-stack/pull/36)のrunbook更新に記録された。

これは**official-public-beta deploymentの適用時追補**であり、§10の`b6-artifact-candidate-set-4`、§11の
Scratch tag target `df9264ec…`、GitHub prerelease notes、b6横断gateを後から別identityへ読み替えない。
McRemote JAR、Python artifact、Paper、protocol `23.0.0`、WireScope ZIPのidentityは変わらない。
却下した案は、set 4のScratch OCIをそのまま適用して公開footerのraw SHA表示を次releaseまで残すことである。
次のScratch／Bridge releaseでは、後続fixを含むdefault branch SHAから正式candidate／release identityを新たに固定し、
deployment追補を通常のrelease identityへ収束させる。
