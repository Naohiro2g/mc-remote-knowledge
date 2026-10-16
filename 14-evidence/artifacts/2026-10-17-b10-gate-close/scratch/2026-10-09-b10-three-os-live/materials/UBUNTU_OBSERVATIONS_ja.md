# Ubuntuの観測（進行中）

## Java 21の環境確認

- 根拠: human ownerが会話へ貼った`sdk current java`と`java -version`の実行出力。terminal promptのユーザー名・host名・pathは省略。
- SDKMAN識別子: `21.0.12+1.1-zulu`
- Java version: `21.0.12.1`、LTS、公開日`2026-08-18`
- Runtime / VM: `Zulu21.52+203-CA`
- build: `21.0.12.1+1-LTS`
- VM: `64-Bit Server VM`、`mixed mode, sharing`
- 利用予定: Paper 1.21.11系。後続のPaper起動とワールド参加の報告は下記。実際の起動Javaとの対応は未採取。
- macOSのFX版`21.0.12+8-LTS`とJavaパッチ版まで同一ではない。両者をJava 21系列として個別に記録する。
- 追加のユーザー申告: Ubuntuでも通常版とFX版の両方をインストールし、Javaパッチ版の差はmacOSと同じだった。Ubuntu FX版の完全な`java -version`出力は未受領。
- ユーザーが確認した意味: 「fxの方が遅い」は更新の追随を指す。今回の候補では通常版がJava`21.0.12.1`、FX版が`21.0.12`で、FX版の更新が遅れているという観察として記録する。
- Ubuntuの版、実行CPU architecture、Java 25側の情報は未報告。

```text
Using java version 21.0.12+1.1-zulu

openjdk version "21.0.12.1" 2026-08-18 LTS
OpenJDK Runtime Environment Zulu21.52+203-CA (build 21.0.12.1+1-LTS)
OpenJDK 64-Bit Server VM Zulu21.52+203-CA (build 21.0.12.1+1-LTS, mixed mode, sharing)
```

## Scratch ZIPのSHA-256確認

- human ownerがLinux用ZIPのSHA-256一致を報告。提供された出力は固定candidateのhashと一致。
- ブラウザによる取得の詳細、OS標準展開、初回起動の結果は未報告。

```text
sha256sum mc-remote-scratch-local-2320.0.0b10-linux-x64.zip
245d83aeab8f6a10bc3703547e0f897b3e82a8c9152c1a131378454f0debdf8b  mc-remote-scratch-local-2320.0.0b10-linux-x64.zip
```

## Minecraftサーバーの準備とワールド参加

- 根拠: human ownerの操作報告。UbuntuでPaper 1.21.11／26.2の両環境にMcRemote b10を導入し、ワールド参加まで確認完了。
- Paper exact build、McRemote JARのhash、各環境の起動Java、認証設定とLuckPermsの有無は未採取。
- Scratch Localの起動・接続・ペアリング・命令実行は、今回のサーバー準備完了報告には含まれない。

## 未確認の項目

- Scratch ZIPのブラウザ取得の詳細、OS標準展開、初回起動、警告。
- 設定ページ、接続先保存、ペアリング、hello、命令実行。
- 再起動時の警告、設定保持、再接続。
- 1台構成とLAN構成それぞれの結果。
- Paperの実使用build、JARのhash、Java 25側の起動情報。
