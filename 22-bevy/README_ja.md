# Minecraft Remote Bevy App

Bevy Webアプリの設計スポーク。.NET箱庭のserverへつなぐ2つ目の参加アプリとして、手元で実験する（`2026-11-27-01`。
呼び方は`2026-11-28-01`）。前の記録の「Bevy箱庭」と「Bevy Web」はBevy Webアプリを、「Unity箱庭のserver」は.NET箱庭のserverを指す。

## 現在地

- 2026-11-27：Bevy Webから始めると決めた（`2026-11-27-01`）。hub NOTESの「Bevy（＋Blender）の箱庭」（2026-11-24）を昇格した
- 2026-11-28：Bevy WebアプリとRust箱庭（検討中）と呼ぶことにし（`2026-11-28-01`）、repoを`mc-remote-bevy-app`へ改名した
  （`2026-11-28-03`①）。GitHubでの改名はhuman owner。coordinatorが`README.md`と`AGENTS.md`の名前を直し
  （`240c55664c19ad0c8bc776a70f16a4351b7f5f8e`）、手元のcloneのremoteを替え、`AGENTS.md`のbootstrap commandが通ることを確かめた
- repository: `Naohiro2g/mc-remote-bevy-app`（human ownerが2026-11-27に`mc-remote-bevy-sandbox`として作った。public、LICENSEはMIT、
  default branchは`main`。初期commit `4f08a2b077c3adb1cfc96356126eee3a973e1b3b`）
- 入口（2026-11-27、coordinator）: dev-repo protocolの雛形の`AGENTS.md`と、`.gitignore`へoperator-localのfile（`CLAUDE.md`、
  `NOTES_ja.md`、`handoff-materials/`、`.env`）を足した（`8bfc86003c13c2bb3a0e651af9e676c3ed1b95fe`）。手元のcloneに`CLAUDE.md`（`@AGENTS.md`の1行）を置き、
  `AGENTS.md`のbootstrap commandが通り、runtime blockのmarkerが1組だけあることを確かめた
- 相談の票（2026-11-27）: `00-hub/bevy-sandbox-consultation-instructions_ja.md`。codeは書かない
- 相談の返却（2026-11-28）: Bevyのrepoの`handoff-materials/2026-11-27-bevy-web-consultation/materials/consultation-response_ja.md`
  （37,842 bytes、`6441a65eb1621e3e813d05e34cc9ca9f8fdd9138b3ad7cf1af07ff679c1d6576`。knowledge `72f003c`を読んだ）。human ownerが、版、
  repoの形、`/ws/sync`を読むcommit、最初のsliceの着手を認めた（human owner 2026-11-28「６，７オッケー」）
- 最初のsliceの票（2026-11-28）: `00-hub/bevy-app-first-slice-instructions_ja.md`。Slice 0（骨格とCI）とSlice 1（`snapshot`と
  `blockDelta`を受けて描く）
- BevyとRustの版：Bevy `0.20.1`、Rust `1.100.0`。`rust-toolchain.toml`と、commitした`Cargo.lock`で固定する（相談の返却の1）
- repoの形：Cargo workspace。`crates/sync-core`（Bevyに依存しない。`/ws/sync`のmessage、座標の換算、地形と箱の差分）と
  `crates/bevy-app`（相談の返却の2）
- `/ws/sync`を読むcommit：`mc-remote-unity-sandbox`の`6ce475e`（`2400.0.0rc1`）。`2400.0.0`との差は版と画面の文字だけで、
  契約は同じ。12月から1月の版で契約が変わったら、読み直す
- 名前：ブラウザのviewerの保存のkeyは`mc_remote_bevy_viewer_id_v1`（参加アプリごとに分ける）、nativeの接続先の環境変数は
  `MC_REMOTE_APP_WS_URL`（hub NOTESの「参加アプリと箱庭の内部の名前」。最初のsliceの票で決めた）
- 12月：手元で最初のsliceを進め、12月末に何らかのトライアル公開をする（human owner 2026-11-27「平行して、Bevy箱庭の
  ファーストスライスを手元で進める。12末で何らかのトライアル公開。」）。12月末までの教材の整理の優先は変わらない
- 実験場: `Naohiro2g/bevy-sandbox`。human ownerが2026-11-26に作り、coordinatorがhello world（回る立方体、Bevy 0.20.1）を置いた
  （`a9a3c259eb12ace79f97853d11084d4b1ae512ea`）。マイクラリモコンの外の実験場として残す

## 形

- .NET箱庭のserverは1つのまま。Bevy Webアプリは`/ws/sync`で同じserverにつなぎ、同じ世界を表示する。Unity Webアプリと並ぶ
  2つ目の参加アプリになる
- `mc-remote-unity-sandbox`は、世界のモデル（UnityEngineに依存しないC#）、server（.NET）、Unity Webアプリの3つに分かれていて、
  Unityなのは表示だけ（`d3539c3`の`docs/unity-sandbox-display-sync_ja.md` §1）。server、世界のモデル、守りの部分（pairing、token、
  上限`2026-11-24-01`）、配る仕組みは、.NET箱庭のものを使う
- Bevy WebアプリはUnity Webアプリを追いかける。.NET箱庭とUnity Webアプリの作業と公開を止めず、新しい義務を足さない
- 最初は公開せず、手元で実験する。12月末のトライアル公開の形は、最初のsliceを見て決める
- .NET箱庭とUnity Webアプリは、12月から1月にかけて、blockの種類、太陽と月の運行、世界の拡張、世界の保存を順に出す（human owner
  2026-11-27、hub NOTESの「お楽しみ要素を計画して出す」）。Bevy Webアプリは、その間に変わる`/ws/sync`とUnity Webアプリを追う
- Unity Webアプリとの関係：外から見える体験は揃え、中の作りは、寄せるか分けるかを協議する（human owner 2026-11-28「これは
  私が言ったことだが、Unityとの関係性の一般論だね。ルールにしなくてオッケー。」）。分けたところは、理由を記録する
- Bevy Webアプリは、`/ws/sync`でserverにつなぎ、JSON-RPCのclientではない。Bevyで作ったゲームからblockを送る使い方
  （`21-rust-client/`の「位置づけ」）はクライアントの側で、Rustのclient libraryを使う

## `/ws/sync`の契約

- 正本は`mc-remote-unity-sandbox`の`docs/unity-sandbox-display-sync_ja.md`。knowledgeへ上げず、しばらくそのrepoで育てる
  （human owner 2026-11-27。今toolingをScratchが持っているのと同じ）
- Bevy Webアプリは、それを固定したcommitで読んで追う。読んだcommitを返却に書く

## repoの境目

- `mc-remote-bevy-app`（前の名前は`mc-remote-bevy-sandbox`）：マイクラリモコンに組み込むコード。最初からここで書き、
  `bevy-sandbox`から移さない
- `bevy-sandbox`：マイクラリモコンの外の実験場。改名しない
- 境目は、マイクラリモコンの言葉（wire、`/ws/sync`、blockのID、地形）を使うかどうか（言い方はclaude.aiの案）

## 決まっていないこと

- Rust箱庭（serverと世界のモデルもRustにするか。`2026-11-28-01`③）。Bevy Webアプリが成り立ってから決める。Bevy担当の案
  （相談の返却の2）は、作るなら別のrepoにし、`/ws/sync`でつなぐ。workspaceの形は、どちらに決まっても困らない
- 公開の名前、port、gate、Stack（12月末のトライアル公開で、どこまで要るか）
- Blenderの扱い（human owner 2026-11-24「Unity箱庭に続いてBevy（＋Blender)箱庭。」）
- 確かめていないこと（claude.aiの票、2026-11-27）：wasmの大きさ、性能、日本語の入力、CIでbuildできるか。Bevyの現状
  （0.20は2026-10-08、右手系Y-up、公式のeditorはまだ）はwebの記述。右手系Y-upなら、Minecraftの座標
  （`00-hub/world-coordinates-facts_ja.md` §2）を符号を変えずに写せる
- `/ws/sync`は、つなぐ側のOriginもHostも見ていない（Unity担当が、公開VPSで動いている`1594805`と`6ce475e`のsourceで確かめた。
  2026-11-28）。別のoriginから開いたBevy Webアプリが実際につながるかは、相談の票で確かめる
- 日本語のfont：Bevy担当の案は、Noto Sans CJK JPをJIS第1水準ほどに絞る。ほかの人のchatで、入っていない漢字が豆腐になる
  ことがある。Slice 3の前に確かめる

## 正本境界

- 始め方、境目: `2026-11-27-01`。呼び方: `2026-11-28-01`。repo名: `2026-11-28-03`①
- `/ws/sync`の契約、server、世界のモデル: `Naohiro2g/mc-remote-unity-sandbox`（`19-unity/`）
- wire、versioning、authentication等のProtocol contract: `10-protocol`
- Rust Client Library: `21-rust-client/`
- 実装、build、Bevyに閉じる判断: `Naohiro2g/mc-remote-bevy-app`

## bootstrapの手順

1. human ownerがGitHubでrepo `Naohiro2g/mc-remote-bevy-sandbox`を作る（LICENSE（MIT）、README、Rustの`.gitignore`の初期commit）。
   2026-11-27に済んだ
2. knowledgeが`AGENTS.md`と`.gitignore`の追記をcommitしてpushする（`00-hub/dev-repo-protocol_ja.md`の雛形。関連スポークは
   `22-bevy/`、`19-unity/`、`10-protocol/`）。2026-11-27に済んだ
3. knowledgeが手元のcloneに`CLAUDE.md`（`@AGENTS.md`の1行）を置き、`AGENTS.md`のbootstrap commandが通ることを確かめる。
   2026-11-27に済んだ
4. 担当sessionに相談の票を出す（codeは書かない）。2026-11-27に出した（`00-hub/bevy-sandbox-consultation-instructions_ja.md`）
5. human ownerがGitHubでrepoを`mc-remote-bevy-app`へ改名する。knowledgeが`README.md`と`AGENTS.md`の名前を直し、手元のcloneの
   remoteを替える（`2026-11-28-03`①）。2026-11-28に済んだ
6. 返ってきた案を見て、最初のsliceの票を出す。最初のsliceもUnity Webアプリを追うので、agentに多く任せる。2026-11-28に出した
   （`00-hub/bevy-app-first-slice-instructions_ja.md`）

## AGENTS.mdの「このrepository固有の指示」

案はclaude.ai（2026-11-27の確定搬送票の付録）。

- BevyとRustの版は、`22-bevy`の「現在地」に従う。使った版を記録する
- `/ws/sync`の正本は`Naohiro2g/mc-remote-unity-sandbox`の`docs/unity-sandbox-display-sync_ja.md`。読んだcommitを記録する。
  Bevyの側で契約を広げない。足りないものは、unity-sandboxへの提案としてknowledgeへ返す
- .NET箱庭のserverとUnity Webアプリのsourceを、このrepoへ複製しない。手元では、公開のimageか、unity-sandboxのserverを起動して使う
- Minecraft（Mojang）のtexture、model、音などの素材をcommitしない。自作か、licenseが明確で再配布できるものだけを使い、
  出どころを記録する
- `target/`、webのbuildの成果物など、生成されるものをcommitしない
- 公開の配信、release workflow、container imageは、knowledge SSOTで決まるまで足さない
- token、private endpoint、credential、operator-localの設定をcommitしない
- 横断する発見はlocalの`NOTES_ja.md`へ一時捕捉し、session／sliceの終わりにknowledge hubへ上げる
- 自分が編集したpathだけを明示stageする
