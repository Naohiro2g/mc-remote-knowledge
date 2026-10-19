# McRemote rc1 gate確認票への追記 — candidate返却

2026-10-18のfixture受領前の票から変わった項目を返す。

## Release gate 確認票（差分）

- 対象 repo: `Naohiro2g/McRemote`
- 対象 branch/commit: `agent/rc1-pre-fixture@192a777ae1d484bcc9b58fcc7c58d6aed1a374af`。push済みのsourceをCI runの`head_sha`と照合。mainへの統合は未実施。
- release / channel: protocol `23.2.1`、artifact `2321.0.0rc1`、GitHub pre-release予定。tag／Releaseは未作成。
- gate coordinator: knowledge担当session（Claude Code）。human release owner: プロジェクトオーナー。
- current phase: rc1 gate OPEN、component candidateの検証結果返却。横断判定は未実施。
- knowledge contract path: `00-hub/rc1-gate-work-instructions_ja.md`、`00-hub/release-gate-notes_ja.md`、`00-hub/INDEX_ja.md`、`11-plugin/platform-design_ja.md`。版・wireの契約は前票で読んだ`10-protocol/versioning-design_ja.md` §8と`10-protocol/wire-format-design_ja.md`に従う。
- knowledge contract commit: 最新runtime／上記文書の実読は`277fa69c56b8e16b8cbcc3d54ee3cccb639feb03`。依頼指定`d0be94624659e82d5f91bac6eba48063cc1c3c7b`で前回取得した着手依頼本文とbytes同一を確認。
- gate manifest identity: component candidateは下表。横断exact setは未凍結。CI run [39065266196](https://github.com/Naohiro2g/McRemote/actions/runs/39065266196)は全7 jobs success。candidate artifact ID `12112853171`、ZIP 294,255 bytes、provider SHA-256 `ef4bf641ac4c229a6c1ca413c0698dd4350559bdcb5f643e72cdf807b53686be`。取得ZIPの実digest、source stamp、同梱宣言を照合した。
- change cone: `192a777`でtoolingの23.2.1 fixtureを新fileとして2件取り込み、契約testのsource／digest／schema／版／件数を更新。旧`*-v23.2.json`のraw bytesは変更していない。前commit`f6f2f4c`の版／README／23.2.0互換testと合わせてcandidateとした。新fixtureは旧fixtureから`schema`と`protocol`だけが変わり、case内容は不変。
- reused PASS / rationale: この候補ではb10のpulseを継承せず、同じCI JARで両版の通常pulse・通常再起動を新規実行した。
- exact compatibility set / freeze status: `release/minecraft-targets.json`は`["1.21.11", "26.3"]`。供試Paperは1.21.11 #132（Java 21.0.2）と26.3 #203（Java 25.0.2）。他componentとのexact setはcoordinatorの凍結待ち。
- target deployment / profile / lock: `/tmp`の隔離ローカルPaper。ゲーム接続はloopback、通常環境・公開worldのcopyは使わず新規flat world。認証ON、試験専用credentialは既存`localCompatibilityFixture`で実CredentialServiceから発行。LuckPermsなしのfallback permissionsで実行。
- authorized next action: candidateとcomponent結果をcoordinatorへ返す。通常dev環境・shared deploy・3 OS live-human・tag／releaseは凍結後の別票に従う。
- test class: unit/deterministic、および隔離Paperのlive-auto。
- 実行した command / 手順: `./gradlew build sqlitePackagingProbe sqliteMissingProviderProbe --offline`、`python3 -m unittest discover -s scripts -p 'test_*release*.py'`、CI `ci.yml`のworkflow_dispatch。固定CI JARを取得後、`run-pulse.py`から既存`compatibility_pulse.py`、`--restart-only`、`prepare_minecraft_verification.py`を実行。`create_release_manifest.py --schema-version 2`で固定Schema検査を通した（`--preflight`不使用）。
- 結果: local Java 355 tests PASS、release Python 38 tests PASS、CI全7 jobs success（3 OS × Java 21/25 credential contractsとbuild）。両Paperで通常pulse 8 groups、通常再起動pulse 4 groups PASS。4回とも正常enable／HEALTHY／認証ON／disable／exit 0。同じcredentialで再起動後も認証できた。通常pulseと別の素材で、23.2.0の認証付きhelloを受け入れ、23.2.1を広告し、MC版と同梱対応版宣言が一致することを両版で確認。
- evidence record / artifact: このpacketはdev搬送素材。`pulse-*.json`、`restart-pulse-*.json`、`lifecycle-*.json`、`legacy-hello-*.json`、版別verification、`manifest.json`、`candidate-identity.json`、`fixture-identity.json`、`sqlite-provider-observations.json`。正式record／artifactの配置はknowledge担当。命名案: `14-evidence/records/2026-10-18-rc1-mcremote-candidate_ja.md`、`14-evidence/artifacts/2026-10-18-rc1-mcremote-candidate/`。
- 未検証の境界: 実Python b9／Scratch b10の配布物からの接続、実playerのevent callback、描画・音・看板の人間確認、授業規模の負荷、Windows／macOSでの実Paper起動、rc1→b10の実rollback、通常dev／shared環境、Pass C。旧版helloの結果はMcRemoteのwire受容を示し、client全体の検証ではない。
- security / compatibility / rollback の確認: 製品のconfig、SQLite schema、credential形式、API／wire内容は未変更。認証なしhelloが`auth_required`になることを各起動で確認。SQLiteの既存probeは「McRemote JARのSQLite同梱entryが0、Paper相当JDBCで動作」「JDBCを検査classpathから外すと認証backendがfail closed」を検査する。新しい同梱やbackend変更ではない。実Paper 2版とも提供元`sqlite-jdbc-3.49.1.0.jar`、JDBC 3.49.1.0／engine 3.49.1を観測。
- 判定を求める事項: candidate identityと2版のcomponent結果を横断exact setへ採用するか。shared deployや人間試験の開始はこの票で求めない。

## candidateのidentity

| file | bytes | SHA-256 |
| --- | ---: | --- |
| `mc-remote-2321.0.0rc1.jar` | 315,352 | `917c358c201aa219277b96a447fb85116e8bdb0260870a4d76a8c51219d31c37` |
| `minecraft-targets.json` | 126 | `8e830732decd6bcde13f91eb6c071d062ba6993342a7edb52e6ea543b9e0c361` |
| `manifest.json` | 1,988 | `e49761d22c8c60ac49915d04f1c6236ca101b13bf94b257c0cbcbb4328c6a1c2` |
| `mc-remote-verification-1.21.11.json` | 62,784 | `b3ae515b037429517ce1f90bc1708d3feeebef4bc9bd359fcf175a5e0a221f49` |
| `mc-remote-verification-26.3.json` | 62,766 | `82b62c167bc11b13128f06724b0f66051509ba192d5e302b50d92625a54d0c66` |

## tooling fixtureの照合

source `Naohiro2g/minecraft-remote-tooling@6447f6e8cbfbeeb9d229990b5c4f6e82a5875666`、CI run `39053886890` success、artifact ID `12109060950`、provider digest `5b644de44ae2f9a2fb9de09d221c2930218f6c317baffee3b5c7f817309555fa`をAPIで照合。fixture本体は同commitのContents APIから取得し、実bytes／SHAを照合した。toolingの114 MB artifact ZIP全体は取得していない。

| fixture | bytes | SHA-256 | inventory |
| --- | ---: | --- | --- |
| `chat-event-compat-v23.2.1.json` | 32,384 | `eead244a7340c315cb63e1e77ede0fe9cf48162c06fedbeef36d941950d5000d` | chat 7、event batches 22、stateful rejection 4 |
| `entity-particle-v23.2.1.json` | 36,483 | `0319ff8373a96798cf5e9e421a804729fd33a0fa53e96adc12c93ed7994777ae` | nearby 19、handle transaction 7、lifecycle 7、particle 26、sound 37、resource ID 15 |

## Paper buildの選定

- 1.21.11 #132: server JAR SHA-256 `5ffef465eeeb5f2a3c23a24419d97c51afd7dbb4923ff42df9a3f58bba1ccfba`。
- 26.3 #203: server JAR SHA-256 `0fcb63f341abe5d8370d354bb2e39d47c917d8010c817f4567f89e97b5c3ecf9`。
- 最初の#200案はpulse前にhuman ownerが#203まで進んだことを指摘したため、#203へ更新した。[Paper公式コード差分](https://github.com/PaperMC/Paper/compare/09ee222482646f8ed84413aea89d0108653af938...1b443e0ac8193f8f90e10c117802a325e64d251b)は3 commits／6 files。ArmorStandの非tick時の死亡処理修正、Entityのalliance API追加、anti-xrayのpalette preset値の明示的追加。public APIからの削除はなく、今回のpulseを#203で実施した。
- 両server JARは公式Downloads Serviceの固定build metadataのsize／SHAと照合。metadataのcopyを同梱。今後新buildが出た場合は差分と不具合情報で再試験要否をcoordinatorへ返す。この票の観測は上記exact buildに固定する。
