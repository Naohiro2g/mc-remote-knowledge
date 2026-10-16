# b10 pre-releaseの3 OS試験（2026-10-14〜17）

> test class: `live-human`。実施票`00-hub/b10-gate-live-test-instructions_ja.md`（2026-10-14版）による。human ownerが送った画面、
> log、文字をcoordinatorが要約した。token、ペアコード、IPアドレス、ホスト名、player名とUUID、WireScopeの表示ID、アカウント名は
> 収録しない。素材はGit外。2026-10-16〜17はcoordinatorが進行を案内しながら行った。

## identity

- 取得はpre-release `v2320.0.0b10`のassetから、ブラウザで（Scratch LANパッケージ）。ZIPのbytesは3 OSとも期待値と一致
  （Windows 261,590,008、macOS 265,941,672、Linux 271,197,726）。assetのSHA-256はcoordinatorが2026-10-14にGitHub APIで照合済み
  （`00-hub/release-gate-notes_ja.md` b10）
- McRemote `mc-remote-2320.0.0b10.jar`はpre-releaseのassetから。全サーバーの起動logで`Enabling McRemote v2320.0.0b10`、
  `Auth enforcement: true`、`Credential domain health: HEALTHY`
- Paper 1.21.11 build 132、26.3 build 181（10-14）、194（10-16）、200（10-17）。実施票の26.3 build 181から、Paperの更新に合わせて替えた

| PC | OS | ブラウザ | サーバーのJava |
| --- | --- | --- | --- |
| Windows | Windows 11 Pro 26H2（26300.9711）、Smart App Controlオン | Chrome 155 | 25.0.2（Oracle OpenJDK） |
| macOS | macOS Tahoe 26.7.1、Apple M1、メモリ8 GB | Chrome 155 | Temurin 25.0.4.1 |
| Ubuntu | Ubuntu 24.04（kernel 7.0.0-30）、Core i5-8250U | Chrome 151 | 21.0.2（Oracle OpenJDK） |

## 結果

human ownerの判断（2026-10-17）：b10は合格。

| 項目 | Windows | macOS | Ubuntu |
| --- | --- | --- | --- |
| 取得〜初回起動 | 「許可する」→ ダブルクリック | 「このまま開く」→ ダブルクリック | 「プログラムとして実行」 |
| 1台構成 | 26.3（181、200） | 26.3 build 194、McRemoteのDBが無い新しいサーバー | 1.21.11 build 132 |
| ペアリング待ちの画面 | 見た | 見た | 見た |
| 保存・再開 | 済み（10-14） | 済み、`.sb3`のドロップ | 再開 |
| LAN構成 | Windows → macOS（26.3 build 200） | Mac → Ubuntu（1.21.11） | サーバー役 |

- Windows（10-14）：小学生（経験者で相当できる。標準的な小学生の結果ではない）が、mise、Paper 26.3、McRemoteの構築に続けて、
  LANパッケージで接続とチャットと建築まで、30分以内に大きな迷いなく進んだ。human ownerは保存と再開まで
- Windows：Smart App Controlがオンのまま、ZIPのプロパティで「許可する」にチェックしてから展開すると、`start-mc-remote.cmd`は
  ダブルクリックで警告なく起動した（`2026-10-14-01`）
- macOS：最初の警告の窓を閉じた後、「システム設定 → プライバシーとセキュリティ」に「このまま開く」が出る。押すと確認の窓で
  もう一度「このまま開く」、続いて管理者のパスワード。2回目からは警告なし
- Ubuntu：`start-mc-remote.sh`はダブルクリックではテキストエディターが開く。右クリック →「プログラムとして実行」で端末が開いて
  起動。実行の権限はZIPから残っていた。ダブルクリックの動作を「プログラムとして実行」へ変える設定は無い
- 3 OSとも、ランチャーの起動で設定画面が自動で開き、「このPC」または「LAN内の別のPC」の保存で`settings.json`ができ、
  「改造版のScratchを開く」でScratchが別のタブに開いた。Node.jsへの警告、firewallの確認は出なかった
- 「接続する」でWireScope miniが自動で開き、ペアコードとコマンドが出た。チャットで実行すると「ペアリング成功 / Paired.」、
  miniは「OK 接続」。WireScopeでhello（`token_not_found`の後に成功）、`mc_version`、`catalog_hash`がサーバーの値と一致
- macOS：setBlocks 32×32×32（32,768）は約1秒で完了。`.sb3`のドロップで、今の作品がブラウザに保存されてから切り替わった
  （human owner「このブラウザ保存／ロード、ファイル保存、ドロップロード体験はとても良い」）
- macOS：Minecraftサーバーの再起動の後、miniは「切断」「再接続 要」と出て、「接続する」でブラウザの再読み込みなしに、
  ペアリングなしで接続できた。2026-10-12の既知の問題（「接続」の表示のまま失敗）はこの回は起きなかった
- ランチャーを止めると、miniはすぐに「切断」。起動し直すとScratchのタブが開き（Ubuntuは自動で再読み込み）、ペアリングなしで
  接続できた
- Ubuntuのufwが有効（80/443だけ許可）のとき、MacからのLAN構成は「エラー」になった。25565と25575を許可するとつながった。
  それ以前のMac → Ubuntuの試験はufwを無効にして行った
- Scratchのsession tokenは約2時間で失効する（`13-scratch-client/scratch-plan_ja.md`、`2026-08-02-08`）。約2時間20分後の接続で
  `token_expired`になり、ペアリングし直した（設計どおり）。human owner：家庭やLANでの失効も、session tokenの体験に慣れる意味で
  有効。ペアリングはそれほど負担ではない。WireScope miniで詳しく分かれば、さらによい。分かる人はauthをoffにできる

## 見つかったこと

改善はrcからstableにかけての文言と案内、または初回stableの後のコードの変更として扱う（hub NOTES 2026-10-12、2026-10-17）。

1. `はじめに.html`：冒頭は概略の流れだけにして、その後にOS別に分ける。macOSとLinuxの起動の段落が埋もれている。macOSの
   許可の手順が実際と違う（案内は「このまま開く → 開く」。実際は警告の窓を閉じる、「このまま開く」を2回、管理者のパスワード）。
   設定画面のURLがリンクでなく、画面の画像も無い。小学校高学年には厳しく、保護者やメンターがいる想定なら足りる（human owner）。
   Chromeの「Geminiに相談」で要約させると、手順どおりの答えが返った
2. 前の版のランチャーが残って8601を使っていると、`Scratch Local: 起動できません: listen EADDRINUSE: address already in use
   127.0.0.1:8601`で終わり、次に何をすればよいか分からない（macOS）
3. macOSの`.command`は、利用者が既定にしているターミナル（iTerm2など）でなく標準のターミナルで開く
4. ランチャーの画面で`McRemote bridge listening on ws://127.0.0.1:8602`が2回以上出る（3 OS）。同梱のファイルの日付が
   1980年1月1日と表示される（macOS、Ubuntu）
5. 設定画面の「Scratchに戻る」がタブを切り替えなかった（macOSのChrome。案内は手でタブを選ぶよう断っている）
6. ペア待ちのminiの「次にすること：『接続する』ブロックを実行し、もう一度ペアリングしてください。」は、その時点ですることと
   ずれている（human owner「慣れてしまっていたが、おかしい」）
7. ペアコードがタイムアウトしても、miniは同じコードで「ペア待ち」のまま。Minecraft側の表示は「コードが見つかりません」
8. Minecraftサーバーが止まっているとき、firewallで止められたとき、どちらもminiは閉じたまま「エラー」、「接続を確認して、
   もう一度試してください。」で区別できない。miniは開いたほうがよい（human owner）
9. 接続先のポートをMinecraftのポート（25565）にすると、Scratchは「未接続」のままタイムアウトせず、サーバーのlogにも何も出ない。
   miniの表示にポートは出ない
10. Minecraftを抜けて入り直しても、Scratchの状況の表示では変化が分からない。ペアリングなしで接続できたとき、Minecraft側に
    表示が無い
11. 初期のスポーン（0, y, 0）と建築原点の初期値（200, 0, 200）が離れていて、原点の付近が山岳地帯のこともある
12. カタログピッカーの検索欄が目立たない
13. Windows（Smart App Controlオン、Windows → macOSのLAN構成）で、Git Bashからの起動の後に「接続する」でエラーになることが
    あった（2回）。コンソールの表示は普通で、Scratchは開く。間にダブルクリックで起動すると成功し、その後PowerShellとGit Bashからの
    起動も成功した。HTTPサーバーとBridgeの重複ではない。画面は取れていない。human ownerは同じエラーをScratch担当が準備した
    Ubuntuのローカル起動などで前にも見ている。`Zone.Identifier`は無かった（展開の前にZIPで「許可する」にした）
14. Paperの起動で、プラグインの初期化の後に、Windowsは6秒、macOSは2秒かかった（同じ26.3 build 200）。Ubuntuの1.21.11は
    JARの再マップを含めて10秒以上

## 主張しない範囲

翌日に誘導なしで始める回（human owner自身では意味が無い。human owner：今回の改善点を直せば、2回目もスムーズに行く見込み。
b10とrc1を使う中でフィードバックを得る）。Windowsのターミナルからの起動での接続のエラー（上の13）の原因。小学生の回の画面にあった
`Sprite1: x [mcr-error:entity_not_found]`は、何を試したときのものか分からない。授業規模の同時接続。
