# ナレッジ向け搬送票：ローカル試運転で確定したScratch入力支援

以下はhuman ownerの実画面レビューと実装指示による局所決定2件。
artifactのidentityは同directoryの `REPLY_ja.md` と `MANIFEST_ja.md` を参照。
参照knowledge commitは `49d5a59f50d357bfe7cd9c5401811a5e9e58eb59`。

## 確定搬送票（1：pickerのデフォルト値省略）

- 搬送元 repo: Naohiro2g/scratch-editor
- 搬送元 surface: カタログpicker／Scratch block value入力支援
- 搬送元 branch/commit: `agent/b8-compatibility`、実装 `12b65b12c9`、更新candidate `691576f60b7f0824e1753bd6823901d01fbe2422`（push済み）
- 作成日: 2026-10-02
- 種別: 局所決定
- 決定: pickerのproperty選択肢はcatalogの順序を保ち、各値を1回だけ表示する。デフォルト値に「（デフォルト）」を付け、選ぶとStateTextからそのpropertyを省略する。有効な現在catalogと照合できる既存入力・手入力でもデフォルト値を省略する。catalogが利用できない入力や無効な自由入力は保持する。
- 理由: human ownerが「デフォルトは設定を省いたときに使われる値」としてUIを統一するよう指示。同じ値の二重表示と、説明に反する結果欄の表示をなくす。
- 却下案（3件まで）: 別のデフォルト選択肢と同じ値を並べる案。デフォルト値を明示的に保持する操作をpickerへ残す案。
- 影響: pickerを開いて適用すると、catalogのデフォルト値の明示指定は保存されない。`world.getBlock`由来のBlockInfoTextのfull state、一般StateText parser、手書きscriptのwire stateは変更しない。共有fixtureは変更しない。
- 根拠/検証: human ownerの指定と実画面確認。unit/deterministicのpicker／block-ref／block-names 26件PASS。独立browserの試験用catalogで選択肢の順序・重複排除・デフォルト省略・Scratch入力への適用を確認。正式横断live-humanではない。
- 既に変更した実装/文書: picker JSX／CSS／日英・ひらがな表示文言／対応test。左右60:40、ID横のcatalog状態、結果StateTextだけの文字拡大もhuman owner確認済み。
- ナレッジ着地希望: `13-scratch-client/scratch-block-value-projection-design_ja.md` §6とScratch roadmap。現行§6の「既存StateTextの明示property集合維持」「get由来full stateの全property保持」は、このpickerのデフォルト値省略に揃える。§7は多言語表示と検索で、今回の保持規則の該当箇所は§6。
- 捕捉 cleanup: 本票と検証素材はローカル `handoff-materials/2026-10-02-b8-candidate-local-fixes/`。gate確認票も同directoryを参照しているため、着地確認とgateの素材整理で参照先を決めて処理する。
- 着地後の確認戻り先: Scratch担当session。着地した公開SHAとpathを返してほしい。

## 確定搬送票（2：BlockInfoText手入力の名前空間省略）

- 搬送元 repo: Naohiro2g/scratch-editor
- 搬送元 surface: BlockInfoTextの4 accessor
- 搬送元 branch/commit: `agent/b8-compatibility`、実装 `95156290ec`、更新candidate `691576f60b7f0824e1753bd6823901d01fbe2422`（push済み）
- 作成日: 2026-10-02
- 種別: 局所決定
- 決定: BlockInfoTextのID／状態／property／property有無の4 accessorで、手入力のblock IDにnamespaceが無ければ `minecraft:` を補って受理する。`oak_log[axis=z]`のIDは `minecraft:oak_log` を返す。他namespaceは保持する。
- 理由: human ownerが他のresource ID入力との整合を求めた。wire §5.0.2のnamespace省略規則に揃え、手入力でも同じ書き方を使えるようにする。
- 却下案（3件まで）: 手入力でも完全修飾IDだけを受理する案。
- 影響: Scratch内の入力受理範囲だけを拡張。serverからのBlockValue、生成されるBlockInfoText、accessorのID出力は完全修飾を維持。空namespace・複数コロン・大文字・空白・状態重複・非正準のproperty順序の拒否を維持。wire／共有fixtureは変更しない。
- 根拠/検証: knowledgeのwire §5.0.2、Scratch projection §3・4。unit/deterministicでblock-value 10 subtests／94 assertions、拡張123 subtests／528 assertions PASS。production GUIの独立browserで登録済み4 primitiveの省略入力、別namespace保持、壊れた入力拒否を確認。実MCへの追加通信なし。
- 既に変更した実装/文書: VM共通BlockInfoText parserと対応test。local NOTESへ経緯を捕捉。
- ナレッジ着地希望: `13-scratch-client/scratch-block-value-projection-design_ja.md` §3・4とScratch roadmap。生成値の正準形と手入力の受理範囲を区別し、手入力はnamespace省略を受けて完全修飾へ補うと明記する。
- 捕捉 cleanup: 本票とcandidate確認票をknowledgeへ着地確認後、gateの参照先を確定して同directoryの素材を整理する。
- 着地後の確認戻り先: Scratch担当session。着地した公開SHAとpathを返してほしい。

## その他の同梱変更

- workspace zoomのcontent resize延期による中心ずれ修正：`d69c4bb12b`。ブラウザ自体の表示倍率を変えたhuman ownerの確認も済み。
- 拡張機能カードのSVG2枚、名前・説明・協力表記、palette／notice等のmc-remote表示名：`691576f60b`。human ownerが各言語・各場所で確認済み。
- candidate成果物の更新まで完了。正式dev横断試験、shared配置、tag／release公開は未実施。
