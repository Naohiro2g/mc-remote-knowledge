## Release gate 確認票

- 対象 repo：McRemote。
- 対象 branch/commit：`main@17bcf2645c112133935bc9d993d4fdd4669ceb98`。公開tagのpeeled commitも同じ。
- release / channel：`v2320.0.0b10`／GitHub pre-release。draft=false、prerelease=true、Latest非対象。
- gate coordinator：knowledge担当session。
- human release owner：human owner。
- current phase：許可されたpre-release作成と公開asset照合を完了。3 OSの人間試験とpre-release解除は後続の別指示。
- contract maturity / required test tier：既に採用された同一candidateの公開経路確認。tag CI／公開workflow、公開assetのdigest・bytes・実file照合。新しい製品コードやwire変更なし。
- knowledge contract path：`00-hub/release-gate-notes_ja.md` b10の進捗／2026-10-14 human owner公開許可、`00-hub/release-operations-responsibility-design_ja.md`、指示票`instruction-prerelease-b10.md`。参照DEC `2026-10-13-05`／`2026-10-13-07`。
- knowledge contract commit：`84b402782ecc8b7f050e8dd7f2ae29ed58b09a85`（runtime／INDEX／関連文書を取得・実読）。指示票が根拠とした許可は`dd92462d9a65d4d8ea98c3be0c07c09372a5e2dd`にあり、実読refでも確認。
- gate manifest identity：新しい横断setを作成・freezeしていない。
- change cone：公開tag、pre-release metadata／asset、公開経路の照合のみ。
- reused PASS / rationale：採用元CI `38347345527`／artifact `11789398049`の4 fileと、タグCIの4 fileが全bytes一致。保持JAR／record／manifestを公開fileとも照合した。1.21.11／26.3のpulseと通常restartの同一JAR観測を引き継ぎ、新しい実行や3 OSの人間試験をしたとはしない。
- exact compatibility set / freeze status：McRemote対応版は1.21.11／26.3。下記source／tag／asset identityを固定。横断freezeではない。
- target deployment / profile / lock：GitHub Releaseのみ。shared／通常dev／箱庭／homepageのdeployなし。
- authorized next action：指示票McRemote節のtag作成、GitHub pre-release作成、各assetのGitHub digestと再download bytes／SHA-256の返却を実施。
- test class：publication／artifact integrity verification。tag CIと公開workflowのunit/deterministic。今回新しいlive-auto／live-humanなし。
- 実行した command / 手順：下記。公開workflowは照合済みタグCI artifactを再buildせず昇格。
- 結果：pre-release作成成功、公開workflow success、5 assetすべてGitHub digest／sizeと再download実fileが一致、採用元のfileと全bytes一致。
- evidence record / artifact：本directoryの`tag-binding.json`、`tag-ci-candidate-comparison.json`、`tag-ci-run.json`、`release-workflow.json`、`release-api.json`、`public-assets-verification.json`等。元candidateとpulseは`handoff-materials/2026-10-13-b10-paper263/`。正式evidenceではなくknowledge向け返却素材。
- 未検証の境界：pre-releaseのassetからのWindows／macOS／Linuxの人間試験、各実機のMinecraft接続・操作、Windows／macOSでのPaper26.3起動、実player event callback。pre-release解除・通常公開判定はしていない。
- security / compatibility / rollback の確認：認証情報・raw log・DB／worldをassetに含めない。版別recordはsanitizedを点検し、公開後のbytesも一致。公開した番号／tagは差し替えない。元candidateの同一性とmanifest v2契約を保持。
- 判定を求める事項：pre-releaseと公開asset照合の受領、Scratchと併せた3 OS人間試験の後続指示。pre-release解除／shared deployは引き続き別指示待ち。

### Release URL・tag target

- Release：[https://github.com/Naohiro2g/McRemote/releases/tag/v2320.0.0b10](https://github.com/Naohiro2g/McRemote/releases/tag/v2320.0.0b10)。
- Release ID：`412440460`。
- title：`McRemote 2320.0.0b10 (Minecraft 1.21.11, 26.3)`。
- tag：`v2320.0.0b10`。
- tag object SHA：`bcc76f5c8578ab3220f1890714b2a2f685852433`。
- **tagが指すcommit：`17bcf2645c112133935bc9d993d4fdd4669ceb98`**。remote annotated tagをAPIでpeeled commitまで照合。
- published_at：`2026-10-14T07:26:42Z`（GitHub API、UTC）。
- flags：draft=false、prerelease=true。作成・公開時とも`--latest=false`を指定。`releases/latest`は前後とも`v1.21.8-1.4.0`のまま。

### 公開assetのbytes・SHA-256

各rowのSHA-256は、GitHubのasset digest（`sha256:<同値>`）と匿名HTTPS downloadした実fileで**別々に照合して一致**した値。さらに保持した元fileとも全bytes一致。個別のGitHub digest文字列、download SHA、asset ID／URLは`public-assets-verification.json`に収録。

| asset | bytes | SHA-256（GitHub／download共通） |
| --- | ---: | --- |
| [`manifest.json`](https://github.com/Naohiro2g/McRemote/releases/download/v2320.0.0b10/manifest.json) | 1,761 | `508a34b9ea29357105e6fcc124a7ab0c0eba8ec9fa258eee52bb196222856627` |
| [`mc-remote-2320.0.0b10.jar`](https://github.com/Naohiro2g/McRemote/releases/download/v2320.0.0b10/mc-remote-2320.0.0b10.jar) | 315,352 | `96ddf09f765a77811740d5c62f3787f7a87c8be6cd7247d345f6dfe9e93512a4` |
| [`mc-remote-verification-1.21.11.json`](https://github.com/Naohiro2g/McRemote/releases/download/v2320.0.0b10/mc-remote-verification-1.21.11.json) | 63,177 | `c79ca8e667f46b0df4f6703ce3173c40741e9c37427e4de7908cc396390674f9` |
| [`mc-remote-verification-26.3.json`](https://github.com/Naohiro2g/McRemote/releases/download/v2320.0.0b10/mc-remote-verification-26.3.json) | 63,717 | `e07fd1513f731d587302621b95234fb135fa95553ca87111829bcda3618b1754` |
| [`minecraft-targets.json`](https://github.com/Naohiro2g/McRemote/releases/download/v2320.0.0b10/minecraft-targets.json) | 126 | `8e830732decd6bcde13f91eb6c071d062ba6993342a7edb52e6ea543b9e0c361` |

指示票のJAR315,352 bytes／`96ddf09f…512a4`、manifest1,761 bytes／`508a34b9…56627`と一致。既存b10の公開workflowはmanifest v2の検証recordを同じReleaseから取得するため、版別record2件を先に添付した。公開workflowがJAR／manifest／宣言を添付し、5 asset構成になっている。JARの作り直しやrecordの付け替えはしていない。

### CIと公開workflow

- 採用元CI：[38347345527](https://github.com/Naohiro2g/McRemote/actions/runs/38347345527)、artifact `11789398049`。
- tag CI：[38525157673](https://github.com/Naohiro2g/McRemote/actions/runs/38525157673)、success、artifact `11875384710`。
- tag CI artifact ZIP：294,247 bytes、SHA-256 `34df232ed723a68ab03dfa449e37e216f9547aaac3144c637071890a8b25d9c5`。provider digestとdownload ZIPを照合。ZIP container自体のdigestは採用元と異なるが、JAR／declaration／SHA256SUMS／source stampの全4 fileは採用元と同じbytes。
- 公開workflow：[38528358810](https://github.com/Naohiro2g/McRemote/actions/runs/38528358810)、release event、source `17bcf2645c112133935bc9d993d4fdd4669ceb98`、全job success。ログの`candidate run 38525157673`とJARのSHA256SUMS OKを照合。公開段階で再buildなし。

### 本文と操作

本文は採用済みgeneratorの`release-targets-section_ja.md`を使い、1.21.11はJava21／26.3はJava25、server folder別のmise固定とtag版READMEの案内を追加した。title／対応版の一覧は同じdeclarationから導出している。公開workflowの本文読取・書戻しにより末尾改行が1つ増えるが、その他の本文は準備fileと同じ。`release-body-published_ja.md`にAPIから取得した本文を収録。

実施した主な操作：

```sh
git tag -a v2320.0.0b10 17bcf2645c112133935bc9d993d4fdd4669ceb98 -m "McRemote 2320.0.0b10 prerelease"
git push origin refs/tags/v2320.0.0b10
# tag CI成功、採用candidateとの4file全bytes一致を確認
# gh release create: --verify-tag --draft --prerelease --latest=false、title／notes-file、版別record2件を指定
# gh release edit v2320.0.0b10 --draft=false --prerelease --latest=false
# 公開workflow成功後、全assetをbrowser_download_urlから匿名HTTPS downloadして照合
```

既存ユーザーのREADME編集とおすすめプラグイン文書はそのまま保持。今回製品sourceのcommit／main pushはしていない。Scratch担当への指示実行・repository variables変更・shared deploy・pre-release解除はしていない。

### packetの保持

採用元の26.3 packetは公開JAR／manifestの照合元として実際に使い、今回の一致を確認した。元packetと本packetはknowledge coordinatorへの分類②参照移管対象とし、今回の確認票受領と後続の3 OS試験への参照移管が確認できるまで保持する。
