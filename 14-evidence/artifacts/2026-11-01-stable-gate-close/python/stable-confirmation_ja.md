<!-- Sanitized copy for evidence handoff. -->

- 元資料: `2026-10-22-stable-python-confirmation/materials/confirmation_ja.md`。
- 元bytes: 12900、元SHA-256: `3e7a12397773f80ed3ec7fb1e3921f6c7f5c405ae1563e8a624f9cac717bb5b7`。
- 加工: provider URL 1箇所、hostname 5箇所、address 0箇所、local absolute path 0箇所を置換。その他の本文は保持。
- これは当時の返却票。公開前・承認待ちの記述は当時の状態であり、最終状態はpost-approval-provider-observation.jsonとclose分類票を参照。

---

## Release gate 確認票

- 対象 repo: `Naohiro2g/minecraft-remote-api`（Python client）
- 対象 branch/commit: `main@c30105349ef26413e925699143396ea05bd3e380`。remote mainと`v2321.0.0rc1`のtag targetも同一（GitHub API照合）。未commitの作業tree差分は以下の範囲分離を適用する。
- release / channel: 初回stable `2321.0.0` / tag案 `v2321.0.0` / GitHub Release（pre-release OFF、draft OFF、Latest）/ [hostname-omitted]。まだ作成・公開していない。
- gate coordinator: knowledge担当session（Claude Code）
- human release owner: プロジェクトオーナー（PyPI environmentのrequired reviewerは`Naohiro2g`）
- current phase: OPEN、確認票返却（2026-10-22、返却目安10/23より前）
- contract maturity / required test tier: protocol `23.2.1`の既存公開contract。Pythonは版番号のみ。rc1の決定論的CIとlive-human結果を再利用する方針。stable候補の版・source差分・build/asset照合を追加し、通常CIはそのcandidateで実行する。
- knowledge contract path: `00-hub/stable-gate-confirmation-instructions_ja.md`（共通、Python client）、`00-hub/release-gate-notes_ja.md`「2026-10-22 初回stable（2321.0.0）横断release gate」、`00-hub/DECISIONS_ja.md` `2026-10-22-01`〜`-03`
- knowledge contract commit: `61d5fd8df66ca49a5429fe010a131eab58f702ba`（remoteから実読。runtime、INDEXも同SHA）
- gate manifest identity: stable候補のexact set／source commit／artifact digestは未提示・未凍結。再利用元は`rc1-integrated-artifact-set-1`。
- change cone: rc1 sourceからpackage版を`2321.0.0rc1`→`2321.0.0`、関連lock/文書/生成APIの版表記/版アサーションを同期。protocol/API/wire、認証、server/設定、WireScope同梱実体、fixtureは変更しない案。Release本文に最小移行案内と既存WireScope注意を載せる。
- reused PASS / rationale: rc1 candidate CI `39067369316`（Python 3.10〜3.13 各784 PASS）、main CI `39216669184`、3 OS live-human `2026-10-19-rc1-candidate-3os-live-human`、公開・closeの照合。版metadataだけを変えることをcandidate diffで確認して採用をcoordinatorへ返す。今回新たなlive PASSは主張しない。
- exact compatibility set / freeze status: 現在のPythonはrc1 source `c30105349ef26413e925699143396ea05bd3e380`。stable set未凍結。同梱WireScope source `6447f6e8cbfbeeb9d229990b5c4f6e82a5875666`のpinとZIP/manifestを維持する案。新しいowner入力を自動採用しない。
- target deployment / profile / lock: 今回は指定無し、変更無し。箱庭の11月`sb-beta`／12月の切替は下の案に従い、shared環境の接続・deploy・DNS変更を実施していない。
- authorized next action: 本確認票を返す。Pythonのstable候補作成の具体的な着手、凍結、tag/Release公開、PyPI承認はcoordinatorの次指示に従う。今回sourceの版更新・公開・他repoへの着手依頼はしていない。
- test class: 今回はunit/deterministic相当の静的照合とprovider API照合。再利用元はunit/deterministicおよびlive-human。live-auto/live-humanは新規実施無し。
- 実行した command / 手順: knowledge指定文書のAPI取得、`git rev-list --count v2321.0.0rc1..HEAD`、rc1 sourceの`git grep`で版番号を棚卸し、`git diff --name-only -- mc_remote .github pyproject.toml uv.lock scripts`、GitHub main/tag/rc1 Release/environment/公開変数/branch policy API、PyPI JSON API、`git diff --check`。
- 結果: rc1後にmainへ入ったcommit 0、main/tag/HEAD一致。runtime/workflow/project/lock/scriptsの作業tree差分無し。旧PyPI既定stable `1214.10.13`（non-yanked）、rc1のPyPI wheel/sdist digestはGitHub provider digestと一致。PyPI required reviewer有効、admin bypass不可、tag `v*`のみ、`PYPI_PUBLISH_ENABLED=true`を確認。今回のrepoコード変更は無し。
- evidence record / artifact: knowledge `14-evidence/records/2026-10-19-rc1-candidate-3os-live-human_ja.md`、`14-evidence/records/2026-10-19-rc1-gate-close_ja.md`、`14-evidence/artifacts/2026-10-19-rc1-gate-close/python/`。今回の返却素材は本packetのprovider/source/PyPI観測JSON（正式evidenceではない）。
- 未検証の境界: stable source commit／wheel／sdist／manifestは未作成。stable CI、rc2の実機、stable indexでの無指定取得、Release/Latest実公開、PyPI公開後のbytesとyank状態、移行ページの開通は未検証。既存sample草稿の見え方やcold-readerもstableのPASSに含めない。
- security / compatibility / rollback の確認: human ownerのPyPI承認を保持。旧1214利用者にはexact pinと移行期間を案内。旧環境のlock/requirements/作品は保存する。既存tag/Releaseの付替え・同名artifactの再uploadはしない。Python環境の復帰とworld復元は別。private設定、local NOTES/CLAUDEは公開commitに含めない。
- 判定を求める事項: ①rc1を基点とする版番号だけの候補、②最小移行案内をRelease本文＋knowledgeの`/migration/`へ置く案、③11月のガイド強化と改善の分離、④12月のstarter切替案。component/横断gateのGREEN/HOLD/REDは判定しない。

### 共通への回答

#### 1. rc1後のdefault branch差分と基点

- remote `main`もrc1 tagも`c30105349ef26413e925699143396ea05bd3e380`。rc1後のcommitは0。
- stableはrc1 tagを明示したcleanな作業treeから作る案。今のmainと同じ内容なので、機能差分を選ぶ問題は無い。
- 作業中のREADME再編、旧protocol移行ガイド、XYZ教材対応、axis/particle作例、新規testは未commit。すべて初回stableへ混ぜず、後続で扱う。既存の利用者変更3 fileも保全する。安定版の並行保守branchを新設する案ではない。

#### 2. 版番号だけを変える場所と手間

| 対象 | 予定する更新 |
| --- | --- |
| `pyproject.toml`、`uv.lock` | project版を`2321.0.0`へ。依存解決を余分に更新しない |
| `README.md`、`starter/README_ja.md` | rc1基点の構成のまま、導入pinと版表記だけ更新 |
| `docs/migrate-to-uv_ja.md`、`docs/update-rollback_ja.md`、`docs/windows-install_ja.md`、`docs/python-examples_ja.md`、`PUBLISHING.md` | 現行版を示すrc1番号をstableへ同期。歴史の数字・fixtureまで一括置換しない |
| `docs/python-api-reference_ja.md` | 既存generatorで再生成し、版bannerだけ変わることを確認。metadata/API定義は変えない |
| `tests/test_b8.py`、`tests/test_b9.py` | current package版のアサーションだけ更新。`PROTOCOL == "23.2.1"`は維持 |
| CI配布物とmanifest | `minecraft_remote_api-2321.0.0-py3-none-any.whl`、`minecraft_remote_api-2321.0.0.tar.gz`。manifestのtag/source/digestは新candidateから生成 |
| Release本文/title | titleは`minecraft-remote-api 2321.0.0`。既存WireScope注意、最小移行案内、feedback導線 |

`test_release_workflow.py`中のrc1は過去caseの入力であり、本体のversion依存ではない。stable形式も既存guardが受理する。
同梱WireScope source、protocol定数、共有fixtureの版は更新しない。

工数見積もりは、版同期と差分確認1〜2時間、通常CI・build・配布物チェックの結果確認1〜2時間、Release本文と返却の整理1時間程度、合計0.5〜1人日。runnerやcoordinator/human ownerの待ちは別。10/29〜30の候補作成、10/31照合の予定に対応可能と見込む。

版metadataが変わるため、stableのwheel/sdistがrc1と同一bytesとは主張しない。凍結したstable candidateと公開物/PyPIのbytesを照合する。

#### 3. stableで変わる公開操作

- coordinatorの公開指示後、tag `v2321.0.0`を確定sourceへ固定。GitHubはpre-release OFF、draft OFF、Latestを明示的にON。
- Release workflowは同commitの成功CI artifactを昇格し、公開時に再buildしない。stable形式とpre-release OFFの整合guardは既存実装にある。
- [hostname-omitted] jobはrc1と同じ`pypi` environmentでhuman owner承認待ちにする。4 repoのGitHub公開とcoordinator照合が揃った後、human ownerが承認する。
- TestPyPIは現行workflowでは公開時に自動実行される。手動化parkの変更を今回持ち込まない。
- 公開後はexact pinに加え、対応Pythonのfresh環境で無指定の`pip install`／`uv add`が`2321.0.0`を選ぶことも確認。PyPI JSONのbytes/digest/yankをReleaseへ照合する。

#### 4. 11/1の見込みと止まっている点

- Python側で判明している実装blockerは無い。rc1 sourceと承認経路が残っており、上記見積もりで対応可能。
- 未完了はcoordinatorの候補作成指示、新source/artifactの凍結、rc2について予定された試験、4 repo公開後のPyPI承認、移行ページの準備。これらを自repoで完了したとは扱わない。
- rc2で問題が出た場合は11/7の予備日に従う。Python独自に対象source/APIを広げない。

### Python節への回答

#### 公開時に要る最小移行案内

対応Python（3.10以上）の新規環境では、stable公開後の無指定取得が新protocol版に変わることをRelease本文の上部へ書く。
旧protocolを続ける場合は、動作確認済みの1214系を明示する。PyPIで存在・non-yankedを確認した現行の例は次のとおり。

```bash
pip install "minecraft-remote-api==1214.10.13"
uv add "minecraft-remote-api==1214.10.13"
```

導入済み環境はlock/requirementsを保存する。新protocol版と旧protocolサーバーを混ぜず、新版へ移すときは対応Python/対応サーバーを選び、ペアリングし、建築原点・Y座標を1個のblockで確かめる。
11月中は旧`sb`が残り、latestは`sb-beta`。12月から旧protocolサーバーを止め、名前の役割が変わる予定を案内する。

リンクはRelease本文の版/接続説明の直後に「旧版から移行する方へ」を置き、knowledgeの`[provider-link-omitted]
このページは今回未開通確認なので、knowledgeが公開し、coordinatorが照合してからリンクを確定する。
既存のuv移行説明は`docs/migrate-to-uv_ja.md`にある。未commitの新ガイドへのリンクを公開済みとして使わない。

#### 11月中に強くする部分

| 内容 | 現在地／案 |
| --- | --- |
| pyenv/pip/Poetry→uv | 公開済み`docs/migrate-to-uv_ja.md`。版固定、lock退避、既存projectの移行を通して確認する |
| 旧protocol→23.2.1 | `docs/migrate-legacy-protocol_ja.md`は未commit草稿。setPlayer→pairing+dimension/origin、Yの加算、dict/BlockValue、block state/定数を扱う。実作品の前後比較で強化 |
| 更新/復帰 | 公開済み`docs/update-rollback_ja.md`。Python環境の復帰とworld変更の復元を分ける |
| 教材・particle・README再編 | 未commitの準備。最小移行案内と分けて、後続改善期へ。初回stableの試験条件にしない |
| WireScope観測開始/終了・接続詳細 | `2321.1.0`でPython優先。初回stableには実装を含めず、注意書きを引き継ぐ |

#### WireScope注意の継承

rc1 Releaseの本文をAPIで取得し、`wirescope=True`時の最初と最後の`input()`、ブラウザの接続code入力、Python process終了で配信終了、attach前の操作が表示されないことを継承する。
具体的な本文案は同packetの`stable-release-notes-draft_ja.md`。実装改善の完了やPython終了後の閲覧保証は主張しない。

#### starterと箱庭の12月の切替案

- 11月：`starter/param_mc_remote.template.py`の`[hostname-omitted]`を維持。READMEの案内も同じ。初回stableで箱庭名を変えない。
- 12月：安定版向けの配布templateとREADMEを`[hostname-omitted]`へ更新。beta版を案内する文書は`[hostname-omitted]`と`2330.0.0`のbetaを明記する。
- 利用者がコピー済みの`param_mc_remote.py`や保存credentialを自動書換えしない。移行ページから、接続先を確認して手元設定を変更し、必要なら再ペアリングする手順を案内する。
- 実施時期/切替済みの確認はcoordinator/Stackの返却と照合して決める。今回DNSやserverへ触っていない。

### 保存・後続

この確認票はdev側の返却物。正式なgate notes/evidenceのauthoring・採否はknowledge側。
packetは分類②、用途はstable coordinatorの確認・候補作成時の引継ぎ。knowledgeに必要な確認/観測事実が収容され、stable closeで後続状態が引き継がれた時点で整理可能。公開sourceや正式evidenceとして扱わない。
