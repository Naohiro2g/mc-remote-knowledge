# 周辺プラグインのPaper 26.3対応とJavaの要件（2026-10-12〜17）

> 公開VPS（箱庭）で使っている周辺プラグインについて、Stack担当が調べた結果。test classは`static`（公式JARの検査）、
> `author metadata`（作者の配布情報）、`live-auto`（複製したworldでの起動）。live-humanは行っていない。
> 搬送元はmc-remote-stack `main@1a4f8e5`のStack担当（確定搬送票、2026-10-18）。素材は
> `14-evidence/artifacts/2026-10-18-plugin-compatibility/`（31 file、`SHA256SUMS`。第三者のJAR本体は含まない）。
> 自分でサーバーを用意する人が、プラグインの版を選ぶときや、Minecraftの版を移すときの材料として公開する。
> 利用者向けのおすすめの案内は、McRemoteの`docs/recommended-plugins_ja.md`が受け持つ。

## 前提

Paperは、1.20〜1.21.11がJava 21、26.1以降がJava 25で動く（Paper公式のgetting started）。Java 25向けにbuildされた
プラグイン（classのmajor 69）は、Java 21のサーバーでは動かない。作者が対応版に1.21.11を挙げていても、それだけでは
Java 21で使えるとは言えない。

## 結果

| プラグイン | 作者の26.3の申告（10/17） | Java | 26.3の複製worldで（10/17、live-auto） |
| --- | --- | --- | --- |
| ViaVersion／ViaBackwards | 5.12.1で対応 | — | 有効になった |
| Geyser-Spigot | 2.12.0 build 1259で対応（26.3対応のPRは10/14にmerge） | Java 21以上（Geyserの[supported versions](https://geysermc.org/wiki/geyser/supported-versions)、2026-10-18に確認）。2.12.0の公式JARもclass 65（10/17の検査）。搬送票の「Java 21では動かない」は、Java 21未満を切ったことの読み違いと見る（human owner 2026-10-18）。2.12.0をPaper 1.21.11で使えるかは確かめていない | 有効、UDPで待ち受けた |
| Floodgate | build 141で対応 | — | 有効になった |
| WorldEdit（Bukkit） | 7.4.6の正式版（10/15）で対応 | 7.4.3〜7.4.6はJava 25（class 69、10/12のJAR検査） | 7.4.6が有効になった |
| LuckPerms（Bukkit） | 5.5.71に26.3対応の掲載（公式の最新は5.5.87） | — | 5.5.71が有効、McRemoteとの連携を確認 |
| DiscordSRV | 1.30.5に26.3対応の掲載 | — | botを二重に接続しないため試していない |
| DirectionHUD（Paper） | 1.8.4.0+26.2まで。26.3は未宣言 | Java 25（class 69）。OtterLibが要る | 有効、serverの起動まで |
| OtterLib（Paper） | 0.4.0.1+26.2（beta）まで | Java 25（class 69） | DirectionHUDと一緒に有効 |
| AdvancedPortals | 2.8.0まで、26.2までの掲載 | — | 使っていないので試していない |
| ServerBackup | 2.10.0（作者のtested版の表示は1.21まで） | — | 実際のbackup ZIPを作れた（762,337,236 bytes、1,345 entries、CRC PASS、26.3で変わったnetherとendの配置を含む） |

複製worldの試験（10/17）：完了済みのbackupから、world、ローカルの権限DB、プラグインの設定を複製し、公開portの無い別の
コンテナで、Paper 26.3 #200／Temurin 25.0.3+9を起動した。本番のcredentialは共有していない。プラグイン10個が有効になり、
startupにERRORは無く、McRemote（`2320.0.0b10`）のcredentialはHEALTHY。元のworldは変えていない。

## 主張しない範囲

実際のplayerでのloginとpairing、DirectionHUDの実際の表示、backupからのrestore、各プラグインのゲーム中の操作、
XServer GAMEsの実機。作者の申告は申告で、ここで動作を保証するものではない。表の版は2026-10-17の観測で、以後の更新は
各作者の配布情報を見る。Paperは更新した後のworldを旧版で読めない（Paper公式の26.3の告知）ので、26.3へ移すときは
旧worldと旧セットを戻り先として残す（`2026-08-25-02`、`2026-10-18-02`）。
