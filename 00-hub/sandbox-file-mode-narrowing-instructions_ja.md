# 今の箱庭のfileの権限を狭める依頼（Stack）

> mcrctlの権限の票（`00-hub/mcrctl-file-mode-instructions_ja.md`の「返却と照合（2026-11-11）」）で、Stackは今の箱庭を読み、
> 直したmcrctlと違うmodeを見た。(1) `generated/compose.yaml`と`generated/render-manifest.json`が`0644`で、直したmcrctlでは
> `0600`になる。(2) 稼働volumeの中で、McRemoteのcredential snapshotが`0664`、authorityのdirectoryが`0775`。(2)はMcRemoteが
> 作るfileで、作り方はMcRemoteへの票（`00-hub/mcremote-credential-file-mode-instructions_ja.md`）で直す。human owner
> 2026-11-11：「いま、変更しよう。」 参照するknowledge commitは、この依頼が入ったmainのcommitです。

## 欲しいもの

- (1)の2 fileを`0600`にする（直したmcrctlが作るmodeと同じ）
- (2)のMcRemoteが専用に持つcredentialのfile（snapshotとauthorityのDB、WAL、SHM、journal）を`0600`、McRemoteが専用に持つ
  directoryを`0700`にする
- 稼働中のサービスの動きを変えない

## すること

1. 変える前に、対象の一覧を作る。pathの役割、owner、group、mode、そのfileを読み書きするprocessの実行user。ownerがその実行
   userと違うなら、そのfileは変えずに返す
2. (1)：直したmcrctlで作り直すか、modeだけを合わせるかは、Stackが選び、理由を返す。中身は変えない
3. (2)：McRemoteが専用に持つfileとdirectoryだけを変える。共有の親directoryとvolume rootは、再帰で変えない。fileの中身は読まない
4. 変えた後に、McRemoteのcredential storeの障害（`credential_store_unavailable`など）がlogに出ていないことと、Stackのいつもの
   確認の手順で接続が通ることを確かめる
5. McRemoteが直るまでは、SQLiteがWALやSHMを作り直すと、広いmodeに戻りうる。変えた直後と、時間を置いた後に、もう一度modeを読む
6. 手順と実際のpathは、private opsの記録に残す。knowledgeへの返却には、path、host、uidの値を書かない

## 返却

- 1の一覧（pathの役割、ownerとgroupが実行userと合うか、変える前と後のmode）
- 2の手段と理由
- 4の確認の結果
- 5で読み直した結果（広いmodeに戻ったか、戻ったならどのfileか）
- 変えなかったものと、その理由

## coordinatorがすること

- 返却を、この票とhub NOTESの「McRemoteのcredentialのDBを、owner-onlyの権限で作る」の行に記録する
- McRemoteの返却が届いたら、直したMcRemoteを入れた後のmodeを確かめる票をStackへ作る（McRemoteの票の「coordinatorがすること」）

## 返却と照合（2026-11-11）

Stack担当はknowledge `562b5c008c7a4e391f04a79ed4496bbd44670896`を読んだ（この票の本文は今と同じ）。Stackのsourceは変えていない。
手順と実際のpathはprivate opsの記録に残した（commitは担当の返却による。coordinatorはbackstageを読まないので照合していない）。
公開の返却は、pathの役割の表、環境の値を除いたresult、ダミーでの手順のtest 4件のlogで、どれも返却の`SHA256SUMS`と一致した。

- 一覧：10項目。全項目で、ownerとgroupが、読み書きするprocessの実行userとgroupに一致した。変えずに返したものは無い
  - (1)：生成されたComposeとrender manifestを、`0644`から`0600`へ
  - (2)：McRemoteのcredentialの専用のfile 4つ（snapshotとauthorityのDB、旧file backendのsnapshotとauthority manifest）を、
    `0664`から`0600`へ。専用のdirectory 4つ（credentialのroot、authorityのDB、旧authority、snapshot）を、`0775`から`0700`へ。
    旧file backendのfileは、中身を読まずにmodeだけを変えた
- 手段：(1)は作り直さず、modeだけを合わせた（中身、inode、size、mtime、ownerが変わらないことを確かめた）。再renderや
  containerの作り直しが要らないため。(2)は明示した対象だけを、型、owner、symlink、hardlinkの数を確かめてから変えた
- 確認：変えた後のdoctorは、約2時間52分後と約3時間18分後の2回とも正常。credential store、credentialのbackend、SQLiteの障害の
  logは0件。4つのserviceのcontainer、開始の時刻、restartの回数は変わらず、deploy、restart、reloadはしていない。doctorの
  接続の確認は認証なしのhelloで、pairingはしていない
- 読み直し：変えた直後と、2回のdoctorの前後に読み、広いmodeへは戻っていなかった。両DBのWAL、SHM、journalは、どの時点でも
  無かった。McRemoteが作り直す時のmodeは、この操作では保証されない
- 変えなかったもの：共有の親directoryとvolume root（mode、owner、group、inodeが変わらないことを確かめた）、すでに`0600`の
  runtime config、無いsidecar（作らない）、ほかの生成物、ほかのplugin、processのumask、artifact、版、image
- McRemoteの修正版（`2026-11-11-03`）を入れた後に、両DBとsidecarのmodeを確かめる票は、その版が出た時に作る（hub NOTESの
  「McRemoteのcredentialのDBを、owner-onlyの権限で作る」の行）
