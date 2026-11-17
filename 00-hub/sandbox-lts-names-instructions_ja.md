# 12月1日に、公開の名前を最新版とLTSの組にする依頼（mc-remote-stack）

> human ownerが2026-11-16に、12月1日から公開の箱庭とWebの名前を最新版とLTSの組にすると決めた（`2026-11-16-05`）。
> 2026-10-24に伝えた12月の配置（`sb`のMinecraftを有料GAMEsへ移し、`sb-beta`を公開VPSに残す。`00-hub/release-gate-notes_ja.md`の
> 「箱庭のhostと統合版のport（2026-10-24）」）は、これで置き換わる。参照するknowledge commitは、この依頼が入ったmainのcommitです。

## 決まったこと

| 名前 | 出すもの | 置き場所 |
| --- | --- | --- |
| `sb` | Minecraftの最新版 | 公開VPS（今のまま） |
| `sb-lts` | MinecraftのLTS | 有料のXServer GAMEs（新しい名前） |
| `scratch`、`wirescope` | Webの最新版 | 公開VPS（今のまま） |
| `scratch-lts`、`wirescope-lts` | WebのLTS | 公開VPS（新しい名前） |
| `sb-beta`、`scratch-beta`、`wirescope-beta` | 最新版（しばらく残す） | 公開VPS（今のまま） |

- `2400`が出るまでは、LTSも最新版と同じ`2321`の版を出す
- 有料GAMEsのMinecraftは、11月末までは旧protocolの`sb-retro`で、12月1日から新protocolで動かす（human owner。2026-10-24の節）
- DNSはhuman owner（backstage）が変える
- Unity箱庭の`unity-sb`と`unity-sb-lts`は、`00-hub/unity-sandbox-vps-instructions_ja.md`で頼んだ。`scratch-lts`の組の接続先の
  一覧には、12月1日にこの依頼で両方を入れる（2026-11-17に改めた、`2026-11-17-04`）

## すること

1. 12月1日の手順を書く：`scratch-lts`と`wirescope-lts`のTLS、Caddy、Bridgeが受け付けるorigin、runtime configの`connection_targets`、
   WireScopeの受け渡しのheader
2. 接続先は、`scratch`の組は`sb`を既定にして`sb-lts`も選べ、`scratch-lts`の組は`sb-lts`を既定にして`sb`も選べるようにする
   （`2026-10-24-01`の形を新しい名前へ移す）。どちらの組も、`unity-sb`と`unity-sb-lts`も選べる（2026-11-17に足した、
   `2026-11-17-04`）。`scratch-beta`の組は今のまま
3. WireScopeの受け渡しに、`scratch-lts`→`wirescope-lts`の組を足す。三つの組が混ざらないこと（`scratch-lts`から`wirescope`へ
   渡るなど）も確かめる
4. 公開VPSのBridgeから、有料GAMEsの`sb-lts`のTCP 25575へつなぐ（2026-10-24の(b)、外の接続先）
5. doctorで、`sb-lts`への到達と認証を確かめる
6. 12月1日の当日に、human ownerが`scratch-lts`と`scratch`から`sb-lts`を選んでペアリングし、helloが通ることを確かめる手順を書く

## 返却

- 実際に読んだknowledge commit
- 1〜6のPR（番号、head、merge）と手順の場所。12月1日の当日にすることの順番
- 4：外の接続先が、今どこまでできているか
- Stackの外で要るもの（DNS、有料GAMEsのMcRemoteの設定など）
- 確かめられなかったことと、その理由

## coordinatorがすること

- PRをGitHubのAPIで照合する
- ホームページ（移行のページ、リリース一覧、ロードマップ）の文面を12月1日の前に作り、human ownerに見せる
