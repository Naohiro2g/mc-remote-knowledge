# 公開の箱庭の`2321.1.0`への更新（2026-11-09）

> test class: `live-auto`と`live-human`（報告ベース）。`2321.1`横断release gate（`00-hub/release-gate-notes_ja.md`の2026-11-06の節）で、
> human ownerがPR 87をmergeし、時刻を知らせた後に、Stack担当が公開の箱庭を`public-web-paper@18`へ更新した。返却は
> `mc-remote-stack`の`handoff-materials/2026-11-09-stack-23211-sandbox-update/materials/RETURN_ja.md`（13,124 bytes、
> `b5d2ba14bf0a11b83679033279c121891b19ab34da1798febb5cd1bf83ee041a`。knowledge `c753874`を読んだ）。素材はGit外に置き、ここへは
> 写さない。backupの本体、config、認証のデータ、raw log、player名、token、ペアコードは収録しない。

## identity

| 対象 | 値 |
| --- | --- |
| Stack | PR 87（merge commit `ba40ccdc54b1238d3f7cf9c9fa8dac7a806dca9f`、head `7185c726c1258ec5cb348abeef95ee4d290e7b18`） |
| preset | `public-web-paper@18`、content SHA-256 `e9fe4c6f4e0be3c02d95a52f2e95904463fbd5cdd0250e13518ce7aa566a4b3e` |
| profile | `vps-server@18`、content SHA-256 `3d659e8f49e99a7547c331692d8593845550f5cd19a40fc1b33334c89cf432b8` |
| lock | `sha256:e4beef4927ecbe5ca60205d04ddfe8200bd41e74960f165fa348fea6bfd37bb3`→`sha256:cb5793011d7160edaf321ef1072d1affeb89d300ed8acb058ac3bbc75ab6c5c7` |
| plan | `sha256:af582efee1b62ef8f952db83bf308caacf3dac05e9c9db7f3a5d197588041bce`、最後のphaseは`complete` |
| McRemote | 2321.1.0、`cd1fff723b2b8349f45184b940cd5da1ca3cdcacc9bad988fa71cd00ea960112` |
| Paper | 26.3 #244、`9601f9a26a2a52a0f2c807cf1abf691f96ee4fb287878313b601cebc2c51eabf` |
| Scratch OCI | `sha256:f3bcf6a6e9ae939e8a8781628ad1e9b40507286da34224f91dfba711a4920c67`（`scratch.`と`scratch-beta.`） |
| runtime | `sha256:69b73187717bf509fa30937b4e4c202dddf18e523cc9668dcf31dd62851a66f0`（Temurin 25.0.5+8）、heap 3G／3G |

プラグイン：AdvancedPortals 2.8.0、DiscordSRV 1.30.5、floodgate 2.2.5-SNAPSHOT（b141）、Geyser 2.12.1-b1294、LuckPerms 5.5.91、
ServerBackup 2.10.0、ViaBackwards 5.12.2、ViaVersion 5.12.2、WorldEdit 7.4.6、McRemote 2321.1.0の10本。DirectionHUDとOtterLibを
外した。Bridge、WireScope、Caddyは変えていない。world、volume、networkは続けて使う。

## 経過（JST）

| 時刻 | 出来事 |
| --- | --- |
| 10:35〜10:38 | 更新の前のbackup（ServerBackup）。939,101,768 bytes、`3e83d297a1b683fd78e6b8999f3ce5e58e3577bbc493519fe846c398bb7229e3`。CRCが正しく、3つのdimension、LuckPermsのDB、McRemoteの認証のデータが入っている。sourceのprojectとconfigもprivateな場所へ保存した |
| 10:42:09〜10:43:57 | 1回目のapply。新しい構成でCaddyが起動できず、doctorが「公開のportがlockと合わない」で落ちた。自動で戻す処理も同じ理由で落ちた（`rollback-failed`） |
| 10:44:34 | Stack担当が手で直し、旧構成のCaddyが起動した |
| 10:46:41 | 旧構成のdoctorが全項目成功 |
| 10:46:41〜10:47:38 | 同じplanでの2回目のapply。`complete` |

- 1回目が失敗した原因：Stack担当が手元で使ったスクリプトが、秘密を守るための`umask 077`をmcrctlにも引き継いだ。作り直した
  Caddyfileなどが、containerの中の実行userから読めなかった（`open /etc/caddy/Caddyfile: permission denied`）。自動で戻す処理の
  作り直しにも同じumaskが効いた。Stack担当は、作り直した21のfileを保存しておいたsourceと同じmodeへ戻し、Caddyだけを再起動
  した。mcrctlの子プロセスだけumaskを022にして、同じplanを当て直した。world、権限DB、session、ペアリングは巻き戻していない
- 止まった時間：最後の切り替えは、Minecraftの停止の要求から新しいPaperの準備まで46.485秒（Dockerのeventとログの差。外からの
  計測ではない）。1回目の停止の始まりはDockerの記録に残っておらず、正確な秒数は分からない。1回目の開始から最後のdoctorまでは
  329.332秒で、途中に旧構成が動いていた時間がある。見込みは2〜5分、枠は10〜15分だった

## 結果

### 機械の確認（Stack）

- Paper 26.3 #244とMcRemote 2321.1.0が起動した。Paperの`Done`は23.661秒。10本のJARのSHA-256は期待の値と一致し、起動の
  一覧も10本。予期しないERROR／FATALは0件（1回目のCaddyの失敗は含めない）
- McRemoteは`hud.enabled`と`hud.toggle_on_swap`を`true`で、色の既定とともに補った（configへは書いていない）
- Geyserの`/v1/join`はHTTP 200（protocol 2225、26.62）
- `scratch.`と`scratch-beta.`はHTTPS 200で、index.htmlのbytesは指定のOCIのcontainerの中のものと同じ
- doctorは全項目成功。VPSの通常のStackも`ba40ccd`へ揃え、そこからのdoctorも成功
- McRemoteのconfig：`supported_mc_versions`を元へ戻すスクリプトにも不備があり、値が一時的に`[1.21.11, 26.3]`になった。Stack担当が
  testを足して直し、今までの値がすべて残っていることを読み直して確かめた。再起動はしていない

### coordinatorの照合（2026-11-09）

- GitHubのAPIで、PR 87のmergeと`main`の`ba40ccd`を確かめた
- 素材の`SHA256SUMS`は全件一致。返却の値は素材のJSONと同じ
- `scratch.`と`scratch-beta.`を外から取り、index.html（`7c6255a2cdb18eebe820c81c79b4c185964e3594d4c1830b9623c16d9ff25ecc`）と
  それぞれのruntime JSONがStackの確認と同じであることを確かめた。index.htmlの最終更新は2026-11-07で、`set-2`を作った日と合う

### 人の確認（human owner）

- Stack担当への返答：参加、ペアリング、チャット、setBlock、HUDのbarの表示と切り替えが、すべて確認できた
- coordinatorへの報告：hello world、setBlock、getBlock、WireScope、HUDに問題はない
- iPad（第6世代、iPadOS 17.7.11、Safari）、iPhone SE（第3世代、iOS 27.2、Safari）、Android（Chrome。機種と版は報告に無い）：Scratchを開くことと、
  Minecraftで参加することはできた。1台ではペアリングが成功しなかった。Scratchでペアコードを出してからMinecraftへ移ると、
  Minecraftはサーバーから切れて参加し直しになる。Scratchが無くても、Minecraftからアプリの一覧へ行って戻るだけで、切れて自動で
  参加し直す。ブラウザは、戻っても読み込み直さない。human ownerの見立て：サーバーが切ったのなら自動で参加し直すことはないので、
  clientがもう一度認証からやり直している。リソース不足ではない（NOTES 2026-11-09の行）
- clientの版、Java版と統合版の別、Fとcommandの別は報告に無い

## 確かめていないこと

- backupの別の場所への転送と、実際の復元
- DiscordSRVからDiscordへの実際の送受信
- 端末とOSの組み合わせごとの結果、外からのUDPの到達、授業に相当する負荷、長時間の稼働
- 実施票の「公開の後（タブレット）」の1（カテゴリを切り替えてブロックを探す）と2（ソフトウェアキーボードで探す）
