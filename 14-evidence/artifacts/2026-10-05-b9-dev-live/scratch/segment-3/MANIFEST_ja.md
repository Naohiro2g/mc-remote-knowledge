# b9 Scratchの手元dev接続準備

- 作成日: 2026-10-05
- 依頼: human owner「次はb9 scratchから接続したい」
- knowledge参照: `561de98b5c15864ac9b86cb6dcaeef1f20ce635b`、`00-hub/b9-gate-live-test-sheet_ja.md`
- 配布元: 凍結set `b9-integrated-artifact-set-1`のScratch候補 `7fbbf034488760d8fc7e034bf23f3e08e6e1807d`、tooling `dc1ab834183e29f2eb03059b07e99d2b463776ee`
- 入力: `../2026-10-05-b9-tooling-migration/artifacts/scratch-candidate-7fbbf03448.zip`。外側ZIPと使用した4 artifactのbytes／SHA-256を再照合
- 配信: localhost 8611（GUI）／8612（Bridge）／4183（WireScope）。b8と同じbrowser origin／targetを維持。接続設定はprivateへ収容
- 実行形態: GUIとWireScopeは候補から展開した静的配信。Bridgeは凍結OCIのlinux/amd64 `/app`を展開してhost-native Nodeで実行。Docker daemonが無いためOCI containerの実行は未検証
- 検証: 配信GUIのindex／gui.jsとWireScopeの全6 fileが入力とbyte一致。配信runtime config一致。移管Bridge経由のhelloはauth_required、one-shot auth.pairBeginで6桁pair code発行。socketを正常切断
- human確認: b9 Scratch→b9 pluginで再ペアリングなしの接続成功。WireScope提示のhelloでclient2320.0.0b9、protocol23.2.0、MC1.21.11を照合。提示2行は`materials/user-b9-hello.json`
- 追記検証: 独立Chromiumで新規pairingをhuman ownerが承認。最初の認証済みhelloはprotocol23.2.0／MC1.21.11一致。代表ブロック12回（チャット、設置・読戻し、entity、particle、sound、カタログID一覧、picker日英検索と適用）がPASS。22 frameすべての独立WireScope表示をDOMで照合、画像を保存
- 後片付け: 空の試験位置を事前確認、gold_blockを元のairへ復元し読戻し一致。生成armor_standは削除成功
- human列幅確認: 2026-10-05、human ownerが`wirescope-b9-columns.png`を確認し「画像確認しました。オッケーです。」。時刻列／方向列の幅はPASS。記録は`materials/human-width-review.json`
- 未検証: OCI container実行、稼働JAR／Paper／Java／credential healthの本担当による採取は未実施。描画・音のhuman試験はb8結果を再利用。Bridgeのhost-native実行の採否はcoordinator判断待ち
- 公開source、tag／Release、devのMCサーバー設定・JARに変更なし。代表試験のworld変更は復元済み
- 素材: `materials/CONFIRMATION_ja.md`、`materials/representative-results.json`、browser helper3件、WireScope／picker画像、`materials/runtime-identity.json`、準備時の`materials/readiness.json`、`artifacts/`の使用artifact。helperの失敗結果3件は別fileへ保持。正式evidenceはknowledge側へ搬送予定
- private: deployment、起動script、稼働PID、service log。公開搬送しない
- 完了処理: 試験専用Chromiumを終了。通常browserは未操作。Scratch8611／WireScope4183の配信HTTP200を確認し継続。`materials/completion.json`へ記録
- 後続: b9 Scratch接続／segment 3へ引き継ぐ。稼働serviceがruntimeを参照中なので使用終了前に削除しない。b8 runtimeは戻し先として保持
