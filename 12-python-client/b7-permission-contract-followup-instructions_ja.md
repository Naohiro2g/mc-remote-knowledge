# b7 permission contract追従指示書（Python）

> status: `2026-09-01-02`批准済み。Python担当への確定指示。

Python API shape、reason透過、observer、retry方針は変更しない。Scratch protocol ownerがsuccessor fixtureを発行した後、
そのexact bytesを取得してfixture ledgerを再実行し、README／starter／observerに旧`mcr.lightning`前提があれば削除する。

- base candidate: `codex/b7-python-pass-a@c9e0c19925a56dbcece409982df1b707d41f51ae`
- predecessor fixture SHA-256: `faad66c93d2c8ee8eb541f6b7297163cb681054b3de05ba3d130ac4288c1046a`
- protocol／package: `23.1.0`／`2301.0.0b7`（不変）
- `strikeLightning(x,y,z) -> None`、directionのimmutable 3-tuple、server reason無変換、自動retryなし（不変）

Python clientはLuckPermsを解決せず、hello responseのpermission snapshotをserver事実として読む。client側でonline／offlineの
包含を推測したり、permission／rangeをcommandごとに再取得したり、`mcr.lightning`互換aliasを作ったりしない。

返却物はpush済みbranch／commit、successor fixture identityと全case ledger、targeted／全回帰、build metadata、変更path、
実plugin live非実施のnon-claimとする。successor fixture待ちは実装調査やREADME修正の開始gateではなく、最終exact PASSのgateである。
