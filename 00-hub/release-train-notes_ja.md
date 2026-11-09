# 横断の版の台帳

配布物の版`X.Y.Z`のX.Yごとに、何を出したかを書く（`2026-11-05-02`）。ホームページの版の表は、この台帳から写す。

## 決まり

- Xは、protocolのmajorに`00`を付けたもの（`2400`から、`2026-11-05-01`）。`2321`は、それより前の付け方（protocol `23.2.1`を
  つなげたもの）のまま、major 23の終わりまで使う
- Yは全component（McRemote、Python、Scratch、minecraft-remote-tooling、Java、TypeScript、C#）で共通。機能を足すreleaseは、
  同じXの中でいちばん大きいYの次を使う。同じ時期に出すものは、中身が関係しなくても1つのX.Yにまとめてよい
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
