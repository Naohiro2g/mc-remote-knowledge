## b8 token継続試験 返却票（Python）

- knowledge contract commit: `749ba60dc8c18938e50ce66b8e820aac4401c69e`。
- exact set: `b8-integrated-artifact-set-1`。
- Python source: `52d35f5304e62f465c1f47ab47c00fe9bcf62470`。
- 使用wheel: CI run36860299749、2320.0.0b8、SHA-256 `dcedff010feac0d5df24ff85dd84b321fb819f78563c39431ac32d9d75bc0180`。
- 場所: human owner指定の通常dev。private接続先は返却票に記載しない。
- 手順: b7で新規session pairing（Minecraftで人間承認）→local保存→保存tokenでb7 hello→human ownerのb8差し替え完了連絡→同じendpoint・保存tokenを照合→b8 hello。b7 phaseは凍結wheelのtransportからprotocol23.1.0を明示した。
- test class: b7新規pairはlive-human、保存tokenでb7／b8 helloはlive-auto。

| 操作 | 結果 | protocol | mc_version | reason |
| --- | --- | --- | --- | --- |
| b7で新規pairとlocal保存 | PASS | — | — | なし |
| 保存tokenでb7 hello | PASS | 23.1.0 | 1.21.11 | なし |
| 同じ保存tokenでb8 hello | PASS | 23.2.0 | 1.21.11 | なし |

- 観測: b8 phaseのpairing_started=false、same_saved_token=true。tokenの同一性はprivate stateのdigestで照合。token実値、pairing_id、private address、player UUIDはsummaryへ出力していない。保存token／credentialの削除・上書き、server設定変更、world書き込みなし。
- evidence素材: `b7_summary.json` SHA-256 `f1c5d7e812c080f4dc7a26a90c3cae8656a4eef1bf650accdb2f87ecdb41bd06`、`b8_summary.json` SHA-256 `81da6bb092cf4d59f5df6c81905651653d048384ffe5f50f918b3082334e45ef`、`token_upgrade.py`。素材の正式record／artifact化はknowledge担当が行う。
- 未実施: Python代表往復、WireScope real-browser表示、2-player receiver、粒子の描画／サウンド聴取、graph、Windows。この票だけで横断gateのGREENを判定しない。
- 注意: 最初のhost aliasのDNS失敗はserver接続前の設定診断。ローカルSSH設定から同じaliasを解決して接続先設定を補正した。candidate／serverには変更を加えていない。

