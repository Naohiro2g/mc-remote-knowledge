パレットでカテゴリを選んだときの見出しのずれを修正し、ブロック選択画面でクリエイティブインベントリのカテゴリ名も検索できるようにしました。Scratch本家の更新も取り込んでいます。

- **パレットの頭出しを修正**：カテゴリを選んだとき、見出しが先頭からずれる問題を直しました。
- **ブロックのカテゴリ名で検索**：ID・日本語名・英語名に加え、「建築ブロック gold」や「Redstone Blocks」などでも絞り込めます。Minecraftの公式の日本語・英語のカテゴリ名に対応しています。
- **Scratch本家の更新を取り込み**：作品の読み込み・保存、SVG／コスチューム処理などの改善を取り込みました。

**推奨ブラウザーの下限が上がりました。** 本家への追従に伴い、Chrome／Edge 124以降、Firefox 125以降、Safari 17.4以降が推奨となります。iPhone／iPadでSafariを使う場合は、iOS／iPadOS 17.4以降をご確認ください。

protocolは**23.2.1のまま**で、APIと通信は**2321.0.0と同じ**です。

Web版は[マイクラリモコン改造版Scratch](https://scratch.mc-remote.com/)、通信の確認画面は[WireScope](https://wirescope.mc-remote.com/)です。

LANパッケージは、使うPCのOSに合うZIPを**1つ**ダウンロードしてください。Scratch、Bridge、WireScope、Node.jsを同梱しています。MinecraftサーバーにはMcRemoteプラグインを入れ、プレイヤーとしてワールドに参加しておきます。[サーバーの準備方法](https://github.com/Naohiro2g/McRemote#readme)も参照してください。

| OS | ダウンロードするZIP | 起動ファイル |
| --- | --- | --- |
| Windows 11、Intel／AMD 64ビット | [Windows x64版](https://github.com/Naohiro2g/scratch-editor/releases/download/v2321.1.0/mc-remote-scratch-LAN-2321.1.0-windows-x64.zip) | `start-mc-remote.cmd` |
| macOS、Apple Silicon | [macOS arm64版](https://github.com/Naohiro2g/scratch-editor/releases/download/v2321.1.0/mc-remote-scratch-LAN-2321.1.0-macos-arm64.zip) | `start-mc-remote.command` |
| Linux、Intel／AMD 64ビット | [Linux x64版](https://github.com/Naohiro2g/scratch-editor/releases/download/v2321.1.0/mc-remote-scratch-LAN-2321.1.0-linux-x64.zip) | `start-mc-remote.sh` |

**Windowsでは、ZIPを展開する前に**エクスプローラーでZIPを右クリックし、「プロパティ」→「全般」の「許可する」にチェックして「適用」を押してください。その後で展開します。

展開先の内側にある`mc-remote-scratch-LAN`フォルダーを、自分のホームフォルダーの`mc-remote`へコピーします。中の`2321.1.0`フォルダーに`はじめに.html`と起動ファイルがあります。

- Windowsは`start-mc-remote.cmd`をダブルクリックします。
- Macは`start-mc-remote.command`をダブルクリックします。初回に開発元確認の警告が出た場合は、システム設定の「プライバシーとセキュリティ」から「このまま開く」を選びます。
- Ubuntuは`start-mc-remote.sh`を右クリックして「プログラムとして実行」を選ぶか、端末から`./start-mc-remote.sh`を実行します。

初回はブラウザーの設定画面で、MinecraftサーバーのあるPCとMcRemoteのポート（通常25575）を指定して保存し、「改造版のScratchを開く」を押します。Scratchの「接続する」ブロックを実行し、WireScope miniにペアリングコマンドが出たらMinecraftのチャットへコピーして実行してください。起動したターミナル画面は、使用中は閉じずにおきます。

前の版を使っている場合は、旧版を終了してから、新しい`2321.1.0`フォルダーを前の版のフォルダーの隣に置いて起動します。接続先の設定は新版でも指定してください。

Scratch作品の`.sb3`ファイルは、開いているScratch画面へドラッグ＆ドロップして読み込めます。詳しくはZIP内の`はじめに.html`、または[LANパッケージの案内](https://mc-remote.com/lan/scratch/)を参照してください。[Scratchブロック一覧](https://mc-remote.com/api/scratch/)も利用できます。

配布物の情報は、このReleaseの[manifest.json](https://github.com/Naohiro2g/scratch-editor/releases/download/v2321.1.0/manifest.json)を参照してください。

使ってみた結果や困ったことは、[feedback](https://github.com/Naohiro2g/mc-remote-knowledge/issues/new?template=feedback.yml)へお寄せください。
