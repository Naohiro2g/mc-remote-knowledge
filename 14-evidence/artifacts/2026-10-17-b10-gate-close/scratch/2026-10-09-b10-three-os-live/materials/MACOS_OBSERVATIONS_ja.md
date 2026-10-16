# macOSの観測（進行中）

## Java 21の環境確認

- 根拠: human ownerが会話へ貼った`java -version`と`sdk current java`の実行出力。
- SDKMAN識別子: `21.0.12.fx-zulu`
- Java version: `21.0.12`、LTS、公開日`2026-07-21`
- Runtime / VM: `Zulu21.52+15-CA`
- build: `21.0.12+8-LTS`
- VM: `64-Bit Server VM`、`mixed mode, sharing`
- 利用予定: Paper 1.21.11系。後続のPaper起動とワールド参加の報告は下記。実際の起動Javaとの対応は未採取。
- インストール時の申告: `sdk install java 21.0.12+1.1-zulu`は失敗し、`21.0.12.fx-zulu`を採用。失敗時の文言を受領し、home pathを`~`へ置換して`MACOS_SDKMAN_INSTALL_FAILURE.txt`へ記録。原因は未確定。
- macOSの版、実行CPU architecture、Java 25側の情報は未報告。

```text
openjdk version "21.0.12" 2026-07-21 LTS
OpenJDK Runtime Environment Zulu21.52+15-CA (build 21.0.12+8-LTS)
OpenJDK 64-Bit Server VM Zulu21.52+15-CA (build 21.0.12+8-LTS, mixed mode, sharing)

Using java version 21.0.12.fx-zulu
```

## Scratch ZIPのSHA-256確認

- human ownerがmacOS用ZIPのSHA-256一致を報告。提供された出力は固定candidateのhashと一致。
- ブラウザによる取得の詳細、OS標準展開、初回起動の結果は未報告。

```text
shasum -a 256 mc-remote-scratch-local-2320.0.0b10-macos-arm64.zip
60d69479079eb5f7b7022547d417abc5dc31b237eb12766354885e4db53e6908  mc-remote-scratch-local-2320.0.0b10-macos-arm64.zip
```

## Minecraftサーバーの準備とワールド参加

- 根拠: human ownerの操作報告。macOSでPaper 1.21.11／26.2の両環境にMcRemote b10を導入し、ワールド参加まで確認完了。
- Paper exact build、McRemote JARのhash、各環境の起動Java、認証設定とLuckPermsの有無は未採取。
- Scratch Localの起動・接続・ペアリング・命令実行は、今回のサーバー準備完了報告には含まれない。

## 未確認の項目

- Scratch ZIPのブラウザ取得の詳細、OS標準展開、初回起動、警告。
- 設定ページ、接続先保存、ペアリング、hello、命令実行。
- 再起動時の警告、設定保持、再接続。
- 1台構成とLAN構成それぞれの結果。
- Paperの実使用build、JARのhash、Java 25側の起動情報。
- 両MC版の並行検証を希望するユーザー判断は受領。実施票では1.21.11 build 130／26.2 build 132の一方でよいとされている。1.21.11を132へ変更する正式gate指定の更新は未確認。

## SDKMAN通常版のインストール失敗

- ログではdownload後、repackaging中に`tmp/out/*/Contents/Home`と`tmp/out/*`へ一致するpathが無く、zipを作れず、続くunzipも失敗している。最後の「archive was corrupt」だけから配布元の原archiveが破損していたとは判定しない。
- agentによるread-only調査: SDKMAN brokerのmacOS arm64向けredirectは、通常版が`zulu21.52.203-ca-jdk21.0.12.1-macosx_aarch64.tar.gz`、FX版が`zulu21.52.15-ca-fx-jdk21.0.12-macosx_aarch64.tar.gz`。
- 両Azul公式archiveの先頭1 MiBをRange取得してtar directoryを確認。どちらも最上位directory下に`Contents/Home`がある。通常版全体205923685 bytes、FX版全体305135602 bytes（Content-Range）。全archiveのhashやユーザーが当時取得したfileの同一性は未検証。
- 単純な公式archiveのdirectory構成差とは説明できない。downloadした内容、手元の展開処理、一時directoryの状態などは未確認。SDKMAN／JavaFX自体の原因へ断定しない。
- 2つのSDKMAN識別子はJavaFX同梱の有無に加え、Javaパッチ版も違う。macOSで実際に使用するFX版は`21.0.12+8-LTS`。

