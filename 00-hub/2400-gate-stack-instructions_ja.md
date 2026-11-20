# `2400`と、12月1日の最新版とLTSの依頼（mc-remote-stack）

> 2026-11-19に、`2400.0.0`を12月1日0時（JST）に出し、同じ時にLTSの名前で`2321`の系列を出すと決めた（`2026-11-19-01`、
> `2026-11-19-02`）。12月1日の名前の票（`00-hub/sandbox-lts-names-instructions_ja.md`）の続きで、そこと違うところはこの票に従う。
> gateは`00-hub/release-gate-notes_ja.md`の「2026-11-19 `2400`横断release gate」。参照するknowledge commitは、この依頼が入った
> mainのcommitです。

## 決まったこと

- 12月1日0時に出す。デプロイとホームページの改訂まで、3時間以内に終える。延期するかは11月27日に決め、延期なら12月5日
- 12月1日の姿：

  | 名前 | 最新版（`2400`） | LTS（`2321`） |
  | --- | --- | --- |
  | Minecraft | `sb`：McRemote `2400.0.0`（公開VPS） | `sb-lts`：McRemote `2321.2.0`（有料GAMEs） |
  | Web | `scratch`、`wirescope`：Scratch `2400.0.0`、Bridge `2400.0.0`、runtime config `schema_version: 2` | `scratch-lts`、`wirescope-lts`：Scratch `v2321.1.0`、Bridge `v2321.0.0` |
  | Unity箱庭 | `unity-sb`：`2400.0.0`、外のport `25586` | `unity-sb-lts`：`2321.2.0`（IMEと座標の見え方を直したもの）、外のport `25585` |

- 接続先の一覧は、組ごとに同じ系列だけにする。`scratch`の組は`sb`と`unity-sb`、`scratch-lts`の組は`sb-lts`と`unity-sb-lts`
  （`2026-11-19-02`③。前の票の「どちらの組も両方を選べる」を改める）。majorが違うとhelloで断られる
- Unity箱庭は、`unity-sb`と`unity-sb-lts`を別のcontainerにする。外へTCPを開け、`unity-sb-lts`は`25585`、`unity-sb`は`25586`
  （`2026-11-20-03`。下の「公開VPSのUnity箱庭のport（2026-11-20に足した）」）
- `-beta`の名前：11月中は`2400`の予行演習に使う。12月からは、しばらく最新版を指す保険として残す。案内の正面は、接尾辞の無い
  名前とLTS（`2026-11-19-02`④）
- Scratch OCIは、凍結したdigestのまま出す。今の公開のworkflowには作り直す経路があるので、`2321.1`と同じように止めて出す
- 出した後に、McRemoteのcredentialのfileのmode（`0600`、`0700`）を、`sb`と`sb-lts`の両方で確かめる（`2026-11-11-03`）

## すること

1. **11月中の予行演習**（11/25〜30）：`2400.0.0rc1`を`sb-beta`（McRemote）、`scratch-beta`（Scratch、Bridge、runtime config
   `schema_version: 2`）、`wirescope-beta`で動かす。Unity箱庭のrc1をどうつなぐかの案（名前を足すか、手元で試すか）。その間、
   `scratch`の組（`2321.1.0`）の一覧の`sb-beta`はつながらなくなるので、外すかどうか
2. **12月1日の構成**：上の姿のprofile、preset、lock、runtime config
3. **検証機での通し**（11/28〜29）：最後の候補で、12月1日の手順を最初から最後まで通し、時間を計る
4. **12月1日0時からの手順**：順番、それぞれにかかる時間、うまく行かなかったときの戻し方
5. **`sb-lts`**：有料GAMEsのMinecraftを、旧protocolの`sb-retro`から、McRemote `2321.2.0`へ移す手順と、止まる時間。公開VPSの
   LTSのBridgeから、GAMEsのTCP 25575へつなぐ
6. **doctor**：両方の系列で、到達と認証を確かめる

## 返却

- 実際に読んだknowledge commit
- 1〜6のPR（番号、head、merge）と手順の場所
- 1：rc1を`-beta`で動かしたimageのdigest、Unity箱庭のrc1の案
- 3：検証機で通した時間と、つまずいたところ
- 4：12月1日0時からの順番と時間の見込み
- 5：止まる時間と、Stackの外で要るもの（DNS、有料GAMEsのMcRemoteの設定など）
- 確かめられなかったことと、その理由

## 公開VPSのUnity箱庭のport（2026-11-20に足した）

`2026-11-20-03`。human owner 2026-11-20「Unity箱庭を25586、Unity箱庭LTSを25585（デフォルト値）として、外部からの接続を許すことに
する。」「今作っているコンテナイメージをデプロイ。」。今は、Unity箱庭のTCPを外へ開けていない（`2026-11-18-01`）。

- 外へTCPを開ける：`25585`はLTSの系列（`unity-sb-lts`）、`25586`は最新版の系列（`unity-sb`）。開ける前に、下の「上限の無い間の
  対策と見張り（2026-11-20に足した）」を用意する（`2026-11-20-04`。`2026-11-20-03`③を改めた）
- 12月1日まで：`25585`にLTSの`2321.2.0`を置く。今の公開のScratch（`2321.1.0`、Bridge `2321.0.0`）がつなぐUnity箱庭も、この
  containerにする。`25586`には`2400.0.0rc1`を置き、`scratch-beta`の組からつなぐ（上の「すること」の1の、Unity箱庭のrc1をどう
  つなぐかの答え）。12月1日に、`25586`を`2400.0.0`へ替える
- Bridgeが中からつなぐportは、外のportと別に持てる。LTSのBridge（`v2321.0.0`）は、全ての接続先に共通のportを1つしか持たない
  （`sb-lts`はGAMEsの`25575`）。中のportの割り当ての案を出す
- image：coordinatorが2026-11-20にGHCRで照合した次のdigestを動かす。数日のうちに、上限の対策を入れた版へ替える（coordinatorが
  照合してから）。`candidate-be17313`は、戻すときのため12月1日まで消さない

  | port | tag | 版 | indexのdigest |
  | --- | --- | --- | --- |
  | `25585` | `candidate-f7d0f9a` | `2321.2.0` | `sha256:b11d435f2cd327d66d1af0a424d130970044eeeb55cb2838ff5ad763e008bfc0` |
  | `25586` | `candidate-1dc3cbd` | `2400.0.0rc1` | `sha256:563f55f456eab1aae90cb522b23e34ed7b0d79b4f9c29b8c9b43bb279ecf67a0` |

返却に足すもの：PR、firewallとcomposeの差分、外から2つのportへhelloを送った結果（`protocol`と`server.version`）、動かしたdigest、
Bridgeの接続先の設定（中のport）

## 上限の無い間の対策と見張り（2026-11-20に足した）

`2026-11-20-04`。human owner 2026-11-20「docker側でできる対策やモニタリングの手法など準備した上で、実際に攻撃があるのか、プラス
自分で攻撃して確かめる、で行きたい。」。Unity箱庭のserverには、TCPの接続の数（送り元ごと、全体）、helloの前に待つ時間、
`auth.pairBegin`の回数、承認を待つcodeの数、1行の長さの上限が無い。待つcodeの記録の一部は、pollされないと消えない。Unity Webの
`/ws/sync`の受け取る長さにも上限が無い（Unity Webは今も公開している）。数日のうちに、serverに上限を入れた版へ替える

- docker側でできる対策：上のどれかを突かれても、Unity箱庭のcontainerが同じ機械のほかのserviceを巻き込まず、落ちたら戻るように
  する。案を出し、human ownerと相談して入れる。Unity箱庭のserverは、再起動するとtokenを失い、利用者はペアリングし直す
  （`2026-11-15-06`）
- Unity担当の見立て（2026-11-20）：composeで、memory 512MB（swap無し）、CPU 0.5、process 256、開けるfile 1024、
  `restart: unless-stopped`、logは10MBを3つまで。これで同じ機械のほかのserviceに影響は出ないと見ている。Stackは、これを出発点に、
  機械の余裕、普段のmemory、送り元ごとの絞り方（hostのfirewall）、見張りを足して案を出す
- 見張り：接続の数、containerのmemoryとCPU、再起動の回数などを、どう見るかの案
- 攻撃して確かめる：human ownerが自分で攻撃して確かめる。試す項目（上の上限の無いところ）と、その間に見るものの案を出す

返却に足すもの：docker側の対策の差分、見張りの方法、開けた後に見た接続（攻撃らしいものがあったか）、攻撃して確かめたときに
起きたこと（containerと機械への影響）。送り元のaddressは返却に書かず、数で返す

## coordinatorがすること

- PRをGitHubのAPIで照合する。候補のdigestと、`-beta`と検証機で動かしたdigestを突き合わせる
- 12月1日の前に、ホームページ（版の表、リリース一覧、はじめる（1）と（2）、LTSの説明、移行のページ、ロードマップ）と、
  Scratchのお知らせの文を作って、human ownerに見せる
