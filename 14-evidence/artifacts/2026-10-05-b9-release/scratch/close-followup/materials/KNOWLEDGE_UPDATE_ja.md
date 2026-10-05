# b9 close②の追跡更新・cleanup実施の搬送票（Scratch → knowledge）

- 搬送元 repo: `Naohiro2g/scratch-editor`
- 搬送元 surface: b9 close、Stack／backstageの受領確認と元資料の整理
- 搬送元 branch/commit: `agent/b9-tooling@7fbbf034488760d8fc7e034bf23f3e08e6e1807d`（製品source変更なし）
- 作成日: 2026-10-06
- 種別: その他（受領・整理の事実と追跡更新）
- knowledge contract commit: `5beaad2557abbc6e90ada03edf7d0a2918fa7a52`（remote mainを確認し、このSHAの下記文書を実読）
- knowledge contract path: `00-hub/dev-repo-protocol_ja.md` runtime、`00-hub/b9-gate-close-instructions_ja.md`、`00-hub/release-gate-notes_ja.md` b9節、`14-evidence/records/2026-10-05-b9-release_ja.md`
- 指示: human ownerから両宛先の返却票を受け取り、2026-10-06「進めて」で受領済み元資料の条件付きcleanupと本追跡更新票の作成を実施

## 受領・照合の結果

| 引継ぎ先 | 根拠 | 更新する状態 |
| --- | --- | --- |
| Stack | `STACK_RECEIPT_ja.md`: 9,247 bytes／SHA-256 `ed5dbd56488b259e86f8040d2500bd10f8d1173da2502ac9a682d82282954483`。報告source `a30aa8b1b230e88ed92c515b357a088d97ddb0da`。6 file／13,894 bytesの全文・bytes・SHA-256がScratchの元、搬送inventory、受領inventory、Stack収容実体と一致 | 設定生成と直接Bridge／外側WSS検査の対応完了報告を受領。回答2件の受領待ちは解消。元6 fileと空になった2 directoryを整理済み |
| backstage | `BACKSTAGE_RECEIPT_ja.md`: 3,118 bytes／SHA-256 `d116d9238f1ac0718a077aa2a8a03166e9735362095a54c6c484be4bd09a90e3`。管理名 `scratch-private-intake-20261006`。28件棚卸し、必要17件をGit外暗号化コピー・復号後bytes／SHA一致という報告を受領 | 受領待ちは解消。原画像10件は別用途・参照を確認してScratch元を整理。起動関連7件、長期非保存11件、runtimeは引き続き保持 |

Stackの収容先への対応は`stack-received-inventory.json`に全6件を記載した。5件は新規コピー、WSS回答本文1件は既存全文を再利用。以後、旧Scratch source pathは搬送時のidentityとして扱い、全文はこのinventoryのStack側received_pathから参照できる。

backstageの暗号化保管物には本担当からアクセスしていない。17件のコピー・復号照合は同担当の報告として扱う。原画像本体をknowledgeの公開evidenceへ代替収容したという主張はしない。

## 正式evidenceの着地確認と整理

最新knowledgeのb9節とrelease記録で、①151件の正式収容と4 logのhome path置換を確認した。Git treeがtruncatedではないことを確認し、該当blobの実体を取得、Git blob SHAとbytesを検証して元と全文照合した。

- 今回収容151件: 147件は全文・bytes・SHA-256一致。4 logはhome pathを`~`へ置換した場合のみ一致し、他の差は無い
- 既収容live 18件とclose packet 11件も全文一致
- 合計180件: 176件は全文一致、4件は上記置換のみ。搬送元・収容先それぞれのbytes／SHA-256とknowledge blob identityは`evidence-receipt-verification.json`に保存
- 照合完了後、元180件、役目を終えた複製・一時入力36件、Stack移管済み6件、backstage移管済み原画像10件を整理。合計232件／1,703,300,137 bytes、空になったsource directory13件を除去
- 元の一覧、削除前のbytes／SHA-256、分類は`cleanup-plan.json`、実施結果は`cleanup-result.json`
- 10/5の分類・確認票は当時のsnapshotをknowledgeの正式収容先に保持し、本票を現在の更新差分とする

## 残る②と終了条件

| Scratch側のdirectory | 保持するもの・担当 | 整理できる条件 |
| --- | --- | --- |
| `2026-10-05-b9-scratch-dev` | 現行b9のruntime、private起動設定・script・管理情報、browser状態・log。手元配信のScratch担当 | ownerの終了／置換指示、参照終了、後続入力確保。非保存の一時素材も使用終了を確認後に扱う |
| `2026-10-03-b8-scratch-live-gate` | b8のruntimeと戻し先設定・script・変更前設定、一時browser／観測・旧管理情報・log。手元配信／戻し先のScratch担当 | ownerの不要判断、b9管理情報等からの参照終了、後続入力確保。現在b9管理情報にb8戻し先への参照がある |
| `2026-10-01-b8-local-playtest` | 旧配信の設定・起動／probe script、server log等。旧配信のScratch担当 | 旧配信と戻し用途の終了、参照終了。BridgeとWireScopeのlogを現にprocessが開いている |
| `2026-10-06-stack-backstage-handoff` | 両返却票と受領確認、元／収容先inventory、照合・cleanup記録、本搬送票。Scratchの引継ぎ確認担当 | 本追跡更新と必要記録のknowledge正式収容を確認後に整理。privateな運用実値は収録していない |

保持3,537 fileについて、全fileの存在とlog以外のbytes／SHA-256が整理前後で変わらないことを確認した。稼働b9 supervisorと旧配信logの参照をhost側で読み取り専用確認。確認できたprocessのopen file／command引数に削除対象は無かった。一部desktop／system processのdescriptorは権限上読めなかったため、browser状態・一時private素材11件は一括削除せず保持した。service停止・設定変更・credential操作は行っていない。整理後、b9の8611／8612／4183は接続可能、supervisor存続を確認。旧8602／4173も接続可能だったが、旧Scratch GUIの8601は接続拒否だった。旧GUIの整理直前の待受けは確認していないため、停止時期の判断はせず、起動・再起動も行っていない（post-cleanup-services.json）。

## ナレッジ着地希望

1. `00-hub/release-gate-notes_ja.md` b9節のScratch②の「Stack受領待ち」「原画像のbackstage移管待ち」を受領済みへ更新し、元処理済みと継続保持条件を記録
2. 本票と両返却／ACK、照合・cleanup結果、各source／receiver inventoryをb9 closeの追記evidenceとして正式収容。既存close票と併読できる配置にする
3. 旧Scratch source pathの参照は、Stack受領inventoryまたは本票のknowledge収容先への追跡に引き継ぐ。歴史的なsource identityは書き換えない

- 根拠/検証: artifact／収容内容の決定論的照合と参照確認。今回live試験・製品test・buildは行っていない。Stackの製品test結果は同担当の報告であり、再実行していない
- 既に変更した文書: ignoredな本packet、ローカル`NOTES_ja.md`。製品source、fixture、tag、Release、develop、他repoは変更なし
- 捕捉cleanup: 処理可能な元資料は整理済み。残る稼働・戻し用途と本packetは上記条件で②保持。比較用helper branch／worktreeも本票の正式着地確認まで保持
- 着地後の確認戻り先: Scratch担当へknowledgeのpush済みSHA、収容先、置換したfileの一覧を返す。照合後、本packetの処理を進める
