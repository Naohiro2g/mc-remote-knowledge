# b10 ケータリング型簡易版：3 OS 実施票（human owner 向け）

- 根拠: `00-hub/release-gate-notes_ja.md` b10、DECISIONS `2026-10-07-04`、`2026-10-09-01`
- 目的: 公開するのと同じZIP（同じSHA-256）で、利用者がする手順のとおりに取得・展開・起動・接続・ペアリングまで進め、
  途中の警告やつまずきを記録する。動けばよい、ではなく「どこで止まりそうか」を見る
- test class: live-human

> 2026-10-09 改訂：初回の試行（Windows、macOS）で、Windowsで認証ONの接続ができない問題と、独立WireScopeが同梱されて
> いない問題が見つかった。McRemoteとScratchの両方のcandidateを作り直すので、下の「使うもの」の表は新しいcandidateが
> そろったら差し替える。今すぐ行うのは「Windowsの診断（今すぐ）」だけ。3 OSの試験は、新しいcandidateがそろってからやり直す。
>
> 2026-10-09 追記：Windowsの診断は実施済みで、原因が確定した（release-gate-notes b10）。
>
> 2026-10-09 追記：両方の新しいcandidateがそろった。下の「使うもの」で3 OSの試験をやり直す。

## Windowsの診断（今すぐ）

Windowsで認証ONの接続ができない原因を確かめる。McRemote担当の静的点検では、credential storeの「directoryを開いて同期する」
処理がWindowsでできないことが最有力の原因候補。次の手順は、credentialのfileを作らず、消さず、中身も読まない。

コマンドはGit Bashで行う。

1. Windowsで、試験に使ったPaperサーバーのフォルダ（`plugins`の一つ上。例 `paper-1.21.11`）へGit Bashで`cd`する。
   以下のコマンドは、すべてこの場所で実行する（`plugins`の中で実行すると、対象が見つからず`stage=validate-directory`で止まる）
2. 実際に使ったJARと環境の版を採る

   ```bash
   sha256sum plugins/mc-remote-2320.0.0b10.jar
   java -version
   ```

3. 診断プログラム[`DirectoryForceProbe.java`](../14-evidence/artifacts/2026-10-09-b10-live/mcremote/DirectoryForceProbe.java)
   （McRemote担当が作った41行のJava。directoryを開いて同期するだけで、fileの作成・削除・読み取りをしない）を、Paperの
   フォルダへ落として、SHA-256を確かめてから実行する

   ```bash
   curl -fsSLO https://raw.githubusercontent.com/Naohiro2g/mc-remote-knowledge/main/14-evidence/artifacts/2026-10-09-b10-live/mcremote/DirectoryForceProbe.java
   sha256sum DirectoryForceProbe.java
   # 4d9c9abda5059ac73f1b85b22a4bec0dbff9058cf74b1db01c0d783563c2302c と一致すること
   java DirectoryForceProbe.java ./plugins/McRemote
   ```

   原因候補どおりなら`result=ERROR`、`stage=open-directory-read`、
   `exception=java.nio.file.AccessDeniedException`と出る
4. 次のものがあるか、種類（directory／file）だけを見る。中身は見ない。削除や変更はしない。「No such file or directory」も
   結果としてそのまま返す

   ```bash
   ls -ld plugins/McRemote/credential-revocations
   ls -la plugins/McRemote/credential-revocations
   ls -l  plugins/McRemote/credential-store/snapshot.json
   ```

   見たいのは、`credential-revocations`（directory）、その中の`manifest.json`と`.bootstrap-pending.json`、
   `credential-store/snapshot.json`の有無
5. 2〜4の出力を、private path（ユーザー名を含むpath）を伏せて返す

## 使うもの

> 2026-10-09 差し替え：Scratchは独立WireScopeを同梱したcandidate、McRemoteはWindowsのcredential storeをSQLiteにした
> candidate。初回の試行のcandidate（Scratch run 37808012407、McRemote `60ca6e17…3ef7`）は使わない。

### ZIP（Scratch candidate、source `ec29372`、CI run 37933218014、artifact ID 11616819485）

| OS | file | bytes | SHA-256 |
| --- | --- | ---: | --- |
| Windows 11 | `mc-remote-scratch-local-2320.0.0b10-windows-x64.zip` | 260532718 | `f9d09ee84eb8cc54324c6b9d83dc3ab9371d7592ec0535346cf527d3db931a77` |
| macOS（Apple Silicon） | `mc-remote-scratch-local-2320.0.0b10-macos-arm64.zip` | 264884384 | `16e20e5b2ecbfe1a7070d18f3700739bf2d4d567920347398e7ff82d1a40edc0` |
| Linux | `mc-remote-scratch-local-2320.0.0b10-linux-x64.zip` | 270120781 | `3717f4dd55c0996c8e35ce121f293b06ed78e1a1c1bd7e4dad8c1a297fc186fc` |

### Minecraftサーバー側（McRemote candidate、source `61ba539`、CI run 37943254478、artifact ID 11622727242）

- JAR: `mc-remote-2320.0.0b10.jar`、12320559 bytes、SHA-256 `9902507a3b3f92459da1dbcf9621059425de8966a50289c080aee14a0f9ed7d2`
  （Xerial SQLite JDBCを同梱したので大きくなった）
- 取得先: McRemoteのActions run 37943254478（<https://github.com/Naohiro2g/McRemote/actions/runs/37943254478>）のArtifacts
  `mc-remote-candidate`。落としたzipの中にJARがある。サーバー側のJARは警告の観察の対象ではないので、どこから持ってきても
  よい。使う前にSHA-256を確かめ、`plugins`の古いJAR（`60ca6e17…`）と置き換える
- Paper: 1.21.11 build 130、または 26.2 build 132（どちらか一つでよい。使った方を記録する）
- 準備はMcRemote READMEのクイックスタートのとおり。認証ON（既定）、LuckPermsは入れない
- Windowsでは、認証情報を`plugins/McRemote/credential-store/snapshot.json.sqlite`と
  `plugins/McRemote/credential-revocations-sqlite/authority.sqlite`に保存する。初回の試行で残ったJSONのfileは読まれない
  （消さなくてよい）。Java 25ではSQLiteの読み込みで警告が出ることがあるが、動作には影響しない
- Minecraftサーバーのフォルダを、OneDriveなどのクラウド同期の対象に置かない（SQLiteのDBとWALが同期でつかまれたり
  食い違ったりする）。試験でも同期の対象の外で行う

## 取得のしかた（案A、human owner 2026-10-09）

警告を本番と同じ形で見るため、各PCのブラウザでインターネット側から取ってくる（USBやLAN内のコピーでは、Macの隔離属性や
WindowsのMark of the Webが本番と違う）。公開した後に、Releaseのassetで初回の警告だけ短く見直す。

取得は2段になる。

1. ScratchのActions run 37933218014（<https://github.com/Naohiro2g/scratch-editor/actions/runs/37933218014>）のArtifacts
   から、artifact（`scratch-candidate-ec29372…`、約1.36 GB）を各PCのブラウザで落とし、
   展開する。中に3つのOSのZIPが入っている
2. **自分のOSのZIPだけ**を選ぶ（Windowsは`windows-x64`、Apple Siliconのmacは`macos-arm64`、Linuxは`linux-x64`）。
   ほかのOSのZIPを展開して動かさない（初回の試行で、macOSでLinux用のNodeを実行して失敗した）
3. 選んだZIPのSHA-256を照合する（Windows（Git Bash）とLinux: `sha256sum <file>`、macOS: `shasum -a 256 <file>`）

## 手順（各OSで、まず1台構成、次にLAN構成）

### 始める前に採ること

- OSの正確な版（Windows 11のbuild、macOSの版、Linuxのdistro）、CPU、ブラウザ
- Windowsは「Windowsセキュリティ → アプリとブラウザーの制御 → Smart App Control」の状態（オン／評価／オフ）
- 使うZIPとJARのSHA-256、Paperの版とbuild、`java -version`

### 1台構成（そのPCでMinecraftサーバーも動かす）

1. 自分のOSのZIPを展開する（OS標準の方法で）。展開先のpathを記録（日本語や空白を含む場所も一度試せるとよい）。
   展開すると`mc-remote-scratch-local-2320.0.0b10-<os>-<arch>/`というフォルダができ、その直下にランチャー、`README_ja.md`、
   `NOTICE_ja.md`、`SOURCE_ja.md`、`identity.json`がある
2. ランチャーを起動する（Windows `start-mc-remote.cmd`、macOS `start-mc-remote.command`、Linux `start-mc-remote.sh`）
3. 出た警告を、文言と画面のまま記録する（スクリーンショット）。許可は公式の個別の方法だけで行い、OSの保護を全体で
   切らない
   - macOS: Gatekeeperに止められたら「システム設定 → プライバシーとセキュリティ → このまま開く」。`.command`と同梱の
     Node（runtime）のどちらで警告が出たかを分けて記録
   - Windows: SmartScreenなら「詳細情報 → 実行」。Smart App Controlがオンで止まった場合はそのことを記録する（オフにして
     進めた結果を、オンの端末での成功とは数えない）
   - firewallの許可を求められたら記録（localhostだけで待ち受けるので、出ない見込み）
4. ブラウザで設定ページが開くか。開かなければ、どのURLを手で開いたか
5. 接続先に、同じPCのMinecraftサーバー（host `localhost`、port）を入れて保存
6. Scratchで拡張を追加し、接続のブロックを実行する。従来のペアリング（ゲーム内での承認）を行い、helloが通るまで。
   認証はONのまま行う（OFFにして通った結果は、この試験の成功に数えない）
7. 簡単な命令（例: chat、setBlock）が通るか。可能なら setBlocks 32×32×32（32768）を一度。完了までの時間と、ゲームの
   重さを一言（TPSを守ることが目的ではなく、重くなる様子の観察）
8. 独立WireScopeへのリンクが出るか、開いて通信が見えるか
9. ランチャーを閉じて、もう一度起動。二度目に警告が出るか、設定が残っているか、再接続できるか
10. Minecraftサーバーを通常の手順で止めて、もう一度起動し、ペアリングし直さずに再接続できるか（認証情報が保存されて
    いるか）。Windowsでは、とくにこの手順を確かめる。revokeは実機では行わない（revokeに特有の非上書き、矛盾の検出、
    commitの前後での停止はCIのWindows runnerで確かめた。実機の環境の影響は、ペアリングと再起動で同じDBの書き込みと
    読み直しを通るので、この手順で見える）

### LAN構成（Minecraftサーバーは別のPC）

11. 接続先を、LAN内の別PCのMinecraftサーバー（hostはIPかホスト名、port）に変えて保存
12. 6〜8と同じ。firewallの警告、接続できなかったときの表示を記録

## 記録してほしいこと（OSごと）

- 「始める前に採ること」の全項目
- 取得の方法と、SHA-256の照合結果
- 各手順で、出た警告の文言とスクリーンショット、行った許可の操作、止まった箇所
- 構築にかかったおおよその時間、迷った箇所、説明が欲しかった箇所
- 1台構成とLAN構成それぞれの成否
- 記録にtoken、pairingのcode、実際のIPアドレス、player UUIDを書かない（IPは「LANの別PC」などで足りる）

結果はknowledgeへ返してください。coordinatorがsanitized recordとして`14-evidence/`へ起こします。
