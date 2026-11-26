# Minecraft Remote Bevy Sandbox

Bevyの世界と箱庭の設計スポーク。最初は、Unity箱庭のserverへつなぐ2つ目の表示「Bevy Web」として、手元で実験する
（`2026-11-27-01`）。

## 現在地

- 2026-11-27：Bevy Webから始めると決めた（`2026-11-27-01`）。hub NOTESの「Bevy（＋Blender）の箱庭」（2026-11-24）を昇格した
- repository: `Naohiro2g/mc-remote-bevy-sandbox`（human ownerが2026-11-27に作った。public、LICENSEはMIT、default branchは`main`。
  初期commit `4f08a2b077c3adb1cfc96356126eee3a973e1b3b`）
- 入口（2026-11-27、coordinator）: dev-repo protocolの雛形の`AGENTS.md`と、`.gitignore`へoperator-localのfile（`CLAUDE.md`、
  `NOTES_ja.md`、`handoff-materials/`、`.env`）を足した（`8bfc86003c13c2bb3a0e651af9e676c3ed1b95fe`）。手元のcloneに`CLAUDE.md`（`@AGENTS.md`の1行）を置き、
  `AGENTS.md`のbootstrap commandが通り、runtime blockのmarkerが1組だけあることを確かめた
- 相談の票（2026-11-27）: `00-hub/bevy-sandbox-consultation-instructions_ja.md`。codeは書かない
- BevyとRustの版：まだ決めていない（相談の票の1）。`bevy-sandbox`のhello worldはBevy 0.20.1
- 12月：手元で最初のsliceを進め、12月末に何らかのトライアル公開をする（human owner 2026-11-27「平行して、Bevy箱庭の
  ファーストスライスを手元で進める。12末で何らかのトライアル公開。」）。12月末までの教材の整理の優先は変わらない
- 実験場: `Naohiro2g/bevy-sandbox`。human ownerが2026-11-26に作り、coordinatorがhello world（回る立方体、Bevy 0.20.1）を置いた
  （`a9a3c259eb12ace79f97853d11084d4b1ae512ea`）。マイクラリモコンの外の実験場として残す

## 形

- Unity箱庭のserver（.NET）は1つのまま。Bevy Webは`/ws/sync`で同じserverにつなぎ、同じ世界を表示する。Unity Webと並ぶ
  2つ目の表示になる
- Unity箱庭は、世界のモデル（UnityEngineに依存しないC#）、server（.NET）、Unity Webの3つに分かれていて、Unityなのは表示だけ
  （Unity箱庭の`d3539c3`の`docs/unity-sandbox-display-sync_ja.md` §1）。server、世界のモデル、守りの部分（pairing、token、
  上限`2026-11-24-01`）、配る仕組みは、Unity箱庭のものを使う
- Bevy WebはUnity Webを追いかける。Unity箱庭の作業と公開を止めず、新しい義務を足さない
- 最初は公開せず、手元で実験する。12月末のトライアル公開の形は、最初のsliceを見て決める
- Unity箱庭は、12月から1月にかけて、blockの種類、太陽と月の運行、世界の拡張、世界の保存を順に出す（human owner 2026-11-27、
  hub NOTESの「お楽しみ要素を計画して出す」）。Bevy Webは、その間に変わる`/ws/sync`とUnity Webを追う
- 表示のBevy Webは、`/ws/sync`でserverにつなぎ、JSON-RPCのclientではない。Bevyのアプリからblockを送る使い方
  （`21-rust-client/`の「位置づけ」）は別で、そちらはRustのclient libraryを使う

## `/ws/sync`の契約

- 正本はUnity箱庭のrepoの`docs/unity-sandbox-display-sync_ja.md`。knowledgeへ上げず、しばらくUnity箱庭で育てる
  （human owner 2026-11-27。今toolingをScratchが持っているのと同じ）
- Bevy Webは、それを固定したcommitで読んで追う。読んだcommitを返却に書く

## repoの境目

- `mc-remote-bevy-sandbox`：マイクラリモコンに組み込むコード。最初からここで書き、`bevy-sandbox`から移さない
- `bevy-sandbox`：マイクラリモコンの外の実験場。改名しない
- 境目は、マイクラリモコンの言葉（wire、`/ws/sync`、blockのID、地形）を使うかどうか（言い方はclaude.aiの案）

## 決まっていないこと

- serverと世界のモデルもRustにするか。Bevy Webが成り立ってから決める
- 公開の箱庭の名前、port、gate、Stack（12月末のトライアル公開で、どこまで要るか）
- Blenderの扱い（human owner 2026-11-24「Unity箱庭に続いてBevy（＋Blender)箱庭。」）
- 確かめていないこと（claude.aiの票、2026-11-27）：wasmの大きさ、性能、日本語の入力、CIでbuildできるか。Bevyの現状
  （0.20は2026-10-08、右手系Y-up、公式のeditorはまだ）はwebの記述。右手系Y-upなら、Minecraftの座標
  （`00-hub/world-coordinates-facts_ja.md` §2）を符号を変えずに写せる
- `/ws/sync`は、つなぐ側のOriginを見ていない（claude.aiが`d3539c3`のserverのsourceを読んだ範囲。動かしてはいない）。
  別のoriginから開いたBevy Webがつながるかは、相談の票で確かめる

## 正本境界

- 始め方、repo、境目: `2026-11-27-01`
- `/ws/sync`の契約、server、世界のモデル: `Naohiro2g/mc-remote-unity-sandbox`（`19-unity/`）
- wire、versioning、authentication等のProtocol contract: `10-protocol`
- Rust Client Library: `21-rust-client/`
- 実装、build、Bevyに閉じる判断: `Naohiro2g/mc-remote-bevy-sandbox`

## bootstrapの手順

1. human ownerがGitHubでrepo `Naohiro2g/mc-remote-bevy-sandbox`を作る（LICENSE（MIT）、README、Rustの`.gitignore`の初期commit）。
   2026-11-27に済んだ
2. knowledgeが`AGENTS.md`と`.gitignore`の追記をcommitしてpushする（`00-hub/dev-repo-protocol_ja.md`の雛形。関連スポークは
   `22-bevy/`、`19-unity/`、`10-protocol/`）。2026-11-27に済んだ
3. knowledgeが手元のcloneに`CLAUDE.md`（`@AGENTS.md`の1行）を置き、`AGENTS.md`のbootstrap commandが通ることを確かめる。
   2026-11-27に済んだ
4. 担当sessionに相談の票を出す（codeは書かない）。2026-11-27に出した（`00-hub/bevy-sandbox-consultation-instructions_ja.md`）
5. 返ってきた案を見て、最初のsliceの票を出す。最初のsliceもUnity Webを追うので、agentに多く任せる

## AGENTS.mdの「このrepository固有の指示」

案はclaude.ai（2026-11-27の確定搬送票の付録）。

- BevyとRustの版は、`22-bevy`の「現在地」に従う。使った版を記録する
- `/ws/sync`の正本は`Naohiro2g/mc-remote-unity-sandbox`の`docs/unity-sandbox-display-sync_ja.md`。読んだcommitを記録する。
  Bevyの側で契約を広げない。足りないものは、unity-sandboxへの提案としてknowledgeへ返す
- Unity箱庭のserverとUnity Webのsourceを、このrepoへ複製しない。手元では、公開のimageか、unity-sandboxのserverを起動して使う
- Minecraft（Mojang）のtexture、model、音などの素材をcommitしない。自作か、licenseが明確で再配布できるものだけを使い、
  出どころを記録する
- `target/`、webのbuildの成果物など、生成されるものをcommitしない
- 公開の配信、release workflow、container imageは、knowledge SSOTで決まるまで足さない
- token、private endpoint、credential、operator-localの設定をcommitしない
- 横断する発見はlocalの`NOTES_ja.md`へ一時捕捉し、session／sliceの終わりにknowledge hubへ上げる
- 自分が編集したpathだけを明示stageする
