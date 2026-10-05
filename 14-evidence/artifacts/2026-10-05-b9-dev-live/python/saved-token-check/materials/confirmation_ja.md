# b9 Python 接続確認票 — 保存tokenの期限切れで停止（2026-10-05）

## Release gate 確認票

- 対象 repo: `Naohiro2g/minecraft-remote-api`
- 対象 branch/commit: `codex/b9-python-contracts-pypi@b901c88fe41b67530ff353271683ece9fd453076`
- release / channel: 凍結candidate `2320.0.0b9`、protocol `23.2.0`。公開は実施していない
- gate coordinator: knowledge担当session（Claude Code）
- human release owner: プロジェクトオーナー
- current phase: 凍結後の実機試験。今回のPython接続確認は認証済みhelloの入口で停止
- contract maturity / required test tier: b9 API freeze。実施票のrequired tierはTier 3。今回実行したのは接続preflightと保存tokenのhelloだけ
- knowledge contract path: `00-hub/b9-gate-live-test-sheet_ja.md`（共通、segment 0の実token継続、segment 2の入口）、`00-hub/release-gate-notes_ja.md`（2026-10-04 b9節、凍結set）
- knowledge contract commit: `561de98b5c15864ac9b86cb6dcaeef1f20ce635b`（実読。remote mainのruntime marker区間とINDEXもこのSHAから読んだ）
- gate manifest identity: `b9-integrated-artifact-set-1`。knowledgeのgate節と統一実施票が示す凍結identityを使用。独立したgate manifest fileは受領していない
- change cone: 稼働するdev pluginへの保存tokenによる認証とhello identityの照合。世界を変える操作は含めていない
- reused PASS / rationale: 凍結wheelのCI・fixture・移管bytesの既存PASSをidentityの根拠として使用。今回の認証成功や代表往復のPASSへ置き換えていない
- exact compatibility set / freeze status: 凍結済み。未pushのworktreeや一時buildを実行環境へ差し込んでいない
- target deployment / profile / lock: devの通常環境。接続先は既存のlocal private profileを使用し、ユーザー指定のSSH aliasと一致することを確認。実addressはこの票へ収録しない
- authorized next action: human ownerの「dev通常環境をb9 pluginへ差し替え済み、接続チェック」と確認票作成依頼。実施票の停止ルールにより、認証失敗後の継続は行わず返却
- test class: `live-auto`
- 実行した command / 手順: 下記「実行」。frozen wheelを独立venvへ導入し、保存tokenを読むだけで`Minecraft.hello(token)`を1回実行
- 結果: TCP接続はPASS。認証済みhelloはFAIL、RPC code `-32000`／reason `token_expired`。再pairing・自動再試行なし。接続closeはPASS、token storeは実行前後でbyte一致
- evidence record / artifact: `result.json`（sanitized結果）、`check_saved_token.py`（実際に使ったrunner）、この確認票。正式record／artifactへの収容はknowledge側へ委ねる
- 未検証の境界: 認証済みhelloのprotocol／MC版、segment 2のpostToChat／pollEvents／entity／particle／sound、同梱WireScopeのreal-browser表示とhuman観測。稼働中JARの実SHA-256・Paper build・Java版・server logも今回のPython接続では照合していない
- security / compatibility / rollback の確認: token実値、pairing_id、private address、player UUIDを出力・搬送していない。debugはFalse。保存tokenを削除・更新していない。pairing、world変更、server設定変更なし。public source・wheel・同梱WireScopeのidentityは不変
- 判定を求める事項: `token_expired`を受けた保存token継続試験の扱いと、human owner参加の新規pairingから再開する指示。Python代表往復と横断gateの最終判定は主張しない

## 使用identity

| 対象 | identity |
| --- | --- |
| exact set | `b9-integrated-artifact-set-1` |
| Python source | `b901c88fe41b67530ff353271683ece9fd453076` |
| CI run／artifact | `37233244696`／`11314197935` |
| wheel | `minecraft_remote_api-2320.0.0b9-py3-none-any.whl` |
| wheel bytes／SHA-256 | 196,221／`e166bc9c14c425b3859f9af6c7af52900b58d1769fc077a3524a5368d05638c6` |
| installed package | `minecraft-remote-api==2320.0.0b9` |
| bundled WireScope source | `dc1ab834183e29f2eb03059b07e99d2b463776ee` |
| frozen pluginの指定identity | source `5cb33ebad4bf2c5e36c3433b0f70fe6070915b00`、JAR SHA-256 `4feb90dbdba8550cd16800cc3d384e42fed16a5c5e20faa489a0381ad2cda58e` |

human ownerはb9 pluginへ差し替えて起動済みと報告した。
上表のplugin identityはknowledgeにある指定値であり、Python側が稼働中JARを読み取って検証した値ではない。
wheelは本体のbytes／SHA-256を再照合し、isolated venv（Python 3.13.13）へインストールして実行した。

## 実行と観測

```bash
/tmp/mcr-b9-dev-hello-venv/bin/python \
  handoff-materials/2026-10-05-b9-dev-hello/materials/check_saved_token.py \
  --profile handoff-materials/2026-10-03-b8-dev-token-upgrade/materials/param_dev.py \
  --wheel /tmp/mcr-b9-python-final-ci/minecraft_remote_api-2320.0.0b9-py3-none-any.whl \
  --output handoff-materials/2026-10-05-b9-dev-hello/materials/result.json
```

private LAN接続が必要なため、承認されたsandbox外で実行した。
profileのhostがlocalの`ssh -G`で解決するユーザー指定aliasと一致し、portが指定値であることを確認。
そのprofileのhost／port用token store entryを読み込んだ。別環境のtokenへ切り替えていない。
`Minecraft.authenticate()`の期限切れtoken削除・pairing fallbackを通さず、`hello(token)`を直接呼んだ。

実行時刻: 2026-10-05 08:14:08 JST（2026-10-04 23:14:08 UTC）。

| 項目 | 結果 | 観測 |
| --- | --- | --- |
| frozen wheelの本体照合 | PASS | 上記bytes／SHA-256一致 |
| dev用保存tokenの存在 | PASS | token実値を表示せず確認 |
| devへのTCP接続 | PASS | 接続成功 |
| 保存tokenで認証済みhello | FAIL | code `-32000`、reason `token_expired` |
| 再pairingなしのtoken継続成功 | 未成立 | 期限切れにより認証を完了できなかった |
| helloのprotocol／MC版照合 | 未実施 | requestは`23.2.0`、成功resultを受領できていない |
| 接続close | PASS | 正常にclose |
| token store保持 | PASS | 実行前後でbyte一致 |
| segment 2の代表往復・WireScope確認 | 未実施 | 停止ルールに従い進めなかった |

返されたreasonは`token_expired`であり、今回の結果だけでb9 upgradeによるcredential破損・domain resetを断定しない。
serverがRPCに応答するところまでは確認できたが、認証済みの接続成功は確認できていない。

## 次の段階

coordinatorへ上記FAILとreasonを返し、新規pairingから再開する扱いを確認する。
再開時はhuman ownerがMinecraft内でpairingを承認し、認証済みhelloの`23.2.0`／`1.21.11`を照合してから、
別の実行としてsegment 2の代表往復とWireScope表示のhuman観測を行う。
