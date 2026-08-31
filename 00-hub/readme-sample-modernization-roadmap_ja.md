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

1. これは何か、誰が何に使えるか
2. 現在の提供状態と対応version
3. 最短の導入と「最初の成功」
4. 最小sampleと期待される画面／Minecraft上の結果
5. 主なcapabilityと、詳しいAPI／教材／運用文書への導線
6. 制約、データ変更、security、復旧の要点
7. examples、contribution、issue、licenseへの導線

release台帳、内部branch名、過去の設計論争、網羅的な設定一覧を冒頭へ置かない。情報を消すのではなく、正本や
詳細文書へ移してREADMEから案内する。Scratchのようなforkでは、McRemote固有の入口を先に示し、upstreamの
build／contribution情報へ明確に接続する。

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

昇格済みAPIのsampleは薄い呼出例だけで終えず、必要に応じて小さい操作から同じ機能を作るreconstruction sampleを
併置する。下流prototypeをpluginへ昇格した後も、旧prototypeを第二のproduction実装として永久保守する必要はない。
比較教材として残す場合は対象版と非推奨／教材用の状態を明示する。

rcまでのparticle／effect sampleは互換性の差を順に見せる。b6／protocol 23.0から既存の単点
`world.spawnParticle`、b7／23.1からdamage-capableな`world.strikeLightning`、b8／23.2からreceiver／typed dataを使うPython
3D graph、b9／23.3を発行した場合だけbatch版を置く。b8の単点版はb9後もreconstruction／性能比較sampleとして
残せるが、対象protocolと推奨用途を明示する。Scratch版は別trackで追従し、Python版との同時公開を必須にしない。

## 5. 進め方

### Pass A — 直ちに開始、b7前後

- public repoのtop-level READMEと既存sampleをinventoryし、古いversion、未実装claim、入口欠落を分類する。
- McRemote／Python／Java／Scratch／`mc_remote_samples`に、現在公開済みb6またはJava bootstrap baselineから
  動かせる最短経路を一つずつ置く。
- sample repoに一覧と実行前後のworld変更／cleanup表示を置く。

### Pass B — b8からAPI freeze

- sign、event、direction／navigation、entity、lightning、particle／3D graph、preview等をconcept／application
  sampleへ整理する。b8の単点particle sampleは、条件付きb9 batchを採るか判断する実測入力にもする。
- Python、Scratch、plugin／wireのどこで実現しているかを、利用者向け説明を壊さない小さな注記で追えるようにする。
- Stack、knowledgeを含む残READMEの入口とrepo間linkを揃える。

### Pass C — RCから初回stable

- install、update、rollback、既知制約、対応platformをstable candidateへ固定する。
- cold readerが会話履歴なしで最初の成功、sample選択、失敗時の戻り先へ到達できるか確認する。
- API reference／release noteの生成や半自動化は、手書きREADMEの役割が見えてから導入する。

Pass Aはb7 API実装の開始を止めるprotocol gateではないが、同時に着手する最優先companionとする。Pass Cは
初回stable readinessの重要入力とし、正式なHOLD条件はRC gate定義時に人間確認する。

## 6. 完了判定

- 初見の人がREADMEだけから対象、現行version、最初の操作、次の文書を選べる。
- copy可能な最小sampleが実行され、期待結果とcleanupが一致する。
- READMEのversion／support claimがrelease identityと一致する。
- sampleが実world変更と一時的なplayer表示を混同しない。
- READMEとsampleが独立した第二のcontractにならず、正本へ辿れる。
