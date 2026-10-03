## Release gate 確認票 — Python segment 2 追記（残りの試験）

- 対象 repo: `Naohiro2g/minecraft-remote-api`
- 対象 branch/commit: `codex/b8-python-entity-particle@52d35f5304e62f465c1f47ab47c00fe9bcf62470`
- release / channel: `2320.0.0b8`／GitHub prerelease候補。今回公開操作なし。
- gate coordinator: knowledge担当session（Claude Code）
- human release owner: プロジェクトオーナー
- current phase: 凍結exact setの通常dev試験。Python segment 2の残りの試験はPASSで終了し、結果・素材を返却する段階。横断gateの判定はcoordinatorへ返す。
- contract maturity / required test tier: b8契約・exact set凍結済み。Tier 3（変更範囲内の短いlive-autoと、WireScope表示のlive-human）。
- knowledge contract path: `00-hub/release-gate-notes_ja.md`（2026-09-30のb8 gate節）、`00-hub/b8-gate-live-test-sheet_ja.md`（共通／2. Python）、`10-protocol/wire-format-design_ja.md`（§5.8.3）、`15-wirescope/wirescope-station-attach-design_ja.md`（§8）。
- knowledge contract commit: `396326def73d99aae91dca4de9416f4eca6d2aea`（実際に読んだSHA）。
- gate manifest identity: `b8-integrated-artifact-set-1`。上記gate節で凍結されたidentityを使用。
- change cone: Git外の残り専用test runnerと観測素材だけ。Python source／wheel／sdist／同梱WireScope、他repo、server配置／configに変更なし。
- reused PASS / rationale: coordinator回答396326dに従い、同じ凍結identityのrun 1でPASSした短いimport、entity lifecycle、ParticleSpec、playSound、WireScope frame 1〜34を再利用。b7で新規pairingした保存tokenによるb7→b8 hello継続PASSも既存記録を維持。
- exact compatibility set / freeze status: `b8-integrated-artifact-set-1`（凍結継続）。Python source `52d35f5304e62f465c1f47ab47c00fe9bcf62470`、CI wheel 195,068 bytes／SHA-256 `dcedff010feac0d5df24ff85dd84b321fb819f78563c39431ac32d9d75bc0180`。同梱WireScope source `df34849d2502a498a06c5fe07a91d03e925124eb`、ZIP 83,746 bytes／`4cb349894b71d61d7ca143d8362a5b79deb1810e1d7a9e31ad30e29bfe370a07`。新artifact生成・再凍結なし。
- target deployment / profile / lock: human owner指定の通常dev／host-native。接続先はGit外のlocal設定を使用し、票・素材には記載しない。配置identityはcoordinatorのgate記録を参照し、Python担当からdeploy／lock操作はしていない。
- authorized next action: coordinator396326dが同じ凍結identityで残りだけを許可。userが「残り専用runnerで実施し、新しいSHAを返す」を選択。run 2のWireScope接続準備停止後はuser「準備できた。新runnerで再開」によりrun 3を実施。今後のsegment開始・release判定はcoordinatorへ戻す。
- test class: `live-auto`＋`live-human`（human ownerによる実browserのWireScope観測）。
- 実行した command / 手順: CI wheelを導入した隔離Python 3.13環境で `/tmp/mcr-b8-52d35f5-wheel-venv/bin/python -I handoff-materials/2026-10-03-b8-dev-token-upgrade/materials/run-3/python_remaining.py` をTTY実行。start→同じ保存tokenの認証済みhello→human attach確認→getBlock／5kind sound／block復元→human core表示確認→凍結sample draw_graph→human graph表示確認→finish。実runner SHA-256 `c001bd5cbc8ab8b5151133c995dec4f226d82f4b9ac83f786a2e9797574a5c7c`。
- 結果: **残りの試験PASS（実素材run 3、exit0）**。21件のPASS行、212 frames／106 RPC往復。詳細は下表。途中のrun 2は接続準備でFAIL・本体未実施として別に保存し、PASSへ書き換えない。
- evidence record / artifact: 正式evidenceのrecord／artifact配置はknowledge担当のauthoring待ち。搬送素材は本repoのGit外 `handoff-materials/2026-10-03-b8-dev-token-upgrade/materials/`。run 1、run 2、run 3を分けて保持し、今回のsummary／sanitized transcript／human観測／runnerを下記hashで固定。ローカル素材を正式evidenceとは主張しない。
- 未検証の境界: server内部のSoundGroup volume／pitch数値そのもの、2-player receiver差、particle描画、音の聴取・定位（segment 4）、Windows実機導入。graphのUI全162行をhumanが個別に確認したとは主張せず、human貼り付けはframe113〜212、loggerは51〜212の全81往復を保持。
- security / compatibility / rollback の確認: 同じ保存tokenで23.2.0／MC1.21.11のhello成功、再pairなし、保存token削除・上書きなし、auth設定変更なし。token／pairing_id／private endpoint／player UUID／表示用attach codeを素材に含めない。仮stoneは元のairへ復元・readback一致、仮block残りなし。connection／WireScope station正常close。今回rollback操作なし。
- 判定を求める事項: 再利用PASSと今回の残りPASSをPython segment 2へ記録し、素材を正式evidence化してほしい。SoundGroup既定はwire省略とresult:nullの正常往復までの観測として扱う。server内部数値・聴取等を本票のPASSへ含めるかは拡張せず、coordinatorが残りのgateを進行する。

### 実行結果・WireScope観測

| 対象 | 結果・観測 |
| --- | --- |
| 保存tokenのhello | PASS。protocol23.2.0／MC1.21.11、再pairなし。ownerが実browserのframe1〜2を貼り付け |
| getBlock取得／一時設置／復元 | PASS。BlockValueの属性でairを取得→無印stone設置→stone readback→元airへ復元→readback一致。ownerのframe10／14／50のpayloadでも確認 |
| playBlockSound 5kind | PASS。place／hit／break／step／fallを各3制御（options省略、pitch=0.75＋self、note=18＋world）で計15往復。送信paramsを照合、各result:null。ownerがframe15〜44をpayload付きで貼り付け |
| Python既定呼出 | PASS。hitの追加1往復、receiver:worldのみ送信しvolume／pitch／noteは省略。frame45〜46でownerが確認 |
| SoundGroup既定へ委譲する形 | PASSはoptions省略と正常ACKの範囲。server内部のvolume／pitch数値、実音の正しさは直接観測していない |
| pitch／noteによる置き換え | 5kindでそれぞれのoptionだけを送って正常ACK。合成・変換をclient側で行っていない。実際の音高の判定はsegment4へ残す |
| 凍結3D graph sample | PASS。source52d35f5のexamples/particle_graph.pyそのものを使用。81 dust／self request、81 result:1、frame51〜212 |
| graphのreal-browser表示 | ownerがframe113〜212をpayload付きで貼り付け、送信dust／selfと受信result:1の表示を確認 |
| cleanup | 仮block復元／readback一致、station／connection正常close、run3 exit0 |

### 素材identity

実runnerは基準補正版 `15c5c2cfa1ace74b03fd21c54d0ac575b656f75a39315754f283d8255fbf1003` から残りだけ・5kindのrun 2を作り、その待機部分に開始前readinessと製品既存のbounded reissue操作を追加したもの。baselineとrun 2の原本は変更していない。run 3では再発行操作を使わず、最初のattachで成立した。

| 素材 | bytes | SHA-256 |
| --- | --- | --- |
| `run-3/python_remaining.py` | 11,595 | `c001bd5cbc8ab8b5151133c995dec4f226d82f4b9ac83f786a2e9797574a5c7c` |
| `run-3/frames.jsonl` | 44,212 | `35922a3de2bb5c8d36e7162c98e68b5ea886f965edc2b2ed8b401da1552646a8` |
| `run-3/summary.json` | 6,243 | `ad90cddaef3a62a3a4cc41eb364e6479b2d50bd36e1fd4cdfa4971582452f7de` |
| `run-3/owner-observation_ja.md` | 3,075 | `80e23e9a93818750b330f2cd110d88e8f5d91ae1144bac39ad1d91f48c07a29d` |

凍結graphファイル `particle_graph_frozen.py` SHA-256: `e3824c3800aea4acc3ca1141a289e5a04d34c52cb2492af25b38f050bfe824d3`。

run 2準備停止は `run-2/return_ja.md`、実runner `46b4b61f85eef5679114223755eea9ad4ac8f3fb5de2aca2ed0258348da90271`、frames2件 `12a224e9c87fc0d5d0c0630549c2a12329a56da92dcd472011c4b531c4166794`、summary `b61cb618110a9aa9e0896e5c0309f493f26e7f9dc325e5d6b4722a24d7d0c825`。helloはPASS、owner回答「時間切れ」で準備を中止、world操作0回。今回のPASSはその後、再開確認を受けたrun 3の結果。

接続先設定 `param_dev.py` とprivate credential continuity stateは搬送対象に含めない。正式evidence化・参照先の着地後に素材directoryを昇格／移管／失効へ分類する。
