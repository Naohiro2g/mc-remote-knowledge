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

## 返却と照合（2026-11-13）

Stackは、knowledge `f05f2a1440cbf2aed0841689bd0c3fc60d4ada03`（この依頼が入ったcommit）と、Stack
`8c6afcb1ad4017c16f1eb14af37bb1db86d6a2ee`（PR 89のmerge）を読んだ。coordinatorはGitHubのAPIで、このcommitが今もmainの先頭で
あることを確かめた。設定の変更、deploy、接続のprobe、共有の環境での測定はしていない。公開VPSでは、設定、Dockerのmetadata、
sysctlを読んだだけ（2026-11-13）。

経路全体で、何秒静かなら切れるかは、まだ分からない。

**どのprofileにも共通のもの**（ソースの既定の値と、読んだ値。接続を測った値ではない）

| 部品 | 値 | 意味 |
| --- | --- | --- |
| Caddy 2.11.4（どのpresetもdigestで固定。Stackは下の値を上書きしない） | `stream_timeout` 0、上流の読み書きの期限 0 | WebSocketの寿命の上限も、静かな時間の上限も無い |
| 同 | browserの側のTCP keepalive：15秒、15秒、9回 | 応答しないbrowserを約2.5分で切る。静かでも生きている接続は切らない |
| 同 | Bridgeの側のTCP keepalive：間隔30秒 | |
| 同 | HTTPの`idle_timeout` 5分、上流のpoolの2分 | 次のHTTP requestを待つ時間で、WebSocketの静かな時間には当たらない |
| Bridge（公開のimage `2321.0.0`、source `6447f6e`） | pingも、静かな時間の上限も無い。McRemoteへのTCPにkeepaliveを付けない | Node.jsの既定でkeepaliveは無効 |
| Linux（公開VPSのhostと、Caddy、Bridge、Minecraftのcontainer） | `tcp_keepalive_*`は7200秒、75秒、9回。Stackは変えていない | SO_KEEPALIVEを付け、値を指定しないsocketの既定 |
| conntrack | ESTABLISHEDは5日 | |

**profileごと**

- 公開VPS（`vps-server@18`、`public-web-paper@18`）：browser → Caddy（TLS）→ Bridge → McRemote。直接のTCPのclientは、公開のport
  → McRemoteで、CaddyとBridgeを通らない。VPSの事業者のnetwork、clientの側のrouterやWi-Fi、host firewallの規則は分からない
  （firewallの読み取りは3つとも失敗した）
- LANのケータリング（`classroom@1`）：今のpresetは、同じ端末のloopbackに3つのserviceを出す形で、CaddyとTLSは無い。LANの別の
  端末へ出すprofileは、まだ無い
- home（`home-alpha-full@2`、`home-server@6`）：browser → hostが用意するHTTPSとWSSの入口 → Caddy（TLSは終端しない）→ Bridge →
  McRemote。hostの入口の値は分からない

**4（Bridgeのpingを持つ場所）**：既定の値と設定の形はBridgeが持ち、presetが対応するartifactを固定する。Stackで上書きが要る
ときは、合意した後に版つきのoperatorの入力を足し、どのprofileにも同じ意味で出す。WebSocketのpingはbrowserとBridgeの間だけで、
BridgeからMcRemoteへのTCPと、直接のTCPのclientには、別の生存確認が要る。

**5（測るなら）**：手順は、Stackの搬送素材で返った。1つのcaseを1つの接続で、待つ時間ごとに新しい接続で試す（候補は1、5、15、
30、60、120分）。待つ間は何も送らず、待った後に読み取りだけのAPIを1回呼ぶ。公開VPSのWebSocketと直接のTCP、教室のloopback、
homeを分けて測る。共有の環境では測っていない。測るかと、対象のcaseは、human ownerが決める。

**6（案）**：まず、Caddyのbrowserの側のkeepalive（約2.5分で切る）が、耐えたいWi-Fiの切断に足りるかを照らし合わせる。外の経路が
分からないまま、Caddyやsysctlを変えない。globalのsysctlは一律には変えない。

`2026-11-13-02`で、値を測らずに決めた。測定とBridgeのpingは今はしない（hub NOTES 2026-11-13の「生存確認とつなぎ直しで、
今はしないこと」の行）。
