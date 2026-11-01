# McRemote 2321.0.0 公開完了票

- knowledge contract path: `00-hub/stable-gate-release-instructions_ja.md` 共通・McRemote、`00-hub/release-gate-notes_ja.md` 初回stable。
- knowledge contract commit: `10fe11cfd437ab45f8c000517595598229e1011e`（最新remote mainを確認し実読）。
- 公開日: 2026-11-01（JST）。
- Release: https://github.com/Naohiro2g/McRemote/releases/tag/v2321.0.0
- published_at: `2026-10-31T15:27:29Z`。
- 公開状態: `draft=false`、`prerelease=false`、Latest。GitHub APIで照合済み。
- mainのfast-forward: `7960a913a11c621d85e6120ee412b696fe125457` → `525c31823a8efb736463aec471c2756089546391`。
- tag: `v2321.0.0` → `525c31823a8efb736463aec471c2756089546391`。annotated tagのobjectは`64a85991a67f934a519940efa76583311eb68dfc`。
- README・Javaガイド反映後のmain: `331a32644a6b6ee7044a1e4473e5a01c57e040fa`。
- release sourceはmainへ統合済み。公開後のcommitは`README.md`と`docs/java-mise_ja.md`の2点のみで、tagは凍結sourceのまま。リモートの両文書がローカルと一致。

## 実行・照合

- tag CIのcandidateを取得し、JAR・宣言・Temurin verification 2件のbytesとSHA-256を公開前に照合。manifest生成と固定Schema検査、Release workflowのdry-runがPASSした後に公開した。
- 公開workflowはtag CIのcandidateを昇格。公開asset全5件を再取得し、凍結物と事前の期待manifestにbytes単位で一致することを確認。manifest内のsource・JAR・宣言・verificationも同じ。
- 本文はhuman ownerが直接修正しknowledgeで採用された2,152 bytes／SHA-256 `0ccf9df7dce03093e5cd741f0a4abf1c471ad17da4130ee26b78cb8e5fbb719a`を使用。公開workflowが末尾改行を1つ追加しただけで、内容は一致。公開本文は2,153 bytes／SHA-256 `4303a024ea09cabafd2620a4b7431f9a0934bd7b499f5b2d74320f705423481d`。

| run | 用途 | 結果 |
| --- | --- | --- |
| [41213130587](https://github.com/Naohiro2g/McRemote/actions/runs/41213130587) | tag CI | success |
| [41213698159](https://github.com/Naohiro2g/McRemote/actions/runs/41213698159) | Release dry-run | success |
| [41214940424](https://github.com/Naohiro2g/McRemote/actions/runs/41214940424) | 正式公開workflow | success |

## 公開asset

| file | bytes | SHA-256 |
| --- | --- | --- |
| `manifest.json` | 2,063 | `62b9dad0400107798edd110869cc33dbd37dc92c8f40f736378458801a30f8b5` |
| `mc-remote-2321.0.0.jar` | 315,868 | `e3f7cc2ab9ee9b3130f927935634e32e8ddffe7d7603b6d873973968f68db4ab` |
| `mc-remote-verification-1.21.11.json` | 63,705 | `34dcf75c54434768463ab69e1e311029fa575044f6765b25a7c82e988e7127fe` |
| `mc-remote-verification-26.3.json` | 63,667 | `00c4c675a7483793e97bb5853a13d23ac21c28afa501f5cf690e540c8c431545` |
| `minecraft-targets.json` | 126 | `8e830732decd6bcde13f91eb6c071d062ba6993342a7edb52e6ea543b9e0c361` |

## 返却・保持

- 詳細な照合値: `stable-publication-verification.json`（2,880 bytes、SHA-256 `4296c4e0e061ec0e6232e29a168866710fd85c92dcdcfdb79987569c9779468b`）。
- 本票と照合素材はknowledge担当へ公開結果の記録・横断照合用に移管する（分類②）。必要素材の着地照合とrelease close時の分類まで保持する。
- Temurin再確認の過去recordと旧Releaseは保持。Java方針の元packetは教材・ホームページへの転用完了まで保持する。userの`mise.toml`は変更・commitしていない。
- この票はMcRemoteの公開完了の事実を返すもの。VPS・他component・横断gateの最終判定は担当とcoordinatorの範囲。
