# Unityの作業をmc-remote-unity-sandboxへ移す依頼（minecraft-remote-csharpのCodexセッション）

> Unityの世界と箱庭を、一般用途のC# Client Libraryから分け、新しいrepo `Naohiro2g/mc-remote-unity-sandbox`（MIT）で進めると
> 決めた（`2026-11-11-02`、スポークは`19-unity/README_ja.md`）。human ownerがrepoを作り、knowledgeがbootstrap（`AGENTS.md`と
> `.gitignore`の追記）を置いた。この票は、その確定搬送票（`minecraft-remote-csharp` `534e422e4894d43d377b71c77068d2c391e0ca05`）
> の着地確認を兼ねる。参照するknowledge commitは、この依頼が入ったmainのcommitです。

## 移すもの

`minecraft-remote-csharp`の`main`から（搬送票のとおり）：

- `experiments/unity-local-demo/`の一式（README、観察の記録、準備のscript、`Assets/`、画像、`.gitignore`）
- `docs/unity-shared-sandbox-draft_ja.md`、`docs/unity-internal-preparation_ja.md`
- `docs/diagrams/unity-shared-sandbox-connections.svg`、`unity-shared-sandbox-layout.svg`、`unity-shared-sandbox-runtime.svg`

## すること

1. 移す前に、移す範囲の履歴のすべてのblobに、Minecraft（Mojang）の素材、token、private endpoint、operator-localのfileが
   無いことを確かめる（`2026-11-11-02`⑤）。あれば、移さずに返す
2. 履歴ごと移す。手段（たとえば`git filter-repo`で抜き出す）は担当が選び、理由を返す。新repoには初期commitがあるので、
   移した履歴を既定のbranchの履歴とつなげて（たとえば`--allow-unrelated-histories`のmerge）、PRにする
3. 新repoでの置き場所（Unityのprojectをroot直下にするか、subdirectoryにするか）は担当が選び、理由を返す。human ownerが
   置いたUnity用の`.gitignore`は、root直下のprojectを前提にしている（`/[Ll]ibrary/`など）。置き場所に合わせて直す
4. 移した文書の中の参照（図のpath、repoの中のlink、「このrepo」が指すもの）を、新repoに合わせて直す。knowledgeを指す参照は
   変えずに、直すべきものがあれば返す
5. Unity 6.6の修正版で、移した後のデモを準備のscriptから開いて、移す前と同じに動くことを確かめる。使ったパッチ版を書く
   （`2026-11-11-02`③）
6. `minecraft-remote-csharp`から移したfileを外し、READMEなどに移った先を書く。library、`src/`、test、CIは変えない
7. 両repoとも、既定のbranchへのPRにする。mergeはhuman ownerが判断する

## 返却

- 実際に読んだknowledge commit
- 1の確かめ方と結果
- 両repoのPRの番号、head、CIのrun ID（あれば）
- 移したfileの一覧（元のpath → 新しいpath、bytes、SHA-256）と、新repoで履歴が残ったことの確かめ方
- 3で選んだ置き場所と理由、`.gitignore`の変更
- 4で直した参照と、knowledgeで直すべき参照
- 5のUnityの版と結果
- C#のrepoに残るUnityの記述（あれば）

## coordinatorがすること

- PR、merge commit、fileのbytesとSHA-256を、GitHubのAPIで照合する
- `19-unity/README_ja.md`と`18-csharp-client/README_ja.md`の参照を、移った先へ直す
- C#の実装を始める票（`00-hub/polyglot-csharp-start-instructions_ja.md`）は、この移行の後に始めてもらう

## 返却と照合（2026-11-11）

`minecraft-remote-csharp`のCodexセッションはknowledge `a409c9695e1a117d88abc36084b9c582b54d7c50`を読み、搬送票（`534e422`）の
着地確認をOKとした。human ownerが2026-11-11に、`mc-remote-unity-sandbox` PR #1（head `bc5dbdab2911d0bb39972216d6021e8d37ad5724`）を
merge commit `958b676e293427165e872d9abd7b5bfc4173efd6`で、その後に`minecraft-remote-csharp` PR #2（head
`46891c2870f1d730b466e48721257163bdf28a35`）をmerge commit `9b623c9b1cd0d5b344bd958586af3897f6a19b9b`でmergeした（どちらも
親が2つのmerge commitで、`main`の先頭）。coordinatorはGitHubのAPIで、両PR、merge commitの親、移した32 file、C#のCIを確かめた。

- 1の確かめ方：元の`534e422`で、移す範囲のpathの全祖先のblob 40件（text 38、PNG 2）を列挙し、秘密鍵、tokenの形、credentialの
  代入、private IP、home path、operator-localのpath、埋め込みのbinaryを調べた。URLと素材を作るコードを読み、PNG 2件を目で見た。
  Mojangの素材、token、private endpoint、operator-localのfileは無かった
- 移し方：新しい作業用のcloneで`git-filter-repo`により対象のpathだけを抜き出し（元のrepoの公開の履歴は変えない）、新repoの初期の
  履歴とmerge `0e6ab40`でつないだ。抜き出した5 commit（`680ebb3`→`7a16a6e`など、対応は移行先の
  `docs/migration-20261111/commit-map.tsv`）が、移行先の`main`の祖先に残っている
- 移したfile：32件。元のpath、新しいpath、bytes、SHA-256は、移行先の`docs/migration-20261111/files.json`。coordinatorは32件を、
  元の`534e422`と移行先のhead `bc5dbda`の両方で取得し、bytesとSHA-256が表と一致することを確かめた（不一致0）。中身を直したのは、
  設計メモ2本、デモのREADME（→`docs/local-demo_ja.md`）、観察の記録（→`docs/observations_ja.md`）、準備のscript
  （→`scripts/prepare-project.sh`）、Unity用の`.gitignore`（→`unity/.gitignore`）の6件で、ほかは元のbytesのまま
- 置き場所：Unityのprojectは`unity/`、文書と画像は`docs/`、図は`docs/diagrams/`、scriptは`scripts/`。理由は、後で来る.NETの
  hostと世界のモデルを同じrepoで育てながら、生成物とbuildの境界を保つため。human ownerが置いたroot直下向けのUnity用の
  `.gitignore`は`unity/.gitignore`へ移し、rootには共通のlocalの設定と生成物（operator-localのfile、`.env`、OSとeditor、.NETの
  buildの出力）を置いた
- 参照：移した文書の中の、設計メモとデモの間、project の場所、「このrepo」が指す範囲を直した。knowledgeを指すURLは変えていない
- Unity：`6000.6.8f1`（revision `237b6593792b`）、Linux、Built-in Render Pipeline。新しいprojectから準備のscriptで開き、座標と
  配置の検証、Playのsmoke、描画が通った（各processの終了コード0）。Web build、URP、tablet、実機の性能、通信と同期、新しい
  人の試用は主張しない
- C#のrepo：32 fileを外し、READMEに移った先を書いた。`.gitignore`には、手元の旧projectのpathを残した。`src/`、test、
  solution、CIは変えていない。PRのCI run `43026373632`と、merge後の`main`のrun `43059800299`が成功。C#のrepoに残るUnityの
  記述は、READMEの利用先の例、移った先への案内、libraryの配布との関係
