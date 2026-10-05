# b9 dev live 素材の一覧

2026-10-05のclose分類で、Scratchのsegment 3の画面PNG 4枚（pickerの検索2枚、WireScopeの全体と列幅。列幅はhuman ownerが確認した画像）を追加で収容した。Scratch担当がtokenの省略とprivate address／player UUIDが出ていないことを目視で確かめている。

各担当の搬送素材（Git外のhandoff-materials）から収容した。収容した後に変えたのは、McRemote segment 0の`restart-result_ja.md`と`deployment-result.json`のhome directoryのpathを`~`へ置き換えた2 fileだけで、この2 fileは搬送元のMANIFESTのdigestと一致しない。

収容しなかったもの: Scratchの`private/`、`runtime/`、`artifacts/`（凍結artifactの本体。identityはrecordにある）、McRemoteの`__pycache__`。

| path | bytes | SHA-256 |
| --- | ---: | --- |
| `mcremote/segment-0/MANIFEST_ja.md` | 1555 | `8adf2ecda26517bf6e90805331c4409c8f9214d8a60eedd59d1c02d27c56ace2` |
| `mcremote/segment-0/materials/deployment-result.json` | 2614 | `c43b05d1066548495908be062efb50adb039ee6c89def1411527f544b1124a06` |
| `mcremote/segment-0/materials/restart-result_ja.md` | 5263 | `bae3e7bc448e7f501deac738733a6c9928a138526cfb9fb07a737d187088248f` |
| `mcremote/segment-0/materials/scratch-hello-observation.json` | 1663 | `347a9bf8f87d7ff6a57e9fb7a8e5a0a117c2497e66a3503b4f11183f6836eb34` |
| `mcremote/segment-0/materials/session-close_ja.md` | 2054 | `021ab9199daed351ec685be2cbd4f3499aeebca7f03e6da611d52ef8750436cd` |
| `mcremote/segment-1/MANIFEST_ja.md` | 2275 | `e36b453b8e347ef1985ef0b815e6bf53091c9e83969e7c385ef1be91108f4a7f` |
| `mcremote/segment-1/materials/attempt-1-expired/cleanup-summary.json` | 156 | `6475fdf11e3b891cac2740bc5edcd1982c8db384f97bbdb2e580598c19ea4383` |
| `mcremote/segment-1/materials/attempt-1-expired/live-auto.log` | 119 | `b863036f578016dc5a31d7cee1fe34a5638066bc025dd1eaa4c7854e51f70365` |
| `mcremote/segment-1/materials/attempt-1-expired/rpc-transcript.jsonl` | 75857 | `74f063e90cd30a052c611b7e6964022ab3ddbd621ed00f78e4bc733659704718` |
| `mcremote/segment-1/materials/cleanup-summary.json` | 160 | `d408a6345cfc8ea1b762ad926cf5b8f53ce1d0b8d023df34ad22c262249f2af2` |
| `mcremote/segment-1/materials/confirmation_ja.md` | 10425 | `e8de6bc6f5cdd51ab4c47d57f86f0b2baefdb463568eb759386caa3b7d76c0fa` |
| `mcremote/segment-1/materials/environment.json` | 787 | `909c7dbda8bd6c174e9c485b5bc07bda8c69e05d817fd7401700f6abbb9b7ebf` |
| `mcremote/segment-1/materials/live-auto.log` | 3199 | `84c03f7d74ddf2c7b7fe340b9bc06e5587c572e1e6c35d38d98c32611bee4b6a` |
| `mcremote/segment-1/materials/post-run-identity.json` | 174 | `22ed8464f1949b3bbfeca11dcd6d5cbcd203804bb0a6c7ff5f53f16deed7133c` |
| `mcremote/segment-1/materials/resume-state.json` | 1241 | `c121f1161c494d039205164a5594d7eefd02a6fb54dce45d839df7ba00ed75dc` |
| `mcremote/segment-1/materials/rpc-transcript.jsonl` | 431925 | `dc8b5f5c9260c6850f7bc11912dfdc0a27361608db015d8b2bf81ce45aa53b76` |
| `mcremote/segment-1/materials/run-summary.json` | 1148 | `730c8203e0ec4eccfbf5e8ca0a1d5dab0ad6ba33facfe11a50c2f58c87df2bc0` |
| `mcremote/segment-1/materials/run_with_transcript.py` | 10473 | `96299d693f479a5e6b04e2210b7eb06cf04a487555f32e1d95522ebd3e21dfd1` |
| `mcremote/segment-1/materials/session-close_ja.md` | 2041 | `4d23e3df1d427470518cf3f5563a7114ef781e459be5310ffca00e995a31612b` |
| `python/saved-token-check/MANIFEST_ja.md` | 1207 | `b6cd7fda93d4e881d6ba694fed1d84abf5c874cf1b968ff43ef6d03532bf3c9a` |
| `python/saved-token-check/materials/check_saved_token.py` | 5249 | `cb6ca3084c0bf0a1493ae566b4337c3826c712a2a2f6181cc37ea094ece2ade7` |
| `python/saved-token-check/materials/confirmation_ja.md` | 6912 | `1f7b654804787833efe9f8ac13bda96ca1d5cc4d0361c44f1881803ea8a5c874` |
| `python/saved-token-check/materials/result.json` | 986 | `31af3cae137368eee5e5476728e221bba7ad59ec805d5ae60c87987022ead70e` |
| `python/segment-2/MANIFEST_ja.md` | 1800 | `cf0221ea8164f7706c95db43950a33b1f5c0f0edf6e00a026790dc4ba7889bf8` |
| `python/segment-2/materials/confirmation_ja.md` | 7049 | `35dee1710d4b2f5d5672dbdb0cda7f6ac0e8cbe2c609267c913e3d9e347c293b` |
| `python/segment-2/materials/human-wirescope-observation_ja.md` | 2909 | `d26ee1b173146b89c5e7f8c0317ed66ad1b6a68c9e2732cf586fe6817f346a29` |
| `python/segment-2/materials/observer_snapshot.json` | 9513 | `ef4d0bdf2ed8fbb3919b1a8cfadfcc79a7c749517a19efd669befe4d84c042fe` |
| `python/segment-2/materials/result.json` | 2492 | `53f8b414f0a45df9932c3542d7e720faaebd12581e46aec1eee94decdb4767ea` |
| `python/segment-2/materials/run_segment2.py` | 9550 | `50d7c0d46186a2f534ff79ceb6e37578d876ae6e8b646a3789a58a28e9c7fd83` |
| `scratch/segment-3/INVENTORY.json` | 4363 | `12053910a2083975c37d7b698e3c6889d6f2258b9dbbc6a30535fe0fa8252437` |
| `scratch/segment-3/MANIFEST_ja.md` | 3222 | `34bcf2e9545cfe7fffc7a88e240536ce401d3ea37be693f44fdd0e3dcb74838a` |
| `scratch/segment-3/SHA256SUMS` | 2499 | `f96bfc942017222ffe8ae9486acc83bfaf63f6617e9847740fcd578b37471c29` |
| `scratch/segment-3/materials/CONFIRMATION_ja.md` | 10745 | `3972dffd5e1d988dd9bae07cc779903ce512933852838d22e18c383014123a13` |
| `scratch/segment-3/materials/check-representative-blocks.cjs` | 15893 | `6bbc1a0c0d6fa4ad9d67ac53f40e936d2d70d5a18f50771f7a606747983dc330` |
| `scratch/segment-3/materials/completion.json` | 228 | `916c850af1412f1d480c4266f46027e81d425e5d0b50ea688924593c128f4f93` |
| `scratch/segment-3/materials/finalize-browser-check.cjs` | 5413 | `9a2ffc31a2bd6d8c585096927061d7a8f22be6e5177a151b791a91211d5cdb6c` |
| `scratch/segment-3/materials/human-width-review.json` | 372 | `70d317a45c0a04ddf72b1748e9fcc9178155e846c081081e308ea2b319aa78d4` |
| `scratch/segment-3/materials/independent-browser-hello.json` | 256 | `5a0385f4506b6018be55d27a6e0105661072066767e33bbde8611f8eddbdc519` |
| `scratch/segment-3/materials/open-validation-browser.cjs` | 5308 | `05da0c82081e9039baf3dcd7376ecc346eb38608c9d1660b77c9e4b9d5ce64b6` |
| `scratch/segment-3/materials/picker-door.png` | 59644 | `dacaf7691205f693a9f1b5ecb271c3845d3b4c91e3a8e28fd1a47c25f56bd67c` |
| `scratch/segment-3/materials/picker-gold.png` | 59232 | `b687d991ab96f952180659e267863dd69e1fc049244047f883ea4c37cd7e1723` |
| `scratch/segment-3/materials/prepare-runtime.py` | 5718 | `b2d5451b7c38976e198b10e767f5b45caa3d51c0dca945d582390d51c9039c9a` |
| `scratch/segment-3/materials/readiness.json` | 409 | `08dab281e698acbe35ed12d2e6156d7eb897847c5d80829bf4513ba8cda94224` |
| `scratch/segment-3/materials/representative-results-display-check-failure.json` | 14875 | `e0c4bdc0cf834aeb694600bfeb95e170967f04f4c911f0b44e32a39c8878b134` |
| `scratch/segment-3/materials/representative-results-focus-failure.json` | 1324 | `6dc777af4dd54348bfc55d5c507f257ea35d27fd8d9f5c6f50c6dc2e37cdbddc` |
| `scratch/segment-3/materials/representative-results-harness-failure.json` | 2647 | `d6c2b3740570fa247bd4749eba636a2f6f08e6cb97590163bb60ef9f2f643213` |
| `scratch/segment-3/materials/representative-results.json` | 32487 | `df6d54de0ae78a7fc92564c40091796ff4481d05c82d11b19d41d67ae9f749c7` |
| `scratch/segment-3/materials/runtime-identity.json` | 368579 | `5dc05395aa13e2afa1b695de70471e247f25654163551f2568ad16ec64f1e803` |
| `scratch/segment-3/materials/user-b9-hello.json` | 1727 | `0cb866ebe745f9ad224a6274ce32384731a679c4dff58b5602f0866845d4e463` |
| `scratch/segment-3/materials/wirescope-b9-columns.png` | 162322 | `45906eefbd1a8418bb2241e2135f7010676aa8156d306c1bbc6f51a7721588e4` |
| `scratch/segment-3/materials/wirescope-b9.png` | 345206 | `f30946eff47e11b22c01136b4cdcb811b46bbcd2c3fe3272df1288e23c00c9eb` |
