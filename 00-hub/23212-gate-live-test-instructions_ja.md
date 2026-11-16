# 2321.2 McRemoteの実施票（human owner 向け）

- 根拠: `00-hub/release-gate-notes_ja.md`「2026-11-15 `2321.2`横断release gate」（範囲、人間の試験）、DECISIONS `2026-11-12-02`、
  `2026-11-14-02`、`2026-11-14-04`、`2026-11-14-05`、`2026-11-15-02`、`2026-11-15-03`、hub NOTESの2026-11-12の行
  「次の横断gateの人間の試験で、McRemoteのゲーム内の文の言語を見る」
- 目的: McRemote `2321.2.0`で変わったところを、利用者と同じように確かめる。ゲーム内の文の言語、新しいreason、前のclientが
  そのまま使えること
- test class: live-human。Paperの自動の確認とunitで確かめたことは繰り返さない（「範囲の外」）
- 結果に分類を設けず、判断は結果から行う
- 始める条件: 満たしている。coordinatorがCIのartifactを取り直して、JARのbytesとSHA-256を確かめた（gate notesの
  「返却の照合（2026-11-15〜16）」）

## 使うもの

- McRemote（`2ccf0b1`、PR #21。`main`へはmerge済み）：CIのrun <https://github.com/Naohiro2g/McRemote/actions/runs/43678473697>
  のartifact `mc-remote-candidate`（ZIP 325,685 bytes）。中の`mc-remote-2321.2.0.jar`は348,720 bytes、SHA-256
  `16e927a79ea9b9ae9f1aa544cd5101eb3a6c39228ef9c0da7175853d100703f8`。入れる前にSHA-256を計って比べる（Windowsは
  PowerShellの`Get-FileHash`）。今回はMcRemoteだけなので、mc-remote.comに候補を置かず、GitHubから取る
- 前のclient：Python `2321.1.0`（PyPI）、ScratchのLANパッケージ`v2321.1.0`（WireScopeも入っている）
- Paper：26.3 #244（Java 25）。認証ON。configは配布の既定
- プラグイン：そのPaperの版に合う最新版のGeyser／Floodgate、ViaVersion／ViaBackwards。LuckPermsは入れない（`2321.1`と同じ）

## 始める前に採ること

- OS、`java -version`、Paperのbuild、Minecraftのclient（Java版、統合版）の版
- 入れたプラグインとその版
- `/worldborder get`の値（4で変えて、後で戻す）

## ゲーム内の文の言語

1. **Java版、日本語**：clientの言語を日本語にしてつなぎ、Python（またはScratch）でペアリングする。ペアリング成功の文と、
   `/mcr hud status`の対象の名前が日本語だけで出るか（「日本語 / English」の併記が残っていないか）
2. **Java版、English (US)**：同じことを英語で。英語の画面に日本語や併記が残らないか
3. **つないだまま切り替え**：つないだままclientの言語を切り替え、次の`/mcr hud status`と、BossBarの方位（北〜北西／N〜NW）が
   同じ言語にそろうか
4. **統合版**：Geyser経由で、日本語と英語で1と2の画面を見る
5. **help**：`/help mcr`と`/version McRemote`で、製品名と構文が読めるか

## 新しいreasonと、前のclient

PythonとScratchのそれぞれで、原点を置いてから行う。Pythonは例外の中身、Scratchは止まらずに次のブロックへ進むかと、
WireScopeに出るerrorを見る。どちらも、errorの後に次の命令（setBlockなど）が通るか、接続が切れないかを見る。

6. **hello**：WireScopeで、helloの応答の`protocol`が`23.3.0`か。前のclient（`23.2.1`で申告する）がそのままつながるか
7. **高さの外（`out_of_bounds`）**：相対のyを400にしてsetBlockする。errorのreasonが`out_of_bounds`で、ブロックが置かれないか
8. **水平の外（`out_of_bounds`）**：`/worldborder center 0 0`、`/worldborder set 400`にして、x=300あたりへsetBlockする。7と同じに
   なるか。終わったら`/worldborder set`で、採った値に戻す
9. **1回に置ける数（`block_count_limit_exceeded`）**：(0,0,0)から(32,32,32)まで（35,937個）をsetBlocksする。reasonが
   `block_count_limit_exceeded`で、1つも置かれないか。(0,0,0)から(31,31,31)まで（32,768個）は置けるか
10. **建築範囲（`build_range_exceeded`）**：WireScopeでhelloの`permissions.buildRange`を見て、それより遠いxへsetBlockする。
    reasonが`build_range_exceeded`か。範囲が広すぎて試せなければ、試せなかったと書く
11. **回帰**：ペアリング、チャット、setBlock、getBlock、HUDの表示が、`2321.1.0`と同じようにできるか

## 範囲の外

- `protocol_mismatch`と`expected_hello`のcodeは、通常のclientからは起こせない。unitと実TCPのtestで確かめた
- hello、認証、catalog、block、sign、entity、events、particle、chat、再起動の後の互換は、Paperの自動の確認（1.21.11 #132、
  26.3 #244）で確かめた。1.21.11は人では見ない（human owner 2026-11-15）
- credentialのfileのmode（`0600`、`0700`）は、出した後にStackが箱庭（Linux）で確かめる
- BANで拒む経路の直しとsocketごとのkeepaliveは、この版に入っていない
- 新しいreasonの、Scratchの新しい表示は、Scratchの試験で見る

## 記録してほしいこと

- 番号ごとに、できたか、できなかったか、気づいたこと。画面の写真は、言語の画面と、errorの場面
- できなかったときは、そこで止めて、その番号と画面をcoordinatorへ渡す
