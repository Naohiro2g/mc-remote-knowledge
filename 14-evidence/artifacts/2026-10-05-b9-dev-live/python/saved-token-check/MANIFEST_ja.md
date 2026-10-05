# b9 dev保存tokenのhello停止報告

- 分類: **① knowledgeの正式evidenceへ移す**
- 移す先の提案: `14-evidence/records/2026-10-05-b9-dev-live_ja.md` と `14-evidence/artifacts/2026-10-05-b9-dev-live/python/hello/`
- 理由: 凍結したb9 wheelでのlive-auto接続、期限切れreason、停止境界を保持し、再開後の試験と区別するため
- knowledge参照: `561de98b5c15864ac9b86cb6dcaeef1f20ce635b`
- Python source: `b901c88fe41b67530ff353271683ece9fd453076`
- 正式evidenceの配置・authoringはknowledge側。収容と照合の完了前に素材を削除しない
- private profileとtoken storeは収容対象外。runnerはtokenを表示せず、失敗時もstoreを変更しない
- artifact binaryは重複収容しない。取得元はCI run `37233244696`／artifact `11314197935`

| File | bytes | SHA-256 |
| --- | ---: | --- |
| `materials/check_saved_token.py` | 5,249 | `cb6ca3084c0bf0a1493ae566b4337c3826c712a2a2f6181cc37ea094ece2ade7` |
| `materials/confirmation_ja.md` | 6,912 | `1f7b654804787833efe9f8ac13bda96ca1d5cc4d0361c44f1881803ea8a5c874` |
| `materials/result.json` | 986 | `31af3cae137368eee5e5476728e221bba7ad59ec805d5ae60c87987022ead70e` |
