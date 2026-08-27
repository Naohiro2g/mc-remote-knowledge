# b6 Scratch／WireScope継続pulse evidence

## Record

- test ID: `2026-08-28-b6-scratch-wirescope-live-human`
- test class: `unit/deterministic` + `live-human`
- observed date: `2026-08-27`〜`2026-08-28` JST
- result: **PARTIAL PASS / b6横断gateはOPENのまま**
- protocol: `23.0.0`
- artifact version: `2300.0.0b6`
- predecessor: [`2026-08-27-b6-tier2-integration-pulse`](2026-08-27-b6-tier2-integration-pulse_ja.md)
- target: host-native `dev-integration`／Minecraft `1.21.11`／Paper `1.21.11-132`
- axes: `protocol`、`plugin`、`scratch-client`、`bridge`、`server-runtime`、`human`、`ux`

## Scope items

- `pickaxe_poke`: 一回の物理操作、一event、canonical payload、腕振りfeedback
- Scratch mini: tab行配置、dropdown表示、独立WireScopeへの導線
- WireScope filter: player request／response pair、pending `events.poll`、payload選択／copy
- WireScope pause: 停止snapshot、新着badge、filter／検索、最新windowへの再開
- artifact identity: client-only change coneとcandidate set 1〜3の継承境界

本recordは、先行recordで未実施だった`pickaxe_poke`人間操作とScratch→Bridge→plugin→WireScopeのreal-browser経路、
そこで発見したmini dropdown／pending poll表示の不具合、その後のclient-only修正を記録する。途中でScratch／
WireScope sourceが変わったため、旧setのPASSを新artifactのPASSへ読み替えず、観測時のsourceと最終artifactを分ける。

## Inputとchange cone

| 面 | identity | 本recordでの扱い |
| --- | --- | --- |
| McRemote | source `88d818703be5e7314bc1e45597a66237796db641`／JAR SHA-256 `4e28603c…70e8` | set 1から不変。server runtime、sign／handle PASSを再利用 |
| Python | source `0ba22e80b9b1b339dfd11085b1b24cef646599b2`／wheel SHA-256 `0887807f…1877b` | 本recordでは操作しない。先行PASSを再利用 |
| Scratch GUI | source `1d1b21d5acdbabdb596476c087c14033d5c33d32`／GUI SHA-256 `1757f665…7ef5` | mini dropdown修正版 |
| Bridge | SHA-256 `11199a8e…31c72` | set 1からexact bytes再利用。local deployment設定だけを修正 |
| WireScope live fix | source `7b4f71d71e8ecd665d402682e677dc4e425d160f` | 実plugin接続real-browserの観測対象 |
| WireScope current | source `24077ef005e4969bf3a7434b45532ae53cefbc28` | 表示停止を追加したset 3 artifact。deterministic browserまで |

共有fixture、wire、protocol、plugin、Python、Bridge、Scratch VM API surfaceはchange cone外である。最終七artifactの
identityは[b6 artifact candidate記録](../../10-protocol/b6-artifact-candidate-record_ja.md) §7.2を正とする。

## `pickaxe_poke` live-human

実playerがdiamond pickaxeで一回blockを右クリックし、次を確認した。

- 一回の物理操作から`pickaxe_poke`一件だけを受信
- `item=minecraft:diamond_pickaxe`、`hand=main`、fully-qualified item
- event loss delta `0`
- McRemote sessionを持つplayerにだけ腕振りfeedbackが見える

初回probeはfixtureのcanonical `hand=main`を旧runner期待`main_hand`と比較して停止した。製品eventは正しく、runnerの
期待だけを直した再試験をPASSとする。plugin source／JAR／server設定は変えていない。人間は腕振りを「大丈夫」と確認した。

## Scratch miniと実接続

最初のGUIでは、tab行へ移したminiの詳細が親panelの`overflow: hidden`でclipされ、開けず、独立WireScopeへの導線も
見えなかった。source `1d1b21d5ac…`はpanel自体のclipを外して角丸処理を子要素へ移し、Code／Costumes／Soundsの
三tab、折りたたみ、palette非干渉、dropdown表示をreal-browserでPASSした。

local BridgeのupgradeではOrigin allowlistと`mcremote.bridge.one-shot.v1` subprotocolを両方満たす必要がある。
さらに論理host名が実行環境ではSSH aliasに過ぎず、NodeのDNS名として解決できないことをBridge logの
`getaddrinfo`失敗で特定した。deployment-owned runtime configとBridge allowlistを解決済みLAN targetへ合わせ、
workstationからMcRemote listenerへのTCP到達とBridge one-shot→pluginの`auth_required`往復を再確認した。
private addressは本recordへ収録せず、source／artifact変更には数えない。

接続後、Scratch blockから`player.getPos`を実行し、独立WireScopeでrequest／responseの二frameを確認した。
responseはdimensionと三要素posを持ち、filter summaryは保持100 frame中表示2 frameだった。player groupをOFF／ONすると
request／responseが一体で消える／戻ることを確認した。

## pending poll不具合と修正

空振りOFFでも、約1秒ごとの`events.poll` requestがresponse前に一瞬表示され、empty response到着後に消えた。
さらにsnapshotごとにframe table全体を再構築していたため、非表示pollだけでもpayloadの選択範囲が解除され、copyを
妨げた。これは見た目だけでなく観察・転記の利用性を壊すFAILとして、GUI修正版set 2をそのままrelease候補にしなかった。

source `7b4f71d71e…`は、send-only pending pollをOR検索を含め無条件に保留し、response後にpairを原子的に判定する。
また、filter後frameの順序付き`sequence` signatureが変わらないsnapshotではtable bodyを再構築しない。搬送元は
`@mc-remote/live` 130/130件、lint／buildをPASSした。実plugin＋local Bridgeのreal-browserで次をPASSした。

- 空振りOFFでpending requestが点滅しない
- 空振りpoll継続中も既存payloadを選択・copyできる
- 非空`pickaxe_poke`のrequest／response pairが同時に現れる
- player groupで`player.getPos` request／responseが一体で表示／非表示になる

## 表示一時停止candidate

source `24077ef005…`は各streamに「表示を一時停止」／「表示を再開」を追加した。停止は表示snapshotだけを固定し、
frame収集、poll、保持window、`dropped_frames`を止めない。新着件数をbadge表示し、filter／検索は停止snapshotへ適用、
再開時は最新windowへ一度だけ切り替える。停止stateは保存せず、観測target変更時に破棄する。

130/130件、lint／buildをPASSし、deterministic sourceのreal-browserでtable固定、新着badge、copy、filter／検索、
一括再開をPASSした。観測target変更後の自動再開と、実plugin接続中のpause操作は未実施・未主張である。

## Current WireScope artifact

- `wirescope-app.zip`: 79,169 bytes、SHA-256
  `b3d6270299195d2c3db93c9d122938be6ae20d23e0f10e19afe3b0e99e3ca315`
- `wirescope-app.manifest.json`: 2,321 bytes、SHA-256
  `5fafdc54af45d8f498cd48b13590797eaaa6316adaf017a40595566f0f507b2e`

coordinatorは返却fileを再hashし、manifest内source `24077ef005…`とarchive digestを照合した。set 2のGUI、set 1の
Bridge／plugin／Pythonを再利用した七fileを`b6-artifact-candidate-set-3`として別directoryへ固定し、旧setを上書きしていない。

## Sanitized artifacts

- [result-summary.json](../artifacts/2026-08-28-b6-scratch-wirescope-live-human/result-summary.json)
  - SHA-256: `4df2d4ce46e5f7a9242c3a35884cb7e23a42d6aa29aec5d92c8b846ff4a40119`
- [redactions.json](../artifacts/2026-08-28-b6-scratch-wirescope-live-human/redactions.json)
  - SHA-256: `a92f9456805153fd1f24f29b61d1696dd62b4e616b9b403218b5dd90aca0d85b`

raw token、pair code、private address、player UUID、server log、実座標は収録しない。

## Gate conclusion

`pickaxe_poke`の一操作一eventと腕振り、Scratch→Bridge→plugin→WireScopeの現行allowlist method、player filter、
pending pollの原子的表示とcopy安定性はPASSした。mini dropdownも修正後GUIでPASSした。これらはb6 core wireを
戻す差分ではなく、Scratch／WireScope client-only change coneで閉じた。

一方、set 3 exact ZIPの実plugin接続pause、`dropped_frames`の同接続での実値、Scratch text-only sign三操作、
browser保存のexact integrated artifact操作、Bridge deploy package境界、default branch統合、releaseは未完である。
表示filter／pauseはb6非blocking companionだが、sign／browser保存とartifact／統合gateが残るため、b6横断gateはOPENを維持する。

## Non-claim

- set 3 exact WireScope artifactの実plugin接続pause、観測target変更後の自動再開
- Scratch sign三操作の実plugin round-trip
- exact integrated GUIでのproject／sprite browser保存代表操作
- `sign_update_failed` stale競合、waxed sign
- Bridge tar単独のdependency-complete deployment
- iPad／Safari、storage eviction、long soak、capacity
- rollback実操作、default branch統合、公開artifact、tag、registry upload、b6 release
