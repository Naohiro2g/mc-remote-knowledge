# Scratch private素材の受領票（2026-10-06）

- 宛先: Scratch担当／human owner経由
- 対象票: `handoff-materials/2026-10-06-stack-backstage-handoff/materials/BACKSTAGE_ja.md`
- 元repo／source: `Naohiro2g/scratch-editor`、`7fbbf034488760d8fc7e034bf23f3e08e6e1807d`
- private inventory管理名: `scratch-private-intake-20261006`。privateな所在・実値・照合詳細はBackstage管理先に保持する。公開側の追跡は本票の受領結果・終了条件で行える。
- 結果: 指定28ファイルを棚卸しし、必要17件をGit外へ暗号化してコピー受領。全17件で復号後のbytes／SHA-256が元と一致。11件は長期保管不要として非保存に分類。受領対象の読取り・照合不能は0件。

| Scratch相対path（基点`handoff-materials/`） | 棚卸し | コピー受領 | 非保存 |
| --- | ---: | ---: | ---: |
| `2026-10-05-b9-scratch-dev/private/` | 5 | 起動設定・script・管理情報3件 | 一時browser状態・service log2件 |
| `2026-10-03-b8-scratch-live-gate/private/` | 9 | 設定・script・変更前設定3件 | 一時browser／WireScope観測・旧PID・log6件 |
| `2026-10-03-b8-scratch-live-human/private/` | 10 | 原画像10件 | 0件 |
| `2026-10-01-b8-local-playtest/`の指定設定・log | 4 | runtime config1件 | service log3件 |

受領した起動関連7件は、b9手元配信・b8戻し先・旧配信の終了と後続入力確保まで保存する。原画像10件はb8の結果をb9で再利用した根拠と後続差分確認のため保存し、後続確認終了・正式evidenceだけで足りることの確認後に保持要否を見直す。正式evidenceには観測JSONと画像identityがあり、原画像本体の代替画像が収容済みとは確認できなかった。

元の処理条件:

- 原画像10件は受領・照合済み。Scratch側で別用途や参照がなければ元を処理可。
- b9起動設定・script・管理情報はownerの終了／置換指示、参照終了、後続入力確保まで元を保持。
- b8戻し先はownerが不要と判断し、b9管理情報等の参照終了と後続入力確保まで元を保持。
- 旧runtime configは旧配信／戻し用途と参照の終了まで元を保持。
- 非保存11件はScratch側のbrowser／helper／対応serviceの参照終了後に整理可。受領時も一部service logを稼働processが開いており、今回の受領だけで削除可にはしない。
- `runtime/`配信物は対象外。Scratch側の継続保持に変更なし。

元ファイルの削除・移動、service停止、設定変更、credential操作、過去の動作試験の再実施は行っていない。受領のための新たな保存用途の判断待ちは0件。元の整理には上記のowner判断と参照終了確認が残る。

未完了はScratch側の終了・参照確認とcleanup、およびKnowledgeのb9 close②追跡への本受領結果・保持条件の反映。本票はhuman owner経由の返却用に作成し、外部送信は未実施。②全体のclose完了とは扱わない。
