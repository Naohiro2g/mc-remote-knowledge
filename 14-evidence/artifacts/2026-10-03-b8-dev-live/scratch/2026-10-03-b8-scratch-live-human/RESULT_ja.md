# Release gate 確認票（追記：Scratchからのlive-human終了）

- 対象 repo: scratch-editor。
- 対象 branch/commit: agent/b8-compatibility。実行した凍結sourceは`691576f60b7f0824e1753bd6823901d01fbe2422`。現在のHEAD`01cdb0bfee3a681697ffa44db5b890045b74b01c`のWireScope列幅変更はb9持ち越しで、今回の実行成果物には含めていない。
- release / channel: 2320.0.0b8 / beta候補。protocol 23.2.0。
- gate coordinator: knowledge coordinator。
- human release owner: human owner。
- current phase: Scratch担当の実施終了。segment 4の3D graph描画はhuman ownerがPython環境で続行する。
- contract maturity / required test tier: b8 wire確定境界の凍結成果物によるlive-human。サウンドシーケンスは初回stable後の未批准案。
- knowledge contract path: `00-hub/b8-gate-live-test-sheet_ja.md`「共通」「3. Scratch」「4. live-human」、`00-hub/release-gate-notes_ja.md`の2026-09-30節、`10-protocol/wire-format-design_ja.md` §5.8.3。教材・後続案の参照は`10-protocol/sound-extension-notes_ja.md` §5。
- knowledge contract commit: `3f0c14ab9e41e469a23f865b3e7a313744bdcdc7`。終了票作成時にremote mainと照合し、統一実施票とgate節を実参照した。凍結原票は`749ba60dc8c18938e50ce66b8e820aac4401c69e`。
- gate manifest identity: 上記gate節の`b8-integrated-artifact-set-1`。
- change cone: 凍結成果物を変更せず、human ownerのMinecraft描画・聴取・字幕の観測を追記。製品コード、fixture、source、artifactの変更なし。
- reused PASS / rationale: segment 3のScratch学習面・real-browser WireScopeの返却は`../2026-10-03-b8-scratch-live-gate/RESULT_ja.md`。同じ凍結成果物のまま、今回の描画・聴感の確認を追加した。segment 3のbackpressure案内の実機確認はNOTRUNであり、PASSへ置き換えない。knowledgeのgate節ではhuman ownerの判断でb8を止める理由にしないと記録されている。
- exact compatibility set / freeze status: `b8-integrated-artifact-set-1`を維持。使用したGUI／Bridge／WireScopeのbytes・SHA-256は上記segment 3票の凍結identity表。fixtureはowner`054a3af017f1abb8cc01cf85b3bc83181e648e19`、entity-particle-v23.2.json、36481 bytes／111 case／SHA-256 `ca636b4a2685ea67f24d8e7931e3d30a84e7cec872bb5c5d2eadd178cdac39f2`のまま。
- target deployment / profile / lock: devの通常環境。Scratch／Bridgeは手元の開発端末、Minecraftはdev。privateな接続値は本票に含めない。Javaクライアントは画像タイトル26.2、server MCは認証済みhelloの1.21.11。第二端末はiPad Bedrock、実版と導入済みGeyser／Floodgateの実版は未採取。
- authorized next action: human owner「ここまでで漏れがなければ閉じてください。続きはPython環境でやります」に従いScratch側を閉じる。3D描画の続行はhuman ownerがPython側で行う。当agentから他repoへ着手・指示しない。
- test class: live-human。human ownerがScratchとMinecraftを操作し、agentがガイドと返答の捕捉を行った。遅延原因候補の確認には自repoと公式Geyser sourceのread-only参照を使用。
- 実行した command / 手順: 認証済みhelloでprotocol23.2.0／MC1.21.11を照合。particle／soundのself・world、dustのRGBとサイズ、block particle、音の定位・距離減衰・N指定、playBlockSoundのplace／hit／break／step／fallを順に確認。開始時helloは14:11:59。終了時、残る音の定位・減衰・N指定の両端末確認への問いにhuman owner「全てオッケーでした」と返答。
- 結果: 下表。iPadのdustサイズ差は途中のFAILを維持。「全てオッケー」の適用範囲は最後に尋ねた音の3確認であり、dust差分や未実施の3DをPASSへ変えない。
- evidence record / artifact: 正式配置はknowledge coordinatorが行う。提案recordは`14-evidence/records/b8-scratch-live-human-2026-10-03_ja.md`、artifactは`14-evidence/artifacts/b8-scratch-live-human-2026-10-03/`。本票、`DUST-BEDROCK-DIFFERENCE_ja.md`、`materials/start-observation.json`、`observations.json`、`image-identities.json`、`export-identities.json`を搬送素材として準備。原画像はprivateに保持し搬送しない。これらのローカルpathを正式evidenceとは扱わない。
- 未検証の境界: 3D graphの描画はPython側の続行待ち。iPadのMinecraft版・導入済み周辺プラグインの版との照合、dustサイズ差の原因確定、正確な可聴距離・減衰曲線・音の周波数・遅延時間、全resource IDの描画・聴取の網羅は未実施。字幕の観測端末・音ID・methodは未指定。人間試験の操作ごとの完全なwire transcriptはなく、保存frameは開始helloと入力エラー／固定ID成功の抜粋。
- security / compatibility / rollback の確認: token、pairing_id、private address、player UUIDを搬送JSONへ含めない。参加者名を含む原画像はprivateで保持。認証設定、server、world、config、credentialを当agentから変更していない。製品修正・再凍結・rollback試験、tag／release公開なし。終了指示は作業セッションの終了として扱い、ユーザーのブラウザ・配信サービス・Minecraftの終了操作は行っていない。
- 判定を求める事項: iPadのdustサイズ差をどの対応範囲／制限として扱うか、導入済みGeyserの実版照合の要否、Pythonでの3D描画結果を含む横断gateの判定はcoordinatorへ返す。Scratch担当はGREEN／HOLD／REDやrelease可否を判定しない。

| 確認項目 | Java | iPad | 根拠・境界 |
| --- | --- | --- | --- |
| particle self／world | PASS | PASS | selfは本人のみ、worldは近くの両playerへの表示をhuman ownerが確認 |
| sound self／world・聴取 | PASS | PASS | 両receiverの聴取をhuman ownerが確認 |
| dust RGB | PASS | PASS | 両端末のRGB指定を明示確認 |
| dust サイズ変更 | PASS | FAIL | Javaでは変わり、iPadでは約1相当で固定との観測。0.0はエラー、0.01は受け付けられた |
| block particle | PASS | PASS | gold_block／stone／sea_lanternの試行と追加確認。全blockの網羅ではない |
| 音の左右の定位・距離減衰 | PASS | PASS | 終了時に両端末の確認への問いに「全てオッケーでした」 |
| N指定の音階変化 | PASS | PASS | 同じ終了時の明示確認。正確な調律の測定ではない |
| block音5kind | PASS | PASS | 「5種類、Java/iPadで確認」。違いは聞き分けにくいとの観測も保持 |
| 3D graph描画 | NOTRUN | NOTRUN | human ownerがPython環境で続行する |

追加観測として、音の字幕表現がコマンド実行でも表示されることを捕捉した。端末・音ID・methodが未指定なので、全クライアント共通の主張にはしない。

後続へ残す内容は、selfの表示を「自分だけ」にする案、座標指定とブロック指定で音源位置が違うことを比較する教材案、連続playSoundでは和音が揃わない観測とシーケンス早期実装への関心。サウンドの通常プレイの動作別補正を加えない仕様と、明示したvolume／noteの置き換えも実機観測と合わせて記録した。対象releaseや設計の批准を当票では変更しない。
