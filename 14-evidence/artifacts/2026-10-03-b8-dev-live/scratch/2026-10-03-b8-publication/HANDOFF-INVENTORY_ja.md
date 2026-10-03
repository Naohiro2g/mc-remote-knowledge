# b8公開時のローカル搬送素材の分類

release operations §12。全14 directoryに引継ぎ先、entryのSHA-256、次の一手を指定。正式summary着地済みでも詳細artifactの配置確認や非参照確認を飛ばして破棄しない。

この一覧は引継ぎ対象を指定するものです。正式evidenceへの配置完了や、外部への送信完了を主張しません。private素材は公開搬送せずbackstage担当へ渡す対象です。

| directory | 分類・引継ぎ先 | 次の一手 |
| --- | --- | --- |
| 2026-09-30-b8-gate-confirmation | ② 後続担当へ引継ぎ：knowledge coordinator（b8 close） | 確認票のknowledge着地と参照を照合し、詳細素材を正式evidenceへ移すか非参照を確認して整理する。 |
| 2026-09-30-b8-scratch-blocks | ② 後続担当へ引継ぎ：b9 Scratch担当 | 公開v2320.0.0b8のブロック仕様と素材を照合し、作例・再利用の要否と非参照を確認して整理する。 |
| 2026-09-30-b8-scratch-candidate | ② 後続担当へ引継ぎ：knowledge coordinator（b8 close） | 旧candidateのmanifestがb8経緯・Python同梱物の参照に使われているかを確認し、正式配置または非参照の整理を決める。 |
| 2026-09-30-block-picker-names | ② 後続担当へ引継ぎ：b9 Scratch担当 | 公開v2320.0.0b8の表示名と照合し、picker仕上げ・素材取得の後続作業へ必要な参照を移す。 |
| 2026-10-01-b8-candidate-b7-fixes | ② 後続担当へ引継ぎ：knowledge coordinator（b8 close） | 是正3件の返却とcandidateの経緯を現release manifestへ照合し、必要な詳細を正式配置して非参照素材を整理する。 |
| 2026-10-01-b8-fixture-preflight | ② 後続担当へ引継ぎ：b9 Protocol／fixture移管のgate coordinator | 691576fの凍結後棚卸しと合わせて移管担当へ渡し、consumer・依存・workflow roleを移管開始時に再確認する。 |
| 2026-10-01-b8-local-playtest | ② 後続担当へ引継ぎ：b9 Scratch担当（private運用素材はbackstage担当） | ローカル試運転の資料・補助serverの用途を確認し、必要なprivate素材はbackstageへ移し、残りは参照確認後に整理する。 |
| 2026-10-02-b8-candidate-local-fixes | ② 後続担当へ引継ぎ：knowledge coordinator（b8 close） | 691576fのcandidate素材を公開manifestのidentityと照合し、局所決定・素材参照の着地を確認して整理する。 |
| 2026-10-02-home-scratch-contract-reply | ② 後続担当へ引継ぎ：Stackのhome環境担当 | 68832e0a95c0462462e9a10115bfae272ec1a6d7を対象とした回答の受領・採用を確認し、home対応へ参照を移す。 |
| 2026-10-02-stack-wss-reply | ② 後続担当へ引継ぎ：Stackのhome環境担当 | WSS subprotocolの回答と再現素材を受領し、b7.post2のhome検査の修正結果を返す。 |
| 2026-10-03-b8-publication | ② 後続担当へ引継ぎ：knowledge coordinator（b8 close） | 本票の公開identityをGitHub・GHCRで読み取り照合し、公開後の正式evidenceとgateの終了へ移す。 |
| 2026-10-03-b8-scratch-live-gate | ② 後続担当へ引継ぎ：knowledge coordinator（正式evidence担当。private素材はbackstage担当） | fd7cad7の正式recordでsummaryの着地を確認済み。詳細素材・原画像・private運用値の参照を照合し、必要な正式artifact／backstageへ配置して整理する。 |
| 2026-10-03-b8-scratch-live-human | ② 後続担当へ引継ぎ：knowledge coordinator（正式evidence担当。後続教材はb9 Scratch担当） | fd7cad7の正式recordでsummaryの着地を確認済み。詳細観測・字幕・教材・和音と画像の参照を照合し、正式artifactまたは後続担当へ移す。 |
| 2026-10-03-wirescope-column-width | ② 後続担当へ引継ぎ：b9 WireScope担当 | 01cdb0bfee3a681697ffa44db5b890045b74b01cと素材を取り込み、b9候補のrelease source・artifact・Python同梱物のidentityを確認する。 |

entryの正確なSHA-256は`materials/handoff-inventory.json`を参照。判定対象はdirectoryの削除可否であり、正式evidenceからの非参照はまだ確定していません。
