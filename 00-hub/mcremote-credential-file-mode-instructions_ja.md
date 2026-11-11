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

## 返却と照合（2026-11-11）

McRemote担当はknowledge `562b5c008c7a4e391f04a79ed4496bbd44670896`を読んだ（この票の本文は今と同じ）。McRemote PR #16（head
`cade9aa734e92e12c7b5f3fe2d5f87069a269928`、base `a38beaf121ce06594391237cb09745ec0da7649d`）を、human ownerが2026-11-11に
merge commit `bc18243c6275387953f24b59b70a2dbd499b9b20`でmergeした。coordinatorはGitHubのAPIで、PR、変わった7 file、CIの
run `43012721267`（同じhead、7 jobすべて成功。McRemoteのworkflowはtagと手動で動くので`workflow_dispatch`）、artifact 7件の
bytesとdigestを確かめた。そのうち2件は取得してSHA-256を照合し、JUnitを読んだ（Ubuntu、Java 21：
`SqliteCredentialFileModesTest` 10 test、skip 0。Windows、Java 25：10 testのうち、POSIX専用の7がskip）。

- 一覧：snapshotとauthorityの専用DB、そのsidecar、保存のために新しく作るdirectoryを、McRemoteが扱う。前からあるdirectory、
  共有の親directory、volume rootは変えない。旧file backendのfileは開かず、modeも変えない
- 直す前の失敗：7 testのうち5が、modeの違いで落ちた（`umask 002`で、新しいdirectoryが`rwxrwxr-x`、広げておいた今あるDBが
  `rw-rw-r--`のまま）。後から、狭められない時、読み戻し、symlinkの3 testを足して10 test
- 手段：作る時にfile `0600`、directory `0700`を指定し、読み戻す。SQLiteへ渡す前、開いた後、`BEGIN IMMEDIATE`の後に、DBと、
  あるsidecarを`0600`へ合わせる。SQLiteはsidecarのmodeをDBから引き継ぐので、DBを先に狭める。選ばなかった手段（umaskを
  `077`にする、DBだけ、または開いた後だけ合わせる、親を再帰でchmodする）と理由は返却のとおり
- 結果：Ubuntu 24.04とmacOS 26のJava 21と25で、`umask 077`、`022`、`002`のどれでも、新しく作る時、広い今あるDBとsidecarを
  起動で開く時、再open、更新、reset、作り直しがPASS。WindowsはPOSIXのmodeを確かめたことにしない
- 5の案：DECISIONS `2026-11-11-03`の③〜⑥として、案のまま決めた。releaseは⑧（McRemoteの次のreleaseに入れる）
- Stackが確かめること：共有の親directoryとvolume rootの管理者とアクセス権、mountの配置、同じvolumeを見られるほかの
  processとcontainer。修正を入れた版を箱庭へ入れた後の、両DBとsidecarのmode
- 稼働中の環境のfile、release、tagは変えていない
