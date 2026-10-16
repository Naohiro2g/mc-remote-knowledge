# b10 Scratch Local candidate — 捕捉素材

- source: agent/b10-scratch-local@c717d0c2ed9b045b8c3bb925b0e1fcd8ee33010b（commit/push済み）
- knowledge contract: 5e248a9cd9243c1ca654abfbed65ee2646087316、b10「次の操作」
- workflow: mc-remote-candidate.yml、run37808012407 success
- artifact: ID11563852835、1361803350 bytes、sha256:75b1df3df6d659514ee6eb3a2913a7d9bf6e062a449316c352e9a59078a89aea
- 主票: materials/CONFIRMATION_ja.md（3 ZIPの全identityとcoordinatorへの未確定事項）
- 機械入力: ZIP_IDENTITIES.json、candidate-manifest.json、CANDIDATE_VERIFICATION.json、CI_ARTIFACT.json、CI_RUN.json、SOURCE_INPUTS.json
- licenses: ORIGINAL_135_CI_RECONCILIATION.json（元135全件）、CI_LICENSE_REVIEW.json（最終CI130件）、LICENSE_SUPPLEMENTS.json（補完26の出典hash）。LICENSE_CLASSIFICATION.jsonは手元132件の旧入力
- 検証: logs/、VERIFY_CANDIDATE.py（repo rootでartifact metadata JSON／外側ZIPをargvとして再検査可能）
- 配布入力: scratch-editorのcandidate/ci-37808012407/。native3 ZIPはGit管理外。正式evidenceとして巨大ZIPを複製するものではなく、CI artifactをID／digestで参照
- 未確定: microee0.0.6原BSD本文・条項数。license gate PASSとは主張しない
- evidence着地希望: knowledge b10 gate進捗とOS実施票のexact input。正式records/artifacts authoringはknowledge担当
- cleanup: b10 gate close時に正式evidence／後続／失効を分類する。受領前は保持する
