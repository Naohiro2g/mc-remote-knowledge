# rc1横断release gate 確認票依頼

> rc1横断release gate（`00-hub/release-gate-notes_ja.md`の2026-10-17の節）を開いたときに、各担当へ出す確認票の依頼です。
> 参照するknowledge commitは、この依頼が入ったmainのcommitです。各担当は、自分の節と「共通」を読んで確認票を返して
> ください。

## 共通

- rc1は、protocolをパッチで`23.2.1`へ上げ、artifact `2321.0.0rc1`とする（`2026-10-17-03`）。APIとwireの中身は変えない。b9で
  `chat.post`の成功resultを`null`に決めた修正を番号に刻み、2320の版と切り分ける。GitHubのpre-releaseで出す
- 互換判定は「メジャー一致、`plugin.minor >= client.minor`、パッチは問わない」（versioning §8）。23.2.1のcomponentは、
  23.2.0のcomponent（McRemote b10、Python b9、Scratch b10）とそのまま話せることが前提
- 日程：目標は10/24（`2026-10-13-06`）。厳しければ、2321への切り替えを落とさず日程をずらす（`2026-10-17-03`）。
  **確認票の返却の目安は10/19**
- rc1の目的：外部testerが会話履歴なしで開始・更新・復旧・feedbackできる入口を用意する（grand-design roadmap §4）。
  ホームページの入口は`https://mc-remote.com/#lan`と`https://mc-remote.com/lan/scratch/`（`2026-10-17-02`）

各担当に共通で聞くこと:

- b10の公開後に、default branchへ入ったもの（commitと一行の説明）。rc1で出すつもりのもの
- `23.2.0` → `23.2.1`の変更範囲：protocolの定数、helloで送る／返す版、互換判定とそのtest、共有fixture、artifactや配布物の名前、
  README等の記述。変える箇所の一覧と、手間の見積もり
- READMEの人間向け再編（hub NOTES 2026-08-28 `[priority]`）で残っているもの。初めて読む人が通せるかの確認（Pass C）を
  どう行うか
- 10/24に対する見込みと、止まっている点

返却は`release-gate-notes_ja.md`の確認票の形式。`knowledge contract commit`には実際に読んだSHAを書く。自repoの事実と根拠
だけを返し、他repoへの着手、shared環境の変更、人間参加の試験、tag／releaseの公開はしない。この票では調べて返すだけで、
版の変更には着手しない（着手依頼は返却を受けて出す）。

## McRemote

- 23.2.1のMcRemoteが、23.2.0のclient（Python b9、Scratch b10）のhelloを受け入れることを、どのtestで確かめられるか
- 対応版はrc1では1.21.11と26.3のまま（`2026-10-13-07`）。対応版を1.21.11、26.1.2、26.2、26.3へ広げる検討（各系列の最終版の
  最終buildをsupportする方針）は、rc1の後の検討として、別に搬送票で出してほしい（human owner 2026-10-17、hub NOTES）
- READMEのmiseの手順：Git Bashでのmiseの不具合（`C:\...`と`/c/...`のpathの変換）と、shimsへpathを通す形（human ownerの手元で
  直った方法）に照らして、今の手順で足りるか（hub NOTES 2026-10-17「Windowsの生徒のPCで要る実績」）
- READMEの導線：ホームページの`#lan`から「マイクラサーバーを用意する」でREADMEへ来た人が、迷わずクイックスタートへ
  進めるか。READMEからホームページの`/lan/scratch/`へ戻る導線を置く場所の案
- rollback（hub NOTES 2026-09-30「rc1のrollbackの範囲」）：rc1で起動した後にb10のJARへ戻したとき、config、credential、DBが
  そのまま使えるか。b8のような起動時のkeyの移し替えがrc1に無いか
- 未生成chunkへの操作の制限（hub NOTES 2026-10-07）：新しい拒否のreasonはwireの追加になるので、rc1には入れない案。採否に
  ついての意見だけ返す

## Python client

- 23.2.1への変更範囲（共通の問い）。同梱WireScopeを、toolingの新しいreleaseから作り直す手順
- PyPIへのrc1：GitHubのpre-releaseで試した後に、`2321.0.0rc1`をPyPIへ出す手順（`2026-10-13-05`、versioning §10.9）。
  案内は`uv add "minecraft-remote-api==2321.0.0rc1"`の版の指定
- READMEの導線：自分のマイクラサーバーへの接続先の変え方（ホームページの`#lan`の「Pythonで使う」）と、READMEの記述が
  食い違わないか。ホームページへのリンクを置く場所の案
- rollback：clientの戻し方（版の指定し直し）が、手順書のどこに書いてあるか

## Scratch editor（minecraft-remote-tooling、LANパッケージ）

- tooling：protocolの定義、共有fixture、WireScope、Bridgeで、23.2.1へ変える箇所。toolingの新しいrelease（`2321.0.0rc1`）を
  作る手順と、ScratchとPythonがその固定へ切り替える手順
- Scratch：protocolの定数、LANパッケージのZIP名（`mc-remote-scratch-LAN-2321.0.0rc1-<os>-<arch>.zip`）と版のフォルダー。
  Scratchのアドレス（`127.0.0.1:8601`）は版をまたいで変えない（`13-scratch-client/scratch-lan-package-design_ja.md` §6）
- `はじめに.html`の文言（hub NOTES 2026-10-17「LANパッケージのランチャー、`はじめに.html`」の①）：冒頭は概略の流れだけにして、
  その後にOS別に分ける。macOSの許可の手順を実際に合わせる（警告の窓を閉じる、「このまま開く」を2回、管理者のパスワード）。
  設定画面のURLをリンクにし、画面の画像を置く。rc1に入れられるか。ホームページの`/lan/scratch/`との食い違いがあれば挙げる
- 製品notice（hub NOTES 2026-10-05「Scratchの製品noticeを一つに絞る」）：今の公開物で、製品noticeが一つのentryになって
  いるか
- OCIのversionラベルとmtime（hub NOTES 2026-10-05「Scratch OCIのversionラベル」）：candidateと公開で同じdigestにするための
  変更をrc1で入れられるか
- pickerのalias検索と読み上げ（hub NOTES 2026-08-19）：rc1に入れられるか。aliasに登録する語はhuman ownerが選ぶので、
  選ぶための候補の形（一覧の置き場所と書式）を返す
- READMEの導線：READMEからホームページの`/lan/scratch/`へのリンクを置く場所の案

## Stack

- rollback（hub NOTES 2026-09-30「rc1のrollbackの範囲」）：同じenvironmentへ1つ前のpreset／lockをapplyして、既存のworld、
  config、credentialのまま動かせるか。今の経路でできるか
- 箱庭サーバー（VPSベータ）をrc1で26.3へ移す場合（human owner 2026-10-17の見込み。決めるのはhuman owner）：Minecraftの版を
  またぐworldの扱い（`2026-08-25-02`）と、Stackの経路で行う手順
- rc1のpreset／lock（`2321.0.0rc1`のset）を作る手順で、b10から変わるところ

## Java client（gateの条件にしない）

参加しない（`2026-09-30-04`）。protocol `23.2.1`への追従は、初回stableの後の追従で行う。
