# b9 Python公開 preflight

- knowledge contract commit: `d6d59d91032230a959b7288807179e1bd8100041`
- path: `00-hub/release-gate-notes_ja.md` b9節「release authorization」
- 凍結set: `b9-integrated-artifact-set-1`
- 対象source: `b901c88fe41b67530ff353271683ece9fd453076`
- remote main: `7981031765cfcc43acc23f03e86e97ba74bae494`。対象sourceへfast-forward可能
- tag `v2320.0.0b9`とReleaseは未作成（provider API 404）
- candidate CI run `37233244696`／artifact `11314197935`のmanifestと本体を照合
- wheel: 196,221 bytes／`e166bc9c14c425b3859f9af6c7af52900b58d1769fc077a3524a5368d05638c6`
- sdist: 190,627 bytes／`bd027b8b94ff775bfb7a3c02ada9716ad8785e5499180bb0cfb26f1da4afe479`
- GitHub repository variable `PYPI_PUBLISH_ENABLED=true`をprovider APIで確認済み
- environment `pypi`: required reviewer `Naohiro2g`、prevent_self_review false、admin bypass false、deploymentはtag `v*`のみ
- ユーザー編集中のexamplesを避け、対象sourceの独立worktree `/tmp/mcr-b9-release-worktree`を準備
- 公開指示のsdist略記 `bd027b8b…e179` と上記本体／manifestが不一致。同knowledge文書のcandidate詳細欄は上記full SHAと一致
- runtime指示「typoや過期限identityの場合は実在する『最新』を自動代用せずcoordinatorへ返す」に従い、digestの確認を依頼中
- 本段階ではmain変更、tag、Release、indexへのuploadを行っていない

その後remote main `ede3d0fc8d548e76eefadc93b6dd415f9dce7b1b`のruntimeとrelease authorizationも実読。runtimeは同一で、Pythonのsdist略記は未訂正。Scratch OCIのpackaging差の許可はPythonのartifact照合条件を変更しない。
