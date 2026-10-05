## B9 dev 通常環境の JAR 差し替え結果

- knowledge contract path: `00-hub/b9-gate-live-test-sheet_ja.md` 共通／segment 0、`00-hub/release-gate-notes_ja.md` B9 exact set、`00-hub/release-operations-responsibility-design_ja.md` §3／§8。
- knowledge contract commit: `561de98b5c15864ac9b86cb6dcaeef1f20ce635b`（remote main から取得）。
- 許可: human owner の直接依頼。対象は凍結済み `b9-integrated-artifact-set-1` の McRemote JAR。
- 場所: ホームサーバーの通常 host-native dev、Paper directory と既存 `run.sh`／名前付き Screen を実機確認して使用。
- artifact: CI candidate `5cb33ebad4bf2c5e36c3433b0f70fe6070915b00` の `mc-remote-1.21.11-2320.0.0b9.jar`、261,016 bytes、SHA-256 `4feb90dbdba8550cd16800cc3d384e42fed16a5c5e20faa489a0381ad2cda58e`。local、upload 後、配置後の本体 digest を照合。

実施: 稼働中の b8 を確認し、b9 を staging へ転送。Screen console に `stop` を送り正常停止を確認してから、旧 JAR を plugins 外へ退避し、b9 一件へ置換した。既存 `bash run.sh` で起動した。

| 確認 | 結果 |
| --- | --- |
| Minecraft | `1.21.11` |
| Paper | `1.21.11-132-ver/1.21.11@c5eb079`、起動 JAR の digest は変更前と同じ |
| Java | `21.0.12.1`、変更前と同じ Java 21 executable |
| McRemote 起動ログ | `Enabling McRemote v1.21.11-2320.0.0b9` |
| 完了ログ | `Done (21.340s)!` |
| 認証 | `Auth enforcement: true` |
| credential health | `Credential domain health: HEALTHY` |
| listener | Paper `25565`、McRemote `25575` が同じ新 Paper process で待受 |
| 二重起動 | 対象 directory の Paper process 一件、通常 Screen 一件、McRemote JAR 一件 |
| config／起動 script | 変更前の bytes と一致 |
| credential revocation files | 正常停止後の bytes と一致 |

旧 b8 は公開 asset のものではなく、従来の dev 配置物だった。退避した本体は 261,025 bytes／SHA-256 `7ab24fa1ff6c20513e46cbf3629f1f4860365acbf3a7e191e48a4e75af1677fb`、退避後も同じ digest。

退避先（server 側）:

```text
~/MINECRAFT_SERVERS/PaperMC/.mcremote-updates/2026-10-05-b9-8qo329e0/mc-remote-1.21.11-2320.0.0b8.jar
```

credential の snapshot は再起動後に byte 変化があったため、全 plugin 保存ファイルの byte 不変は主張しない。server 側の件数・時刻だけを観測し、再起動前発行の credential 一件の `last_used_at` が再起動後に更新され、新規発行は0件だった。既存 credential の再利用時に snapshot を更新する production の挙動と整合する。domain の revocation files は byte 不変で、reset／再pairingの操作はしていない。token／token hash／UUID／private address は返却素材へ出力していない。

初回の readiness 確認 script は期待する plugin version から Minecraft の接頭辞を落とし、起動済み b9 のログ照合だけが不一致となった。実 JAR の `plugin.yml` にある `1.21.11-2320.0.0b9` を基準に再照合し、上の全 readiness を確認した。これを product の起動失敗として扱わない。

実施範囲は segment 0 の JAR 差し替え・再起動・identity／readiness の確認。指定した Python／Scratch client を使う token 継続試験、認証済み hello の protocol 照合、live-auto、chat null 往復、world の全 byte 比較、live-human は今回未実施。Paper／world／config／credential の operator 編集は行っていない。サーバーは b9 で稼働を継続している。

採取値と安全な startup 行: `deployment-result.json`。横断 gate の最終判定は coordinator が行う。

### 08:02:10 の Scratch 接続観測（human owner から追記）

human owner が、b9 Scratch から b9 plugin へペアリングし直さず接続できたことと、送受信の hello 表示を本 session に提示した。test class は `live-human`、actor は human owner。Codex がこの hello を再実行した結果ではない。

- request: protocol `23.2.0`、client `scratch-mcremote`／version `2320.0.0b9`／locale `ja`。
- response: protocol `23.2.0`、mc_version `1.21.11`、supported_mc_versions `["1.21.11"]`。
- segment 0 の既存 credential 継続利用: human owner の「ペアリングなしで接続成功」により PASS として返す。
- 共通の開始時 protocol／MC 版照合: 提示された hello result により PASS。
- origin `[200,0,200]`、dimension `minecraft:overworld`、y_sea `62`、permissions online／offline `true`、build_range `1000`。
- sanitizer: 提示値に token／pairing_id／private address／player UUID は含まれていない。受領した表示 payload を `scratch-hello-observation.json` に保存。
- 境界: hello に表示される client version は b9だが、Scratch artifact の固定 source commit まではこの trace で照合できない。segment 1以降の代表操作、chat null、移管 Bridge／WireScope の適合は本観測だけでは判定しない。

上の「指定clientのtoken継続hello未実施」は差し替え作業終了時点の状態。この追記で、Scratch からの継続接続の人間観測が加わった。
