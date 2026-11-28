# Minecraft Remote Unity Sandbox

.NET箱庭とUnity Webアプリの設計スポーク。2つは、repo `mc-remote-unity-sandbox`、image、1つのcontainerに同居している
（`2026-11-28-01`④、`2026-11-28-03`②）。一般用途のC# Client Library（`18-csharp-client/`）とは別の成果物である
（`2026-11-11-02`）。この決定より前の記録の「Unity箱庭」は、この組を指す。

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
- 2026-11-15：最初の区切りが1台のPCで動いた。human ownerが、ScratchのLANパッケージとPythonのclientからUnity箱庭のserverへ
  つなぎ、ペアリングして建てた（wireの確定形を入れた後）。実装はまだcommitされていない（照合は
  `00-hub/unity-sandbox-first-slice-instructions_ja.md`の「返却と照合（2026-11-15）」）。残りを仕上げてPRにする票を出した
  （`00-hub/unity-sandbox-first-slice-pr-instructions_ja.md`）
- 2026-11-15：Unity箱庭を台帳のcomponentに入れ、最初の公開を`2321.3`にした（`2026-11-15-04`）。配る形（`2026-11-15-05`）、
  tokenの扱い（`2026-11-15-06`）、helloの`protocol`（`2026-11-15-03`④）を入れる票を出した
  （`00-hub/unity-sandbox-release-instructions_ja.md`）
- 2026-11-16：PR #2（最初の区切りと`2321.3`の準備、head `bba6e4ca25a7d2a9d5798b99ad049a60022c85b0`）を照合し、human ownerが
  mergeした（merge commit `d29a577643bd44942de99fbd075a24178036f4c4`）。1回に置ける数を越えたときのreason（`2026-11-16-02`）とimageをbuildするmachine（`2026-11-16-03`）を決め、次の票を
  出した（`00-hub/unity-sandbox-release-instructions_ja.md`の「返却と照合（2026-11-16）」と「次にすること（2026-11-16）」）
- 2026-11-16：LANで配るものを使う側とサーバー役に分け（`2026-11-16-04`）、Unity箱庭のLANのセットをhuman ownerと相談して
  進める票を出した（`00-hub/unity-sandbox-lan-instructions_ja.md`）。`2321.3`に間に合えば入れ、間に合わなければ`2321.4`
- 2026-11-16：公開の名前を`unity-sb`（最新版）と`unity-sb-lts`（LTS）にした（`2026-11-16-05`）。最初の公開から両方を出し、
  版が分かれるまでは同じcontainerを指す。ホームページの「はじめる（1）」は、`scratch-lts`から`unity-sb-lts`へつなぐ
- 2026-11-16：PR #3（`block_count_limit_exceeded`と、相談して足したmethod、head `03d3eade37190a090cee26cfcbccfd6b52e0bb40`）を照合し、
  human ownerがmergeした（merge commit `d3539c3964c4dc9b19b969999ebde729f530fa6e`。`00-hub/unity-sandbox-release-instructions_ja.md`の
  「PR #3の返却と照合（2026-11-16）」）
- 2026-11-17：最初の公開を`2321.2.0`にした（`2026-11-17-01`）。候補の返却に要るものは、`00-hub/23212-gate-candidate-instructions_ja.md`の
  「範囲を広げた後の候補（2026-11-17）」
- 2026-11-17：`unity-sb`と`unity-sb-lts`を、`scratch`と`scratch-lts`の組の接続先の一覧に入れる。`2321.2`を出すのを待たない。
  はじめる（1）は、既定のMinecraftのLTSから、利用者がUnity箱庭を選ぶ（`2026-11-17-04`）
- 2026-11-24：公開VPSのUnity箱庭に、serverに上限を入れた版を出す（`2026-11-24-01`。`2321.2.0`は`1594805`、`2400.0.0rc1`は
  `6ce475e`。照合は`00-hub/release-gate-notes_ja.md`の「Unity箱庭の上限の対策版の照合（2026-11-24）」）
- 2026-11-28：「Unity箱庭」を、.NET箱庭とUnity Webアプリに分けて呼ぶ（`2026-11-28-01`）。公開の名前を、.NET箱庭は`dotnet-sb`と
  `dotnet-sb-lts`、Unity Webアプリは`unity-app`と`unity-app-lts`にし、旧名の`unity-sb`と`unity-sb-lts`はCNAMEで残す
  （`2026-11-28-02`）。repoは当面このまま同居させる。分けるときの形は下の「repoを分けるとき」（`2026-11-28-03`②）。画面に出る
  旧名の文字（タブの題とchatの歓迎文）は、最新版の`2400.0.0`の最後の候補で替え、LTSの`2321.2.0`は旧名のまま出す（`2026-11-28-04`）

## 公開Unity箱庭

URLを開けば、Minecraftを買わず入れずに、Scratchから建てられる公開の箱庭。Unity版マイクラリモコンの最初の段として、
2026-11-13に最優先にした（`2026-11-13-04`）。見出しは前の記録が指すので変えない。中身は.NET箱庭とUnity Webアプリ。

- 名前（`2026-11-28-01`）：世界とserverは「.NET箱庭」、ブラウザで開いて見るものは「Unity Webアプリ」。公開の面で接続先を言う
  ときは「.NET箱庭サーバー」（`2026-11-28-02`）。記録でも、1つの箱庭を指すときは「マイクラ箱庭」「.NET箱庭」と名前で書く。
  前の記録の「Unity箱庭のserver」は.NET箱庭のserverを、「箱庭サーバー」はMinecraftの公開serverを指す
- 経路：Scratch → Bridge → .NET箱庭のserver → 表示同期 → Unity Webアプリ。.NET箱庭のserverは、McRemoteと同じ改行区切りの
  JSON-RPCをTCPで受ける。ほかのclientも同じserverへつながる。serverの形は、設計メモの第一案（描画しない.NETのprocess）
- 表示同期（`/ws/sync`）：契約の正本はこのrepoの`docs/unity-sandbox-display-sync_ja.md`で、knowledgeへ上げない。Unity Webアプリの
  ほかに、手元の実験としてBevy Webアプリ（`22-bevy/`）が同じserverへつなぎ、固定したcommitで読んで追う。.NET箱庭とUnity Webアプリの
  作業と公開に、新しい義務は足さない（`2026-11-27-01`）
- pairing：Scratchに出たcodeを、Unity Webアプリのchatで`/mcremote pair NNN-NNN`と打って承認する。Minecraftでの操作と同じにする
- 世界のモデル：Minecraft 1.21.11に準拠する。高さは-64〜319、地面も置き換えられ（リセットで戻す）、blockはIDとstateで持つ
  （`minecraft:gold_block`など）。どこまで沿わせるか（blockのふるまいなど）は段ごとに決める
- 地形と基本のblock（human owner 2026-11-14、2026-11-15）：最初から整地してある。区画の原点のまわり（x、zが原点から±48）は、
  草（`minecraft:grass_block`）がy=62。区画の間はy=62が空気で、y=61の土が見える。その下は、土（`minecraft:dirt`）が61〜60、
  石（`minecraft:stone`）が59〜-64。基本のblockは、空気、草、土、石、金、鉄、シーランタン、ガラス、ダイヤモンド、TNT。
  地面の中のイースターエッグは、各区画の原点の真下の3×3に、yが10の倍数（-60〜50）の層で置いた
- 版と配る形：版は台帳のX.Y.Zに従い、serverとUnity Webアプリを同じ版で出す（`2026-11-15-04`）。最初の公開は`2321.2.0`（`2026-11-17-01`）。Unity Webアプリ
  （WebGLのbuild）を入れたcontainer imageをGHCRへpushし、Stackが公開VPSで動かす（`2026-11-15-05`）。imageは`ghcr.io/naohiro2g/mc-remote-unity-sandbox`で公開し、凍結の前に候補のtagで置いて、
  GHCRのdigestで照合する（`2026-11-17-02`）。WebGLはUnityの開発機で、
  imageはhuman ownerが決めた手元の1台のDockerでbuildする（`2026-11-16-03`）。LANでは、.NET箱庭のserverとUnity Webアプリの
  セットを、Scratch LANパッケージと別に配る（`2026-11-16-04`）

### .NET箱庭のserverが応えるもの

`2026-11-14-01`、`2026-11-14-02`。Scratchが今のままつながる範囲から決めた（Scratchの返却は
`00-hub/unity-sandbox-scratch-instructions_ja.md`の「返却と照合（2026-11-14）」）。`server`の形と`out_of_bounds`の`data`は、
McRemoteの返却を見て`2026-11-14-03`、`2026-11-14-04`で決めた。

- 待ち受け：McRemoteと同じ改行区切りのJSON-RPCをTCPで受ける。portの既定は`25585`で、起動のときに変えられる
  （`2026-11-15-01`。同じPCでMcRemoteの`25575`と並べられる）。手元のcompose、LAN、公開VPSのどれでも既定は`25585`
  （`2026-11-18-01`）。同じ機械で2つを動かすときは、片方を既定から変える。公開VPSは、TCPを外へ開け、LTSの`dotnet-sb-lts`を
  `25585`、最新版の`dotnet-sb`を`25586`にする（`2026-11-20-03`、名前は`2026-11-28-02`）
- hello：`protocol`は`23.3.0`（`2026-11-15-03`④）。`mc_version`と`supported_mc_versions`は、世界のモデルが従う`1.21.11`。.NET箱庭であることは`server`で
  名乗る（`name`は`mc-remote-unity-sandbox`、`version`は組の版、`2026-11-15-04`）。`dimension`は`minecraft:overworld`だけ、buildを省いたときの`origin`は`[0, 0, 0]`、`world_constants`は
  `y_sea`だけ（ほかのkeyは`2400`）、`permissions`はMcRemoteと同じ形
- tokenと画面：tokenは、chatで`/mcremote pair NNN-NNN`を打った画面に結ぶ。画面は、browserに残る推測できない画面のIDで見分け、
  そのIDはどこにも出さない。helloの`player`は、画面ごとに作るUUID（画面のIDとは別。Minecraftのaccountではない）。pairingは
  `pairing_id`で相関し、TCPの接続に結ばない。codeの有効時間は120秒。世界のリセットではtokenを消さない。serverの再起動の後には残さない（`2026-11-15-06`）
- catalog：基本の10種類を、1.21.11と同じstatesと既定で返す。同じIDは、McRemoteが1.21.11で返すcatalogと同じ中身。一覧に無い
  blockは`unknown_block`
- 応えるmethod：`hello`、`auth.pairBegin`、`auth.pairPoll`、`catalog.get`、`events.poll`（空の応答）、`chat.post`、`world.setBlock`、
  `world.getBlock`、`world.setBlocks`（FASTのnotificationを含む）、`build.setDimension`、`build.setOrigin`、`connection.flush`。
  ほかは`method_not_found`
- 世界の外：置ける高さ（-64〜319）の外と、400×400の外周の外へ置く、または読むと、`out_of_bounds`（McRemoteも同じ。Minecraftの
  水平方向の端はworld border）。`data`はwire §7.3の表の下の箇条の形で、外周は中心`(0, 0)`、大きさ`400`のworld borderとして
  返す。権限による範囲の外は`build_range_exceeded`（`2026-11-14-05`）
- 1回に置ける数：`world.setBlocks`は32,768個まで。越えると`block_count_limit_exceeded`（`data.limit`と`data.requested`。McRemoteと
  同じ形、`2026-11-16-02`）
- 上限（`2026-11-24-01`）：TCPの接続の数（全体、helloの前、送り元ごと）、helloの前に待つ時間とhelloまでの期限、`auth.pairBegin`の
  回数、承認を待つcodeの数、1行の長さ、Unity Webアプリの`/ws/sync`の受け取る長さに上限がある。当たると、応答を返さずに閉じる
  （McRemoteと同じ、`2026-10-07-02`）。helloの後は、何も来なくても切らない。値の正本は`mc-remote-unity-sandbox`のsource。Bridgeを通る利用者は、
  serverから1つの送り元に見える
- ホームページのトップの「はじめる」：はじめる（1）は、`scratch-lts`から`dotnet-sb-lts`へつなぎ、`unity-app-lts`で見る。
  はじめる（2）は、ScratchやPythonから`sb`か`dotnet-sb`へつなぐ（`2026-11-28-02`④）
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
- .NET箱庭のserverと世界のモデル：最初の区切りで作る（`2026-11-13-04`）
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
- Unity箱庭は`d3539c3`の時点でMinecraftの座標をそのまま写していて、見え方が鏡像になる（北を向くと東が左）。右手系と北向きの
  標準（`00-hub/world-coordinates-facts_ja.md` §2）に合わせて直し、最初のカメラを北に向ける（human owner 2026-11-20）。12月1日の
  LTSの`2321.2.0`と`2400.0.0`に入れる（`2026-11-20-01`）

## 正本境界

- wire、versioning、authentication等のProtocol contract: `10-protocol`
- C# Client Library: `18-csharp-client/`
- Unityのrepoと置くもの、Unityの版: `2026-11-11-02`
- 公開Unity箱庭の優先、pairing、1.21.11への準拠: `2026-11-13-04`（名前は`2026-11-28-01`で改めた）
- 座標の見え方（右手系、北向きの標準）: `2026-11-20-01`
- 3層の呼び方（.NET箱庭とUnity Webアプリ）と、前の記録の「Unity箱庭」の読み方: `2026-11-28-01`、`00-hub/sandbox-layers-guide_ja.md`
- 公開の名前（`dotnet-sb`、`dotnet-sb-lts`、`unity-app`、`unity-app-lts`）と旧名のCNAME: `2026-11-28-02`。最新版とLTSの組と
  「はじめる（1）」: `2026-11-16-05`、`2026-11-17-04`。公開VPSのportと「はじめる（2）」: `2026-11-20-03`
- 同居と、repoを分けるときの形: `2026-11-28-03`②
- 版と配る形: `2026-11-15-04`、`2026-11-15-05`、`2026-11-16-03`、`2026-11-16-04`
- Unity内部の準備を並行して進めること: `2026-10-23-01`
- 旧for Unityの扱い: `2026-10-22-08`
- `/ws/sync`を使う2つ目の参加アプリ（Bevy Webアプリ）: `2026-11-27-01`、`22-bevy/`
- 実装、build、Unityに閉じる判断: `Naohiro2g/mc-remote-unity-sandbox`

## repoを分けるとき

当面は、このrepoに.NET箱庭とUnity Webアプリを同居させる。分けるときは、`mc-remote-dotnet-sandbox`（server、世界のモデル、
`/ws/sync`の契約）と`mc-remote-unity-app`（Unity Webアプリ）を新しく作って履歴ごと移し、このrepoをアーカイブする
（`2026-11-28-03`②）。knowledgeとevidenceが固定して参照しているcommitとGHCRのdigestは、旧名のまま使える。

分けるときに見るもの（claude.aiの案）：

- helloの`server.name`（今は`mc-remote-unity-sandbox`、`WorldConstants.DefaultServerName`）と、それを見て絞り込むclient（Scratchの
  GUIが、未対応の操作のエラーに出すserverの名前を選ぶのに使っている。2026-11-28のScratch担当の返却）
- 保存のkey、URLのquery、環境変数（hub NOTESの「参加アプリと箱庭の内部の名前」）
- namespaceの`Code2Create.UnitySandbox.*`
- image `ghcr.io/naohiro2g/mc-remote-unity-sandbox`（digestを固定して参照しているので消さない）
- productNameとchatの文（最新版は`2400.0.0`で新しい語にする。`2026-11-28-04`）
- LANのセットの置き場所
- Bevy Webアプリの`AGENTS.md`の`/ws/sync`の参照先
- Stack、台帳のcomponent（`2026-11-15-04`）、このスポーク

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
