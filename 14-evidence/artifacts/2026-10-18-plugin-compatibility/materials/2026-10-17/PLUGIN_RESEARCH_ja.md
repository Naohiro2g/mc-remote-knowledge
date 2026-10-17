# Paper26.3・周辺プラグイン再確認（2026-10-17）

10月13日の調査からの差分を作者の公式配布情報で再確認した。実機試験はVPS上の複製worldで行い、本番のPaper1.21.11／Java21と周辺pluginは維持した。

| 対象 | 作者の現在の配布情報 | 今回の確認 |
| --- | --- | --- |
| Paper | [公式API](https://fill.papermc.io/v3/projects/paper/versions/26.3/builds)の26.3 #200がSTABLE | 公式JAR SHA `0e104a19ad818f05266a4571c0a9b0cada241c2016ee64883e5d38435332fa8d`で複製world起動 |
| ViaVersion／ViaBackwards | [5.12.1](https://github.com/ViaVersion/ViaVersion/releases/tag/5.12.1)／[5.12.1](https://github.com/ViaVersion/ViaBackwards/releases/tag/5.12.1)が最新安定。26.3対応 | 現行JARを使って26.3でenable |
| Geyser-Spigot | 公式default配布は2.12.0 build1259。[対応一覧](https://geysermc.org/wiki/geyser/supported-versions/)がJava版26.3、Bedrock26.30〜26.52へ更新。[PR6712](https://github.com/GeyserMC/Geyser/pull/6712)は10/14にmerge | SHA `79ec9a7e6aba1ff0d401c0c3f052297c9c339b3958bacb3537c5a725be60c172`、class65。26.3起動・UDP listen確認。本番は既存2.11.3 #1251を維持 |
| Floodgate | 2.2.5 build141のまま。[26.3対応PR686](https://github.com/GeyserMC/Floodgate/pull/686)取り込み済み | 26.3でenable。本番JARも同じ |
| WorldEdit Bukkit | [作者Modrinth版metadata](https://api.modrinth.com/v2/version/YFnqiUlL)で7.4.6がrelease、Paper／Bukkit／26.3対応 | bytes7,870,216、SHA `e0ce67d870ad1fef8a40dd9d7926360caf3bb44722438545d6b20b55f82a0c91`、class69。26.3でenable。本番Java21は7.4.2を維持 |
| DirectionHUD Paper | [1.8.4.0+26.2](https://modrinth.com/plugin/directionhud/version/u876aZ5C)のまま。26.3未宣言、OtterLib依存 | 公式Paper JAR class69。26.3でenable・Started serverを確認。実playerのHUD表示・追跡・再接続時表示は未確認 |
| OtterLib Paper | [作者配布一覧](https://modrinth.com/plugin/otterlib/versions)は0.4.0.1+26.2 beta | class69。DirectionHUDと一緒に26.3でenable |
| LuckPerms Bukkit | [公式metadata](https://metadata.luckperms.net/data/all)は5.5.87。[Bukkit5.5.71の作者掲載](https://modrinth.com/plugin/luckperms/version/b0mk8uS6)にも26.3対応あり | 本番の5.5.71を複製へ持ち込み、ローカルH2 DBで26.3起動・McRemote連携確認。5.5.87への本番更新は今回行っていない |
| DiscordSRV | [1.30.5](https://modrinth.com/plugin/discordsrv/version/ATlquwiT)のまま、作者に26.3対応掲載あり | 本番は維持。botを二重接続しないため複製試験から除外 |
| AdvancedPortals | [2.8.0-spigot](https://modrinth.com/plugin/advanced-portals/version/OiYxu4ab)のまま、作者掲載は26.2まで | 未使用というhuman owner申告。複製試験から除外。本番はJava21維持に合わせ既存2.7.1を継承 |
| ServerBackup | [公式サイト](https://server-backup.net/)は2.10.0のまま | 26.3上で@server backupを作成。762,337,236 bytes、1,345 entries、CRC PASS、nether／endの新dimension配置を包含。restoreは未試験 |

## 試験範囲と運用判断

完了済みZIPからworld・ローカル権限DB・plugin設定を複製し、本番credential authorityは共有しなかった。公開port無し、メモリ・CPU上限を持つ別コンテナでPaper26.3#200／Temurin25.0.3+9を起動した。原本のworldは変更していない。

10pluginsのenable、server Done、McRemote credential HEALTHY、Geyser UDP listen、ServerBackup実ZIPを確認。実playerの参加・HUDの表示やゲーム中の個々の機能までをPASSに含めない。previewと準備用bootstrap containerは試験後に停止した。

human ownerは今回のVPSについて「1.21.11／Java21を維持し、McRemote・Scratchをb10へ更新」を選択した。GAMEsは旧安定版・旧プロトコル／Paper26.1.2／Java25として当面維持する。将来の26.3移行では、実HUD表示とbackup restore、必要pluginの実操作を追加確認する。

素材は各作者APIのJSON、`research-identities.json`、取得JAR、`preview-result.json`、scriptに保存。classはstatic／live-auto。これは新しい横断release gateの判定や、Knowledgeの正式evidenceを意味しない。
