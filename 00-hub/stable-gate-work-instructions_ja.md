# 初回stable（2321.0.0）横断release gate 着手依頼

> 初回stable（`00-hub/release-gate-notes_ja.md`の2026-10-22の節）の確認票の返却を受け、human ownerが次を了承した（2026-10-22）。
> McRemoteの`2321.0.0rc2`の公開、Scratch／toolingの最小限の配布対応、Pythonの版の番号だけの候補、Stackのrc2のpreset。
> 参照するknowledge commitは、この依頼が入ったmainのcommitです。各担当は、自分の節と「共通」を読んでください。

## 共通

- 決定：`2026-10-22-01`（stableの中身と日程）、`-02`（ガイドの側）、`-03`（stableの後の版）、`-04`（箱庭の名前の切り替え）、
  `-05`（箱庭をPaper 26.3へ、プラグイン、候補の置き場所）
- 箱庭の名前（`2026-10-22-04`）：11月1日に、旧protocolのサーバーの`sb`を`sb-retro`へ（11月末まで）、公開VPSの`sb-beta`を`sb`へ。
  11月中は`sb`と`sb-beta`のどちらも公開VPSの同じ安定版を指す。12月から`sb-beta`は`2330.0.0`のbeta版で、公開VPSに置く。
  確認票（knowledge `61d5fd8`）を返した時点の案（11月は`sb`を旧protocolのまま）とは違うので、自分の返却の該当箇所を読み替える
- 移行のページ：<https://mc-remote.com/migration/>（knowledgeが公開する。旧版の構成、移行スケジュール、Python、Scratch、サーバー）
- stableの候補は、10/30までに作って返す。凍結は10/31、公開は11/1 0:00（JST）から（gate notesの時間割）。この依頼では、McRemoteの
  rc2を除き、tag／Releaseの公開はしない
- 返却：実際に読んだknowledge commit、候補のsource commit、assetごとのファイル名、bytes、SHA-256（OCIはdigest）

### WebのScratchとWireScopeの名前（`2026-10-22-06`）

11月1日から、WebのScratchとWireScopeの安定版を`scratch.mc-remote.com`、`wirescope.mc-remote.com`で動かす。11月中は
`scratch-beta`と`wirescope-beta`も同じ安定版を出し続け、12月から`2330.0.0`のbeta版にする（ブラウザに保存した作品はoriginごとに
分かれるので、`scratch-beta`に保存した人が`.sb3`で書き出して移れる期間を置く）。README、教材、作例のリンクは`-beta`なしの名前
（`sb`、`scratch`、`wirescope`）にそろえる。`-beta`の名前は、ホームページからの案内と、将来は教材の一部で使う。自repoで次を返す。

- その名前が、build済みの生成物（JS、OCI、ZIP、wheel）に入っているか、実行時の設定（runtime config、Caddy、Bridgeが受け付ける
  origin）で決まるか。生成物に入っているなら、stableの候補で変える箇所
- 二つの名前（`-beta`ありとなし）で同じ安定版を出すときに、変える箇所と手間
- README、文書、作例のリンクで、`-beta`の名前を書いている箇所の数と、`-beta`なしへ変える時期の案（stableの候補に入れるか、
  `2321.1.0`か）

## McRemote

1. **rc2の公開（すぐに着手してよい）**
   - source：`agent/stable-rc2-legacy-config@7960a913a11c621d85e6120ee412b696fe125457` → `main`へfast-forward。fast-forwardに
     ならないときは止めて返す
   - tag：`v2321.0.0rc2`を`7960a91`へ。Release：`prerelease=true`、`draft=false`、Latestにしない
   - 照合：公開するJARが、確認票の候補 `mc-remote-2321.0.0rc2.jar` 315,871 bytes／
     `ce66abaf41a94800217a11161145b9f868333b7bfa605fd1f77b888878620e50`と同じであること。違ったら公開せずに返す
   - Release本文：確認票の`rc2-release-body-draft_ja.md`をもとに、旧`b5:`／`b7:`キーが残っていればPaperごと止まることと直し方、
     protocol `23.2.1`、feedbackの入口<https://github.com/Naohiro2g/mc-remote-knowledge/issues/new?template=feedback.yml>
   - 返却：mainの新しい先頭、tagが指すSHA、Release URL、run ID、assetのbytesとSHA-256
2. **stableの候補（10/30まで）**：rc2と同じsourceで、`pluginVersion`を`2321.0.0`にする。候補のJARのidentityを返す。公開しない
3. **追補（2026-10-29）：Temurinでの確認のやり直し**（`2026-10-29-01`）
   - JAR：同じ候補（`agent/stable-2321-candidate@525c31823a8efb736463aec471c2756089546391`、`mc-remote-2321.0.0.jar` 315,868 bytes、
     `e3f7cc2ab9ee9b3130f927935634e32e8ddffe7d7603b6d873973968f68db4ab`）。Javaを替えるだけのためにbuildし直さない
   - Java：Paper 26.3はTemurin `25.0.5+8`、Paper 1.21.11はTemurin `21.0.13+9`
   - Paper 26.3のbuild：human ownerが10/30の正午ごろに決める。決まったら、その番号とJARのSHA-256をknowledgeから伝える。
     1.21.11は先に始めてよい
   - 確かめること（搬送票の§3の1）：両方のPaperで、起動、有効化、正常な停止、認証した接続での建築と読み戻し、再起動の後の接続など
   - 人の確認はやり直さない（human owner 2026-10-29）。25.0.2などの過去の結果は書き換えない
   - 返却（10/30まで）：Paperごとに、Javaのvendorとfull version（`java -version`の出力）、PaperのbuildとJARのSHA-256、確認した
     項目と結果、使ったCIのrun（あれば）

## Python client

1. **stableの候補（10/30まで）**：rc1のtag `c30105349ef26413e925699143396ea05bd3e380`から、版の番号だけを`2321.0.0`にする（確認票の
   表の範囲）。作業中のREADMEの再編、移行ガイドの草稿、作例は混ぜない。候補のwheel／sdistとmanifestのidentityを返す
2. **Release本文の案**：確認票の`stable-release-notes-draft_ja.md`を、`2026-10-22-04`に合わせて直す。11月1日に`sb`が新protocolの
   安定版になり、旧protocolのサーバーは`sb-retro`へ移る（11月末まで）。旧版を続けるときは`==1214.10.13`を指定し、つなぎ先を
   `sb-retro`にする。移行のページへのリンク。rc1のWireScopeの注意
3. **starter**：stableでは変えない（`sb-beta`は11月も公開VPSの安定版を指すので、そのままつながる）。`sb`への書き換えは、12月の
   前に`2321.1.0`で行う
4. PyPI.orgの公開は、11/1にcoordinatorがGitHubの4 repoのassetを照合してから、human ownerが承認する（`2026-10-18-04`）

## Scratch editor（WireScope、minecraft-remote-tooling）

1. **Scratchのstableの候補（10/30まで）**：rc1のtag `ec79b3b0e364e722d6926a0932eb4bf088ddd3a1`から一時的な候補用のbranchを作る。
   developの本家の取り込みは入れない。入れるもの：
   - `client-version.js`を`2321.0.0`へ
   - 配布のscript 2か所（`scripts/build-mcremote-release-manifest.mjs`、`scripts/mcremote-local-artifacts.mjs`）が、接尾辞の無い
     stableの版を受け入れるようにする。commit、dirty、bytes、OS／archの検査は保つ。受け入れと、不正な値を拒むことの回帰test
   - `はじめに.html`の元（`USER_GUIDE_ja.md`）に、ホームページの`/lan/scratch/`へのリンクを1つ足す
   - LANのZIP 3つ、OCI（versionラベル`v2321.0.0`、revisionは候補のsource、`SOURCE_DATE_EPOCH`はそのcommitの時刻）、
     ブロック一覧の`site/2321.0.0/`と入口
   - 公開の後に、配布対応の変更をdevelopへ入れる（本家の取り込みは取り消さない）
2. **tooling**：`v2321.0.0`も`6447f6e8cbfbeeb9d229990b5c4f6e82a5875666`を指し、rc1の生成物（WireScopeのZIPとmanifest、Bridge
   OCI）をそのまま新しいReleaseへ出す案で進める。生成物のファイル名、manifestの中身、OCIのtagに`rc1`の文字が入っていて、
   stableの公開物として紛らわしくならないかを確かめて返す。入っているなら、どうするかの案を返す（作り直すとScratchの
   tooling lockまで固定し直しになるので、勝手に作り直さない）
3. 返却：候補のsource commit、ZIP 3つとOCIとブロック一覧のidentity、回帰testの結果、上の「WebのScratchとWireScopeの名前」

## Stack（mc-remote-stack）

1. **rc2のpresetと事前の起動**：McRemoteのrc2が出たら、rc2とPaper 26.3のpresetを作り、新しいセットを公開portなしで先に起動して
   試す（確認票の案どおり）。worldのコピーとリセットの準備も
2. **確認票の判定を求める事項への答え**（human owner 2026-10-22）
   - 11月の`sb-beta`：公開VPSを指したまま残す。12月以降も公開VPSに置く（`2026-10-22-04`）。Scratchからもつなげるよう、Bridgeの
     許可に`sb-beta`も入れる
   - `scratch`と`wirescope`（`2026-10-22-06`）：11月1日から`-beta`なしの名前で安定版を出し、11月中は`-beta`の名前でも同じ安定版を
     出す。DNS、TLS、Caddyの経路、Bridgeが受け付けるorigin、runtime config、ScratchからWireScopeへの受け渡しのheaderを、二つの
     名前の組で確かめる。手順と手間を返す
3. **`scratch.mc-remote.com`と`wirescope.mc-remote.com`を先に動かす**（human owner 2026-10-22「先に動かす案で進めて」）
   - 今の箱庭（rc1のセット）に、`scratch.mc-remote.com`と`wirescope.mc-remote.com`の名前を足す。`scratch-beta`と`wirescope-beta`は
     今のまま動かす。11月1日の夜中に、新しい名前の組で詰まらないよう、先に通しておくのが目的
   - ホームページや各repoからは、11月1日までリンクしない（knowledgeが11月1日にリンクを替える）
   - DNSはhuman ownerが付ける。Stackは、TLS、Caddyの経路、Bridgeが受け付けるorigin、runtime config、ScratchからWireScopeへの
     受け渡しのheaderを、`scratch.`→`wirescope.`の組と、`scratch-beta`→`wirescope-beta`の組の両方で通す。二つの組が混ざらないこと
     （`scratch.`から`wirescope-beta`へ渡るなど）も確かめる
   - 確かめること：二つの名前のどちらでも、Scratchを開いて拡張を読み込み、接続とペアリング、代表の操作（チャット、setBlock）、
     WireScope miniとWireScopeを開くことができる。外から証明書と応答のheaderを取って照合する。人間の操作が要る部分はhuman ownerへ
     頼む
   - 11月1日に切り替える26.3の新しいセットは、初めから両方の名前で作る
   - 返却：変えた設定（orderやoperator入力）のcommit、照合の結果、11月1日の当日に残る作業
   - 12月の`sb-beta`（`2330.0.0`のbeta）：公開VPSに、安定版の`sb`と並べて置く。同じhostで二つのMinecraftのセットを動かすときの
     portの割り当て（予約の25566／25576、Java版のSRV record、統合版のUDP）、memoryなどの資源、Bridgeの経路の案を返す。急がない
     （11月中でよい）
     - **訂正（2026-10-24、`2026-10-24-01`）**：上の「安定版の`sb`と並べて置く」はknowledgeの誤り。12月から、`sb`の
       Minecraftは有料のXServer GAMEs、`sb-beta`のMinecraftは公開VPSで動かす。公開VPSで二つのMinecraftのセットを常に
       並べることはない。統合版のportはTCPとUDPの19132（`2026-10-24-02`）
   - 26.3用のプラグインの一覧：human ownerが10/28ごろに出す。DirectionHUDは、McRemoteのHUDへ機能を取り込めるまで残す
     （`2026-10-22-05`）。worldをリセットするかは、human ownerが10/31までに決める
4. **追補（2026-10-28）：11月1日の26.3のセット**（knowledge `main@d5cb4208dffcafcc9d03eb07801b17e3a4917426`の記録による）
   - **Geyser**：b1269の指定を、Spigot版の2.12.1 b1273（SHA-256
     `218f57088fd7a147f670c489377da2341fc51f1867b2c36ed181f39c9f379b59`）に改める。b1269は統合版26.60のclientを切る
     （`F-geyser-nethernet`）。configは、b1273が作る既定の`config.yml`を変えずに使う（`sb-beta`の2026-10-28の更新と同じ。
     `transport: nethernet`、port 19132、`webrtc-port: 0`、signalingは`builtin`、HTTPSの指定なし）
   - **`nethernet/identity.pem`**：特別な作業はしない（human owner 2026-10-28）。平文のHTTPでは、信頼の確認がこの鍵ごとに出る。
     新しいセットでGeyserのdataが作り直されてidentityが変われば、全員に確認が一度出る。どちらになったかを、前後のSHA-256が
     同じかどうかで返す（鍵の中身は書かない）
   - **HTTPS**：入れない。signalingは今の平文のHTTPのまま（`2026-10-27-01`。HTTPSは初回stableの後、NOTES 2026-10-24の行）
   - **`connection_targets`（(a)）**：2026-10-24の返却どおり、Scratchの組ごとに`connection_targets`と既定を持たせて、
     このセットに入れる。接続先の一覧ひとつで管理する形（`2026-10-24-06`）と、Bridgeの対応表は後続で、このセットには入れない
   - **26.3用のプラグインの一覧**と**worldをリセットするか**：どちらもまだ（human owner 2026-10-28）。worldは10/31までに決める
     - **決まった（2026-10-29、Stackの確定搬送票）**：MinecraftはPaper 26.3。Paperのbuildはまだ決めない（human ownerが挙げた
       今のbuild #227を、そのまま採用の値にしない。その時点のlatestにも自動で追従しない）。決めたら、provider APIと取得物で
       JARのdigestを照合して固定する。プラグインは今と同じ組み（DirectionHUDを残し、AdvancedPortalsも入れる）で、それぞれ
       26.3とJava 25に合う最新版を使う（human owner 2026-10-29の訂正。版は現場で判断する）。worldはリセットせず、新しい26.3のセットへ引き継ぐ。12月以降のリセットの方針には広げない
   - **返してほしいこと（10/29まで）**
     - rc2と26.3のpresetを作り、新しいセットを公開portなしで起動して試したか。済んでいれば、その結果とidentity
       （commit、plan、lock）
     - b1273と既定のconfigで、新しいセットのGeyserが起動し、`/v1/join`が26.60で応答するか（公開portなしで確かめられる範囲で）
     - 10/31の凍結で、McRemote `2321.0.0`のJARの値を受け取ってから、stableのpresetを作るまでの手順と所要時間
     - 11月1日の切り替えで、Stackに残る作業の順序と、人間の操作が要る点（DNSはhuman owner）
   - **このセットに入れないもの**：HTTPS、統合版の別の名前、Bridgeの対応表、`home-server`の19132（別PR、gateに関わらない）
5. **追補（2026-10-29）：Java**（`2026-10-29-01`）
   - 新しい26.3のセットで、**Paperを実際に動かすcontainer**のJavaをTemurin `25.0.5+8`にする。hostのmiseだけを更新したことでは
     当てたことにしない
   - Paper 26.3のbuild：human ownerが10/30の正午ごろに決める。決まったら、provider APIと取得物でJARのdigestを照合して固定する
     （4の「決まった」のとおり）
   - 起動のflag：今回のreleaseでは変えない（human owner 2026-10-29）。今の箱庭と新しいセットのheap、containerのmemoryの上限、
     JVMのflagを、記録のために返す
   - 確かめること：公開予定のPaperのbuild、プラグイン、引き継ぐworldを含む新しいセットで、起動、参加、代表の操作
   - 返却：containerの中のJavaのvendorとfull version、imageのdigest、今の箱庭のJava（human ownerの報告では25.0.3。配布元と
     full versionも）、上の起動の設定と確かめた結果
   - 10/31の凍結の記録に、McRemoteのJAR、Paperのbuild、Javaのvendorとfull version、imageのdigestを入れ、公開まではその環境を
     保つ。変える必要が出たら、gateで判断し直す
