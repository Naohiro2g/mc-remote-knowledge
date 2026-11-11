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
