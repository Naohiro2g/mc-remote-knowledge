# b9公開完了・確認票返却

- 最新knowledge: `7eec4255e1b820cf996dc71c42b34d672dea44f8`、b9「Scratch OCIのCOPY layer」。公開後actual OCIも承認された範囲内でPASS。
- 最新返却票: `materials/PUBLISHED_ja.md`。旧 `PUBLICATION_ja.md`／`RESUME_ja.md`／`CONFIRMATION_ja.md` は停止と再開の履歴。
- Scratch tag／develop: `7fbbf034488760d8fc7e034bf23f3e08e6e1807d`。prerelease403409264、Latest非対象。固定workflow37270517123 success。
- 公開Scratch OCI: `sha256:f44e7a6c1a3b041aba787eba5e052a3ae78ce4ce733732bc7213207a3b17f607`。比較run37271363905 success。amd64／arm64各9layer byte同一、COPY1746entryの内容等同一、1743mtime差。許可されたconfig生成metadataのみ。
- Bridge registry index／WireScope ZIP・manifest／contractsは凍結値。公開manifest.json1168 bytes／`cbc6af558a0633cd252d2f6e2192523e4d92f2602c629e9092677e2f2cb920da`。
- 比較helper: 隔離branch `agent/b9-release-preflight@dfebdfebd6aad8fd1e3246ca1566653f6b198b95`。製品へ統合しない。公開sourceは既にdefault developへ統合済み。
- 分類: ①本票と比較／公開素材をknowledge正式evidenceへ収容する候補、②大archiveと比較branchは収容確認までclose担当へ引継ぎ、③削除なし。詳細とidentityは本票とINVENTORY／SHA256SUMS。runtime／privateはこのdirectoryに無い。手元サービスと未追跡user fileは不変。
- 未検証: 新OCIのcontainer起動／deploy・再live。Bridge container確認はknowledge指示のVPSベータhuman確認へ。本担当の公開作業に残り無し。横断closeはknowledge担当へ。

# 許可更新前の履歴（ede3d0f）

- 作成日: 2026-10-05
- 最新knowledge: `ede3d0fc8d548e76eefadc93b6dd415f9dce7b1b`、b9 release authorization「Scratch OCIのversionラベル」
- 最新返却票: `materials/PUBLICATION_ja.md`
- tooling: 凍結dc1ab83へannotated tag `v2320.0.0b9`、Release403384824をprerelease ON／draft OFF／make_latest=falseで公開。WireScope ZIP／manifest／Bridge OCI archiveのidentityを照合。Bridge registry copyは未実施
- Scratch: 凍結7fbbのsourceとdevelopを維持。隔離branchのworkflowで公開設定のOCIをexportし、新旧比較。両architectureの先頭9 layerは同じ、最後のCOPY layerのdigestだけ違う。layer内の1746 entryの内容・型・リンクは同一、1743 entryのmtimeだけ異なる。GUI tarもbyte同一。指示の全layer一致条件を満たさないため、tag／Release／registryは未操作
- run: build37266780367／比較37267805360。workflow branchはagent/b9-release-preflight（build9ed22a4、比較027424e）。製品checkoutとSOURCE_REVISIONは7fbbへpin
- 素材: 最新票、source・provider metadata、操作request／response、OCI比較とCOPY layerの詳細、検証script、artifact ZIP2件
- 歴史: `materials/CONFIRMATION_ja.md`はd6d59d9時点の初回停止票、`RESUME_ja.md`は再開途中のsnapshot。現在の公開状態はPUBLICATIONを正とする
- 再現入力: 旧candidateは`../2026-10-05-b9-tooling-migration/artifacts/scratch-candidate-7fbbf03448.zip`。新candidateは`artifacts/scratch-release-preflight-7fbbf03448.zip`。旧archiveは複製せず元directoryを維持
- cleanup分類: テキストの公開・比較証拠は①knowledgeの正式evidenceへ移す候補。新OCIを含む大きいZIP、source参照branch、比較helperは②b9公開再開へ引継ぎ。coordinatorの収容確認と再開指示までは削除しない。公開操作なしという旧票の記録を現在の状態へ誤用しない
- 未完了: COPY layerのmtime差をpackaging差として受け入れるかの判断とScratch公開。VPSでのBridge container起動は別作業。dev／localhostサービスとuserの未追跡ファイルには変更なし
