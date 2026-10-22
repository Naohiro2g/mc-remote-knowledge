# 初回stable（2321.0.0）横断release gate 確認票依頼

> 初回stable（`00-hub/release-gate-notes_ja.md`の2026-10-22の節）を開いたときに、各担当へ出す確認票の依頼です。参照する
> knowledge commitは、この依頼が入ったmainのcommitです。各担当は、自分の節と「共通」を読んで確認票を返してください。
> McRemoteは、同じ票でrc2の実装に着手してよい。

## 共通

- 初回stable `2321.0.0`は、rc1のsourceに、McRemoteの旧`b5.`／`b7.`キーの移行の処理を外すことだけを足して出す
  （`2026-10-22-01`）。protocolは`23.2.1`のままで、APIとwireは変えない。McRemoteだけ`2321.0.0rc2`をGitHubのpre-releaseで
  挟み、ほかのcomponentはrc1のsourceから版の番号だけを変える
- 日程：GitHubのLatestを11月1日。rc2で何か出れば11月7日。**確認票の返却の目安は10/23**
- rc1のtag：tooling `6447f6e8cbfbeeb9d229990b5c4f6e82a5875666`、Scratch `ec79b3b0e364e722d6926a0932eb4bf088ddd3a1`、McRemote
  `192a777ae1d484bcc9b58fcc7c58d6aed1a374af`、Python `c30105349ef26413e925699143396ea05bd3e380`
- stableの後の改善（PythonのWireScopeの観測、Scratchのランチャーや`はじめに.html`など）は`2321.1.0`で出す
  （`2026-10-22-03`）。この版には入れない

各担当に共通で聞くこと:

- rc1のtagの後に、default branchへ入ったもの（commitと一行の説明）。あれば、stableをrc1のtagから作るか、今のdefault
  branchから作るかの案と、その差分がstableに入ってよいものか
- rc1から版の番号だけを変えるときに変える箇所（定数、配布物の名前、README、Release本文など）と、手間の見積もり
- stableで変わる公開の操作：pre-releaseの印を外す、Latestにする、registryの既定の版が変わるなど。rc1と違う手順があれば書く
- 11月1日に対する見込みと、止まっている点

返却は`release-gate-notes_ja.md`の確認票の形式。`knowledge contract commit`には実際に読んだSHAを書く。自repoの事実と根拠
だけを返し、他repoへの着手、shared環境の変更、人間参加の試験、tag／releaseの公開はしない（McRemoteのrc2は下の節に従う）。

## McRemote

rc2の実装に着手してよい。tag、Releaseの公開は、返却を受けてcoordinatorが着手を出してから。

- 外すもの：起動時に旧`b5.`／`b7.`キーの値を新しいキーへ移し、旧キーを消す処理（`2026-10-01-01`）
- 外した後の挙動（`2026-10-22-01`）：configに旧`b5:`／`b7:`のキーが残っていたら、McRemoteはエラーをlogに出して、Paper
  サーバーの起動ごと止める。McRemoteだけを無効にしてPaperを動かし続けることはしない（リモコンが使えないだけで、logを見る
  契機にならない）。黙って無視して既定値で動かない。logには、どのキーが残っているかと、直し方（新しいキーの名前、旧キーを
  消すこと）を書く。Paperで起動を止める方法と、そのときのlogの見え方を返す
- test：①新しいキーだけのconfigで、今までどおり起動する ②旧キーが残ったconfigでPaperが止まり、logに上の内容が出る ③rc1が
  移行を済ませたconfigで、何も変わらない。単一JARで、同じJARを1.21.11と26.3で起動、有効化、停止、helloと代表の読み書き
  （b10のpulseの形）
- README、upgradeの案内：b7以前のconfigを使っている人への案内を、どこに書くか
- 返却：変更の範囲、testの結果、rc2の候補のidentity（commit、JARのSHA-256）

## Python client

- stableを出すと、版を指定しない`pip install`／`uv add`で入る版が、旧protocolの1214系から`2321.0.0`に変わる。PyPIへの
  公開はrc1と同じく`pypi` environmentのhuman owner承認で止める（`2026-10-18-04`）
- Release本文：rc1のWireScopeの注意書き（`input()`で待つ）を引き継ぐ。旧protocolからの移行の案内へのリンクの置き場所
- 移行ガイド（`2026-10-22-02`③）：旧protocolから新protocolへ、pyenv／poetryからuvへ。今ある案内の場所と、強くするときの
  案。初回stableの公開に要る最小限（版を指定しないと新しい版が入ること、旧protocolを使い続ける人の版の指定）と、11月中に
  強くする部分を分けて返す
- starter（`sb-beta`を指している）：11月1日に箱庭の名前を切り替え、`sb`が新protocolの安定版になる（`2026-10-22-04`。旧protocolは
  `sb-retro`で11月末まで）。starterとREADMEの箱庭の名前を`sb`へ変える案。旧版を使い続ける人の案内は`sb-retro`

## Scratch editor（WireScope、minecraft-remote-tooling）

- 順番はrc1と同じく、toolingを先に出し、ScratchはtoolingのReleaseの後
- LANパッケージのZIP、OCI、ブロック一覧のsiteを、版の番号だけ変えて作る。OCIはrc1と同じく、凍結したものをCLIでそのまま
  昇格する経路でよいか
- ブロック一覧：`site/2321.0.0/`と、入口を今の版のページと同じbytesにすること
- `はじめに.html`とLANパッケージの中の版の表記、ホームページへのリンク（`/lan/scratch/`）

## Stack（mc-remote-stack）

- `2321.0.0`のpreset。rc1からの差分
- 箱庭（`sb-beta`）のMcRemoteのconfigに、旧`b5:`／`b7:`のキーが残っていないこと。残っていると、stableのMcRemoteは止まる
  （`2026-10-22-01`）。切り替えの前のdoctorで確かめられるか
- 11月1日に名前を切り替える（`2026-10-22-04`）：旧protocolのサーバーの`sb`を`sb-retro`へ、公開VPSの`sb-beta`を`sb`へ。11月中は、
  `sb`と`sb-beta`のどちらも公開VPSの同じ安定版を指す。`sb-retro`は11月末で止め、12月から`sb-beta`を`2330.0.0`のbeta版にする。DNSと証明書の
  手順、切り替えにかかる時間の見込み、ScratchとWireScopeの名前（`scratch-beta`、`wirescope-beta`）を同じく切り替えるかの案
- 候補の置き場所（`/candidates/`、`2026-10-18-07`）：McRemoteのrc2とstableの候補を置くか。置くなら、rc1と同じ経路でよいか
