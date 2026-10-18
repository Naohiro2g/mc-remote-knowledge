# rc1 実施票（human owner 向け）

- 根拠: `00-hub/release-gate-notes_ja.md` rc1（exact set凍結）、DECISIONS `2026-10-17-03`、`2026-10-18-02`、`2026-10-18-04`、
  `13-scratch-client/scratch-lan-package-design_ja.md` §6、§8
- 目的: rc1で変わったところを、利用者と同じようにブラウザでダウンロードして確かめる。b10からの版の更新、
  新しい`はじめに.html`での初めての導入、23.2.0と23.2.1の組み合わせ、26.3の名前
- test class: live-human。b10の実施票（`00-hub/b10-gate-live-test-instructions_ja.md`）で通ったところは繰り返さない
- 結果に分類を設けず、判断は結果から行う（b10と同じ）

## 使うもの

mc-remote.comに置いた候補（`rc1-integrated-artifact-set-1`、リリースはこの試験の後）。置き場所は`https://mc-remote.com/candidates/2321.0.0rc1/set-1/`で、一覧は
出ないので、下のURLを直接開く。coordinatorが外からダウンロードして、5つのbytesとSHA-256が凍結値と一致することを確かめた
（2026-10-18）。試験ではファイル名とサイズだけ記録する。

- Scratch LANパッケージ（Scratch `ec79b3b`）
  - Windows 11 x64：<https://mc-remote.com/candidates/2321.0.0rc1/set-1/mc-remote-scratch-LAN-2321.0.0rc1-windows-x64.zip>（261,848,009 bytes）
  - macOS（Apple Silicon）：<https://mc-remote.com/candidates/2321.0.0rc1/set-1/mc-remote-scratch-LAN-2321.0.0rc1-macos-arm64.zip>（266,199,673 bytes）
  - Linux x64：<https://mc-remote.com/candidates/2321.0.0rc1/set-1/mc-remote-scratch-LAN-2321.0.0rc1-linux-x64.zip>（271,455,727 bytes）
- McRemote（`192a777`）：<https://mc-remote.com/candidates/2321.0.0rc1/set-1/mc-remote-2321.0.0rc1.jar>（315,352 bytes）
- Python（`c301053`）：<https://mc-remote.com/candidates/2321.0.0rc1/set-1/minecraft_remote_api-2321.0.0rc1-py3-none-any.whl>（196,098 bytes）。PyPI.orgへはまだ出ていない
  （承認は試験の後、`2026-10-18-04`）ので、候補のwheelを入れる（例 `uv add "minecraft-remote-api @ <このURL>"`）
- 比べる相手（b10の公開物）：McRemote `mc-remote-2320.0.0b10.jar`、Scratch LANパッケージ`2320.0.0b10`、Python
  `minecraft-remote-api==2320.0.0b9`（PyPI.org）
- Paper：1.21.11 build 132（Java 21）と26.3 build 203（Java 25）。McRemoteのcandidateのpulseと同じbuild。試験全体で両方を
  一度は使う。認証ON、LuckPermsは入れない

## 始める前に採ること

- OSの版、CPU、ブラウザとその版、Paperの版とbuild、`java -version`
- 手元に残っている`HOME/mc-remote/mc-remote-scratch-LAN/`の中の版のフォルダー（`2320.0.0b10/`があるか）

## A. b10からの版の更新（b10を入れてあるOSで、一つ以上）

1. 候補のURLから、ブラウザで自分のOSのZIPを取る（Windowsは展開の前に「許可する」）。ブラウザのダウンロードの警告が出たら、
   文言を記録する（mc-remote.comはGitHub.comより評判が低いので、警告が出やすい側の確認になる）
2. 展開して、`mc-remote-scratch-LAN/2321.0.0rc1/`を、今ある`2320.0.0b10/`の隣に置く。案内から、隣に置けばよいと分かるか
3. `2321.0.0rc1/`の起動ファイルで始める。設定画面で接続先を入れ直す必要があるか（`settings.json`は版のフォルダーごと）。
   入れ直すことが案内から分かるか
4. Scratchを開き、b10で保存した作品が一覧に残っているか（アドレスは`127.0.0.1:8601`のまま変わらない）
5. 接続する。ペアリングが要るか（b10のsession tokenは約2時間で失効するので、時間がたっていればペアリングし直すのが設計どおり）
6. 古い`2320.0.0b10/`をどうすればよいか（残す、消す）が案内から分かるか

## B. 新しい`はじめに.html`で初めて入れる（Aと別のOSで、一つ以上）

`2321.0.0rc1/`も`2320.0.0b10/`も無い状態から始める。

1. 起動の前に`はじめに.html`を開く。冒頭の概略の流れから、自分のOSの節へ迷わず進めるか
2. 自分のOSの手順のとおりに起動する。macOSは、警告の窓を閉じる →「システム設定」→「プライバシーとセキュリティ」の
   「このまま開く」→ 確認の窓でもう一度「このまま開く」→ 管理者のパスワード、の順が実際と合うか
3. 設定画面のURLがリンクになっていて、開けるか
4. 1台構成で接続し、チャットとsetBlockが届くか。WireScopeで通信が見えるか
5. ホームページの`https://mc-remote.com/lan/scratch/`と`はじめに.html`とで、手順の食い違いがないか（ホームページはrc1の
   公開まではb10を指している。版の番号の違いは食い違いに数えない）

## C. 23.2.0と23.2.1の組み合わせ（どのOSでもよい）

各組み合わせで、接続、チャット、setBlockを一度ずつ。

| client | server（McRemote） | 見ること |
| --- | --- | --- |
| Scratch rc1 | b10（`2320.0.0b10`） | つながる。版の違いを理由に止まらない |
| Scratch b10 | rc1（`2321.0.0rc1`） | つながる |
| Python rc1（wheel） | b10 | つながる |
| Python b9（`2320.0.0b9`） | rc1 | つながる |

Pythonはサーバーごとにペアリングが要る。可能ならPython rc1で、同梱のWireScopeを開く。

## D. 26.3の名前（Paper 26.3で）

1. Scratch rc1を26.3のサーバーにつなぎ、カタログピッカーで26.3のデータで足したブロック（例：Scratchのtestで使ったポプラの原木）が日本語の名前で
   出るか、名前で検索できるか
2. 1.21.11のサーバーにつないだときに、26.3にしか無いブロックがどう見えるか（出ない、または使えないと分かるか）

## 範囲の外

- 公開VPS（`sb-beta.mc-remote.com`）への切り替え：リリースの作業を終えてから（`2026-10-18-02`）
- 初めて読む人の通し（Pass C）：生徒がb10とホームページで10/24までに行う
- PyPI.orgからの`uv add "minecraft-remote-api==2321.0.0rc1"`：承認の後に確かめる
- 候補と公開のOCIのdigestの比較：Scratch担当が公開のときに記録する

## 記録してほしいこと

- 「始める前に採ること」、使ったZIPのファイル名とサイズ
- 場面ごとの結果と、案内の外で行った操作。迷った箇所、説明が欲しかった箇所
- 警告の文言とスクリーンショット
- 記録にtoken、ペアリングのコマンド、実際のIPアドレス、player UUIDを書かない

結果はknowledgeへ返してください。coordinatorがsanitized recordとして`14-evidence/`へ起こします。
