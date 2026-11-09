# `2321.1`横断release gate closeの依頼（handoff-materialsの分類）

> `2321.1`横断release gate（`00-hub/release-gate-notes_ja.md`の2026-11-06の節）は、2026-11-09に`2321.1-set-2`を3 repoの
> `v2321.1.0`（Latest）とPyPI.orgへ出し、公開の箱庭を更新し、ホームページを同期した。どのassetも凍結値と同じbytesであること、
> OCIのdigest、PyPI.orgのfile、ホームページの全fileとブロック一覧を、coordinatorが照合済み（同じ節の「公開（2026-11-09）」から
> 「ブロック一覧の照合と片付けの案（2026-11-09、Stack）」まで）。gateを閉じる前に、`2321.1`の間に作った`handoff-materials`の
> 分類を頼む依頼です。参照するknowledge commitは、この依頼が入ったmainのcommitです。各担当は、自分の節と「共通」を読んでください。

## 共通

- 分類：自repoの`2321.1`の`handoff-materials`（2026-11-02〜11-09のdirectory。初回stableのcloseの分類で返したものは除く）を、
  次の3つに分ける
  - ① knowledgeのevidenceへ移す：後から同じ観測を再現しにくいもの（実機での確認、公開の時の照合、人間の確認など）
  - ② 自repoで持ち続ける：後続で使うもの。何に使うかと、捨ててよくなる条件を書く
  - ③ 捨てる：knowledgeか公開物に同じ内容があるもの、一時的なもの
- 守ること：knowledgeへ全文が移ったことをcoordinatorが確かめるまで、①の元を消さない。token、attach code、private address、
  ホスト名、player名とUUID、private設定は①に入れない。この依頼では分類を返すだけで、消さない
- 返却：directoryごとに①②③と理由、①はfile一覧（bytes、SHA-256）と収容先の案、②は使い道と捨ててよくなる条件。knowledgeの
  commitは実際に読んだSHAを書く
- 下の一覧はcoordinatorの手元のcloneから取ったもので、古いかもしれない。足りないdirectoryがあれば足して返す

## McRemote

分類するもの：`2026-11-04-hud-current-spec`、`2026-11-06-23211-gate`、`2026-11-06-hud-bold-compass`、`2026-11-06-hud-compass-regular`、
`2026-11-06-hud-direction-mark`、`2026-11-06-hud-hsb-colors`、`2026-11-06-hud-lifecycle-review`、`2026-11-06-hud-release-palette`、
`2026-11-07-23211-hud-status-lowercase`、`2026-11-07-23211-paper244`、`2026-11-07-23211-swap-default-on`、`2026-11-09-23211-release`

- HUDの次の版（複数の接続の対応とQuick Actions、NOTES 2026-11-07のHUDの原点の行）や、統合版での調整（NOTES 2026-11-09の
  統合版の行）で使うものは②にし、どれに使うかを書く

## Python client

分類するもの：`2026-11-06-python-2321-1-candidate`、`2026-11-09-python-23211-release`

## Scratch editor（WireScope、minecraft-remote-tooling）

1. 分類するもの：`2026-11-04-scratch-standalone-release-review`、`2026-11-04-upstream-sync`、`2026-11-05-tooling-fixture-mit-license`、
   `2026-11-06-scratch-2321-1-candidate`、`2026-11-06-scratch-fixture-mit-consumer`、`2026-11-07-scratch-23211-block-list`、
   `2026-11-07-scratch-23211-rebuild`、`2026-11-09-scratch-23211-release`。minecraft-remote-toolingに`2321.1`の`handoff-materials`が
   あれば、それも返す
   - 共有fixtureの2つ（11-05、11-06）は、gateの後のfixtureの付け直しの票で使うなら②にする
2. パレットの頭出しのずれ（NOTES 2026-11-01の行）：`2321.1.0`で直した原因と、回帰のtestがあるかを返す（人間の試験の7では
   ずれが出なかった）。この行を閉じるのに使う

## Stack（mc-remote-stack）

分類するもの：`2026-11-07-stack-23211-candidates`、`2026-11-07-stack-23211-investigation`、`2026-11-07-stack-23211-work`、
`2026-11-09-homepage-23211-sync`、`2026-11-09-stack-23211-sandbox-preparation`、`2026-11-09-stack-23211-sandbox-update`、
`2026-11-09-stack-23211-close-proposal`

- 箱庭の更新は、knowledgeに記録がある（`14-evidence/records/2026-11-09-stack-23211-sandbox-update_ja.md`）。素材のうち、記録に
  無くて残すべきものがあれば①にする
- `2026-11-09-stack-23211-close-proposal`は、片付けの実行（human ownerが案を認めた。NOTES 2026-11-09の片付けの行）の入力。
  1回目のapplyの失敗の再現の情報は、mcrctlの権限の票（NOTES 2026-11-09の行）の入力。それぞれ②にするなら、そう書く
- 片付けの実行とmcrctlの権限は、この依頼では扱わない（gateを閉じた後に別の票）

## coordinatorが閉じる前にすること

- 各担当の①を受け取り、`14-evidence/`へ収容する
- gate notesの節を`CLOSED`にし、閉じた日と、後続へ送ったものの行き先を書く。告知は出さない（human owner 2026-11-09）
- 台帳（`00-hub/release-train-notes_ja.md`）の`2321.1`の行を「公開」にする
- hub NOTESの`[priority]`と、再開の条件がこのgateに結びついた行を確かめる（`00-hub/release-operations-responsibility-design_ja.md`
  §10のstep 12）
