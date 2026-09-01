# b7 direction／lightning live gate evidence

> status: 人間確認済み。後続decision `2026-09-01-02`を反映した正式record。

## Record

- test ID: `2026-09-01-b7-direction-lightning-live`
- test class: `live-auto` + `live-human`
- observed date: `2026-09-01` JST
- result: **HOLD（製品／contract blocker 2件、観測方法不足2件）**
- protocol: `23.1.0`
- artifact version: `2301.0.0b7`
- contract: `10-protocol/wire-format-design_ja.md` §5.8.2
- decisions: `2026-09-01-01`、`2026-09-01-02`
- knowledge execution snapshot: `73b850c3a10d35425564c8caec0008427000300d`
- target: host-native `dev-integration`／Minecraft `1.21.11`／Paper `1.21.11-132`
  SHA-256 `5ffef465eeeb5f2a3c23a24419d97c51afd7dbb4923ff42df9a3f58bba1ccfba`／Java `21.0.12`

本recordは、direction四method、entity handleの外部変化、damage-capableな
`world.strikeLightning`、event cancellation、ParticleBuilder Stage 1の代表描画を実Paperで照合した結果を残す。
雷の視聴覚確認は、人間が目的と予測を理解したうえでMinecraft画面を観察した範囲だけを主張する。途中で発見した
runner／説明手順の不足を製品FAILへ混ぜず、再試験可能な形で残す。

## Fixed input

| 面 | identity | 本recordでの扱い |
| --- | --- | --- |
| McRemote source | `codex/b7-direction-lightning-particle@9db95e8af0bcc9feaf66c1bbbffc05b9fb8304e0` | product candidate |
| McRemote JAR | `mc-remote-1.21.11-2301.0.0b7.jar`、222,313 bytes、SHA-256 `f47e08f1c6c2d0754b2d9f59a3e5a80fdf7307c5d011582c455fb10895f7b3ef` | deployed test artifact |
| live runner／probe | `agent/b7-live-auto-runner@51f4304da0c6bbf7185454644807729faca4b3c3` | product source／registry差分なし |
| probe JAR | `mc-remote-b7-live-probe-23.1.0-b7.jar`、13,444 bytes、SHA-256 `641a7bf12190e7f73d008689918427f92a1cf7592cb9ee48367997fc0f486e70` | test-only plugin |
| shared fixture | owner `scratch-editor@607cda40588ec4579c503d457c3784385419ac65`、SHA-256 `faad66c93d2c8ee8eb541f6b7297163cb681054b3de05ba3d130ac4288c1046a` | 旧permission contractの81 case基線。successor fixtureが必要 |

private endpoint、token、pairing identity、player UUID、実座標は収録しない。test worldは人間の明示判断により
使い捨てとし、world snapshot復元を要求しない。

## Human-facing試験項目

| 試験 | 意図・背景 | 方法 | 予測／判断材料 |
| --- | --- | --- | --- |
| direction | setが向きだけを変え、位置・dimensionを動かさないことを確かめる | player／entityでget→set→get | 6桁以内のunit vector、post-read一致、位置・dimension不変 |
| handle外部remove | 実体消滅後のhandle終端を確かめる | handle取得後にprobeでentityをremove | 初回`entity_unavailable`、直後から`entity_not_found` |
| handle外部dimension移動 | 同じentityが別dimensionへ移った場合を消滅と区別できるか確かめる | handle取得後にprobeで別dimensionへteleport | 初回`entity_dimension_changed`、直後から`entity_not_found` |
| 通常落雷 | full lightningが通常のMinecraft副作用を起こし得ることを観察する | pig、damage対象、着火可能地点へexact strike | RPC `null`、CUSTOM event 1件。変身・damage・fireは起こり得るが件数や順序は固定しない |
| 変身後handle | 変身が旧entity identityの継続か置換かを確かめる | pig変身後に旧handleを読む | 旧handleは失効。新entityは将来の周辺検索等で新handleを取得する対象 |
| rod／copper | rod等へ当たるように狙った雷が、通常のrod／copper作用を起こすかを見る | rodの1 block上へexact strikeし、通電と銅状態を観察 | rod通電を明示観測する。銅変化は発生した場合だけ記録し、不発を実装FAILにしない |
| event cancel | server上の別pluginが禁止した落雷をMcRemoteが強行しないことを確かめる | probeが対象eventをcancel | RPCは受理されても、実際の落雷は起きない |
| particle | ParticleBuilder Stage 1後も既存particleを人間が見られることを確かめる | 目印の1 block上へ1秒間隔で4回表示 | 同じ場所で4回認識できる。単発だけを十分な人間確認としない |
| 落雷距離比較 | 落雷の光と音を距離別に比較する | 近距離3回→自動移動→中間距離3回、約1秒間隔 | 両地点で認識でき、単発より差を比較しやすい |

## Live-auto結果

### Directionとhandle

- player／entityのget→set→get、6桁以内、post-read、位置・dimension不変: **PASS**
- 外部remove後の`entity_unavailable`、直後の`entity_not_found`: **PASS**
- 外部dimension移動後の初回reason: **FAIL**
  - expected: `entity_dimension_changed`
  - actual: `entity_unavailable`
  - probeによる別dimensionへのteleport自体は成功した。
  - runnerは初回reason不一致で停止したため、このcaseの二回目`entity_not_found`は未実施である。

source inspectionでは、handle resolveがdimension照合より先にnull／dead／invalid／world所属を評価する順序が
候補原因である。これは推測であり、修正版のdeterministic testと実Paper再試験で確定する。

### Lightning、cancel、particle

- 通常落雷: exact target、対象event 1件、`CUSTOM`、cancelなし、RPC `result:null`: **PASS**
- 後続観測: pigからzombified piglinへの変化、fire、damage対象の消失を観察した。副作用の件数、順序、収束は主張しない。
- 変身前pigの旧handle: `entity_unavailable`後に`entity_not_found`: **PASS**
- cancellation: exact target、対象event 1件、`CUSTOM`、final cancelled、RPC `result:null`: **PASS**
- 既存9-param `world.spawnParticle`: accepted count `1`: **PASS**

最初の通常落雷runは、online test playerが`mcr.online`を持っていても旧candidateが別途`mcr.lightning`を要求したため
`permission_denied`となり、雷を発生させず停止した。これは旧`2026-09-01-01`とcandidateの一致だけを見れば想定どおりの
拒否だが、live-humanの運用で孤立した個別permissionの不自然さが明確になった。継続観測のため一時的にnodeを付与したことは、
その要求を批准したことを意味しない。

後続source auditでは、公開stable b6 `4e8f1ff1bd48bfa28c465f2dc24060fbb419317f`も、helloがplayer状態を見ず
`mcr.online OR mcr.offline`で通す一方、`setBlock`／`setBlocks`は以後construction permissionを再確認せず、他handlerは
異なるタイミングで再確認していた。online-only権限のoffline sessionが基本block setterへ到達でき、offline-only権限の
online sessionはmethodごとに結果が分かれる。よってこれは単なる環境設定漏れではなく、session admission contractと実装の
不整合である。`2026-09-01-02`で二permissionを独立した状態別snapshotへ統一し、`mcr.lightning`を削除したため、旧candidateと
旧fixtureは修正対象とする。

## Live-human結果

### 通常落雷とcancellation

人間は通常落雷でbolt／flash、音、fire、zombified piglinを目視した。変身したpigは旧handleと別identityであることを
重要な観察として確認した。b7には周辺entity検索がないため新handleの再取得は行っていない。

cancellation試験は「McRemoteが雷を要求しても、server上の別pluginが禁止した場合、実際の雷が起きないこと」を
目的として事前説明した。人間は実際の落雷が起きなかったことを確認し、**PASS**とした。

### Rod／copper

runnerはlightning rodを設置し、その1 block上をexplicit targetにした。これはMcRemoteによるrod探索／retargetを
試したものではない。exact strikeはPASSしたが、probeはrodのpowered stateを保存せず、目視可能なlamp等も用意して
いなかった。oxidized copperは観測時点で変化しなかった。

したがってrod通電は**未判定**、copperは「今回変化を観測しなかった」だけとする。これは
`world.strikeLightning`のexact contract違反ではなく、試験方法不足である。

### Particle

単発のflameを人間が目視し、product wire／代表描画は**PASS**した。ただし空中の単発表示は位置と回数を判定しにくい。
次回使う場合は、事前配置した目印の1 block上へ約1秒間隔で4回出す。これは複数particleを一requestへbatchするAPI試験
ではなく、人間が同じ既存methodを認識しやすくする試験fixtureである。

### 落雷の距離比較

96 blockの単発試験では人間が全く認識できなかったが、ターミナル承認へ画面を切り替える手順と距離選定が不適切だった。
「96 blockでは見えない」という結論には使わず、**未判定**とする。

改善runでは、金blockを目印に、近距離約20 blockで3回、その後playerを中間距離約48 blockへ自動移動し3回、各約
1.05秒間隔で落雷要求を送った。title／subtitle／chat通知は使わなかった。全6 requestは`result:null`で、rate拒否はない。
人間は次を報告した。

- 近距離3回: 光と音を明瞭に認識
- 中間距離3回: 光と音を明瞭に認識。ただし音量差は小さい
- 単発より距離差が明らかに分かりやすい
- 自動移動と画面通知なしの流れは確認しやすい

この6回はRPC successと人間観察を記録する。probeを各回armしていないため、各eventのexact target／causeを6回分個別に
再主張しない。exact target／causeは先行する単発probeで確認済みである。

## Harness／進行上の観察

- `run_id`をrunner CLIへ誤って渡した試行と、`player.setPos`からdimension引数を落とした試行は、いずれも落雷送信前に停止した。製品FAILではない。
- title／subtitleは過剰で、command feedbackがchat履歴を汚し観察を妨げた。後続runでは使わない。
- live-human中に無関係な次項目へ自動進行すると、人間が直前結果を記録できない。関連する短いsequenceだけを事前合意して一回で動かし、終了後に停止する。
- 探索と深掘りは人間自身がPython／Scratchから行う方が速い。半自動live-humanは、事前の項目表、目印、反復、時間制御を備えた再現確認へ限定する。

## Gate conclusion

direction、外部remove、full lightning、CUSTOM event、cancellation、変身後handle失効、既存particle代表描画、
近／中距離の光と音は要求範囲でPASSした。

一方、外部dimension移動後の初回reasonがexact contractと異なり、construction permissionも一貫したsession admissionに
なっていないため、**b7 gateは二blockerでHOLD**とする。protocol ownerは`2026-09-01-02`を含むsuccessor fixtureを発行し、
McRemote担当は`entity_dimension_changed`の判定順、permission snapshot、join／quit closure、snapshot build range、
`mcr.lightning`削除を実装してdeterministic test、Paper 1.21.11、Paper 26.2／Java 25 compatibility pulseを返す。
修正版でproduct JAR identityが変わるため、coordinatorは新JARを固定し、外部dimension移動、online-only lightning、
session状態遷移に限定したlive-autoを行う。

rod／copperと96 block単発はcontract blockerではなく、試験方法不足による未判定である。visual／audio、個別副作用の
件数・順序・収束は元のnon-claimを維持する。今回の二修正はvisual／audio surfaceを変えないため、追加live-humanは
b7 close条件にしない。

## Sanitized artifact

- [result-summary.json](../artifacts/2026-09-01-b7-direction-lightning-live/result-summary.json)
  - SHA-256: `1b785b8a95c6aff27d6ae59280b8629818f5e26a4456b03e13741adee18ec1a0`

artifactは判定、固定source／JAR、公開可能な環境identity、case別結果だけを収録する。token、private endpoint、
pairing identity、player UUID、実座標、raw server logは収録しない。

## Non-claim

- Paper 26.2でのlive実行
- Python candidateから実pluginへの代表往復
- Scratch学習者向けdirection／lightning block
- rod powered state、copper deoxidationの発生保証
- 雷の可視／可聴距離の閾値、音量曲線、client設定間の同値
- damage／fire／変身の件数、順序、収束、later tick barrier
- 変身後entityの新handle取得
- world cleanup／snapshot rollback
- default branch統合、公開artifact、tag、release
