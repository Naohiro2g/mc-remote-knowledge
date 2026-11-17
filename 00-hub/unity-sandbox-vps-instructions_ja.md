# Unity箱庭の候補を公開VPSで動かす依頼（mc-remote-stack）

> `2321.2`のgateで、Unity箱庭のimageの候補をGHCRに置いた（`2026-11-17-02`）。Stackは、公開VPSでその候補をdigestで動かして
> 確かめる（同⑤）。Stackの PR #90（head `84add98be6d35c2c4a105e28078fa224300aa890`、open。単体の構成と、公開VPSに同居させる
> `vps-server@19`）の続きとして頼む。参照するknowledge commitは、この依頼が入ったmainのcommitです。

## 決まったこと

- image：`ghcr.io/naohiro2g/mc-remote-unity-sandbox@sha256:eef8787de7f61f17e155742900a25013057e06a3b6c879f17d724e490b13460c`
  （tag `candidate-be17313`、labelの`version` `2321.2.0`、`revision` `be17313007155227a46098e7b8c85c381a0dd3f3`）。loginなしで取れる。
  公開のときは、同じdigestに`v2321.2.0`のtagが足される（作り直さない）。coordinatorが照合した（`00-hub/release-gate-notes_ja.md`の
  2321.2の節の「Unity箱庭の作り直しの照合（2026-11-17）」）
- PR #90のalphaで使ったimageから変わったこと：containerはuid 1654（`app`）で動き、rootではない（configの`User`）。Unity Webと
  同じ場所で`/THIRD-PARTY-NOTICES.txt`を配る
- 世界とtokenはprocessの中だけに持つ。再起動すると世界は最初に戻り、tokenは消える（`2026-11-15-06`）。volumeは要らない
- 名前は`unity-sb`と`unity-sb-lts`。版が分かれるまでは同じcontainerを指す（`2026-11-16-05`③）
- 公開の箱庭で開けるportは、Stackで公開VPSへ出すときに、Bridgeの接続先と一緒に決める（`2026-11-15-01`）。`2321.2`のBridgeは、
  接続先ごとに`host`と`port`を持てる（`2026-11-16-01`）
- 公開の名前に置き、公開の組の接続先の一覧に出すのは、`2321.2`を出した後（gate notesの2321.2の節の「出した後」）。Unity箱庭の
  使いすぎを抑える上限は、まだ決めていない（同じ節の「未決」）

## すること

1. PR #90の構成で、上のdigestを公開VPSで動かす。`2321.2`を出すまでは、公開の組（`scratch`、`scratch-beta`）の接続先の一覧に
   足さず、ホームページからもつながない。確かめるときのhostnameと、どのScratchとBridgeからつなぐかは、Stackが案を出し、
   human ownerと決める（DNSはhuman owner）
2. 確かめること：`/healthz`（`version` `2321.2.0`、`protocol` `23.3.0`）、Scratchからのペアリング、建築とUnity Webの表示、
   `/THIRD-PARTY-NOTICES.txt`、doctor
3. uid 1654で動くことで、PR #90の構成（Caddy、network、doctor）に変わるところがあるか
4. TCPのport：PR #90は、今のBridge（共通のport）に合わせて`--tcp-port 25575`で動かしている。`2321.2`のBridgeへ移った後も
   `25575`のままにするか、既定の`25585`にするかの案
5. `unity-sb`と`unity-sb-lts`を同じcontainerへ向ける形

## 返却

- 実際に読んだknowledge commit
- PR（番号、head、merge）と、VPSで動かしたimageのdigest（`RepoDigests`など、digestが分かるもの）
- `/healthz`の応答と、helloの`server.version`と`protocol`
- 1と2で確かめたこと（hostname、使ったScratchとBridgeの版）と、確かめられなかったこと
- 3〜5の案と理由

## coordinatorがすること

- PRをGitHubのAPIで照合する
- gateを凍結した後に、`2321.2`の公開の票を作る（Scratch、Bridge、runtime configの接続先の一覧、`unity-sb`と`unity-sb-lts`）
