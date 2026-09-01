# b7 default branch統合指示書（Scratch protocol owner）

> status: 実行可。fixture ownerを`develop`へ着地する。tag／releaseは禁止。

## 固定入力

- knowledge: `95b1011126901898c538ad6c0b7c790a26268b88`
- default: `develop@5df50144da13b1a1c8c23b01f2d0138ffd17b953`
- candidate: `agent/b7-permission-fixture-amendment@773e2984132d82bb6e740d6458107fe42ef68a0a`
- candidate parent chain: `607cda40588ec4579c503d457c3784385419ac65`を包含
- remote比較: candidateはdefaultに対して`+2 / -0`
- fixture: `mc-remote/protocol/test/fixtures/direction-lightning-v23.1.json`
- fixture identity: 20,367 bytes、Git blob `7371787ca6484a45dec0c7893608339961ae6fcf`、SHA-256
  `586d24bf40136eec31f1827f23ef5b317f15100a17a635d7fe9f165e0af40dce`、93 unique cases

## 実行

dirtyな既存worktreeを変更、stash、cleanしない。隔離worktreeまたはremote refだけで作業する。

1. `origin/develop`とcandidate branchをfetchする。
2. `origin/develop`が固定SHAのままで、candidateがstrictly aheadかつbehind 0であることを再確認する。
3. candidate上でprotocol workspaceのtest／lint／Prettier／buildを再実行する。
4. fixture digest、93/93 unique ID、protocol配下の`mcr.lightning` 0件を再確認する。
5. merge commit、squash、cherry-pick、内容編集を行わず、`develop`をcandidate commitへfast-forwardしてpushする。
6. push後の`origin/develop`がexact candidate SHAであることを確認する。

作業前の`origin/develop`が固定SHAから動いていた場合は停止し、現在SHAとahead／behindを返す。自動rebaseしない。

## Change cone

`@mc-remote/protocol`の23.1 mirrorとsuccessor fixtureだけを統合する。Scratch学習者向けdirection／lightning block、
Bridge、WireScope、GUI UX、OCI、Pagesを追加変更しない。park済みProtocol repositoryへownerを移さない。

## 返却

- integration前後の`origin/develop` SHA
- candidateとのfast-forward／tree一致
- test／lint／format／build結果
- fixture path／bytes／blob／digest／93 case
- local HEADとremote SHA一致、clean隔離worktree
- tag、release、artifact、Pages、OCI、shared deployを行っていないnon-claim
