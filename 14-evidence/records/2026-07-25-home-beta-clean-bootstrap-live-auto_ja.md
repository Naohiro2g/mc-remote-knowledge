# home-beta clean bootstrap live-auto evidence

## Record

- test ID: `2026-07-25-home-beta-clean-bootstrap-live-auto`
- test class: `live-auto`
- result: PASS
- observed at: `2026-07-24T22:26:04Z`
- source repository: `Naohiro2g/mc-remote-stack`
- source checkout: `e63f27dd2d68e2ffc86d47c154e07db18a9d2e26`
- tested implementation commit: `3589d3537c234addaa3f709662d78828f5866f50`
- knowledge contract commit: `f1b99a049b6bc57799c3356c3e54d29e45031451`
- axes: `deployment`、`server-runtime`、`protocol`、`ux`

`e63f27d`はテスト済み実装`3589d35`へ公開NOTESだけを追加したcommitであり、runtime code、
profile、preset、artifact identityは同一である。

## 用語上の位置づけ

本 record は**ケータリング型**（`2026-07-25-03` / `2026-07-25-04`）による構築の実証である。
対象 host 上に**準備済み deployment**（resolve ・ fetch ・ render 済みの論理状態）が成立し、
isolated で apply ・ doctor まで到達したことを示す。

**ケータリングキットの実証ではない**。本 subject は home 構成であり、AP ・ DHCP ・ DNS ・ NAT を
含む `classroom-all-in-one` ではなく `home-server@2` profile を使っている。AP topology を含む
キット構成の検証は教室構成で別途行う。

本節は語の対応を明示するだけで、以下の Subject ・ Scope items ・ 未検証の境界が主張する範囲を
広げも狭めもしない。

## Subject

- profile: `home-server@2`
- profile SHA-256:
  `a59b8ac2bf4148256ee6f45884a6a47b11d8c890043603f180149e873722e63c`
- preset: `mcremote-paper@1`
- preset SHA-256:
  `ac6716635424dd1a13d99e4250e51969b3a7d34db4f9d17466a1db102db87c27`
- component set SHA-256:
  `96e2f2291c9dbdd70e4cb6471d6dbef82a02eec5799f45593f86b958523e0166`
- protocol: `21.0.0`
- Minecraft: `1.21.11`
- Paper: `1.21.11-132`
- McRemote package: `2100.0.0b2`
- Minecraft image:
  `docker.io/itzg/minecraft-server:2026.7.2-java21@sha256:7f69fd6688e03495c8a8f5a46e8a8e82001b4465f4b55bdcd024c02c3624d8c8`
- Paper JAR SHA-256:
  `5ffef465eeeb5f2a3c23a24419d97c51afd7dbb4923ff42df9a3f58bba1ccfba`
- McRemote JAR SHA-256:
  `ad2674fa93645cc3c4c0d2b6aa5b37f11a8f9519162f61ac00b8be7122b023c7`

## Scope items and claims

| Scope item / claim | Constraint | Observation | Result |
| --- | --- | --- | --- |
| clean bootstrap | Ubuntu Server 24.04 amd64、既存container / volume / imageなし | target上205 tests / Ruff、exact fetch、canonical render、review済みlockで初回apply | PASS |
| `profile-render` | exact subject、`compose@1`、presetが許可する`beta / integration`、profileが許可する`isolated / lan-only` | isolatedはcanonical render、初回apply、doctorまで確認。lan-onlyは同じ実artifactで別の一時projectをresolve / fetch / render / validateし、RFC 1918 bindをComposeへ投影することを確認（applyなし） | PASS |
| `protocol-hello` | protocol `21.0.0`、Minecraft `1.21.11`、tokenなしhello | doctorがprotocol / Minecraft targetとhello応答を確認。対象環境は`auth=not-required` | PASS |
| agent-assisted UX | 管理端末上agent + SSH。privileged / agreement / mutation checkpointは人間へ戻す | SSH hardening、package導入、EULA、unverified理由、plan / lock review、applyを人間が承認 | PASS |

## Sanitized artifacts

- `../artifacts/2026-07-25-home-beta-clean-bootstrap-live-auto/bootstrap-transcript.txt`
  - SHA-256:
    `53ce3b6975e6ac79c343c8f09b71082184e75c14626baf5b79e4c924ca99af3a`
- `../artifacts/2026-07-25-home-beta-clean-bootstrap-live-auto/doctor-transcript.txt`
  - SHA-256:
    `44e5af9e1a5821a12dcc0cdc059a1f47020c6027c324078dfe95aee0785635fa`
- `../artifacts/2026-07-25-home-beta-clean-bootstrap-live-auto/lan-only-render-transcript.txt`
  - SHA-256:
    `b4f937debc325f7642b993f1bf82de2aa7c5b12f749d8fd204968b332a5eb3c7`

transcriptはprivate host名、IP、MAC address、SSH alias、OS user名、home / project absolute pathを
除去した。uptimeはcompatibility claimに影響しないため`healthy`へ正規化した。lock identity、
artifact digest、loopback address、公開component versionは主張を束縛する非secret値として保持した。
lan-only renderの実private IPv4とtest portは意味を保持するplaceholderへ置換した。token、pair code、
player UUID、生container logは取得していない。

## Human checkpoints

人間はtarget、固定IPv4、SSH hardening、toolchain導入、Minecraft EULA、unverified理由、
planに表示されたlock / artifact / volume / world / bind port、bootstrap applyを個別に確認した。
agentは反復可能なpreflight、取得、生成、test、apply、doctorと差分整理を担当した。
追加のlan-only検証は一時projectに限定し、applyもDocker操作も行っていない。

## 未検証の境界

- pairing、authorization、LuckPerms
- token必須時のhello
- hello以外のprotocol commandと実player操作
- backup / restore
- upgrade / rollback
- lan-only runtimeの起動・到達性・host firewallとの責任分界
- public exposure（profileの許可範囲外）
- 複数deployment projectのhost-level transaction
- 対象host上agentの限定実験

本recordは上記subjectに対し、許可された2 exposureの`profile-render`と、isolated runtimeにおける
tokenなし`protocol-hello`のcoverageを支える。lan-onlyで生成したruntimeの安全性、production
readiness、認証全体、復旧可能性、公開networkの安全性は主張しない。
