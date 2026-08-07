# b3 candidate Dev pairing and token reconnect — sanitized summary

- 実施日時: 2026-08-07 13:19 JST
- test class: `live-human`
- Scratch candidate: `release/b3@3f1a10a366bfbe76e32b5a31c54da19eddd56e56`
- protocol: `21.0.0`
- connection target: private Dev route

## 観測

1. 先行pairing attemptはoperator操作前に期限切れとなったため、正式観測から除外した。
2. 新しいpairingを開始し、operatorがMinecraft内でpair操作を完了した。
3. `auth.pairPoll`は`status: ok`とtokenを返し、観察ログではtokenが`[redacted]`だった。
4. Scratchは直後に保存済みtokenを載せた`hello`を送信した。
5. `hello.params.client.version`はcandidate SHAと一致し、protocol `21.0.0`、Minecraft `1.21.11`、online permissionを含むresultで成功した。
6. 同じbrowser windowを強制再読込し、直後に接続した。
7. 新しいpairingを要求せず接続に成功した。
8. パレットは設定先と実接続先をともにDevと表示し、両者一致／再接続不要を示した。

## 判定

exact candidate上でprivate Dev routeの新規pairing、token保存、再読込後のtoken再利用がPASS。

## Redaction

token、pair code、pairing ID、private host、player UUIDは記録していない。ユーザー貼付rawは本handoffへ複製していない。
