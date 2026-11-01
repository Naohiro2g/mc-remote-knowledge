# 初回stable 着手返却 — McRemote

- 作成日: 2026-10-22
- 対象repo: `Naohiro2g/McRemote`
- knowledge contract path: `00-hub/stable-gate-work-instructions_ja.md` 共通・McRemote、`00-hub/release-gate-notes_ja.md` 初回stable節、`00-hub/DECISIONS_ja.md` 2026-10-22-04〜06
- knowledge contract commit: `b3887126aa09ffde1981dcd4b6493ca5056eb3ae`を実読し、同remote mainのruntime protocolも取得。追加依頼の `abf8130faf8637fe1167af35477ea97bca43c42a` で着手票の全文とStack節3の追記を実読
- gate coordinator: knowledge担当session（Claude Code）
- human release owner: プロジェクトオーナー
- current phase: OPEN。許可されたrc2公開とstable候補作成の結果を返す。横断判定と人間試験の開始はcoordinatorへ返す

## 1. rc2の公開

旧main `192a777ae1d484bcc9b58fcc7c58d6aed1a374af`からfast-forwardした。source SHAの変更・merge commitの追加はない。

- mainの先頭: `7960a913a11c621d85e6120ee412b696fe125457`
- annotated tag: `v2321.0.0rc2` → `7960a913a11c621d85e6120ee412b696fe125457`
- Release: https://github.com/Naohiro2g/McRemote/releases/tag/v2321.0.0rc2
- Release ID: `420311190`
- `prerelease=true`、`draft=false`。Latestは`v1.21.8-1.4.0`のままとAPIで照合
- tag CI: [39719769373](https://github.com/Naohiro2g/McRemote/actions/runs/39719769373)、success
- Release dry run: [39723170103](https://github.com/Naohiro2g/McRemote/actions/runs/39723170103)、success
- Release公開workflow: [39723317773](https://github.com/Naohiro2g/McRemote/actions/runs/39723317773)、success

公開前にタグCI artifact `12400189381`を取得し、JAR 315,871 bytes／SHA-256 `ce66abaf41a94800217a11161145b9f868333b7bfa605fd1f77b888878620e50`が確認票の凍結候補とbytesまで一致することを確認した。その後、既存Release workflowでタグCIのcandidateを再buildせず昇格した。

公開後に全5 assetをReleaseのdownload経路で再取得し、次の値と元素材のbytes一致を照合した。

| asset | bytes | SHA-256 |
| --- | ---: | --- |
| `mc-remote-2321.0.0rc2.jar` | 315871 | `ce66abaf41a94800217a11161145b9f868333b7bfa605fd1f77b888878620e50` |
| `manifest.json` | 1988 | `f5c60a852921e25c1cfb00d4a4f5df76afa0e8de701ae61e8c1f397993c524b6` |
| `minecraft-targets.json` | 126 | `8e830732decd6bcde13f91eb6c071d062ba6993342a7edb52e6ea543b9e0c361` |
| `mc-remote-verification-1.21.11.json` | 62784 | `96cb1262c0c422a06c39e2af5e3aea4659c47ab74ec7ac12fcfe76a984a3c5cd` |
| `mc-remote-verification-26.3.json` | 62766 | `f31d7ddff902c8951242d0a95fa1e24a6a5083235de2e8603a788a16b2a50501` |

Release本文は確認票の案をもとに作成し、旧`b5:`／`b7:`があればPaper全体が停止すること、値を新キーへ移して旧セクションを消すこと、protocol `23.2.1`、指定の[feedback入口](https://github.com/Naohiro2g/mc-remote-knowledge/issues/new?template=feedback.yml)を掲載・公開後に照合した。

## 2. stable候補（公開していない）

- branch: `agent/stable-2321-candidate`（push済み）
- source commit: `525c31823a8efb736463aec471c2756089546391`
- 親: rc2 `7960a913a11c621d85e6120ee412b696fe125457`
- source差分: `gradle.properties`の`pluginVersion=2321.0.0rc2` → `2321.0.0`の1行のみ
- JAR: `mc-remote-2321.0.0.jar`、315,868 bytes
- JAR SHA-256: `e3f7cc2ab9ee9b3130f927935634e32e8ddffe7d7603b6d873973968f68db4ab`
- CI: [39720103168](https://github.com/Naohiro2g/McRemote/actions/runs/39720103168)、success
- CI artifact: `mc-remote-candidate`、ID `12399974471`、294,756 bytes
- artifact ZIP SHA-256: `2995b4d47bf8de885c0206d615cf692ac0d583db4c3534320606821aea49d699`

候補は既存`./gradlew clean jar`でbuildしたものとCI取得物のbytes一致を確認した。rc2とのJAR全entry比較では`plugin.yml`の版表記だけが異なり、全classと他のresourceのbytesは一致した。
CI候補内のfile別identityは次のとおり。source／checksumsはpacket内ではstable-を付けて保持している。

| file | bytes | SHA-256 |
| --- | ---: | --- |
| `mc-remote-2321.0.0.jar` | 315868 | `e3f7cc2ab9ee9b3130f927935634e32e8ddffe7d7603b6d873973968f68db4ab` |
| `minecraft-targets.json` | 126 | `8e830732decd6bcde13f91eb6c071d062ba6993342a7edb52e6ea543b9e0c361` |
| `source-commit.txt` | 41 | `3201d74bd5e694d735303ef5d55c9591a7796582654f21b723e9050fb380fb47` |
| `SHA256SUMS` | 89 | `682ea59a1141ce2ab6d6ca810b02fada535c243101a608cf30967b7e2daebb83` |

stableのtag／GitHub Releaseは作成していない。mainはrc2のままで、stable候補は作業branchに保持する。10/30返却期限より前に候補の用意は完了した。rc2の人間試験とcoordinatorの10/31凍結・公開指示に従う。

## 3. 共通 — WebのScratch・WireScopeの名前

### 生成物に埋め込まれているか

McRemoteの全追跡fileとrc2／stableのJAR全entryを検査し、`sb`／`scratch`／`wirescope`の各`.mc-remote.com`と、その`-beta`版の埋め込みは0件。追跡fileの`sb-beta`／`scratch-beta`／`wirescope-beta`断片も0件。
McRemoteはTCPの`api_port`で接続を受ける。Webのホスト名やBridgeの許可originをJARに固定していないため、今回の名前の追加に伴うMcRemoteの再build・設定変更は不要。DNS／TLS／Caddy／Bridgeの許可origin／runtime config／headerはStack担当の着手項目。

### 二つの名前で同じ安定版を出すとき

McRemote側の変更箇所0件、追加の実装工数なし。同じTCP接続先に解決する構成では、同じJARをそのまま使用できる。実際の名前の経路と組合せの成功はStackの検証で確認する事項として扱い、McRemoteの静的監査から接続成功を主張しない。

### README・文書・作例のリンク

追跡fileの`-beta`リンクは0件（README、docs、scripts、src、release、.githubを含む全追跡fileの検査）。変更対象が無いので、stable候補／`2321.1.0`ともこの名前のための修正は不要。READMEのLAN案内は従来の`https://mc-remote.com/lan/scratch/`を使う。
`abf8130`のStack節3に合わせ、新しいWeb名へのリンクを11/1より前には追加していない。今のrc1セットへ二つのWeb名を先に足し、両方の名前の組を通す追加作業はStackの担当項目として確認した。

## 4. 検証と境界

- test class: unit/deterministic、既存CI、公開assetの取得とidentity照合。
- rc2の357 testsと1.21.11 #132／26.3 #203のruntime PASSは元の確認票・検証recordのidentityを維持し、公開JARとbytes一致で接続した。
- stable候補はCI成功と版だけの差分・JAR内容比較を確認した。rc2のruntime recordをstableの別SHAへ書き換えていない。
- 実環境へのdeploy、Stackの設定変更、人間参加試験は今回のMcRemote作業に含めていない。Webの名前の事前稼働成功は未確認。
- 未追跡の`mise.toml`は保持。製品の変更はstable候補の版番号1行だけ。

## 5. 後続へ渡すこと

- coordinatorへ: rc2公開物のidentity照合結果、stable候補identity、共通のWeb名の影響0件を返却する。
- rc2の人間試験、Stackのpreset／事前稼働、新しい名前の組の検証、stable凍結・公開は担当票どおり進行する。
- 正式evidenceの着地はknowledge側。rc2の元検証は`handoff-materials/2026-10-22-stable-rc2-confirmation/`を参照し、本packetとともにgate close分類まで分類②で保持する。
