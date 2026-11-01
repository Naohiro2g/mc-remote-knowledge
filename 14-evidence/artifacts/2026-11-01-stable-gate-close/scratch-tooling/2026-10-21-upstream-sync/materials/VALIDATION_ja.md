# upstream追従の追加検証

- source: `6c5a9211231194984621d58325fe8c06cfc6e3b8`
- worktree: `/tmp/scratch-upstream-sync-20261021`
- branch: `agent/upstream-sync-2026-10-21`、remote head一致（6c5a921123）。
- runtime: 公式Node24.22.0、npm10.9.9。全production build済み。
- 変更: GUI保存仕様に統合testを合わせる。Render test helperのconstructor.name依存を解消。

## 結果とコマンド

- 新回帰test: `node packages/scratch-render/test/unit/PageUtilTests.js`。修正前4件中2 FAIL、修正後4 PASS。
- Render: `npm run tap --workspace=packages/scratch-render`。182 PASS（production bundle、実Chromium）。
- GUI: scratch-guiで `../../node_modules/.bin/jest --runInBand test/integration/menu-bar.test.js`。13 PASS。
- GUI変更fileとRender helper/new testのeslint、git diff --check PASS。
- Render probe: `node render-readiness-probe.cjs`。修正前はloadFile解決時にconstructor名BのSVG画像がcomplete=falseのまま残ることを実測。
- 既実行の全build／lint／他packageテストはPR本文案・ローカルNOTES参照。今回の追加変更はテストのみ。

## 制限

- 新headはpush済み。CI run39687278973（push）/39687285062（PR）はBuild、全8 package、Test Resultsがすべて成功。最新headのcheck-runsに失敗・pendingなし。
- 旧head540ea6c2のCI失敗ログ・JUnitを確認して原因を特定した。
- GUI全体実行は125 PASS/2 FAIL/7 skip後、失敗2件を修正または個別再確認してPASS。
- パレットずれの製品修正、公開release、deploy、develop統合は未実施。
- 実行時は一時Node binとChromeDriverをPATHへ、PLAYWRIGHT_BROWSERS_PATHを一時browser cacheへ設定する。
