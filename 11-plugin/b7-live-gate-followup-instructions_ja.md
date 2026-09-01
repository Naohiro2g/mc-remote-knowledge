# b7 live gate追補指示書

> status: product／deterministic／targeted live-auto完了。release統合は未完。

## 目的

McRemote `9db95e8af0bcc9feaf66c1bbbffc05b9fb8304e0`のb7 live gateで見つかった二つのblocker、外部dimension移動後の
handle reason不一致とconstruction permissionの不整合を修正する。direction、full lightningのrate／work／副作用境界、
ParticleBuilder Stage 1は変えず、gate再開に必要なartifactとtargeted evidenceを返す。

## 固定入力

- exact contract: `10-protocol/wire-format-design_ja.md` §5.8.2
- decisions: `2026-09-01-01`、`2026-09-01-02`
- base candidate: `9db95e8af0bcc9feaf66c1bbbffc05b9fb8304e0`
- live runner／probe: `51f4304da0c6bbf7185454644807729faca4b3c3`
- predecessor fixture SHA-256: `faad66c93d2c8ee8eb541f6b7297163cb681054b3de05ba3d130ac4288c1046a`
  （旧permission contractの履歴。successor fixtureの代替にしない）
- observed handle mismatch: 別dimensionへの外部teleport成功後、初回`entity.getDirection(handle)`が
  expected `entity_dimension_changed`に対してactual `entity_unavailable`
- observed permission mismatch: stable b6とb7 candidateはhello／handler間でconstruction permissionの判定が一貫せず、
  b7 candidateはさらに孤立した`mcr.lightning`を要求する

## Product修正

1. `EntityHandleRegistry`が登録済みentityの現在dimensionを識別できる場合、一般的なunavailable判定より先に
   `entity_dimension_changed`を返せるよう原因を確定する。
2. 初回terminal reasonを返した時点でhandleを即時失効し、二回目以降を`entity_not_found`とする既契約を維持する。
3. remove、dead、invalid、unloaded等の`entity_unavailable`をdimension変更へ誤分類しない。
4. auth enforcement ONのplayer-bound helloで、paired UUIDの`mcr.online`、`mcr.offline`、build rangeを
   `server=global` contextから一度解決し、sessionへ`onlineAllowed`／`offlineAllowed`／`buildRange`として保存する。
5. 現在onlineなら`onlineAllowed`、offlineなら`offlineAllowed`をhello成功条件にする。二permissionは独立で、片方を
   他方の包含として扱わない。
6. online-only sessionは`PlayerQuitEvent`、offline-only sessionは`PlayerJoinEvent`で閉じる。両方trueなら状態遷移を
   またいで継続する。permission／range変更は再接続時に反映し、即時停止は既存session／credential revokeを使う。
7. handlerごとのLuckPerms再load／再照合を削除し、全construction methodが同じsession snapshotとbuild rangeを使う。
8. `mcr.lightning`をconfig、PermissionProvider、plugin permission宣言、handler、test、fixture、READMEから削除する。
   代替のmethod固有permissionを追加しない。
9. direction四method、`world.strikeLightning`、rate／work、ParticleBuilder、registry method集合、protocol
   `23.1.0`、artifact `2301.0.0b7`を変更しない。
10. `world.strikeLightningEffect`を追加しない。

handleの候補原因は、dimension照合より先にnull／dead／invalid／world所属を評価しているresolve順である。これは指示時点の
source inspectionによる仮説であり、実装者がPaper上のentity参照状態とtestで確定する。

## Deterministic verification

- 外部dimension移動: `entity_dimension_changed`→即時`entity_not_found`
- 外部remove／dead／invalid／unavailable: `entity_unavailable`→即時`entity_not_found`
- foreign／unknown／旧epoch／旧形式handleの既存同値化
- online／offlineそれぞれについて、permissionなし、onlineのみ、offlineのみ、両方のhello admission matrix
- online-only quit、offline-only joinでsession close、両permissionでjoin／quit後もsession継続
- permission／build range変更が既存sessionへ途中反映されず、再接続後に反映されること
- session／credential revokeによる即時停止
- player、entity、block、sign、height、spawn、particle、direction、lightning等の全construction handlerが同じsession
  snapshotを使い、handler固有のLuckPerms照合へ戻らないこと
- `mcr.lightning`設定／node／runtime参照が0件で、online playerの`mcr.online` sessionからlightning admissionへ進めること
- player／entity directionの位置・dimension不変、post-read
- protocol ownerが発行するsuccessor fixtureのexact bytesと全対応。旧81 case fixtureだけのPASSを完成根拠にしない
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
- successor fixture owner branch／commit、path、bytes、SHA-256、case対応表
- protocol／artifact／method registry不変の照合
- live non-claimと、coordinatorが再実行すべきtargeted case

shared serverへの配置、live実行、tag、releaseはMcRemote担当の作業範囲外とする。successor fixtureが未発行でも、
permission実装とlocal testは並行して進めてよいが、最終のexact fixture PASSはfixture着地後に返す。coordinatorが
返却artifactを固定してから、外部dimension移動、online-only lightning、session状態遷移をtargeted live-autoで実行する。
今回のchange coneにvisual／audio変更はないため、追加live-humanはb7 close条件にしない。

## 完了identityと残作業

- branch／commit: `agent/b7-live-gate-blockers@3d5f710db97f4b14613f7e0abaafd535701d1906`
- base: `9db95e8af0bcc9feaf66c1bbbffc05b9fb8304e0`
- successor fixture: 20,367 bytes、Git blob `7371787ca6484a45dec0c7893608339961ae6fcf`、
  SHA-256 `586d24bf40136eec31f1827f23ef5b317f15100a17a635d7fe9f165e0af40dce`、93 unique cases
- 担当報告のlocal JAR: `mc-remote-1.21.11-2301.0.0b7.jar`、222,951 bytes、
  SHA-256 `f08388cf393e02db1eb605e707dfaec890792e7a475de5a51caacbc940028ee9`

coordinatorはremote commit／base、McRemote配置fixtureのexact bytesと93 ID、production／README配下の
`mcr.lightning` 0件を照合した。担当報告ではPaper 1.21.11全203 tests、Paper 26.2／Java 25 compatibility、
successor fixture、method registry、clean build、`git diff --check`がPASSした。これによりproduct修正と
deterministic gateはCLOSEDである。

JARは既存gate用durable staging
`/home/tsuji/.local/share/mc-remote/gates/b7-mcremote-candidate-3d5f710/mc-remote-1.21.11-2301.0.0b7.jar`
へ固定された。coordinatorは222,951 bytes、mode `0444`、SHA-256
`f08388cf393e02db1eb605e707dfaec890792e7a475de5a51caacbc940028ee9`を実体から再照合した。shared配置は未実施である。
外部dimension移動とonline-only sessionからのlightningはtargeted live-autoでPASSした。join／quit状態遷移は
successor fixtureとPaper deterministic suiteで閉じ、追加のplayer再接続をlive gateへ要求しない。追加live-humanも
要求しない。product／contract blockerはCLOSEDであり、残作業はdefault branch統合、release candidate artifact set、tag、
公開releaseである。
