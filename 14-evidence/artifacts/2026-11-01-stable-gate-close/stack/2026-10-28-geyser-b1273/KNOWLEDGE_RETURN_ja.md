Stackからknowledge sessionへの返却（2026-10-28）

human ownerから、統合版26.60のリリース後に有料GAMEsのsbへiPhoneで参加できたとの報告を受け、公開VPSのsb-betaにも同様の処置を実施しました。sbについてはhuman ownerの報告であり、Stackが直接設定・packetを検査した結果ではありません。

追補：human ownerがconfigの差分を確認し、実質的な差はなく、「config.ymlが不適合だった」という初報は勘違いだったと訂正しました。BDSの複数UDPポート指定の形式などとの取り違えだった可能性、という説明です。これはhuman ownerの確認結果であり、Stackによる追加の比較結果ではありません。configの再生成は実施した作業として残しますが、不整合の修復や、接続復旧に必要だった処置としては扱いません。

具体例として、human ownerからBDSのserver.propertiesに`server-udp-ports=49152-49251`と書く指定が提示されました。[XServer VPSの公式案内（2026-10-08）](https://vps.xserver.ne.jp/support/information_detail.php?view_id=19629)でも同じ設定例を確認しました。これはBDSのNetherNet用UDP範囲の指定例です。取り違えの説明を補う資料として残し、今回のGeyserやfirewallの設定変更は行っていません。

sb-betaは、Geyser-Spigotを2.12.0 b1269から**2.12.1 b1273**へ更新しました。旧config.ymlを`config.yml.before-b1273-20261028`へ改名し、b1273に新しいconfig.ymlを生成させています。生成後のconfigは編集していません。NetherNetのidentity.pemは更新前後で同じSHA-256であることを確認しました。

human ownerが更新後のsb-betaへiPhoneの統合版26.60で接続し、**TOFU警告の後、参加成功**と報告しました。今回の作業ではHTTPSを設定しておらず、signalingはHTTPです。外部からのHTTP応答も26.60／protocol 2225です。TOFU画面の画像やpacket captureは取得していません。

**固定したidentity**

- knowledge contract commit：`feabc66aae033325106ed00f9b1f9f3717ae3f9b`
- knowledge参照：runtime protocol、release operations responsibility、release gate notes、既存のiOSの外部事実と証明書のpark
- Stack：`488475f2b3dfeeb3252bddda2d87b4fca39fb2a6`
- profile／preset：`vps-server@16`／`public-web-paper@15`（維持）
- Paper／McRemote：Paper 1.21.11／McRemote 2321.0.0rc1（維持）
- Geyser：2.12.1 b1273
- 公式metadata：[2.12.1 build 1273](https://download.geysermc.org/v2/projects/geyser/versions/2.12.1/builds/1273)
- 配布JAR：[固定したSpigot版](https://download.geysermc.org/v2/projects/geyser/versions/2.12.1/builds/1273/downloads/spigot)
- JAR SHA-256：`218f57088fd7a147f670c489377da2341fc51f1867b2c36ed181f39c9f379b59`（公式metadata、取得物、実行container内で一致）
- 実行時診断のversion：`2.12.1-b1273 (git-master-a24ba9c)`
- 更新plan：`sha256:e27828a021de38fd0ebf9a0ebc9b70bab74efb7e9df2b9bb6b758f1998e39468`
- source lock：`sha256:fab36a05e301b33b8fe623790257cf76aceb53cb34cbe0d1fafebb5da6a859ee`
- target lock：`sha256:a9eb516219a82c0ee37d3306b4d52c629dac230b440fc7267eef954bb27ea403`

**確認したこと**

- 更新前doctorは全項目正常、停止直前の参加者は0人。
- `minecraft-plugins`のtyped inputでGeyserのSHAだけを変更し、通常の`deployment update plan`／`apply`を使用。profile／preset、release artifact、ほかのoperator input、world、network、volumeのidentityが変わらないことを照合。
- 旧configとGeyser directoryをprivateに退避。NetherNetのidentityを保持。
- 通常の更新transactionで4 serviceを再作成。applyは`status=complete`。
- 新しいconfigは`config-version: 11`、`transport: nethernet`、port 19132、`webrtc-port: 0`、signaling `builtin`、HTTPSの証明書指定なし。
- config上のJava認証は既定の`online`。外部へアップロードしない`geyser dump offline`による実行時診断では、`config.java.auth-type: FLOODGATE`を確認。既存Floodgateの自動検出が働いており、configを変更する必要はなかった。
- Geyser 2.12.1の起動、built-in HTTP signaling、Floodgateの有効化、Paperの起動完了、McRemote credential HEALTHYを確認。
- 更新後doctorはruntime、lock／render、network、McRemote応答と認証必須、homepage、Scratch runtime、WireScopeすべて正常。
- 外部から`http://VPS_HOST_REDACTED:19132/v1/join`へ接続でき、version 26.60、protocol 2225の応答を確認。
- human owner：iPhoneの統合版26.60でsb-betaへ接続し、TOFU警告後に参加成功。
- repo指定の検査：`uv sync --extra dev`成功、`uv run pytest`は598 passed（879.59秒）、`uv run ruff check .`成功。今回は追跡対象の実装変更がないため、新しいtestコードは追加していない。

test classは、Stackによる`live-auto`と、human ownerによる`live-human`です。正式evidenceへ昇格する場合のrecord path案は`14-evidence/records/2026-10-28-bedrock-2660-ios-b1273_ja.md`です。この本文をsanitized summaryの材料として使用できます。正式配置とcommitはknowledge側で行ってください。

**主張しないことと後続**

- client版とGeyser版の更新後の成功であり、26.60だけで復旧したという因果の切り分けはしていません。config再生成も実施しましたが、不整合や再生成の必要性を示す根拠はありません（上記の初報訂正）。
- iPad、Windows、Androidの今回の接続は未試験です。
- TLSを試してからHTTPへfallbackしたかなどの順序はpacketで観測していません。
- HTTPが将来も使えることの保証、HTTPS／証明書更新、Caddy／Wardenの検証ではありません。
- homepage、DNS、SSOT、11/1用の別セットは変更していません。

knowledgeでは`F-bedrock-ios-signaling-tls`へ今回の条件付き成功を追記し、10/24の古い観測はその版での観測として残してください。証明書のparkでは、iOSの参加不通の解消と、引き続き進めるHTTPS化を分けて扱う材料になります。`2026-10-27-01`の前倒し方針は継続です。11/1の26.3セットをb1269で作る既存指定については、26.60対応のために見直す必要がありますが、その別セットの更新は今回実施していません。
