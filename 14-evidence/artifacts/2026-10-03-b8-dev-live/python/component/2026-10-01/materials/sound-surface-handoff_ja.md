## 確定搬送票

- 搬送元 repo: minecraft-remote-api
- 搬送元 surface: Codex
- 搬送元 branch/commit: codex/b8-python-entity-particle@52d35f5304e62f465c1f47ab47c00fe9bcf62470
- 作成日: 2026-10-01
- 種別: 局所決定
- 決定: PythonのplaySound／playBlockSoundはvolume・pitch・note・receiverをkeyword-onlyで受ける。volume／pitch／noteの既定はNone、receiverはworld。Noneはその項目の省略としてwireへnullを送らない。pitchとnoteの両指定は送信前にValueError。どちらも無ければserver既定（通常音1.0、blockはSoundGroup）を保持。note=0・volume=0を省略しない。音名の換算はユーザーコード。
- 理由: 引数名と型補完で意味が分かる。pitch=1.0をsignature既定にすると、省略と明示指定を区別できずnoteの指定を潰す。両指定を明示エラーにすればnoteを黙って捨てない。block固有の既定値を保持する。
- 却下案（3件まで）: pitch優先でnoteを捨てる／pitch=1.0をsignature既定にする／options dictを第5位置引数で受ける旧candidate surface。
- 影響: Pythonの公開surfaceと利用例。wireのshape・数値policy・protocol版は不変。旧candidateの第5位置dictはTypeError。dict変数は**controlsで渡せる。
- 根拠/検証: user 2026-10-01「オッケー、では提案の形に変更してください」。knowledge fd29db7 wire §5.8.3、4f0b46f sound-extension-notes §3.3。tests/test_b8_surface.py・test_b8_fixture.py（keyword・0・None・排他・fixture projection）、unit/deterministic全685 PASS、B8対象432 PASS。shared fixtureは111case、consumer143 tests。CI Python3.10〜3.13全success。
- 既に変更した実装/文書: mc_remote/minecraft.py、sound_value.py、docs/b8-python_ja.md、test_b8_surface.py、test_b8_fixture.py。
- ナレッジ着地希望: 12-python-clientの利用面／sound-extension-notes §3.3へPython surfaceの省略・排他の説明を必要に応じて反映。wireへPythonのNoneの規則を混ぜない。
- 捕捉 cleanup: local NOTESの未確定・未実装2行は本実装のidentityへ更新。knowledge反映後に着地確認を戻す。
- 着地後の確認戻り先: このPython担当session。
