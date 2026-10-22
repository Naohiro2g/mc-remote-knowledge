# Minecraft Remote for C#

現行Minecraft Remote ProtocolをC#へ投影する、一般用途Client Libraryの設計スポーク。Unity専用品にはしない。
Unityは、このlibraryを使う主な場の一つである（`10-protocol/polyglot-client-roadmap_ja.md` §25）。

## 現在地

`2026-10-22-07`で、担当sessionを呼べるbootstrapまでrepoを先に作ると決めた。実装は、多言語の比較とconformanceの
一般化（ロードマップのPhase E／F）をknowledgeで具体化してから始める。

- repository: `Naohiro2g/minecraft-remote-csharp`。bootstrapは`4b295a0404b2fea7b4e5d4eedc3e880d2bc8aec7`（knowledge
  `41e3680`を読んだ。CI 39832732071が成功し、test 1件が通った。2026-10-23にknowledgeが照合した）
- toolchain: miseで固定した.NET SDK 10.0.402。library projectのtargetは`netstandard2.1`だけで、test projectは.NET 10で動く
- 根のnamespace: `Code2Create.MinecraftRemote.Client`（Javaの`club.code2create.mcremote.client`と同じC2CCの系列）
- target: `netstandard2.1`を含める（Unityから使える）
- NuGetのpackage ID: `MinecraftRemote.Client`は第一候補で、NuGetへ出す準備のときに決める（NOTES 2026-08-29）
- 比べる基準: 初回stable `2321.0.0`（protocol `23.2.1`）

## 旧for UnityとUnityの世界

旧for Unity（`Naohiro2g/minecraft_remote_unity`）はアーカイブ扱いにした（`2026-10-22-08`）。Unityの中にserver
（受け手）とclient（送り手）を持ち、送り手は旧protocolのMcRemoteへもつながった。マイクラの世界とUnityの世界を二つの
出力先にでき、「serverが2種類×clientが多数」の形になる。

新protocolでは、まずこのrepoで一般用途のClient Libraryを作る。Unityには、このlibraryを使う側として、また
Unityの世界のserverとして後で戻る。server側の範囲と学習の登山道は、`00-hub/NOTES_ja.md`の2026-10-18のpark
（for Unityを新しいprotocolで続ける）に置いている。

## 正本境界

- wire、versioning、authentication等のProtocol contract: `10-protocol`
- 多言語展開の進行: `10-protocol/polyglot-client-roadmap_ja.md`（§25）
- 名前: `2026-08-29-03`
- bootstrapと実装の順番、namespace、target: `2026-10-22-07`
- 旧for Unityの扱い: `2026-10-22-08`
- 実装、build、C#に閉じるClient APIの判断: `Naohiro2g/minecraft-remote-csharp`

C#も、JavaやPythonのコードを翻訳して作らない。Protocol contractと共有fixtureを主な入力にする。

## bootstrapの手順

1. human ownerがGitHubでrepoを作る。Javaと同じく、LICENSE（MIT）とREADMEの初期commit
2. knowledgeが`AGENTS.md`と`.gitignore`（operator-localの`CLAUDE.md`、`NOTES_ja.md`、`handoff-materials/`と、`.env`を外す。Javaと同じ）をcommitしてpushする
   （`00-hub/dev-repo-protocol_ja.md`の雛形。関連スポークは`18-csharp-client/`と`10-protocol/`）
3. knowledgeが手元のcloneを作り、`CLAUDE.md`（`@AGENTS.md`の1行）を置いて、`AGENTS.md`のbootstrap commandが
   通ることを確かめる（human owner 2026-10-22の依頼。dev-repo protocolでは運用者の作業）
4. 担当sessionが、下の「bootstrapで作るもの」を作って返す

## bootstrapで作るもの

- .NET SDK（miseで選ぶ）、solution、library project、test project
- library projectのtargetに`netstandard2.1`を含める。ほかのtargetを足すかは担当の案。test projectは今の.NETのLTSで動かす
- 根のnamespace`Code2Create.MinecraftRemote.Client`で、root namespaceのunit test 1件、GitHub ActionsのCI
- README（何のrepoか、まだ実装の前であること、knowledgeへの入口）

入れないもの:

- transport、`hello`、authentication等のprotocolの実装（Phase E／Fの具体化の後）
- NuGetへのpackとpublishの設定、release workflow
- Unityのproject

返却: 実際に読んだknowledge commit、bootstrapのcommit、CIのrun、.NET SDKの版、library projectのtarget

## AGENTS.mdの「このrepository固有の指示」（案）

- .NET SDKの選択と切り替えはmiseを正準とする。library projectのtargetに`netstandard2.1`を保つ
- 根のnamespaceは`Code2Create.MinecraftRemote.Client`とし、repository名やNuGetのpackage IDから置き換えない
- NuGetのpackage ID、publish、release workflowは、knowledge SSOTで決まるまで足さない
- wire formatに触れる前に`10-protocol`、このrepoの作業では`18-csharp-client`を読む
- token、private endpoint、credential、operator-localの設定をcommitしない
- 横断する発見はlocalの`NOTES_ja.md`へ一時捕捉し、session／sliceの終わりにknowledge hubへ上げる
- 自分が編集したpathだけを明示stageする
