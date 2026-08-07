# WireScope 初期版 live-human evidence

## Record

- test ID: `2026-08-08-wirescope-initial-live-human`
- test class: `live-human` + source inspection
- result: **PASS（下記 Claim boundary の範囲）**
- observed on: 2026-08-08（exact start／endは搬送票に含まれない）
- source repository: `Naohiro2g/scratch-editor`
- source branch: `develop`
- source commit: `1cf1f02c6a6519b2edf3514a47481ad36d44a363`
- observer schema: `mcremote.observer` version `1`
- protocol: `21.0.0`
- Minecraft: `1.21.11`
- prior knowledge contract commit: `a60d6cb6a5e8a6c7bf67d2e4acd74c2d9c2a92e4`

source commitはGitHub remoteで存在を確認し、commit message
`feat: add independent WireScope observer`、tracked roadmap、schema、fixture、view-state testを照合した。
秘密実値とsource-side raw materialはpublic knowledgeへ搬送していない。公開した保持／除去境界は
[redactions.json](../artifacts/2026-08-08-wirescope-initial-live-human/redactions.json) に固定した。

## Claim boundary

| Claim | Observation | Result |
| --- | --- | --- |
| initial end-to-end observation path | local Scratch→Bridge→Minecraft→独立WireScope | PASS |
| handshake frame | `hello` request／responseを表示 | PASS |
| command frame | `chat.post` request／responseを表示 | PASS |
| stream lifecycle | 同一main streamのsnapshot継続更新 | PASS |
| narrow UI | Minecraft／Scratch／WireScopeを横並びにできる狭幅2 column表示 | PASS |
| localization | `ja-Hira`表示 | PASS |
| schema v1 boundary | `hello.world`／`hello.origin`を初期handshake記録として保持 | ACCEPTED |

## Schema acceptance

初期schema v1と狭幅UIを合格とする。`streams[].hello` は初期handshakeの記録であり、後続の
`build.setWorld`／`build.setOrigin` で現在値へ上書きしない。現在world／originは次のschema sliceで
`current_build_state` としてlifecycle／fixture／Scratch・Python adapter conformanceを同時に固定する。

却下したのは、①`hello`値を現在stateで上書きする、②現在値のためだけにMinecraftを25msごとにpollingする、
③schema v1へversioningなしでfieldを追加する、の3案である。handshake記録と可変build stateを分け、
Scratch／Pythonで同じobserver契約を保つためである。

## Human checkpoint と受理判断

人間は実ブラウザーで、`hello`／`chat.post` のrequest／response、同一main streamの継続更新、
`ja-Hira`、3画面を横並びにする狭幅UIを確認し、schema v1初期版を合格とした。agentが独自に
human observationを再現したとは主張しない。確定搬送票のhuman判定と、固定commit内のtracked roadmap／
schema／fixtureが同じ範囲を支持することをknowledge側で照合して受理した。

source-side `handoff-materials/wirescope-live-human-20260808/` の本文はcommitに含まれず、本recordへ
verbatim搬送していない。このため本recordは上のclaim matrixを越えて、raw時系列、pixel値、private環境identity、
全browser行列を主張しない。

## Sanitized artifacts

- [live-summary_ja.md](../artifacts/2026-08-08-wirescope-initial-live-human/live-summary_ja.md)
  - SHA-256: `c865b1efae37b01c0a2c52ffd118f067e42065414c9599ac6224ec9d3735e065`
- [redactions.json](../artifacts/2026-08-08-wirescope-initial-live-human/redactions.json)
  - SHA-256: `58a035430b6d4f076e51c975e1529affbd8403446271eb36c059ce0a7a8455be`

## CI／release boundary

GitHub APIでsource commitのBuild check成功は確認したが、同時点のcommit-wide checksは全greenではなかった。
本recordはlive-human初期版検収であり、source commit全体のCI green、公開配信、release readinessを
根拠化しない。unit／deterministicの正式根拠も、それぞれのtest code・PASS command・commitで別に扱う。

## 未検証の境界

- 公開配信artifactとCSP／COOP／cache／artifact identity response headerのdeploy gate
- Python adapter／local relay
- 実際の複数connectionを使うmulti-stream E2E
- `current_build_state` schema sliceのshape、version、実装、更新頻度
- source commit全体のCI greenとrelease readiness
- plugin／Bridge artifactのexact identityと再現build

## Acceptance

本recordを、Scratch初期版のschema v1、初期main stream E2E、狭幅UI、`ja-Hira`に対する正式な
live-human根拠として受理する。初期版E2Eの完了を公開deploy、Python追従、multi-stream、現在build state
まで拡張して読まない。
