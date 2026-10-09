# b10 ケータリング型簡易版：3 OS 実施票（human owner 向け）

- 根拠: `00-hub/release-gate-notes_ja.md` b10（進捗 2026-10-09）、DECISIONS `2026-10-07-04`
- 目的: 公開するのと同じZIP（同じSHA-256）で、利用者がする手順のとおりに取得・展開・起動・接続・ペアリングまで進め、
  途中の警告やつまずきを記録する。動けばよい、ではなく「どこで止まりそうか」を見る
- test class: live-human

## 使うもの

### ZIP（Scratch candidate、CI run 37808012407、artifact ID 11563852835）

| OS | file | bytes | SHA-256 |
| --- | --- | ---: | --- |
| Windows 11 | `mc-remote-scratch-local-2320.0.0b10-windows-x64.zip` | 260361934 | `08340c801c1196c30a1227a7e495feb32131a95e4816ffbb29278557cadab9c1` |
| macOS（Apple Silicon） | `mc-remote-scratch-local-2320.0.0b10-macos-arm64.zip` | 264713598 | `60d69479079eb5f7b7022547d417abc5dc31b237eb12766354885e4db53e6908` |
| Linux | `mc-remote-scratch-local-2320.0.0b10-linux-x64.zip` | 269950028 | `245d83aeab8f6a10bc3703547e0f897b3e82a8c9152c1a131378454f0debdf8b` |

### Minecraftサーバー側（McRemote candidate）

- JAR: `mc-remote-2320.0.0b10.jar`、282260 bytes、SHA-256 `60ca6e17fb89ed8474e2341d710c23ab62f4ddfd366c49afc1d233f6526c3ef7`
  （McRemote CI run 37802721957、artifact ID 11561402977）
- Paper: 1.21.11 build 130、または 26.2 build 132（どちらか一つでよい。使った方を記録する）
- 準備はMcRemote READMEのクイックスタートのとおり。認証ON（既定）、LuckPermsは入れない

## 取得のしかた（案A、human owner 2026-10-09）

警告を本番と同じ形で見るため、各PCのブラウザでインターネット側から取ってくる（USBやLAN内のコピーでは、Macの隔離属性や
WindowsのMark of the Webが本番と違う）。GitHubのActions run 37808012407
（[run 37808012407](https://github.com/Naohiro2g/scratch-editor/actions/runs/37808012407)）のArtifactsから、各PCのブラウザでartifact
`scratch-candidate-c717d0c2ed9b045b8c3bb925b0e1fcd8ee33010b`をダウンロードし、中の該当ZIPを取り出す。外側のartifactは
1.36 GBで、中から取り出す一手間は本番と違う。公開した後に、Releaseのassetで初回の警告だけ短く見直す。

取り出したZIPのSHA-256を上の表と照合してから始める（Windows: `certutil -hashfile <file> SHA256`、
macOS: `shasum -a 256 <file>`、Linux: `sha256sum <file>`）。

## 手順（各OSで、まず1台構成、次にLAN構成）

### 1台構成（そのPCでMinecraftサーバーも動かす）

1. ZIPを展開する（OS標準の方法で）。展開先のpathを記録（日本語や空白を含む場所も一度試せるとよい）
2. ランチャーを起動する（Windows `start-mc-remote.cmd`、macOS `start-mc-remote.command`、Linux `start-mc-remote.sh`）
3. 出た警告を、文言と画面のまま記録する（スクリーンショット）。許可は公式の個別の方法だけで行い、OSの保護を全体で
   切らない
   - macOS: Gatekeeperに止められたら「システム設定 → プライバシーとセキュリティ → このまま開く」。`.command`と同梱の
     Node（runtime）のどちらで警告が出たかを分けて記録
   - Windows: SmartScreenなら「詳細情報 → 実行」。あわせて「Windowsセキュリティ → アプリとブラウザーの制御 →
     Smart App Control」の状態（オン／評価／オフ）を記録し、オンで止まった場合はそのことを記録する（オフにして進めた
     結果を、オンの端末での成功とは数えない）
   - firewallの許可を求められたら記録（localhostだけで待ち受けるので、出ない見込み）
4. ブラウザで設定ページが開くか。開かなければ、どのURLを手で開いたか
5. 接続先に、同じPCのMinecraftサーバー（host `localhost`、port）を入れて保存
6. Scratchで拡張を追加し、接続のブロックを実行する。従来のペアリング（ゲーム内での承認）を行い、hello が通るまで
7. 簡単な命令（例: chat、setBlock）が通るか。可能なら setBlocks 32×32×32（32768）を一度。完了までの時間と、ゲームの
   重さを一言（TPSを守ることが目的ではなく、重くなる様子の観察）
8. ランチャーを閉じて、もう一度起動。二度目に警告が出るか、設定が残っているか、再接続できるか

### LAN構成（Minecraftサーバーは別のPC）

9. 接続先を、LAN内の別PCのMinecraftサーバー（hostはIPかホスト名、port）に変えて保存
10. 6〜7と同じ。firewallの警告、接続できなかったときの表示を記録

## 記録してほしいこと（OSごと）

- OSの版（Windows 11のbuild、macOSの版、Linuxのdistro）、ブラウザ
- 取得の方法（案A／B）と、SHA-256の照合結果
- 各手順で、出た警告の文言とスクリーンショット、行った許可の操作、止まった箇所
- 構築にかかったおおよその時間、迷った箇所、説明が欲しかった箇所
- 1台構成とLAN構成それぞれの成否、Paperの版
- 記録にtoken、pairingのcode、実際のIPアドレス、player UUIDを書かない（IPは「LANの別PC」などで足りる）

結果はknowledgeへ返してください。coordinatorがsanitized recordとして`14-evidence/`へ起こします。
