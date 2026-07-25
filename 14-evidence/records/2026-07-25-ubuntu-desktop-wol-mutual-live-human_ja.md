# Ubuntu desktop 2台 WoL 相互 live-human evidence

## Record

- test ID: `2026-07-25-ubuntu-desktop-wol-mutual-live-human`
- test class: `live-human`
- result: PASS（strict matrix 8 cases）
- observed at: 2026-07-25
- source repository: `Naohiro2g/mc-remote-stack`
- source branch: `main`
- source base commit: `6ef817ed7621f2af8f1a30d84b1f26c45ad19163`
- knowledge contract commit: `44017c2905363fb0c41f3142443e4b36efa7eb21`
- handoff ID: `2026-07-25-wol-optional-operation`
- axes: `deployment`、`server-runtime`、`human`、`ux`

検証時の field note、checker、sanitized summary は source base commit 後の gitignored / uncommitted
handoff 素材であり、source commit の tracked tree には含まれない。本 record は handoff manifest と
各素材の SHA-256 を照合し、public knowledge の claim と redaction boundary を knowledge owner が
再 authoring した正式 evidence である。

## Subject

- target / sender: 異なる Ubuntu desktop hardware 2台を同一 LAN 上で相互利用
- sender implementations: Python 3.12.3 / `wakeonlan 0.41`
- destination: target subnet の directed broadcast、UDP/9
- tested power states: deep sleep / poweroff
- recovery observations: SSH、boot ID、既存 service health
- hardware A: 既存1 service
- hardware B: 独立した既存2 services

hardware A / B は public record 上の pseudonym である。private host名、IP、MAC、SSH port、
boot ID 実値、absolute path、exact private inventory は本 record と artifact に含めない。
したがって本 record から特定 hardware の compatibility entry を作らず、上記2台での
hardware-specific field report としてだけ扱う。

McRemote protocol / package の互換性は本検証の subject ではない。

## Scope items and claims

| Scope item / claim | Constraint | Observation | Result |
| --- | --- | --- | --- |
| sender parity | 同じ target、directed broadcast、UDP/9、power state で Python と `wakeonlan` を比較 | 両 sender implementations が2台・2 power statesで復帰を成立させた | PASS |
| deep sleep recovery | 2方向 × 2 sender implementations、packet前に複数回の到達不能と自然復帰しないことを確認 | 4 casesでSSH・service healthが復帰し、boot IDを維持 | PASS |
| poweroff recovery | 2方向 × 2 sender implementations、人間がmonitor / LEDで完全消灯を確認後にpacket送信 | 4 strict casesでSSH・service healthが復帰し、boot IDを更新 | PASS |
| service recovery | packet送信前に既存service数とhealthを確認 | hardware Aの1 service、hardware Bの独立した2 servicesが元のhealthy状態へ復帰 | PASS |
| poweroff checkpoint | checkerの3回連続到達不能と、人間の完全消灯確認を分離 | network / SSH停止が完全poweroffより先行する観測を受け、二段checkpointへ変更後にstrict PASS | PASS |

## Strict matrix

| target | sender | method | power state | SSH復帰 | service health復帰 | boot ID | result |
| --- | --- | --- | --- | ---: | ---: | --- | --- |
| hardware A | hardware B | Python | deep sleep | 11秒 | 13秒 | 維持 | PASS |
| hardware A | hardware B | `wakeonlan` | deep sleep | 10秒 | 11秒 | 維持 | PASS |
| hardware A | hardware B | Python | poweroff | 28秒 | 57秒 | 更新 | PASS |
| hardware A | hardware B | `wakeonlan` | poweroff | 27秒 | 57秒 | 更新 | PASS |
| hardware B | hardware A | Python | deep sleep | 8秒 | 9秒 | 維持 | PASS |
| hardware B | hardware A | `wakeonlan` | deep sleep | 8秒 | 9秒 | 維持 | PASS |
| hardware B | hardware A | Python | poweroff | 32秒 | 55秒 | 更新 | PASS |
| hardware B | hardware A | `wakeonlan` | poweroff | 29秒 | 52秒 | 更新 | PASS |

復帰秒数は packet 送信からの観測値である。

## Invalid trials and method correction

hardware B の最初の Python poweroff 試行は strict matrix から除外した。3回連続の SSH 不能と
追加3秒後に packet を送ったが、target の monitor / LED では shutdown が継続しており、
packet 送信後180秒以内に復帰しなかった。人間が完全消灯を確認してから Python packet を再送すると、
SSH と2 services は復帰した。

この観測により、poweroff の checkpoint を次へ変更した。

1. checker が3回連続の到達不能を確認する。
2. 人間が monitor / KVM / LED で完全消灯を確認する。
3. checker へ明示 confirmation を返してから packet を送る。

二段 checkpoint で Python poweroff を再実行し、strict PASS を得た。続く `wakeonlan` poweroff も
同じ checkpoint で PASS した。

confirmation 入力の最初の実装は非 TTY stdin が EOF となり packet 送信前に停止した。
これは target / WoL の FAIL ではない。TTY 付き checker へ修正し、packet 未送信のまま停止した
target は既知 Python packet で回復した。この試行も strict matrix へ含めない。

## Sanitized artifacts

- `../artifacts/2026-07-25-ubuntu-desktop-wol-mutual-live-human/wol-mutual-live-human-summary_ja.md`
  - SHA-256:
    `d3ba72984419080ad87f70f2c214c1bea6c6aa6dddf8ccc8af99bb8ff6173557`
- `../artifacts/2026-07-25-ubuntu-desktop-wol-mutual-live-human/run-wol-case.sh`
  - SHA-256:
    `64e8644493e22109a40c59fb599571ca0f47cde887e2f67ea995cd3f11413d63`

summary は source handoff の sanitized observation を verbatim で保持する。checker は検証時点の
method snapshot であり、標準 bootstrap、normative runbook、保守対象の operator tool ではない。
checker は private MAC を既存 local alias から実行時に解決し、MAC と broadcast address を
summary 出力で redact する。artifact 内に private alias の名前や解決値は含まれない。

raw terminal history は正式 artifact として受領していない。knowledge owner は handoff manifest の
記載と各素材の SHA-256 が一致すること、summary と checker に MAC、private IP、private host名、
SSH port、boot ID 実値、absolute path が固定値として含まれないことを確認した。

## Human checkpoints

人間は sender / target と power state を確認し、poweroff では monitor / LED による完全消灯確認後に
checker へ明示 confirmation を返した。checker は default LAN interface と subnet の directed
broadcast、packet 前の boot ID と service health、3回連続の到達不能、packet 後の SSH、boot ID、
元の service 数と health を検査した。

常に sender 1台と別の物理回復経路を残し、2台を同時に停止していない。

## Claim boundary

本 record が主張する範囲は次に限る。

- 上記2台、同一 LAN、directed broadcast、Python / `wakeonlan`
- tested deep sleep / poweroff からの復帰
- deep sleep の boot ID 維持、poweroff の boot ID 更新
- SSH と既存 service health の復帰
- poweroff で network / SSH 停止と完全消灯を分ける checkpoint の必要性

次は未確認であり、本 record は主張しない。

- macOS、OS差、package version差
- WoWLAN、hibernate、hybrid sleep
- router越え、USB Wi-Fi / Ethernet、Wi-Fi-to-Ethernet bridge
- 停電復旧、watchdog、OS hang、backup / restore
- WoL を一般 bootstrap、profile capability、compatibility 条件、release / b3 開始 gate にすること
- McRemote protocol / package の compatibility または production readiness

本 evidence は、WoL を準24時間運用で重要な optional operator 機能として扱うこと、sender
implementation と power state を分けて観測すること、poweroff に人間の完全消灯 checkpoint を
置くことを支える。特定 hardware の互換性や一般環境での remote 復帰保証は支えない。
