# B9 gate close — McRemote搬送素材の分類返却票

指定7 directoryを **①1件、②1件、③5件** に分類した。今回作成したclose返却素材は別途①。収容済み実機素材は全文を照合し、19 fileに不足・説明外の差分はなかった。

- 搬送元: `Naohiro2g/McRemote` / Codex。
- branch / commit: `main@5cb33ebad4bf2c5e36c3433b0f70fe6070915b00`。
- knowledge contract path: `00-hub/b9-gate-close-instructions_ja.md`（共通／McRemote）。INDEX、release-gate-notes B9／B8、正式live INVENTORY、DECISIONS `2026-10-05-02`も参照した。
- knowledge contract commit: **`099c40b0c312694712653885200f3114ea4bed33`**。最新runtimeのbootstrapと指定SHAが一致、指定pathをGitHub APIから取得して読んだ。knowledgeの作業cloneは操作していない。
- 対象: 2026-10-04〜10-05のMcRemote B9素材6 directoryと、B8から引き継いだ比較素材1 directory。default branch統合は指示に従い今回の作業対象外。
- 返却範囲: 分類、収容済み素材の移管照合、①のfile一覧／収容案、②の用途・廃棄条件、B8素材を捨ててよいかの回答。前回公開時の「全件②」を今回のclose指示に従って更新する。

## Directoryごとの分類

| directory | 分類 | 理由・用途・廃棄条件 |
| --- | --- | --- |
| `2026-10-04-b9-mcremote-confirmation` | ③ 廃棄可 | 凍結前のstatic確認票／audit／48 testsの結果は、指定knowledgeのB9「確認票の返却」に着地。旧source `14cd3b7`とtest codeはGitに残り、後のcandidate票と現行契約で置き換わった。独立した実機観測は含まない。旧auditの再実行も可能で、rc1の基準に使わない |
| `2026-10-05-b9-mcremote-candidate` | ② 自repoで保持 | rc1のJAR権限bit／再現性／fixture provenance比較に使用。B9 source `5cb33eb`、JAR `4feb90db…a58e`、CI `37220994120`、umask002／022の比較JSON・script・JARを基準とする。**rc1の固定sourceで手元002／022とCIのmode・entry bytes／metadata・JAR SHA一致を確認し、その結果と新しい比較基準が正式に着地した時点で廃棄可**。用途が不要と明示された場合もcoordinatorのclose判断後に廃棄可 |
| `2026-10-05-b9-mcremote-release` | ① knowledge evidenceへ移管 | 公開前の凍結JAR照合、tag CI→公開assetのbyte一致、API snapshots／公開manifestの観測は再現しにくい。全21 fileの一覧を添付。収容先案 `14-evidence/artifacts/2026-10-05-b9-mcremote-release/`。全文移管をcoordinatorが確認するまで元を保持 |
| `2026-10-05-tooling-repo-name` | ③ 廃棄可 | 命名決定はknowledge `945807b4f0b13e9f0a3aa3b5fc02127db01f119a`／DEC `2026-10-05-02`に着地確認済み。指定099c40でも、既存repo再利用、`minecraft-remote-tooling`への改名、選択理由が一致。B9の取得経路切替も完了し、本素材を次のowner判断の正本として使わない |
| `2026-10-05-b9-dev-restart` | ③ 廃棄可（収容済み） | 正式segment-0へ全5 file収容済み。3 fileはbytes／SHA完全一致、2 fileは指示に記載されたhome pathの`~`化だけで全文一致。結果・人間のhello観測を失わず元を廃棄できる |
| `2026-10-05-b9-mcremote-live-auto` | ③ 廃棄可（収容済み） | 正式segment-1へ14 file収容済み、全てbytes／SHA完全一致。初回失効の3 fileも含む。唯一の未収容fileは再生成可能な`__pycache__`で、正式証跡に不要 |
| `2026-10-03-b8-mcremote-release` | ③ 廃棄可 | **捨ててよい。** 引継ぎ目的だったunix権限bit差の調査・固定はB9で完了。B8 gateに146 entryの権限bit差、凍結JAR `7ab24fa1…77fb`／公開JAR `fdffaf0c…80c6`、公開停止・再承認・公開identityが記録され、公開B8 JAR／manifest・Git sourceも残る。今後の基準は保持するB9 candidateの002／022／CI比較と公開B9 JARへ移る。B8の旧比較directoryをrc1の必須入力にしない |

③の分類は元directoryの廃棄可否の回答。本依頼は分類と返却を求めているため、今回はdirectoryを削除していない。①の元を削除していない。B8の稼働server上の運用backup、Git branch／tag、GitHub Releaseは本directory分類の対象外。

## 収容済み2 directoryの全文照合

収容先とINVENTORYを指定099c40から取得し、各fileのcontentをdecode、bytes数とGit blob SHAを検証した。ローカルとのbyte比較・SHA-256比較、正式INVENTORYのbytes／SHA-256比較を行った。

- 正式root: `14-evidence/artifacts/2026-10-05-b9-dev-live/mcremote/`。
- segment-0: **5 file、3件完全一致、2件sanitization後一致**。
- segment-1: **14 file、14件完全一致**。
- 説明外の差分・不足file: **0**。正式INVENTORY照合: **19／19 PASS**。
- 未収容file: `materials/__pycache__/run_with_transcript.cpython-311.pyc`だけ。指示に記載された除外と一致。
- coordinatorの収容確認: 指定close指示の「既に収容したもの」表と、正式INVENTORYが根拠。
- receipt: [live-transfer-verification.json](live-transfer-verification.json)。全19 fileのlocal／knowledge bytesとSHA-256、変換の有無、Git blob identityを記載。
- 再現手順: [verify-knowledge-transfer.py](verify-knowledge-transfer.py)。実サーバーへ接続せず、knowledge remoteと元素材だけを読む。

2 fileの差分は以下のとおり。元fileの内容に一般的な整形や追記を加えて一致させたものではなく、指示に明記されたhome directory prefixの置換だけを行った。

| file | local bytes | knowledge bytes | knowledge SHA-256 |
| --- | ---: | ---: | --- |
| `segment-0/materials/deployment-result.json` | 2624 | 2614 | `c43b05d1066548495908be062efb50adb039ee6c89def1411527f544b1124a06` |
| `segment-0/materials/restart-result_ja.md` | 5273 | 5263 | `bae3e7bc448e7f501deac738733a6c9928a138526cfb9fb07a737d187088248f` |

## ①の移管一覧と収容先案

[evidence-transfer-files_ja.md](evidence-transfer-files_ja.md)に全fileのbytes／SHA-256と収容先案を記載。[evidence-transfer-files.json](evidence-transfer-files.json)は機械可読の同一覧。

公開素材の21 fileは元directoryからそのまま移す案。JAR／manifestは公開物と同一でも、公開時に実際に取得してCI candidateと照合した素材として、観測JSONと共に収容する。token、private address、player UUID、private設定を収容する案は含めていない。秘匿化点検済み。

今回の `2026-10-05-b9-mcremote-close` は分類①。収容先案 `14-evidence/artifacts/2026-10-05-b9-mcremote-close/`。本票、分類JSON、全文移管照合receipt、検証script、session-closeを追加のclose証跡として移管する。正式record案は `14-evidence/records/2026-10-05-b9-mcremote-close_ja.md`。正式authoringと収容はknowledge担当が行う。

## 次の一手

B9 coordinatorへ本分類と①のfile一覧を返し、公開照合素材／close receiptを正式収容してもらう。①の全文移管確認後にlocal copyのcleanupを行う。②は上記用途と廃棄条件付きでMcRemote担当が持つ。③は今回の廃棄可否回答をB9 close記録に収容してもらう。横断gate closeの最終判定はcoordinatorへ返す。
