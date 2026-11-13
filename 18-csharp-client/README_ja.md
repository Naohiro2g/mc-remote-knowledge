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
- 2026-11-11：TypeScriptの最初の縦sliceが通ったので、最初の縦slice（helloからsetBlock／getBlockまで、直接のTCP）の実装を
  始める票を出した（`00-hub/polyglot-csharp-start-instructions_ja.md`）
- 2026-11-12：最初の縦sliceが通った（PR #3、merge `bbca1e44dd0e6defc1092d1d47f956918904658e`）。F1の取得元をtooling `d2691cd`へ
  固定し直し、v1の52 caseをCIで通した（PR #4、merge `1f069dc321dbb3534447584946ec2cfd7912a289`）。実McRemoteとのpulseと、Unity
  6000.6.8f1でDLLが動くことを確かめた。待ち方と自動のつなぎ直し（`2026-11-11-01`③⑤）はまだ入れていない。照合は同じ票の
  「返却と照合（2026-11-12）」
- 2026-11-13：待ち方と自動のつなぎ直し（`2026-11-11-01`③⑤）と、pairingの途中の切断（`2026-11-12-05`）を入れ、F1の取得元を
  tooling `335c604`へ固定し直した（PR #5、merge `0f9f12d41376d78b92e51700b395dde50ee56de9`）。v1の54 caseと、v2の12 caseのうち
  10 caseをCIで通した（OP-06、OP-11は無い機能のためtodo）。`ConnectionRestored`などをUnityのmain threadへ戻す例をdocsに書き、
  repo外のUnity 6000.6.8f1で更新したDLLが動くことを確かめた。照合は`00-hub/polyglot-e2-reconnect-instructions_ja.md`の
  「返却と照合（2026-11-13）」。応答待ちの長さが違うときに最長へ合わせる直し（`2026-11-13-01`）は、次のC#の票で頼む

## Unityとの関係

Unityの世界と箱庭は、2026-11-11に新しいrepo `Naohiro2g/mc-remote-unity-sandbox`へ分けた（`2026-11-11-02`、スポークは
`19-unity/README_ja.md`）。このrepoは一般用途のClient Libraryだけを持つ。Unityは、ほかの利用者と同じく公開された形で
このlibraryを使う。Unityへ渡す形（packageやDLL）は、libraryの配布としてこのrepoで扱う。

旧for Unity、二つの世界、Unity内部の準備の説明は`19-unity/README_ja.md`へ移した。2026-11-11まで、ここに置き、
「Unity用のrepoやpackageの置き場所は未決」としていた。

## 正本境界

- wire、versioning、authentication等のProtocol contract: `10-protocol`
- 多言語展開の進行: `10-protocol/polyglot-client-roadmap_ja.md`（§25）
- 名前: `2026-08-29-03`
- bootstrapと実装の順番、namespace、target: `2026-10-22-07`
- 旧for Unityの扱い: `2026-10-22-08`。Unityのrepo: `2026-11-11-02`
- Phase E／Fの進め方、C#の実装の時期、Unityの準備: `2026-10-23-01`
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
