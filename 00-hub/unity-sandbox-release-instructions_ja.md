# Unity箱庭を`2321.3`で出す準備の依頼（mc-remote-unity-sandbox）

> human owner 2026-11-15「2321.3もUnity箱庭を入れてなるはや。」。Unity箱庭を台帳のcomponentに入れ、配る形とtokenの扱いを
> 決めた。仕上げてPRにする依頼（`00-hub/unity-sandbox-first-slice-pr-instructions_ja.md`）と同じPRに入れても、別のPRにしても
> よい。参照するknowledge commitは、この依頼が入ったmainのcommitです。

## 決まったこと（2026-11-15）

- 版（`2026-11-15-04`）：Unity箱庭は台帳のcomponentに入る。版は台帳のX.Y.Zに従い、最初の公開は`2321.3.0`。serverと
  Unity Webは同じ版で出す。helloの`server.version`はこの版
- protocol（`2026-11-15-03`④）：helloの`protocol`は`23.3.0`
- 配る形（`2026-11-15-05`）：Unity Web（WebGLのbuild）を入れたcontainer image。ローカルの開発機で、WebGLのbuildとimageの
  buildをして、GHCRへpushする。Stackがそのimageを公開VPSで動かす。`AGENTS.md`の「配布、公開の配信、release workflowは、
  knowledge SSOTで決まるまで足さない」のうち、配る形はこれで決まった
- token（`2026-11-15-06`）：serverの再起動の後に残さない

## すること

1. helloの`protocol`を`23.3.0`にする。先にtestの期待を変え、今の`23.2.1`で落ちるのを見る
2. 版を書く所（helloの`server.version`、imageのlabel、Unity Webの表示など）が1か所から決まるようにする。`2321.3.0`にするのは、
   `2321.3`のgateで候補を作るとき
3. tokenと、tokenと画面の結び付きを、processの中だけに持つ。再起動の前のtokenで来たhelloが、どのreasonで断られるかを
   testで見る（McRemoteでは、知らないtokenは`token_not_found`）
4. Dockerfileと、WebGLのbuildからimageのbuildまでをローカルで通す手順を足す。human ownerに伝わっている案は、multi-stageの
   buildで、`dotnet publish`したserverと、WebGLの静的なfileを`/app/wwwroot`に入れる形。imageがどのcommitから作られたかを、
   gateで照合できるようにする（OCIのlabelなど）
5. 作ったimageを手元で動かし、human ownerがScratchのLANパッケージとPythonのclientからつないで建てる
6. GHCRへのpushはしない。pushは`2321.3`のgateの公開の段で、human ownerが判断してから行う

## 返却

- 実際に読んだknowledge commit
- PRの番号、head、CIのrun（あれば）
- 1で落ちたtestと、直した後
- 3：再起動の前のtokenで来たhelloへのreason。再起動で、世界（置いたblock）がどうなるか
- 4：Dockerfileとbuildの手順の場所、base image、imageの大きさ、labelに書いたもの、imageの名前とtagの案（ほかの
  componentは`ghcr.io/naohiro2g/mc-remote-scratch:v2321.0.0`の形）
- Stackが動かすために要るもの：開くport（TCPの`25585`、Unity Webと表示同期のHTTP）、起動のoption、環境変数、volumeが要るか、
  動いていることの確かめ方
- 5の結果と、確かめられなかったことと、その理由

## coordinatorがすること

- PRとCIを、GitHubのAPIで照合する
- imageの名前、tag、loginなしで取れるかを、`2321.3`のgateでhuman ownerと決め、Stackへの票を作る（Bridgeの接続先の
  返却と合わせる）

## 返却と照合（2026-11-16）

Unity担当は、knowledge `99e582b`を読んだ。返却は`mc-remote-unity-sandbox`の
`handoff-materials/2026-11-15-unity-first-slice-return/materials/unity-first-slice-return_ja.md`（16,366 bytes、
`adc17c8461bfeaa9d54e841b5b0ebb29da77b279fcad99fb5a30392ccdda39c1`）で、この依頼と`00-hub/unity-sandbox-first-slice-pr-instructions_ja.md`の
両方への返却。

- PR #2：`feat/first-slice-shared-sandbox` → `main`（`958b676`）、head `bba6e4ca25a7d2a9d5798b99ad049a60022c85b0`、4 commit、57 file。
  coordinatorがGitHubのAPIで確かめた。このrepoにCIは無い（checkもrunも0件）。testは担当の申告
- 1：helloの`protocol`は`23.3.0`。直す前は19 testのうち3つが落ち（`23.3.0`と再起動のtest）、直した後は19が通った
- 2：版は`VERSION`の1か所（今は`0.1.0`）から、helloの`server.version`、`/healthz`、Unity Webの`bundleVersion`、imageのlabelへ入る
- 3：token、tokenと画面の結び付き、世界は、processの中だけに持つ。再起動の前のtokenは`token_not_found`（`-32000`。McRemoteと
  同じ）。再起動すると世界は最初の地形に戻る。世界のリセットではtokenを消さない。codeの試行は、WebSocketの接続と画面のIDごとに、
  60秒で5回の失敗まで
- 4：multi-stageの`Dockerfile`、`.dockerignore`、`scripts/build-container.sh`。WebGLはUnityの開発機でbuildし、imageは`DOCKER_HOST`で
  つないだ別のmachineのDockerでbuildする。試しのimage `ghcr.io/naohiro2g/mc-remote-unity-sandbox:v0.1.0`は371MB（中身107MB）。
  labelは`version` `0.1.0`、`revision` `0b69a03c2fef6faa83f56553038a4abd2844a258`（PRの先頭ではない）、`licenses` `MIT`など。
  GHCRへはpushしていない
- Stackが動かすために：port `8080/tcp`（Unity Web、`/ws/sync`、`/healthz`）と`25585/tcp`（JSON-RPC）。volumeは要らない。起動は
  `--url http://0.0.0.0:8080 --web-root /app/wwwroot --tcp-host 0.0.0.0 --tcp-port 25585`。環境変数は`UNITY_SANDBOX_VERSION`、
  `UNITY_SANDBOX_GIT_COMMIT`、`ASPNETCORE_URLS`。動いていることは`GET /healthz`（`status`、`version`、`protocol`、`tcpPort`など）で見る
- 返ってこなかったもの：base imageの名前とdigest。5（作ったimageを動かし、human ownerがScratchのLANパッケージとPythonのclientから
  つなぐ）はまだ
- McRemoteとの食い違い：32,769個の`world.setBlocks`に`work_limit_exceeded`を返す（coordinatorの前の票のとおり）。McRemoteは
  `block_count_limit_exceeded`
- human ownerの判断（2026-11-16）：①1回に置ける数を越えたら`block_count_limit_exceeded`（`2026-11-16-02`）②imageのbuildは、
  human ownerが決めた手元の1台で行う（`2026-11-16-03`）③PR #2はmergeする（「PR#2はマージします。」）。mergeした（merge commit `d29a577643bd44942de99fbd075a24178036f4c4`）

## 次にすること（2026-11-16）

1. 32,768個を越える`world.setBlocks`を、`block_count_limit_exceeded`で拒む（`2026-11-16-02`）。先にtestの期待を変え、今の
   `work_limit_exceeded`で落ちるのを見る
2. imageのbuildは、human ownerが伝えるmachineで行う（`2026-11-16-03`）。mergeした後の`main`のcommitからimageを作り、labelの
   `revision`がそのcommitであることを確かめる
3. 作ったimageを手元で動かし、human ownerがScratchのLANパッケージとPythonのclientからつないで建てる（上の「すること」の5）
4. GHCRへのpushはしない（上の「すること」の6のまま）

### human ownerと相談して進めること（2026-11-16）

human owner 2026-11-16「2321.3に入れる線で検討を進めよう。」。次のmethodを`2321.3`に入れる線で、human ownerと相談しながら
仮実装して、形を決める。

- `world.getBlocks`、`player.getPos`、`player.setPos`、`player.getPose`、`player.setPose`、`player.getDirection`、`player.setDirection`
- `world.getHeight`（human owner「最有力ではある」）と、`events.poll`のチャットのイベント（human owner「入れてしまって良い」）。
  ほかのmethod（看板、エンティティ、パーティクル、音、雷）とは「明確に距離がある」（human owner）
- 守るもの：wireのmethodの形は変えない。protocolは`23.3.0`のまま
- 材料：wireの§5.2、§5.3、§5.4、§5.8.2、`10-protocol/block-value-design_ja.md`の`world.getBlocks`、共有fixtureの
  `mcremote.chat-event-compat.v23.2.1`、McRemoteのふるまい
- 相談で決めることの例：Unity箱庭で「プレイヤー」を何にするか、その画面が開いていないときの答え、世界の外へのsetPos、地面の
  高さを何で決めるか、どのチャットをイベントにするか

返却：実際に読んだknowledge commit、PRの番号とhead、1で落ちたtestと直した後、imageのbase imageの名前とdigest、imageのdigestと
label、3の結果、相談して決めた形と採らなかった案（相談した日とhuman ownerの言葉）、確かめられなかったことと、その理由

## PR #3の返却と照合（2026-11-16）

Unity担当は、knowledge `fdc3c8c`を読んだ。返却はrepoに置かず、human ownerが会話に貼った。上の「次にすること（2026-11-16）」と
「human ownerと相談して進めること（2026-11-16）」への返却。

- PR #3：`feat/23213-sandbox-methods` → `main`（`d29a577`）、head `03d3eade37190a090cee26cfcbccfd6b52e0bb40`、3 commit、23 file
  （+2,206／−98）。coordinatorがGitHubのAPIで確かめた。CIは無い。testは担当の申告。human ownerが2026-11-16にmergeした
  （merge commit `d3539c3964c4dc9b19b969999ebde729f530fa6e`）
- 1：32,768個を越える`world.setBlocks`の期待を先に変え、19のtestのうち2つが`work_limit_exceeded`で落ちた。直した後は19が通った。
  `data`は`limit`（32768）と`requested`で`violating`は無く、codeは`-32000`。wire §7.3とMcRemoteに合う（`2026-11-16-02`）
- 足したmethod：`world.getBlocks`、`world.getHeight`、`player.getPos`、`player.setPos`、`player.getPose`、`player.setPose`、
  `player.getDirection`、`player.setDirection`、`events.poll`の`chat_posted`。.NETのtestは24が通った。Unity `6000.6.8f1`で、検証、
  playのsmoke、WebGLのbuildが通った
- 相談して決めた形（2026-11-16。human ownerの言葉は返却に無い）
  - プレイヤーは、ペアリングした画面の一人称の歩行者。画面ごとの`viewerId`で、`/ws/sync`の`playerPose`を両方向に同期する
  - 画面がつながっていなければ`player_offline`。tokenと画面の結び付きは残す
  - 範囲の外（水平が-200〜199、高さが-64〜320の外）への`player.setPos`と`player.setPose`は、副作用の前に`out_of_bounds`で拒む
  - `world.getHeight`でpassableなのは`minecraft:air`だけ
  - `chat_posted`は、ペアリングした画面の普通のchatだけ。`/`で始まるコマンド、`chat.post`、ほかの画面のchatは入れない
  - 採らなかった案：画面と別に、serverの側だけで座標を持つ／最後の座標を返し続ける／`teleport_failed`で返す／glassなども
    passableにする／`chat.post`やコマンドもイベントにする
- knowledgeとの突き合わせ：`player_offline`、`chat_posted`の範囲（wireの「paired playerが投稿した…slash commandは除外」）、
  `world.getHeight`（§5.6）は、wireの意味と同じ。`player.setPos`と`player.setPose`の`out_of_bounds`は、`2026-11-14-04`が当てる
  method（`world.*`）の外で、playerの高さの上限320はblockの319と違う。そのときの`data.bounds`の`y_max`は返却に無い。McRemoteで
  同じ呼び出しがどうなるかは、knowledgeに書いていない
- image：PR #3のhead `03d3ead`から作った（上の「次にすること」の2の「mergeした後の`main`から」ではないが、labelの`revision`は
  `03d3ead`で対応は取れる）。ID `sha256:7189463292558aca0699ae5cdd272133023dd2c0c49f7e7d5168a10c27d65bdb`、370,651,953 bytes、
  labelの`version`は`0.1.0`、`licenses`は`MIT`。base imageは`mcr.microsoft.com/dotnet/sdk:9.0`（index
  `sha256:1dfdb27e9c2c345cb598925ccf6b13719ecfebea8467bd4745c23a3c108cdf84`）と`mcr.microsoft.com/dotnet/aspnet:9.0`（index
  `sha256:22db800f670f4c21327f463df2a0bc8f0947b44f58c13e582ab4ed7e34310f3e`）。一時のcontainerで、`/healthz`（`protocol` `23.3.0`、
  `tcpPort` 25585）と、足したmethodとerrorのsmokeが通った（担当の申告）。GHCRへはpushしていない
- READMEの学習の言い方を、ホームページに合わせた（「コーディングで学ぶ」「学び方を学ぶ」）
- 確かめられなかったこと：人がbrowserで歩いて、`setPos`などの視界と重力を見ること。ScratchのLANパッケージとPythonからつなぐこと。
  human ownerは2026-11-16に、このimageを動かして新しいScratchとつないだ
- 次：最初の公開を`2321.2.0`にした（`2026-11-17-01`）。候補の返却に要るものは`00-hub/23212-gate-candidate-instructions_ja.md`の
  「範囲を広げた後の候補（2026-11-17）」

## 候補の返却と照合（2026-11-17）

Unity担当は、knowledge `3bf79ef`を読んだ。返却は`mc-remote-unity-sandbox`の
`handoff-materials/2026-11-17-unity-23213-rc-return/materials/RETURN_ja.md`（21,614 bytes、
`f18b743565a4fbb16fb4b4c1504098e684622fd5d2ab7881b0cba9aa31fd351f`）で、人間の試験の案は同じ場所の`HUMAN_TEST_ja.md`（5,550 bytes、
`ce5d7c36a391dabe7f9776456e47a9ba49f84cdca00ab43d2b9555058592f1ea`）。coordinatorが手元のfileを計り、返却の値と一致した。

- PR #4：`feat/ui-polish-monospace-i18n` → `main`（`d3539c3`）、head `8099216d5d12b4aed8388e5de17b80b3ac6b90ce`、2 commit、14 file
  （+772／−120）、open。coordinatorがGitHubのAPIで確かめた。CIは無い。`VERSION`は`0.1.0`のまま
- 中身はUnity Webの画面だけ（HUDとchat、等幅のfont（Noto Sans Mono CJK JPのsubset、11,128,896 bytes、SIL OFL 1.1）、日本語と英語の
  切り替え、区画へのワープ、置いたblockの発光、browserでの誤操作の防ぎ）。server、TCPのJSON-RPC、`/ws/sync`、Dockerfileは
  変えていない（担当の申告）
- image：`8099216`から作った。`sha256:2b7fe4ca7abd999be2e2b9959b2cc1fcb4f547d025bc371fbe3394e1dafbdcca`（manifest
  `sha256:58d2762a2f15cb8f9d08c7a2e76345fdf84a4c9a04cda2262cc37045fa037664`、config
  `sha256:cec2ac46bf9e567ddbfbf6ad5ccba8d9d9b3cc29a600df8ff0598d95f43d68e9`）、381,262,761 bytes。labelの`revision`は`8099216`、`version`は
  `0.1.0`、`licenses`は`MIT`。GHCRへはpushしていない
- test：.NETの24、Unityの検証、WebGLのbuild（31,933,672 bytes）は`8099216`で通った。playのsmokeは`5204abd`で通ったもの（歩行などの
  fileは`8099216`で変えていない、と担当）
- knowledgeと合うもの：`world.getBlocks`の上限（各軸10、全体1,000、超えたら走査の前に`work_limit_exceeded`）は、wire §7.1.1と同じ
- 気づいたこと
  - `zero_direction`：返却の確定搬送票は、codeを`-32000`と書いている。wire（`DirectionValue`の規則と§7.3の表）とMcRemoteは`-32602`
  - playerの世界の外：「高さ`[-64, 320]`」と「Y: -64..319」が並んで書かれていて、どちらか分からない。`data.bounds`の`y_max`の例も
    無い
  - methodの数：「計21」（最初の12と足した9）とあるが、足したmethodとして挙がっているのは8つ（`world.getBlocks`、
    `world.getHeight`、`player.*`の6つ）。一覧が要る
  - 相談の結果について、human ownerの言葉は返却に無い
- 返却の「確定搬送票」（足したmethodの形）は、上の気づいたことが片付いてから、coordinatorがDECISIONSに起案する
- 次：`00-hub/23212-gate-candidate-instructions_ja.md`の「範囲を広げた後の候補（2026-11-17）」のUnity箱庭の節（`VERSION`を
  `2321.2.0`にしたcommit、そこから作ったimage、methodの一覧、playerの`out_of_bounds`の`data`の例）
