# McRemote 2321.1 — Paper 26.3 #244 自動確認の返却

依頼されたlive-autoはすべてPASS。凍結したMcRemoteのJARを作り直さず、Paper 26.3 #244とTemurin 25.0.5+8で実行した。
通常8 groups、正常再起動後4 groups、両回のlifecycleと`toggle_on_swap`の欠落時補完を確認した。看板の読み書きもPASS。
横断gateの最終判定と人間の試験はcoordinator／human ownerが行う。

## Release gate 確認票

- 対象 repo: `Naohiro2g/McRemote`
- 対象 branch/commit: `feat/coordinate-time-hud@5b78ded96d1ad6d45160b67c5f8a13e14adb3fc8`
- release / channel: `2321.1.0`、stable候補
- exact set: `2321.1-set-1`
- gate coordinator: knowledge担当session（Claude Code）
- human release owner: プロジェクトオーナー
- current phase: McRemoteの26.3 #244での自動確認が完了。coordinatorへの返却。人間の試験の前
- knowledge contract path: `00-hub/release-gate-notes_ja.md`「2026-11-06 2321.1横断release gate」の「凍結するexact set」
- knowledge contract commit: `f40b003eda9ec560b0c6b4656b12bfa902746d39`（実読）
- リモート反映確認: 実行前にGitHub APIでknowledge mainと指定commitの実在を確認。runtimeは前回実読時と同じ。
  INDEXとgateの当該節を読んだ。McRemoteのremote branch先頭も上の凍結commitと一致
- reused PASS / rationale: 1.21.11 #132の自動確認とJava 21／25のunitはgate notesの採用済み結果を利用。
  今回の26.3の結果は、下記の凍結JARと#244で新たに実行した観測。#231の結果のidentityは書き換えていない
- target deployment / profile / lock: 新しい隔離ローカルruntime、平坦な新規world、合成credential、`auth.enforcement=true`、LuckPermsなし。
  Minecraftはloopbackで待ち受け、API試験もloopbackへ接続した。McRemoteのAPI待受は製品実装どおりwildcard。
  shared環境／公開VPSは変更していない
- authorized next action: 依頼された自動確認の結果を返す。shared deploy、人間の試験、公開はcoordinatorの進行待ち
- 実装・文書の変更: 製品source、tracked scripts、候補commit、JAR、tag、Releaseは変更していない。
  このローカル搬送packetとrootのローカルNOTESだけを作成／更新

## 使った実物の照合

| 対象 | bytes | SHA-256 |
| --- | ---: | --- |
| `mc-remote-2321.1.0.jar` | 340,193 | `cd1fff723b2b8349f45184b940cd5da1ca3cdcacc9bad988fa71cd00ea960112` |
| `paper-26.3-244.jar` | 55,279,049 | `9601f9a26a2a52a0f2c807cf1abf691f96ee4fb287878313b601cebc2c51eabf` |

- McRemoteは既存の`2026-11-07-23211-hud-status-lowercase/materials/mc-remote-2321.1.0.jar`を使用。
  開始前と終了後に凍結値を照合し、runtimeに配置したcopyも一致
- Paperは[公式API](https://fill.papermc.io/v3/projects/paper/versions/26.3/builds/244)で照合して公式URLから取得。
  メタデータを[paper-build.json](paper-build.json)に保存。両回の起動logでも`26.3-244-main@35a2d15`を確認
- JavaはEclipse Adoptium、`Temurin-25.0.5+8`、`25.0.5+8-LTS`。`release`ファイルと`java -version`、起動logで照合
- 起動のflagは前回と同じ`-Xms256M -Xmx1536M -XX:ActiveProcessorCount=2`、`nogui`。新しいGCのflagは追加していない
- 実物のidentityは[runtime-identity.json](runtime-identity.json)。JARの再buildやGradle testの再実行はしていない。
  合成credentialは既存の`LocalCompatibilityFixture`を凍結JARとPaperのSQLite依存で動かして新規発行した

## groupごとの結果

| 通常のgroup | 結果 | 主な確認内容 |
| --- | --- | --- |
| `authenticated_hello_and_bundled_targets` | PASS | 認証付きhello、MC版、同梱の対応版宣言、権限、建築原点 |
| `resource_catalog` | PASS | catalogの取得とhelloのcatalogHash |
| `structured_block_read_write` | PASS | BlockSpec／BlockValueの読み書き、state、既定値、入力エラー |
| `bulk_32768_scheduler_and_notification_flush` | PASS | 32,768ブロックの編集、notification後のflushと読み取り、上限超過の拒否 |
| `sign_read_write_style` | PASS | 看板の表裏、文字列とstyle、色・装飾、1行更新、入力エラー |
| `entity_handle_pose_remove` | PASS | entity生成、handle、pose、削除 |
| `event_poll_surface` | PASS | events.pollの応答 |
| `particle_and_chat` | PASS | particle生成とchat.post |

正常再起動後は`authenticated_hello_and_bundled_targets`、`resource_catalog`、`structured_block_read_write`、
`ordinary_restart_authenticated_read_write`の4 groupsがPASS。同じ合成credentialで再認証して読み書きした。

| lifecycle等 | 初回 | 再起動後 |
| --- | --- | --- |
| McRemote有効化／credential domain HEALTHY／Paper ready | PASS | PASS |
| token無しhelloを`auth_required`で拒否 | PASS | PASS |
| 23.2.0のhelloを受け、23.2.1／26.3を返す | PASS | 対象外 |
| consoleのHUD commandがplayer専用guardへ到達 | PASS | PASS |
| `hud.toggle_on_swap`を省いてから起動し、`true`の補完を確認 | PASS | PASS |
| McRemote無効化／正常終了 | PASS（exit 0） | PASS（exit 0） |
| Paper logのERROR／FATAL | 0件 | 0件 |

WARNは意図した不正入力・認証拒否と、隔離環境のMinecraft offline-mode／非対話terminalの通知。
McRemoteの認証は両回とも有効。終了後に試験用のMinecraft／APIポートが解放されたことを確認した。

## 看板の確認範囲

通常pulseが既存の`sign_live_auto.py`を呼ぶ。3 methodあわせて31 callで、成功17、意図したエラー14。

- `world.setSign`：表裏を独立して書き込み。文字列／objectの混在、4行の形、named色とhex色、5種類の装飾を確認
- `world.getSign`：書いた文字とstyleの往復、既定の行の形、表裏の独立性を確認
- `world.updateSignLine`：指定した面の指定した1行だけを変更し、残る行と反対面を維持することを確認
- 看板以外のblock、不正な色・装飾、行数、face、line index等のエラーも期待どおり

## #231との差

- 通常8 groups／再起動後4 groupsの名前とPASS結果は同じ。追加の失敗は無い
- catalogの応答の要約SHA-256は両回とも#231と一致：
  `7c758470e450aa2353e6d8bbbccf8272088ff96ef24d7682b5f12850032f6513`
- Javaは前回と同じ。Paperだけ#231から#244へ更新し、McRemoteは旧観測の`db7f7db`から凍結候補`5b78ded`へ。
  旧JARとの製品差分が状態の文字列だけであることはgate notesで照合済み。今回は新しいJARで実際に確認した
- 欠落キーの補完は、初回だけでなく再起動直前にも明示的にキーを省いて観測した
- 比較の機械可読記録：[comparison-with-231.json](comparison-with-231.json)。旧結果の原本は保持したまま

## 記録と未検証の境界

- 統合した観測：[mc-remote-verification-26.3.json](mc-remote-verification-26.3.json)
- groupとsanitized transcript：[pulse-26.3.json](pulse-26.3.json)、[restart-pulse-26.3.json](restart-pulse-26.3.json)
- lifecycle：[lifecycle-26.3.json](lifecycle-26.3.json)、認証拒否／旧hello：[old-client-hello-26.3.json](old-client-hello-26.3.json)、
  [auth-guard-26.3-full.json](auth-guard-26.3-full.json)、[auth-guard-26.3-restart.json](auth-guard-26.3-restart.json)
- 実行log：[runtime-pulse.log](validation/runtime-pulse.log)、sanitized起動終了log：
  [初回](validation/paper-26.3-full.log)、[再起動](validation/paper-26.3-restart.log)
- 再現のrecipe：[prepare-runtime.py](prepare-runtime.py)、[run-runtime-pulse.py](run-runtime-pulse.py)。
  既存test scriptsのidentityは[script-identities.json](script-identities.json)
- 未検証：HUDの実画面・物理キー、看板の画面上の色と蜂蜜でwaxした看板、player callback、LuckPermsとの統合、
  Windows／macOSでの実行、負荷／MSPT／長時間運転、公開VPS／実worldの更新。これらの合格へ読み替えない
- 1.21.11とunitの再実行は依頼の範囲外で、採用済み結果を保持

このpacketは正式な14-evidenceではなく、knowledgeへの搬送素材。分類②としてMcRemote担当が保持する。
knowledgeによる必要な観測の収容・照合、gateの返却／公開／close分類と必要な移管が済み、参照用途が終われば整理できる。
raw runtimeと合成credentialはローカル限定で、公開素材へ含めない。候補のJARは元packetで保持する。
