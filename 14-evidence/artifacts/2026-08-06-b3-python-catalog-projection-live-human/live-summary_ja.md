# Python b3 catalog/projection live-human summary

## 判定

**PASS**。Python candidate固有の live smoke を、exact-pinした plugin と人間参加 pairing により完了した。
正式 gate 根拠化には、この素材を knowledge `14-evidence/` へ着地する必要がある。

## identity

- Python commit: `af2d11d66a16e3085f569241406a703a1c28c348`
- Python version: `2100.0.0b3`
- protocol: `21.0.0`
- plugin commit（人間申告・deploy側確認値）: `a3dab998b710f65f42f95058a68ec51d419b097c`
- plugin version: `1.21.11-2100.0.0b3`
- deployed JAR SHA-256: `aeb190705bd9957ce73557dc1be0fe15efe7250ba9bc688945e6f537e00ef78e`
- Paper: `1.21.11-130-ver/1.21.11@c5a2736`
- Minecraft: `1.21.11`
- Bridge: `N/A（Python client / McRemote plugin構成にBridge componentなし）`
- server: `[LOCAL_TEST_SERVER]`
- world / build origin: `overworld` / `(200, 0, 200)`

## live catalog / projection

- 人間がゲーム内 pairing を実施し、認証済み `hello` と `catalog.get` が成功。
- hello `catalogHash`: `6d0f8524b70e37fb8d7b34d0fdb45c2b058dcfea82920d86ca9aaabb9fcadc83`
- 宣言 hash、Python再計算 hash、cacheファイル名が一致。
- catalog counts: block 1166 / entity 157 / particle 115。
- network取得後、2回目の `--no-pair` 同期で `catalog_source=cache` を確認。
- cache rootは isolated `$MCREMOTE_CACHE_DIR` を使用し、正準 `mcremote/catalogs/<catalogHash>.json` 形を確認。
- `mc_constants.py`: 71,779 bytes / 1,462 lines。
- manifest: 327 bytes。manifest記載の artifact SHA-256と実ファイルが一致。
- projection key: `31dda5aa5af4783a4515440cd1afa347d2e32ccf0015849b76240ab9d30abccf`
- generator version: `1` / projection schema version: `1`
- entity実例: `entity.ITEM_FRAME == "minecraft:item_frame"`
- particle実例: `particle.VIBRATION == "minecraft:vibration"`

## state付き block_ref() 往復と復元

ユーザーの明示承認後、次の4地点だけを `元状態保存 → air → 読み戻し → state付きstairs配置 → 正規化読み戻し → 元状態復元 → 完全一致確認` の順で操作した。

- absolute `(205, 76, 202)`: north
- absolute `(207, 76, 202)`: east
- absolute `(209, 76, 202)`: west
- absolute `(211, 76, 202)`: south

4地点すべてで air 読み戻し、`block_ref(name=block.OAK_STAIRS, facing=..., half="bottom")` の配置、
`shape=straight,waterlogged=false` を含む canonical full state の読み戻し、保存値への完全復元が PASS。
最終状態は実施前と同一。

## candidate gate

- b1 tests: 13/13 PASS
- b2 tests: 27/27 PASS
- b3 tests: 40/40 PASS
- build: PASS
- sdist / wheel の SHA-256は `checksums.txt` に固定。
- projection生成物は配布物へ同梱していない。
- dev worktreeに存在するユーザー所有の変更には触れていない。

## 観測事項と境界

- observed at: `2026-08-06T17:25:27+09:00–2026-08-06T17:31:24+09:00`
- knowledge contract commit: `1d10c773452a2b58255faeeebed0eec427c3023a`
- 最初の未認証接続は応答前にcloseしたが、再接続後に所定の auth-required / pairing flow が成立した。再試行後の正式シナリオは PASS。
- `permission_denied` の live と実機 rollback は今回の catalog/projection 固有 gate では未実施。unit根拠と未検証境界の明記で扱う。
- entity／particle は b3 の live catalog・projection・import対象として確認した。現行 b3 Python surface に spawn/particle world RPC はないため、ワールド生成操作は試験対象外。
- GitHub tag/release作成およびPyPI公開は本試験では行っていない。
- private host、接続情報、pairing code、token、player UUID、filesystem絶対local pathは搬送物から除外済み。
