# Release gate notes — public baseline

> 新public正本世代の単一template／状態集約。旧世代のrelease固有履歴はcarryしない。

release判定は、実装repo側が事実と根拠を記入し、単一のgate coordinatorがknowledge側で
contractと照合します。shared環境へのcandidate deployと人間参加試験は、coordinatorがexact setと
許可済みの次操作を示した後に行います。責務と正準進行は
[release運用と責務分担](release-operations-responsibility-design_ja.md)を参照します。
秘密実値、private inventory、未sanitized raw logはここへ貼りません。

## 確認票

```markdown
## Release gate 確認票

- 対象 repo:
- 対象 branch/commit:
- release / channel:
- gate coordinator:
- human release owner:
- current phase:
- knowledge contract path:
- knowledge contract commit:
- exact compatibility set / freeze status:
- target deployment / profile / lock:
- authorized next action:
- test class: unit/deterministic / live-auto / live-human
- 実行した command / 手順:
- 結果:
- evidence record / artifact:
- 未検証の境界:
- security / compatibility / rollback の確認:
- 判定を求める事項:
```

`live-human` や高い再現コストを持つ検証は `14-evidence/` の sanitized record を参照します。private evidence は `mc-remote-backstage`、秘密を含む raw は Git 外です（`2026-07-06-03` / `2026-07-21-04`）。

repo担当は自repoの事実と根拠を返し、他repoの着手、shared環境へのdeploy、人間参加試験、横断判定を
開始しません。candidate identityが変わった場合は旧exact setを失効させ、gate coordinatorへ戻します。

## 2026-08-21 b5横断release gate（進行中）

- gate coordinator: knowledge担当session。人間による明示handoffなしに他担当へ移さない
- human release owner: プロジェクトオーナー
- current phase: component candidate準備／通常dev環境の設計準備
- contract: 技術scopeはDECISIONS `2026-08-21-01`／`2026-08-21-02`およびknowledge `f50ebb13f00facfc2e73163a24f002f4c8b77d43`、進行責任は`2026-08-21-03`／`2026-08-21-04`およびknowledge `575ce310048525f38e11815c8a38d01658b843b3`
- exact compatibility set / freeze status: **未凍結**。各componentのpush済みcandidateとcommon artifactの収束待ち
- component readiness:
  - McRemote: **決定論的candidate準備済み**。`main@6214a6a5efe5180c1cd0f374089736908b07ee34`、JAR SHA-256 `f293e63a77f178bc8d3cba8276e95124f2ee6b3eca77c15867a6fc5e5f166531`、85 tests PASS。GitHub remote main一致と変更範囲をknowledge coordinatorが再確認済み。live未実施
  - Scratch: event sliceとcommon WireScope artifact待ち
  - Python: Scratch common artifact受領後の再固定待ち
- input correction: McRemote作業票のknowledge SHA `f50ebb17…`は存在せず、実在する`f50ebb13f00facfc2e73163a24f002f4c8b77d43`を参照。契約差分なし
- target deployment / profile / lock: 通常dev環境。exact deployment／profile／lockはStack確認後に固定。ケータリング型は本gate対象外
- authorized next action:
  - McRemote: candidateを変更せず待機する。追加のhuman／Stack／実server試験を開始しない
  - Scratch: event poller／3種hat／thread-local contextとcommon WireScope artifactを決定論的に完了し、push済みidentityを返す
  - Python: Scratch common artifact受領後に同梱artifactを再固定し、push済みwheel／sdist identityを返す
  - Stack／backstage: 通常dev環境のinventory、profile再利用可否、order／lock、preflight／doctor経路を準備する。candidate deployはまだ行わない
- live-auto / live-human: **未許可**。exact set凍結とenvironment readiness確認後にcoordinatorが統一実施票を発行する
- non-claim: component GREEN、b5横断GREEN、通常dev環境完成、release承認をまだ主張しない

## 2026-08-07 Scratch editor `2100.0.0b3`

- candidate: `release/b3@3f1a10a366bfbe76e32b5a31c54da19eddd56e56`
- contract: `13-scratch-client/scratch-roadmap_ja.md` §2.3 / knowledge `3dfbf57c07f2b7985c65edc5564b879f9e67e122`
- CI: run `31145335984`、exact candidate、全job success
- evidence: `14-evidence/records/2026-08-07-scratch-b3-release-gate_ja.md`
- status: **GREEN — tag `v2100.0.0b3`とGitHub prerelease作成を承認**
- release条件: tag targetは上記candidate完全SHA、prerelease ON、draft OFF、Latest非対象
- rollback: `v2100.0.0b2@e19247069d1ae55037c0e9ffc52ea88cde612ac3`
- scope boundary: hosted surface更新は含めない。更新時はdeploy smoke / rollback / re-deployを別gateで確認する
- deferred: catalog picker / WireScope miniはb4、独立WireScopeは`2026-08-06-03`どおりb3非blocker

## 2026-08-07 b3 横断 milestone close

- status: **CLOSED — b3の横断スコープを完了扱いとし、b4の利用者向け機能へ進む**
- decision: `2026-08-07-01`
- Python API: `v2100.0.0b3@af2d11d66a16e3085f569241406a703a1c28c348`、GitHub prerelease、PyPI非公開。正式live根拠は `14-evidence/records/2026-08-06-b3-python-catalog-projection-live-human_ja.md`
- McRemote: `v1.21.11-2100.0.0b3@a3dab998b710f65f42f95058a68ec51d419b097c`、GitHub prerelease、JAR SHA-256 `aeb190705bd9957ce73557dc1be0fe15efe7250ba9bc688945e6f537e00ef78e`
- Scratch editor: `v2100.0.0b3@3f1a10a366bfbe76e32b5a31c54da19eddd56e56`、GitHub prerelease。正式gate根拠は `14-evidence/records/2026-08-07-scratch-b3-release-gate_ja.md`
- scope: versioning §10.11.1項14のcatalog一式、Scratch現行roadmapのb3 scope、各componentのb3 prereleaseを区切りとして閉じる。component番号の永久同期やstable releaseを主張しない
- deferred: long-lived credentialの公開gate、checkpoint＋doctor、end-to-end snapshot rollback、reset／災害復旧は閉じたまま後続へ送る。既定は`session`のまま
- non-claim: Stackの一般profile公開、hosted surface更新、long-lived公開可否をGREENとする記録ではない。これらをb3完了へ遡及混入しない

## 2026-08-16 Python `2100.0.0b4` candidate

- candidate: `codex/b4-player-pose@4d510442db58a94f8b249ddcd9d959381f97276c`
- contract: DECISIONS `2026-08-16-08` / knowledge `b747fa2b3b6c278f1a8e920ba8e02b45e2cf2b47`
- evidence: `14-evidence/records/2026-08-16-b4-python-pose-wirescope-live-human_ja.md`
- status: **PYTHON CANDIDATE PASS — tag／releaseは未承認**
- verified: candidate wheel、main stream 1件、`player.getPose`／`player.setPose`、origin相対座標、automatic browser launch、WireScope UI、終了表示、distribution／license gate
- compatibility set: McRemote `9df8c46d600ff9605dc1822b304715de713e6767` / JAR SHA-256 `ab3b87c38b6876ec4ba26112eff35d7cb016395a1dae1661578fd3690e1dbc46` / WireScope source `56011f71291f47ced69cc4e3c377734f501b6081` / ZIP SHA-256 `1a56617c78c283332f1afe3bdd3797ab37f0cdc3455c86c73c926c751721657f`
- rollback candidate: `v2100.0.0b3@af2d11d66a16e3085f569241406a703a1c28c348`。rollback実操作と再復帰は未実施
- remaining: Scratch／Pythonの順次横断real-browser E2E、home alpha、plugin artifactを含むexact compatibility set最終批准、release後identity確認
- non-claim: 本項だけでPython tag、GitHub prerelease、横断b4 milestoneをGREENにしない

## 2026-08-16 Scratch editor `2100.0.0b4` candidate

- candidate: `release/b4@56011f71291f47ced69cc4e3c377734f501b6081`
- contract: DECISIONS `2026-08-16-08` / knowledge `b747fa2b3b6c278f1a8e920ba8e02b45e2cf2b47`
- CI: run `31934776981`、exact candidate、全job success
- evidence: `14-evidence/records/2026-08-16-scratch-b4-release-gate_ja.md`
- status: **SCRATCH COMPONENT GREEN — tag／releaseは横断gateまで保留**
- verified: Catalog Picker、`player.getPose`／`player.setPose`、Scratch main stream 1件のMessageChannel観察、pose対応common app、clean artifact reproduction、unit／build／CI
- common artifact: ZIP SHA-256 `1a56617c78c283332f1afe3bdd3797ab37f0cdc3455c86c73c926c751721657f` / manifest SHA-256 `f3ec11496b595bbca4ba27a6e938a1149336eb5a2da55e742d60e1681cf4d154`。Python candidateと一致
- rollback target: `v2100.0.0b3@3f1a10a366bfbe76e32b5a31c54da19eddd56e56`。hosted deploy／rollback実操作／再復帰は未実施
- remaining: Scratch／Pythonの順次横断real-browser E2E、plugin artifactを含むexact compatibility set、home alpha、release後identity確認
- non-claim: 本項からPython／plugin／home alphaまたは横断b4 milestoneのGREENを推測しない

## 2026-08-17 b4 home-alpha pre-auth transport correction（初回観測）

- decision: `2026-08-17-01`
- evidence: `14-evidence/records/2026-08-17-b4-home-alpha-integration_ja.md`
- status: **PARTIAL PASS — one-shot認証とb4機能統合はPASS、session token再起動耐性はBLOCKED**
- observed gap: McRemote `dab6908494290c894d8efbe6828707e544860fa1`のclose-after-flushでもresponseからEOF観測まで約41msあり、Bridge経由で`auth_required`直後0msに送る`auth.pairBegin`はtimeoutする。100ms待機では成功し、直接新TCPでは成功したが、固定delayは解決として採用しない
- McRemote input: close-after-flush JAR SHA-256 `f902ed360ac1674143d8e79a49c8e109968f2c38dc36656c91a50dec89082aa8`。plugin追加変更は要求しない
- implemented set: Scratch／Bridge one-shot `8b69ecefc9771a47e2eac8bea242cf96c09d36f3`、pagehide lifecycle `1d2f18785d260564ad4bc30a26a45ef33fc813d6`、McRemote JARは上記digest、Python `4d510442db58a94f8b249ddcd9d959381f97276c`、WireScope ZIP `1a56617c78c283332f1afe3bdd3797ab37f0cdc3455c86c73c926c751721657f`
- passed: `auth_required`直後0msのone-shot pairing、Scratch／Python／WireScope実機一巡、canonical b3 rollback、corrected b4再適用
- failed: 同一corrected b4 runtimeの通常再起動後、期限内session tokenが`auth_required`。candidateはsession tokenをin-memoryだけに保持し、`2026-08-02-08`のhash-only snapshot永続化と不一致
- doctor gap: credential domain `UNINITIALIZED`を現行doctorが検出せずPASS。`2026-08-06-02`のcredential checkpoint／doctor contractは未実装
- next gate: McRemote session record永続化→artifact再固定→同一b4再起動とb3→b4再適用でtoken再利用→Stack credential health／doctor再照合
- non-claim: 既存のPython candidate PASS／Scratch component GREENと今回の機能統合PASSは維持するが、認証再起動FAILが閉じるまでhome-alpha認証、credential継続を含むrollback／再適用、b4 releaseはGREENにしない。100ms待機、EOF依存、自動再送をfixture／runbookへ残さない
- resolution: このFAIL観測は削除しない。後続McRemote `3496db9293baa6e1d4f79439cacbd239ba15e2b7`と`2026-08-18-b4-session-persistence-home-alpha`でsame-b4再起動とb4再適用後のtoken再利用がPASSし、最終判定は下記2026-08-18項へ移った

## 2026-08-18 b4 横断 release gate

- decision: `2026-08-16-08`／`2026-08-17-01`／`2026-08-18-01`
- status: **CLOSED — exact b4 compatibility setのGitHub prerelease公開identityを確認し、b4 milestoneを閉じる**
- protected value: Scratch／Pythonの保存済み建築コード。復旧基準はコード保存→空環境再構築→再pairing→必要なら書き換え→再実行
- exact set:
  - McRemote `3496db9293baa6e1d4f79439cacbd239ba15e2b7`／JAR SHA-256 `331633ef15a729658496e89fe49cb8a5eb5ebcb2ec86937b7e5313528d7ec997`
  - Python `4d510442db58a94f8b249ddcd9d959381f97276c`／wheel SHA-256 `eeed6261972987946b5e22dd8ff8d3533a758c7db57472d1d82766fbf964e7d0`
  - Scratch／Bridge one-shot `8b69ecefc9771a47e2eac8bea242cf96c09d36f3`、pagehide lifecycle `1d2f18785d260564ad4bc30a26a45ef33fc813d6`
  - WireScope ZIP SHA-256 `1a56617c78c283332f1afe3bdd3797ab37f0cdc3455c86c73c926c751721657f`／manifest SHA-256 `f3ec11496b595bbca4ba27a6e938a1149336eb5a2da55e742d60e1681cf4d154`
  - Stack `780d99291d669fd1ec98c513245bf6fdbac36271`／runtime implementation `cd3ff18e31534f394e5fc7ad63af1f164ce54f15`／`home-server@3`／`mcremote-paper@6`
- passed:
  - Scratch Catalog Picker、player pose、Scratch／Python main stream各1件の共通WireScope観察
  - pre-auth one-shot pairing、固定delay・自動再送なし
  - same-b4通常再起動後の期限内session token認証
  - b4再適用後の同token認証。b3はb4 session recordを読めずfail closedし、snapshotを破損しなかった
  - 新規world／credential環境でのScratch `.sb3`／Python source再pairing・再実行とserver側独立照合
  - b3 artifact rollback／b4再適用、exact artifact／lock照合
- formal evidence:
  - `2026-08-16-scratch-b4-release-gate`
  - `2026-08-16-b4-python-pose-wirescope-live-human`
  - `2026-08-17-b4-home-alpha-integration`（初回PASS／FAILを保持）
  - `2026-08-18-b4-session-persistence-home-alpha`
  - `2026-08-18-b4-code-preservation-recovery-live-human`
- release identities（GitHub API再確認済み）:
  - [Python `v2100.0.0b4`](https://github.com/Naohiro2g/minecraft-remote-api/releases/tag/v2100.0.0b4): target=`4d510442db58a94f8b249ddcd9d959381f97276c`、prerelease=true、draft=false、Latest非対象。binary assetなし、release notesにwheel／sdist digestを固定、PyPI／TestPyPI非公開
  - [Scratch `v2100.0.0b4`](https://github.com/Naohiro2g/scratch-editor/releases/tag/v2100.0.0b4): target=`1d2f18785d260564ad4bc30a26a45ef33fc813d6`、release ID `372338711`、prerelease=true、draft=false、Latest非対象、追加assetなし
  - [McRemote `v1.21.11-2100.0.0b4`](https://github.com/Naohiro2g/McRemote/releases/tag/v1.21.11-2100.0.0b4): annotated tag target=`3496db9293baa6e1d4f79439cacbd239ba15e2b7`、prerelease=true、draft=false、Latest非対象。asset=`mc-remote-1.21.11-2100.0.0b4.jar`／140,712 bytes／SHA-256 `331633ef15a729658496e89fe49cb8a5eb5ebcb2ec86937b7e5313528d7ec997`
- non-blocking observations:
  - b3はb4の`session` recordを理解せず`unknown_persisted_credential_type_session`となる。b3をcredential継続付きdowngrade runtimeとしては承認しない
  - checkpoint projectionは未実装で、Stack doctorは`doctor_credential_health_unsupported`としてfail closedする。これをdoctor PASSへ読み替えない
- deferred / non-claim: long-lived credential一般公開、checkpoint／doctor完成、world backup／restore、一般Stack profile、public hosted deployment、PyPI／Modrinth公開、substream／multi-stream、b5以降。これらをb4 GREENから推測しない
