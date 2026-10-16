# Windows 11の観測（進行中）

## Scratch ZIPの取得とSHA-256確認

- 根拠: human ownerの操作報告。hash出力そのものは未提供だが、以下の各シェルで固定candidateのSHA-256との一致を確認したとの報告を受領。
- 操作: ダウンロードした`scratch-candidate-c717d0c2ed9b045b8c3bb925b0e1fcd8ee33010b.zip`を開き、中から`mc-remote-scratch-local-2320.0.0b10-windows-x64.zip`を取り出した。
- 対象SHA-256: `08340c801c1196c30a1227a7e495feb32131a95e4816ffbb29278557cadab9c1`
- Git Bashでは`sha256sum.exe`を使用。今回の環境では`certutil`が使えなかったとの申告。エラー内容は未提供で、全Git Bash環境で使えないという主張はしない。
- CMD、従来のPowerShell、PowerShell 7.6.6では`certutil`を使用し、いずれも一致したとの報告。
- ブラウザによる取得の詳細とWindows 11 buildは未報告。

Git Bash:

```sh
sha256sum.exe mc-remote-scratch-local-2320.0.0b10-windows-x64.zip
```

CMD / 従来のPowerShell / PowerShell 7.6.6:

```text
certutil -hashfile mc-remote-scratch-local-2320.0.0b10-windows-x64.zip SHA256
```

## Javaのインストール準備

- human ownerの報告: UniGetUIで`java 21.0.12.0`と`java 25.0.4.1`をインストールした。
- これらは報告されたインストール管理側の版表示として記録。後続の報告で、UniGetUIのカタログに見えていたMicrosoft版を選んだとの説明を受領。このインストール分の`java -version`の完全な出力とinstallation pathは未受領。
- 検証の視点: human ownerの指示によりOSS利用者が既存の案内を使って進める手順を観察する。agentが提案した起動.cmdの自作は実施結果へ含めない。

## miseでの導入とJava 21／25の切り替え

- 根拠: human ownerの操作報告と貼付した実行出力。
- mise本体をUniGetUIからインストールし、WindowsのBashから使えたとの報告。mise本体の版は未報告。
- Bashの有効化に`eval "$(mise activate bash)"`が必要だったとの報告。human ownerが、通常どおりインストールしたGit for WindowsのGit BashをWindows Terminalで使用していると確認。promptの種別は`UCRT64`で、内部pathが以前の`/mingw64/`から`/ucrt64/`へ変わったとの観測。Gitの版は未報告。
- `mise use java@microsoft-21`で`microsoft-21.0.12.1`をインストール（表示時間24.7秒）。`mise use java@microsoft-25`で`microsoft-25.0.4.1`をインストール（表示時間30.0秒）。
- Java 25を選択した後の`java -version`、Java 21へ切り替えた後の`java -version`を受領。両者とも64bitのMicrosoft OpenJDKで、選択結果と一致。
- 最後に確認した選択: Java 21。Paper起動とワールド参加は後続で報告されたが、各環境の起動Javaとの対応は未採取。
- human ownerが`echo 'eval "$(mise activate bash)"' >> ~/.bashrc`を実行し、毎回の手入力が不要になったと報告。Git for Windowsが`.bash_profile`の欠如を通知して作成したとの観測。生成fileの内容は未採取。
- macOS／Ubuntuでのmise実行は未報告。
- human ownerの評価: 「mise、良い」「sdkmanより長期的にも使えそう」。利用者手順の検討材料として保持し、将来の保守性や全OSでの採用決定を確定したという主張はしない。
- 追加の使い勝手の報告: TABキーによる補完がSDKMANより弱く感じる一方、インストール後は`@21`／`@25`で切り替えられて便利。短縮指定の完全なコマンドと出力、補完設定は未受領。
- sanitized実行出力: `WINDOWS_MISE_JAVA_OUTPUT.txt`。terminal promptのユーザー名とhost名は省略し、設定fileのhome pathを`~`に置換。
- human ownerからIntelliJとの共存への懸念を受領。IntelliJでの実動作は未検証。[JetBrainsのSDK説明](https://www.jetbrains.com/help/idea/sdk.html)ではJDKのhome directoryを登録し、IDEからのダウンロードも可能。[miseのJava説明](https://mise.jdx.dev/lang/java.html)では有効化したshellの`JAVA_HOME`を変更する。[IntelliJのterminal説明](https://www.jetbrains.com/help/idea/terminal-emulator.html)でもproject JDKを`JAVA_HOME`／`PATH`へ設定するため、内蔵terminalで使うJDKは実環境で別途確認する。

### UCRT64の公式資料との照合

- [MSYS2の環境説明](https://www.msys2.org/docs/environments/): MINGW64は旧MSVCRT、UCRT64は新しいUniversal C Runtimeを使う64bit環境。MSYS2は2022-10-29に既定をUCRT64へ変更し、2026-03-15にMINGW64を非推奨とした。
- [Git for WindowsのRelease Notes](https://github.com/git-for-windows/build-extra/blob/main/ReleaseNotes.md): v2.56.0（2026-09-28）でMINGW64からUCRT64へ移行し、内部pathも変更。今回の表示はこの変更と整合するが、手元のGit版の照合は未実施。

| 系統 | miseで選択された版 | Runtime / VM | Java build |
| --- | --- | --- | --- |
| Java 21 | `microsoft-21.0.12.1` | `Microsoft-14941484` | `21.0.12.1+1-LTS` |
| Java 25 | `microsoft-25.0.4.1` | `Microsoft-14951867` | `25.0.4.1+1-LTS` |

## Minecraftサーバーの準備とワールド参加

- 根拠: human ownerの操作報告。Windows 11でPaper 1.21.11／26.2の両環境にMcRemote b10を導入し、ワールド参加まで確認完了。
- Paper exact build、McRemote JARのhash、各環境の起動Java、認証設定とLuckPermsの有無は未採取。
- Scratch Localの起動・接続・ペアリング・命令実行は、今回のサーバー準備完了報告には含まれない。

## 未確認の項目

- ZIPのOS標準展開の詳細、Smart App Controlの状態、firewallの個別の確認。
- 設定ページと接続先保存の詳細、認証ONでの接続完了、wire hello出力、独立WireScope。
- 再起動時の警告、設定保持、再接続。
- 1台構成とLAN構成それぞれの結果。
- Paperの実使用build、JARのhash、Paper起動時に使ったJavaの確認。

## Scratch Localの初回起動と接続の障害

- human ownerがWindows 11でランチャーを使い、警告なしで起動できたと報告。
- pair codeが発行され、認証された表示になるが、接続は完了しない。server startup logはcredential backendのsnapshot／authority_manifest欠如後の初期化失敗と`UNHEALTHY`を示す。sanitized logは`WINDOWS_CREDENTIAL_STARTUP_SANITIZED.txt`。
- human ownerがconfigの認証をOFFにすると、接続しhello worldを送信できたと報告。認証ONの検証を代替するPASSにはしない。
- 接続後に独立WireScopeへのリンクが出ない。固定ZIPを調べ、launcherのruntime configに`wirescope_url`が無く、WireScope appも未同梱と確認。3 OS ZIPとも同じ欠落。`LOCAL_WIRESCOPE_STATIC_INSPECTION.json`へ記録。
- 調査結果と担当別の次操作は`WINDOWS_ISSUES_HANDOFF_ja.md`。候補sourceとZIPは変更していない。
