knowledge commit: `7eec4255e1b820cf996dc71c42b34d672dea44f8`
path: `00-hub/release-gate-notes_ja.md`、b9の節

  - Scratch OCIのCOPY layer（2026-10-05）: Scratch担当が公開前のbuild（run `37266780367`、index `sha256:da7c9622…ff27`）を凍結した
    OCIと比べ（run `37267805360`）、止めた。amd64とarm64とも先頭9 layerは同じで、最後のGUIのCOPY layerだけdigestが違う。
    その1,746 entryのpath、中身のSHA、size、type、link先、mode、uid／gidはすべて同じで、違いは1,743 entryのmtimeだけ。GUI tarは
    凍結値とbytesもSHA-256も同じ。human ownerの判断で、**このmtimeの差もpackagingとして受け入れる**。判定の条件を次へ改める:
    各layerの中身（path、内容、size、type、link先、mode、所有者）が凍結したOCIと一致し、違いはmtimeとconfigの生成metadata
    （versionラベル、作成時刻、それに伴う履歴とdiff_id）だけであること。固定workflowで公開し、公開したOCIにも同じ照合をして
    返す。合わなければ公開を取り消せる状態で止めて返す。実機試験のPASSは再利用する
- human owner（2026-10-05）: `minecraft-remote-tooling`の名前変更とpark解除はScratchに頼む。Pythonをmatureへ移す（`2026-10-05-03`。
