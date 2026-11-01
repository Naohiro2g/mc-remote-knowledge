# 安定版2321.0.0のgate closeの素材（2026-11-01）

> 1年ぶりの安定版（2321.0.0）の横断release gate（`00-hub/release-gate-notes_ja.md`の2026-10-22の節）のclose分類
> （`00-hub/stable-gate-close-instructions_ja.md`、knowledge `867adb7ed8d621d72ff97bc39c2b2e8514a79688`）で、McRemote、Python、
> Scratch／tooling、Stackが①とした素材を収容した。公開の照合はgate notesの「公開（2026-11-01）」にある。Temurinでの確認、26.3の
> セットの最終の確認、切り替えた後の人の確認は、それぞれ別のrecordにした。この記録は素材の置き場所と分類を示す。

## 収容した素材

| 収容先（`14-evidence/artifacts/2026-11-01-stable-gate-close/`） | 中身 | 搬送元 |
| --- | --- | --- |
| `mcremote/2026-10-22-rc2-publication-stable-candidate/` | rc2の公開の前後の照合（取得した実体とGitHubのdigest）、安定版の候補を決めたidentity、作業の返却票 | McRemote 同名 |
| `mcremote/2026-10-22-stable-rc2-confirmation/` | rc2の隔離したPaper（1.21.11、26.3）での観測、旧`b5.`／`b7.`のキーでの起動の停止、rc1のconfigを移した後の保持とpulse、実行したrunner | McRemote 同名 |
| `mcremote/2026-10-29-stable-temurin-validation/` | Temurinでの確認（`14-evidence/records/2026-10-29-mcremote-stable-temurin-runtime_ja.md`） | McRemote 同名 |
| `mcremote/2026-10-31-stable-release-preparation/` | 安定版の公開の返却票と、refs、Latest、CI、5 assetの照合 | McRemote 同名 |
| `python/` | 候補の返却票と確認票、安定版より前のPyPIの既定の観測、公開の返却票、公開のassetの実取得と承認の後のproviderの観測 | minecraft-remote-api `2026-10-22-stable-python-candidate`、`2026-10-22-stable-python-confirmation`、`2026-10-31-stable-python-release` |
| `scratch-tooling/2026-10-21-upstream-sync/` | 本家への追従の後のパレットの頭出しのずれの実測（live-auto、実ブラウザ）、probeのscriptとJSONとPNG | scratch-editor 同名 |
| `scratch-tooling/2026-10-22-stable-work-scratch-tooling/` | 凍結の候補の返却票、identity、候補の照合、ブロック一覧のidentity、一般CIの既知の差 | scratch-editor 同名 |
| `scratch-tooling/2026-10-31-stable-publication/` | toolingとScratchの公開の返却票と公開物の値、凍結値の照合、公開の手順書 | scratch-editor 同名 |
| `stack/2026-10-28-geyser-b1273/` | 統合版26.60への対応（`sb-beta`のGeyserをb1273へ、既定のconfig、iPhoneの26.60で信頼の確認の後に参加）の返却票 | mc-remote-stack 同名 |
| `stack/2026-10-31-stack-return-four-items-java/` | 26.3のセットの最終の確認（`14-evidence/records/2026-10-31-stack-paper231-temurin25-heap3g_ja.md`） | mc-remote-stack 同名 |

52 file（718,131 bytes）を、各担当の一覧のbytesとSHA-256で照合した（不一致0）。McRemoteの23 file（339,877 bytes）は
McRemote `handoff-materials/2026-11-01-stable-gate-close/materials/inventory.json`、Pythonの7 file（41,322 bytes）は
minecraft-remote-api `handoff-materials/2026-11-01-stable-python-close/materials/evidence-transfer.json`、Scratch／toolingの15 file
（262,201 bytes）はscratch-editor `handoff-materials/2026-11-01-stable-gate-close-scratch-tooling/materials/EVIDENCE_FILES_ja.md`、
Stackの7 file（74,731 bytes）はmc-remote-stack `handoff-materials/2026-11-01-stable-gate-close/MANIFEST_ja.md`の値。

- 写しの加工（各担当）：McRemoteはhome directoryのpathを`/USER_HOME`に（2 file、3か所）。Pythonは3つの票のURL、ホスト名、
  address、local pathを置き換え、JSONは公開の状態に要るfieldを抜き出した（元のpath、bytes、SHA-256を各fileに記載）。Scratchは元と同じ
  bytes。Stackは`/v1/join`に外から接続した先のホスト1件と、pulseのtokenとplayerの4つのfieldを置き換えた
- Stackの最初の写しは、プラグインの版（`1.8.4.0+26.2`、`0.4.0.1+26.2`）、APIのメソッド名`chat.post`、公開の出典のURLのホストまで
  伏せていた。coordinatorが元と比べて指摘し、Stackが直した写しを収容した
- 収容の後、coordinatorがprivate address、home directoryのpath、UUIDの定型、tokenを点検した。tokenは`[REDACTED]`と
  `[REDACTED_TOKEN]`だけ。`mcr_eh_`の値は隔離したworldで作ったentityのhandleで、秘密ではない。`mc-remote.local`は公開のschema名
  `mc-remote.local-compatibility-pulse`の一部。scriptと票の中の`/tmp/`のpathは当時の実行場所で、収容した先から動かす入口ではない

## 分類

| 担当 | ① | ② | ③ |
| --- | --- | --- | --- |
| McRemote（8 directory、90 file） | 4 directoryから23 file | HUDの3つ（`2026-10-23-game-hud-first-slice`、`2026-10-24-hud-colors-input`、`2026-10-26-hud-quick-actions`。`2321.1.0`のHUDと入力の改善の候補）、`2026-10-29-java-temurin-policy`（教材とホームページのhow-toへの転用元。human ownerの一時保持の指示）、close返却packet（31 file） | 36 file（公開のJAR、manifest、本文と同じもの、aggregateに含まれるpulse、置き換わった案） |
| Python（4 directory、46 file） | 3 directoryから5 file（写しは7 file） | `2026-10-23-wirescope-python-development`（6 file。editableの修正と47 testsのreview、WireScopeの観測の開始と終了、Jupyter／.pyの往復の設計の入力）、close返却packet | 35 file（wheel、sdist、CIのZIPなど。公開物と同じbytes） |
| Scratch／tooling（7 directory、151 file） | 3 directoryから15 file | パレットの実測（①と同じ4 file。修正の原因の追跡と回帰test、`2321.1.0`の範囲の検討の候補）、`2026-10-24-bridge-multiple-targets-confirmation`（6 file。Bridgeの複数の接続先、`2026-10-24-06`）、`2026-10-27-scratch-wirescope-lifecycle`（2 file。WireScopeの観測の順序と再接続の比較）、close返却packet | 127 file（公開物の重複、Actionsの外側のZIP、OCIの転送用のlayoutなど） |
| Stack（10 directory） | 2 directory（写しは7 file） | `2026-10-27-bedrock-https-review`（統合版のHTTPSの検討の入力）、`2026-10-29-vps-load-motd-icon`（負荷試験、残りのMOTD、アイコンの規定） | 6 directory（`2026-10-29-jvm-flags-review`、`2026-10-29-rc2-263-preflight`、`2026-10-29-stable-deployment-conditions`、`2026-10-29-stack-four-items-java-return`、`2026-10-31-paper263-build231`、`2026-10-31-web-pair-target-selections`。knowledgeや後の返却に統合済み、またはコードから再実行できる） |

- 各担当の②の使い道と捨ててよくなる条件は、搬送元の分類票にある（McRemote `classification_ja.md`、Python `classification_ja.md`、
  Scratch `RETURN_ja.md`の3、Stackの返却）
- ③は、元のpathをgate notesが参照しているものを含む。各担当は、①の収容をこの記録で確かめた後に整理してよい
- toolingのcheckoutに今回の期間の`handoff-materials`は無い。toolingの資料はScratchのpacketに同居している
- Stackの11/1の切り替えの素材は`handoff-materials`に無い。新しいセットのServerBackupのarchiveと旧セットのcutoverのarchiveはworldと
  設定を含むので、knowledgeへは移さず、private opsで持つ

## close依頼の残り（各担当の返却）

- Scratch：候補のbranchの配布対応の5 file（配布のscript 2つと回帰test 2つ、`mc-remote/local/USER_GUIDE_ja.md`のリンク）を`develop`へ
  入れた。`develop`は`b1f3ab883a8124b7b3e5a9c46e6f7cc41e3a310b`（`bee41dc`から1 commit）。coordinatorが確かめた：GitHubのcompareで
  変わったのはこの5 fileだけで、`d3aa547`の同じ5 fileと同じ中身。CI run `41241123827`はsuccess。testは取り込む前に2件がFAILし、
  取り込んだ後に102件PASS（Scratch担当）
- Stack：
  - ServerBackup：新しいセットのbackupのoutboxに、切り替えの後のarchive（2026-11-01 04:30:48 JST、938,714,728 bytes）。中身は展開していない
  - ブロック一覧：直した条件で照合した。`d3aa547`は`ffb496e`の祖先（2 commit ahead、0 behind）、間の変更は`mc-remote/block-reference/site/`
    とunit testの1 fileで、ブロックの定義の変更は無い。knowledgeの64 fileは公開のtagの対応するfileと同じbytes
  - 旧セット：停止した旧project、退避したvolume、cutoverのarchiveを、2026-12-01と、新しいセットで定期のbackupとoff-hostへの保管
    またはrestoreの確認が済む時点の、遅いほうまで持つ案。消すのはhuman ownerの了承の後
