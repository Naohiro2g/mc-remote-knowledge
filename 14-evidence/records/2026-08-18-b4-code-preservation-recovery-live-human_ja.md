# b4 code-preservation recovery evidence

## Record

- test ID: `2026-08-18-b4-code-preservation-recovery-live-human`
- test class: `unit/deterministic` + `live-auto` + `live-human`
- result: **PASS — 保存済みScratch／Python建築コードを空環境へ持ち込み再実行**
- observed date: `2026-08-18`
- source repository: `Naohiro2g/mc-remote-stack`
- source branch／commit: `agent/b4-home-alpha@780d99291d669fd1ec98c513245bf6fdbac36271`
- environment: isolated home-alpha / private forwarded topology
- decision: `2026-08-18-01`
- knowledge contract: `af81126df519d6b02341e9127fb0bd0402c9fac7`

本recordは、利用者が書いた建築コードをb4の既定保護対象とする復旧基準を検証する。旧world、旧credential、
旧tokenを使わずexact b4環境を空から構築し、新規pairing後に保存済み`.sb3`とPython sourceを再実行した。

## Exact compatibility set

| Component | Identity |
| --- | --- |
| Stack final source | `780d99291d669fd1ec98c513245bf6fdbac36271` |
| Stack runtime implementation | `cd3ff18e31534f394e5fc7ad63af1f164ce54f15` |
| profile／preset | `home-server@3`／`mcremote-paper@6` |
| replay lock | `sha256:e037b47824a1062804d7db67fdb9fc3cf0c16700ff9d24400be4d42ebc00bffa` |
| McRemote source | `3496db9293baa6e1d4f79439cacbd239ba15e2b7` |
| McRemote JAR SHA-256 | `331633ef15a729658496e89fe49cb8a5eb5ebcb2ec86937b7e5313528d7ec997` |
| Python source | `4d510442db58a94f8b249ddcd9d959381f97276c` |
| Python wheel SHA-256 | `eeed6261972987946b5e22dd8ff8d3533a758c7db57472d1d82766fbf964e7d0` |
| Scratch GUI source | `1d2f18785d260564ad4bc30a26a45ef33fc813d6` |
| Scratch GUI CI artifact | ID `9287627432` / digest `sha256:924254363ab431c1f11ea8661f950b9325da56c248f52613cf87d70cb6562a71` |
| Bridge source | `8b69ecefc9771a47e2eac8bea242cf96c09d36f3` |
| Bridge CI artifact | ID `9283550231` / digest `sha256:fa62fff67311e365b2c02c9a79c47c288192bb0495bec7f962638d6f5ce7236c` |
| WireScope ZIP／manifest | `1a56617c78c283332f1afe3bdd3797ab37f0cdc3455c86c73c926c751721657f`／`f3ec11496b595bbca4ba27a6e938a1149336eb5a2da55e742d60e1681cf4d154` |
| protocol | `21.0.0` |

## Empty-environment boundary

- 新規deployment identity、world identity、minecraft-data volumeを作成した。
- credential snapshot／revocation authorityも新規volumeとし、旧bytesをコピーしなかった。
- plugin所有console commandで新credential domainをbootstrapした。
- tokenなしhelloが`auth_required`であることを確認した。
- 旧pairing／session tokenを再利用せず、ScratchとPythonでそれぞれ新規pairingした。

## Scratch result

- fixture: `Scratch_test_code.sb3`
- bytes: 43,488
- SHA-256: `f6656d77b43945342700724c0c387b4d6c6cdad376130c3b5e91243ae6ca75bf`
- 実行前に固定3点が期待blockでないことをserver consoleで確認した。
- 保存作品を読み込み、green flagで建築コードを実行した。
- 実行後の固定署名:
  - `(-1, 90, 0)` = `minecraft:gold_block`: PASS
  - `(0, 90, 0)` = `minecraft:sea_lantern`: PASS
  - `(1, 90, 0)` = `minecraft:iron_block`: PASS
- 人間目視に加え、server consoleの相補条件で独立照合した。

## Python result

- fixture: `python_building_code.py`
- SHA-256: `2fbd80a0c4bc6512bd5136fa57ed315e28dad99ac60246ff97f8ab9915c172a9`
- exact wheelをfresh Python 3.11 venvへinstallし、version `2100.0.0b4`／protocol `21.0.0`を確認した。
- 実行前に固定3点が期待blockでないことをserver consoleで確認した。
- 新しい一時credential directoryでpairingし、保存sourceを実行した。
- client `getBlock`: `PASS python building-code reuse protocol=21.0.0 blocks=3`
- server console独立照合:
  - `(4, 90, 0)` = `minecraft:lapis_block`: PASS
  - `(5, 90, 0)` = `minecraft:redstone_block`: PASS
  - `(6, 90, 0)` = `minecraft:diamond_block`: PASS

## Stack regression

- test-first README回帰: 修正前FAIL、修正後PASS。
- `uv sync --extra dev`: PASS。
- `uv run pytest`: 326 passed。
- `uv run ruff check .`: PASS。
- `git diff --check`: PASS。
- final runtime: healthy。
- final credential domain: `HEALTHY`。

## Sanitized artifacts

- [Scratch_test_code.sb3](../artifacts/2026-08-18-b4-code-preservation-recovery-live-human/Scratch_test_code.sb3)
  - SHA-256: `f6656d77b43945342700724c0c387b4d6c6cdad376130c3b5e91243ae6ca75bf`
- [python_building_code.py](../artifacts/2026-08-18-b4-code-preservation-recovery-live-human/python_building_code.py)
  - SHA-256: `2fbd80a0c4bc6512bd5136fa57ed315e28dad99ac60246ff97f8ab9915c172a9`
- [live-auto-summary.txt](../artifacts/2026-08-18-b4-code-preservation-recovery-live-human/live-auto-summary.txt)
  - SHA-256: `73e0a48671e3fd1ffb8539908458233eabe120a00fde4b3156639d7220a9c474`
- [live-human-summary.txt](../artifacts/2026-08-18-b4-code-preservation-recovery-live-human/live-human-summary.txt)
  - SHA-256: `772712e5eb0ea293f95359217af35d5498f15b25ab31f29cc991a89e05db567f`
- source-side handoff manifest SHA-256: `561ca7aa144ea89ec1332d4094a18aa4bee4f7b71d4655ba60e57ee0808562e5`

Redaction境界は[redactions.json](../artifacts/2026-08-18-b4-code-preservation-recovery-live-human/redactions.json)を参照する。

## Claim boundary

本recordが証明するのは、上記exact setで保存済みScratch／Python建築コードを空環境へ再投入し、
新規pairing後に同じ固定建築結果を得られることである。次は証明しない。

- checkpoint／doctor完成、long-lived credential一般公開
- world backup／restoreまたは接続／WireScope状態の継続
- b3 credential downgrade互換
- 任意の旧記法を無変更で実行できる恒久shim
- public deployment、tag／release後identity
