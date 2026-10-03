# b8 Python公開・公開後照合の搬送素材

- 2026-10-03 gate close分類票: `materials/b8-close-classification_ja.md`。knowledge `2a8c3eae4e489e67f044111b0d1e6cdd22ead86a` のb8 CLOSEDに追従し、今回の5 directoryを①正式evidence／②具体的な後続／③廃棄候補へfile範囲付きで分類した。詳細inventoryは `materials/b8-close-file-inventory.json`、後続票は `materials/b9-python-followup_ja.md`。移設・削除なし。knowledgeの既存recordは要約であり、coordinatorの全文移管確認は未受領。以前の `handoff-inventory_ja.md` は全11 directoryの旧一覧として保持し、今回のb8分類には新票を使う。

- 最新返却票: materials/release-return_ja.md（Release gate確認票形式）。公開指示1〜5をPython担当自身で実行済み。
- knowledge contract commit: fd7cad78564dd96ee91831d284abf1560fdf65b0。runtime、INDEX、gate release authorization、公開運用責務、Python TestPyPI指示を読んだ。
- exact set: b8-integrated-artifact-set-1。mainをfast-forwardし、mainとv2320.0.0b8のtargetを52d35f5304e62f465c1f47ab47c00fe9bcf62470へ固定した。
- new main CI37113256520／artifact11271101046のwheel195068 bytes、sdist188775 bytesが凍結SHAと一致してから公開。公開Release assetを実downloadして再照合。
- Release402437492、title minecraft-remote-api 2320.0.0b8、prerelease=true／draft=false／make_latest=false。Latest APIは従来のv1214.10.11。
- 固定workflow37113530599のpromote／publish-testpypi success。TestPyPI公式JSONの2 filesが同じbytes／SHA、yanked=false。
- 公開manifest681 bytes／SHA-256 7aa2868f1d9fc75b414cb37ac8d0886d390691d7b169f060def99248e29d9fc0。source_commit52d35f5／同梱WireScope sourcedf34849を照合。
- Windows検証用の公開wheel URLを匿名取得し、195068 bytes／凍結SHA dcedff01…0180を確認。Windowsの実機導入はhuman ownerの後続試験。
- 元worktreeのuser変更2ファイルは開始時と同じ内容で保持、commitしていない。clean一時worktreeを使用して統合し、公開後に削除済み。
- 分類: sanitized公開結果・素材をknowledge担当へ移管して正式evidence化／gate closeの照合に使う。正式authoringはPython担当から行っていない。全handoff directoryはmaterials/handoff-inventory_ja.mdに引継ぎ先・参照identity・次の一手を明示。
- materials/state.jsonはuser設定ファイルのpreservation fingerprintを含み、公開搬送から除外する。private config／credential／local cacheはcommitしない。
