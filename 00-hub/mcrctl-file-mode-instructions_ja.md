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

## 返却と照合（2026-11-11）

Stack担当はknowledge `f29ce18129bd6b64eb2dbcaef7b4d89e44c99f7a`を読んだ（この票の本文は今と同じ）。mc-remote-stack PR #89
（head `34750fdeefe933388e03ba64862019d8d6a04bed`、base `eb19fd2c9b72e8a177d5aa8c9a3945b51153fd7f`）を、human ownerが2026-11-11に
merge commit `8c6afcb1ad4017c16f1eb14af37bb1db86d6a2ee`でmergeした（`main`の先頭）。coordinatorはGitHubのAPIで、PR、merge commitの
親、変わった6 fileを確かめた。Stackのtestは、このrepoのCIでは走らない。検査はlocal（`uv run pytest` 655 passed、`ruff check`、
presetのcatalogの`--check`、`git diff --check`）で、担当の返却による。

- 一覧：mcrctlの作成と書き換えの76箇所を洗い出し、pathの役割ごとにmodeを決めた（PRの`docs/generated-file-permissions_ja.md`）。
  Caddyfile、Scratchのruntime JSON、Minecraftの生成seed、WireScopeのassetsはfile `0644`、必要なdirectory `0755`。render root
  は`0700`。Compose、render manifest、compact lock、分類していない新しいfileは`0600`。秘密を含みうる追加のCompose snapshotと
  新しいoperatorの入力は、元のmodeのまま。secret store、backup、稼働volumeの中のfileは、この処理で変えない
- 直す前の失敗：`umask 077`で5 failed、1 passed（public renderの2 profile、compactのruntime JSON、更新と自動で戻す処理）。
  ほかに、private copyと新しいoperator入力が`022`と`002`で広がること、modeだけを直すとseedのmtimeが変わることも、先に落ちる
  ことを見た
- 手段：pathの役割を`render_modes.py`で明示し、書く前にdescriptorへmodeを設定する。private copyは元のmodeの一時fileへ書いて
  置き換える。変わらないかの判定にmodeも入れ、modeだけ違うときはmtimeを保つ。umaskは変えない。選ばなかった手段（umaskを`022`
  にする、全体を再帰でchmodする、Caddyfileだけ直す、copyの後でmodeを合わせる、imageやUIDを変える）と理由は返却のとおり
- 結果：`077`、`022`、`002`のどれでも、更新は`complete`、targetの検査を失敗させると自動で`rolled-back`。private snapshotと
  新しいprivate入力は`0600`のまま、secret storeはfile `0600`／directory `0700`
- 今の箱庭（読んだだけ）：`generated/compose.yaml`と`generated/render-manifest.json`が`0644`で、直したmcrctlでは`0600`になる。
  ほかの生成物は一致。稼働volumeの中で、McRemoteのcredential snapshotが`0664`、authorityのdirectoryが`0775`だった（mcrctlの
  生成物ではなく、比べる対象の外。中身は読んでいない）
- 1回目のapplyで失敗したtransactionと準備用のCLIのcheckout：この修正の再現と検証には、もう使わない。testは合成のfixtureで
  再現する。消すのは片付けの票で、それまで消さない
- 公開の箱庭へはapplyしていない。直したmcrctlは次の更新から使う
