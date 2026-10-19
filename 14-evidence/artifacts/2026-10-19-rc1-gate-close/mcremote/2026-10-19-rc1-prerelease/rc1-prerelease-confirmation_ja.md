# McRemote rc1公開確認票 — 2026-10-19

## Release gate 確認票

- 対象 repo: `Naohiro2g/McRemote`
- 対象 branch/commit: remote `main@192a777ae1d484bcc9b58fcc7c58d6aed1a374af`。`e2ed84df9498ad2fbe88f75759d8f0110f32f85f`から2 commitsをfast-forwardし、候補source SHAを維持した。
- release / channel: `v2321.0.0rc1`、protocol `23.2.1`、GitHub prerelease。
- gate coordinator: knowledge担当session（Claude Code）。human release owner: プロジェクトオーナー。
- current phase: human ownerの合格・公開依頼（2026-10-19）に基づくMcRemoteの公開完了。横断gateの最終判定はcoordinator。
- knowledge contract path: `00-hub/rc1-gate-release-instructions_ja.md`の「共通」「McRemote」、`00-hub/release-gate-notes_ja.md`、`00-hub/release-operations-responsibility-design_ja.md`。
- knowledge contract commit: `32fd7d4892a410ef9d38f90320a511f383aaa9f9`（remote mainからruntime protocol／INDEX／上記文書を実読）。
- gate manifest identity: `rc1-integrated-artifact-set-1`。McRemote source `192a777ae1d484bcc9b58fcc7c58d6aed1a374af`、JAR 315,352 bytes／SHA-256 `917c358c201aa219277b96a447fb85116e8bdb0260870a4d76a8c51219d31c37`。
- tag: `v2321.0.0rc1`（annotated tag object `15b3f52a13cd77337349a938ae713c4d0bdce0b3`）→ commit `192a777ae1d484bcc9b58fcc7c58d6aed1a374af`。GitとGitHub APIで照合。
- Release URL: <https://github.com/Naohiro2g/McRemote/releases/tag/v2321.0.0rc1>（Release ID `417021272`、published at `2026-10-19T07:50:22Z`）。
- 公開属性: `prerelease=true`、`draft=false`、`latest=false`で公開。latest endpointは既存の`v1.21.8-1.4.0`（Release ID `233734810`）を引き続き返すことを照合。
- change cone: 凍結sourceのmain統合、annotated tag作成・push、同sourceのtag CI、draftと版別record準備、公開workflowのdry run、公開、asset照合。製品sourceの追加変更なし。
- reused PASS / rationale: 候補で実施済みの1.21.11 #132／26.3 #203のpulse・通常再起動・旧23.2.0 helloのrecordを、同じsource／JAR bytesと照合して使用した。公開workflowはtag CIのJARを再buildせず昇格した。公開のための新しいlive試験は行っていない。
- exact compatibility set / freeze status: 凍結setのMcRemote identityを維持。対応Minecraft宣言は`["1.21.11", "26.3"]`。
- target deployment / profile / lock: 公開操作はGitHub Releaseのみ。shared環境／公開VPSの変更は未実施。
- authorized next action: coordinatorへ公開identityを返す。ホームページ／Stack／他componentの公開後の作業は、それぞれの担当に渡された指示に従う。
- test class: unit/deterministic（tag CI、release script／manifest検証、digestとraw bytes照合）。live-auto／live-humanは候補の結果を同一bytesに対して使用。
- 実行した command / 手順: mainを`git merge --ff-only 192a777ae1d484bcc9b58fcc7c58d6aed1a374af`してpush。`git tag -a v2321.0.0rc1 192a777ae1d484bcc9b58fcc7c58d6aed1a374af`をpush。tag CIを待ち、provider ZIP／source stamp／JARを検査。版別record2件を添えたdraftでrelease workflowのdry runを実行し、生成manifestが候補のmanifestと等しいことを照合。`gh release edit --draft=false --prerelease --latest=false`で公開。公開workflow成功後に全5 assetを認証headerなしのHTTPSで取得し、provider digest／手元の凍結素材／実fileを照合。
- 結果: 下表の全5件がbytes・SHA-256・raw bytesで一致。JARは公開前・公開後ともknowledgeの凍結値と全桁一致。source commit／main／tag targetは同じSHA。Release本文には23.2.1、23.2.0のserver／clientとの互換を試験確認したこと、feedbackフォームを記載。
- evidence record / artifact: このpacketの`public-assets-verification.json`、`tag-ci-identity.json`、`release-dry-run-verification.json`、公開本文、JAR、対応版宣言、manifest、版別records。正式evidenceへの配置はknowledge担当。記録path案: `14-evidence/records/2026-10-19-rc1-mcremote-prerelease_ja.md`。
- 未検証の境界: 新しいshared deploy／公開VPS切替はこの作業の外。横断合否・他component公開の完了は判定しない。
- security / compatibility / rollback の確認: 認証・config・DB・APIの変更なし。検証record内のtoken／UUIDは候補時にsanitized済み。公開JARが試験時の同一bytesであることを確認。
- 判定を求める事項: coordinatorの公開後照合と横断gateの後続処理。

## runとartifact

| 操作 | run ID | 結果 |
| --- | --- | --- |
| tag CI | [39216357412](https://github.com/Naohiro2g/McRemote/actions/runs/39216357412) | success |
| 公開workflow dry run | [39217207650](https://github.com/Naohiro2g/McRemote/actions/runs/39217207650) | success、生成manifestは凍結素材と一致 |
| 公開workflow | [39218586262](https://github.com/Naohiro2g/McRemote/actions/runs/39218586262) | success、再buildせずtag CIのcandidateを昇格 |

- tag CI candidate artifact: ID `12170425142`、ZIP 294,255 bytes／`sha256:6f0318caa196b7c58d56b070f6a4505ad3e916457a26ecc4288cdfb9dc08d224`。providerのdigestと取得ZIPの実digestは一致。ZIP自体は候補時のZIPとdigestが違うが、展開した全4 file（JAR／宣言／source stamp／SHA256SUMS）は凍結candidateとbytes同一。

## 公開assetの照合

| file | bytes | SHA-256（provider／匿名HTTPS取得file／凍結素材共通） | 結果 |
| --- | ---: | --- | --- |
| `manifest.json` | 1,988 | `e49761d22c8c60ac49915d04f1c6236ca101b13bf94b257c0cbcbb4328c6a1c2` | 一致 |
| `mc-remote-2321.0.0rc1.jar` | 315,352 | `917c358c201aa219277b96a447fb85116e8bdb0260870a4d76a8c51219d31c37` | 一致 |
| `mc-remote-verification-1.21.11.json` | 62,784 | `b3ae515b037429517ce1f90bc1708d3feeebef4bc9bd359fcf175a5e0a221f49` | 一致 |
| `mc-remote-verification-26.3.json` | 62,766 | `82b62c167bc11b13128f06724b0f66051509ba192d5e302b50d92625a54d0c66` | 一致 |
| `minecraft-targets.json` | 126 | `8e830732decd6bcde13f91eb6c071d062ba6993342a7edb52e6ea543b9e0c361` | 一致 |

## 引継ぎとローカル状態

- 公開sourceはmainへ統合済み。作業branch `agent/rc1-pre-fixture`と公開tagを保持している。
- 候補packet `handoff-materials/2026-10-18-rc1-candidate/`、前段の確認票、今回の公開packetはcoordinatorのclose／正式evidence移管時の分類用に保持。今回の公開処理だけで素材を削除していない。
- `NOTES_ja.md`へ公開identityと後続の照合待ちを記録。製品sourceの追加commitはない。
