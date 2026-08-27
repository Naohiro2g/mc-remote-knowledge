# b6 artifact candidate記録

> 2026-08-27時点の`b6-artifact-candidate-set-1`を、人間が照合できる形で固定する記録です。
> 公開release manifest、machine-readable gate manifest、配布済みartifactの主張ではありません。

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

runtime readiness後、少なくともhello identity、sign三操作、`pickaxe_poke`の一操作一event、
`mcr_eh_` handle、WireScope表示filterと`dropped_frames`を実plugin接続で確認する。人間参加結果を
release根拠へ使う場合は、sanitized formal evidenceを`14-evidence/`へ作る。

公開release、tag、registry upload、default branch統合は、このTier 2 pulseの結果をgate coordinatorへ返すまで
行わない。
