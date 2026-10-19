## Release gate 確認票 delta — Scratch / tooling

- knowledge contract path: `00-hub/rc1-gate-work-instructions_ja.md`。
- knowledge contract commit: `d0be94624659e82d5f91bac6eba48063cc1c3c7b`。
- release / channel: `2321.0.0rc1` / GitHub pre-release 候補。protocol `23.2.1`。API と wire の意味は変更していない。
- gate coordinator / human release owner: knowledge 記載の担当。Scratch 担当は exact set の凍結と横断判定を行わない。

### Tooling owner

- branch / commit: `Naohiro2g/minecraft-remote-tooling` `agent/rc1-protocol-2321@6447f6e8cbfbeeb9d229990b5c4f6e82a5875666`。draft PR #1。
- 新 fixture: `chat-event-compat-v23.2.1.json` 32384 bytes SHA-256 `eead244a7340c315cb63e1e77ede0fe9cf48162c06fedbeef36d941950d5000d`、`entity-particle-v23.2.1.json` 36483 bytes SHA-256 `0319ff8373a96798cf5e9e421a804729fd33a0fa53e96adc12c93ed7994777ae`。旧 v23.2 fixture は残している。
- owner CI: workflow_dispatch run `39053886890`、head SHA `6447f6e8cbfbeeb9d229990b5c4f6e82a5875666`、success。Actions artifact ID `12109060950`、digest `sha256:5b644de44ae2f9a2fb9de09d221c2930218f6c317baffee3b5c7f817309555fa`、114136814 bytes。
- WireScope ZIP: 83854 bytes SHA-256 `da3da0b6cf4d05265bc0c11abaa4913208c7cfc3600b0c3e78c93a356fc431ad`。detached manifest: 2339 bytes SHA-256 `3dd668a236463809a4cdc6d19375f3e6d75eea0c8089a616d2b761d3a4a05235`。
- Bridge OCI archive: 114626048 bytes SHA-256 `3982876466fb860dca250438d73e18e441a2a85d67d9f149f537a7a8d1a1c44c`、OCI digest `sha256:305d6e38b36e195a0e158522f32f3a8c45d39da2aeec7b7e46f785c920406acf`。candidate manifest: 972 bytes SHA-256 `05fafc241a73b831bfd74128610435af1472c46b056fc8be70c2851657038f3e`。
- test: `npm ci`、`npm test`（Protocol 127、Bridge 30、WireScope 144）、`npm run build` PASS。Scratch consumer は新 commit の fixture 15 件と artifact を検証取得済み。

### Scratch owner

- branch / commit: `Naohiro2g/scratch-editor` `agent/rc1-scratch-2321@ec79b3b0e364e722d6926a0932eb4bf088ddd3a1`。draft PR #26。
- VM: hello の protocol `23.2.1`、client 診断版 `2321.0.0rc1`。23.2.1 client が 23.2.0 server を受け入れる回帰 test を追加。
- tooling lock: 上記 exact owner commit / fixture / artifact に固定。b10 fixture は保持。
- LAN: 8601 / 8602 / 8603 の loopback 境界は維持。version を workflow / script で導出。`はじめに.html` 原稿を概略→OS別→接続に整理し、Mac の観測手順を反映。公式 `/lan/scratch/` 原稿と照合し、手順上の食い違いなし。設定画面 URL をリンク化。設定画面の画像は未追加。
- OCI: candidate と公開で `RELEASE_VERSION=v2321.0.0rc1` と source commit の `SOURCE_DATE_EPOCH` を揃え、provenance / SBOM を candidate にも追加。candidate と公開の OCI digest 同一性は未検証で、相違が出ても rc1 gate を止めない契約。
- 26.3: Mojang の公式言語 asset から 1275 件の block ID と en / ja 名を生成。`poplar_log ポプラの原木` の GUI 表示・検索を catalog 状態の test で確認。実際の 26.3 server 接続は未実施。
- ブロック一覧: b9 / b10 を維持。`site/2321.0.0rc1/` の 56 ブロックと例 2 件を build 済み editor から生成。release 後の knowledge 取り込み用で、公開サイトへは未反映。
- test: `npm run build` PASS。McRemote VM 対象 test 534 assertions PASS。GUI 名前・picker 対象 test 25 PASS。`npm run local:test` Node 23 + Python 11 PASS。release manifest 契約 94 PASS（ローカル Node 22 では Node 24 用 `--test-isolation` option を読めず、同じ test file を直接実行）。`npm run local:lint` / `npm run release-manifest:lint` PASS。block 画像 58 参照すべて解決。Linux の dirty local ZIP に対する起動・Bridge WS→TCP・終了 smoke PASS。
- candidate workflow: 初回 run `39060684619` は ZIP smoke の送信 protocol に旧 `23.2.0` が残ったため失敗。修正後、最終 run `39072595749`、head SHA `ec79b3b0e364e722d6926a0932eb4bf088ddd3a1`、success。Actions artifact ID `12116296168`、名前 `scratch-candidate-ec79b3b0e364e722d6926a0932eb4bf088ddd3a1`、1370212918 bytes、digest `sha256:259ca91e68616035a81deb49bb1060300138c85942597a2b11c7b7f5133d66e8`。
- Windows ZIP: `mc-remote-scratch-LAN-2321.0.0rc1-windows-x64.zip` 261848009 bytes、SHA-256 `86bbaf9a278683315ffe2ebd4f19d56ba53f5501289e4cddfc22f284d8d4e209`。
- macOS ZIP: `mc-remote-scratch-LAN-2321.0.0rc1-macos-arm64.zip` 266199673 bytes、SHA-256 `bdfff47b8c1210a359ed65a8be6fca26624546e3c04add125063968acc091412`。
- Linux ZIP: `mc-remote-scratch-LAN-2321.0.0rc1-linux-x64.zip` 271455727 bytes、SHA-256 `b76b574803c58403e38438d2569917bd72ca95f039026f12ed3a294edfcfba54`。CI で bundled Node 起動、HTTP GUI/config、WireScope、Bridge WS→23.2.0 stub、終了時ポート解放 PASS。3 OS の sidecar は最終 source commit / clean tree を記録。
- Scratch OCI archive: 325822464 bytes、SHA-256 `88d81fba1aca0194c85f638cf19c66a1a2087748f32ff501bdb1dd283ea1d0c5`、OCI digest `sha256:75e76edb6b8a1de4fb896184b5c26bed7cb1791296f82903e6b1ec4a1a5ab840`。
- その他: `scratch-gui.tar.gz` 138835708 bytes、SHA-256 `2dafb257c511989946da021591191cc1501e0d1a9211cc559373ed7de30f19c2`。`contracts.tar.gz` 1908 bytes、SHA-256 `48948ba47d55409f02a8ff8e0d44021b07859e11ffa5ca0f8598e6ef06082390`。`candidate-manifest.json` 2676 bytes、SHA-256 `a29b56239a060f95fe9c67f708023a14c64ac422bd108097586d544d201afbd2`。大きい artifact の一括取得はタイムアウトしたため、ZIP 内 manifest / sidecar を範囲取得して CI ログと照合した。各大容量 file 本体の SHA-256 は生成 workflow が記録した値で、再ダウンロードしての独立計算ではない。
- 未検証の境界: 3 OS での ZIP 取得・展開・起動・接続、人間参加の LAN 試験、26.3 live server、候補と公開の OCI digest 比較、shared deployment。
- GUI integration CI の `menu-bar.test.js` は、基準 develop の run `38525476758` でも同じ `NoSuchAlertError` で失敗する。rc1 head でも再現。待機追加を試したが改善せず、差分から取り消した。GUI unit 538 tests とその他の integration 126 tests は通過した。GUI 全体の green は主張しない。

### README 結果追補 — Scratch 節6（2026-10-18）

- knowledge contract path: `00-hub/rc1-gate-work-instructions_ja.md`、Scratch editor 節6。
- knowledge contract commit: `2a742bc4b24eb447f128ac757974671610a3532d`（今回実際に参照した remote main）。
- branch / commit: `agent/rc1-scratch-2321@f20e55eb53f192eab6cdc4f0d5aae4f52b2dc8db`。push 済み。GitHub API で commit の存在と変更ファイル `README_mc-remote.md` 1件を照合。
- `README_mc-remote.md`: 「自分のPCやLAN内」の段落の直前に `https://mc-remote.com/lan/scratch/` の案内を配置済み。
- `mc-remote/local/README.md`: 冒頭に同じ LAN 案内を配置済み。「公開済み配布物ではありません」を削除し、公開b10のOS別ZIPを取得できることと、rc1候補が検証中であることを記載済み（既存 candidate source `ec79b3b0e364e722d6926a0932eb4bf088ddd3a1` に含まれる）。
- API リンク: `README_mc-remote.md` の `/api/23.2.0/` が残っていたため、今回 `https://mc-remote.com/api/` へ修正。クライアントごとの版の資料を参照する説明は保持。
- 検証: LAN 案内の位置2件、旧公開状態表記の除去、API入口リンクを静的確認して PASS。`git diff --check` PASS。文書のみの変更のため build / runtime test は再実行していない。
- artifact 境界: 上記の既存 candidate run `39072595749` / artifact ID `12116296168` の source は `ec79b3b0e364e722d6926a0932eb4bf088ddd3a1`。README追補 commit からの candidate は未生成。既存 exact set の再利用可否は coordinator の判断へ返す。
