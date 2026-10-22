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

### WebのScratchとWireScopeの名前について（聞くこと）

human ownerは、11月1日から`scratch-beta`と`wirescope-beta`も`-beta`なしにそろえたい（`scratch.mc-remote.com`、
`wirescope.mc-remote.com`。WireScopeの名前の決まり`2026-08-20-01`は、stableを接尾辞なし、betaを`-beta`としている）。11月中は
`-beta`の名前も同じ安定版を指す案。まだ決めていない。影響の範囲を判断するため、自repoで次を返してほしい。

- その名前が、build済みの生成物（JS、OCI、ZIP、wheel）に入っているか、実行時の設定（runtime config、Caddy、Bridgeの許可）で
  決まるか
- 名前を変えたとき、または二つの名前で同じサーバーを出すときに、変える箇所と手間
- 利用者への影響：ブラウザに保存した作品、ペアリングのtoken、WireScopeの設定は、originごとに分かれる。名前が変わると
  見えなくなるものと、その案内
- README、文書、作例のリンクで、その名前を書いている箇所の数

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
   - `scratch-beta`と`wirescope-beta`：上の「WebのScratchとWireScopeの名前」で影響の範囲を返す。DNS、TLS、Caddyの経路、Bridgeの
     許可、runtime config、COOPなどのheaderを含めて
   - 12月の`sb-beta`（`2330.0.0`のbeta）：公開VPSに、安定版の`sb`と並べて置く。同じhostで二つのMinecraftのセットを動かすときの
     portの割り当て（予約の25566／25576、Java版のSRV record、統合版のUDP）、memoryなどの資源、Bridgeの経路の案を返す。急がない
     （11月中でよい）
   - 26.3用のプラグインの一覧：human ownerが10/28ごろに出す。DirectionHUDは、McRemoteのHUDへ機能を取り込めるまで残す
     （`2026-10-22-05`）。worldをリセットするかは、human ownerが10/31までに決める
