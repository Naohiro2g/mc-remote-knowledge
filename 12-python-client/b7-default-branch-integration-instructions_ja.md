# b7 default branch統合指示書（Python）

> status: 完了。`main@8f4bc4b96ae74fb5370a3d804676cd07e5352346`へstrict fast-forward済み。

## 固定入力

- knowledge: `95b1011126901898c538ad6c0b7c790a26268b88`
- default: `main@ddcdc9da431aab7102867e103478469dda567e6f`
- candidate: `codex/b7-permission-contract-followup@8f4bc4b96ae74fb5370a3d804676cd07e5352346`
- remote比較: candidateはdefaultに対して`+3 / -0`
- protocol／package: `23.1.0`／`2301.0.0b7`
- successor fixture SHA-256: `586d24bf40136eec31f1827f23ef5b317f15100a17a635d7fe9f165e0af40dce`
- candidate wheel SHA-256: `cc5842b79501fd103f1e7d2e3a4ea1cc72029e6969265591f60c9324338d3094`
- candidate sdist SHA-256: `6be3db058cc1aff7cf5375b58dc11737e5d471f0f67a6cdaa28a869d0c12c236`

## 実行

dirtyな既存worktreeを変更、stash、cleanしない。隔離worktreeで作業する。

1. `origin/main`とcandidate branchをfetchする。
2. `origin/main`が固定SHAのままで、candidateがstrictly aheadかつbehind 0であることを再確認する。
3. candidateのclean checkoutでtargeted 48件、全253件、lint／format、`uv lock --check`、sdist／wheel build、
   METADATAを再検証する。
4. fixture digest、93/93 unique ID、`mcr.lightning`残存0件を再確認する。
5. merge commit、squash、cherry-pick、内容編集を行わず、`main`をcandidate commitへfast-forwardしてpushする。
6. push後の`origin/main`がexact candidate SHAであることを確認する。
7. 統合後mainのclean checkoutからwheel／sdistを再生成し、bytes／SHA-256を返す。candidate artifactとの同一／差分を
   明記する。

作業前の`origin/main`が固定SHAから動いていた場合は停止し、現在SHAとahead／behindを返す。自動rebaseしない。

## 不変条件

directionのimmutable 3-tuple、server reason透過、`strikeLightningEffect` aliasなし、自動retryなし、hello permission
snapshotをclientが再解釈しない境界を維持する。API、README、starter、observerへ統合時だけの修正を追加しない。

## 返却

- integration前後の`origin/main` SHA
- candidateとのfast-forward／tree一致
- targeted／全回帰／lint／format／lock／build／metadata結果
- 統合後main生成wheel／sdistのfilename／bytes／SHA-256
- fixture identityと93 case ledger
- local HEADとremote SHA一致、clean隔離worktree
- 実plugin live、tag、GitHub release、PyPI公開を行っていないnon-claim
