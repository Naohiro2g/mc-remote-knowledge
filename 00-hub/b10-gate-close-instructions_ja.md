# b10横断release gate closeの依頼（handoff-materialsの分類）

> b10横断release gate（`00-hub/release-gate-notes_ja.md`の2026-10-07の節）は、McRemoteとScratchのpre-release `v2320.0.0b10`を
> 3 OSで試し、human ownerが合格とした（2026-10-17、`14-evidence/records/2026-10-17-b10-prerelease-3os-live-human_ja.md`）。
> pre-releaseの印は外さない（bootstrapの間はpre-releaseのままを公開とする）。gateを閉じる前に、b10の間に作った
> `handoff-materials`を分類してもらう依頼です。参照するknowledge commitは、この依頼が入ったmainのcommitです。default branchへの
> 統合はcoordinatorが照合済み（McRemote `main`＝tag target `17bcf2645c112133935bc9d993d4fdd4669ceb98`、Scratch `develop`＝tag
> target `0809eb5e49e4b83c17a4e91b435d151b9d1b0655`）なので、この依頼には含めない。shared deployはこの後に別に頼む。

## 共通

- 分類：自repoのb10の`handoff-materials`（2026-10-07〜10-17のdirectory）を、次の3つに分ける
  - ① knowledgeのevidenceへ移す：後から同じ観測を再現しにくいもの（実機試験の素材、公開時の照合、人間の確認など）
  - ② 自repoで持ち続ける：後続（rc1、初回stableの後の実装など）で使うもの。何に使うかと、捨ててよくなる条件を書く
  - ③ 捨てる：knowledgeか公開物に同じ内容があるもの、一時的なもの
- 守ること：knowledgeへ全文が移ったことをcoordinatorが確かめるまで、①の元を消さない。token、ペアコード、private address、
  ホスト名、player UUID、private設定は①に入れない
- 返却：directoryごとに①②③と理由、①はfile一覧（bytes、SHA-256）と収容先の案、②は使い道と捨ててよくなる条件。knowledgeの
  commitは実際に読んだSHAを書く
- 下の一覧はcoordinatorの手元のcloneから取ったもので、古いかもしれない。足りないdirectoryがあれば足して返す

## McRemote

分類するもの：`2026-10-07-b10-open`、`2026-10-08-b10-declaration-object`、`2026-10-08-b10-manifest-v2`、
`2026-10-09-b10-ci-candidate`、`2026-10-09-b10-three-os-live-observations`、`2026-10-09-b10-windows-credential-investigation`、
`2026-10-09-b10-windows-persistence-options`、`2026-10-09-b10-windows-sqlite`、`2026-10-10-b10-paper-sqlite`、
`2026-10-10-b10-paper-sqlite-implementation`、`2026-10-10-windows-startup-investigation`、`2026-10-13-b10-paper263`、
`2026-10-13-client-save-directory`、`2026-10-13-coordinate-hud-design`、`2026-10-14-b10-prerelease`

- `2026-10-13-coordinate-hud-design`は初回stableの後の入力と重なる（hub NOTES 2026-10-17「初期のスポーンと建築原点の
  初期値のずれ」、DirectionHUDを取り込む動機）。②にするなら、そのparkとの関係を書く

## Scratch editor（WireScope、minecraft-remote-tooling）

分類するもの：`2026-10-07-b10-native-scratch-set`、`2026-10-07-b10-release-manifest-v2-review`、
`2026-10-07-b10-scratch-local-implementation`、`2026-10-08-b10-declaration-object`、`2026-10-08-b10-release-manifest-v2`、
`2026-10-09-b10-scratch-local-candidate`、`2026-10-09-b10-three-os-live`、`2026-10-09-b10-wirescope-local-candidate`、
`2026-10-12-b10-followup-inventory`、`2026-10-12-b10-local-dogfooding`、`2026-10-12-b10-local-launcher-ux`、
`2026-10-13-sb3-drop-browser-save`、`2026-10-14-b10-candidate`、`2026-10-14-b10-prerelease`、`2026-10-14-b10-quickstart-source`、
`2026-10-14-post-stable-connection-ux`。minecraft-remote-toolingにb10の`handoff-materials`があれば、それも返す

- `2026-10-14-post-stable-connection-ux`は、knowledge `2a66fb1cbfafbda687b6d801f5af51e5276e9f4b`でhub NOTESの2026-10-12の
  park（サーバーの再起動の後の接続）へ着地した。2026-10-17に、b10の3 OSの試験で見た接続の表示の観察⑥〜⑪を同じparkへ
  足した。票の意図と食い違っていないかを、この返却で一言返す。local `NOTES_ja.md`の捕捉は、knowledgeのparkへの参照にしてよい
- b10の3 OSの試験で見つかった、ランチャー、`はじめに.html`、カタログピッカーの改善はhub NOTES 2026-10-17のparkにある。
  ②にするdirectoryがそれらの入力になるなら、そう書く
