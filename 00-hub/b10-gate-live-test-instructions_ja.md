# b10 ケータリング型簡易版：3 OS 実施票（human owner 向け）

- 根拠: `00-hub/release-gate-notes_ja.md` b10、DECISIONS `2026-10-07-04`、`2026-10-09-01`
- 目的: 公開するのと同じZIP（同じSHA-256）で、利用者がする手順のとおりに取得・展開・起動・接続・ペアリングまで進め、
  途中の警告やつまずきを記録する。動けばよい、ではなく「どこで止まりそうか」を見る
- test class: live-human

> 2026-10-09 改訂：初回の試行（Windows、macOS）で、Windowsで認証ONの接続ができない問題と、独立WireScopeが同梱されて
> いない問題が見つかった。McRemoteとScratchの両方のcandidateを作り直すので、下の「使うもの」の表は新しいcandidateが
> そろったら差し替える。今すぐ行うのは「Windowsの診断（今すぐ）」だけ。3 OSの試験は、新しいcandidateがそろってからやり直す。

## Windowsの診断（今すぐ）

Windowsで認証ONの接続ができない原因を確かめる。McRemote担当の静的点検では、credential storeの「directoryを開いて同期する」
処理がWindowsでできないことが最有力の原因候補。次の手順は、credentialのfileを作らず、消さず、中身も読まない。

コマンドはGit Bashで行う。

1. Windowsで、試験に使ったPaperサーバーのフォルダ（`plugins`がある場所）をGit Bashで開く（`cd`する）
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

### ZIP（Scratch candidate）

> 初回の試行で使ったcandidate（CI run 37808012407、artifact ID 11563852835）。WireScopeを同梱した新しいcandidateで差し替える。

| OS | file | bytes | SHA-256 |
| --- | --- | ---: | --- |
| Windows 11 | `mc-remote-scratch-local-2320.0.0b10-windows-x64.zip` | 260361934 | `08340c801c1196c30a1227a7e495feb32131a95e4816ffbb29278557cadab9c1` |
| macOS（Apple Silicon） | `mc-remote-scratch-local-2320.0.0b10-macos-arm64.zip` | 264713598 | `60d69479079eb5f7b7022547d417abc5dc31b237eb12766354885e4db53e6908` |
| Linux | `mc-remote-scratch-local-2320.0.0b10-linux-x64.zip` | 269950028 | `245d83aeab8f6a10bc3703547e0f897b3e82a8c9152c1a131378454f0debdf8b` |

### Minecraftサーバー側（McRemote candidate）

> 初回の試行で使ったcandidate。Windowsの永続化を直した新しいcandidateで差し替える。

- JAR: `mc-remote-2320.0.0b10.jar`、282260 bytes、SHA-256 `60ca6e17fb89ed8474e2341d710c23ab62f4ddfd366c49afc1d233f6526c3ef7`
- 取得先: McRemoteのActions run 37802721957（<https://github.com/Naohiro2g/McRemote/actions/runs/37802721957>）のArtifacts
  `mc-remote-candidate`（artifact ID 11561402977）。落としたzipの中にJARがある。手元のMcRemote
  `handoff-materials/2026-10-09-b10-ci-candidate/materials/`にも同じJARがある。サーバー側のJARは警告の観察の対象では
  ないので、どこから持ってきてもよい。使う前にSHA-256を確かめる
- Paper: 1.21.11 build 130、または 26.2 build 132（どちらか一つでよい。使った方を記録する）
- 準備はMcRemote READMEのクイックスタートのとおり。認証ON（既定）、LuckPermsは入れない

## 取得のしかた（案A、human owner 2026-10-09）

警告を本番と同じ形で見るため、各PCのブラウザでインターネット側から取ってくる（USBやLAN内のコピーでは、Macの隔離属性や
WindowsのMark of the Webが本番と違う）。公開した後に、Releaseのassetで初回の警告だけ短く見直す。

取得は2段になる。

1. ScratchのActions runのページのArtifactsから、artifact（`scratch-candidate-…`、約1.36 GB）を各PCのブラウザで落とし、
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

### LAN構成（Minecraftサーバーは別のPC）

10. 接続先を、LAN内の別PCのMinecraftサーバー（hostはIPかホスト名、port）に変えて保存
11. 6〜8と同じ。firewallの警告、接続できなかったときの表示を記録

## 記録してほしいこと（OSごと）

- 「始める前に採ること」の全項目
- 取得の方法と、SHA-256の照合結果
- 各手順で、出た警告の文言とスクリーンショット、行った許可の操作、止まった箇所
- 構築にかかったおおよその時間、迷った箇所、説明が欲しかった箇所
- 1台構成とLAN構成それぞれの成否
- 記録にtoken、pairingのcode、実際のIPアドレス、player UUIDを書かない（IPは「LANの別PC」などで足りる）

結果はknowledgeへ返してください。coordinatorがsanitized recordとして`14-evidence/`へ起こします。
