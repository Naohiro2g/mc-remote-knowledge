# b9 Scratch確認票の別紙

参照knowledge: `ceba53099fa001fea6b83d68deadc1eb9e0038fe`。調査対象は自repo、公開b8 source、knowledgeの指定文書。実装・移管・他repo操作は行っていない。工数は実装を試した計測値ではなく、確認した依存と作業箇所に基づく推定。

## 1. b8公開後のdefault branchとb9予定

default branchは`develop@00c01460e2f994c4ed5f097070cae41867c320a9`。

| commit | 内容 |
| --- | --- |
| `16887de920` | READMEに公開Protocol API一覧とReleaseへのリンク。元commit `4fce39e21a` |
| `00c01460e2` | Scratchブロック一覧ドラフト、56ブロック＋組み合わせ2例のSVG、生成器、README入口。元commit `1ecd531221` |

公開b8からのdefault branch差分は文書・一覧・生成器の73 fileで、製品runtime／shared fixtureは不変。保持branch `agent/b8-compatibility@1ecd531221`にある`01cdb0bfee`（WireScope列幅）はdefault branchへ取り込んでいない。b9はこの列幅、契約2件への対応とfixture、批准後の移管と取得経路、picker aliasを予定する材料がある。selfの表示を「自分だけ」へ短くするhuman owner提案もローカルNOTESに残る。

一覧はknowledge側へコピーされたとのhuman owner連絡があり、現在のremote main `ceba530`もその収容commit。ただし本票では公開サーバーの反映・runtime notices更新を検証していない。

## 2. 現在の依存

| 部品 | runtime／build | testと配布の結合、外へ出すと切れるもの |
| --- | --- | --- |
| Protocol `mc-remote/protocol` | dependency-freeのTypeScript投影。VM／GUI／Bridge／WireScopeはこのpackageをruntime importしない。VMはinline wire定数、WireScopeは自分のobserver parserを持つ | owner testは同packageのfixtureを読む。root workspace／lock／CIに所属。VMの4 test fileとWireScopeの3 test fileに、Protocol fixtureへの直接の相対pathがある |
| WireScope `mc-remote/live` | 独立Vite browser app＋observer/session/station/handoff library。GUIからこのpackageへの直接importはない。GUIは自分の`mcremote-wirescope-source.js`でMessageChannel sourceを提供 | observer/session testがProtocol fixtureを読む。VM testがdisplay-alias fixtureを読む。artifact generatorはroot LICENSE／lock、Scratch repo URL、`mc-remote/live`を固定している |
| Bridge `mc-remote/bridge` | NodeでWebSocket⇄newline TCPを中継。通常のwire payloadは解釈しない。`one-shot-v1`の外側だけを解く。Protocol package importなし | VM testがone-shot fixtureを読む。CIの明示job、Dockerfile、image workflow、root workspace／lockに所属。ブラウザ接続を維持するにはBridgeまたは同等のWS⇄TCP経路が必要 |

直接参照するVM testは`extension_mcremote.js`、`mcremote_block_value.js`、`mcremote_event.js`、`mcremote_sign.js`。WireScope側は`observer.test.ts`、`sound-resource-observer.test.ts`、`session.test.ts`。共有fixture12件のconsumerの完全一覧は既存の正式`FIXTURES_ja.md`を正とする。

runtimeのimportがないので、GUI／VMの通常buildへ新しいnpm packageを必須にしなくても切替できる。fixture consumerの取得とpath、root `package.json`のworkspacesと`package-lock.json`、`.github/path-filters.yml`、CI／package test workflow、release workflow、README／AGENTSの所有説明を変える必要がある。

Scratchに残すもの: VM／GUI、wire commandを生成する拡張、Scratch固有のframe生成・handoff開始・起動UI・mini表示・browser接続設定、Scratch product/runtime config契約（`packages/scratch-gui/contracts/`）、そのconsumer test、ブロック名辞書・picker・一覧生成器。

WireScope browser側の`scratch-adapter.ts`は、viewerがScratch sourceへattachするadapterであり、viewerとともに移す候補。Scratch側sourceはGUIに残す。station adapter／observer schema／session／fixture／artifact generatorは共通owner候補。b9の移管に合わせて`source_kind`やobserver schemaを再設計する必要は別途評価する。現在のschemaは`scratch`／`python`に限られ、Java等への中立化を実装済みとは主張しない。

## 3. topology別の具体案

以下はhuman owner判断のための比較。日数は1担当がScratch／新owner側を扱う作業日で、他repo担当の工数・外部設定・CI待ち・統一liveは含まない。

| 候補 | 移す範囲／Scratchに残すもの | CI／releaseの変更 | 見込み |
| --- | --- | --- | --- |
| 共通TypeScript tooling monorepo（推奨） | Protocol型・定数・owner test・7 fixture、WireScope app/library/adapters・4 fixture・artifact generator、Bridge transport/config/test・1 fixture。Scratch側は上記consumer部分 | 新ownerの独立npm lockと3 packageのbuild/test、WireScope ZIP＋detached manifest、Bridge OCIを用意。Scratchはfixtureを固定SHAで取得し、release workflowが新owner artifactを収集する。旧workspace／owner sourceは撤去 | 2〜4作業日。10/6に範囲が決まり、依存を据え置いて移すなら10/10は条件付きで可能 |
| Protocol repo＋WireScope repo | ProtocolとWireScopeを別ownerにする。Bridgeはどちらに置くか、Scratch専用として残すかの追加判断が必要 | 2つ以上のlock／CI／release／provenanceと、repo間のfixture pinを持つ。Scratchは複数の取得先を読む | 3〜5作業日以上。10/10の範囲としては余裕が少なく、最初から分ける実益を確認したい |
| 一時Hybrid | 新ownerに正本を移し、Scratch側には新ownerから取得した生成物／fixtureを一方向で消費させる。編集可能なowner sourceを恒久的に残さない | SHA／digest一致をCIで検査する。b9／次release等の終了時期、完全切替の条件、削除対象を先に決める | 最初の切替は1.5〜3作業日程度だが、その後の撤去を含む全体では短いとは限らない |

既存`Naohiro2g/minecraft-remote-protocol`を使う場合: knowledgeでparkされた`3f7c3586…`は古いProtocol snapshotで、b8最新版ではない。park解除・役割／名前の判断後、公開b8 source＋fixture12件を起点として更新する。monorepo案ならWireScope／Bridgeとrootのlock／CI／releaseも加える。bootstrapの存在だけではowner切替にならない。

既存repoを使わない場合: 中立repoを新設し、同じ公開b8起点を取り込む。新repo名・visibility・権限・CI／registry接続の外部操作が増える。既存park repoは引き続きparkのままで、consumerを混在させない。どちらの場合も移すsourceの範囲と公開sourceへの参照を先に決める。

## 4. Bridgeの選択材料

このrepoで確認できる利用経路はScratchのbrowser接続とone-shot pairing。Python等のdirect TCPはSSOTにある別経路で、Bridgeを通る必要はない。他deploymentの全利用者は調査していない。

| 選択 | 材料 |
| --- | --- |
| 現機能を維持して共通ownerへ移す（推奨） | 新APIを加えず、Scratchの接続経路とOrigin／Sandbox allowlist・TLS終端境界を保つ。現在の透明なtransportとして他browserでも利用できる |
| 一般化 | browser client／station向けのprofileや命名を整理できるが、認証包み・routing・deployment契約・security testの変更が増える。b9の移管と分ける案 |
| Scratch専用へ縮小して残す | runtime source移動は小さくなるが、共通transportのowner境界が分かれる。VMのone-shot fixtureをどこが持つかも決める必要がある |
| 廃止 | 同等のWS⇄TCPとOrigin／target制御を担う代替が要る。今回の調査では置換可能な実装を確認できていない。station adapterはobserver attach用で、Scratch command transportの代替にはならない |

## 5. 取得方式とbuild

| 方式 | 現在のScratch buildとの関係 |
| --- | --- |
| npm | fixtureの配布や型をnpmへ収める構成は可能だが、現在の3 packageは`private: true`で手動publishを止めている。新しいregistry所有・公開workflow・fixture同梱が要る。現状のruntimeにnpm依存を加える必要はない |
| Git commit pin（fixtureの推奨） | 新ownerを固定SHAでcheckout／archive取得し、VM testがその取得directoryを読む。通常のGUI／VM buildは直接importがないので回せる。複数workspaceを持つGit repoの一部を、そのままnpmのgit dependencyに指定する方式とは区別する |
| vendor | 固定SHA由来のread-only消費物とdigest検査なら一時Hybridに使える。Scratchでsourceを編集し、新ownerと双方向同期する方式は採らない |
| 生成物（WireScopeの推奨） | 新ownerのZIP／detached manifestを固定digestで取得する。Scratchのreleaseは取得したassetを収集し、Python等はそのsource／artifact identityを自分の固定経路へ反映する。取得経路の現checkout調査は各担当の返却を待つ |

fixtureの取得先が変わっても、VMのwire inline定数・command blockのcompileにProtocol npm packageは必須にならない。今の`npm run build`は3 tooling packageもroot workspacesの一部としてbuildするので、移管後はそのworkspace宣言とlock／CIを直す。

## 6. manifest／artifactとrollback

現在の固定workflow `.github/workflows/mc-remote-images.yml`は同じScratch release commitから全workspaceをbuildし、Scratch OCI、Bridge OCI、WireScope ZIP＋manifest、Scratch contracts archiveを収集する。

| manifest role | 現在の実体／移管時の材料 |
| --- | --- |
| `scratch` | GUI buildからのOCI。Scratch ownerのまま |
| `bridge` | `mc-remote/bridge/dist/main.js`とruntime lock依存を使ったOCI。新ownerのimage／digestを収集する経路に変える候補 |
| `wirescope` | browser `dist/index.html`／assets／LICENSE／NOTICEから作る`wirescope-app.zip`。common ownerが生成し、Scratchはcollectorにする候補 |
| `wirescope-manifest` | ZIP digest、assetごとのbytes／digest、source repo／commit／subdirectory、build toolchainとlock digest、observer関連protocolを含むdetached JSON |
| `contracts` | `packages/scratch-gui/contracts`の`contracts.tar.gz`。Scratch product/runtime configの契約なのでScratch側に残す |

WireScopeのartifact generatorにはsource repository=`https://github.com/Naohiro2g/scratch-editor`とsubdirectory=`mc-remote/live`の固定があり、移管後のsourceを正しく表示するように変更する必要がある。package lock／repo URL／source commitが変わればdetached manifestのdigestも変わる。Bridge OCIもsource metadataを変える場合は同じdigestとは限らない。fixture全12件のbyte一致とは区別して、何をartifact一致の対象とするかをcoordinatorへ返す。

b9の列幅や未知event修正はそもそもWireScope app bytesを変える。移管の前後比較は、機能修正だけの差分とowner移動だけの差分を分け、移管前の同じ機能版を基準に行う案。b8のfixture12件はそのままbyte一致を別に検査する。

rollbackのsource起点は公開b8 `691576f60b7f0824e1753bd6823901d01fbe2422`。Scratch source・root workspace／lock・fixture path・CI／artifact recipeをそのtagへ戻せば新ownerへの取得依存を外せる。既存のb8 Release assets／OCI digestを保持し、deploymentはcoordinator／Stackの経路で旧setへ戻す。新ownerのhistoryや旧公開tagを消す操作は要らない。fixture byte一致の検証に本票のbaseline JSON／再現scriptを使える。

## 7. 契約2件とshared fixture

| 対象 | 現状 | 変更案 |
| --- | --- | --- |
| Scratch `chat.post` | `postToChat`→`_commandRequest`はid付き応答を待ち、resultを捨てる。`null`で壊れないことをprobeで確認 | null応答のconsumer testを足す。wire送信は変更不要 |
| protocol mirror | `ChatPostParams`はあるが`ChatPostResult = null`はない | 批准済みnull resultの型／owner testを加える |
| WireScope `chat.post` | 専用result branchがなく、`jsonScalar`でnullもtrueも受ける | null専用検証へ揃える。scalar値を受ける現在の挙動を新契約適合とは主張しない |
| Scratchの未知event | `event.js:eventDto`がthrowし、`_pollEvents`はcursor更新前にpollerを止める | 未知eventは共通fieldと順序を検査した上で省略する案。`through_sequence`とserver loss counterはそのまま採用し、未知だけのbatchでもcursorを進める。既知eventの不正は引き続き検査する |
| WireScopeの未知event | `observer.ts:parseEvent`がthrowしてsnapshot全体を拒否。`frame-filter.ts`の`other`分類は現在UIでは到達不能扱い | 共通fieldだけのopaque summaryを保持する案。未知追加payloadを無検査で表示せず、`other`の分類／表示を有効にする。cursor／lossはそのまま見せる |

共有fixtureを追加する実装は可能。候補caseは、id付きchatのnull成功・非null拒否（observer側）、既知／未知／既知の混在、未知だけのbatch、未知が最後で`through_sequence`が進むbatch、loss counter非零の保持、不正な既知event・順序・cursor境界の拒否。未知typeでpollを失敗させないことと、不正な既知DTOを黙認することを混ぜない。

公開b8の12 fixtureは移管の比較起点として保存し、新契約のcaseは追加fixtureへ置く案。file名・schema・case ID・発行するownerは移管の実行範囲が決まってから固定する。本票では既存fixtureを変更せず、successorも発行していない。

## 8. UI／README／park

| 項目 | 状態 |
| --- | --- |
| WireScope列幅 | `01cdb0bfee`。human ownerが実browserで確認しb9へ送った。timestamp／送受信状態の幅を縮める表示変更で、そのままb9へ入れる材料がある。新candidateのbrowser確認は未実施 |
| b7是正①空poll | `76f9e7d638`で空pollが有用な保持履歴を押し出さないよう修正し、公開b8へ入った |
| b7是正②数値欄Ctrl+C | `df34849d25`でネイティブな編集ショートカットを通し、公開b8へ入った |
| b7是正③backpressure案内 | `b407ca9cfb`でserver由来とlocal delivery停止を分けた。GUIはserver由来に専用案内を選び、報告対象のlightning経路はsocketを維持して後続retryできる。既存VM／GUI testとb8記録あり |
| post-b7表示park2件 | 時刻・handshake配置とMcRemoteカード説明はb8へ入った |
| picker alias | 未実装。現行検索対象はID・ja・enだけ。alias候補の確定・実装・testが残る |
| 名前データの場所とschema | `packages/scratch-gui/src/lib/mcremote-block-names/{1.21.11,26.2}.json`。完全修飾ID→`{en, ja}`。件数1,154／1,184。`sources.json`に公式元URL／digestとenのJAR内path。開発時だけ最小名称を抽出し、通常buildやpickerは公式配信へアクセスしない |
| 一段／二段表示 | ja／ja-HiraはID＋日本語名を一段目、英語名を二段目で右寄せ。英語ではID＋英語名。60:40配置、state結果の文字拡大、default値の重複解消・省略はb8実装とhuman確認済み |
| 読み上げ | search label、native button/select、件数のaria-liveはある。候補の読み上げ・長い名前の扱いを人間のscreen readerで確認していない。選択中候補はclassによる表示で、追加のaria選択状態は現状ない |
| ErrorText周辺 | `⟦mcr-error:reason⟧`とis-error Boolean block、actionable通知は実装済み。ErrorTextの説明reporter、set commandをbranch可能なresultにする横断設計などは今回増やしていない |
| README | 入口・接続・保存・WireScope・公式APIリンクとブロック一覧ドラフトは整備済み。rootのfork説明／上流Noteの日英はhuman owner指定で維持。段階的作例・stable install/update/rollback案内はparkを維持。ブロック一覧はドラフトで、公開後のREADME URL切替とお知らせは別の反映作業 |

aliasは公式名称JSONを膨らませず、Scratch独自の小さい検索用辞書へ分ける案。例として`minecraft:crafting_table`の「クラフト台」や`minecraft:gold_block`の「きんブロック」など、human ownerが選んだ読み・呼び方だけを手で登録し、CURRENT catalogにあるIDの検索にだけ使う。公式言語ファイル全体を保存せず、公式名称由来と自作aliasを分けるので`2026-09-30-10`の最小保存方針を維持できる。例は提案であって採用済み一覧ではない。

## 9. 10/10に向けた見込みと判断材料

契約2件の自repo対応と追加fixtureは概算0.5〜1作業日。aliasとreceiver文言の局所変更は小さな候補で、移管のcritical pathと切り分けられる。共通monorepoへの切替・CI／release・Scratch consumer調整は別に概算2〜4作業日。分割repoやBridge置換／observer schemaの全面再設計まで同時に含めると、10/10の見込みは下がる。

現状で未決なのは、topology、既存park repoの利用／新設、Bridge owner、fixture／artifact取得方式、artifact一致の判定対象、各consumerの切替日程。10/6までに移管だけの小さい範囲が決まり、各担当のfixture取り込みが間に合うことが、10/10に向けた条件。外部registryの新しいpublishを前提にせず、固定Git SHAと生成物を使う案が現在の依存には合う。

予定する外部操作の材料: 採用repoのpark解除または新repo作成、source／owner test／12 fixtureの収容、workflow／権限／必要なregistry設定、正式な新owner artifact発行、Scratchのconsumer切替とrelease collector更新。いずれも今回未実行。他repo担当への作業指示、shared環境変更、live-humanの開始、tag／release公開はしない。

ナレッジへ渡す決定文案（採番なし）: 「Protocol projection・共有fixture、WireScope common app・固有fixture、Bridgeの現行transportを、Scratchから独立した共通TypeScript tooling monorepoのownerへ移す。Scratchは固有sourceとGUI／VMを残し、固定Git commitのfixtureと固定digestのWireScope生成物を消費する。package／release versionを同一repoという理由だけで同期させない。公開b8の12 fixtureをbyte一致で保持し、旧owner sourceをScratchから撤去する。Bridge一般化・source_kind再設計・npm公開は別の判断とする。rollbackは公開b8 sourceと既存setを保持する」。これは批准済み決定ではなく、比較結果に基づく提案。
