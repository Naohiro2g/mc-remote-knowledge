# `build_denied`を原因ごとに分け、世界の外の判定をほかのmethodへ広げる依頼（McRemote）

> 前の依頼（`00-hub/mcremote-out-of-bounds-instructions_ja.md`）の返却で、`build_denied`は14のmethodで返り、原因は
> 建築範囲（`buildRange`）の外と、playerごとの1回に置けるblock数の上限の2つだと分かった。human ownerの「なんでも
> build_deniedになって、よくわからない、になっている。」（2026-11-14）を受けて、原因ごとにreasonを分ける
> （`2026-11-14-05`）。また、`out_of_bounds`の`data`の形を決め、判定をblockを扱うほかのmethodへ広げる（`2026-11-14-04`）。
> 正本はwire「7.3 エラー設計」の表の下の箇条。参照するknowledge commitは、この依頼が入ったmainのcommitです。

## すること

1. **世界の外の判定を広げる**（`2026-11-14-04`④）：PR #19と同じ判定、同じ`data`、同じ順番（権限や建築範囲より先）にする
   - `world.getBlocks`、`world.setSign`、`world.updateSignLine`：置ける高さと、world border
   - `world.getHeight`：x、zのworld borderだけ
   - entity、粒子、音、落雷には当てない
2. **`build_range_exceeded`**：今`build_denied`を返す建築範囲の外を、すべてこのreasonにする（返却の4の表の14のmethod）
   - codeは`-32000`。判定する位置や量は、今のまま
   - `data.bounds`は`{ "center": { "x", "z" }, "build_range" }`。`center`は建築の原点の絶対座標、`build_range`は判定に
     使った値
   - `data.violating`は、外れた点の絶対座標（`out_of_bounds`と同じ形）
3. **`block_count_limit_exceeded`**：playerごとの1回に置けるblock数の上限（`mcr.build.blocks`）を越えたときを、このreasonにする
   （`world.setBlock`、`world.setBlocks`）
   - codeは`-32000`。`data.limit`に上限、`data.requested`に置こうとした数
4. `build_denied`を返すところが残らないようにする。判定の順番は変えない
5. unit testで、直す前に落ち、直した後に通ることを確かめる。id付きのrequestとnotificationの両方
6. PRにする。mergeはhuman ownerが判断する。PR #19と同じ、McRemoteの次のreleaseに入れる（hub NOTESの「McRemoteの次の
   release」の行）

## 返却

- 実際に読んだknowledge commit
- PRの番号、head、CIのrun
- methodごとに、`violating`に入れる点（座標が実数のmethod、箱や範囲で確かめるmethodでは、どの点か）と、3つのreasonの
  `data`の例
- testが直す前に落ちたことの確かめ方
- 確かめられなかったことと、その理由

## coordinatorがすること

- PRとCIを、GitHubのAPIで照合する
- releaseに入ったら、wire §7.3の表へ`out_of_bounds`、`build_range_exceeded`、`block_count_limit_exceeded`を移し、`build_denied`の
  行に返さなくなった版を書く。wireと`11-plugin/platform-design_ja.md`のほかの`build_denied`も直す。F1のcase（tooling）と
  各clientの表示を頼む
