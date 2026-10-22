# Minecraft Remote for TypeScript

現行Minecraft Remote ProtocolをTypeScriptへ投影する、一般用途Client Libraryの設計スポーク。Scratch Clientとは
別の成果物である（`00-hub/terms-glossary_ja.md`）。

## 現在地

`2026-10-22-07`で、担当sessionを呼べるbootstrapまでrepoを先に作ると決めた。実装は、多言語の比較とconformanceの
一般化（`10-protocol/polyglot-client-roadmap_ja.md`のPhase E／F）をknowledgeで具体化してから始める。

- repository: `Naohiro2g/minecraft-remote-typescript`（まだ作っていない）
- package名: `@mc-remote/client`は第一候補で、npmへ出す準備のときに決める（NOTES 2026-08-29）
- 比べる基準: 初回stable `2321.0.0`（protocol `23.2.1`）
- `@mc-remote/protocol`（minecraft-remote-tooling）のコードには依存しない。protocolの型と定数はこのrepoで持ち、共有
  fixtureはデータとして、固定したcommitで読む（`2026-10-22-07`）

## 正本境界

- wire、versioning、authentication等のProtocol contract: `10-protocol`
- 多言語展開の進行: `10-protocol/polyglot-client-roadmap_ja.md`（§21、§22、§23）
- 名前: `2026-08-29-03`
- bootstrapと実装の順番、`@mc-remote/protocol`との関係: `2026-10-22-07`
- 実装、build、TypeScriptに閉じるClient APIの判断: `Naohiro2g/minecraft-remote-typescript`

TypeScriptは、JavaやPythonのコードを翻訳して作らない。Protocol contractと共有fixtureを主な入力にし、Pythonと
Javaは調べる材料として使う（ロードマップ§21）。最初はNode.jsのTCPで作り、browserとBridgeの経路は後にする（§23）。

## bootstrapの手順

1. human ownerがGitHubでrepoを作る。Javaと同じく、LICENSE（MIT）とREADMEの初期commit
2. knowledgeが`AGENTS.md`と`.gitignore`（operator-localの`CLAUDE.md`、`NOTES_ja.md`、`handoff-materials/`と、`.env`を外す。Javaと同じ）をcommitしてpushする
   （`00-hub/dev-repo-protocol_ja.md`の雛形。関連スポークは`17-typescript-client/`と`10-protocol/`）
3. knowledgeが手元のcloneを作り、`CLAUDE.md`（`@AGENTS.md`の1行）を置いて、`AGENTS.md`のbootstrap commandが
   通ることを確かめる（human owner 2026-10-22の依頼。dev-repo protocolでは運用者の作業）
4. 担当sessionが、下の「bootstrapで作るもの」を作って返す

## bootstrapで作るもの

- Node.js（miseで選ぶ）、TypeScript、ESM。package managerとtest runnerは担当の案で、理由と合わせて返す
- `package.json`は`private: true`で、npmへ出さない。`name`は第一候補の`@mc-remote/client`を仮に置く
- build、lint、root moduleのunit test 1件、GitHub ActionsのCI
- README（何のrepoか、まだ実装の前であること、knowledgeへの入口）

入れないもの:

- transport、`hello`、authentication等のprotocolの実装（Phase E／Fの具体化の後）
- `@mc-remote/protocol`への依存
- publishの設定、release workflow

返却: 実際に読んだknowledge commit、bootstrapのcommit、CIのrun、toolchainの版、選んだpackage managerとtest runner

## AGENTS.mdの「このrepository固有の指示」（案）

- Node.jsの選択と切り替えはmiseを正準とする
- `@mc-remote/protocol`に依存しない。共有fixtureは固定したcommitで読む
- publish、registryの名前、release workflowは、knowledge SSOTで決まるまで足さない
- wire formatに触れる前に`10-protocol`、このrepoの作業では`17-typescript-client`を読む
- token、private endpoint、credential、operator-localの設定をcommitしない
- 横断する発見はlocalの`NOTES_ja.md`へ一時捕捉し、session／sliceの終わりにknowledge hubへ上げる
- 自分が編集したpathだけを明示stageする
