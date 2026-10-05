## b9公開再開の作業状態

- knowledge contract commit: `ede3d0fc8d548e76eefadc93b6dd415f9dce7b1b`（取得時remote mainも一致）
- knowledge contract path: `00-hub/release-gate-notes_ja.md`のb9節「Scratch OCIのversionラベル」
- 判断: 公開設定でOCIをbuildし直し、versionラベルと生成metadataの差はpackaging差として受け入れる。公開前にamd64／arm64の全layer digest一致と、config差の範囲を確認。layer不一致なら停止して返す
- tooling: tag `v2320.0.0b9`を凍結`dc1ab834183e29f2eb03059b07e99d2b463776ee`へ作成。Release `403384824`はprerelease=true、draft=false、make_latest=falseで公開済み。添付のWireScope ZIP・detached manifest・Bridge OCI archiveはbytes／SHA-256が凍結値と一致。Bridge OCIの置き場所とindex digestはRelease notesへ記録
- tooling Release: https://github.com/Naohiro2g/minecraft-remote-tooling/releases/tag/v2320.0.0b9
- Scratch公開前build: `agent/b9-release-preflight@9ed22a4a14cb10974940ed93060b7b14b0113996`、run `37266780367`。変更は比較用candidate workflow 1 fileだけ。実際のcheckoutとSOURCE_REVISIONは凍結`7fbbf034488760d8fc7e034bf23f3e08e6e1807d`にpinし、RELEASE_VERSIONは`v2320.0.0b9`、provenance mode=max／SBOM=trueで公開workflowの設定に合わせた。OCI exportのみ、registry push=false。developは凍結sourceのまま
- Scratch: tag／Release／registryの公開はまだ行っていない。新OCIの比較結果待ち
- 比較script: `materials/compare-scratch-oci.py`。archive SHAとOCI blob SHAを検証し、linux/amd64・arm64それぞれのordered layer digestとconfig差を検査する。attestation／SBOMは生成metadataとしてruntime layerとは別に扱う
- 旧停止票は当時の事前照合として保持。再開後の操作を旧票の「公開操作なし」に遡及して混ぜない

- 最終追記: 比較でamd64／arm64のCOPY layerが不一致。1746 entryの内容等は同じで1743 entryのmtimeのみ差。Scratch公開は停止。最新票は`PUBLICATION_ja.md`、詳細は`copy-layer-inspection.json`。CI比較は027424e／run37267805360。
