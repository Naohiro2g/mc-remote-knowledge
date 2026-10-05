# b9契約fixture（確定搬送素材）

- 初回発行: scratch-editor@62e46fd156a55c57794227d370a72f3558aa43d8、`mc-remote/protocol/test/fixtures/chat-event-compat-v23.2.json`
- 移管後: minecraft-remote-tooling@dc1ab834183e29f2eb03059b07e99d2b463776ee、`packages/protocol/test/fixtures/chat-event-compat-v23.2.json`
- schema: `mcremote.chat-event-compat.v23.2`
- bytes: 32382
- SHA-256: `670b0a86df1956c0e44c6986a0a2598caab32c7328804f9c703190e62e9dd727`
- case数: 33（chat.post 7、event batch 22、stateful rejection 4）。case IDは重複しない。
- knowledge契約: 900f6f4b8027d265a62ba7f139d4f3b1bbe78100、wire §4／§5.4、DEC 2026-10-03-01／02。

`chat_post.cases`はid付き成功のnull受理と非null拒否。notificationの無応答とerrorの維持は、このresult形検査fixtureの範囲外。

`event_batches.cases`は混在、未知のみ、末尾が未知、through/cursor進行、loss counters、共通fieldの不正、順序、既知payloadの拒否を含む。`expected_client`はlearner eventsとcursor/status/lossDelta、`expected_observer`は未知を共通fieldだけにしたpoll result。

`event_batches.stateful_rejections`は既存cursorと前回statusがある場合の拒否。WireScopeの単独snapshot形検査へそのまま適用するcaseではない。`future_event`等は将来typeの互換性を検査する仮の値で、新APIや実際のserver eventを追加するものではない。

公開b8の12件を変更せずに追加した。移管先とScratchの取得キャッシュは元のbytesに一致する。McRemote／Pythonのconsumer取り込みは各担当の範囲で、Scratch担当は実施していない。
