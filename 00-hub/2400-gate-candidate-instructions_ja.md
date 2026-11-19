# `2400`の候補を作る依頼（McRemote、Python、Scratch、minecraft-remote-tooling、Unity箱庭、Java、TypeScript、C#）

> 2026-11-19に、`2400.0.0`を12月1日0時（JST）に出すと決めた（`2026-11-19-01`）。中身は`2321.2`のために作ったもので、版を
> `2400.0.0`、helloの`protocol`を`24.0.0`にする。同じ日に、LTSとしてMcRemoteとUnity箱庭の`2321.2.0`を出す（`2026-11-19-02`）。
> gateは`00-hub/release-gate-notes_ja.md`の「2026-11-19 `2400`横断release gate」。参照するknowledge commitは、この依頼が入った
> mainのcommitです。

## 全componentで共通

- 版：rcは`2400.0.0rc1`（tagは`v2400.0.0rc1`）、最後は`2400.0.0`（`10-protocol/versioning-design_ja.md` §10.5）。最後の候補は、
  最後のrcと同じsourceで、版だけを変えて作る
- helloの`protocol`は`24.0.0`。互換はmajorの一致で判定する（§8.2）ので、`23.x`の相手とはつながらない。clientは`24.0.0`を
  申告する
- 中身は、版とprotocolのほかは変えない（下の各節に書いたものを除く）。`24.0.0`の中身は`23.3.0`と同じで、壊す変更は無い
- knowledgeの共有fixtureやwireの例に版が入っているところは、coordinatorが合わせる。componentのtestで変えたところは返却に書く
- rc1は、GitHubのpre-release（Latestにしない）で出す。PythonはPyPIのpre-release、Unity箱庭はGHCRの候補のtag。rc1は11月中に
  `sb-beta`、`scratch-beta`、`wirescope-beta`で動かし、human ownerがそこで試す（Stackへの票は`00-hub/2400-gate-stack-instructions_ja.md`）
- CIのrunnerは`ubuntu-24.04`のまま（hub NOTES 2026-11-10のrunnerの行）
- 12月1日の0時には、下書きにしたReleaseを公開するだけで済むようにする

日程：

| 日 | すること |
| --- | --- |
| 11/24（火）まで | rc1の返却 |
| 11/25 | coordinatorが照合して凍結。pre-releaseで出し、`-beta`で動かす |
| 11/26〜27 | human ownerの試験。11/27に、延期するかを決める（延期なら12月5日） |
| 11/28〜29 | 直しがあればrc2。最後の候補（`2400.0.0`）を作り、Releaseを下書きにする |
| 12/1 0:00 | 公開 |

返却（共通）：

- 実際に読んだknowledge commit
- 候補のcommit、branch、PR、CIのrun、artifactのIDとdigest、配布物の名前とbytesとSHA-256（全桁）
- base（下の各節）から変えたものの一覧
- helloの`protocol`と版を確かめたtestと、`23.x`の相手を断るtest。断る処理を外すとそのtestが落ちることを見たか
- 公開の手順の案（tag、Release、Latest、`manifest.json`、配布物。12月1日の0時にすること）

## McRemote

- base：`release/2321.2.0@2ccf0b1aba6008c314abe6df4d19b6fffb60ff58`（`2321.2-set-1`で凍結したもの）
- 足すもの：版、helloの`protocol` `24.0.0`、helloの応答の`server`（`{"name": "McRemote", "version": "<pluginの版>"}`、
  `2026-11-14-03`②）
- Paperの自動の確認は、1.21.11 #132と26.3 #244で
- LTS：`2321.2.0`は、凍結したartifact（`14147053531`、`mc-remote-2321.2.0.jar` 348,720 bytes
  `16e927a79ea9b9ae9f1aa544cd5101eb3a6c39228ef9c0da7175853d100703f8`）のまま、12月1日に出す。作り直さない
- 12月1日に2つの版を出す：GitHubのLatestは`2400.0.0`。`2321.2.0`はLatestにしない。`manifest.json`をどうするかの案
- BANで拒む経路の直しとkeepaliveは入れない（後の版）

返却に足すもの：helloの応答の例（`server`を含む）、`2321.2.0`と`2400.0.0`を同じ日に出す手順の案

## Python（`minecraft-remote-api`）

- base：tag `v2321.1.0`。`2321.2`の範囲には入っていなかった
- 足すもの：版、申告する`protocol` `24.0.0`、helloの互換の判定（major 24）
- `v2321.1.0`の後にmainへ入ったものは、一覧にして返す。入れるかは、human ownerと決める
- starterの既定の接続先は`sb`のまま（`2026-11-16-05`④）。12月1日から`sb`は`2400`になる
- rc1はPyPIのpre-release、`2400.0.0`は12月1日の0時にPyPIへ

返却に足すもの：`2321.1.0`のPythonが`2400`のserverへつないだときと、`2400`のPythonが`2321`のserver（`sb-lts`）へつないだときに
出る文（ホームページの説明に使う）

## Scratch

- base：`develop`（PR #38のmerge `8895313602301cf9561ab9ad9180582db1d5dad1`）
- 足すもの：版、申告する`protocol` `24.0.0`、toolingの`2400.0.0rc1`の候補の固定（`mc-remote/tooling-lock.json`）、下の直し
- ブロック一覧は、候補のcommitから`2400.0.0`で作り直す（一覧の`protocol`は`24.0.0`）。「Unity」の絞り込みの基準は、
  Unity箱庭の`2400`の候補のsource（応えるmethodは変わらない）。Stackの取り込みの条件は前と同じ
  （`00-hub/23212-gate-candidate-instructions_ja.md`の「Scratchの作り直し（2026-11-16）」）

直すもの（`2321.2-set-1`の人間の試験。記録は`14-evidence/records/2026-11-19-23212-scratch-unity-live-human_ja.md`）：

1. **ブロックを置く操作の拒否を、miniに出す**：DEBUGで`world.setBlock`と`world.setBlocks`が`out_of_bounds`、
   `block_count_limit_exceeded`、`build_range_exceeded`で拒まれても、miniに何も出なかった（試験の8、9、16の`x=205`、17。Minecraftと
   Unity箱庭の両方）。WireScopeの別窓では、どれも`data`まで読めた。前の返却の`CHANGE_SUMMARY_ja.md`は「WireScope mini：未対応操作、
   世界/建築範囲外、個数上限の原因・座標・範囲・数値を表示」と書いている。Scratch担当の説明（human ownerが会話に貼った）では、
   この2つのmethodの拒否を「最後のエラー」に渡していない。拒まれた後に作品が次へ進むことは、今のまま
2. **接続先が応えないmethodを、miniに出す**：Unity箱庭で`world.spawnEntity`と`world.spawnParticle`が`method_not_found`
   （`-32601`）を返しても、miniに何も出なかった（15）
3. **入力の誤りに、接続の案内を出さない**：Unity箱庭で`player.setDirection`にゼロのベクトルを渡すと、`zero_direction`
   （`-32602`）が返り、通知「操作に失敗しました。WireScope miniを開いて確認してください。」と、miniの「次にすること：接続を
   確認して、もう一度試してください。」が出た。原因は出なかった（16）。miniが詳しく説明する4種のほかのreasonでも、原因が
   分かるようにする
4. **設定ページ**（human owner 2026-11-18の提案）
   - 冒頭の文が、Minecraftだけを前提にしている。human ownerの文：「マイクラリモコンするとき、マイクラサーバーの場合は、
     そのマイクラ世界にプレイヤーとして参加している必要があります。Unity箱庭サーバーの場合は、マイクラアカウントが必要
     ありません。」
   - 「接続先を追加」を、一覧の上の右に置く（今の位置では、何度も足す間違いが起きやすい）。押したら、足した接続先の入力欄へ
     フォーカスを移す

確かめてほしいこと：

5. **ペアリングと、接続先のhostの書き方**（試験の23、macOS）：Unity WebをIPアドレスで開き、Scratchの接続先のhostを機械の
   名前（mDNSの`.local`）にすると、ペアリングできなかった。Unity Webも名前で開くと、ペアリングできた。ペアリングの後は、
   接続先ごとにtokenを持ち、IPアドレスの接続先と名前の接続先のどちらもつながった（human owner「開いたときのアドレス、名前が
   一致しないとだめ。」）。同じ試験で、WindowsからUnity箱庭の機械のDockerの公開portへ、IPv6ではつながらず、IPv4ではつながった。
   名前がIPv6に引かれた影響かは、分けていない。再現して、原因がScratch、Bridge、Unity箱庭のどこにあるかを返す。Unity箱庭へも
   同じことを頼んでいる。Bridgeを直す必要が分かったら、直す前にcoordinatorへ返す
6. **前の版の設定の読み替え**（試験の3）：`v2321.1.0`の`host`と`port`の設定を、ID `local`の1件へ読み替えることは、前の版の
   設定を持つ機械が無く、人の試験で確かめられなかった。どのtestで確かめているか。testが無ければ足し、読み替えを外すと落ちる
   ことを見る

返却に足すもの：Scratch OCIのdigest、`candidate-manifest.json`、1〜4で変えたものと、reasonごとにminiと通知に出る文、5の結果、
6のtestの名前、ブロック一覧の`release`と`sourceCommit`、`05f7326`から変わったもの（Release本文の材料）、人間の試験の手順の案

## minecraft-remote-tooling

- base：`agent/tooling-23212-candidate-20261117@37a4e79f7536b4b4a5cc9eeb7a2470b1d622a726`（PR #13）
- 足すもの：版（Bridge OCIのlabel、WireScope）
- BridgeとWireScopeに、protocolの版（`23.x`）に頼るところがあるかを確かめる。あれば返却に書く

返却に足すもの：Bridge OCIのdigest、WireScopeのZIPとmanifestのbytesとSHA-256（全桁）

## Unity箱庭

同じsourceから、2つのimageを作る。

| 用途 | 版 | helloの`protocol` | 動かす名前 |
| --- | --- | --- | --- |
| LTS | `2321.2.0` | `23.3.0` | `unity-sb-lts` |
| 最新版 | `2400.0.0rc1`、最後は`2400.0.0` | `24.0.0` | `unity-sb`（rc1は11月中に試す場所） |

- LTSの`2321.2.0`：PR #4（head `be17313007155227a46098e7b8c85c381a0dd3f3`）の上に、Unity WebのIMEの直しを積む。いま実機で確かめて
  いるもの（human owner 2026-11-19、Ubuntuでうまく動いた。Windows、macOS、iPadでも試す）
- ほかに入れてよいもの：ほかのcomponentの候補と凍結の照合を、そのまま使えるもの。helloの形、errorの形、応えるmethod（今の20）、
  portの既定、user、`licenses`のlabelは変えない。ブロックの追加は12月12日の版へ回す（human owner 2026-11-19）ので、catalogは
  基本の10種類のまま。迷うものは、human ownerと相談する
- 最新版の`2400`：LTSのcommitの上で、版とhelloの`protocol`だけを変える
- それぞれのcommitから、WebGLのbuildとimageのbuildを行い、`candidate-<commitの先頭7桁>`でGHCRへpushする（`2026-11-17-02`）。
  12月1日に、LTSのdigestへ`v2321.2.0`、最新版の最後のdigestへ`v2400.0.0`のtagを足す
- `candidate-be17313`は、公開VPSが12月1日まで動かしているので消さない

確かめてほしいこと：Scratchの節の5と同じ観察。Unity Webを開いたhostと、Bridgeがつないだhostが違うことが、Unity箱庭の側で
ペアリングに関わるか

返却に足すもの：

- 2つのimageそれぞれの、commit、GHCRのtag、indexのdigest、linux/amd64のmanifestのdigest、configのdigest、labelの全部、
  configの`User`、`THIRD-PARTY-NOTICES.txt`のbytesとSHA-256（全桁）、loginなしでpullできたこと
- 2つのcommitの差（版とprotocolだけか）
- `be17313`から入れたものの一覧（何が変わるか、安全と言える理由）と、入れなかったもの
- `/healthz`の応答、helloの`server.version`と`protocol`、`catalog.get`の`catalog_hash`、応えるmethodの一覧（前の20と同じか）
- IMEを確かめたOSとbrowser

## Java、TypeScript、C#（Client Library）

- `2400`に揃える（`2026-11-19-01`①）。sourceとtestを、申告する`protocol` `24.0.0`、helloの互換の判定（major 24）、版`2400.0.0`に
  する。公開のreleaseはせず、GitHubのtag `v2400.0.0`までにする。package registry（Maven、npm、NuGet）には出さない
- base：それぞれの今の`main`
- 11月25日から、`sb-beta`で動く`2400.0.0rc1`のMcRemoteへつないで確かめる（hello、pairing、`setBlock`、`getBlock`）。12月1日の公開を
  止める条件にはしない
- tagは、12月1日に最新版を出した後に打つ
- 一緒に入れるもの（hub NOTES 2026-11-13の行。単独の票にしないと決めたもの）
  - C#：同じ接続で応答待ちの長さが違うとき、最短でなく最長に合わせる（`2026-11-13-01`）。「.NETコンソールで始める」の作例
    （`examples`）と導入の説明。最初の成功体験は「1ブロックを置いて読み戻す」（`18-csharp-client/README_ja.md`の「2つの始め方」）
  - TypeScript：C#の1つ目と同じことを確かめる。生存確認で切れたと判断するまでの約40秒を数分にし（`2026-11-13-02`）、codeの
    コメント「Linuxの既定で約12分」を直す

返却：

- 実際に読んだknowledge commit
- 揃えたcommit、PR、CIのrun
- 申告する版と互換の判定を確かめたtestと、`23.x`のserverを断ることを見たtest（断る処理を外すと落ちるか）
- `sb-beta`のrc1へつないだ結果
- 一緒に入れたものの結果

## coordinatorがすること

- 返却をGitHubのAPIで照合し、配布物を取り直して計る。Unity箱庭はloginなしでGHCRから取る
- そろったら、`2400.0.0rc1`のexact setと、LTSのUnity箱庭`2321.2.0`を凍結する
- 人間の試験の票を、rc1と`-beta`の名前で改める
- knowledge：wire §7.3、Protocol Inventory、API一覧（`api/23.3.0/`と`api/24.0.0/`）、versioning、`19-unity/README_ja.md`。
  ホームページ（LTSの説明を含む）の文を、11月25日ごろに見せる
