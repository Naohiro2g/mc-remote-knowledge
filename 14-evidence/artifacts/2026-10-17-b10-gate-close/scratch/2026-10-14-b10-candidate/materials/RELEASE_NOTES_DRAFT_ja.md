# mc-remote Scratch 2320.0.0b10

マイクラリモコン改造版ScratchのLANパッケージを、Windows 11 x64、Apple Silicon Mac、Linux x64向けに用意しました。使うPCのOSに合うZIPを**1つ**ダウンロードしてください。Minecraftサーバーには対応するマイクラリモコンのプラグインMcRemoteを入れ、プレイヤーとしてワールドに参加しておきます。[サーバーの準備方法](https://github.com/Naohiro2g/McRemote#readme)。



**【重要】Windowsでは、ZIPを展開する前に**エクスプローラーでZIPを右クリックし、「プロパティ」→「全般」の「許可する」にチェックして「適用」を押してください。その後で展開します。この方法はSmart App ControlをオンにしたWindows 11で起動を確認しています。

| PC | ダウンロードするZIP | 起動ファイル |
| --- | --- | --- |
| Windows 11、Intel／AMD 64ビット | `mc-remote-scratch-LAN-2320.0.0b10-windows-x64.zip` | `start-mc-remote.cmd` |
| macOS、Apple Silicon | `mc-remote-scratch-LAN-2320.0.0b10-macos-arm64.zip` | `start-mc-remote.command` |
| Linux、Intel／AMD 64ビット | `mc-remote-scratch-LAN-2320.0.0b10-linux-x64.zip` | `start-mc-remote.sh` |

展開先の内側にある`mc-remote-scratch-LAN`フォルダーを、自分のホームフォルダーの`mc-remote`へコピーします。中の`2320.0.0b10`フォルダーに`はじめに.html`と起動ファイルがあります。


- Windowsは起動ファイルをダブルクリックします。または、Windowsターミナルで`./start-mc-remote.cmd`を実行します。GitBashやPowerShellを使えます。



- Macは起動ファイルをダブルクリックします。または、ターミナルで`./start-mc-remote.command`を実行します。初回起動時にブロックされた場合は、システム設定の「プライバシーとセキュリティ」から「このまま開く」を選びます。



- Ubuntuでは起動ファイルを右クリックして「プログラムとして実行」を選ぶか、ターミナルから`./start-mc-remote.sh`を実行します。



初回はブラウザーの設定画面で、Minecraftサーバー／マイクラリモコンサーバーのあるPCと、マイクラリモコンのポートを指定して保存し、「改造版のScratchを開く」を押します。Scratchの「接続する」ブロックを実行し、WireScope miniにペアリングコマンドが出たらMinecraftのチャットにコピペして実行してください。次回からは設定済みの接続先でScratchが開きます。起動したターミナル画面は、使用中は閉じずにおきます。

Scratch作品の`.sb3`ファイルは、開いているScratch画面へドラッグ＆ドロップして読み込めます。現在の作品をブラウザーへ保存してから切り替わります。詳しくはZIP内の`はじめに.html`を参照してください。

この版はpre-releaseです。安定版ではないので不具合が発生することがあります。



Scratch、Bridge、WireScope、Node.jsをZIPへ同梱しています。配布物の正確なidentityは同じReleaseの`manifest.json`を参照してください。

ZIPのSHA-256を自分で照合したい場合の値です。

| OS | bytes | SHA-256 |
| --- | ---: | --- |
| Windows x64 | 261,590,008 | `00e73b71d63859f088595257abdec7ce204a09282d79f26daa8d851e0f4af1e8` |
| macOS arm64 | 265,941,672 | `edcc757b931d8b89fc18487ee385c20d9ecbdc398b7f34f017e2137fe26c12d2` |
| Linux x64 | 271,197,726 | `b69e5b1118dba284604c217b0f3b06ea40b9876014166461705fdc400f647526` |
