# b7 permission contract追従指示書（Python）

> status: successor fixture固定済み。Python担当の最終exact fixture gateを解除する。

Python API shape、reason透過、observer、retry方針は変更しない。Scratch protocol ownerがsuccessor fixtureを発行した後、
そのexact bytesを取得してfixture ledgerを再実行し、README／starter／observerに旧`mcr.lightning`前提があれば削除する。

- base candidate: `codex/b7-python-pass-a@c9e0c19925a56dbcece409982df1b707d41f51ae`
- predecessor fixture SHA-256: `faad66c93d2c8ee8eb541f6b7297163cb681054b3de05ba3d130ac4288c1046a`
- successor owner: `scratch-editor agent/b7-permission-fixture-amendment@773e2984132d82bb6e740d6458107fe42ef68a0a`
- successor path: `mc-remote/protocol/test/fixtures/direction-lightning-v23.1.json`
- successor bytes／blob: `20367`／`7371787ca6484a45dec0c7893608339961ae6fcf`
- successor SHA-256／case: `586d24bf40136eec31f1827f23ef5b317f15100a17a635d7fe9f165e0af40dce`／93 unique IDs
- protocol／package: `23.1.0`／`2301.0.0b7`（不変）
- `strikeLightning(x,y,z) -> None`、directionのimmutable 3-tuple、server reason無変換、自動retryなし（不変）

Python clientはLuckPermsを解決せず、hello responseのpermission snapshotをserver事実として読む。client側でonline／offlineの
包含を推測したり、permission／rangeをcommandごとに再取得したり、`mcr.lightning`互換aliasを作ったりしない。

返却物はpush済みbranch／commit、successor fixture identityと全case ledger、targeted／全回帰、build metadata、変更path、
実plugin live非実施のnon-claimとする。successor fixture待ちは実装調査やREADME修正の開始gateではなく、最終exact PASSのgateである。

coordinatorはsuccessorのremote commit／parent、exact bytes、blob、digest、93 IDのunique性を照合済みである。
旧81 case fixtureや値の転記を使わず、上記owner pathからexact bytesを取得して作業を再開する。
