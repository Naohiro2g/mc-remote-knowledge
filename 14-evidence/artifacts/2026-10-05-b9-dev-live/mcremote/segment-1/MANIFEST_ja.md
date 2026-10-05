# B9 McRemote segment 1 live-auto と chat null の搬送素材

- 搬送元: McRemote / Codex、`feat/b9-contract-packaging@5cb33ebad4bf2c5e36c3433b0f70fe6070915b00`
- 作成日: 2026-10-05
- 入力: human owner の live-auto／chat.post null 確認・確認票作成依頼、knowledge `561de98b5c15864ac9b86cb6dcaeef1f20ce635b` の `00-hub/b9-gate-live-test-sheet_ja.md` 共通／segment 1。
- exact set: `b9-integrated-artifact-set-1`
- McRemote JAR: 261,016 bytes、SHA-256 `4feb90dbdba8550cd16800cc3d384e42fed16a5c5e20faa489a0381ad2cda58e`
- runner: `scripts/live_auto.py`、SHA-256 `7a093d27ac349023e7be90c48597ead1a1207772a4fee084933ee2f8c794352f`。source を編集せず実行する。
- 記録: `materials/run_with_transcript.py`、`environment.json`、`rpc-transcript.jsonl`、`live-auto.log`、`cleanup-summary.json`、`confirmation_ja.md`、`session-close_ja.md`。
- wrapper: knowledge の正式保存済み B8 wrapper を再利用し、B9 identity、独立 chat null 確認、試験で生成した entity の削除と9箇所の BlockValue 保存・復元確認を追加。token は取得後も process memory のみ。auth.enforcement を変更しない。
- test class: live-auto。pairing の human owner のゲーム内承認は前提条件として記録し、product の live-human 代表試験を代行しない。
- 分類②: B9 knowledge coordinator へ、上記 exact set／source／JAR／knowledge SHA を参照 identity として移管。正式 record・artifact の authoring／配置／commit は knowledge 側。
- 位置づけ: gitignore 対象の搬送素材、正式 evidence ではない。最終の結果・未検証の境界は確認票を参照。
- 結果: 2026-10-05 08:44:49–08:45:41 JST、live-auto60 PASS行／FAIL0、chat null1 PASS、exit0。entity258体削除、9箇所BlockValue復元・再読一致。試験後もJAR SHA一致、Paper／config／run.sh不変。
- 確認票: [materials/confirmation_ja.md](materials/confirmation_ja.md)。segment 0の既報再起動・Scratch既存token継続観測とsegment 1の結果を併記。
- 追加素材: `materials/run-summary.json`、`post-run-identity.json`、`resume-state.json`。初回の承認前失効は `materials/attempt-1-expired/` に保持。SSH tunnel終了済み。
