# b9公開ベータ：プラグイン最新版再確認

- 確認日: 2026-10-12 JST
- 調査時刻（UTC）: 2026-10-12T10:02:50.211067+00:00
- SSOT実読: `mc-remote-knowledge@f2eddd178f4c3760cfe280d2c570e266b14001b4`のruntime、INDEX、release運用責務§15
- 範囲: 作者GitHub Release、公式download metadata、作者Modrinth配布情報の読み取りとDirectionHUDの実配布JARの静的検査
- 稼働VPSへの接続・差し替え・停止・再起動は実施無し。現行配置版の再観測や起動互換性検証は主張しない
- 前回比較: 会話で指定された更新候補。現在のVPS実測値とは区別する

| プラグイン | 確認した最新版 | 補足 |
| --- | --- | --- |
| ViaVersion | [5.12.1（安定）](https://github.com/ViaVersion/ViaVersion/releases/tag/5.12.1) | 前回候補5.12.0から更新 |
| ViaBackwards | [5.12.1（安定）](https://github.com/ViaVersion/ViaBackwards/releases/tag/5.12.1) | 前回候補5.12.0から更新 |
| Geyser-Spigot | [2.11.3 build #1251](https://download.geysermc.org/v2/projects/geyser/versions/latest/builds/latest) | 前回候補#1249から更新。公式default build |
| Floodgate | [2.2.5 build #141](https://download.geysermc.org/v2/projects/floodgate/versions/latest/builds/latest) | 前回候補と同じ。公式default build |
| LuckPerms Bukkit | [5.5.87](https://metadata.luckperms.net/data/all) | 前回候補と同じ |
| AdvancedPortals | [2.8.0](https://github.com/sekwah41/Advanced-Portals/releases/tag/v2.8.0) | 前回候補と同じ |
| DirectionHUD Paper | [1.8.4.0+26.2](https://modrinth.com/plugin/directionhud/version/u876aZ5C) | Java 25・Paper 26.2 API・OtterLib必須。b9への差替候補から除外 |
| WorldEdit Bukkit | [7.4.5（安定）](https://modrinth.com/plugin/worldedit/version/F5ea2ov3) | 最新betaは7.4.6-beta-02。7.4.5は1.21.11を配布元の対応版に含む |
| DiscordSRV | [1.30.5（安定）](https://github.com/DiscordSRV/DiscordSRV/releases/tag/v1.30.5) | 安定版の新規更新なし |
| ServerBackup | [2.10.0](https://server-backup.net/) | 作者公式配布サイトとSpigotの表示を確認 |
| McRemote | [1.21.11-2320.0.0b9（beta）](https://github.com/Naohiro2g/McRemote/releases/tag/v1.21.11-2320.0.0b9) | 公開済みbetaの最新。b9本体は維持する前提 |

## DirectionHUD

最新版Paper JARとb9向けの旧Paper JAR、最新版Spigot JARを取得し、Modrinth発行のsize／SHA-512を全件照合した。
実JARの`plugin.yml`と自前のclassのmajor versionを検査した（`directionhud-bytecode-check.json`）。

- Paper `1.8.4.0+26.2`: class major **69**（Java 25）、`api-version: 26.2`、`depend: [OtterLib]`。b9のPaper 1.21.11／Java 21では使用不可
- Paper `1.8.2.3+1.21.11`: class major **65**（Java 21）、`api-version: 1.21`。公式Modrinth一覧でPaper 1.21.11向けの最新はこの版のまま
- Spigot `1.8.4.0+26.1-26.2`: class major65でも`api-version: 26.1`、OtterLib必須。Java 21向けという一点だけでPaper 1.21.11に適用しない
- Fabric `1.8.4.0+26.3`は別loader向けで、今回のPaperサーバー用プラグイン更新対象外
- JVM class formatの根拠: https://docs.oracle.com/javase/specs/jvms/se25/html/jvms-4.html#jvms-4.1

旧Paper配布JARのSHA-256 `806b389dee47415fd3369a526e3a7c7f0e2decf52dfffc56ae57bb65bb729068`は、
10/5の保存inventoryのDirectionHUDと同一。現在の稼働VPSの再計測ではない。

## 後続更新用の固定download URL

- Geyser #1251: https://download.geysermc.org/v2/projects/geyser/versions/2.11.3/builds/1251/downloads/spigot
  - 公式metadataのSHA-256: `0bd00484f688c49e45f84f7c8bf9326f52d48a4c697d72a28526f2fe3f55dc36`
- Floodgate #141: https://download.geysermc.org/v2/projects/floodgate/versions/2.2.5/builds/141/downloads/spigot
  - 公式metadataのSHA-256: `21570aff9ce17d6983928e8552777760e1ede5050026b04c686b0ae112e6fd7e`
- LuckPerms: https://download.luckperms.net/1674/bukkit/loader/LuckPerms-Bukkit-5.5.87.jar
- ViaVersion: https://github.com/ViaVersion/ViaVersion/releases/download/5.12.1/ViaVersion-5.12.1.jar
- ViaBackwards: https://github.com/ViaVersion/ViaBackwards/releases/download/5.12.1/ViaBackwards-5.12.1.jar

この最新版調査時点ではDirectionHUD以外の配布JARを取得していなかった。
後続更新作業でViaVersion・ViaBackwards・Geyser・WorldEditの実JARを検査した。
WorldEdit 7.4.3／7.4.4／7.4.5はいずれもmain class major69（Java 25）だったため、
human ownerの追加回答に従い、b9のJava 21とWorldEdit 7.4.2を維持した。
適用結果は`../../2026-10-12-b9-plugin-update/materials/UPDATE_RESULT_ja.md`を参照。
配布metadataにMinecraft 1.21.11が含まれることだけでは、Java 21への適用可否は確定しない。
JSTタイムスタンプ修正は別の未適用項目として維持する。
