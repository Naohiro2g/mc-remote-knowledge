# b8 gate close — Pythonのhandoff素材分類票

- 対象repo: `Naohiro2g/minecraft-remote-api`。Scratch宛ての追加票は共有用であり、この票はPythonだけを対象にする。
- knowledge contract commit: `2a8c3eae4e489e67f044111b0d1e6cdd22ead86a`。remote mainのruntime、INDEX、b8 gateのclose、release operations §12、hub NOTES、14-evidence README／INDEX／b8 recordを実際に読んだ。
- 公開identity: `main`／`v2320.0.0b8`のtarget `52d35f5304e62f465c1f47ab47c00fe9bcf62470`、exact set `b8-integrated-artifact-set-1`。
- 対象: 今回のb8で作成した5 directory。b2／b5／browser調査／2026-09-23 versioning票の計6 directoryは今回の対象外。
- 状態: **分類の返却のみ。移設・削除・commit／push・再試験は行っていない**。既存の全素材を保持する。

## 移す先

正式authoringと着地確認のownerはknowledge coordinator。以下のartifact配下は**着地先の提案**であり、作成済みとは主張しない。

| ID | 移す先／担当 | 理由と次の一手 |
| --- | --- | --- |
| E1 | knowledge `14-evidence/artifacts/2026-10-03-b8-dev-live/python/component/` | 凍結candidateの検証根拠・source identityを保全。既存record `14-evidence/records/2026-10-03-b8-dev-live_ja.md`から必要な原本を参照する。 |
| E2 | knowledge `14-evidence/artifacts/2026-10-03-b8-dev-live/python/segment-2/` | token継続・run別の結果、runnerの停止と補正、humanのWireScope観測を全文保存。成功部分と停止部分を区別して既存recordへ結ぶ。 |
| E3 | knowledge `14-evidence/artifacts/2026-10-03-b8-dev-live/python/release/` | main／tag、CIと公開assetの一致、TestPyPI結果を保存。gateの公開identity照合に根拠を添える。 |
| H | knowledge `14-evidence/artifacts/2026-10-03-b8-dev-live/python/history/` | 廃棄候補の全文受領先の提案。旧candidateとlocalhost診断は経過資料であり、凍結setや正式dev PASSの入力に使わない。 |
| F | Pythonのb9移管担当へ `handoff-materials/b9-python-tooling-transfer/`（提案・未作成） | `materials/b9-python-followup_ja.md`とsound surface票を引き継ぐ。coordinatorが所有先を決めてからfixture取得元・同梱appのsource／hash／license参照を更新する。決定の着地はknowledge `12-python-client/`／sound notesとhubのb9移管事項。 |
| W | human owner／Python後続担当、knowledge hub NOTESの「WindowsでのPython導入の2ルート」 | b9のPyPI登録判断に向け、公開wheel URLとtracked `docs/windows-b8-entry_ja.md`で入口ルートを実機確認する。結果が来たら停止した手順と通常ルートの要否を返す。 |
| P | Python後続担当のGit外ローカル運用（現pathで保持） | private dev設定とrelease時のuserファイル保全fingerprintを保持する。必要になった時点でprivate ops ownerへ別途渡す。knowledge公開evidenceには含めない。 |

## directoryごとの分類

directory内で用途が違うため、混在するものはfile範囲も指定する。全fileの割当は同directoryの `b8-close-file-inventory.json` に記録する。

| directory（`handoff-materials/`からの相対path） | 分類 | 対象・移す先・理由 |
| --- | --- | --- |
| `2026-09-30-b8-python-component/` | ①履歴票、③旧artifact | `MANIFEST_ja.md`、初期票、candidate追記はE1の履歴として保存。`candidate-fc6c700/`と`ci-36718297434/`の6 fileは③候補。source `fc6c700`の失効したcandidateで、公開source `52d35f5`の入力ではない。Hへの全文移管・非参照確認後にだけローカル原本を捨てる。 |
| `2026-10-01-b8-python-successor/` | ①正式evidence、②b9 | `return_ja.md`、CI `36860299749`成果物、WireScope生成／test log、79-frame snapshot、MANIFESTはE1。`sound-surface-handoff_ja.md`はFへ。keyword-only、None省略、pitch／note排他、server既定保持の決定と理由を失わないため。 |
| `2026-10-02-localhost-smoke/` | ③廃棄候補 | MANIFESTと確認票の2 fileをHへ全文受領してから廃棄。通常devの正式gateに採用していないローカル診断で、b7→b8 token継続の証拠に読み替えない。保存localhost tokenの失敗と新規pairing成功の経過を先に保存する。 |
| `2026-10-03-b8-dev-token-upgrade/` | ①正式evidence、②private運用、③重複・cache | b7／b8 summary、runner、凍結graph、run 1〜3原本、human観測、確認票、搬送ZIPはE2。`param_dev.py`と`endpoint-resolution-failure.json`はP。rootのframes／summary／handoffの同内容コピー3 fileと`__pycache__/`の2 fileは③候補。run別原本への着地と全文・非参照確認まで残す。 |
| `2026-10-03-b8-python-release/` | ①正式evidence、②Windows／b9／private運用、③重複・旧一覧 | 公開返却票、GitHub／TestPyPI snapshot、Release asset原本3 file、CI ZIP／manifest、照合script、公開request、MANIFESTはE3。新しいb9 followup票はF／W、`state.json`はP。CI展開wheel／sdist、匿名取得wheel、旧 `handoff-inventory_ja.md` の4 fileは③候補。Release原本とこの詳細分類を残し、旧一覧の対象外6 directoryの情報も保存してから整理する。 |

## 原本と重複の確認

- token／Python segmentの既存公開搬送ZIP: `2026-10-03-b8-dev-token-upgrade/python-segment-2-return.zip`、44,012 bytes、SHA-256 `ed283f90f068043dac53375053e1d5061a38aa109e80c852a38200de34e21f03`。19 file＋entry manifest。private config／credential state／cacheは収録していない。このZIPだけで対象directory全体の全文移管が完了したとは扱わない。
- 最新summary／framesの原本は `materials/run-3/`。run 1とrun 2は消さず、製品FAILとrunner／接続準備の停止を混同しない。token継続の原本は `b7_summary.json`／`b8_summary.json`。
- `materials/handoff_ja.md`は`run-3/return_ja.md`、rootの`representative_frames.jsonl`／`representative_summary.json`はrun-1配下の同名fileとそれぞれbyte-for-byte同一。
- Releaseのwheel／sdistを原本とし、CI展開版と匿名取得wheelはbytes／SHA-256が一致するコピー。公開 `manifest.json`（681 bytes）とCI manifest（672 bytes）は別物で、両方を保存する。
- 旧fc6c700のlocal wheelとCI wheelは異なるbytesであり、同内容コピーとは扱わない。どちらも旧candidateとして③に割り当てた。

## 削除条件と未完の境界

- knowledgeの指定commitには正式b8 recordの**要約**があるが、`14-evidence/artifacts/2026-10-03-b8-dev-live/`以下のPython原本は見当たらなかった。coordinatorによる全文移管の確認戻りは未受領。
- ③は候補であり、**現時点では一つも削除しない**。③を含む原本全文の受領先、knowledge着地commit／path、inventoryのbytes／SHA一致、他の正本／evidenceから非参照であることをcoordinatorが確認してから整理する。cacheもこの保留に含める。
- private fileは公開搬送から除外する。②のローカル運用保持であり、publicへ全文をコピーすることを削除条件の代用にしない。credential store／continuity stateはこのdirectory分類の外にあり、触れていない。
- `__pycache__/`も公開搬送から除外する。③のまま現pathで保持し、coordinatorの全文確認が完了するまで削除しない。cacheの受領先は未指定であり、Hへの公開commitは提案しない。
- ①と②の移設も未実行。Windows実機・b9移管の実装には着手していない。Scratchのhandoff分類・公開sourceのfixture一覧はScratch担当の返却事項。
- 元worktreeの `examples/param_mc_remote.py`／`examples/particle_graph.py` のuser変更を保持した。source／wheel／WireScopeのidentityを変えていない。
