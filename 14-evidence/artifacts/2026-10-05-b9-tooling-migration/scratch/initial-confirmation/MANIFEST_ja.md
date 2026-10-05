# b9 Scratch確認票の搬送素材

- 作成日: 2026-10-04
- 搬送元: `Naohiro2g/scratch-editor`、`agent/b8-compatibility@1ecd531221ed88523594284a5bc963bad97a2f83`。default branchは`develop@00c01460e2f994c4ed5f097070cae41867c320a9`
- 種別: b9 gateの確認票返却と移管評価材料。横断判定・移管実行の承認ではない
- knowledge contract commit: `ceba53099fa001fea6b83d68deadc1eb9e0038fe`
- 読む順: `materials/CONFIRMATION_ja.md` → `materials/ASSESSMENT_ja.md`
- 材料: 上記2文書、契約の監査script／結果JSON、fixture byte照合script／結果JSON、正式起点のfixture baseline metadata、`SHA256SUMS`
- 再現方法: リポジトリルートから確認票に記載したNode／Python commandを実行する。Node probeはinstall済みの既存TypeScriptを使い、現在のWireScope parser sourceを一時的にtranspileして調べる。製品fileやbuild出力は変更しない
- 比較起点: 公開b8 source `691576f60b7f0824e1753bd6823901d01fbe2422`とknowledgeの正式fixture一覧。baseline metadataは同一覧のpath／bytes／digest／case数を写した照合入力であり、fixtureのowner copyではない
- test class: unit/deterministic。未知event拒否とnull受入の再現は現在の実装の監査であり、b9適合を証明するPASSではない
- non-claim: new owner build／CI／consumer、candidate／artifact、shared deploy、実機／live-human、公開サーバー反映、tag／release公開は今回行っていない
- ナレッジ着地: b9 gateの確認票返却。正式evidenceの収容・recordのauthoringはknowledge側で扱う
- cleanup: 後続b9作業の起点として保持。knowledgeへの収容・照合後に処理する。公開Gitへstage／commit／pushしない
