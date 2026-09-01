# b7 live gate追補指示書

> status: 人間レビュー前のMcRemote担当向け指示案。

## 目的

McRemote `9db95e8af0bcc9feaf66c1bbbffc05b9fb8304e0`のb7 live gateで見つかった、外部dimension移動後の
handle reason不一致を修正する。lightning、direction、ParticleBuilder Stage 1のcontractを変更せず、gate再開に必要な
artifactとtargeted evidenceを返す。

## 固定入力

- knowledge: `73b850c3a10d35425564c8caec0008427000300d`
- exact contract: `10-protocol/wire-format-design_ja.md` §5.8.2
- decision: `2026-09-01-01`
- base candidate: `9db95e8af0bcc9feaf66c1bbbffc05b9fb8304e0`
- live runner／probe: `51f4304da0c6bbf7185454644807729faca4b3c3`
- fixture SHA-256: `faad66c93d2c8ee8eb541f6b7297163cb681054b3de05ba3d130ac4288c1046a`
- observed mismatch: 別dimensionへの外部teleport成功後、初回`entity.getDirection(handle)`が
  expected `entity_dimension_changed`に対してactual `entity_unavailable`

## Product修正

1. `EntityHandleRegistry`が、登録済みentityの現在dimensionを識別できる場合、一般的なunavailable判定より先に
   `entity_dimension_changed`を返せるよう原因を確定する。
2. 初回terminal reasonを返した時点でhandleを即時失効し、二回目以降を`entity_not_found`とする既契約を維持する。
3. remove、dead、invalid、unloaded等の`entity_unavailable`をdimension変更へ誤分類しない。
4. direction四method、`world.strikeLightning`、rate／work、ParticleBuilder、registry method集合、protocol
   `23.1.0`、artifact `2301.0.0b7`を変更しない。
5. `world.strikeLightningEffect`を追加しない。

候補原因は、dimension照合より先にnull／dead／invalid／world所属を評価しているresolve順である。これは指示時点では
source inspectionによる仮説であり、実装者がPaper上のentity参照状態とtestで確定する。

## Deterministic verification

- 外部dimension移動: `entity_dimension_changed`→即時`entity_not_found`
- 外部remove／dead／invalid／unavailable: `entity_unavailable`→即時`entity_not_found`
- foreign／unknown／旧epoch／旧形式handleの既存同値化
- player／entity directionの位置・dimension不変、post-read
- 共有fixture 81 caseのexact bytesと全対応
- Paper 1.21.11全suite
- Paper 26.2／Java 25 targeted compatibility compile／test
- `./gradlew build`、`git diff --check`

## Runner改善

product修正と分離できる場合は別commitにする。runnerは人間の探索toolではなく、事前合意した再現確認を短い一連動作で
行うtoolとして扱う。

- 実行前に「意図・背景・方法・予測／判断材料」を一覧で提示できるscenario manifestを置く。
- human checkpointを越えて無関係な次caseへ自動進行しない。事前合意した近距離→移動→中間距離等だけを一sequenceにする。
- title／subtitle／chat command feedbackを使わない。
- `player.setPos`はdimensionを含むexact paramsを使い、deterministic testへ固定する。
- lightning視認は目印、近距離、約1秒間隔3回、中間距離への自動移動、約1秒間隔3回を再利用可能にする。
- particle視認は目印の1 block上へ約1秒間隔4回表示する。四回をbatch APIの主張にしない。
- rod確認を残す場合はpowered stateをtick内で捕捉するかlamp等で可視化する。copper不変をFAILにしない。
- non-idempotentなlightningは失敗／backpressure時にauto retryしない。
- token、endpoint、UUID、private host、実座標をsource／公開logへ残さない。

## 返却物

- branchとpush済みcommit
- base／parent、local HEADとremote SHA一致、clean worktree
- product変更pathとrunner変更pathの分離
- 原因、修正した判定順、却下した代案
- deterministic test名と件数、全suite結果
- Paper 1.21.11／26.2 compatibility結果
- candidate JAR filename、bytes、SHA-256
- fixture path、bytes、SHA-256
- protocol／artifact／method registry不変の照合
- live non-claimと、coordinatorが再実行すべきtargeted case

shared serverへの配置、live実行、tag、releaseはMcRemote担当の作業範囲外とする。coordinatorが返却artifactを固定してから、
外部dimension移動caseと最小representative smokeを実行する。handle解決順だけのchange coneで閉じる場合、追加
live-humanはb7 close条件にしない。
