# b4 session token persistence home-alpha evidence

## Record

- test ID: `2026-08-18-b4-session-persistence-home-alpha`
- test class: `unit/deterministic` + `live-auto` + `live-human`
- result: **PASS — same-b4再起動とb4再適用後の期限内session token認証**
- observed date: `2026-08-18`
- source repository: `Naohiro2g/mc-remote-stack`
- source branch: `agent/b4-home-alpha`
- source commit: `cd3ff18e31534f394e5fc7ad63af1f164ce54f15`
- environment: isolated home-alpha / private forwarded topology
- decision: `2026-08-02-08` / `2026-08-18-01`
- knowledge contract: `af81126df519d6b02341e9127fb0bd0402c9fac7`

本recordは、`2026-08-17-b4-home-alpha-integration`で見つかったsession token再起動FAILを、
修正済みMcRemote artifactとStack profileで追試した結果を固定する。旧FAILを削除せず、後続exact setで
どの主張がPASSへ変わったかを分けて記録する。

## Exact compatibility set

| Component | Identity |
| --- | --- |
| Stack source | `cd3ff18e31534f394e5fc7ad63af1f164ce54f15` |
| Stack profile／preset | `home-server@3`／`mcremote-paper@6` |
| b4 lock | `sha256:7bb6a81e6428aa986a42418025c101ef4621c4cd26cf793bb3296e582ee10baf` |
| McRemote source | `3496db9293baa6e1d4f79439cacbd239ba15e2b7` |
| McRemote artifact | `mc-remote-1.21.11-2100.0.0b4.jar` / 140,712 bytes |
| McRemote JAR SHA-256 | `331633ef15a729658496e89fe49cb8a5eb5ebcb2ec86937b7e5313528d7ec997` |
| protocol | `21.0.0` |

## Result matrix

| Scope | Observation | Result |
| --- | --- | --- |
| Stack deterministic | 325 tests、Ruff、diff check | PASS |
| artifact apply | exact lock／JAR、三volume topology | PASS |
| explicit bootstrap | plugin所有console command後にcredential health `HEALTHY` | PASS |
| doctor boundary | checkpoint未実装を`doctor_credential_health_unsupported`で停止 | EXPECTED FAIL-CLOSED |
| immediate reconnect | 発行直後の同一session token認証 | PASS |
| same-b4 restart | 通常再起動後の同一期限内token認証 | PASS |
| b3 runtime start | exact b3 lock／JAR起動 | PASS |
| b3 credential compatibility | b4 session recordを`unknown_persisted_credential_type_session`として拒否 | OBSERVED FAIL-CLOSED |
| b4 reapply | exact b4 artifactとcredential health `HEALTHY`へ復帰 | PASS |
| post-reapply token | rollback前と同じ期限内token認証 | PASS |

## Session persistence result

人間がsession pairingを一度実施し、発行直後、同一b4 runtimeの通常再起動後、b3切替後にb4を再適用した後の
三地点で同じ期限内tokenによるauthenticated helloを確認した。再起動直後にplayerがofflineだったときは
`player.getPose=player_offline`だったが、auth-only probeで認証成功とplayer状態を分離して判定した。

McRemote `3496db9293baa6e1d4f79439cacbd239ba15e2b7`は`mcrs_` recordをhash-only snapshotへ収容する。
したがって、`2026-08-02-08`のsame-b4通常再起動契約について、旧candidateの実装差分は閉じた。

## b3 rollback observation

b3 runtimeは起動したが、b4が書いた`session` recordを理解せずcredential healthを`UNHEALTHY`にした。
backendをreset、bootstrap、編集せずb4へ再適用すると、snapshotは再び`HEALTHY`となり、同じtokenを認証できた。

この結果は「b3がb4 credentialを利用可能な形で読む」ことを証明しない。`2026-08-18-01`は、利用者が書いた
建築コードをb4の既定保護対象とし、b3 credential downgrade互換をb4 blockerから分離する。観測自体は
将来のcredential migration／downgrade設計の入力として保持する。

## Doctor boundary

checkpoint projectionは未実装である。Stack doctorはmount topology検査後に
`doctor_credential_health_unsupported`でfail closedし、これをPASSへ読み替えなかった。
checkpoint／doctor完成は`2026-08-06-02`とauthentication roadmapのpost-b4 credential-lifecycle sliceへ残す。

## Sanitized artifacts

- [live-auto-summary.txt](../artifacts/2026-08-18-b4-session-persistence-home-alpha/live-auto-summary.txt)
  - SHA-256: `acab915cb9120fb04161529bb4d072569daf9f7805191352cf1aec6a4a6b7ff1`
- [live-human-summary.txt](../artifacts/2026-08-18-b4-session-persistence-home-alpha/live-human-summary.txt)
  - SHA-256: `5ed6ab907f90043fff5be0aa1664326bc641d7e07dc7e4efcbb29733cfc7e7f9`
- [session_persistence_probe.py](../artifacts/2026-08-18-b4-session-persistence-home-alpha/session_persistence_probe.py)
  - SHA-256: `1f027f64f6470b77533eae83c1a9372944cc95017e4e113bd2f6de85ee401801`
- source-side handoff manifest SHA-256: `f16dd3a784f073af0a329a0471054227729da70502f5add237be070a3125b51a`

Redaction境界は[redactions.json](../artifacts/2026-08-18-b4-session-persistence-home-alpha/redactions.json)を参照する。

## Claim boundary

本recordが証明するのは、上記exact setでのsession record永続化、same-b4再起動、b4再適用後のtoken再利用、
未対応doctorのfail-closeである。次は証明しない。

- b3をcredential継続付きdowngrade runtimeとして利用できること
- checkpoint／doctor contractの完成
- long-lived credentialの一般公開
- public deployment、tag／release後identity
- world backup／restoreまたは接続状態の復元
