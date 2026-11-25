# `2400.0.0rc1`の実施票（human owner 向け）

- 根拠: `00-hub/release-gate-notes_ja.md`「2026-11-19 `2400`横断release gate」（範囲、凍結するexact set `2400-set-1`）、
  `00-hub/2400-gate-candidate-instructions_ja.md`（Scratchの直し1〜4、Unity箱庭の座標の見え方と最初のカメラ、Pythonの版）、
  DECISIONS `2026-11-20-01`（座標の見え方）、`2026-11-20-02`（操作のエラーの知らせ方）、`2026-11-24-01`（Unity箱庭の上限）
- 目的: `2400.0.0rc1`を`-beta`の組で、利用者と同じように使う。`2321.2-set-1`の試験で見つかったものが直ったこと、protocol `24.0.0`と
  `23.x`の境で断られ方が分かることを確かめる
- test class: live-human。CIとunit、coordinatorの照合で確かめたことは繰り返さない（「範囲の外」）
- 結果に分類を設けず、判断は結果から行う
- 日程: 11/26〜27。11/27に延期するかを決める（延期なら12月5日）
- 始める条件: `00-hub/2400-gate-rc1-release-instructions_ja.md`のpre-releaseが出て、coordinatorが照合し、Stackが`sb-beta`、`scratch-beta`、
  `wirescope-beta`をrc1にした後。Pythonの項目は、PyPI.orgへ出た後（その前なら、GitHubのpre-releaseのwheel）
- 進め方: 公開の`-beta`の組を正面にする。LANパッケージは、Ubuntuの機械とWindowsのPCで使う。切断の項目（14）だけ、手元で
  Unity箱庭を動かす

## 使うもの

| | 最新版候補（`2400.0.0rc1`、protocol `24.0.0`） | LTS（protocol `23.3.0`。境の項目だけ） |
| --- | --- | --- |
| Minecraft | `sb-beta`：McRemote `2400.0.0rc1`（公開VPS、新しいworld） | `sb-lts`：McRemote `2321.2.0`（有料GAMEs） |
| Unity箱庭 | `unity-sb`：`candidate-6ce475e`（公開VPS、外のport `25586`） | `unity-sb-lts`：`candidate-1594805-2`（外のport `25585`。真っ黒になった`candidate-1594805`を作り直したもの。25） |
| Web | `scratch-beta`、`wirescope-beta` | `scratch`（`2321.1.0`） |

- Scratch LANパッケージ：Scratchのpre-release `v2400.0.0rc1`のページから取る。入れる前にSHA-256を計って比べる（Windowsは
  PowerShellの`Get-FileHash`）
  - Linux x64：`mc-remote-scratch-LAN-2400.0.0rc1-linux-x64.zip` 274,192,377 bytes
    `35a576583fc0c61729ec044336d4167f8d448b56339db2031417a0e1baad130b`
  - Windows x64：`mc-remote-scratch-LAN-2400.0.0rc1-windows-x64.zip` 264,584,655 bytes
    `d49e1bac359d43caa1d2cbd8e31e47dc54cede0923ec7dee25d24821a30f12ea`
  - macOS arm64：`mc-remote-scratch-LAN-2400.0.0rc1-macos-arm64.zip` 268,936,322 bytes
    `8b1f272835f0e5297fa14e048e8c80f1d60c1267ba1af44d3e5ace227a592834`
- Python：`pip install minecraft-remote-api==2400.0.0rc1`。比べる相手は`2321.1.0`。venvを分ける
- 手元のUnity箱庭（14だけ）：
  `ghcr.io/naohiro2g/mc-remote-unity-sandbox@sha256:e39109f0e3ff6bbc9ef2a0f4fb6048735817fa250a5226b404430ace52101097`（loginなしで
  取れる）。たとえば`docker run --rm -p 8080:8080 -p 25585:25585 <このimage>`。containerを止めると、世界とtokenは消える
- 同じ端末でプレイヤーを替えるときは、前のtokenに気をつける（`2321.2`の試験の「2026-11-24〜25」。hub NOTESの「同じ端末で
  プレイヤーを替えると」の行）

## 始める前に採ること

- OSの版、browserとその版、Dockerの版、`sb-beta`のPaperのbuild
- `unity-sb`の`/healthz`の応答（`version` `2400.0.0rc1`、`protocol` `24.0.0`になっているか）

## 版と取り方

0. **版**：「はじめに.html」、LANとWebのScratchの画面、Unity Webのchatの最初の文（「ようこそ、Unity箱庭へ！ (v…)」）が
   `2400.0.0rc1`か
1. **取り方**：Chromeで、pre-releaseのページからLANのZIPを取れるか。止められたら、どう出たかを写す（`2321.2`の試験では、
   GitHubのActionsのartifactのZIPを、Chromeが危険なファイルとして止めた）

## LANの設定ページ（Ubuntu、Linux x64）

2. **冒頭の文**：Minecraftのserverならプレイヤーとして参加している必要があり、Unity箱庭ならマイクラのアカウントが要らない、と
   読めるか
3. **接続先を追加**：ボタンが一覧の上の右にあるか。押すと、足した接続先の表示名の欄にカーソルが移るか。`sb-beta`と`unity-sb`を
   足す
4. **前の版の設定**：`v2321.1.0`か`2321.2.0`の候補で接続先を設定していた機械なら、どう出るか（`v2321.1.0`のhostとportは、
   ID `local`の1件になるはず）

## 両方の接続先で（`sb-beta`、`unity-sb`。LANのUbuntuと`scratch-beta`）

5. **ペアリング**：miniのペアリングのcommandが1行で読めるか。「コピー」で、ゲームのchatかUnity Webのchatへ貼れるか。miniに出る
   serverの名前と版が、相手と合うか（McRemoteも、`2400.0.0rc1`から名前と版を返す）
6. **ペアリングの前に待つ**：`unity-sb`で、「接続する」の後、ペアリングのcommandを打つまで30秒より長く待つ。そのままペアリング
   できるか。できなければ、どう出たか（Unity箱庭は、何も送らない接続を30秒で切る。`2026-11-24-01`）
7. **WireScope**：「WireScopeを開く」の別窓で、helloの`protocol` `24.0.0`と、serverの名前と版が見えるか

## 操作のエラーの知らせ方（`2026-11-20-02`）

8〜13では、毎回、WireScope miniが開いて「最後の操作エラー」が約3秒強調されるか、上部の通知が出ないか（13を除く）を見る。
miniの文は、Scratchの返却の対応表（`handoff-materials/2026-11-20-scratch-2400-rc1/materials/NOTIFICATIONS_ja.md`）と比べる。

8. **世界の外（高さ）**：`sb-beta`でDEBUGにし、`y=320`へ1つ置く。「指定した高さ{y}は世界の外です。使える高さは{min}〜{max}です。」が
   出るか。強調が消えても詳細が残るか。低いwindowで「エラーの詳細」をスクロールしてコピーできるか。その後も普通に置けるか
9. **1回に置ける数**：1回の`setBlocks`で`0,0,0`〜`32,32,32`（35,937個）を指す。指定と上限の数が読めるか
10. **建築範囲**：`sb-beta`で、建築範囲の外へ置く。試せなければ、理由を書く
11. **世界の外（水平）**：`unity-sb`で`x=205`へ置く。世界の外と分かるか。世界の外周が補足に出るか
12. **使えない操作**：`unity-sb`でエンティティとパーティクルを出す。接続先の名前と、使えない操作の名前が出るか
13. **入力の誤りと未接続**：`unity-sb`で、向きにゼロのベクトルを渡す。入力の直し方が出て、上部と「次にすること」に接続の確認が
    出ないか。別に、未接続のまま操作を2回行い、上部の接続の案内が1回目だけ出るか
14. **送信が途切れたとき**（手元のUnity箱庭で）：LANの接続先に`127.0.0.1:25585`を足してペアリングし、FASTで大きめの範囲を
    置いている途中で、containerを止める。上部の通知で、
    送れていないのか、送った後の結果が分からないのかを読み分けられるか。イベントの取りこぼしと受信の停止は、起こせたら見る

## Unity箱庭（`unity-sb`）

15. **最初のカメラ**：開いた直後に北を向くか（HUDの方位が「北」か「N」。区画8のラベルが正立）
16. **見え方**：Scratchで原点の東（`x`が大きい側）に赤、北（`z`が小さい側）に青を置く。北を向いたとき、青が正面、赤が右に見えるか。
    東、南、西を向いても、右がそれぞれ南、西、北か（Minecraftと同じ）
17. **chatと建築**：Unity WebのchatでIMEの日本語を送れるか。置いたブロックがすぐ出るか。Scratchのchatのhatが動くか。
    Unity Webで歩いても、Scratchのプレイヤーの位置と向きのレポーターは変わらない（知っている不具合で、`2401`で直す。hub NOTESの行）

## Pythonと、版の境

18. **Python**：`2400.0.0rc1`で`sb-beta`と`unity-sb`へつなぎ、chatと`setBlock`が通るか
19. **版が合わないとき（Python）**：`2400.0.0rc1`を`sb-lts`へ、`2321.1.0`を`sb-beta`へ向ける。どう出るかを、そのまま写す。今の
    表示は`[protocol_mismatch] protocol_mismatch`で、双方の版は例外の`data`にだけ入る。文を直すのは`2401`（hub NOTESの
    2026-11-20の行）。分かりにくさの感想も書く
20. **版が合わないとき（Scratch）**：LANのrc1で、接続先を`sb-lts`か`unity-sb-lts`にする。版が合わないと分かり、操作が始まらないか

## Windows（とmacOS）のLANパッケージ

21. **Windows**：Windows x64のZIPを展開して起動する。`sb-beta`と`unity-sb`の両方へつながるか。WireScopeの別窓が開くか。終わった
    後に、`8601`、`8602`、`8603`が閉じるか
22. **macOS**（使える機械があれば）：21と同じこと。加えて、手元のUnity箱庭に対し、Unity WebをIPで開くか`名前.local`で開くかと、
    Scratchの接続先をIPにするか`名前.local`にするかの4通りで、ペアリングできるか。時刻と、名前が引けたaddress（IPv4かIPv6か）を
    書く（`2321.2`の試験の23。担当の手元では再現していない）

## Web（`scratch-beta`、`wirescope-beta`）

23. **接続先の一覧**：`scratch-beta`の一覧が`sb-beta`と`unity-sb`か。`scratch`（`2321.1.0`）の一覧が`sb`と`unity-sb-lts`か
24. **wirescope-beta**：開いて、Scratchの操作が見えるか

## LTSのUnity箱庭（imageを替えた後）

25. **LTSのUnity箱庭**：Stackが`unity-sb-lts`を`candidate-1594805-2`へ替えた後に開いて、ロゴの後に世界が見えるか（替える前の
    `candidate-1594805`は真っ黒になった。hub gate notesの「Stackの返却の照合（2026-11-26）」）

## 範囲の外

- Scratch：GUIとVMのtest、release metadataの契約、LinuxのZIPの起動と終了は、CIで確かめた。前の版の設定の読み替えを外すと
  testが落ちることは、担当が見た（`2400-set-1`の「Scratchの6」）
- 配布物とimage：bytes、SHA-256、OCIのdigestとlabelは、coordinatorが照合した
- Unity箱庭の上限：5つの自己攻撃の確かめは、Stackの票（「上限の対策版へ替える（2026-11-24に足した）」）で行う
- `-beta`の組のdoctorと、runtime config（`schema_version: 2`）は、Stackの票で確かめる
- McRemoteの中身は`2321.2.0`と同じで、版とprotocolとhelloの`server`だけが違う。McRemoteで変わったところは、`2321.2`の実施票
  （`00-hub/23212-gate-live-test-instructions_ja.md`）で見た
- Java、TypeScript、C#は、12月1日の公開を止める条件にしない。`sb-beta`へつなぐ試験は、別に頼む

## 記録してほしいこと

- 番号ごとに、できたか、できなかったか、気づいたこと。画面の写真は、errorの表示、上部の通知、Unity Web、設定ページ
- できなかったときは、そこで止めて、その番号と画面をcoordinatorへ渡す
