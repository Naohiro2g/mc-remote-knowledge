# b8 gate close：handoff-materials分類の返却

- 搬送元: scratch-editor / Codex、作成日2026-10-03。
- branch: `agent/b8-compatibility@01cdb0bfee3a681697ffa44db5b890045b74b01c`。公開source／tag／developは`691576f60b7f0824e1753bd6823901d01fbe2422`。
- knowledge contract path: `00-hub/release-gate-notes_ja.md`のb8 CLOSED節、`00-hub/dev-repo-protocol_ja.md`、`10-protocol/protocol-tooling-migration-plan_ja.md`。
- knowledge contract commit: 指示票`2a8c3eae4e489e67f044111b0d1e6cdd22ead86a`のCLOSED節を実参照。bootstrapした最新remote main `90cf87fbcd132984ef027a98a263e5911aaf30bf`のruntime／INDEX／移管計画／既存live recordも読んだ。
- 既存14 directoryの分類: **①正式evidence候補5、②後続へ引継ぎ6、③廃棄候補3**。本返信directoryを含めると15件（①6、②6、③3）。
- これは分類と搬送素材の返却。正式配置、外部送信、directory削除、b9移管の実装は行っていない。①の新しいrecord／artifact pathは命名提案で、authoringと配置はknowledge担当。
- ③はcoordinatorによる**本文全文の着地確認と旧素材の非参照確認待ち**。summaryだけの着地で廃棄可とは扱わない。未着地の内容があれば、残して①または②へ再分類する。
- `2026-10-03-b8-publication/HANDOFF-INVENTORY_ja.md`の全②の暫定分類を本票で置き換える。以前の票／export hashは改変せず履歴として残した。

## 既存directoryの全件分類

全pathは`handoff-materials/`からの相対path。

| directory | 分類 | 移す先／引継ぎ先 | 理由 |
| --- | --- | --- | --- |
| `2026-09-30-b8-gate-confirmation/` | 3 | 廃棄候補（coordinatorの全文着地確認待ち） | 初回確認票・カタログ着地回答・観測欠落の再現。後続の実装・公開・live結果へ更新済み。 |
| `2026-09-30-b8-scratch-blocks/` | 3 | 廃棄候補（coordinatorの全文着地確認待ち） | 未commit時の9ブロック案と59 case版fixtureへの問い合わせ回答。実装は公開source、fixtureは111 case版へ進んだ。 |
| `2026-09-30-b8-scratch-candidate/` | 3 | 廃棄候補（coordinatorの全文着地確認待ち） | dfcb03cfの旧candidate。df34849のPython同梱由来と691576fの凍結・公開素材は別directoryで残す。 |
| `2026-09-30-block-picker-names/` | 2 | b9のScratch picker担当。設計正本は13-scratch-client/scratch-block-value-projection-design_ja.md §7／scratch-roadmap_ja.md | 日英名・検索の元票、長い名前の表示例とbrowser scriptをalias検索・幅・読み上げ確認へ引き継ぐ。 |
| `2026-10-01-b8-candidate-b7-fixes/` | 1 | knowledge 14-evidence/records/2026-10-03-b8-scratch-close_ja.md と14-evidence/artifacts/2026-10-03-b8-scratch-close/candidate-df34849/（命名提案） | Python同梱WireScopeのsource df34849と、B7是正3件のcommit・artifact identityをつなぐ由来を保存する。 |
| `2026-10-01-b8-fixture-preflight/` | 2 | b9移管coordinator／tooling担当。10-protocol/protocol-tooling-migration-plan_ja.mdのb8基線へ本返信の凍結一覧と一緒に渡す | 凍結前の棚卸しと依存関係の整理。今回の691576fの一覧が移管基線、事前票は一致の履歴として残す。 |
| `2026-10-01-b8-local-playtest/` | 2 | Scratch後続のローカル動作確認担当。private設定・運用ログを保管する場合はmc-remote-backstage担当へ | 接続・表示の再現scriptとローカル試運転の観測を利用できる。正式b8 gateのPASS根拠には使わない。 |
| `2026-10-02-b8-candidate-local-fixes/` | 1 | knowledge 14-evidence/records/2026-10-03-b8-scratch-close_ja.md と14-evidence/artifacts/2026-10-03-b8-scratch-close/candidate-691576f/（命名提案） | 凍結candidateの5 artifact、GUIローカル試験入力、picker／BlockInfoText局所決定を公開sourceへ結び付ける。 |
| `2026-10-02-home-scratch-contract-reply/` | 2 | Stackのホーム設定担当、およびScratchのruntime-config表示担当。元票2026-10-02-home-scratch-contract-driftへの回答 | 設定contractの照合と、設定異常／意図的disabledを画面で区別できない未対応を継続して追跡する。 |
| `2026-10-02-stack-wss-reply/` | 2 | Stackのホーム接続検査／doctor担当。元票2026-10-02-home-runtime-permissionsへの回答 | WSS 401の検査要求にone-shot subprotocolが欠けることを切り分けた回答とローカル再現を保持する。 |
| `2026-10-03-b8-publication/` | 1 | knowledge 14-evidence/records/2026-10-03-b8-scratch-close_ja.md と14-evidence/artifacts/2026-10-03-b8-scratch-close/publication/（命名提案） | 公開tag／develop／workflow／Release asset／OCIのprovider実照合値と公開成果物を保存する。 |
| `2026-10-03-b8-scratch-live-gate/` | 1 | knowledgeの既存14-evidence/records/2026-10-03-b8-dev-live_ja.mdと14-evidence/artifacts/2026-10-03-b8-dev-live/scratch-segment-3/（artifact名は提案）。依存／fixture棚卸しはb9 tooling担当にも渡す | segment 3の実ブラウザ・ブロック往復・human目視の詳細観測を、着地済みsummaryの根拠として残す。 |
| `2026-10-03-b8-scratch-live-human/` | 1 | knowledgeの既存14-evidence/records/2026-10-03-b8-dev-live_ja.mdと14-evidence/artifacts/2026-10-03-b8-dev-live/scratch-live-human/（artifact名は提案）。後続観測はScratch／教材／サウンド担当にも渡す | 2 playerの申告、dustサイズ差、音と教材候補の観測を要約に潰さず保存する。 |
| `2026-10-03-wirescope-column-width/` | 2 | b9 WireScope担当。agent/b8-compatibilityの01cdb0bとGATE-ADDENDUMを起点にする | human owner承認済み・commit／push済みの列幅改訂をb9へ送る決定。b8公開には含まない。 |

## 参照identityと受領後の処理

### 2026-09-30-b8-gate-confirmation

- 参照identity: `5aaa9c59acc393cd0a0de5cb45a5e619a5e87abe`。
- 次の一手: landing-confirmationとrelease-gate-confirmationの全文がknowledgeへ移っていること、再現素材が他票から不要となったことをcoordinatorが確認する。未着地の内容があれば残して再分類する。

### 2026-09-30-b8-scratch-blocks

- 参照identity: `5aaa9c59acc393cd0a0de5cb45a5e619a5e87abe`。
- 次の一手: mcremote-replyとscratch-blocksの全文をknowledgeのgate記録・Scratch spokeと照合。未着地のreason/config回答や局所決定があれば残す。旧59 caseの案を現行contractとして再利用しない。

### 2026-09-30-b8-scratch-candidate

- 参照identity: `dfcb03cf97fed998268b4714feb32d03a209f549`。
- 次の一手: MANIFESTの全文と旧artifact identityのknowledge着地、旧archiveへの非参照を確認する。その後に限り旧build logとarchiveを処分する。

### 2026-09-30-block-picker-names

- 参照identity: `初期base 5aaa9c59acc393cd0a0de5cb45a5e619a5e87abe／公開実装 691576f60b7f0824e1753bd6823901d01fbe2422`。
- 次の一手: 後続担当がknowledge-handoff、browser-smoke、画像を受領し、公開実装に対して再現入口を更新する。旧画面の承認をb9の検証済み扱いにしない。

### 2026-10-01-b8-candidate-b7-fixes

- 参照identity: `df34849d2502a498a06c5fe07a91d03e925124eb`。
- 次の一手: MANIFEST・REPLY・detached manifestとartifact identityを正式配置。ZIPの同一bytesとsourceの異なるmanifestを区別する。重複GUI／Bridge archiveは全文着地・非参照確認後だけ整理。

### 2026-10-01-b8-fixture-preflight

- 参照identity: `dfcb03cf97fed998268b4714feb32d03a209f549 → 691576f60b7f0824e1753bd6823901d01fbe2422`。
- 次の一手: 本返信の12 fixture／consumer一覧を主入口にし、事前票を比較用として受領する。owner・source・配布先の変更は別途批准された範囲で行う。

### 2026-10-01-b8-local-playtest

- 参照identity: `df34849d2502a498a06c5fe07a91d03e925124eb（試運転準備時点）`。
- 次の一手: 起動script・観測・画像を後続担当へ渡し、runtime-configと運用値は公開票から除く。稼働サービスがこのpathを参照し得るため受領だけを根拠に削除しない。

### 2026-10-02-b8-candidate-local-fixes

- 参照identity: `691576f60b7f0824e1753bd6823901d01fbe2422`。
- 次の一手: MANIFEST・REPLY・DECISIONS-HANDOFF・verification.json・verify-artifacts.pyを正式配置する。局所決定は着地済みspokeへ参照。大きな入力archiveはidentityと試験入力の参照を残し、廃棄可否を別途確認する。

### 2026-10-02-home-scratch-contract-reply

- 参照identity: `Scratch df34849d2502a498a06c5fe07a91d03e925124eb／元票Stack 68832e0a95c0462462e9a10115bfae272ec1a6d7`。
- 次の一手: materials/reply_ja.mdをStack担当へ人間経由で返し、表示課題はScratch NOTESで継続する。設定schemaを変更する判断ではない。

### 2026-10-02-stack-wss-reply

- 参照identity: `調査対象 f133fc95ed7b23109cc1908dc4f0dae066510258（b7.post2）／元票Stack 19c8afa68a3133addf82f308ab642d8ca4e51e15`。
- 次の一手: reply、probe-subprotocol.mjs、probe-result.jsonを検査修正へ引き継ぐ。実ホームTLS／proxy経路は今回未検証、製品改訂は不要と回答済み。

### 2026-10-03-b8-publication

- 参照identity: `v2320.0.0b8 → 691576f60b7f0824e1753bd6823901d01fbe2422／workflow 37113933602`。
- 次の一手: RESULTとprovider・asset・OCI identity、公開manifest／detached manifestを正式配置。旧HANDOFF-INVENTORYの全②の暫定分類は本返信で置き換える。

### 2026-10-03-b8-scratch-live-gate

- 参照identity: `691576f60b7f0824e1753bd6823901d01fbe2422／b8-integrated-artifact-set-1`。
- 次の一手: RESULT、live-results、human-review、frozen-identities、画像digestとsanitized画像を正式配置。browser-step等を再現入口に添える。private/は公開搬送せずbackstage担当、runtime/は重複展開物で稼働参照終了と移管確認まで保持。backpressure実機NOTRUNを維持する。

### 2026-10-03-b8-scratch-live-human

- 参照identity: `691576f60b7f0824e1753bd6823901d01fbe2422／knowledge参照3f0c14ab9e41e469a23f865b3e7a313744bdcdc7`。
- 次の一手: RESULT、DUST-BEDROCK-DIFFERENCE、observations・start-observation・image-identities・export-identitiesを正式配置。iPad dustサイズのFAILを原観測として保持。private原画像は公開搬送せずbackstageへ。self文言、音源位置教材、シーケンス関心は後続担当へ渡し、実装時期は確定しない。

### 2026-10-03-wirescope-column-width

- 参照identity: `01cdb0bfee3a681697ffa44db5b890045b74b01c`。
- 次の一手: patch・測定JSON・画像・再現script・ZIP／manifestを受領する。b9候補のsource・依存に合わせてartifact identityと確認を更新する。

## 混在素材の扱いと未完了

- 既存正式live recordは`14-evidence/records/2026-10-03-b8-dev-live_ja.md`。latest `90cf87fbcd132984ef027a98a263e5911aaf30bf`の本文にも「各担当の返却票を要約した」とある。詳細JSON・画像・再現scriptの全文移管をこのsummaryから推定しない。
- live 2 directoryの`private/`、接続先実値、認証・運用ログ、参加者名を含む原画像は①の公開搬送に含めない。保持先は②`mc-remote-backstage`担当。raw画像はhash参照を使い、公開画像へ採用する場合は別途匿名化する。
- ①のJSON／画像は正式配置前にknowledge担当がredactionを確認する。今回directory全体を公開用archiveへまとめたり、private素材を新しい返信へコピーしたりしていない。
- live-gateの`runtime/`は凍結artifactの展開物。保存済み入力との同一性を参照し、稼働サービスのpath参照終了と必要素材の移管を確認してから③へ回す。今回サービス停止・設定変更は行っていない。
- 旧candidateの大きなGUI／Bridge入力archiveを全部knowledgeへ複製する要求ではない。正式記録へticket全文・artifact identity・検証結果を移し、再取得経路／参照の要否をcoordinatorが確認した後だけ重複archiveを整理する。
- ②の受領、①の正式配置、③の確認結果は未受領。現状は全件ローカル保持。entry MANIFESTのbytes／SHA-256を`materials/handoff-classification.json`へ記録した。
- 本返信directory `2026-10-03-b8-close-inventory/` は①。同close recordとartifactへ分類一覧・fixture一覧・採取script・JSONを移す提案。fixture一覧は`10-protocol/protocol-tooling-migration-plan_ja.md`から参照するb8基線にも使う。

## fixture一覧と検証

- 完全一覧: [FIXTURES_ja.md](FIXTURES_ja.md)。公開sourceからProtocol 7、WireScope 4、Bridge 1の計12件。
- B7明示caseは93、B8は111（nearby19＋handle7＋entity7＋particle26＋sound37＋resource ID15）、signは7個の名前付きcase group。他9 fixtureの全体case数は未定義とし、構造の件数を別欄に出した。
- `git show`による12件のbytes／SHA-256と既存凍結後棚卸しとの照合PASS。readerは同sourceのtest内のrepo相対import／require／URL参照を解決して採取した。
- 全14 directoryに重複なく分類を付けたことをscriptで確認。機械可読一覧は`materials/handoff-classification.json`／`fixture-inventory.json`。
- 再採取: `python3 handoff-materials/2026-10-03-b8-close-inventory/materials/collect-inventory.py`。
- 製品source／fixtureの変更、build、live再試験、commit／pushなし。公開sourceとb9列幅branchを維持。knowledge／Stack／backstage repoへの書込みなし。
