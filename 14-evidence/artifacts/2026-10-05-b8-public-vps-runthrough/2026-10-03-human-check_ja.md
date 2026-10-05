# 公開betaの人間操作確認

2026-10-03 22:35 JST、human ownerがscratch-betaからペアリング成功を報告した。

- 認証前のhello: error -32000、reason auth_required。
- ペアリング後のhello: protocol 23.2.0、Scratch client 2320.0.0b8、Minecraft1.21.11、overworld、origin [200,0,200]。
- 権限応答: online=true、offline=true、build_range=500。VPSの起動観測でLuckPermsPermissionManager使用を確認済み。
- chat.post送信52、受信53: params／result「Hello, Minecraft!」成功。

これは公開Scratch・Bridge・McRemoteの認証付き接続とchatを確認した結果。Java／統合版の新規world参加、noticeペイン表示、フルWireScope画面の操作は、この報告では確認していない。

2026-10-03の追加報告: root用の永続UDPフィルタ修正・backup転送drop-in導入を「エラー無く完了」と報告。続けて「iPadからもマイクラ世界に入れている」と報告。統合版の公開world参加を確認済みとする。外部UDP statusも26.51／protocol2193でPASS（public-smoke.json）。
