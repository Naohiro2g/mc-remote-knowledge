# rc1横断release gate closeの依頼（handoff-materialsの分類、候補の削除）

> rc1横断release gate（`00-hub/release-gate-notes_ja.md` rc1）は、mc-remote.comに置いた候補をhuman ownerが3 OSで試して合格とし
> （2026-10-19、`14-evidence/records/2026-10-19-rc1-candidate-3os-live-human_ja.md`）、凍結した`rc1-integrated-artifact-set-1`を
> 4 repoのprereleaseとPyPI.orgへ出した。どのassetも試験したものと同じbytesであることを、coordinatorが照合済み。gateを閉じる前に、
> rc1の間に作った`handoff-materials`の分類と、候補の置き場所の中身の削除を頼む依頼です。参照するknowledge commitは、この依頼が
> 入ったmainのcommitです。default branchへの統合はcoordinatorが照合済み（tooling `main`＝tag target
> `6447f6e8cbfbeeb9d229990b5c4f6e82a5875666`、Scratch `develop`＝`f20e55eb53f192eab6cdc4f0d5aae4f52b2dc8db`（tag target
> `ec79b3b0e364e722d6926a0932eb4bf088ddd3a1`）、McRemote `main`＝tag target `192a777ae1d484bcc9b58fcc7c58d6aed1a374af`、Python `main`＝
> tag target `c30105349ef26413e925699143396ea05bd3e380`）なので、この依頼には含めない。公開VPS（箱庭）のrc1への切り替えは、
> この後に別に頼む（`2026-10-18-02`）。

## 共通

- 分類：自repoのrc1の`handoff-materials`（2026-10-17〜10-19のdirectory。b10のcloseの分類で返したものは除く）を、次の3つに分ける
  - ① knowledgeのevidenceへ移す：後から同じ観測を再現しにくいもの（実機試験の素材、公開時の照合、人間の確認など）
  - ② 自repoで持ち続ける：後続（初回stable、その後の実装など）で使うもの。何に使うかと、捨ててよくなる条件を書く
  - ③ 捨てる：knowledgeか公開物に同じ内容があるもの、一時的なもの
- 守ること：knowledgeへ全文が移ったことをcoordinatorが確かめるまで、①の元を消さない。token、ペアコード、attach code、
  private address、ホスト名、player UUID、private設定は①に入れない
- 返却：directoryごとに①②③と理由、①はfile一覧（bytes、SHA-256）と収容先の案、②は使い道と捨ててよくなる条件。knowledgeの
  commitは実際に読んだSHAを書く
- 下の一覧はcoordinatorの手元のcloneから取ったもので、古いかもしれない。足りないdirectoryがあれば足して返す

## McRemote

分類するもの：`2026-10-17-post-rc1-mc-version-support`、`2026-10-17-rc1-gate-confirmation`、`2026-10-18-rc1-candidate`、
`2026-10-18-rc1-pre-fixture-progress`、`2026-10-19-rc1-prerelease`

- `2026-10-17-post-rc1-mc-version-support`は、hub NOTES 2026-10-17のpark（McRemoteの対応版を各系列の最終版へ広げる検討）の
  入力と重なる。②にするなら、そのparkとの関係を書く

## Python client

分類するもの：`2026-10-18-rc1-python-candidate`、`2026-10-19-rc1-python-release`

- rc1の確認票の返却など、2026-10-17以前に作ったrc1のdirectoryがあれば足す
- WireScopeの観測の開始と終了の確定搬送票は、knowledge `775e61f`でhub NOTES 2026-10-19のparkへ着地した。local `NOTES_ja.md`の
  捕捉は、knowledgeのparkへの参照にしてよい

## Scratch editor（WireScope、minecraft-remote-tooling）

分類するもの：`2026-10-17-scratch-reference-versions`、`2026-10-18-rc1-scratch-confirmation`、`2026-10-18-rc1-work-scratch`、
`2026-10-19-rc1-release-scratch-tooling`。minecraft-remote-toolingにrc1の`handoff-materials`があれば、それも返す

- rc1の3 OSの試験で見つかった、`はじめに.html`、ランチャー、パレットの頭出しのずれ、WireScope miniの表示の改善は、
  `14-evidence/records/2026-10-19-rc1-candidate-3os-live-human_ja.md`の「見つかったこと」とhub NOTES 2026-10-19のparkにある。
  ②にするdirectoryがそれらの入力になるなら、そう書く

## Stack（mc-remote-stack）

1. 候補の置き場所の中身を消す（human owner 2026-10-19了承、`2026-10-18-07`）：公開VPSの`/candidates/2321.0.0rc1/set-1/`の5 fileと
   `SHA256SUMS`を消す。`/candidates/*`の経路と、Caddyの設定は残す。消したことと、その時刻を返す。coordinatorが外から、5つのURLが
   404になることを確かめる
2. 分類：rc1の`handoff-materials`（`/candidates/*`の経路、PR #73〜#75、1回目のapplyの`rollback-failed`の記録など）があれば、
   上の共通の形で返す
