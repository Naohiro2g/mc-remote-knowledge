# B9 dev 通常環境の JAR 差し替え・再起動

- 搬送元: McRemote / Codex、`feat/b9-contract-packaging@5cb33ebad4bf2c5e36c3433b0f70fe6070915b00`
- 作成日: 2026-10-05
- 依頼: human owner の「devの通常環境で、McRemoteのJARをb9（4feb90db…a58e）に差し替えて再起動して」
- SSOT: knowledge `561de98b5c15864ac9b86cb6dcaeef1f20ce635b` の runtime、INDEX、release-operations §3／§8、release-gate-notes の B9 凍結、`00-hub/b9-gate-live-test-sheet_ja.md` 共通／segment 0。
- 確認結果: `materials/restart-result_ja.md` / `materials/deployment-result.json`
- 後続の人間観測: `materials/scratch-hello-observation.json`。08:02:10、human owner が b9 Scratch から再pairingなしの hello 成功を報告。segment 0 の token 継続／開始時版照合の追記として coordinator へ返す。正式 live-human record の authoring は knowledge 側。
- セッションクローズ票: `materials/session-close_ja.md`
- 分類②: B9 knowledge coordinator と後続 segment 担当へ、`b9-integrated-artifact-set-1` の環境準備の結果として移管。参照 identity は McRemote source `5cb33eb...`、JAR SHA-256 `4feb90dbdba8550cd16800cc3d384e42fed16a5c5e20faa489a0381ad2cda58e`、Paper `1.21.11-132-ver/1.21.11@c5eb079`、検証時刻は JSON を参照。
- 位置づけ: gitignore 対象の搬送素材。正式 knowledge evidence authoring は coordinator 側。退避 JAR は server の運用 backup として保持し、公開 source／tag／release は変更していない。
