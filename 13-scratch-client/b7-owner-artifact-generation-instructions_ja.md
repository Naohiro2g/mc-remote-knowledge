# b7 Scratch owner artifact生成指示書

> status: 実行待ち。coordinator参考buildを正式artifactとして使わず、Scratch ownerが生成して返却する。

## 目的

`scratch-editor`の統合済みdefault branchから、Scratch owner責任でb7のGUI、Bridge中間build、common WireScope artifactを
生成し、source commitとartifact bytesを結び付けてcoordinatorへ返す。coordinatorは返却identityの横断照合だけを行い、
不足artifactを自分で生成してowner artifactの代替にしない。

## 固定入力

- repository: `Naohiro2g/scratch-editor`
- branch: `develop`
- source commit: `773e2984132d82bb6e740d6458107fe42ef68a0a`
- tree: `e48fe82916ec82a5d05b216f50e353bcbf87a6f4`
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

- source `HEAD == origin/develop == 773e298…`、worktree clean
- fixture 20,367 bytes、指定SHA、93/93 unique、protocol配下`mcr.lightning` 0件
- GUI tarに`build/index.html`、`build/mc-remote-runtime-config.json`、`dist/scratch-gui.js`が存在
- WireScope manifestのsource commit、archive digest、toolchain、recipeが返却値と一致
- archive integrity検査PASS
- GUIのb6との差は、b6後のrelease-label修正`5df50144…`で説明できること。差分なしとは推測しない
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
