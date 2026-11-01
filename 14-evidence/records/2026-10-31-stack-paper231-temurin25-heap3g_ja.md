# 公開VPSの26.3のセットの最終の確認（Paper 26.3 #231、Temurin 25.0.5+8、heap 3G、2026-10-31）

> test class: `live-auto`。1年ぶりの安定版（2321.0.0）の横断release gate（`00-hub/release-gate-notes_ja.md`の2026-10-22の節）で、11/1に切り替える
> 公開VPSの26.3のセットを、human ownerの「最新バージョンで最終確認してください」（2026-10-31）を受けてStack担当が確かめた。
> 返却はStack `main@488475f`、knowledge `d012c91`を読んだもの。素材は
> `14-evidence/artifacts/2026-11-01-stable-gate-close/stack/2026-10-31-stack-return-four-items-java/`（6 file）。新しいlive-humanは無い。
> 切り替えた後の公開のworldでの人の確認は`14-evidence/records/2026-11-01-stable-public-live-human_ja.md`にある。

## identity

| 対象 | 値 |
| --- | --- |
| Paper | 26.3 #231（STABLE）、`paper-26.3-231.jar` 55,258,607 bytes、`a836a016be7ac52352eb3a1efb6857bb42ee73a6c78d46e292f7e87742edb0e6` |
| McRemote | 安定版の候補`525c31823a8efb736463aec471c2756089546391`、JAR `e3f7cc2ab9ee9b3130f927935634e32e8ddffe7d7603b6d873973968f68db4ab` |
| Java | Eclipse Adoptium、Temurin-25.0.5+8（runtime 25.0.5+8-LTS） |
| heap | `-Xms3G -Xmx3G`（human ownerの指定）。追加の`-XX`／`-Xlog`は無い。containerのmemoryの上限は指定していない |
| image | `itzg/minecraft-server:2026.7.2-java25`（固定のdigest）のJREを、公式のTemurin JRE 25.0.5+8（61,736,206 bytes、`6fac98f0c8202efc3135a9e9e42aa61963ec42d1c5cbb40caf231e7b14a24ef6`）に替えたもの。image ID `sha256:df6898c45b2decc621a320f09e79dcc700cc6f8852e219a38294269525f6ac1c`（Dockerのconfig digestで、registryの参照ではない） |

プラグイン（公式のmetadataと照合）：WorldEdit 7.4.6、ViaVersion 5.12.2、ViaBackwards 5.12.2、Geyser 2.12.1-b1279、LuckPerms 5.5.88、
DirectionHUD 1.8.4.0+26.2、OtterLib 0.4.0.1+26.2、AdvancedPortals 2.8.0、DiscordSRV 1.30.5、Floodgate 2.2.5-b141、ServerBackup 2.10.0。
DirectionHUDとOtterLibはPaper向けの最新が26.2の表記。

置き場所：公開のworldのbackupから作った専用のコピー。ゲームの公開portは持たず、RPCはloopbackだけ。認証は有効なまま、試験用の
短いsessionを1件だけ足した。公開側の認証DBと権限DBは変えていない。二重の接続を避けるため、DiscordSRVだけを無効にした。

## 結果

**PASS**。

- producerの`compatibility_pulse.py`で、通常のpulse 8 groups、通常の再起動の後のpulse 4 groups（同じsessionで認証、読み取り、書き込み）、
  tokenなしの`hello`の拒否（`auth_required`）
- 起動は34.304秒、通常の再起動は29.703秒。OOMなし
- Geyser b1279（`234fa467a32bbc780bd495296eb18fa0fbd7af8dab41f137ed5f7a45aabfbb90`）は既定のconfigのまま（config-version 11、nethernet、19132、
  `webrtc-port: 0`）で、`/v1/join`が26.60（protocol 2225）を返した
- coordinatorが照合した（2026-10-31）：添付の`SHA256SUMS`が全件一致。Paper #231はfill.papermc.ioのAPIと取得したJAR、Geyser b1279は
  Geyserの公式のAPI、Temurin JREはAdoptiumのAPIと一致

前段（10/29、rc2、Paper 26.3 #203、Temurin 25.0.3+9）の事前の起動も返却票の1にある。当時の条件の記録で、上の結果の代わりではない。

## 確かめていないこと

授業に相当する負荷、swap／GCの分布、長時間の容量。HUDの画面とportalの人の操作。端末からの統合版の参加とUDPの到達。この
imageを公開した後の`ghcr.io/naohiro2g/mc-remote-paper-runtime-temurin@sha256:69b73187717bf509fa30937b4e4c202dddf18e523cc9668dcf31dd62851a66f0`
は、11/1の切り替えで使った（Javaの版は同じ）。

## 素材

| file | bytes | SHA-256 | 元からの変更 |
| --- | ---: | --- | --- |
| `RETURN_ja.md` | 16,291 | `2a39747f5617c4258bae1e92605bc4834fe6a1630b8b4ab28e14eeb63592bed2` | なし |
| `final-pulse.json` | 37,166 | `082c1aa4b7246642d1281090d8347d1084c90e1f7ec172e19f89d31307441e4d` | token、playerを`[REDACTED]` |
| `restart-pulse.json` | 13,120 | `5737d52738c075ec79274ab0cd8ed0bf6ba4ad95dea292d99a70ac0161296cc7` | token、playerを`[REDACTED]` |
| `paper231-api.json` | 490 | `f779a1b79506a557d2bba8b07cc88ea37197191e499d78127a2ac6303051bcc6` | なし |
| `paper231-verification.json` | 667 | `47fb4c440150445caf8d577018f86ead011289d254ef66bedb4d5aef34c7c59a` | なし |
| `paper-artifact.toml` | 453 | `ee2bf226a71427feeacf43a7c477e712931c3123fd60e1a95635a34e36e454ad` | なし |

- 元は`final-pulse.json` 37,177 bytes `808d570a57a28e289b3639b3c23a7f784f8f671bd10e2a94b557fa8d5e2d09f6`、`restart-pulse.json` 13,131 bytes
  `f2a9dbf4bc091af960fbbf5d009e284974a4e3d2dae7508be9debaed4a6c9e37`（Stackの`SHA256SUMS`と一致）。写しはStack担当が作った
- `RETURN_ja.md`の版：gate notesは、coordinatorが10/31 14:15の時点で読んだ16,091 bytes（`0f766ac48fc1ca15a9cef63e0f833ca4b1fbca5e1daa2a80ec5281062f2e1a26`）を
  書いている。Stackは同じ日の18:35に、`connection_targets`の(a)をPR #81で実装したことを2段落に足した（「3. 10/31の凍結手順と所要時間」と
  「終了状態、添付、未完了」）。coordinatorが前の版と比べ、違いはこの2段落だけで、観測は変わっていないことを確かめた（2026-11-01）
