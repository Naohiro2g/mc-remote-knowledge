# 使用fileのidentity

Paperと本体plugin 10本は以下の全11 JARです。byte/SHAは試験に配置した実物を計測しました。

| file | bytes | SHA-256 |
| --- | ---: | --- |
| `paper-26.3-244.jar` | 55,279,049 | `9601f9a26a2a52a0f2c807cf1abf691f96ee4fb287878313b601cebc2c51eabf` |
| `DiscordSRV-Build-1.30.5.jar` | 10,653,915 | `ef2fa1f2eb146c7c77412b7190a7dd33f1fc91282683fe45407739554c8aefef` |
| `Geyser-Spigot.jar` | 52,208,355 | `71c9ebd88fb729ff8dd881de5846a1cea04eb4ce89dc1004e67002d8a5077e4c` |
| `LuckPerms-Bukkit-5.5.91.jar` | 1,509,565 | `2a6834c51830b133ec8763703391b20240f7a3b4748746503251a45d70cf1b39` |
| `ServerBackup-2.10.0.jar` | 9,806,864 | `961e77895a31980b129307f14081231b6b12e84f064a8b74765478d526d4fc1e` |
| `ViaBackwards-5.12.2.jar` | 1,439,642 | `9a148a80ea22074f4bd1626cdbe254a4cd998bf44e7ceaff4e285a1b6b35da42` |
| `ViaVersion-5.12.2.jar` | 6,508,813 | `24e4876fefe73e08a4c87cd6c457ee0916e62dd69656631caf41e26f909d504b` |
| `advanced-portals-2.8.0-spigot.jar` | 3,221,235 | `abd3e4be48c1f34bc60530aaa344ab8bffd4146281b8ad33fc83628c93e7287d` |
| `floodgate-spigot.jar` | 11,561,096 | `21570aff9ce17d6983928e8552777760e1ede5050026b04c686b0ae112e6fd7e` |
| `mc-remote-2321.1.0.jar` | 340,193 | `cd1fff723b2b8349f45184b940cd5da1ca3cdcacc9bad988fa71cd00ea960112` |
| `worldedit-bukkit-7.4.6.jar` | 7,870,216 | `e0ce67d870ad1fef8a40dd9d7926360caf3bb44722438545d6b20b55f82a0c91` |

試験用probeは本体plugin集合から分け、初回の10本構成の起動後に追加してping・dimension・有効化を調べました。

| 試験file | bytes | SHA-256 |
| --- | ---: | --- |
| `probe/StackGateProbe.jar` | 4,705 | `f3ae497bbfea44c54ba3e75ca9f6370e3e98829b147d9b2b63501766bce5abeb` |
| `probe/StackGateProbe.java` | 2,449 | `efa23bf808058bad72c2d7fddadca4b3171e076ce9c526cb63fc3f387f7d38e0` |
| `probe/baseline_checks.py` | 2,569 | `dc2963d3c7907918d0c789ab6220e7ccf0ec7df10fe2770b3af9ab74484bc272` |
| `probe/finish_trial.py` | 3,709 | `9f5dc6fd5f3285f97885febf7d1987b3e6af14565f5cd3d6961110a698af38b1` |
| `probe/prepare_isolated.py` | 3,038 | `552634d045f62c0e368b808f3512338b3710bc83f2e705f459626ec6473ed1ad` |
| `probe/restart_trial.py` | 2,079 | `98164c0bbc3020ac61f3b41fd9f14844e2d7ebc42babbf0f6972ccb9936825c0` |
| `probe/start_trial.py` | 3,098 | `12d299519af0583b980b9506aa0eac020fd2627f2ce6101dafad61675f592865` |

元backupは939,102,968 bytes、SHA-256 `31a5da45fa45e374303c0ecdcdbb2cc18c243f25018c586e2b81b21919c0e6f2`。公開VPS側の実物とコピー側で一致しました。中身はprivateに保持します。

McRemote configの入力は1,169 bytes、SHA-256 `a6c2cd042f648fb4330bbed161c282bb91fad7bede2db2a429f02aba1866ec59`。完成済みbackupと現行configの内容一致を確認しました。補完後は1,676 bytes、SHA-256 `5177aeccf798497d03852839ccb507d4da6ace99b200229874ba0d41093f24d8`です。

runtime imageは`ghcr.io/naohiro2g/mc-remote-paper-runtime-temurin@sha256:69b73187717bf509fa30937b4e4c202dddf18e523cc9668dcf31dd62851a66f0`。OCIなので個別JARのような単一fileのbytesではなくdigestで固定しました。

Geyserは公式APIのSpigot用SHA-256と実物を照合。LuckPermsは公式build 1678のdownloadから実物のSHA-256を計測しました。公式metadataに独立した期待SHAの記載はなく、その照合は主張しません。
