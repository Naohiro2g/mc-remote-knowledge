# b10 Scratch candidate返却票

- knowledge contract path: `00-hub/release-gate-notes_ja.md` b10「次の操作（2026-10-14）」、`13-scratch-client/scratch-lan-package-design_ja.md` §5・§7・§8、`00-hub/DECISIONS_ja.md` `2026-10-14-01`
- knowledge contract commit: `d4678134260f161c17c0f39ce8c0befe9ad53c1b`
- Scratch branch／source commit: `agent/b10-scratch-local@0809eb5e49e4b83c17a4e91b435d151b9d1b0655`（push済み）
- default branch統合: **pre-releaseより前に**`develop`をこのsource commitへstrict fast-forwardする必要がある。b10の公開workflowは本branchで変更されており、現行`develop`のrelease event workflowには固定candidate ZIPの収集とmanifest v2生成がない。現時点で`origin/develop...HEAD`は`0 ahead / 6 ahead`でfast-forward可能。coordinatorの公開指示までは統合しない
- 公開workflowの入力: `release`イベントには`workflow_dispatch`の入力が来ないため、公開前にrepository variables `SCRATCH_LOCAL_CANDIDATE_ARTIFACT_ID=11862469927`、`SCRATCH_LOCAL_CANDIDATE_ARTIFACT_DIGEST=sha256:6576a64d75f7eb46f2245ea5d38b336e18388131c79b0db869e693edc3a1fb23`を設定する必要がある。2026-10-14のGitHub APIでは両変数とも404（未設定として扱う）。別案はRelease作成後の手動`workflow_dispatch`へ同値を入力するが、通常の`release`イベントrunが先に失敗しうるので推奨しない
- CI run: [38495047680](https://github.com/Naohiro2g/scratch-editor/actions/runs/38495047680)、source commit `0809eb5e49e4b83c17a4e91b435d151b9d1b0655`、conclusion `success`
- Actions artifact ID: `11862469927`、名前 `scratch-candidate-0809eb5e49e4b83c17a4e91b435d151b9d1b0655`、外側archive 1,368,927,620 bytes／`sha256:6576a64d75f7eb46f2245ea5d38b336e18388131c79b0db869e693edc3a1fb23`。実archiveの全bytesを取得し、SHA-256をGitHub APIのartifact metadataと独立に照合済み。ZIPの展開もPASS
- 3 OS ZIP（CI logとActions artifactの実fileで照合。すべて`working_tree_dirty:false`、同一source commit）:

  | OS | bytes | SHA-256 |
  | --- | ---: | --- |
  | windows-x64 | 261,590,008 | `00e73b71d63859f088595257abdec7ce204a09282d79f26daa8d851e0f4af1e8` |
  | macos-arm64 | 265,941,672 | `edcc757b931d8b89fc18487ee385c20d9ecbdc398b7f34f017e2137fe26c12d2` |
  | linux-x64 | 271,197,726 | `b69e5b1118dba284604c217b0f3b06ea40b9876014166461705fdc400f647526` |

- `candidate-manifest.json`: 2,676 bytes／SHA-256 `02d82f0cfabfa7caa5120f53c19c811ad7a913132dda2a5add9ed97c67a3b923`。9 artifact entryのfile bytes／SHA-256をすべて実fileと照合済み
- 固定Bridge／WireScope（`mc-remote/tooling-lock.json`）：tooling source `dc1ab834183e29f2eb03059b07e99d2b463776ee`。Bridge OCI archive 114,628,096 bytes／SHA-256 `b6a6feec07e8d7ae9805a81e8dc370e6220e91af145ef3117ce5ed12e703b100`、OCI index digest `sha256:5828304c9bb1d60df8672f9189f503790050e09358bd375f39e4d59d190eb84f`。WireScope ZIP 83,854 bytes／SHA-256 `da3da0b6cf4d05265bc0c11abaa4913208c7cfc3600b0c3e78c93a356fc431ad`、detached manifest 2,339 bytes／SHA-256 `c654f7d1f0be2773d6737e889279b2587317088717f162b082c82be9cff910d7`。CIのdigest保存性チェックPASS。取得artifactの実fileと全3 ZIP内の`data/identity.json`をtooling lockへ独立に照合済み
- manifestの区別: candidate artifactにあるのは`mc-remote.candidate-manifest` v1の`candidate-manifest.json`。公開用`mc-remote.release-manifest` v2の`manifest.json`はtag／Releaseを作った後、公開workflowが固定candidateとOCI digestから生成する。CIはv2 schemaと共有fixtureのconsumer testをPASSしている
- 公開v2の事前生成: 同じcandidateの3 ZIP・contracts・WireScope pair、Scratch OCI digest `sha256:3add03deeb308c22439d01badffe984ba6076d8ea18a40d6538a5c294f611339`、固定Bridge digestを入力に`materials/PROVISIONAL_RELEASE_MANIFEST.json`を生成し、v2契約検証PASS。2,105 bytes／SHA-256 `67b92f8a7b0ddaee6ac0e966c21d5558b573936cc7b6a60b20ab1bc29de31a2c`。これは**公開manifestの予告値ではない**。公開workflowが実際に採用したScratch OCI digestとRelease assetから生成した`manifest.json`を、公開後に改めて照合する
- ライセンス: `mc-remote/local/LICENSE_REVIEW_ja.md`は依存更新前135件を再分類し、手元の入力132件（runtime 26／build-only 106）を記録。**このCI配布物の正は全3 ZIP内`data/licenses/review.json`の130件（runtime 26／build-only 104）**で、差はCIに入らなかったbuild-onlyの`@napi-rs/wasm-runtime 1.1.1`と`@tybys/wasm-util 0.10.1`のみ。runtime 26件へ本文とnoticeを補充済み。`microee 0.0.6`の原表記「BSD」の条項数は未確定で、参考BSD-3本文と原表記を並記。knowledge b10 gateの2026-10-09 human owner「案A、ライセンスそのままで」に従う
- tests: 本番build PASS、Scratch GUI unit 535 PASS（1 skipped）、Scratch Local Node 22＋Python 11 PASS、release manifest共有fixture 93 PASS、candidate manifest 6 PASS、GUI lintエラー0、local／manifest lint PASS。CI runもbuild、local boundary、tooling／v2 manifest consumer、固定Bridge digestの照合を含めて`success`。CI Linux ZIPの同梱Node起動・3 port終了・Bridge WS→TCPをPASS。取得した3 ZIPは`unzip -tq`ですべてCRC PASS
- 未実施: 今回の固定ZIPの3 OS実機取得・展開・接続、ペアリング待ちの表示、`.sb3`の配布ZIPでのドロップ操作。pre-release後の実施票で確認する
- manifest role: `scratch-local`を維持する案。tooling v2 schemaはroleの語彙を列挙せず、Scratch producerとStack consumerがこのroleで実装済み。名前の変更には両者とrelease contractの更新が要るため、b10では変更しない
- File System Access書き出し: b10へ入れない案。現在のブラウザー保存とファイルダウンロードを維持し、投入releaseはcoordinatorへ返す。初回stable後のsliceが候補
- Release本文案: `materials/RELEASE_NOTES_DRAFT_ja.md`
- tag／Release: 未作成。coordinatorの別指示待ち

## knowledge着地確認

- `.sb3`搬送票はknowledge `13-scratch-client/scratch-project-storage-transfer-design_ja.md` §8、`scratch-roadmap_ja.md`の保存・移送作業束、`scratch-lan-package-design_ja.md` §7と照合。単一ファイルのドロップ、ブラウザ保存成功後の切り替え、失敗時の作品保持とエラー、上流へ「確認なし」を持ち込まない境界が一致
- 入門導線搬送票はknowledge DECISION `2026-10-14-01`、LAN設計 §5／§9、b10 gate、hub NOTESと照合。WindowsのZIP展開前の「許可する」、Smart App Controlを切る方法を利用者手順に入れないこと、専用Scratch入門ページができてから内容を共通化する順序、ホームページ画像のhuman owner担当が一致
- ローカルの設計§7・§15と`NOTES_ja.md`の捕捉はDEC参照で閉じた。両packetはknowledge着地後の履歴素材として保持し、新しい未着地依頼としては扱わない
