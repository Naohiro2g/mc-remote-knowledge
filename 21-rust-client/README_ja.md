# Minecraft Remote for Rust

現行Minecraft Remote ProtocolをRustへ投影する、一般用途Client Libraryの設計スポーク。

## 現在地

`2026-11-26-01`で、repoを作り、担当sessionを呼べるところまで入口を置いた。buildの骨組み、CI、toolchainの固定はまだ無い。

- repository: `Naohiro2g/minecraft-remote-rust`（human ownerが2026-11-26に作った。public、LICENSEはMIT、default branchは`main`）
- 入口（2026-11-26、coordinator）: dev-repo protocolの雛形の`AGENTS.md`と、`.gitignore`へoperator-localのfile（`CLAUDE.md`、
  `NOTES_ja.md`、`handoff-materials/`、`.env`）を足した（`7e88f15854814d2613a1eab9ec9f1b8caf01895c`）。手元のcloneに`CLAUDE.md`（`@AGENTS.md`の1行）を置き、`AGENTS.md`の
  bootstrap commandが通り、runtime blockのmarkerが1組だけあることを確かめた（knowledge `454449e`）

## 位置づけ

hub NOTESの「Scratch、Python、Rustの線」（2026-11-25）から。

- human owner 2026-11-25：Java、TypeScript、C#よりも優先度は高い。Scratch、Python、Rustの線を強める
- 2つの使い方を並べる：Pythonから速くしたい部分をRustで書く使い方（pyxelの中のRustと同じ）と、ピュアRust
- Rustに慣れたらBevyへ進み、Bevyのアプリから箱庭へつなぐ。そのためにRustのclient libraryが要る

## 決まっていないこと

- crate名と、crates.ioへ出すか
- Rustのeditionと、toolchainの固定のしかた
- Pythonから使う形（拡張moduleにするか、何で作るか）
- 最初の縦slice（TypeScriptとC#では、helloからsetBlock／getBlockまでを直接のTCPで）と、比べる基準のprotocol
- polyglotロードマップの中の順番（hub NOTESの行は、これを書き直したときに閉じる）

## 正本境界

- wire、versioning、authentication等のProtocol contract: `10-protocol`
- 多言語展開の進行: `10-protocol/polyglot-client-roadmap_ja.md`
- repoと入口: `2026-11-26-01`
- 実装、build、Rustに閉じるClient APIの判断: `Naohiro2g/minecraft-remote-rust`

Rustも、ほかの言語のコードを翻訳して作らない。Protocol contractと共有fixtureを主な入力にする。

## bootstrapの手順

1. human ownerがGitHubでrepoを作る（LICENSE（MIT）、README、Rustの`.gitignore`の初期commit）。2026-11-26に済んだ
2. knowledgeが`AGENTS.md`と`.gitignore`の追記をcommitしてpushする（`00-hub/dev-repo-protocol_ja.md`の雛形。関連スポークは
   `21-rust-client/`と`10-protocol/`）
3. knowledgeが手元のcloneに`CLAUDE.md`（`@AGENTS.md`の1行）を置き、`AGENTS.md`のbootstrap commandが通ることを確かめる
   （human owner 2026-11-26の依頼「ローカルのbootstrapをお願い」）
4. 担当sessionが、下の「bootstrapで作るもの」を作って返す（票はまだ出していない）

## bootstrapで作るもの（案）

- toolchainの固定（`rust-toolchain.toml`かmiseか、editionは担当の案）、library crate、unit test 1件、GitHub ActionsのCI
  （runnerは`ubuntu-24.04`）
- README（何のrepoか、まだ実装の前であること、knowledgeへの入口）

入れないもの:

- transport、`hello`、authentication等のprotocolの実装
- crates.ioへのpublishの設定、release workflow
- Pythonの拡張module、Bevy

返却: 実際に読んだknowledge commit、bootstrapのcommit、CIのrun、Rustの版とedition、crateの名前の案
