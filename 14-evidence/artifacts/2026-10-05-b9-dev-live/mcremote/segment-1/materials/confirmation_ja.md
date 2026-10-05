# B9 実機試験確認票 — McRemote（segment 0・1）

2026-10-05。segment 1 は **live-auto 60 PASS 行／FAIL 0、id 付き `chat.post` の `result:null` 確認 PASS、終了コード0**。chat 確認を含む合計は61 PASS行。PASS行数はテストケース数ではなく、runner の完走サマリ行も含む。生成したentity258体は全て削除し、保存した9箇所のBlockValueを復元・再読して一致を確認した。

## Release gate 確認票

- 対象 repo: `Naohiro2g/McRemote`
- 対象 branch/commit: `feat/b9-contract-packaging@5cb33ebad4bf2c5e36c3433b0f70fe6070915b00`。push済みの凍結sourceを使用。tracked working tree はclean、今回source変更なし。
- release / channel: `1.21.11-2320.0.0b9` / beta。artifact version `2320.0.0b9`、wire protocol `23.2.0`。
- gate coordinator: knowledge担当session（Claude Code）。
- human release owner: プロジェクトオーナー。
- current phase: 凍結済み・実機試験。本票は通常devでのsegment 0の既存観測とsegment 1の実施結果。
- contract maturity / required test tier: B9 exact set凍結済み、Tier 3の指定live試験。横断GREENの判定前。
- knowledge contract path: `00-hub/b9-gate-live-test-sheet_ja.md`（共通／segment 0・1）、`00-hub/release-gate-notes_ja.md`（確認票／2026-10-04 B9 gate／exact set凍結）、`00-hub/release-operations-responsibility-design_ja.md` §3・§8。最新runtimeとINDEXを入口として参照済み。
- knowledge contract commit: `561de98b5c15864ac9b86cb6dcaeef1f20ce635b`。依頼SHAとbootstrap時のremote mainが一致し、上記SSOTをこのrefで読んだ。
- gate manifest identity: `00-hub/release-gate-notes_ja.md` の `b9-integrated-artifact-set-1`、上記knowledge SHA。
- change cone: B9の `chat.post` 成功null、共有fixture取得元移管、JAR作成とREADMEの既報差分。本実施では製品source・凍結JARを変更せず、既存live-autoに記録・秘匿化・清掃wrapperと一回のchat確認を付けた。
- reused PASS / rationale: 実施票の指定に従い、変更に影響しないB8 live PASSと未知event typeのdeterministic試験を再利用する方針。今回の60 PASS行とchat nullはB9で新規実行。281 deterministic tests、umask 002／022／CIのJAR一致、fixture byte一致は既報のcandidate確認票を参照し、今回再実行していない。B8全証跡の再監査はしていない。
- exact compatibility set / freeze status: `b9-integrated-artifact-set-1` 凍結済み。今回の実行対象はそのMcRemote sourceとJAR。Python／Scratch／toolingの代表往復は他segmentに属する。
- target deployment / profile / lock: dev通常環境のホームサーバー、Paper／McRemote host-native、既存run.sh／Screenで稼働。Paper `1.21.11-132-ver/1.21.11@c5eb079`、MC `1.21.11`、Java `21.0.12.1`。接続先は受領済みdev接続先へ一時SSH tunnelで接続。deployment lockは本票では提示・検証していない。
- authorized next action: human ownerからの通常devへの差し替え・再起動、live-auto／chat null確認、実施票確認票作成を完了。coordinatorへ本結果と素材を返す。
- test class: `live-auto`。pairingのゲーム内承認と既存Scratch接続はhuman ownerの操作・観測として区別する。
- 実行した command / 手順: 下記「実施手順」。認証済みhelloの版照合を先に行い、凍結runnerで本体を実行、その後id付きchat要求を一回実行した。
- 結果: 下記一覧のとおり。成功runは2026-10-05 **08:44:49–08:45:41 JST**、exit0。認証済みhello4件がいずれもprotocol `23.2.0`／MC `1.21.11`。FAIL行0、cleanup failures0。
- evidence record / artifact: 本directoryのsanitized transcript／log／JSON／wrapper、下記segment 0素材とcandidate確認票。正式knowledge record／artifactは未authoring。分類②としてB9 coordinatorへ、knowledge SHA／exact set／source SHA／JAR SHAを参照identityとして移管する。
- 未検証の境界: segment 2（Python代表往復と同梱WireScope）・segment 3（Scratch／移管Bridge／WireScope代表操作・表示幅目視）は本担当未実施。Scratch接続観測だけでsegment 3全体PASSとはしない。未知eventのlive生成、world全体／NBT／全entity／chunk／fluidなどの完全巻き戻し、実機rollback、cold-reader、Paper 26.3／単一JARは本票の検証範囲外。
- security / compatibility / rollback の確認: Auth ONとCredential HEALTHYを起動logで確認。認証設定を変更せず、human owner承認の試験用pairingを使用。tokenはrunner process memoryに保持し素材へ保存しない。token／pairing_id／private address／player UUIDを秘匿化・点検した。試験後JAR digest一致、Paper／config／起動script不変。通常利用・pairingに伴うcredentialの更新はあり得るためcredential保存bytes不変とはしない。b8退避物は保持、rollback実行なし。
- 判定を求める事項: segment 0の観測とsegment 1のPASS／素材をB9 gate証跡として採用するか。component／横断gateの最終判定と公開指示はcoordinatorに返す。

## PASS／FAILと観測

| segment／項目 | 結果 | 根拠・観測 |
| --- | --- | --- |
| 0：b9へ一件差し替え・再起動 | PASS（既報） | 07:50:15 JSTにPaper Done、b9 enable。b8を退避し、凍結JARを配置 |
| 0：JAR／Paper／Java／Auth | PASS | JAR 261,016 bytes、下記SHA。Paper build132／Java21。Auth enforcement true／Credential HEALTHY |
| 0：既存実token継続 | PASS（人間観測） | 08:02:10 JST、human ownerがb9 Scratchから再pairingなしのhello成功を報告。protocol23.2.0／MC1.21.11。表示payloadを保存済み。Scratch source commitの独立照合は本担当未実施 |
| 1：認証済みhelloの先行照合 | PASS | 成功runで4件、protocol23.2.0／MC1.21.11。違う版で本体を実行していない |
| 1：指定live-auto | PASS | 60 PASS行、FAIL 0。logに各項目。hello／build状態、BlockSpec／BlockValue、FIFO／flush／1041 notification、events、entity、particle、soundなど指定runnerの完走 |
| 1：id付きchat.post成功null | PASS | 要求id5、応答に `result:null`。文字列resultやerrorでないことを検査 |
| 1：生成entityの扱い | PASS | 258体生成。試験中1体削除、close前に試験生成の残り257体を削除。already_absent0、cleanup failures0 |
| 1：変更blockの扱い | PASS | 9箇所のBlockValueを事前保存、close前に復元、各getBlockで保存値との一致を確認 |
| 試験後のartifact／設定 | PASS | JAR SHA一致。Paper／config／run.shは差し替え前の採取digestと一致 |

凍結JAR: `mc-remote-1.21.11-2320.0.0b9.jar`、261,016 bytes、SHA-256:

```text
4feb90dbdba8550cd16800cc3d384e42fed16a5c5e20faa489a0381ad2cda58e
```

## 実施手順

固定 `scripts/live_auto.py` のSHA-256は `7a093d27ac349023e7be90c48597ead1a1207772a4fee084933ee2f8c794352f`。このfileを編集せず、B8正式保存wrapperを基にした `run_with_transcript.py` からimportした。wrapperは要求・応答採取、秘匿化、試験生成entityの削除、9箇所BlockValueの保存・復元照合、独立chat null確認を担当する。runnerのテスト本体・合格条件は変更していない。

接続値を秘匿した実行形:

```sh
python3 -u handoff-materials/2026-10-05-b9-mcremote-live-auto/materials/run_with_transcript.py \
  --host <受領したdev接続先へのtunnel> --port <tunnel-port> \
  --expect-mc 1.21.11 --protocol 23.2.0 \
  --handle-capacity 256 --particle-limit 1000 --interactive-pair
```

初回はpairing `212-814` が承認前に失効してexit1で停止。認証済みhello／本体／chat確認は未実施、world試験変更0。human ownerの「ちょっと待って」で待機し、後の新コード依頼と `284-264` の実行報告を受けて再開した。初回素材は `attempt-1-expired/` に保持。初回は認証前提条件の未成立であり、今回成功runのFAIL行0と混同しない。候補や認証設定を修正して続行したものではない。

成功runの本体と清掃後、新しい認証済み接続から以下の要求・応答を採取した。

```json
{"jsonrpc":"2.0","id":5,"method":"chat.post","params":["McRemote b9 live-auto: chat.post result null verification"]}
{"jsonrpc":"2.0","id":5,"result":null}
```

blockの座標は試験connectionのbuild contextに対する相対座標。事前値は次の9箇所。復元後はblock_idだけでなくstateを含むBlockValue全体を照合した。

| 座標 | 事前BlockValue |
| --- | --- |
| `[0,73,0]`、`[1,73,0]`、`[2,73,0]`、`[3,73,0]`、`[4,73,0]`、`[3,73,1]` | `{"block_id":"minecraft:air","state":{}}` |
| `[4,73,1]`、`[7,73,0]`、`[8,73,0]` | `{"block_id":"minecraft:stone","state":{}}` |

## 搬送素材

- [run-summary.json](run-summary.json)：時刻、終了値、行数、hello数、chat応答、cleanup集計、主要artifact SHA。
- [rpc-transcript.jsonl](rpc-transcript.jsonl)：sanitized要求・応答、BlockValue保存値など、2,407 records。
- [live-auto.log](live-auto.log)：60 PASS行とchat null1 PASS行。
- [cleanup-summary.json](cleanup-summary.json)：entity258／block9の清掃集計、failures空。
- [environment.json](environment.json)、[post-run-identity.json](post-run-identity.json)：開始identity／起動log、試験後のdigest照合。
- [run_with_transcript.py](run_with_transcript.py)：使用wrapper。
- [segment 0再起動結果](../../2026-10-05-b9-dev-restart/materials/restart-result_ja.md)、[Scratch人間観測payload](../../2026-10-05-b9-dev-restart/materials/scratch-hello-observation.json)。
- [candidate確認票](../../2026-10-05-b9-mcremote-candidate/materials/confirmation-delta_ja.md)：再利用するdeterministic／artifact比較のidentity・結果・範囲。
- `attempt-1-expired/`：初回停止のlog／transcript／cleanup集計。

主要sanitized transcript SHA-256は `dc8b5f5c9260c6850f7bc11912dfdc0a27361608db015d8b2bf81ce45aa53b76`、logは `84c03f7d74ddf2c7b7fe340b9bc06e5587c572e1e6c35d38d98c32611bee4b6a`。その他はrun-summaryを参照。素材はgitignore対象で、正式knowledge evidenceのauthoring・配置・commitはknowledge担当に委ねる。
