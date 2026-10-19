# rc1候補の3 OS試験（2026-10-18〜19）

> test class: `live-human`。実施票`00-hub/rc1-gate-live-test-instructions_ja.md`（2026-10-19にOS別へ書き直した版）による。
> human ownerが送った画面、log、文字をcoordinatorが要約した。経過の詳細は`00-hub/release-gate-notes_ja.md` rc1の「試験」。
> token、ペアコード、attach code、IPアドレス、ホスト名、player名とUUID、WireScopeの表示ID、アカウント名、機器の識別番号は
> 収録しない。素材はGit外。coordinatorが進行を案内しながら行った。

## identity

- 凍結`rc1-integrated-artifact-set-1`（2026-10-18）。候補はリリースの前に
  `https://mc-remote.com/candidates/2321.0.0rc1/set-1/`へ置き、coordinatorが外からHTTPSで5 fileのbytesとSHA-256を凍結値と
  照合済み（`00-hub/release-gate-notes_ja.md` rc1、`2026-10-18-07`）
- 取得は3 OSともChromeでmc-remote.comから。Windows ZIPは261,848,009 bytes（凍結値と一致）
- Scratch LANパッケージ`2321.0.0rc1`（Scratch `ec79b3b`）、McRemote `mc-remote-2321.0.0rc1.jar`（`192a777`）、Python
  `minecraft_remote_api-2321.0.0rc1-py3-none-any.whl`（`c301053`）。比べる相手はb10の公開物（McRemote `2320.0.0b10`、Scratch LAN
  パッケージ`2320.0.0b10`）とPyPI.orgの`minecraft-remote-api==2320.0.0b9`
- McRemoteは全サーバーの起動logで`Enabling McRemote v2321.0.0rc1`（b10は`v2320.0.0b10`）、`Auth enforcement: true`、
  `Credential domain health: HEALTHY`。catalogはb10とrc1で同じ（26.3：blocks=1286、hash
  `3eaae42e9bcbd5e6ef6a2d1df702b25a878ca3157dcadc58ae29822fe5277663`。1.21.11：blocks=1166、hash
  `6d0f8524b70e37fb8d7b34d0fdb45c2b058dcfea82920d86ca9aaabb9fcadc83`）

| PC | OS | ブラウザ | 役割 | サーバー |
| --- | --- | --- | --- | --- |
| Windows | Windows 11 Pro 26H2（26300.9711）、Core i3-8145U、メモリ16 GB | Chrome 155.0.8059.85 | 1台構成 | Paper 26.3 build 203、Java 25.0.2（Oracle OpenJDK） |
| Ubuntu | Ubuntu 24.04（kernel 7.0.0-38） | Chrome 155.0.8059.84 | 1台構成、Macのサーバー役 | Paper 1.21.11 build 132、Java 21.0.2（Oracle OpenJDK） |
| macOS | macOS 26.7.1（25G241）、Mac mini M1、メモリ8 GB | Chrome 155.0.8059.85 | Mac → Ubuntu | なし |

## 結果

human ownerの判断（2026-10-19）：rc1は合格。PythonのWireScope（見つかったことの1）は注意書きで扱う。

| 項目 | 結果 |
| --- | --- |
| ダウンロード | mc-remote.comからChromeで、3 OSとも警告なし |
| b10からの更新（Windows、Linux） | `2321.0.0rc1/`を`2320.0.0b10/`の隣に置いて起動。b10の作品は一覧に残る。古い版を消す人は少ないと見る。隣に置くことは図解されていて理解されそう（human owner） |
| 新しく入れる（macOS） | `はじめに.html`の手順の順（警告を閉じる →「このまま開く」→ もう一度「このまま開く」→ パスワード）が実際と合った。設定画面のURLはリンクで、押すと開いているタブが表に来る。ホームページの`/lan/scratch/`とずれは無いと見る。ホームページのほうが整理されていて分かりやすい（human owner） |
| Scratch rc1 ↔ McRemote b10（26.3） | 送信23.2.1、受信23.2.0で止まらず、チャットとsetBlock |
| Scratch rc1 ↔ McRemote rc1（26.3、1.21.11） | チャット、setBlock、setBlocks、player.getPos／setPos／setDirection |
| Scratch b10 ↔ McRemote rc1（26.3） | 送信23.2.0、受信23.2.1で止まらず、チャットとsetBlocks |
| Python rc1 ↔ McRemote b10（1.21.11） | ペアリング、チャット、setBlock |
| Python b9 ↔ McRemote rc1（1.21.11） | チャット、setBlock。ペアリングは要らなかった（Python rc1でのペアリングが、McRemoteをrc1へ替えた後もb9から使えたと読める） |
| Python rc1の同梱WireScope | processを終わらせなければ、attach codeでつながり、helloが見える（下の1） |
| 26.3の名前 | 26.3のサーバーで「ポプラ」23件、「ポプラの原木」が出る。1.21.11のサーバーでは「ポプラ」0件で、26.3にしか無いブロックは出ない。語を並べた検索（「door iron」）も効く |

- Windows：rc1の初回は`settings.json`が無く、設定画面だけが開いた。既定の「このPC」で保存して進んだ。b10の起動では、残っていた
  設定（b10の試験のLAN構成）で設定画面の後にScratchが表に開き、「接続」はエラー。WireScope miniの「設定先」「実接続先」で
  原因がすぐ分かり、Scratchのタブを閉じて「このPC」にするとつながった。Scratchのタブが開いている間は「設定を保存する」が押せない。
  human owner：「ぼんやりと操作して間違えても、脱出は容易な感じ。良い。」
- session tokenは約2時間で失効し、時間がたった接続ではペアリングし直した（設計どおり）
- 設定画面の「改造版のScratchを開く」は、保存するまで押せない。設定画面に版（`mc-remote Scratch 2321.0.0rc1`）が出る。Scratchの
  製品noticeは版、「詳細はGitHub.comのリリースページへ。」、「リリースページを見る」「ホームページ」
- 独立のWireScopeは`http://127.0.0.1:8603`
- macOS：`HOME/mc-remote/`へ移してからの起動では、警告もアクセス権の確認も出ず、設定画面が裏、Scratchが表に開き、ペアリングなしで
  接続できた
- Ubuntuのサーバーでは、b10とrc1のどちらも起動logに「config supported_mc_versions differs from the bundled declaration; hello
  uses [1.21.11, 26.3]. The configured value is preserved.」（WARN）。helloは`[1.21.11, 26.3]`を返した

## 見つかったこと

1. Python `wirescope=True`：端末にattach codeは出るが、URLは出ない。ブラウザは裏で`127.0.0.1`の空いているportを開く。短い
   scriptではページが出る前にprocessが終わり、真っ白になる。終わらないようにする（`input()`）と、ページに「Python端末に表示された
   接続codeを入力してください。」と出て、つながる。それより前に終わったチャットとsetBlockは出ない。human owner：「うまく
   行ったり、真っ白だったりすると思うので、嫌な動作だね。」
2. Pythonの送信のhelloは`{"protocol":"23.2.1"}`だけ（Scratchはclientの名前と版も送る）
3. `はじめに.html`の中の「版番号のフォルダーではじめに.htmlを開き、start-mc-remote.commandをダブルクリックします。」は、すでに
   開いて読んでいる人に「開き」と言っている（macOS）
4. macOSの「このまま開く」は「プライバシーとセキュリティ」のかなり下にあり、スクロールが要る。最初の警告の窓のボタンは
   「ゴミ箱に入れる」「完了」（human owner「捨てる人はいないとは思う」）
5. macOSで「ダウンロード」の中のまま起動すると、「“ターミナル.app”から“ダウンロード”フォルダ内のファイルへのアクセス権を
   求められています」が追加で出る
6. mc-remoteのブロックへパレットの中で頭出しすると、位置が微妙に下にずれる。ブラウザの表示を拡大縮小すると直る（Linux、
   macOSのChrome 155）
7. 接続の接続先と状態の表示が詳細になれば、もっと良い（human owner。b10の見つかったことの8、9と同じ向き）
8. `settings.json`は版のフォルダーごとなので、b10をLAN構成で使っていた人は、rc1の初回で接続先を入れ直すことになる
9. b10から変わっていないこと：同梱のfileの更新日が1980/01/01（Linux、b10の4）。ランチャーの画面に`McRemote bridge listening on
   ws://127.0.0.1:8602`が2回目も出る（macOS、b10の4）。macOSの`.command`は既定のターミナルでなく標準の「ターミナル」で開く
   （b10の3）

## 試験の進め方

- 最初の実施票は場面（A〜D）別で、human ownerから「進め方が自由すぎてやりにくい」。OS別に番号の順で進める形へ書き直した
- 実施票の`uv init`は、uv 0.12.19では`src/<名前>/`のpackageの形を作り、階層が深くなった。`uv init --no-package`へ直した

## 主張しない範囲

PyPI.orgからの`2321.0.0rc1`の取得（承認の後）。公開VPSへの切り替え。初めて読む人の通し（Pass C。rc1では生徒の初学者を対象に
しない、`2026-10-19-01`）。macOSとUbuntuのZIPの
bytesの照合（試験ではWindowsだけ記録。置き場所のbytesはcoordinatorが照合済み）。Python b9 ↔ McRemote rc1でペアリングが
要らなかった理由（tokenの保存場所は確かめていない）。授業規模の同時接続。
