# `2400.0.0rc1`のpre-releaseと、McRemote `2321.2.0`の公開の依頼

> `2400`横断release gate（`00-hub/release-gate-notes_ja.md`の「2026-11-19 `2400`横断release gate」）で凍結した`2400-set-1`
> （同じ節の「凍結するexact set（2026-11-25、`2400-set-1`）」）を、作り直さずにpre-releaseで出す依頼です。11月中は`-beta`で
> 動かし、human ownerがそこで試します。同じ日に、McRemote `2321.2.0`をLTSとして出します（`2026-11-21-01`、`2321.2-set-1`）。
> 参照するknowledge commitは、この依頼が入ったmainのcommitです。各担当は、自分の節と「共通」を読んでください。

## 共通

- 始める時：human ownerが知らせてから。それより前にtagやReleaseを作らない。McRemote `2321.2.0`は、rc1とは別に、McRemoteの
  人間の試験の残り（8〜11）が済んでからhuman ownerが知らせる
- 順番：toolingを先に出す。ScratchはtoolingのReleaseができてから（10月のrc1と同じ）。McRemote、Python、Unity箱庭は待たなくてよい
  → coordinatorが照合する → human ownerがPyPI.orgのjobを承認する → coordinatorが照合する → Stack
  （`00-hub/2400-gate-stack-instructions_ja.md`）
- 既定のbranch：動かさない。tagだけを、下に書いた凍結したcommitへ打つ。PRは開いたままにする。Pythonの候補は`v2321.1.0`の上に
  あり、`main`（PR #13〜#16が入った）からfast-forwardにならないため、rcの間はどのrepoも同じにする
- tag：`v2400.0.0rc1`（annotated）
- Release：rc1は`prerelease=true`、`draft=false`、Latestにしない
- 公開の前の照合：tagのCIや公開のworkflowが作るものを、下の凍結値（bytesとSHA-256の全桁、OCIはindex digest）と比べる。違ったら
  公開せずに止めて、coordinatorへ返す。OCIは、凍結したtarやdigestをそのままregistryへ出す。作り直す経路は止める（`2321.1`と同じ）
- Release本文（rc1）：最新版候補であること。protocol `24.0.0`で、中身は`23.3.0`と同じこと。`2321`の系列（protocol `23.x`）の
  serverとclientとは、helloで断られてつながらないこと（`protocol_mismatch`）。11月中は`sb-beta`、`scratch-beta`、`wirescope-beta`で
  試せること。feedbackの入口<https://github.com/Naohiro2g/mc-remote-knowledge/issues/new?template=feedback.yml>。本文は、出した後に
  coordinatorが見る。直すときは本文だけを直す（assetは替えない）
- 返却：実際に読んだknowledge commit、tagが指すSHA、Release URL、run ID（とそのjobの「Runner Image」の名前と版）、assetごとの
  ファイル名、bytes、SHA-256、凍結値との照合の結果（OCIはdigest）
- 途中で止まったら：公開済みの分はそのままにして止め、coordinatorへ返す

## McRemote

### `v2400.0.0rc1`

- source：`release/2400.0.0rc1@d93f5212d189650cd1c7c7fb2aa14c8a73934fc1`（PR #22）。tag `v2400.0.0rc1`を`d93f521`へ
- 経路：返却の案（`handoff-materials/2026-11-19-2400-rc1-candidate/materials/RETURN_ja.md`の「公開の手順の案」の3の2）のとおり。
  tagのCIのJARが凍結値と全桁同じなら、下書きに検証の記録2つを付け、`dry_run`の後に`release.yml`で出す。違ったら止めて返す
- 添付と照合：CI `44524127846`のartifact `14529373048`（`sha256:ba190fb2f0ec9be9d0e3d2d7590ee6dd086e93081b27511bf36b83e42ef5dc1d`）
  - `mc-remote-2400.0.0rc1.jar` 349,793 bytes／`9583b7e9db16e3062cfb8ea5be1c7b5330e1df92eaeea1dd7b2fdb77a75d457a`
  - `minecraft-targets.json`（`1.21.11`と`26.3`）／`8e830732decd6bcde13f91eb6c071d062ba6993342a7edb52e6ea543b9e0c361`
  - `mc-remote-verification-1.21.11.json` 63,255 bytes／`aa4d4807dff3d90295363edcd592a6dfc3ac0cd1ce86fb47a6cb1115e868fb2e`
  - `mc-remote-verification-26.3.json` 63,234 bytes／`979c71adeda625a687fd7040cb11d1e39a359f0d99fe3cf8d6a82df9327337dd`
  - `manifest.json`：`release.yml`が作る。`release_tag`、`source_commit`、JARのbytesとSHA-256を返す

### `v2321.2.0`（LTS）

- 始める時：McRemoteの人間の試験の8〜11が済み、human ownerが知らせてから
- source：`release/2321.2.0@2ccf0b1aba6008c314abe6df4d19b6fffb60ff58`（`main`の`5fca9f2`の祖先）。tag `v2321.2.0`を`2ccf0b1`へ
- 経路（2026-11-20に決めた形。tagのbuildを11/28〜29から今日へ早める）：tagのCIのJARが凍結値と全桁同じなら、それを出す。
  違ったら、凍結した5つのfileを下書きに付け、`release.yml`を止めて出し、後で戻す
- 添付と照合：CI `43678473697`のartifact `14147053531`（`sha256:fe4eeaa73fe7b8de06401e3260cb96ba39a3d6466775c2948e2f1281dbb5e646`）
  - `mc-remote-2321.2.0.jar` 348,720 bytes／`16e927a79ea9b9ae9f1aa544cd5101eb3a6c39228ef9c0da7175853d100703f8`
  - 検証の記録：`handoff-materials/2026-11-15-23212-candidate/materials/`の2つを、中身を変えずに名前だけ替えて付ける
    - `minecraft-verification-1.21.11.json` → `mc-remote-verification-1.21.11.json`：62,489 bytes／
      `0bdb54863290c01245d1e26e79917d73e637c0f327cf2efa8748484446bb2923`
    - `minecraft-verification-26.3.json` → `mc-remote-verification-26.3.json`：62,468 bytes／
      `2cde971c76fb6a850082a4715499d2be06ec0207d3ba397d2a20cbeac7c321da`
  - `minecraft-targets.json`と`manifest.json`：artifactの中のものと、`release.yml`（または止めたときは`create_release_manifest.py`）が
    作るもの。どちらもbytesとSHA-256を返す
- Release：`prerelease=false`、`draft=false`。Latestにする（11月25日〜30日。12月1日に`v2400.0.0`を出すと、Latestはそちらへ移る）
- Release本文：LTS（`2321`の系列、protocol `23.3.0`）であること（`2026-11-21-03`）。「今の最新版」のような、時期で変わる言い方は
  使わない（返却の案。12月1日に本文を直さずに済む）。`2321.1.0`から変わったこと（`handoff-materials/2026-11-15-23212-candidate/
  materials/RETURN_ja.md`の「2321.1.0から変わったもの（Release本文の材料）」）。feedbackの入口。本文の案を先に返す。human ownerが
  見てから出す

## Python client

- source：`agent/python-2400-rc1@d0aae0092ee44400b44b56087ec7f9eb49ef8dac`（draft PR #17）。tag `v2400.0.0rc1`を`d0aae00`へ
- 添付と照合：CI `44486884399`のartifact `14510823109`（`sha256:5625636a3055b213446a14b8e8853cec3ef53f2701549e0b370311384388678f`）
  - wheel `minecraft_remote_api-2400.0.0rc1-py3-none-any.whl` 196,455 bytes／`1e54fa253a397ffd4cfef6ba623260386b2414d3543dcbbc1246e1061bf71dc2`
  - sdist `minecraft_remote_api-2400.0.0rc1.tar.gz` 190,594 bytes／`1ab6f8c5e43bf1eb50d172572462156141ee0f79877f1b0e921c2e838955e426`
  - `manifest.json`：候補のmanifest（674 bytes／`4a2c86b5d798ac507044b8a14b249cdff12618f7506e13abb28c3c5f8a37804f`）に`release_tag`
    `v2400.0.0rc1`を入れたもの。違いが`release_tag`だけであることを返す
- TestPyPIとPyPI.org：公開のworkflowは、両方のjobを起動する。TestPyPIはそのまま出してよい（10月のrc1と同じ）。PyPI.orgのjobは、
  human ownerの承認を待って止める。coordinatorがGitHubのRelease assetを凍結値と照合してから、human ownerが承認する（`2026-10-18-04`）。
  PyPI.orgにはpre-releaseとして載り、版を指定しない取得は`2321.1.0`のまま（`2026-10-05-03`）
- Release本文：上の共通の項目に加え、入れ方（`pip install minecraft-remote-api==2400.0.0rc1`）。版が合わないときの表示は
  `[protocol_mismatch] protocol_mismatch`で、双方の版は例外の`data`にだけ入ること（文を直すのは`2401`）

## minecraft-remote-tooling（Scratch担当）

- source：`agent/tooling-2400-rc1@541e7b3bd3a5653d4a5d2c48f464805782bad9fb`（draft PR #14）。tag `v2400.0.0rc1`を`541e7b3`へ
- 添付と照合：CI `44621700308`のartifact `14578100932`（`sha256:c85de11b1fde25378dce4f6dfa055348f5e1749ba4fe5c3be72e4452ca523eaf`）
  - `wirescope-app.zip` 85,269 bytes／`09a62fc044ccd933614dc6a2cdf5c53b368202d450abd3d66680468b06268a1c`
  - `wirescope-app.manifest.json` 2,339 bytes／`6a2de3d3f4cf9024ffd6d1316347c07a2471eef822262da931ae2314b8709603`
  - Bridge OCI：`bridge.oci.tar` 114,625,024 bytes／`dcc7360e9362859a9f0a42a6ef2d1e66f021c1ffef04958f65e01d16d64e7161`。GHCRの
    `mc-remote-bridge:v2400.0.0rc1`のindex digestを、凍結値`sha256:d8b7024475c5d1f6a855e1d8be84c2fec7136d6e992cb8464091ebc63a548aa9`に
    する。置き場所とdigestをRelease本文かmanifestに書く

## Scratch editor

- source：`agent/scratch-2400-rc1@0ae8af418d095bac734f37bfca35804810ec1cae`（draft PR #40）。tag `v2400.0.0rc1`を`0ae8af4`へ
- 添付と照合：run `44650257207`のartifact `14590773440`（`sha256:76ff9210e5c2ef099ad2e7e594af087114dca5c4fe758284dcf6de579ed0edb5`）の
  中のfileを、そのまま使う。`release:published`による作り直しはしない（`2321.1`と同じく、image workflowを止めて出し、後で戻す）
  - `mc-remote-scratch-LAN-2400.0.0rc1-windows-x64.zip` 264,584,655 bytes／`d49e1bac359d43caa1d2cbd8e31e47dc54cede0923ec7dee25d24821a30f12ea`
  - `mc-remote-scratch-LAN-2400.0.0rc1-macos-arm64.zip` 268,936,322 bytes／`8b1f272835f0e5297fa14e048e8c80f1d60c1267ba1af44d3e5ace227a592834`
  - `mc-remote-scratch-LAN-2400.0.0rc1-linux-x64.zip` 274,192,377 bytes／`35a576583fc0c61729ec044336d4167f8d448b56339db2031417a0e1baad130b`
  - `scratch-gui.tar.gz` 141,185,544 bytes／`04879de729e04ce13d4ef90d139c49b67ffc14977c35dc60f096739ecd867529`
  - `contracts.tar.gz` 2,641 bytes／`ea16b791383b510de93cce8f43c072b5a9c856df7d23217f825af5cda392eb25`
  - 同梱のWireScopeとBridge OCIは、上のtoolingの凍結値と同じ
  - `manifest.json`：候補のmanifest（2,676 bytes／`94a0e2bed7fa8c5a52632c3ba9e5dc8ca6d6ef834b8edb9d2484db1710adc7c3`）から作る。
    違いがあれば、その箇所を返す
- Scratch OCI：凍結した`scratch.oci.tar`（330,516,480 bytes／`cf4b693005d284616fc00a6b37d4d977662b5635e8f231f37ac13bd5c9676172`）を
  そのままregistryへ出し、`mc-remote-scratch:v2400.0.0rc1`のindex digestを
  `sha256:a24be219c79d8fa5273bc0a82df0ec94fcc3da3a2114e5577cde5a3f5d7780a9`にする
- Release本文：上の共通の項目に加え、`はじめに.html`の案内（ZIPを`HOME/mc-remote/`へ置き、前の版の隣に置けること）

## Unity箱庭

- source：`release/2400.0.0rc1@6ce475ef64155268037c8e13f063b7151aac6134`（draft PR #5）。tag `v2400.0.0rc1`を`6ce475e`へ
- GHCR：`candidate-6ce475e`と同じdigest`sha256:e39109f0e3ff6bbc9ef2a0f4fb6048735817fa250a5226b404430ace52101097`に、`v2400.0.0rc1`の
  tagを足す。作り直さない。配布物はimageだけで、Releaseにassetは付けない（返却の案）
- LTSの`2321.2.0`（`candidate-1594805`）は、12月1日に出す（`2026-11-21-01`）。今日は出さない
- Release本文：上の共通の項目に加え、imageの置き場所とdigest

## 公開の後（coordinator、human owner、Stack）

- coordinatorがGitHub APIで、tagが指すSHA、prerelease／draft／Latest、assetのbytesとSHA-256、`manifest.json`のidentity、OCIのdigestを
  照合する。Python：照合の後にhuman ownerがPyPI.orgのjobを承認し、coordinatorがPyPI.orgのfileを照合する
- Stack：`sb-beta`、`scratch-beta`、`wirescope-beta`をrc1にする（Stackの票の「すること」の1）。Unity箱庭の上限の対策版への切り替えは、
  この票を待たない（Stackの票の「上限の対策版へ替える（2026-11-24に足した）」）
- McRemote `2321.2.0`：human ownerが有料GAMEsの`sb-lts`へ入れる。出した後に、credentialのfileのmodeを確かめる（`2026-11-11-03`）
- knowledge：人間の試験の票を、rc1と`-beta`の名前で改める。ホームページの文（LTSの説明を含む）を見せる
