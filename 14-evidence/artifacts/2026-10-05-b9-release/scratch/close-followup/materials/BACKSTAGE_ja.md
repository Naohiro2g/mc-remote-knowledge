# 搬送票：Scratch → backstage（private運用素材の棚卸しと引取り）

対象範囲を読み取りで棚卸しし、継続保管が必要なprivate素材をbackstageの管理先へコピーで収容してください。必要・不要・Scratch側で継続使用するものを分け、受領結果と元資料の処理条件を返してください。

- 搬送元 repo: `Naohiro2g/scratch-editor`
- 搬送元 surface: Scratch担当／Codex
- 搬送元 branch/commit: `agent/b9-tooling@7fbbf034488760d8fc7e034bf23f3e08e6e1807d`（公開b9 source）。本票と元のhandoff資料はGit管理外
- 作成日: 2026-10-06
- knowledge contract path: `00-hub/dev-repo-protocol_ja.md` runtime、`00-hub/b9-gate-close-instructions_ja.md`
- knowledge contract commit: `5beaad2557abbc6e90ada03edf7d0a2918fa7a52`（remote mainと一致を確認して実読）
- b9 close分類の起点: `handoff-materials/2026-10-05-b9-close/materials/CLOSE_ja.md`（実読knowledge `099c40b0c312694712653885200f3114ea4bed33`）
- 宛先: `mc-remote-backstage`担当
- 種別: その他（private ops／元画像の保管先整理と受領依頼）
- 決定／依頼: b9 closeで②として残したprivate素材の必要分をbackstageへ引き継ぐ。稼働のための手元参照はScratch側で維持する
- 理由: 公開evidenceへ含めない運用設定・log・参加者情報入りの原画像を、必要性と保管先を明記して扱うため
- 却下案: なし
- 影響: private素材の長期保管先と、Scratch側の元を処理できる条件を確定する

## 対象範囲

以下はScratch repoルートからの相対path。privateの実値はこの票へ複製していない。受領先はbackstage担当が管理するprivate保管先とする。

| 範囲 | 用途／確認してほしいこと |
| --- | --- |
| `handoff-materials/2026-10-05-b9-scratch-dev/private/` | 手元b9の起動設定、startup、稼働情報とservice log。運用を継続するために必要な分と、一時調査の残りを分ける |
| `handoff-materials/2026-10-03-b8-scratch-live-gate/private/` | 手元b8の起動・接続設定と戻し先。b9 startupが参照している戻し先を保護し、恒久保管が必要な分を引き取る |
| `handoff-materials/2026-10-03-b8-scratch-live-human/private/` | 参加者情報等を含む試験の原画像・private素材。公開evidenceのsanitize済み版で足りるものと、元を必要とするものを分ける |
| `handoff-materials/2026-10-01-b8-local-playtest/runtime-config.json`と`materials/bridge-server.log`、`materials/scratch-server.log`、`materials/wirescope-server.log` | 旧ローカル開発配信の設定・運用log。継続保管が必要なprivate opsだけを対象にする |

`runtime/`のGUI／Bridge／WireScope配信物はScratch側が使う②で、このprivate引取りの対象には含めない。初回の範囲確認は上記のfile一覧・用途から始め、内容の参照と保管はbackstage担当のprivate環境で行う。

## 実施してほしいこと

1. 指定範囲のfileを、必要なprivate保管／一時素材で不要／Scratchで継続使用、に分類する。必要な保存期間または終了条件を示す
2. 必要分をbackstageへコピーし、元とコピー先のbytes／SHA-256を照合する。backstage側のprivate inventoryへ元path・コピー先・照合結果を残す。credentialの実値は公開票・knowledge・GitHubへの転記対象にしない
3. 稼働を支えるfileは元を維持する。service停止、設定変更、移動・削除、credential操作はこの引取りに含めない
4. 過去の動作観測は再実施せず、保管の必要性を判断する。Bridgeのcontainer起動やVPS deployの試験は別の指示・作業として扱う
5. 元資料を読めない、コピー先へアクセスできない、保存する必要性が判断できない場合は、その範囲を未受領または判断待ちとして返す

## 稼働と保持条件

10/5の分類時点では、8611／8612／4183と8601／8602／4173のlistenerを確認した。b9 startupにはb8の戻し先参照があった。これは当時の観測であり、10/6の最新稼働状態を今回再確認したものではない。使用中かは引取り時に読み取りで確認する。

- b9起動・設定: コピー受領後も手元配信が参照する間はScratch側に保持。human ownerの終了・置換指示と参照終了、後続起動入力の確保後に整理する
- b8戻し先: human ownerが戻し先を不要とし、startup等の参照終了を確認した後に整理する
- 原画像・一時log: backstageが必要分を受領し照合した後、不要分または受領済み分について処理可否を返す。必要性が無ければその判断を明記する

## 返却物

- 引き取ったfile一覧、private収容先、bytes／SHA-256照合結果。実値を含む詳細はprivate記録へ置く
- 公開可能な受領票には、対象範囲、file数、受領済み／未受領、private inventoryの参照名、未完了と処理条件を記載する。privateな接続先やcredentialの実値、player UUIDを載せない
- 不要と判断したもの、Scratch側で継続保持するものと理由
- 元を処理してよい範囲と、service参照等によりまだ処理できない範囲
- 判断が必要な保存用途が残る場合、その具体的な項目

## 根拠・処理条件

- 根拠/検証: b9 closeの分類票と元directoryの存在を確認。本搬送作業ではprivate実値を読出し・転記せず、稼働の再確認とbackstage側の収容は行っていない
- 既に変更した実装/文書: 本搬送票とローカルNOTES。元private／runtime、稼働service、backstage repoは変更していない
- ナレッジ着地希望: private詳細を除く受領・保持・終了条件をb9 closeの②追跡へ反映。private inventoryの正式管理先はbackstage担当が決める
- 捕捉 cleanup: コピー受領・照合だけでは稼働参照中の元を削除可にしない。受領と参照終了等の条件が戻ってからScratch担当が処理する
- 着地後の確認戻り先: human owner経由でこのScratch担当sessionへ返す。本票作成時点では外部送信・backstage側の受領は未実施
