# Bevy Webアプリの最初のsliceの依頼（mc-remote-bevy-app、Slice 0と1）

> 相談の返却（2026-11-28）を見て、human ownerが版、repoの形、`/ws/sync`を読むcommit、最初のsliceの着手を認めた
> （human owner 2026-11-28「６，７オッケー」）。この票は、相談の返却の「9. 最初のslice」のうち、Slice 0（骨格とCI）と
> Slice 1（`snapshot`と`blockDelta`を受けて描く）の依頼です。Slice 2からは、この返却を見て次の票で頼む。参照するknowledge
> commitは、この依頼が入ったmainのcommitです。

## 入力

- 相談の返却：このrepoの`handoff-materials/2026-11-27-bevy-web-consultation/materials/consultation-response_ja.md`（37,842 bytes、
  `6441a65eb1621e3e813d05e34cc9ca9f8fdd9138b3ad7cf1af07ff679c1d6576`）。下の「決まっていること」は、ここの案を採ったもの
- `/ws/sync`の契約：`Naohiro2g/mc-remote-unity-sandbox`の`6ce475ef64155268037c8e13f063b7151aac6134`（`2400.0.0rc1`）の
  `docs/unity-sandbox-display-sync_ja.md`
- knowledge：`22-bevy/README_ja.md`、`00-hub/sandbox-layers-guide_ja.md`、`00-hub/world-coordinates-facts_ja.md` §2

## 決まっていること（守るもの）

- 版：Bevy `0.20.1`、Rust `1.100.0`。`rust-toolchain.toml`（rustfmt、clippy、`wasm32-unknown-unknown`）と、commitした
  `Cargo.lock`で固定する
- repoの形：Cargo workspaceにし、`crates/sync-core`（Bevyに依存しない。`/ws/sync`のmessageの型、座標とyaw、pitchの換算、
  地形と箱の差分）と`crates/bevy-app`に分ける
- webのbuild：`cargo build --target wasm32-unknown-unknown`と`wasm-bindgen-cli`を、薄いscriptで呼ぶ。WebGL2を既定にする
- 開発中は、手元のnativeの窓からも`/ws/sync`へつなぐ。Bevyのデスクトップアプリは検討中のまま（`2026-11-28-01`①）で、
  このsliceの成果物にしない
- 座標：Minecraftの座標を、符号を変えずにそのまま写す。最初のcameraは北（`-Z`）へ向ける
- 接続先：URLに`?ws=`があればそれへ、無ければ開いたhostの`/ws/sync`へつなぐ（Unity Webアプリと同じ）。nativeは
  環境変数`MC_REMOTE_APP_WS_URL`か、起動の引数で渡す
- viewerの保存のkey：ブラウザは`mc_remote_bevy_viewer_id_v1`（参加アプリごとに分ける。Unity Webアプリの
  `mc_remote_unity_viewer_id_v1`は替えない）。nativeは、OSの設定のdirectoryに置き、repoの中に書かない
- 手元のserver：GHCRの公開image（`ghcr.io/naohiro2g/mc-remote-unity-sandbox:candidate-6ce475e`、
  `sha256:e39109f0e3ff6bbc9ef2a0f4fb6048735817fa250a5226b404430ace52101097`）を主に使う。12月1日の後は`v2400.0.0`でもよい。
  .NET箱庭のserverとUnity Webアプリのsourceは、このrepoへ複製しない
- Unity Webアプリとの関係：外から見える体験は揃え、中の作りは、寄せるか分けるかを協議する（human ownerの一般論。規則にはしない）。
  分けたところは、理由を記録する
- 公開の配信、release workflow、container imageは足さない（このrepoの`AGENTS.md`）

## 作るもの

### Slice 0：骨格とCI

- workspace、`rust-toolchain.toml`、Bevy `0.20.1`、WebGL2のbuildの手順
- CI（`ubuntu-24.04`）：fmt、clippy、`sync-core`のtest、nativeのcheck、wasmのbuild
- 終わりの基準：nativeの窓とブラウザの両方で、最初の画面が開く。CIが通る

### Slice 1：`snapshot`と`blockDelta`を受けて描く

- `/ws/sync`の接続と再接続、viewerのIDの保存
- 地形と9区画の目印、箱の描き方（Unity Webアプリと同じく、箱のまま描き、重なりは最大6つに分ける）、基本の10種類と、
  知らないblockの代わりの見た目、面ごとに繰り返すUV（1ブロックずつ数えられる）、北を向いた最初のcamera
- 終わりの基準：
  1. `sync-core`のtestが通る。yawとpitchの換算は全方位を確かめ、符号を1つ変えるとtestが落ちることを見る
  2. 手元の.NET箱庭のserverに、Unity WebアプリとBevy Webアプリ（とnative）を並べてつなぐ。PythonかScratchから送った
     `setBlock`と`setBlocks`（空気でくり抜くものも）が、同じ座標、同じ向き、1つずつ数えられる見た目で出る。読み直しても
     `snapshot`で戻る

## 先に試してよいこと

相談の返却の「わからないこと」の1（wasmの大きさと描画の性能）は、このsliceの前か途中で`bevy-sandbox`で測ってよい。
2（`getrandom`と日本語のfont）と3（winitとDOMの入力）は、Slice 3の前に`bevy-sandbox`で試す。4〜6は、このsliceの中で決める。

## 返却

- 実際に読んだknowledgeのcommitと、`/ws/sync`の契約を読んだcommit
- commit、branch、CIのrun、かかった時間
- 使った版（Bevy、Rust、`wasm-bindgen`）
- wasmの大きさ（`wasm-opt`の前と後、圧縮した後）
- Slice 1の終わりの基準の結果。担当が自分で確かめたことと、human ownerが手元で見るときの手順（coordinatorがその場で案内する）
- Unity Webアプリと分けたところと、その理由
- `/ws/sync`の契約で足りなかったこと（unity-sandboxへの提案として）
- 横断する発見（hub NOTESへ上げる候補）

## coordinatorがすること

- 返却を照合し、human ownerと一緒に見て、Slice 2からの票を出す。12月1日の公開の前後（11/29〜12/1）は、照合が遅れることがある
- 決まったことを`22-bevy/README_ja.md`へ書く
