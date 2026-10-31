# 初回stable（2321.0.0）の公開の依頼

> 初回stableの横断release gate（`00-hub/release-gate-notes_ja.md`の2026-10-22の節）で、2026-10-31に凍結したexact set（同じ節の
> 「凍結するexact set（2026-10-31）」）を、作り直さずにそのまま公開する依頼です。参照するknowledge commitは、この依頼が入った
> mainのcommitです。各担当は、自分の節と「共通」を読んでください。

## 共通

- 始める時刻：2026年11月1日 0:00（JST）から。それより前にtagやReleaseを作らない
- 順番（gate notesの時間割）：toolingを先に出し、coordinatorが照合する → Scratch、McRemote、Python → coordinatorが照合する →
  human ownerがPyPI.orgのjobを承認する → coordinatorが照合する。McRemoteとPythonは、toolingの照合を待たずに始めてよい。
  Scratchは、toolingのReleaseと照合が済んでから
- 既定のbranch：下に書いた凍結したcommitへ、既定のbranchをfast-forwardで進める。fast-forwardにならない（既定のbranchが動いた）
  ときは、止めてcoordinatorへ返す。Scratchは`develop`を動かさない（下のScratch）
- tag：`v2321.0.0`を、凍結したsourceのcommitへ打つ
- Release：`prerelease=false`、`draft=false`、Latestにする
- 配布物：凍結した候補のfile（CIのartifactの中身）を、作り直さずにそのまま添付する。公開のworkflowが作り直す場合は、添付の前に
  作ったものを下の凍結値（bytesとSHA-256の全桁、OCIはindex digest）と比べ、違ったら公開せずに止めて返す
- Release本文：各repoの本文の案をもとにする。protocol `23.2.1`、APIと通信はrc1と同じであること、旧版から移る人への
  [移行のページ](https://mc-remote.com/migration/)、feedbackの入口<https://github.com/Naohiro2g/mc-remote-knowledge/issues/new?template=feedback.yml>
  を入れる。Scratchの名前は`-beta`のない`scratch.mc-remote.com`、`wirescope.mc-remote.com`、箱庭は`sb.mc-remote.com`
- 返却：実際に読んだknowledge commit、既定のbranchの新しい先頭のSHA、tagが指すSHA、Release URL、run ID、assetごとのファイル名、
  bytes、SHA-256、凍結値との照合の結果（OCIはdigest）
- 夜中に止まったら：公開済みの分はそのままにして止め、coordinatorへ返す。続きは朝に回す

## minecraft-remote-tooling（Scratch担当）

- source：`main@6447f6e8cbfbeeb9d229990b5c4f6e82a5875666`（rc1と同じ。mainは動かさない）。tag `v2321.0.0`を`6447f6e`へ。rc1のtagは残す
- 添付：rc1の生成物をそのまま使う
  - `wirescope-app.zip` 83,854 bytes／`da3da0b6cf4d05265bc0c11abaa4913208c7cfc3600b0c3e78c93a356fc431ad`
  - `wirescope-app.manifest.json` 2,339 bytes／`3dd668a236463809a4cdc6d19375f3e6d75eea0c8089a616d2b761d3a4a05235`
  - `bridge.oci.tar` 114,626,048 bytes／`3982876466fb860dca250438d73e18e441a2a85d67d9f149f537a7a8d1a1c44c`
- Bridge OCI：registryの同じindex（`sha256:305d6e38b36e195a0e158522f32f3a8c45d39da2aeec7b7e46f785c920406acf`）に`v2321.0.0`のtagを
  足す。provenanceは書き換えない（human owner 2026-10-22）
- Release本文：`tooling-release-notes-draft_ja.md`（scratch-editor
  `handoff-materials/2026-10-22-stable-work-scratch-tooling/materials/`）

## Scratch editor

- source：`agent/stable-scratch-2321@ffb496ed50d751d307f685f2ae555c94c893fae5`。tag `v2321.0.0`を`ffb496e`へ。`develop`はこの公開では
  動かさない（最小の配布対応をdevelopへ入れるのは公開の後）
- 添付：候補のartifact（run `39744827621`、artifact `12410683112`、`sha256:9f0a148a286c8bc3528f1b0e4f948f2d5b9d0da141ac9d393e610e3615d81a6c`）
  の中のfileを、そのまま使う。`release:published`による作り直しはしない
  - `mc-remote-scratch-LAN-2321.0.0-windows-x64.zip` 261,870,138 bytes／`262f67442e9699a06afb39d2259fda7f429a1a16524539e2ba51b52ceddd9525`
  - `mc-remote-scratch-LAN-2321.0.0-macos-arm64.zip` 266,221,800 bytes／`8cacff36c64adf8a9a6570e76db564bc81a54d1ace180e0042dbd1836f77b92f`
  - `mc-remote-scratch-LAN-2321.0.0-linux-x64.zip` 271,477,855 bytes／`e3361bf69036417c8f9d03db7087d00b46e680f0f0fca1360994f16cbadba581`
  - `scratch-gui.tar.gz` 138,834,579 bytes／`fa4a1939843a83b453d882dda54ad2713ff3d53f0e1a16458e0bfc731947947a`
  - `contracts.tar.gz` 1,908 bytes／`48948ba47d55409f02a8ff8e0d44021b07859e11ffa5ca0f8598e6ef06082390`
  - 同梱のWireScopeとBridge OCIは、上のtoolingの値と同じ
  - `manifest.json`：候補の`manifest.stable-draft.json`（2,093 bytes／`95b7cf9d997c9da144a5050b30560da311668dcfd35940c32eb012938d8de364`）
    から作る。違いがあれば、その箇所を返す
- Scratch OCI：凍結した`scratch.oci.tar`（325,819,392 bytes／`373effd2c5da766d64077b1bcf1a70f258d59970ee5dacb15fc51b8d9bcdd491`）を
  そのままregistryへ出し、index digestを`sha256:d85e37291ef75e4d64ab7f0c52b9a496889205071d3afc51b796dbcc1161903c`にする
- Release本文：`scratch-release-notes-draft_ja.md`（同じfolder）

## McRemote

- source：`agent/stable-2321-candidate@525c31823a8efb736463aec471c2756089546391` → `main`（rc2の`7960a91`からfast-forward）。tag
  `v2321.0.0`を`525c318`へ（human owner 2026-10-31）。README（Temurin）と`docs/java-mise_ja.md`は、tagの後でmainへ入れる
- 添付：
  - `mc-remote-2321.0.0.jar` 315,868 bytes／`e3f7cc2ab9ee9b3130f927935634e32e8ddffe7d7603b6d873973968f68db4ab`
  - `minecraft-targets.json` 126 bytes／`8e830732decd6bcde13f91eb6c071d062ba6993342a7edb52e6ea543b9e0c361`
  - `mc-remote-verification-1.21.11.json` 63,705 bytes／`34dcf75c54434768463ab69e1e311029fa575044f6765b25a7c82e988e7127fe`と
    `mc-remote-verification-26.3.json` 63,667 bytes／`00c4c675a7483793e97bb5853a13d23ac21c28afa501f5cf690e540c8c431545`
    （2026-10-29〜31のTemurinでの確認の記録。McRemoteの確認票`handoff-materials/2026-10-29-stable-temurin-validation/`）
  - `manifest.json`：公開のときに作る。中のJAR、宣言、verificationの値が上と同じであることを返す
- Release本文：rc2の本文をもとに、初回stableとして書く。対応はPaper 1.21.11と26.3、Javaは「Temurin Java 21／25、最新パッチ推奨」
  （`2026-10-29-01`）、旧`b5:`／`b7:`のキーが残っていればPaperごと止まることと直し方。**本文の案を10/31のうちに返す**。
  coordinatorが見てから公開する（human owner 2026-10-31）
- 旧版の`v1.21.8-1.4.0`はLatestでなくなる。Releaseは消さない

## Python client

- source：`agent/stable-python-2321@fac0313ea9162dc0730412c53d665e6c42a93791` → `main`（rc1のtag `c301053`からfast-forward）。tag
  `v2321.0.0`を`fac0313`へ
- 添付：
  - `minecraft_remote_api-2321.0.0-py3-none-any.whl` 196,033 bytes／`a0c88b864c26e6e1a0ab2ef2248df6851cc9a3189af93579fbd50132d8c747a0`
  - `minecraft_remote_api-2321.0.0.tar.gz` 190,248 bytes／`a6feaec48ac5df1611208c42e7770d87e0a7bafe66794a39b30942f94140cb88`
  - `manifest.json` 675 bytes／`229179c8274d54f06765bf2d717ae416f02742a99077acde09787ea6bd90ee4a`（候補のmanifestに`release_tag`
    `v2321.0.0`を入れたもの）
- PyPI.org：jobはhuman ownerの承認を待って止める。coordinatorがGitHubのRelease assetを凍結値と照合してから、human ownerが承認する
  （`2026-10-18-04`）。PyPI.orgへ出すのは戻せない公開なので、照合が済むまで承認しない
- Release本文：`stable-release-notes-draft_ja.md`（`handoff-materials/2026-10-22-stable-python-candidate/materials/`）

## 公開の後（coordinator、human owner、Stack）

- coordinatorがGitHub APIで、tagが指すSHA、prerelease／draft／Latest、assetのbytesとSHA-256、`manifest.json`のidentity、OCIのdigestを
  照合する。PyPI.orgの承認の後に、PyPI.orgのfileも照合する
- ホームページ：knowledgeのbranch `homepage-stable-2321`をmainへ入れてpushし、human ownerが同期する。coordinatorが外から取って、
  repoと同じbytesであることを照合する
- 箱庭：Stackが26.3のセットへ切り替える（指示票の「Stack」の節の4〜6）。名前の切り替え（`sb`→`sb-retro`、`sb-beta`→`sb`）のDNSは
  human owner。coordinatorが外から照合する
- 告知は、照合が済んでから
