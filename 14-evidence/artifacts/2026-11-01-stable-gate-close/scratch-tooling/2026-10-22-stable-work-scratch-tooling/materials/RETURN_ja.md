# Release gate 確認票 — 初回stable候補の返却（Scratch／tooling）

- 対象 repo: Naohiro2g/scratch-editor、Naohiro2g/minecraft-remote-tooling
- 対象 branch/commit: Scratch `agent/stable-scratch-2321@ffb496ed50d751d307f685f2ae555c94c893fae5`（push済み）。tooling `main@6447f6e8cbfbeeb9d229990b5c4f6e82a5875666`（rc1据置）。
- release / channel: artifact 2321.0.0、protocol23.2.1、stable候補（未公開）。
- gate coordinator: knowledge担当session（Claude Code）
- human release owner: プロジェクトオーナー
- current phase: 候補作成・独立照合完了、coordinatorの凍結／判定待ち。横断GREEN等の最終判定はしていない。
- contract maturity / required test tier: API凍結済み。依頼された最小配布対応、unit/deterministic、Linux packaged smoke。rc1のlive-humanは指示の範囲で再利用を求める。
- knowledge contract path: `00-hub/stable-gate-work-instructions_ja.md` 共通／Scratch。`00-hub/release-gate-notes_ja.md`、決定2026-10-22-01〜-06。
- knowledge contract commit: `abf8130faf8637fe1167af35477ea97bca43c42a`（latest remote mainからruntimeを実読。改訂前b3887126の依頼とも照合）。
- gate manifest identity: 未採番。この候補のidentityはIDENTITY.json。新exact setの確定はcoordinatorが行う。
- change cone: rc1 tag ec79b3b0e364e722d6926a0932eb4bf088ddd3a1基点。client版表示、配布guard2か所、その回帰test、既存VMテストの版期待値3件、案内へのLANリンク1つ、stableの一覧snapshotと入口。本家追従、protocol/wire、runtime動作、依存、tooling lockは変えていない。
- reused PASS / rationale: rc1の3 OS live-human記録 `14-evidence/records/2026-10-19-rc1-candidate-3os-live-human_ja.md` を、変更していない動作の根拠として再利用する範囲を返す。旧exact set／ZIP hashを新しいstableの値として流用しない。
- exact compatibility set / freeze status: stable全体は未凍結。候補Actions artifactの全体digestと内側全9 assetを独立照合済み。toolingの入力はrc1のまま。
- target deployment / profile / lock: LAN3 OS、Scratch OCI2 architecture、ブロック一覧。Stackのshared環境・order・DNS・TLSは変更していない。
- authorized next action: この票と候補の収集／coordinator照合。tag、Release、registry tag、公開siteの更新は公開指示後。配布対応のdevelop統合も公開後。
- test class: unit/deterministic、候補workflowのLinux loopback実行。新規live-human／実MC操作はしていない。
- 実行した command / 手順: 下記の検証、候補workflow run39744827621、verify-candidate.py、公開manifest関数による未公開草稿の検証。
- 結果: 候補workflow success。外側artifactのbytes／SHA-256、内側9 asset、ZIP3つのsource／版／dirty／同梱source hash／案内、OCI全blobと両architectureのlabel／revision／createdを照合済み。
- evidence record / artifact: このpacketのmaterials、上記knowledgeのrc1正式記録。packet自体は正式evidenceではない。
- 未検証の境界: 新しいWindows／macOS実機試験、公開後の匿名取得とLatest、Web二組の実運用、箱庭の切替は未実施。一般CIに既知GUIテスト1件が残る（下記）。全CI成功とはしていない。
- security / compatibility / rollback の確認: commit／dirty／bytes／OS／arch検証を維持。23.2.1のAPI・wireと全lockを維持。旧rc1 tag／配布物は保持。SOURCE_DATE_EPOCHはsource commitの時刻。凍結後のCLI直接転送ならmetadataとmtimeを保持でき、再buildを前提にしない。
- 判定を求める事項: (1)一般CIの既知GUIテスト失敗の扱い (2)tooling provenanceの歴史的rc1ブランチ名を保持して同じdigestへstable tagを追加する案 (3)新candidate identityのexact setへの採用。こちらで最終判定しない。

## 候補の取得identity

- source: `ffb496ed50d751d307f685f2ae555c94c893fae5`
- branch: `agent/stable-scratch-2321`
- run: https://github.com/Naohiro2g/scratch-editor/actions/runs/39744827621
- artifact ID: `12410683112`
- artifact全体: 1370347310 bytes／`sha256:9f0a148a286c8bc3528f1b0e4f948f2d5b9d0da141ac9d393e610e3615d81a6c`
- 最初の試行run39723278534／artifact12402247154はsuperseded。返却setには使わない。

| file | bytes | SHA-256 |
| --- | ---: | --- |
| `scratch-gui.tar.gz` | 138834579 | `fa4a1939843a83b453d882dda54ad2713ff3d53f0e1a16458e0bfc731947947a` |
| `scratch.oci.tar` | 325819392 | `373effd2c5da766d64077b1bcf1a70f258d59970ee5dacb15fc51b8d9bcdd491` |
| `bridge.oci.tar` | 114626048 | `3982876466fb860dca250438d73e18e441a2a85d67d9f149f537a7a8d1a1c44c` |
| `wirescope-app.zip` | 83854 | `da3da0b6cf4d05265bc0c11abaa4913208c7cfc3600b0c3e78c93a356fc431ad` |
| `wirescope-app.manifest.json` | 2339 | `3dd668a236463809a4cdc6d19375f3e6d75eea0c8089a616d2b761d3a4a05235` |
| `contracts.tar.gz` | 1908 | `48948ba47d55409f02a8ff8e0d44021b07859e11ffa5ca0f8598e6ef06082390` |
| `mc-remote-scratch-LAN-2321.0.0-windows-x64.zip` | 261870138 | `262f67442e9699a06afb39d2259fda7f429a1a16524539e2ba51b52ceddd9525` |
| `mc-remote-scratch-LAN-2321.0.0-macos-arm64.zip` | 266221800 | `8cacff36c64adf8a9a6570e76db564bc81a54d1ace180e0042dbd1836f77b92f` |
| `mc-remote-scratch-LAN-2321.0.0-linux-x64.zip` | 271477855 | `e3361bf69036417c8f9d03db7087d00b46e680f0f0fca1360994f16cbadba581` |

## OCI

- Scratch index: `sha256:d85e37291ef75e4d64ab7f0c52b9a496889205071d3afc51b796dbcc1161903c`
- version label: 両architectureとも `v2321.0.0`
- revision: 両architectureとも `ffb496ed50d751d307f685f2ae555c94c893fae5`
- SOURCE_DATE_EPOCH: `1792656135`。createdは両architectureとも `2026-10-22T08:02:15Z`（commit時刻と一致）。
- amd64／arm64のmanifest／config digestはcandidate-verification.json。
- COPY layerのmtimeを別build間で揃える実装は追加していない。公開時は凍結したこのOCIをCLIで直接転送する。

## ブロック一覧

- `site/2321.0.0/`と入口を更新。既存b9／b10／rc1のsnapshotを保持。
- 56 block＋2例。入口と版別の対応62 fileは同じbytes。block data、SVG58 fileはrc1と同一。
- archive `scratch-block-reference-2321.0.0.tar.gz`: 247864 bytes／`76eda18e7fd92ebd3366eff7c01104bca7bb8143b44c19c88db70fbac28ee708`。
- archiveはこのpacketに同梱。全fileのbytes／SHA-256はblock-reference-identity.json。
- generator sourceは `d3aa547ccfdfa00e7164d89df72cfc29cde497eb`。最終候補sourceまでの差分は一覧の追加と版期待値のテストだけで、generatorが読むVM/src等の差分は0。sourceCommitの意味を維持した。

## 回帰・既存検証

- 配布guardのstable受入れ2件は修正前FAIL、修正後の関連16 test PASS、skip0。
- VMの版期待値は修正前531 PASS／3 FAIL、修正後534 PASS。一般CIのVM workspaceもsuccess。
- runtime config／WireScope handoffのGUI unit45 PASS。
- 全workspace production build、Local／manifest／変更file lint、git diff --check PASS。
- 候補workflowはowner側で配布／contract検証、全build、3 ZIP、Linux packaged smoke、OCI生成を実施してsuccess。
- 一般CI run39744780763はBuildとVMを含む7 packageがsuccess。GUIはunit538 PASS／skip1、integration126 PASS／1 FAIL／skip7。失敗は既存menu-bar.test.jsのNoSuchAlertError。GUI本体と当該テストはrc1から差分0。今回は最小scopeを越えて修正せず、判定用に分離して返す。

## toolingとWeb名

- toolingの3 fileは上表のrc1固定値と同一。WireScopeのpath／manifest／収録内容にrc1表記無し。
- Bridge version labelはsha-6447…で、provenanceに生成時のagent/rc1-protocol-2321だけが残る。履歴を改変せず、公開時に同じdigestへv2321.0.0 tagを追加する案。
- Web名の詳細はWEB_NAMES_ja.md。実体の走査結果はcandidate-hostname-scan.json、tooling-reuse-scan.json等。
- Scratch JSには既定値sb.mc-remote.comがあるがruntime configで上書き。Bridgeにもscratch／sbの既定値があるがenvで上書き。WireScopeのbeta名固定値は無い。Webの二組を理由にしたartifact変更は不要。
- 二組の対応はruntime configのwirescope_url、Bridgeのorigin／sandbox allowlist、Caddyの経路とhandoff headerで決める。コードがstable／betaの組を自動推測するわけではない。
- Scratch／toolingのREADME・文書・作例のbetaリンクは0件。sb-betaはScratchのテスト2 fileに6件だけ。置換の持越しは無い。
- 新Web名を現rc1へ先行追加するshared作業はStack §3の担当。こちらでは実施していない。11月1日前の公開誘導も追加していない。
- 11月1日のsb／sb-retro切替と11月中のsb-beta併存は改訂後の指示を採用。旧確認票の「11月はsbが旧protocol」は使わない。

## 公開前の状態

- tag／Release／registry tag／公開site／shared環境は今回変更していない。
- manifest.stable-draft.jsonは未公開草稿。schema v2／semantics／実fileの検証を通した8 artifactの公開metadata案。
- 公開本文草稿はscratch-release-notes-draft_ja.md、tooling-release-notes-draft_ja.md。
- 大容量の候補はowner Actionsの上記ID／digestから取得可能。ローカル取得先は/tmp/codex-stable-work-20261022/candidate/。このpacketは小さいidentity／検証素材と一覧archiveを保持する。
- 公開許可後はtoolingを先に、続いてScratch。Scratchのrelease:published再buildを避ける手順を確定し、凍結物を直接昇格して照合する。
