# 一般CIの既知差分と版期待値の追補

- 初回source8783cc4666の一般CI: run39723268631。
- VMのJUnitから、leaf assertionの失敗はclient.versionの旧期待値3件と確認。sourceffb496ed50で期待値だけstableへ更新した。ローカル実行では534 PASS（修正前531 PASS／3 FAIL）。
- GUIはunit538 PASS／skip1、integration126 PASS／1 FAIL／skip7。
- GUI失敗: menu-bar.test.js「User is warned before uploading project file over an edited project」のNoSuchAlertError。forkは既存作品をブラウザへ保存してから別作品を読み込み、confirmを出さない。
- GUI本体とこのテストはrc1 tag ec79b3bから差分0。developにはPR #27で正しい保存・復元を検証するテストがあるが、今回はstable最小scopeに含めていない。
- 新candidate sourceffb496ed50の一般CIはrun39744780763。VMは成功、GUIは同じ旧alert期待1件だけ失敗（unit538 PASS／skip1、integration126 PASS／1 FAIL／skip7）。VMを含む7 packageとBuildは成功。候補用Actions run39744827621は成功。一般CIを全件成功と主張しない。
- 候補用Actionsの成否、版の回帰test、rc1 PASSの再利用条件をcoordinatorに返し、横断の最終判定は行わない。
