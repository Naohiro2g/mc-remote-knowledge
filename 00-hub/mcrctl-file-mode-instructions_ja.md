# mcrctlが作るfileの権限を、手元のumaskに左右されないようにする依頼（Stack）

> `2321.1`の箱庭の更新（2026-11-09）で、Stack担当の手元のスクリプトが、秘密を守るための`umask 077`をmcrctlへ引き継いだ。
> 作り直したCaddyfileなどがcontainerの中の実行userから読めず（`open /etc/caddy/Caddyfile: permission denied`）、apply
> （`deployment update`）が落ちた。自動で戻す処理も同じumaskで落ちた（`rollback-failed`）。記録は
> `14-evidence/records/2026-11-09-stack-23211-sandbox-update_ja.md`の「経過（JST）」。human ownerの判断（2026-11-09）：「mcrctlを
> 手元の設定に左右されないようにする」（hub NOTES 2026-11-09の行）。参照するknowledge commitは、この依頼が入ったmainのcommitです。

## 欲しいもの

- mcrctlが書いて、containerが読むfileを、親プロセスのumaskにかかわらず、そのcontainerの実行userが読める権限で作る
- 更新（`deployment update`）と、自動で戻す処理の両方
- 秘密を含むfileは、今より広く読めるようにしない

## すること

1. mcrctlがfileやdirectoryを作る、または書き直すところを洗い出す。それぞれ、読むcontainerと実行user、秘密を含むかを書く
2. 再現のtestを先に書き、`umask 077`で落ちることを確かめる（落ちたlogを返却に残す）。1回目のapplyの素材（Stackの②、
   `handoff-materials/2026-11-09-stack-23211-sandbox-update/`）を使ってよい
3. mcrctlを直す。手段（modeを明示して作る、書いた後にmodeを合わせる、など）はStackが選び、返却に理由を書く
4. 同じtestが`umask 077`、`022`、`002`のどれでも通ることを確かめる。更新と自動で戻す処理の両方を見る
5. 既定のbranchへのPRにする。localの検査（pytest、ruff）を通す。mergeはhuman ownerが判断する
6. 公開の箱庭へapplyしない。直したmcrctlは次の更新から使う

## 返却

- 1の一覧（pathの型、作る処理、読むcontainerと実行user、秘密を含むか、直した後のmode）
- 2で落ちたtestと、そのlogの抜粋
- 3の手段と理由。手段の候補で選ばなかったもの
- 4の結果（umaskごと、更新と自動で戻す処理ごと）
- PRの番号とhead、localの検査の結果
- 今の箱庭のfileのmodeが、直した後のmcrctlが作るものと違うところ（読むだけ。直さない）
- 片付けの案で「mcrctlの権限の票で再現に使い終えてから消すもの」とした、1回目のapplyで失敗したtransactionと準備用のCLIの
  checkout（`00-hub/release-gate-notes_ja.md`の「ブロック一覧の照合と片付けの案（2026-11-09、Stack）」の2）を、もう使わないか

## coordinatorがすること

- PRの差分とtestをGitHubのAPIで照合する
- mergeの後に、hub NOTESの行を閉じる
