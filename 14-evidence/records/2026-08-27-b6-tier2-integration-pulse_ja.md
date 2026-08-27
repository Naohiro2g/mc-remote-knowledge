# b6 artifact candidate set 1 Tier 2統合pulse evidence

## Record

- test ID: `2026-08-27-b6-tier2-integration-pulse`
- test class: `live-auto` + `live-human`（pairing commandのみ）
- observed date: `2026-08-27` JST
- result: **PARTIAL PASS / b6横断gateはOPENのまま**
- protocol: `23.0.0`
- artifact version: `2300.0.0b6`
- candidate set: `b6-artifact-candidate-set-1`
- target: host-native `dev-integration`／Minecraft `1.21.11`／Paper `1.21.11-132`
- gate contract: `00-hub/release-gate-notes_ja.md`の2026-08-27 b6横断release gate

本recordは、固定済みcandidate bytesを通常devへ置き、server runtime、exact Python wheel、exact Bridge
buildを実pluginへ接続した最初のTier 2 pulseを記録する。Scratch GUI／WireScopeの実ブラウザ操作、
`pickaxe_poke`の一操作一eventと腕振りはまだ行っていないため、b6横断`GREEN`やrelease可とは判定しない。

> 継続: 後続のScratch／WireScope実ブラウザ、`pickaxe_poke`、そこで発見したclient-only修正は
> [`2026-08-28-b6-scratch-wirescope-live-human`](2026-08-28-b6-scratch-wirescope-live-human_ja.md)へ記録した。
> 本recordの「未実施」はset 1初回pulse終了時点の事実として残し、後からPASSへ上書きしない。

## Exact input

| Component | Source | Artifact |
| --- | --- | --- |
| McRemote | `88d818703be5e7314bc1e45597a66237796db641` | JAR SHA-256 `4e28603caefa4273fabfe325e1c75a28239a6fa9eb44fb5a2b49da7be79870e8` |
| Python | `0ba22e80b9b1b339dfd11085b1b24cef646599b2` | wheel SHA-256 `0887807f0d00f71fcb543caf16c3963b70580bf073b6a7576d7f274399a1877b` |
| Scratch／Bridge／WireScope | `104f194deddc9c244e6e07c4223965c792551f9d` | GUI `3ba9940e…f617`／Bridge `11199a8e…1c72`／WireScope ZIP `06a6fb44…b7d` |

七artifactの完全なname／size／digestは
[b6 artifact candidate記録](../../10-protocol/b6-artifact-candidate-record_ja.md)を正とする。

## Server runtime readiness

server consoleから通常停止し、公開済みb5 JARを`plugins`外へrollback入力として保持して、McRemote JAR一件だけを
b6 candidateへ交換した。world、config、credential backend、Paper JARは変更していない。再起動後に次を確認した。

- Paper `1.21.11-132`、McRemote `1.21.11-2300.0.0b6`
- credential domain `HEALTHY`
- 標準Minecraft／McRemote listenerの稼働
- protocol `23.0.0`でtokenなし=`auth_required`、存在しないtoken=`token_not_found`、形式不正token=`token_invalid`

最初のclient probeはSSH aliasを通常DNS名として扱って接続前に名前解決失敗した。SSH設定から実addressを解決する
runnerへ直した再試験はPASSし、candidate、server、artifactは変更していない。

## Python product pulse

固定wheelをPython `3.11.5`のisolated venvへinstallし、package metadata `2300.0.0b6`、
`mc_remote.minecraft.PROTOCOL == "23.0.0"`、sign value surfaceのimportを確認した。人間が表示された
`/mcremote pair` commandをMinecraftで一度実行した後、同wheelから次をPASSした。

| Case | Observation | Result |
| --- | --- | --- |
| hello | 認証済みhelloがprotocol `23.0.0`を返す | PASS |
| `world.setSign`／`world.getSign` | plain、named color＋bold、hex color＋italic、front／backをround-trip。plainのcanonical colorは`black` | PASS |
| `world.updateSignLine` | front index `2`だけを更新し、他三行とback面を維持。decorationsはcanonical順 | PASS |
| handle | `world.spawnEntity`がopaque `mcr_eh_`を返し、旧`mceh_`ではない | PASS |
| cleanup | 試験に使ったsign blockを元の完全BlockValueへ復元 | PASS |

初回二回はprobeが`getPos()`のresultを旧想定のobject座標として読んだため、world mutationより前に停止した。
実resultの`pos`配列を読むようrunnerだけを直した最終runをPASSとする。接続時の`CatalogProjectionWarning`は、
既存の利用者管理`mc_constants.py`を安全に上書きできないというcompletion更新の警告であり、接続、sign、handleの
wire結果には影響しなかった。この警告を解消済みとも、catalog projectionを本pulseでPASSしたとも主張しない。

## Bridge product pulse

exact Bridge tarの`dist/`を展開し、source lockと一致するproduction dependency `ws 8.18.3`
（npm integrity `sha512-PEIG…tvzg==`、exact sourceの`package-lock.json` SHA-256
`98bd8649bef2f16132c680348a342e3bdd5e4e2b430c83036b0defb39919da26`）をruntime側で解決した。
GUI buildは変更せず、deployment-owned runtime configからloopback Bridgeと論理targetを指定した。
Scratch originと同じallowlist条件、`mcremote.bridge.one-shot.v1`選択、`one-shot-v1` envelopeで
`hello(protocol=23.0.0)`を送信し、実pluginの未認証境界`auth_required`を受信した。

これはexact Bridge buildからMcRemoteまでの一往復を示すが、Scratch VM自身のWebSocket生成、pairing、block実行、
observer handoffを示さない。また、今回のBridge tarは`dist/`だけでproduction dependencyを同梱しないため、
単独deploy可能artifactとは扱わない。Tier 2ではexact source installの`ws 8.18.3`を外部runtime入力として固定した。
公開配布形態ではOCIまたは別packageが`package.json`／lock済みdependencyを含む必要があり、後続artifact gateで閉じる。

## 起動済みだが未観測のScratch surface

exact GUI／Bridge／WireScope bytesをworkstation上の分離したloopback portへ起動し、GUI runtime configの
`release_identity=2300.0.0b6`、Bridge URL、WireScope URLと各HTTP到達性を確認した。tracked GUI build内の
b5公開profileは変更せず、deployment-owned responseだけをb6 dev profileへ差し替えた。

Codex内ブラウザは環境のtrust boundaryで接続できなかった。別のheadless browserへ切り替えず、実ブラウザでの
Scratch pairing、sign block、browser保存、WireScope表示filter／`dropped_frames`／mini配置は未実施として残す。

## Sanitized artifacts

- [result-summary.json](../artifacts/2026-08-27-b6-tier2-integration-pulse/result-summary.json)
  - SHA-256: `0030409b17703d1166e9bb9515486abdd5ae24f02c399f1d48e2d9ae7e6a6314`
- [redactions.json](../artifacts/2026-08-27-b6-tier2-integration-pulse/redactions.json)
  - SHA-256: `96d31e6f3690c06b9cd583d17f224e71a429c468830c098bfe5cbadf5af9880c`

raw token、private address、player UUID、server logは収録しない。pair codeは必須redaction対象ではないが、
今回の主張に不要なため収録しない。

## Gate conclusion

server runtime readiness、exact Python wheelによるsign三操作／`mcr_eh_`、exact Bridgeによる実plugin一往復は
PASSした。candidate source／artifact bytesを変える契約差分は見つからなかった。一方、Bridgeのdeploy package境界、
Scratch実ブラウザ、WireScope、`pickaxe_poke`人間操作が残るため、b6横断release gateはOPENを維持する。

次は同じset 1で、Scratch実ブラウザpairing、Scratch sign surface、browser保存の代表操作、WireScopeの
hello／poke frame・表示filter・`dropped_frames`、一回の物理pokeから一eventと腕振りを確認する。
source修正が必要ならset 1を失効させ、観測済みPASSはchange coneを明記して再評価する。

## Non-claim

- Scratch GUI／VM、WireScopeの実plugin E2Eは未実施
- `pickaxe_poke`の一操作一event、腕振りfeedbackは未実施
- `sign_update_failed`のstale競合、waxed signは未実施
- Bridge tar単独でのdependency-complete deploymentは未達
- browser保存のexact integrated artifact上での再確認、iPad／Safari、storage evictionは未実施
- rollback実操作、default branch統合、公開artifact、tag、registry upload、b6 releaseは未実施
