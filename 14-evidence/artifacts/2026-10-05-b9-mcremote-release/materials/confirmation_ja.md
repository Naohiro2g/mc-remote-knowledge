# B9 McRemote 公開確認票

**公開完了。** mainとtag targetは凍結source `5cb33ebad4bf2c5e36c3433b0f70fe6070915b00`。tag CIと固定Release workflowはSUCCESS。公開JARを取得し、凍結JAR・tag CI candidateとbytes／SHA-256が一致、公開manifestの参照identityも一致することを確認した。

Release: [McRemote 1.21.11 / 2320.0.0b9](https://github.com/Naohiro2g/McRemote/releases/tag/v1.21.11-2320.0.0b9)

## Release gate 確認票

- 対象 repo: `Naohiro2g/McRemote`。
- 対象 branch/commit: `main@5cb33ebad4bf2c5e36c3433b0f70fe6070915b00`。`feat/b9-contract-packaging`の凍結sourceをfast-forwardで統合。ローカルmain／origin/main／GitHub mainが一致し、tracked treeはclean。
- release / channel: `v1.21.11-2320.0.0b9` / GitHub beta prerelease。title `McRemote 1.21.11 / 2320.0.0b9`、prerelease ON、draft OFF、Latest非対象で作成。protocol `23.2.0`。
- gate coordinator: knowledge担当session（Claude Code）。
- human release owner: プロジェクトオーナー。2026-10-05の明示承認がSSOTに記載済み。
- current phase: B9 GREEN／release authorizationを受領し、McRemoteの公開と公開後照合を完了。横断closeはcoordinator側。
- contract maturity / required test tier: exact set凍結・指定Tier 3実機試験完了。今回は公開identity／artifactの照合、live再試験なし。
- knowledge contract path: `00-hub/release-gate-notes_ja.md` B9 release authorization／凍結set／GREEN、`00-hub/release-operations-responsibility-design_ja.md` §7・§10・§12、`14-evidence/records/2026-10-05-b9-dev-live_ja.md`。INDEXを入口に参照。
- knowledge contract commit: 指定authorization `d6d59d91032230a959b7288807179e1bd8100041`。最新runtimeはremote main `6df2d14033a4646ce958737c06849725fcaee51e`から取得。同mainのrelease-gateも読み、McRemoteへの公開指示が同一であることを確認した。最新のPython digest訂正／Scratch OCI packaging追記はMcRemoteの指定identityを変更しない。
- gate manifest identity: `b9-integrated-artifact-set-1`、指定authorization commitのrelease-gate-notes。
- change cone: 公開操作のみ。凍結sourceへのmain fast-forward、annotated tag、tag CI、承認済みRelease公開、固定workflowで既存candidateの昇格。製品source／JARへの追加修正なし。
- reused PASS / rationale: 同一source・同一JARの既報281 deterministic tests、JAR再現性、segment 1 live-auto60 PASS行／FAIL0、chat nullとsegment 0観測を再利用。正式live recordのMcRemote記載は担当素材と一致。今回はtag CIを新規実行し、公開artifactを照合した。
- exact compatibility set / freeze status: 凍結 `b9-integrated-artifact-set-1`。McRemote source／artifact identityを維持。toolingの先行公開をGitHub APIで確認し、WireScope ZIP／manifestは凍結digest一致、tooling annotated tag targetは `dc1ab834183e29f2eb03059b07e99d2b463776ee`。
- target deployment / profile / lock: 今回はGitHub Release公開。通常devの稼働serverやdeployment設定は操作していない。
- authorized next action: 承認済みMcRemote main統合・tag CI一致後のprerelease公開を実施済み。coordinatorへ公開identityを返し、read-only照合と横断closeに用いてもらう。
- test class: `unit/deterministic`はtag CI build、その他はGit／provider APIとartifact実bytesのstatic identity照合。新規live-auto／live-humanなし。
- 実行した command / 手順: 下記「手順と照合」。
- 結果: main／tag target一致、tag CI SUCCESS、JAR凍結値一致、固定Release workflow SUCCESS、公開assetの実bytes／provider digest／manifest identity一致。Release ID `403397549`。
- evidence record / artifact: 本directoryのJSON／candidate／公開asset／Release notes／分類票。正式live recordは上記knowledge SHAの `14-evidence/records/2026-10-05-b9-dev-live_ja.md`。本公開素材は分類②でB9 coordinatorへ移管し、正式knowledge authoringはknowledge側。
- 未検証の境界: 他repoの公開完了／PyPI.orgの版、Bridge OCI container起動、公開deployment、実機rollback、cold-reader、Paper 26.3／単一JAR。既存live正式artifact全fileのbyte移管検証は今回未実施。
- security / compatibility / rollback の確認: 認証／config／credential／worldへの追加操作なし。公開sourceは凍結commit、公開JARは実機試験時と同一digest。既存b8 tag／Releaseや退避JARを差し替えない。rollbackの実行なし。
- 判定を求める事項: この公開identityと添付素材をread-only照合し、McRemote公開完了としてB9 gateに収容すること。横断判定とcloseはcoordinatorに返す。

## 手順と照合

1. source branch／main／既存tag／Release状態をAPIとGitで確認。main旧先頭 `14cd3b733169c246215d39af122688cb2de525f1` は凍結sourceの祖先だった。
2. tooling先行公開を確認（Release ID `403384824`、tag `v2320.0.0b9`、prerelease true、draft false）。toolingを変更していない。
3. `git switch main`、`git merge --ff-only 5cb33ebad4bf2c5e36c3433b0f70fe6070915b00`、main push。merge commitや追加製品commitを作らず凍結sourceそのものへ統合。
4. 同commitへannotated tag `v1.21.11-2320.0.0b9`を作成・push。tag object `b4e264ffae083106db9f3d9a9287b8075bb33e37`、peeled target `5cb33ebad4bf2c5e36c3433b0f70fe6070915b00`。
5. [tag CI run 37268144239](https://github.com/Naohiro2g/McRemote/actions/runs/37268144239) SUCCESS後、`mc-remote-candidate`を取得。`source-commit.txt`、SHA256SUMS、実JARのbytes／SHA-256を照合してから公開。
6. 以下を実行し、Release公開を固定workflowのtriggerにした。

```sh
gh release create v1.21.11-2320.0.0b9 --repo Naohiro2g/McRemote --verify-tag \
  --title 'McRemote 1.21.11 / 2320.0.0b9' --prerelease --latest=false \
  --notes-file handoff-materials/2026-10-05-b9-mcremote-release/materials/release-notes_ja.md
```

7. [Release workflow run 37268629380](https://github.com/Naohiro2g/McRemote/actions/runs/37268629380) SUCCESS。固定workflowがtag CI candidateを再buildせず昇格し、JAR／manifestを添付した。
8. 公開assetをdownloadし、candidateとのbyte一致と以下を検証。

| 項目 | 公開値・確認 |
| --- | --- |
| main／tag target | `5cb33ebad4bf2c5e36c3433b0f70fe6070915b00` |
| JAR | `mc-remote-1.21.11-2320.0.0b9.jar`、261,016 bytes |
| JAR SHA-256 | `4feb90dbdba8550cd16800cc3d384e42fed16a5c5e20faa489a0381ad2cda58e` |
| manifest bytes／SHA-256 | 387 bytes／`1b18e60c473116f450f75882814db7cf9640aa29d34839faa40bc02b7ed00fd6` |
| manifest release_tag | `v1.21.11-2320.0.0b9` |
| manifest source_commit | `5cb33ebad4bf2c5e36c3433b0f70fe6070915b00` |
| manifest artifacts | role `jar`、kind `https-file`、上記JAR filename／SHA-256と一致 |
| Release状態 | title一致、prerelease true、draft false、作成と固定workflow双方でLatest非対象を明示 |

## 素材と引継ぎ

- [release-result.json](release-result.json)：最終照合集計、公開URL／時刻、source／tag／CI／workflow／JAR／manifest identity。
- [prepublish-verification.json](prepublish-verification.json)：公開前のtag CI candidate照合。
- `tag-ci-run.json`、`tag-ci-artifacts.json`、`tag-ci-candidate/`：公開前のCI素材。
- `release-final.json`、`release-workflow-run.json`、`remote-main.txt`、`remote-tag.json`、`published-assets/`：公開後APIとasset本体。
- [release-notes_ja.md](release-notes_ja.md)：実際に公開したRelease本文。
- [handoff-classification_ja.md](handoff-classification_ja.md)、[handoff-classification.json](handoff-classification.json)：現存7搬送directoryを全件分類②、B9 coordinatorへ参照identityと次の一手を明示して移管。local copyは保持。

knowledge作業cloneを操作せず、本素材はgitignore対象。正式record／artifact／gate notesへのauthoring・commitはknowledge側。
