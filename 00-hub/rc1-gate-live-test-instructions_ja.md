# rc1 実施票（human owner 向け）

- 根拠: `00-hub/release-gate-notes_ja.md` rc1（exact set凍結）、DECISIONS `2026-10-17-03`、`2026-10-18-02`、`2026-10-18-04`、
  `13-scratch-client/scratch-lan-package-design_ja.md` §6、§8
- 目的: rc1で変わったところを、利用者と同じようにブラウザでダウンロードして確かめる。b10からの版の更新、
  新しい`はじめに.html`での初めての導入、23.2.0と23.2.1の組み合わせ、26.3の名前
- test class: live-human。b10の実施票（`00-hub/b10-gate-live-test-instructions_ja.md`）で通ったところは繰り返さない
- 結果に分類を設けず、判断は結果から行う（b10と同じ）
- 進め方：OSごとに、Windows → Ubuntu → Macの順に、番号の順で進める（2026-10-19にOS別へ書き直した）。Macは
  Ubuntuのサーバーへつなぐので、Ubuntuの後にする
- 進み具合：Windowsは済み（2026-10-19）。次はUbuntu。結果は`00-hub/release-gate-notes_ja.md` rc1の「試験」

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
  （承認は試験の後、`2026-10-18-04`）ので、候補のwheelを入れる
- 比べる相手（b10の公開物）：McRemote `mc-remote-2320.0.0b10.jar`、Scratch LANパッケージ`2320.0.0b10`、Python
  `minecraft-remote-api==2320.0.0b9`（PyPI.org）
- Paper：Windowsは26.3 build 203（Java 25）、Ubuntuは1.21.11 build 132（Java 21）。Macはサーバーを動かさない。認証ON、
  LuckPermsは入れない

## どのOSでも、始める前に採ること

- OSの版、CPU、ブラウザとその版、`java -version`
- `HOME/mc-remote/mc-remote-scratch-LAN/`の中にある版のフォルダー

## Windows（1台構成、Paper 26.3）：b10からの更新、組み合わせ、26.3の名前

1. Chromeで自分のOSのZIPを取る。ダウンロードの警告が出たら、文言とスクリーンショットを記録する（mc-remote.comは
   GitHub.comより評判が低いので、警告が出やすい側の確認になる）。ZIPのプロパティで「許可する」にチェックしてから展開する
2. `2321.0.0rc1/`を、今ある`2320.0.0b10/`の隣に置く。隣に置けばよいと案内から分かったか
3. Paper 26.3を起動する。McRemoteは**b10のまま**
4. rc1の`start-mc-remote.cmd`をダブルクリックで起動し、接続する（**Scratch rc1 ↔ McRemote b10**）
   - 設定画面で接続先を入れ直す必要があったか（`settings.json`は版のフォルダーごと）、入れ直すことが案内から分かったか
   - b10で保存した作品が一覧に残っているか（アドレスは`127.0.0.1:8601`のまま変わらない）
   - ペアリングが要ったか（b10のsession tokenは約2時間で失効するので、時間がたっていればペアリングし直すのが設計どおり）
   - チャットとsetBlockが届くか。WireScopeのhelloで、送った版（23.2.1）と返った版（23.2.0）
   - カタログピッカーで「ポプラの原木」が日本語の名前で出るか、名前で検索できるか
5. Scratch rc1とPaperを止める。`plugins/`の`mc-remote-2320.0.0b10.jar`を外へ移し、`mc-remote-2321.0.0rc1.jar`を置いて、
   Paperを起動する。logで`Enabling McRemote v2321.0.0rc1`
6. Scratch rc1で接続し、チャットとsetBlock（**Scratch rc1 ↔ McRemote rc1**）。ペアリングが要ったか
7. Scratch rc1を止めて、b10の`start-mc-remote.cmd`で起動し、接続、チャット、setBlock（**Scratch b10 ↔ McRemote rc1**）。
   rc1とb10は同じ`127.0.0.1:8601`を使うので、同時に起動しない
8. 古い`2320.0.0b10/`をどうすればよいか（残す、消す）が案内から分かるか

## Ubuntu（サーバー役、Paper 1.21.11）：Python、Linuxの更新、1.21.11での26.3の名前

Pythonは試験用のフォルダーを2つ作り、それぞれに入れる。ペアリングは、Pythonの画面に出たコマンドをMinecraftのチャットで
実行する。

```bash
mkdir -p ~/rc1-test/py-rc1 && cd ~/rc1-test/py-rc1 && uv init
uv add "minecraft-remote-api @ https://mc-remote.com/candidates/2321.0.0rc1/set-1/minecraft_remote_api-2321.0.0rc1-py3-none-any.whl"
mkdir -p ~/rc1-test/py-b9 && cd ~/rc1-test/py-b9 && uv init
uv add "minecraft-remote-api==2320.0.0b9"
```

両方のフォルダーに、次の`hello.py`を置く（`12-python-client/python-client-guide_ja.md` §2の形。試験なので接続先を直接書く）。

```python
from mc_remote.minecraft import Minecraft

mc = Minecraft.create(address="127.0.0.1", port=25575)
mc.postToChat("Hello from Python")
mc.setBlock(5, 62 + 5, 5, "sea_lantern")
```

1. Paper 1.21.11を起動する。McRemoteは**b10のまま**
2. `~/rc1-test/py-rc1`で`uv run python hello.py`（**Python rc1 ↔ McRemote b10**）。ペアリング、チャット、setBlock
3. Paperを止め、McRemoteをrc1のJARに替えて起動する。logで`Enabling McRemote v2321.0.0rc1`
4. `~/rc1-test/py-b9`で`uv run python hello.py`（**Python b9 ↔ McRemote rc1**）
5. `~/rc1-test/py-rc1`の`hello.py`の`Minecraft.create(...)`に`wirescope=True`を足して実行し、同梱のWireScopeが開いて
   通信が見えるか
6. ChromeでLinuxのZIPを取り、`2321.0.0rc1/`を`2320.0.0b10/`の隣に置く。`start-mc-remote.sh`を右クリック →
   「プログラムとして実行」で起動し、このPCのサーバーへ接続、チャット、setBlock
7. カタログピッカーで「ポプラの原木」を探す。1.21.11のサーバーで、26.3にしか無いブロックがどう見えるか（出ない、または
   使えないと分かるか）
8. Scratch rc1を止める。Paper 1.21.11（McRemote rc1）は、Macの試験のために動かしたままにする

## Mac（新しく入れる、Mac → UbuntuのLAN構成）：新しい`はじめに.html`

b10の試験と同じMac → Ubuntuにする。Ubuntuのufwが有効なら、25575（Macからマイクラに入るなら25565も）を許可しておく。

1. `HOME/mc-remote/mc-remote-scratch-LAN/`の中の`2320.0.0b10/`を、試験の間だけ別の場所（デスクトップなど）へ移す。
   `2321.0.0rc1/`も`2320.0.0b10/`も無い状態から始める
2. ChromeでmacOSのZIPを取って展開し、起動の前に`はじめに.html`を開く。冒頭の概略の流れから、自分のOSの節へ迷わず進めるか
3. macOSの手順のとおりに起動する。警告の窓を閉じる →「システム設定」→「プライバシーとセキュリティ」の「このまま開く」→
   確認の窓でもう一度「このまま開く」→ 管理者のパスワード、の順が実際と合うか
4. 設定画面のURLがリンクになっていて、開けるか。「LAN内の別のPC」でUbuntuのサーバーを入れる
5. 接続し、チャットとsetBlockが届くか。WireScopeで通信が見えるか
6. ホームページの`https://mc-remote.com/lan/scratch/`と`はじめに.html`とで、手順の食い違いがないか（ホームページはrc1の
   公開まではb10を指している。版の番号の違いは食い違いに数えない）
7. 移した`2320.0.0b10/`を元の場所へ戻す

## 範囲の外

- 公開VPS（`sb-beta.mc-remote.com`）への切り替え：リリースの作業を終えてから（`2026-10-18-02`）
- 初めて読む人の通し（Pass C）：生徒がb10とホームページで10/24までに行う
- PyPI.orgからの`uv add "minecraft-remote-api==2321.0.0rc1"`：承認の後に確かめる
- 候補と公開のOCIのdigestの比較：Scratch担当が公開のときに記録する

## 記録してほしいこと

- 「始める前に採ること」、使ったZIPのファイル名とサイズ
- 手順ごとの結果と、案内の外で行った操作。迷った箇所、説明が欲しかった箇所
- 警告の文言とスクリーンショット
- 記録にtoken、ペアリングのコマンド、実際のIPアドレス、player UUIDを書かない

結果はknowledgeへ返してください。coordinatorがsanitized recordとして`14-evidence/`へ起こします。
