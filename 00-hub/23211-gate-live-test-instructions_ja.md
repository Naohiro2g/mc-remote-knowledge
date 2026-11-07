# 2321.1 実施票（human owner 向け）

- 根拠: `00-hub/release-gate-notes_ja.md`「2026-11-06 `2321.1`横断release gate」（範囲、凍結するexact set `2321.1-set-2`）、
  DECISIONS `2026-11-07-01`、`2026-11-07-02`、`11-plugin/platform-design_ja.md` §11
- 目的: `2321.1.0`で変わったところを、利用者と同じように確かめる。McRemoteのHUD、Scratchのパレットとpickerと本家への追従、
  Pythonのstarterの接続先
- test class: live-human。自動の確認とunitで確かめたことは繰り返さない（「範囲の外」）
- 結果に分類を設けず、判断は結果から行う（rc1と同じ）
- 始める条件: McRemoteが26.3 #244で自動の確認をやり直して通り、coordinatorが置いた候補を外からダウンロードして凍結値と
  照合した後。coordinatorが始めてよいと伝える
- 進め方: Ubuntu（1.21.11）→ Windows（26.3）の順。HUDは両方で、ScratchとPythonはそれぞれ片方で

## 使うもの

mc-remote.comに置いた候補（`2321.1-set-2`、リリースはこの試験の後）。一覧は出ないので、下のURLを直接開く。Stackが
`rsync`で入れて`sha256sum -c`で確かめ、coordinatorが外からダウンロードして、bytesとSHA-256が凍結値と一致することを確かめる。
試験ではファイル名とサイズだけ記録する。

- McRemote（`5b78ded`）：<https://mc-remote.com/candidates/2321.1.0/set-2/mc-remote-2321.1.0.jar>（340,193 bytes）
- Python（`09bbda4`）：<https://mc-remote.com/candidates/2321.1.0/set-2/minecraft_remote_api-2321.1.0-py3-none-any.whl>
  （196,026 bytes）。PyPI.orgへはまだ出ていないので、候補のwheelを入れる
- Scratch LANパッケージ（`57fb769`）
  - Linux x64：<https://mc-remote.com/candidates/2321.1.0/set-2/mc-remote-scratch-LAN-2321.1.0-linux-x64.zip>（272,115,968 bytes）
  - Windows 11 x64：<https://mc-remote.com/candidates/2321.1.0/set-2/mc-remote-scratch-LAN-2321.1.0-windows-x64.zip>
    （262,508,252 bytes）
- 比べる相手：公開中の`2321.0.0`
- Paper：Ubuntuは1.21.11 #132（Java 21）、Windowsは26.3 #244（Java 25）。認証ON。configは`hud.*`を書かない（配布の既定）
- プラグイン（`2026-11-07-02`）：そのPaperの版に合う最新版を入れる。Geyser／Floodgate、ViaVersion／ViaBackwards。
  AdvancedPortalsとWorldEditも入れる（必須度は下がる）。LuckPermsは入れない（LANパッケージの利用者と同じ。LuckPermsを
  入れた構成は公開の箱庭で見る）

## 始める前に採ること

- OSの版、ブラウザとその版、`java -version`、Paperのbuild、Minecraftのclientの版と言語
- 入れたプラグインとその版

## Ubuntu（Paper 1.21.11）：HUD、Scratch

1. **HUDの表示**：参加して、`2321.0.0`のPython（またはScratch）でつなぎ、原点を置く。画面の上にbarが1本出て、
   `絶対 / 相対 / 方位 / tick / 時計`が読めるか。足元のブロックと、照準で狙ったブロックが、表示の座標と合っているか。照準を
   空へ外すと`[-]`になるか
2. **Fでの切り替え**：何も設定せずに、Fで足元と照準が切り替わるか。Shiftは要らないか。`/mcr hud off`にすると、Fが通常の
   オフハンドの交換に戻るか。`/mcr hud on`、`/mcr hud toggle-on-swap off`でも、Fが交換に戻るか
3. **command**：`/mcr hud status`が`HUD: on / … / toggle-on-swap: on`の形で、小文字の`on`／`off`で出るか。`/mcr hud legs`、
   `/mcr hud target`、`/mcr hud toggle`が効くか。`/mcr`でほかのcommand（たとえばpair）も使えるか
4. **戻る、移る**：退出して入り直す、死んで復活する、ネザーへ行って戻る。barが消えたまま、または2本にならず、今の位置を
   表示するか。ネザーでは相対が`[ - - - ]`になり、戻ると表示されるか。入り直すと、2で変えた設定が既定（`on`）に戻るか
5. **方位の言語**：clientの言語を日本語と英語で切り替え、方位が北〜北西とN〜NWで出るか
6. **ScratchのLANパッケージ**：Linuxの`2321.1.0`のZIPを、今の`2321.0.0`の隣に置いて起動し、このPaperにつなぐ。
   `はじめに.html`の版の表示が`2321.1.0`か
7. **パレットの頭出し**：mc-remoteのカテゴリを選んだとき、見出しが上に揃うか（rc1でずれた場面）。ブラウザの拡大縮小をしなくても
   ずれないか
8. **picker**：ブロック選択画面で、カテゴリ名（たとえば「建築ブロック gold」「Redstone Blocks」）で絞り込み、選んだブロックで
   実際に建てられるか
9. **作品**：`2321.0.0`で保存した作品を開いて、動かす。保存して開き直す。SVGのコスチュームを描いて編集する

## Windows（Paper 26.3）：HUD、Python

1. **HUD**：Ubuntuの1〜5を、26.3で繰り返す
2. **Python**：wheelを入れ、starterのテンプレートの接続先が`sb.mc-remote.com`、portが25575になっているか。公開中の箱庭
   `sb.mc-remote.com`へつないで、ペアリングとsetBlock、getBlockができるか（箱庭は`2321.0.0`のまま）

## 公開の後（タブレット）

公開のWeb editorで、iPadのSafariとAndroidの更新済みChromeを使う。問題が出たら次の版で直す（human owner 2026-11-07）。

1. カテゴリを切り替えてブロックを探す。見出しが見つけやすいか、押しやすいか、作業中に位置を見失わないか
2. ソフトウェアキーボードを出し、日本語のカテゴリ語を入れて、結果を選んで作品へ戻る。キーボードで選ぶ操作や適用が
   妨げられないか

## 範囲の外

- McRemote：hello、認証、block、sign、entity、再起動の後の互換は、自動の確認（1.21.11 #132、26.3 #244）で確かめる（26.3は#244でやり直す）。接続の順、
  2本目が表示を取らないこと、切れた後の移り先、時刻の換算、照準の距離、色の値はunitで確かめた。複数の接続を画面で試さない
- Scratch：AND検索、版ごとの分離、IDだけを送ること、頭出しの位置の数値はunitと実Chromiumで確かめた。LANのランチャーは
  `2321.0.0`と同じなので、macOSとWindowsの起動は繰り返さない
- Python：APIとwireは変わらない。starterの接続先は静的な照合とtestで確かめた

## 記録してほしいこと

- 番号ごとに、できたか、できなかったか、気づいたこと。画面の写真は、HUDのbar、ずれ、エラーの場面
- できなかったときは、そこで止めて、その番号と画面をcoordinatorへ渡す
