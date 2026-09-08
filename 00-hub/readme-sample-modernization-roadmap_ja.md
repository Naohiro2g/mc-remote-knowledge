# README・sample近代化ロードマップ

## 1. 目的

各public repositoryのREADMEを、内部経緯を知る開発者向けの断片から、人間が「何ができ、どう始め、次に何を
読めばよいか」を判断できる入口へ直す。sample codeはAPIの存在証明ではなく、動かす、観察する、改造する、
自分の部品へ作り直すための実行可能な学習面として整える。

このtrackはAPI追加後の仕上げではない。b7以降のAPI設計と並行して直ちに始め、追加APIの命名、粒度、各言語での
見え方をsampleからも評価する。READMEだけにcontractを持たせず、正本へリンクする投影層として扱う。

## 2. 対象とowner

| 対象 | owner | 最初に直す入口 |
| --- | --- | --- |
| `McRemote` | plugin repo | 対応Minecraft／Paper、導入、最小接続、permission、release取得 |
| `minecraft-remote-api` | Python repo | install、最小Python例、接続／pairing、API・examplesへの導線 |
| `scratch-editor` | Scratch repo | forkの目的、起動方法、接続、保存、WireScope、upstreamとの関係 |
| `minecraft-remote-java` | Java repo | build、接続／pairing、現行Client APIと一緒に検証する最小examples |
| `mc_remote_samples` | sample repo | concept-firstな言語間比較、実行環境、期待結果、変更／cleanup境界 |
| `mc-remote-stack` | Stack repo | 対応済みdeployment、最短runbook、更新／rollback、doctor |
| `mc-remote-knowledge` | knowledge repo | project全体像、各repoへの入口、設計・決定・教材の読み分け |

各repoは自READMEと実行可能codeを所有する。knowledgeは共通の利用者像、語彙、repo間導線、進捗を所有し、本文を
複製しない。privateなbackstage情報は対象外とする。

各Client Library開発repoは、現行APIと同じcheckoutでbuild／testできるREADME隣接の最小examplesを所有する。
`mc_remote_samples`はそれらを置き換えず、同じconceptを言語nativeな実装で比較する学習面を所有する。比較面は
正準exampleへlinkしても、学習目的の独立実装を持ってもよいが、owner不明のcopyを作らない。詳細は
`2026-08-30-01`と[Client sampleの配置と多言語学習UX](../20-教材/client-sample-learning-ux_ja.md)を正とする。

## 3. 人間向けREADMEの最小骨格

top-level READMEは、少なくとも次の順で答える。

1. これは何か、誰が何に使えるか（日本語主体で平易に）
2. 現在の提供状態と対応version（現行リリースを基準とし、過渡期や過去バージョンの釈明を書かない）
3. 最短の導入と「最初の成功」（3行・3ステップで到達できる手順）
4. 最小sampleと期待される画面／Minecraft上の結果
5. 主な作例（ワクワクするテーマ）と、詳しいAPI／教材／運用文書への導線
6. 制約、データ変更、security、復旧の要点
7. examples、contribution、issue、licenseへの導線

### 内部防衛・契約の隔離規律（Deep-hiding）

READMEは「投影層」であり、拘束層でも説明層でもない（`document-style-guide_ja.md`）。次の内部事情をREADME冒頭やファーストビューへ置くことを禁じる。これらはREADME下部の「開発者・詳細仕様（Advanced）」または別ファイル／別リポへ強制退避させる。

- **成果物検証データ**: SHA-256ハッシュ値、バイト数等のチェックサム（`manifest.json` や GitHub Release assets へ集約、`2026-09-06-02`）
- **ライセンス分離の弁明**: AGPL同梱の法務的経緯、ライセンス論争（`LICENSE`、`ARCHITECTURE.md`、`COMPLIANCE.md` へ退避）
- **過渡期の地層**: 「b6では…」「b7 prereleaseでは…」といった過去バージョンの比較・釈明（`CHANGELOG.md` や Release Notes へ退避）
- **プロトコル・通信詳細**: パケット仕様、ネゴシエーション内部処理（`10-protocol/` へリンク）
- **主要言語方針と日英パラレルの排除**: プロジェクト全体の第一言語（日本語）単一SSOT方針（`LANGUAGE_POLICY.md`、決定 `2026-09-08-02`）に基づき、英語優先や同一ファイル内での日英逐語並記を廃止する。各リポREADME冒頭にはナレッジリポの `LANGUAGE_POLICY.md` へのリンクを含む標準Noteアラートを置き、本文は平易な日本語で通読性を最大化する。

Scratchのようなforkでは、McRemote固有の入口を先に示し、upstreamのbuild／contribution情報へ明確に接続する。

## 4. sampleの段階

| 段階 | 役割 | 例 |
| --- | --- | --- |
| minimum | installと接続が成立する最小例 | hello、player position、chat |
| concept | 一つの概念を短く観察する | sign、event、direction、preview |
| application | 複数APIで意味のある体験を作る | 建築、walkthrough、HUD、3D turtle |
| reconstruction | 用意された機能を自分のcodeで作り直す | helper、class、module、Scratch定義block |

各sampleは、最小protocol／client package版、確認したMinecraft／Paper target、前提、実行方法、期待結果、
実worldを変更するかplayerだけの表示か、cleanup、利用するMcRemote API、実現位置と成熟状態、関連するPaper
capabilityを短いmetadataまたはREADMEで示す。`DEBUG`／`TRACE`／`FAST`の実行modeと、`REAL`／`PREVIEW`／
`PYGAME`等の出力先は別fieldにする。複数言語で同じsampleを機械的に複製せず、その言語で自然な入口と学習目的を
明記する。

**三層モデル（実現位置）注記の学習面からの排除**: 「これはどの層（プラグイン／ワイヤ／クライアント）で実現しているか」の追跡（`2026-08-29-01`）は、README本体や入門sampleに露出させない。それは初学者にとって不要な認知ノイズである。実現位置の追跡は教材の発展編（reconstruction sample）や設計ドキュメントの役目に限定し、入門sampleの主眼は「学習者がワクワクするテーマ別作例（建築、ミニゲーム、ドット絵など）」へ集中させる。

昇格済みAPIのsampleは薄い呼出例だけで終えず、必要に応じて小さい操作から同じ機能を作るreconstruction sampleを
併置する。下流prototypeをpluginへ昇格した後も、旧prototypeを第二のproduction実装として永久保守する必要はない。
比較教材として残す場合は対象版と非推奨／教材用の状態を明示する。

rcまでのparticle／effect sampleは互換性の差を順に見せる。b6／protocol 23.0から既存の単点
`world.spawnParticle`、b7／23.1からdamage-capableな`world.strikeLightning`、b8／23.2からreceiver／typed dataを使うPython
3D graph、b9／23.3を発行した場合だけbatch版を置く。b8の単点版はb9後もreconstruction／性能比較sampleとして
残せるが、対象protocolと推奨用途を明示する。Scratch版は別trackで追従し、Python版との同時公開を必須にしない。

## 5. 進め方

### Pass A — 直ちに開始（初学者向けフロントエンドの奪還）

- **【最優先】最重要2リポ（Python, Scratch）のファーストビューを奪還**: 「3行・3ステップで動く人間向けガイド」に差し替える。
- **基準バージョンの更新と地層一掃**: 現行の公開リリース（b7 / b7.post2）および間近のb8を基準とし、過去の過渡期釈明（b6差分、prerelease注意書き等）を一掃する。
- **内部事情の隔離（Deep-hiding）**: SHA-256ハッシュ値、WireScopeライセンス条項、プロトコルネゴ詳細などをREADME冒頭から別セクション／別文書へ完全退避。
- **日英パラレルの解消**: 日本語主体の平易でスッキリした構成へ整える。
- **【完了検証】Cold Reader（冷読者）テスト**: 前提知識のない初学者（または独立した新規LLMセッション）が、READMEだけを見て3分で「最初の成功（ブロック設置またはチャット）」に到達できることをPass Aの完了条件として前倒し実施する。

### Pass B — b8期（ワクワクする作例・サンプルの拡充）

- **テーマ別作例カタログの整備**: `mc_remote_samples` のサンドボックスアドレスを更新し、建築、アート、ミニゲーム等のテーマ別作例を展開する。
- **段階的ステップアップの提示**: 「ブロックを置く」から「イベント（叩いた、話した）を使う」「プレイヤーを動かす」への明確な学習パスを示す。
- **三層モデル注記の隔離**: 内部の実現位置追跡はREADMEに露出させず、発展教材（reconstruction sample）や設計文書へ閉じる。
- **残るリポの骨格統一**: McRemote (plugin)、Stack、Java client、および本knowledgeリポのREADMEを人間向け骨格へ揃える。

### Pass C — RCから初回stable（辞書機能の完全分離）

- **API Referenceの生成分離**: 網羅的なAPI一覧・シグネチャ・戻り値は、生成ツールによる「API Reference」（`2026-09-04-06`）へ完全に分離し、手書きREADMEを辞書化させない。
- **薄く親切な入口の完成**: READMEは「ようこそ ＋ クイックスタート ＋ 代表作例 ＋ リファレンスへの案内」という薄い入口に徹する。
- **安定運用の固定**: install、update、rollback、既知制約、対応platformをstable candidateへ固定する。

## 6. 完了判定

- **Cold Reader通過**: 前提文脈のない初見の人がREADMEだけから3分で最初の操作に成功できる（Pass Aで検証済み）。
- **ファーストビューの純化**: README冒頭に内部事情（ハッシュ、過渡期地層、ライセンス弁明）がなく、初学者が歓迎される入口になっている。
- **copy可能な最小sample**: 最小sampleが実行され、期待結果とcleanupが一致する。
- **バージョン主張の一致**: READMEのversion／support claimが現行release identityと一致し、過去バージョンの言い訳を含まない。
- **辞書の分離**: 網羅的API仕様が生成API reference（人間可読版・機械可読版）へ分離され、READMEが肥大化していない。
- **投影層の規律**: READMEとsampleが独立した第二のcontractにならず、正本へ辿れる。
