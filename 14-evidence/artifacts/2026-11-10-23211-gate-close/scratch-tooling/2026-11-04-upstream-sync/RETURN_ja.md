# 本家追従：追加56 commitの統合・検証結果

- 実読knowledge：`6d408c789aa72cffa2c547fe5ae97c3aa56e6d93`。runtime／INDEX、`13-scratch-client/scratch-upstream-design_ja.md`を実読。
- base：`origin/develop@b1f3ab883a8124b7b3e5a9c46e6f7cc41e3a310b`。
- 今回取得した本家head：`01421e767f962e64b2a71e59699774ab3f51a621`。開始時のbehind 56、取り込み後の作業branchはこのheadに対してbehind 0。
- 統合commit：`d11f2b1ecae17d47d252c16205c488c817d3c964`。baseと本家headを親に持つmerge commit。
- branch：`agent/upstream-sync-2026-11-04`。push済み。
- PR：[Naohiro2g/scratch-editor #28](https://github.com/Naohiro2g/scratch-editor/pull/28)。Draftを解除し、レビュー可能な状態。developへのmerge、tag／Release／OCIの公開はしていない。

## 取り込んだ内容と競合の解消

22fileの変更。scratch-blocks 2.2.2、scratch-l10n 6.2.3、音声・描画font等の依存、Node 24.22.2、Scratch workspace 15.3.0の更新が中心。
開発buildではSVG sandboxのscriptをinline配信し、本番のHTTP(S)ではURL配信する本家の修正も含む。

競合はroot package／lock、GUI packageの3fileで、McRemote本体に直接競合なし。
McRemote用のroot Ajv 8.20.0、markdown-it 14.1.1、GUI Ajv 8.17.1と独自scriptを維持した。
本家のbuild依存のdevDependencies移動とroot npm pinの削除を採用し、npmでlockを整合した。
本家から追加されたBrowser Baselineの指示もAGENTSに取り込んだ。

McRemote拡張、runtime config／schema、product notice、LAN launcher、tooling／Node配布／manifest lockはbaseから差分0。
パレットの製品修正、保存先指定、接続UI等の新機能を今回の追従へ加えていない。

## 検証

- Node 24.22.2／npm 11.19.1。Node archiveは公式SHA-256一覧と照合済み。
- `npm ci`、全workspace `npm run build`、`git diff --check` PASS。buildの既存のbundle size等のwarningは残る。
- CI：push run `41798158174`、PR run `41799334911`ともsuccess。Build、全8packageのtest、結果集約を確認した。
- ローカル：GUI unit 544 PASS／1 skip、SVG unit 254 PASS、SVG実Chromium 69 PASS、Local Node25＋Python11 PASS、manifest96 PASS、tooling6 PASS。
- GUI／VM／SVGとLocal／manifestのlint PASS。
- ローカルVM全体は並列・coverage実行で4235 PASS／9 FAIL。control／execute／vm-state-snapshotの時間依存の失敗と後続timeoutで、controlはproject loadの完了より先に2秒timerが発火した。3fileを同じNodeで単独実行して2／165／118件すべてPASS。VMのCIもsuccess。テストコードの修正は加えていない。
- 詳細は`LOCAL_CHECKS.json`、`VM_RECHECKS.json`、suiteごとのlog。初回失敗のlogも保持し、全ローカルtestが初回から成功したとは主張しない。

## パレットの実画面観測

内蔵Browserはnative接続が初期化できず、skillのtroubleshootingを確認後、独立Playwright／Chromiumで一時HTTP配信したbuildを測定した。
McRemoteへの接続は無効なruntime configのまま使用し、実Minecraftには接続していない。

- page error 0。
- McRemoteカテゴリの頭出し誤差：約21.1567px。
- 古いscrollHeight 8188.7625、実scrollHeight 8180.6625。前回と同じく古い寸法の換算比が残っている。
- probeの`scrollbar.resize()`後は誤差0、scrollTargetも解消。
- `palette-probe.json`、`palette-before.png`／`palette-after.png`を保持。
- **scratch-blocks 2.2.2への更新だけでは既知の頭出しずれは直らなかった。** 修正を追加するかは次のrelease範囲で選ぶ。
- 一時HTTPサーバーは停止済み。新しい3 OS実機確認、iPad／Androidでの参加確認はしていない。

## 単独版の準備で扱うこと

本家は対応ブラウザー下限をChrome／Edge124、Firefox125、Safari17.4へ変更した。iPadのSafari下限に関係するので公開時の案内へ含める。
これはbrowser floorのsource確認であり、iPad実機の合格を意味しない。

公開stableに入っていなかった前回の本家追従と今回の56 commitを、新しいScratch単独版へ採用する候補が整った。
release番号、版別ブロック一覧の保持・生成、お知らせ、追加の修正範囲、採用するgateと実機検証は、`2026-11-04-scratch-standalone-release-review`の棚卸しに接続する。
単独版の公開や他component／Stackの更新は今回実施していない。
