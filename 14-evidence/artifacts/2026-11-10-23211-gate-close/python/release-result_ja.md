# Python 2321.1.0 公開の返却（PyPI.org承認待ち）

- 実際に読んだknowledge commit: `2f337180c919a80aa80200e9f9d959d64812543e`
- knowledge contract path: `00-hub/23211-gate-release-instructions_ja.md`「共通」「Python client」
- 開始の許可: human ownerの2026-11-09「これで進めてください」。
- この票はPython担当の実施結果。横断gateの最終判定ではない。

## 共通の返却項目

- repo: `Naohiro2g/minecraft-remote-api`
- 既定branch: `main`
- mainの新しい先頭SHA: `09bbda421645235b2433a6c205d528be15a49f34`（`fac0313ea9162dc0730412c53d665e6c42a93791`からfast-forward。新規commitなし）
- tag: `v2321.1.0`（annotated）
- tagが指すcommit SHA: `09bbda421645235b2433a6c205d528be15a49f34`
- annotated tag object SHA: `4cbe70d859a0f06b34304bb24e42f170480e1bf1`
- Release URL: https://github.com/Naohiro2g/minecraft-remote-api/releases/tag/v2321.1.0
- Release ID: `438500924`
- Release title: `minecraft-remote-api 2321.1.0`
- 公開時刻: 2026-11-09 05:27:02 JST
- `prerelease=false`、`draft=false`、Latest。`v2321.0.0`のtagとReleaseは残した。
- PyPI.org: [run 42520379366](https://github.com/Naohiro2g/minecraft-remote-api/actions/runs/42520379366)の`publish-pypi`（job `128852424758`）がenvironment `pypi`の**承認待ち**。agentは承認を送っていない。coordinatorによるRelease asset照合の後にhuman ownerが承認する。

### RunとRunner Image

jobのログの`Runner Image` groupから取得。`Runner Image Provisioner`の版とは区別した。

| run / job | run ID | job ID | Runner Image | Version |
| --- | --- | --- | --- | --- |
| 凍結候補 CI / build-candidate | `42227543303` | `127924972337` | `ubuntu-24.04` | `20261101.360.1` |
| main CI / build-candidate | `42520098818` | `128851583998` | `ubuntu-24.04` | `20261101.360.1` |
| 公開 / prepare-publication | `42520379366` | `128852384418` | `ubuntu-24.04` | `20261101.360.1` |
| 自動公開 / promote | `42520175969` | `128851745614` | `ubuntu-24.04` | `20261101.360.1` |
| 自動公開 / publish-testpypi | `42520175969` | `128851839415` | `ubuntu-24.04` | `20261101.360.1` |
| 公開 / publish-pypi | `42520379366` | `128852424758` | 未割当（承認待ち） | 未割当 |

該当ログの抜粋を`runner-image-*.txt`へ収容した。

### 公開assetと凍結値との照合

最終的に公開された3 assetをGitHubから再取得し、file本体のbytesとSHA-256を計算して照合。providerのasset digestも一致。

| file | bytes | SHA-256 | 凍結値との照合 |
| --- | ---: | --- | --- |
| `manifest.json` | 675 | `460f1558135dbf3e8095bbc8133946641a5eff61ab5f13db3deeb8c693b7c614` | PASS: release_tag only |
| `minecraft_remote_api-2321.1.0-py3-none-any.whl` | 196,026 | `ee80d81be4128f8e2327646f607fbc46053bec91a527eb9140f54c9dc9d6a26f` | PASS |
| `minecraft_remote_api-2321.1.0.tar.gz` | 190,241 | `2d49d096eb30c8721627f8d8f878551396a8f0d298466a007ce1b71559e255d9` | PASS |

- 凍結元: CI `42227543303` / artifact `13507135196`、outer ZIP 383,489 bytes / SHA-256 `3c35499f479bfe0874ef7ddb4e2b04a349cf0118df3efab9a2d8dbdf42c12177`。再取得してprovider digestとfile本体を照合した。
- 候補の`manifest.json`: 668 bytes / SHA-256 `8f361f8b54b1deba76b4105da50acf472e56dbe0d27fd5bd006eefd1bf214d05`。
- 公開manifestと候補manifestをJSONで比較し、差分は**`release_tag: null → v2321.1.0`だけ**。source commit、同梱WireScope source、両artifactのfile名とSHA-256は不変。
- 同梱WireScope source: tooling `6447f6e8cbfbeeb9d229990b5c4f6e82a5875666`のまま。

## 公開経路で起きたこと

1. 編集済みの本文を使い、Protocol `23.2.1`、公開API・通信が`2321.0.0`と同じことを明記し、手順で必須のfeedbackリンクを追加した。E1とWireScopeの段落は載せなかった。
2. TestPyPI自動送信を避ける目的でRelease workflowを一時停止し、凍結元artifactの3 fileを添付して公開、workflowを復帰した。しかし停止・復帰では公開イベントの自動runを防げなかった。
3. 自動run `42520175969`は`promote`、`prepare-publication`、`publish-testpypi`に成功した。`promote`はmainのpushで動いたCI `42520098818`を選んでいた。そのartifact `13632502854`（outer digest `sha256:da0ef925eb8959218951d2d0dde0f0d5111615a35e36befbb280277ede75563b`）も取得し、wheel・sdist・候補manifestの**全bytesが元の凍結artifactと同じ**ことを確認した。
4. TestPyPIへも送信された。TestPyPIの2321.1.0 metadataを取得し、file2件のbytesとSHA-256が凍結値と一致し、yankされていないことを確認した。公開済みのfileは残している。
5. 自動runの承認待ちPyPI jobを含む重複runをcancelし、run全体の`conclusion=cancelled`を確認した。`channel=pypi`を明示して起動したrun `42520379366`だけを承認待ちに残した。このrunの`prepare-publication`はsuccess、`promote`と`publish-testpypi`はskipped。
6. 最終的なGitHubの3 assetを再度取得して、上表の凍結値と一致することを確認した。Release workflowは`active`に復帰している。PyPI environmentの保護設定と公開workflowのsourceは変更していない。

## Release本文

公開本文は`release-body_ja.md`。868 bytes / SHA-256 `8ed23a8b45113d83f29a479f5149529080a405c3137d764fdb87e1c359f3f14d`。GitHub APIから取得した本文とも一致。
feedback: https://github.com/Naohiro2g/mc-remote-knowledge/issues/new?template=feedback.yml

## 残っていることと作業状態

- coordinator: GitHub Release assetと凍結値の照合。
- human owner: coordinatorの照合が済んでから、run `42520379366`のenvironment `pypi`を承認する。agentは承認しない。
- 承認後のPyPI.org公開・file照合は未実施。今回の返却時点は承認待ち。
- この作業では実サーバーのdeploy、人間参加試験、横断gateのcloseは行っていない。
- mainの作業場所`/tmp/mcr-stable-release-main`はclean。candidate/E1のbranchはmainへ統合済みの祖先として保持し、削除していない。
- 元のroot作業場所の未commit 26 filesは作業開始時のSHA-256と一致。教材・README草稿・WireScopeのローカル修正は取り込んでいない。
- candidate搬送素材は引き続き`handoff-materials/2026-11-06-python-2321-1-candidate/`へ保持。今回の公開packetもrelease closeで分類する。
