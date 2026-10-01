# サウンド拡張の検討メモ（初回stable後）

> 状態: 未批准の検討メモ。初回stable後のサウンド拡張（シーケンス演奏、イベント登録、後続の候補）を検討するときの
> 参照先（`2026-09-30-03`、hub NOTESのpark「初回stable後のサウンド拡張」）。b8で確定した部分は`2026-09-30-02`と
> wire §5.8.3「サウンド」を正とし、この文書では決めない。
>
> 出典: McRemote dev sessionの検討素材`handoff-materials/2026-09-30-sound-api-review/materials/mc-remote-api-and-sound_ja.md`
> （`feat/b8-entity-lifecycle-particle`、2026-09-30、git管理外。その後McRemote側で破棄済み）の§2、§3.4、§3.6、§4、§5、§6。
> McRemoteの提案によりknowledgeへ移した。残りの§1、§3.1〜§3.3、§3.5は付録Aに復元した。節番号はこの文書で振り直した。記憶に基づく未検証の記述は、素材のとおり「未検証」「記憶」と書いてある。

## 1. サウンドでできること（Paper の事実）

### 1.1 音の種類

音は 1 つの registry（`Registry.SOUND_EVENT`、全 1838 個）にまとまっている。分類は ID の接頭辞だけ。

| 接頭辞 | 数 | 中身 |
| --- | --- | --- |
| `entity.*` | 830 | entity の種類ごと。1 種類に複数の場面がある（例 `entity.cow.ambient`、`.hurt`、`.death`、`.step`、`.milk`） |
| `block.*` | 801 | ブロックの種類ごと。場面は break、place、step、hit、fall など。似たブロックは同じ音を共有する（例 `block.stone.*`） |
| `item.*` | 113 | アイテムの動作ごと（例 `item.bucket.fill`、`item.trident.throw`）。すべてのアイテムに音があるわけではない |
| `music.*` | 52 | BGM |
| `ambient.*` | 22 | 環境音 |
| `ui.*` | 10 | UI 音 |
| その他 | 10 | `weather.*`、`event.*` など |

- 楽器（音符ブロックの音色）は `block.note_block.*` の 22 個。独立した種類ではない。
- `Registry.SOUNDS` は 1.21.4 から `@ApiStatus.Obsolete`。`SOUND_EVENT` を使う。

### 1.2 どこから鳴らすか

| 鳴らし方 | Paper API | 現象 |
| --- | --- | --- |
| 位置を決めて鳴らす | `playSound(Location, Sound, SoundCategory, volume, pitch)` | その場所から音がする。音は動かない |
| entity に結びつけて鳴らす | `playSound(Entity, Sound, SoundCategory, volume, pitch)` | entity の位置から音がする。entity が動けば音も付いていく |

- どちらも `World`（周りの player 全員に届く）と `Player`（その player だけに届く）の両方にある。
- どちらにも、seed（`long`）付きの版がある。場面によっては音に複数のバリエーションがあり、seed でどれを鳴らすかを決められる。
- `Player#stopSound(...)` で、その player に鳴っている音を止められる。`World` には無い。

### 1.3 ピッチと音階

- pitch は再生速度の倍率。0.5 が 1 オクターブ下、1.0 が元の高さ、2.0 が 1 オクターブ上。すべての音に使える。
- 元の高さは音ごとにまちまちなので、絶対的な音名にはならない。
- ただし、サンプリング音源を鍵盤で弾くのと同じで、どの音にも半音刻みの 25 段階（0〜24）を当てはめられる。倍率は `2^((n - 12) / 12)`。12 が元の高さ、0 と 24 がちょうど 1 オクターブ下と上。
- 音符ブロックの音色は調律済みなので、この 25 段階がそのまま音名になる。Paper の `Note`（id 0〜24）、`Note#getPitch()`、`Instrument#getSound()` はこの関係をそのまま持っている。

### 1.4 「鳴かせる」

- Paper に「鳴かせる」専用の method は無い。
- entity 自身の音は getter で取れる。
  - `Mob#getAmbientSound()`（普段の鳴き声）
  - `LivingEntity#getHurtSound()`、`getDeathSound()`、`getFallDamageSound(int)`、`getEatingSound(ItemStack)`、`getDrinkingSound(ItemStack)`
  - `Entity#getSwimSound()`、`getSwimSplashSound()`
- 「鳴かせる」は、「その entity の音を、その entity に結びつけて鳴らす」ことで再現できる。
- 結びつける音は何でもよい。牛から猫の声や音符ブロックの音を鳴らすこともできる。
- 鳴らすのは音だけで、口を動かすなどの動作は伴わない。
- `Entity#setSilent(boolean)` で、その entity が自分では鳴かないようにできる。

### 1.5 ブロックの音

- `BlockData#getSoundGroup()` で、そのブロックの音のセット（`SoundGroup`）が取れる。
- `SoundGroup` は `getPlaceSound()`、`getHitSound()`、`getBreakSound()`、`getStepSound()`、`getFallSound()` と、標準の `getVolume()`、`getPitch()` を持つ。
- 使いどころ: つついたブロックの叩き音（`pickaxe_poke` に対応）、置いたブロックの設置音（`setBlock` に対応）。API の `setBlock` で置いたときは、音は自動では鳴らない。

#### 1.5.1 SoundGroup の種類（Paper 1.21.11 のサーバー jar で確認）

`SoundGroup` の中身は vanilla の `SoundType`（`net.minecraft.world.level.block.SoundType`）。サーバー jar の定義を `javap` で読み出した。

- 全部で 123 種類。木、石、砂利、草、ガラス、羊毛、砂、雪、金属、鉄、銅、アメジスト、深層岩、スカルク、泥、竹など。
- 種類ごとに別の音素材（録音）を持つ。同じ素材を高めや低めにしたグループではない。
- 標準の音量と高さが 1.0 でないのは 3 種類だけ。

| SoundGroup | 音量 | 高さ | 備考 |
| --- | --- | --- | --- |
| `METAL` | 1.0 | 1.5 | 金属専用の音素材を 1.5 倍で鳴らす |
| `ANVIL` | 0.3 | 1.0 | 金床の音を小さく |
| `TWISTING_VINES` | 1.0 | 0.5 | `WEEPING_VINES` と同じ音素材を 1 オクターブ下げている |

- 同じ音素材で高さだけ違うのは、ねじれツタとしだれツタの 1 組だけ。
- 主なブロックとグループの対応（ブロック定義の bytecode から機械的に拾った。取りこぼしの可能性あり）:
  - `METAL`（×1.5）: レール 4 種、ホッパー、金・ダイヤモンド・エメラルド・レッドストーンのブロック、カメの卵、スニッファーの卵
  - `IRON`（×1.0）: 鉄ブロック、鉄格子
  - `ANVIL`（音量 0.3）: 金床 3 種、鐘
  - `COPPER`（×1.0）: 銅ブロック、銅のチェスト、避雷針

#### 1.5.2 vanilla の場面ごとの調整

vanilla は、場面ごとに音量と高さを掛けてから鳴らす。

| 場面 | vanilla の調整 | 確認 |
| --- | --- | --- |
| 置く（`place`） | 高さ ×0.8。音量も `getVolume()` から計算している | サーバー jar（`BlockItem`） |
| 歩く（`step`） | 音量 ×0.15 | サーバー jar（`Entity`） |
| 落ちる（`fall`） | 音量 ×0.5、高さ ×0.75 | サーバー jar（`LivingEntity`） |
| 叩く（`hit`）、壊す（`break`） | クライアント側のコードで鳴らす | サーバー jar からは確認できない |

- ゲーム内で聞くブロックの音が素材より低めなのは、主にこの場面ごとの調整による（`SoundGroup` 自体の高さは、ほとんどが 1.0）。

#### 1.5.3 mc-remote での扱い（human owner 2026-09-30）

- `world.playBlockSound` は、options を省略したら `SoundGroup` の値をそのまま使う（場面ごとの調整はしない）。多くのブロックは素材そのままの高さで鳴り、`METAL` は 1.5 倍、`ANVIL` は音量 0.3 で鳴る。
- ゲーム内の手触りに近づけたいときは、ユーザーコードで `pitch` や `volume` を指定する（例: 置く音なら高さ ×0.8）。
- 既定は項目ごと。`volume` だけ指定したら、高さは `SoundGroup` の値のまま。
- `pitch` や `note` を指定したら、`SoundGroup` の高さを掛けずに置き換える（`note` 12 は素材そのままの高さ）。

### 1.6 位置と距離（クライアントの挙動。未検証）

以下は Minecraft クライアントの挙動についての記憶で、実機では確かめていない。人が参加する試験で耳で確認する。

- 左右の定位: 聞く人から見た音源の方向で左右に振り分けられる。
- 距離による減衰: 音源から離れるほど小さくなる。volume 1 以下では、おおよそ 16 ブロックで聞こえなくなる。
- volume が 1 を超えると、大きくはならずに聞こえる距離が延びる（約 16×volume ブロック）。
- world に届ける場合、周りの各 player が、自分と音源の距離と方向に応じた音量と定位で聞く。self に届ける場合も、本人から見た定位と減衰は同じように効く。
- 使い方の例: self で試作して world で公開する。各自が自分の位置から鳴らせば、集まると合奏になり、並び方がそのまま舞台の配置になる。

### 1.7 音楽

- Paper に `playMusic` という API は無い（`World`、`Player`、`Server` を確認）。
- `music.*` は 52 個: レコード（`music_disc.*`）21、地上の BGM 19、ネザー 5、エンド、クリエイティブ、クレジットなどの単発 7。
- 手段は 2 つ。
  - `playSound` で鳴らす。category はレコードなら `RECORDS`、BGM なら `MUSIC`。止めるには `Player#stopSound` を player ごとに呼ぶ。
  - ジュークボックス（`org.bukkit.block.Jukebox`）: `setRecord(ItemStack)`、`startPlaying()`、`stopPlaying()`、`isPlaying()`、`eject()`。位置にジュークボックスのブロックが要る。周りに「再生中」の表示が出る。
- 曲の長さを返す API は無い。
- クライアントの「音楽」の音量を 0 にしている人は多い。レコードは別の音量スライダーなので聞こえやすい（記憶。未検証）。

### 1.8 vanilla のコマンド（Paper 1.21.11 の実機で確認）

| コマンド | 書式 |
| --- | --- |
| `/playsound` | `<sound> [<source>] [<targets>] [<pos>] [<volume>] [<pitch>] [<minVolume>]` |
| `/stopsound` | `<targets> [<source>または*] [<sound>]` |
| `/particle` | `<name> [<pos>] ...` |
| `/summon` | `<entity> [<pos>]` |
| `/setblock` | `<pos> <block> [destroy/keep/replace/strict]` |

- `source` の値は単数形: `master`、`music`、`record`、`weather`、`block`、`hostile`、`neutral`、`player`、`ambient`、`voice`、`ui`。
- 範囲: `volume` は 0 以上（上限なし）、`pitch` は 0.0〜2.0、`minVolume` は 0.0〜1.0。範囲外はコマンドの解析で拒否される。
- `targets` は `@a`（全員）や `@s`（自分）など。mc-remote の `receiver` では `world` ≒ `@a`、`self` ≒ `@s` と対応づけられる。
- mc-remote の pitch は 0.5〜2.0 にする。0.5 未満はクライアントで 0.5 に切り詰められると記憶している（未確認）ので、受けると暗黙の切り詰めになる。
- vanilla 自体は、名前が先のもの（`/particle`、`/summon`、`/playsound`）と位置が先のもの（`/setblock`）が混在している。

## 2. 候補の一覧と実装順（human owner 2026-09-30）

> b8の2 method（`world.playSound`、`world.playBlockSound`）は`2026-09-30-02`で確定し、exact contractはwire §5.8.3「サウンド」にある。
> 下の表のb8の行は当時の検討として残す。stable後の行は`2026-09-30-03`とhub NOTESのparkに入った。

| 順 | 候補 | wire | 内容 |
| --- | --- | --- | --- |
| b8 | 位置から鳴らす | `world.playSound` | 位置と sound を指定して鳴らす |
| b8 | ブロックを鳴らす | `world.playBlockSound` | そのブロックの音（place、hit、break、step、fall）を鳴らす |
| stable 後 | シーケンス演奏 | `setMusicSequence` など（§5） | サーバー側で tick ごとに正確に鳴らす。優先度を上げる |
| stable 後 | イベント登録 | §6 | イベントでシーケンスを開始する。シーケンスと同時に優先度を上げる |
| 後続 | 本人から鳴らす | `player.playSound` | 演奏する |
| 後続 | 鳴かせる | `entity.playSound` | entity 自身の音を、その entity から鳴らす |
| 後続 | 曲を鳴らす | `playMusic` | 曲の ID で鳴らす。止める手段とセットで検討する |
| 後続 | 音を止める | 未定 | `playMusic` とセットで検討する |
| 後続 | catalog に sound を追加 | `catalog.get` の拡張 | Scratch のドロップダウン用 |

- 初期は `world.playSound` でも `music.*` の ID を鳴らせるようにしておく。ただし止める手段が無いので、長い曲には向かない。
- `playMusic` は扱いがかなり違う（長さ、止める、ジュークボックス、音量設定）ので、別の候補として検討する。
- `sound` の指定は、ID 文字列か `{sound_id, receiver?, category?}` の spec（particle と同じ形）を想定している。
- `world.playBlockSound` は、その位置のブロックを読んで音のセットを引くので、`world.getBlock` と同じく chunk の準備が要る。`world.playSound` は chunk の準備が要らない。

## 3. 後続で決める点

- volume が 1 を超える（聞こえる距離を延ばす）使い方を許すか
- 音量の種類を options として足すか。足すなら項目名は `source`、値は vanilla の単数形（`master`、`music`、`record`、`weather`、`block`、`hostile`、`neutral`、`player`、`ambient`、`voice`、`ui`）
- `minVolume`（聞こえる範囲の外の人にも小さく聞かせる）を options として足すか
- entity とブロックの「場面」の語彙の拡張
- entity に結びつけるときの handle の失敗理由（entity lifecycle の規則に揃える前提）
- `playMusic` の方式（`playSound` 系か、ジュークボックス方式か）と、止める手段の形

## 4. 参考: Scratch の音のブロックとの対応

Scratch の仕様は scratch-editor の scratch-vm（`packages/scratch-vm/src/blocks/scratch3_sound.js`、`packages/scratch-vm/src/extensions/scratch3_music/index.js`）で確認した。

### 4.1 標準の「音」

| Scratch のブロック | Scratch の仕様 | mc-remote での対応 |
| --- | --- | --- |
| 音を鳴らす | 鳴らしてすぐ次へ進む | `playSound`（鳴らしっぱなし）に対応する |
| 終わるまで音を鳴らす | 音の終わりを待つ | そのままは作れない。サーバーは MC の音の長さを知らない |
| すべての音を止める | 自分のプロジェクトの音を止める | 「止める」が要る。本人だけなら `Player#stopSound` で作れる |
| ピッチの効果を〜にする／変える | 範囲 −360〜+360（±3 オクターブ）、10 で半音 | MC は ±1 オクターブ（±120）まで。倍率は `2^(効果 / 120)`。10 の倍数なら `note = 12 + 効果 / 10` |
| 効果「左右にパン」 | 範囲 −100〜+100 | MC は音源の位置で定位が決まる。聞く人の左右に音源をずらせば近いことができる |
| 音量を〜%にする／変える | 範囲 0〜100 | MC の volume 0.0〜1.0 に対応する |

### 4.2 拡張の「音楽」

| Scratch のブロック | Scratch の仕様 | mc-remote での対応 |
| --- | --- | --- |
| 音符を〜拍鳴らす | MIDI の音番号 0〜130（60 が C4） | MIDI 番号を `note`（0〜24）へ換算する。音符ブロックの音域は 2 オクターブなので、はみ出す分は楽器の選び方かオクターブの折り返しで扱う |
| 楽器を〜にする | 21 種類（ピアノ、エレクトリックピアノ、オルガン、ギター、エレキギター、ベース、ピチカート、チェロ、トロンボーン、クラリネット、サックス、フルート、木のフルート、バスーン、合唱、ビブラフォン、オルゴール、スチールドラム、マリンバ、シンセリード、シンセパッド） | MC の音符ブロックの 16 音色への対応表が要る。`note` はどの sound にも使えるので、楽器以外の音を当ててもよい |
| ドラムを〜拍鳴らす | 18 種類（スネア、バスドラム、サイドスティック、クラッシュシンバル、オープンハイハット、クローズドハイハット、タンバリン、ハンドクラップ、クラベス、ウッドブロック、カウベル、トライアングル、ボンゴ、コンガ、カバサ、ギロ、ビブラスラップ、クイーカ） | MC の basedrum、snare、hat、cow_bell に加えて、任意の sound を当てられる |
| 休む | 拍数 0〜100 | クライアント側のタイミングで扱う |
| テンポを〜にする／変える | 範囲 20〜500 | クライアント側で扱う |

### 4.3 protocol への示唆

- wire は最小でよい。要るのは「鳴らす」（`pitch` か `note`、volume、receiver）と「止める」だけ。効果、音量の状態、テンポ、楽器の対応表は、Scratch 自身がスプライトの状態として持っているのと同じく、クライアント側で持てる。
- volume を 0〜1 にする案は、Scratch の 0〜100% と素直に対応する。
- 「すべての音を止める」は Scratch の標準ブロックなので、本人だけを止める `player.stopSound` は優先度が上がる。
- 「終わるまで鳴らす」は、クライアント側に音の長さの表を持たない限り作れない。
- 未確認: 音符ブロックの harp の音域を F#3〜F#5（MIDI 54〜78）とする換算は記憶に基づく。換算表を作るときは実機か Paper の実装で確かめる。

## 5. 候補: 音楽シーケンス（stable 後に実装）

### 5.1 目的

クライアントから 1 音ずつ送る方式では、音のタイミングに 2 つのずれが重なる。

- tick への量子化: McRemote は受け取った命令を 1 tick（標準 50 ms）ごとの同期タスクでまとめて実行する（`scheduleSyncRepeatingTask(..., 1, 1)`、1 tick で最大 1000 件）。
- 通信の揺らぎ: 送信から到着までの時間が音ごとにばらつき、別々の tick に落ちたり、同じ tick に固まったりする。

シーケンスをサーバーに登録してサーバー側で鳴らせば、通信の揺らぎは消える。tick への量子化は残る（Minecraft の音はサーバーから tick 単位で送られるため）。

- テンポ 120 なら 4 分音符は 500 ms で、ちょうど 10 tick。16 分音符は 125 ms で 2.5 tick になり割り切れない。
- テンポを 20 tick の約数に合う値（100、120、150 など）にすると揃う。

### 5.1a 時間分解能（見立て。未測定）

| 観点 | 見立て |
| --- | --- |
| 刻み（分解能） | 1 tick = 50 ms。1 秒に 20 か所しか音を置けない |
| 刻みの中の正確さ | 同じ tick の音は一緒に送られ、tick 同士の間隔は 50 ms の倍数になる。揺れは tick 処理の開始時刻のぶれと通信のぶれだけで、負荷の低いサーバーと LAN なら数 ms 程度のはず |
| 開始の遅れ | 演奏全体が一定だけ遅れるだけ。1 人で聞く分には問題にならない。合奏で他の人と揃えるときは効く |
| サーバーが重いとき | 1 tick の処理が 50 ms を超えると、その後ろが全部遅れる（テンポが揺れる） |

| テンポ | 4 分音符 | 8 分音符 | 16 分音符 |
| --- | --- | --- | --- |
| 100 | 12 tick | 6 tick | 3 tick |
| 120 | 10 tick | 5 tick | 2.5 tick（割り切れない） |
| 150 | 8 tick | 4 tick | 2 tick |

- 50 ms の格子より細かいリズム（32 分音符、細かいスイング）は表現できない。
- 比較: redstone で作る音符ブロックの音楽は、リピーター 1 段が 2 tick（100 ms）なので、100 ms の格子で作られていることが多い。サーバー側のシーケンスはその倍の細かさ。
- tick より細かくする可能性（要調査）: 別スレッドから音の packet を直接送れば、tick を待たずに送れるかもしれない。ただし Paper が保証する使い方ではなく、スレッド安全性の検証が要る。クライアント側の処理が自身の tick（50 ms）に同期しているなら、サーバーだけ細かくしても効かない。
- イベント登録（§6）で反応する場合の遅れは、次の tick を待つ時間（平均 25 ms、最大 50 ms）に通信の片道 2 回が乗る。

### 5.2 method（案）

| method | 内容 |
| --- | --- |
| `setMusicSequence` | シーケンスを登録する |
| `playSequence` | 登録したシーケンスを選んで演奏する。音源（位置、player、entity）、receiver、loop を指定する |
| `pauseSequence` | 一時停止と再開を切り替える（トグル）。再開は止めた位置から続ける |
| `stopSequence` | 演奏を止める |

### 5.3 イベント（案）

`events` は `[{note または pitch, duration, volume, on/off}, ...]`。

- `note`（0〜24）か `pitch`（0.5〜2.0）のどちらか一方。
- `duration` は次のイベントまでの時間（tick の整数）。拍やテンポ（BPM）から tick への換算はクライアント側で行う。
- `on` で音を鳴らし、`off` イベントで止める。
- loop を指定すると、最後のイベントの後に先頭へ戻り、tick の刻みのまま正確に繰り返す。

### 5.4 検討メモ

- `off` で止める手段は `Player#stopSound(sound, category)` になる。これは、その player に鳴っている同じ sound をまとめて止めるもので、重なっている同じ音のうち 1 つだけを止めることはできない。world に届ける場合は、周りの player ごとに呼ぶ。
- 音符ブロックの音はもともと短いので、`off` が意味を持つのは長い音（持続する音や曲）のとき。
- 上限: 1 つのシーケンスのイベント数と長さ、接続ごとの登録数、同時に演奏できる数を runtime policy で持つ。
- 1 tick あたりの音の上限は、演奏中も効かせる。1 tick に詰め込みすぎのシーケンスは、登録の時点で断る。
- 寿命: 登録と演奏は接続ごとにし、切断したら破棄して止める（entity の handle と同じ扱い）。
- 終了の通知: loop しない演奏が終わったら、`events.poll` に通知を出すかどうか。
- サーバーの TPS が落ちると演奏も遅れる。これはどの方式でも避けられない。
- MIDI ファイルからの変換は、ユーザーコードかクライアントのライブラリで行う。
- 既存の method を変えない追加なので、stable 後に minor 版で足しても互換は壊れない。b8 で決める `playSound` の語彙（`pitch`／`note`、音源、receiver）を、イベントでもそのまま使う。

## 6. 候補: イベント登録（stable 後に実装）

### 6.1 目的

ツルハシでつついてからクライアントがブロックの音を鳴らす方式では、音が鳴るまでに次の段が直列に重なる。

1. サーバーがイベントを捕まえて、イベントの蓄え（event ring）に入れる。
2. クライアントが `events.poll` で取りに来るまで待つ（poll の間隔しだいで、ここが最も大きい）。
3. イベントがクライアントへ届く（片道の通信）。
4. クライアントが音の命令を送る（片道の通信）。
5. サーバーが、届いた後の次の tick で実行する（最大 50 ms）。
6. 音の packet が player のクライアントへ届く（片道の通信）。

楽器としては 20 ms を超えると使えない（human owner の判断）。

- 常に全員へ鳴らす案（`pickaxe_poke` のたびにサーバーが叩き音を鳴らす）は採らない。
- 学びの流れとして「最初はもどかしい → 新しい仕組みで良くなる」を狙う。

### 6.2 形（案）

「イベントが起きたら、サーバー側でシーケンスを開始する」という反応を登録する。

- 反応の中身はシーケンスの開始を基本にする。1 音だけのシーケンスは単発の音と同じなので、単発の音から短いフレーズまでを 1 種類でまかなえる。
- 音源の既定は、イベントが起きた場所（つついたブロックの位置）。ブロックごとに定位が付く。
- 絞り込み: イベントの種類（`pickaxe_poke`、chat など）に加えて、ブロックの位置、範囲、種類で絞れるようにする。ブロックごとに別のシーケンスを割り当てれば「ブロックの鍵盤」になる。
- 反応の種類: 開始のほかに、止める、一時停止の切り替えを持てると表現が広がる。

### 6.3 検討メモ

- 鳴っている最中にもう一度起きたとき、重ねて鳴らすか、頭から鳴らし直すか、無視するか。
- 寿命: シーケンスと同じく接続ごとにし、切断したら登録も消す。
- 登録数の上限を runtime policy で持つ。
- 20 ms の壁（見立て。未測定）: サーバー側で反応しても、操作がサーバーに届いてから次の tick を待つ（最大 50 ms）ことと、音がクライアントへ届く片道の通信が残る。これは vanilla の音符ブロックを叩いたときと同じ経路で、Minecraft での上限にあたる。poll の待ちと往復 1 回分の通信は消えるので、今の方式よりは大幅に縮む。実装するときに、つついてから鳴るまでを実機で測る。

## 付録A. 素材のうち、移し忘れていた節（復元）

> McRemoteの素材は、§2、§3.4、§3.6、§4〜§6を移した後で失効破棄された。coordinatorが残りの節を移さないまま
> 「破棄してよい」と連絡したためである。以下の§1、§3.1〜§3.3、§3.5は、coordinatorが2026-09-30にこの会話で読んだ
> 時点の本文から復元した。その後に素材側で書き換えられていた場合、その変更は復元できていない。§3.5のb8の形は
> `2026-09-30-02`とwire §5.8.3を正とし、ここは経緯として残す。

### A.1 現在の wire API（protocol 23.2.0。素材§1）

座標 `x, y, z` はすべて stream origin からの相対値。

#### 接続・認証

| method | params | result |
| --- | --- | --- |
| `hello` | `{protocol, auth?, build?}` | 接続情報（protocol、mc_version、player、dimension、origin など） |
| `auth.pairBegin` | `{token_type, client}` | `{pairing_id, pair_code, expires_in}` |
| `auth.pairPoll` | `{pairing_id}` | `{status, token?}` |
| `auth.listCredentials` | credential 管理 | 一覧 |
| `auth.revoke` | credential 管理 | 結果 |
| `auth.logout` | credential 管理 | 結果 |
| `connection.flush` | `[]` | `null` |

#### 建築の文脈

| method | params | result |
| --- | --- | --- |
| `build.setDimension` | `[dimension_ref]` | `{dimension, origin}` |
| `build.setOrigin` | `[x, y, z]` | `{dimension, origin}` |

#### ブロック

| method | params | result |
| --- | --- | --- |
| `world.setBlock` | `[x, y, z, BlockSpec]` | `null` |
| `world.setBlocks` | `[x1, y1, z1, x2, y2, z2, BlockSpec]` | `null` |
| `world.getBlock` | `[x, y, z]` | BlockValue |
| `world.getBlocks` | `[x1, y1, z1, x2, y2, z2]` | 範囲の BlockValue |
| `world.getHeight` | `[x, z, max_y?]` | y |
| `world.setSign` | `[x, y, z, {front?, back?}]` | `null` |
| `world.getSign` | `[x, y, z]` | `{front, back, waxed}` |
| `world.updateSignLine` | `[x, y, z, face, line_index, LineSpec]` | `null` |

#### player（ペアリングした本人）

| method | params | result |
| --- | --- | --- |
| `player.getPos` | `[]` | `{dimension, pos}` |
| `player.setPos` | `[dimension, x, y, z]` | `{dimension, pos}` |
| `player.getPose` | `[]` | `{dimension, pos, yaw, pitch}` |
| `player.setPose` | `[dimension, x, y, z, yaw, pitch]` | `{dimension, pos, yaw, pitch}` |
| `player.getDirection` | `[]` | `[x, y, z]`（単位ベクトル） |
| `player.setDirection` | `[x, y, z]` | `[x, y, z]` |

#### entity（handle で指す）

| method | params | result |
| --- | --- | --- |
| `world.spawnEntity` | `[x, y, z, entity_id]` | handle |
| `world.getNearbyEntities` | `[x, y, z, radius, max_entities]` | `[{handle, type, pos}, ...]` |
| `entity.getPose` | `[handle]` | `{dimension, pos, yaw, pitch}` |
| `entity.setPose` | `[handle, dimension, x, y, z, yaw, pitch]` | `{dimension, pos, yaw, pitch}` |
| `entity.getDirection` | `[handle]` | `[x, y, z]` |
| `entity.setDirection` | `[handle, x, y, z]` | `[x, y, z]` |
| `entity.remove` | `[handle]` | `null` |

#### 演出（その場で起きて残らないもの）

| method | params | result |
| --- | --- | --- |
| `world.spawnParticle` | `[x, y, z, ox, oy, oz, particle, speed, count, force?]` | 受理した count |
| `world.strikeLightning` | `[x, y, z]` | `null` |

`world.spawnParticle` の `particle` は ID 文字列か `{particle_id, receiver?, data?}`。

#### その他

| method | params | result |
| --- | --- | --- |
| `chat.post` | `[message]` | 既定は送信のみ |
| `events.poll` | `[after_sequence, {max_events}?]` | イベントの一覧 |
| `catalog.get` | `[]` | block、entity、particle の一覧 |

#### 再構成で目につく点

- `world.*` に、ブロックの読み書き、entity の生成と検索、演出が同居している。生成後の entity 操作は `entity.*`。
- player は `getPos`／`setPos` と `getPose`／`setPose` が重なる。entity は Pose と Direction だけ。
- 「誰に届けるか」（receiver）は particle の spec の中にある。sound も同じ形にすると演出系で揃う。

### A.2 設計の軸（素材§3.1）

| 軸 | 選択肢 |
| --- | --- |
| 何を鳴らすか | 任意の sound ID、または対象自身の音（entity の鳴き声、ブロックの設置音など） |
| 高さの指定 | 精密な倍率 `pitch`（0.5〜2.0）、または 25 段階 `note`（0〜24） |
| 何が音源か | 位置、entity（handle）、player 本人、ブロック |
| 誰に届けるか | `world`（周りの全員）、`self`（本人だけ） |

### A.3 method と名前の対応（素材§3.2）

wire の名前は 4 つとも `*.playSound` で揃え、名前空間で音源を表す。学習者向けの名前は、Python の既存の流儀（`mc.setPos` が player 本人、`mc.setBlock` が位置）に合わせる。

| wire | 現象 | クライアント名 | 基本の引数 | オプション |
| --- | --- | --- | --- | --- |
| `world.playSound` | 音を出す | `playSoundAt` | 位置、sound | 高さ、volume、receiver、category |
| `entity.playSound` | 鳴かせる | `makeNoise`（候補 `makeSound`） | handle、場面（ambient、hurt、death など） | 他の sound、高さ、volume、receiver |
| `player.playSound` | 演奏する | `playSound` | sound | 高さ、volume、receiver、category |
| `world.playBlockSound` | ブロックを鳴らす | `playBlock`（候補 `playBlockSound`） | 位置、場面（place、hit、break、step、fall） | 高さ、volume、receiver |

名前の検討メモ:

- `makeNoise`: 英語の noise には「雑音・騒音」の含みがある。楽器の音を割り当てたときに違和感が出るかもしれない。候補は `makeSound`。
- `playBlock`: Scratch では「ブロック」がコードのブロックも指す。Python でも「ブロックを置く」と取り違えやすい。候補は `playBlockSound`。
- wire の `world.playSound` とクライアントの `playSound`（player 本人）は指すものが違う。WireScope では wire の名前が見えるので、対応表を教材側に置く。

### A.4 高さの指定（`pitch` と `note`。素材§3.3）

- wire では、`pitch`（0.5〜2.0 の倍率）と `note`（0〜24 の整数）のどちらか一方だけを受ける。
  - 両方あれば `invalid_params`。
  - どちらも無ければ元の高さ（pitch 1.0）。
- `note` の倍率は `2^((note - 12) / 12)`。12 が元の高さ、0 と 24 がちょうど 1 オクターブ下と上。楽器に限らず、どの sound でも使える（サンプラーを鍵盤で弾くのと同じ）。
- 音名（ドレミ、C4 など）はユーザーコードで `note` に換算する。音符ブロックの音色は調律済みなので、25 段階がそのまま音名になる。
- Scratch の入力の案: 数字なら `pitch`、`N0`〜`N24` なら `note`。
- Python などは、`pitch=` と `note=` を別の引数名で受ける。

### A.5 b8 で決めた wire の形（素材§3.5。経緯として残す。正は`2026-09-30-02`とwire §5.8.3）

| # | 項目 | 決定 |
| --- | --- | --- |
| 1 | params の形 | `world.playSound [x, y, z, sound_id, options?]`、`world.playBlockSound [x, y, z, kind, options?]`。`options` は `{volume?, pitch?, note?, receiver?}` で、未知の項目は `invalid_params` |
| 2 | volume | 0.0〜1.0、既定 1.0 |
| 3 | 高さ | `pitch` は 0.5〜2.0、`note` は整数 0〜24。どちらか一方だけ（両方なら `invalid_params`）。省略時は元の高さ |
| 4 | receiver | `world`（既定）か `self`。`self` は未束縛なら `auth_required`、offline なら `player_offline` |
| 5 | 音量の種類（source） | b8 では指定させない。`playSound` は `master`、`playBlockSound` は `block` に固定（vanilla の `source` の値。Bukkit では `SoundCategory.MASTER`／`BLOCKS`） |
| 6 | 連打の制限 | 1 tick あたりの上限を runtime policy で持つ（既定: 接続ごと 16、全体 64）。超えたら `backpressure` |
| 7 | 未登録の sound | 新しい reason `unknown_sound`（-32602） |
| 8 | result と work cost | result は `null`、work cost は 1 |
| 9 | 座標 | `playSound` は有限の数値（小数可）、`playBlockSound` はブロックの整数座標 |
| 10 | `kind` の語彙 | `place`、`hit`、`break`、`step`、`fall`。それ以外は `invalid_params` |
| 11 | ブロックの音の既定 | options を省略したら、`SoundGroup` の標準値（`getVolume()`、`getPitch()`）で鳴らす |
| 12 | 空気のブロック | 新しい reason `no_block`（判定は `Material#isAir()`。`air`、`cave_air`、`void_air`） |
| 13 | permission、build range、chunk | どちらも permission と build range を確認する。`playBlockSound` だけ chunk を準備する（`getBlock` と同じ） |
| 14 | 引数の順 | 位置が先（mc-remote の `setBlock`、`spawnParticle`、`spawnEntity` と揃える）。語彙（`volume`、`pitch`、将来の `source`）は vanilla の `/playsound` に合わせる |
