# 静かな接続が経路の途中で切られる時間を返す依頼（Stack）

> 多言語Client LibraryのE2で、clientの待ち方とつなぎ直しを決めた（`2026-11-11-01`③⑤）。clientは既定で長く待ち、transportの
> 生存確認で切れた接続を見つけ、Wi-Fiの一時的な切断には長めに耐える。値は言語ごとに実測で決める。検討メモ
> （`10-protocol/connection-liveness-notes_ja.md`の「3」の4）では、proxyやNATが、何も流れない接続を切る時間が分かっていない。
> その時間より生存確認の間隔が長いと、何もしていない間に接続が切られる。この票は、Stackが配置する経路で、それを返してもらう
> 依頼です。設定は変えない。参照するknowledge commitは、この依頼が入ったmainのcommitです。

## 前提

- 経路は2つ：
  - browser（Scratch、WireScope）→ TLSの終端（Caddyなど）→ Bridge（WebSocketとTCPの中継）→ McRemote
  - 直接のTCPのclient（Python、Java、TypeScript、C#）→ McRemote
- Bridgeのcodeは、scratch-editorの`mc-remote/bridge`にある（`13-scratch-client/scratch-plan_ja.md`の「モノリポ構成」）。Bridgeから
  pingを送るかの案は、Scratchへの票（`00-hub/polyglot-e2-reconnect-instructions_ja.md`の「Scratch」）で頼んだ。この票では、
  Stackの設定と配置の側だけを聞く
- browserのWebSocketのAPIからはpingを送れない（メモの「3」の3）
- 決まっていないこと：生存確認の間隔と、経路の設定を変えるか。この票の返却を見て決める

## 返してほしいこと

Stackが持つprofile（公開のVPS、LANのケータリング、homeなど）ごとに答える。読んだStackのcommitを書く。

1. **Stackが設定するもの**：TLSの終端、reverse proxy、containerのnetwork、firewallなど、Stackが置く部品のうち、何も流れない
   接続を切りうるもの。それぞれの今の設定の値（Stackで書いていなければ、その部品の既定の値と、その出典）。WebSocketと、
   直接のTCPの両方
2. **Stackの外にあるもの**：VPSの事業者のnetwork、家庭や教室のrouterのNATなど、Stackが設定しない部品。分かっていること、
   分からないこと
3. **OSのTCP keepalive**：McRemoteとBridgeが動くhostやcontainerで、OSのTCP keepaliveの既定（Linuxの`net.ipv4.tcp_keepalive_*`
   など）をStackが変えているか
4. **Bridgeのpingを入れるとしたら**：その間隔や有無を、Stackのprofileや設定のどこで持つのがよいか。1の値との関係
5. **測るなら**：1と2の時間を実測する方法の案。共有の環境で測る前に止めて、手順を返す（human ownerが判断する）
6. 1〜4のうち、変えた方がよいと思うものがあれば、案を返す（設定は変えない）

## 返却

- 実際に読んだknowledge commitと、Stackのcommit
- 1〜6の答え。profileごとに分ける
- 確かめられなかったことと、その理由
- host、IP、domainの実値、account、backupの中身など、privateな運用の値を書かない（`2026-07-21-03`）

## coordinatorがすること

- 返却を、検討メモと、各clientの③⑤の返却（生存確認の既定）と突き合わせ、間隔の案を作ってhuman ownerに見せる
