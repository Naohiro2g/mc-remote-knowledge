# `2321.2-set-1`のScratchとUnity箱庭の人の試験（2026-11-18〜19）

> test class: `live-human`（報告ベース）。`2321.2`横断release gate（`00-hub/release-gate-notes_ja.md`の2026-11-15の節）で、
> human ownerが実施票`00-hub/23212-gate-scratch-unity-test-instructions_ja.md`に沿って、凍結した`2321.2-set-1`のScratchのLAN
> パッケージとUnity箱庭のimageを、手元の機械で確かめた。結果と画面は、human ownerが会話に貼った。素材はGit外。IPアドレス、
> ホスト名、機器名、player名とUUID、token、ペアコードは収録しない。

## identity

- Scratch `05f7326`（`2321.2-set-1`）：LANのZIPのSHA-256は、使った3台で、それぞれ凍結した値と一致した
  - Linux x64 `651541f704cff1a392977d81da0cf4f6f99a006f5ac33297877d5f54b803bb20`
  - Windows x64 `1b75f50e2ccfbf3767c5ddeac014df8defeb0700c59127a6c01185dce85a2eaf`
  - macOS arm64 `8193e35c8e377e494ffa18dfe03f33b3036db6a90be5f1291c0c98e2118aced3`
- Unity箱庭 `be17313`：
  `ghcr.io/naohiro2g/mc-remote-unity-sandbox@sha256:eef8787de7f61f17e155742900a25013057e06a3b6c879f17d724e490b13460c`
- McRemote `2321.2.0`（`mc-remote-2321.2.0.jar`、`16e927a79ea9b9ae9f1aa544cd5101eb3a6c39228ef9c0da7175853d100703f8`）
- 実施票は1台の機械を想定していたが、2台で行った
  - 機械A（Scratch LANパッケージのLinux x64、Paper）：Ubuntu 24.04（kernel 7.0.0-38）、Chrome 156.0.8078.47。Paper 26.3 #244
    （`35a2d15`）、Temurin 25.0.5+8。プラグイン：McRemote 2321.2.0、Geyser-Spigot 2.12.1-SNAPSHOT、floodgate 2.2.5-SNAPSHOT（b141）、
    ViaVersion 5.12.3-SNAPSHOT、ViaBackwards 5.12.3-SNAPSHOT、WorldEdit 7.4.6、AdvancedPortals 2.8.0
  - 機械B（Unity箱庭）：Ubuntu 24.04（kernel 7.0.0-43）、Docker 29.10.0。`docker run`で動かした。`/healthz`は
    `{"status":"ok","version":"2321.2.0","protocol":"23.3.0","worldEpoch":1,"seq":0,"connections":0,"tcpPort":25585}`
  - Windows x64とmacOS arm64のPC（22、23）。それぞれChromeを使った
- helloの応答：McRemoteは`protocol` `23.3.0`、`mc_version` `26.3`、`server`なし、`permissions.buildRange` 1000。Unity箱庭は
  `protocol` `23.3.0`、`mc_version` `1.21.11`、`supported_mc_versions` `["1.21.11"]`、`server`
  `{"name":"mc-remote-unity-sandbox","version":"2321.2.0"}`、`origin` `[0,0,0]`

## 結果

| 項目 | 結果 |
| --- | --- |
| 0 版 | できた。設定ページ、Scratchの「について」、「はじめに.html」が`2321.2.0` |
| 1 起動 | できた。接続先はMinecraft（`127.0.0.1:25575`、既定）とUnity箱庭（`127.0.0.1:25585`） |
| 2 一覧を変える | できた。追加、表示名とhostとportの変更、既定の移動、削除、ランチャーを起動し直した後の保存。IDは設定ページに出ず、miniの「設定先」に出る（`minecraft`、`unity`、足したものは`target-<uuid>`）。hostを変えてもIDは変わらない |
| 3 前の版の設定 | 確かめられなかった。3台とも、`v2321.1.0`の設定が無いか、既定と同じ値だった |
| 4 切り替え | できた。メニューで選ぶと、miniの「設定先」が変わり「再接続 要」になり、つなぎ直すと「実接続先」が変わる。Minecraft→Unity箱庭→Minecraftで、選んだ相手に届き、作品は残った。Minecraftへ戻ったとき、ペアリングし直さずにつながった |
| 5 ペアリング | できた（両方）。Unity箱庭では、miniに「サーバー実装 / 版」として`mc-remote-unity-sandbox / 2321.2.0`が出た。Minecraftでは、その行が出ない |
| 6 picker | できた（両方）。カタログの表示のhashは、helloの`catalog_hash`と合う。Minecraftは1,286件で、状態を指定した階段を置いて読むと、IDと状態が合う。Unity箱庭は10件で、`tnt[unstable=true]`を置いて読むと合い、Unity Webに出た。無い状態（`axis`）を読むreporterは`[[mcr-error:unknown_state_property]]`を返す |
| 7 FAST | できた（両方）。27個を置き、待った後に読み返して「違う」は0。比べる相手を変えると27になる |
| 8 世界の外 | serverはできた。Scratchの表示はできなかった。高さ320への`setBlock`は、どちらも`out_of_bounds`（`bounds`の`y_min` -64、`y_max` 319。`world_border`はMinecraftが`size` 59,999,968、Unity箱庭が中心`(0, 0)`、`size` 400）。319には置けた。miniを開いた状態でやり直しても、miniに何も出なかった |
| 9 1回に置ける数 | serverはできた。Scratchの表示はできなかった。35,937個の`setBlocks`は、どちらも`block_count_limit_exceeded`（`limit` 32,768、`requested` 35,937）で、何も置かれない。その後の3,267個は置けた。miniに何も出なかった |
| 10 WireScope | できた。別窓の接続元のIDがminiと同じ。Unity箱庭のserverの名前と版がminiと合う。8と9のerrorの`data`が読める |
| 11 Unity Web | できた。HUDの日本語と英語が背景に対して読める。ボタン、区画、操作説明、chatの見出しも切り替わる |
| 12 建築 | できた。`build.setDimension`は`overworld`で成功し、`the_nether`と`the_end`は`unknown_dimension`（wire §7.3の基本のreason）。`build.setOrigin`が効く |
| 13 プレイヤー | できた。位置、姿勢、向きの設定と読み取りが合う（向きは正規化した値で返る）。地面の高さは2種とも wire §5.6のとおり（非passableで、直上がpassableの最上のblock。`max_y`を含む）。範囲の取得は5×8×5で200件。カタログはブロック10件、エンティティ0件 |
| 14 チャット | できた。Scratchからのchatが出て、Unity Webからのchatで、Scratchの「チャットが投稿されたとき」が動く。Unity Webのchatの入力欄で、日本語のIMEが使えない（Ubuntu、Windows）。日本語の表示と、貼り付けての送信はできる |
| 15 使えない操作 | serverはできた。Scratchの表示はできなかった。`world.spawnEntity`と`world.spawnParticle`は`method_not_found`（`-32601`）。miniに何も出なかった |
| 16 世界の端 | serverはできた。Scratchの表示はできなかった。`x=205`は`out_of_bounds`（`size` 400）で、miniに何も出なかった。ゼロのベクトルの`player.setDirection`は`zero_direction`（`-32602`）で、通知「操作に失敗しました。WireScope miniを開いて確認してください。」と、miniの「次にすること：接続を確認して、もう一度試してください。」が出て、原因は出なかった。作品は止まらずに進んだ |
| 17 建築範囲 | serverはできた。Scratchの表示はできなかった。範囲の外への`setBlock`は`build_range_exceeded`（`bounds`の`build_range` 1000と建築の原点、`violating`は絶対座標）。通知もminiの表示も無かった |
| 18 パレット | できた。列へドラッグして消したブロックは、右クリックの「取り消し」で戻る。編集メニューの「削除の取り消し」では戻らず、標準のブロックも、本家のScratchも同じ |
| 19 並びと文言 | できた |
| 20 狭い画面 | できた。低いwindowでは、まず検索結果の一覧が縮み、さらに低いとdialog全体がscrollする |
| 21 作品 | できた。`v2321.1.0`のペアリングの3ブロックを使う作品も読み込んで動き、値は空になる。パレットにその3つは無い |
| 22 Windows | できた。両方の接続先へペアリングしてつながり、WireScopeの別窓が開く。終わった後に`8601`、`8602`、`8603`が閉じる |
| 23 macOS | できた。WireScopeの別窓と、portが閉じることも同じ。Unity箱庭へのペアリングでは、下の「見つかったこと」の3 |

## 見つかったこと

1. Scratchは、`world.setBlock`と`world.setBlocks`の拒否と、`method_not_found`を、miniに出さない（8、9、15、16、17）。返却の
   `CHANGE_SUMMARY_ja.md`の「WireScope mini：未対応操作、世界/建築範囲外、個数上限の原因・座標・範囲・数値を表示」と違う。
   Scratch担当の説明（human ownerが貼った）：miniは、Scratchが画面のために渡した「最後のエラー」の要約を出す。`setBlock`と
   `setBlocks`はDEBUGとTRACEで拒まれると開発者consoleに警告して次へ進み（前からの形）、その拒否を「最後のエラー」に渡して
   いなかった。`method_not_found`が出ないことと、`zero_direction`の案内は、その説明に含まれていない
2. `zero_direction`（入力の誤り）に、接続を確かめる案内が出る（16）
3. macOSで、Unity WebをIPアドレスで開き、Scratchの接続先のhostを機械の名前（mDNSの`.local`）にすると、ペアリングできなかった。
   Unity Webも名前で開くと、できた。ペアリングの後は、接続先ごとにtokenを持ち、どちらの接続先もつながる（human owner
   「開いたときのアドレス、名前が一致しないとだめ。」）。原因のcomponentは分かっていない
4. WindowsからUnity箱庭の機械のDockerの公開port（`25585`）へは、IPv6でつながらず、IPv4でつながった
5. macOSのChromeは、名前で開いたUnity Webをhttpsへ切り替え、`ERR_SSL_PROTOCOL_ERROR`で開けなかった。`http://`と書くと開いた
6. Chromeが、GitHubのActionsのartifactのZIPのダウンロードを、危険なファイルとして止めた（Ubuntu、Windows）
7. 設定ページの冒頭の文が、Minecraftだけを前提にしている（「そのマイクラ世界にプレイヤーとして参加している必要」）。
   human ownerの文の案：「マイクラリモコンするとき、マイクラサーバーの場合は、そのマイクラ世界にプレイヤーとして参加している
   必要があります。Unity箱庭サーバーの場合は、マイクラアカウントが必要ありません。」。「接続先を追加」の位置にも、human ownerの
   提案：「[接続先を追加]を上部右側に表示したほうが良い。今の位置にあると、おそらく、何度も追加する間違いが起きやすい。追加
   ボタンを押したら、新しいエントリーのフォームにフォーカス。」
8. Unity Webのchatで、原点の同期が「[ペアリング]」の札で出る。言語を切り替える前の行は、前の言語のまま残る。human owner：
   「Unity箱庭 チャットのラベルはデバッグを兼ねて内部情報そのまま、ということにしている。内部カテゴリー、表示ラベルについては
   後続検討。」
9. errorの`message`は、McRemoteが`out_of_bounds`（reasonと同じ）、Unity箱庭が`out of bounds`（空白の英語）。どちらも
   「`message`は英語の短文、分岐は`data.reason`」（`2026-06-27-03`）に合う
10. 実施票の12の「原点と向きの設定」は誤りで、`build.setDimension`は次元の設定

## human ownerの判断

- 2026-11-19：「Scratchを2321.2で直す。やり直し。」「unityの実装は終わったので、両方作り直そう。」。同じ日に、`2400.0.0`を
  12月1日に出すと決めた（`2026-11-19-01`）。Scratchの直しは`2400`の候補に入れる（`00-hub/2400-gate-candidate-instructions_ja.md`）。
  LTSとして、McRemote `2321.2.0`と、Unity WebのIMEを直したUnity箱庭`2321.2.0`を出す（`2026-11-19-02`）
- Unity WebのchatのIMEは、作り直しに入れる（human owner「IME対応はすぐにできそうなので、実装中」。2026-11-19に、Ubuntuで
  うまく動いた）。Unity箱庭のブロックの追加は、12月12日の版へ回す
- Unity Webのchatの札は後で考える（hub NOTESの行）
