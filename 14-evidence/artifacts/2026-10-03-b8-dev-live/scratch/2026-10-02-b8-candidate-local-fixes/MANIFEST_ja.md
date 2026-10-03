# B8更新candidate素材（ローカル試運転の修正4件）

- 作成日: 2026-10-02
- source: `agent/b8-compatibility@691576f60b7f0824e1753bd6823901d01fbe2422`（push済み。GitHub APIのbranch refとHEADの一致を確認）
- knowledge contract commit: `49d5a59f50d357bfe7cd9c5401811a5e9e58eb59`（remote main。gate、着手指示、Scratch roadmapとruntimeを参照）
- 旧candidate: `df34849d2502a498a06c5fe07a91d03e925124eb`
- B8共有fixture: `054a3af017f1abb8cc01cf85b3bc83181e648e19`版と同一、36,481 bytes／111 case／SHA-256 `ca636b4a2685ea67f24d8e7931e3d30a84e7cec872bb5c5d2eadd178cdac39f2`。fixture変更なし。

## 採用した修正

```text
691576f60b feat(gui): update mc-remote artwork and display names
d69c4bb12b fix(gui): preserve script position during workspace zoom
95156290ec fix(vm): accept unqualified block information IDs
12b65b12c9 fix(gui): simplify catalog picker default states
```

pickerは選択肢の重複をなくし、catalogの順序のままデフォルト値を表示し、結果のStateTextからデフォルト値を省略する。60:40の配置、IDの右のcatalog状態、結果欄の文字拡大も含む。
BlockInfoTextの4 accessorは手入力のminecraft namespace省略を受け入れ、IDを完全修飾して返す。wire responseと生成値の完全修飾は維持する。
ズームは途中のcontent resizeを延期して中心ずれを直す。カードは新SVG2枚と指定文言、各表示名はmc-remoteへ更新する。

## 成果物

| file | bytes | SHA-256 |
| --- | ---: | --- |
| `scratch-image-inputs.tar.gz` | 138,375,344 | `c7318efdfb22076c2d40501a526d7ca16a121510f7685d875fff34cdc4404843` |
| `bridge-image-inputs.tar.gz` | 38,138 | `fd43f714c77d2bc184bf882460dfc05a1ce345dc6d4f5b52505a6a9d2850908f` |
| `wirescope-app.zip` | 83,746 | `4cb349894b71d61d7ca143d8362a5b79deb1810e1d7a9e31ad30e29bfe370a07` |
| `wirescope-app.manifest.json` | 2,321 | `6ea468f50d50b52722b8f34145743df86cebc60865fe0e827be5632c26b024d0` |
| `contracts.tar.gz` | 1,908 | `48948ba47d55409f02a8ff8e0d44021b07859e11ffa5ca0f8598e6ef06082390` |

GUI／Bridge tarはDocker imageの入力でありOCIではない。registry／Release assetへ掲載していない。通常devでは開発端末で動かすとのcoordinator指示を維持する。
WireScope ZIP、Bridge tar、contracts tarは旧candidateとbyte一致。WireScope detached manifestは新source commitを記録するため更新。Pythonの同梱WireScope再生成入力は上記source。

## ビルドとPASSの再利用

Node v24.19.0。既存のlock-installed workspaceを使用し、npm ciは再実行していない。

今回、新しいpush済みHEADで実行してPASS:

```sh
npm run build --workspace=@mc-remote/bridge
npm run build:artifact --workspace=@mc-remote/live -- --source-commit 691576f60b7f0824e1753bd6823901d01fbe2422
python3 handoff-materials/2026-10-02-b8-candidate-local-fixes/materials/verify-artifacts.py
```

GUI／VMはコミット直前に同じ製品コードで行った次のproduction buildを使用。コミットは内容の保存のみで、その後のGUI／VM source変更はなく、HEADとの差分なしを確認した。配布対象はGUI `build/` であり、以前のGUI `dist/`／standalone出力は今回のtarへ含めない。

```sh
NODE_ENV=production npm run build --workspace=packages/scratch-vm
NODE_ENV=production npm run build:dev --workspace=packages/scratch-gui
```

VM playground／node／webとGUI build:devはPASS。既存のoptional canvas／bundle size警告あり。Node版VMの追加起動smokeはjsdom stylesheet pathのENOENTで未解決であり、build成功やGUIのbrowser確認と区別する。今回その経路は変更していない。

実装時のunit／対象lint／翻訳抽出／ブラウザ確認を再利用:

- picker／block-ref／block-names: 3 suites／26 tests PASS。
- zoom helper／flyout／Blocks container: 3 suites／13 tests PASS。helper最終版3件もPASS。
- BlockInfoText: 10 subtests／94 assertions、McRemote extension: 123 subtests／528 assertions PASS。
- 表示名のGUI: WireScope panel／notice 25件、menu 6件、localization 5件の合計36件PASS。最初の3-suite batchでlocalizationの1件が失敗したが、翻訳IDの誤変更を直しlocalization全5件を再実行してPASS。他2 suiteとmenuのPASSを再利用した。初回失敗と再試験の両logを保存。
- GUI／VM対象lint error 0、翻訳抽出PASS。
- production GUIでの独立browser: picker 60:40、状態結果17.6px／選択13.6px、default省略、狭い幅の縦配置、namespace省略4 accessor、zoomの通常／min／max／resetの中心ずれ0pxを確認。
- 最新GUI表示の独立browser: palette mc-remote、notice footerと記事、ja-Hira説明文と協力表記を確認。human ownerも各言語／各表示場所とズームの改善を確認。

ログは `materials/verification-logs/`、machine-readable照合結果は `materials/verification.json`。ローカル素材であり正式knowledge evidenceではない。

## アーカイブの照合と再生成

全tarのmemberを入力directoryの全regular fileと集合・bytes・SHA-256で照合。GUI 1,729、Bridge 24、contracts 11ファイル。WireScope ZIPの全6 assetをmanifestのbytes／hashへ照合。manifestのsource commit、lockfile／package identityもHEADへ照合。GUI runtime configはschema_version 1、connection_enabled false。Bridgeにはworkspace-localのlock固定ws 8.18.3を収録する（repo rootのwsはScratch用の6.2.3で、Bridge入力ではない）。

入力tarは次の共通flagsを使う。

```sh
tar --sort=name --mtime='UTC 1980-01-01' --owner=0 --group=0 --numeric-owner --mode='a+rX,u+w,go-w' -cf - -C packages/scratch-gui Dockerfile.mc-remote build | gzip -n > scratch-image-inputs.tar.gz
tar --sort=name --mtime='UTC 1980-01-01' --owner=0 --group=0 --numeric-owner --mode='a+rX,u+w,go-w' -cf - -C mc-remote/bridge Dockerfile package.json dist node_modules/ws | gzip -n > bridge-image-inputs.tar.gz
tar --sort=name --mtime='UTC 1980-01-01' --owner=0 --group=0 --numeric-owner --mode='a+rX,u+w,go-w' -cf - -C packages/scratch-gui contracts | gzip -n > contracts.tar.gz
```

実際の保存先はこのdirectoryの `materials/`。既存candidate素材を上書きせず、旧素材はknowledgeのgate記録から参照されているため後継pathを付けて保持する。

## 残りと搬送

- devの統一実施票で、残るentity／nearby、typed particle／FAST通知、無印入力、2-player receiver、描画・音・定位、token継続、real-browser WireScopeを確認する。今回のartifact更新で完了とはしない。
- pickerとBlockInfoText受理範囲の局所決定は `DECISIONS-HANDOFF_ja.md` でknowledgeへ搬送する。projection §6の明示default保持の記述をhuman owner指示に揃える必要がある。
- fixture移管棚卸しは既存事前票を維持し、source凍結後に再採取する。owner／配布／sourceはb8で移さない。
- shared環境の変更、実MCへの操作、新たな人間参加試験、横断gate判定、tag／release公開は行っていない。
