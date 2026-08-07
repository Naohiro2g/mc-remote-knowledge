# b3 candidate target-specific token — sanitized summary

- 実施日時: 2026-08-07 13:48 JST
- test class: `live-human`
- Scratch candidate: `release/b3@3f1a10a366bfbe76e32b5a31c54da19eddd56e56`
- protocol: `21.0.0`
- connection targets: Localhost route / private Dev route

## 観測

1. Dev接続中に設定先をLocalhostへ変更すると、パレットは設定先Localhost／実接続先Dev、不一致／再接続要を示した。
2. 同じbrowser windowを強制再読込してLocalhostへ接続した。有効なLocalhost tokenがなかったため新規pairingが必要となり、operatorがpairingを完了した。
3. Localhost接続中に設定先をDevへ変更すると、パレットは設定先Dev／実接続先Localhost、不一致／再接続要を示した。
4. 同じbrowser windowを強制再読込して直後に接続した。
5. 新しいpairingを要求せず、先に保存済みだったDev route tokenを載せた`hello`が送信された。
6. `hello.params.client.version`はcandidate SHAと一致し、`hello`は成功した。
7. パレットは設定先と実接続先をともにDevと表示し、両者一致／再接続不要を示した。

## 判定

Localhostで新しいtokenを保存してもDev route tokenは上書きされず、Devへ戻した際に再利用された。接続先別token、接続中の設定先／実接続先不一致表示、再接続後の一致表示はPASS。

## Redaction

token、pair code、pairing ID、private host、player UUIDは記録していない。ユーザー貼付rawは本handoffへ複製していない。
