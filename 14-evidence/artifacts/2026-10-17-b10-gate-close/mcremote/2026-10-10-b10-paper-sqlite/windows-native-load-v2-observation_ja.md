# Windows実機 DLL比較 v2：受領した観測

- 受領日：2026-10-10。
- 観測主体：human owner／Windows実機担当。McRemote側担当は以下の報告を受領した。rawログを直接読んでの再判定はしていない。
- 発行素材：`../../2026-10-10-windows-startup-investigation/materials/windows-native-load-comparison-v2.zip`。
- ZIP：1,591,401 bytes、SHA-256 `f4540828875413f72f09b6f5cc53ca212b9e9b536ea6eec8730be1e38acf0eed`。

## 実行条件と結果

Windows 11 x64、JVM amd64。通常WindowsユーザーのBashから、miseのOpenJDK 21.0.2と25.0.2の絶対パスを固定した。
各Javaについて両DLLを各1回、別JVMで実行。事前にJavaプロセスが無いことを確認したとの報告。

| Java | DLL | JVM時刻（2026-10-10 JST） | JVM PID | 結果 | exit |
|---|---|---|---:|---|---:|
| OpenJDK 21.0.2+13-58 | McRemote同梱版 3.53.4.0 | 15:00:53.8343155 | 17220 | PASS | 0 |
| OpenJDK 21.0.2+13-58 | Paper版 3.49.1.0 | 15:00:54.3855599 | 13736 | PASS | 0 |
| OpenJDK 25.0.2+10-69 | McRemote同梱版 3.53.4.0 | 15:04:13.8428498 | 15464 | PASS | 0 |
| OpenJDK 25.0.2+10-69 | Paper版 3.49.1.0 | 15:04:14.3820357 | 12080 | PASS | 0 |

- Smart App Control：`VerifiedAndReputablePolicyState=1`。メモリ整合性：`Enabled=1`。
- `SHA256SUMS`全15件が一致。各probeでもDLLと同版のJavaクラスJARを照合し、`CLASSPATH_READY`から`system-load`へ進んだ。
- 全4件でOSロードとJNI初期化が成功。例外なし、`db_opened=false`。
- Java 21のstderrは空。Java 25.0.2は`System.load`に対するnative-access警告のみ。警告を抑える設定・起動オプションは使っていない。
- 失敗が無いためCodeIntegrity 3077／3089照会は実施していない。該当イベントが存在しないと確認した意味ではない。
- セキュリティ設定・既存DB・既存JARは変更していない。Java選択のためユーザーが診断素材v2のmise設定を更新した。

## 比較対象のSHA-256

| 対象 | SHA-256 |
|---|---|
| 3.53.4.0 native | `f16882d2eded914edd1e1d313e7c8579e040b0da090a52ea99ad7b0c5d961c45` |
| 3.53.4.0 JavaクラスJAR | `0ee2eca3b6bfb8f30a19d15b11e7502d2b8fc74088115a50a1cb0484978383bc` |
| 3.49.1.0 native | `91990dddfdc41d3c06a97bb22222a796255c215f31a738c6e5fb4c2cedb41b18` |
| 3.49.1.0 JavaクラスJAR | `e189577fee9ecb0b44d1be5027795269a2c95b769098cf54a66586cea150b7bf` |

上のJavaクラスJARは診断用に上流の全class bytesを保持してnative resourcesを除いたもの。Paper本体の配布JARのSHA-256とは区別する。

## 範囲と限界

現在の条件で両Java・両DLLのロードとJNI初期化が成功し、過去のDLL拒否を再現しなかったという観測である。
DB処理、WAL-reset、Paper plugin classloader、通常Paper起動全体の成功は検証範囲に含まれない。
過去のSACによる拒否の証拠は別途保持し、過去の拒否理由と現在の成功理由の差は断定しない。
Paper同梱版への依存変更がSAC問題を解消すると主張しない。

初回v1の`NoClassDefFoundError`は診断素材のJavaクラス不足であり、OS拒否やDLL採否の材料にしない。
PowerShellでのOracle Java 25.0.4.1実行も両DLL PASSだったとの報告があるが、上表とは独立した観測である。

## 実機ローカル根拠

- `results-bash-20261010-150052-2182/`（Java 21.0.2）。
- `results-bash-20261010-150412-2219/`（Java 25.0.2）。
- rawログとprobe用temp DLLは実機ローカルで保持。この素材にはユーザー名・マシン名・ユーザーパスを収録しない。

正式evidenceへ昇格する場合はknowledge担当が必要なsanitized artifactを実機担当から受け取る。
