<!-- Sanitized copy for evidence handoff. -->

- 元資料: `2026-10-22-stable-python-candidate/materials/candidate_ja.md`。
- 元bytes: 11608、元SHA-256: `7d2a868ce7949b7cbb3b160c4158aa7c1de62cc548f2cca33019c9a46f561142`。
- 加工: provider URL 2箇所、hostname 8箇所、address 1箇所、local absolute path 0箇所を置換。その他の本文は保持。
- これは当時の返却票。公開前・承認待ちの記述は当時の状態であり、最終状態はpost-approval-provider-observation.jsonとclose分類票を参照。

---

# Python 初回stable候補の返却（2026-10-22）

## Release gate 確認票

- 対象 repo: `Naohiro2g/minecraft-remote-api`（Python client）
- 対象 branch/commit: `agent/stable-python-2321@fac0313ea9162dc0730412c53d665e6c42a93791`（remote push済み）。基点はrc1 tag `c30105349ef26413e925699143396ea05bd3e380`。mainは基点のまま。
- release / channel: `2321.0.0` stable候補。将来のtagは`v2321.0.0`。tag／Release／Latest／PyPIの公開操作は未実施。
- gate coordinator: knowledge担当session。横断判定はcoordinator／human ownerへ返す。
- human release owner: プロジェクトオーナー。
- current phase: OPEN、Python候補作成・identity返却。凍結／公開の指示待ち。
- contract maturity / required test tier: protocol `23.2.1`の公開contract。版番号だけの変更。通常CIと配布物検査を追加し、rc1の実機PASSを再利用する根拠を返す。
- knowledge contract path: `00-hub/stable-gate-work-instructions_ja.md`「共通」「Python client」、`00-hub/release-gate-notes_ja.md`初回stable節、`00-hub/DECISIONS_ja.md` `2026-10-22-01`〜`-06`。runtime／INDEXもremoteから確認。
- knowledge contract commit: `abf8130faf8637fe1167af35477ea97bca43c42a`（実読）。ユーザーの追記を含む版を使用。
- gate manifest identity: CI `manifest.json`は下表。横断exact setは未指定・未凍結。公開時のtag付与後のmanifest期待値も別記する。
- change cone: rc1から12ファイル・16箇所の`2321.0.0rc1`→`2321.0.0`だけ。package、lock、導入pin、生成API banner、版アサーション。全変更fileについて旧bytesへの同一置換と一致することを確認。
- reused PASS / rationale: rc1 CI `39067369316`（3.10〜3.13各784 PASS）、main CI `39216669184`、knowledge `14-evidence/records/2026-10-19-rc1-candidate-3os-live-human_ja.md`およびrc1公開・close照合。API／wire／認証／fixture／同梱WireScope／starter接続先／workflowの差分は無いため、rc1の実機観測を再利用する提案。新たな実機PASSは主張しない。
- exact compatibility set / freeze status: Python候補sourceは上記SHA、protocol `23.2.1`。同梱tooling source `6447f6e8cbfbeeb9d229990b5c4f6e82a5875666`。McRemote rc2／stableとの横断setはcoordinatorが固定する。
- target deployment / profile / lock: shared環境への接続・deploy・DNS変更は実施無し。PythonのWireScopeは従来のbrowser-loopback。starterは`[hostname-omitted]`を維持。
- authorized next action: 候補作成、branch push、通常CI、配布物照合、本文案と共通回答の返却まで完了。mainの更新、tag／Release／PyPI公開は次の明示指示を待つ。
- test class: unit/deterministic（今回）。live-humanはrc1の記録を参照。live-auto／live-humanの新規実施無し。
- 実行した command / 手順: rc1からclean worktree作成、版番号の限定置換、`uv lock --check`、API generator `--check`、`uv run --frozen --with pytest pytest -q`、CI workflow_dispatch、provider APIとartifact ZIPのSHA照合、wheel checker、wheel／sdist内部のmetadata・同梱pairのbytes比較、ホスト名の棚卸し、元作業treeの保存hash照合。
- 結果: ローカルPython 3.11.9で784 PASS。CI全5 jobs success（下表）。artifact provider digestと実取得ZIP一致。wheel／sdist metadataの版は`2321.0.0`、同梱pairとsource pinはrc1と一致。元の作業中19ファイルを保全。
- evidence record / artifact: CI run [39720157153]([provider-link-omitted])、artifact ID `12400618111`。本packetのprovider／source／package検査JSON、source patch、取得した生成物。正式evidenceへの収容はknowledge側。
- 未検証の境界: 新しい横断set／rc2との実機、Web新旧名前のTLS・routing・header・操作（Stack担当）、移行ページの公開、stable indexでの無指定取得、将来のRelease／PyPI公開後の照合。候補を公開済みとは扱わない。
- security / compatibility / rollback の確認: ユーザー設定・未commitの教材／README再編はcommitに含めない。local NOTES／CLAUDE／packetはignored。既存tagを変更しない。PyPIの既存human approvalを維持し、GitHub 4 repoのasset照合後にhuman ownerが承認する（11/1の手順）。
- 判定を求める事項: このsource／生成物を10/31の凍結対象にするか、Release本文案と下記の名前更新時期。Pythonから横断gateの合否は宣言しない。

## 1. 候補のidentity

- source: `fac0313ea9162dc0730412c53d665e6c42a93791`、branch `agent/stable-python-2321`。rc1から1 commit。
- CI run: `39720157153` / success。artifact名: `minecraft-remote-api-dist`。
- artifact ID: `12400618111`。取得ZIP `ci-artifact.zip`: **383,066 bytes**、SHA-256 `99f219aa6bead9984fdf0359d32ec72cadadcb3b5fd46221ffd7ffc42e96fa78`（provider digestと一致）。
- artifactのprovider有効期限: `2027-01-20T04:02:44Z`。本packetにも取得bytesを保存。

| file | bytes | SHA-256 |
| --- | ---: | --- |
| `manifest.json` | 668 | `47dd3820a8e75951df4a4e7d360cb7c3685921e137ebd5ee3feb1238416577b9` |
| `minecraft_remote_api-2321.0.0-py3-none-any.whl` | 196,033 | `a0c88b864c26e6e1a0ab2ef2248df6851cc9a3189af93579fbd50132d8c747a0` |
| `minecraft_remote_api-2321.0.0.tar.gz` | 190,248 | `a6feaec48ac5df1611208c42e7770d87e0a7bafe66794a39b30942f94140cb88` |

### 公開時のmanifest

候補の`manifest.json`は`release_tag: null`。既存release workflowはwheel／sdistを再buildせず、同じsourceの成功CIから昇格する。
manifestのみ既存の`jq --arg t v2321.0.0 '.release_tag = $t'`を通すため、公開時は次の期待値となる。

- 公開file名: `manifest.json`（本packetでは区別のため`release-manifest.expected.json`として保存）。
- **675 bytes**、SHA-256 **`229179c8274d54f06765bf2d717ae416f02742a99077acde09787ea6bd90ee4a`**。
- 変更は`release_tag`だけ。source、同梱source、wheel／sdist digestは候補版から維持。
- これは未公開の期待bytesであり、公開後にprovider assetと照合する。candidate manifestの668 bytesと取り違えない。

### 同梱WireScope（wheel／sdistの両方で確認）

- source: `Naohiro2g/minecraft-remote-tooling@6447f6e8cbfbeeb9d229990b5c4f6e82a5875666`。
- `wirescope-app.zip`: **83,854 bytes** / `da3da0b6cf4d05265bc0c11abaa4913208c7cfc3600b0c3e78c93a356fc431ad`。
- `wirescope-app.manifest.json`: **2,339 bytes** / `3dd668a236463809a4cdc6d19375f3e6d75eea0c8089a616d2b761d3a4a05235`。
- rc1のpairそのもの。wheel checker PASS、両archiveの内部bytesもrc1 sourceと一致。

## 2. 検証結果

| CI job | 結果 |
| --- | --- |
| test (3.10) | 784 passed in 4.61s |
| test (3.13) | 784 passed in 4.37s |
| test (3.11) | 784 passed in 4.58s |
| test (3.12) | 784 passed in 4.54s |
| build-candidate | build / API freshness / wheel checker PASS |

互換性test `tests/test_b1.py::test_rc1_client_accepts_compatible_hello_response[23.2.0]`も上記784件に含まれる（23.2.1 clientが23.2.0 serverのhello応答を受け入れるunit test）。実機での23.2.0 server接続を新規に行ったという意味ではない。

`source-checks.json`に変更fileと置換数、`source.patch`に全差分を保存。現在package版に依存しない`test_release_workflow.py`のrc1入力例やfixtureの歴史版は変更しない。
元mainのREADME再編、旧protocol移行ガイド、教材・作例、利用者の変更3ファイルはすべて候補へ混ぜていない。

## 3. 共通：WebのScratchとWireScopeの名前（2026-10-22-06）

### 生成物に名前が入るか

Pythonの追跡file全体、同梱ZIP内部、実際のwheel／sdistを調査した。
`[hostname-omitted]`、`[hostname-omitted]`は**0箇所**。`[hostname-omitted]`／`[hostname-omitted]`もPythonから開く先ではない。
Pythonは同梱WireScopeを`[address-omitted]`の動的portで配信し、そのloopback URLをブラウザで開く（`mc_remote/_wirescope_http.py`、`mc_remote/wirescope.py`）。
従ってWeb名のためにPython wheel／sdist／同梱ZIPを変更する箇所は無い。WebのDNS、TLS、Caddy、Bridge origin、runtime configはStack／tooling側の管理で、Python側では設定していない。

一方、Minecraft接続先の`sb-beta`はREADMEに1箇所あり、wheelのMETADATAに1箇所、sdistのREADME／PKG-INFOに各1箇所入る。
これはWebのWireScope URLではない。starter templateの接続先も1箇所ある（今回のwheel／sdistにはstarter templateは含まれない）。

### 二つのWeb名で同じ安定版を出すとき

Python側の変更・build工数は無し（棚卸しと返却だけ）。同梱pairの再生成・runtime URL切替は不要。
Web名二組の先行開通・証明書・header・ScratchからWireScopeの受け渡しの実操作はStackの返却事項。
11/1まで新しいWeb名へのリンクを増やさず、Stackの先行開通を公開済みの案内として扱わない。

### README／文書／作例の-beta棚卸しと時期

| 範囲（候補sourceの追跡file） | 箇所数 | 対応案 |
| --- | ---: | --- |
| READMEの`[hostname-omitted]` | 1 | `2321.1.0`で`sb`へ。12月の前に配布 |
| その他の文書／教材／examples内の-beta名 | 0 | 新たな置換無し |
| starter templateの`[hostname-omitted]` | 1 | Python節3に従いstableでは維持、`2321.1.0`で`sb`へ |
| Webの`scratch-beta`／`wirescope-beta`リンク | 0 | 変更不要 |
| templateを検査するtest内の`sb-beta` | 1 | starter更新と同じ`2321.1.0`で期待値を同期 |

文書・作例の集計はREADME **1 file／1箇所**、他0。設定template・testを含む全sourceでは**3 files／3箇所**。
棚卸しJSONは`source-checks.json`と`package-checks.json`。未commit草稿やローカルprivate設定は今回の候補の集計対象外。

## 4. Release本文案・starter・公開の扱い

本文案は`stable-release-notes-draft_ja.md`。
11/1に`sb`が新protocol stable、旧protocolは`sb-retro`（11月末まで）、11月中は`sb-beta`も同じstableと明記した。
旧版を続ける人には`==1214.10.13`の指定と`sb-retro`への変更、移行ページ`[provider-link-omitted]
`wirescope=True`について、接続完了前と観察終了までの`input()`、Python終了で配信が止まること、attach前の命令は表示されないことをrc1から継承。
starterの接続先は依頼どおり変更無し。初回stableの後のWireScope改善は`2321.1.0`の優先事項として持ち越す。

本依頼では候補branchとCI artifactだけを作成した。tag／Release／PyPIの公開、PyPI jobの起動・承認はしていない。
11/1の公開時はGitHub 4 repoのasset照合後にhuman ownerが[hostname-omitted]を承認する。

## 5. 保存と後続

このpacketは分類②。用途はcoordinatorの凍結前照合、公開時の同一bytes昇格、Release本文確定、後続への引継ぎ。
正式evidenceと必要生成物がknowledge等の指定先へ収容され、stable closeで後続（starter／名前、WireScope、教材）の引継ぎが済めば整理可能。
既存の確認票packetは履歴として保持するが、その旧11月の箱庭案は本票と`2026-10-22-04`で置き換わる。
元作業tree、既存分類②のarchiveはそのまま保持する。
