# b10 ケータリング型簡易版の3 OS試験（2026-10-11〜12）

> test class: `live-human`。実施票`00-hub/b10-gate-live-test-instructions_ja.md`による。human ownerがDiscordに残した文字、log、
> 画面をcoordinatorが要約した。token、pairingのcode、IPアドレス、host名、player UUID、private pathは収録しない。素材はGit外。

## identity

- Scratch `ec29372dadac9c51b2812c746e72032d48d987b6`（run `37933218014`、artifact `11616819485`）。各OSのZIPのSHA-256を各PCで照合して一致
- McRemote `56af9389d1a688ed5ba88df7512b008499d75d7d`（run `38033919529`、artifact `11663343578`、外側zip `28404eb9…198a`を照合）。
  全サーバーの起動logで`v2320.0.0b10`、Paperの`sqlite-jdbc-3.49.1.0.jar`、`Auth enforcement: true`、`HEALTHY`
- Paper 1.21.11 build 132、26.2 build 132。取得はActionsのartifactから（Releaseのassetではない）

| PC | OS | サーバーのJava |
| --- | --- | --- |
| Windows | Windows 11、Smart App Controlオン、ネットワークはプライベート | 21.0.2／25.0.2（Oracle OpenJDK） |
| macOS | macOS 26.7.1、Apple Silicon | Temurin 21.0.12.1（途中まではZulu 25で1.21.11を動かした）／Temurin 25.0.4.1（mise） |
| Ubuntu | Linux 7.0.0-30-generic | 25.0.2（26.2） |

## 結果

動作はPASS。3つのOSの1台構成で、認証ONのペアリング、hello、chat、setBlocks、WireScope miniから独立WireScopeまでが通った。
サーバーの通常の再起動の後、ペアリングし直さずに再接続できた（Windows、macOSは両方の版、Ubuntuは26.2）。初回の起動では
SQLiteのDBが無いので新しいdomainを作り、以前のtokenを持つScratchは`token_not_found`の後にペアリングし直した（`2026-10-10-01`の
とおり）。LAN構成はUbuntu→Windows、Ubuntu→macOS、Windows→macOSが通った。

setBlocksは、1回あたり28,227と30,603ブロックを約40回続けて完了し、負荷に余裕があった。32,768を超える要求が拒否されるのも
見たが、logは無い。

OSの警告はWindowsでJavaのポート開放の確認だけだった。ただしランチャーは3つのOSともターミナルから起動した。

## 見つかったこと

1. サーバーの再起動の後、Scratchが「接続」の表示のまま、次の操作で新しい接続にhelloより先に`chat.post`を送り、サーバーが
   拒否した（2回）。接続のブロックを実行し直すと通った。扱いはhub NOTESで見直し中
2. ランチャーの構成、連携、文言は、OSSの利用者向けにはまだ遠い（human owner）。ランチャーが多数のfileに埋もれている、
   bridgeの`listening`の行が2回出る、サーバーが止まっているときに`ECONNREFUSED`がそのまま出る、など
3. カタログピッカーで、ブロックIDに変数を入れたときの説明が混乱させる
4. Windowsは、使うネットワークを「プライベート」に指定することが大事。教室や家庭のWi-Fiは既定で「パブリック」のことが多く、
   パブリックの設定が緩められていく（human owner）

## 主張しない範囲

ダブルクリックでの起動と、そのときのOSの警告。Releaseのassetからの取得（公開の利用者と同じ導入手順を通したとは言えない）。
Xerialのcandidateで作ったDBの実機での継続。実機でのrevoke。
