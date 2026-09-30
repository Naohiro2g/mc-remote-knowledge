# b8横断release gate 確認票依頼

> b8横断release gate（`00-hub/release-gate-notes_ja.md`の2026-09-30の節）を開いたときに、各担当へ出す確認票の依頼です。
> 参照するknowledge commitは`2d0830a741997573248ee94e945c719316a0c299`です。各担当は、自分の節と「共通」を読んで
> 確認票を返してください。shared環境の接続先は、この段階では使いません（candidateの配置と人間参加の試験は、
> exact setを凍結した後に別の票で示します）。

## 共通

返却は`release-gate-notes_ja.md`の確認票の形式。`knowledge contract commit`には実際に読んだSHAを書く。
自repoの事実と根拠だけを返し、他repoへの着手、shared環境の変更、人間参加の試験はしない。

各担当に共通で聞くこと（hub NOTESの棚卸し、`2026-09-30-09`）:

- READMEの人間向け再編（hub NOTES 2026-08-28 `[priority]`）は終わったか。残っているものは何か
- 担当agentが実際のbrowserを操作できる範囲（DOM操作、click／type、screenshot、localhostの表示）。b8のlive-humanに
  real-browserのWireScope確認が入るため（hub NOTES 2026-08-28のpark行）

## McRemote

- b8 candidateのbranch／commit（照会の回答では`b3b3ba8`）と、1.21.11向けJARのbytes／SHA-256
- B8のentity lifecycle四method、Particle Stage 2、サウンド2 method、resource IDの無印の受け入れが、そのcandidateに
  入っているか
- b8必須是正（main `4d39362`／`6f8d69d`）とcredentialの自動初期化（`2026-09-25-01`）がcandidateの祖先にあるか
- 実施済みのtest（unit、live-auto）と、認証／credentialの強化分として行ったもの
- B8共有fixtureの使用状況（Scratchが発行したbytes／SHA-256）。resource IDのcaseを消費し、公開済みb7のJARで落ちる
  ことを確かめたか
- 移管の準備: 共有fixtureを自repoのどこへどう取り込み、どのtestがdigestを見ているか。scratch-editorのrepo名や
  URLを直接書いている箇所があるか
- 10/3に対する見込みと、止まっている点

## Python client

- b8 candidateのbranch／commitと、wheel／sdistのbytes／SHA-256
- B8のPython surface（entity lifecycle、ParticleSpec、サウンド）、短いimport、`pygame` extraの状況
- 3D graphの小さいsampleの有無
- 同梱WireScopeの取得元（Scratchのsource commit）と、23.2.0への対応
- B8共有fixtureの使用状況（resource IDのcaseを含む）
- resource ID（block、particle、entity、sound）を無印のまま送るか、client側で`minecraft:`を補ってから送るか、
  client側で無印を拒否していないか（`2026-09-30-06`）
- Windowsでの導入手順の検証の準備（手順、誰が通すか）
- 移管の準備: 共有fixtureの取り込み方、`bundled_wirescope_source_commit`の作り方、scratch-editorを直接書いている箇所
- 10/3に対する見込みと、止まっている点

## Scratch editor（WireScope）

- B8共有fixtureの発行状況（commit、bytes、SHA-256、case数）。サウンドのcaseと、resource種別ごとの無印・完全修飾・
  非正準形のcase（`2026-09-30-06`）を含むか
- `@mc-remote/protocol` 23.2.0のmirror、WireScopeのvalidator／method認識／sanitizerの状況とbranch
- resource IDの無印: Scratchは無印のまま送るか補ってから送るか、WireScopeのvalidatorが無印を不正と表示しないか
- カタログのID一覧をリストへ入れるブロック（搬送票1。b8に入れる）のcommit状況
- カタログピッカー: いまのpickerで日本語名（例: `金ブロック / Block of Gold / gold_block`）が出るか、その名前をどこから
  持ってきているか、検索が何を対象にしているか（`block-value-design_ja.md` §8、`scratch-block-value-projection-design_ja.md` §7）。
  名前は公式の言語データから最小限（IDと各言語の表示名）だけを保存し、言語ファイル全体は持たない（`2026-09-30-10`）
- Scratch runtime（VM／GUI）とlearner blockをb8で変えるか（変えない場合もその旨）
- NOTES `[priority]` b7 release後の是正候補3件の状態
- post-b7のWireScope時刻表示と配置の復元、拡張機能選択画面のMcRemoteカード説明の修正（hub NOTES 2026-09-03のpark
  2行）に着手したか
- 移管の準備: protocol package、fixture、WireScope、Bridgeのrepo内の依存（何が何をimportするか）、Scratch VMが
  fixtureをどう読んでいるか、release workflowが出すmanifestの`wirescope`／`wirescope-manifest`／`contracts`の中身
- 10/3に対する見込みと、止まっている点

## Stack（deploymentの準備）

- `dev-integration`（1.21.11）の現状と、b8 candidateを置ける状態か
- 稼働中deploymentのidentity（MC版、Paperのexact build、Java版、McRemote JARのSHA-256）を示す`status`があるか
- 移管の準備: Scratch releaseから何をどう集めているか（WireScopeや`contracts`が別repoへ移ると、収集の入口が増える）
- 26.3のdeploymentは、Paper 26.3のstableが出た後に頼む（`2026-09-30-07`）。いまは用意しない
- hub NOTESの2026-07-23のpark 8行（plugin config ownership、world lineage、backup lifecycle、restore contract、
  recommendation、`mc-remote.toml`の物理ファイル粒度、dev／alphaのdeployment運用差、preset registry）が、Stack側で
  決着したか、Stack側の正本がどこか。特にbackup lifecycleとrestore contractはrc1のrollbackに直結する
- public側のWireScope（hub NOTES 2026-08-20のpark行）が配信されているか。①DNS／TLS等〜⑥multi-user等のどれが残っているか
- candidateの配置はまだしない。exact setとauthorized next actionは後で示す
