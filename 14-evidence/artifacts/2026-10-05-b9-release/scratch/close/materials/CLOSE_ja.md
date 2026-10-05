## Release gate 確認票（b9 close・handoff分類）

- 対象 repo / surface: `Naohiro2g/scratch-editor`／Scratch、共通tooling移管・公開の手元素材
- 対象 branch/commit: `agent/b9-tooling`／`develop@7fbbf034488760d8fc7e034bf23f3e08e6e1807d`。公開tag `v2320.0.0b9`。比較helperは `agent/b9-release-preflight@dfebdfebd6aad8fd1e3246ca1566653f6b198b95`
- knowledge contract path: `00-hub/dev-repo-protocol_ja.md` runtime、`00-hub/b9-gate-close-instructions_ja.md`
- knowledge contract commit: `099c40b0c312694712653885200f3114ea4bed33`（取得時remote mainと一致、実読）
- 作業範囲: 指定b9の4 directoryと、残っていたb8の11 directory、計15 directoryの分類。本返却用directoryも①として下記に追加。source統合と横断gateの最終判定は本作業の対象外
- 結果: 分類完了。①の移管対象は151 file／5,966,766 bytes（本close packet自身を除く）。③候補54 file。②は現行配信・rollback／Stack回答／private opsの明記した用途だけを残す
- 収容済みの照合: `2026-10-05-b9-scratch-dev`のknowledge収容分18 file／476,065 bytesは、全文byte一致・SHA-256一致。指定knowledgeのGit treeからblobを取得し、blob SHA-1も検証。改変なし。詳細は`materials/landed-evidence-verification.json`
- 公開物との照合: `2026-10-03-b8-publication`に残る`contracts.tar.gz`／`wirescope-app.zip`の2 fileは、公開b8 Release assetのprovider bytes／SHA-256と一致。詳細は`materials/b8-published-file-verification.json`
- 今回変更したもの: 本close packetとローカル`NOTES_ja.md`。既存素材の中身は変更していない。削除・service停止・source／tag／Release／registry変更なし
- 未完了: ①のknowledge正式収容とcoordinatorの全文移管確認、②の明記した使用終了／引継ぎ条件。b9の公開作業の残りではない。③は分類済みで、今回削除していない

分類（file数は調査時点。複数分類のdirectoryはfile集合を明確に分ける）:

| directory | 分類 | file数 | 理由 |
| --- | --- | --- | --- |
| `2026-10-04-b9-scratch-confirmation` | ① | ①:9 | 当時の移管評価と契約監査・確認票を残す |
| `2026-10-05-b9-tooling-migration` | ①・③ | ①:43 / ③:2 | 移管前後の照合とfixture発行・consumer pin・CIの観測を残す |
| `2026-10-05-b9-release` | ①・③ | ①:67 / ③:12 | 公開前の停止・packaging差の原因・承認後のactual OCI照合と公開操作を残す |
| `2026-10-05-b9-scratch-dev` | ①・②・③ | ①:4 / ②:1762 / ③:23 | 収容済み18 fileは③、未収容4 PNGは①、現行配信runtime/privateは② |
| `2026-09-30-block-picker-names` | ① | ①:8 | b8の名前表示・検索の初期ブラウザ観測と局所決定搬送素材 |
| `2026-10-01-b8-fixture-preflight` | ③ | ③:1 | b8凍結時の正式一覧とb9移管時の全13件照合で役目を終えた |
| `2026-10-01-b8-local-playtest` | ①・② | ①:6 / ②:7 | ローカル試運転の画像・UI観測は①、現行8601系の起動設定等は② |
| `2026-10-02-home-scratch-contract-reply` | ② | ②:2 | Stack問い合わせの回答はStack担当への引継ぎ・受領確認待ち |
| `2026-10-02-stack-wss-reply` | ② | ②:4 | StackのWSS 401検査修正の回答・再現を引き継ぐ |
| `2026-10-03-wirescope-column-width` | ①・③ | ①:14 / ③:6 | b9へ採用・移管済み。人間承認の元画像と観測は①、旧preview/buildは③ |
| `2026-10-01-b8-candidate-b7-fixes` | ③ | ③:4 | 旧candidateのみ。検証本文はb8 evidenceへ移管済みで、b8/b9公開物へ置換済み |
| `2026-10-02-b8-candidate-local-fixes` | ③ | ③:4 | 旧candidateのみ。検証本文はb8 evidenceへ移管済みで、b8/b9公開物へ置換済み |
| `2026-10-03-b8-publication` | ③ | ③:2 | 残っている2 assetは公開b8 Releaseと同じ内容 |
| `2026-10-03-b8-scratch-live-gate` | ② | ②:1768 | 残るruntime/privateは手元b9配信の戻し先とprivate opsの引継ぎ |
| `2026-10-03-b8-scratch-live-human` | ② | ②:10 | 残るprivate原画像はbackstageへ移す対象。sanitizeした正式evidenceは収容済み |
| `2026-10-05-b9-close` | ① | 本packetのINVENTORY参照 | 分類票と収容照合の結果。本gate closeへの返却素材 |

①のfile一覧と収容先案:

- `materials/EVIDENCE_FILES.tsv`に全151 fileの元directory・相対path・bytes・SHA-256・収容先案を記載。`materials/classification.json`にはdirectoryごとの集計と③の全候補pathを記載
- b9初回確認: `14-evidence/artifacts/2026-10-05-b9-tooling-migration/scratch/initial-confirmation/`
- b9移管／consumer: `14-evidence/artifacts/2026-10-05-b9-tooling-migration/scratch/`
- b9公開・OCI比較: `14-evidence/artifacts/2026-10-05-b9-release/scratch/`。テキスト・比較JSON・操作metadata・監査scriptを①とし、大archiveと公開assetの複製は③候補。公開されたactual OCIとの比較結果を含む
- b9実機未収容の画像4枚: `14-evidence/artifacts/2026-10-05-b9-dev-live/scratch/segment-3/materials/`。`picker-door.png`、`picker-gold.png`、`wirescope-b9-columns.png`、`wirescope-b9.png`。日英検索・人間が確認した列幅の元画像を残す。WireScope画像のtoken省略、private address／player UUIDが出ていないことを目視確認
- b8 pickerの初期観測、ローカル試運転、列幅の元観測: `14-evidence/artifacts/2026-10-03-b8-dev-live/scratch/<元directory>/`
- 本close packet: `14-evidence/artifacts/2026-10-05-b9-release/scratch/close/`。本packetのfile一覧・bytes・SHA-256は同directoryの`INVENTORY.json`／`SHA256SUMS`へ記載（inventory自身と再生成cacheを除く）
- 正式authoring・配置・record／INDEXはknowledge担当。①の元はcoordinatorが全文収容を確認するまで消さない。絶対home pathを含む旧script／logは収容時に`~`への置換可、原fileのhashと変換を区別して記録してほしい

②の使い道と終了条件:

| 保持対象 | 引継ぎ先／用途 | 捨ててよくなる条件 |
| --- | --- | --- |
| b9 scratch-devの`runtime/` | Scratch手元配信担当。現在8611／8612／4183が稼働、rc1への切替前のb9を使う | human ownerがこの配信の終了・置換を指示し、serviceのfile参照が終わり、後続の起動入力を確保した後 |
| b9 scratch-devの`private/` | 同配信の起動設定・PIDとprivate ops。公開evidenceへ出さない。恒久的なprivate保管が必要な分はbackstageへ引継ぎ | 配信終了に加え、必要なprivate opsのbackstage受領・不要分の失効を確認した後 |
| b8 scratch-live-gateの`runtime/`／`private/` | Scratch手元担当。b9 startupの`previous_b8_startup`が指す戻し先／起動設定。現時点ではb8 supervisor自体は停止 | human ownerがb8 rollback入力を不要とし、後続起動経路の参照が無くなり、必要なprivate opsを引き継いだ後 |
| b8 scratch-live-humanの`private/` | 参加者情報を含む原画像等。backstage担当への引継ぎ対象 | backstageでの受領または不要・削除の判断を確認した後。公開evidenceへは含めない |
| b8 local-playtestのrootの起動／設定／probeとserver log | Scratch手元担当。8601／8602／4173もlistenerがあり、開発配信の起動・運用素材を保持 | human ownerが旧開発配信を終了・置換し、起動fileの参照終了と必要な運用logの引継ぎ／失効を確認した後 |
| home-scratch-contract-replyの全文 | Stackのホーム統合担当。`main@68832e0…`起点の回答受領・仕様の着地確認 | Stack担当の受領と、必要な結論が正式な参照先へ着地したことを確認した後 |
| stack-wss-replyの全文 | StackのWSS検査担当。`agent/home-runtime-permissions@19c8afa…`起点の回答・再現 | 検査修正／後続への正式引継ぎと、回答・probeが不要になったことを確認した後 |
| 比較helper branch／worktree（handoff外） | b9 close担当。照合再現と収容漏れを補う参照。公開sourceへは統合しない | 本close・公開比較script／workflowの正式収容確認後、GitHubのrunが参照するcommitを保持したうえで不要なworktree等を整理する |

③の根拠と処理条件:

- b9 scratch-devの18 fileは指定knowledgeへ全文一致で収容済みなので、元を③として扱える。private／runtime／未収容PNGは対象外
- b9 scratch-devの`artifacts/`は凍結candidateからの配信入力の複製。実稼働は展開済みruntimeを参照するためarchiveコピーの役目は終了。公開source・公開asset／OCIとidentity記録が存在する
- b9 tooling-migrationの巨大candidate ZIP、b9 releaseの巨大公開前build ZIP／比較ZIP／Release asset複製は照合済みの一時入力。①の比較結果・script・metadataの正式収容を確認してから処理する。Archiveごと丸ごとの恒久evidence保存は提案しない
- b8 fixture-preflightはb8正式fixture一覧とb9新ownerの13 fixture照合へ置き換わった。先行票の再利用は終了
- b8列幅のpreview-app／旧ZIP／commit-messageは、b9で採用・公開・人間確認まで済んだ。元画像・測定・patch等は①で収容するまで保持。01cdb0bの列幅をb9へ残すという後続用途は終了
- b8の2旧candidate directoryは再現用の正本ではなく旧試行成果物。b8に収容済みの検証本文と公開source／成果物があり、b9のための保持は終了。b8 publicationの2 assetは公開Releaseから再取得でき、bytes／SHA-256一致を今回確認した
- `__pycache__`等の再生成cacheは③。今回削除していない。③集合と①集合は重ならない

セッションクローズ票:

- repo / surface: scratch-editor／b9 gate close
- branch/commit: agent/b9-tooling／7fbbf034488760d8fc7e034bf23f3e08e6e1807d
- 今回やったこと: 収容済み18 fileの実体照合、未収容素材・稼働入力・旧candidateの分類、①のbytes／SHA一覧確定
- 変更ファイル: ignoredの本close packetとNOTESのみ
- 検証: 18 file byte一致、b8公開2 asset一致、private／runtimeの①除外、classificationの集合分離、user未追跡fileとtracked/indexの状態確認
- 未完了／次の一手: knowledge担当の正式収容確認と、②の用途終了条件に従う後続処理。正式evidenceへ未着地の搬送物は本票の①一覧
- NOTES/DECISIONS: NOTESへ本票と保持・終了条件を記録。新しい横断決定の採番なし
- 注意点: 稼働serviceとprivateは処理していない。default branch統合の再実施・他repo操作・shared環境変更なし
