# Python stable公開の観測素材（収容用sanitized版）

- 対象repo: Naohiro2g/minecraft-remote-api。
- close依頼の実読commit: `867adb7ed8d621d72ff97bc39c2b2e8514a79688`。
- class: 公開時のprovider／配布物照合。新規の実機・live-human試験は無し。

## 時系列

1. 2026-10-22T00:17:42.280757+00:00に、公開indexの旧既定stableが1214.10.13であること、旧版とrc1のfile情報を観測した。版を指定しない新規導入の移行前を示す記録として残す。
2. 公開前の既定branchはc301053、candidateはfac0313。人間の公開承認ゲートと、承認回避不可を確認した。
3. 既定branchを`fac0313ea9162dc0730412c53d665e6c42a93791`へfast-forward。tag v2321.0.0も同SHA。Release ID 430008193を2026-10-31T15:10:17Zにstable/Latestとして公開した。
4. main CI 41213013218、artifact 13045859840を公開前に凍結値へ照合。公開run 41213563824のpromoteも、このCI runを使用した。Release時の再buildは無し。
5. 2026-10-31T15:12:41.460481+00:00に、公開asset 3件を実際に取得し、bytes／SHA-256を凍結値とprovider digestに照合した。全件一致。GitHubのLatestも一致。公開本文にはprotocol 23.2.1、rc1とAPI／通信が同じこと、移行の案内、WireScopeの起動・終了の注意を載せた。
6. 同観測時点では予行用indexの公開は成功、正式indexの公開jobは人間の承認待ち。この待機状態は当時の事実として残す。
7. close依頼のknowledge gate notesは、その後human ownerが承認し、正式indexへの公開が成功したと記録している。coordinatorは配布物の実取得・非yanked・無指定解決を確認済み。解決確認はcoordinatorの観測であり、今回新規実行した試験ではない。
8. close分類時の追加GETでも、run 41213563824の全job成功、既定branchとtagとLatest、正式indexの版別file metadataの一致・非yankedを確認した。新しい実機試験・公開操作は行っていない。

## 正式記録への収容案

- 記録名案: `14-evidence/records/2026-11-01-stable-python-publication_ja.md`。横断stable公開recordへまとめてもよい。
- 添付先案: `14-evidence/artifacts/2026-11-01-stable-gate-close/python/`。
- 3つのJSON、sanitized版の確認票／候補票／公開返却票と本書（計7 files）をそのまま移す。元資料のpath、bytes、SHA-256はJSONのsource_materialsで追跡可能。
- 個別の接続コード、認証秘密、非公開接続情報、player UUID、利用者設定、hostname文字列は収容用4 filesへ含めていない。
- 今回のclose分類で横断gateの合否やcloseを宣言しない。正式authoringと全文収容確認はknowledge coordinatorが行う。
