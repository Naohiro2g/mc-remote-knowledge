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
