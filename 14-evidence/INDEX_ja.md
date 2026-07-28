# Evidence index

新 public 正本世代の sanitized evidence index。

| Test ID | Class | Contract / scope | Record | Artifact | Commit |
| --- | --- | --- | --- | --- | --- |
| `2026-07-25-home-beta-clean-bootstrap-live-auto` | `live-auto` | `home-server@2` / `mcremote-paper@1`: clean bootstrap、`profile-render`、tokenなし`protocol-hello` | [record](records/2026-07-25-home-beta-clean-bootstrap-live-auto_ja.md) | [artifacts](artifacts/2026-07-25-home-beta-clean-bootstrap-live-auto/) | `9b58b62c9af80d415cfbc90925a839f07e78e4f3` |
| `2026-07-25-ubuntu-desktop-wol-mutual-live-human` | `live-human` | 異なるUbuntu desktop hardware 2台: directed broadcast、Python / `wakeonlan`、deep sleep / poweroff、人間の完全消灯checkpoint | [record](records/2026-07-25-ubuntu-desktop-wol-mutual-live-human_ja.md) | [artifacts](artifacts/2026-07-25-ubuntu-desktop-wol-mutual-live-human/) | `ea67ab007ad7535f8129cc8b9efda93913eeed6b` |
| `2026-07-28-scratch-showcase-failclose` | `unit/deterministic` + `live-auto` + `live-human` | Scratch showcase 二重 guard: build 時 `disableMcRemoteConnection()` ラッチ＋runtime `connection_enabled`、拒否理由 `connection_disabled` 統一。Addendum（2026-07-29）で `NODE_ENV=production` 成果物と Pages 公開面の再確認を追加 | [record](records/2026-07-28-scratch-showcase-failclose_ja.md) | なし（sanitized counts を record に直接収録） | `19790d9e58d0dc1aafe907486bdd7cfbde28d316`（初版）/ `c7087d7badd906f6bd5eb93776ec8fab0934d5ee`（Addendum） |
