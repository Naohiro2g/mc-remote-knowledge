# GitHub Actionsのrunnerのimageの版をそろえる依頼

> GitHubは、`ubuntu-latest`のlabelを2026-10-19から数週間かけてUbuntu 26.04へ移している。移し終えるのは2026-11-19の予定
> （actions/runner-images#14748）。`2321.1`の配布物は、どれも`ubuntu-24.04`のimage（`20261101.360.1`）で作った。human ownerの方針
> （2026-11-07、hub NOTESの「GitHub Actionsのrunnerのimageの版を指定する」の行）は、`2321.1`のgateを閉じた後に、全componentの
> workflowを`ubuntu-24.04`の指定にそろえ、`windows-latest`と`macos-latest`も一緒に扱う、というもの。26.04へは、時期を決めて
> 全componentを一度に移す（たとえば`2400`の準備の中）。`2321.1`のgateは2026-11-10に閉じた。参照するknowledge commitは、この
> 依頼が入ったmainのcommitです。各担当は、「共通」と自分の節を読んでください。

## 共通

- 対象：自repoの`.github/workflows/`のすべてのworkflowの`runs-on`。matrixの値や、reusable workflowの入力で渡しているものも含む
- `ubuntu-latest`は`ubuntu-24.04`にする
- `windows-latest`と`macos-latest`は、今それが指しているimageの版の名前にする（たとえば`windows-2025`）。直近のrunのlogの
  「Runner Image」の`Image:`の行で確かめる。版を上げたり下げたりしない
- すでに版を指定しているlabelは変えない。返却に、そのlabelを書く
- ほかの変更（actionsの版、toolの版、job名、workflowのfile名）は混ぜない
- 既定のbranchへのPRにして、CIが通ることを確かめる。CIが通ったら、担当がmergeしてよい（human owner 2026-11-10）。tag、Release、
  公開のworkflowの実行はしない
- 返却：
  - 変えたfileと`runs-on`の前と後
  - `windows`と`macos`の版を選んだ根拠のrun（run IDと`Image:`の行）
  - PRの番号、merge commit、mergeの後のCIのrun ID（どのjobも`Runner Image`の行）
  - `-latest`が残るところと、その理由
  - workflowが無いrepoは、無いと書く

## McRemote

共通のとおり。

## Python client

共通のとおり。PyPI.orgのtrusted publishingはworkflowのfile名とenvironmentの名前で結びついているので、どちらも変えない。

## Scratch editor（WireScope、minecraft-remote-tooling）

共通のとおり。scratch-editorとminecraft-remote-toolingの両方を返す。arm64のimageを作るjobがarmのrunnerを使っていれば、そのlabelも
返す。

## Stack（mc-remote-stack）

共通のとおり。

## Java client、TypeScript client、C# client

それぞれ共通のとおり（`minecraft-remote-java`、`minecraft-remote-typescript`、`minecraft-remote-csharp`）。

## knowledge

coordinatorが、この依頼と同じcommitで`.github/workflows/knowledge-checks.yml`の`ubuntu-latest`を`ubuntu-24.04`にした。

## coordinatorがすること

- 各担当の返却を、GitHubのAPI（PR、merge commit、CIのrunのRunner Image）で照合する
- 全componentが着地したら、hub NOTESの行を閉じる。26.04へ移る時期は、別に決める

## 返却と照合（2026-11-10）

7担当、8つのrepoが既定のbranchへmergeした。coordinatorがGitHubのAPIで、PRの差分、merge commitと既定のbranchの先頭、
merge commitで動いたCIのrunと、各jobのlogの「Runner Image」を確かめた。McRemote、Python、Scratch、Stack、C#の返却は、knowledge
`86a4ce2431696a6c8a699b75058ea0d07fa916bd`を読んだ。Java、TypeScriptの返却の本文は各repoの手元のNOTESにあり、coordinatorはAPIだけで
照合した。

| 担当 | repo | PR | merge commit | merge後のCI | Runner Image（全job） |
| --- | --- | --- | --- | --- | --- |
| McRemote | McRemote | #14 | `713fb7dff4d170ddc788f581fb9e6d8caf68cf0d` | run 42659959329（Build、手動） | 7 job：`ubuntu-24.04`（`20261101.360.1`）3、`windows-2025-vs2026`（`20261103.298.1`）2、`macos-26-arm64`（`20261102.0473.1`）2 |
| Python | minecraft-remote-api | #12 | `d59a0ec9d890ef6f5a6bf3b42348bcfd447b38e3` | run 42658873838 | 5 job：`ubuntu-24.04`（`20261101.360.1`） |
| Scratch | scratch-editor（既定は`develop`） | #31 | `24876896e8f47245dff43be336a0eaf5899e3436` | run 42664658122 | 10 job：`ubuntu-24.04`（`20261101.360.1`）。報告用のcheck 1件はrunnerを使わない |
| Scratch | minecraft-remote-tooling | #3 | `df61e589aa994d4c65b2a2cdc9a4d4cbc0721b2b` | run 42660197216 | 1 job：`ubuntu-24.04`（`20261101.360.1`） |
| Stack | mc-remote-stack | #88 | `eb19fd2c9b72e8a177d5aa8c9a3945b51153fd7f` | なし | なし |
| Java | minecraft-remote-java | #1 | `f5ffc06e315bc93ced42c43590aa34025599641d` | run 42659931547 | 2 job：`ubuntu-24.04`（`20261101.360.1`） |
| TypeScript | minecraft-remote-typescript | #1 | `60f759a994daf9350357e542adccc8331a939273` | run 42683327101 | 1 job：`ubuntu-24.04`（`20261101.360.1`） |
| C# | minecraft-remote-csharp | #1 | `534e422e4894d43d377b71c77068d2c391e0ca05` | run 42659108229 | 1 job：`ubuntu-24.04`（`20261101.360.1`） |

- 差分はrunnerのlabelだけ：McRemote 2 file（matrixの3つのlabelと`runs-on` 2か所）、Python 2 file・6か所、Scratch 12 file・17か所、
  tooling、Stack、Java、TypeScript、C#は1 file・1か所。PRのCIはどれも成功した（Stackを除く）
- `windows`と`macos`はMcRemoteだけ。根拠のrunは42519567217（source `5b78ded`）で、job 128849885498が`windows-2025-vs2026`
  （`20261103.298.1`）、job 128849885704が`macos-26-arm64`（`20261102.0473.1`）。macOSのlabelは`macos-26`にした
- 前から版を指定していたlabelは、どのrepoにも無かった
- 既定のbranchのworkflowの`runs-on`に`-latest`は残っていない（coordinatorが全workflowを読んだ）。Scratchの
  `request-copilot-review.yml`が呼ぶ本家のreusable workflow（SHAで固定）は、その中で`ubuntu-latest`を使う。自repoからは変えられない
- 公開のworkflow（McRemoteの`promote`、Pythonの公開の4 job、Scratchの`publish.yml`など、Stackの`publish-temurin-paper-runtime.yml`）は
  動かしていない。labelは差分で確かめただけ
- Stack：PRとpushで動くCIが無い。Stack担当はlocalの検査（pytest 629 passed、ruff）の後、human ownerの「続けて」でmergeした
- Scratch：PRのhead `79a34d4`の`pull_request_target`のrun 3件が`startup_failure`（Signature Assistant 42658685761と42664659196、
  Debug Info 42658687405）。返却は2件を挙げ、mergeの時の1件（42664659196）を含まない。このPRの前の同じeventは成功かskipだった
  （たとえば2026-11-07の42328588600）。原因は未確定（hub NOTESの行）。mergeの後のDebug Info（push、workflow_run、schedule）は
  `ubuntu-24.04`で成功した
