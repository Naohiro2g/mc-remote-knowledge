# b3 candidate deterministic summary

- test class: `unit/deterministic`
- Scratch candidate: `release/b3@3f1a10a366bfbe76e32b5a31c54da19eddd56e56`
- GitHub CI: run `31145335984`

## 結果

- McRemote changed scope lint:
  - `npx eslint src/playground/render-gui.jsx test/unit/playground/render-gui.test.jsx --max-warnings=0`
  - exit 0、0 errors、0 warnings。
- scratch-gui full lint:
  - `npm run test:lint --workspace=packages/scratch-gui`
  - exit 0、0 errors、908 upstream既存warnings。
- scratch-gui関連unit:
  - McRemote runtime config、target persistence／reducer、observation reducer、WireScope、playground初期化。
  - 6 suites、28 tests PASS。
- scratch-gui full unit:
  - `npm run test:unit --workspace=packages/scratch-gui -- --runInBand`
  - 56 suites PASS、372 tests PASS、1 skipped、15 snapshots PASS。
- scratch-gui full build:
  - `CI=1 NODE_OPTIONS=--max-old-space-size=4096 npm run build --workspace=packages/scratch-gui`
  - exit 0。dev build warningなし。dist／standaloneは既存asset-size warningのみ。
- scratch-vm McRemote:
  - `node test/unit/extension_mcremote.js`
  - 52 subtests、147 assertions PASS。
  - disabled runtime config、build-time disableの一方向性、token非読出し、WebSocket非生成を含む。
- VM state snapshot／`.sb3` serialization regression:
  - `node test/integration/vm-state-snapshot.js`
  - 117 fixtures、117 PASS。
- GitHub Actions:
  - run `31145335984`、exact candidate SHA一致。
  - Build、Test scratch-gui、Test Resultsすべてsuccess。
- `git diff --check`: PASS。

## 境界

scratch-vm treeは先行candidateから変更されていないが、上記McRemote unitとstate snapshotは最終candidate worktree上で再実行した。buildのasset-size warningとfull lintの908 warningsは既存であり、今回変更起因warningは0。
