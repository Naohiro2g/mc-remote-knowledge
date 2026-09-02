# b7 Scratch owner artifact生成指示書

> status: **set 2完了・identity確認済み**（coordinatorがlocal staging bytes／SHA-256を照合、一致）。human release ownerが2026-09-02、ScratchおよびWireScopeをb7 release対象と明示決定し、
> 「fixture ownerのみ・runtime非参加」としたset 1後の判断（`b7-release-coordination-handoff_ja.md`／
> `b7-artifact-candidate-record_ja.md`§9）を撤回した。Scratch担当はこの決定後、direction／lightning learner block実装を
> 完了し、coordinatorがremote identityを照合済み（下記§0）。set 1（`773e2984…`ベース、機能実装なし）の記録は
> 履歴として残すが、b7 artifact生成の入力にはしない。

## 0. Coordinatorが確認済みのcandidate lineage（identity照合のみ、実装内容は未評価）

```text
develop@773e2984 (fixture owner commit、旧set 1の入力)
└─ 57e2885016  fix(mcremote): align scratch client b7 version
   └─ 3d5142f208  feat(mcremote): add b7 direction and lightning blocks
      └─ 31ca03ceed  fix(mcremote): finalize b7 scratch release identity
         └─ 0be46fcfa  feat(wirescope): observe b7 direction and lightning  ← 現行push済みHEAD
```

- branch: `agent/b7-scratch-wirescope`
- HEAD: `0be46fcfaca409a5ede10f592520d93e7c59ba15`（origin一致、coordinatorが`git ls-remote`で確認済み）
- 773e2984および57e2885が0be46fcfaの祖先であることをcoordinatorが`merge-base --is-ancestor`で確認済み
- fixture `mc-remote/protocol/test/fixtures/direction-lightning-v23.1.json`はこのcommitでも20,367 bytes／
  SHA-256 `586d24bf40136eec31f1827f23ef5b317f15100a17a635d7fe9f165e0af40dce`で不変（coordinator確認済み）
- 誤branch`agent/b7-client-version-followup@57e28850…`は独立branchではなく、このlineageの一部として
  必要な祖先に位置する。単独採用・破棄のいずれも行わず、そのまま使う（[`b7-client-version-followup-instructions_ja.md`](b7-client-version-followup-instructions_ja.md)はこの指示で superseded）

## 目的

`scratch-editor`のb7実装lineage（上記0）から、Scratch owner責任でb7のGUI、Bridge中間build、common WireScope
artifactを生成し、source commitとartifact bytesを結び付けてcoordinatorへ返す。coordinatorは返却identityの
横断照合だけを行い、不足artifactを自分で生成してowner artifactの代替にしない。

## 固定入力

- repository: `Naohiro2g/scratch-editor`
- branch: `agent/b7-scratch-wirescope`（develop統合は今回の前提にしない。統合はgate close時に別途判断）
- source commit: `0be46fcfaca409a5ede10f592520d93e7c59ba15`
- protocol: `23.1.0`
- artifact version: `2301.0.0b7`
- fixture: `mc-remote/protocol/test/fixtures/direction-lightning-v23.1.json`
- fixture SHA-256: `586d24bf40136eec31f1827f23ef5b317f15100a17a635d7fe9f165e0af40dce`
- fixture ledger: 93/93 unique ID
- knowledge: この指示書を含むcommit

既存のdirty worktreeを変更、stash、cleanしない。exact remote commitの隔離checkoutで実行する。

## 実行範囲

1. remote `develop`が固定commit／treeと一致することを確認する。
2. lockfileどおり依存を取得し、Node／npm versionを記録する。
3. `@mc-remote/protocol`のlint、Prettier、test、buildを実行する。
4. `@mc-remote/bridge`のlint、Prettier、test、buildを実行する。
5. `@mc-remote/live`のlint、Prettier、testを実行し、`--source-commit`へ固定40桁SHAを渡して
   `wirescope-app.zip`とdetached manifestを生成する。
6. repositoryの正式なroot production build経路でScratch GUIを生成する。workspace単体を依存workspace未buildのまま
   直接起動しない。
7. GUIの`build/`と`dist/`を次の決定論的条件で一つのtar.gzへ梱包する。
   - entry順をnameでsort
   - mtime `UTC 1980-01-01`
   - owner／group `0`、numeric owner
   - gzip headerへ生成時刻／元filenameを入れない
8. Bridge `dist/`も同じ決定論的条件で中間tarへ梱包する。ただしこれは`ws`を含む単独release artifactではない。
9. 成果物をowner管理のdurable local stagingへcopyし、mode `0444`、copy後size／SHA-256を再確認する。

## 生成物

- `scratch-gui-build-b7.tar.gz`（`build/`と`dist/`を含む）
- `mc-remote-bridge-dist-b7.tar.gz`（中間入力、release artifactではない）
- `wirescope-app.zip`
- `wirescope-app.manifest.json`

coordinatorが作成した
`/home/tsuji/.local/share/mc-remote/gates/b7-integrated-artifact-input-1/`のfileをcopy、再label、入力比較元として
使わない。owner自身のexact checkoutから独立生成する。

## 必須照合

- source `HEAD == origin/agent/b7-scratch-wirescope == 0be46fcfaca409a5ede10f592520d93e7c59ba15`、worktree clean
- fixture 20,367 bytes、指定SHA、93/93 unique、protocol配下`mcr.lightning` 0件
- GUI tarに`build/index.html`、`build/mc-remote-runtime-config.json`、`dist/scratch-gui.js`が存在
- WireScope manifestのsource commit、archive digest、toolchain、recipeが返却値と一致
- archive integrity検査PASS
- GUIのb6（set 1相当）との差は、b7 direction／lightning learner block実装（`3d5142f2`）とWireScope観測対応
  （`0be46fcfa`）で説明できること。差分なしとは推測しない
- Bridge tar／WireScope ZIPがb6と一致した場合も、実測digestとして返し、再利用をcoordinatorに推測させない

## 返却

- source branch／commit／tree、remote一致、clean状態
- Node／npm versionと実行command
- protocol／Bridge／WireScope／root buildの結果とtest件数
- 四成果物のowner staging path、filename、bytes、SHA-256、mode
- fixture path／bytes／SHA-256／case数
- WireScope manifest内のsource／archive identity
- b6 artifactとのbyte比較結果と、異なる場合のsource changeによる説明
- dependency audit等の警告。自動fixしていないこと
- source変更、commit、push、tag、release、OCI、Pages、shared deployを行っていないnon-claim

## 禁止する拡張

artifact生成中にsource、lockfile、version、runtime config、fixtureを修正しない。`npm audit fix`、依存更新、GUI UX修正、
Protocol owner移管、Python bundled WireScope更新、OCI push、tag／releaseを混ぜない。生成不能またはidentity不一致なら、
原因と観測値を返して停止する。

## Set 2結果

owner staging `b7-scratch-owner-artifact-set-2`（coordinatorがlocal filesystemでbytes／SHA-256照合済み、
一致）。source `agent/b7-scratch-wirescope@0be46fcfaca409a5ede10f592520d93e7c59ba15`。

| artifact | bytes | SHA-256 |
| --- | ---: | --- |
| `scratch-gui-build-b7.tar.gz` | 234,651,616 | `d6a569f1f315ca06a24f9d7a987129e824f5df60eb32d226dd6d776f47d20b8c` |
| `mc-remote-bridge-dist-b7.tar.gz` | 3,052 | `11199a8e6966e8a5160411104934498657f4befd3d27a8fc25c88f51afa31c72` |
| `wirescope-app.zip` | 79,418 | `98d684dc15f369f6568d249357d8fd3af11893859d3c07c2554295df19a263b8` |
| `wirescope-app.manifest.json` | 2,321 | `7498e32150884aec8c3d562b454d8b042032aa21893ae7fe886c06df2baf028f` |

fixture 20,367 bytes／93 cases／SHA-256 `586d24bf40136eec31f1827f23ef5b317f15100a17a635d7fe9f165e0af40dce`不変。
test: Protocol 28/28、Bridge 30/30、WireScope 134/134、GUI unit 476passed/1skipped、integration
127passed/7skipped、Playwright 8/8。Bridge tarはset 1とbyte一致（source変更なし）、GUI tar／WireScope ZIPは
b7 block実装・observer allowlist追加分で増分。source変更／新規push／develop変更／tag／release／OCIなし。

## Set 1結果（履歴。b7 artifact生成の入力には不採用）

owner staging `b7-scratch-owner-artifact-set-1`へ四成果物を生成し、source／tree、size／mode／digest、archive inventory、
WireScope manifest、fixture、test／build結果をcoordinatorが再buildなしで照合した。返却値は一致した。

`MCREMOTE_CLIENT_VERSION=2300.0.0b6`は当時の実Scratch Clientのprotocol 23.0.0／b6 surfaceと整合していた。これをb7
blockerとした後続判断（version文字列だけの`57e28850…`）は撤回済み。その後human release ownerがScratch／WireScopeを
b7 release対象と確定し、Scratch担当がdirection／lightning learner blockを実装（`3d5142f208`〜`0be46fcfa`）したため、
set 1はbuild健全性の参考としてのみ保持し、set 2がb7 artifactの正式生成対象となる。
