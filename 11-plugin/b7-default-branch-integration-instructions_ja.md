# b7 default branch統合指示書（McRemote）

> status: 完了。`main@3d5f710db97f4b14613f7e0abaafd535701d1906`へstrict fast-forward済み。

## 固定入力

- knowledge: `95b1011126901898c538ad6c0b7c790a26268b88`
- default: `main@4e8f1ff1bd48bfa28c465f2dc24060fbb419317f`
- candidate: `agent/b7-live-gate-blockers@3d5f710db97f4b14613f7e0abaafd535701d1906`
- remote比較: candidateはdefaultに対して`+5 / -0`
- protocol／artifact: `23.1.0`／`2301.0.0b7`
- successor fixture SHA-256: `586d24bf40136eec31f1827f23ef5b317f15100a17a635d7fe9f165e0af40dce`
- live PASS JAR: 222,951 bytes、SHA-256
  `f08388cf393e02db1eb605e707dfaec890792e7a475de5a51caacbc940028ee9`

## 実行

dirtyな既存worktreeを変更、stash、cleanしない。隔離worktreeで作業する。

1. `origin/main`とcandidate branchをfetchする。
2. `origin/main`が固定SHAのままで、candidateがstrictly aheadかつbehind 0であることを再確認する。
3. candidateのclean checkoutでPaper 1.21.11全suite、clean build／JAR、fixture 93 cases、method registry、
   `mcr.lightning` production残存0件、`git diff --check`を再実行する。
4. 可能な範囲でPaper 26.2／Java 25 compatibility pulseを再実行する。
5. merge commit、squash、cherry-pick、内容編集を行わず、`main`をcandidate commitへfast-forwardしてpushする。
6. push後の`origin/main`がexact candidate SHAであることを確認する。
7. 統合後mainのclean checkoutからJARを再生成し、filename、bytes、SHA-256を返す。live使用JARとの同一／差分を明記する。

作業前の`origin/main`が固定SHAから動いていた場合は停止し、現在SHAとahead／behindを返す。自動rebaseしない。

## 統合しないもの

- `agent/b7-live-auto-runner@51f4304da0c6bbf7185454644807729faca4b3c3`
- coordinatorがgate stagingへ置いたtargeted runner
- probe source／JAR、private runtime、raw log、pairing情報
- Stack設定、shared server、tag、GitHub release

live runner branchは旧`mcr.lightning`前提のREADMEと今回不要な広いscenarioを含むため、product mainへ混ぜない。
runner改善を保存する場合はb7 release後の独立tooling changeとして再設計する。

## 返却

- integration前後の`origin/main` SHA
- candidateとのfast-forward／tree一致
- 全検証結果とtest件数
- 統合後main生成JARのfilename／bytes／SHA-256
- protocol／artifact／fixture／method registry identity
- local HEADとremote SHA一致、clean隔離worktree
- deploy、tag、releaseを行っていないnon-claim
