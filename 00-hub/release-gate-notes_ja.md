# Release gate notes — public baseline

> 新public正本世代の単一template／状態集約。旧世代のrelease固有履歴はcarryしない。

release判定は、実装repo側が事実と根拠を記入し、単一のgate coordinatorがknowledge側で
contractと照合します。shared環境へのcandidate deployと人間参加試験は、coordinatorがexact setと
許可済みの次操作を示した後に行います。責務と正準進行は
[release運用と責務分担](release-operations-responsibility-design_ja.md)を参照します。
秘密実値、private inventory、未sanitized raw logはここへ貼りません。

## 確認票

```markdown
## Release gate 確認票

- 対象 repo:
- 対象 branch/commit:
- release / channel:
- gate coordinator:
- human release owner:
- current phase:
- contract maturity / required test tier:
- knowledge contract path:
- knowledge contract commit:
- gate manifest identity:
- change cone:
- reused PASS / rationale:
- exact compatibility set / freeze status:
- target deployment / profile / lock:
- authorized next action:
- test class: unit/deterministic / live-auto / live-human
- 実行した command / 手順:
- 結果:
- evidence record / artifact:
- 未検証の境界:
- security / compatibility / rollback の確認:
- 判定を求める事項:
```

`live-human` や高い再現コストを持つ検証は `14-evidence/` の sanitized record を参照します。private evidence は `mc-remote-backstage`、秘密を含む raw は Git 外です（`2026-07-06-03` / `2026-07-21-04`）。

repo担当は自repoの事実と根拠を返し、他repoの着手、shared環境へのdeploy、人間参加試験、横断判定を
開始しません。candidate identityが変わった場合は旧exact setを失効させ、gate coordinatorへ戻します。
ただし旧setの観測事実まで自動的に破棄せず、`2026-08-23-01`のchange coneとPASS再利用条件で再評価します。
仕様形成中はTier 0〜2を既定とし、人間参加・全回帰・capacity／soakをrelease候補より前へ自動的に持ち込みません。

## 単独更新の記録書式

単独更新のrelease gate（release運用と責務分担 §15、`2026-09-27-05`）は、次の1件で記録します。

```markdown
## YYYY-MM-DD 単独更新 <component> <version>

- 基準set:
- 差し替え: <component> <旧版> → <新版>
- change cone:
- 実施した確認:
- 再利用したPASSと理由:
- non-claim:
- coordinator判定／human release owner承認:
```

## 2026-09-27 単独更新 minecraft-remote-api 2301.0.0b7.post3

- 基準set: b7.post2（2026-09-07）
- 差し替え: minecraft-remote-api `2301.0.0b7.post2` → `2301.0.0b7.post3`
- change cone: docs／metadata（README、`requires-python`、classifiers、CI、release workflow）。Python担当の報告ではコードはpost2と同一（coordinator未照合）
- 公開identity: tag `v2301.0.0b7.post3`（annotated、`1ea043b`）、Release「minecraft-remote-api 2301.0.0b7.post3」（prerelease）。wheel SHA-256 `76e56f9eacbddcdee0c7a5558d7a941f2c735f48c93866de955a3ad03b55fc62`、sdist SHA-256 `c883b2764698a0035cc0fe3f4bec0a381af29ed9f3639da5265277209e8dec0b`。coordinatorがRelease assetとTestPyPIのdigest一致を照合済み（2026-09-28）
- 実施した確認: pytest 253/253（CI 3.10〜3.13）。TestPyPIからexact-pinで入れたpost3で、sb-betaへのhello.pyとpairingが成功（human、報告ベース）。詳細は`14-evidence/records/2026-09-28-python-testpypi-soak-gates_ja.md`
- 再利用したPASSと理由: McRemote、Scratch、WireScopeはpost2のまま。post2からの変更はREADME、docs、PUBLISHING、pyprojectのmetadata、CI、release workflowだけで、wire、protocol、共有fixture、他componentが読む形、認証まわりに触れていない（Python担当の報告）
- non-claim: PyPI.orgへの公開はしない。mature判定はしない。Windowsでは検証していない
- coordinator判定／human release owner承認: human ownerがpost2のsetへの組み入れを判定（2026-09-26、`2026-09-27-01`）。coordinatorはchange coneが閉じていることを確認し、単独更新gateを通過とする（2026-09-28）。**CLOSED**

## 2026-10-07 b10横断release gate（OPEN）

- gate coordinator: knowledge担当session（Claude Code）。人間による明示handoffなしに他担当へ移さない
- human release owner: プロジェクトオーナー
- current phase: **OPEN**（2026-10-07、human ownerの判断）。実装・検証・公開はいずれも未実施
- 目標日: b10 2026-10-17。rc1（10/24まで）と初回stable（11/1）の目標日は維持する
- release mode: 軽量mode（release運用と責務分担 §14、`2026-08-28-02`）。単一JARとケータリング型簡易版のZIPは新しい配布の形
  なので、その部分は§14の但し書きにより検証を強める（b9の移管と同じ扱い）
- contract: protocol `23.2.0`のまま、artifact `2320.0.0b10`。APIは変えない
  - b10の範囲: `2026-10-07-03`（tick分割、単一JAR、名前）、`2026-10-07-04`（ケータリング型簡易版）、`2026-10-07-05`
    （`mcr.build.blocks`の既定）、`2026-10-07-06`（対応版の一覧の作り方）
  - 前提の決定: `2026-10-07-01`（1要求32768、TPSの位置づけ）、`2026-10-07-02`（認証前の上限超過は閉じるだけ）
  - gate開閉時のpark確認: `2026-09-30-09`
- 基準set: b9（McRemote `v1.21.11-2320.0.0b9`、Python `v2320.0.0b9`、Scratch `v2320.0.0b9`、minecraft-remote-tooling
  `v2320.0.0b9`）。McRemoteはその後の`main@cff92c09c39159bb1fe7964bfbb35de9a1c0f4d5`（認証前の制限、`mcr.build.blocks`、
  1要求32768。platform-design §8.2・§8.3）から始める
- 参加component:
  - McRemote:
    - setBlocksのtick分割：既定の1要求32768を既定のtick予算のまま施工できるようにする。同じ接続の後続を追い越させず、
      id付き要求は全量の施工後に`result:null`。切断、途中の失敗、複数接続・同じplayerの進み方は実装前に整理する
      （McRemoteの検討案`setblocks-tick-slicing-proposal_ja.md`）
    - 単一JAR：Java 21／Paper 1.21.11を開発の床とし、1.21.11と26.2で同じSHA-256のJARを検証する（§4のpulse）。Paper 26.2の
      exact buildは公式Downloads Serviceから取得して確認票で固定する。初回stableの26.xを26.2か26.3かはrc1のgateを開くときに
      判断する。名前はtag `v2320.0.0b10`、JAR `mc-remote-2320.0.0b10.jar`、titleは対応版を列挙（versioning §10.12.1）
    - 対応版の一覧（`2026-10-07-06`）：candidateのbuild前に対応対象を宣言し、同じJARで各対象を検証し、宣言とPASSの集合が
      一致することを公開時に確かめる。その一覧からhelloの`supported_mc_versions`の配布値、release title、本文を揃える
    - `mcr.build.blocks`の既定：configのトップレベル`default_build_blocks`（配布既定32768）。LuckPermsが無いときはこの値、
      LuckPermsがあってmetaが無いときは`0`。既存configの明示値は上書きしない（platform-design §8.2）
  - Scratch（toolingのBridgeを配布入力にする）:
    - ケータリング型簡易版：標準からDocker、証明書の設定、Stackのpreset／orderを除いたもの。Scratch、Bridge、実行環境、
      ランチャーをOS別のZIP（Scratch Local版）にまとめ、1台構成とLAN構成に対応する。認証はON。
      `mc-remote-scratch-local-2320.0.0b10-{windows-x64,macos-arm64,linux-x64}.zip`をScratchのrelease `v2320.0.0b10`の
      assetとし、公開releaseの`manifest.json`（`mc-remote.release-manifest` v1）へrole `scratch-local`、kind `https-file`、
      `os`、`arch`で載せる。サーバー側はMcRemote READMEのクイックスタートへ案内する
    - 公開するZIPと同じSHA-256でWindows 11、macOS、Linuxを検証し、構築の手順と運用で要る調整（OSの警告、firewall、接続先、
      ペアリング）を観察して記録する。Windowsは、SmartScreenの個別許可と、アプリ単位の許可が無いSmart App Controlを分けて
      観察する。署名・公証の要否はこの結果で判断する。同梱物のライセンスは`2026-08-11-01`の配布前確認を通す
  - 不参加: Python（APIが変わらず、簡易版の案内先もMcRemote README）。minecraft-remote-toolingは、Bridgeの配布入力として
    固定版を使うだけなら新しいreleaseを出さない（Scratchの確認票で確かめる）
- 範囲に入れないもの: 未生成chunkの制限（hub NOTES 2026-10-07の候補）、新しいmethodやclientのjob／progress API
- gateを開くときのpark確認（`2026-09-30-09`、`tools/list-reopen-conditions.py`）: b10に結びつく2件を拾った。
  setBlocksのtick分割はMcRemoteの範囲として着手する。FASTのparticleが負荷のもとで黙って描かれない件は、b10の範囲に入れず、
  消費した件数を認証前と同じ理由別の集計に足す程度で軽く済むかをMcRemote担当に聞く（軽く済まなければ初回stableの後へ送る）。
  rc1に結びつく行（製品notice、OCIのversionラベル、API一覧、rollback、README再編、block value投影の残り、未生成chunk、
  認証前テーブルの較正）はrc1 gateで見る

## 2026-10-04 b9横断release gate（CLOSED）

- gate coordinator: knowledge担当session（Claude Code）。人間による明示handoffなしに他担当へ移さない
- human release owner: プロジェクトオーナー
- current phase: **CLOSED**（2026-10-06、human ownerの判断）
- 目標日: 2026-10-10 release（`2026-09-29-02`）
- release mode: 軽量mode（release運用と責務分担 §14、`2026-08-28-02`）。移管はconsumerの取得経路とrelease workflowを
  変えるので、その部分は§14の但し書きにより検証を強める
- contract: protocol `23.2.0`のまま、artifact `2320.0.0b9`（`2026-09-30-03`）。APIは変えない
  - b9の範囲: `2026-09-30-03`（API freeze、移管、PyPI登録）
  - freeze前の契約2件: `2026-10-03-01`（id付き`chat.post`の成功resultは`null`）、`2026-10-03-02`（知らないevent typeで
    `events.poll`を失敗させない）
  - 移管: `2026-09-13-02`（b8後へ送った）、`2026-09-30-04`（Java以外のconsumerで行い、Javaは初回stable後に再検証）、
    移管計画、人間向け固定文
  - PyPI: `2026-09-26-03`（機構モード soak→mature）、`2026-09-29-02`（Windowsの検証を受けてmature判定をしてから登録）、
    versioning-design §10.9の遷移ゲート①〜④
  - API一覧: `2026-09-30-05`（公開releaseだけ、knowledgeが持つ）
  - gate開閉時のpark確認: `2026-09-30-09`
- 基準set: b8（McRemote `v1.21.11-2320.0.0b8`、Python `v2320.0.0b8`、Scratch `v2320.0.0b8`）
- 参加component:
  - McRemote: 契約2件のうち`chat.post`のresult、JARのunix権限bitの固定（hub NOTES 2026-10-03）、移管後のfixtureの取得経路
  - Python client: PyPIへの登録（TestPyPIでの予行とmature判定の材料）、知らないevent typeの扱い、移管後のfixtureと
    同梱WireScopeの取得経路
  - Scratch editor（Bridge・WireScope同梱）: 移管の現ownerとして調査と実施、知らないevent typeの扱い（Scratch、WireScope）、
    WireScopeの列幅（`agent/b8-compatibility@01cdb0b`、b9で出す）、pickerのalias検索
  - 不参加: Java（`2026-09-30-04`。契約2件には自分で追従し、gateの条件にしない）。Stackはdeploymentで関わる
    （human ownerの直接管理、2026-10-01）
- 変更範囲（change cone）:
  - 移管: Protocol projection、shared fixture、WireScope、Bridgeのowner → 各consumerの取得経路、owner test、CI、
    release workflowとmanifest、Pythonの同梱WireScope、Stackの収集の入口
  - 契約2件 → McRemoteの`chat.post`、各clientのpoll、shared fixtureのcase
  - Pythonの公開チャンネル → TestPyPI／PyPIへのpublish workflow、exact-pinの手順
  - McRemoteのJARの作り方 → JARのdigest（中身は変えない）
- required tier: 確認票と移管の作業はTier 2。exact set凍結後にTier 3（移管の前後でfixtureとartifactが同じであることを
  確かめる。代表往復だけlive）
- acceptance:
  1. 移管した後のowner（`minecraft-remote-tooling`）が、b8時点のfixture 12件（移管計画の「b8時点の起点」）をbyte一致で再現する
  2. McRemote、Python、Scratchが、新しいownerと取得経路からfixtureを取ってconsumer testを通す。Scratch側に編集できる
     owner copyを残さない（hybridを選んだ場合は終了条件を先に決める）
  3. 移管の前に戻せる（rollback先はb8のScratch source `691576f`とfixture一覧）
  4. 契約2件に各componentが適合し、shared fixtureにcaseがある
  5. API freeze: wireの§4コマンド表と§7.3 error表がb8から変わらない（API一覧の`api.json`の差分で確かめる）
  6. Python: TestPyPIで予行し、遷移ゲート①〜④の材料をそろえる。mature判定とPyPI.orgへの登録はhuman ownerが決める
  7. McRemote: 手元とCIのJARのdigestが一致する
  8. 1.21.11での代表往復。live試験の開始時にhelloの`mc_version`を照合し、違えば本体を実行せずFAIL
- 再利用するPASS: b8のlive PASSは、APIを変えないので再利用する。移管と契約2件で変わる箇所だけを取り直す
- 日程（案）: 10/5に確認票の返却 → 10/6に移管のtopologyと範囲を決める → 10/6〜10/8に作業と凍結 → 10/9に実機試験 →
  10/10にrelease。移管が10/10に収まらない見込みになったら、10/6の時点で日程か範囲を相談する
- park確認（`2026-09-30-09`、`tools/list-reopen-conditions.py --release-tied`、2026-10-04）: b9 gateを開くときに再開する
  行を次のように扱う
  - McRemote JARのunix権限bit: b9に入れる（McRemoteへ依頼）
  - freeze前の契約2件: b9に入れる（確認票で聞く）
  - API一覧: 公開版ごとに残すページ、クライアントAPI一覧とのつなぎ方を、b9の公開に合わせて決める
  - public README／sample codeの再編: 各repoの残りを確認票で聞く
  - `2026-08-23-01`のrelease gate方法論の残り（gate manifest）: b9でも作らない案をhuman ownerに示す
  - protocol 22 Scratch block value投影の残り: Scratchの確認票で聞く
  - b8で非blockerにしたもの: サウンドのlearner block（command 2つとoptionsのブロック）とpost-b7のpark 2件はb8に入って公開済み
    （b8の節の凍結とsegment 3）。残るpickerのalias検索と、b7 release後の是正候補のうちb8で終わらなかったものをScratchの確認票で聞く
- 判断を求める事項: API freezeの範囲（wireだけか、Python APIとScratchのブロックも含めるか）。b9に残る学習面の作業
  （pickerのalias検索）には影響しないので、確認票の返却の後に決める
- 確認票の返却（2026-10-04。担当報告、coordinatorはhandoff-materialsの票を読んだだけで照合していない）:
  - McRemote（`main@14cd3b7`、knowledge `71814e4`、48 tests PASS）: id付き`chat.post`は送ったmessageの文字列をresultに
    返している（`2026-10-03-01`に合わない。`null`へ直す）。知らないevent typeはserverに選別がなく、successor fixtureで照合する。
    JARの権限bitは`tasks.jar`に`filePermissions { unix("0644") }`と`dirPermissions { unix("0755") }`を足す案で、umask
    002／022の手元buildとCIのdigestを比べる。共有fixture 4件（direction-lightning、entity-particle、events、sign）は
    `src/test/resources/fixtures/`へのcopyで、公開b8 sourceとbyte一致。取得元を変えるだけならbuildとruntimeは変えない。
    scratch-editorの直接記載はコメント5箇所。b8の後のmainは`14cd3b7`（smoke／player testの既定protocolを`23.2.0`へ）。
    見込みは着手後1〜2作業日、10/6に移管先が決まれば10/8にcandidateを返せる
  - Python（`main@7981031`、knowledge `71814e4`）: 知らないevent typeで`decode_event()`が失敗し、batch全体が落ち、cursorが
    進まず同じeventを取り直し続ける（`2026-10-03-02`に合わない）。省略で直す予定。`chat.post`の`null`は`None`として
    受けられる。共有fixture 6件（Protocol 4、WireScope 2）はcopyでsidecarにprovenance、同梱WireScopeはScratch
    `df34849`から作ったZIP／manifestのvendor。Bridgeは使っていない。PyPI: TestPyPIの固定triggerは動いている。PyPI.org用の
    jobは未実装。遷移ゲート①〜③はb7.post3の記録あり（③のPyPI.org側のowner／2FAは未確認）、④はWindowsが未了。
    human ownerの外部操作は、PyPI.orgの既存project `minecraft-remote-api`の権限と2FAの確認、Trusted Publisherの登録
    （`Naohiro2g`／`minecraft-remote-api`／`release.yml`／environment `pypi`）、GitHub environment `pypi`の保護設定。
    b8の後のmainは`74243d4`（README等を公開状態へ）と`7981031`（PythonクライアントAPI一覧のドラフト）。見込みは1〜2作業日
  - Java（gateの条件にしない、knowledge `06b069a`）: freeze前の契約の棚卸しは完了で、2件のほかに決めることは残っていない。
    2件へは未commitで追従済み。fixture 3件はcopyで、Scratchのpathやrepositoryが変わってもbuildとCIは切れない
  - Scratch（`develop@00c0146`、knowledge `ceba530`）: 知らないevent typeで、Scratch VMはpoll応答を拒否してpollerを止め、
    WireScopeはsnapshot全体を拒否する（`2026-10-03-02`に合わない）。`chat.post`の`null`はScratchが受けられるが、WireScopeは
    `true`なども受けてしまい、mirrorに`ChatPostResult = null`が無い。fixture 12件は公開b8とbyte一致。b7 release後の是正3件は
    すべてb8に入っていた。WireScopeの列幅`01cdb0b`はdevelopに未統合。pickerのalias検索は未実装（名前データの置き場所、
    schema、二段表示はb8で実装済み、読み上げは人間の確認が未了）。b8の後のdevelopは`16887de`（READMEにAPI一覧への
    リンク）と`00c0146`（Scratchブロック一覧のドラフト）。移管は別紙`ASSESSMENT_ja.md`で、共通TypeScript tooling monorepo、
    Bridgeは今の機能のまま共通ownerへ、fixtureは固定Git SHA、WireScopeは固定digestの生成物で取得、を推奨。見込みは契約2件と
    追加fixtureが0.5〜1作業日、monorepoへの移管が2〜4作業日で、10/10は条件付き
- Windows（2026-10-05）: クリーンなWindows 11から、Gitなしでuv、b8のRelease wheel、import、JupyterLabまで成功した
  （human ownerの報告、`14-evidence/records/2026-10-05-python-windows-entry_ja.md`）。遷移ゲート④の材料がそろった。mature判定は
  human owner
- PyPI.orgの準備（2026-10-05）: human ownerが完了を報告した（Python確認票が挙げた、既存projectの権限と2FAの確認、
  Trusted Publisherの登録、GitHub environment `pypi`の保護。coordinatorは照合していない）
- 移管の判断（human owner 2026-10-05）: 共通TypeScript tooling monorepo、Bridgeは今の機能のまま移す、fixtureは固定Git commit、
  WireScopeは固定digestの生成物で取り込む（`2026-10-05-01`）。移管先は`minecraft-remote-protocol`を`minecraft-remote-tooling`へ
  名前を変えて使う（`2026-10-05-02`、McRemote確定搬送票）。「同じ」の判定は次のとおりにする
  - fixture 12件はbyte一致。契約2件のcaseを足したfixtureは別のidentityとして記録する
  - 配布物は中身を比べる。source URLやcommitを書き込むdetached manifestとOCIのmetadataは、移管で必ずdigestが変わるので
    一致の対象から外し、ZIPの中のassetのbytesを比べる
  - 移管だけの差分と機能の差分を分ける。b9の列幅と知らないevent typeの修正はWireScopeのbytesを変えるので、移管前の同じ
    機能版を基準に比べる
- 着手の返却（2026-10-05）:
  - McRemote（knowledge `900f6f4`）: 着手項目1〜7を完了。candidate `feat/b9-contract-packaging@5cb33ebad4bf2c5e36c3433b0f70fe6070915b00`、
    `mc-remote-1.21.11-2320.0.0b9.jar` 261,016 bytes／SHA-256 `4feb90dbdba8550cd16800cc3d384e42fed16a5c5e20faa489a0381ad2cda58e`。
    commitは`b6a974a`（`chat.post`の`null`、JARの権限bit、version）→`33fb693`（README）→`344dc2b`（契約2件のfixtureの取り込み。
    移管を外すときのsource）→`5cb33eb`（fixtureの取得元を`minecraft-remote-tooling`へ）。281 tests PASS（umask 002と022のそれぞれ）。
    手元の002／022とCIのJARで、全148 entryのmode、bytes、順序とJAR全体のSHA-256が一致した（担当報告）。共有fixture 4件は
    公開b8とbyte一致
    - coordinatorの照合: remote branchの先頭が`5cb33eb`。CI run `37220994120`はこのcommitでsuccess、artifact
      `mc-remote-candidate`のJARは261,016 bytes／`4feb90db…a58e`、`source-commit.txt`は`5cb33eb`。追加のshared fixture
      `chat-event-compat-v23.2.json`（32,382 bytes／SHA-256 `670b0a86df1956c0e44c6986a0a2598caab32c7328804f9c703190e62e9dd727`、33 case）は、
      Scratchの発行元`scratch-editor@62e46fd`と移管先`minecraft-remote-tooling@98e4208`の`packages/protocol/test/fixtures/`でbytesと
      SHA-256が一致。`Naohiro2g/minecraft-remote-protocol`は`minecraft-remote-tooling`へ名前が変わっている
  - Python（knowledge `900f6f4`）: candidate `codex/b9-python-contracts-pypi@b901c88fe41b67530ff353271683ece9fd453076`。commitは
    `2f943ff`（契約2件、PyPI.org用のjob、version）→`10c0cc5`（追加fixtureの取り込みとpollのcounterの逆行検査。移管を外すときの
    source）→`fc1935b`（fixtureと同梱WireScopeの取得元を`minecraft-remote-tooling`へ）→`b901c88`（更新・戻し方の案内、starter、
    API一覧の説明）。780 tests PASS、CI（Python 3.10〜3.13）success。共有fixture 7件は公開b8とScratch `62e46fd`にbyte一致。
    同梱WireScopeは`minecraft-remote-tooling@dc1ab83`の`packages/live`から（ZIP 83,854 bytes／`da3da0b6…31ad`）。移管直前の
    Scratch `c7505c8`から作ったZIPとbyte一致（manifestはsource metadataが変わるので比較から除いた）。CI成果物はwheel 196,221 bytes／
    `e166bc9c14c425b3859f9af6c7af52900b58d1769fc077a3524a5368d05638c6`、sdist 190,627 bytes／
    `bd027b8b94ff775bfb7a3c02ada9716ad8785e5499180bb0cfb26f1da4afe479`。PyPI.orgへの公開は`PYPI_PUBLISH_ENABLED`が未設定で、
    まだ動かない。TestPyPIはb9では今までどおり自動で予行し、初回のPyPI公開の後に手動へ絞る案
    - coordinatorの照合: remote branchの先頭が`b901c88`、CI run `37233244696`はこのcommitでsuccess。artifactのwheel、sdist、
      `manifest.json`のSHA-256が上と一致し、manifestの`source_commit`は`b901c88`、`bundled_wirescope_source_commit`は`dc1ab83`。
      GitHub environment `pypi`は`protection_rules`が空、`deployment_branch_policy`が`null`（human ownerが報告した保護設定と
      合わない）
    - 注意: McRemoteは`minecraft-remote-tooling@98e4208`、Pythonは`@dc1ab83`を取得元に記録している。fixtureのbytesは同じ。
      凍結では、Scratchの返すtoolingのcommitに揃える
  - Scratch（knowledge `900f6f4`）: 着手項目1〜6を完了。Scratch `develop@7fbbf034488760d8fc7e034bf23f3e08e6e1807d`、
    `minecraft-remote-tooling` `main@dc1ab834183e29f2eb03059b07e99d2b463776ee`。Scratchのcommitは`62e46fd`（契約2件、`ChatPostResult`、
    追加fixtureの発行）→`c7505c8`（WireScopeの列幅）→`688b1b1`（client identityをb9へ）→`ea796dc`（GUIの観測の契約追従）→
    `3e5ac5f`（consumerへの切り替え、旧ownerの撤去、`mc-remote/tooling-lock.json`、CI、collector）→`7fbbf03`（GUI unitのmock指定の
    修正、製品codeは不変）。toolingはProtocol 39／Bridge 30／WireScope 144 tests PASS、ScratchはCI（unit 530、integration 127、
    Playwright 8）success。移管前のScratch `c7505c8`と移管後のtoolingで、runtime、fixture、index HTMLの44 fileとWireScope ZIP内の
    6 assetがbyte一致（担当報告）。candidate: tooling run `37220882228`（WireScope ZIP 83,854 bytes／`da3da0b6…31ad`、manifest
    2,339 bytes／`c654f7d1…10d7`、Bridge OCI index `sha256:5828304c9bb1d60df8672f9189f503790050e09358bd375f39e4d59d190eb84f`、
    linux/amd64とarm64）、Scratch run `37232396741`（`scratch-gui.tar.gz` 138,376,671 bytes／`c0d08c26…c75d`、Scratch OCI index
    `sha256:6702b112ad53b48efa2bf99fc0145fc7b23d24a1d20743018582f781f61c9e34`、`contracts.tar.gz`は公開b8と同じ1,908 bytes／
    `48948ba4…2390`）。OCIのregistryへはまだ出していない。pickerのalias検索は非blockerのまま（登録する語をhuman ownerが選ぶ）
    - coordinatorの照合: Scratch developの先頭が`7fbbf03`、toolingのmainの先頭が`dc1ab83`。3つのrun（tooling `37220882228`、
      Scratch CI `37232360354`、candidate `37232396741`）はそれぞれのcommitでsuccess。toolingの`dc1ab83`で、b8時点のfixture 12件
      （`packages/`配下）がb8 closeの一覧とbytesとSHA-256で全件一致（acceptance 1）。Scratchの`7fbbf03`の`mc-remote/`には
      `README.md`、`block-reference`、`tooling-lock.json`だけが残り、旧ownerのsourceは無い。McRemoteが記録した`98e4208`から
      `dc1ab83`の差分は`.dockerignore`の1 fileだけで、fixtureは同じ（McRemoteの取得元の記録はそのままでよい）
    - API freeze（acceptance 5）: b8 closeの`2a8c3ea`から、wireの文書は変わっていない（最後の変更は10/3の契約2件の`46033d8`）。
      `tools/build-api-reference.py --check`はOK（32 method、35 reason）
- **exact set凍結（`b9-integrated-artifact-set-1`、human owner承認 2026-10-05）**: protocol `23.2.0`／artifact `2320.0.0b9`
  - McRemote: source `5cb33ebad4bf2c5e36c3433b0f70fe6070915b00`、`mc-remote-1.21.11-2320.0.0b9.jar` 261,016 bytes／
    `4feb90dbdba8550cd16800cc3d384e42fed16a5c5e20faa489a0381ad2cda58e`（CI run `37220994120`）
  - Python: source `b901c88fe41b67530ff353271683ece9fd453076`、wheel 196,221 bytes／`e166bc9c…38c6`、sdist 190,627 bytes／
    `bd027b8b94ff775bfb7a3c02ada9716ad8785e5499180bb0cfb26f1da4afe479`（CI run `37233244696`）
  - Scratch: source `7fbbf034488760d8fc7e034bf23f3e08e6e1807d`、Scratch OCI `sha256:6702b112…9e34`、`scratch-gui.tar.gz`
    `c0d08c26…c75d`、`contracts.tar.gz` `48948ba4…2390`（run `37232396741`）
  - minecraft-remote-tooling: source `dc1ab834183e29f2eb03059b07e99d2b463776ee`、WireScope ZIP 83,854 bytes／`da3da0b6…31ad`、
    manifest 2,339 bytes／`c654f7d1…10d7`、Bridge OCI `sha256:5828304c…b84f`（run `37220882228`）
  - shared fixture: b8時点の12件（不変）と`chat-event-compat-v23.2.json` 32,382 bytes／`670b0a86…d727`（33 case）
  - 実施票: `00-hub/b9-gate-live-test-sheet_ja.md`
- PyPI.orgへの公開の設定（human owner 2026-10-05）: GitHub environment `pypi`に承認者（Required reviewer、Prevent self-reviewはOFF）
  とtagの制限、repositoryの変数`PYPI_PUBLISH_ENABLED`は`false`。coordinatorがGitHub APIで照合した（承認者`Naohiro2g`、
  `prevent_self_review: false`、deployment policyはtag `v*`、変数は`false`）。b9の公開の前に`true`にする。TestPyPIの予行は
  b9では自動のまま、以降は手動のときだけにする（Pythonの案を採用）
- 実機試験（2026-10-05、`14-evidence/records/2026-10-05-b9-dev-live_ja.md`）: segment 0〜3がすべてPASS
  - segment 0: b9のJARへ一件だけ差し替え、b8とb9のScratchから保存tokenのまま再pairingなしで`hello`が通った（human owner）
  - segment 1: live-autoのPASS行60、FAIL行0。id付き`chat.post`の応答が`result: null`
  - segment 2: Pythonの代表往復と同梱WireScopeの22 frames。Pythonのb8の保存tokenは`token_expired`で、新しくpairingして行った
  - segment 3: 移管したBridgeでのpairing、代表ブロック、独立ChromiumのWireScopeで22 frames、列幅をhuman ownerが確認
  - 未検証の境界: Bridgeは、Docker daemonが無いため凍結OCIの中のcodeをhost-nativeのNodeで動かした。containerとしての起動は
    確かめていない
- **判定: GREEN**（human owner 2026-10-05）。Bridge OCIのcontainerとしての起動は、ケータリング方式のVPSベータへのdeployで
  human ownerが確かめる。起動しなければOCIのpackagingだけを直し、他のPASSは再利用する（release運用と責務分担 §7）
- release authorization: プロジェクトオーナーの明示承認（2026-10-05）。4 repoともGitHub prerelease ON、draft OFF、Latest非対象。
  `minecraft-remote-tooling`も`v2320.0.0b9`で自分のReleaseを出す（human owner 2026-10-05。b9の公開setに入るためで、同じrepoに
  あることを理由にversionを揃えるのではない、`2026-10-05-01`）。公開の指示は次のとおり
  - 順番: toolingを先に出す。Scratchの公開物（WireScope、Bridge）はtoolingの生成物を集めるため
  - minecraft-remote-tooling（Scratch担当）: tag `v2320.0.0b9`を凍結した`dc1ab83`へ打ち、WireScope ZIP（`da3da0b6…31ad`）と
    detached manifest（`c654f7d1…10d7`）を添付し、Bridge OCI（index `sha256:5828304c…b84f`）の置き場所とdigestをRelease notesか
    manifestに記録する。registryへ出すBridge OCIのindex digestは凍結値と同じにする
  - Scratch: tag `v2320.0.0b9`を凍結した`7fbbf03`へ打つ（developの先頭と同じ）。固定workflowが添付するWireScope、Bridge、
    Scratch OCI、contractsが凍結値と一致すること
  - McRemote: `feat/b9-contract-packaging`（`5cb33eb`）をmainへ統合し、tag `v1.21.11-2320.0.0b9`。tagのCIが作るJARが`4feb90db…a58e`と
    一致してから公開する（b9で権限bitを固定したので一致するはず）
  - Python: mainを`b901c88`へfast-forwardし、tag `v2320.0.0b9`。CI成果物がwheel `e166bc9c…38c6`／sdist `bd027b8b94ff775bfb7a3c02ada9716ad8785e5499180bb0cfb26f1da4afe479`と一致してから
    公開する。tagを打つ前に、human ownerが変数`PYPI_PUBLISH_ENABLED`を`true`にする。PyPI.orgへのjobはhuman ownerの承認を待つ。
    TestPyPIへも固定triggerで出す
  - 一致しないもの（tagのCIのJAR、wheel、OCIのdigest等）が出たら、公開せずに止めてcoordinatorへ返す
  - 公開後、coordinatorがtag target、prerelease／draft、assetと`manifest.json`のidentity、PyPI.orgの版をGitHub APIとPyPIで読むだけ照合する
  - sdistのdigestの誤記（2026-10-05）: Pythonが公開前の照合で止めた。凍結setとこの指示に書いたsdistの略記`bd027b8b…e179`は
    coordinatorの書き誤りで、正しくは`bd027b8b…e479`（全桁`bd027b8b94ff775bfb7a3c02ada9716ad8785e5499180bb0cfb26f1da4afe479`、
    Pythonの返却とcoordinatorの照合の値）。上の2箇所を全桁へ直した。凍結したartifactは変わらない
  - Scratch OCIのversionラベル（2026-10-05）: Scratch担当が公開前の照合で止めた。candidateのworkflowはOCIの
    `org.opencontainers.image.version`に`2320.0.0b9`を、公開workflowはtag名から`v2320.0.0b9`を入れるので、amd64とarm64の
    configが変わり、凍結したScratch OCI（`sha256:6702b112…9e34`）と同じdigestにならない。toolingとScratchのtag、Release、registryは
    未操作。human ownerの判断で、**公開workflowでbuildし直し、ラベルの違いはpackagingの差として受け入れる**（release運用と責務分担
    §7。b8のMcRemote JARの権限bitと同じ扱い）。条件: 公開する前にScratch担当が新しいOCIと凍結したOCIを比べ、amd64とarm64の
    layerのdigestがすべて同じで、configの違いがversionラベルと生成のmetadata（作成時刻など）だけであることを確かめる。layerが
    違えば止めて返す。実機試験のPASSは再利用する。公開するScratch OCIのdigestは、照合の後に記録する
  - toolingの公開（2026-10-05、coordinatorがGitHub APIで照合）: [v2320.0.0b9](https://github.com/Naohiro2g/minecraft-remote-tooling/releases/tag/v2320.0.0b9)、
    title「mc-remote tooling 2320.0.0b9」、prerelease=true、draft=false、Latestなし。annotated tagのtarget `dc1ab834183e29f2eb03059b07e99d2b463776ee`。
    asset: `wirescope-app.zip` 83,854 bytes／`da3da0b6…31ad`、`wirescope-app.manifest.json` 2,339 bytes／`c654f7d1…10d7`、`bridge.oci.tar`
    114,628,096 bytes／`b6a6feec…b100`（OCI index `sha256:5828304c…b84f`。registryへはまだ出していない）
  - McRemoteの公開（2026-10-05、coordinatorがGitHub APIで照合）: [v1.21.11-2320.0.0b9](https://github.com/Naohiro2g/McRemote/releases/tag/v1.21.11-2320.0.0b9)、
    title「McRemote 1.21.11 / 2320.0.0b9」、prerelease=true、draft=false。annotated tagのtarget `5cb33ebad4bf2c5e36c3433b0f70fe6070915b00`で、
    mainの先頭と一致。asset: `mc-remote-1.21.11-2320.0.0b9.jar` 261,016 bytes／`4feb90db…a58e`（凍結したJARと同じ。b9で権限bitを
    固定したので、b8のような食い違いは出なかった）、`manifest.json` 387 bytes／`1b18e60c…0fd6`（`release_tag` `v1.21.11-2320.0.0b9`、
    `source_commit` `5cb33eb`、role `jar`のdigestが一致）。Latestは`v1.21.8-1.4.0`のまま
  - Pythonの公開（2026-10-05、coordinatorがGitHub APIとPyPIで照合）: [v2320.0.0b9](https://github.com/Naohiro2g/minecraft-remote-api/releases/tag/v2320.0.0b9)、
    title「minecraft-remote-api 2320.0.0b9」、prerelease=true、draft=false。tag（lightweight）のtarget `b901c88fe41b67530ff353271683ece9fd453076`。
    mainはその1つ先の`39f2ec9`（公開後の文書だけ: README、PUBLISHING、`docs/pypi-publication_ja.md`ほか）。asset: wheel 196,221 bytes／
    `e166bc9c…38c6`、sdist 190,627 bytes／`bd027b8b…e479`、`manifest.json` 681 bytes／`da9887d1…e838`（`source_commit` `b901c88`、
    `bundled_wirescope_source_commit` `dc1ab83`）。**PyPI.org**: [2320.0.0b9](https://pypi.org/project/minecraft-remote-api/2320.0.0b9/)の
    wheelとsdistのSHA-256がReleaseと一致し、yankなし。無指定の取得は`1214.10.13`のまま（versioning-design §10.4）。TestPyPIの
    2320.0.0b9も同じdigest。新しいuv環境での`uv add "minecraft-remote-api==2320.0.0b9"`とimportの成功は担当報告。Latestは
    `v1214.10.11`のまま。**b9で初めてPyPI.orgへpre-releaseを出した**（`2026-10-05-03`）
  - Scratch OCIのCOPY layer（2026-10-05）: Scratch担当が公開前のbuild（run `37266780367`、index `sha256:da7c9622…ff27`）を凍結した
    OCIと比べ（run `37267805360`）、止めた。amd64とarm64とも先頭9 layerは同じで、最後のGUIのCOPY layerだけdigestが違う。
    その1,746 entryのpath、中身のSHA、size、type、link先、mode、uid／gidはすべて同じで、違いは1,743 entryのmtimeだけ。GUI tarは
    凍結値とbytesもSHA-256も同じ。human ownerの判断で、**このmtimeの差もpackagingとして受け入れる**。判定の条件を次へ改める:
    各layerの中身（path、内容、size、type、link先、mode、所有者）が凍結したOCIと一致し、違いはmtimeとconfigの生成metadata
    （versionラベル、作成時刻、それに伴う履歴とdiff_id）だけであること。固定workflowで公開し、公開したOCIにも同じ照合をして
    返す。合わなければ公開を取り消せる状態で止めて返す。実機試験のPASSは再利用する
  - Scratchの公開（2026-10-05、coordinatorがGitHub APIとGHCRで照合）: [v2320.0.0b9](https://github.com/Naohiro2g/scratch-editor/releases/tag/v2320.0.0b9)、
    title「mc-remote Scratch 2320.0.0b9」、prerelease=true、draft=false、Latestなし。annotated tagのtarget `7fbbf034488760d8fc7e034bf23f3e08e6e1807d`
    で、developの先頭と一致。固定workflow（run `37270517123`、release event、head `7fbbf03`）がsuccess。asset: `wirescope-app.zip`
    `da3da0b6…31ad`、`wirescope-app.manifest.json` `c654f7d1…10d7`、`contracts.tar.gz` `48948ba4…2390`（いずれも凍結値）、`manifest.json`
    1,168 bytes／`cbc6af55…20da`。manifestのOCIは`scratch` `ghcr.io/naohiro2g/mc-remote-scratch@sha256:f44e7a6c1a3b041aba787eba5e052a3ae78ce4ce733732bc7213207a3b17f607`、
    `bridge` `ghcr.io/naohiro2g/mc-remote-bridge@sha256:5828304c…b84f`（凍結値）で、どちらのdigestもGHCRにある。公開したScratch OCIを
    凍結したOCIと比べた結果（run `37271363905`、success）は、amd64とarm64とも先頭9 layerが同じで、最後のCOPY layerは1,746 entryの
    中身と属性が一致し、違いは1,743 entryのmtimeだけ。configの違いは許した生成metadataだけ（担当報告）。公開したScratch OCIの
    digestは`f44e7a6c…f607`（試験した`6702b112…9e34`と中身は同じ）
- gate result（公開）: **4 repoのGitHub prereleaseとPyPI.orgの公開identityを確認した（2026-10-05）**。残りはgateのclose（各repoの
  `handoff-materials`の分類、parkの見直し、default branchへの統合の確認）
- handoff-materialsの分類（2026-10-05、knowledge `099c40b`の依頼）: 3担当が返した①を`14-evidence/artifacts/`へ収容した（記録
  `14-evidence/records/2026-10-05-b9-release_ja.md`。Scratchの151 fileは搬送元の一覧と照合して不一致0、4つのlogのpathを`~`へ置換、
  McRemoteのJARの複製2つは収容していない）。収容済みだった素材は、3担当とも全文とSHA-256が一致したと返した
  - McRemote: ①は公開の照合とclose票。②はcandidateの比較（rc1でJARの再現性を確かめた後に捨てる）。③は5件（b8のJARの権限bitの
    比較を含む。b9で固定したので用が済んだ）
  - Python: ①は公開の照合（PyPI.orgへの初公開）とclose票。②は`b9-python-work`（TestPyPIを手動へ絞る後続作業）と`b9-python-tooling`
    （次の入力更新の比較基準）。③は4件
  - Scratch: ①は移管、公開、b8から残していたもののうち用が済んだもの、b9の画面PNG。②は手元の配信のruntimeとprivate（b9とb8の
    戻し先）、Stackへの回答2件（`home-scratch-contract-reply`、`stack-wss-reply`。Stackの受領待ち）、b8のlive-humanのprivateな原画像
    （backstageへ移す対象）。③は54 file
  - human ownerの判断が要る②: Stackへの回答2件の受け取り（Stackはhuman ownerの直接管理）、privateな原画像のbackstageへの移管、
    手元の配信の終了。いずれもgateのcloseを止めない
  - Scratch②の追跡（2026-10-06、Scratch担当の追跡更新票、収容先`14-evidence/artifacts/2026-10-05-b9-release/scratch/close-followup/`）:
    Stackの受領待ちと原画像のbackstage移管待ちは解消した。Stackは回答2件の6 fileを全文とSHA-256で照合して受け取った（Scratchの元の
    pathから収容先への対応は`materials/stack-received-inventory.json`）。backstageは28件を棚卸しし、必要な17件（原画像10件、起動関連
    7件）を暗号化コピーで受け取った（管理名`scratch-private-intake-20261006`、担当報告。knowledgeは中身を見ていない）。Scratchは
    knowledgeへ収容済みの180件を照合してから元を整理した（232 file）。残る②は手元の配信のruntimeとprivate（b9、b8の戻し先、旧配信）と
    この追跡票で、ownerの終了判断と参照の終了を待つ
- default branchへの統合（2026-10-05、coordinatorが照合）: McRemote main `5cb33eb`、Python mainは`b901c88`の1つ先の`39f2ec9`（公開後の
  文書だけ）、Scratch develop `7fbbf03`、minecraft-remote-tooling main `dc1ab83`。それぞれ公開tagを含む
- gateを閉じるときのpark確認（`2026-09-30-09`、2026-10-06、human owner同意）: 契約2件と`2026-08-23-01`のrelease gate方法論の
  残り（gate manifestは作らない）を閉じた。API一覧はb9へ更新し、クライアントAPI一覧とのつなぎ方をrc1へ。README／sampleの
  Pass C、pickerのalias検索と読み上げはrc1へ、Scratch block value投影の残りは初回stable後へ回した。b9のgate中に起こした
  park（Scratch OCIを凍結と公開で揃える、製品noticeを一つに絞る）はrc1 gateを開くときに再開する
- close（2026-10-06、human ownerの判断）: **b9 gateをCLOSEDとする**。ホームページ（releases、roadmap、履歴、Pythonの導入を
  PyPIの版指定へ）、API一覧、knowledgeのREADME、grand-design roadmapをb9へ更新した。Stack／Backstage（b9のVPSベータへの
  deployとBridge OCIのcontainerとしての起動の確認を含む）はhuman ownerが扱う

- human owner（2026-10-05）: `minecraft-remote-tooling`の名前変更とpark解除はScratchに頼む。Pythonをmatureへ移す（`2026-10-05-03`。
  b9からPyPI.orgへpre-release）
- human owner（2026-10-04）: WindowsでのPythonの導入手順の確認とPyPI.orgの準備は、今日中を目標にする。契約2件のcaseを
  足したshared fixtureは、今のownerのScratchが先に出す（移管より前）

## 2026-09-30 b8横断release gate（CLOSED）

- gate coordinator: knowledge担当session（Claude Code）。人間による明示handoffなしに他担当へ移さない
- human release owner: プロジェクトオーナー
- current phase: **横断接続の前**。McRemote、Python、Scratchの実装は人間確認の直前まで進んでいる（human owner申告、
  2026-09-30）。McRemoteからはサウンドの照会への回答でcandidate `feat/b8-entity-lifecycle-particle@b3b3ba8`（PR #12、
  未merge、271件PASS）を受け取った（担当報告、coordinator未照合）。Python、Scratchのidentityはまだ受け取っていない。
  次は確認票でidentityを受け取り、Tier 2の横断接続 → exact setの凍結 → live-humanへ進む
- 目標日: 2026-10-03 release（`2026-09-29-02`）
- release mode: 軽量mode（release運用と責務分担 §14、`2026-08-28-02`）。McRemoteの変更範囲に認証の既定値と
  credentialの自動初期化（`2026-09-03-01`、`2026-09-25-01`）が入るため、その部分は§14の但し書きにより検証を強める
- contract: protocol `23.2.0`／artifact `2320.0.0b8`（foldは`2026-09-23-03`）。wire §5.0.2、§5.8.3、method表、error表
  - B8 API: `2026-09-23-01`／`2026-09-30-01`／`2026-09-30-02`（サウンド）
  - resource IDの補い方: `2026-09-30-06`
  - 初回stableまでのAPI範囲とb9: `2026-09-30-03`
  - Java: `2026-09-30-04`
  - pickerの名前データ: `2026-09-30-10`
  - gate開閉時のpark確認: `2026-09-30-09`
  - MC target（b8は1.21.11だけ、26.xは26.3を対象）: `2026-09-30-07`
  - McRemoteの是正: `2026-09-03-01`／`2026-09-03-02`／`2026-09-25-01`
  - Python surface: `2026-09-28-01`（`from mc_remote import Minecraft`）／`2026-09-28-02`（`pygame-ce`をoptional extraへ）
  - live試験のMC版照合: `2026-09-28-03`
  - 日程とWindows検証: `2026-09-29-02`
  - shared fixtureのownerはScratchのまま（`2026-09-13-02`）
- knowledge contract commit: `2d0830a741997573248ee94e945c719316a0c299`（`2026-09-30-02`〜`-10`を着地したcommit）。
  gateの節と確認票依頼は`16668c5e5152d593c4b184939c9a9e723529d6e9`で加えた（wireとDECISIONSは同一）。確認票依頼に
  `2d0830a`とだけ書いたのはcoordinatorの誤りで、Pythonは参照先にgateの節が無いと返した。依頼を訂正した
- 基準set: b7.post2（McRemote `v1.21.11-2301.0.0b7.post2`、Scratch `v2301.0.0b7.post2`）＋Python `2301.0.0b7.post3`
- 参加component:
  - McRemote: entity lifecycle四method、Particle Stage 2、サウンド2 method、resource IDの無印の受け入れ、b8必須是正
    （auth三点、意味別config、READMEの設定解説）、credentialの自動初期化。MC targetは1.21.11だけ
  - Python client: B8のPython surface（entity lifecycle、ParticleSpec、サウンド）、短いimport、`pygame` extra、
    3D graphの小さいsample、同梱WireScopeの23.2.0対応
  - Scratch editor（Bridge・WireScope同梱）: B8共有fixtureの発行（サウンドとresource IDのcaseを含む）、
    `@mc-remote/protocol` 23.2.0のmirror、WireScopeのvalidator／method認識／sanitizer。learner block（カタログの
    ID一覧をリストへ入れるブロックを含む）は非blocker
  - 不参加: Java（`2026-09-30-04`により、b8にもb9にも含めず、公開releaseへ後から追従する）。Stackはdeploymentの
    準備で関わり、component releaseはしない
- 変更範囲（change cone）:
  - wire（6 methodの追加、`world.spawnParticle`のobject形、新reason `particle_data_unsupported`／`unknown_sound`／
    `no_block`）→ plugin codec、Python adapter、WireScope validator、共有fixture、代表往復
  - resource IDの無印の受け入れ（particle、entityは拒否から受け入れへ、soundは新規。`2026-09-30-06`）→ plugin、
    Python／Scratchの送り方、WireScope validatorの表示、共有fixtureのcase
  - 認証の既定値／credentialの自動初期化／configの再編 → fresh installでauth ON、両方欠落・片方欠落の自動初期化、
    b7.post2のcredential domainからのupgradeでsession tokenが続くこと、旧`b5.`／`b7.`キーの起動時の移行（新キーへ移して旧キーを消す。`2026-10-01-01`）
  - Pythonのpackaging（extra、短いimport）→ 再現性、metadata、依存解決、importと読み直しの挙動
- required tier: 横断接続まではTier 2。exact set凍結後にTier 3（変更範囲内の短いlive-auto、人間でしか判定できない
  箇所だけlive-human）
- acceptance:
  1. B8共有fixtureをMcRemote／Python／WireScopeが同じbytesで使う
  2. resource IDのfixture caseが、無印を拒否していた旧McRemote（公開済みb7のJAR）では意図どおり落ち、b8 candidateでは
     通ることを一度確かめる
  3. receiverが対象のplayerだけへ届く2-player確認（particleとサウンドを同じ回で見る）
  4. dust／blockの描画
  5. サウンド: 実際に聞こえる、定位と距離による減衰、`self`は本人にだけ聞こえる
  6. Python 3D graphの小さいsample
  7. 1.21.11での代表往復。live試験の開始時にhelloの`mc_version`を照合し、違えば本体を実行せずFAIL
  8. Windowsでの導入手順の検証（human ownerが行う）: 関心は、いちばんハードルの低い入口ルート（クリーンインストールのWindows 11から、
     Gitなしでuvだけ、Release wheelのURL、Jupyterまで）で通るか。通らなければ正準の通常ルート（Git for Windows）へ進む
  9. McRemoteの認証／credentialの強化分（上の変更範囲）
- 再利用するPASS: b7のdirection／lightning／particle Stage 1のlive PASSは、B8で意味を変えない範囲で再利用する。
  McRemoteのJARは変わるので、代表往復だけ取り直す。Python post3のsoak gate ①〜③と④（Windowsを除く）は再利用する
- 移管の準備（`2026-09-30-03`）: b8 release時点でScratchが持つprotocol packageと全共有fixtureの一覧（file、bytes、
  SHA-256、case数、protocol version）をこの欄に記録し、b9の移管の起点とrollback先にする。各consumerの取り込み方は
  確認票で返してもらう。b8の間はrepositoryの操作、sourceの移動、owner・配布の変更をしない（`2026-09-13-02`）
- 持ち越し: b7.post2欄の未検証の境界（WireScopeの横断real-browser E2E、home alpha、Stack後続gateの再判定）は、
  b8で扱うか再開条件を置くかをgate中に決める。NOTES `[priority]` b7 release後の是正候補3件（Scratch／WireScope）も、
  Scratchの確認票で状態を聞いてから扱いを決める
- exact compatibility set / freeze status: **凍結**（2026-10-03、`b8-integrated-artifact-set-1`。下の「exact setの凍結」）。source／artifact identityが
  一つでも変われば失効する
- devの接続先: 各担当は「devの通常環境」で通じる（human owner 2026-10-03）。coordinatorは接続先を票に書かない
- target deployment: 論理deployment `dev-integration`（1.21.11、ホームサーバー`home-host-2`、host-native）の通常環境で行う
  （human owner 2026-09-30）。2026-09-30時点では公開済みb7（`mc-remote-1.21.11-2301.0.0b7.jar`）が稼働している（human ownerの
  console log）。Stackの配置経路が無いので、Stack担当が一回限りの許可で読むだけの事前確認をし、exact setの凍結後に別の
  指示でJARを一件だけ差し替える。作り直しはb8の後
- gate manifest identity: 未成立。公開後は各repoのrelease `manifest.json`をread-onlyで照合する
- gateを開くときのpark確認（`2026-09-30-09`）: `tools/list-reopen-conditions.py --release-tied`の16行を見た。b8に関わる
  行（ピッカーの多言語metadata、browser検証能力、b7公開後のScratch 3件、WireScopeのpublic deploy後続、Stackの
  2026-07-23の行、Windowsの導入2ルート）は、確認票の質問と統一実施票へ入れた。iPad（Carnets）はb8の公開後に扱う
- 確認票の返却（2026-09-30。担当報告、coordinatorは実装の正しさを判定しない）:
  - McRemote: candidate `feat/b8-entity-lifecycle-particle@b3b3ba805fbf8413e22407c087b6abe4f201707b`（PR #12、未merge。
    coordinatorがGitHub APIでbranchの先頭と一致を確認）。JAR `mc-remote-1.21.11-2320.0.0b8.jar` 261,025 bytes／SHA-256
    `7ab24fa1ff6c20513e46cbf3629f1f4860365acbf3a7e191e48a4e75af1677fb`（担当が2回のclean buildで一致を確認）。unit 271件PASS。
    live-autoはローカルPaper 1.21.11で`f48a18e`（53行）と`5c4d558`（60行、サウンド含む）がPASS、`b3b3ba8`は未実施。
    b8必須是正（`4d39362`／`6f8d69d`）とcredentialの自動初期化（`e60b194`）は祖先にある。B8共有fixtureは
    `entity-particle-v23.2.json`（Scratch `0735a9c957d069f719bee9c91e8be0f9322f4920`、20,967 bytes、SHA-256
    `09c1565bf81d33c92d6282e6e20d926559168cb9d780c07d30ad2f9f5895640e`、59 case）を使用。サウンドとresource IDのcaseは未受領。
    未検証: fresh installでの認証ON既定、b7.post2からのupgradeで実tokenが続くこと、live-human
  - McRemoteの着手依頼5（2026-10-01）: 正式段階の固定trigger（`.github/workflows/release.yml`、`release: published`）と、tagからtitle・JAR名・
    pre-releaseを導出する`scripts/release_identity.py`を`main@d17712fc3caedb5e8f2ce12d4f31f0d49bc0989d`（PR #13）へ入れた。公開済み
    `v1.21.11-2301.0.0b7.post2`でのdry run（Actions run `36856681548`）がsuccessで、導出したtitleとpre-releaseは今のReleaseと一致し、
    Releaseは変えていない（coordinatorがGitHub APIでmainの先頭とrunの結果を確認）。b8のtagは、PR #12と#13の両方がmainに入った
    状態で打ち、tagのCIが成功してからReleaseを公開する
  - McRemoteの訂正（2026-10-01に`2026-10-01-01`として着地）: 旧`b5.`／`b7.`キーは、実装（`366f363`）では起動時に値を新キーへ移して旧キーを削除している。
    上の変更範囲の「読み替えと警告」と`2026-09-03-02`の状態欄「起動時にoperatorの`config.yml`を自動で書き換えない」は
    実装と合わない。McRemoteがb8の実装報告の搬送票で訂正を出す。この結果、b8で起動した後にb7.post2のJARへ戻すと、
    運用者が変えていた値が効かなくなる（hub NOTESのpark「rc1のrollbackの範囲」）
  - Python: B8の実装は`codex/b8-python-entity-particle`（HEAD `70596ed5fc96d826d5107f2033354a59cccfc2e6`）の上の未commit差分で、
    candidateは未固定。entity lifecycle四method、ParticleSpec、3D graphのsampleは実装済み。サウンド、短いimport、`pygame` extraは
    未実装。particle／entityの無印IDをclient側で拒否している（`2026-09-30-06`への修正が要る）。同梱WireScopeはScratch
    `5aaa9c5`から作り、サウンドとresource IDには未追従。10/3に間に合うとは確約できない
  - browserの操作: McRemote（Claude Code CLI）、Python（browser skillの初期化に失敗）、Stackは実browserを操作できない。
    Scratchは独立のChromiumでlocalhostの表示、DOM、click／type、screenshotを実測済み（内蔵のBrowserは接続エラー）。
    real-browserのWireScope確認は、Scratch担当と人間で行える
  - Windows: Pythonの担当agentはLinuxで、Windows実機の試験はできない。試験担当は未割当
  - README再編: McRemoteは冒頭から設定解説まで済み、capabilityの一覧（b7／b8の機能）とsmoke testのprotocolの例が残る。
    Pythonはstarter READMEの旧記述、更新・rollbackの導線、Windows、cold-readerの確認が残る
  - Stack（main `68832e0`）: b8のchange coneは無い。公開VPS（official-public-beta）はb7.post2のlock
    `sha256:8de1c89b158727a610a42dbd5222f53c6ce8cbda86f3358068d03e5eb09d1e07`のままで、PR #55〜#60の内部整理の後もdoctorは全項目OK、
    renderは不変。**dev-integration（1.21.11、ホームサーバー`home-host-2`、host-native）はStackの仕組みの外にあり**、host-nativeの
    旧runbookも削除済み。human ownerの判断（2026-09-28）で作り直す予定。このためStackの経路ではb8のcandidateを置けず、置くなら
    人の手作業でJARを差し替えることになる。稼働中deploymentのidentityを示す専用の`status`は無い（`mcrctl plan`はlockの中身と
    SHA-256を出すが、MC版・Paperのbuild・Java版は出さない。`mcrctl doctor`は認証が有効なため`mc_version`を出さない）。
    public側のWireScopeはbetaのVPSで配信済み
  - Scratch（`agent/b8-compatibility@5aaa9c59acc393cd0a0de5cb45a5e619a5e87abe`＋未commit差分）: Protocol 35/35、WireScope 137/137、
    VM 119 subtests／485 assertionsがPASS。B8共有fixtureは`0735a9c`（59 case）で、サウンドのcaseとresource種別ごとの
    無印・完全修飾・非正準形のcaseは未収録。Protocol mirrorとWireScopeは23.2.0のentity lifecycleとtyped particleに対応済みで、
    `world.playSound`／`world.playBlockSound`／`unknown_sound`は未対応。**Scratchからの観測では、B8 entityの4 method、typed particle、
    particleのFAST通知がScratch側のallowlistで落ちる**（再現済み。独立WireScopeの対応だけでは観測が完成しない）。VMは無印の
    resource IDをそのまま送るが、WireScopeのvalidatorはparticle／entityの無印を拒否する（`2026-09-30-06`への修正が要る）。
    カタログID一覧ブロック、entity／particleの9ブロック、pickerの変更は実装済みで未commit。サウンドのlearner blockは未実装
    （非blocker）。pickerは日本語名・英語名・IDの表示とAND検索ができ、公式の言語データから開発時に抽出した最小の辞書を
    GUIの版別JSONへ同梱する（言語ファイル全体は持たない。`2026-09-30-10`どおり）。b7 release後の是正候補3件とpost-b7の
    park 2件は未着手。移管の準備では、Protocolは依存なし、VM／WireScope／BridgeはProtocolをruntime importせず、testが共有
    JSONを相対pathで読む。release manifestの`contracts`はGUIのproduct／runtime config schemaとfixturesで、B8のprotocol
    fixtureは含まない。現時点ではrelease可能と返せない
  - Pythonの追記（同日）: `codex/b8-python-entity-particle@fc6c700b1588a1d052499314f47e8e7e5b06ae27`をpush（coordinatorがGitHub APIで
    branchの先頭と一致、CI run `36718297434`がこのcommitでsuccessを確認）。無印IDの受け入れ、サウンド2 method、observerの追従、
    読み直しに対応した短いimport、`pygame` extraを実装し、ローカル588件PASS、CIはPython 3.10〜3.13とbuildが成功（担当報告）。
    CI成果物は、wheel 192,394 bytes／SHA-256 `8ce5382381091a54c739b78e695b85a52a3b0485ef10dc20671b90c0049510a8`、sdist 185,422 bytes／
    SHA-256 `90242c9922750a0338139cb884823fbe17e1ead0b3c5deb317080cb4c95e64b4`。同梱WireScopeは引き続きScratch `5aaa9c5`から作っており、
    Scratchのsuccessor fixture／WireScopeの取り込みが残る。Windowsの入口手順（Python repoの`docs/windows-b8-entry_ja.md`）を用意済み
  - 全担当の返却がそろった（2026-09-30）
  - McRemoteの追記（2026-10-01、knowledge `10484ae`を読んだ）: candidate `feat/b8-entity-lifecycle-particle@17309919f6340b07abbbe16476ad1d4f762518c0`
    （coordinatorがGitHub APIでbranchの先頭と一致を確認。`b3b3ba8`からの差分は`scripts/live_auto.py`、test、fixtureだけで、plugin本体は不変）。
    JARは`b3b3ba8`と同一の261,025 bytes／`7ab24fa1…77fb`（担当がclean jarで確認）。fixture successor（`054a3af`、36,481 bytes、
    `ca636b4a…39f2`）をbytesのまま取り込み、SHA-256とcase数をtestで固定し、サウンド37件とresource ID 15件のconsumerを追加した。
    `./gradlew test` 273件PASS。**acceptance 2**: ローカルPaper 1.21.11で公開済みb7.post2のJARに一時的に戻し、無印の`flame`が
    `unknown_particle`、`cow`が`unknown_entity`で意図どおり落ち、完全修飾の`minecraft:flame`／`minecraft:cow`は成功した（担当報告）。
    rollbackの注記の裏付けとして、b8が旧キーを移して消した後のconfigでb7は既定値で起動した（この環境では値が既定値と同じで、
    挙動は変わらない）。着手依頼の1と2は、別の追記（`9010c59`時点、JARは同一）で返った。1: ローカルPaper 1.21.11でlive-autoがPASS行61で
    全PASS（無印の`block.bell.use`と`flame`の受理を含む。試験中だけ`auth.enforcement=false`にして戻した）。2: McRemoteの設定を
    置かない新しいserver directoryで、生成された`config.yml`が`auth.enforcement: true`、credentialは両方欠落から自動初期化されて
    `HEALTHY`、token無しの`hello`は`auth_required`で拒否（担当報告）。McRemote側で残る未検証は、b7からのupgradeで実tokenが続くことと
    live-human
  - Scratchの追記（2026-10-01、knowledge `4f0b46f`を読んだ）: candidate `agent/b8-compatibility@dfcb03cf97fed998268b4714feb32d03a209f549`
    （coordinatorがGitHub APIでbranchの先頭と一致、`054a3af`／`a88c540`／`acc9138`が祖先であることを確認）。
    **10/1の確認点のblocker 3点がそろった**。B8共有fixture successorは`054a3af017f1abb8cc01cf85b3bc83181e648e19`の
    `mc-remote/protocol/test/fixtures/entity-particle-v23.2.json`、36,481 bytes、SHA-256
    `ca636b4a2685ea67f24d8e7931e3d30a84e7cec872bb5c5d2eadd178cdac39f2`、111 case（既存59＋サウンド37＋resource ID 15。coordinatorが
    GitHubから取り出してbytesとSHA-256を照合）。同じcommitでProtocol mirror／WireScopeのサウンド対応、validatorの無印受け入れ、
    Scratch側の観測allowlistの修正。learner block（entity／particleの9ブロック、カタログID一覧、pickerの日英名と検索、サウンド2
    command）、post-b7のpark 2件（WireScopeの時刻列とhandshake配置、McRemoteカードの短文化）、root READMEの整理もcandidateに入った。
    test: Protocol 37、Bridge 30、WireScope 142、VM 121 subtests／514 assertions、GUI対象42＋localization 5＋観測20がPASS（担当報告）。
    candidateのローカル成果物（`dfcb03c`から生成、未公開、OCI未発行）: `scratch-image-inputs.tar.gz` 152,986,359 bytes／`e637c7e2…69e2`、
    `bridge-image-inputs.tar.gz` 38,138 bytes／`fd43f714…908f`、`wirescope-app.zip` 83,746 bytes／
    `4cb349894b71d61d7ca143d8362a5b79deb1810e1d7a9e31ad30e29bfe370a07`、`wirescope-app.manifest.json` 2,321 bytes／`65c02083…748f`、
    `contracts.tar.gz` 1,908 bytes／`48948ba4…2390`。b7 release後の是正3件は実装・検証済みだが未commitで、candidateに含まない。human ownerの判断（2026-10-01）でb8に入れる。Scratchがcommitしてcandidateを更新する（Pythonの同梱WireScopeはその新しいsourceから作る）
  - Scratchの更新（2026-10-01、knowledge `893cbfd`を読んだ）: candidate `agent/b8-compatibility@df34849d2502a498a06c5fe07a91d03e925124eb`
    （coordinatorがGitHub APIでbranchの先頭と一致を確認。`dfcb03c`からの3 commitの差分はScratch GUIとVMだけで、Protocol、WireScope、
    Bridgeは不変）。是正3件は`76f9e7d`（空pollの履歴保持）、`b407ca9`（backpressureの案内分離）、`df34849`（入力欄の編集ショートカット）。
    VM 123 subtests／524 assertions、GUI対象41 tests、WireScope 142 testsがPASS（担当報告）。fixtureは`054a3af`のまま。成果物:
    `scratch-image-inputs.tar.gz` 152,885,920 bytes／`2b3eda9a…e458`、`bridge-image-inputs.tar.gz`と`wirescope-app.zip`
    （83,746 bytes／`4cb34989…0a07`）と`contracts.tar.gz`は前のcandidateと同一、`wirescope-app.manifest.json`はsource commitが変わり
    2,321 bytes／`45d56d50…1413`。Pythonは`df34849`から同梱WireScopeを作り直す
- 凍結前の最終返却（2026-10-02。いずれもcoordinatorがGitHub APIでbranchの先頭と一致を確認）:
  - Python: `codex/b8-python-entity-particle@52d35f5304e62f465c1f47ab47c00fe9bcf62470`。CI run `36860299749`がこのcommitでsuccess。
    fixture successor（`054a3af`、111 case）をbytesのまま取り込み、Python全685件PASS（担当報告）。同梱WireScopeは`df34849`から作り直し、
    ZIP 83,746 bytes／`4cb34989…0a07`とmanifest 2,321 bytes／`45d56d50…1413`がScratchの生成物と一致。CI成果物はwheel 195,068 bytes／
    `dcedff010feac0d5df24ff85dd84b321fb819f78563c39431ac32d9d75bc0180`、sdist 188,775 bytes／
    `9d56d92b10936787e1eebc1cf85a521ea19aa2e57b391f474eb695b0ba3fad32`。localhostでの診断で、保存済みtokenは`token_not_found`だったが、
    そのtokenを現在のserverが発行したかは未確認で、b7からの継続の判定には使わない
  - Scratch: `agent/b8-compatibility@691576f60b7f0824e1753bd6823901d01fbe2422`。human ownerが確認したローカル修正4件（pickerの既定値の
    省略、BlockInfoTextの手入力のnamespace補完、workspace zoomの位置ずれ、カード画像と表示名）を加えた。`df34849`からの差分は
    Scratch GUIとVMだけ。fixtureは`054a3af`のまま。成果物: `scratch-image-inputs.tar.gz` 138,375,344 bytes／
    `c7318efdfb22076c2d40501a526d7ca16a121510f7685d875fff34cdc4404843`、`wirescope-app.manifest.json` 2,321 bytes／`6ea468f5…24d0`、
    `wirescope-app.zip`と`bridge-image-inputs.tar.gz`と`contracts.tar.gz`は前のcandidateと同一。局所決定2件はScratchのspokeへ着地
  - Pythonの同梱WireScopeの扱い: `df34849`と`691576f`の間でWireScopeのsourceは変わらず、ZIPはbyte一致で、manifestはsource
    commitだけが違う。このためPythonに作り直しを求めず、`df34849`由来の同梱物のまま凍結に使う（coordinatorの判断。change coneの外）
- **exact setの凍結（`b8-integrated-artifact-set-1`、human owner 2026-10-03承認）**:
  - protocol `23.2.0`／artifact `2320.0.0b8`、Minecraft 1.21.11
  - McRemote `feat/b8-entity-lifecycle-particle@17309919f6340b07abbbe16476ad1d4f762518c0`／JAR `mc-remote-1.21.11-2320.0.0b8.jar` 261,025 bytes／
    `7ab24fa1ff6c20513e46cbf3629f1f4860365acbf3a7e191e48a4e75af1677fb`
  - Python `codex/b8-python-entity-particle@52d35f5304e62f465c1f47ab47c00fe9bcf62470`／wheel `dcedff01…0180`／sdist `9d56d92b…ad32`／
    同梱WireScopeのsource `df34849`
  - Scratch `agent/b8-compatibility@691576f60b7f0824e1753bd6823901d01fbe2422`／上の成果物
  - 共有fixture `scratch-editor@054a3af…`の`entity-particle-v23.2.json` 36,481 bytes／`ca636b4a…39f2`／111 case
  - devの通常環境のidentity（2026-10-03、human ownerがJARを差し替えて記録）: host-native、Minecraft `1.21.11`、Paper `1.21.11-132`、
    Java `21.0.12.1+1`、McRemote JAR `7ab24fa1ff6c20513e46cbf3629f1f4860365acbf3a7e191e48a4e75af1677fb`。認証ON、credential `HEALTHY`、
    標準portの待ち受けを確認。旧b7のJAR、設定、credentialは退避済み
  - 実tokenの継続（統一実施票 0-3）: 未完了。確かめたPythonの保存済みtokenは、差し替え前のb7でも`token_not_found`だったので、
    継続の判定に使えない
  - 実tokenの継続（2026-10-03、Python担当とhuman owner）: **PASS**。devを一時的にb7へ戻してPythonで新しくpairingし（human ownerが
    Minecraftで承認）、保存tokenでb7の`hello`（protocol `23.1.0`）が通った後、b8のJARへ戻して同じtokenで`hello`（protocol `23.2.0`、
    `mc_version` `1.21.11`）が再pairingなしで通った
  - segment 2（Python）の1回目（2026-10-03）: 短いimport、entity lifecycle（無印の`cow`でspawn→nearby→pose get／set→remove）、
    ParticleSpec（dust／blockを`world`／`self`で、無印の`flame`）、`playSound`（無印の`block.bell.use`を`pitch`／`world`、harpを
    `note`／`self`）がPASS。WireScopeのframe 1〜34の表示をhuman ownerが確認した。`playBlockSound`の前の準備で、試験runnerが
    `world.getBlock`の戻り値（`BlockValue`）を辞書として扱った`TypeError`で停止した。serverは`minecraft:air`を正常に返し、clientも
    正常にdecodeしていた（製品の不具合ではない）。Python担当はGit外のrunnerだけを直し、凍結したidentityは変えていない
  - coordinatorの判断: runnerだけの修正なので再凍結しない。1回目のPASSは再利用し、残り（`playBlockSound`、3D graph、`getBlock`の
    WireScope表示）を直したrunnerで同じ凍結identityのまま流す（release運用と責務分担 §7の「harness／runbook／hostのみ」）
  - segment 1（McRemote live-auto、2026-10-03）: **PASS**。PASS行60、FAIL行0、exit code 0。認証ONのまま試験用に一度pairingし（human owner
    承認）、3つの認証済みconnection epochで`protocol` `23.2.0`／`mc_version` `1.21.11`を照合。devのJARが凍結identityと一致することを
    読み取りで確認。試験で作ったcow 257体（容量試験）と試験blockはoriginの近く（overworld、y=72）に残し、原状復元しない（b5と同じ扱い）
  - segment 2（Python）の残り（2026-10-03、run 3）: **PASS**。`getBlock`の取得と仮のstone設置・airへの復元、`playBlockSound`の5つの
    `kind`で既定・`pitch`・`note`とPythonの既定呼び出しの16往復、3D graphのsample 81往復。WireScopeのframe 1〜50と113〜212の表示を
    human ownerが確認。runnerは`15c5c2cf…`を基に残りだけを流す版`c001bd5cbc8ab8b5151133c995dec4f226d82f4b9ac83f786a2e9797574a5c7c`
    （human ownerの選択。Git外のrunnerだけの違いで受け入れる）。凍結identityは不変、再pairingなし。SoundGroupの内部数値、描画、
    聴取、定位、2-playerの差は未検証（segment 4で見る）
  - segment 3（Scratch、2026-10-03、凍結source `691576f`と凍結成果物）: **PASS**（1項目はNOTRUN）。最初の認証済み`hello`で
    `23.2.0`／`1.21.11`を照合、認証ONのまま（pairingはhuman owner承認）。entity lifecycleの各ブロック、particle（無印`flame`、dust、
    block）、サウンド（`playSound`、`playBlockSound`、`N12`→`note`と数字→`pitch`）、カタログID一覧（block 1166／entity 157／particle 115件）、
    pickerの日英名と検索（`gold_block 金ブロック`／`Block of Gold`）と既定値の省略、BlockInfoTextのnamespace補完がPASS。Scratch担当が
    独立のChromiumでWireScope（Scratch source）を開き、entityの4 method、typed particle、サウンド、particleのIDなし通知（送信済み・
    結果未確認）の表示をDOMとscreenshotで確認し、human ownerも4点を目視で承認。b7 release後の是正のうち、空pollで履歴を押し出さない
    ことと数値欄のCtrl+C／Ctrl+VはPASS。server backpressureの案内は、通常の操作でbackpressureが起きず**NOTRUN**（設定変更や負荷で
    無理に起こさなかった）。未確認の範囲として記録し、b8を止める理由にしない（human owner 2026-10-03。是正自体はunit testで確認済み）。試験scriptの誤り2件（TRACE delayの省略、FASTがparticleにも効くという誤ったassertion）はscript側の修正で、
    製品とcandidateは変えていない
  - segment 4（live-human、2026-10-03）: **PASS**（既知の制限1件）。Java版とiPad（Bedrock、Geyser経由）の2 playerで、receiverの`self`／`world`
    （particle、サウンド）、dustの色、block particle、音の定位・減衰・`note`の音階・`playBlockSound`の5 kindを確認。3D graphの描画もPASS
    （効果的なデモにするには工夫が要る、とhuman owner）。iPadではdustの大きさが約1のまま変わらない（Java版では変わる）。b8の対象は
    Java版のserverとclientなので、Bedrockでのdustの大きさは既知の制限として記録する
  - evidence: [`14-evidence/records/2026-10-03-b8-dev-live_ja.md`](../14-evidence/records/2026-10-03-b8-dev-live_ja.md)
  - 凍結後のWireScope列幅の調整: human ownerの希望で時刻列と方向列を詰めた変更が`agent/b8-compatibility@01cdb0bfee3a681697ffa44db5b890045b74b01c`
    にある（`mc-remote/live`の2 fileだけ、142 tests PASS）。新しいWireScope ZIPは83,993 bytes／`7d66aa0d…e579`。凍結set
    `b8-integrated-artifact-set-1`は置き換えていない。b8には入れず、b9で出す（human owner 2026-10-03）
  - release時の注意: McRemoteのtagは、PR #12（candidate）と#13（release workflow）をmainへ入れた後のcommitに打つ。そのcommitの
    CIが作るJARが`7ab24fa1…`と一致するかを、公開前に照合する（plugin本体のsourceは同じで、buildは再現可能と報告されている）
- Stack／backstageの扱い（2026-10-01）: 当面、human ownerが直接コントロールする。coordinatorはStackへ確認票や着手依頼を
  出さない。devの通常環境の事前確認とJARの差し替えはhuman ownerが行い、coordinatorは凍結したexact setと、差し替え後の
  環境のidentity（MC版、Paperのbuild、Java版、JARのSHA-256）の記録だけを受け取る
- blockerと非blocker（human owner 2026-09-30了承）:
  - blocker: Scratchのfixture successor（サウンドのcase、resource種別ごとの無印・完全修飾・非正準形のcase）、Protocol mirror
    とWireScopeのサウンド対応と無印の受け入れ、Scratchからの観測のallowlistの修正。McRemote／Pythonによる取り込み（Pythonは
    同梱WireScopeの作り直しを含む）。McRemoteのcandidateでのlive-autoと、fresh installでの認証ON既定の確認、無印のcaseが
    公開済みb7のJARで落ちることの確認。exact setの凍結後の通常devでの実機試験（代表往復と`mc_version`の照合、2-playerの
    receiver確認をparticleとサウンドで、dust／blockの描画、音が聞こえること・定位、b7からb8へJARを差し替えたときに実tokenの
    まま再接続できること）
  - 非blocker（b9のgateを開くときに扱う）: Scratchのサウンドのlearner block、pickerのalias、b7 release後の是正候補3件、post-b7の
    park 2件、各repoのREADMEの残り。Scratchのentity／particleの9ブロック、カタログID一覧ブロック、pickerの日本語名と検索は
    実装済みなのでcandidateに入れるが、blockerにはしない
  - Windowsの入口ルートは、b8の公開直後にhuman ownerがRelease wheelのURLで確かめる。releaseを止める条件にはせず、結果を
    b9のPyPI登録の判断材料にする
- 日程: 目標は10/3。確認点は10/1の終わりで、Scratchのblockerがそろったかを見る。そろわなければ、その時点で日程を相談する。
  10/2に取り込みと凍結、10/2〜10/3に実機試験
- authorized next action（2026-10-03）: [統一実施票](b8-gate-live-test-sheet_ja.md)を出す。human ownerがdevの通常環境でJARを差し替えて
  identityを記録した後、segment 1〜4を順に行う。tag／releaseの公開はまだ許可しない
- 以前のauthorized next action: [着手依頼](b8-gate-work-instructions_ja.md)を各担当へ出す。
  Stack担当は、dev-integrationの読むだけの事前確認をしてよい（稼働中のMC版、Paperのbuild、Java版、McRemote JARの
  SHA-256、listener、credential domainのhealth。変更しない）。ケータリング方式のセットアップは、b8の公開後にStackの
  別作業として、b8のrelease tagを材料に行う（新規セットアップを1日で仕上げるのが目標。hub NOTESのpark）。このgateの根拠には使わない。shared環境へのcandidate deploy、人間参加の試験、tag／releaseの
  公開はまだ許可しない
- gate result（2026-10-03）: **GREEN — b8横断技術gate完了**。blockerはすべてPASS。non-claimは、server backpressureの案内の実機表示、
  Bedrockでのdustの大きさ、正確な聴感の測定、capacity／soak／rollback、Windows（公開後）、Paper 26.x。公開にはhuman ownerの承認が要る
- release authorization: プロジェクトオーナーの明示承認（2026-10-03）。3 repoともprerelease ON、draft OFF、Latest非対象。tag target、
  default branchへの統合、公開後の照合は下の指示票による
  - McRemote: PR #12をmainへmergeし、そのcommitへ`v1.21.11-2320.0.0b8`。tagのCIが作るJARが`7ab24fa1…77fb`と一致してから公開する。
    添付とtitleは固定workflow（`release.yml`）
  - Python: `52d35f5`をmainへ統合し、そのcommitへ`v2320.0.0b8`。CI成果物がwheel `dcedff01…0180`／sdist `9d56d92b…ad32`と一致して
    から公開する。固定triggerがTestPyPIにも出す
  - Scratch: tagは凍結した`691576f`へ`v2320.0.0b8`。developは`691576f`まで統合する。branchの先頭の`01cdb0b`（列幅、b9）はtagにも
    developにも入れない
  - 一致しないもの（tagのCIのJAR、wheelのdigest等）が出たら、公開せずに止めてcoordinatorへ返す
  - McRemoteのJARの食い違い（2026-10-03）: PR #12をmergeしたcommit `8f13b2f4dc14798899ab5153a0a647c2dea7aa18`へtag
    `v1.21.11-2320.0.0b8`を打ち、tagのCI（run `37113943263`）が作ったJARは261,025 bytesで同じだが、SHA-256が
    `fdffaf0c6e8bf0928ef9872c519ec0ad0c609547cd087040bc2d44daf14d80c6`になり、McRemoteは公開を止めた。coordinatorがCIの成果物と凍結した
    JARを取り出して比べ、148 entryの名前・並び・CRC・サイズ・圧縮方式・時刻・中身のbytesが一致し、違いは146 entryのunix権限bit
    （ファイル664／644、ディレクトリ775／755。buildした環境のumaskの差）だけであることを確かめた。human ownerの判断（2026-10-03）で、
    **CIのJAR `fdffaf0c…`をb8の公開物として受け入れる**。実機試験のPASSは再利用する（release運用と責務分担 §7の「packaging／
    archive metadata」）。凍結set `b8-integrated-artifact-set-1`のMcRemoteの公開JARは`fdffaf0c…`（試験したJAR `7ab24fa1…`と中身は同じ）
- release identity verification（2026-10-03、coordinatorがGitHub APIで読むだけ照合）:
  - Python [v2320.0.0b8](https://github.com/Naohiro2g/minecraft-remote-api/releases/tag/v2320.0.0b8): title「minecraft-remote-api 2320.0.0b8」、
    prerelease=true、draft=false、tag target `52d35f5304e62f465c1f47ab47c00fe9bcf62470`（mainへfast-forward統合、mainの先頭と一致）。asset:
    wheel 195,068 bytes／`dcedff01…0180`、sdist 188,775 bytes／`9d56d92b…ad32`、`manifest.json` 681 bytes／`7aa2868f…9fc0`。manifestは
    schema `mc-remote.release-manifest` v1、`release_tag` `v2320.0.0b8`、`source_commit` `52d35f5`、`bundled_wirescope_source_commit` `df34849`。
    TestPyPIへの公開も成功（担当報告）。Windows検証用のwheel URLは
    `https://github.com/Naohiro2g/minecraft-remote-api/releases/download/v2320.0.0b8/minecraft_remote_api-2320.0.0b8-py3-none-any.whl`
  - Scratch [v2320.0.0b8](https://github.com/Naohiro2g/scratch-editor/releases/tag/v2320.0.0b8): title「mc-remote Scratch 2320.0.0b8」、
    prerelease=true、draft=false、annotated tagのtarget `691576f60b7f0824e1753bd6823901d01fbe2422`、developの先頭も`691576f`（`01cdb0b`は
    b9用のbranchに保持）。asset: `wirescope-app.zip` 83,746 bytes／`4cb34989…0a07`、`wirescope-app.manifest.json` 2,321 bytes／`6ea468f5…24d0`、
    `contracts.tar.gz` 1,908 bytes／`48948ba4…2390`、`manifest.json` 1,168 bytes／`122846bd…2887`。manifestはschema v1、`release_tag`
    `v2320.0.0b8`、`source_commit` `691576f`、OCIは`scratch` `sha256:d595992e05feb891ead10860a14eb292228968d8ca9460505a34fa1d24a1d8c0`、
    `bridge` `sha256:0d7802aba4af418a634afb74c52813810d3b9224ee1ae8e97a485551cf9d79dc`
  - McRemote [v1.21.11-2320.0.0b8](https://github.com/Naohiro2g/McRemote/releases/tag/v1.21.11-2320.0.0b8): title「McRemote 1.21.11 / 2320.0.0b8」、
    prerelease=true、draft=false、annotated tagのtarget `8f13b2f4dc14798899ab5153a0a647c2dea7aa18`（PR #12をmergeしたmainの先頭と一致）。
    asset: `mc-remote-1.21.11-2320.0.0b8.jar` 261,025 bytes／`fdffaf0c…80c6`（受け入れたCIのJAR）、`manifest.json` 387 bytes／
    `382a7a3e…037e`。manifestの`release_tag` `v1.21.11-2320.0.0b8`、`source_commit` `8f13b2f`、role `jar`のdigestが一致。release
    workflow run `37117743334`がsuccess
  - Latest: 3 repoとも変えていない（McRemoteは`v1.21.8-1.4.0`、Pythonは`v1214.10.11`、ScratchはLatestなし）
- gate result（公開）: **3 repoのGitHub prerelease公開identityを確認した（2026-10-03）**。残りはgateのclose（default branchへの
  統合の確認、各repoの`handoff-materials`の分類、parkの見直し、b9の移管の起点にするfixtureの一覧の記録）
- b9の移管の起点（2026-10-03、Scratchの返却）: 公開source `691576f`時点のfixture 12件（Protocol 7、WireScope 4、Bridge 1）の
  path、bytes、SHA-256、case数、consumerを[一覧](../14-evidence/artifacts/2026-10-03-b8-dev-live/scratch/2026-10-03-b8-close-inventory/FIXTURES_ja.md)に収容した。Protocolの主なものは`direction-lightning-v23.1.json`
  20,367 bytes／`586d24bf…0dce`／93 case、`entity-particle-v23.2.json` 36,481 bytes／`ca636b4a…39f2`／111 case、`sign-v23.json`
  5,043 bytes／`7ffb63c2…d30e`／7 group。VM runtimeは`@mc-remote/protocol`をimportせず、VMとWireScopeのtestがrepo相対pathでfixtureを
  読む。release manifestの`contracts`はScratch GUIのconfig schemaで、protocol fixtureの配布物ではない
- handoff-materialsの分類（2026-10-03）: McRemote、Python、Scratchの①の素材と、Scratchの③の素材のテキストを
  `14-evidence/artifacts/2026-10-03-b8-dev-live/`へ全文のまま収容した（一覧と収容しなかったfileは`INVENTORY_ja.md`）。②は各担当が
  後続（b9等）のために保持する
- close（2026-10-03、human ownerの判断）: **b8 gateをCLOSEDとする**。default branchへの統合は照合済み（McRemote main `8f13b2f`、
  Python main `52d35f5`、Scratch develop `691576f`がそれぞれtagと一致）。gateを閉じるときのpark確認（`2026-09-30-09`）で、API一覧、
  ケータリング、Windows、iPad、browser検証能力の行を更新した。各repoの`handoff-materials`の分類と、b9の移管の起点にする
  fixtureの一覧の記録は、hub NOTESのpark「b8 gate closeの残り」で追う
- authorized next action（2026-10-03、公開）: 各repoへ公開の指示票を出す。公開後、coordinatorがtag target、prerelease／draft、
  `manifest.json`のartifact identityをGitHub APIで読むだけ照合し、gateを閉じる
- non-claim: PyPI.orgへの公開とAPI freeze（b9）、capacity／soak／rollback（rc1。rollbackの範囲案はhub NOTESにpark）、public deploy、Scratch learner block、
  サウンド以外の新API（`2026-09-30-03`で初回stable後）、tooling移管（b9）、26.x（`2026-09-30-07`）、Java、
  初回stableの互換

## 2026-09-07 b7.post2（manifest.json導入・収集経路ランスルー／完走）

- gate coordinator: knowledge担当session。人間による明示handoffなしに他担当へ移さない
- human release owner: プロジェクトオーナー
- current phase: **ランスルー完走**。mc-remote-stackのCodexセッションが2026-09-07に収集→preset／order／lock確定→apply→doctorを実作業で通し、発見2件をStack側で手当てして完了した
- 目的: `2026-09-06-02`〜`2026-09-06-04`で確定したmanifest.json方式を実装し、release closeから収集・preset／order／lock確定・apply・doctorまでの経路を実際に通して検証する。protocol／APIは変更しない
- release mode: 軽量mode（`release-operations-responsibility-design_ja.md` §14）。protocol `23.1.0`／artifact `2301.0.0b7`のpost-releaseであり、新API、wire変更、b8実装を含まない
- version／tag表記: `.postN`（ドット区切り）を使う（`2026-09-07-03`）。Scratch `v2301.0.0b7.post2`、McRemote `v1.21.11-2301.0.0b7.post2`、Python `2301.0.0b7.post2`。既に公開済みの`v2301.0.0b7-post1`は差し替えない
- manifest contract: top-levelへ`schema`（`"mc-remote.release-manifest"`）、`schema_version`（整数）、`release_tag`、`source_commit`。`artifacts[]`は`kind`を必ず明示し、`kind:oci`は`locator`＋`digest`、`kind:https-file`は`file`＋`sha256`を持つ。WireScopeは`wirescope`（zip）と`wirescope-manifest`（detached manifest）の2件を個別に載せる。contractsは`contracts.tar.gz`（role `contracts`）。Pythonは`bundled_wirescope_source_commit`をtop-levelへ持つ。manifestはrepo単位で生成し各repo自身のReleaseへ添付する（横断統合manifestは作らない）
- 参加component: McRemote／Python client／Scratch editor（Bridge・WireScopeはScratch releaseへ同梱）。human release ownerの指定により実施した
- 公開されたrelease（coordinatorがGitHub APIでread-only照合）:
  - Scratch `v2301.0.0b7.post2`（source `f133fc95ed7b23109cc1908dc4f0dae066510258`）。manifest roleは`scratch`（oci `ghcr.io/naohiro2g/mc-remote-scratch@sha256:738dae72…`）／`bridge`（oci `ghcr.io/naohiro2g/mc-remote-bridge@sha256:099d24d5…`）／`wirescope`／`wirescope-manifest`／`contracts`の5件
  - Python client `v2301.0.0b7.post2`（source `b94af23404d3f197b37060c0a272a1a1cd972f7d`）。role`wheel`／`sdist`、`bundled_wirescope_source_commit`＝`0be46fcfaca409a5ede10f592520d93e7c59ba15`
  - McRemote `v1.21.11-2301.0.0b7.post2`（source `f99ee8046e1a000699e6c38a4d8625f9918832c5`）。role`jar`
- manifest schema適合: 3件とも`schema`＝`mc-remote.release-manifest`／`schema_version`＝`1`を持ち、全artifactが`kind`を明示していた。tagは3件とも`.postN`ドット表記（`2026-09-06-04`／`2026-09-07-03`のとおり）
- 成功基準（ランスルーの観測対象）: release close直後に開始し、収集がrelease tag 1件の指定だけで完結すること。人間またはagentが個別のcommit／digestを会話やhandoffテキストから思い出す場面が発生しないこと。通常（非ケータリング）でserver起動まで10分未満、ケータリング型でも小幅な追加に収まること（`2026-09-06-02`）
- ランスルーの発見と手当（いずれもStack側でmerge済み。coordinatorはPR本文の申告を受理し、実装の正しさを独自に判定しない）:
  - 非対話SSHで`uv`がPATHに無く、runbook stepが`command not found`で止まった。call siteごとの回避でなく、pinned `uv`を`/usr/local/bin`へsymlinkして解決（mc-remote-stack PR #49）
  - 前presetのprojectから持ち越されたoperator noticeが、対象releaseのScratch product configが既に表示している内容と重複した。`plan`／`apply`／`doctor`はいずれもPASSしている——operatorとproduct noticeの重複は意図的に行う場合があり、機械には持ち越し事故と区別できないため`doctor`の検査対象にしない。収集直後に人間へkeep／edit／add／deleteを問うcheckpointをrunbookへ置く手当てとした（mc-remote-stack PR #50）
- 成功基準に対する観測: 収集段階で個別のcommit／digestを会話やhandoffから思い出す場面は報告されなかった。発見2件はいずれもidentity解決ではなく、環境bootstrapと人間判断の欠落だった。所要時間は未計測のため10分基準の達成可否は主張しない
- 未検証の境界: WireScopeの横断real-browser E2E（同一artifactをPython／Scratch両sourceで順に使う）とhome alphaが未完で、Stack後続gateの再判定も未了（`15-wirescope/wirescope-station-attach-design_ja.md` §10 step 7／step 9）。`2026-09-06-01`によりrelease判定条件はこの欄で扱い、未達のまま進める場合は再開条件をここへ記録する
- 既知の前提: b7以前の公開済みreleaseにはmanifestが無い。既存releaseのartifact identityは本ファイルの凍結済みexact setを正本とする（`deployment-interface-design_ja.md` §4）
- authorized next action: mc-remote-stack担当（Codexセッション）が、収集→preset／order／lock確定→apply→doctorのランスルーを実施し、観測を返す。target host、exact set、実施範囲はhuman release ownerとcoordinatorが指定するまで拡張しない。実行commandの正本はStack runbookに置き、本ファイルへ複製しない（`2026-09-04-04`）
- 返却してほしいもの: 実際に使ったrelease tagとmanifest identity、収集で手が止まった箇所（会話やhandoffから値を思い出す必要が生じた箇所）、各段階の所要時間、doctorの結果、未実施範囲、non-claim
- gate result: **ランスルーの目的（収集経路が実作業で通ること）は達成**。coordinatorが確認したのはGitHub API上のrelease identityとmanifest schema適合までで、実機のapply／doctor結果はStack担当の報告として受理した（`2026-09-03-07`）。横断release gateとしてのGREENは主張しない
- B8への投影（2026-09-23確認、`2026-09-23-02`）: この完走で`2026-09-04-04`のB8 HOLD再開条件は満たされた。B8 contract lockと実装を再開可能とする。B8 release GREEN、public deploy、shared環境変更の許可はこの観測から導かない
- non-claim: b8実装、protocol変更、public deployの可否、初回stable互換は本gateに含めない

## 2026-09-02 b7横断release gate（CLOSED）

- gate coordinator: knowledge担当session。人間による明示handoffなしに他担当へ移さない
- human release owner: プロジェクトオーナー
- current phase: **GitHub prerelease公開完了／b7 gate close**。McRemote／Python／Scratchの3リポをdefault branch（main／main／develop）へ統合し、`v1.21.11-2301.0.0b7`／`v2301.0.0b7`／`v2301.0.0b7`をprerelease公開した。Java／Stackは今回動かさない。OCI pushは未実施
- contract: protocol `23.1.0`／artifact `2301.0.0b7`、`10-protocol/wire-format-design_ja.md` §5.8.2、DECISIONS `2026-09-01-01`／`2026-09-01-02`。permission改訂はhello時snapshot、`mcr.online`／`mcr.offline`独立、状態不一致session close、`mcr.lightning`削除
- exact source set: `b7-integrated-source-set-1`。McRemote `main@3d5f710db97f4b14613f7e0abaafd535701d1906`、Python `main@8f4bc4b96ae74fb5370a3d804676cd07e5352346`、Scratch `develop@773e2984132d82bb6e740d6458107fe42ef68a0a`
- shared fixture: 20,367 bytes、93/93 unique、SHA-256 `586d24bf40136eec31f1827f23ef5b317f15100a17a635d7fe9f165e0af40dce`。三default branchでexact一致。ownerはpark判断どおりScratch内`@mc-remote/protocol`を維持
- gate manifest identity: 正式pre-OCI manifestは未成立。coordinator生成`b7-integrated-artifact-input-1`／manifest SHA-256 `f77242b5…1de8`は参考観測として履歴保持するが、owner provenanceを欠くためgate入力へ使わない
- verification: McRemote／Python担当の統合artifact返却は維持する。Scratch owner set 2（`0be46fcfa…`、direction／lightning learner block実装込み）の四成果物をcoordinatorがlocal stagingでbytes／SHA-256照合し一致。branch実在・HEAD一致・lineage ancestry（`773e298`→`57e2885`→`3d5142f`→`31ca03c`→`0be46fc`）もGitで確認済み。旧「Scratch非参加」判断は`2026-09-02-01`で撤回
- component artifact identity（`b7-scratch-owner-artifact-set-2`、詳細は`13-scratch-client/b7-owner-artifact-generation-instructions_ja.md`）: GUI tar 234,651,616 bytes／SHA-256`d6a569f1…20b8c`、Bridge中間tar 3,052 bytes／SHA-256`11199a8e…31c72`（b6と一致）、WireScope ZIP 79,418 bytes／SHA-256`98d684dc…a263b8`、manifest 2,321 bytes／SHA-256`7498e321…f028f`。test: Protocol28/28、Bridge30/30、WireScope134/134、GUI unit476/1skip、integration127/7skip、Playwright8/8
- component artifact identity（Python更新版）: `codex/b7-wirescope-set2@91a25d317c95570fd9d92b5e63a5f585a856eda3`（parent`8f4bc4b9…`、coordinatorがancestryとbundled WireScope pair一致をGitで確認）。wheel 196,970 bytes／SHA-256`81540d22…6d2ba`、sdist 203,313 bytes／SHA-256`55a9915b…b37a0b`。旧wheel/sdist（177,243／183,908 bytes）はb5時点bundled WireScopeを含むため失効。全回帰253 passed、targeted WireScope/b7 112 passed
- **exact set凍結（`b7-integrated-artifact-set-1`）**: protocol `23.1.0`／artifact `2301.0.0b7`。
  McRemote `main@3d5f710db97f4b14613f7e0abaafd535701d1906`／JAR 222,951 bytes SHA-256`f08388cf393e02db1eb605e707dfaec890792e7a475de5a51caacbc940028ee9`。
  Python `codex/b7-wirescope-set2@91a25d317c95570fd9d92b5e63a5f585a856eda3`（parent`8f4bc4b96ae74fb5370a3d804676cd07e5352346`）／
  wheel 196,970 bytes SHA-256`81540d22b1ee05d7b24bd2e6c9270a37a194c6c1ddc868148a8263624826d2ba`／
  sdist 203,313 bytes SHA-256`55a9915b7607e35e2c1f335561b65fcd38deff90fe49f5b56c65122665b37a0b`。
  Scratch `agent/b7-scratch-wirescope@0be46fcfaca409a5ede10f592520d93e7c59ba15`／
  GUI 234,651,616 bytes SHA-256`d6a569f1f315ca06a24f9d7a987129e824f5df60eb32d226dd6d776f47d20b8c`／
  Bridge中間 3,052 bytes SHA-256`11199a8e6966e8a5160411104934498657f4befd3d27a8fc25c88f51afa31c72`／
  WireScope ZIP 79,418 bytes SHA-256`98d684dc15f369f6568d249357d8fd3af11893859d3c07c2554295df19a263b8`／
  manifest 2,321 bytes SHA-256`7498e32150884aec8c3d562b454d8b042032aa21893ae7fe886c06df2baf028f`。
  shared fixture 20,367 bytes／93 cases SHA-256`586d24bf40136eec31f1827f23ef5b317f15100a17a635d7fe9f165e0af40dce`。
  Java／Stackはこのsetに含めない（b6 baseline維持）。source／artifact identityが一つでも変われば本freezeは失効する
- live-human結果: `2026-09-03-b7-direction-lightning-live`。Python segment PASS（direction／entity direction／lightning、視聴覚確認）、Scratch／WireScope segment PASS（同5 method、real-browser視聴覚確認）。McRemote plugin側blockerは`2026-09-01-b7-direction-lightning-live`のaddendumで既にCLOSED。四component全てのlive-human完了。証跡: [`14-evidence/records/2026-09-03-b7-direction-lightning-live_ja.md`](../14-evidence/records/2026-09-03-b7-direction-lightning-live_ja.md)
- release後是正候補（b7 candidateは変更せず搬送）: WireScope保持windowの空振り占有、Scratch数値入力欄のCtrl+C不動作、server backpressureをclient切断と誤案内するGUI表示。詳細は上記evidence record
- gate result: **GREEN — b7横断技術gate完了／GitHub prerelease公開identity確認完了**
- release authorization: プロジェクトオーナーの明示承認（2026-09-03）。McRemote `v1.21.11-2301.0.0b7`を`3d5f710db97f4b14613f7e0abaafd535701d1906`（既存default）へ、Pythonは`v2301.0.0b7`を`91a25d317c95570fd9d92b5e63a5f585a856eda3`へ、Scratchは`v2301.0.0b7`を`0be46fcfaca409a5ede10f592520d93e7c59ba15`へ固定。Python `main`とScratch `develop`はcoordinatorがScratch担当の分岐なし確認後、これらcandidateへstrict fast-forward統合してから公開した。各releaseはprerelease ON、draft OFF、Latest非対象
- release identity verification: McRemote [v1.21.11-2301.0.0b7](https://github.com/Naohiro2g/McRemote/releases/tag/v1.21.11-2301.0.0b7)はtag target `3d5f710db97f4b14613f7e0abaafd535701d1906`、JAR asset 222,951 bytes／SHA-256 `f08388cf393e02db1eb605e707dfaec890792e7a475de5a51caacbc940028ee9`。Python [v2301.0.0b7](https://github.com/Naohiro2g/minecraft-remote-api/releases/tag/v2301.0.0b7)はtag target `91a25d317c95570fd9d92b5e63a5f585a856eda3`、assetsなし、release notesにwheel／sdist digest記載。Scratch [v2301.0.0b7](https://github.com/Naohiro2g/scratch-editor/releases/tag/v2301.0.0b7)はtag target `0be46fcfaca409a5ede10f592520d93e7c59ba15`、assetsなし、release notesにGUI／Bridge／WireScope digest記載。三件ともprerelease=true、draft=false、既存stable Latest（McRemote `v1.21.8-1.4.0`、Python `v1214.10.11`、Scratchはlatestなし）を変更していないことをGitHub APIで確認した
- authorized next action: default branch統合とrelease identity確認をもってb7 gateをcloseする。PyPI／TestPyPI、registry publish、public deploy、runtime／server変更、b8実装はこのrelease確認に含めない
- non-claim: PyPI／TestPyPI、npm、Modrinth、public server deploy、通常dev環境runbook改訂を主張しない

## 2026-08-27 b6横断release gate（CLOSED）

- gate coordinator: knowledge担当session。人間による明示handoffなしに他担当へ移さない
- human release owner: プロジェクトオーナー
- current phase: **GitHub prerelease identity確認完了／b6 gate close**。`b6-artifact-candidate-set-4`を人間承認後に三repoのtag／GitHub prereleaseへ公開し、tag target、prerelease／draft、Latest非対象、McRemote JAR asset、release notes digestをAPIで確認した
- contract maturity / required test tier: b6 wire contract、共有fixture、target、server runtime identityは固定・照合済み。Tier 2で見つかった二件はScratch GUI／WireScopeのclient-only change coneで閉じ、set 1／2の観測履歴を残してset 3を固定した。b6横断技術gateと公開identityをGREENとして閉じるが、Tier 3完了やstable互換は主張しない
- knowledge contract: `10-protocol/versioning-design_ja.md` §10.11.4、`10-protocol/wire-format-design_ja.md` §5.4／§5.8／§7.3、`10-protocol/beta-to-stable-release-roadmap_ja.md` §3.1、`10-protocol/b6-compatibility-fixture-plan_ja.md`、`15-wirescope/wirescope-deployment-design_ja.md` §14。DECISIONS `2026-08-26-05`／`2026-08-26-06`／`2026-08-26-08`／`2026-08-27-01`／`2026-08-27-02`／`2026-08-27-03`／`2026-08-28-01`。core b6 contract baselineは`b47d979c6779842e9eea892e90f69f0bdbd4dc4b`
- gate manifest identity: Tier 2 evidence入力は`b6-artifact-candidate-set-3`、現行sourceは`b6-integrated-source-set-1`、OCI前の六artifactは`b6-integrated-artifact-input-1`として履歴固定する。入力manifest SHA-256は`1a3b40fc3747359bd2a206f37aa4b8508989b97aedc6b6d584d8cfd49b3c4a4b`。六artifactとScratch／Bridge OCIを`b6-artifact-candidate-set-4`として固定した。OCI identity JSONのSHA-256は`f7229cf2484858867a52b782f8de89c358b6920532555f06e955f05e08413634`。人間可読のbinding recordは`10-protocol/b6-artifact-candidate-record_ja.md` §7〜§10である
- exact compatibility set / freeze status: **公開release identityとして凍結**。McRemote `main@4e8f1ff1bd48bfa28c465f2dc24060fbb419317f`、Python `main@a30a37b15658da655fe1e3535a73fb0e80c06f56`、Scratch／Bridge／WireScope `develop@df9264ec355dd722a848df46e96d4b0fc9340ca2`。protocol `23.0.0`、artifact version `2300.0.0b6`。三repoのtagは各SHAを直接指す
- component readiness:
  - McRemote: clean exportで149/149件とJAR生成をPASSし、JAR 204,463 bytes／SHA-256 `0ec8d4c0b105f3034361b260fc39fcb78013e932e684d34d5ca95c9a6c6a87a6`をdurable stagingと通常devへ固定した。オンライン0人、旧candidate JARのrollback入力を確認して正常停止・一件交換・再起動し、version、credential `HEALTHY`、標準listener、auth否定4 pathをPASSした。新規session pairing後の認証済みhello＋`catalog.get`、同じJARの正常再起動後にpairingなしで同じ期限内tokenを再利用した`catalog.get`もPASS
  - Python: 統合後mainの全source treeはcandidateと同一。clean tarballで242/242件をPASSし、再生成wheel／sdistはset 3とbyte-for-byte同一の`0887807f…1877b`／`0507a10c…da3b`だった。digestをrelease notesへ固定し、binary asset／PyPIなしのGitHub prereleaseとして公開した
  - Scratch: candidateをconflictなしでdevelopへno-ff mergeし、機能差分なし。isolated clean checkoutの`npm ci`＋全workspace production buildをPASSし、GUI tarは旧setと同一`1757f665…7ef5`、WireScope ZIPも同一`b3d62702…ca315`、統合SHAを持つmanifestは新digest`8570d3ee…296f`として固定した。owner報告はprotocol 22/22、WireScope 130/130、Bridge 30/30、GUI 471件PASS＋既知1 skip。Scratch VM aggregateの総数と内訳の表記差はfull suite exact集計PASSへ読み替えないが、関連suiteのisolated PASSとbuild／Tier 2実証が成立し、新規regression観測がないためb6 blockerにしない。manual workflow run `33136505029`でScratch／Bridge OCI build／push／identity生成をPASSし、digestをrelease notesへ固定したGitHub prereleaseとして公開した
- change cone: b6必須はsign三操作、`pickaxe_poke`、Scratch project／sprite browser保存、protocol 23 cleanup。WireScope表示filter／`dropped_frames`／mini配置／poll pair安定化／表示停止はclient-only companionであり、server wire、observer schema、plugin、Python、Bridgeを変更しない
- reused PASS / rationale: set 3のTier 2実証は統合sourceの祖先candidateへ結び、履歴として再利用する。Python／Scratchの統合には機能差分がない。McRemoteの追加change coneは既にb4／b5で実測済みのsession token永続化だけで、production blobも同一のため、全Tier 2 E2Eは反復せず新JARの最小統合smokeへ限定する。Scratch aggregateは全件PASSへ書き換えず、isolated PASSと未返却の集計内訳を分けて保持する
- canonical case audit: `10-protocol/b6-compatibility-fixture-plan_ja.md`。protocol／artifact identity、handle、sign、`pickaxe_poke`、legacy method不在をcase IDへ分け、source candidate set 1のgap、set 2のowner発行と投影、`data.allowed`追補、source candidate set 3のPASSまで記録した。artifact candidate set 1〜3とは別の番号列であり、根本wire shapeの再設計を要求する差分はない
- shared fixture owner: Scratch `agent/b6-source-refresh@104f194d…`の`@mc-remote/protocol/test/fixtures/`。`sign-v23.json`はSHA-256 `7ffb63c264602cba56117eefff1f9604b955df04c5cc655e877772b8ff7cd30e`、`events-v23.json`は`31760d267f3c2641042fbe8595fda9c259134a1c05423271a99cb74da1efa9aa`。三repoの配置bytes、case接続、McRemote productionのsign error順を照合し、共有fixture gate PASS
- target and preflight: 人間承認により論理deployment `dev-integration`、物理hostはホームサーバー`home-host-2`、host-native `run.sh`＋Screen runtimeを再利用する。2026-08-27のread-only preflightでは旧systemd版はinactive、`Minecraft server` Screen sessionと標準port `25565`／`25575`が稼働中で、Paper JARはb5と同じSHA-256 `5ffef465eeeb5f2a3c23a24419d97c51afd7dbb4923ff42df9a3f58bba1ccfba`、現行b5 McRemote JARは公開releaseと同じ`f7ddbcb5a92acadfe1adb7a9f6a4f50a05707e2eefbd1c01ff9aeeebe0a36547`だった。private address、player UUID等のraw log値は本票へ収録しない
- staging and runtime result: set 1〜3を上書きせず、統合後六artifactと入力manifestを別のdurable stagingへ固定して全size／SHA-256を再照合した。通常devは旧candidate JARから統合JARへ一件だけ交換し、Paper、world、config、credential backendを維持した。server起動、新規session認証済み代表call、同じJARの正常再起動後session再利用までPASS。既存`run.sh`を別Screenで包んだ初回操作はserver開始前に終了し、dead outer sessionを除去して`run.sh`を直接実行した。この訂正で製品入力は変更していない。raw token、pairing code、private address、player identityは収録しない
- release authorization: プロジェクトオーナーの明示承認（2026-08-28）。McRemote `v1.21.11-2300.0.0b6`、Python `v2300.0.0b6`、Scratch `v2300.0.0b6`を上記default branch SHAへ固定し、prerelease ON、draft OFF、Latest非対象で公開する。PyPI、Modrinth、public server deploy、通常dev再構築は含めない
- release identity verification: McRemote [v1.21.11-2300.0.0b6](https://github.com/Naohiro2g/McRemote/releases/tag/v1.21.11-2300.0.0b6)はtag target `4e8f1ff1bd48bfa28c465f2dc24060fbb419317f`、JAR 204,463 bytes／SHA-256 `0ec8d4c0…a87a6`、release notes SHA-256 `731f491b…2059`。Python [v2300.0.0b6](https://github.com/Naohiro2g/minecraft-remote-api/releases/tag/v2300.0.0b6)はtag target `a30a37b15658da655fe1e3535a73fb0e80c06f56`、assetsなし、release notes SHA-256 `d7e8293c…55c`。Scratch [v2300.0.0b6](https://github.com/Naohiro2g/scratch-editor/releases/tag/v2300.0.0b6)はtag target `df9264ec355dd722a848df46e96d4b0fc9340ca2`、assetsなし、release notes SHA-256 `a81a0bed…842a`。三件ともprerelease=true、draft=falseで、既存stable Latestを変更していない
- component close verification: McRemoteは三b6 candidate branchがtag／mainの祖先で、protocol／artifact versionと未批准API不在を確認した。Pythonはb6 candidateがtagの祖先で、PyPI／TestPyPI非公開を維持し、post-release ledger `PUBLISHING.md`を`main@b66e7815a2d35101a2e57ce61e91c1993671cb1d`で更新した。Scratchはb6関連branchのcommitまたはcherry-pick内容がtag／developへ全収容され、OCI workflow／digestと再生成WireScope artifactがrelease identityへ一致した。三repoともb6未収容commitなし、branch／worktree削除なし、追加実装なし
- authorized next action: release identityとcomponent close確認をもってb6 gateをcloseする。Python `README.md`のPackage Information表をb5から公開済みb6へ更新する小follow-upだけを残す。Paper 26.2 compatibility pulse、browser bootstrap整理、b7以降のAPI再編は別taskとして起票し、b6 gateへ戻さない
- resolved human decision: `2026-08-27-01`で現行WireScope表示filterをb6 client-only UX v1として受理し、後続の実使用からpending pair保留、表示signatureによるDOM安定化、「表示を一時停止」を同じclient-only UXへ具体化した。表示停止は観測／pollを止めず、通常時の非点滅／copy安定化の代替にしない。正本は`15-wirescope/wirescope-deployment-design_ja.md` §14
- resolved observer boundary: 現行observer allowlistがb6 sign三操作を含まない点は、`2026-08-27-01`がallowlist拡張を含めないと明記した範囲どおり、b6では**WireScope v1の非必須観測範囲**と判定する。signの互換性はScratch APIと実worldで確認し、WireScope E2Eはhello／`pickaxe_poke`／現行allowlist method／`dropped_frames`を使う。filterの`world`分類からsign frame観測済みと推測せず、本判定を理由にScratch SHAを変えない
- resolved Bridge package boundary: set 1〜3の`mc-remote-bridge-dist.tar.gz`はViteが`ws`をexternalizeした`dist/`だけの中間buildで、単独deploy可能なrelease artifactではない。`2026-07-14-04`、Bridge Dockerfile、manual image workflowが既に、`dist/`＋`package.json`＋lock済み`node_modules/ws/`だけを非root runtimeへ入れるmulti-arch OCIを正としている。tarへdependencyを追加する新形式は作らず、残件を統合sourceからのOCI生成／digest固定／container smokeへ限定する
- evidence: `14-evidence/records/2026-08-27-b6-tier2-integration-pulse_ja.md`はset 1初回pulse、`14-evidence/records/2026-08-28-b6-scratch-wirescope-live-human_ja.md`はpoke／Scratch／WireScope継続pulseとset 2／3 change cone、`14-evidence/records/2026-08-28-b6-integrated-artifact-smoke_ja.md`は統合後artifact入力とMcRemote最小runtime smokeを記録する
- gate result: **GREEN — b6横断技術gate完了／最終artifact candidate確認完了**。host-native通常dev、実browser、component test／build、共有fixture、統合後JAR smoke、OCI registry identityの範囲でb6 release candidateを受理する
- non-claim: 観測target変更後の自動再開、live `dropped_frames`、Scratch full suite exact aggregate、OCI runtime deployment smoke、public server deploy、PyPI／Modrinth公開を主張しない。これらをGitHub prerelease作成のblockerにしない
- rollback: 公開済みb5 exact release set。b6 rollback実操作は未実施

## 2026-08-21 b5横断release gate（CLOSED）

- gate coordinator: knowledge担当session。人間による明示handoffなしに他担当へ移さない
- human release owner: プロジェクトオーナー
- current phase: **b5 prerelease identity確認完了／技術gate close**。3 componentのGitHub prereleaseがexact setへ固定され、tag target、公開状態、Latest非対象、asset／release notes digestをAPIで確認した
- contract: 技術scopeはDECISIONS `2026-08-21-01`／`2026-08-21-02`／`2026-08-22-02`、進行責任は`2026-08-21-03`／`2026-08-21-04`。DimensionKeyの説明正本は`10-protocol/dimension-key-design_ja.md`
- exact compatibility set / freeze status: **凍結**。McRemote `bbbb53602a9c375e2ead3ee4c22174d5cf424f55`／JAR 195,998 bytes・SHA-256 `f7ddbcb5a92acadfe1adb7a9f6a4f50a05707e2eefbd1c01ff9aeeebe0a36547`、Scratch `1a11c46bac5696afd3f494caac56ae682ed00fb0`／CI run `32574020556`／GUI build artifact ID `9476135596`・digest `sha256:a5fef95460d2e07accd5eb82276def9eafa36692166e1db34e833447e6f6865e`／Bridge artifact ID `9476136894`・digest `sha256:2b84bf753ac67ea4906c9beb590cdb63d03da282015e40995ec129e3697b8e7b`／common WireScope ZIP `407031d5…a6964`・manifest `15d0c6b9…5bda`、Python `64b0f8831fa33e74f1b70b9102b3f29ec99b8e14`／wheel 170,271 bytes・SHA-256 `370f0fef3d5124a1024cbea8dfb4c65f2080cb545ab342086a827287d0f3f195`／sdist 175,715 bytes・SHA-256 `4337c6502f2be58e2bbf526d657c3f41d962bab08dd5a68eeb9527d66c9896b6`を一組とする。protocol `22.0.0`、artifact `2200.0.0b5`、observer schema／session／handoff／station attach version `1`、compatibility revision `v1.1`。いずれかのsourceまたはartifact identityが変わればこのfreezeを失効させる
- landing verification: `2026-08-21-03`／`2026-08-21-04`の責務契約は全担当で一致。McRemote、Python、Scratch／WireScopeはknowledge `f9d5dc7780ab2673b8872dc7481d230e10ca95d9`とremote mainの一致、`2026-08-22-02`との設計差分なしを確認した。各返却で列挙された差分はknowledge契約の不一致ではなく、旧world契約candidateの未追従実装である。設計再検討へ戻さず、3担当の実装とpush済みidentity返却を許可する
- DimensionKey component refresh:
  - McRemote: **candidate入力固定済み**。remote branch `codex/b5-reproducible-jar@bbbb53602a9c375e2ead3ee4c22174d5cf424f55`。共通DimensionRef codec／resolver、`Bukkit.getWorld(NamespacedKey)`、`build.setDimension`、hello／build context／player／event／entity handleの`dimension`、`unknown_dimension`／`entity_dimension_changed`を実装し、旧method／field／alias／fallbackを撤去した。Java 95 tests、runner 4 tests、clean build、構文検査、diff check PASS。独立clean checkout 2件のJARはbyte-for-byte一致。JARは195,998 bytes／SHA-256 `f7ddbcb5a92acadfe1adb7a9f6a4f50a05707e2eefbd1c01ff9aeeebe0a36547`
  - Scratch／WireScope: **candidate入力固定済み**。remote branch `agent/b5-protocol22-block-value@1a11c46bac5696afd3f494caac56ae682ed00fb0`。DimensionKey command／DTO／build context、標準menuと一般namespace自由入力、validator／adapter／表示を同時更新し、旧union／alias／shimを撤去した。CI run `32574020556`は全job PASS。GUI build artifact ID `9476135596`／digest `sha256:a5fef95460d2e07accd5eb82276def9eafa36692166e1db34e833447e6f6865e`、Bridge artifact ID `9476136894`／digest `sha256:2b84bf753ac67ea4906c9beb590cdb63d03da282015e40995ec129e3697b8e7b`。common WireScope ZIPは59,836 bytes／SHA-256 `407031d5e64279d90572f0843c788d2e4d9daac5b1ad12ffa121fa7f9fca6964`、manifestは2,321 bytes／SHA-256 `15d0c6b9a46ee68ac93dc850c9c5014c46476f7af1a49c7e98b2397cd7f95bda`。同一commitから2回生成してbyte-for-byte一致。observer schema／session、Scratch handoff、station attachはversion `1`
  - Python: **candidate入力固定済み**。remote branch `codex/b5-structured-block-value@64b0f8831fa33e74f1b70b9102b3f29ec99b8e14`。`setDimension()`、canonical build contextの原子的同期、player／event／guard、observer／stationをDimensionKeyへ更新し、旧world API／field／unionを撤去した。Scratch exact sourceからNode `24.19.0`で独立再生成したcommon WireScopeとPython同梱物はbyte-for-byte一致。Python 3.11／3.13で各225 tests、lock／compile／fixture／metadata／RECORD／license検査PASS。独立clean checkout 2件のwheel／sdistはそれぞれbyte-for-byte一致。wheelは170,271 bytes／SHA-256 `370f0fef3d5124a1024cbea8dfb4c65f2080cb545ab342086a827287d0f3f195`、sdistは175,715 bytes／SHA-256 `4337c6502f2be58e2bbf526d657c3f41d962bab08dd5a68eeb9527d66c9896b6`
- component readiness（以下の旧candidate PASSは影響外の観測履歴として保持し、DimensionKey sliceの合格には使わない）:
  - McRemote: **live-auto segment PASS**。source `fc84c8fd5e41c07c5d89671f193fdb7012eabd36`／JAR SHA-256 `7f9bf3616accc27cac100c705aa3bfc722024978a76a5505015d80047054012f`をhost-native `dev-integration`で実行し、runner全項目PASS。修正対象の`world.spawnParticle`は未ロードchunkのload／generate後にaccepted count `1`、`world.spawnEntity`は256 unique handles、257件目`entity_capacity_exhausted`、別epoch独立を実機確認した。structured block、`getBlocks`、`getHeight`、FIFO／flush、1041 notification burst、`events.poll`、validationもPASS。serverは試験後もactiveで標準portを待受。旧source `ef025ce5…`／JAR `17cdc457…aeb6`は修正前candidateとして失効する。試験で生成したentity／blockは再生成可能なruntime stateであり清掃を後続segmentの開始条件にしない。stale／latest cursor、server poll上限縮小、reconnect後cursor失効、3種eventの人間操作は本segmentのnon-claimとして後続へ送る
  - Scratch／WireScope: **決定論的component candidate準備済み**。remote branch `agent/b5-protocol22-block-value@602ecdf809f87a7e33e50d7c465b7248429e26dc`、protocol `22.0.0`／artifact `2200.0.0b5`。CI run `32504972088`はexact headのBuild／Scratch VM／Scratch GUI／Test Resultsが全てsuccess。GUI build artifact ID `9455095975`／digest `sha256:4b8186a32cdeba62dfaf69a58e95c909dcd0351559b6b30459aba4e0b72c9592`、Bridge artifact ID `9455099784`／digest `sha256:cab330cabf38351699bca92e3c22a6299cb23ddaecd7c9c39788f998df284950`。common WireScope ZIPは59,340 bytes／SHA-256 `f3ffaa1c55122b21acaccf9467bbd39c775c44d7e982fa3b11658d10a14b0f49`、detached manifestは2,321 bytes／SHA-256 `b7565dd7f4883020737bbe5f5dfb28819862d0edc54bb4b4d5503d99c5d65780`。manifestはsource commit、Node `24.19.0`、`npm ci && npm run build:artifact --workspace=@mc-remote/live -- --source-commit 602ecdf809f87a7e33e50d7c465b7248429e26dc`、observer schema／session／handoff／station attach version `1`を固定。専用CI uploadはなくlocal `/tmp`を取得元にはしないため、Pythonがpush済みsourceから独立再生成して両SHAへ一致させる。live未実施
  - Python: **決定論的component candidate準備済み**。remote branch `codex/b5-structured-block-value@af2b19dd4a4f0404c4bde439021ca7e017904a04`、protocol `22.0.0`／artifact `2200.0.0b5`。push済みsource内のWireScope ZIP／manifest blobをknowledge coordinatorが再hashし、ScratchのSHAと一致。wheelは167,478 bytes／SHA-256 `a3dacff46027108a6216ded320ad7b75f9b42b4dbdb3e424059c49e0935fcf0c`、sdistは172,944 bytes／SHA-256 `e6684f15197d165203c8b5b9f99669b16893de19f95cfe2456074359e43403fd`。clean commitからのbuild再現、52 focused tests／216全決定論的tests、compileall、metadata／RECORD／license／corresponding source検査PASSと担当報告。observer schema／session／handoff／station attachはversion `1`、compatibility revision `v1.1`は別管理。Actions workflow／runはなく、wheel／sdistはsource commitとexact digestから再生成・照合する。live未実施
- frozen runtime policy / schema: protocol `22.0.0`、artifact `2200.0.0b5`、Minecraft `1.21.11`。plugin command FIFO `1024`、response queue `64` frames、event ring `256` events／`262144` bytes、event poll default／server max `64`／`64`、entity handles `256`、particle count `1000`、work request／session／player／global `4096`／`4096`／`8192`／`32768`、compact poll response最大`61440` bytes。Python send queue `1024`、request／flush timeout `60.0`秒（timeout時は完了不明、自動retryなし、connection回収）、TRACE delay既定`0.25`秒／範囲`0.0`〜`2.0`秒。observer schema、observer session、Scratch handoff、station attachはversion `1`、compatibility set revisionは`v1.1`、observer session frame最大`65536` bytes
- environment preparation correction: プロジェクトオーナーのいう「通常dev環境」は、ケータリング型でないだけでなく、**Docker／Composeを使わずホームサーバー（`home-host-2`）上でPaper／McRemoteを直接動かすhost-native環境**を指す。knowledge coordinatorがこれを「非ケータリングの永続環境」とだけ解釈して`home-server@5`／`compose@5`を採用したのは誤り。knowledge commit `e854039646a84468b506c2c286bc5314f1e10d20`によるapply／doctor許可を撤回する
- invalidated Docker path: Stack PR `#26`／`#27`／`#28`とその検証事実は履歴として保持するが、本gateの通常dev targetとして`home-server@5`、container runtimeを内包する`mcremote-paper@7`、OCI index `sha256:7f69fd6688e03495c8a8f5a46e8a8e82001b4465f4b55bdcd024c02c3624d8c8`、container内Java `jdk-21.0.11+10`、adapter `compose@5`を採用しない。order semantic `97561f1b49aa8f4d96e59ab24647ff2fb3ef93dab670178c33dc9867f13c708d`、lock identity `sha256:b5840f077f0a6fd55221be1795751cad809da00a033933df3f461ca2292ab705`、render manifest `6cd55bd02b6ed52958e6ee163ab852ec809bc0c01541f571e3943e75d3778ea6`はこのgateへapplyしてはならない
- reusable preparation: Stackのreview済みartifact import、標準port `25565`／`25575`、未知listener時のreadiness取消、Paper `1.21.11-132`（54,846,016 bytes／SHA-256 `5ffef465eeeb5f2a3c23a24419d97c51afd7dbb4923ff42df9a3f58bba1ccfba`）の照合結果は再利用できる。旧McRemote JAR `17cdc457…aeb6`のCAS照合結果は履歴として保持するが、現行live setのartifact identityには使わない
- environment staging result: 訂正前のknowledge commit `e854039646a84468b506c2c286bc5314f1e10d20`による許可とHOLD訂正が入れ違いになり、Stackは旧lockを用いたDocker applyを一回実行した。containerはrunning／healthy、Paper／McRemoteのread-only mountと3 managed volumes、OCI index、order／lock／compose／render bindingは旧setと一致したが、doctorはgit-build artifactの`output_filename`／`output_sha256`を共通mount検査が`filename`／`sha256`として読まない実装差分により`doctor_artifact_mount_mismatch`でFAILした。order／lock／generated file／containerの手修正、再apply、rollback、製品live試験は行っていない。この失敗をhost-native gateの失敗へ読み替えず、Docker経路の観測として保持する。runtimeは停止確認が返るまで**意図しない稼働中state**であり、通常dev readinessを取り下げる
- host-native first smoke: knowledge `b84e9901265f15bb9e0ccd30a74be5a2bdc130c5`により旧Docker runtimeを停止し、OpenJDK `21.0.11+10`、Paper `1.21.11-132`、McRemote `1.21.11-2200.0.0b5`をsystemdで直接起動した。Docker container非稼働、port解放後のhost-native listen、workstation LAN到達、tokenなしhelloの`auth_required`はPASS。一方、root所有のMcRemote configへpluginがb5既定値を追記できず`Permission denied`、credential snapshot／revocation authorityが未初期化でcredential domainが`UNHEALTHY`となったためPARTIAL PASSで停止した。serviceはinactive、port `25565`／`25575`解放、追加手修正・再起動・製品試験なし。これはcandidate不具合でなくbootstrap手順の不足として扱う
- host-native readiness: knowledge `5400560225f4a329fd0f40725c91b5465187d872`の最小差分後、systemd serviceは専用accountでactive、boot enableはdisabled、credential domainは`HEALTHY`、通常再起動後も同一domainで`HEALTHY`。Paper／McRemote exact SHA、port `25565`／`25575`、workstation LAN到達、tokenなしprotocol 22 helloの`auth_required`、Docker container 0、未知service／listenerなしを確認。Stack PR `#29` head `8e65214d766a4448b3fc294b794262f294c2679a`は454 tests／ruff／ShellCheck／self-test PASS、backstage PR `#5` head `c91d82d816cb17569ddda621adbab9d8f8df117b`はTOML parse／secret scan／diff check PASS。両PRはdraft／clean。製品API liveは未実施
- Stack PR review: `#29`のhost-native経路とreadiness barrierは採用可能。ただし`data/plugins`がservice account所有のため、root所有JAR fileでもserviceがunlink／置換でき、「immutable入力」という主張と不一致。merge前に`data/plugins`をroot所有・非書込み、`data/plugins/McRemote`だけをservice所有とし、service accountがJARを置換できずconfig／credential backendへ書ける回帰testを追加する。この修正は製品artifact／runtime policyを変えないためlive試験と並行する。backstage `#5`はdraft解除・merge可
- McRemote first segment attempt: candidate `b5_live_auto.py`はtoken／credential入力とpairingを持たず、tokenなしhelloの成功を要求したため、exact auth-enforced serverの正しい`auth_required`でrunner preflight FAIL。plugin不具合とAPI FAILは未観測で、world／entity／origin変更なし。source／JAR／server readinessは維持する。これは製品candidateを失効させず、test harness identityだけを追加固定するgapとする
- runbook cleanup: Stack PR `#28`はreview済みhead `94b86b6f4142024a443a77bcfb1a39c8107aace9`／merge commit `e3d73a5dae44086bde60f36d0fdfa3630d330b28`でmerge済み。通常dev guideとrunbook testの2 filesだけを変更し、orderの既存acknowledgement 2 scalarを具体的なgate理由で設定して再validate、`resolve --allow-unverified`、plan review、後続`apply --allow-unverified`へ進むdurable＋one-shot境界、成功条件、`acknowledgement_reason_required`／`unverified_not_acknowledged`からの戻り先を記載する。lock／generated treeの手編集は禁止したまま。coordinatorはremote main一致、reviewed head包含、外部check 0件をGitHub APIで確認した。担当報告は452 tests／ruff／diff check PASSで、preset／order／lock／artifact／render identity不変。CLI変更なし
- input correction: McRemote作業票のknowledge SHA `f50ebb17…`は存在せず、実在する`f50ebb13f00facfc2e73163a24f002f4c8b77d43`を参照。契約差分なし
- target deployment / profile / lock: logical deploymentは`dev-integration`、physical hostはbackstage管理下のホームサーバー`home-host-2`、channel=`dev`、exposure=`lan-only`、purpose=`integration`、標準server portはJava `25565`／McRemote `25575`。現在の試験runtimeはhost上のPaper server directoryを`run.sh`から名前付きScreen session `Minecraft server`で起動するhost-native／non-Docker環境。旧systemd版はinactive。Paper `1.21.11-132`、McRemote `2200.0.0b5`／JAR `f7ddbcb5…36547`、credential domain `HEALTHY`、両port LISTEN、tokenなしhello `auth_required`を確認済み。起動方式とrunbookの恒久改訂は進行中の製品試験へ混ぜず、試験完了後の別作業とする
- authorized next action:
  - unified test ID: `2026-08-22-b5-dimension-key-live`
  - Python segment: **PASS**。exact source `64b0f8831fa33e74f1b70b9102b3f29ec99b8e14`／wheel `370f0fef…f195`、McRemote `bbbb5360…`／JAR `f7ddbcb5…36547`、WireScope `407031d5…a6964`／manifest `15d0c6b9…5bda`を使用した。authenticated hello、shorthandからcanonical DimensionKeyへの正準化、両build setterのcontext一体同期、pose、旧alias不採用、一般namespaceのserver到達、旧method拒否、失敗時context不変、3 event DTO、same-context guard、意図的mismatch拒否、WireScope schema version `1`／`world` fieldなし、real-browser終了表示をすべてPASS。初期2停止は試験runnerの過剰なerror値固定とbrowserによるsnapshot slot消費で、candidate不具合ではない。最終runは正常終了しcandidate／server／config変更なし
  - Scratch segment: **PASS**。exact source `1a11c46b…`／CI run `32574020556`を使い、標準3dimension menuと完全修飾result、一般namespaceのserver到達、旧`world` alias不在、pose、3 event hat、canonical dimension／origin／loss `0`、real-browser WireScopeのbuild／player／event frameと`world` field不在を確認した。poll frameが履歴を押し流すため操作ごとの分割runを使い、初回旧localhost cacheはfresh originで同じexact artifactを表示して解消。candidate／server設定変更なし、接続終了、worktree clean
  - 省略範囲: standalone McRemote live runner、spawn capacity、block／height、FIFO／1041 notification burst、poll上限、全回帰、試験前後の重複readiness、world／entity清掃を実施しない。既存PASSを再利用する
  - 進行規則: Python PASS後にScratchを開始する。失敗時はそのsegmentで停止し、exact request／response、reason、candidate identityだけを返す。candidate、server配置、config、起動方式を試験中に変更しない。人間操作の取り直しは失敗した操作だけに限定する
  - 返却: 各担当は実行したexact artifact、PASS／FAIL一覧、WireScope確認、未実施範囲、candidate変更なし、接続終了だけを一枚で返す。component GREENや横断GREENを主張しない
- live-auto / live-human: **完了**。追加試験を行わない。正式recordは`14-evidence/records/2026-08-22-b5-dimension-key-live_ja.md`
- gate result: **GREEN — b5横断技術gate完了／prerelease identity確認完了**。exact compatibility setと技術evidenceを変更せず、3 componentのprereleaseを受理する
- release authorization: プロジェクトオーナーの明示承認（2026-08-23）。McRemoteは`v1.21.11-2200.0.0b5`を`bbbb53602a9c375e2ead3ee4c22174d5cf424f55`へ、Pythonは`v2200.0.0b5`を`64b0f8831fa33e74f1b70b9102b3f29ec99b8e14`へ、Scratchは`v2200.0.0b5`を`1a11c46bac5696afd3f494caac56ae682ed00fb0`へ固定する。各releaseはprerelease ON、draft OFF、Latest非対象とし、作成後にtag target、公開状態、asset／release notesのSHA-256をGitHub APIで確認する。McRemote JAR assetを登録し、Pythonはwheel／sdistのSHA-256をrelease notesへ記載する。ScratchはCI／Bridge artifact ID、common WireScope ZIP／manifest SHAをrelease notesへ記載する
- release identity verification: McRemote [v1.21.11-2200.0.0b5](https://github.com/Naohiro2g/McRemote/releases/tag/v1.21.11-2200.0.0b5)はtag target `bbbb53602a9c375e2ead3ee4c22174d5cf424f55`、prerelease ON、draft OFF、Latest非対象、JAR asset 195,998 bytes／SHA-256 `f7ddbcb5…36547`、release notes SHA-256 `64f2cedd…a364`。Python [v2200.0.0b5](https://github.com/Naohiro2g/minecraft-remote-api/releases/tag/v2200.0.0b5)はtag target `64b0f8831fa33e74f1b70b9102b3f29ec99b8e14`、prerelease ON、draft OFF、Latest非対象、assetsなし、release notes SHA-256 `c0375238…0dc04`。Scratch [v2200.0.0b5](https://github.com/Naohiro2g/scratch-editor/releases/tag/v2200.0.0b5)はtag target `1a11c46bac5696afd3f494caac56ae682ed00fb0`、prerelease ON、draft OFF、Latest非対象、追加assetsなし、CI／Bridge digestとWireScope SHAをnotesへ記載。各repo worktreeはclean
- authorized next action: release identity確認をもってb5 gateをcloseする。PyPI／TestPyPI、registry publish、public deploy、runtime／server変更、b6実装はこのrelease確認に含めない。次の作業は別途b5後・b6前の保存entry gateまたはb6 scopeとして起票する
- non-claim: Scratch browser保存、b6 API、full load／soak、capacity本較正、custom loaded dimension成功、他Minecraft／Paper版、通常dev環境runbook改訂、public deploymentを主張しない

### b5から次gateへ持ち越す方法論

- decision: `2026-08-23-01`
- b5の厳密検証でspawn、runner認証、DimensionKeyの問題を発見したことは有効であり、試験項目を破棄しない。
- 手戻りの主因は、仕様形成中の毎回へrelease gate級の固定・環境準備・全検証を適用したこと、通常dev harnessとdeploymentを混同したこと、identityを手転記したことである。
- b6／b7／b8はTier 0〜2でcontractを収束させ、RC候補までTier 4を自動要求しない。capacity／soakは実装が載った後の実測へ送る。
- 次の横断候補前に、常設通常dev integration harnessの正準入口とmachine-readable gate manifestをStack／backstage／knowledgeの各責務に従って実装する。
- b5で実施した非影響PASSは、change coneと元identity／non-claimを明示できる場合に限り後続gateへ再利用できる。

### b5 public deploy 実施記録（2026-08-23）

- decision: `2026-08-23-02`
- 対象 repo: mc-remote-stack（協調: McRemote, scratch-editor）
- gate coordinator: mc-remote-stackリポのClaude Codeセッション。human release ownerが本セッション内でpublic VPS beta（official-public-beta）へのb5 exact set適用を明示承認し、実行した
- 実施日: 2026-08-23
- exact compatibility set遷移: `public-web-paper@5` → `@6`（Stack PR `#31`、merge `7cb0168`）→ `@7`（Stack PR `#34`、merge `a58f51d`）。`vps-server@8` → `@12`
- 適用先: official-public-beta VPS、lock `sha256:a2e93aaf512f895f4ec5482c443a0763ff534f68f611dd14ca58fb49b109bb92`
- credential永続化regressionと修正: 適用直後にMcRemote CredentialServiceが`UNHEALTHY`（`Unknown persisted credential type: session`）となった。`git log --graph`によるcommit history比較で、b5ブランチが共有merge-base `9df8c46`（b4 player pose commits）から、b4側のsession token永続化fix `3496db9`（2026-08-18、`2026-08-02-08`実装、evidence `2026-08-18-b4-session-persistence-home-alpha`）がマージされる前に分岐しており、b5独自のprotocol-22作業が同じcredential関連fileを独立に書き換えたためこの修正が欠落していたと判明した。意図的なb5設計変更ではなく並行branch間の取り込み漏れであり、既存on-disk `session`型recordを読込み時に黙って捨てるだけのshimは、b4で実機検証済みの同一runtime再起動を跨ぐsession token継続を回復しない不完全な対応として不採用とし、`3496db9`をcherry-pickして修正した。McRemote `v1.21.11-2200.0.1b5`（JAR SHA-256 `b20705899e3d352a434640b2b075845e34bdac9bda895ee8d1a768f8d232a844`、独立clean checkout 2件でbyte-for-byte一致、`./gradlew check` 101 tests PASS、うちsession-persistence関連6 tests）としてVPSへ適用した
- live doctor結果: 適用時点で接続player 0名・直近backup 1時間以内の低リスクな窓だった。修正適用後、`docker logs`で`[McRemote] Credential domain health: HEALTHY (healthy)`を確認。`mcrctl doctor`はruntime／lock／network／protocol／homepage／scratch-runtime／wirescope全項目OKで、`compatibility=unverified`のみ既存の想定内WARN（regressionと無関係）
- non-claim: capacity較正、soak、rollback実演、公開向け人間参加試験は本follow-upで実施しない
- 関連決定: `2026-08-23-02`（「b5後・b6前の保存entry gate」という語は時期を示すだけで、public deploy可否を制限する条件ではないという訂正を含む）

## 2026-08-07 Scratch editor `2100.0.0b3`

- candidate: `release/b3@3f1a10a366bfbe76e32b5a31c54da19eddd56e56`
- contract: `13-scratch-client/scratch-roadmap_ja.md` §2.3 / knowledge `3dfbf57c07f2b7985c65edc5564b879f9e67e122`
- CI: run `31145335984`、exact candidate、全job success
- evidence: `14-evidence/records/2026-08-07-scratch-b3-release-gate_ja.md`
- status: **GREEN — tag `v2100.0.0b3`とGitHub prerelease作成を承認**
- release条件: tag targetは上記candidate完全SHA、prerelease ON、draft OFF、Latest非対象
- rollback: `v2100.0.0b2@e19247069d1ae55037c0e9ffc52ea88cde612ac3`
- scope boundary: hosted surface更新は含めない。更新時はdeploy smoke / rollback / re-deployを別gateで確認する
- deferred: catalog picker / WireScope miniはb4、独立WireScopeは`2026-08-06-03`どおりb3非blocker

## 2026-08-07 b3 横断 milestone close

- status: **CLOSED — b3の横断スコープを完了扱いとし、b4の利用者向け機能へ進む**
- decision: `2026-08-07-01`
- Python API: `v2100.0.0b3@af2d11d66a16e3085f569241406a703a1c28c348`、GitHub prerelease、PyPI非公開。正式live根拠は `14-evidence/records/2026-08-06-b3-python-catalog-projection-live-human_ja.md`
- McRemote: `v1.21.11-2100.0.0b3@a3dab998b710f65f42f95058a68ec51d419b097c`、GitHub prerelease、JAR SHA-256 `aeb190705bd9957ce73557dc1be0fe15efe7250ba9bc688945e6f537e00ef78e`
- Scratch editor: `v2100.0.0b3@3f1a10a366bfbe76e32b5a31c54da19eddd56e56`、GitHub prerelease。正式gate根拠は `14-evidence/records/2026-08-07-scratch-b3-release-gate_ja.md`
- scope: versioning §10.11.1項14のcatalog一式、Scratch現行roadmapのb3 scope、各componentのb3 prereleaseを区切りとして閉じる。component番号の永久同期やstable releaseを主張しない
- deferred: long-lived credentialの公開gate、checkpoint＋doctor、end-to-end snapshot rollback、reset／災害復旧は閉じたまま後続へ送る。既定は`session`のまま
- non-claim: Stackの一般profile公開、hosted surface更新、long-lived公開可否をGREENとする記録ではない。これらをb3完了へ遡及混入しない

## 2026-08-16 Python `2100.0.0b4` candidate

- candidate: `codex/b4-player-pose@4d510442db58a94f8b249ddcd9d959381f97276c`
- contract: DECISIONS `2026-08-16-08` / knowledge `b747fa2b3b6c278f1a8e920ba8e02b45e2cf2b47`
- evidence: `14-evidence/records/2026-08-16-b4-python-pose-wirescope-live-human_ja.md`
- status: **PYTHON CANDIDATE PASS — tag／releaseは未承認**
- verified: candidate wheel、main stream 1件、`player.getPose`／`player.setPose`、origin相対座標、automatic browser launch、WireScope UI、終了表示、distribution／license gate
- compatibility set: McRemote `9df8c46d600ff9605dc1822b304715de713e6767` / JAR SHA-256 `ab3b87c38b6876ec4ba26112eff35d7cb016395a1dae1661578fd3690e1dbc46` / WireScope source `56011f71291f47ced69cc4e3c377734f501b6081` / ZIP SHA-256 `1a56617c78c283332f1afe3bdd3797ab37f0cdc3455c86c73c926c751721657f`
- rollback candidate: `v2100.0.0b3@af2d11d66a16e3085f569241406a703a1c28c348`。rollback実操作と再復帰は未実施
- remaining: Scratch／Pythonの順次横断real-browser E2E、home alpha、plugin artifactを含むexact compatibility set最終批准、release後identity確認
- non-claim: 本項だけでPython tag、GitHub prerelease、横断b4 milestoneをGREENにしない

## 2026-08-16 Scratch editor `2100.0.0b4` candidate

- candidate: `release/b4@56011f71291f47ced69cc4e3c377734f501b6081`
- contract: DECISIONS `2026-08-16-08` / knowledge `b747fa2b3b6c278f1a8e920ba8e02b45e2cf2b47`
- CI: run `31934776981`、exact candidate、全job success
- evidence: `14-evidence/records/2026-08-16-scratch-b4-release-gate_ja.md`
- status: **SCRATCH COMPONENT GREEN — tag／releaseは横断gateまで保留**
- verified: Catalog Picker、`player.getPose`／`player.setPose`、Scratch main stream 1件のMessageChannel観察、pose対応common app、clean artifact reproduction、unit／build／CI
- common artifact: ZIP SHA-256 `1a56617c78c283332f1afe3bdd3797ab37f0cdc3455c86c73c926c751721657f` / manifest SHA-256 `f3ec11496b595bbca4ba27a6e938a1149336eb5a2da55e742d60e1681cf4d154`。Python candidateと一致
- rollback target: `v2100.0.0b3@3f1a10a366bfbe76e32b5a31c54da19eddd56e56`。hosted deploy／rollback実操作／再復帰は未実施
- remaining: Scratch／Pythonの順次横断real-browser E2E、plugin artifactを含むexact compatibility set、home alpha、release後identity確認
- non-claim: 本項からPython／plugin／home alphaまたは横断b4 milestoneのGREENを推測しない

## 2026-08-17 b4 home-alpha pre-auth transport correction（初回観測）

- decision: `2026-08-17-01`
- evidence: `14-evidence/records/2026-08-17-b4-home-alpha-integration_ja.md`
- status: **PARTIAL PASS — one-shot認証とb4機能統合はPASS、session token再起動耐性はBLOCKED**
- observed gap: McRemote `dab6908494290c894d8efbe6828707e544860fa1`のclose-after-flushでもresponseからEOF観測まで約41msあり、Bridge経由で`auth_required`直後0msに送る`auth.pairBegin`はtimeoutする。100ms待機では成功し、直接新TCPでは成功したが、固定delayは解決として採用しない
- McRemote input: close-after-flush JAR SHA-256 `f902ed360ac1674143d8e79a49c8e109968f2c38dc36656c91a50dec89082aa8`。plugin追加変更は要求しない
- implemented set: Scratch／Bridge one-shot `8b69ecefc9771a47e2eac8bea242cf96c09d36f3`、pagehide lifecycle `1d2f18785d260564ad4bc30a26a45ef33fc813d6`、McRemote JARは上記digest、Python `4d510442db58a94f8b249ddcd9d959381f97276c`、WireScope ZIP `1a56617c78c283332f1afe3bdd3797ab37f0cdc3455c86c73c926c751721657f`
- passed: `auth_required`直後0msのone-shot pairing、Scratch／Python／WireScope実機一巡、canonical b3 rollback、corrected b4再適用
- failed: 同一corrected b4 runtimeの通常再起動後、期限内session tokenが`auth_required`。candidateはsession tokenをin-memoryだけに保持し、`2026-08-02-08`のhash-only snapshot永続化と不一致
- doctor gap: credential domain `UNINITIALIZED`を現行doctorが検出せずPASS。`2026-08-06-02`のcredential checkpoint／doctor contractは未実装
- next gate: McRemote session record永続化→artifact再固定→同一b4再起動とb3→b4再適用でtoken再利用→Stack credential health／doctor再照合
- non-claim: 既存のPython candidate PASS／Scratch component GREENと今回の機能統合PASSは維持するが、認証再起動FAILが閉じるまでhome-alpha認証、credential継続を含むrollback／再適用、b4 releaseはGREENにしない。100ms待機、EOF依存、自動再送をfixture／runbookへ残さない
- resolution: このFAIL観測は削除しない。後続McRemote `3496db9293baa6e1d4f79439cacbd239ba15e2b7`と`2026-08-18-b4-session-persistence-home-alpha`でsame-b4再起動とb4再適用後のtoken再利用がPASSし、最終判定は下記2026-08-18項へ移った

## 2026-08-18 b4 横断 release gate

- decision: `2026-08-16-08`／`2026-08-17-01`／`2026-08-18-01`
- status: **CLOSED — exact b4 compatibility setのGitHub prerelease公開identityを確認し、b4 milestoneを閉じる**
- protected value: Scratch／Pythonの保存済み建築コード。復旧基準はコード保存→空環境再構築→再pairing→必要なら書き換え→再実行
- exact set:
  - McRemote `3496db9293baa6e1d4f79439cacbd239ba15e2b7`／JAR SHA-256 `331633ef15a729658496e89fe49cb8a5eb5ebcb2ec86937b7e5313528d7ec997`
  - Python `4d510442db58a94f8b249ddcd9d959381f97276c`／wheel SHA-256 `eeed6261972987946b5e22dd8ff8d3533a758c7db57472d1d82766fbf964e7d0`
  - Scratch／Bridge one-shot `8b69ecefc9771a47e2eac8bea242cf96c09d36f3`、pagehide lifecycle `1d2f18785d260564ad4bc30a26a45ef33fc813d6`
  - WireScope ZIP SHA-256 `1a56617c78c283332f1afe3bdd3797ab37f0cdc3455c86c73c926c751721657f`／manifest SHA-256 `f3ec11496b595bbca4ba27a6e938a1149336eb5a2da55e742d60e1681cf4d154`
  - Stack `780d99291d669fd1ec98c513245bf6fdbac36271`／runtime implementation `cd3ff18e31534f394e5fc7ad63af1f164ce54f15`／`home-server@3`／`mcremote-paper@6`
- passed:
  - Scratch Catalog Picker、player pose、Scratch／Python main stream各1件の共通WireScope観察
  - pre-auth one-shot pairing、固定delay・自動再送なし
  - same-b4通常再起動後の期限内session token認証
  - b4再適用後の同token認証。b3はb4 session recordを読めずfail closedし、snapshotを破損しなかった
  - 新規world／credential環境でのScratch `.sb3`／Python source再pairing・再実行とserver側独立照合
  - b3 artifact rollback／b4再適用、exact artifact／lock照合
- formal evidence:
  - `2026-08-16-scratch-b4-release-gate`
  - `2026-08-16-b4-python-pose-wirescope-live-human`
  - `2026-08-17-b4-home-alpha-integration`（初回PASS／FAILを保持）
  - `2026-08-18-b4-session-persistence-home-alpha`
  - `2026-08-18-b4-code-preservation-recovery-live-human`
- release identities（GitHub API再確認済み）:
  - [Python `v2100.0.0b4`](https://github.com/Naohiro2g/minecraft-remote-api/releases/tag/v2100.0.0b4): target=`4d510442db58a94f8b249ddcd9d959381f97276c`、prerelease=true、draft=false、Latest非対象。binary assetなし、release notesにwheel／sdist digestを固定、PyPI／TestPyPI非公開
  - [Scratch `v2100.0.0b4`](https://github.com/Naohiro2g/scratch-editor/releases/tag/v2100.0.0b4): target=`1d2f18785d260564ad4bc30a26a45ef33fc813d6`、release ID `372338711`、prerelease=true、draft=false、Latest非対象、追加assetなし
  - [McRemote `v1.21.11-2100.0.0b4`](https://github.com/Naohiro2g/McRemote/releases/tag/v1.21.11-2100.0.0b4): annotated tag target=`3496db9293baa6e1d4f79439cacbd239ba15e2b7`、prerelease=true、draft=false、Latest非対象。asset=`mc-remote-1.21.11-2100.0.0b4.jar`／140,712 bytes／SHA-256 `331633ef15a729658496e89fe49cb8a5eb5ebcb2ec86937b7e5313528d7ec997`
- non-blocking observations:
  - b3はb4の`session` recordを理解せず`unknown_persisted_credential_type_session`となる。b3をcredential継続付きdowngrade runtimeとしては承認しない
  - checkpoint projectionは未実装で、Stack doctorは`doctor_credential_health_unsupported`としてfail closedする。これをdoctor PASSへ読み替えない
- deferred / non-claim: long-lived credential一般公開、checkpoint／doctor完成、world backup／restore、一般Stack profile、public hosted deployment、PyPI／Modrinth公開、substream／multi-stream、b5以降。これらをb4 GREENから推測しない
