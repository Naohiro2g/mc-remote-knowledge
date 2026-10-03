# b8 live-human差分：iPadのdustサイズ（Java・色の追加確認済み）

- 日付: 2026-10-03
- knowledge contract path: `00-hub/b8-gate-live-test-sheet_ja.md`「共通」「4. live-human」。
- knowledge contract commit: `3f0c14ab9e41e469a23f865b3e7a313744bdcdc7`（remote mainと照合、実参照済み）。
- Scratch実行source: 凍結GUI `691576f60b7f0824e1753bd6823901d01fbe2422`。serverは認証済みhelloでprotocol23.2.0／MC1.21.11。Javaクライアント画像のタイトルは26.2。iPad版と周辺プラグインの実版は未採取。
- test class: live-human。human ownerがScratchから実行し、Java／iPadで観察。
- 観測: human owner「iPadだと、大きさの変化がない。1ぐらいで固定」。iPadでdustのsize反映を確かめるassertionはFAILとして記録。
- 追加観測: human ownerがJava側のサイズ変化と両端末のRGB色指定を確認。JavaのsizeとJava／iPadの色のassertionはPASS。0.0については「0.0はエラーだった。0.01はオッケー」と訂正を受領し反映した。0.0を受け入れたとは記録しない。
- 下限: B8 fixtureの範囲は0.01〜4で、Scratchのdust設定ブロックにも同じ検証がある。今回のJava画面では実際に見えたのが約0.2からとの報告。0.01の受け付けと、見た目での可視性を区別する。error reasonとどの層で拒否されたかは未採取。
- 入力: 添付Scratch画像ではworld、位置0,124,0、ずれ各0.3、speed0、count20、force=true。赤size1→赤size4→青size1を順に生成。size1と4はいずれもB8の範囲内。
- 根拠: `materials/observations.json`。画像は`private/dust-color-size-blocks.png`へ保存し、digestを`materials/image-identities.json`に記録。dustの要求・応答frameは未受領で、wire error reasonは観測していない。
- 原因候補: [Geyser公式sourceのDUST変換](https://github.com/GeyserMC/Geyser/blob/63a4e2b79b12f0d138777d5fd80176a112b4bd72/core/src/main/java/org/geysermc/geyser/translator/protocol/java/level/JavaLevelParticlesTranslator.java#L135-L144)をread-onlyで確認。色をFALLING_DUSTへ渡し、scaleを反映していない。今回の観測と整合するが、導入済み版との照合前なので原因を確定しない。
- 続行: 差分を記録して残りの確認を続ける問いに、human owner「続行」（2026-10-03）。同じ凍結版で残りを確認する。iPadのsize assertionのFAILは維持する。
- 確認待ち: 導入済みGeyser版との照合と、iPadのサイズ差の対応範囲。差分を返す素材は用意済み。
- 境界: Scratch／McRemoteの不具合、Geyserの導入版の原因、component／横断GREEN・HOLD・RED、release可否は未確定。凍結source／artifact、serverの設定・プラグインはagentから変更していない。
- 返却先: knowledge coordinator。ベータでの統合版の対応範囲、制限として記録する扱い、残りのlive-human確認の継続を判断する材料とする。
