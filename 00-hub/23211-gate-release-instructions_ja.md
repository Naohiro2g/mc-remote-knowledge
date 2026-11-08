# `2321.1`の公開の依頼

> `2321.1`横断release gate（`00-hub/release-gate-notes_ja.md`の2026-11-06の節）で、人間の試験に通った`2321.1-set-2`（同じ節の
> 「凍結するexact set」と「凍結し直すexact set」）を、作り直さずにそのまま公開する依頼です。human ownerの判断は同じ節の
> 「人間の試験（2026-11-07〜09）」。参照するknowledge commitは、この依頼が入ったmainのcommitです。各担当は、自分の節と
> 「共通」を読んでください。

## 共通

- 始める時：human ownerが知らせてから。それより前にtagやReleaseを作らない
- 順番：McRemote、Python、Scratchは並べて進めてよい → coordinatorが照合する → human ownerがPyPI.orgのjobを承認する →
  coordinatorが照合する → Stack（別の票）。toolingは`v2321.0.0`のままで、出さない
- 既定のbranch：下に書いた凍結したcommitへ、既定のbranchをfast-forwardで進める（2026-11-09にGitHubのAPIで、3つとも
  fast-forwardになることを確かめた）。fast-forwardにならない（既定のbranchが動いた）ときは、止めてcoordinatorへ返す
- tag：`v2321.1.0`を、凍結したsourceのcommitへ打つ（annotated）。`v2321.0.0`のtagとReleaseは残す
- Release：`prerelease=false`、`draft=false`、Latestにする
- 配布物：凍結した候補のfile（CIのartifactの中身）を、作り直さずにそのまま添付する。公開のworkflowが作り直す場合は、添付の前に
  作ったものを下の凍結値（bytesとSHA-256の全桁、OCIはindex digest）と比べ、違ったら公開せずに止めて返す
- Release本文：protocol `23.2.1`のままで、APIと通信は`2321.0.0`と同じであることと、feedbackの入口
  <https://github.com/Naohiro2g/mc-remote-knowledge/issues/new?template=feedback.yml>を入れる
- 返却：実際に読んだknowledge commit、既定のbranchの新しい先頭のSHA、tagが指すSHA、Release URL、run ID（とそのjobの
  「Runner Image」の名前と版）、assetごとのファイル名、bytes、SHA-256、凍結値との照合の結果（OCIはdigest）
- 途中で止まったら：公開済みの分はそのままにして止め、coordinatorへ返す

## McRemote

- source：`feat/coordinate-time-hud@5b78ded96d1ad6d45160b67c5f8a13e14adb3fc8` → `main`（今の`77b77c6`からfast-forward）。tag
  `v2321.1.0`を`5b78ded`へ
- 添付：CI `42291740554`のartifact `13540651077`（`sha256:9dd6d88106b3415f96cd51c34064d39bbda362411390594462ab3644eb140803`）の
  中のfile
  - `mc-remote-2321.1.0.jar` 340,193 bytes／`cd1fff723b2b8349f45184b940cd5da1ca3cdcacc9bad988fa71cd00ea960112`
  - ほかの添付（宣言、verificationの記録、`manifest.json`）は、`2321.0.0`と同じ形で付ける。verificationの記録は、どのJARと
    Paperで採ったものかを返す（26.3は凍結したJARとPaper #244。1.21.11は`db7f7db`のJAR）
- Release本文：human ownerが編集した本文を使い、「統合版ではFで切り替えられない」を足す（人間の試験で見えた。human owner
  2026-11-09）
- `v2321.0.0`はLatestでなくなる。Releaseは消さない

## Python client

- source：`agent/python-2321-1-starter@09bbda421645235b2433a6c205d528be15a49f34` → `main`（今の`fac0313`からfast-forward）。tag
  `v2321.1.0`を`09bbda4`へ
- 添付：CI `42227543303`のartifact `13507135196`（`sha256:3c35499f479bfe0874ef7ddb4e2b04a349cf0118df3efab9a2d8dbdf42c12177`）の
  中のfile
  - `minecraft_remote_api-2321.1.0-py3-none-any.whl` 196,026 bytes／`ee80d81be4128f8e2327646f607fbc46053bec91a527eb9140f54c9dc9d6a26f`
  - `minecraft_remote_api-2321.1.0.tar.gz` 190,241 bytes／`2d49d096eb30c8721627f8d8f878551396a8f0d298466a007ce1b71559e255d9`
  - `manifest.json`：候補のmanifestに`release_tag` `v2321.1.0`を入れたもの。違いが`release_tag`だけであることを返す
- PyPI.org：jobはhuman ownerの承認を待って止める。coordinatorがGitHubのRelease assetを凍結値と照合してから、human ownerが承認する
  （`2026-10-18-04`）。PyPI.orgへ出すのは戻せない公開なので、照合が済むまで承認しない
- Release本文：human ownerが編集する本文を使う（E1の部分は外した）

## Scratch editor

- source：`develop@57fb7691bb5d9a5895785b200ae78734240ebfa6`（今の先頭。動かさない）。tag `v2321.1.0`を`57fb769`へ
- 添付：run `42350684690`のartifact `13565862576`（`sha256:47a4f4601dbec0c2e8fc58d9359f69290fda4c1f4f2f58bb387e73590a172050`）の
  中のfileを、そのまま使う。`release:published`による作り直しはしない（`2321.0.0`と同じく、image workflowを止めて出し、後で戻す）
  - `mc-remote-scratch-LAN-2321.1.0-windows-x64.zip` 262,508,252 bytes／`8edf5c1890df3550b3d4ffdd8d39dfbc1cbd35509531266ebd5e80103cab7ad6`
  - `mc-remote-scratch-LAN-2321.1.0-macos-arm64.zip` 266,859,915 bytes／`d9bb5976f62ad5043130c911551f23b0f4b127a5f0a80a6465ff8cd7decb768e`
  - `mc-remote-scratch-LAN-2321.1.0-linux-x64.zip` 272,115,968 bytes／`52f1f4b3eff59cec44c634c8974d5b41cfb18ee873d1348021e7e1831a2cbe42`
  - `scratch-gui.tar.gz` 139,262,746 bytes／`0f0b2597a8694863fb264340c1b3b89685849c85ce7c32e9f4b210e645fbdff8`
  - `contracts.tar.gz` 1,908 bytes／`48948ba47d55409f02a8ff8e0d44021b07859e11ffa5ca0f8598e6ef06082390`
  - 同梱のWireScopeとBridge OCIは、tooling `v2321.0.0`の値と同じ
  - `manifest.json`：候補のmanifest（2,664 bytes／`19aec7258f726f11ce497783b0e3c9b97f39be4fc4d8ccd7f25cfdc084061d47`）から作る。
    違いがあれば、その箇所を返す
- Scratch OCI：凍結した`scratch.oci.tar`（326,605,824 bytes／`c1dc8dc79a4e7dd351af728aa5e80677ce3aa08a84f8a4583dc9b4d9d84d7e10`）を
  そのままregistryへ出し、index digestを`sha256:f3bcf6a6e9ae939e8a8781628ad1e9b40507286da34224f91dfba711a4920c67`にする
- Release本文：本文の案を先に返す。coordinatorが見てから公開する。本家への追従で推奨ブラウザの下限がChrome／Edge 124、
  Firefox 125、Safari 17.4へ上がったことを入れる

## 公開の後（coordinator、human owner、Stack）

- coordinatorがGitHub APIで、tagが指すSHA、prerelease／draft／Latest、assetのbytesとSHA-256、`manifest.json`のidentity、OCIのdigestを
  照合する。PyPI.orgの承認の後に、PyPI.orgのfileも照合する
- Scratchのブロック一覧：coordinatorが、tag `v2321.1.0`の`mc-remote/block-reference/site/`をホームページの`/api/scratch/`へ入れる
  （2026-11-01の条件：一覧の`sourceCommit` `11bce31`がtagの指すcommitの祖先で、間はsiteの生成物だけ、取り込むfileがtagの
  `site/`と同じbytes）
- ホームページ：新着と`/releases/`を`2321.1.0`にする。human ownerが同期し、coordinatorが外から取って、repoと同じbytesであることを
  照合する
- 箱庭：Stackへの別の票で、presetの`public-web-paper@18`を正式にし（McRemoteは公開のReleaseのJAR、Scratch OCIは`set-2`の
  digest、Paper 26.3 #244）、`e5571f7`を新しいPRで`main`へ入れ、箱庭を更新する。DirectionHUDとOtterLibを外し、Geyserを
  2.12.1-b1294、LuckPermsを5.5.91へ上げる（human owner 2026-11-07）
- 告知は、照合が済んでから
