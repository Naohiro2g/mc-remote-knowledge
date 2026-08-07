# b3 candidate permission_denied token preservation — sanitized summary

- 実施日時: 2026-08-07 13:40–13:41 JST
- test class: `live-human`
- Scratch candidate: `release/b3@3f1a10a366bfbe76e32b5a31c54da19eddd56e56`
- protocol: `21.0.0`
- connection target: private Dev route

## 観測

1. operatorがpaired playerの`mcr.online`を無効にした。
2. 同じbrowser windowを強制再読込し、接続操作を1回行った。
3. Scratchは保存済みDev route tokenを`auth.token`へ載せた`hello`を送信した。観察ログのtokenは`[redacted]`だった。
4. `hello.params.client.version`はcandidate SHAと一致した。
5. 同じ`hello`に対し、JSON-RPC code `-32000`、reason `permission_denied`が返った。新しいpairingは開始されなかった。
6. operatorが`mcr.online`を有効に戻した。
7. 同じbrowser windowを強制再読込し、接続操作を1回行った。
8. Scratchは保存済みDev route tokenを載せた`hello`を送信し、candidate SHAと一致するclient version、`permissions.online: true`を含むresultで成功した。
9. パレットは設定先と実接続先をともにDevと表示し、両者一致／再接続不要を示した。

## 判定

`permission_denied`後もScratchはDev route tokenを破棄せず、権限復帰後に新しいpairingなしで再接続できた。b3 matrixの`permission_denied`時のtoken温存はPASS。

## Redaction

token、pair code、pairing ID、private host、player UUIDは記録していない。ユーザー貼付rawは本handoffへ複製していない。
