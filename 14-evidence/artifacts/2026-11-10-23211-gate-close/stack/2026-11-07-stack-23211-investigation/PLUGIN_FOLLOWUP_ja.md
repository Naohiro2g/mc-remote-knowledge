## 周辺pluginの調査追補（2026-11-07）

初回の「他pluginは現行版を維持する案」は、Paper #231で動作した既存構成を基準とし、Paperの更新概要に必須更新の根拠を見つけなかったことから、変更範囲を絞るというStack担当の推論だった。各pluginの公開最新版と修正内容の比較を終えた結論ではなかった。この根拠で一括維持を勧めた点を訂正する。

**周辺pluginの更新方針（human ownerによる2026-11-07の明確化）**

基本的には最新版に追従し、問題がないか確認する。各デプロイの準備で、対象のMinecraft／Java／loaderに合う公式配布の最新版を調べ、今回採用する版・build・取得元・SHA-256を固定して確認する。

リリース前後で検証工数を確保できない場合など、状況に応じて実績のある版に留めることもできる。最新版への更新を毎回必須にはしない。旧版を選ぶ場合は、その対象と検証工数・実績などの理由を記録する。「今回のPaper向け必須修正がない」ことだけから、基本方針を現行維持へ読み替えない。

Geyserは版の番号だけでなくbuild番号まで毎回照合する。今回調査した時点では2.12.1-b1294を選定案とし、LuckPermsも5.5.91への更新を選定案とする。後続の実施準備では、その時点の最新版を再確認してcoordinatorへ返す。凍結したsetへの反映は採用identityを明示して行い、実行時に暗黙の`latest`へ置き換えない。この票だけでdeploy済み／検証済みとは扱わない。

記述の不一致も見つかった。Stack `docs/public-vps-preparation-guide_ja.md:75`は「周辺pluginの更新は必要なものを選ぶ」となっており、基本方針と旧版を選ぶ条件が伝わらない。SSOTの初回stable gateには、10/29の条件として「それぞれ26.3とJava 25に合う最新版にする」、10/31の最終確認ではGeyser b1273から当時の最新b1279へ更新したことが記録されている。runbookの上記行の修正文案は「周辺pluginは基本的に対象環境に合う最新版に追従し、問題がないか確認する。リリース前後の検証工数などの事情により、理由を記録して実績のある版に留めることもできる」。knowledgeへの返却にこの文案を含める。今回は調査依頼の範囲なので追跡文書は編集していない。

根拠：[Stackの該当行](https://github.com/Naohiro2g/mc-remote-stack/blob/2b5c04842e78b9767c31903e9d8328d7554ce702/docs/public-vps-preparation-guide_ja.md#L75)、[SSOTの10/29の条件と10/31のGeyser更新](https://github.com/Naohiro2g/mc-remote-knowledge/blob/f40b003eda9ec560b0c6b4656b12bfa902746d39/00-hub/release-gate-notes_ja.md#L222)、および2026-11-07のhuman ownerの本sessionでの明示。

- knowledge contract commit: `f40b003eda9ec560b0c6b4656b12bfa902746d39`（追加調査のbootstrapでも同じリモートmain）
- Stack基準: `main@2b5c04842e78b9767c31903e9d8328d7554ce702`
- 今回の操作: 作者の配布ページ・公式API・修正PRを読み取った。公開VPSへの追加操作、実装、deploy、凍結setの更新はしていない

| plugin | 現行 | 今回確認した公開最新版 | 判断に使える根拠 |
| --- | --- | --- | --- |
| WorldEdit（Bukkit/Paper） | 7.4.6 | 7.4.6 | 同版。26.3対応が配布metadataに明記されている |
| ViaVersion | 5.12.2 | 5.12.2 | GitHubのlatest Releaseと同版。26.3関連の修正を既に含む |
| ViaBackwards | 5.12.2 | 5.12.2 | GitHubのlatest Releaseと同版。26.3関連の修正を既に含む |
| Geyser | 2.12.1-b1279 | 2.12.1-b1294 | 最新版へ更新する基本方針に従いb1294を選定案とする。26.3向けの修正も含む |
| LuckPerms | 5.5.88 | 5.5.91 | 最新版へ更新する基本方針に従い5.5.91を選定案とする |
| AdvancedPortals | 2.8.0 | 2.8.0 | GitHubのlatest Releaseと同版 |
| DiscordSRV | 1.30.5 | 1.30.5 | GitHubのlatest Releaseと同版。26.xのGameProfile関連修正を含む |
| Floodgate | 2.2.5-b141 | 2.2.5-b141 | 公式default配布の最新buildと同版。26.3対応のbuild |
| ServerBackup | 2.10.0 | 2.10.0 | 作者のSpigotMC配布ページの版と同じ。ただし同ページのtested versionsに26.3の明記はない |

「同版」の7本は、今回調べた正式Release／作者の配布経路で新しい版が確認されなかったため、現在の版を採用する根拠がある。これはPaper #244での動作試験の代わりにはならない。開発中snapshotや未公開branchまで網羅した主張でもない。

**Geyserには更新する具体的な理由がある。**

- b1283は26.3サーバーで、取り消されたブロック破壊の後にブロック表示が食い違う不具合の修正を含む
- b1293はPaper 26.3のping passthrough修正を含む。Paperの`NetworkClient#getSocketAddress`追加にGeyser側実装が追従しておらず、server-list ping処理が`AbstractMethodError`になる問題への対応（[公式PR #6818](https://github.com/GeyserMC/Geyser/pull/6818)）
- 最新b1294にもこれらの修正が含まれる。公式APIのSpigot用JARのSHA-256は`71c9ebd88fb729ff8dd881de5846a1cea04eb4ce89dc1004e67002d8a5077e4c`

以上から、Geyserについてはb1279の維持案を撤回し、b1294を更新候補として提案する。現行VPSで上記不具合の発生を再現したわけではない。b1280にはRakNet専用transport削除／PROXY protocol周辺の変更もあるため、新buildの採用前には現行Geyser設定、NetherNetのjoin、port、統合版接続を確認する。最新という理由だけで未検証のまま採用済みとは扱わない。

根拠：[build一覧の公式API](https://download.geysermc.org/v2/projects/geyser/versions/2.12.1/builds)、[b1294公式metadata](https://download.geysermc.org/v2/projects/geyser/versions/2.12.1/builds/1294)。

**LuckPermsも最新版を選定案とする。**

公式metadataでは最新5.5.91。5.5.89は初期設定の案内commandの操作改善、5.5.90はFabricでplayerなしのplaceholder解決の修正、5.5.91は操作logの比較処理に対象名を含める修正。最新版へ更新する基本方針に従い5.5.91を選定案とする。Paper #244向けの必須互換修正の有無は、更新の前提条件にはしない。

根拠：[公式metadata](https://metadata.luckperms.net/data/all)、[5.5.91の修正commit](https://github.com/LuckPerms/LuckPerms/commit/b878ae92ff7558621f30c245ff8494fd6cf63f24)。

ほかの7本の出典：[WorldEditのBukkit/Paper版metadata](https://api.modrinth.com/v2/project/worldedit/version?loaders=%5B%22bukkit%22%2C%22paper%22%2C%22spigot%22%5D)、[ViaVersion](https://github.com/ViaVersion/ViaVersion/releases/tag/5.12.2)、[ViaBackwards](https://github.com/ViaVersion/ViaBackwards/releases/tag/5.12.2)、[AdvancedPortals](https://github.com/sekwah41/Advanced-Portals/releases/tag/v2.8.0)、[DiscordSRV](https://github.com/DiscordSRV/DiscordSRV/releases/tag/v1.30.5)、[Floodgate](https://download.geysermc.org/v2/projects/floodgate/versions/2.2.5/builds/141)、[ServerBackupの作者配布ページ](https://www.spigotmc.org/resources/server-backup-ingame-dropbox-ftp-backup-1-18-1-21-multithreaded.79320/)。

coordinatorへ返す選定案は、調査時点の最新版であるGeyser b1294とLuckPerms 5.5.91への更新。ほか7本は、同じく最新版を照合した結果として現行と同じ版になる。実施準備時には最新版を再照合する。第三者artifactの最終採用、exact lock、新セットの動作確認は未完了で、横断gate判定はしていない。
