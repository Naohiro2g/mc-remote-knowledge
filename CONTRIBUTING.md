# Contributing

Issue と Pull Request を歓迎します。archive や private backstage へのアクセスは不要です。

## 基本の流れ

1. 大きな設計変更は、先に Issue で目的・理由・却下候補を共有する。
2. fork から小さな PR を作る。変更した文書と、その判断が影響する範囲を明記する。
3. 文書変更では結論だけでなく「なぜ」と、比較した案を残す。
4. protocol や複数スポークへ波及する変更は `00-hub/DECISIONS_ja.md` の対象とする。
5. 秘密の実値、private inventory、未公開の脆弱性情報を Issue / PR へ載せない。

設計、命名、public/private 境界の変更は human review を gate とします。maintainer は合意済みの機械的変更を direct-main できます。default branch の force push と削除は行いません。

## ライセンス

Contribution は、明示的な別合意がない限り、変更対象と同じライセンスで提供されます。文書・図・教育資料は CC BY-SA 4.0、独立コード・tool は MIT です。初期運営では CLA / DCO を要求しません。

## Security

security-sensitive な内容は public Issue に書かず、[SECURITY.md](SECURITY.md) の経路を使ってください。
