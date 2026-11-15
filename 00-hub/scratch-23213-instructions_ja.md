# `2321.3`に向けて、Scratchでhuman ownerと相談して進めること（scratch-editor）

> `2321.3`（公開Unity箱庭の最初の公開）に入れるScratchの変更。「決まったこと」のほかは、human ownerと相談し、仮実装しながら
> 形を決める。`2321.2`の作り直し（`00-hub/23212-gate-candidate-instructions_ja.md`の「Scratchの作り直し（2026-11-16）」）を先に
> する。参照するknowledge commitは、この票が入ったmainのcommitです。

## 決まったこと（2026-11-16）

- ペアリングの状態をScratchのコードで扱う3つのブロック（(ペアコード)、(ペアリングコマンド)、{ペアリングできたとき}）は、
  パレットから外す。前の作品が読み込めて動くことは残す（human owner 2026-11-16「ペアリング状態自体をScratchコードで扱う
  ことに関しては、今の所使いどころが見えないので、蓋をする。読み込み、実行可能性は残しておこう。」）。ペアコードとコマンドは
  WireScope miniが出す（`2026-08-02-09`①）
- [接続する]は残す。外すのは、WireScope miniとの統合と接続状態の表示を足した後（human owner 2026-11-16。hub NOTESの
  「WireScopeの観測の開始と終了、接続の状態の詳細」の行）
- ブロック一覧（ホームページの`/api/scratch/`）に、Unity箱庭のserverで使えるブロックが分かるカテゴリーとキーワードを足す
  （human owner 2026-11-16「Scratchのブロック一覧にUnity箱庭サーバーで使えるもの、というカテゴリー、キーワードを追加しよう。」）。
  どのブロックが使えるかは、`2321.3`でUnity箱庭が答えるmethodで決まる（下の2と同じ相談）。coordinatorは`2321.1.0`の一覧の
  `methods`から、今のUnity箱庭で動くのは56のうち18と数えた（値を読むだけのブロックは、その値を作るブロックが動くかで数え、
  イベントのブロックは`events.poll`が空なので動かないとした）
- 接続先の一覧の形は`2026-11-16-01`（PR #35）

## human ownerと相談して進めること

1. パレットの中の並びを見直して直す（human owner 2026-11-16「Scratchのパレット内での並びも改善できることがあった気がして
   いるので、再度チェックしてこの機会に修正。」）
2. 接続先が答えないmethodのブロックを使ったとき（`method_not_found`）に、今の接続先では使えないことが学習者に分かる表示。
   接続先はhelloの`server`で分かる（Unity箱庭は`mc-remote-unity-sandbox`。McRemoteは`2400`まで`server`を返さない）。Unity箱庭が
   答えるmethodは`19-unity/README_ja.md`の「Unity箱庭のserverが応えるもの」で、`2321.3`で足すものはUnity担当とhuman ownerが
   相談している（`00-hub/unity-sandbox-release-instructions_ja.md`の「human ownerと相談して進めること（2026-11-16）」）
3. 新しいreasonの表示：`out_of_bounds`、`build_range_exceeded`、`block_count_limit_exceeded`と、その`data`（範囲、外れた点、上限、
   置こうとした数）。wire §7.3、`2026-11-14-02`、`2026-11-14-04`、`2026-11-14-05`、`2026-11-15-02`。McRemote `2321.2.0`（PR #21）と
   Unity箱庭のserverが返す。検討メモは`10-protocol/learner-error-diagnostics-notes_ja.md`の「1. エラーの原因を学習者が特定
   できるようにする」
4. Minecraftという語を含む案内（blockのmenu、LANの設定画面など）を、接続先に合わせる（`00-hub/unity-sandbox-scratch-instructions_ja.md`
   の「返却と照合（2026-11-14）」の4と6）
5. WireScopeで、helloの`server`（`2026-11-14-03`）を見せる

## 返却

- 実際に読んだknowledge commit
- branch、head、PR、CIのrun
- 外した3つのブロックを使った前の作品が、読み込めて動くことを、どう確かめたか
- 1〜5で、相談して決めた形と、採らなかった案（相談した日とhuman ownerの言葉）
- 見本の作品、test、文書、ブロック一覧、ホームページの案内のうち、変更が及ぶもの
- 確かめられなかったことと、その理由

## coordinatorがすること

- PRとCIを、GitHubのAPIで照合する。決めた形を、返却を見てDECISIONSに書く
