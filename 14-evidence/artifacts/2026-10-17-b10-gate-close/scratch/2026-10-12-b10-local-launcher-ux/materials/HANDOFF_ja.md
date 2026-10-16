## 確定搬送票

- 搬送元 repo: Naohiro2g/scratch-editor
- 搬送元 surface: Scratch Localの起動・設定ページ・ZIP内の配置
- 搬送元 branch/commit: agent/b10-scratch-local、HEAD ec29372dadac9c51b2812c746e72032d48d987b6に対する未コミット実装
- 作成日: 2026-10-12
- 種別: 局所決定
- 決定: 初回は設定ページでhost／portを保存して別タブのScratchを開く。設定済みならランチャーが設定ページとmc-remote拡張機能入りのScratchを順に開く。ScratchのURLは常に http://127.0.0.1:8601/editor/?extension=mcremote 。設定ページは開いているScratchを把握し、繰り返し押してもタブを増やさず再読み込みも行わない。接続先の変更はScratchのタブを閉じた後に行う。
- 決定: ZIP最上位にはstart-mc-remote.*、README_ja.md、NOTICE_ja.md、SOURCE_ja.mdを残し、その他はdata/へ収める。起動名とZIP名・manifest contractは維持。WindowsとmacOSはダブルクリック、Linuxはデスクトップ環境によるため端末からの実行を案内する。
- 理由: human ownerの要望「ブラウザで箱庭サーバーを開くのと変わりない難易度」、毎回の設定操作を除くこと、起動ファイルを他の実行物から見つけやすくすること。
- 却下案: 毎回設定ページで保存操作を要求すること。
- 影響: Scratch LocalのGUI起動導線とZIP内path。settings.jsonはdata/配下、identityのsource archiveはdata/source配下になる。Bridge、WireScope、protocol、共有fixtureは変更していない。通常のHTTP／WS loopback構成・browser credential保存originは維持。
- 根拠/検証: knowledge remote main f2eddd178f4c3760cfe280d2c570e266b14001b4のdev agent runtime、DEC 2026-10-07-04／2026-10-09-01、13-scratch-client/scratch-roadmap_ja.mdのURL入力境界を参照。npm run local:testはNode20件・Python9件PASS。npm run local:lint、git diff --check PASS。独立Chromiumの模擬editor／Bridgeによる初回設定、連打防止、未保存入力保持、tab close後の接続先変更、設定済み起動の確認PASS。Linux試作ZIPの日本語／空白path・固定BridgeのWS→模擬TCP hello・WireScope asset identity・正常終了・3 port解放PASS。
- 既に変更した実装/文書: mc-remote/localのlauncher、setup HTML／modules／tests、ZIP builderとarchive smoke、USER_GUIDE、README、NOTICE、AGENTS.md、local:test script。
- ナレッジ着地希望: Scratch spokeと必要に応じてenvironment-guideの起動導線・ZIP配置の補足。公開candidate固定に進む際、ZIP内配置・起動導線の変更と既存のOS観測の扱いはcoordinatorが判断する。
- 捕捉 cleanup: ローカルNOTESに未コミット状態・試作のidentity・未検証境界を捕捉。knowledge収容確認後にこの票を整理。
- 着地後の確認戻り先: scratch-editor担当。

### 未検証の境界

- 変更後のWindows／macOS ZIPの実機起動、OSによるブラウザのタブ順序・前面切り替えは未検証。前面切り替えはブラウザの制御に従う。
- Chromium確認は模擬editorであり、実際のScratch作品・Minecraft・pairing・live-human gateを実施したものではない。
- 初回の「Scratchを開く」はポップアップを開くため、ブロックされた場合は設定ページ内で許可が必要。
- 起動ファイルの移動は単体では不可。Windows shortcutは可。フォルダー全体の移動は可。
- 未コミットの試作ZIPはworking_tree_dirty=true。既存candidateの固定identityを置き換えず、公開・tag・Release・shared deploy・人間参加試験も行っていない。

### Linux試作（公開用identityではない）

- file: mc-remote-scratch-local-2320.0.0b10-linux-x64.zip
- bytes: 270173064
- SHA-256: 3bc05c7108466b751f7141d66e56b5e554a059fd661c01c73e0e44419d7be2f9
- working_tree_dirty: true
