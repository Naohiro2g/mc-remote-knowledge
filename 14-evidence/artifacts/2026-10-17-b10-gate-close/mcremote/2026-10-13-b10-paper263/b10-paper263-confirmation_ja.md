## Release gate 確認票

- 対象 repo：McRemote。
- 対象 branch/commit：`main@17bcf2645c112133935bc9d993d4fdd4669ceb98`（commit／push済み。CI headとsource stampを照合）。
- release / channel：`2320.0.0b10`／beta。planned tag `v2320.0.0b10`。公開pre-releaseの作成は別指示待ち。
- gate coordinator：knowledge担当session。
- human release owner：human owner。
- current phase：26.3切替の静的点検・candidate生成・両版のpulse完了。componentの事実返却。横断判定は行わない。
- contract maturity / required test tier：b9でwire freeze。今回のchange coneは対応版宣言／配布config／README Java案内。静的点検、既存unit/deterministic、同一JARのlive-auto compatibility pulseと通常再起動。
- knowledge contract path：`00-hub/DECISIONS_ja.md` `2026-10-13-07`／`2026-10-12-02`／`2026-10-07-06`／`2026-10-07-07`、`00-hub/release-gate-notes_ja.md` b10、`10-protocol/versioning-design_ja.md` §7.1／§10.12、`11-plugin/platform-design_ja.md`、`00-hub/release-operations-responsibility-design_ja.md`。
- knowledge contract commit：`c29bb1d1b81e42d2676791100b90a8e6f1742d8e`（remote mainから取得して読んだSHA）。
- gate manifest identity：今回の横断exact setは未提示。旧candidate `56af938`と26.2の試験を新candidateの根拠に使わない。
- change cone：build前の対応版宣言を1.21.11／26.3へ更新、配布configの同じ一覧を生成、宣言の既存testを追従、READMEにサーバーfolderごとのmise／Java案内を追加。実行コード・wire・開発の床は変更なし。
- reused PASS / rationale：両版のpulse・通常再起動とCIは新JARで実行し直した。過去の26.2／旧JARのPASSは引き継がない。toolingの固定schema identityは不変で、4 fileのbytes／SHA-256を再照合した。
- exact compatibility set / freeze status：McRemote対応版の宣言は`["1.21.11", "26.3"]`。下表のexact Paper buildと同じJARで検証。componentの検証identityであり横断freezeではない。
- target deployment / profile / lock：Ubuntuの隔離/tmp Paper環境でauth ON。shared／dev通常環境／公開serverは変更していない。
- authorized next action：依頼票`request-mcremote-26-3.md`の静的点検→コード変更不要なら宣言更新→CI candidate→両版pulse／README→返却を実施。tag／Release／shared deployは別指示待ち。
- test class：unit/deterministic、static inspection、live-auto。live-humanは未実施。
- 実行した command / 手順：下記と`REPRODUCE_ja.md`。
- 結果：静的点検で26.3対応コード変更不要と判断。CI全7 job、local Java 355 tests／release Python 34 tests、SQLite packaging／missing-provider、両版8項目pulse／通常再起動、manifest v2検証PASS。
- evidence record / artifact：本directoryのstatic review／compile log、CI API情報、candidate identity／archive identity、pulse／restart-pulse／lifecycle、版別verification、manifest／tooling-validation等。dev搬送素材であり、正式`14-evidence/` authoringはknowledge担当。rawログ／token／DB／worldは/tmpのローカル限定。
- 未検証の境界：新candidateをGitHub pre-releaseのassetから取得する3 OSの人間参加試験、Windows／macOS上の26.3 Paper起動、実playerのevent callbacks、授業負荷／MSPT、公開world migration。CIの3 OS credential試験とLinux Paper pulseをこれらのPASSとして扱わない。
- security / compatibility / rollback の確認：auth ON／Paper SQLite3.49.1提供元・HEALTHY、通常停止exit0、同じdomain／sessionでrestart接続、旧config値保存／warning／helloの同梱宣言を確認。org/sqlite同梱0件、全製品classはJava21 major65。通常環境／公開worldの変更なし。
- 判定を求める事項：この新candidate／manifestと対応版一覧の採用、旧26.2 candidateとのexact set差替え、pre-release公開と3 OS実施票の後続指示。repo側で横断GREENや公開許可を確定しない。

### 1. 静的点検の先行返却

[static-review_ja.md](static-review_ja.md)のとおり、Paper 26.3 STABLE build 178から展開したAPIと依存libraryに対し、既存Gradleで全main sourceをcompileした。Java25 compiler／`--release 21`、一時init script、/tmp出力でPASS。製品コードは変更不要と判断し、依頼票の2へ進んだ。

NMS／CraftBukkitへの直接依存なし。DimensionKey、registry、block／sign、entity、event、schedulerの公開APIでcompileが通る。`ParticleBuilder.extra(double)`と`Sound.getKey()`には削除予定の非推奨警告があるが、今回のコード変更は不要。将来版の削除への対応は今回のPASSで保証しない。

開発の床は`gradle.properties`のJava21／Paper1.21.11を維持。READMEに、Paper26.3はJava25、1.21.11はJava21、server folderごとの`mise use --path mise.toml --pin java@25`（1.21.11は21）と`mise exec --`を追加した。ユーザーの既存README編集／おすすめプラグイン文書はそのまま保持し、今回のcommitへ含めていない。

### 2. CI candidateと対応版宣言

- source commit：`17bcf2645c112133935bc9d993d4fdd4669ceb98`。
- CI：[38347345527](https://github.com/Naohiro2g/McRemote/actions/runs/38347345527)、success。3 OS×Java21／25のcredential-contract 6 jobとbuild-onlyが全てsuccess。
- artifact：`mc-remote-candidate` ID `11789398049`、ZIP 294,247 bytes、SHA-256 `7cc5c31f5d8a395a3a1ff98a762653acd69fdd7a1c82f2f7ee301eec321adc1b`。ダウンロードZIPとprovider digest、全4 file、CI source stampの一致を確認。
- JAR：`mc-remote-2320.0.0b10.jar`、**315,352 bytes**、SHA-256 **`96ddf09f765a77811740d5c62f3787f7a87c8be6cd7247d345f6dfe9e93512a4`**。
- 対応版：**1.21.11、26.3**。tracked `release/minecraft-targets.json`→同梱宣言とconfig配布既定→hello／release title／本文、の同じ一覧。JAR同梱とsource宣言はbytes一致。
- title：`McRemote 2320.0.0b10 (Minecraft 1.21.11, 26.3)`。`release-targets-section_ja.md`と`release-identity.txt`は既存generatorの出力。tag／Releaseの作成はしていない。
- 旧`bed7508603d849d92b37ff38ee6e6bba29b65ff503ec3fb4a12f2298ce07ada1`との差：entry追加／削除0、内容変更は`minecraft-targets.json`と`config.yml`の2件だけ。製品classの内容は不変。

### 3. 同一JARのcompatibility pulseと通常再起動

| 項目 | Paper 1.21.11 | Paper 26.3 |
| --- | --- | --- |
| exact build | 130 | STABLE 178（2026-10-12T20:42:19Z） |
| server JAR SHA-256 | `25eb85bd8415195ce4bc188e1939e0c7cef77fb51d26d4e766407ee922561097` | `5dd0c8fb20a96eb7c98f3c4b1c890e99ef6db56fd689a2cf06975a3471fda757` |
| Java | Ubuntu OpenJDK 21.0.12.1+1-1-24.04.4-Ubuntu | Temurin 25.0.4.1+1-LTS |
| enable／disable、正常停止 | PASS、first／restartともexit0 | PASS、first／restartともexit0 |
| 認証済みhello／宣言／DimensionKey | PASS | PASS |
| registry／resource catalog | PASS | PASS |
| structured block read／write | PASS | PASS |
| 32768個のtick分割／FAST＋flush／上限拒否 | PASS | PASS |
| sign read／write／style | PASS | PASS |
| entity handle／pose／remove | PASS | PASS |
| events.poll surface | PASS | PASS |
| particle／chat | PASS | PASS |
| 通常restart後の同じsession／block read-write | PASS | PASS |
| SQLite提供元／engine／HEALTHY | `sqlite-jdbc-3.49.1.0.jar`／3.49.1／PASS | 同左、PASS |
| 旧config保存／mismatch warning／hello宣言 | PASS | PASS |

両版で上記の同一CI JARを使った。時刻／Java版／buildは実行・APIに基づく。schedulerは32768個の施工とFAST後flushで確認、実player event callbackは未検証。最後は両Paperとも通常停止済み。

試験素材の初回起動前に、runnerがBukkit YAMLの無字下げlistを読めず中断した。runnerの表記対応を直して実施し、製品source／candidateは変更していない。CI artifactの初回展開もローカルsource stampとの同名衝突で中断したため、ZIP全体を再取得しprovider digestと全file／stampを検証した。いずれもPaper／APIのFAILではない。

### 4. hub NOTES 2026-09-28のparkへの答え

**解消済み。閉じてよい。** `McRemote`の起動時に`MinecraftTargets.bundled()`を正とし、`RemoteSession`のhelloはpluginのその一覧を使う。configの`supported_mc_versions`は比較とwarningだけに使い、対応版の正本にはしない。

今回の両serverは、configに旧`[1.21.11, 26.2]`を明示して起動した。その値がfirst／restart後も保存され、warningが出て、helloは`[1.21.11, 26.3]`となることを実際に確認した。`2026-10-07-07`の方針を静的点検とlive-autoで照合している。

### 5. manifest v2

新JAR、同梱宣言と一致するsource宣言、1.21.11／26.3のfresh verification recordを束ねた。`--preflight`を使わず、tooling `5f567f14adaa24603e9dee3c0ec9909d428b7c4b`の固定schema／fixture等4 fileを照合して、既存Pythonとtoolingのsemantics／actual contentsを検査した。全PASS。

- `manifest.json`：1,761 bytes、SHA-256 `508a34b9ea29357105e6fcc124a7ab0c0eba8ec9fa258eee52bb196222856627`。
- 対応版とverificationの集合：1.21.11／26.3、双方PASS。26.2 recordを使っていない。
- `release-manifest-lock.json`：従来の固定identityを維持。

### 返却・捕捉

返却先はknowledge coordinator。分類②、knowledge coordinator／McRemote・Stack後続への参照移管。元の26.2 candidateとその観測は当時の事実として残し、今回のb10対応版の根拠にはしない。正式evidenceへの昇格または参照移管を確認したらローカルNOTES／本packetを閉じる。
