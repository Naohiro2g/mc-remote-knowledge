# Scratch 2321.1.0 候補の返却

- knowledge contract path：`00-hub/release-gate-notes_ja.md`「2026-11-06 2321.1横断release gate」。
- knowledge contract commit（実読）：`d355cc33cefc7fa361367244d6a982d44945931e`。userのpush連絡後、remoteの存在と内容を確認。
- 関連するpickerデータの設計とruntimeも参照。判定はcoordinator／human release ownerが行う。共有環境の変更・人間試験開始・tag／Release公開は行っていない。

## 1. 候補と検証

- repository：`Naohiro2g/scratch-editor`。
- branch：`agent/palette-picker-2026-11-06`。
- commit：`07f98ebf9be84db5ad2467cebe2c166bbe4c43f5`。
- PR：[29](https://github.com/Naohiro2g/scratch-editor/pull/29)（base `develop@05bf1dd014256dd978ebc5284f67b9255480fc50`）。2026-11-07 06:04 JSTにmerge済み。
- client表示：`2321.1.0`。protocol：`23.2.1`。
- マージ先：`develop@11bce3193c524135931a5bf342a9edb1bfdfbbac`（remoteで確認）。候補とmerge commitのtreeはいずれも`50a173cd1933f55afaf8c8b2cfbcb1d3538a4838`で同一。生成済みartifactのsourceは`07f98ebf9be84db5ad2467cebe2c166bbe4c43f5`のままで、merge後の再生成はしていない。
- [merge後CI](https://github.com/Naohiro2g/scratch-editor/actions/runs/42293693018)：実行中。照合記録は`MERGE_CONFIRMATION.json`。
- 最終commitの[push CI](https://github.com/Naohiro2g/scratch-editor/actions/runs/42245524926)：success（build／GUI／VM）。同じcommitの[PR CI](https://github.com/Naohiro2g/scratch-editor/actions/runs/42245536170)も全項目success。
- [候補配布物の生成](https://github.com/Naohiro2g/scratch-editor/actions/runs/42245622899)：success。Web／LAN 3 OS／Scratch OCI生成、Linux ZIP起動・終了と3ポートcloseの決定論的smoke、Bridge OCIのdigest維持、manifest／lock照合がすべて成功。

| 変更する境界 | 実行した検証と結果 |
| --- | --- |
| パレットの座標変換 | `configure-continuous-flyout.test.js`の新2件は修正前FAIL、修正後は既存4件を含め6 PASS。GUI全unitにも含む。 |
| picker検索・適用 | `mcremote-block-names.test.js`／`mcremote-block-picker.test.jsx`＋flyoutの対象3suiteで36 PASS。カテゴリの重複所属、版・namespace・current catalog限定、AND検索、IDだけの適用を確認。新検索テストは実装前FAILを確認。 |
| GUI全体 | `node ../../node_modules/jest/bin/jest.js --runInBand test/unit`：74 suite、551 PASS、既存skip 1、snapshot 15 PASS。 |
| 拡張の版表示と既存動作 | `node test/unit/extension_mcremote.js`：125 subtest、534 assertions PASS。 |
| lint | 変更したGUIのJS／MJSはerror 0。新生成器・flyout source/testはwarning 0。picker周辺のwarning 18件はすべてbaseから不変の行。VM変更2fileもlint PASS。新たなlint除外なし。 |
| ビルド | Node 24.22.2でルートの`npm run build`：全workspace PASS。既存のbundle size等のwebpack warningは残る。 |
| 実Chromium | パレット初回の頭出し誤差が修正前21.1846px→修正後0px。toolbox再描画後とscrollbar resize後も0px。pageerror 0。pickerは合成CURRENT catalog（26.3）で`建築ブロック gold`→`gold_block`／空stateの適用を確認。実サーバー接続はしていない。 |
| 公式カテゴリ生成 | 公式client／metadata／library／ja assetのSHA-1を照合して3版とも抽出成功。helperと出力のSHA-256を`sources.json`と照合。全11カテゴリ、1.21.11=1,089／26.2=1,118／26.3=1,207ブロック。 |
| LAN配布のlicense収集 | 初回候補生成はBlockly 12.5.1の本文補完不足でFAIL。npm gitHeadと公式tagの同一commitを確認し、既存の補完表に追加後、実依存からのlicense収集PASS。`python3 scripts/build-mcremote-local.test.py`：11 PASS。 |

ブラウザ検証はin-app browserのnative bridgeが利用不可だったため、troubleshooting確認後に独立Playwright/Chromiumを使用した。ユーザーの既存ブラウザ状態は使用していない。詳細は同梱JSONとscript。

## 2. v2321.0.0から入る変更の全体

比較元：`v2321.0.0@ffb496ed50d751d307f685f2ae555c94c893fae5`。全commitは`ALL_COMMITS.txt`、全file差分は`CHANGED_FILES.txt`。

1. 本家追従PR #27（136 commit）と #28（追加56 commit）。対象本家headは`01421e767f962e64b2a71e59699774ab3f51a621`。SVG sandboxのscript配信・CSP・nonce・eval除去とPaper.js、作品ロード時の欠けた変数／リスト／broadcast定義とIDの修復、stage／spriteの共有定義、サムネイルの取得・保存callbackと失敗時処理、ライブラリ画像URL設定、Redux middlewareのstore単位化、関連テスト／文書を含む。
2. 上記に伴う依存と開発基盤の更新。Scratch Blocks 2.2.2、Blockly 12.5.1、翻訳・audio・sb1 converter・render fonts等、webpack／開発server／lint／Node 24.22.2、lockfile、各package版とCI／release／i18n／署名・review workflowを含む。GUIのbuild依存のdevDependencies移動とroot npm pinの削除、sandboxのdevelopment時inline／production URL配信も含む。推奨ブラウザ下限はChrome／Edge 124、Firefox 125、Safari 17.4。
3. fork側の追従テスト整合：別作品ロード前のブラウザ保存・復元、SVG描画待機等。本家SVG隔離と作品定義の修復はsecurity／永続データに関わる差分として明示する。今回の2機能だけをstableとの差分全体とは扱わない。
4. MIT fixture取得元更新（merge済み`48d357a31265fc7487f693ba1df5d20b6ea92759`）。取得元をtooling `21a2a9a0aed8b4d9c715da46616aad86f1174b4c`へ固定し、MIT LICENSEの取得・検証を追加。artifact用source `6447f6e8cbfbeeb9d229990b5c4f6e82a5875666`とは分けた。既存fixture JSON15本のidentityは不変。
5. 今回のパレット修正（`9a4ac4c265f44eaa5fa8e81eefd016c85c138db5`）。カテゴリへのauto-scroll前にscrollbarの寸法を更新し、現在の座標変換を使う。親の丸め・手動scrollのキャンセルを維持。
6. 今回のpicker改善（`dc4296d9e8`）。公式カテゴリの英語・日本語aliasを別データとして同梱し、検索対象へ追加。表示用の既存ブロック名辞書は不変。カテゴリの取得元・抽出条件・更新用generatorと説明、翻訳placeholder、回帰testを追加。管理者用アイテムの表示を有効にしたVanillaの通常feature flagsで抽出し、重複所属を保持する。生成用JDK 25はエディターのビルド・利用には不要。
7. 候補の版表示を2321.1.0へ更新し、対応する拡張テストを更新（`c75322f1f7b9f1452776167bb27029942320bd3f`）。
8. 公開済みstableのブロック一覧と版別snapshotをそのままdevelopへ保持（`ee004ea65ace5b9786cc59920c909a9548bd0ef9`）。`mc-remote/block-reference/site/`はstableとbytes同一。公開ページは変更していない。2321.1.0版の一覧ページと入口の公開更新は、release用の配布準備で行う。
9. LAN生成に必要なBlockly 12.5.1のlicense補完表と本文・NOTICEを追加（候補head）。公式tag／npm gitHeadはいずれも`6f7d50552ee658299de16c139673c2d126ac9b16`。Apache-2.0本文は11,358 bytes、SHA-256 `cfc7749b96f63bd31c3c42b5c471bf756814053e847c10f3eb003417bc523d30`。launcher・guide・builderのcodeには変更なし。

stable closeでdevelopへ戻した配布guard・LAN案内リンク（`b1f3ab883a`）は、公開stableに既に含まれるため新機能として数えない。READMEのrc1追補等の文書差分は全file一覧に含めた。

### 変えていない共通部分

- wire／API：McRemote VM拡張`index.js`はstableとbytes同一。拡張source内の差分はclient-versionのみ。protocol 23.2.1のまま。
- Bridge本体・WireScope本体：ownerはtoolingであり、本PRに変更はない。tooling-lockのartifact設定とartifact用sourceはstableと一致。
- Bridge index：`sha256:305d6e38b36e195a0e158522f32f3a8c45d39da2aeec7b7e46f785c920406acf`。
- WireScope ZIP：83,854 bytes、SHA-256 `da3da0b6cf4d05265bc0c11abaa4913208c7cfc3600b0c3e78c93a356fc431ad`。manifestも固定値不変。
- 共有fixture：既存15 JSONのbytes／SHA-256はstableのlockと一致。MIT LICENSEを含むcache16fileもlockに全件一致。
- runtime config／product configのschema、WireScope観測feedのcode、Node runtime lock、release manifest lockは変更なし。
- LICENSE：`mc-remote/tooling/fixtures/protocol/test/fixtures/LICENSE`、1,070 bytes、SHA-256 `aa329a0bafc839b95124306141db13a381de45818bf629e983c44ea55ab5a7fb`。

## 3. 作り直す配布物

| 配布物 | 2321.1.0としての扱い |
| --- | --- |
| Web editor | 新しいGUI・カテゴリデータ・版表示で再ビルドする。 |
| LAN package | Windows x64／macOS arm64／Linux x64の3 ZIPを再生成し、内部のエディターを更新する。Bridge／WireScope／Nodeは既定の固定入力を再利用する。 |
| Scratch OCI | 新しいWeb editorでlinux/amd64／linux/arm64を再生成する。共通Bridge OCIは固定digestを保つ。 |

LANのランチャーはv2321.0.0と同一。「はじめに.html」はuserが許可した版表示2か所（titleと版の段落）だけ2321.0.0→2321.1.0に変える。本文・動作は同一。guide生成器とZIP生成器のcodeもstableと同一で、実生成したHTMLを版文字列だけ置換してbytes一致を確認した。Blocklyのlicense補完は配布物の第三者ライセンス資料の追加であり、launcher／guideの変更ではない。

最初の生成run `42242356556`はlicense不足で失敗した旧headの試行で、候補として採用しない。最終生成物のidentityは最終headのrunとmanifestで返す。tag／Releaseは作らない。

## 4. 人間の試験案（coordinatorの進行待ち）

自動testで確かめたAND検索・版分離・ID送信・数値としての位置ずれ・file identityは人間試験へ重複して課さない。

- 実際に使うiPad／Androidタブレットで、カテゴリを切り替えてブロックを探す一連の操作を行う。見出しの見つけやすさ、タップのしやすさ、作業中に位置を見失わないかを確認する。
- ソフトウェアキーボードを出して日本語カテゴリ語を入力し、検索結果を選んで元の作品へ戻る。キーボードやviewportにより選択・適用が妨げられず、入力し直しや確定操作が自然にできれば合格。
- 普段の制作で探すカテゴリ語（建築・天然・色付き・レッドストーン等）を使い、公式タブ名の検索結果が理解できるかを確認する。意図したブロックを選んで制作を続けられれば合格。

端末候補：iPad第6世代のSafari 17.4以降、Android 10端末の更新済みChrome。端末／接続先と開始時期はcoordinatorが指定する。実機参加試験はまだ開始していない。

## 5. release notes案／tag案

tag案：`v2321.1.0`。

> パレットでカテゴリを選んだとき、見出しの位置がずれる問題を修正しました。
>
> ブロック選択画面で、クリエイティブインベントリのカテゴリ名でも検索できるようになりました。たとえば「建築ブロック gold」や「Redstone Blocks」で絞り込めます。Minecraft 1.21.11・26.2・26.3の公式の日本語名・英語名に対応します。
>
> Scratch本家の更新を取り込み、作品の読み込み・保存、SVG／コスチューム処理などを更新しました。推奨ブラウザの下限はChrome／Edge 124、Firefox 125、Safari 17.4です。iPad／iPhoneではiPadOS／iOS 17.4以降が目安になります。
>
> Web版・LANパッケージ・コンテナを更新します。通信protocolは23.2.1のままで、McRemoteのAPIは変わりません。

Release本文に内部の凍結経緯やSHA表は置かない。配布物のidentityはmanifest／checksumsから参照する。

## 6. 未検証の境界と残るrelease準備

- iPad第6世代／Safari 17.4、Android 10を含む実機での操作・ソフトウェアキーボード・小さい画面の見やすさは未検証。
- 今回のブラウザ検証は合成catalogであり、McRemote 1.21.11／26.3と実接続した結果ではない。
- 3 OSの実機LAN起動・native dialog・署名警告は今回未検証。coordinatorが変更範囲と過去結果の再利用可否を判断する。
- 新規カテゴリ抽出はVanillaの通常feature flags・管理者用アイテム表示での所属。resource pack、mod、実験的featureや、同梱3版以外へのカテゴリ語の対応は主張しない。対応がない場合も既存のID／名前検索を使う。
- 2321.1.0版のブロック一覧生成と公開入口の更新は、release用の配布準備で行う。旧版は保持済み。
- 最終配布物の凍結、他componentとのexact set、共有環境へのdeploy、人間試験、公開可否はcoordinatorの工程。今回の成功を横断gate合格の宣言にはしない。

## tooling E1（別返却、2321.1 releaseの範囲外）

- 2026-11-07 06:18 JST、PR #2のmergeと`main@1f1a6ac8584e786de996a00ea089eaff45ee92cb`への反映を確認。merge前の文書とtree同一。文書2fileだけで、fixtureと実装は不変。
- [マージ後CI](https://github.com/Naohiro2g/minecraft-remote-tooling/actions/runs/42295652027)：実行中。確認記録は`TOOLING_E1_MERGE_CONFIRMATION.json`。Scratch候補のfixture取得元は21a2a9aのまま変更していない。

- 実読knowledge：`8c81c0f115127189de117c3848d1e254f79571c9`の指定3文書。
- branch：`agent/e1-fixture-inventory-2026-11-06`。
- push済みcommit：`1286eb486bcaea93c4195c11e94304bdb51f53ba`。
- 文書：[packages/protocol/FIXTURE_INVENTORY_ja.md](https://github.com/Naohiro2g/minecraft-remote-tooling/blob/1286eb486bcaea93c4195c11e94304bdb51f53ba/packages/protocol/FIXTURE_INVENTORY_ja.md)。READMEからリンク。PR [2](https://github.com/Naohiro2g/minecraft-remote-tooling/pull/2)。
- metadata32 method、auth5、能力14の51行をInventoryと同順で記載。fixtureの現行／履歴とcase範囲、10本のprotocol／case数／目的／位置づけ、F1の不足と追加案を記載した。
- 基準tooling `21a2a9a0aed8b4d9c715da46616aad86f1174b4c`のJSON10本とLICENSEを変更していない。fixtureは追加していない。
- CI [42227863796](https://github.com/Naohiro2g/minecraft-remote-tooling/actions/runs/42227863796)：success。
