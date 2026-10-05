# b9 Python handoff-materials分類返却票

- 対象repo: `Naohiro2g/minecraft-remote-api`
- knowledge contract path: `00-hub/b9-gate-close-instructions_ja.md`、`00-hub/release-gate-notes_ja.md`の2026-10-04 b9節
- knowledge contract commit: `099c40b0c312694712653885200f3114ea4bed33`（実際に取得・実読したSHA。dev agent runtimeとINDEXも同commitで参照）
- 対象: 指示票に挙げられた7 directory、45 file、150,870 bytes。内訳は①1件、②2件、③4件
- 結果: 収容済み3 directoryの対象12 file、53,876 bytesは、knowledgeの全文bytesとSHA-256に一致（PASS）
- 実施範囲: 分類、移管済み素材の読取・照合、返却素材の保存。対象directoryの元fileは変更・削除していない

以下の分類が、元MANIFESTに書かれた作成時の分類・未了状態を更新する。移管済みMANIFESTも全文照合の対象なので、元を編集せず本票で更新する。

## Directoryごとの分類

| directory（`handoff-materials/`配下） | 分類 | 理由と移す先／保持先 |
| --- | --- | --- |
| `2026-10-04-b9-python-confirmation` | ③ 廃棄候補 | 実装前の決定論的なstub観測、旧fixture inventory、初期確認票。b9で契約追従・移管・公開が完了し、調査用の一時素材として用が済んだ。元sourceは公開Git履歴`7981031765cfcc43acc23f03e86e97ba74bae494`、経過はknowledgeのb9節で参照できる。本directoryの全文がknowledgeに収容されたという主張ではない |
| `2026-10-05-b9-python-work` | ② 自repoで保持 | TestPyPIをb9後に手動実行へ絞る後続作業の起点。保持先は自repoの同directory。元の取り込み待ち項目は完了しているため、後続の用途・終了条件を下記へ更新する |
| `2026-10-05-b9-python-tooling` | ② 自repoで保持 | rc1などでfixture／同梱WireScopeの入力を更新するときの比較基準、取得元と移管を外すsourceの引継ぎ。保持先は自repoの同directory |
| `2026-10-05-b9-python-release` | ① knowledgeへ移す | PyPI.orgへの初公開、当時のenvironment／公開許可、tag CI、公開本体と両index、fresh uv取得の照合素材。後から同じ時点の観測は取り直せない。収容先案は下記 |
| `2026-10-05-b9-python-live` | ③ 廃棄候補 | `14-evidence/artifacts/2026-10-05-b9-dev-live/python/segment-2/`の6 file（MANIFESTを含む）と全文・SHA-256一致 |
| `2026-10-05-b9-dev-hello` | ③ 廃棄候補 | `14-evidence/artifacts/2026-10-05-b9-dev-live/python/saved-token-check/`の4 file（MANIFESTを含む）と全文・SHA-256一致。保存tokenでの`token_expired`観測もそのまま保持されている |
| `2026-10-05-python-windows-entry` | ③ 廃棄候補 | `14-evidence/artifacts/2026-10-05-python-windows-entry/`にmaterialsの2 fileが全文・SHA-256一致で収容済み。ローカルの`MANIFEST_ja.md`は未収容だが、転送用の一覧として用が済んだ |

### ②の使い道と捨ててよくなる条件

**python-work**: `materials/confirmation_ja.md`のTestPyPI継続案と、当時のworkflow／CI設定を後続作業へ渡す。knowledgeのb9節は「b9では自動のまま、以降は手動のときだけにする」を採用済み。この票ではworkflow変更を実施していない。

捨ててよくなる条件は、後続作業で手動実行のみの経路を実装・検証・pushし、runbookとknowledgeへの返却がそろい、本directory固有の未処理事項がなくなること。旧candidate `2f943ff`のCI digestや当時の未設定environmentは経過であり、現在の公開identity／設定として用いない。

**python-tooling**: `fixture-comparison.json`、`wirescope-comparison.json`、`tooling-input-identities.json`を次の入力更新時の比較に使う。移管前の同機能版Scratch `c7505c8`とtooling `dc1ab83`のWireScope ZIP／asset一致、fixture 7件の一致、取得元のprovenanceを引き継ぐ。`confirmation_ja.md`の移管を外すsource `10c0cc5`も、Python側の復帰経路を確認するときの起点になる。

捨ててよくなる条件は、rc1などで次の入力・比較結果・取得手順・復帰先を記録し、この基準のうち引き続き必要な情報がknowledgeまたは公開の管理対象文書へ収容・採用されること。移管前へ戻す実操作を今回実施したという主張ではない。

## ① 公開時素材の収容先案と全file一覧

- 記録案: `14-evidence/records/2026-10-05-b9-python-release_ja.md`。返却票を正式recordへ採用するかはknowledge側で判断する
- 全文素材の収容先案: `14-evidence/artifacts/2026-10-05-b9-python-release/`
- 下表の相対pathを維持して15 file、28,841 bytesを収容する案。rootのMANIFESTも対象
- 公開source: `b901c88fe41b67530ff353271683ece9fd453076`／tag `v2320.0.0b9`。公開後文書commitは`39f2ec951b7cf0deb07bbfb7156faa26832372f4`
- wheel／sdistなどのbinaryは素材に重複収容していない。token実値、private address、player UUID、private設定は①へ入れない
- `verify_publication.py`のmain一致条件は、文書更新前に実施した時点の検査条件。現在のmainへ同じ条件で再実行するためのscriptではない

| 相対path | bytes | SHA-256 |
| --- | ---: | --- |
| `MANIFEST_ja.md` | 2,816 | `c6b6c772c51e4d3709c93468474447e69f4b4233cec458750aa4cc0724f88ab3` |
| `materials/authorization-preflight_ja.md` | 1,699 | `95bdcb1154a249e195c8cf83c6a6fbde1589156f786df45714acf6ab5e8282c9` |
| `materials/preflight.json` | 2,071 | `866b3fc6e6cffff15e79e7b4fb396c056dc047f54e377b3f3e286c5995a8e0ad` |
| `materials/pypi-entry-check.json` | 680 | `e6967a42d29ae14d6e59b9398d50c48ca4aa3b2155c0ceedd540de2d43feff21` |
| `materials/pypi-entry-check.pyproject.toml` | 530 | `a68bf648b1cea7900bfeb8a73f7e49ff43e18502fa105c167416cedb45f241b4` |
| `materials/pypi-entry-check.uv.lock` | 1,048 | `f3a4f158c0c0e600a9e7df91ac368dd19cdde199cc75c8d943d6c46af3df6145` |
| `materials/pypi-verification.json` | 1,176 | `b9b6e3ae276c4759b69c0583af51df84caf408b7d3367c0a06403a7987b3719a` |
| `materials/release-manifest.json` | 681 | `da9887d12e57d929a93531bbcffc7795895aa0bbc7eef1792e2d03cb4979e838` |
| `materials/release-notes_ja.md` | 1,674 | `33e3795ecf661a64e9f287f8009a9b644d0efed0d1976b8f049b1ecc96288ed7` |
| `materials/release-return_ja.md` | 7,810 | `863af82f8b6d3487f9956f1ad693dfe11988cfccacc2f5595f5d7548209028b1` |
| `materials/release-verification.json` | 1,469 | `9c39a550838f91e5fce424c2e8d582f1a8c2e0e6776b5825297460345f08485e` |
| `materials/tag-ci-manifest.json` | 672 | `10b8e5cc102df5f53b0726a41df8b3f110656b1760cc0918e902684661645121` |
| `materials/tag-ci-verification.json` | 631 | `fffe0292e8485484d4edf120cfbd3e7d6558fdb4edc0b121bfeabdf22416ad83` |
| `materials/testpypi-verification.json` | 1,200 | `3c563a57ce61d1e0c456d89ca8235b8fdc9aa427f9842bca730b85b13eaaa05f` |
| `materials/verify_publication.py` | 4,684 | `9ede7a96d9a7525106987916e6f83977878a72f26ff418e0474772f672decfe3` |

knowledgeの全文収容・照合確認まで、この①の元は保持する。

## 収容済み3 directoryの照合

knowledgeは上記固定SHAのGitHub Contents APIから取得した。base64を復号したbytesをローカル原本と直接比較し、bytes数・SHA-256も照合した。APIのGit blob SHAも検査し、収容先のfile集合に不足・余分がないことを確かめた。

| ローカルdirectory | 対象file | 収容先との全文・SHA-256 | 補足 |
| --- | ---: | --- | --- |
| `2026-10-05-b9-python-live` | 6 | PASS | root MANIFEST＋materials 5件 |
| `2026-10-05-b9-dev-hello` | 4 | PASS | root MANIFEST＋materials 3件 |
| `2026-10-05-python-windows-entry` | 2 | PASS | materialsの2件を収容先rootへ配置。ローカルMANIFESTは未収容 |

| ローカルpath（`handoff-materials/`配下） | bytes | ローカル・knowledge共通のSHA-256 | 全文 |
| --- | ---: | --- | --- |
| `2026-10-05-b9-python-live/MANIFEST_ja.md` | 1,800 | `cf0221ea8164f7706c95db43950a33b1f5c0f0edf6e00a026790dc4ba7889bf8` | 一致 |
| `2026-10-05-b9-python-live/materials/confirmation_ja.md` | 7,049 | `35dee1710d4b2f5d5672dbdb0cda7f6ac0e8cbe2c609267c913e3d9e347c293b` | 一致 |
| `2026-10-05-b9-python-live/materials/human-wirescope-observation_ja.md` | 2,909 | `d26ee1b173146b89c5e7f8c0317ed66ad1b6a68c9e2732cf586fe6817f346a29` | 一致 |
| `2026-10-05-b9-python-live/materials/observer_snapshot.json` | 9,513 | `ef4d0bdf2ed8fbb3919b1a8cfadfcc79a7c749517a19efd669befe4d84c042fe` | 一致 |
| `2026-10-05-b9-python-live/materials/result.json` | 2,492 | `53f8b414f0a45df9932c3542d7e720faaebd12581e46aec1eee94decdb4767ea` | 一致 |
| `2026-10-05-b9-python-live/materials/run_segment2.py` | 9,550 | `50d7c0d46186a2f534ff79ceb6e37578d876ae6e8b646a3789a58a28e9c7fd83` | 一致 |
| `2026-10-05-b9-dev-hello/MANIFEST_ja.md` | 1,207 | `b6cd7fda93d4e881d6ba694fed1d84abf5c874cf1b968ff43ef6d03532bf3c9a` | 一致 |
| `2026-10-05-b9-dev-hello/materials/check_saved_token.py` | 5,249 | `cb6ca3084c0bf0a1493ae566b4337c3826c712a2a2f6181cc37ea094ece2ade7` | 一致 |
| `2026-10-05-b9-dev-hello/materials/confirmation_ja.md` | 6,912 | `1f7b654804787833efe9f8ac13bda96ca1d5cc4d0361c44f1881803ea8a5c874` | 一致 |
| `2026-10-05-b9-dev-hello/materials/result.json` | 986 | `31af3cae137368eee5e5476728e221bba7ad59ec805d5ae60c87987022ead70e` | 一致 |
| `2026-10-05-python-windows-entry/materials/handoff_ja.md` | 3,736 | `68379f4e962021bdfb920ec43c90cfb0df0e276599530105f6278850d4feadb8` | 一致 |
| `2026-10-05-python-windows-entry/materials/windows-user-report_ja.md` | 2,473 | `21c3376f5384658fb9fcee2dbd7dfc57263fe9fcf76a996096ddbcf165a24fff` | 一致 |

WindowsのローカルMANIFEST（1,863 bytes）は全文移管の照合対象外。廃棄理由は「同じ全文がある」ではなく、転送一覧の用が済んだため。実際のWindows試験報告2件は一致を確認済み。

## 検証素材と処理状態

| directory | 分類 | file数 | bytes |
| --- | --- | ---: | ---: |
| `2026-10-04-b9-python-confirmation` | ③ | 5 | 22,679 |
| `2026-10-05-b9-python-work` | ② | 4 | 15,424 |
| `2026-10-05-b9-python-tooling` | ② | 8 | 28,187 |
| `2026-10-05-b9-python-release` | ① | 15 | 28,841 |
| `2026-10-05-b9-python-live` | ③ | 6 | 33,313 |
| `2026-10-05-b9-dev-hello` | ③ | 4 | 14,354 |
| `2026-10-05-python-windows-entry` | ③ | 3 | 8,072 |

- `transfer-verification.json`: 12件のローカル／knowledge path、双方のbytes／SHA-256、直接bytes比較結果、7 directory全45件のinventory
- `verify_close.py`: 実際に使った照合script。取得済み固定SHAのContents API JSONを入力とする。API取得用の一時入力は`/tmp/mcr-b9-close-knowledge-inputs.json`に保持し、正式evidence案には重複収容しない
- 本close返却素材も①の候補。収容先案は`14-evidence/artifacts/2026-10-05-b9-python-close/`
- ①・②・③とも元fileは保持したまま。対象directoryに削除・上書きはない。①はcoordinatorの全文移管確認待ち、②は上記用途のため保持、③は廃棄可能な候補として返却する
- private設定と保存tokenは分類対象の7 directory外にあり、この作業では取得・変更していない
- default branch統合は指示票でcoordinatorが照合済みとして扱う。今回の分類に伴うcommit／push、追加公開、shared環境の変更、人間参加の再試験はない
- gateの最終CLOSED記録はknowledge coordinatorが行う
