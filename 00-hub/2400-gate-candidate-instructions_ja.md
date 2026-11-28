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
  `16e927a79ea9b9ae9f1aa544cd5101eb3a6c39228ef9c0da7175853d100703f8`）のまま、11月25日に出す（`2026-11-21-01`。12月1日から改めた）。作り直さない
- 11月25日に`2321.2.0`を出し、12月1日に`2400.0.0`を出す。12月1日からのGitHubのLatestは`2400.0.0`。11月25日から30日まで
  `2321.2.0`をLatestにするか、`manifest.json`をどうするかの案（12月1日に2つの版を出すとしていたのを改めた）
- BANで拒む経路の直しとkeepaliveは入れない（後の版）

返却に足すもの：helloの応答の例（`server`を含む）、`2321.2.0`と`2400.0.0`を同じ日に出す手順の案

2026-11-20：返却を照合した。この候補（`d93f521`）を凍結に回す（`00-hub/release-gate-notes_ja.md`の「2026-11-19 `2400`横断
release gate」の「返却の照合（2026-11-20）」）。`2321.2.0`は、`2ccf0b1`に打ったtagでCIにbuildさせ、JARが凍結のものと全桁
同じなら、それを出す。同じbytesなので、上の「作り直さない」と同じことになる。合わなければ、凍結した5つのfileを出す。human
ownerが返却の案を採った

### `2321.2.0`は11月25日に（2026-11-21に足した）

`2026-11-21-01`。`2321.2.0`はLTSとして11月25日に出し、同じ日に、human ownerが有料GAMEsの`sb-lts`へ入れる。12月1日は`2400.0.0`
だけを出す。

- 出す前に、`2321.2`の人間の試験の残り（4、8〜11。`00-hub/release-gate-notes_ja.md`の`2321.2`の節の「人間の試験（McRemote、
  2026-11-17〜）」）を済ませる
- Releaseの文に、LTS（`2321`の系列）であることを書く（`2026-11-21-03`）

返却に足すもの：11月25日と12月1日に分けた公開の手順の案

## Python（`minecraft-remote-api`）

- base：tag `v2321.1.0`。`2321.2`の範囲には入っていなかった
- 足すもの：版、申告する`protocol` `24.0.0`、helloの互換の判定（major 24）
- `v2321.1.0`の後にmainへ入ったものは、一覧にして返す。入れるかは、human ownerと決める
- starterの既定の接続先は`sb`のまま（`2026-11-16-05`④）。12月1日から`sb`は`2400`になる
- rc1はPyPIのpre-release、`2400.0.0`は12月1日の0時にPyPIへ

返却に足すもの：`2321.1.0`のPythonが`2400`のserverへつないだときと、`2400`のPythonが`2321`のserver（`sb-lts`）へつないだときに
出る文（ホームページの説明に使う）

2026-11-20：返却を照合した。mainに入ったもの（PR #13〜#16）と、版が合わないときの例外の文は、`2400`に入れず`2401`で出すと
human ownerが決めた。この候補（`d0aae00`）を凍結に回す（`00-hub/release-gate-notes_ja.md`の「2026-11-19 `2400`横断release gate」の
「返却の照合（2026-11-20）」）

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

### 操作のエラーの知らせ方（2026-11-20に足した）

Scratchの確定搬送票で、知らせ方を決めた（`2026-11-20-02`）。1〜3は、この形で直す。候補は、搬送票のcommit
（`agent/scratch-2400-mini-diagnostics@671f5b3ce56f3374978e06e7e946f66d1216df0d`）から作る。同じcommitに入っている、miniのscroll、
ペアリングのcommandとエラーの詳細のコピー、1行のペアリングのcommandも、`2400`に入れる（human ownerが確認版で見た。human owner 2026-11-20「2400に入れます。」）。

返却に足すもの：

- 上の「reasonごとにminiと通知に出る文」を、`2026-11-20-02`の分け方（miniだけのもの、上部にも出るもの）で
- 未接続のときの上部の案内が、前と同じく、最初のcommandを実行したときだけか（`13-scratch-client/scratch-roadmap_ja.md`）
- `zero_direction`などの入力の誤りで、miniの「次にすること」が接続の確認を案内しないこと（3）

2026-11-20：返却を照合した。この候補（`0ae8af4`）とtoolingの候補（`541e7b3`）を凍結に回す（`00-hub/release-gate-notes_ja.md`の
「2026-11-19 `2400`横断release gate」の「返却の照合（2026-11-20）」）。6のtestで、読み替えを外すと落ちることを見てもらう
（候補のcodeは変えない）。「Unity」の絞り込みは、Unity箱庭の積み直した`2400`の候補と照合する

### 最後の候補のブロック一覧（2026-11-26に足した）

rc1のtag `v2400.0.0rc1`（`0ae8af418d095bac734f37bfca35804810ec1cae`）の`mc-remote/block-reference/site/`には、`2400.0.0`の一覧が
入っていない。入口の`site/blocks.json`は`release` `2321.2.0`、`protocol` `23.2.1`のまま。`2400.0.0`の一覧は、tagより3 commit先の
`agent/scratch-2400-block-reference@7a4a6db`にある（`site/2400.0.0/blocks.json` 88,687 bytes
`759573b6c8d8657c812428dccc3f4397644db4ea944c2723c9934ea07ab93dcb`、`release` `2400.0.0`、`protocol` `24.0.0`、`sourceCommit`
`0ae8af4`の全桁、53 block）。ホームページの`/api/scratch/`は、tagの`site/`と同じbytesのfileだけを取り込む（Stackの取り込みの条件）
ので、このままでは12月1日に取り込めない（human owner 2026-11-26「1〜3、それで進めてください」）。

- 最後の候補（`2400.0.0`、11/28〜29）のcommitに、`7a4a6db`の`site/2400.0.0/`を入れる。入口の`site/blocks.json`、`index.html`
  なども`2400.0.0`にする。rc1の後にブロックの定義が変わっていなければ、`sourceCommit`は`0ae8af4`のままでよい
- `site/2321.2.0/`は、ホームページへは取り込まない（Scratchの`2321.2.0`は出していない）。repoに残すかは任せる

返却に足すもの：最後の候補のcommitの`site/`のうち、`2400.0.0/blocks.json`と入口の`blocks.json`のbytes、SHA-256、`release`、
`protocol`、`sourceCommit`。`sourceCommit`から最後の候補までに、ブロックの定義が変わっていないこと

## minecraft-remote-tooling

- base：`agent/tooling-23212-candidate-20261117@37a4e79f7536b4b4a5cc9eeb7a2470b1d622a726`（PR #13）
- 足すもの：版（Bridge OCIのlabel、WireScope）
- BridgeとWireScopeに、protocolの版（`23.x`）に頼るところがあるかを確かめる。あれば返却に書く

返却に足すもの：Bridge OCIのdigest、WireScopeのZIPとmanifestのbytesとSHA-256（全桁）

2026-11-20：Scratchの返却に入っていたものを照合した。この候補（`541e7b3`）を凍結に回す（上のScratchの節と同じ記録）

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

### 座標の見え方の直し（2026-11-20に足した）

`2026-11-20-01`④。human owner 2026-11-20「鏡像の直しを12月1日に入れる。Unity箱庭の最初のカメラも北向きにする。」

- LTSの`2321.2.0`に入れる。最新版の`2400`は、その上で版とprotocolだけを変えるので、同じ直しが入る
- 右手系の見え方にする。北を向くと、東（+X）が右、上（+Y）が上、南（+Z）が手前に見える。今はMinecraftの座標を左手系の
  Unityへそのまま写していて、北を向くと東が左に見える（claude.aiが`d3539c3`のコードを読んで見たもの：`DemoCoordinates.Center`、
  北＝−Z、`mcYaw = −eulerY`）
- 最初のカメラは北を向く
- wireの値は変えない。座標、yawとpitch、向きのベクトル、`world.getHeight`は、今までどおりMcRemoteと同じ値を返す（wire §5）
- 説明は`00-hub/world-coordinates-facts_ja.md`（§2と図2が見え方、§4がマイクラリモコンの値）

返却に足すもの：

- 直したものの一覧と、testで確かめたこと（直しを外すと落ちるtestがあるか）
- 北、東、南、西を向いたとき、画面の右と左がどの方角か。最初のカメラの向き
- `player.setPose`と`player.getPose`のyaw、`player.setDirection`と`player.getDirection`のベクトルが、McRemoteと同じ値になるか
- Unity WebのHUDやchatに方位や向きの表示があれば、その値

### 外へ開けるときの上限（2026-11-20に足した）

公開VPSで、Unity箱庭のTCPを外へ開ける（`2026-11-20-03`。`unity-sb-lts`は`25585`、`unity-sb`は`25586`）。今の上限は、Unity Webの
側（WebSocketの接続と画面のIDごとに、codeの失敗は60秒で5回まで、`2026-11-17-04`④）だけが記録にある。外へ開けると、誰でも
TCPで直接つないで、pairingを始められる。

開ける前に、今のserverにある上限を返す：TCPの接続の数（送り元ごと、全体）、`auth.pairBegin`の回数と、承認を待つcodeの数、
1つの接続から送れる量。足りないものがあれば、足すかどうかと形をhuman ownerと相談する（仮実装を含む）。LTSの`2321.2.0`に入れる
ものは、最新版の`2400`にも入る

返却に足すもの：今ある上限とその値、確かめたtestの名前。足したものがあれば、その差分と、外すと落ちるtest

### 上限の対策版（2026-11-20に足した）

`2026-11-20-04`。返却（`f7d0f9a`と`1dc3cbd`）の照合は通った（`00-hub/release-gate-notes_ja.md`の「返却の照合（2026-11-20）」）。
この2つを2026-11-20に公開VPSで動かし、TCPを外へ開ける。数日のうちに、上限の対策を入れた版へ替える（human owner 2026-11-20
「数日の間に対策版をデプロイ。」）。凍結は、その版で照合する

- LTSの`2321.2.0`のcommitに入れ、その上に`2400.0.0rc1`を、版とprotocolだけを変えて積み直す（A案と同じ）
- 何を足すかと値は、human ownerと相談する。返却の7.2の案（TCPの接続の数、helloの前に待つ時間、`auth.pairBegin`の回数と待つcodeの
  数、1行の長さ）に、Unity Webの`/ws/sync`の受け取る長さと、pollされないと消えない待つcodeの記録を足して考える
- 上限に当たったときの振る舞いは、McRemoteの`2026-10-07-02`（認証の前は接続を閉じるだけ、新しいreasonを足さない）を見て、
  human ownerと相談する
- 公開VPSでhuman ownerが攻撃して確かめた結果は、Stackの返却から渡す

返却に足すもの：足した上限とその値、それぞれを外すと落ちるtest、2つのcommitとGHCRのtagとdigest（全桁）。版の文字列とhelloは、
今回の返却と同じ形で確かめる

### LTSの作り直し（2026-11-26に足した）

Stackが公開VPSで、LTSの`candidate-1594805`（`sha256:9bd2ec444d5cea362729bacbea4d1b8ccd6905b169a467aaa57cdb4b4d05e24a`）のUnity Webが、
ロゴの後で真っ黒になるのを見つけた（`mc-remote-stack`の`handoff-materials/2026-11-25-beta-rc1-and-unity-limits/materials/RETURN_ja.md`
の§2-3）。通常の窓でもシークレットウィンドウでも同じで、browserのConsoleに次の2行が出る。

- `The referenced script (Unknown) on this Behaviour is missing!`
- `The referenced script on this Behaviour (Game Object 'Local Sandbox Demo') is missing!`

imageの中の`/app/wwwroot/Build/`では、`WebGL.data`だけが違う（Stackが計った。公開VPSが返すfileも同じ）。`index.html`、
`WebGL.loader.js`、`WebGL.framework.js`、`WebGL.wasm`は、`1594805`と`f7d0f9a`で全バイト同じ。`1594805`は`unity/`を変えていない
（coordinatorの2026-11-24の照合）

| image | Unity Web | `WebGL.data` | `WebGL.wasm`のSHA-256 |
| --- | --- | --- | --- |
| `candidate-f7d0f9a` | 見える | 14,208,678 bytes `beb2edb6cfb901bab38cbb74091a27463134d17f90b60a6af966cfebd63abe90` | `2e2dbe830e8e52b1d7785423e9070315c65d64a87c287ed9de4da9628e35a0f8` |
| `candidate-1594805` | 真っ黒 | 14,207,012 bytes `54625694b8cb6fed8de56ba85d023c5a0cc124ef74eb7396a715c013658f23e5` | `2e2dbe830e8e52b1d7785423e9070315c65d64a87c287ed9de4da9628e35a0f8` |
| `candidate-6ce475e` | 見える | 14,208,716 bytes `8ba1065f3a7d1762b9cac9591aa7246411bfd6b89e27926ed898864533b130f1` | `655775cd95b027d10b1ffc4e215a3d29894c16a131762bf1110afd7518cf9a35` |

- 版は`2321.2.0`のまま、`1594805`のsourceから作り直す。期限は11月27日（human owner 2026-11-26。延期を決める日で、Stackが
  11/28〜29に検証機で12月1日の手順を通す）
- 姿勢の直し（hub NOTESの「Unity Webで歩いても、Scratchのプレイヤーの位置と向きが変わらない」）は入れない（human owner 2026-11-26）
- 直すのに新しいcommitが要るなら、`1594805`の上に積み、何を変えたかを返す
- 今の`candidate-1594805`のtagは動かさない（Stackが戻すときの記録に使っている）。同じcommitから作るなら、tagは
  `candidate-1594805-2`にする
- 公開VPSの`unity-sb-lts`は、coordinatorが照合してから、Stackが替える。rc1の`candidate-6ce475e`は替えない

確かめてほしいこと：

1. 新しいimageを手元で動かし、browserの通常の窓とシークレットウィンドウでUnity Webを開く。ロゴの後に世界が見え、chatで
   ペアリングできるか
2. `/app/wwwroot/Build/`の各fileのbytesとSHA-256を、`f7d0f9a`と`6ce475e`のものと比べる
3. 次に同じことが起きたとき、imageを出す前に気づける確かめ方の案。今の`1594805`で落ちることを見せる

返却に足すもの：原因、作り直したcommitとtag、indexとlinux/amd64のmanifestとconfigのdigest（全桁）、labelの`revision`と`version`、
`/healthz`とhelloの版とprotocol（`2321.2.0`、`23.3.0`）、上限のtestがそのまま通ること、上の1〜3の結果

2026-11-26に返り、照合した。`2400-set-1`のLTSを`candidate-1594805-2`へ替えた（`00-hub/release-gate-notes_ja.md`の「McRemote
`2321.2.0`と、LTSのUnity箱庭の作り直しの照合（2026-11-26）」）

### pushの前の2段の確かめ（2026-11-26に足した）

LTSの作り直しの返却で、担当が作った確かめ（`handoff-materials/2026-11-26-unity-lts-rebuild/materials/prepush_verify_webgl.md`）を、
次から毎回通す。12月1日の`2400.0.0`の最後のimageも（human owner 2026-11-26）

- (a) WebGLのbuildの直後：`WebGL.data`の中に、場面が使うscriptがそろっているか
- (b) imageを作った後、pushの前：imageから取り出した`/app/wwwroot`で(a)をもう一度行い、通常の窓とシークレットウィンドウで
  開いて、描画とペアリングを見る

返却に足すもの：(a)と(b)の結果

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

## 名前の替えの確認（2026-11-28に足した。Unity、Scratch、Python）

`2026-11-28-01`、`2026-11-28-02`。「Unity箱庭」を、.NET箱庭（server）とUnity Webアプリ（ブラウザで開いて見るもの）に分けて呼び、
公開の名前を`dotnet-sb`（最新版、`25586`）、`dotnet-sb-lts`（LTS、`25585`）、`https://unity-app.mc-remote.com/`、
`https://unity-app-lts.mc-remote.com/`にする。旧名の`unity-sb`と`unity-sb-lts`はCNAMEで残す。portとcontainerは変えず、名前の替えの
ためにimageを作り直さない。考え方の正本は`00-hub/sandbox-layers-guide_ja.md`。

判断の期限（11月27日）の後の変更なので、返事は11月29日中にほしい。12月1日に出すか、延期して12月5日にするかは、human ownerが
この返事を見て決める。確かめるだけで、まだ何も変えない。

### Unity

公開VPSで動いている2つのimageについて答える。LTSは`candidate-1594805-2`
（`sha256:0737c28a1753847d8d1c4218a26561af083886def4457c2e3cd64d84f3c76828`）、最新版のrc1は`candidate-6ce475e`
（`sha256:e39109f0e3ff6bbc9ef2a0f4fb6048735817fa250a5226b404430ace52101097`）。

1. Unity Webアプリは、既定で、開いたhostの`/ws/sync`へつなぐか（`unity-app`で開けば`unity-app`へ）。固定したhost名が入っていないか。
   serverの側で、`/ws/sync`のOriginやHostを見ていないか（見ているなら、許している名前）
2. 利用者に見える旧名の文字（「Unity箱庭」、`unity-sb`、「Unity Sandbox」など）の一覧と、それぞれがどこで作られるか（server、
   WebGL、`index.html`）。分かっているもの：productName「Minecraft Remote Unity Sandbox」（2026-11-27の人間の試験で、タブの題は
   「Unity Web Player | Minecraft…」と出た）、chatの歓迎文「ようこそ Unity箱庭！」（claude.aiが`d3539c3`のsourceで読んだ。
   動いている版では見ていない）
3. 2の文字を替えるとしたら、何が要るか。最新版の`2400.0.0`は、最後の候補で、もともとWebGLとimageを作り直す（上の「Unity箱庭」の
   節）。その中で替えるときと、LTSの`2321.2.0`を作り直して替えるときの、それぞれの手間と時間と、確かめ直すこと。替える文字は
   human ownerが決める
4. LANのセットのREADMEと起動の文で、旧名が出るところ

返却に足すもの：1〜4の答え。見たcommitとimageのdigest

2026-11-28に返り、human ownerが決めた（`2026-11-28-04`①②。下の「最後の候補で替える旧名の文字（2026-11-28に足した）」）

### Scratch

1. rc1の`v2400.0.0rc1`と、LTSの`v2321.1.0`で、「Unity箱庭」や`unity-sb`が固定で入っているところ（ブロック、メッセージ、miniの
   表示、設定ページ、LANパッケージの`はじめに.html`とREADME）。接続先の一覧の名前と表示名は、全部runtime configから来るか
2. 一覧の接続先の名前やIDが替わったとき、ブラウザに残った選択はどうなるか（既定に戻るか、無い接続先を指したままか）
3. 最後の候補（`2400.0.0`）で、1の文字を替えるとしたら、何が要るか

返却に足すもの：1〜3の答え。見たcommit

2026-11-28に返り、human ownerが決めた（`2026-11-28-04`③④。下の「最後の候補で替える旧名の文字（2026-11-28に足した）」）

### Python

1. `2400.0.0rc1`と最後の候補で、README、starter、例外の文に、`unity-sb`や「Unity箱庭」が出るところ。旧名はCNAMEで残るので、
   12月1日を止める条件にしない

返却に足すもの：1の答え。見たcommit

## 最後の候補で替える旧名の文字（2026-11-28に足した）

`2026-11-28-04`。最新版の`2400.0.0`の最後の候補で、画面に出る旧名の文字を替える。上の「全componentで共通」の「最後の候補は、
最後のrcと同じsourceで、版だけを変えて作る」の例外にする。

### Unity

| 画面 | rc1（`6ce475e`） | 最後の候補 |
| --- | --- | --- |
| タブの題（productNameから作られる） | `Unity Web Player \| Minecraft Remote Unity Sandbox` | `Unity Web Player \| Minecraft Remote Unity Web App` |
| chatの歓迎文（日本語） | `ようこそ、Unity箱庭へ！ (v2400.0.0rc1)` | `ようこそ、.NET箱庭へ！ (v2400.0.0)` |
| chatの歓迎文（英語） | `Welcome to Unity Sandbox! (v2400.0.0rc1)` | `Welcome to the .NET Sandbox! (v2400.0.0)` |

- productNameだけを替える。前に付く「Unity Web Player | 」は残す。`index.html`の隠れたfooterとJSのconfigも、productNameから
  作られるので一緒に替わる
- 替えないもの：helloの`server.name`、imageのlabel、保存のkey、環境変数、namespace（hub NOTESの「参加アプリと箱庭の内部の名前」）
- LTSの`2321.2.0`（`candidate-1594805-2`）は作り直さない

確かめてほしいこと：

1. 最後の候補のいつもの確かめ（上の「pushの前の2段の確かめ」を含む）で、通常の窓とシークレットウィンドウの両方で、タブの題と、
   日本語と英語（`?lang=en`）の歓迎文を目で見る
2. productNameを替えて、ほかに変わるもの（buildのfileの名前、ブラウザに保存する場所など）が無いか。変わるなら、pushの前に知らせる
3. rc1の`6ce475e`から最後の候補までの差が、版と、この2か所の文字だけであること

返却に足すもの：上の1〜3の結果と、変えたfileの一覧

### Scratch

| 画面 | rc1（`0ae8af4`） | 最後の候補 |
| --- | --- | --- |
| エラーの文に出すserverの名前（`gui.mcremote.server.unity`） | `Unity箱庭`、ひらがなの表示は`Unityはこにわ`、英語は`Unity sandbox` | `.NET箱庭`、`.NETはこにわ`、`.NET sandbox` |
| LANのセットの初めの一覧の表示名 | `Unity箱庭` | `.NET箱庭サーバー` |
| LANの設定ページ、はじめに.html、ZIPの中の`README_ja.md` | 「Unity箱庭」 | 「.NET箱庭」 |
| ブロック一覧（`site/2400.0.0/`と入口） | 「Unity箱庭で使える」など | 「.NET箱庭で使える」など |

- 替えないもの：helloの`server.name`が`mc-remote-unity-sandbox`かを見る判定（serverの名乗りは12月1日には替えない）と、LANの
  一覧の`id: 'unity'`（保存した設定とtokenをそのまま使うため）
- ブロック一覧の検索の語には、旧名の「Unity箱庭」「Unity」「ユニティ」を残し、「.NET箱庭」を足す
- repoの中のREADME、提案の文書、testの文字は、合わせて直してよい
- LTSの`v2321.1.0`は替えない（旧名が無い）

確かめてほしいこと：

1. GUIのunit testと、LANのセットの`local:test`と`local:lint`が通ること（文字を確かめているtestは、新しい文字にする）
2. rc1の`0ae8af4`から最後の候補までの差が、版と、この文字と、ブロック一覧の`site/2400.0.0/`だけであること
3. 最後のLANのZIP 3つのbytesとSHA-256。3つのOSでの人間の試験はやり直さない（`2026-11-28-04`④）。human ownerがLinuxで1回
   開いて、設定ページとはじめに.htmlの文字を見る

返却に足すもの：上の1〜3の結果と、変えたfileの一覧

## coordinatorがすること

- 返却をGitHubのAPIで照合し、配布物を取り直して計る。Unity箱庭はloginなしでGHCRから取る
- そろったら、`2400.0.0rc1`のexact setと、LTSのUnity箱庭`2321.2.0`を凍結する
- 人間の試験の票を、rc1と`-beta`の名前で改める。Unity箱庭の見え方と最初のカメラの向き、版が合わないときのPythonの文を入れる
- knowledge：wire §7.3、Protocol Inventory、API一覧（`api/23.3.0/`と`api/24.0.0/`）、versioning、`19-unity/README_ja.md`。
  ホームページ（LTSの説明を含む）の文を、11月25日ごろに見せる
