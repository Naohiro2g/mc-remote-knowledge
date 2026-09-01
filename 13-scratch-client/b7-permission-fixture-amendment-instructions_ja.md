# b7 permission fixture改訂指示書

> status: 完了。`agent/b7-permission-fixture-amendment@773e2984132d82bb6e740d6458107fe42ef68a0a`を
> coordinatorがremote／exact bytes照合済み。develop未統合。

## 目的

旧b7 owner fixtureを、construction permissionのsession admission snapshotへ追従させる。これはprotocol mirror／共有fixtureの
作業であり、Scratch学習者向けdirection／lightning blockの完成を開始条件にしない。

## predecessor

- owner branch／commit: `agent/b7-protocol-owner-fixture@607cda40588ec4579c503d457c3784385419ac65`
- path: `mc-remote/protocol/test/fixtures/direction-lightning-v23.1.json`
- bytes: `14179`
- SHA-256: `faad66c93d2c8ee8eb541f6b7297163cb681054b3de05ba3d130ac4288c1046a`
- protocol: `23.1.0`

このidentityは旧contractを固定した履歴として残すが、新contractのcompletion evidenceには使わない。

## 改訂内容

- `mcr.lightning`の要求、node、拒否caseを削除し、fixture／method mirrorから参照しない。
- hello時に`mcr.online`、`mcr.offline`、build rangeを一度snapshotするcaseを追加する。
- online／offlineそれぞれで、permissionなし、onlineのみ、offlineのみ、両方のadmission結果を固定する。
- online-only sessionはquit、offline-only sessionはjoinで閉じ、両permission sessionは状態遷移をまたぐことを固定する。
- permission／rangeの途中変更は既存sessionへ反映せず、再接続後に反映することを固定する。
- immediate session／credential revokeは既存のrevoke契約を再利用し、新しいwire methodを作らない。
- lightningはsession admission後にbuild range、専用rate、work 256、chunk、full strikeへ進む既存順序を維持する。
- direction、handle、rate／work、notification FIFO、ParticleBuilderの既存caseとexact valueを不要に変更しない。
- protocol `23.1.0`、package `2301.0.0b7`、method／params／result／reason shapeを変更しない。

case IDは既存IDを意味違いのまま再利用しない。削除・置換・追加の対応をmanifestに明記し、全case IDのunique性と未消費caseを
検出するowner testを維持する。

## 検証と返却

- protocol lint／format／unit test／build
- predecessorからのfixture semantic diff
- branchとpush済みcommit、parent、local／remote SHA一致、clean worktree
- successor path、bytes、Git blob、SHA-256、総case数
- 旧ID→新ID／削除ID／追加IDの対応表
- `mcr.lightning`参照0件の検索結果
- learner block、Bridge、WireScope、artifact、liveを変更していないnon-claim

専用branchへpushし、developへ直接pushしない。coordinatorがexact bytesをknowledgeへ着地した後、McRemoteとPythonへ同じ
fixture identityを搬送する。

## 完了identity

- branch／commit: `agent/b7-permission-fixture-amendment@773e2984132d82bb6e740d6458107fe42ef68a0a`
- parent: `607cda40588ec4579c503d457c3784385419ac65`
- path: `mc-remote/protocol/test/fixtures/direction-lightning-v23.1.json`
- bytes: `20367`
- Git blob: `7371787ca6484a45dec0c7893608339961ae6fcf`
- SHA-256: `586d24bf40136eec31f1827f23ef5b317f15100a17a635d7fe9f165e0af40dce`
- case: 93件、93 unique ID

predecessor 81件から4件を削除し16件を追加、77件はobject単位で不変である。旧`B7-L14`の
`mcr.lightning`拒否caseは後継なしで削除し、`B7-A01`、`B7-A10`〜`A17`、`B7-A20`〜`A23`、
`B7-A30`〜`A32`へpermission snapshotと状態遷移を固定した。coordinatorはremote branch／parent、fixtureの
blob／bytes／digest、93 IDのunique性、protocol配下の`mcr.lightning` 0件を照合した。owner報告ではlint、
Prettier、Vitest 28件、build、predecessor／successor比較がPASSした。Scratch学習者向けblock、Bridge、
WireScope、live、artifact、develop統合は未実施・未主張である。
