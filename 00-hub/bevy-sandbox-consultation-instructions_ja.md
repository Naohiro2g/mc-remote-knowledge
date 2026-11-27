# Bevy Webの最初の相談（mc-remote-bevy-sandbox）

> Bevy箱庭を、Unity箱庭のserverへつなぐ2つ目の表示「Bevy Web」から始める（`2026-11-27-01`、`22-bevy/README_ja.md`）。
> Bevy WebはUnity Webを追い、最初は公開せず手元で動かす。この票は相談だけで、codeは書かない。
> 返ってきた案を見て、最初のsliceの票を出す。参照するknowledge commitは、この票が入ったmainのcommitです。
>
> 12月の見通し（human owner 2026-11-27）：手元で最初のsliceを進め、12月末に何らかのトライアル公開をする。Unity箱庭は、
> 12月から1月にかけて、blockの種類、太陽と月の運行、世界の拡張、世界の保存を順に出す。Bevy Webは、その間に変わる
> `/ws/sync`とUnity Webを追う。
>
> 2026-11-28の注記：repoを`mc-remote-bevy-app`へ改名すると決めた（`2026-11-28-03`①）。この票の「Bevy箱庭」と「Bevy Web」は
> Bevy Webアプリ、「Unity箱庭のserver」は.NET箱庭のserver、「Unity Web」はUnity Webアプリと読む（`2026-11-28-01`）。本文は
> 出したときのまま変えない。

## 読むもの

- knowledge：`22-bevy/README_ja.md`、`19-unity/README_ja.md`、`10-protocol/`のwire（helloとpairingの範囲）
- `Naohiro2g/mc-remote-unity-sandbox`の`main`：
  - `docs/unity-sandbox-display-sync_ja.md`（`/ws/sync`の正本）、`README.md`、`docs/local-demo_ja.md`
  - Unity Webが何をしているか：`unity/Assets/LocalSandboxDemo/Runtime/`の`SandboxSyncClient`、`DemoBlocks`、`LocalSandboxWalker`
  - `server/`の`/ws/sync`の実装
- 参考：`Naohiro2g/bevy-sandbox`（マイクラリモコンの外の実験場。Bevy 0.20.1のhello worldと、環境構築のrunbook）。codeは持ち込まない

## 相談したいこと（それぞれ、案と理由、却下した案）

1. 版：BevyとRustの版と、その固定のしかた
2. repoの形：Cargo workspaceにするか。後でRustのserverと世界のモデルを足す余地をどう残すか
3. webのbuild：bevy CLIを使うか、wasm-bindgenを直接使うか。WebGL2とWebGPUのどちらを既定にするか。開発中、手元のnativeの窓からも
   `/ws/sync`へつなぐか
4. `/ws/sync`のclient：wasmとnativeで使うWebSocketの部品。`viewerId`をどこに持つか（Unity Webは`localStorage`）
5. 手元のserver：GHCRの公開imageを使うか、unity-sandboxのserverをdotnetで起動するか。Bevy Webを別のportから開いたときに
   `/ws/sync`へつながるか（Origin、上限を入れた版）
6. blockの描き方：
   - `snapshot`の`regions`と`blockDelta`の箱をどう描くか。Unity Webは箱のまま描き、面ごとにUVを繰り返して、1ブロックずつ
     数えられるようにしている
   - 座標をMinecraftのまま写せるか。最初のcameraを北に向けられるか
7. 日本語：fontの出どころ（Unity WebはNoto Sans CJKのsubset、OFL）。chatの入力（IME）とpointer lockの見込み
8. CI：GitHub Actionsで、nativeとwasmのbuildを回せるか。かかる時間とcache
9. 最初のsliceの案：Unity Webのどこまでを、どの順に追うか。たとえば次の順で、それぞれの終わりの基準と確かめ方をつける。
   12月末のトライアル公開に、どこまでが間に合うかの見込みもつける
   - `snapshot`と`blockDelta`を受けて描く
   - 歩く、見回す
   - chatと`/mcremote pair`
   - `playerPose`
   - HUD

## 返却

- 実際に読んだknowledgeのcommitと、unity-sandboxのcommit
- 1〜9の案と理由、却下した案
- わからないことと、試さないと決められないこと。試す場所の案もつける：
  - マイクラリモコンの言葉を使わないなら`bevy-sandbox`
  - 使うなら、このrepoの最初のslice
- 横断する発見（あれば、hub NOTESへ上げる候補として）

## coordinatorがすること

- 返却を、human ownerと一緒に見る。決めたこと（版、repoの形など）を`22-bevy/README_ja.md`へ書き、最初のsliceの票を出す
