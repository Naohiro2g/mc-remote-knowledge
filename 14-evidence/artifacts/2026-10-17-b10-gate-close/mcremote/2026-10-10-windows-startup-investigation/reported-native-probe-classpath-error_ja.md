# v1診断素材のclasspath不足 — Windows側担当の戻り

- 受領日: 2026-10-10
- 報告元: human ownerを経由したWindows側Codexの診断
- 対象: `windows-native-load-comparison.zip`（1129856 bytes、SHA-256 `a1b090b0245a5a3a79811e2634c85280d0c27f1f573cdc9813ba77bc342c5a11`）
- 報告: 両DLLともJNI初期化が `org.sqlite.core.NativeDB` を要求するが、v1 READMEの `-cp .` にはSQLite JDBCのJavaクラス群がなく `NoClassDefFoundError`。Windows policyによる拒否の証拠ではなく、初期化未完了のためPASSにもできない。
- 原因: McRemote担当がDLLだけでOS loadを比較できるとして素材を作った際の前提不足。v1で行ったcompile／help確認ではJNI初期化を確認していなかった。
- 検証: 上流JNI_OnLoadのNativeDB／Function／Collation等の参照、元JARの全class、v1ソース・classpathと整合。実機のrawログ／時刻／PID／Java identityは今回の戻りには未添付。
- 対応: v1を比較の成功・policy拒否判断に使わず、版を揃えたJavaクラスを同梱する独立v2へ修正。v1の素材とidentityは経緯の参照として保持する。
- この戻りは、過去に3077／3089で確認したMcRemoteのDLL拒否の証拠を取り消さない。今回の診断素材のエラーと、その起動時の拒否は別の事実。
- 分類②: Windows側Codex／human owner／knowledge coordinator／McRemote担当へ移管。修正素材の返却・観測の着地照合後に閉じる。
