# WireScope 初期版 live-human summary

## 判定

**PASS（下記 claim boundary の範囲）**。独立 WireScope の schema v1 初期版と狭幅 read-only UI を
Scratch 参照実装の合格点として受理した。

## identity

- source repository: `Naohiro2g/scratch-editor`
- source branch: `develop`
- source commit: `1cf1f02c6a6519b2edf3514a47481ad36d44a363`
- commit message: `feat: add independent WireScope observer`
- observer schema: `mcremote.observer` version `1`
- protocol: `21.0.0`
- Minecraft: `1.21.11`
- environment: local Scratch／Bridge／Minecraft／WireScope構成（private接続情報は保持しない）
- observed on: 2026-08-08（開始・終了時刻は搬送票に含まれない）

## claim boundary

| Claim | Observation | Result |
| --- | --- | --- |
| full path for the initial slice | Scratch→Bridge→Minecraft→独立WireScopeで観測 | PASS |
| handshake | `hello` request／responseを独立WireScopeで表示 | PASS |
| command frame | `chat.post` request／responseを独立WireScopeで表示 | PASS |
| continuing session | 同一main streamでsnapshot更新が継続 | PASS |
| narrow layout | Minecraft、Scratch、WireScopeを横並びにできる狭幅2 column UI | PASS |
| learner locale | 独立WireScopeの`ja-Hira`表示 | PASS |
| schema v1 semantics | `streams[].hello`は初期handshake記録。現在world／originで上書きしない | ACCEPTED |

## contract boundary

- `hello.world`／`hello.origin` は初期 handshake 値として保持する。
- `build.setWorld`／`build.setOrigin` は観測frameであり、schema v1の `hello` を現在値へ書き換えない。
- 現在の可変 build state はschema v1へ無断追加せず、次のschema sliceで
  `current_build_state`、lifecycle、fixture、adapter conformanceを一緒に定義する。
- 現在値を得るためだけにMinecraftを25msごとにpollingしない。
- 初期版はread-onlyであり、pairing、credential操作、command発行権限をWireScopeへ追加しない。

## 根拠の構成

確定搬送票のhuman判定に加え、GitHub remote上の固定commitで次を確認した。

- `WIRESCOPE_ROADMAP_ja.md`: live-human E2E、狭幅UI、`ja-Hira`、残範囲の記録
- `mc-remote/live/src/observer.ts`: schema名／version、`streams[]`、`hello` shape
- `mc-remote/live/test/fixtures/scratch-main-lifecycle.json`: 初期handshakeを保持したmain stream更新fixture
- `mc-remote/live/src/view-state.ts` と `test/view-state.test.ts`: stream tab選択とfallback

搬送票が参照するsource-side `handoff-materials/wirescope-live-human-20260808/` はcommit対象ではなく、
その本文やraw transcriptはpublic knowledgeへ搬送していない。本summaryは、確定搬送票と固定commit内の
tracked roadmap／実装から公開可能なclaimだけを再構成したものである。

## 未検証／主張しない範囲

- 公開配信artifactとCSP／COOP／cache／artifact identity response headerのdeploy gate
- Python adapter／local relay
- 実際の複数connectionを使うmulti-stream E2E
- `current_build_state` schema sliceのshape、version、実装、更新頻度
- source commit全体のCI greenまたはrelease readiness
- UIのpixel-perfect layout、browser／viewport全組合せ
- plugin／Bridge artifactのexact identityと再現build

## secret／private境界

token、pair code、player UUID、private host／port、credential／device情報、filesystem絶対path、raw browser
captureは収録していない。保持したのはpublic commit、protocol／Minecraft version、一般化した接続経路、
schema境界、PASS／ACCEPTED判定だけである。
