Minecraft Java Edition 1.21.11向けのベータ版です。wire protocolは23.2.0です。

- `chat.post`の成功応答を`result: null`へ揃えました。
- JAR内のファイル・ディレクトリの権限を固定し、手元とCIのJARが同じbytesになることを確認しました。
- 共有契約fixtureの取得元を`minecraft-remote-tooling`へ移管し、chat／event互換性のfixtureを追加しました。
- READMEの機能一覧、APIへの導線、更新・戻し方を更新しました。

通常devのPaper 1.21.11でlive-auto 60 PASS行／FAIL 0、id付き`chat.post`の`result: null`を確認しました。

JARと`manifest.json`は、このtagのCIが生成したcandidateを固定Release workflowで添付します。
