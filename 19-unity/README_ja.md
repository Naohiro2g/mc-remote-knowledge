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
- 2026-11-13：公開Unity箱庭を最優先にした（`2026-11-13-04`、下の「公開Unity箱庭」）。最初の区切りの票を、Unity
  （`00-hub/unity-sandbox-first-slice-instructions_ja.md`）とScratch（`00-hub/unity-sandbox-scratch-instructions_ja.md`）へ出した

## 公開Unity箱庭

URLを開けば、Minecraftを買わず入れずに、Scratchから建てられる公開の箱庭。Unity版マイクラリモコンの最初の段として、
2026-11-13に最優先にした（`2026-11-13-04`）。

- 名前：「Unity箱庭」、そのserverを「Unity箱庭のserver」と呼ぶ。今の記録で「箱庭サーバー」と書くと、Minecraftの公開server
  を指す
- 経路：Scratch → Bridge → Unity箱庭のserver → 表示同期 → Unity Web。Unity箱庭のserverは、McRemoteと同じ改行区切りの
  JSON-RPCをTCPで受ける。ほかのclientも同じserverへつながる。serverの形は、設計メモの第一案（描画しない.NETのprocess）
- pairing：Scratchに出たcodeを、Unity Webのchatで`/mcremote pair NNN-NNN`と打って承認する。Minecraftでの操作と同じにする
- 世界のモデル：Minecraft 1.21.11に準拠する。高さは-64〜319、地面も置き換えられ（リセットで戻す）、blockはIDとstateで持つ
  （`minecraft:gold_block`など）。どこまで沿わせるか（blockのふるまいなど）は段ごとに決める
- ホームページのトップの「はじめる」：公開Unity箱庭が使えるようになったら、Scratch→Unity箱庭にする。それまでは今の流れのまま
- UnityからMinecraftを動かすこと（`10-protocol/polyglot-client-roadmap_ja.md`のMilestone I）は、その後にする
- 最初の区切り：1台のPCで、今のScratchからBridgeを通して、Unity箱庭のserverへ4つの操作（`chat.post`、`world.setBlock`、
  `world.getBlock`、`world.setBlocks`）を送り、Unity Webの画面に出る。次に、Stackで公開VPSへ出す。hubで決めることと、公開の
  前に要るものは、hub NOTESの「公開Unity箱庭へ進む」の行にある

## 何を置くか

- Unityのproject（`unity/`）：今の通信を使わないローカルデモ（手順は`docs/local-demo_ja.md`、準備のscriptは`scripts/`）から、
  Unity Webへ
- 設計メモ：公開共有箱庭（`docs/unity-shared-sandbox-draft_ja.md`。到達形の案：URLを開けばPython、Scratch、C#で建築でき、
  複数人が同じ箱庭を見られるUnity Webの公開共有箱庭）と、Unity内部の先行作業（`docs/unity-internal-preparation_ja.md`。
  ブロックの材質、地面と座標、HUDのローカル表示、Web build、描画の性能）。図は`docs/diagrams/`。どちらもhuman ownerの起案
  （C#のrepoの`680ebb3`で入り、移行で`7a16a6e`になった）
- Unity箱庭のserverと世界のモデル：最初の区切りで作る（`2026-11-13-04`）
- 後で：C# Client Libraryを使う側のadapter

置かないもの：一般用途のC# Client Library（`minecraft-remote-csharp`）。Unityは公開された形でlibraryを使い、`src/`を直接
参照しない。Minecraft（Mojang）の素材。

## 旧for Unityと二つの世界

旧for Unity（`Naohiro2g/minecraft_remote_unity`）はアーカイブ扱いにした（`2026-10-22-08`）。Unityの中にserver
（受け手）とclient（送り手）を持ち、送り手は旧protocolのMcRemoteへもつながった。マイクラの世界とUnityの世界を二つの
出力先にでき、「serverが2種類×clientが多数」の形になる。

新protocolでは、一般用途のC# Client Libraryを先に作り、Unityには、そのlibraryを使う側として、またUnityの世界のserverと
して戻る。Unityの内部の準備は、共通のProtocolとClient Libraryに依存しないので、並行して進める（`2026-10-23-01`④）。
server側の範囲と学習の登山道は、下の「やりたいことと未決」に置く。

## やりたいことと未決

もとはhub NOTESの2026-10-18のpark（for Unityを新しいprotocolで続ける）にあった。2026-11-13に、ここへ移した（`2026-11-13-03`）。

- 旧for Unity：`Naohiro2g/minecraft_remote_unity`（最後のcommitは2023-10、forkに`kazu2g/minecraft_remote_unity`）は、C#の
  serverとclientを内包し、旧protocolの`setBlock`と`setBlocks`を持っていた。`PythonScripts/`のコードは、Unityの世界とマイクラの
  世界を切り替えてそのまま動き、外のPythonからのリモコンもできた。マイクラの世界とUnityの世界を交換できた。ブロックは4、5種類の
  制限があったが、テクスチャを取り込んでほぼすべてのブロックを再現しようとしていた
- やりたいこと（human owner 2026-10-18）：C#のclientと、C#のserver／Unityの世界の利用の両方。できるならどこまでも。PythonがTCPを
  残すのは、シンプルな通信を学ぶ素材としてで、Unityでもそれができる。Scratchと同じWebSocketのルートも使えるようにする。
  マイクラの単純なシミュレーションから、もっとUnityネイティブに振ってもよい
- 見込み（human owner）：認証はclientとしてはそれほど大変でなく、serverとしてもMcRemoteで実現したものを取り込める。wire §2
  では、Bridgeからプラグインまでも直接TCPなので、UnityのserverがTCPを話せば、ScratchがBridge経由で届く見込みがある（未確認）
- 二つの向き（2026-10-18）：Unityからマイクラへは、C#のclient（Phase Iに収録済み）。外形はPythonのclientと同じ系列で、Unityの
  中にpairingを入れれば、Unityのフレームの中からマイクラへつながる。Pygameへ出しているものがマイクラにも、というのと同じで、
  `20-教材/ai-learning-design_ja.md`の出力先の軸（`REAL`／`PREVIEW`／`PYGAME`）にUnityが加わる。PythonからUnityへは、Unityが
  serverになる側。二つがそろうと旧for Unityの交換になる
- clientの気をつける点：通信でフレームを止めない（UnityのAPIは主スレッドから）、pairingの表示とcredentialの置き場所、WebGLでは
  TCPが使えずWebSocketとBridgeを通る
- 判断の軸：なんでもできるからなんでもやる、ではなく、その中で創造性を引き出せる学習の登山道を見つけ出す
- 未決：どのAPIの範囲で交換できればよいか、ブロックIDとUnityの表現の対応（IDは1.21.11のものを使う：`2026-11-13-04`④）、
  登山道の形
- 記録の欠け：`10-protocol/polyglot-client-roadmap_ja.md`の「25. Phase I — C# / Unity」はC#のclientしか扱わず、server側と、
  二つの世界を交換できることは収録されていない

## 正本境界

- wire、versioning、authentication等のProtocol contract: `10-protocol`
- C# Client Library: `18-csharp-client/`
- Unityのrepoと置くもの、Unityの版: `2026-11-11-02`
- 公開Unity箱庭の優先、pairing、1.21.11への準拠、名前: `2026-11-13-04`
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
