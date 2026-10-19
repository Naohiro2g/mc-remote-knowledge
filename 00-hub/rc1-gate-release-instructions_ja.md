# rc1の公開の依頼

> rc1横断release gate（`00-hub/release-gate-notes_ja.md` rc1）は、mc-remote.comに置いた候補での試験をhuman ownerが合格と
> 判断した（2026-10-19、`14-evidence/records/2026-10-19-rc1-candidate-3os-live-human_ja.md`）。凍結した
> `rc1-integrated-artifact-set-1`を、作り直さずにそのまま公開する依頼です（`2026-10-18-07`）。参照するknowledge commitは、
> この依頼が入ったmainのcommitです。

## 共通

- 順番：toolingを先に出す。ScratchはtoolingのReleaseができてから（Scratchの公開物がtoolingの生成物を集めるため）。
  McRemoteとPythonはtoolingを待たなくてよい
- 既定のbranch：作業branchを既定のbranchへfast-forwardで入れる。fast-forwardにならない（既定のbranchが動いた）ときは、
  止めてcoordinatorへ返す
- tag：`v2321.0.0rc1`を、下に書いた凍結したsourceのcommitへ打つ
- Release：`prerelease=true`、`draft=false`、latestにしない
- 公開の前の照合：tagのCIや公開workflowが作るものを、下の凍結値（bytesとSHA-256の全桁）と比べる。違ったら公開せずに止めて、
  coordinatorへ返す。ScratchのOCIのdigestだけは、違っても止めずに中身を比べて差を記録する（b9と同じ扱い。下のScratch）
- Release本文に入れること：protocol `23.2.1`、このrc1は23.2.0のserver／clientともつながること（試験で確かめた）、
  feedbackの入口<https://github.com/Naohiro2g/mc-remote-knowledge/issues/new?template=feedback.yml>（`2026-10-18-06`）
- 返却：実際に読んだknowledge commit、既定のbranchの新しい先頭のSHA、tagが指すSHA、Release URL、run ID、assetごとのファイル名、
  bytes、SHA-256、凍結値との照合の結果（OCIはdigest）

## minecraft-remote-tooling（Scratch担当）

- source：`agent/rc1-protocol-2321@6447f6e8cbfbeeb9d229990b5c4f6e82a5875666`（draft PR #1）→ `main`。tagは`6447f6e`
- 添付と照合：
  - `wirescope-app.zip` 83,854 bytes／`da3da0b6cf4d05265bc0c11abaa4913208c7cfc3600b0c3e78c93a356fc431ad`
  - `wirescope-app.manifest.json` 2,339 bytes／`3dd668a236463809a4cdc6d19375f3e6d75eea0c8089a616d2b761d3a4a05235`
  - Bridge OCI：registryへ出すindex digestは凍結値`sha256:305d6e38b36e195a0e158522f32f3a8c45d39da2aeec7b7e46f785c920406acf`と同じに
    する（`bridge.oci.tar` 114,626,048 bytes／`3982876466fb860dca250438d73e18e441a2a85d67d9f149f537a7a8d1a1c44c`）。置き場所とdigestを
    Release本文かmanifestに書く
  - shared fixture（repoの中のfile。b9と同じく添付するかはrepoの慣例どおり）：`chat-event-compat-v23.2.1.json` 32,384 bytes／
    `eead244a7340c315cb63e1e77ede0fe9cf48162c06fedbeef36d941950d5000d`、`entity-particle-v23.2.1.json` 36,483 bytes／
    `0319ff8373a96798cf5e9e421a804729fd33a0fa53e96adc12c93ed7994777ae`

## Scratch editor

- source：`agent/rc1-scratch-2321`（draft PR #26）→ `develop`は`f20e55eb53f192eab6cdc4f0d5aae4f52b2dc8db`までfast-forwardしてよい
  （`README_mc-remote.md`だけの1 commit）。tagは凍結したsource`ec79b3b0e364e722d6926a0932eb4bf088ddd3a1`に打つ（tagと`develop`の先頭は
  一致しなくなる。作り直すとOCIのlabelとsidecarのsource commitが変わるため）
- 添付と照合：
  - `mc-remote-scratch-LAN-2321.0.0rc1-windows-x64.zip` 261,848,009 bytes／`86bbaf9a278683315ffe2ebd4f19d56ba53f5501289e4cddfc22f284d8d4e209`
  - `mc-remote-scratch-LAN-2321.0.0rc1-macos-arm64.zip` 266,199,673 bytes／`bdfff47b8c1210a359ed65a8be6fca26624546e3c04add125063968acc091412`
  - `mc-remote-scratch-LAN-2321.0.0rc1-linux-x64.zip` 271,455,727 bytes／`b76b574803c58403e38438d2569917bd72ca95f039026f12ed3a294edfcfba54`
  - `scratch-gui.tar.gz` 138,835,708 bytes／`2dafb257c511989946da021591191cc1501e0d1a9211cc559373ed7de30f19c2`
  - `contracts.tar.gz` 1,908 bytes／`48948ba47d55409f02a8ff8e0d44021b07859e11ffa5ca0f8598e6ef06082390`
  - 同梱のWireScopeとBridge OCIは、上のtoolingの凍結値と同じ
  - Scratch OCI：凍結は325,822,464 bytes／`88d81fba1aca0194c85f638cf19c66a1a2087748f32ff501bdb1dd283ea1d0c5`、index
    `sha256:75e76edb6b8a1de4fb896184b5c26bed7cb1791296f82903e6b1ec4a1a5ab840`。公開するOCIのdigestが違ったら、公開する前に凍結したOCIと
    比べ、amd64とarm64の中身と属性が同じで、違いが許した生成metadata（versionラベル、作成時刻とそれに伴う履歴、mtime）だけであることを
    確かめて記録する。それ以外が違えば止めて返す（b9と同じ）。digestが違う原因は自分たちのworkflowの差（candidateと公開で
    versionラベルの文字列、作成時刻、GUIのCOPY layerのmtime）で、rc1の着手依頼の5で揃えることを目標にした（揃わなくても止めない、
    human owner 2026-10-18）。揃えたかどうかと、公開したOCIのdigestが凍結値と一致したかを返す
- Release本文：上の共通の項目に加え、`はじめに.html`の案内（ZIPを`HOME/mc-remote/`へ置き、前の版の隣に置けること）

## McRemote

- source：`agent/rc1-pre-fixture@192a777ae1d484bcc9b58fcc7c58d6aed1a374af` → `main`。tagは`192a777`
- 添付と照合：`mc-remote-2321.0.0rc1.jar` 315,352 bytes／`917c358c201aa219277b96a447fb85116e8bdb0260870a4d76a8c51219d31c37`
  （対応版の宣言は1.21.11と26.3）

## Python client

- source：`codex/rc1-python-pre-fixture@c30105349ef26413e925699143396ea05bd3e380` → `main`。tagは`c301053`
- 添付と照合：
  - wheel `minecraft_remote_api-2321.0.0rc1-py3-none-any.whl` 196,098 bytes／`5f12dfcf4953bfaf5dcbe649d4a1ca2d3f5f4b5307b9896e79284478216944ca`
  - sdist `minecraft_remote_api-2321.0.0rc1.tar.gz` 190,285 bytes／`dc8d9f30f538c14cfa04260c92f32e8f451748b99a8e596aeb3e59b1968e5611`
- PyPI.org：jobはhuman ownerの承認を待って止める。coordinatorがGitHubのRelease assetを凍結値と照合してから、human ownerが承認する
  （`2026-10-18-04`）
- Release本文に、`wirescope=True`の注意書きを入れる（試験で見つかったこと、human owner 2026-10-19）：WireScopeはPythonのprocessの
  中で動くので、processが終わるとWireScopeも止まる。短いscriptでは、ブラウザがページを読み込む前に終わって白いページになる。
  ブラウザがつながる前に送った命令は表示されない。見るときは、`Minecraft.create(...)`の直後に`input()`などで待ってブラウザで接続codeを
  入れ、最後も`input()`などで待つ。直す方向はhub NOTES（2026-10-19、WireScopeの観測の開始と終了）

## 公開の後（coordinator、human owner）

- coordinatorがGitHub APIで、tagが指すSHA、prerelease／draft／latest、assetのbytesとSHA-256、`manifest.json`のidentityを照合する。
  assetが試験したもの（凍結値）と同じbytesであることを、ここで確かめる
- Python：照合の後にhuman ownerがPyPI.orgのjobを承認し、coordinatorがPyPI.orgのfileを照合する
- knowledge：ホームページ（版の表示、`/lan/scratch/`のZIPへのリンク、Gemini Notebookのパネル）、API一覧（`api/23.2.1/`、
  metadataを`23.2.1`へ、`protocol.note`を外す）、ブロック一覧の`2321.0.0rc1`のsnapshot、McRemote READMEへのリンク
- Stack：rc1のpresetと、公開VPSの別セットへの切り替え（`2026-10-18-02`）
- 候補の中身（`/candidates/2321.0.0rc1/set-1/`）は、human ownerが決めた時期に消す（経路は残す、`2026-10-18-07`）
