# b6 artifact candidate記録

> 2026-08-27時点の`b6-artifact-candidate-set-1`を、人間が照合できる形で固定する記録です。
> 公開release manifest、machine-readable gate manifest、配布済みartifactの主張ではありません。
> Tier 2で生じたset 2／3は§7へ追記し、set 1の原記録を上書きしません。

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

Tier 2 requested sliceはPASSした。Bridge OCI生成、default branch統合、正式release artifact freeze、公開releaseは
引き続き未完である。観測target変更後の自動再開とlive `dropped_frames`はclient-only補足で、b6 coreをHOLDにしない。
