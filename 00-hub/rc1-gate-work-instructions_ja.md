# rc1横断release gate 着手依頼

> rc1横断release gate（`00-hub/release-gate-notes_ja.md`の2026-10-17の節）で、4担当の確認票（2026-10-17〜18）を受けて出す
> 着手依頼です。参照するknowledge commitは、この依頼が入ったmainのcommitです。各担当は、自分の節と「共通」を読んでください。

## 共通

- rc1はprotocol `23.2.1`（パッチ）、artifact `2321.0.0rc1`、GitHubのpre-release（`2026-10-17-03`）。APIとwireの中身は変えない
- 共有fixtureの23.2.1版は、中身を変えずに新しいfileとして出し、23.2の版は履歴として残す（`2026-10-18-03`）。履歴のfixture
  （v22、v23.1など）は改名しない
- 互換：23.2.1のcomponentは23.2.0のcomponent（McRemote b10、Python b9、Scratch b10）と話せること。各componentで、
  23.2.1と23.2.0の組み合わせを受け入れるtestを足す（判定の式は変えない）
- 依存順:
  1. Scratch担当がtoolingを23.2.1にし、fixtureの23.2.1版、WireScopeのZIPとmanifest、Bridge OCIを出して、identity（commit、
     file名、bytes、SHA-256、Actionsのrunとartifact ID、OCI digest）を返す。tag／Releaseの公開は凍結の後
  2. McRemote、Python、Scratchが、そのidentityを取り込んで版を`2321.0.0rc1`にし、candidateを作って返す。Stackは
     manifest v2のconsumerをmainへ入れる（1と並行してよい）
  3. coordinatorがexact setを凍結し、devの通常環境での確認と、3 OSのLANパッケージの試験を示す。Pass C（初めて読む人の通し）は、
     生徒がb10とホームページで10/24までに行う（human owner 2026-10-18）。rc1との差（版の番号、`はじめに.html`）は凍結の後に確かめる
  4. GitHubのpre-releaseを作る。公開VPSは別セットへ切り替える（`2026-10-18-02`）。PyPIはpre-releaseで試し終えてから承認する
     （`2026-10-18-04`）
- 日程（human owner 2026-10-18了承）：10/19〜20にtooling、10/20〜21に各candidate、10/22に凍結、10/23に試験、10/24にrelease。
  厳しければ、2321を落とさず日程をずらす（`2026-10-17-03`）。各担当は、遅れそうなら早めに返す
- 箱庭の名前：rc1の案内はすべて`sb-beta.mc-remote.com`を指す（`2026-10-18-05`）
- 返却：確認票の形式で、変わったところだけを追記として返す（branch／commit、artifactのbytes／SHA-256、実行したtestと結果、
  未検証の境界）。`knowledge contract commit`には実際に読んだSHAを書く
- しないこと：他repoの編集、shared環境の変更、人間参加の試験、tag／releaseの公開。これらは凍結の後に別の票で示す

## Scratch editor（minecraft-remote-tooling、LANパッケージ）

1. **tooling（最優先）**：`PROTOCOL_VERSION`を`23.2.1`にし、contract testを直す。fixtureの23.2.1版を新しいfileで足す。新しい
   commitのCIで、WireScopeのZIPとdetached manifest、Bridge OCI、candidate manifestを作り、identityを返す
2. **Scratch**：VMの`PROTOCOL_VERSION`、`client-version.js`、test（23.2.1のclientが23.2.0のserverを受け入れる回帰testを含む）、
   `mc-remote/tooling-lock.json`を新しいtoolingのidentityへ。b10を固定で書いたworkflowとscriptを、版から導く形にする
3. **LANパッケージ**：`mc-remote-scratch-LAN-2321.0.0rc1-<os>-<arch>.zip`の3 OSのcandidate。`127.0.0.1:8601`は変えない
4. **`はじめに.html`（`mc-remote/local/USER_GUIDE_ja.md`）**：冒頭は概略の流れだけにして、その後にOS別に分ける。macOSの許可の
   手順を観測に合わせる（警告の窓を閉じる、「システム設定」→「プライバシーとセキュリティ」の「このまま開く」、確認の窓でもう一度
   「このまま開く」、管理者のパスワード。`14-evidence/records/2026-10-17-b10-prerelease-3os-live-human_ja.md`）。設定画面のURLを
   リンクにする。設定画面の画像は、撮れれば置く。ホームページの`/lan/scratch/`との食い違いがあれば挙げる
5. **OCIのdigest**：candidateと公開で、version labelの文字列とbuildの条件（created、mtime、provenance／SBOM）を揃える。
   揃えることを目標にするが、揃わなくてもrc1を止めない。b9と同じく、差を記録して受け入れる（human owner 2026-10-18）
6. **README**：`README_mc-remote.md`の「自分のPCやLAN内」の直前と、`mc-remote/local/README.md`の冒頭に
   `https://mc-remote.com/lan/scratch/`を置く。`mc-remote/local/README.md`の「公開済み配布物ではありません」を直す。
   APIへのリンクは`https://mc-remote.com/api/`（今のprotocolのページへ送る入口）を使う
7. **ブロック一覧**：rc1の版ごとのsnapshot（`2321.0.0rc1`）を、release後にknowledgeへ取り込めるよう用意する
8. **pickerの26.3の名前**：GUIに同梱する名前のデータ（今は1.21.11と26.2）に、26.3を足す。取り出し方は`2026-09-30-10`
   （公式の言語データから、IDと各言語の表示名だけ）。26.3のサーバーにつないだときに日本語名が出ることを確かめて返す。
   aliasの検索（インベントリのタブのカテゴリーで探す、読みや呼び方）、読み上げ、検索欄の見た目は初回stableの後
   （human owner 2026-10-18）

## McRemote

1. `ProtocolInfo.PROTOCOL`を`23.2.1`、`pluginVersion`を`2321.0.0rc1`にする。`ProtocolInfoTest`で、23.2.0と23.2.1を受け入れ、
   23.3.0、他のmajor、不正な値を拒否することを明示する。23.2.0のclientのhelloを受け入れる確認は、`PreAuthTransportTest`への
   追加か、旧版のhelloのsmokeで行い、通常のlive-autoと分けて記録する
2. toolingのfixtureの23.2.1版が出たら取り込み、digestと件数を更新する。b10の履歴の素材は一括で置き換えない
3. 対応版は1.21.11と26.3のまま。candidateで両方のpulseを行う
4. README：`#lan`から最短手順へ直接来られる印（anchor）を置き、Step 3の直後に`/lan/scratch/`への1行を足す。READMEの
   `https://mc-remote.com/#quickstart`は、入口が`#lan`のところを直す。Windowsのmiseは今の手順のまま出す（hub NOTES 2026-10-17）
5. 未生成chunkの制限はrc1に入れない
6. candidateを作ったら、branch／commitとJARのbytes／SHA-256、pulseの結果を返す

## Python client

1. `PROTOCOL = "23.2.1"`、pyproject、uv.lockを`2321.0.0rc1`にする。23.2.1のclientが23.2.0のserverとつながるtestを足す
2. toolingのfixtureの23.2.1版と、新しいWireScopeを取り込む（`docs/tooling-consumption_ja.md`の手順。artifact ID、bytes、
   SHA-256を照合）
3. starterのtemplateの箱庭を`sb-beta.mc-remote.com`にする（`2026-10-18-05`）
4. README：Step 2の接続先の説明から`https://mc-remote.com/#lan`へのリンクを置く。案内の版の指定は
   `uv add "minecraft-remote-api==2321.0.0rc1"`
5. PyPI：release workflowは今の構成（`pypi` environmentの承認待ち）のまま。承認はhuman ownerが、GitHubのpre-releaseで試し
   終えてから行う（`2026-10-18-04`）
6. candidateを作ったら、branch／commitとwheel／sdistのbytes／SHA-256、同梱WireScopeのsourceを返す

## Stack

1. **最初に**：`agent/b10-manifest-v2-consumer@2eaf41b`をmainへ入れる（b10のcloseで入れるはずだったもの）。mainのCLIで、
   b10公開版のmanifestの`verify`が通ることを確かめる
2. rc1のpresetを用意する。各componentのrc1のtagとmanifestが出てから、版の値を入れる
3. 公開VPSは別セットへ切り替える（`2026-10-18-02`、`public-vps-cutover-guide_ja.md`）。箱庭を戻すことは考えない。26.3にするかは、
   human ownerが手元かGAMEsサーバーで26.3のセットを試してから決める
4. README：「ホームでb7.post2の新セット」の古い記述と、「目指す形と、今との差」の節を直す
5. 公開deploymentに、製品notice以外の追加noticeが出ていないかを確かめる（Scratchの製品noticeを一つに絞るpark）

## Java client（gateの条件にしない）

参加しない（`2026-09-30-04`）。protocol `23.2.1`への追従は、初回stableの後の追従で行う。
