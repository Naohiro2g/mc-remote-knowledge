# McRemoteのcredentialのDBを、owner-onlyの権限で作る依頼（McRemote）

> mcrctlの権限の票（`00-hub/mcrctl-file-mode-instructions_ja.md`の「返却と照合（2026-11-11）」）で、Stackが稼働volumeの中の
> McRemoteのcredentialのfileを読み、group書込みとother読取りのbitがあるmodeを見た。McRemote担当が調べ、現行のSQLite
> backend（`11-plugin/platform-design_ja.md`の「9.4 create-only file backend 契約」の「SQLite backend」）は、DBと親directoryを
> 作るときにmodeを指定せず、既存のmodeも検査しないことを確かめた。隔離したダミーのDBで、`umask 002`ならDB、WAL、SHMが
> `0664`、新しい親directoryが`0775`になり、更新と再openでも変わらない。DBだけを`0600`にしても、今あるWALとSHMは変わらない。
> human owner 2026-11-11：「McRemote側に問題」。参照するknowledge commitは、この依頼が入ったmainのcommitです。

## 欲しいもの

- McRemoteが専用に持つcredentialのDB（snapshotとauthority）と、そのWAL、SHM、journalを、親プロセスのumaskにかかわらず
  owner-only（POSIXでfile `0600`）で作る。McRemoteが作る専用のdirectoryは`0700`
- 今あるDBと関連fileも、起動と再openのときに同じmodeへ狭める。初期化、reset、作り直しも対象
- 共有の親directoryやvolume rootは、再帰でchmodしない。McRemoteが作った専用のdirectoryだけを扱う
- processのumaskを変えない（ほかのpluginに影響させない）
- 今の全OSの契約（`2026-10-09-02`、`2026-10-10-01`）を壊さない

## すること

1. McRemoteがcredentialのために作る、または開くfileとdirectoryを洗い出す。それぞれ、専用か共有か、作るのは誰かを書く
2. 再現のtestを先に書き、`umask 002`で、DB、WAL、SHM、新しい親directoryが広いmodeになって落ちることを確かめる
   （落ちたlogを返却に残す）。今あるDBとsidecarが広いmodeのまま開かれるcaseも入れる
3. 直す。手段（作るときにmodeを渡す、開いた後で合わせる、など）は担当が選び、返却に理由を書く。WALとSHMはSQLiteが作るので、
   それも含めて確かめる
4. 同じtestが`umask 077`、`022`、`002`のどれでも通ることを確かめる。新しく作るとき、今あるfileを開くとき、更新、reset
5. 次のことは、案を返す（決めて実装してよいが、理由を書く）：
   - ownerやgroupが違う、symlink、狭められないときに、fail closedにするか、診断を出して続けるか
   - Windowsなど、POSIXのmodeが使えない環境の扱い
6. 既定のbranchへのPRにする。localとCIの検査を通す。mergeはhuman ownerが判断する
7. 稼働中の環境のfileは変えない。releaseの版と時期は、human ownerが決める

## 返却

- 1の一覧（pathの型、専用か共有か、直した後のmode）
- 2で落ちたtestと、そのlogの抜粋
- 3の手段と理由。選ばなかった手段
- 4の結果（umaskごと、新しく作るとき、今あるfileを開くとき、更新、reset）
- 5の案と理由
- PRの番号とhead、CIのrun ID
- Stackが確かめるべきこと（共有の親directoryとmount、同じvolumeを見られるほかのprocess）。pathや環境の値は書かない

## coordinatorがすること

- PRの差分、test、CIをGitHubのAPIで照合する
- 5の案をhuman ownerに見せ、決まったことをDECISIONSと`11-plugin/platform-design_ja.md`の「9.7 plugin が保証する範囲と
  deployment が保証する範囲」へ書く
- Stackへ、共有の親directoryとmount、今の環境のfileを確かめる票を作る
