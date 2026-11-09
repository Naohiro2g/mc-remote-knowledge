# Scratch 2321.1.0 再作成候補の返却

- knowledge contract path：`00-hub/release-gate-notes_ja.md`の2321.1 gate「Scratchのブロック一覧の返却」の後のhuman owner判断。
- knowledge contract commit（実読）：`087ff8474e057a127c5c0da99c8141d8800ef264`。remote mainも同SHA。最新runtimeと該当判断を実読。
- 依頼票：`REQUEST_ja.md`。
- 実行した操作：指定のcandidate workflowのdispatchと、生成物・ログの取得／比較。source／workflow／`mc-remote-images.yml`は変更していない。tag／Release／共有環境は操作していない。
- 返却先：knowledge gate coordinator。今回のidentityをScratchの`2321.1-set-2`へ採用するための事実の返却で、横断gateの合否判定ではない。

## run／Runner Image

- [run 42350684690](https://github.com/Naohiro2g/scratch-editor/actions/runs/42350684690)：**success**。
- `head_sha`：`57fb7691bb5d9a5895785b200ae78734240ebfa6`、`head_branch: develop`。
- dispatch直前にremote developが指定SHAと一致することを確認した。そのまま`ref=develop`でdispatchし、runのhead_shaも一致。追加branchは作っていない。
- 開始：`2026-11-07T07:17:52Z`。job終了：`2026-11-07T07:27:51Z`。この差は**599秒（9分59秒）**。
- job logのRunner Image：**ubuntu-24.04 / 20261101.360.1**。OS表示はUbuntu 24.04.5 LTS。set-1と同じimage名・版で、一度だけ実行した。
- command：`gh api repos/Naohiro2g/scratch-editor/actions/workflows/mc-remote-candidate.yml/dispatches -X POST -f ref=develop`。

## artifact

- ID：`13565862576`。
- 名前：`scratch-candidate-57fb7691bb5d9a5895785b200ae78734240ebfa6`。
- archive：1,373,409,925 bytes、digest **`sha256:47a4f4601dbec0c2e8fc58d9359f69290fda4c1f4f2f58bb387e73590a172050`**。
- 期限：`2027-02-05T07:17:53Z`、取得時`expired: false`。
- [取得先](https://github.com/Naohiro2g/scratch-editor/actions/runs/42350684690/artifacts/13565862576)。
- set-1／set-2を両方取得し、providerのarchive digest、ZIP entryのCRC、全13 fileのbytes／SHA-256を実測して照合した。各candidate manifestのfile identityとも一致。

## 全fileの実測identity（set-2）

| file | bytes | SHA-256 |
| --- | ---: | --- |
| `bridge.oci.tar` | 114,626,048 | `3982876466fb860dca250438d73e18e441a2a85d67d9f149f537a7a8d1a1c44c` |
| `candidate-manifest.json` | 2,664 | `19aec7258f726f11ce497783b0e3c9b97f39be4fc4d8ccd7f25cfdc084061d47` |
| `contracts.tar.gz` | 1,908 | `48948ba47d55409f02a8ff8e0d44021b07859e11ffa5ca0f8598e6ef06082390` |
| `mc-remote-scratch-LAN-2321.1.0-linux-x64.artifact.json` | 336 | `49d15735c35e408bbaa7fc81d09ed8325bb9a7b70ad10f751b6ee5c857b59c3f` |
| `mc-remote-scratch-LAN-2321.1.0-linux-x64.zip` | 272,115,968 | `52f1f4b3eff59cec44c634c8974d5b41cfb18ee873d1348021e7e1831a2cbe42` |
| `mc-remote-scratch-LAN-2321.1.0-macos-arm64.artifact.json` | 340 | `ba46238f36120ee9a38f64c6740c0247a346e500897f9bb6531fd9c1221f3e98` |
| `mc-remote-scratch-LAN-2321.1.0-macos-arm64.zip` | 266,859,915 | `d9bb5976f62ad5043130c911551f23b0f4b127a5f0a80a6465ff8cd7decb768e` |
| `mc-remote-scratch-LAN-2321.1.0-windows-x64.artifact.json` | 340 | `1c9e9f5b0bd38b3b67af0e5a2123676bd13b8c8e5feb5bc540aadf28c8289cd7` |
| `mc-remote-scratch-LAN-2321.1.0-windows-x64.zip` | 262,508,252 | `8edf5c1890df3550b3d4ffdd8d39dfbc1cbd35509531266ebd5e80103cab7ad6` |
| `scratch-gui.tar.gz` | 139,262,746 | `0f0b2597a8694863fb264340c1b3b89685849c85ce7c32e9f4b210e645fbdff8` |
| `scratch.oci.tar` | 326,605,824 | `c1dc8dc79a4e7dd351af728aa5e80677ce3aa08a84f8a4583dc9b4d9d84d7e10` |
| `wirescope-app.manifest.json` | 2,339 | `3dd668a236463809a4cdc6d19375f3e6d75eea0c8089a616d2b761d3a4a05235` |
| `wirescope-app.zip` | 83,854 | `da3da0b6cf4d05265bc0c11abaa4913208c7cfc3600b0c3e78c93a356fc431ad` |

- Scratch OCI index：**`sha256:f3bcf6a6e9ae939e8a8781628ad1e9b40507286da34224f91dfba711a4920c67`**。
- Bridge OCI index：`sha256:305d6e38b36e195a0e158522f32f3a8c45d39da2aeec7b7e46f785c920406acf`（変更なし）。
- 元のset-1 archive digest：`sha256:73a6aadbc91571d12f71218f40f54d00b626d05cd148ba8c26f9ec85fe8b6833`。旧値の全明細は`set-1-ALL_FILES.json`、新値は`set-2-ALL_FILES.json`。

## 生成元とLAN同梱ソース

- candidate manifestの`source.commit`は`57fb7691bb5d9a5895785b200ae78734240ebfa6`。
- LAN Windows x64／macOS arm64／Linux x64の外の`.artifact.json.source_commit`と、中の`data/identity.json.source.commit`は**3つとも同じ57fb769の全桁SHA**。いずれもdirty=false。
- 3 ZIPの`data/source/scratch-source.tar.gz`を実際に読み、`mc-remote/block-reference/site/2321.1.0/`の**62 file**を全3 OSで確認した。
- 同梱source archiveのSHA-256は3 OS共通：`38ffb80ccbb86b47d433ea9c09a68dcd5528b0b8219273efa9d6fe602c0dea07`。`data/identity.json`の`archive_sha256`とも一致する。
- 一覧JSONの`release`は2321.1.0。**一覧JSON自身の`sourceCommit`と`sourceRef`は既存の`11bce3193c524135931a5bf342a9edb1bfdfbbac`のまま**。今回のdispatchはmetadataを書き換える操作ではない。生成元11bce319は57fb769の祖先で、間の差分はsite生成物のみという2026-11-01の条件を維持する。tag予定commit／配布物と、この一覧の生成元fieldをすべて文字どおり57に書き換えた結果とは返さない。

全3 OSの外・中のidentityとsourceの比較は`LAN_COMPARISON.json`、外のJSONは個別fileでも添付。

## set-1との比較

以下の「同一」はSHA-256一致によるbytes同一。サイズだけの一致とは分けた。

| file | set-1 bytes | set-2 bytes | 中身のbytes |
| --- | ---: | ---: | --- |
| `bridge.oci.tar` | 114,626,048 | 114,626,048 | 同一 |
| `candidate-manifest.json` | 2,664 | 2,664 | 異なる |
| `contracts.tar.gz` | 1,908 | 1,908 | 同一 |
| `mc-remote-scratch-LAN-2321.1.0-linux-x64.artifact.json` | 336 | 336 | 異なる |
| `mc-remote-scratch-LAN-2321.1.0-linux-x64.zip` | 272,069,485 | 272,115,968 | 異なる |
| `mc-remote-scratch-LAN-2321.1.0-macos-arm64.artifact.json` | 340 | 340 | 異なる |
| `mc-remote-scratch-LAN-2321.1.0-macos-arm64.zip` | 266,813,430 | 266,859,915 | 異なる |
| `mc-remote-scratch-LAN-2321.1.0-windows-x64.artifact.json` | 340 | 340 | 異なる |
| `mc-remote-scratch-LAN-2321.1.0-windows-x64.zip` | 262,461,767 | 262,508,252 | 異なる |
| `scratch-gui.tar.gz` | 139,262,746 | 139,262,746 | 同一 |
| `scratch.oci.tar` | 326,607,872 | 326,605,824 | 異なる |
| `wirescope-app.manifest.json` | 2,339 | 2,339 | 同一 |
| `wirescope-app.zip` | 83,854 | 83,854 | 同一 |

### LAN：変更は同梱sourceとidentityだけ

全3 OSで、ZIP内の全fileの内容・mode・ZIP timestampを比較した。差があるのは次の**2 fileだけ**。

- `data/source/scratch-source.tar.gz`：新しい`site/2321.1.0/`の62 file追加と、最新の`site/blocks.json`／`site/index.html`の更新。source内の差分はこの64 fileだけ。
- `data/identity.json`：生成元commitと、上記source archiveのhashの更新。

実行用editor、launcher、guide、runtime Node、Bridge、WireScope、license等はset-1と同じbytes。ZIP全体が変わるのは、このsource／identity変更の結果。外の`.artifact.json`は新commit・ZIPサイズ・ZIPのhashを記録するため変わる。

### OCI：入力の変更と、build metadataの非決定性を分ける

旧index：`sha256:7f79830e7b625ab7d90dccbd5be949bbacd93d83686a3f4c16c9feb4a9dddb6a`。新index：`sha256:f3bcf6a6e9ae939e8a8781628ad1e9b40507286da34224f91dfba711a4920c67`。

linux/amd64とlinux/arm64をそれぞれ展開して比較した。

1. **変えて渡した入力**：`SOURCE_REVISION`が07f98eb→57fb769、`SOURCE_DATE_EPOCH`が1793979694→1794020567。imageのrevisionラベルとARG／LABEL履歴が変わり、config.createdは`2026-11-06T15:41:34Z`→`2026-11-07T03:02:47Z`へ変わった。これは対象commitを替えたことによる差。
2. **同じ内容でもbuildごとに変わるmetadata**：Web配下の1,749 entry（file／dir）のうち**1,748 entryはmtimeだけが異なる**。旧は主に`2026-11-06T15:46:34Z`／`15:46:35Z`、新は`2026-11-07T07:23:15Z`で、生成時の時刻がCOPY layerへ入っている。`SOURCE_DATE_EPOCH`はこのファイルmtimeを揃えていない。
3. **その他の非決定的な記録**：config historyのEXPOSE文字列にはbuild内部のアドレス値が記録されて変わっている。公開portの設定自体は同じ。SBOMの作成時刻・namespace、provenanceのbuild時刻／run metadata／refや生成物digest等も変わる。provenance内には対象commit・epochという入力差も記録される。
4. **実行内容**：両archともベースimageのlayer digestは同じ。Webファイルの追加・削除・内容のbytes差は**0**で、Web配下のmetadata差はmtimeだけ。versionラベルは両方とも**v2321.1.0**、新revisionは57fb769。したがって、今回のOCI差はLAN source追加がコンテナに入った差ではなく、commit入力とpackaging／provenanceの記録によるもの。ただし**OCI archiveはbit単位で再現可能なbuildにはなっていない**。

COPY layer全体も両archで1,752 entryを比較し、差は1,749 entryのmtimeだけだった（Web配下1,748件に、配信root directoryの1件が加わる）。uid／gid／mode／link等に差はなく、Web以外のpayload fileも無い。`LAYER_METADATA.json`を添付。

`OCI_COMPARISON.json`と`OCI_METADATA_SUMMARY.json`に両archの実測差を添付した。今回、Dockerfileやworkflowの正規化処理を追加していない。

### その他のfile

Web editor tar、contracts、Bridge OCI archive、WireScope ZIP／manifestは全件set-1と同じbytes。candidate manifestは新しいsource.commitと、変わったOCI／LANのbytes・hash・digestを記録するため変わる（fileの長さは同じ2,664 bytes）。

## smokeと検証結果

成功した候補jobのlogで確認した。

- release manifest contract：96 tests PASS。
- acquisition／candidate manifest／LAN境界：34 tests PASS。
- Python archive：11 tests PASS。
- workspace build、lint、固定artifact取得、Bridge digest維持、3 OS ZIP生成、Scratch OCI生成：すべてsuccess。
- Linux ZIP smoke：hash/source、空白・日本語を含むpath、同梱Node起動、GUI／configのHTTP配信、別originのWireScopeと固定asset、Bridge WS→TCP、正常終了、Scratch／Bridge／WireScopeの3 port解放：**PASS**。
- 取得後の実測：2つのarchive digest、13 fileずつのbytes／SHA-256、candidate manifestとの一致、LAN3の全entry比較・source62file、OCI両archのconfig／layer／Web payload比較：完了。

根拠：`RUNNER_AND_SMOKE.json`。このjob内のsmokeはstub TCP相手の決定論的試験である。

## 未検証の境界

- 実Minecraft、ペアリング、人間の画面操作、Windows／macOS実機での起動、OSのdownload／署名警告、iPad／Android操作はこのrunでは検証していない。人間試験はcoordinatorの実施票に従う。
- 共有環境への配置・公開後の取り込み照合は行っていない。新artifactを採用して凍結するexact setの判断はcoordinatorが行う。
- 一覧JSON自身の生成元fieldは11bce319であること、OCIのmtime／履歴／attestationに非決定性が残ることを上に分けて明記した。承認されたものとして省略していない。
- 新しいtag、Release、公開manifestは作っていない。`mc-remote-images.yml`も起動・改変していない。

## 搬送素材の扱い

分類②。引継ぎ先はknowledge gate coordinator／Scratch担当。新しいexact setと生成物identity、差分と未検証境界が正式recordへ移り、この素材への固有参照がなくなれば破棄可。大容量archive・展開物は`/tmp/scratch-23211-rebuild-20261107/set-1/`と`set-2/`の検証cacheにあり、正式な生成物の取得先はActions artifact。検証cacheは比較事実の正式収容後に破棄できる一時物③。
