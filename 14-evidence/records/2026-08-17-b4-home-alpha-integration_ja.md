# b4 home-alpha 統合・認証再起動 evidence

## Record

- test ID: `2026-08-17-b4-home-alpha-integration`
- test class: `live-auto` + `live-human`
- result: **PARTIAL PASS — b4機能統合／one-shot認証／rollback再適用はPASS、session token再起動耐性はFAIL**
- observed date: `2026-08-17`〜`2026-08-18`
- source repository: `Naohiro2g/mc-remote-stack`
- source branch: `agent/b4-home-alpha`
- source commit: `d91235b334957925ad9b876961373e382b3cc568`
- environment: isolated home-alpha / private forwarded topology
- decision: `2026-08-16-08` / `2026-08-17-01`
- knowledge contract at test start: `8e00a1dc6a888d567b192e6d172b81aa9bbeb8b9`
- knowledge contract at auth restart retest: `e6e0c1d56022743b9d19ca7fb7c72e21eda6015e`

本recordは、b4 exact compatibility setをhome-alphaへ配置し、Scratch／Python／WireScope、b3 rollback、
b4再適用、pre-auth one-shot transport、session token再起動耐性を一連で検証した結果を固定する。
機能統合のPASSと認証永続化のFAILを相殺せず、別の主張として扱う。本recordだけでb4 releaseをGREENにしない。

## Exact compatibility set

| Component | Identity |
| --- | --- |
| Stack source | `d91235b334957925ad9b876961373e382b3cc568` |
| Stack preset | `mcremote-paper@5` |
| b4 lock | `sha256:d2a2f7dce08ce5e56f688d217dfbc68556d2c76ac9a7038040ee06dd0a4cc23e` |
| b3 rollback lock | `sha256:0bcace337a82f9197b5bcb3e6237ec27a8a12b42fbdfcaafbfa1f01332bcaf08` |
| McRemote source | `dab6908494290c894d8efbe6828707e544860fa1` |
| McRemote artifact | `mc-remote-1.21.11-2100.0.0b4.jar` / 140,590 bytes |
| McRemote JAR SHA-256 | `f902ed360ac1674143d8e79a49c8e109968f2c38dc36656c91a50dec89082aa8` |
| Scratch／Bridge one-shot source | `8b69ecefc9771a47e2eac8bea242cf96c09d36f3` |
| Bridge CI artifact | ID `9283550231` / digest `sha256:fa62fff67311e365b2c02c9a79c47c288192bb0495bec7f962638d6f5ce7236c` |
| Scratch pagehide source | `1d2f18785d260564ad4bc30a26a45ef33fc813d6` |
| Scratch GUI artifact | ID `9287627432` / digest `sha256:924254363ab431c1f11ea8661f950b9325da56c248f52613cf87d70cb6562a71` |
| Python source | `4d510442db58a94f8b249ddcd9d959381f97276c` |
| Python wheel SHA-256 | `eeed6261972987946b5e22dd8ff8d3533a758c7db57472d1d82766fbf964e7d0` |
| WireScope ZIP SHA-256 | `1a56617c78c283332f1afe3bdd3797ab37f0cdc3455c86c73c926c751721657f` |
| WireScope manifest SHA-256 | `f3ec11496b595bbca4ba27a6e938a1149336eb5a2da55e742d60e1681cf4d154` |

## Result matrix

| Scope | Observation | Result |
| --- | --- | --- |
| corrected b4 deploy | exact lock／JAR、runtime health、doctor、loopback、auth enforcement | PASS |
| pre-auth one-shot | Bridge越しの0ms `hello → pairBegin → pairPoll` | PASS |
| Scratch b4 | pairing、authenticated hello、Catalog Picker、pose正常系／境界／失敗時不変 | PASS |
| Scratch lifecycle | player offlineで接続維持、通常tab終了でWireScope source／main終了 | PASS |
| Python b4 | pairing、WireScope attach、pose正常系／境界／失敗時不変、origin／pose復元 | PASS |
| Python lifecycle | client closeでWireScope source／main終了 | PASS |
| b3 rollback | canonical b3 lock、doctor、`player.getPose=method_not_found` | PASS |
| b4 reapply | exact b4 lock／JAR、doctor、`player.getPose`成功 | PASS |
| session token immediate reconnect | restart前の同一token再接続 | PASS |
| same-b4 restart | runtime health／現行doctor | PASS |
| session token restart reuse | 通常再起動後の同一`mcrs_` tokenが`auth_required` | **FAIL** |
| credential health detection | `UNINITIALIZED`を現行doctorが検出せずPASS | **FAIL** |

## One-shot transport and b4 feature result

McRemoteのterminal auth responseは完全responseからEOF観測まで約41msを要したが、
`2026-08-17-01`のexact one-shot Bridgeを使い、固定delayなしで0msの
`hello → auth.pairBegin → auth.pairPoll`を通過した。これにより、EOFを速めるだけでは閉じなかった
pre-auth競合について、Scratch／Bridge側のtransport correctionはhome-alphaで合格した。

Scratchでは、認証済みhello、Catalog Picker、`player.getPose`／`player.setPose`、yaw正規化、pitch境界、
`invalid_params`時のpose不変、player offline時の接続維持を確認した。通常tab終了後、WireScopeはsourceと
main streamの終了を表示し、reload後はsource待機へ戻った。

Pythonでは、pairing、browser-loopback WireScope attach、main stream 1件、pose正常系／境界／invalid params、
origin／pose復元、client close後のsource／main終了を確認した。runnerの最終結果は
`LIVE-HUMAN B4 POSE + WIRESCOPE PASS`だった。

## Rollback and reapply result

canonical b3 lockへrollbackし、doctor PASS、protocol `21.0.0`、b4 method
`player.getPose`が`method_not_found`になることを確認した。その後corrected b4 lockを再適用し、exact JAR、
doctor、`player.getPose`成功を確認した。したがって、artifactのb3 rollbackとb4再適用は合格である。

この合格はcredential継続を含まない。後述のsession token再起動FAILが残るため、rollback／再適用を含む
認証全体のgateは未完了である。

## Session token restart failure

再起動前は同じsession tokenで即時再接続できた。同じcorrected b4 runtimeを通常再起動するとhealthと
現行doctorはPASSしたが、同じtokenでのhelloは`auth_required`になった。

固定candidate `dab6908494290c894d8efbe6828707e544860fa1`の実装照合では、session tokenは
`ConcurrentHashMap`のin-memory storeだけに置かれ、credential snapshotへ永続化されていなかった。
一方、`2026-08-02-08`は`mcrs_` session tokenをhash-only snapshot recordとして保存し、通常の
plugin／server再起動を跨いで`expires_at`まで再利用可能とする。よって今回のFAILは現行SSOTと
McRemote実装の差分である。

起動時credential domainは`UNINITIALIZED`、detailはexplicit bootstrap requiredだった。現行Stack doctorは
この状態でもPASSした。`2026-08-06-02`のnonce付きcredential checkpoint／doctor contractは未実装であり、
今回の結果はMcRemoteのsession record永続化とStackのcredential health検出の双方を後続修正入力にする。

## Security and redaction

- pair code、pairing ID、attach code、token／credential、player UUID／名前を収録していない。
- private host／IP、SSH target、forward portを収録していない。
- world名、pose座標・角度は秘密扱い不要だが、本artifactでは具体値を収録していない。
- raw packet capture、raw server log、raw browser captureは受領・収録していない。
- summarized evidenceだけを公開し、private forwarded topologyの実値を再構成できる情報を置かない。

詳細は[redactions.json](../artifacts/2026-08-17-b4-home-alpha-integration/redactions.json)を参照する。

## Sanitized artifacts

- [live-auto-summary.txt](../artifacts/2026-08-17-b4-home-alpha-integration/live-auto-summary.txt)
  - SHA-256: `85cca3e2f9ea1357632fbe34463cfa78eabba6cf66cf3f946ff7bf3e444a7c53`
- [live-human-summary.txt](../artifacts/2026-08-17-b4-home-alpha-integration/live-human-summary.txt)
  - SHA-256: `2e9a25defdad5cb8c3c986cb9cca9ac0fef2f33075b84da12801ff6b62667ea7`
- [rollback_reapply_probe.py](../artifacts/2026-08-17-b4-home-alpha-integration/rollback_reapply_probe.py)
  - SHA-256: `12f25dd9631c919f6b36d5884bc4f4c9472efe74c171a9dc0246d7d233d097de`
- source-side handoff manifest SHA-256: `33ab47a3b6002466be8fff53187b1a1276eee4dcb2657deae33322a77508b901`

## Claim boundary and next gate

本recordが証明するのは、上記exact setでのb4機能統合、one-shot認証、b3 rollback、b4再適用である。
次は証明しない。

- session tokenの通常再起動耐性
- credential domain healthのdoctorによるfail-closed検出
- credentialを継続したままのb3→b4／同一b4再起動／再適用
- public deployment、public artifact channel、tag／release後identity
- b4 release全体のGREEN

McRemoteで`2026-08-02-08`に適合するhash-only session recordを実装してartifactを再固定した後、
同一b4通常再起動とb3→b4再適用の両方で同じ期限内tokenを再試験する。Stackはcredential bootstrap／health
projectionとdoctor検出を再照合する。両方が合格するまでhome-alpha認証修正とb4 release gateを閉じない。

## Addendum — 2026-08-18

本recordのFAILは当時のexact setに対する有効な観測として保持する。後続McRemote
`3496db9293baa6e1d4f79439cacbd239ba15e2b7`はsession recordをhash-only snapshotへ収容し、
JAR SHA-256 `331633ef15a729658496e89fe49cb8a5eb5ebcb2ec86937b7e5313528d7ec997`として再固定された。

後続正式根拠[`2026-08-18-b4-session-persistence-home-alpha`](2026-08-18-b4-session-persistence-home-alpha_ja.md)で、
同一b4通常再起動後とb4再適用後の期限内token認証がPASSした。Stack doctorは未実装checkpointを
`doctor_credential_health_unsupported`としてfail closedにした。b3がb4 session recordを読めない観測は維持するが、
`2026-08-18-01`により建築コード保護のb4 blockerから分離した。空環境からのコード再実行は
[`2026-08-18-b4-code-preservation-recovery-live-human`](2026-08-18-b4-code-preservation-recovery-live-human_ja.md)を参照する。
