# 初回stable（2321.0.0）横断release gate closeの依頼（handoff-materialsの分類、公開の後の残り）

> 初回stableの横断release gate（`00-hub/release-gate-notes_ja.md`の2026-10-22の節）は、2026-10-31に凍結したexact setを
> 2026-11-01に4 repoの`v2321.0.0`（Latest）とPyPI.orgへ出し、箱庭を26.3のセットへ切り替え、ホームページを同期した。どの
> assetも凍結値と同じbytesであること、OCIのdigest、PyPI.orgのfile、ホームページの全fileを、coordinatorが照合済み（同じ節の
> 「公開（2026-11-01）」）。gateを閉じる前に、初回stableの間に作った`handoff-materials`の分類と、公開の後の残りを頼む依頼です。
> 参照するknowledge commitは、この依頼が入ったmainのcommitです。

## 共通

- 分類：自repoの初回stableの`handoff-materials`（2026-10-20〜11-01のdirectory。rc1のcloseの分類で返したものは除く）を、次の
  3つに分ける
  - ① knowledgeのevidenceへ移す：後から同じ観測を再現しにくいもの（実機での確認、Temurinでの確認、公開の時の照合、人間の確認など）
  - ② 自repoで持ち続ける：後続（`2321.1.0`、`2330.0.0`、統合版のHTTPSなど）で使うもの。何に使うかと、捨ててよくなる条件を書く
  - ③ 捨てる：knowledgeか公開物に同じ内容があるもの、一時的なもの
- 守ること：knowledgeへ全文が移ったことをcoordinatorが確かめるまで、①の元を消さない。token、attach code、private address、
  ホスト名、player UUID、private設定は①に入れない
- 返却：directoryごとに①②③と理由、①はfile一覧（bytes、SHA-256）と収容先の案、②は使い道と捨ててよくなる条件。knowledgeの
  commitは実際に読んだSHAを書く
- 下の一覧はcoordinatorの手元のcloneから取ったもので、古いかもしれない。足りないdirectoryがあれば足して返す

## McRemote

分類するもの：`2026-10-22-rc2-publication-stable-candidate`、`2026-10-22-stable-rc2-confirmation`、`2026-10-23-game-hud-first-slice`、
`2026-10-24-hud-colors-input`、`2026-10-26-hud-quick-actions`、`2026-10-29-java-temurin-policy`、`2026-10-29-stable-temurin-validation`、
`2026-10-31-stable-release-preparation`

- `2026-10-29-stable-temurin-validation`は、knowledgeに正式な記録を置くよう頼まれている。①にするなら、置く記録の名前の案を書く
- HUDの3つ（10-23〜10-26）は初回stableの範囲の外。②にするなら、どの後続で使うかを書く

## Python client

分類するもの：`2026-10-22-stable-python-candidate`、`2026-10-22-stable-python-confirmation`、`2026-10-23-wirescope-python-development`、
`2026-10-31-stable-python-release`

## Scratch editor（WireScope、minecraft-remote-tooling）

1. developへの取り込み（`00-hub/stable-gate-work-instructions_ja.md`の「Scratch」の1）：候補のbranchの配布対応の変更（配布の
   script 2か所と回帰test、`USER_GUIDE_ja.md`のリンク）を`develop`へ入れる。本家の取り込みは取り消さない。`develop`の新しい
   先頭のSHAと、入れたcommitを返す
2. 分類するもの：`2026-10-21-upstream-sync`、`2026-10-22-rc1-release-body-review`、`2026-10-22-stable-confirmation-scratch-tooling`、
   `2026-10-22-stable-work-scratch-tooling`、`2026-10-24-bridge-multiple-targets-confirmation`、`2026-10-27-scratch-wirescope-lifecycle`、
   `2026-10-31-stable-publication`。minecraft-remote-toolingに初回stableの`handoff-materials`があれば、それも返す

## Stack（mc-remote-stack）

1. ServerBackup：切り替えた後に、ServerBackupが新しいworldのbackupを作ったことを確かめて返す（時刻、file名、bytes。中身の
   展開は要らない）
2. ブロック一覧の照合の条件：「`sourceCommit`がtagの指すcommitの祖先で、間にブロックの定義の変更がなく、取り込むfileがtagの
   `site/`と同じbytes」に直した結果を返す（gate notesの「Scratchのブロック一覧の取り込み」、human owner 2026-11-01）
3. 旧セット：切り替えの前に退避した旧セット（rc1のproject、`minecraft-data.tar`などのvolumeの保存）を、いつまで持つかの案を返す。
   消すのはhuman ownerの了承の後
4. 分類するもの：`2026-10-27-bedrock-https-review`、`2026-10-28-geyser-b1273`、`2026-10-29-jvm-flags-review`、`2026-10-29-rc2-263-preflight`、
   `2026-10-29-stable-deployment-conditions`、`2026-10-29-stack-four-items-java-return`、`2026-10-29-vps-load-motd-icon`、
   `2026-10-31-paper263-build231`、`2026-10-31-stack-return-four-items-java`、`2026-10-31-web-pair-target-selections`。11/1の切り替えの
   素材があれば足す
   - `2026-10-31-stack-return-four-items-java`（26.3 #231の最終の確認）は、knowledgeに正式な記録を置くよう頼まれている。①にするなら、
     置く記録の名前の案を書く
   - `2026-10-27-bedrock-https-review`は、11/2からの統合版のHTTPS（案a）の入力。②にするなら、そう書く

## coordinatorが閉じる前にすること

- 各担当の①を受け取り、`14-evidence/`へ正式な記録を置く（Temurinでの確認、26.3 #231の最終の確認、公開の照合）
- gate notesの節を`CLOSED`にし、閉じた日と、後続へ送ったものの行き先を書く
- 後続へ送るもの（統合版のHTTPS、`2321.1.0`、`2330.0.0`など）は、hub NOTESに再開の条件つきの行があることを確かめる
