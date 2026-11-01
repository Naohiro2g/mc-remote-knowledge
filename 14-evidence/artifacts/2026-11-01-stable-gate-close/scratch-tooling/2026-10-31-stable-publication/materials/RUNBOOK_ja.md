# 初回stable公開：実施時の手順

## 許可の範囲と再開条件

- 指示：knowledge `9dee6881a414a2b1fd4a37fa4fe26ddbedd9d8a5`、`00-hub/stable-gate-release-instructions_ja.md`。
- **tag／Releaseの作成は2026-11-01 00:00 JST（2026-10-31 15:00 UTC）以降**。この準備では作成していない。
- toolingを公開したら、公開情報と照合結果をcoordinatorへ返す。**coordinatorのtooling照合完了を受けるまでScratchは公開しない。**
- 両repoの既定branchを動かさない。tooling main=6447f6e、Scratch develop=bee41dcを公開直前にも再確認する。
- 新たな凍結値・順序の変更が来た場合は、その明示された契約を照合する。異なる値を自動代用しない。

## 今回準備した入力

- `downloads/scratch-candidate.zip`：artifact12410683112を取得。外側1370347310 bytes／SHA-256一致。
- `candidate/`：そのまま展開した候補13 file。配布対象9 fileすべて凍結値一致。
- `tooling-assets/`：Bridge OCI archiveとWireScope pair、計3 file。同じ候補からのhardlinkでrc1凍結値と一致。
- `scratch-assets/`：3 ZIP、GUI tar、contracts tar、WireScope pair、manifestの計8 file。
- `scratch-assets/manifest.json`：2093 bytes／95b7cf9d997c9da144a5050b30560da311668dcfd35940c32eb012938d8de364。草稿と差分なし。
- `scratch-oci/`：凍結scratch.oci.tarをregctlでローカルOCI layoutへimport。index digestは凍結値と同一。buildではない。
- `downloads/regctl`：公式v0.11.7、SHA-256 3737fbbdd791e04e7a831640b681f3397a376498e80e2ad9b1b2d27296f239bcを照合。
- `tooling-release-notes_ja.md`、`scratch-release-notes_ja.md`：公開用本文。内部手順やSHA-256表なし。protocol／rc1同一API・通信／migration／feedbackを記載。

## 公開直前のtime guard

変更する各phaseの開始時に実行する。

```sh
python3 - <<'PY'
from datetime import datetime,timezone
start=datetime(2026,10,31,15,0,tzinfo=timezone.utc)
assert datetime.now(timezone.utc)>=start, '公開可能時刻前。tag／Releaseを作らない'
PY
```

## tooling

1. remote mainが`6447f6e8cbfbeeb9d229990b5c4f6e82a5875666`、stable tag／Releaseが未作成であることを再確認。
2. 読取確認済みのBridge indexをそのままstable tagへcopyする（認証は既存Docker credentialを使う。tokenをlogへ出さない）。
   `regctl image copy --force-recursive ghcr.io/naohiro2g/mc-remote-bridge@sha256:305d6e38b36e195a0e158522f32f3a8c45d39da2aeec7b7e46f785c920406acf ghcr.io/naohiro2g/mc-remote-bridge:v2321.0.0`
3. registryのstable tagをHEAD／GETして同じindex digestを確認。rc1 tagとprovenanceは保持。
4. `tooling-tag.json`を使いGitHub Git Tags APIでannotated tag objectを作り、返されたtag object SHAを使って`refs/tags/v2321.0.0`を作る。targetをcommitまでdereferenceして一致確認。
5. `gh release create v2321.0.0 --repo Naohiro2g/minecraft-remote-tooling --verify-tag --draft --title 'minecraft-remote-tooling 2321.0.0' --notes-file <本文>`。
6. tooling-assetsの3 fileをそのままupload。providerのbytes／digestを照合し、必要な再取得で実値も確認。
7. `gh release edit v2321.0.0 --repo Naohiro2g/minecraft-remote-tooling --draft=false --prerelease=false --latest`。
8. 公開readbackでtag／draft=false／prerelease=false／Latest／全asset／registry indexを確認し、coordinatorへ返す。

## coordinatorのtooling照合後：Scratch

1. 照合完了の連絡またはknowledgeの明示記録を確認してから開始。時刻だけを根拠にこのphaseへ進まない。
2. source branchが`ffb496ed50d751d307f685f2ae555c94c893fae5`、developが`bee41dc9629ee3225c19ef1d6be1299b6b4bf7d1`のままであることを再確認。
3. **release:published再buildを避けるため、workflow312664341（mc-remote-images.yml）を一時disable**する。準備時はactiveだった。実行時の状態を記録し、自分がdisableした場合のみ後で復帰。
   `gh api --method PUT repos/Naohiro2g/scratch-editor/actions/workflows/312664341/disable`
4. 凍結OCIを、準備したlocal OCI layoutからstable tagへcopyする。2 archとattestationを含むindex全体を維持する。
   `regctl image copy --force-recursive ocidir://<absolute scratch-oci path>:v2321.0.0 ghcr.io/naohiro2g/mc-remote-scratch:v2321.0.0`
5. registryのindexが`sha256:d85e37291ef75e4d64ab7f0c52b9a496889205071d3afc51b796dbcc1161903c`と一致することを確認。違えば公開せず止めて返す。
6. `scratch-tag.json`のannotated tag objectを作り、返されたobject SHAから`refs/tags/v2321.0.0`を作る。commitまでdereferenceしてsource一致確認。
7. draft Releaseを作り、scratch-assetsの8 fileをそのままuploadする。manifestは草稿からのcopyで内容差分なし。
8. bytes／SHA-256を確認後、`--draft=false --prerelease=false --latest`で公開。新しいbuild workflowをdispatchしない。
9. tag／Release／全asset／manifest／OCI／develop不変をreadbackし、公開によるimage workflowのrunがないことを確認する。
10. 自分がdisableしたworkflowをenableへ戻す。enableだけでは過去のpublished eventを実行しない。runがないことを確認。
11. 公開情報をcoordinatorへ返す。shared・homepage・Stack設定は変更しない。

## 返却に含める情報

knowledge commit、両repo既定branchのhead、tag target、Release URL、Latest／prerelease／draft、
候補run39744827621／artifact12410683112、手動公開の実施時刻、全assetのbytes・SHA-256、
manifestの差分なし、OCI index、再build未実施、workflow停止／復帰の状態。
手動公開なので新しい公開CI runがない場合は、その事実を記録する。成功runを捏造しない。

## エラー時

公開した分を残して止め、coordinatorへ実値と差分を返す。凍結値の不一致を再buildで合わせ込まない。
