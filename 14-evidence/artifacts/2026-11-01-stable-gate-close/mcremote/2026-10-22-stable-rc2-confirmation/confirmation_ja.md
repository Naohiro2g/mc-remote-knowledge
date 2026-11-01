## Release gate 確認票

- 対象 repo: `Naohiro2g/McRemote`
- 対象 branch/commit: `agent/stable-rc2-legacy-config@7960a913a11c621d85e6120ee412b696fe125457`（push済み）
- release / channel: 候補 `2321.0.0rc2`／GitHub pre-release、後続 `2321.0.0`／stable・Latest
- gate coordinator: knowledge担当session（Claude Code）
- human release owner: プロジェクトオーナー
- current phase: OPEN。McRemoteは実装と今回の局所検証を完了、rc2のtag／Release公開はcoordinatorの着手待ち
- contract maturity / required test tier: protocol `23.2.1`、API／wireは既存の凍結範囲。今回はunit/deterministicと隔離live-auto。後続の人間参加試験はcoordinatorが進行
- knowledge contract path: `00-hub/stable-gate-confirmation-instructions_ja.md`（共通・McRemote）、`00-hub/release-gate-notes_ja.md`（2026-10-22の節・確認票形式）、`00-hub/DECISIONS_ja.md`（2026-10-22-01〜03）、`10-protocol/beta-to-stable-release-roadmap_ja.md` §5、`10-protocol/versioning-design_ja.md`、`11-plugin/platform-design_ja.md`
- knowledge contract commit: `61d5fd8df66ca49a5429fe010a131eab58f702ba`（remote mainからruntimeを取得し、上記を同refで実読）
- gate manifest identity: 未提示。上記knowledgeのstable gate節を参照
- change cone: rc1から旧`b5.`／`b7.`キーの移行・読み替えを除去。残存時のERRORとPaper全体停止、対応するtest・設定comment・README、版`2321.0.0rc2`。protocol・API・wire・fixture・対応Minecraft宣言は変更なし
- reused PASS / rationale: 今回のMcRemote候補に必要なunitと両Minecraft版のpulseは新規実行。rc1の他component・3 OS人間試験の再利用はgateの方針に従い、McRemoteが独自に横断確定しない
- exact compatibility set / freeze status: McRemote候補identityは下記。rc1の組合せをこの候補の凍結済みsetとは扱わない。横断exact set／freezeはcoordinatorへ返す
- target deployment / profile / lock: 本票では隔離ローカルPaperのみ。shared／箱庭のprofile・lock・実configは未操作。箱庭の旧キー点検はStackの節の作業
- authorized next action: 許可されたrc2実装・検証の結果を返却。coordinatorからrc2のtag／Release公開の着手を受ける
- test class: unit/deterministic、live-auto。live-humanは未実施
- 実行した command / 手順: `./gradlew test --tests club.code2create.mcremote.LegacyConfigKeysTest --tests club.code2create.mcremote.RuntimePolicyTest --tests club.code2create.mcremote.LightningRuntimePolicyTest`、`./gradlew clean build --console=plain`、CI `ci.yml`のbranch dispatch、既存`localCompatibilityFixture`、packet内`run-rc2-validation.py`から既存`compatibility_pulse.py`と`prepare_minecraft_verification.py`を実行
- 結果: clean build 357 tests PASS。CI全7 jobs成功（Windows／macOS／Linux × Java 21／25のcredential contractsとbuild）。同一CI JARで両Minecraft版の通常8 groups・再起動4 groups・rc1移行済み設定4 groups、旧キーによるPaper全体停止・ERROR案内・config／credential DB不変をPASS
- evidence record / artifact: ローカル素材は本packetの`materials/`、`inventory.json`を参照。CI https://github.com/Naohiro2g/McRemote/actions/runs/39699287525 。正式record／artifactはknowledge未着地（候補 `14-evidence/records/2026-10-22-mcremote-rc2-candidate_ja.md`）
- 未検証の境界: shared／箱庭、Python・Scratchからの人間参加試験、rc2の公開assetからの取得、stableの番号に変更した候補、26.3 #203より後のbuild。今回のlocal pulseはLuckPerms未導入のfallback権限で行い、実環境のLuckPerms設定を検証した主張はしない
- security / compatibility / rollback の確認: 旧キー検出はdefault追記、credential初期化、socket公開より前。拒否時はconfigとcredential DBを変更しない。認証ONと通常再起動後の同一tokenを確認。DB schema／wire変更なし。READMEの更新手順にJAR・config・worldの退避、旧キーの直し方、前版のJARと対応configによる戻し方を記載
- 判定を求める事項: 下記のrc2候補の採用とtag／pre-release公開への着手。横断GREEN／HOLD／REDやhuman ownerの合格判定は本票では行わない

## 共通の返却

### rc1のtag以降とsourceの選び方

着手時のremote mainとlocal mainはともに`192a777ae1d484bcc9b58fcc7c58d6aed1a374af`。annotated tag `v2321.0.0rc1`の解決先もGitHub APIで同SHAと照合した。rc1のtag後にdefault branchへ入ったcommitは無い。
rc1と同じmainから作業branchを切り、今回のcommitを1件だけ追加した。stableは、このrc2の検証・合格後に同sourceから版番号だけを変更する案。対象外の改善は加えていない。

### stableへ版番号だけを変える箇所と見積もり

- `gradle.properties`の`pluginVersion`を`2321.0.0`へ変更する。`plugin.yml`とJAR名は既存Gradleから生成される。
- `ProtocolInfo.PROTOCOL=23.2.1`、対応Minecraft `1.21.11`／`26.3`、既存fixtureは維持する。
- tag／Releaseは`v2321.0.0`、JAR名は`mc-remote-2321.0.0.jar`。title、manifestは既存scriptから生成し、新候補のcommit／digestで検証recordを用意する。
- READMEの旧設定の案内は今回追加済み。stableの番号だけの変更で新たな全面改稿は不要。Release本文は旧キー停止の注意を継承し、rc2の表記をstableへ更新する。
- 版変更・clean build・候補照合・本文案は半日以内の見込み。公開と人間参加試験の待ち時間は含めない。10/29–30の候補作成、10/31凍結の予定に対応可能。

### 公開操作の違い

rc2はtag CIのcandidateを再buildせず昇格し、GitHub pre-release、Latest対象外。stableはpre-releaseの印を外し、Latestを明示して公開する。現LatestはAPI確認時点で`v1.21.8-1.4.0`。tag CI成功、対象別検証record、既存Release workflowによるmanifest生成・candidate昇格、公開assetの凍結値との照合という経路は同じ。
McRemoteの既存workflowにはregistryへの公開処理は無い。rc2のtagとReleaseはまだ作成していない。

### 日程と止まっている点

10/22時点でrc2の実装・CI・両版の今回の検証は完了。11/1目標への実装上の阻害要因は見つかっていない。次はcoordinatorの公開着手、その後の公開物照合と人間参加試験。rc2で問題が出ればgateの11/7予備日へ戻す。
`2321.1.0`の改善、サウンド拡張、対応Minecraft系列の拡張、Pass Cの代替ガイド整備は今回に含めない。

## McRemoteの返却

### Paperの止め方とログ

`McRemote.onEnable()`で旧キーを検出したら`Server.shutdown()`を呼び、直ちに初期化をreturnする。pluginだけを無効化する経路ではなく、両版のPaper processが終了コード0で終了したことを確認した。
ログは次の形で、旧キーごとに新しい名前と旧キーを消すことを案内する。実際のログでは先頭の3行は`[McRemote]`付きのERRORとなる。

```text
Unsupported legacy keys in plugins/McRemote/config.yml. Stopping the entire Paper server.
config.yml: unsupported legacy key 'b5.entity_handle_capacity'. Use 'entities.handle_capacity' instead, then remove 'b5.entity_handle_capacity'.
config.yml: unsupported legacy key 'b7.lightning.global_per_tick'. Use 'lightning.global_per_tick' instead, then remove 'b7.lightning.global_per_tick'.
Keep the intended values under the new keys, remove the b5: and b7: sections, then restart Paper. No config values have been migrated or saved.
Stopping server
```

空の旧セクション・未知の旧項目も検出し、旧項目の値はログへ出さない。新しい項目も存在する場合に旧キーを黙って無視することもない。

### 実機検証

| 対象 | 新しい設定のみ・代表操作 | 通常再起動 | 旧キー残存でPaper停止 | rc1が実際に移行したconfig |
| --- | --- | --- | --- | --- |
| Paper 1.21.11 #132／Java 21.0.2 | PASS 8 groups | PASS 4 groups | PASS、config／credential DB不変 | PASS、bytes不変・4 groups |
| Paper 26.3 #203／Java 25.0.2 | PASS 8 groups | PASS 4 groups | PASS、config／credential DB不変 | PASS、bytes不変・4 groups |

供試Paperはrc1と同じbuildを固定し、今回のconfig差分を確かめた。rc1移行確認では公開済みrc1 JAR（SHA-256 `917c358c201aa219277b96a447fb85116e8bdb0260870a4d76a8c51219d31c37`）を実際に起動して旧値8／5を新キーへ移し、そのconfigをrc2へ渡した。rc2で値・file bytesが変わらず、認証と代表の読み書きが通った。

### 候補identity

- source: `7960a913a11c621d85e6120ee412b696fe125457`
- branch: `agent/stable-rc2-legacy-config`（push済み、mainへは未統合）
- CI run: `39699287525`（success）、artifact `12392277293`
- CI artifact ZIP: 294,765 bytes、SHA-256 `7bbcaae733df60baa4502eadcca3e027b28388a729b8f72e00bc176453d24edc`
- JAR: `mc-remote-2321.0.0rc2.jar`、315,871 bytes
- JAR SHA-256: `ce66abaf41a94800217a11161145b9f868333b7bfa605fd1f77b888878620e50`

最終の全runtime recordはCI取得JARに固定している。最初のローカルJARとの差は、作業treeに残っていた未追跡の空の旧SQLite resourceディレクトリだけだった。全entryの内容は一致し、その空directoryを整理した後の`./gradlew clean jar`でCIとbytes一致を確認した。最初のローカルJARのpulseを最終候補の根拠には使っていない。

### README・upgradeの案内

README「設定」の直後から「旧b5／b7設定からの更新」へリンクし、「更新と前の版への戻し」の中に17項目の旧→新の対応表を追加した。同梱configのcommentも停止・手動修正の案内へ変更した。公開用Release本文の案は同packetの`rc2-release-body-draft_ja.md`。
