# Minecraft Remote for Rust

現行Minecraft Remote ProtocolをRustへ投影する、一般用途Client Libraryの設計スポーク。

## 現在地

`2026-11-26-01`で、repoを作り、担当sessionを呼べるところまで入口を置いた。`2026-11-26-02`で、crate名、edition、toolchainの
固定のしかた、最初の縦sliceを決めた。buildの骨組みとCIはまだ無い（票はまだ出していない）。

- repository: `Naohiro2g/minecraft-remote-rust`（human ownerが2026-11-26に作った。public、LICENSEはMIT、default branchは`main`）
- 入口（2026-11-26、coordinator）: dev-repo protocolの雛形の`AGENTS.md`と、`.gitignore`へoperator-localのfile（`CLAUDE.md`、
  `NOTES_ja.md`、`handoff-materials/`、`.env`）を足した（`7e88f15854814d2613a1eab9ec9f1b8caf01895c`）。手元のcloneに`CLAUDE.md`（`@AGENTS.md`の1行）を置き、`AGENTS.md`の
  bootstrap commandが通り、runtime blockのmarkerが1組だけあることを確かめた（knowledge `454449e`）

## 位置づけ

hub NOTESの「Scratch、Python、Rustの線」（2026-11-25）から。

- human owner 2026-11-25：Java、TypeScript、C#よりも優先度は高い。Scratch、Python、Rustの線を強める
- 2つの使い方を並べる：Pythonから速くしたい部分をRustで書く使い方（pyxelの中のRustと同じ）と、ピュアRust
- Rustに慣れたらBevyへ進み、Bevyのアプリから箱庭へつなぐ。そのためにRustのclient libraryが要る
- `2026-11-26-03`：新しい言語の作業は、Scratch、Python、Rustの線を先にする。RustはJava、TypeScript、C#より先に進める
- Bevyとpyxelは、まずマイクラリモコンの外で試す（human owner 2026-11-26）。repoは`Naohiro2g/bevy-sandbox`と
  `Naohiro2g/pyxel-samples`

## 決めたこと（`2026-11-26-02`）

- crate名: `minecraft-remote-client`（コードでは`minecraft_remote_client`）。Javaのartifact IDと同じ。repo名は
  `minecraft-remote-rust`のまま
- crates.io: 最初の縦sliceが通ってから、出すかを決める。それまで`Cargo.toml`は`publish = false`
- edition: 2024
- toolchain: `rust-toolchain.toml`に版の番号で固定し、rustfmtとclippyを入れる。rustupがこのfileを読むので、Windows、
  VS Code、CIが同じ版になる
- Pythonから使うRust: client libraryとは別に、PyO3とmaturinで作る。最初の題材は、モンテカルロ法で円周率を求める
  学習ネタ（hub NOTESの行）。Pythonのclient（`minecraft-remote-api`）は純Pythonのまま
- 最初の縦slice: TypeScriptとC#と同じく、直接のTCPでhelloからsetBlock／getBlockとcloseまで。F1をCIで通し、
  実McRemoteとのpulseを1本通す。比べる基準はprotocol `24.0.0`（`2400.0.0`）

まだ決めないこと:

- 同期にするかasyncにするか（担当sessionが、Bevyから使うことも考えて、理由と合わせて案を返す）
- crates.ioへ出す時期

## 開発環境

- Windows: rustupが標準で入れるMSVC版（`x86_64-pc-windows-msvc`）を使う。Visual Studio Build Toolsの「C++による
  デスクトップ開発」（MSVCとWindows SDK）が要る。入っていないと、rustup-initが入れ方を案内する。ライセンスは
  「個人、学術、オープンソースは無料」と案内されるので、会社の端末では条件を確かめる。MinGWのGNU版でもbuildできるが、
  WindowsのPythonとBevyに合わせて、MSVC版にそろえる
- Linux: Cのcompiler（Ubuntuなら`build-essential`）
- macOS: Xcode Command Line Tools
- IDE: VS Codeとrust-analyzer。デバッガーは、Windowsでは「C/C++」拡張かCodeLLDB

## 正本境界

- wire、versioning、authentication等のProtocol contract: `10-protocol`
- 多言語展開の進行: `10-protocol/polyglot-client-roadmap_ja.md`（順番は`2026-11-26-03`）
- repoと入口: `2026-11-26-01`
- crate名、edition、toolchain、最初の縦slice: `2026-11-26-02`
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

- `rust-toolchain.toml`（その時の最新stableの版の番号と、rustfmt、clippy）、edition 2024のlibrary crate
  `minecraft-remote-client`（`publish = false`）、unit test 1件、GitHub ActionsのCI（runnerは`ubuntu-24.04`）
- README（何のrepoか、まだ実装の前であること、knowledgeへの入口）

入れないもの:

- transport、`hello`、authentication等のprotocolの実装
- crates.ioへのpublishの設定、release workflow
- Pythonの拡張module、Bevy

返却: 実際に読んだknowledge commit、bootstrapのcommit、CIのrun、Rustの版
