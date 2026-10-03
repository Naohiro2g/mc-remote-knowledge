## ② Release gate 確認票

- 対象 repo: `Naohiro2g/scratch-editor`（Scratch VM／GUI、Protocol、WireScope、Bridge）。
- 対象 branch/commit: `agent/b8-compatibility@5aaa9c59acc393cd0a0de5cb45a5e619a5e87abe`＋学習者ブロック／pickerの未commit差分。shared fixture発行は`agent/b8-owner-fixture@0735a9c957d069f719bee9c91e8be0f9322f4920`。両remote branchを`git ls-remote origin`で照合。
- release / channel: `2320.0.0b8`／prerelease候補。公開は未実施。
- gate coordinator: 依頼元knowledge coordinator。指定SHAのb8節に担当identityがないため、正式なb8記録との照合は未完。
- human release owner: 依頼元のhuman owner。指定SHAのb8節での照合は未完。
- current phase: 自repoの事実確認・返却。依頼本文ではb8 gate開始、指定SHAの`release-gate-notes_ja.md`には2026-09-30 b8節が無い。参照SHAの差分をcoordinatorへ返す。
- contract maturity / required test tier: wire §5.8.3／§5.0.2を実際に読んだ。今回実施はunit/deterministic（Tier 0／1）。Tier 2／3の実施範囲・exact setはcoordinator未提示。fixture／sound／sourceの不足を残すため、B8全contract適合は主張しない。
- knowledge contract path: `00-hub/release-gate-notes_ja.md`（確認票書式）、`10-protocol/wire-format-design_ja.md` §5.0.2／§5.8.3、`10-protocol/block-value-design_ja.md` §8、`13-scratch-client/scratch-block-value-projection-design_ja.md` §7、`14-evidence/beta-verification-design_ja.md`。
- knowledge contract commit: 上記は実読SHA `2d0830a741997573248ee94e945c719316a0c299`。①の着地とbootstrap／INDEX／roadmap／tag設計／DEC 2026-09-30-08は実読SHA `16668c5e5152d593c4b184939c9a9e723529d6e9`。指定gate SHAを別SHAへ自動代用していない。
- gate manifest identity: 未提示。B8の公開manifest／artifactは本repoで未生成。
- change cone: protocol 23.2.0の型・method・reason mirror、B8 entity／particle shared fixture、独立WireScope validator／filter、VM hello／診断版。追加の未commit差分はentity／particle learner block、catalog ID一覧、GUI案内、block名辞書とpicker表示・検索。Bridge／release workflow／auth／transportを今回は変更していない。
- reused PASS / rationale: GUI names追加後の全70 suites／512 tests（1 skipped）、VM／GUI build・lintを既存局所確認として参照。最終の表示調整後はGUI関連4 suites／29 tests、lint、i18n:src、build:devを確認済み。Protocol／WireScope／VMは本棚卸しで再実行。これらはexact setに固定された横断PASSではなく、未実装sound／source欠落のPASSにも流用しない。
- exact compatibility set / freeze status: 未提示／未凍結。source baseはpush済みだが、ID一覧・learner block・pickerは未commitで候補identity未固定。
- target deployment / profile / lock: 今回は指定無し、接続していない。shared環境の接続先・現行状態を推測しない。
- authorized next action: 自repoのread-only棚卸し、unit/deterministic、①のNOTES更新と移管済み素材cleanup、確認票の返却。shared変更・他repoへの着手・人間参加試験は開始していない。
- test class: `unit/deterministic`。local Chromiumの表示用catalogによるDOM／click／type／screenshot確認はdeterministicの補助で、実plugin live-auto／live-humanではない。
- 実行した command / 手順:
  - `npm test --workspace=@mc-remote/protocol`：lint＋35/35 PASS。
  - `npm test --workspace=@mc-remote/live`：lint＋137/137 PASS。
  - `node packages/scratch-vm/test/unit/extension_mcremote.js`：119 subtests／485 assertions PASS。
  - `node handoff-materials/2026-09-30-b8-gate-confirmation/materials/observation-gap-check.mjs`：validatorとScratch sourceを直接呼び、下記の欠落を再現。
  - fixtureの`wc -c`／`sha256sum`、`git ls-remote origin`、source／workflow／NOTESの照合、`git diff --check`。
  - 既存実行：GUIでpicker／names／block-ref／l10nの4 suites／29 tests、対象lint、`npm run i18n:src`、`npm run build:dev`。browser smokeはgold／door、日英AND検索、ID適用、Mojang追加通信0を確認。
- 結果: 自repoの状況は以下のとおり。横断GREEN／HOLD／REDは判定しない。

| 項目 | 自repoの事実・根拠 |
| --- | --- |
| README人間向け再編 | `49e254a3b0699746aed5ea786fdfc67e6eb2d1d4`、`d311c222923abed6de5a7e3e7c934f4dc31b2761`、`bbef2810dc38e2766a4c6c34b15e0bf0e12ac58a`等で入口・接続・保存・WireScope・upstreamへの導線を再編済み。全track完了ではない。rootのMcRemote追記に日英並記が残り、Pass Bの段階的作例・学習path、Pass Cの生成API referenceとstable install／update／rollback固定が未完。cold-reader検証は今回自repoで再実施していない |
| browser操作範囲 | 内蔵Browser skillを読みbootstrapを再試行したが`privileged native pipe bridge is not available; browser-client is not trusted`で接続不可。独立したheadless Chromiumではlocalhost到達、DOM取得、click／type、screenshot・画像確認が実測PASS。利用中のin-app tabやMinecraftクライアントの直接操作、b8 live-humanの同一browserでのWireScope attachは未確認 |
| B8 shared fixture | `mc-remote/protocol/test/fixtures/entity-particle-v23.2.json`。発行commit `0735a9c957d069f719bee9c91e8be0f9322f4920`、20,967 bytes、SHA-256 `09c1565bf81d33c92d6282e6e20d926559168cb9d780c07d30ad2f9f5895640e`、59 unique cases（nearby 19、handle transaction 7、entity lifecycle 7、particle 26）。schema `mcremote.entity-particle.v23.2`。soundケースは無し。resource各種の無印・完全修飾・非正準形を網羅する新fixtureは未発行。既存block／dimension fixtureの一部だけで全種網羅とはしない |
| protocol mirror／WireScope | `5aaa9c59...`でwire定数23.2.0、entity 4method、ParticleSpec、particle_data_unsupportedと既存reasonをmirrorし、独立WireScopeのmethod／params／result／typed particle FAST対応を追加。package.jsonのprivate package版は0.1.0のまま。wireのplaySound／playBlockSoundとunknown_soundはmirror／validator／method認識へ未追加 |
| Scratch sanitizer | GUI `mcremote-wirescope-source.js`のsource allowlistがB8 entity 4methodを含まず、typed particleとparticle FAST通知も落とす。独立WireScopeが受理するrequestでもsourceが0 frameへ投影することを今回のprobeで再現。Scratch source E2Eは未完 |
| resource IDの無印 | VMはblock／entity／particle／dimensionを入力の無印のまま送る。blockのstate型解決だけは内部catalog lookup時にminecraft:を補うが、wire block_idは入力のまま。sound送信ブロックは未実装。独立WireScopeとScratch sourceはblock／dimensionの無印を受けるが、particle／entityは完全修飾しか受けず、無印の拒否／dropをprobeで再現。DEC 2026-09-30-06への追従が未完 |
| catalog ID一覧ブロック | `catalogToList`は実装・unit・ユーザーの表示了承済み。CURRENT・取得待ち・完全修飾ID辞書順・追加RPCなし・一括置換・失敗時保持。未commitで、5aaa9c59自体には未収録。b8への採用判断は受領済み |
| pickerの名前・検索 | 表示済み：日本語／ja-Hiraは`gold_block 金ブロック`と下段右寄せ`Block of Gold`。区切り線と件数を追加。GUI `src/lib/mcremote-block-names/<mcVersion>.json`へ、1.21.11の1,154件と26.2の1,184件を同梱。exact shapeはcanonical IDをキーに`{en,ja}`、例`{"minecraft:gold_block":{"en":"Block of Gold","ja":"金ブロック"}}`。公式manifestから英語はclient JAR内`assets/minecraft/lang/en_us.json`、日本語はasset index経由`ja_jp.json`を読み、元ファイルのSHA-1を照合して開発時に抽出。URL／hashはsources.json。JARと全言語ファイルは保存・同梱しない。build／picker利用時の取得も無し。検索はID・日本語名・英語名のNFKC／小文字化＋空白AND。登録alias／ひらがな読み辞書は未追加。CURRENT catalogの候補だけを使い、版完全一致で名前を参照、不明版／IDはID表示。wire／catalogHash／保存値は変更なし。実装は未commit |
| Scratch runtime／learner block | b8で変える。hello 23.2.0／診断2320.0.0b8はpush済み。未commitで9 block（nearby・entity snapshot／pose・remove、receiver／dust／block ParticleSpec）＋catalogToListを追加し、既存particle blockはobject入力に対応。GUI案内・翻訳とpickerも変更。soundのlearner blockは未実装 |
| b7後の是正3件 | ①空events.pollはVMの100-frame保持windowを使ったまま。既存の表示filter／点滅抑止は保持枠の是正ではない。②数値入力欄Ctrl+Cの是正commit・再検証なし。③server backpressureがGUIのtransport停止案内へ合流したまま。3件とも未完 |
| post-b7 park 2件 | 時刻列HH:mm:ss／詳細tooltipとhandshake上部折り畳み配置は未着手（observed_atは既存schemaにあるが表に時刻を出していない）。McRemote拡張カードもfull lightningの長い副作用一覧が残り、短文化／近接ヘルプへの移設は未着手 |
| 10/3見込み | entity／particleの局所実装とID一覧・pickerは進んでいるが、最新B8 scopeのsound／resource fixture、Scratch source、既知是正、commit／push／candidate artifact固定が残る。shared liveとexact setは未実施で、現時点で10/3 release可とは返せない。参照gate SHAの差分も返す。長い日本語名の幅・文字サイズはユーザーと合意どおり実動作確認で微調整する |

### 移管準備：repo内の依存とRelease manifest

| 所有面 | import／配送の現状 |
| --- | --- |
| Protocol | `@mc-remote/protocol`はdependency-free leaf。型・定数とshared JSON fixtureを所有。fixtureはsource treeにあり、package filesはdistのみ。b8でowner移管は始めていない |
| Scratch VM | production codeはProtocol packageをimportせずinline mirror。Tap testsが`../../../../mc-remote/protocol/test/fixtures/*.json`をCommonJS requireする（block-value、spawn、dimension、events、sign、direction-lightning、entity-particle） |
| WireScope | productionは自packageのobserver／session／adapter／typesをimportし、Protocol packageをimportしない。Vitestは`../../protocol/test/fixtures/*.json`をfilesystemで読む。固有observer lifecycle／station等fixtureはlive/test/fixturesで所有 |
| Scratch GUI source | `mcremote-wirescope-source.js`はGUI内の手書きallowlistでsnapshot／handoffを生成。live／protocol packageのruntime import無し。GUI testsはprotocol JSON fixtureを相対import。ここのB8更新が不足 |
| Bridge | runtime依存はws。Protocol／WireScope／VMをimportせず、payload透過のwss⇄TCP transport。今回差分無し |
| manifestのwirescope | `.github/workflows/mc-remote-images.yml`がrole wirescope／kind https-file／file wirescope-app.zip／sha256を出す。ZIPはbuild済みのbrowser app assetsとlicense／対応source案内で、Protocol packageやshared API fixtureの配送ではない |
| manifestのwirescope-manifest | role wirescope-manifest／kind https-file／file wirescope-app.manifest.json／sha256。detached manifestはschema mcremote.wirescope.app-manifest v1、archive hash、source commit／repo／subdirectory、build input identity／toolchain、observer v1／session v1／handoff v1／station v1、asset bytes／hash、AGPL licenseを持つ |
| manifestのcontracts | role contracts／kind https-file／file contracts.tar.gz／sha256。内容は`packages/scratch-gui/contracts/`のproduct-config／runtime-config schemaとfixtures。固定順・mtime・owner・mode、gzip timestamp無しで生成する。B8 protocol shared fixtureを含むtarではない |

- evidence record / artifact: 正式なknowledge record／artifactは未作成。本票とsame-directoryのunit logs、observation-gap-check.mjs／.jsonはgit管理外の搬送素材。code＋command＋source identityを根拠とするが、未commit差分のexact evidenceは未固定。pickerのbrowser素材は`../../2026-09-30-block-picker-names/materials/`を参照。
- 未検証の境界: 最新B8全contract適合、sound、各resource種別のconformance、Scratch sourceのB8 E2E、実plugin、candidate artifactのclean buildと公開identity、shared live-auto／live-human、同じWireScope artifactの横断real-browser attach、rollback。
- security / compatibility / rollback の確認: Bridge透過性・authを今回変更していない。source sanitizerは未対応frameを落とすのでB8観測互換が未完。secretの外部送信やshared変更は実施していない。b8 rollbackの実環境確認は未実施。
- 判定を求める事項: b8 gate節を含むpush済みknowledge SHAの提示、sound／resource fixtureとScratch source不足のgate上の扱い、既知是正・park 2件とREADME残件のb8範囲、残件を閉じた後のexact set／artifact／live指示。自repo担当は最終release判定をしない。
