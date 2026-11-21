# 横断の版の台帳

配布物の版`X.Y.Z`のX.Yごとに、何を出したかを書く（`2026-11-05-02`）。ホームページの版の表は、この台帳から写す。

## 決まり

- Xは、protocolのmajorに`00`を付けたもの（`2400`から、`2026-11-05-01`）。`2321`は、それより前の付け方（protocol `23.2.1`を
  つなげたもの）のまま、major 23の終わりまで使う。protocolが`23.3.0`になっても`2321`のまま（`2026-11-15-03`）
- Yは全component（McRemote、Python、Scratch、minecraft-remote-tooling、Java、TypeScript、C#、Unity箱庭）で共通（Unity箱庭は
  `2026-11-15-04`から）。機能を足すreleaseは、同じXの中でいちばん大きいYの次を使う。同じ時期に出すものは、中身が
  関係しなくても1つのX.Yにまとめてよい
- Zはバグの修正だけで、componentごとに上げる。この台帳には書かない
- 出さなかったcomponentは、直前の版のまま、そのX.Yのセットに入る
- protocolの外にあるcomponent同士の約束（ScratchとBridge、Stackのpresetとimage、credentialの運用など）を変えたX.Yでは、
  相手のcomponentに要る版を「要る版」の欄に書く

## 番号の取り方

出す前に、coordinatorがこの表に行を足して番号を取る（状態は「予約」）。一緒に出すcomponentは、番号を取る時点で決める。
出したら状態を「公開」にし、日付を入れる。出すのをやめたら「取り消し」にし、行は消さない（そのYは使わない）。

## 台帳

| X.Y | 状態 | 日付（JST） | protocol | 出したcomponentと版 | そのときのセット（出さなかったcomponent） | 要る版 | 記録 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 2321.0 | 公開 | 2026-11-01 | `23.2.1` | McRemote `2321.0.0`、Python（`minecraft-remote-api`）`2321.0.0`、Scratch `v2321.0.0`、minecraft-remote-tooling `v2321.0.0` | Java、TypeScript、C#は公開releaseなし | なし | 1年ぶりの安定版。`00-hub/release-gate-notes_ja.md`の2026-10-22の節 |
| 2321.1 | 公開 | 2026-11-09 | `23.2.1` | McRemote `2321.1.0`、Python（`minecraft-remote-api`）`2321.1.0`、Scratch `v2321.1.0` | minecraft-remote-tooling `v2321.0.0`。Java、TypeScript、C#は公開releaseなし | なし | 座標・時刻HUD、パレットの頭出しの修正とpickerの検索、starterの接続先を`sb`へ。2026-11-06に予約。`00-hub/release-gate-notes_ja.md`の2026-11-06の節 |
| 2321.2 | 予約 | — | `23.3.0` | McRemote `2321.2.0`、Unity箱庭`2321.2.0`（最初の公開）。McRemoteは11月25日、Unity箱庭は12月1日の予定。最初のLTS（`2026-11-19-02`、`2026-11-21-01`、`2026-11-21-03`） | Python（`minecraft-remote-api`）`2321.1.0`、Scratch `v2321.1.0`、minecraft-remote-tooling `v2321.0.0`。Java、TypeScript、C#は公開releaseなし | なし | 2026-11-15に予約。protocolを`23.3.0`へ（`2026-11-15-03`）。2026-11-17にtoolingとUnity箱庭を加えた（`2026-11-17-01`）。2026-11-19に、ScratchとtoolingのUnity箱庭に向けた変更を`2400.0`へ移した（`2026-11-19-01`）。`00-hub/release-gate-notes_ja.md`の2026-11-15の節 |
| 2400.0 | 予約 | — | `24.0.0` | McRemote、Python（`minecraft-remote-api`）、Scratch、minecraft-remote-tooling、Unity箱庭（各`2400.0.0`の予定） | Java、TypeScript、C#は、sourceを`2400.0.0`に揃えてGitHubのtagまで。公開releaseなし | Scratch `v2400.0.0`は、Bridge（minecraft-remote-tooling `v2400.0.0`）と、runtime configの`schema_version: 2`と組で入れる（`2026-11-16-01`③）。`2321`のclientとは、majorが違うのでつながらない | 2026-11-19に予約。12月1日の予定で、延期するときは12月5日（`2026-11-19-01`）。中身は`2321.2`のために作ったものに、Pythonを加えたもの。`00-hub/release-gate-notes_ja.md`の2026-11-19の節 |
