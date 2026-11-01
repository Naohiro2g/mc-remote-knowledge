<!-- Sanitized copy for evidence handoff. -->

- 元資料: `2026-10-31-stable-python-release/materials/release-return_ja.md`。
- 元bytes: 4793、元SHA-256: `4759bd6646e84898de3fbecbb04444274af08f321bf94e48545f78459ec47368`。
- 加工: provider URL 2箇所、hostname 2箇所、address 0箇所、local absolute path 1箇所を置換。その他の本文は保持。
- これは当時の返却票。公開前・承認待ちの記述は当時の状態であり、最終状態はpost-approval-provider-observation.jsonとclose分類票を参照。

---

# Python 2321.0.0 stable公開の返却（2026-11-01）

## 公開結果

- 実読knowledge: 指定の`9dee6881a414a2b1fd4a37fa4fe26ddbedd9d8a5`と、実行時最新の`10fe11cfd437ab45f8c000517595598229e1011e`。両方の`00-hub/stable-gate-release-instructions_ja.md`「共通」「Python client」は同じ指示。runtimeは実行時最新を実読。
- main: **`fac0313ea9162dc0730412c53d665e6c42a93791`**。`c30105349ef26413e925699143396ea05bd3e380`からfast-forward。force無し。
- tag: **`v2321.0.0` → `fac0313ea9162dc0730412c53d665e6c42a93791`**。GitHub APIで照合。
- Release: [provider-link-omitted]
- Release ID: **430008193**。draft=false、prerelease=false。`/releases/latest`のIDも一致。
- 公開時刻: **2026-11-01 00:10:17 JST**（2026-10-31T15:10:17Z）。開始許可の11/1 00:00以降。
- main CI: **41213013218** / success。artifact **13045859840**、digest `sha256:44c974b45846efe16b8fbb3c5c97f7956d8103c562fc01ec49ca909c52843024`。
- Release run: **41213563824** — [provider-link-omitted]
- job結果: `promote` success、`prepare-publication` success、`publish-testpypi` success、**`publish-pypi` waiting**。workflow全体はwaiting（意図した承認待ち）。
- [hostname-omitted]: pending_deploymentsのenvironment=`pypi`、required reviewer=`Naohiro2g`を確認。**承認していない**。coordinatorのGitHub 4 repo照合後にhuman ownerが承認する。
- 観測時刻: 2026-10-31T15:12:41.460481+00:00。自repoでのasset照合の結果を返すもので、coordinatorの横断照合を代行したとは扱わない。

## 公開assetと凍結値の照合

| file | bytes | SHA-256 | 凍結値 |
| --- | ---: | --- | --- |
| `manifest.json` | 675 | `229179c8274d54f06765bf2d717ae416f02742a99077acde09787ea6bd90ee4a` | 一致 |
| `minecraft_remote_api-2321.0.0-py3-none-any.whl` | 196,033 | `a0c88b864c26e6e1a0ab2ef2248df6851cc9a3189af93579fbd50132d8c747a0` | 一致 |
| `minecraft_remote_api-2321.0.0.tar.gz` | 190,248 | `a6feaec48ac5df1611208c42e7770d87e0a7bafe66794a39b30942f94140cb88` | 一致 |

3件ともGitHub provider digestと、公開assetを実際にdownloadしたbytes／SHA-256の両方を照合した。
公開前にもmain CI artifactを取得して同じ凍結値へ照合してからtag／Releaseを作成した。
release workflowは同sourceの成功CI artifactを昇格し、release時の再buildは無し。
manifestは既存の手順で`release_tag`だけを`v2321.0.0`へ設定し、凍結した675 bytesと一致。

## 本文・source・作業保全

- 本文は候補の案を基に、protocol 23.2.1、API／通信はrc1と同じ、移行ページ、旧1214.10.13 pinとsb-retro、feedback、`wirescope=True`の起動直後と観察終了時のinput待ちを掲載。
- 無指定の導入については「[hostname-omitted]への公開後」と記載し、GitHub公開からPyPI承認までの間も公開済みと誤案内しない。
- sourceは版番号だけの凍結candidate。教材／README再編／editable改善／作業セッション設計を混ぜていない。
- 元workspaceは**`work/local-drafts-before-stable-2321@c301053`**へ移して未commit変更26 filesを保全。保存済みhashとの一致を確認。利用者設定をcommitしていない。
- clean main worktreeは`[local-path-omitted]`、main@fac0313。mainへ統合済み、公開tagも同SHA。候補branchはclose時の整理まで保持。

## 検証と残る境界

- class: unit/deterministicおよびprovider／配布物のidentity照合。main CI成功、公開前・公開後のfile照合、main/tag/Latest/保護設定確認。
- rc1の既存実機PASSを版番号のみのchange coneで再利用する方針を継承。今回新たなMinecraft実機・live-human・shared deployはしていない。
- 同梱WireScopeのsource pinは`6447f6e8cbfbeeb9d229990b5c4f6e82a5875666`のまま。公開manifestにも同値。
- 残るのはcoordinatorの横断asset照合、human ownerによるPyPI承認、その後のPyPI配布物・無指定取得の照合。agentからPyPI承認や手動uploadを行わない。
- 正式evidenceの採否・収容はknowledge側。本packetは②、正式収容とstable closeで引継ぎが済むまで保持。

## 素材

- `published-identity.json`: main/tag/Latest/asset実download／workflow／pending deploymentのAPI観測。
- `main-ci-artifact.json`: 公開前に照合したmain CI artifactのprovider identity。
- `published-release-created.json`: Release作成APIの返却。
- `../published-assets/`: 実際に公開URLから取得した3件。`../assets/`の凍結bytesと一致。
- `release-body_ja.md`と`release-request.json`: 掲載本文と実行した要求。
