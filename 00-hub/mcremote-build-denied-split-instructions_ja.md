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

## 返却と照合（2026-11-15）

McRemoteは、knowledge `b4b23631fc6f053fe4e228bb0447c9b4b9502901`（この依頼が入ったcommit）を読み、McRemoteのmain
`3ccb3fd345faa228b195a15c3c45152f5dff7d04`（PR #19のmerge commit）から分けた。返却票はMcRemoteの搬送素材
`handoff-materials/2026-11-15-build-denied-split/materials/RETURN_ja.md`（12,518 bytes、SHA-256
`1f266ab8bf841e0c9b218d86cf965bbce1df27ded5a902c95fdeb6e65cbb9b36`）。coordinatorはGitHubのAPIで、PR #20のheadが
`84e2cc1ba1e113a92cebda34c9c7102dd82f4e23`（親は`3ccb3fd`、1 commit、22 file）であること、CI run `43650919348`がこのheadで
7 jobとも成功したことを確かめた。human ownerが2026-11-15にmergeした（merge commit
`082df43145b4a5bfe5854a3985a82c936ed0ce76`）。

1. **3つのreason**：建築範囲の外はすべて`build_range_exceeded`、1回に置けるblock数の上限は`block_count_limit_exceeded`。
   判定そのもの（`isWithinBuildRange`、`isWithinBuildBlocks`）は変えず、`build_denied`を返すところは残っていない。順番は、
   世界の外、建てる権限、建築範囲、個数の上限、workの順。notificationは同じ検査で、操作をせず、応答も送らない
2. **世界の外を広げた**：`world.getBlocks`、`world.setSign`、`world.updateSignLine`は高さとworld border、`world.getHeight`は
   world borderだけ。entity、粒子、音、落雷には足していない
3. **`violating`に入れる点**：blockを1つ扱うmethodはそのblock。`world.setBlocks`は第1、第2の端点の順に確かめ、最初に外れた点。
   `world.getBlocks`は、建築範囲ではx、zの最小と最大の点（yは原点のy）、世界の外では箱の最小と最大の点。`world.getHeight`は
   列のx、zと原点のy。entity、粒子、音、落雷は指定した点（実数）。`world.getNearbyEntities`は、中心から半径を引いた点と足した
   点（yは中心のy）。`entity.setPose`は移動先。`block_count_limit_exceeded`には`violating`が無い。`2026-11-14-05`の「`out_of_bounds`と
   同じ形」との違いは、`2026-11-15-02`で決めた（human owner「３点はオッケー。」）
4. **testは直す前に落ちた**：BuildDeniedSplitTestの32 caseのうち26が、新しいreasonを期待して`build_denied`が返り、失敗した
   （`build_range_exceeded`が14、`out_of_bounds`が8、`block_count_limit_exceeded`が4）。残りの6は、PR #19ですでに世界の外を
   拒んでいたcase。直した後は48 caseが通り、全534 testが通る。共有fixtureは変えていない。旧版のcaseの2つ（B7-L18、
   B8-N13）は、McRemoteのtestの側で新しいreasonに読みかえた
5. **確かめられなかったこと**：実際のPaperでの試験と、clientの表示
