# SQLite版の実機native load失敗（human owner追加報告）

2026-10-10の会話で提示されたlog。起動logの時刻は03:23:13〜03:23:21、対象日付と当時JAR SHAは未採取。

```text
[03:23:13] [Server thread/INFO]: [McR_CredentialService] Credential persistence backend: sqlite-wal-full
[03:23:14] [Server thread/ERROR]: [McR_CredentialService] Credential domain could not be trusted; operation=backend.load-state; operations=[backend.load-state -> sqlite.open]; cause_chain=[club.code2create.mcremote.CredentialDiagnostics$Failure -> club.code2create.mcremote.CredentialDiagnostics$Failure -> java.io.IOException -> java.sql.SQLException -> org.sqlite.NativeLibraryNotFoundException]
[03:23:14] [Server thread/INFO]: [McRemote] Credential domain health: UNHEALTHY (Credential domain could not be trusted; operation=backend.load-state; operations=[backend.load-state -> sqlite.open]; cause_chain=[club.code2create.mcremote.CredentialDiagnostics$Failure -> club.code2create.mcremote.CredentialDiagnostics$Failure -> java.io.IOException -> java.sql.SQLException -> org.sqlite.NativeLibraryNotFoundException])
[03:23:14] [Server thread/INFO]: [McRemote] Connection profile: [REDACTED_RUNTIME_SETTINGS]
[03:23:21] [Server thread/INFO]: [McRemote] Connection command queue capacity: [REDACTED_RUNTIME_SETTINGS]
[03:23:21] [Server thread/INFO]: [McRemote] Resource catalog ready: blocks=1166 entities=157 particles=115 bytes=170759 hash=6d0f8524b70e37fb8d7b34d0fdb45c2b058dcfea82920d86ca9aaabb9fcadc83
[03:23:21] [Server thread/INFO]: [McRemote] initializing FallbackPermissionManager
[03:23:21] [Server thread/INFO]: [McR_Permission] FallbackPermissionManager initialized with defaultBuildRange: [REDACTED_RUNTIME_SETTINGS]
[03:23:21] [Server thread/INFO]: [McRemote] Server started at port [REDACTED_PORT]
```

所有したlog中のPermissionManager instanceの非本質的なobject identityのみ省略。値の編集による意味の変更なし。

## 到達点

SQLite backend選択後、既存backend.load-stateからsqlite.openへ進んだ際、native libraryのloadを成立させられずUNHEALTHYになった。Paper／McRemoteの起動はその後も進みportの開始を記録しているので、全server process起動停止ではなくcredential機能の不可用が観測されている。

固定driver3.53.4.0のSQLiteJDBCLoaderは、DLLのJARからのtemp展開でIOExceptionを捕捉してfalseを返し、System.loadのUnsatisfiedLinkErrorも捕捉してfalseを返す。全探索で成功しなければNativeLibraryNotFoundExceptionを作る。したがって今回の末尾例外はDLL欠落だけでなく展開失敗・load拒否も含み得る。コードの詳細ログはSQLiteDriverBridgeがprivate pathを通常logへ出さないため当該threadだけ抑制している。元のUnsatisfiedLinkErrorやOS拒否コードはこのcause_chainでは分からない。

[固定上流source](https://github.com/xerial/sqlite-jdbc/blob/3.53.4.0/src/main/java/org/sqlite/SQLiteJDBCLoader.java)

## 次の最小調査

当該logの日付・JAR SHA・Java実体を固定し、その日の03:23:13〜03:23:21付近のCodeIntegrity/Operational（3077、関連3089、policy反映イベント）とDefender/Operational／保護履歴を読む。対象java process／DLLのfileと時刻が一致する拒否ならSAC等の手掛かりになる。メモリ整合性との因果は未確定。

再発時のみ、設定を固定したまま起動前からProcess Monitorで対象java PIDのnative DLL展開／Load Imageを採る。Windows側eventに根拠が無ければ、同梱固定driverのnative load probeを隔離したtemp／使い捨てDBで実施し、詳細は実機ローカル限定で採る。必要ならphaseとOS拒否理由を安全に出す診断改善を提案するが、今回の追記でproduction sourceは変更していない。

現在成功している同じJAR／Javaでの通常再起動後の再接続を既存実施票で確認する。今回のlogはDB内容の破損を示すものではなく、既存DBのreset／削除で調査しない。
