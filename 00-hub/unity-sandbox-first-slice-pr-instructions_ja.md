# 公開Unity箱庭の最初の区切りを仕上げて、PRにする依頼（mc-remote-unity-sandbox）

> 前の依頼（`00-hub/unity-sandbox-first-slice-instructions_ja.md`）の返却で、作る順番の1〜4ができ、human ownerがScratchの
> LANパッケージとPythonのclientからつないで建てた（2026-11-15）。実装はまだcommitされていない。human owner「Unity箱庭は、
> 色々と試行錯誤してかなり完成度が上がっているが、もう少し、残っている。」。残りを仕上げて、PRにする。参照するknowledge
> commitは、この依頼が入ったmainのcommitです。

## 決まったこと（2026-11-15）

- portの既定は`25585`（`2026-11-15-01`）。確定搬送票は、この依頼と同じcommitで着地した。手元のNOTESの行は
  `[→DEC 2026-11-15-01]`にしてよい
- 地形は、human ownerが決めた今の形（`19-unity/README_ja.md`の「公開Unity箱庭」）

## すること

1. 残りを仕上げる。何を残りとするかは、human ownerと決める
2. PRにする。commitの分け方は担当が決める。mergeはhuman ownerが判断する
3. PRのheadで、human ownerがScratchのLANパッケージとPythonのclientからつなぎ、ペアリングと建築を確かめる
4. Webでの公開の配信と、公開のための上限（送り元ごとと全体のcodeの試行、世界のリセットの間隔、tokenをserverの再起動の後も
   残すか）は、hubで決めてから別に頼む。この票では足さない

## 返却

- 実際に読んだknowledge commit
- PRの番号、head、CIのrun（あれば）
- 前の返却から変わったこと（残りとして仕上げたもの）
- testとUnity Editorでの確かめ方と、PRのheadでのhuman ownerの確かめ
- 確かめられなかったことと、その理由

## coordinatorがすること

- PRとCIを、GitHubのAPIで照合する。mergeの後に、`19-unity/README_ja.md`の「現在地」を直す
- 公開の前に決めることの案を、human ownerに見せる（hub NOTESの「公開Unity箱庭へ進む」の行）

## 返却と照合（2026-11-16）

PR #2（head `bba6e4ca25a7d2a9d5798b99ad049a60022c85b0`）で返った。`00-hub/unity-sandbox-release-instructions_ja.md`への返却と
一緒なので、照合は同じfileの「返却と照合（2026-11-16）」にまとめた。human ownerがmergeする（2026-11-16）。
