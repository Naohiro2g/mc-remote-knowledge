# Paper 26.3と周辺プラグイン：2026-10-13調査

作者の配布metadata、release notes、公式issueを確認した。対象は公開b9環境で採用している10個の周辺プラグインと、新しいDirectionHUDの依存OtterLib。対応表は作者の申告を表し、今回Paper 26.3上での起動・実機操作は試していない。現在のサーバーへのプラグイン更新も行っていない。

Paper 26.3は公式配布APIでSTABLEを確認。調査時の最新stableはbuild178、`paper-26.3-178.jar`、SHA-256 `5dd0c8fb20a96eb7c98f3c4b1c890e99ef6db56fd689a2cf06975a3471fda757`。これは調査時の観測で、将来の配備候補への固定ではない。

[Paper公式Java要件](https://docs.papermc.io/paper/getting-started/)は1.20〜1.21.11がJava 21、26.1以降がJava 25。したがって「rc1／Java 21」はMcRemoteの版をrc1にする構成であり、Paper 26.3／Java 21の構成は作れない。

## 作者の26.3対応状況

| プラグイン | 確認した版 | 26.3対応の根拠・採用条件 |
| --- | --- | --- |
| ViaVersion | 5.12.1 安定 | [5.12.0で26.3 client対応](https://github.com/ViaVersion/ViaVersion/releases/tag/5.12.0)、[5.12.1で関連修正](https://github.com/ViaVersion/ViaVersion/releases/tag/5.12.1)。現在のVPS配置版5.12.1を候補にできる |
| ViaBackwards | 5.12.1 安定 | [5.12.0で26.3 server対応](https://github.com/ViaVersion/ViaBackwards/releases/tag/5.12.0)、[最新5.12.1](https://github.com/ViaVersion/ViaBackwards/releases/tag/5.12.1)。旧Java clientから新serverへの変換を担う |
| LuckPerms Bukkit | 公式配布5.5.87。ModrinthのBukkit掲載版5.5.71 | [作者Modrinthの5.5.71にも26.3が明記](https://modrinth.com/plugin/luckperms/version/b0mk8uS6)。[公式配布metadata](https://metadata.luckperms.net/data/all)は5.5.87。26.3向け更新候補はBukkit 5.5.87。Fabric／NeoForge版と区別する |
| DiscordSRV | 1.30.5 安定 | [作者の版別metadataでPaper／26.3対応](https://modrinth.com/plugin/discordsrv/version/ATlquwiT)。現在の配置版と同じ |
| Floodgate | 2.2.5 build141、公式default配布 | [26.3対応PR #686が9/17にmerge](https://github.com/GeyserMC/Floodgate/pull/686)。本日の公式build141 metadataのchangesにもそのcommit `81b65cc…` が載る。配置済みJARのSHAは公式metadataと同じ `21570aff9ce17d6983928e8552777760e1ede5050026b04c686b0ae112e6fd7e`。Geyserの未対応とは分ける |
| Geyser-Spigot | 2.11.3 build1251、公式default配布 | [現在の公式対応はBedrock 26.30〜26.52／Java版26.2](https://geysermc.org/wiki/geyser/supported-versions/)。[26.3対応PR #6712](https://github.com/GeyserMC/Geyser/pull/6712)は未mergeでpreview扱い。[Paper 26.3 build175で#1251が起動できない報告](https://github.com/GeyserMC/Geyser/issues/6763)に作者がpreviewを案内。ViaBackwardsだけで現在のSpigot JARの起動互換性を解決できると考えない |
| WorldEdit Bukkit | 安定7.4.5、26.3向け7.4.6-beta-02 | [作者Bukkit配布一覧](https://dev.curseforge.com/projects/worldedit/files)と保存したModrinth版別metadataで、安定7.4.5は26.2まで、7.4.6-beta-02は26.3対応。安定版を採るという既存の希望では、26.3のWorldEditは待ち。Java 21側は7.4.2を維持。前日の公式JAR実検査で7.4.3〜7.4.5はJava 25必須と確認済み |
| DirectionHUD Paper | 1.8.4.0+26.2 | [Paper版の作者metadataは26.2のみ](https://modrinth.com/plugin/directionhud/version/u876aZ5C)。26.3の公開版はFabricで、Paper用と取り違えない。最新Paper版はJava 25、OtterLib必須（前日の公式JAR実検査）。Paper 26.3での可否は未確認 |
| OtterLib Paper（DirectionHUD依存） | 0.4.0.1+26.2 beta | [作者配布一覧](https://modrinth.com/plugin/otterlib/versions)はPaper26.2のみ。26.3未宣言で依存側の確認も必要。Java 21側の旧DirectionHUDには今回追加しない |
| AdvancedPortals | 2.8.0-spigot 安定 | [作者版別metadata](https://modrinth.com/plugin/advanced-portals/version/OiYxu4ab)は26.2まで。26.3は未宣言。起動だけでなくportal作成、保存、再起動、移動を複製worldで確認してから採用する。legacy-spigot／Folia alphaと区別する |
| ServerBackup | 2.10.0 | [作者のSpigot配布ページ](https://www.spigotmc.org/resources/server-backup-ingame-dropbox-ftp-backup-1-18-1-21-multithreaded.79320/)のtested版は1.21まで。26.3の明示保証は確認できない。複製環境でbackupの作成と復元、3dimensionとplugin dataの包含を確かめる |

## b10、rc1、stableの運用案（未批准）

Knowledge `bc1c6565058c668a23debe0633296cc428f96ce7` の[DECISION 2026-10-13-07](https://github.com/Naohiro2g/mc-remote-knowledge/blob/bc1c6565058c668a23debe0633296cc428f96ce7/00-hub/DECISIONS_ja.md)は、b10の対象を1.21.11と26.3、初回stableの26.xを26.3と定めている。同じJARの双方のpulseがPASSし、human ownerがそのcandidateをb10として採用したとSSOTに記録されている。これはSSOTの申告であり、今回Stackがcomponentの試験を再実施したという意味ではない。箱庭serverのMinecraft版を変える判断は別にhuman ownerが持つ。

McRemoteのrelease番号、PaperのMinecraft版、Java版、周辺plugin setを別々に記録する。**McRemoteが26.3をsupportすることと、周辺plugin込みの既存公開worldを26.3へ移すことは別**である。

| 時期 | XServer GAMEsの旧安定環境 | VPS公開箱庭 |
| --- | --- | --- |
| b10 | 26.3／Java 25の移行準備・複製world試験に使用する案。公開配備はreleaseの確定setを取得してから | 当面1.21.11／Java 21。b10配備とPaper／Java変更を分ける。Geyser＋WorldEdit安定版の条件が整えば26.3移行を再検討 |
| rc1 | rc1＋Paper26.3＋Java25で新世代を実運用する案。必要pluginの可否を先に確かめる | rc1＋Paper1.21.11＋Java21で旧世代・統合版接続を継続する案。WorldEdit7.4.2、旧DirectionHUDを維持 |
| 初回stable | stable＋Paper26.3＋Java25を想定 | stable＋Paper1.21.11＋Java21を維持してもよい。新世代の必須pluginとworld移行が確認できた時点で26.3／Java25へ |

XServer GAMEs側の現在の実機inventory、管理画面の26.3／Java25選択可否、持ち込みJARの制約は今回未確認。上の表は配備手順の確定ではなく、ユーザーの案に対する運用上の候補である。XServer側でも統合版接続が必須なら、Geyserの条件は同様に必要。

stable直後に両環境を同時にPaper26.3へ統合する必要はない。1.21.11／Java21を互換性確認の環境として保持するか、利用者向けには26.3へ統合して旧構成を内部確認だけへ移すかは、その時点の利用状況と運用負担で選ぶ。

26.3へ移す前には、Geyserの通常配布での対応、WorldEditの26.3対応安定版、HUDの対応または採用しない判断、AdvancedPortalsとServerBackupの実動作を閉じる。複製worldでupgradeと代表操作を試し、旧world snapshot＋旧Paper／Java／plugin setで戻れることを確認してから公開worldへ適用する。credentialのlifecycleはworld rollbackから分離する。[Paper公式は更新後worldのdowngrade不可と明記](https://papermc.io/news/26-3/)しており、rollbackで旧Paperに更新済みworldを読ませない。

今回のauthor metadata調査からは、**GeyserとWorldEdit安定版を使うVPSはb10時点で1.21.11／Java21を続け、新世代の先行運用と分ける案を推奨**する。公開releaseと必須pluginの条件が整った時点で再判定する。

## 保存した根拠

- `collect-metadata.py`と各作者APIのJSON（版、loader、game_versions、build、changesを保存）。LuckPerms公式APIは標準User-Agentで403、識別用User-Agentで再取得成功。
- `geyser-263-pr.json`／`floodgate-263-pr.json`: GitHub APIで現在のopen／mergedを照合。
- 前日のJAR検査は`../../2026-10-12-b9-plugin-latest-check/materials/directionhud-bytecode-check.json`と`../../2026-10-12-b9-plugin-update/materials/worldedit-alternatives.json`を参照。
- クラス: author metadata／static research。今回Paper26.3でのlive-auto／live-humanは実施していない。
