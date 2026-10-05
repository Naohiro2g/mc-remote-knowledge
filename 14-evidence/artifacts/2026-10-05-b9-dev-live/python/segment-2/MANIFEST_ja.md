# b9 Python segment 2 — 移管素材一覧

- 分類: **① knowledgeの正式evidenceへ移す**
- 移す先の提案: `14-evidence/records/2026-10-05-b9-dev-live_ja.md` と `14-evidence/artifacts/2026-10-05-b9-dev-live/python/segment-2/`
- 理由: 凍結wheelでの代表往復、humanの実WireScope表示、cleanupの結果を一組の再現・照合可能な素材として保持するため
- knowledge参照: `561de98b5c15864ac9b86cb6dcaeef1f20ce635b`
- exact set: `b9-integrated-artifact-set-1`
- Python source: `b901c88fe41b67530ff353271683ece9fd453076`
- 結果: segment 2各操作PASS、human表示確認PASS、runner exit 0、close PASS
- runner SHA-256は実行前後で一致。human提示22framesとobserver保存22framesのsequence／direction／method／payloadはすべて一致
- 正式evidenceのauthoring・配置・採用はknowledge側。収容と照合の完了前に素材を削除しない
- private profile、token store、生成cacheは素材に含めない。wheel本体はCI artifactを参照し重複収容しない
- 前回の期限切れhello停止素材は別directoryに保持。今回の新規pairing成功で過去のFAILを置き換えない

| File | bytes | SHA-256 |
| --- | ---: | --- |
| `materials/confirmation_ja.md` | 7,049 | `35dee1710d4b2f5d5672dbdb0cda7f6ac0e8cbe2c609267c913e3d9e347c293b` |
| `materials/human-wirescope-observation_ja.md` | 2,909 | `d26ee1b173146b89c5e7f8c0317ed66ad1b6a68c9e2732cf586fe6817f346a29` |
| `materials/observer_snapshot.json` | 9,513 | `ef4d0bdf2ed8fbb3919b1a8cfadfcc79a7c749517a19efd669befe4d84c042fe` |
| `materials/result.json` | 2,492 | `53f8b414f0a45df9932c3542d7e720faaebd12581e46aec1eee94decdb4767ea` |
| `materials/run_segment2.py` | 9,550 | `50d7c0d46186a2f534ff79ceb6e37578d876ae6e8b646a3789a58a28e9c7fd83` |
