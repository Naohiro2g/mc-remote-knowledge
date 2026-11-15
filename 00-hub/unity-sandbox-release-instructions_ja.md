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
