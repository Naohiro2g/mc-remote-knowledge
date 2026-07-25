# WoL相互live-human sanitized summary

## 状態

- observed at: 2026-07-25
- test class: `live-human`
- result: PASS
- subject: 異なるUbuntu desktop hardware 2台の相互WoL
- sender implementations: Python 3.12.3 / `wakeonlan 0.41`
- destination: 同一LANのdirected broadcast、UDP/9
- private host名、IP、MAC、SSH port、boot ID実値、absolute pathは除外済み

## matrix

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

hardware Aでは1 service、hardware Bでは独立した2 servicesが元のhealthy状態へ戻った。

## invalid trialと改善

hardware Bの最初のPython poweroff試行はstrict matrixから除外した。3回連続のSSH不能と
追加3秒後にpacketを送ったが、targetのmonitor / LEDではshutdownが継続しており、
packet送信後180秒以内に復帰しなかった。人間が完全消灯を確認してからPython packetを再送すると、
SSHと2 servicesは復帰した。

この観測により、poweroffでは「network / SSH停止」と「firmwareがWoLを受け取れる完全停止」を
同一視しない二段checkpointへ変更した。

1. checkerが3回連続の到達不能を確認する。
2. 人間がmonitor / KVM / LEDで完全消灯を確認する。
3. checkerへ明示confirmationを返してからpacketを送る。

二段checkpointでPython poweroffを再実行し、strict PASSを得た。続く`wakeonlan` poweroffも
同じcheckpointでPASSした。

confirmation入力の最初の実装は非TTY stdinがEOFとなりpacket送信前に停止した。
これはtarget / WoLのFAILではない。TTY付きcheckerへ修正し、packet未送信のまま停止したtargetは
既知Python packetで回復した。この試行もstrict matrixへ含めない。

## claim boundary

主張する:

- 上記2台、同一LAN、directed broadcast、Python / `wakeonlan`
- tested deep sleep / poweroffからの復帰
- deep sleepのboot ID維持、poweroffのboot ID更新
- SSHと既存service healthの復帰

主張しない:

- macOS、OS差、package version差
- WoWLAN、hibernate、hybrid sleep
- router越え、USB Wi-Fi / Ethernet、Wi-Fi-to-Ethernet bridge
- 停電復旧、watchdog、OS hang、backup / restore
- WoLを一般bootstrap、profile capability、compatibility条件、release gateにすること

## evidence boundary

本summaryとcheckerはgitignored handoff素材であり、正式evidenceではない。正式採用時はknowledge ownerが
内容とredactionをreviewし、`14-evidence/records/`と`14-evidence/artifacts/`をauthoringする。
