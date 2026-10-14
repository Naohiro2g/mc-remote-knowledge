# b10 Scratch LANパッケージ：3 OS 実施票（human owner 向け）

- 根拠: `00-hub/release-gate-notes_ja.md` b10、DECISIONS `2026-10-12-01`、`2026-10-13-05`、`2026-10-14-01`、
  `13-scratch-client/scratch-lan-package-design_ja.md` §8
- 目的: 利用者と同じ経路（pre-releaseのReleaseのページからブラウザで取得、OS標準の展開、案内のとおりの起動）で、取得から
  保存・再開までを通し、どこで迷い、どこで止まるかを見る
- test class: live-human

> 2026-10-14 作り直し：前の版（ケータリング型簡易版、Scratch `ec29372`とMcRemote `56af938`）は2026-10-11〜12に実施済み
> （`14-evidence/records/2026-10-12-b10-scratch-local-3os-live-human_ja.md`）。前の版の本文はGitの履歴にある。

## 使うもの

pre-release `v2320.0.0b10`のasset。Releaseを作った後、coordinatorがassetのSHA-256を下の値と照合してから、この票を
渡す。試験ではSHA-256を照合しなくてよい（同一性は開発側が記録する）。ファイル名とサイズだけ記録する。

### Scratch LANパッケージ（Scratch `0809eb5`、Release：作成後に記入）

| OS | ZIP | bytes | SHA-256 |
| --- | --- | ---: | --- |
| Windows 11 x64 | `mc-remote-scratch-LAN-2320.0.0b10-windows-x64.zip` | 261,590,008 | `00e73b71d63859f088595257abdec7ce204a09282d79f26daa8d851e0f4af1e8` |
| macOS（Apple Silicon） | `mc-remote-scratch-LAN-2320.0.0b10-macos-arm64.zip` | 265,941,672 | `edcc757b931d8b89fc18487ee385c20d9ecbdc398b7f34f017e2137fe26c12d2` |
| Linux x64 | `mc-remote-scratch-LAN-2320.0.0b10-linux-x64.zip` | 271,197,726 | `b69e5b1118dba284604c217b0f3b06ea40b9876014166461705fdc400f647526` |

### Minecraftサーバー側（McRemote `17bcf26`、Release：作成後に記入）

- JAR: `mc-remote-2320.0.0b10.jar`、315,352 bytes、SHA-256 `96ddf09f765a77811740d5c62f3787f7a87c8be6cd7247d345f6dfe9e93512a4`。
  McRemoteのpre-releaseのassetから取る。`plugins`の古いJARと置き換える
- Paper: 1.21.11（build 130、Java 21）か26.3（build 181、Java 25）。McRemoteのpulseは26.3 build 178、b10の前の試験は180。**3つのOSの試験全体で、両方の版を一度は使う**。
  使った版とbuildを記録する。Javaはサーバーのフォルダーごとにmiseで固定する（McRemote README、`2026-10-12-02`）
- 認証ON（既定）、LuckPermsは入れない。サーバーのフォルダーをOneDriveなどのクラウド同期の対象に置かない
- **少なくとも一つのOSでは、McRemoteのDBが無い新しいサーバーのフォルダーで始める**。保存済みのtokenが使えない状態で、
  ペアリング待ちの画面（WireScope miniの自動展開とコマンドの表示）を見るため。前の試験では見ていない

## 始める前に採ること

- OSの正確な版（Windows 11のbuild、macOSの版、Linuxのdistro）、CPU、ブラウザとその版
- Windowsは「Windowsセキュリティ → アプリとブラウザーの制御 → Smart App Control」の状態（オン／評価／オフ）
- Paperの版とbuild、`java -version`
- 前の試験の`HOME/mc-remote/mc-remote-scratch-LAN/2320.0.0b10/`が残っていたら、別の名前に変えて退けておく（同じ版の
  フォルダーに重ねない）

## 手順（各OSで、まず1台構成、次にLAN構成）

案内はReleaseの本文、`はじめに.html`、設定画面、Scratchの画面の表示。案内に無い操作をしたら、それを記録する。

### 1. 選択・取得

1. ブラウザで`v2320.0.0b10`のReleaseのページを開き、本文を読んで自分のOSのZIPを**一つだけ**取る
2. ブラウザのダウンロードの警告、保存の確認が出たら、文言を記録する

### 2. 展開・配置

1. Windows：本文のとおり、**展開の前に**ZIPを右クリック →「プロパティ」→「全般」の「許可する」にチェック →「適用」
2. OS標準の方法で、既定の展開先に展開する（展開先を選び直さない）。長いファイル名などの警告が出たら記録する
3. 外側のフォルダーの内側にある`mc-remote-scratch-LAN`を、ホームフォルダーの`mc-remote`へコピーする
4. `mc-remote-scratch-LAN/2320.0.0b10/`に起動ファイル、`settings.json`は無し、`data/`、`README_ja.md`、`はじめに.html`、
   `NOTICE_ja.md`が並ぶか。迷わず起動ファイルを見つけられたか

### 3. 案内を読む

1. 起動の前に`はじめに.html`を開く。追加のアプリなしで読めるか、今の版と起動の方法が分かるか

### 4. 初回起動

1. 起動ファイルを開く
   - Windows：`start-mc-remote.cmd`をダブルクリック
   - macOS：`start-mc-remote.command`をダブルクリック。止められたら「システム設定 → プライバシーとセキュリティ →
     このまま開く」
   - Linux：`start-mc-remote.sh`を右クリック →「プログラムとして実行」、または端末で`./start-mc-remote.sh`
2. 出た警告を、文言と画面のまま記録する（スクリーンショット）。起動ファイルへの警告と、同梱のNode.jsへの警告を分ける。
   firewallの許可を求められたら記録する
3. ターミナルの画面と、ブラウザで設定画面が開くか。開かなければ、何をして開いたか

### 5. 設定画面

1. 「マイクラサーバーは、どのPCで動いていますか？」で「このPC」を選び、保存する。起動ファイルの隣に`settings.json`が
   できるか
2. 「改造版のScratchを開く」で、別のタブにScratchが開くか
3. Scratchを開いたまま設定画面で接続先を変えようとして、変えられない理由の表示が分かるか
4. 設定画面のタブを閉じて、Scratchを使い続けられるか。設定画面を開き直す方法が分かるか

### 6. 1台構成：接続

1. Scratchで「接続する」を一度クリックする
2. ペアリングが要るときは、WireScope miniにペアリングのコマンドが出るか。Minecraftのチャットに貼って実行し、接続できるか
3. 「チャットに［こんにちは］と言う」がMinecraftのチャットに届くか。簡単なsetBlock
4. 可能なら setBlocks 32×32×32（32768）を一度。完了までの時間と、ゲームの重さを一言
5. WireScopeを開いて、通信が見えるか

### 7. 保存・再開

1. 作品をブラウザに保存する。別の`.sb3`（「ファイル」→「コンピューターに保存」で作ったものでよい）を、開いている
   Scratchの画面へドラッグ＆ドロップする。今の作品が保存されてから切り替わるか。保存した作品が一覧に残っているか
2. ランチャーを終える（ターミナルの画面を閉じる、またはCtrl+C）
3. 時間をおいて（できれば翌日）、**作者の誘導なしに**、いつもの起動ファイルからもう一度始める。保存した接続先でScratchが
   開き、作品を見つけて開き、ペアリングし直さずに接続できるか
4. Minecraftサーバーを通常の手順で止めて、もう一度起動し、ペアリングし直さずに接続できるか。サーバーの再起動の後に
   Scratchが「接続」の表示のまま失敗する問題は既知（hub NOTES 2026-10-12）。起きたら、ブラウザの再読み込みの後に
   接続し直して進め、起きたことだけ記録する

### 8. LAN構成（Minecraftサーバーは別のPC）

1. 設定画面で「LAN内の別のPC」を選び、サーバー役のPCのIPアドレスかホスト名と、McRemoteのポート（通常`25575`）を入れる
2. 6の1〜3と同じ。firewallの警告、つながらなかったときの表示と、そこから次の操作を選べたかを記録する
3. 可能なら、2台のPCでそれぞれ別のプレイヤーとしてつなぎ、互いの接続とペアリングを混同しないか

### 9. つまずき（どれか一つでよい）

- Minecraftサーバーを止めたまま接続する、接続先のポートを間違える、など。表示から次の操作を選べるか

## 範囲の外

- 版の更新（新しい版を隣に置く）：同じ版しか無いので、今回は試さない
- File System Accessの書き出し：b10に入らない（初回stableの後）
- ホームページからの取得：入口はrc1までに作る。今回はReleaseのページから取る

## 記録してほしいこと（OSごと）

- 「始める前に採ること」の全項目、使ったZIPのファイル名とサイズ
- 場面ごとの結果と、案内の外で行った操作
- 警告の文言とスクリーンショット、行った許可の操作、止まった箇所
- かかったおおよその時間、迷った箇所、説明が欲しかった箇所
- 記録にtoken、ペアリングのコマンド、実際のIPアドレス、player UUIDを書かない（IPは「LANの別PC」などで足りる）

結果はknowledgeへ返してください。coordinatorがsanitized recordとして`14-evidence/`へ起こします。

