# 2321.2 ScratchとUnity箱庭の実施票（human owner 向け）

- 根拠: `00-hub/release-gate-notes_ja.md`「2026-11-15 `2321.2`横断release gate」（範囲、凍結するexact set `2321.2-set-1`）、
  DECISIONS `2026-11-14-01`（Unity箱庭が応えるもの）、`2026-11-15-01`（port `25585`）、`2026-11-16-01`（接続先の一覧）、
  `2026-11-17-01`、hub NOTESの2026-11-16の行「Scratchの、Unity箱庭に向けた変更」
- 目的: Scratch `2321.2.0`で変わったところ（接続先の一覧と切り替え、picker、パレット、errorの表示）と、Unity箱庭 `2321.2.0`を
  Scratchから使えることを、利用者と同じように確かめる
- test class: live-human。CIとunit、coordinatorの照合で確かめたことは繰り返さない（「範囲の外」）
- 結果に分類を設けず、判断は結果から行う
- 始める条件: 満たしている。凍結した値を、coordinatorがartifactを取り直して計り、GHCRのdigestで確かめた
- 進め方: McRemoteの実施票（`00-hub/23212-gate-live-test-instructions_ja.md`）と同じUbuntuの機械で、PaperとUnity箱庭を並べて
  動かす。Scratchは、その機械でLinuxのLANパッケージを、別のPCでWindowsのLANパッケージを使う
- 公開の`unity-sb`は、同じ版のUnity箱庭で、今の公開のWebのScratch（`v2321.1.0`）からつながる（human owner 2026-11-18）。この票は
  凍結したScratchの候補をLANパッケージで試すので、Unity箱庭も手元で動かして、そこへつなぐ

## 使うもの

- Scratch LANパッケージ（`05f7326`）：CIのrun <https://github.com/Naohiro2g/scratch-editor/actions/runs/44096287207> のartifact
  `scratch-candidate-05f7326663627dc9429f0513a2b832e797ad47f5`（ZIP 1,385,149,482 bytes。GitHubにloginして取る）。中の次のZIPを使う。
  入れる前にSHA-256を計って比べる（Windowsは PowerShellの`Get-FileHash`）
  - Linux x64：`mc-remote-scratch-LAN-2321.2.0-linux-x64.zip` 274,119,333 bytes
    `651541f704cff1a392977d81da0cf4f6f99a006f5ac33297877d5f54b803bb20`
  - Windows x64：`mc-remote-scratch-LAN-2321.2.0-windows-x64.zip` 264,511,615 bytes
    `1b75f50e2ccfbf3767c5ddeac014df8defeb0700c59127a6c01185dce85a2eaf`
  - macOS arm64：`mc-remote-scratch-LAN-2321.2.0-macos-arm64.zip` 268,863,280 bytes
    `8193e35c8e377e494ffa18dfe03f33b3036db6a90be5f1291c0c98e2118aced3`
- Unity箱庭（`be17313`）：
  `ghcr.io/naohiro2g/mc-remote-unity-sandbox@sha256:eef8787de7f61f17e155742900a25013057e06a3b6c879f17d724e490b13460c`
  （loginなしで取れる）。たとえば`docker run --rm -p 8080:8080 -p 25585:25585 <このimage>`。Unity Webは`http://<その機械>:8080/`、
  Scratchからは`25585`へつなぐ。containerを止めると、世界とtokenは消える
- McRemote：McRemoteの実施票と同じ（`2321.2.0`のJAR、Paper 26.3 #244、Java 25）
- 比べる相手：公開中の`v2321.1.0`のLANパッケージ

## 始める前に採ること

- OSの版、browserとその版、Dockerの版、Paperのbuild
- `http://<その機械>:8080/healthz`の応答（`version` `2321.2.0`、`protocol` `23.3.0`、`tcpPort` `25585`になっているか）

## 版

0. **版**：「はじめに.html」とScratchの画面の版が`2321.2.0`か

## LANのランチャーと接続先の一覧（Ubuntu、Linux x64）

1. **起動**：ZIPを展開して起動する。設定ページの接続先が、Minecraft（`127.0.0.1:25575`）とUnity箱庭（`127.0.0.1:25585`）の2つで、
   既定はMinecraftか
2. **一覧を変える**：接続先を1つ足して、消す。表示名、host、port、既定を変えられ、IDは変わらないか。ランチャーを起動し直しても
   残るか
3. **前の版の設定**：`v2321.1.0`で接続先を設定していたPCなら、その設定が一覧の1件（ID `local`）として出るか
4. **切り替え**：Scratchの接続先のメニューで、MinecraftとUnity箱庭を行き来する。選んだ相手に届くか。作品は保たれるか

## 両方の接続先で（Minecraft、Unity箱庭）

5. **ペアリング**：WireScope miniの案内でペアリングする。Minecraftはゲームのchat、Unity箱庭はUnity Webのchatに、miniに出る
   コマンドを打つ。Unity箱庭では、miniにserverの名前と版が出るか。Minecraftで、名前を推し量った表示が出ないか
6. **picker**：カタログのpickerで、接続先のブロックを選ぶ。状態のあるものも選ぶ。置いて取ると、IDと状態が合うか。Unity箱庭は
   基本の10種類
7. **FAST**：小さい範囲をFASTで置き、「送ったブロック設置が終わるまで待つ」の後に取って、全部置けたか
8. **世界の外**：DEBUGで`y=320`へ置く。世界の外という原因、座標、高さの範囲が読めるか。その後も普通に置けるか
9. **1回に置ける数**：原点を世界の中央寄りに置き、1回の`setBlocks`で`0,0,0`〜`32,32,32`（35,937個）を指す。要求の数と上限が
   読めるか。その後も普通に置けるか
10. **WireScope**：「WireScopeを開く」から別窓を開く。同じ接続の操作とerrorの`data`が見えるか。Unity箱庭のserverの名前と版が、
    miniと合うか

## Unity箱庭で

11. **Unity Web**：エラーなく起動するか。HUDの文字（日本語と英語）が、背景に対して読めるか。ペアリングのcodeと状態が見えるか
12. **建築**：置いたブロックが、Unity Webにすぐ出るか。原点と次元の設定（`build.setOrigin`、`build.setDimension`）が効くか
13. **プレイヤー**：位置、姿勢、向きの設定と読み取り、地面の高さの2種、範囲の取得を、短い作品で使う。設定した値と読んだ値が
    合うか
14. **チャット**：Scratchからのチャットが、Unity Webに出るか。ペアリングした画面からのチャットで、Scratchのチャットのhatが動くか
15. **使えない操作**：看板を読むなど、Unity箱庭が応えない操作で、今の接続先では使えないと分かるか
16. **世界の端**：`x=205`など水平の外でも、8と同じに分かるか。向きにゼロのベクトルを渡しても、作品が止まらずに原因が分かるか

## Minecraftで

17. **建築範囲**：McRemoteの実施票の10と同じ場面を、Scratchで試す。`build_range_exceeded`の説明と範囲が読めるか。試せなければ、
    理由を書く

## 画面と使い心地

18. **パレット**：「コード」のダブルクリックで開き閉じする。スクリプトを左寄りと右寄りに置いても、位置がずれないか。カテゴリーの
    列と追加ボタンは残るか。列へのドラッグで消し、「元に戻す」で戻るか。選んでいるカテゴリーを押しても開くか。列の空白の
    ダブルクリックでも開き閉じするか
19. **並びと文言**：指定した並びで、ブロックが探しやすいか。「自分だけ」の文言が自然か。バックパックが出ないか
20. **狭い画面**：幅800pxくらいで、作品の名前が読めるか。低いwindowでも、pickerのキャンセルと決定を押せるか
21. **作品**：作った作品を保存して開き直し、値、配置、実行が保たれるか。`v2321.1.0`で作った、ペアリングのブロック（(ペアコード)、
    (ペアリングコマンド)、{ペアリングできたとき}）を使う作品を開いて動かす。パレットにはその3つが無いか

## Windows（とmacOS）のLANパッケージ

22. **Windows**：Windows x64のZIPを展開して起動する。設定ページでhostをUbuntuの機械に変え、MinecraftとUnity箱庭の両方へつながるか。
    WireScopeの別窓が開くか。終わった後に、`8601`、`8602`、`8603`が閉じるか
23. **macOS**：使える機械があれば、macOS arm64のZIPで22と同じことを

## 公開の後

- タブレット（iPadのSafari、AndroidのChrome）：公開のWeb editorで、pickerの操作と、カテゴリーを押して開く操作。問題が出たら
  次の版で直す（`2321.1`と同じ扱い）
- ブロック一覧（ホームページの`/api/scratch/`）：「Unity」の絞り込みと検索で27 blockが出て、看板、音、エンティティなどが
  混ざらないか

## 範囲の外

- Scratch：GUIのChromiumとFirefoxのtest、VM、release metadataの契約、LinuxのZIPの起動と終了は、CIで確かめた
- Bridge：接続先の一覧を渡さずに環境変数だけで起動したときに、前と同じに動くことは、toolingの試験で確かめた
- Unity箱庭のimage：label、root以外のuser、`THIRD-PARTY-NOTICES.txt`の中身は、coordinatorがGHCRで照合した
- WebのScratch、Bridge、runtime config（`schema_version: 2`）の組と、公開VPSのUnity箱庭は、Stackの票で確かめる
- McRemoteで変わったところは、McRemoteの実施票で見る

## 記録してほしいこと

- 番号ごとに、できたか、できなかったか、気づいたこと。画面の写真は、errorの表示、Unity Web、設定ページ
- できなかったときは、そこで止めて、その番号と画面をcoordinatorへ渡す
