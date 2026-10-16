# macOS Scratch Local 起動・ペアリングの観測（2026-10-09）

- knowledge contract path: `00-hub/b10-gate-live-test-instructions_ja.md`、`00-hub/release-gate-notes_ja.md` b10。
- knowledge contract commit: `7d1b3809b0987f7fc0e5c5c2f365a42e9046e240`。
- 搬送元: McRemote session、source `main@8f76574e2185b5b502e186d15e4b553ad0912da0`（製品 source 変更なし）。
- test class: live-human。human owner の実機報告と添付画像。agent による実機操作ではない。
- 正式 evidence record/artifact path: 未採番・未配置。knowledge coordinator が authoring するための素材。

## human owner の報告

「macOS用だと、警告もなく起動、ペアリングも成功。WireScopeは無し。」

直前の起動失敗では `...mc-remote-scratch-local-2320.0.0b10-linux-x64/runtime/bin/node` を macOS で実行していた。OS のパッケージ取り違えとして説明し、Apple Silicon 向け macOS ZIP と `start-mc-remote.command` を案内した。その後の macOS 版での報告を、取り違え時の製品起動失敗から区別する。

## 添付画像で確認したこと

- Minecraft window のタイトルは `Minecraft 1.21.11`。
- ゲーム内チャットにペアリング成功（`Paired.`）の表示と `Hello, Minecraft!` がある。
- Scratch の WireScope mini は `OK 接続` を表示し、設定先／実接続先は loopback の `[REDACTED_ADDRESS]`。
- 独立 WireScope のリンクは写っていない。画像の表示範囲だけで全 UI のリンク不存在を証明するものではなく、リンク欠落は human owner の報告として記録する。WireScope mini 自体が無いという意味にはしない。

## 既存調査との対応

scratch-editor `handoff-materials/2026-10-09-b10-three-os-live/materials/WINDOWS_ISSUES_HANDOFF_ja.md` §2 は、固定 3 OS ZIP に独立 WireScope が同梱されず、runtime config に `wirescope_url` が無いことを静的に確認したと報告している。

今回の macOS 実機報告はその欠落と整合する。Windows だけの UI 現象とは扱わず、macOS でも欠落を報告された観測として Scratch 担当／coordinator へ返す。修正の着手や他 repo 変更はこの session で行っていない。

## 未採取と non-claim

- exact macOS version／build、CPU architecture、ブラウザ、Java vendor／exact version、Paper exact build、実使用 ZIP／JAR の SHA-256 は未採取。
- coordinator の実施票にある candidate identity と実使用 bytes の一致は、この画像／報告だけでは認定しない。
- 認証 ON の実施条件と画像のペアリング成功を区別する。実機 config の auth.enforcement 値／credential health log は未採取。
- 起動時の警告無しは human owner が試した今回の起動の報告。取得経路、隔離属性、初回警告の全経路を検証済みとはしない。
- LAN 接続、通常再起動後の接続、32768 setBlocks、独立 WireScope 実画面は未確認。
- Windows credential 初期化障害の原因確定・解消をこの macOS 報告から主張しない。
- 正式 evidence と gate 判定は knowledge coordinator に返す。
