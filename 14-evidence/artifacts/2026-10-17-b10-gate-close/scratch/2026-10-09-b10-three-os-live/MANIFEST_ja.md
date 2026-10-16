# b10 3 OS live-humanの観測素材

- 実施票: knowledge `00-hub/b10-gate-live-test-instructions_ja.md`
- 実読knowledge commit: `7d1b3809b0987f7fc0e5c5c2f365a42e9046e240`
- Scratch candidate: `c717d0c2ed9b045b8c3bb925b0e1fcd8ee33010b`、CI run `37808012407`、artifact ID `11563852835`
- 用途: human ownerから返った操作結果を蓄積し、coordinatorへ搬送する素材。正式evidenceはknowledge側が起こす。
- 現在の観測: 3 OSのScratch ZIPのSHA-256一致をhuman ownerが報告。WindowsのUniGetUI→mise導入とMicrosoft Java 21／25切り替え、macOSとUbuntuのJava 21環境確認、macOSのSDKMAN通常版インストール失敗も受領。Ubuntu／macOS／Windows 11それぞれで、Paper 1.21.11／26.2にMcRemote b10を導入し、ワールド参加まで確認完了との報告を受領（計6組）。Paper exact build、JAR identity、起動Java、認証設定とLuckPermsの有無はこの報告では未確認。Scratch ZIPのブラウザ取得とOS標準展開の詳細は未報告。WindowsのScratch起動・接続の続報は下記。macOS／UbuntuのScratch Local操作結果は未報告。
- 素材: `materials/WINDOWS_OBSERVATIONS_ja.md`、`materials/WINDOWS_MISE_JAVA_OUTPUT.txt`、`materials/MACOS_OBSERVATIONS_ja.md`、`materials/UBUNTU_OBSERVATIONS_ja.md`、`materials/MACOS_SDKMAN_INSTALL_FAILURE.txt`、`materials/ZIP_HASH_OBSERVATIONS.json`
- 記録ではterminal promptのユーザー名・host名を省略する。token、private address、player UUIDを収録しない。
- Windowsの続報: ランチャー初回起動は警告なし。認証ONではpair認証後も接続せず、serverのcredential domainはUNHEALTHY。認証OFFでは接続とhello world成功だが独立WireScopeリンクが出ない。`materials/WINDOWS_ISSUES_HANDOFF_ja.md`へ担当別の障害追記を作成。sanitized startup logと固定3 ZIPのWireScope欠落のstatic inspectionを同梱。candidate変更なし。

