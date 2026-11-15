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
