# b10 gate closeの素材（2026-10-17）

> b10横断release gate（`00-hub/release-gate-notes_ja.md`の2026-10-07の節）のclose分類（`00-hub/b10-gate-close-instructions_ja.md`、
> knowledge `91e7f4e22fa4bbdd98312b2ddb957ca2f7ed425d`）で、McRemoteとScratchが①とした素材を収容した。3 OSの試験の結果は
> `14-evidence/records/2026-10-17-b10-prerelease-3os-live-human_ja.md`にある。この記録は素材の置き場所と分類を示す。

## 収容した素材

| 収容先（`14-evidence/artifacts/2026-10-17-b10-gate-close/`） | 中身 | 搬送元 |
| --- | --- | --- |
| `scratch/2026-10-09-b10-scratch-local-candidate/` | 初回のCI candidate、同梱物のlicenseの分類、検証log | scratch-editor 同名 |
| `scratch/2026-10-09-b10-three-os-live/` | 初回の3 OSの導入の観測、miseでのJavaの切り替えの出力、Windowsの認証の障害の記録 | scratch-editor 同名 |
| `scratch/2026-10-09-b10-wirescope-local-candidate/` | WireScopeを同梱した後のcandidateの照合と検証log | scratch-editor 同名 |
| `scratch/2026-10-12-b10-local-launcher-ux/` | 起動と設定の導線の観察、設定画面の画像 | scratch-editor 同名 |
| `scratch/2026-10-14-b10-candidate/` | 公開の直前のsourceと3つのZIPの固定、Release本文の元の案 | scratch-editor 同名 |
| `scratch/2026-10-14-b10-prerelease/` | 公開した7 assetのGitHubのdigestと取得した実体の照合 | scratch-editor 同名 |
| `mcremote/2026-10-09-b10-three-os-live-observations/` | 初期のmacOSの起動とペアリングの観察（exact identityは採っていない） | McRemote 同名 |
| `mcremote/2026-10-09-b10-windows-persistence-options/` | WindowsのDirectoryForceProbeの実機の報告 | McRemote 同名 |
| `mcremote/2026-10-10-b10-paper-sqlite/` | WindowsのDLLの比較（4件、OSのloadとJNIの初期化まで） | McRemote 同名 |
| `mcremote/2026-10-10-windows-startup-investigation/` | 過去のCodeIntegrityの拒否、署名とeventの照合、nativeの失敗、診断素材の不足 | McRemote 同名 |
| `mcremote/2026-10-13-b10-paper263/` | 26.3のcandidateを採ったときの実測のidentityと確認票 | McRemote 同名 |
| `mcremote/2026-10-14-b10-prerelease/` | 公開のときのGitHubのdigestと取得の照合、tagとtagのCIの一致、Latestの確認、公開workflow | McRemote 同名 |

Scratchの79 file（1,151,600 bytes）は搬送元の一覧（scratch-editor
`handoff-materials/2026-10-17-b10-close-inventory/materials/EVIDENCE_FILES.tsv`）、McRemoteの20 file（54,588 bytes）は搬送元の一覧
（McRemote `handoff-materials/2026-10-17-b10-close/materials/promotion-files.json`）のbytesとSHA-256で照合した（不一致0）。McRemoteの
20 fileは担当が匿名化し直したcopyで、うち8 fileは元のfileとbytesが違う（担当の`redaction-report.json`）。収容の後、coordinatorが
private addressや利用者名などの定型を点検した。UUIDの形の値はMicrosoftの公開のpolicyのIDだけだった。

## 分類

| 担当 | ① | ② | ③ | 設計・アイデア文書 |
| --- | --- | --- | --- | --- |
| Scratch | 6 directory | 10 directory | 0 | 設計・アイデア文書を含むdirectoryはすべて②にした |
| McRemote | 6 directory（20 file） | HUDの2 file、Windowsでのmiseの導入の1 file、close返却packet | 8 directory | ③のMarkdown 57件を遅延削除として保護した |

human owner（2026-10-17）：設計やアイデアの文書は遅延削除とする。日付で消さず、rc1の準備か初回stableの後の該当の設計を
再開するときに読み戻し、アイデアがknowledgeか後続の入力へ移ったことを確かめてから消す。①の元は、この収容の照合の後に
担当が整理してよい。
