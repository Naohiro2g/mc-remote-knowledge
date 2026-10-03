# 公開後のhandoff素材の引継ぎ一覧

- 作成日: 2026-10-03。Python b8公開の節目で、このrepoのhandoff全directoryを棚卸しした。
- 参照する公開identity: main／tag v2320.0.0b8 = 52d35f5304e62f465c1f47ab47c00fe9bcf62470。knowledge fd7cad78564dd96ee91831d284abf1560fdf65b0。
- 以下は分類と引継ぎ先を明示する記録。knowledgeへの正式authoringや他repoへの配置を本sessionが行ったという主張ではない。
- sanitized素材はcoordinatorへ返却し、正式evidence着地後の照合・cleanupはPython後続sessionへ移管する。過去gateの素材は、そのMANIFESTを参照identityとして特定する。非参照確認なしに削除しない。
- private config／credential state／raw token／local cacheは公開evidenceへ移管しない。private opsを別repoへ移す操作はこの公開指示の範囲にないので実行していない。

| directory | 分類 | 引継ぎ先 | 参照identity | 次の一手 |
| --- | --- | --- | --- | --- |
| `2026-07-07-b2-auth-client-recovery-python-plugin` | 後続担当へ移管 | このrepoのPython後続担当session | `MANIFEST_ja.md` SHA-256 `657459e78956a0558edbbb94345ab0176bf81ba7926662aab8699cf52cc268c0` | MANIFEST記載のsource／artifactとknowledge正式evidenceを照合し、既参照の素材とprivate素材を区分して昇格／移管／非参照失効を処理する |
| `2026-07-09-b2-python-live-rerun` | 後続担当へ移管 | このrepoのPython後続担当session | `MANIFEST_ja.md` SHA-256 `5589377c76556f5a5f09e822bf50781f94be2f13f8c8618926b5726b2e235ea3` | MANIFEST記載のsource／artifactとknowledge正式evidenceを照合し、既参照の素材とprivate素材を区分して昇格／移管／非参照失効を処理する |
| `2026-07-09-b2-release-gate-python-client` | 後続担当へ移管 | このrepoのPython後続担当session | `MANIFEST_ja.md` SHA-256 `ae0e6822174071510605826eb1f0c63d0b184fd903e8ee4243bee0618846ba8a` | MANIFEST記載のsource／artifactとknowledge正式evidenceを照合し、既参照の素材とprivate素材を区分して昇格／移管／非参照失効を処理する |
| `2026-08-22-b5-python-live-segment` | 後続担当へ移管 | このrepoのPython後続担当session | `MANIFEST_ja.md` SHA-256 `2aa2354ab171f40efe118190f5de549d6dfcfb626a8bf61bbd57391437008cb9` | MANIFEST記載のsource／artifactとknowledge正式evidenceを照合し、既参照の素材とprivate素材を区分して昇格／移管／非参照失効を処理する |
| `2026-08-22-codex-browser-capability-investigation` | 後続担当へ移管 | このrepoのPython後続担当session | `MANIFEST_ja.md` SHA-256 `f0acbb02d239b1c73e97db96c96affff378b3d68fa62b83896977fb34c9dde43` | MANIFEST記載のsource／artifactとknowledge正式evidenceを照合し、既参照の素材とprivate素材を区分して昇格／移管／非参照失効を処理する |
| `2026-09-23-beta-train-fold-correction` | 後続担当へ移管 | このrepoのPython後続担当session | `MANIFEST_ja.md` SHA-256 `e6a9597b3486a950d02d5e3e0d3ff29a060e47201d8cd39d0f48b4f9a9b76075` | MANIFEST記載のsource／artifactとknowledge正式evidenceを照合し、既参照の素材とprivate素材を区分して昇格／移管／非参照失効を処理する |
| `2026-09-30-b8-python-component` | 後続担当へ移管 | knowledge担当（sanitized素材の正式evidence化・着地照合） | `MANIFEST_ja.md` SHA-256 `c76e791dedc3a3280e9fa8dad31928a28017a9c01073dd43017860bfd447b796` | 公開tag v2320.0.0b8と凍結source52d35f5を参照して受領素材を正式化し、着地SHAをPythonへ戻す |
| `2026-10-01-b8-python-successor` | 後続担当へ移管 | knowledge担当（sanitized素材の正式evidence化・着地照合） | `MANIFEST_ja.md` SHA-256 `ad4fba7500f5be29e92d33bc768312890749b0b65eed2f287e262bced9cd0d95` | 公開tag v2320.0.0b8と凍結source52d35f5を参照して受領素材を正式化し、着地SHAをPythonへ戻す |
| `2026-10-02-localhost-smoke` | 後続担当へ移管 | このrepoのPython後続担当session | `MANIFEST_ja.md` SHA-256 `569a99b07507b1b621760009423bccd31bc0e9c75575a93bc90065605aa9fd3d` | MANIFEST記載のsource／artifactとknowledge正式evidenceを照合し、既参照の素材とprivate素材を区分して昇格／移管／非参照失効を処理する |
| `2026-10-03-b8-dev-token-upgrade` | 後続担当へ移管 | knowledge担当（sanitized素材の正式evidence化・着地照合） | `MANIFEST_ja.md` SHA-256 `7dbfc12d91ca98bd44e05c238a2da107cae3fda125e9214e89a3f46603044ac4` | 公開tag v2320.0.0b8と凍結source52d35f5を参照して受領素材を正式化し、着地SHAをPythonへ戻す |
| `2026-10-03-b8-python-release` | 後続担当へ移管 | knowledge担当（sanitized素材の正式evidence化・着地照合） | `MANIFEST_ja.md` SHA-256 `2ed0fa5ba162256ecc0fb5012d68003e6bc00c23ddbc49f7cbc885b29ca6ca4c` | 公開tag v2320.0.0b8と凍結source52d35f5を参照して受領素材を正式化し、着地SHAをPythonへ戻す |
