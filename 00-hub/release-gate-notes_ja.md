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

## 2026-10-17 rc1横断release gate（OPEN）

- gate coordinator: knowledge担当session（Claude Code）。人間による明示handoffなしに他担当へ移さない
- human release owner: プロジェクトオーナー
- current phase: **OPEN**（2026-10-17、human ownerの判断「rc1ゲートを開く」）。範囲は下の叩き台をhuman ownerが確かめてから決める
- 目標日: rc1 2026-10-24まで、初回stable 11/7（`2026-10-13-06`）。厳しければ、2321への切り替えを落とさず日程をずらす（`2026-10-17-03`）
- 位置づけ: b→rcはAPIの凍結（versioning §10）で、APIはb9で凍結済み。rc1はprotocolをパッチで`23.2.1`へ上げ、artifact
  `2321.0.0rc1`、GitHubのpre-release（`2026-10-17-03`）。APIとwireの中身は変えない。
  rc1から、外部testerが会話履歴なしで開始・更新・復旧・feedbackできる入口を用意する（grand-design roadmap §3、§4）
- 基準set: b10（McRemote `v2320.0.0b10`、Scratch `v2320.0.0b10`、Python `v2320.0.0b9`、minecraft-remote-tooling `v2320.0.0b9`）
- release mode（案）: rcは短期betaでないので、§14の軽量modeを既定にしない。どこまで強めるかはchange coneで決める。コードの変更が
  小さければ、b10のPASSを`2026-08-23-01`の条件で再利用し、外部testerと同じ入口からの通しを人間試験の中心にする
- 範囲の叩き台（human owner確認待ち）:
  1. 版：McRemote、Scratch、Python、minecraft-remote-toolingを`2321.0.0rc1`にする（`2026-10-17-03`。toolingはprotocolの定義を
     持つので出し直す）。Pythonはmatureで、PyPIへ出すのは戻せない公開なので、GitHubのpre-releaseで試した後に行う（`2026-10-13-05`）
  2. 箱庭サーバー（VPSベータ）のMinecraftの版：rc1で26.3へ移す見込み（human owner 2026-10-17「rc1では、26.3へ移行することになると
     思う」）。使っているプラグインの26.3対応はhuman ownerが調査中
  3. 外部testerの入口：ホームページ（箱庭、Python、`/lan/scratch/`）、検証票、feedbackの導線（Discord、GitHub Issuesなど。未決）
  4. READMEからの導線：各repoのREADMEからホームページ（`/lan/scratch/`、`#lan`）へのリンクと、初めて読む人が通せるかの確認
     （下のpark確認のREADME／sample）
  5. LANパッケージの`はじめに.html`の文言（b10の3 OS試験の見つかったこと1）
- rc1の後の検討（範囲外）: McRemoteの対応版を1.21.11、26.1.2、26.2、26.3へ広げる。各系列の最終版の最終buildをsupportする方針。
  McRemote担当が搬送票を出す（human owner 2026-10-17、hub NOTES）
- gateを開くときのpark確認（`2026-09-30-09`、coordinatorの案。human ownerの判断待ち）:

  | park | 案 |
  | --- | --- |
  | Windowsの生徒のPC（mise、Git Bash） | rc1に入れる。McRemoteの確認票で、READMEのmiseの手順をGit Bashでのshimsの形と突き合わせてもらう。生徒のPCでの結果は届いたときに |
  | LANパッケージのランチャー、`はじめに.html`、Scratchの画面 | ①`はじめに.html`の文言をrc1に入れる（Scratchの確認票）。②③⑤は初回stableの後のまま、④は追わない |
  | LANパッケージの教材の部分の収録 | rc1の間にknowledgeが`20-教材`へ収録する |
  | 未生成chunkへの操作の制限 | 持ち越す。新しい拒否のreasonはwireの追加になり、APIの凍結の後に入れない。McRemoteの確認票で採否だけ聞く |
  | 認証前の内部テーブルの較正 | rc1の外部testerの試験は授業規模でないので持ち越す。授業相当のloadを行うときに再開 |
  | Scratchの製品noticeを一つに絞る | Scratchの確認票で聞く |
  | Scratch OCIのversionラベル | rc1でScratch担当へ着手を頼む |
  | API一覧（クライアントAPI一覧へのつなぎ方） | 持ち越す（初回stableの後） |
  | rc1のrollbackの範囲 | rc1で決める。「同じMC版の中で1つ前の公開setへ戻す」案を、Stackの今の経路でできるかStackへ聞く |
  | public README／sample codeの人間向け再編 | rc1に入れる（範囲の4）。Pass Cの確認を外部testerの入口の通しに重ねる |
  | protocol 22 Scratch block値の投影（aliasと読み上げ） | Scratchの確認票で聞く。aliasに登録する語はhuman ownerが選ぶ |

  サーバーの再起動の後の接続（2026-10-12のpark）は、再開が初回stableの後で、rc1には入れない
- 次の操作（2026-10-17）：各担当へ確認票を頼む（`00-hub/rc1-gate-confirmation-instructions_ja.md`）。2321への切り替えの変更範囲と、
  上の範囲・park確認の各項目の事実を返してもらい、着手依頼を出す。knowledge側：versioningとwireの版の記述、API一覧の`23.2.1`、
  ホームページのrc1の記述、教材の収録、feedbackの導線の案
- 進捗（2026-10-17〜18、確認票）：Stack、McRemote、Python、Scratch（tooling、10/18）が返した
  - Stack（`main@1a4f8e5`、knowledge `60ea3c6`を読んだ）：コードにprotocolの定数は無く、版はpresetのデータで持つ。rc1の変更は
    新しいpresetだけ。b10の公開VPSへの更新（10/17、b9→b10、同じvolume）は完了。**manifest v2のconsumer（`agent/b10-manifest-v2-consumer@2eaf41b`）が
    mainに入っていない**（b10の記録では「mainへはb10のcloseで入れる」）。mainのCLIではb10公開版のmanifestの`verify`がFAILし、
    mainと`2eaf41b`のmergeではpytest 543件と同じ`verify`がPASS（手元の一時worktree）。rollback：前へ進む更新は同じvolumeで動き、
    更新の前に旧order、旧lock、operator入力、backupを残しているが、`mcrctl deployment update`は後退の更新を拒否する（`update_not_forward`）。
    26.3：backupから複製した別コンテナ（公開portなし）で、Paper 26.3 #200／Temurin 25でplugin 10個が有効、startupにERRORなし、
    McRemoteのcredentialはHEALTHY、ServerBackupでZIPを作れた（live-auto、10/17）。DirectionHUD／OtterLibとAdvancedPortalsは26.2までの宣言。
    Stackの経路は別セットへの切り替え（`2026-08-25-02`、in-placeでworldを変換しない）。README：b7.post2の古い記述など
  - McRemote（`main@e2ed84d`、knowledge `2fd5cde`を読み、`60ea3c6`の依頼本文と同一と照合）：`ProtocolInfo.PROTOCOL`を変えれば
    helloと互換判定が追従し、判定のalgorithmは変えない。互換の関数はメジャー一致、server minor以上、パッチを問わない。
    `release_identity.py v2321.0.0rc1`は`McRemote 2321.0.0rc1 (Minecraft 1.21.11, 26.3)`、`mc-remote-2321.0.0rc1.jar`、`prerelease=true`を
    導出（release scriptのtest 38件PASS）。b10後のmainはREADMEの再編と`docs/recommended-plugins_ja.md`だけ。rc1の対応版は1.21.11と26.3のまま。
    見積もりは版・test・文書で半日〜1日、fixtureの受領後の照合と2版のpulseで半日〜1日。rollback：rc1で版とfixtureと文書だけを変え、
    config、SQLite schema、credentialに触れなければ、同じMC版でb10のJARへ戻せると静的に見込む（未実施。隔離サーバーでb10→rc1→b10の
    往復とrevokeの非復活を確かめる案）。未生成chunkの制限はrc1から外す案に賛成。READMEは`#lan`から最短手順へ直接来られるanchorと、
    `/lan/scratch/`への戻る1行の案。Windowsのmiseはshimsの案内が足りず、human ownerの再現できる手順が要る
  - Python（`main@49c80a0`、knowledge `60ea3c6`）：b10後の変更なし。変えるのは`PROTOCOL = "23.2.0"`、pyproject、uv.lock、共有fixtureの
    扱い、同梱WireScope（toolingの新しいreleaseから作り直す）、利用者向けの記述。toolingの固定releaseの後、1〜2開発日。
    **starterのtemplateの箱庭が`sb.mc-remote.com`（旧protocol）で、README／ホームページの`sb-beta.mc-remote.com`と食い違う**。
    PyPI：release workflowは`PYPI_PUBLISH_ENABLED=true`で、uploadは`pypi` environmentのhuman owner承認待ちになる構成。
    pytest 267件PASS（今のmain）
  - Scratch（tooling。Scratch `develop@0809eb5`＝公開b10、tooling `main@5f567f1`、knowledge `60ea3c6`を読んだ）：Scratchの`develop`にb10後の
    commitは無い。toolingの`main`はb9のtagより2 commit先（release manifest v2のschemaとfixture、宣言objectの検証の修正）。変える箇所：
    toolingの`PROTOCOL_VERSION`とcontract test、fixtureの版の記述（v22、v23.1などの履歴は改名しない）、WireScopeのZIPとmanifest、
    Bridge OCI、ScratchのVMの`PROTOCOL_VERSION`と`client-version.js`とtest（23.2.1のclientが23.2.0のserverを受け入れる回帰testを足す）、
    `mc-remote/tooling-lock.json`、LANのZIP名と版のフォルダー（`client-version.js`から作る）、b10を固定で書いたworkflowとscript、README、
    ブロック一覧。見積もりは各半日〜1日（review、CI、3 OS、外部testerを含まない）。`はじめに.html`の原稿は`mc-remote/local/USER_GUIDE_ja.md`で、
    macOSの手順は観測と違い（「このまま開く → 開く」）、rc1で直せる。製品noticeはsourceでは1 entry（公開deploymentの追加noticeは未確認）。
    OCIはcandidateが`2320.0.0b10`、公開が`v2320.0.0b10`をversion labelに渡しており、今のままでは同じdigestにならない。pickerのalias辞書と
    読み上げは未実装で、候補の置き場所の案は`packages/scratch-gui/src/lib/mcremote-block-names/aliases.<mc-version>.json`。26.3の名前の
    データはまだ無い。READMEは`README_mc-remote.md`と`mc-remote/local/README.md`の冒頭に`/lan/scratch/`を置く案。`mc-remote/local/README.md`の
    「公開済み配布物ではありません」は古い。10/24はtoolingの固定、candidate、3 OS、外部testerの入力次第で断定できない
- 決定（2026-10-18、human owner）：
  - Stackとbackstageをgate coordinatorの管轄に戻す（`2026-10-18-01`）。Stackのmanifest v2のconsumerを、rc1の作業の最初にmainへ入れる
  - 公開VPSは別セットへ切り替え、rc1で箱庭を戻すことは考えない。26.3のセットを手元かGAMEsサーバーで試し、できれば26.3へ移す。
    DirectionHUDは早めにやめる（`2026-10-18-02`）。rollbackの範囲のparkは閉じた
  - 共有fixtureの23.2.1版は新しいfile、23.2の版は履歴（`2026-10-18-03`）
  - PyPIは承認待ちのまま進め、GitHubのpre-releaseで試し終えるまで承認しない（`2026-10-18-04`）
  - 箱庭の名前：beta／rcは`sb-beta`、latestは`sb`。latestのreleaseで旧protocolのサーバーを消す（`2026-10-18-05`）。Pythonのstarterは`sb-beta`へ
  - Pass Cは生徒が行い、10/24までに済ませる（経験者になる）→ 2026-10-19に改訂：rc1では生徒の初学者を対象にしない（`2026-10-19-01`）
  - Windowsのmiseは今のREADMEの手順のまま出す。困っている生徒のPCで検証が進む見込み
  - pluginの情報は、Stackが別の搬送票で出す
  - McRemoteのREADMEは複数のページに分けたいが、まだできていない。おすすめプラグインのページ（`docs/recommended-plugins_ja.md`）がその足がかり（human owner）
- 次の操作（2026-10-18）：着手依頼（`00-hub/rc1-gate-work-instructions_ja.md`）をhuman ownerが確かめてから各担当へ回す。toolingの23.2.1から始める
- 進捗（2026-10-18）：human ownerがScratchとStackへ着手依頼を回した。knowledge側で、versioning（§9.3、§10.11.4）とwire（§1）に
  `23.2.1`を書いた。wireの§4と§7.3の表はAPI一覧の生成元なので、`23.2.0`のページを変えないよう触らない。rc1の公開のときに
  metadataを`23.2.1`へ切り替え、b8の但し書き（`protocol.note`）を外して`api/23.2.1/`を作る
- 進捗（2026-10-18、tooling）：fixtureの23.2.1版を`minecraft-remote-tooling` `agent/rc1-protocol-2321@6447f6e8cbfbeeb9d229990b5c4f6e82a5875666`
  （mainより1 commit先）に追加し、旧fileを残した（`2026-10-18-03`）。`chat-event-compat-v23.2.1.json` 32,384 bytes、
  `eead244a7340c315cb63e1e77ede0fe9cf48162c06fedbeef36d941950d5000d`、`entity-particle-v23.2.1.json` 36,483 bytes、
  `0319ff8373a96798cf5e9e421a804729fd33a0fa53e96adc12c93ed7994777ae`。CI run `39053886890` success、artifact `12109060950`
  （`sha256:5b644de44ae2f9a2fb9de09d221c2930218f6c317baffee3b5c7f817309555fa`）。coordinatorがGitHub APIで照合し、新旧のfixtureは
  版の識別子（`23.2.0`／`23.2.1`、schema名の`v23.2`／`v23.2.1`）を除いて同じ中身と確かめた。WireScopeとBridgeのidentityは
  Scratchのcandidateと一緒に返る。McRemoteとPythonはこのfixtureで着手できる
- 進捗（2026-10-18、tooling WireScope／Bridge）：同じartifact `12109060950`に、WireScopeとBridgeのcandidateも入っていた
  （`candidate-manifest.json`、source commitは`6447f6e8cbfbeeb9d229990b5c4f6e82a5875666`）。`wirescope-app.zip` 83,854 bytes、
  `da3da0b6cf4d05265bc0c11abaa4913208c7cfc3600b0c3e78c93a356fc431ad`、`wirescope-app.manifest.json` 2,339 bytes、
  `3dd668a236463809a4cdc6d19375f3e6d75eea0c8089a616d2b761d3a4a05235`、`bridge.oci.tar` 114,626,048 bytes、
  `3982876466fb860dca250438d73e18e441a2a85d67d9f149f537a7a8d1a1c44c`（OCI digest
  `sha256:305d6e38b36e195a0e158522f32f3a8c45d39da2aeec7b7e46f785c920406acf`）。coordinatorがartifactをdownloadして、bytesと
  SHA-256、OCIの`index.json`のdigestが一致すると確かめた。PythonはこのWireScopeで同梱を作り直せる。Pythonのwheel／sdistに
  入った後のidentityは、Python担当が照合して返す
- 進捗（2026-10-18、Stack）：v2のconsumer（`agent/b10-manifest-v2-consumer@2eaf41b`）をPR #71で`main@e5f33188820f875e8aa7dc504952316458d87d73`
  へmergeした。mainのCLIで、b10公開版のmanifest（McRemote b10、Scratch b10、Python b9）の`verify`が3件ともexit 0。pytest 543件と
  ruffがPASS。READMEの手直しはPR #72（`agent/rc1-readme@0c5a30d1e23b9762e23160beb13540f746810338`、review待ち）。公開中の
  `scratch-beta.mc-remote.com`の設定JSONで、製品noticeは1件（版とreleaseページへのリンク）、運用者noticeは2件、接続先は
  `sb-beta.mc-remote.com`（配信のJSONだけを見た。ブラウザでの表示は見ていない）。rc1のpresetと別セットへの切り替えは、各componentの
  tagと凍結の後。coordinatorはPR #71のmergeとmainのSHAをGitHubで確かめた
- 進捗（2026-10-18、McRemote）：candidateは`agent/rc1-pre-fixture@192a777ae1d484bcc9b58fcc7c58d6aed1a374af`（mainより2 commit先、
  knowledgeは`277fa69`を実読）。CI run `39065266196` success、artifact `12112853171`（294,255 bytes、
  `sha256:ef4bf641ac4c229a6c1ca413c0698dd4350559bdcb5f643e72cdf807b53686be`）。`mc-remote-2321.0.0rc1.jar` 315,352 bytes、
  `917c358c201aa219277b96a447fb85116e8bdb0260870a4d76a8c51219d31c37`。対応版の宣言は1.21.11と26.3。Paper 1.21.11 #132と26.3 #203の
  隔離した環境で、通常のpulse、再起動のpulse、23.2.0の認証付きhelloの受け入れがPASS。coordinatorはartifactをdownloadして、
  中のJARが票のSHA-256と同じで、`plugin.yml`の版が`2321.0.0rc1`であることを確かめた。素材は
  `McRemote/handoff-materials/2026-10-18-rc1-candidate/`。evidenceのrecordにするかは凍結の後で決める
- 判断（2026-10-18、human owner）：Stackの確認から、park「Scratchの製品noticeを一つに絞る」を閉じた。運用者noticeの「b10版を…」は、
  rc1へ切り替えるときのnoticeの確認の工程で直す。Paper 26.3は#203が出ていて間に合いそうだったので、McRemoteの試験を#203へ
  切り替えた（Stackの10/17の複製worldの試験は#200）
- 進捗（2026-10-18、Python）：candidateは`codex/rc1-python-pre-fixture@c30105349ef26413e925699143396ea05bd3e380`（mainより3 commit先、
  knowledgeは`40a91a7`を実読）。CI run `39067369316` success（Python 3.10〜3.13で各784件）、artifact `12113309553`（383,227 bytes、
  `sha256:df3baf887314934fae1285bb722c90c21e5543191522da9703a3a2a3b948b4c3`）。wheel
  `minecraft_remote_api-2321.0.0rc1-py3-none-any.whl` 196,098 bytes、`5f12dfcf4953bfaf5dcbe649d4a1ca2d3f5f4b5307b9896e79284478216944ca`、
  sdist `minecraft_remote_api-2321.0.0rc1.tar.gz` 190,285 bytes、`dc8d9f30f538c14cfa04260c92f32e8f451748b99a8e596aeb3e59b1968e5611`。
  同梱WireScopeのsourceはtooling `6447f6e`。coordinatorはartifactをdownloadして、wheelとsdistのSHA-256、wheelの中のWireScopeの
  ZIPとmanifestがtoolingのcandidateと同じこと、`Version: 2321.0.0rc1`と`PROTOCOL = "23.2.1"`を確かめた。実サーバーへの接続は
  まだ。素材は`minecraft-remote-api/handoff-materials/2026-10-18-rc1-python-candidate/`
- 進捗（2026-10-18、Scratch）：candidateは`agent/rc1-scratch-2321@ec79b3b0e364e722d6926a0932eb4bf088ddd3a1`（draft PR #26、
  developより7 commit先）。toolingはdraft PR #1（`agent/rc1-protocol-2321@6447f6e`、mainより1 commit先）。最終のCI run
  `39072595749` success（初回の`39060684619`は、ZIPのsmokeが旧`23.2.0`を送っていて失敗し、直した）、artifact `12116296168`
  （1,370,212,918 bytes、`sha256:259ca91e68616035a81deb49bb1060300138c85942597a2b11c7b7f5133d66e8`）。coordinatorはPRのhead、
  runの`head_sha`、artifactのdigestをGitHubで確かめた。ZIPなどの値は下の凍結（案）の表。26.3の名前は公式の言語データから
  1,275件、GUIの表示と検索はtestで確かめた。26.3のサーバーでの日本語名、設定画面の画像はまだ。GUI integrationの
  `menu-bar.test.js`は、基準のdevelop（run `38525476758`）でも同じく落ちる既存の失敗。ブロック一覧の`site/2321.0.0rc1/`は
  用意済み。素材は`scratch-editor/handoff-materials/2026-10-18-rc1-work-scratch/`
- **exact set凍結（`rc1-integrated-artifact-set-1`、human owner承認 2026-10-18）**: protocol `23.2.1`／artifact `2321.0.0rc1`
  - minecraft-remote-tooling: source `6447f6e8cbfbeeb9d229990b5c4f6e82a5875666`（run `39053886890`、artifact `12109060950`）
    - `wirescope-app.zip` 83,854 bytes／`da3da0b6cf4d05265bc0c11abaa4913208c7cfc3600b0c3e78c93a356fc431ad`
    - `wirescope-app.manifest.json` 2,339 bytes／`3dd668a236463809a4cdc6d19375f3e6d75eea0c8089a616d2b761d3a4a05235`
    - Bridge OCI `bridge.oci.tar` 114,626,048 bytes／`3982876466fb860dca250438d73e18e441a2a85d67d9f149f537a7a8d1a1c44c`、
      index `sha256:305d6e38b36e195a0e158522f32f3a8c45d39da2aeec7b7e46f785c920406acf`
    - shared fixture：`chat-event-compat-v23.2.1.json` 32,384 bytes／`eead244a7340c315cb63e1e77ede0fe9cf48162c06fedbeef36d941950d5000d`、
      `entity-particle-v23.2.1.json` 36,483 bytes／`0319ff8373a96798cf5e9e421a804729fd33a0fa53e96adc12c93ed7994777ae`。旧版は履歴として残る
  - Scratch: source `ec79b3b0e364e722d6926a0932eb4bf088ddd3a1`（run `39072595749`、artifact `12116296168`）
    - `mc-remote-scratch-LAN-2321.0.0rc1-windows-x64.zip` 261,848,009 bytes／`86bbaf9a278683315ffe2ebd4f19d56ba53f5501289e4cddfc22f284d8d4e209`
    - `mc-remote-scratch-LAN-2321.0.0rc1-macos-arm64.zip` 266,199,673 bytes／`bdfff47b8c1210a359ed65a8be6fca26624546e3c04add125063968acc091412`
    - `mc-remote-scratch-LAN-2321.0.0rc1-linux-x64.zip` 271,455,727 bytes／`b76b574803c58403e38438d2569917bd72ca95f039026f12ed3a294edfcfba54`
    - Scratch OCI 325,822,464 bytes／`88d81fba1aca0194c85f638cf19c66a1a2087748f32ff501bdb1dd283ea1d0c5`、index
      `sha256:75e76edb6b8a1de4fb896184b5c26bed7cb1791296f82903e6b1ec4a1a5ab840`。公開でdigestが変わっても止めない（b9と同じく差を記録）
    - `scratch-gui.tar.gz` 138,835,708 bytes／`2dafb257c511989946da021591191cc1501e0d1a9211cc559373ed7de30f19c2`、`contracts.tar.gz`
      1,908 bytes／`48948ba47d55409f02a8ff8e0d44021b07859e11ffa5ca0f8598e6ef06082390`
    - coordinatorがartifact（外側のdigestが一致）をdownloadして、上の全fileのbytesとSHA-256、`candidate-manifest.json`
      2,676 bytes／`a29b56239a060f95fe9c67f708023a14c64ac422bd108097586d544d201afbd2`、Scratch OCIの`index.json`のdigestを独立に
      計算し、票の値と一致した。3 OSのsidecarはsource commit `ec79b3b`、`working_tree_dirty:false`。同じartifactの中のWireScopeと
      Bridge OCIはtoolingの凍結値と同じ
  - McRemote: source `192a777ae1d484bcc9b58fcc7c58d6aed1a374af`（run `39065266196`、artifact `12112853171`）
    - `mc-remote-2321.0.0rc1.jar` 315,352 bytes／`917c358c201aa219277b96a447fb85116e8bdb0260870a4d76a8c51219d31c37`。対応版の宣言は
      1.21.11と26.3（`minecraft-targets.json` `8e830732decd6bcde13f91eb6c071d062ba6993342a7edb52e6ea543b9e0c361`）
  - Python: source `c30105349ef26413e925699143396ea05bd3e380`（run `39067369316`、artifact `12113309553`）
    - wheel `minecraft_remote_api-2321.0.0rc1-py3-none-any.whl` 196,098 bytes／`5f12dfcf4953bfaf5dcbe649d4a1ca2d3f5f4b5307b9896e79284478216944ca`
    - sdist `minecraft_remote_api-2321.0.0rc1.tar.gz` 190,285 bytes／`dc8d9f30f538c14cfa04260c92f32e8f451748b99a8e596aeb3e59b1968e5611`
  - Stack: `main@e5f33188820f875e8aa7dc504952316458d87d73`（v2 consumer）。README（PR #72）はrelease物ではないので凍結の外
  - 凍結の前の返却（2026-10-18）:
    - Python：着手依頼の1、3、4はcandidate `c301053`に入っていた。互換のtestは
      `tests/test_b1.py::test_rc1_client_accepts_compatible_hello_response[23.2.0]`（23.2.1を送り、23.2.0のhelloの応答を受け入れる
      unit test。模擬の接続で、実サーバーではない）。starterのtemplateの`ADRS_MCR`は`sb-beta.mc-remote.com`。READMEはStep 2から
      `https://mc-remote.com/#lan`へのリンク、Step 1は`uv add "minecraft-remote-api==2321.0.0rc1"`
    - Scratch：着手依頼の6は、`mc-remote/local/README.md`の分がcandidate `ec79b3b`に入っていて、`README_mc-remote.md`の分
      （`/lan/scratch/`の案内、APIのリンクを`https://mc-remote.com/api/`へ）は次のcommit
      `agent/rc1-scratch-2321@f20e55eb53f192eab6cdc4f0d5aae4f52b2dc8db`（PR #26のhead）。coordinatorがGitHubで、`f20e55e`は`ec79b3b`の
      1 commit先で、変えたのは`README_mc-remote.md`の1 fileだけと確かめた。candidateは作り直さない（coordinatorの判断）。作り直すと
      OCIのlabelとsidecarのsource commitが変わり、凍結値と同じにならない。tagは凍結したsource `ec79b3b`に打ち、`develop`は
      `f20e55e`までfast-forwardしてよい（tagと既定のbranchの先頭は一致しなくなる）
  - 試験と公開の順（2026-10-18、human owner）：凍結 → 候補をmc-remote.comに置く → そこから取って試験 → 判定 → リリース
    → 公開の後に照合。リリースを今までどおり最後にする。b10は先にpre-releaseを作ってそのassetで試したが、GitHub.comから
    取ることでしか確かめられないものは無いと見た。同じbytesであることは公開の後にSHA-256で照合でき、OSの確認（Windowsの
    「許可する」、macOSの「このまま開く」）はダウンロードの印とファイルの中身で決まり、取得元のサイトによらない。ブラウザの
    ダウンロードの警告はサイトの評判が効くので、GitHub.comより評判の低いmc-remote.comで通れば厳しいほうで確かめたことになる
    （human owner「GitHub.comより『怪しい』サイトなので、良いのかもしれない」）。試験で直すことが出れば、candidateを作り直す
  - 候補の置き場所（Stackに頼む、`2026-10-18-07`）:
    - 経路（2026-10-18、Stackの案Aをhuman ownerが採った）：Stackの公開VPSのCaddyfileに`/candidates/*`を固定の経路として足す。
      中身はホームページとは別のhostのディレクトリを読み取り専用でmountする。稼働中のVPSへdeployment updateが1回要る（作り直すのは
      Caddyだけの見込み）。時期はhuman ownerが決める。CDNは通らない。経路は残し、中身は消せる
    - 進捗（2026-10-18、Stack）：PR #73（`agent/rc1-candidates@c3cf1685e18c6a780c877d58a403ca32ef6162b7`）で`/candidates/*`を
      実装した。profile `vps-server@13`、renderer `compose@15`、presetは`public-web-paper@14`のまま。pytest 547件、ruff、catalogの
      確認がPASS（手元。PRにCIの結果は付いていない）。公式のCaddy 2.11.4で、Content-Type、noindex、圧縮しない、Range、一覧を
      出さないことを手元で確かめた。稼働中のVPSの更新では、Minecraftを含む4つのサービスがすべて止まる（見込みのCaddyだけより
      広い）。Stackが読んだknowledgeの`54285e1`はcoordinatorがpushの前に作り直したcommitで、GitHubに無い（正しくは`ca70a75`、
      `set-<N>/`を足したもの）。経路は`/candidates/*`の汎用の形なので、実装への影響は無いと見る。更新の前にPR #73を`main`へ
      mergeし、`main`から更新する。時期はhuman ownerが決める
    - 進捗（2026-10-18、配置）：Stackが`main@204b3c6dcf7bf9c7a44938665eec0c8a2d77dc49`（PR #73、#74をmerge）のprofile
      `vps-server@13`で公開VPSをsame-volumeで更新し、doctorは全項目OK（homepage、Scratch runtime、WireScope current）。止まったのは
      Minecraftが約35秒、HTTPSが数秒。1回目のapplyはStackの実装の漏れで`rollback-failed`になり、#74で直して、human ownerの判断で
      更新先のまま仕上げた。Stackはartifactの外側のdigestを確かめ、取り出した5 fileが凍結値と一致し、VPSの上の`sha256sum -c`も
      5件OK。置き場所に`SHA256SUMS`もある
    - 照合（2026-10-18、coordinator）：外からHTTPSで5 fileを取り、bytesとSHA-256が凍結値と全桁で一致した。`SHA256SUMS`の値も
      凍結値と同じ。ヘッダーはContent-Typeが`application/zip`（`.whl`も）と`application/java-archive`、`x-robots-tag: noindex,
      nofollow`、`Content-Encoding`無し（gzip等を受け入れると伝えても）、`accept-ranges: bytes`でRangeに206。`/candidates/`、
      `/candidates/2321.0.0rc1/`、`set-1/`は404で一覧を出さない。実施票へURLを書いた
    - 1回目のapplyの`rollback-failed`（2026-10-18、Stackの記録。貼り付けで行末が切れた箇所があり、細部はStackの記録が正本）:
      - 漏れ：#73でrenderer `compose@15`を足したとき、版の番号で処理を分けている2か所に`15`を足し忘れた。`render.py`の生成物の
        manifestの検査が`adapter_revision`を`13`と`14`しか受け付けず、更新先のdoctorも巻き戻しのrenderも
        `render_output_tampered`で失敗した。`doctor.py`は公開の確認（homepage、Scratch runtime、WireScope）を`13`のときしか
        走らせず、`compose@15`では確認を飛ばすところだった。#73のtestは空の出力へのrenderだけで、更新のtestはrenderとpublishを
        stubにしていたので見逃した
      - #74（`204b3c6`）：2か所で`compose@15`を公開VPSのrendererとして扱う（doctorは`PUBLIC_RENDERER_REVISIONS = {"13", "15"}`）。
        test 2件（もう一度のrender、doctorの通し）を足し、直す前に落ちることを確かめた。版の番号で分けている箇所を`src/`全体で
        調べ直し、残りはrenderとdoctorだけだった
      - worldとcredential：影響は無い。volumeは同じものを使い続け、Minecraftは「All dimensions are saved」を出してから止まった。
        起動の後、McRemoteはcredential domain `HEALTHY`、auth enforcement `true`。storeとauthorityのfileは更新の前から
        書き換わっていない（Stackの記録）。`rollback-failed`の約15分、動いていたのはplanで決めた更新先の設定で、ずれていたのは
        ディスクの上のproject（order、lock、operator）だけ。containerは作り直されなかった。McRemoteの`config.yml`は生成物から
        入れ直され、先頭行の版番号のほかは同じ値（McRemoteが既定のkeyを書き足すのは、どの更新でも起きる）
      - 切り替え（`2026-10-18-02`）で同じことが起きないと言える根拠：経路が違う。切り替えは別のproject、別の`generated/`、別の
        volumeで作り、`mcrctl apply`で起動する。今回落ちたのは同じ出力の上で版をまたいでrenderし直す経路で、切り替えはそこを
        通らない。旧セットは手つかずで残る。PR #75（pytest 552件 PASS）で、同じ出力への`@12 → @13 → @12 → @13`のrender（直す前の
        `06bf98f`ではVPSと同じ`render_output_tampered`で落ちることを確認）、切り替えで使うbootstrapのapplyと2回目のapply、
        `@13`でのdoctorの通しを確かめた。次のセットにcandidatesのディレクトリが無ければ、準備のrenderが`runtime_content_missing`で
        止まり、旧セットを止める前に気づける
      - Stackに残る弱点（切り替えの経路には関係しない）：same-volumeの更新は、巻き戻しも同じrenderのコードを通るので、そこに
        漏れがあれば両方とも失敗する。Stackには`rollback-failed`から戻す手順が無い（今回は`state.json`を手で書き換えた）
    - 置くもの：LANパッケージのZIP 3つ、McRemoteのJAR、Pythonのwheel。`https://mc-remote.com/candidates/2321.0.0rc1/set-1/`
      （setの番号は凍結の`rc1-integrated-artifact-set-1`。作り直して試し直すときは`set-2/`）。リリースの後に中身を消す
    - 送り方：GitHubのartifactから取り出し、手元でSHA-256を凍結値と照合してから、`rsync --partial`で送る（切れても続きから
      送れる）。VPSの上で`sha256sum -c`
    - 配り方：Content-Typeは`application/zip`等、再圧縮しない、Rangeに応える、ディレクトリの一覧を出さない、
      `X-Robots-Tag: noindex`
    - coordinatorが外からHTTPSで取り、bytesとSHA-256を凍結値と照合してから、実施票で案内する
  - 公開（試験の判定の後）:
    - 順番：toolingを先に出す（Scratchの公開物がtoolingの生成物を集めるため）
    - 各repo：作業branchを既定のbranchへfast-forwardで入れ（tooling `main`、Scratch `develop`、McRemote `main`、Python `main`）、
      tag `v2321.0.0rc1`を凍結したsourceへ打つ（Scratchは上のとおり`ec79b3b`）。fast-forwardにならない（既定のbranchが動いた）
      ときは、止めてcoordinatorへ返す
    - 4 repoとも`prerelease=true`、`draft=false`、latestにしない。tagのCIや公開workflowが作るものが凍結値と違ったら、
      公開せずに止める（OCIのdigestは上の扱い）
    - Python：PyPI.orgのjobは承認待ちで止め、試験の後にhuman ownerが承認する（`2026-10-18-04`）
    - 公開後、coordinatorがtag target、prerelease／draft、assetと`manifest.json`のidentityをGitHub APIで照合する。assetが
      試験したもの（凍結値）と同じbytesであることを、ここで確かめる
  - 試験：実施票`00-hub/rc1-gate-live-test-instructions_ja.md`（mc-remote.comに置いた候補で行う）
    - 2026-10-19：human owner「進め方が自由すぎてやりにくい」。実施票をOS別（Windows → Ubuntu → Mac）に、番号の順で
      進める形へ書き直した。Linux ZIPもUbuntuで一度起動する。MacのBは1台構成の代わりにMac → Ubuntuにし、1.21.11での
      26.3の名前はUbuntuで見る
    - Windows（2026-10-18〜19、手順1〜8済み）：Windows 11 Pro 26H2（26300.9711）、Core i3-8145U、メモリ16 GB、
      Chrome 155.0.8059.85、Java 25.0.2+10-69（Oracle OpenJDK）、Paper 26.3 build 203
      - ZIP `mc-remote-scratch-LAN-2321.0.0rc1-windows-x64.zip`をmc-remote.comからChromeで取得、261,848,009 bytes（凍結値と一致）。
        プロパティで「許可する」にチェック。Chromeのダウンロードの警告は出なかった
      - `2321.0.0rc1/`を`2320.0.0b10/`の隣に置いた（中身はどちらも`NOTICE_ja.md`、`README_ja.md`、`data`、`settings.json`、
        `start-mc-remote.cmd`、`はじめに.html`）
      - McRemote b10（起動logで`Enabling McRemote v2320.0.0b10`、`Auth enforcement: true`、credential `HEALTHY`、
        catalog blocks=1286 hash `3eaae42e9bcbd5e6ef6a2d1df702b25a878ca3157dcadc58ae29822fe5277663`）に、起動ファイルの
        ダブルクリック → 設定画面 → Scratch rc1で「接続」。WireScope miniが開き、ペアリング成功。WireScopeのhelloは送信
        `protocol 23.2.1`、client `scratch-mcremote 2321.0.0rc1`、受信`protocol 23.2.0`、`mc_version 26.3`、
        `supported_mc_versions ["1.21.11","26.3"]`。版の違いで止まらず、`chat.post`は`result:null`。「一通りうごく」（human owner）。
        rc1の初回は`settings.json`が無いので設定画面だけが開き、既定の「このPC」のまま保存して進んだ（human ownerの記憶、
        「はず」）。b10で保存した作品は一覧に残っていた
      - 同じ接続で、カタログピッカーは「取得済み — 26.3 · CACHE · 3eaae42e」。「ポプラ」で23件、`poplar log ポプラの原木`が出た
      - McRemoteをrc1に替えて起動（`Enabling McRemote v2321.0.0rc1`、`Auth enforcement: true`、credential `HEALTHY`、
        catalogはb10と同じblocks=1286、同じhash）。Scratch rc1で接続し、チャットとsetBlockが届いた。前のペアリングから2時間を
        越えていたので、ペアリングし直した（設計どおり）
      - 手順7：b10の起動で、設定画面が開いた後にScratchが表に開いた（human owner：設定が残っているときはこう開き、無いときは
        設定画面だけなので、違いが分かる）。b10の`settings.json`には、b10の試験のWindows → macOSのLAN構成の接続先が残っていて、
        「接続」はエラー。WireScope miniの「設定先」「実接続先」にその接続先が出ていて、原因がすぐ分かった。Scratchのタブが
        開いている間は、設定画面の「設定を保存する」が押せず、「いずれかのタブでScratchが既に開いています。接続先を変えるときは、
        Scratchのタブを閉じてください。」と出る。版の違いのエラーではない
      - 読み取り（coordinator）：`settings.json`は版のフォルダーごとなので、b10をLAN構成で使っていた人は、rc1の初回で接続先を
        入れ直すことになる。1台構成なら既定の「このPC」のままでよい
      - 手順7の続き：Scratchのタブを閉じ、b10の接続先を「このPC」にして接続した。WireScopeのhelloは送信`protocol 23.2.0`、
        client `scratch-mcremote 2320.0.0b10`で、まず`token_expired`（前のペアリングから時間がたっていた）。ペアリングの後の
        helloは受信`protocol 23.2.1`、`mc_version 26.3`、`supported_mc_versions ["1.21.11","26.3"]`、catalog hashは上と同じ。
        ハンドシェイクの表示は「26.3 · 23.2.1」。`chat.post`「hello from b10 to rc1」は`result:null`で、マイクラのチャットに出た。
        続けて`world.setBlocks`で`gold_block`を3段ずつ（x、zは-50〜50）積み、どれも`result:null`で、マイクラに金の塔が建った
      - human owner：「ぼんやりと操作して間違えても、脱出は容易な感じ。良い。接続の接続先／状態表示が詳細になればもっと良い。」
        （後半はb10の見つかったことの8、9と同じ向き。rcからstableにかけて、または初回stableの後の改善として扱う）
      - 手順8：human owner：普通の感覚で、古い版を削除する人は少ないと見る。旧版を残して新版を隣に入れることは図解されているので、
        理解されそう
    - Ubuntu（2026-10-19、手順1〜7済み）：Ubuntu 24.04（kernel 7.0.0-38）、Chrome 155.0.8059.84、Java 21.0.2+13-58（Oracle OpenJDK）、
      Paper 1.21.11 build 132
      - Pythonの試験用フォルダーを2つ作り、rc1は候補のwheelをURLで入れた（`[tool.uv.sources]`に候補のURL）。実施票の`uv init`
        は、uv 0.12.19では`src/<名前>/`のpackageの形を作り、階層が深くなった（human owner「階層が深いな」）。実施票を
        `uv init --no-package`（直下に置ける形）へ直した。作ったフォルダーは`src/`の下の`hello.py`のまま使う
      - McRemote b10で起動（`Enabling McRemote v2320.0.0b10`、`Auth enforcement: true`、credential `HEALTHY`、catalog
        blocks=1166 hash `6d0f8524b70e37fb8d7b34d0fdb45c2b058dcfea82920d86ca9aaabb9fcadc83`）。WARN「config
        supported_mc_versions differs from the bundled declaration; hello uses [1.21.11, 26.3]. The configured value is
        preserved.」（このサーバーの`config.yml`に前の版の値が残っている）。マイクラ1.21.11でサーバーに入った
      - 手順2（Python rc1 ↔ McRemote b10）：`uv run python src/py_rc1/hello.py`で「Minecraft pairing required.」とコマンドが
        出て、マイクラで実行すると「ペアリング成功 / Paired.」。チャットに「Hello from Python rc1」、金のブロックが置かれた。
        `CatalogProjectionWarning`：「Catalog completion was not updated (stage=ignore): mc_constants.py is not safely
        ignored; run `mcremote init` in the project root, then retry. The Minecraft connection is ready and building can
        continue. ...」。試験用のフォルダーで`mcremote init`をしていないため。接続と建築は続いた（best-effort、
        `12-python-client/python-client-guide_ja.md`のとおり）
      - 手順3：`plugins/`のb10のJARを`.bak`にし、`mc-remote-2321.0.0rc1.jar`（315,352 bytes。b10のJARも同じbytes数）を置いて
        起動。`Enabling McRemote v2321.0.0rc1`、`Auth enforcement: true`、credential `HEALTHY`、catalogはb10と同じ
        blocks=1166、同じhash。`supported_mc_versions`のWARNはrc1でも同じ文で出た
      - 手順4（Python b9 ↔ McRemote rc1）：チャットに「Hello from Python b9」、シーランタンが置かれた。ペアリングは
        要らなかった。手順2（Python rc1、McRemote b10）のペアリングが、McRemoteをrc1に替えた後も、b9のclientからも使えたと
        読める（tokenをどこに保存しているかは確かめていない）
      - 手順5（Python rc1、`wirescope=True`）：端末に「WireScope attach code: 」とコードが出て、URLもリンクも出なかった
        （human owner「Pythonでコードは発行されるが、リンクがない」）。ブラウザは裏で`http://127.0.0.1:<空いているport>/`を開いて
        いたが、真っ白だった。`hello.py`は建てるとすぐ終わり、WireScopeも一緒に止まるため。最後に`input()`を足して終わらない
        ようにすると、ページは「stationの準備ができました。Python端末に表示された接続codeを入力してください。」、codeを入れて
        接続できた。ハンドシェイクは「1.21.11 · 23.2.1」、`supported_mc_versions ["1.21.11","26.3"]`、catalog hashはサーバーと
        同じ。通信フレームはhelloの送受信の2件だけで、送信のhelloは`{"protocol":"23.2.1"}`だけ（Scratchはclientの名前と版も
        送る）。チャットとsetBlockは接続の前に終わっていて、出なかった。`CatalogProjectionWarning`は手順2と同じ。attach code、
        WireScopeの表示IDは記録しない
      - 読み取り（coordinator）：短いscriptでは、WireScopeが開く前にprocessが終わり、白いページが残るだけになる。ブラウザが
        裏で開くので、気づきにくい。端末にURLが出ない
        human owner：「うまく行ったり、真っ白だったりすると思うので、嫌な動作だね。」
      - 手順6（Linux ZIP、Scratch rc1 ↔ McRemote rc1）：`2321.0.0rc1/`を`2320.0.0b10/`の隣に置き、`start-mc-remote.sh`を
        右クリック →「プログラムとして実行」で起動。同梱のfileの更新日は1980/01/01のまま（b10の見つかったことの4と同じ。
        human owner「更新日日付はそのままだな」）。設定画面は既定の「このPC」（`127.0.0.1`、25575）で、「改造版のScratchを
        開く」は保存するまで押せず、「接続先を保存してから、改造版のScratchを開いてください。」と出る。ペアリングして接続し、
        チャット、`world.setBlocks`（整地、軸）、`world.setBlock`、`player.getPos`／`setPos`／`setDirection`がどれも返った。
        独立のWireScopeは`http://127.0.0.1:8603`で通信が見えた
      - human owner：mc-remoteのブロックへパレットの中で頭出しすると、位置が微妙に下にずれる。ブラウザの表示を拡大縮小すると
        正常に戻る（Linux、Chrome 155）
      - 手順7（1.21.11での26.3の名前）：カタログピッカーは「取得済み — 1.21.11 · CACHE · 6d0f8524」。「ポプラ」は0件で
        「検索に一致するブロックがありません。」。「原木」は18件でポプラは無い。「金」16件、「door iron」2件（語を並べた検索も効く）。
        26.3にしか無いブロックは、1.21.11のサーバーではピッカーに出ない
    - Mac（2026-10-19、手順1〜6済み。Mac → UbuntuのLAN構成、Paper 1.21.11、McRemote rc1）：Mac mini（M1、2020）、メモリ8 GB、
      macOS 26.7.1（25G241）、Chrome 155.0.8059.85（arm64）
      - 手順2：macOSのZIP（266.2 MB）をmc-remote.comからChromeで取り、展開。警告なし。「ダウンロード」フォルダーのまま
        `はじめに.html`をダブルクリックし、Chromeで開いた。human owner：`はじめに.html`の中の「版番号のフォルダーで
        はじめに.htmlを開き、start-mc-remote.commandをダブルクリックします。」は、すでに開いて読んでいる人に「開き」と言っていて
        おかしい
      - 手順3：`start-mc-remote.command`をダブルクリックすると警告（「ゴミ箱に入れる」「完了」。human owner「捨てる人はいないとは
        思う」）。「システム設定」→「プライバシーとセキュリティ」の「このまま開く」は、かなり下にあってスクロールが要る。
        もう一度の警告（「ゴミ箱に入れる」「このまま開く」「完了」）で「このまま開く」、管理者のパスワードで「ターミナル」が
        開いた。案内の順と合っていた。続けて「“ターミナル.app”から“ダウンロード”フォルダ内のファイルへのアクセス権を
        求められています」が出て、「許可」で進んだ（`HOME/mc-remote/`へ移すのを忘れ、「ダウンロード」の中で起動したため）。human owner：既定にしている
        ターミナルが開いたほうが好ましい（b10の見つかったことの3と同じ）
      - 手順4：設定画面に「mc-remote Scratch 2321.0.0rc1」と版が出る。「LAN内の別のPC」でUbuntuのホスト名を入れて保存し、
        「設定を保存しました。改造版のScratchを開けます。」。保存の後、ランチャーの画面に`McRemote bridge listening on
        ws://127.0.0.1:8602`が2回目も出た（b10の見つかったことの4と同じ）。Scratchの製品noticeは「マイクラリモコンScratch
        クライアント mc-remote Scratch 2321.0.0rc1」、「詳細はGitHub.comのリリースページへ。」、リンク「リリースページを見る」
        「ホームページ」
      - パレットの頭出しのずれはmacOSのChromeでも出て、ズームを変えると直った
      - 「ブラウザに保存した作品」には、b10で保存した作品が出る（保存先は`127.0.0.1:8601`のブラウザなので、新しく入れても
        残る）。b10の`.sb3`を読み込んで使った
      - 手順5：ペアリングして接続。WireScope（`127.0.0.1:8603`）のhelloは送信`protocol 23.2.1`、client
        `scratch-mcremote 2321.0.0rc1`、受信`protocol 23.2.1`、`mc_version 1.21.11`。チャット、`world.setBlocks`（整地、
        軸）がどれも`result:null`で、マイクラに軸が建った
      - `mc-remote-scratch-LAN/`を`HOME/mc-remote/`へ移してダブルクリックすると、警告もアクセス権の確認も出ず、設定画面が裏、
        Scratchが表に開き、ペアリングなしで接続できた
      - 手順4の続き：設定画面は自動で開いた。`はじめに.html`の中の設定画面のURLはリンクで、押すと開いているタブが表に来た
      - 手順6：human owner：新鮮な目で見るのは難しいが、ずれてはいないと思う。ホームページのほうが整理されていて分かりやすい
    - 記録：`14-evidence/records/2026-10-19-rc1-candidate-3os-live-human_ja.md`（human ownerが照合）
    - 判定（2026-10-19、human owner）：**rc1は合格**。PythonのWireScope（processが早く終わると真っ白）は注意書きで扱う。
      LANパッケージの検証では初学者クラスを対象にしない（`2026-10-19-01`）
    - 公開の依頼：`00-hub/rc1-gate-release-instructions_ja.md`（2026-10-19）。feedbackの入口のIssueテンプレートは
      `.github/ISSUE_TEMPLATE/feedback.yml`（`2026-10-18-06`）。PythonのWireScopeの直す方向はhub NOTES 2026-10-19
    - McRemoteの公開（2026-10-19、coordinatorがGitHub APIとassetのdownloadで照合）：[v2321.0.0rc1](https://github.com/Naohiro2g/McRemote/releases/tag/v2321.0.0rc1)、
      title「McRemote 2321.0.0rc1 (Minecraft 1.21.11, 26.3)」、prerelease=true、draft=false、Latestは`v1.21.8-1.4.0`のまま。annotated tagの
      target `192a777ae1d484bcc9b58fcc7c58d6aed1a374af`で、`main`の先頭と同じ。`mc-remote-2321.0.0rc1.jar` 315,352 bytes／
      `917c358c201aa219277b96a447fb85116e8bdb0260870a4d76a8c51219d31c37`（凍結値と同じ）。`manifest.json`（schema v2）1,988 bytes／
      `e49761d22c8c60ac49915d04f1c6236ca101b13bf94b257c0cbcbb4328c6a1c2`は`release_tag`、`source_commit`、JARのdigestとbytes、対応版の
      宣言（`minecraft-targets.json` `8e830732…c361`）と、1.21.11 #132／26.3 #203の検証record 2件（PASS、各JSONのdigestがassetと
      一致）を持つ。Release本文にprotocol 23.2.1、23.2.0との接続、feedbackのフォームへのリンク。素材は
      `McRemote/handoff-materials/2026-10-19-rc1-prerelease/`
    - Pythonの公開（2026-10-19、coordinatorがGitHub APIとassetのdownloadで照合）：[v2321.0.0rc1](https://github.com/Naohiro2g/minecraft-remote-api/releases/tag/v2321.0.0rc1)、
      prerelease=true、draft=false、Latestは`v1214.10.11`のまま。tag（lightweight）のtargetと`main`の先頭はともに
      `c30105349ef26413e925699143396ea05bd3e380`。wheel 196,098 bytes／`5f12dfcf…44ca`、sdist 190,285 bytes／`dc8d9f30…5611`（どちらも全桁が
      凍結値と同じ）。`manifest.json`（schema v1）684 bytes／`c0f5ed68be519e0b40cfa6c890ff6a0aeed791422ca3db75f837ead36a6b8af5`は
      `source_commit`、`bundled_wirescope_source_commit` `6447f6e`、wheelとsdistのdigestが一致。Release本文に`wirescope=True`の注意書き
      （開始の直後と最後に`input()`で待つ例）とfeedbackのフォームへのリンク。main CI `39216669184`、Release workflow `39216950884`は
      PyPI.orgのjobがhuman ownerの承認待ち（TestPyPIは成功、担当報告）。素材は
      `minecraft-remote-api/handoff-materials/2026-10-19-rc1-python-release/`
    - PyPI.org（2026-10-19）：human ownerが承認し、Release workflow `39216950884`は成功。coordinatorがPyPIのJSON APIで
      [2321.0.0rc1](https://pypi.org/project/minecraft-remote-api/2321.0.0rc1/)のwheel 196,098 bytes／`5f12dfcf…44ca`とsdist 190,285 bytes／
      `dc8d9f30…5611`がReleaseと同じで、yankなしと確かめた。版を指定しないで入るのは`1214.10.13`のまま
    - toolingの公開（2026-10-19、coordinatorがGitHub APIとGHCRで照合）：[v2321.0.0rc1](https://github.com/Naohiro2g/minecraft-remote-tooling/releases/tag/v2321.0.0rc1)、
      title「mc-remote tooling 2321.0.0rc1」、prerelease=true、draft=false、Latestなし。annotated tagのtarget
      `6447f6e8cbfbeeb9d229990b5c4f6e82a5875666`で、`main`の先頭と同じ。asset：`wirescope-app.zip` 83,854 bytes／`da3da0b6…31ad`、
      `wirescope-app.manifest.json` 2,339 bytes／`3dd668a2…5235`、`bridge.oci.tar` 114,626,048 bytes／`39828764…c44c`（GitHubが計算した
      assetのdigestが凍結値と全桁で同じ）。GHCRの`mc-remote-bridge:v2321.0.0rc1`は`sha256:305d6e38…406acf`（凍結値と同じ）
    - Scratchの公開（2026-10-19、coordinatorがGitHub APIとGHCRで照合）：[v2321.0.0rc1](https://github.com/Naohiro2g/scratch-editor/releases/tag/v2321.0.0rc1)、
      title「mc-remote Scratch 2321.0.0rc1」、prerelease=true、draft=false、Latestなし。annotated tagのtarget
      `ec79b3b0e364e722d6926a0932eb4bf088ddd3a1`、`develop`の先頭は`f20e55eb53f192eab6cdc4f0d5aae4f52b2dc8db`（依頼どおり）。3 OSのZIP、
      `scratch-gui.tar.gz`、`contracts.tar.gz`、WireScopeのZIPとmanifestは、GitHubが計算したassetのdigestとbytesが凍結値と全桁で同じ。
      `manifest.json`（schema v2）2,320 bytes／`776e0d51a8d8db14cb5ace23f2a41f9d6a56e7eacb0a51e88463bd6bf076c68c`は`source_commit`
      `ec79b3b`、全fileのbytesとdigest、Scratch OCI `sha256:75e76edb…b840`、Bridge OCI `sha256:305d6e38…406acf`を持つ。GHCRの
      `mc-remote-scratch:v2321.0.0rc1`は`sha256:75e76edb6b8a1de4fb896184b5c26bed7cb1791296f82903e6b1ec4a1a5ab840`で、**凍結したOCIと
      同じdigest**（b9、b10では違った）。担当報告：作り直さず、凍結したartifactをCLIで昇格した（新しいActionsの公開runは無い）。
      OCIのversionラベルは`v2321.0.0rc1`に揃えた。mtimeの正規化は未実装で、凍結したOCIをそのまま転送したので公開物のmtimeも同じ。
      素材は`scratch-editor/handoff-materials/2026-10-19-rc1-release-scratch-tooling/`
    - 4 repoとPyPI.orgの公開がそろい、どのassetも試験したもの（凍結値）と同じbytes（2026-10-19）
    - human ownerの判断（2026-10-19）：park「Scratch OCIのversionラベルをcandidateと公開で揃える」を閉じる。ホームページを更新する
      （箱庭のrc1への切り替えはその後なので、箱庭に関わる表記はb10のまま）。候補の置き場所の中身は消してよい。gateを閉じる
    - 次の操作：close分類と候補の削除の依頼（`00-hub/rc1-gate-close-instructions_ja.md`）を各担当へ回す。返ってきたら、gateを閉じる
      ときのparkの確認（`2026-09-30-09`）をしてcloseをhuman ownerに諮る
    - ホームページの更新（2026-10-19、human owner：Pythonの例はrc1、Scratchのブロック一覧の入口はrc1、箱庭に関わる表記はb10のまま）：
      `/lan/scratch/`をrc1（版、3 OSのZIPのリンク、フォルダーの図、feedbackのフォームへのリンク）に。トップの現在地、ロードマップの
      rc1、対応表（McRemote、Python、WireScopeはrc1。ScratchはWeb版b10とLANパッケージrc1を並べる。箱庭の2行は変えない）、リリース
      履歴、Pythonカードの`uv add "minecraft-remote-api==2321.0.0rc1"`。API一覧はmetadataを23.2.1にし、`protocol.note`を外して
      `api/23.2.1/`を生成し、`api/`の入口を23.2.1へ（`api/23.2.0/`は残す。`--check` OK）。Scratchのブロック一覧は、scratch-editorの
      tag `ec79b3b`（site tree `5405380937b577491c85c710cb828a17303ec606`）の`site/2321.0.0rc1/`を`api/scratch/2321.0.0rc1/`へ取り込み、
      入口の`api/scratch/`をそのページと同じbytesにした（Scratchのsiteは、入口を今の版のページと同じbytesで作る。tagのsiteの入口は
      b10のままだった）
    - ホームページの公開（2026-10-19）：human ownerが同期し、coordinatorがトップ、`/lan/scratch/`、`/api/`、`/api/23.2.1/`、
      `/api/23.2.0/`、`/api/scratch/`、`/api/scratch/2321.0.0rc1/`など13 fileを外から取って、repo（`61afff7`）と同じbytesと確かめた
    - close分類（2026-10-19）：McRemote、Python、Scratchがknowledge `04c56b8`を読んで返した（McRemote
      `handoff-materials/2026-10-19-rc1-close/`、Python `handoff-materials/2026-10-19-rc1-python-release/`のclose分類の節、Scratch
      `handoff-materials/2026-10-19-rc1-close-inventory/`）。①はMcRemote 9 file、Python 10 file、Scratch 15 fileで、coordinatorが
      bytesとSHA-256で照合して`14-evidence/artifacts/2026-10-19-rc1-gate-close/`へ収容した（`14-evidence/records/2026-10-19-rc1-gate-close_ja.md`）。
      Stackの返却は下
    - Stackのclose返却（2026-10-19、knowledge `04c56b8`を読んだ）：候補の置き場所は2026-10-19 18:15:48 JST（09:15:48 UTC）に、
      版のdirectory（`candidates/2321.0.0rc1/`、その下の`set-1/`）ごと消した（Stackの手順書`docs/release-candidate-downloads-guide_ja.md`
      §4どおり）。残るのはCaddyのmount元の空の`candidates/`だけ。生成されたCaddyfileの`handle_path /candidates/*`と、Caddyのcontainerの
      読み取り専用のmountは残り、18:22 JSTにnoticeの更新でcontainerを作り直した後も同じ。coordinatorが外から、5 fileと`SHA256SUMS`の
      URLが404になることを確かめた。`handoff-materials`にrc1の期間のdirectoryは無い（最新は2026-10-08）。rc1の成果はStackの公開物
      （`/candidates/*`の経路、PR #73〜#75）、knowledgeへ返した`rollback-failed`の記録、backstage #25、#28にある
    - gateを閉じるときのparkの確認（`2026-09-30-09`、2026-10-19、coordinatorの案。human ownerの判断待ち）：
      | park | 案 |
      | --- | --- |
      | テックブログの1本目、下書きのfile名、feedbackの場所（2026-10-17） | ③はIssueのテンプレートを公開して済んだ（`2026-10-18-06`）。①②はhuman ownerの持ち越しのまま |
      | McRemoteの対応版を各系列の最終版へ広げる検討（2026-10-17） | 再開＝rc1の後で、今が時期。初回stableの対応版は1.21.11と26.3のまま（`2026-10-13-07`）にして、広げるかは初回stableの後に決める案 |
      | Windowsの生徒のPC（2026-10-17） | rc1は今のREADMEのまま出した。初学者はrc1の検証の対象にしない（`2026-10-19-01`）。生徒のPCの結果が届いたとき、または初回stableの前のWindowsの確認のときに再開 |
      | LANパッケージのランチャー、`はじめに.html`、Scratchの画面（2026-10-17） | ①はrc1に入った（macOSの手順が実際と合い、設定画面のURLはリンク。rc1の試験で確認）。rc1の試験の見つかったこと（3〜6、9）を足し、②③⑤とともに初回stableへ |
      | LANパッケージの教材の部分の収録（2026-10-13） | **まだ収録していない**。RCの間（初回stableまで）にknowledgeが`20-教材`へ収録する。gateを閉じた後の最初の作業にする案 |
      | 未生成chunkへの操作の制限（2026-10-07） | rc1から外した（McRemoteも賛成）。再開＝初回stableの後のAPI計画のとき |
      | 認証前の内部テーブルの較正（2026-10-07） | rc1は授業規模のloadをしていない。授業相当のloadを行うときのまま |
      | API一覧（2026-09-30） | `api/23.2.1/`を出した。クライアントAPI一覧へのつなぎ方は初回stableの後のまま |
      | public README／sample codeの人間向け再編（2026-08-28） | rc1ではPass Cを行わない（`2026-10-19-01`）。閉じる条件（初回stableでPass C）は、初回stableの前に見直す |
      | WindowsでのPython導入の2ルート（2026-09-28） | rc中に確認、のまま。human ownerの結果待ち |
  - 公開の後（knowledge）：API一覧の`api/23.2.1/`、ホームページの版の表示と`/lan/scratch/`のZIP、ブロック一覧の`2321.0.0rc1`。
    Stack：rc1のpreset、公開VPSの別セットへの切り替え（`2026-10-18-02`）は、リリースの作業を終えてから
  - feedbackの入口（2026-10-18、human owner）：knowledgeのGitHub Issuesに一つ置く（`2026-10-18-06`）。公開の前に、knowledgeへ
    Issueのテンプレートを置き、各componentのRelease本文とホームページからそこへつなぐ

## 2026-10-07 b10横断release gate（CLOSED）

- gate coordinator: knowledge担当session（Claude Code）。人間による明示handoffなしに他担当へ移さない
- human release owner: プロジェクトオーナー
- current phase: **CLOSED**（2026-10-17、human ownerの判断）。2026-10-07に開き、2026-10-14にpre-releaseとして公開、2026-10-17にhuman ownerが合格とした
- 目標日: b10 2026-10-17、rc1 10/24まで、初回stable 11/7（`2026-10-13-06`）。b10がpre-releaseでの試験で止まればb11を挟む
  （`2026-10-13-05`）
- release mode: 軽量mode（release運用と責務分担 §14、`2026-08-28-02`）。単一JARとケータリング型簡易版のZIPは新しい配布の形
  なので、その部分は§14の但し書きにより検証を強める（b9の移管と同じ扱い）
- contract: protocol `23.2.0`のまま、artifact `2320.0.0b10`。APIは変えない
  - b10の範囲: `2026-10-07-03`（tick分割、単一JAR、名前）、`2026-10-07-04`（ケータリング型簡易版）、`2026-10-07-05`
    （`mcr.build.blocks`の既定）、`2026-10-07-06`／`-07`（対応版の一覧の作り方、helloは同梱の宣言を正とする）、
    `2026-10-07-08`（release manifest v2）
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
      - 2026-10-13改訂（`2026-10-13-07`）：Paper 26.3がstableになったので、対象を1.21.11と26.3にする（26.2を置き換える）。
        26.2から26.3へコードの変更が要るときは、b10を26.2で出し、26.3はb11で入れる
    - 対応版の一覧（`2026-10-07-06`）：candidateのbuild前に対応対象を宣言し、同じJARで各対象を検証し、宣言とPASSの集合が
      一致することを公開時に確かめる。その一覧からhelloの`supported_mc_versions`の配布値、release title、本文を揃える
    - `mcr.build.blocks`の既定：configのトップレベル`default_build_blocks`（配布既定32768）。LuckPermsが無いときはこの値、
      LuckPermsがあってmetaが無いときは`0`。既存configの明示値は上書きしない（platform-design §8.2）
  - Scratch（toolingのBridgeを配布入力にする）:
    - ケータリング型簡易版：標準からDocker、証明書の設定、Stackのpreset／orderを除いたもの。Scratch、Bridge、実行環境、
      ランチャーをOS別のZIP（Scratch Local版）にまとめ、1台構成とLAN構成に対応する。認証はON。
      `mc-remote-scratch-local-2320.0.0b10-{windows-x64,macos-arm64,linux-x64}.zip`をScratchのrelease `v2320.0.0b10`の
      assetとし、公開releaseの`manifest.json`（`mc-remote.release-manifest` v2、`2026-10-07-08`）へrole `scratch-local`、
      kind `https-file`、`os`、`arch`、`bytes`で載せる。サーバー側はMcRemote READMEのクイックスタートへ案内する
    - 公開するZIPと同じSHA-256でWindows 11、macOS、Linuxを検証し、構築の手順と運用で要る調整（OSの警告、firewall、接続先、
      ペアリング）を観察して記録する。Windowsは、SmartScreenの個別許可と、アプリ単位の許可が無いSmart App Controlを分けて
      観察する。署名・公証の要否はこの結果で判断する。同梱物のライセンスは`2026-08-11-01`の配布前確認を通す
  - Stack（2026-10-07からhuman ownerの直接管理を解き、担当sessionへ渡す。releaseからのdeploy手順の完成度が上がったため）:
    単一JARの名前の変更（tagとJAR名にMinecraft版を入れない）と、`mc-remote.release-manifest` v1へ足すfield（McRemoteの
    `minecraft_compatibility`、Scratchの`os`／`arch`と同じroleの複数artifact）を、Stackの収集とdeployの手順が受け入れるかを
    確かめる。受け入れないならv2へ上げるかを返す。2026-10-07の回答（`main@f9b558769375cf704e3bf55c6aa3db93bb2aa3cf`）：名前の
    変更は受け入れる（tagやJAR名から版を読まず、deployするMinecraftの版はpresetの明示値で選ぶ）。追加fieldと同じroleの重複は
    v1のparserが拒否するので、v2を提案した。b10ではv1とv2の両方を読む実装を行う（`2026-10-07-08`）
  - minecraft-remote-tooling（Scratch担当）: release manifest v2のJSON Schemaの正本を置く（`2026-10-07-08`）。下のたたき台の
    reviewが済んでから書く。producerとconsumerが固定版を使う方法（tooling-lockのcommitか、toolingのrelease）を確認票で返す
  - 不参加: Python（APIが変わらず、簡易版の案内先もMcRemote README。manifest v2へは次のreleaseで移る）
  - McRemote（2026-10-07に追加）:
    - FASTのparticleが負荷のもとで黙って描かれない件：particleのnotificationがwork不足で消費されたときだけ数える理由を1種、
      認証前と同じ集計に足す（軽く済むとの回答を受けてb10に入れた。認証前の10理由の意味は変えない）
    - 「LuckPermsの使い方」の案内：LuckPermsを入れるとmeta（`mcr.build.range`、`mcr.build.blocks`）が無いplayerは建築も
      setBlocksもできなくなる。入れた途端に何もできなくなった、を防ぐため、metaの設定手順を短い案内にまとめる。置き場所は
      McRemoteが提案する
    - release manifest v2の生成（`minecraft_compatibility`を含む、`2026-10-07-08`）
- release manifest v2の形（`2026-10-07-09`。McRemote、Scratch、Stackのreviewを突き合わせて確定）:
  - versionで分ける：`schema_version`を見て固定したv1またはv2のschemaで文書全体を検査する。知らないversionと知らない
    fieldは拒否する。v1の規則と挙動は変えない。不正なv2をv1として読み直さない
  - top-level：`schema`（`mc-remote.release-manifest`）、`schema_version`（`2`）、`release_tag`、`source_commit`、`artifacts`。
    v1の任意field `bundled_wirescope_source_commit`（小文字16進40桁）はv2でも任意で残す。`minecraft_compatibility`は下記
  - 全artifact：v1の任意field `artifact_version`（空でない文字列）を残す。ociのartifactはほかを変えない
  - https-fileのartifact：`role`（文字列。roleの語彙をschemaで列挙しない）、`kind`（`"https-file"`）、`file`（空でない文字列。
    同じReleaseのasset名。名前から`os`／`arch`を推定しない）、`sha256`（小文字16進64桁）、`bytes`（必須、0以上の整数。公開する
    fileの生のbyte数）、`os`（`windows`／`macos`／`linux`）と`arch`（`x64`／`arm64`）は任意で、付けるなら両方。片方だけ、
    `null`、空文字、別表記（`amd64`など）は拒否する
  - artifactの鍵：`(role, os, arch)`。`os`／`arch`の無い項目は`(role, なし, なし)`。ociを含む全artifactの間で鍵の重複を拒否する
    （fileやhashが違っても同じ鍵なら重複）。一つのroleの中で`os`／`arch`のある項目と無い項目を混ぜない
  - `minecraft_compatibility`：artifactsにrole `jar`があるv2で必須（producerの名前やtagから判断しない）
    - `declaration`：`path`（manifestの`source_commit`の時点のproducer repoの相対path。McRemoteは`release/minecraft-targets.json`）、
      `sha256`（そのfileの生のbyte列）、`minecraft_versions`（空でなく重複の無い文字列の配列。fileの内容と一致）。producerは
      JARに同梱した宣言とbytesが一致することも確かめる
    - 宣言fileの形（2026-10-08に追記、human owner「objectを正とする案でOK」）：rootはobjectで、`schema`
      （`mc-remote.minecraft-targets`）、`schema_version`（`1`）、`minecraft_versions`（空でなく重複の無い文字列の配列）を持つ。
      知らないfieldと裸の配列は拒否する。照合は`minecraft_versions`の値、fileの生のbytesのdigest、JARに同梱した宣言のbytesの
      一致で行う。McRemoteの提案と実装の形で、manifestと同じくversionで知らない形を検出できる
    - `verifications[]`：宣言した版ごとにちょうど1件。`minecraft_version`、`paper_build`（1以上の整数）、`server_sha256`、
      `java_version`（実測したruntimeの版の文字列をそのまま。例 `21.0.12.1+1-1-24.04.4-Ubuntu`）、`jar_sha256`（`jar`の
      sha256と一致）、`result`（`"PASS"`だけ。失敗や未実施はcandidateの記録に残し、公開manifestには載せない）、
      `record`（`{file, sha256}`。`file`は同じReleaseのassetのbasenameで、pathや外部URLを含めない。recordは`artifacts`には
      載せず、`verifications`からだけ参照する）。Paper以外のserverを足すときは、文字列に詰めず新しいfieldかversionで扱う
  - schemaで表せない検査（鍵の重複、roleの中の混在、宣言とverificationの版の集合の一致、`jar_sha256`の一致、recordと
    宣言fileのdigest照合）は、producerとconsumerの両方が文書全体の整合性検査として行う。toolingに受入と拒否の共有fixtureを
    置き、言語ごとの判定の差を確かめる
  - consumer：1件だけのrole（`scratch`、`bridge`、`jar`など）はちょうど1件と期待するkindを要求する。変種のあるroleは
    呼び出し側が`os`と`arch`を明示して1件を選び、該当0件・複数件・指定不足は拒否する。別のOSやarchへfallbackしない。使わない
    roleは選ばず取得もしないが、文書全体の検査は省かない。deployするMinecraftの版はpresetで明示し、対応集合への包含を確かめる。
    presetのPaper build、server JARのSHA、Java runtimeがverificationの構成と違う場合は「検証済み」とせず、coordinatorへ返す
    （どの観測を引き継げるかはcoordinatorが決める）
  - JSON Schema：Draft 2020-12で、toolingのroot `schemas/release-manifest-v2.schema.json`に置く。共有fixtureも同じcommitに置く。
    取得は固定のGit commit、path、bytes、SHA-256で行い、実行時に`main`やremoteを取りに行かない。schema用のlockはBridge／
    WireScopeのlock（`mc-remote/tooling-lock.json`）と分ける（Scratch案は`mc-remote/release-manifest-lock.json`）。lockの置き場所は
    各repoが決め、同じcontract commitとfileのhashを記録する
- 範囲に入れないもの: 未生成chunkの制限（hub NOTES 2026-10-07の候補）、新しいmethodやclientのjob／progress API
- gateを開くときのpark確認（`2026-09-30-09`、`tools/list-reopen-conditions.py`）: b10に結びつく2件を拾った。
  setBlocksのtick分割はMcRemoteの範囲として着手する。FASTのparticleが負荷のもとで黙って描かれない件は、b10の範囲に入れず、
  消費した件数を認証前と同じ理由別の集計に足す程度で軽く済むかをMcRemote担当に聞く（軽く済まなければ初回stableの後へ送る）。
  rc1に結びつく行（製品notice、OCIのversionラベル、API一覧、rollback、README再編、block value投影の残り、未生成chunk、
  認証前テーブルの較正）はrc1 gateで見る
- 進捗（2026-10-07）:
  - McRemote `main@ce1e08a8e749c60ba1ea5cf4f2a63462bd6ecb10`：`default_build_blocks`を実装（313 tests PASS、担当報告）。
    LuckPermsがあってmetaが無いplayerは`0`になる
  - McRemote Paper 26.2のexact build：build 132（2026-10-06、server JAR SHA-256 `5ab560a769c1ab413cb7f637dd0dc697974571f2db0a667cfbac511422e51b26`、
    APIの宣言値）。metadataの取得だけで、JARのdigest照合とpulseはまだ
  - McRemote setBlocksのtick分割：着手前の整理を受け、着手を許可した。開始前に予算がまったく無ければ副作用前の`backpressure`
    （FASTはFIFO先頭で延期）。一度施工を始めたら`backpressure`を返さず次のtickで同じ要求として続け、全量の後に`result:null`を
    1回。途中のPaper例外やworldの失効は`internal_error`で終え、自動retryしない。施工済みの部分は残し、rollbackしない。切断で
    残りを止める。予約したworkは失敗しても戻さない。1接続で途中のjobは1件、tickごとに巡回の開始位置を回す
  - McRemote単一JARの宣言：tracked `release/minecraft-targets.json`（object。対応版は`minecraft_versions`の`["1.21.11", "26.2"]`。
    形は下の「release manifest v2の形」）をbuild前に固定し、同梱resource、
    configの配布既定、title、本文をここから作る。検証素材はJARのdigestで結ぶ。既存configの`supported_mc_versions`は、hello
    では同梱の宣言を正とし、値は書き換えず、違えばwarningを出す（`2026-10-07-07`）
  - McRemote `main@bd1ce15d90dc14dc59b23441df8677bed021a897`（担当報告、unit／deterministicと隔離ローカルPaperでのlive-auto。
    live-humanは無し）：setBlocksのtick分割、単一JARと同梱の宣言、helloの宣言、particleの集計
    （`PARTICLE_NOTIFICATION_WORK_BACKPRESSURE`）、READMEの「LuckPermsを入れたときの設定」（`mcr.online`、`mcr.build.range`、
    `mcr.build.blocks`をgroup defaultへ設定する例。LuckPermsでの実地試験は未実施）。Java 325 tests、Python 21 tests PASS。
    同じJAR（282,260 bytes、SHA-256 `60ca6e17fb89ed8474e2341d710c23ab62f4ddfd366c49afc1d233f6526c3ef7`、class major 65）を
    Paper 1.21.11 build 130（Java 21）と26.2 build 132（Java 25）で、認証済みhello、宣言、catalog、block、sign、entity handle、
    events.poll、particle／chat、32768のtick分割、FASTとflush、通常再起動の後のread／writeまで確認した。宣言のSHA-256は
    `a202a11a104767c289266f4baf7692d499ed15b717dd4d5a31eca48abc17ca26`。初回の26.2のrunで、bulkの完了直後のsign setterが副作用前の
    `backpressure`を返し、runnerをそのreasonだけ有限回待つ形へ直した。初回のtargeted unitで既存のparticle self receiverの
    caseが1回だけFAIL（receiversがnull）し、再実行と全325 testsでは再現せず、原因は特定されていない。公開candidateとmanifest
    v2の生成はまだ
  - Scratch `agent/b10-scratch-local`（親`271d1ca4ba5374b8f2a370666cf7ecaaabf0d206`、未commit、担当報告）：3つのOSの試作ZIPを
    生成した（`working_tree_dirty`で公開identityではない）。Linuxで実際のランチャー、HTTP配信、固定Bridge（tooling
    `dc1ab83`のOCIから`/app`を取り出し、同梱Node 24.19.0で起動）、模擬peerとのhello往復、終了が通り、対象tests 591件が
    PASS。HTTPとWSは127.0.0.1だけで待ち受け、設定はhostとportだけでtokenを保存しない。toolingの新しいreleaseは要らない。
    同梱物のライセンスinventory 3,363件のうち、LICENSE本文が見つからない135件の分類が残る。manifestはv2の形の確定待ち。
    Windows 11とApple Silicon Macはhuman ownerの手元にあり、最終ZIPを固定してから実施票で案内する
  - minecraft-remote-tooling `agent/b10-release-manifest-v2@fb6880b192a0063241f95c44a5fa6b836f5e7394`（2026-10-08、Scratch担当、
    remoteのbranch targetと一致を確認。mainへの統合はまだ）：`schemas/release-manifest-v2.schema.json`（5,654 bytes、SHA-256
    `537684f063c5604ccb1e99a69fed51a16a73ef6e88c71ee85a410ab6f5ff5b4c`）、共有fixture `schemas/fixtures/release-manifest-v2.json`
    （66 case、受入8・拒否58、112,472 bytes、SHA-256 `757d1b7661ca1c65b071253ef95161730b1050df85c4f6be6299905823a15a26`）、
    整合性検査のreference `schemas/release-manifest-checks.mjs`、回帰用にStackのv1 schemaをbytesのまま収容。tooling 280 tests、
    owner test 67件PASS。fixtureのMinecraftの値は合成で、実機の証拠ではない
  - Scratch（未commit、担当報告）：schema用の`mc-remote/release-manifest-lock.json`で上のcommitを固定し、公開manifestをv2にした
    （OCI 2件、https-file 6件。scratch-local 3件と既存3件に`bytes`）。74 tests PASS。公開b9のmanifestをv1として読めることも
    確かめた。Bridge／WireScopeの`tooling-lock.json`は`dc1ab83`のまま。試作ZIPは旧snapshotのままで、最終ZIPは今後のcommitと
    candidateから作る。3つのOSでの検証は、McRemoteとStackのv2実装が済んでから行う（human owner 2026-10-08）
  - 2026-10-08：toolingの`fb6880b`をmainへfast-forwardで統合した（CI成功）。McRemote `main@d0c548f`（v2の生成と固定素材の
    取り込み、Python 47 tests、共有fixture 66件PASS）とStack `8e3b0b1`（作業branch。v1・v2の読み取りと選択、presetの構成が
    verificationと違えば`release_manifest_foundation_unverified`、pytest 511件PASS）が、宣言fileの形の食い違いを返した：
    toolingのreference、README、fixtureは宣言fileを裸の配列として扱い、McRemoteの実際のobjectを内容の段階で拒否する。
    knowledgeの記録がrootの形を決めておらず、進捗の欄の略記が配列のように読めたことも一因。objectを正とし、toolingの
    reference、README、fixtureを直して出し直し、McRemoteとStackが固定し直して照合する
  - 2026-10-08：toolingの修正版`main@5f567f14adaa24603e9dee3c0ec9909d428b7c4b`（reference、README、共有fixture 85件。schema本体は
    不変。coordinatorが変更4 fileのbytesとSHA-256を照合）。McRemote `main@8f76574e2185b5b502e186d15e4b553ad0912da0`とStack
    `agent/b10-manifest-v2-consumer@2eaf41bee5f11c361b0fe7bb53cdbcf966e39be7`が固定し直し、共有fixture 85件の判定が全件一致し、
    `bd1ce15`の実際のJAR、宣言、版ごとのrecordでmanifest v2の照合がPASSした（McRemote 49 tests、Stack 542 tests）。宣言fileの
    形の食い違いは解消した。どちらも`bd1ce15`の観測をそのsourceのまま使い、新しいcommitのPASSへ付け替えていない
- 次の操作（2026-10-08、human owner「その案でOK」）:
  - McRemote：最終のsourceからCIでcandidateを作り、JARのSHA-256を見る。`bd1ce15`の後の変更はrelease scriptとlockだけで
    Javaは変えていない（担当報告）。CIのJARがpulseで試したJAR（`60ca6e17fb89ed8474e2341d710c23ab62f4ddfd366c49afc1d233f6526c3ef7`）と
    同じbytesなら、両方の版のpulseを引き継ぐ。違えば新しいJARで1.21.11と26.2のpulseをやり直す。tagはまだ打たない
  - Scratch：実装をcommitし、ライセンスの残り135件を分類して、CIでcandidateを作り、3つのZIPのSHA-256を固定する。固定できたら
    coordinatorがWindows 11、macOS、Linuxの実施票を出す。日程上いちばん時間がかかるのはこの後の人の操作なので急ぐ
  - Stack：作業branchのまま置き、mainへはb10のclose（default branchへの統合の確認）で入れる
- 進捗（2026-10-09）:
  - McRemote candidate：最終source `main@8f76574e2185b5b502e186d15e4b553ad0912da0`のCI（run `37802721957`、success、artifact ID
    `11561402977`）のJARは、pulseで試したJARとbytesまで同じ（282,260 bytes、SHA-256
    `60ca6e17fb89ed8474e2341d710c23ab62f4ddfd366c49afc1d233f6526c3ef7`、ZIP entryの内容・属性・順序も一致）。宣言もbytesが同じ。
    そこで`bd1ce15`での1.21.11と26.2のpulseと通常再起動の観測を引き継いだ（新しい実行はしていない）。版ごとのrecordは、root
    の`source_commit`をcandidateの`8f76574`、`observations`を観測時の`bd1ce15`のままとし、`observation_reuse`に引き継ぎの根拠を
    書いた。manifest v2（`minecraft_compatibility`と2件のPASS）を作り、固定schema、共有fixture 85件、Pythonとtoolingの
    referenceで検証してPASS。tagとReleaseはまだ
  - Scratch candidate：`agent/b10-scratch-local@c717d0c2ed9b045b8c3bb925b0e1fcd8ee33010b`のCI（run `37808012407`、success、artifact
    ID `11563852835`、外側ZIPの`sha256:75b1df3df6d659514ee6eb3a2913a7d9bf6e062a449316c352e9a59078a89aea`）で3つのZIPを固定した
    （全て`working_tree_dirty:false`）：
    - `mc-remote-scratch-local-2320.0.0b10-windows-x64.zip` 260,361,934 bytes、`08340c801c1196c30a1227a7e495feb32131a95e4816ffbb29278557cadab9c1`
    - `mc-remote-scratch-local-2320.0.0b10-macos-arm64.zip` 264,713,598 bytes、`60d69479079eb5f7b7022547d417abc5dc31b237eb12766354885e4db53e6908`
    - `mc-remote-scratch-local-2320.0.0b10-linux-x64.zip` 269,950,028 bytes、`245d83aeab8f6a10bc3703547e0f897b3e82a8c9152c1a131378454f0debdf8b`
    手元の対象tests 687件PASS。CIでLinuxのZIPを日本語と空白を含むpathに展開し、模擬peerとの往復まで確かめた（実際の
    Minecraft、ペアリング、OSのダウンロード警告は未確認）。ライセンスは最終のCI入力130件（runtime 26、buildのみ104）を
    分類し、runtimeの26件は本文とnoticeを補った。未確定が1件：`microee 0.0.6`の原表記は「BSD」で、条項数の分かる原本文が
    見つからない（BSD-3-Clauseの標準本文を参考として収め、ライセンスを読み替えたとはしていない）
- 次の操作（2026-10-09、human owner「案A、ライセンスそのままで」）:
  - 3つのOSの人間参加試験（live-human）を、上の固定した3つのZIPとMcRemote candidateのJARで行う（実施票は
    `00-hub/b10-gate-live-test-instructions_ja.md`）。取得はGitHub Actionsの
    run `37808012407`のArtifactsから各PCのブラウザで落とし、中の該当ZIPを取り出して、SHA-256を照合してから始める。外側の
    artifactから取り出す一手間は本番と違うので、公開した後にReleaseのassetで初回の警告だけ短く見直す
  - `microee 0.0.6`は、原表記の「BSD」と参考として収めたBSD-3-Clauseの標準本文をnoticeに明記したまま出す（置き換えない）
- 初回のlive-human（2026-10-09、human owner。正式なrecordはまだ）:
  - Windows 11、Paper 1.21.11：ランチャーは警告なく起動。ペアリングのcodeが出て承認されるが、Scratchの接続が完了しない。
    serverのlogは、snapshotとauthority manifestが無いので新しいcredential domainを作り始め、途中でfail closedして
    `UNHEALTHY`。認証OFFにすると接続でき、hello worldも通った（認証ONの試験の成功には数えない）。実際に使ったJARの
    SHA-256、OSとPaperの正確な版、Smart App Controlの状態は採れていない
  - macOS（Apple Silicon）、Minecraft 1.21.11：最初にLinux用のZIPのNodeを実行して失敗（OSの取り違え）。macOS用では警告なく
    起動し、ペアリングに成功、`Hello, Minecraft!`まで通った。版やhashは採れていない
  - Windowsとmacの両方で、独立WireScopeへのリンクが出ない。Scratch担当の静的点検で、3つのZIPのどれにもWireScopeが入って
    おらず、`wirescope_url`も無いと確認（`2026-10-07-04`で中身にWireScopeを書いていなかった抜け）
  - Windowsの原因候補（McRemote担当の静的点検、`McRemote/handoff-materials/2026-10-09-b10-windows-credential-investigation/`）：
    credential storeの`forceDirectory`が`FileChannel.open(directory, READ)`でdirectoryを開いて同期する処理が、Windowsでは
    できない（directoryを開くのに要るflagをJavaが付けない）。初回起動でauthorityのdirectoryを作った直後、その親の同期で
    止まる。logとは整合するが、Windows実機のstack traceはまだ無い。この処理はsnapshotの書き込み、authorityのmanifest、
    revokeのtombstoneにも使うので、初回起動だけを通しても直らない。platform-design §9.3（directoryの同期をrevokeの確定点
    とする）と§9.4（永続化してから成功を返す）があるので、Windowsで同期を飛ばす・例外を握りつぶすのは契約違反になる
  - Windowsの原因の確定（2026-10-09、human ownerがWindows 11で診断。Microsoft Build of OpenJDK `21.0.12.1+1-LTS`、実際に使った
    JARはcandidateと同じ`60ca6e17fb89ed8474e2341d710c23ab62f4ddfd366c49afc1d233f6526c3ef7`）：`DirectoryForceProbe`
    （`14-evidence/artifacts/2026-10-09-b10-live/mcremote/DirectoryForceProbe.java`、SHA-256
    `4d9c9abda5059ac73f1b85b22a4bec0dbff9058cf74b1db01c0d783563c2302c`）が、`stage=open-directory-read`で
    `java.nio.file.AccessDeniedException`（`WindowsFileSystemProvider.newFileChannel`）になった。Windowsでは
    `FileChannel.open(directory, READ)`でdirectoryを開けず、静的点検の原因候補のとおり
- 次の操作（2026-10-09、human owner「はい」）:
  1. human owner：Windowsで診断（`00-hub/b10-gate-live-test-instructions_ja.md`の「Windowsの診断」）を実行し、原因を確かめる
  2. McRemote：Windowsでの永続化の方式の案を出す（§9.3と§9.4を満たす方法。Windows固有の永続化の手段か、§9.4が許す別の
     backend）。あわせて、失敗した操作名、例外の型、cause chainを起動logに出す（credentialの値は出さない）。案をcoordinatorが
     §9と突き合わせ、human ownerが決める。Windowsの問題はb10の範囲に入れる（認証ONは実施の条件）
  3. Scratch：独立WireScopeを同梱した新しいcandidateを作る（`2026-10-09-01`）
  4. 3つのOSの試験は、McRemoteとScratchの新しいcandidateがそろってからやり直す。初回の観測は新しいcandidateに引き継がず、
     問題を見つけた記録として残す。実施票は2段の取得、ランチャーの場所、JARの取得先、始める前に採る項目を足して直した
- Windowsの永続化の方式（2026-10-09、`2026-10-09-02`）：McRemoteの比較票（ESE、SQLite、Win32のfile API）を§9.3・§9.4と突き合わせ、
  human ownerがWindowsに限るSQLiteのbackendを選んだ（platform-design §9.4の追記）。Xerial SQLite JDBCをJARに同梱し、Windowsの
  旧fileは読まず、移行も退避もしない。CIのWindows runner（Java 21と25）で、commitの前後で子JVMを止める試験まで行い、そのあと
  Windows 11の実機で認証ONの接続、再起動、revokeを確かめる。電源を落とす試験はしない
- 進捗（2026-10-09）：Scratch `agent/b10-scratch-local@ec29372dadac9c51b2812c746e72032d48d987b6`のCI（run `37933218014`、
  artifact ID `11616819485`、外側`sha256:f747f3b537b060aacfa24bbcdbc1e42575169d7cd11b5d3219fdb6a7c0767159`）で、独立WireScopeを
  同梱した3つのZIPを作った（Windows `f9d09ee84eb8cc54324c6b9d83dc3ab9371d7592ec0535346cf527d3db931a77`、macOS
  `16e20e5b2ecbfe1a7070d18f3700739bf2d4d567920347398e7ff82d1a40edc0`、Linux
  `3717f4dd55c0996c8e35ce121f293b06ed78e1a1c1bd7e4dad8c1a297fc186fc`）。固定済みの共通WireScope（`da3da0b6…31ad`）をそのまま
  同梱し、別のloopbackのport（8603）で配信する。CIのLinuxの試験で、日本語と空白を含むpathでの起動とWireScopeの配信まで
  確かめた。3つのOSの試験は、McRemoteのWindowsの修正版がそろってから行う
- 進捗（2026-10-09）：McRemote `main@61ba5398a61c4f545b1ff780adf2dc3cad429f46`でWindowsに限るSQLiteのbackendを実装した（担当報告。
  remoteのmainの一致はcoordinatorが確認）。CI run `37943254478`（3 OS × Java 21／25、全job success）、artifact ID `11622727242`。
  JARは12,320,559 bytes、SHA-256 `9902507a3b3f92459da1dbcf9621059425de8966a50289c080aee14a0f9ed7d2`（Xerial SQLite JDBCとそのnative
  library、ライセンスを同梱。手元のfileでcoordinatorがSHA-256を照合）。宣言は不変（`a202a11a…ca26`）。旧JARのpulseは引き継がず、
  新しいJARでPaper 1.21.11 build 130（Java 21）と26.2 build 132（Java 25）のpulseと通常再起動を認証ONでやり直してPASS。
  manifest v2の検証もPASS。Windowsは既定で`credential-store/snapshot.json.sqlite`と`credential-revocations-sqlite/authority.sqlite`を
  使い、旧JSONは読まない。Windows 11の実機での確認はまだ
- 次の操作（2026-10-09）：実施票`00-hub/b10-gate-live-test-instructions_ja.md`の「使うもの」をScratch `ec29372`とMcRemote
  `61ba539`のcandidateに差し替えた。human ownerが3つのOSで試験をやり直す。Windowsでは、サーバーの通常の再起動の後に
  ペアリングし直さずに再接続できるか（認証情報が保存されているか）を確かめる。revokeは実機では行わず、CIのWindows
  runnerの結果に任せる（revokeに特有の論理はCIで確かめ、実機の環境の影響はペアリングと再起動で同じDBの書き込みと読み直しを
  通るので見える）。Minecraftサーバーのフォルダは、OneDriveなどのクラウド同期の対象に置かない（human owner 2026-10-09「同期
  対象にすべきではない」。試験のWindowsのサーバーも同期の対象ではない）。McRemote READMEのWindowsの保存先の説明に、この
  注意を1行足すようMcRemoteへ依頼する
- Windowsの実機（2026-10-10、human owner、McRemote `61ba539`）：認証ONで動作した。途中、Windowsセキュリティの「スマートアプリ
  コントロール」と「メモリ整合性」をオフからオンへ変えたとき、一度認証できなくなった。その後は両方オンでも動き、原因は分からない
  （hub NOTES 2026-10-10のpark）
- 依存の方式の見直し（2026-10-10、`2026-10-10-01`）：human ownerの指摘でPaperが同梱するSQLiteを調べ、Windows実機の比較でPaper版
  3.49.1.0もJava 21／25でロードとJNIの初期化に成功した。SQLite JDBCはPaperが提供するものを使い（Xerialの同梱をやめる）、保存の
  方式を全OSでSQLiteに揃える。旧fileのtokenは引き継がない（公開の利用者はsession tokenしか持たない）。McRemoteが再実装して新しい
  candidateを作り、b10のまま進める（b11へ送らない）
- 次の操作（2026-10-10）：
  - McRemote：`2026-10-10-01`のとおり再実装する。Paperのdriverを実際に使っていること（classの出所とengineの版）を確かめられる
    ようにし、JARに`org/sqlite`のclassやnative resourceが残らないことを確かめる。起動・停止・再初期化で同じDBへの接続が重ならない
    ことを試験する。Linux、macOS、Windowsで、fileしか無い環境での新しいdomainの初期化と、SQLiteのDBがある環境での継続を
    確かめる。CIで新しいcandidateを作り、Paper 1.21.11 build 130（Java 21）と26.2 build 132（Java 25）のpulseと通常の再起動を
    やり直し、使ったSQLiteの出所と版を返す。manifest v2を作り直す
  - 3つのOSの試験は、McRemoteの新しいcandidateがそろってから、Scratch `ec29372`と組み合わせてやり直す。Windowsは通常の起動、
    ペアリング、サーバーの再起動の後の再接続を確かめる。実機のrevokeは引き続きCIに任せる
- 進捗（2026-10-10）：McRemote `main@56af9389d1a688ed5ba88df7512b008499d75d7d`で`2026-10-10-01`を実装した（担当報告。remoteの
  mainの一致とJARのSHA-256はcoordinatorが確認）。CI run `38033919529`（全job success）、artifact ID `11663343578`。JARは
  315,352 bytes、SHA-256 `bed7508603d849d92b37ff38ee6e6bba29b65ff503ec3fb4a12f2298ce07ada1`で、`org/sqlite`のclassとnative
  resourceは0件（coordinatorも確認）。宣言は不変。両方のPaper（1.21.11 build 130とJava 21、26.2 build 132とJava 25）で、Paperの
  `sqlite-jdbc-3.49.1.0.jar`（engine 3.49.1）を使い、認証ONでpulseと通常の再起動がPASS。同じDBへの接続は、DBのpathごとの
  lockで接続を開く前からcloseまで重ならないようにした。旧candidate（Xerial 3.53.4）で作ったSQLiteのDBとsessionを、新しい
  candidateがPaperの3.49.1で続けて使えることも確かめた。manifest v2を作り直して検証しPASS。READMEにSQLiteの説明、
  再ペアリング、クラウド同期の注意を入れた。実施票のMcRemoteの欄を差し替えた。3つのOSの試験はこれとScratch `ec29372`で行う
- 3つのOSの試験（2026-10-11〜12、Scratch `ec29372`とMcRemote `56af938`、record
  `14-evidence/records/2026-10-12-b10-scratch-local-3os-live-human_ja.md`）：動作はPASS。ただし実施票はdogfoodingの視点を欠き
  （ターミナルからの起動、CIの一括artifactからの取得）、ランチャーの体験は「OSSの利用者向けには遠い」（human owner）。体験の
  目標と検証の範囲を`2026-10-12-01`で、Javaの管理を`2026-10-12-02`で決めた
- 決定（2026-10-13）：呼び名をScratch LANパッケージ、ZIPを`mc-remote-scratch-LAN-<version>-<os>-<arch>.zip`に改めた
  （`2026-10-13-02`）。置き場所（`2026-10-13-03`）と取得から更新までの設計は`13-scratch-client/scratch-lan-package-design_ja.md`。
  b10は各releaseをGitHubのpre-releaseで作って試し、通れば公開、止まればb11（`2026-10-13-05`）。release manifest v2の
  role名`scratch-local`は機械用の識別子なので、変えるかはScratch担当とtooling担当に聞く
- 次の操作（2026-10-13）：
  - Scratch：次のcandidateに、Scratch LANパッケージの設計（名前、置き場所、最上位のもの、設定画面、`はじめに.html`）、
    拡張機能のカードのPNG化、カタログピッカーの説明の見直し、Windowsのネットワークを「プライベート」にする案内を入れ、
    pre-releaseのb10として出す
  - McRemote：26.2から26.3への静的点検（コードの変更の要否）。対応版の一覧を1.21.11と26.3にしたcandidateを作り、
    同じJARで両方のpulseを通す（`2026-10-13-07`）
  - coordinator：Scratch LANパッケージの設計 §8に沿って実施票を作り直し、human ownerが3 OSでやり直す（Minecraftサーバーは
    1.21.11と26.3）
  - サーバーの再起動の後に接続の表示が残る問題（hub NOTES）：「b10はこのまま、初回stableの後に考える」は中間判断で、
    見直し中。方向は利用者の操作なしに復帰すること。体験の仕様を先に決める（human owner 2026-10-12）
- 進捗（2026-10-13、McRemote、`2026-10-13-07`）：静的点検で、26.3（STABLE build 178）のAPIに対して全main sourceのcompileが通り、
  コードの変更は要らないと判断した（`ParticleBuilder.extra(double)`と`Sound.getKey()`に削除予定の非推奨警告。将来版への対応は
  McRemoteが追う）。McRemote `main@17bcf2645c112133935bc9d993d4fdd4669ceb98`で対応版の一覧を`["1.21.11", "26.3"]`にした（remoteの
  mainの一致はcoordinatorが確認）。CI run `38347345527`（全7 job success）、artifact ID `11789398049`。JARは315,352 bytes、SHA-256
  `96ddf09f765a77811740d5c62f3787f7a87c8be6cd7247d345f6dfe9e93512a4`（coordinatorも照合）。旧`bed7508…`との差は
  `minecraft-targets.json`と`config.yml`だけ。同じJARで、Paper 1.21.11 build 130（Java 21）と26.3 STABLE build 178（Java 25）の
  pulseと通常の再起動を認証ONでやり直し、全項目PASS。manifest v2は1,761 bytes、SHA-256
  `508a34b9ea29357105e6fcc124a7ab0c0eba8ec9fa258eee52bb196222856627`でPASS。READMEにサーバーのフォルダーごとのmiseとJavaの案内を
  入れた。helloは同梱の宣言を使い、configの旧値は比較とwarningだけに使うことを実地で確かめた（hub NOTES 2026-09-28のparkを
  閉じた）。返却packetはMcRemote `handoff-materials/2026-10-13-b10-paper263/`。未検証：pre-releaseのassetからの3 OSの人間試験、
  Windows／macOSでの26.3のPaperの起動、実playerのevent callback
- 決定（2026-10-13、human owner「McRemote b10とする」）：上のcandidateをb10のMcRemoteとして採用する。`56af938`と26.2の試験は
  b10の根拠にしない。McRemoteのpre-releaseは、Scratchのcandidateがそろってから一緒に作る。箱庭サーバーの版とホームページの
  箱庭の記述は検証次第で、今は変えない
- 進捗（2026-10-13〜14、Scratch、pre-releaseを使わない試験）：`ec29372`に未commitの変更を載せた試作ZIP（どれも
  `working_tree_dirty:true`で、正式candidateではない）を、一時的なLANのページから取得してhuman ownerが試した（記録は
  scratch-editor `mc-remote/local/PREFLIGHT_3OS_ja.md`、`LAN_EXPERIENCE_DESIGN_ja.md` §15、packet
  `handoff-materials/2026-10-14-b10-quickstart-source/`）。Minecraftサーバーは26.3 build 180（試験を始めたときの最新は
  179、途中で180が出た）
  - Windows 11：起動のたびにファイルマネージャーが2回開き設定画面が開かない問題を直し、設定画面とScratchが開いた。
    ペアリング、チャット、ブラウザ保存、Scratchとランチャーとサーバーの再起動の後の再接続も通った。署名の無い
    `start-mc-remote.cmd`のダブルクリックはSmart App Controlに止められる（`2026-10-14-01`）。配信のときにZIPへ長い別名を
    付けたら、展開先のフォルダー名の長さでWindowsが警告を出した（長いパスを許すWindowsの設定でも消えない）。ZIPの通常の
    名前なら起きない見込みで、配る名前に試験用の接尾辞を付けない
  - macOS：初回は「このまま開く」と管理者の認証、2回目からダブルクリックで起動。ペアリング、チャット、再接続が通った
  - Ubuntu：`.sh`のダブルクリックはテキストエディターが開き、右クリックの「プログラムとして実行」で起動した。設定の
    保存とScratchを開く操作を分け（「流れが良くなった」、human owner）、WireScope miniを自動で開くようにした。Scratchが
    別のタブで開いている間は接続先を変えられない理由を設定画面に出す。保存済みのtokenで接続したので、ペアリング待ちの
    画面はまだ見ていない
  - 公開の配布からのダウンロードで出るOSの警告は、まだ見ていない（pre-releaseで見る）
- 決定（2026-10-14）：
  - `.sb3`のドロップ読み込み（scratch-editor packet `2026-10-13-sb3-drop-browser-save`。今の作品をブラウザに保存してから
    切り替え、失敗したら今の作品を残す）をb10に入れる（human owner「入れる」）。storage design §8
  - LANパッケージは当面、署名と公証をしない。Windowsは、展開の前にZIPのプロパティで「許可する」にチェックしてから
    ダブルクリックで起動する経路を主に案内し、ターミナルも案内する（`2026-10-14-01`）。human ownerが2026-10-14に、
    ブラウザで取得した試作ZIP（276,292,480 bytes）で、Smart App Controlをオンのまま、チェックせずに展開すると
    ダブルクリックが警告で止まり、チェックしてから展開すると問題なく起動することを確かめた。b10の実施票のWindowsはこの経路で行う。チェックは展開の前の操作なので、
    ZIPの中の`はじめに.html`では間に合わない。取得する場所（Releaseの本文、rc1までに作るホームページの取得の入口）に置く。Releaseにはプロパティの画面の画像を
    添付してよい（human owner）
  - ホームページの画像（`scratch-MC-connect.png`は旧表示「ペアリン…」、`scratch-stack.png`は「接続する」をスタックに
    入れている）は、human ownerが作り直す
- 次の操作（2026-10-14）：
  - Scratch：作業ツリーをcommitし、CIでb10のcandidateを作る。中身はScratch LANパッケージの設計、`.sb3`のドロップ読み込み、
    設定画面の改善、Windowsのブラウザの起動の修正、ライセンスの本文の短いパス、拡張機能のカードのPNG化、カタログ
    ピッカーの説明、Windowsのネットワークを「プライベート」にする案内。返すものは、source commit、CI run、ZIP 3つ
    （`mc-remote-scratch-LAN-2320.0.0b10-{windows-x64,macos-arm64,linux-x64}.zip`）のbytesとSHA-256（全桁）、manifest v2、
    ライセンスの一覧の更新。あわせて、manifestのrole名`scratch-local`を変えるか、File System Accessの書き出し
    （`2026-10-13-04`）がb10に入るか（入るなら対応するブラウザと、対応しないときの案内）
  - coordinator：Scratchのcandidateがそろったら、McRemote（`17bcf26`）とScratchにpre-release `v2320.0.0b10`の作成を頼み、
    assetのSHA-256をcandidateと照合する。実施票をLANの設計 §8で作り直す（取得はpre-releaseのReleaseのページから。
    1.21.11と26.3の両方をどこかの試験で使う）
- 進捗（2026-10-14、Scratch candidate）：`agent/b10-scratch-local@0809eb5e49e4b83c17a4e91b435d151b9d1b0655`（remoteの一致は
  coordinatorが確認）。CI run `38495047680`（success）、artifact ID `11862469927`、外側
  `sha256:6576a64d75f7eb46f2245ea5d38b336e18388131c79b0db869e693edc3a1fb23`。ZIP 3つ（すべて`working_tree_dirty:false`）：
  - `mc-remote-scratch-LAN-2320.0.0b10-windows-x64.zip` 261,590,008 bytes、`00e73b71d63859f088595257abdec7ce204a09282d79f26daa8d851e0f4af1e8`
  - `mc-remote-scratch-LAN-2320.0.0b10-macos-arm64.zip` 265,941,672 bytes、`edcc757b931d8b89fc18487ee385c20d9ecbdc398b7f34f017e2137fe26c12d2`
  - `mc-remote-scratch-LAN-2320.0.0b10-linux-x64.zip` 271,197,726 bytes、`b69e5b1118dba284604c217b0f3b06ea40b9876014166461705fdc400f647526`
  `candidate-manifest.json` 2,676 bytes、`02d82f0cfabfa7caa5120f53c19c811ad7a913132dda2a5add9ed97c67a3b923`。固定のBridgeとWireScopeは
  tooling `dc1ab834183e29f2eb03059b07e99d2b463776ee`のまま（WireScope ZIP `da3da0b6cf4d05265bc0c11abaa4913208c7cfc3600b0c3e78c93a356fc431ad`）。
  ライセンスは配布物の`data/licenses/review.json`の130件（runtime 26、buildのみ104）が正で、`microee 0.0.6`は2026-10-09の
  「案A」のまま。tests：GUI unit 535、Scratch Local Node 22とPython 11、manifest v2の共有fixture 93など、全てPASS。CIで
  LinuxのZIPの同梱Nodeの起動とBridgeの往復まで確かめた。公開用のmanifest v2はRelease作成後に公開workflowが作る
  （事前生成した版は予告値でない）。返却packetはscratch-editor `handoff-materials/2026-10-14-b10-candidate/`。
  未確認：このZIPでの3 OSの取得から接続まで、ペアリング待ちの画面、配布ZIPでの`.sb3`のドロップ
  - 公開の前に要ること（Scratch担当）：b10の公開workflowは作業branchで変えたので、`develop`を`0809eb5`へfast-forwardで
    統合する。repository variablesに固定candidateのartifact IDとdigestを入れる（`release`イベントには入力が来ないため）
  - Scratch担当の答え：manifestのrole名は`scratch-local`のまま（Scratchのproducerとstackのconsumerが実装済みで、変えるには
    両者とrelease contractの更新が要る）。File System Accessの書き出し（`2026-10-13-04`）はb10に入れず、初回stableの後の
    候補（ブラウザ保存とファイルのダウンロードのまま）
- 決定（2026-10-14、human owner）：File System Accessの書き出しはb10に入れない（rc1でも足さないので、初回stableは
  ブラウザ保存とファイルのダウンロードのまま）。role名は`scratch-local`のまま。pre-releaseを作ってよい。ScratchのRelease
  本文はhuman ownerが編集した`handoff-materials/2026-10-14-b10-candidate/materials/RELEASE_NOTES_DRAFT_ja.md`（SHA-256
  `90f8957f81ce73136a7b1cb87338985f5033ee3c944f041e1b6bb0c4c6a83f2e`）を使う。Windowsのターミナルの起動はGit Bashのほか
  PowerShellも案内する。human ownerがPowerShell 5.1と7.6.7で確かめた（2026-10-14）
- 方針（2026-10-14、human owner）：実施票（`00-hub/b10-gate-live-test-instructions_ja.md`）を作り直した。結果に分類を
  設けず、判断は結果から行う。b10の最終の試作でかなり改善したが、流れにはまだ改善の余地がある。b10は多少緩くても通す。
  ホームページからの案内と文言はrcからstableにかけて改善し、コードが変わる改善は初回stableの後にまとめて実装する
  （human owner「stable後にまとめて実装」）。これらの準備は
  ケータリングのPCにも有効な部分が多いので、併せて進める。文言はすぐにドリフトするので、意味のない説明や筋の通らない
  理屈を混ぜない
- 進捗（2026-10-14、Scratch pre-release）：<https://github.com/Naohiro2g/scratch-editor/releases/tag/v2320.0.0b10>。tagは
  `0809eb5e49e4b83c17a4e91b435d151b9d1b0655`、`develop`も同じcommitへfast-forward。`prerelease=true`、latestにしていない。本文は
  human ownerが編集した案（作成後に冒頭の重複のtitleを消した）。公開workflow run `38525643511`（success）。asset 7つのbytesと
  SHA-256をcoordinatorがGitHub APIで照合し、3つのZIPはcandidateの値と一致（返却packet scratch-editor
  `handoff-materials/2026-10-14-b10-prerelease/`）：
  - `manifest.json`（v2）2,105 bytes、`7c90c4b0041447f132a1da4bb20bdbdd259eed8a4023d79993f4976295708741`
  - `wirescope-app.zip` 83,854 bytes、`da3da0b6cf4d05265bc0c11abaa4913208c7cfc3600b0c3e78c93a356fc431ad`、
    `wirescope-app.manifest.json` 2,339 bytes、`c654f7d1f0be2773d6737e889279b2587317088717f162b082c82be9cff910d7`、
    `contracts.tar.gz` 1,908 bytes、`48948ba47d55409f02a8ff8e0d44021b07859e11ffa5ca0f8598e6ef06082390`
  - Scratch OCI `ghcr.io/naohiro2g/mc-remote-scratch:v2320.0.0b10`、`sha256:1c7bccb32444e7263841ce87add0547cf798f95df2b47971b9be78db847d3be5`。
    Bridge OCIは固定の`sha256:5828304c9bb1d60df8672f9189f503790050e09358bd375f39e4d59d190eb84f`
  - Windowsの「許可する」の画像はhuman ownerが添付する（まだ無い）。2026-10-17：本文に添付済みを確認
- 進捗（2026-10-14、McRemote pre-release）：<https://github.com/Naohiro2g/McRemote/releases/tag/v2320.0.0b10>。tag（annotated）は
  `17bcf2645c112133935bc9d993d4fdd4669ceb98`を指す。`prerelease=true`、latestは`v1.21.8-1.4.0`のまま。tagのCI run `38525157673`の
  4 fileはcandidateと同じbytesで、公開workflow run `38528358810`（success）は作り直さずに載せた。asset 5つのbytesとSHA-256を
  coordinatorがGitHub APIで照合（返却packet McRemote `handoff-materials/2026-10-14-b10-prerelease/`）：JAR 315,352 bytes、
  `96ddf09f765a77811740d5c62f3787f7a87c8be6cd7247d345f6dfe9e93512a4`。`manifest.json` 1,761 bytes、
  `508a34b9ea29357105e6fcc124a7ab0c0eba8ec9fa258eee52bb196222856627`。`minecraft-targets.json` 126 bytes、
  `8e830732decd6bcde13f91eb6c071d062ba6993342a7edb52e6ea543b9e0c361`。版ごとのrecord（1.21.11は
  `c79ca8e667f46b0df4f6703ce3173c40741e9c37427e4de7908cc396390674f9`、26.3は
  `e07fd1513f731d587302621b95234fb135fa95553ca87111829bcda3618b1754`）
- 次の操作（2026-10-14）：human ownerが実施票で3つのOSを試す。pre-releaseの解除とshared deployは、その結果の後に別に頼む
- 進捗（2026-10-14〜17、3 OS）：pre-releaseのassetで、Windows（Smart App Controlオン、「許可する」→ ダブルクリック）、macOS
  （「このまま開く」）、Ubuntu（「プログラムとして実行」）の取得、初回起動、設定画面、1台構成、ペアリング待ちの画面、
  保存・再開、LAN構成（Mac → Ubuntuの1.21.11、Windows → macOSの26.3）が通った。Paperは1.21.11 build 132と26.3 build 181、194、
  200。見つかったことは14件（`14-evidence/records/2026-10-17-b10-prerelease-3os-live-human_ja.md`）。実施票7.3の「翌日、
  ペアリングし直さずに接続できるか」はsession tokenの約2時間の失効と食い違っていた（coordinatorの誤り。翌日はペアリングし直す
  のが設計どおり）
- 決定（2026-10-17、human owner）：b10は合格（`2026-10-13-05`の「通れば」）。翌日に誘導なしで始める回は、今回の改善点を直せば
  合格の見込みとし、b10とrc1を使う中でフィードバックを得る
- 決定（2026-10-17、human owner）：pre-releaseの印は外さない。今は特殊なbootstrapの期間で、ベータの版をpre-releaseの状態で出す
  （versioning §10.9、b4〜b9も`prerelease=true`）。b10の公開は2026-10-14に作ったpre-releaseのままとする。`2026-10-13-05`の
  「印を外して公開」はこれに合わせて読む（coordinatorは前から外す前提で話していたが、human ownerは「まだ」と考えていた）
- 確認（2026-10-17、coordinatorがGitHub APIで照合）：McRemote `main`と`v2320.0.0b10`のtag targetは同じ
  `17bcf2645c112133935bc9d993d4fdd4669ceb98`、Scratch `develop`とtag targetは同じ`0809eb5e49e4b83c17a4e91b435d151b9d1b0655`。
  どちらも`prerelease=true`、`draft=false`。ScratchのRelease本文の冒頭にWindowsの「許可する」の画像がある（human ownerが添付）
- 方針（2026-10-17、human owner）：shared deployはリリースの作業を終えてから行う。VPSベータのMinecraftの版はhuman ownerが
  調査中（Paper 26.3はまだ若く、他の勧めるプラグインの対応を調べている。逆に1.21.11とJava 21の対応を外したものもある。
  DirectionHUDがその例で、McRemoteに取り込みたい動機もそこにある）。rc1、latest、その後で、サーバーの使い分けも変わる
- 次の操作（2026-10-17）：McRemoteとScratchにb10の`handoff-materials`の分類を頼む（`00-hub/b10-gate-close-instructions_ja.md`）。
  返ってきたら、gateを閉じるときのparkの確認（`2026-09-30-09`）をしてcloseをhuman ownerに諮る。その後にshared deployとrc1
- 進捗（2026-10-17、close分類）：両担当がknowledge `91e7f4e`を読んで返した（McRemote `handoff-materials/2026-10-17-b10-close/`、
  Scratch `handoff-materials/2026-10-17-b10-close-inventory/`）。①はScratch 79 file、McRemote 20 fileで、coordinatorがbytesと
  SHA-256で照合して`14-evidence/artifacts/2026-10-17-b10-gate-close/`へ収容した（`14-evidence/records/2026-10-17-b10-gate-close_ja.md`）。
  human ownerの指示で、設計とアイデアの文書は遅延削除（Scratchは該当のdirectoryを②、McRemoteは③のMarkdown 57件を保護）。
  Scratchは2026-10-12のparkへの⑥〜⑪の追記が元の票と両立すると返し、WireScope miniの層別の診断の案が未収容と返した（parkへ追記）
- gateを閉じるときのpark確認（`2026-09-30-09`、2026-10-17、human owner同意）：tick分割のparkを閉じた（b10で実装と確認）。ホームページの
  2つのルートは再開の条件が来たので2026-10-18に着手する（rc1までにLANの入口）。Smart App Controlの切り替えのparkへ、b10の試験で
  SACオンのまま認証できた観察を足した。auto modeがpushを止めたparkは、b10のclose分類の着地のpush（`6e9e14d`、evidence 99 file）が
  止まらずに通ったので閉じた
- close（2026-10-17、human ownerの判断）：**b10 gateをCLOSEDとする**。残り：shared deploy（VPSベータのMinecraftの版をhuman ownerが
  決めてから）、ホームページ（releasesの記述、LANの入口）、rc1 gateを開くこと
- Backstageのclose分類（2026-10-19受領、`2026-10-18-01`で管轄に戻したための後追い）：b10のclose依頼の宛先にBackstageが入っていなかったので、
  Backstage担当がcloseの手順に沿って後から分類した（返却票はBackstage `handoff-receipts/2026-10-18-b9-b10-close-return_ja.md`、main `e3838bc`、
  4,290 bytes、`e5c86d7ec8ddfa59b47d468c1d41f825b8b845d45357381fb1de87dfb6d85feb`。knowledge `3f80b05`を読んだ。b9とb10の分をまとめた1通）。
  ①は無い。返却票はcoordinatorがbackstageを直接読まず、human ownerが渡した要約で受けた（`2026-09-03-03`）。管理端末の
  `~/.local/share/mc-remote/`のBackstage管理外の10件、park確認の候補6件、Stackの分の分類は、rc1の節で扱う

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
- Backstageのclose分類（2026-10-19受領、`2026-10-18-01`で管轄に戻したための後追い）：b9のclose依頼の宛先にBackstageが入っていなかったので、
  Backstage担当がcloseの手順に沿って後から分類した（返却票はBackstage `handoff-receipts/2026-10-18-b9-b10-close-return_ja.md`、main `e3838bc`、
  4,290 bytes、`e5c86d7ec8ddfa59b47d468c1d41f825b8b845d45357381fb1de87dfb6d85feb`。knowledge `3f80b05`を読んだ。b9とb10の分をまとめた1通）。
  ①は無い。返却票はcoordinatorがbackstageを直接読まず、human ownerが渡した要約で受けた（`2026-09-03-03`）。管理端末の
  `~/.local/share/mc-remote/`のBackstage管理外の10件、park確認の候補6件、Stackの分の分類は、rc1の節で扱う

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
