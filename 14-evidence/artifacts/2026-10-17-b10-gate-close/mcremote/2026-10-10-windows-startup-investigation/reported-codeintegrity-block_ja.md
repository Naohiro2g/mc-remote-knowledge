# CodeIntegrityの拒否を確認（2026-10-10、human owner）

## 経緯の補足

最初はOFFで問題なく接続、途中で接続不可、現在はONでも問題なし。途中はSmart App Controlとメモリ整合性をOFFからONへ変更したと記憶しているが、変更直後という時系列の詳細は未確定。現在ONで成功した事実を保持する。常時ONで再現する問題とは扱わない。

## 提示イベント（private user pathを伏せた）

3077:
```text
Code Integrity determined that a process ([REDACTED_LOCAL_PATH] attempted to load [REDACTED_LOCAL_PATH] that did not meet the Enterprise signing level requirements or violated code integrity policy (Policy ID:{REDACTED_ID_003}).
```
3033: 同じjava.exeとSQLite3.53.4.0 DLLがEnterprise signing levelを満たさないとの通知。
3089: Signature information for another event. Match using the Correlation Id.

## 根拠から確定できること

- イベント3077は実ブロック。McRemote同梱SQLite3.53.4.0のtemp DLLのloadをCodeIntegrityが拒否した。
- Policy ID0283ac0f-fff1-49ae-ada1-8a933130cad6は、Microsoft公式Inbox App Control policiesのVerifiedAndReputableDesktopで、Smart App Control ONのpolicyに対応する。今回は拒否を出したpolicyをSmart App Controlと同定できる。
- 直前に提示されたsqlite.open→NativeLibraryNotFoundException→UNHEALTHY→hello credential_store_unavailableと整合する。イベント時刻・日付・Correlation IDをまだ採れていないので、正式な同一起動回bindingは次の確認。
- java.exeのpathはmise installs/java/21.0.2。フォルダー名と実runtime版は区別し、現在成功している回のjava実体と比較する。

## 未解決と次の最小確認

ONでも成功する現在との差は未解明。UI設定とpolicyの適用状態、JAR／DLL／Javaの実体、信用判定の状態等は比較候補であり、今回のイベントだけからどれかを原因と断定しない。

セキュリティ設定は現在のONを維持して、3077/3033/3089の詳細XMLをローカル保存する。3077のPolicyName／Status／SHA256FlatHash／System TimeCreated／Correlation ActivityID、3089の同ActivityID／TotalSignatureCount／PublisherName／VerificationErrorを照合する。現在の成功回のJAR SHA／java実体／実SQLite版／有効policyも採る。rawは実機ローカル、共有資料のprivate pathは伏せる。

Paper内蔵へ変更する評価では、同条件のSmart App Control ONで実際のPaper DLLをloadし、同梱DLLとの署名／hash／policy判定を比較する。依存版のWAL契約点検も別途必要。今回production codeやcandidateは変更していない。

## 公式資料

- [Inbox App Control policies](https://learn.microsoft.com/en-us/windows/security/application-security/application-control/app-control-for-business/operations/inbox-appcontrol-policies) Policy IDとの対応。
- [App Control debugging](https://learn.microsoft.com/en-us/windows/security/application-security/application-control/app-control-for-business/operations/appcontrol-debugging-and-troubleshooting) 3077/3089のフィールドとActivityID照合。
