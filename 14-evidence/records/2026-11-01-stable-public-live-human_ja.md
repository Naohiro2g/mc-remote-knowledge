# 切り替えた後の箱庭での人の確認（2026-11-01）

> test class: `live-human`（報告ベース）。1年ぶりの安定版（2321.0.0）の横断release gate（`00-hub/release-gate-notes_ja.md`の2026-10-22の節の
> 「公開（2026-11-01）」）で、公開VPSを2321.0.0のセットへ切り替えた後に、human ownerが自分の端末で確かめた。Stackの作業報告に
> 載せた結果を、human ownerが会話に貼った。素材はGit外。IPアドレス、ホスト名の実体、player名とUUID、機器の識別番号、token、
> ペアコードは収録しない。

## identity

- 公開VPS：Stack `main@2b5c04842e78b9767c31903e9d8328d7554ce702`（PR #85）、profile `vps-server@18`、preset `public-web-paper@17`、lock
  `sha256:e4beef4927ecbe5ca60205d04ddfe8200bd41e74960f165fa348fea6bfd37bb3`。Paper 26.3 #231、Temurin 25.0.5+8、heap 3G／3G、McRemote
  `2321.0.0`、Geyser b1279
- `sb`と`sb-beta`はこの公開VPSを指す。`sb-retro`は別のhostで動く旧プロトコルの26.3
- Webの`scratch.mc-remote.com`と`scratch-beta.mc-remote.com`は、Scratch `v2321.0.0`（OCI index
  `sha256:d85e37291ef75e4d64ab7f0c52b9a496889205071d3afc51b796dbcc1161903c`）

## 結果

| 項目 | 結果 |
| --- | --- |
| 接続 | Ubuntu、macOS、iOS、iPadOS、Windowsから`sb`、`sb-beta`、`sb-retro`へ接続できた |
| Scratch（`scratch.`） | Windowsで`sb`に参加し、Ubuntuの`scratch.mc-remote.com`でペアリングして、postToChatとsetblocksが通った |
| Scratch（`scratch-beta`） | `scratch-beta.mc-remote.com`でもペアリングし、保存とロードをした同じコードが動いた |
| ブラウザーの保存 | 2つのScratchで、ブラウザーの保存が共通に使えた |

## 確かめていないこと

OSの版、Minecraftのclientの版、Java版と統合版の別は、報告に無い。公開のworldでの自動のpulseは行っていない（公開のworldを変えない
ため。同じセットの自動の確認は`14-evidence/records/2026-10-31-stack-paper231-temurin25-heap3g_ja.md`）。Python clientからの接続は、
この確認に含まれない。
