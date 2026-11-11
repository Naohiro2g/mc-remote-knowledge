# Minecraft Remote Unity Sandbox

Unityの世界と箱庭の設計スポーク。一般用途のC# Client Library（`18-csharp-client/`）とは別の成果物である
（`2026-11-11-02`）。

## 現在地

- repository: `Naohiro2g/mc-remote-unity-sandbox`（MIT、public）。human ownerが2026-11-11に作った（初期commit
  `4d17e03955989f647d12bcff090fc00d94d249a8`。README、LICENSE、Unity用の`.gitignore`）
- Unityの版：6.6の修正版で試作を進め、近く出る6.7 LTSを検証して基準版にする（`2026-11-11-02`③）。移行の検証で使ったのは
  `6000.6.8f1`
- 2026-11-11：knowledgeがbootstrap（`AGENTS.md`、`.gitignore`の追記）を`2c1ed9febdee9d2a3d225ae6e3ed503ec1e23270`で置いた
- 2026-11-11：`minecraft-remote-csharp`から、ローカルデモ、設計メモ2本、図3件を履歴ごと移した（PR #1、merge commit
  `958b676e293427165e872d9abd7b5bfc4173efd6`。照合は`00-hub/unity-sandbox-migration-instructions_ja.md`の「返却と照合
  （2026-11-11）」）。正本はこのrepoの`main`にある

## 何を置くか

- Unityのproject（`unity/`）：今の通信を使わないローカルデモ（手順は`docs/local-demo_ja.md`、準備のscriptは`scripts/`）から、
  Unity Webへ
- 設計メモ：公開共有箱庭（`docs/unity-shared-sandbox-draft_ja.md`。到達形の案：URLを開けばPython、Scratch、C#で建築でき、
  複数人が同じ箱庭を見られるUnity Webの公開共有箱庭）と、Unity内部の先行作業（`docs/unity-internal-preparation_ja.md`。
  ブロックの材質、地面と座標、HUDのローカル表示、Web build、描画の性能）。図は`docs/diagrams/`。どちらもhuman ownerの起案
  （C#のrepoの`680ebb3`で入り、移行で`7a16a6e`になった）
- 後で：箱庭サーバー（Unityの世界のserver）と世界のモデル、C# Client Libraryを使う側のadapter

置かないもの：一般用途のC# Client Library（`minecraft-remote-csharp`）。Unityは公開された形でlibraryを使い、`src/`を直接
参照しない。Minecraft（Mojang）の素材。

## 旧for Unityと二つの世界

旧for Unity（`Naohiro2g/minecraft_remote_unity`）はアーカイブ扱いにした（`2026-10-22-08`）。Unityの中にserver
（受け手）とclient（送り手）を持ち、送り手は旧protocolのMcRemoteへもつながった。マイクラの世界とUnityの世界を二つの
出力先にでき、「serverが2種類×clientが多数」の形になる。

新protocolでは、一般用途のC# Client Libraryを先に作り、Unityには、そのlibraryを使う側として、またUnityの世界のserverと
して戻る。Unityの内部の準備は、共通のProtocolとClient Libraryに依存しないので、並行して進める（`2026-10-23-01`④）。
server側の範囲と学習の登山道は、`00-hub/NOTES_ja.md`の2026-10-18のpark（for Unityを新しいprotocolで続ける）に置いている。

## 正本境界

- wire、versioning、authentication等のProtocol contract: `10-protocol`
- C# Client Library: `18-csharp-client/`
- Unityのrepoと置くもの、Unityの版: `2026-11-11-02`
- Unity内部の準備を並行して進めること: `2026-10-23-01`
- 旧for Unityの扱い: `2026-10-22-08`
- 実装、build、Unityに閉じる判断: `Naohiro2g/mc-remote-unity-sandbox`

## bootstrapの手順

1. human ownerがGitHubでrepoを作る（済み。MIT、README、Unity用の`.gitignore`）
2. knowledgeが`AGENTS.md`をcommitし、`.gitignore`にoperator-localの`CLAUDE.md`、`NOTES_ja.md`、`handoff-materials/`と、
   `.env`を足してpushする（`00-hub/dev-repo-protocol_ja.md`の雛形。関連スポークは`19-unity/`、`18-csharp-client/`、`10-protocol/`）
3. knowledgeが手元のcloneに`CLAUDE.md`（`@AGENTS.md`の1行）を置いて、`AGENTS.md`のbootstrap commandが通ることを確かめる
4. `minecraft-remote-csharp`のCodexセッションが、移行の票のとおりに移す（済み。2026-11-11）

## AGENTS.mdの「このrepository固有の指示」

- Unity Editorの版は`19-unity/README_ja.md`の「現在地」に従い、使った版を記録する
- 一般用途のC# Client Library（`Naohiro2g/minecraft-remote-csharp`）の`src/`を直接参照しない。公開された形で使う
- Minecraft（Mojang）のtexture、model、音などの素材をcommitしない。自作か、licenseが明確で再配布できる素材だけを使い、
  出どころを記録する
- Unityの`Library/`、build成果物など、生成されるものをcommitしない
- Protocolやwire formatに触れる前に`10-protocol`、このrepositoryの作業では`19-unity`を読む
- 配布、公開の配信、release workflowは、knowledge SSOTで決まるまで足さない
- token、private endpoint、credential、operator-localの設定をcommitしない
- 横断する発見はlocalの`NOTES_ja.md`へ一時捕捉し、session／sliceの終わりにknowledge hubへ上げる
- 自分が編集したpathだけを明示stageする
