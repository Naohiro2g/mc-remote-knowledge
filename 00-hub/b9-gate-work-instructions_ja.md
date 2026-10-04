# b9横断release gate 着手依頼

> b9横断release gate（`00-hub/release-gate-notes_ja.md`の2026-10-04の節）で、確認票の返却を受けて出す着手依頼です。
> 参照するknowledge commitは、この依頼が入ったmainのcommitです。各担当は、自分の節と「共通」を読んでください。
> 移管は`2026-10-05-01`（共通TypeScript tooling monorepo）と`2026-10-05-02`（移管先`minecraft-remote-tooling`）、
> Pythonのmatureは`2026-10-05-03`によります。

## 共通

- b9はAPIを変えない。protocol `23.2.0`のまま、artifact `2320.0.0b9`（`2026-09-30-03`）
- 依存順:
  1. Scratchが今のownerのまま、契約2件のcaseを足したshared fixtureを出す（human owner 2026-10-04）
  2. McRemote、Pythonが取り込む。並行して、Scratchが`minecraft-remote-tooling`へ移す
  3. 各consumerが取得元を`minecraft-remote-tooling`へ切り替える
  4. exact setの凍結 → devの通常環境で実機試験 → release
- 契約2件の修正（McRemoteの`chat.post`、Python／Scratch／WireScopeの知らないevent type）は、fixtureを待たずに今すぐ始める
- 日程:
  - **10/6の終わりが確認点。** shared fixtureが出ていて、`minecraft-remote-tooling`にsourceが入っているかを見る
  - 10/7に取得元の切り替え、10/8に凍結、10/9に実機試験、10/10にrelease
  - **10/7の終わりに移管が凍結に間に合わない見込みなら、** b9は移管なし（freeze、契約2件、PyPI）で出すかをhuman ownerと相談する。
    そのため、契約2件の修正とfixtureの取り込みは、移管と別のcommitにしておく
- 「同じ」の判定: fixture 12件はbyte一致。配布物は中身（ZIPの中のassetのbytes）を比べ、source URLやcommitを書き込むdetached
  manifestとOCIのmetadataは一致の対象から外す。移管だけの差分と機能の差分を分けて比べる（gateの節の「移管の判断」）
- 返却: 確認票の形式で、変わったところだけを追記として返す（branch／commit、artifactのbytes／SHA-256、実行したtestと結果、
  未検証の境界）。`knowledge contract commit`には実際に読んだSHAを書く
- しないこと: 他repoの編集、shared環境の変更、人間参加の試験、tag／releaseの公開。これらは凍結の後に別の票で示す

## Scratch editor（WireScope）— 移管の実施者

1. **契約2件の対応とshared fixture（最優先、10/6の確認点）**
   - Scratch VM: 知らないevent typeを省略する。共通のfieldと順序は検査し、`through_sequence`とloss counterはそのまま使う。
     知らないeventだけのbatchでもcursorを進める。既知eventの不正は今までどおり拒否する
   - WireScope: 知らないevent typeを共通のfieldだけのsummaryとして表示し、snapshotを拒否しない。`chat.post`のresultは`null`だけを
     受ける
   - protocol mirrorに`ChatPostResult = null`を足す
   - 契約2件のcaseを足したshared fixtureを出す（別紙の案: `chat.post`の`null`成功と非`null`の拒否、既知と知らないeventの混在、
     知らないeventだけのbatch、最後が知らないeventで`through_sequence`が進むbatch、loss counterが0でない場合、既知eventの
     不正・順序・cursorの境界の拒否）。公開b8の12件は変えず、新しいfileにする。出したら、commit、file名、bytes、SHA-256、
     case数を返す
2. **WireScopeの列幅**（`agent/b8-compatibility@01cdb0b`）をdevelopへ入れる
3. **`minecraft-remote-tooling`の用意（外部の操作。human ownerの依頼）**
   - `Naohiro2g/minecraft-remote-protocol`の名前を`minecraft-remote-tooling`へ変え、parkの表示を外す
   - Actions、権限、branch保護を設定する。権限が足りずにできない操作があれば、その操作だけをhuman ownerへ返す
4. **移す**
   - 起点は公開b8のScratch source `691576f`ではなく、1と2を入れた後のdevelop。park中のheadは古いので使わない
   - 移すもの: Protocol（型、定数、owner test、fixture 7件と1の追加fixture）、WireScope（app、library、adapter、fixture 4件、artifact
     generator）、Bridge（transport、config、test、fixture 1件。今の機能のまま）
   - `minecraft-remote-tooling`で独立のlock、3 packageのbuildとtest、WireScopeのZIPとdetached manifest、Bridge OCIを作れるようにする
   - fixture 12件がbyte一致することを確かめる
5. **Scratchをconsumerにする**
   - fixtureを`minecraft-remote-tooling`の固定commitから取り込み、VM／GUIのtestがそれを読むようにする
   - release workflowが、`minecraft-remote-tooling`のWireScope生成物とBridge OCIを集めるようにする
   - root workspace、lock、CI、path filter、README／AGENTSの所有の説明を直し、旧ownerのsourceを撤去する
6. candidateのartifactを作り、identityを返す（`minecraft-remote-tooling`のcommit、WireScope ZIPとmanifest、Bridge OCI、Scratchの
   commitとartifact）。PythonはこのWireScopeから同梱物を作り直す
7. 非blocker: pickerのalias検索。何をaliasとして登録するか（読みや呼び方）はhuman ownerが選ぶ。b9に間に合わなくてもよい

## McRemote

1. **今すぐ:** id付き`chat.post`の成功resultを`null`にする（`MiscCommands.handleChatPost`）。production handler経由のtestで、
   id付き成功の`result: null`、notificationの無応答、今までのerrorを確かめる
2. **今すぐ:** JARの権限bitを固定する（`tasks.jar`に`filePermissions { unix("0644") }`と`dirPermissions { unix("0755") }`）。
   umask 002と022の手元build、CIのcandidateで、全entryのmode、bytes、JAR全体のSHA-256を比べる
3. versionを`2320.0.0b9`にする
4. **Scratchのfixtureが出たら:** bytesをそのまま取り込み、digestをtestで固定して、consumer testを通す
5. **`minecraft-remote-tooling`にsourceが入ったら:** 共有fixture 4件の取得元の記録（provenanceのコメント）を新しいownerの
   repo／commit／pathへ変え、bytesがb8と同じことを確かめる。scratch-editorを書いているコメント5箇所も直す
6. candidateを更新したら、branch／commitと1.21.11向けJARのbytes／SHA-256を返す
7. 非blocker: READMEの残り（capabilityにb7／b8の機能、API一覧への導線、更新／rollbackの案内）

## Python client

1. **今すぐ:** 知らないevent typeを省略する（`decode_event()`／`pollEvents()`）。`EventBatch.events`の型はそのまま、知らない
   typeだけを除き、`through_sequence`とloss counterはそのまま使ってcursorを進める。observerは知らないtypeだけを理由に
   frameを拒否しない。既知eventの不正payloadは今までどおり拒否する
2. **今すぐ:** `chat.post`の`null`のconsumer testと、API一覧の戻り値の説明を揃える
3. **今すぐ:** PyPI.org用のpublish jobとrunbookを足す（`2026-10-05-03`）。既存の成果物検証を共有し、environment `pypi`、
   Trusted Publisher（OIDC）で、正式段階の固定triggerから出す。jobを入れたcommitをb9のcandidateに含める。TestPyPIへの
   予行を続けるかは提案として返す
4. versionを`2320.0.0b9`にする
5. **Scratchのfixtureが出たら:** 取り込み、consumer testを通す
6. **`minecraft-remote-tooling`の生成物が出たら:** 共有fixture 6件の取得元の記録（sidecarとtestのsource pin）と、同梱WireScopeの
   取得元（manifestのsource、`_wirescope_artifact.py`、`pyproject.toml`のURL、`check_wirescope_wheel.py`、tests、NOTICE）を
   新しいownerへ変える
7. candidateを更新したら、branch／commitとCI成果物（wheel／sdist）のbytes／SHA-256、同梱WireScopeのsourceを返す
8. 非blocker: `starter/README_ja.md`の古い記述、update／rollbackの案内、API一覧のドラフトのレビュー

## Java client（gateの条件にしない）

参加しない（`2026-09-30-04`）。契約2件への追従は、Javaの判断でcommitしてよい。fixtureの取得元は、初回stableの後の追従で
`minecraft-remote-tooling`へ変える。
