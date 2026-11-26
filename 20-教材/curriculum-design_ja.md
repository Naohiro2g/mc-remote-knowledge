# カリキュラムの設計

これまでの教材を、決まった道筋（カリキュラム）として整える設計記録。12月末までに、ScratchとPythonの教材を整理して
洗練させ、Pyxelを出力先に加え、カリキュラムとしての完成度を上げる（human owner 2026-11-26）。

出典：human ownerの説明（2026-11-26）と、これまでの教材（§5）。

## 1. 位置づけ：自転車の後ろを支える

決まった道筋は、学習支援の考え方とは逆である。それでもカリキュラムを作るのは、従来の学校教育のやり方にはめられてきた生徒を
引き上げるための方便である。human owner 2026-11-26：「自学自習の良い筋を示して、後ろから押されながら、進む道もある程度ガイド
（要するに制限）されながら、シミュレーションする。自転車にはじめて乗る時のお父さん役みたいな支援。スピードに乗ったらあとは自走。」

- ガイドするのは道で、全員の速さはそろえない（[XYZ軸の空間で建てる教材の設計](xyz-space-learning-design_ja.md) §5と同じ）
- 日付つき時計の後は「自由」にする（§2）。後ろから支えていた手を離すところにあたる

## 2. コンテンツと順番

12月の優先は、①、②、③の順（human owner 2026-11-26）。

```text
① 2進数・16進数 → ドットマトリクスフォント（文字コード、デザイナーアプリ） → 日付つき時計 → マイクラの世界に映す
     └ 日付つき時計の後は自由：reversi、ink spillなどのゲーム、Pyxelの落ちゲー
② モンテカルロ法の円周率
③ マイクラ課題：一個 → 柱 → … → ピラミッド
```

- ①：2進数と16進数は、フォントの1行を`01110`のように表すこと、ASCIIのコード（上位3ビットと下位4ビット）、7セグで0〜Fを
  出すことでフォントとつながる（§5のスライド）。デザイナーアプリはScratchとPythonにある
- ①の後の自由：これまでの流れでは、日付つき時計の後は自由にしていた。ゲームの題材は、たとえば
  [Making Games with Python & Pygame](https://inventwithpython.com/pygame/)のreversi（Flippy）やink spill。同じ本には、
  ゲームごとに1か所ずつ虫を入れた版が8本ほどと、それぞれの症状の説明がある（<https://inventwithpython.com/pygame/buggy/>）。
  コードは「Simplified BSD」license。Pyxelの落ちゲーはカリキュラムの道筋とは別のルートで、ここに入る（human owner
  2026-11-26「pyxelによる落ちゲーは、別ルートだね。」）
- ②：100×100ほどの視覚化（有効数字2桁）をScratch、pygame、Pyxelで行い、その先は数値の計算だけにして、Scratch、Python、
  Rustの速さを比べる（`2026-11-26-02`③、hub NOTESの行）
- ③：最初から3Dへ進む。1次元、2次元、3次元と進み、ピラミッドで終わる。道筋は
  [XYZ軸の空間で建てる教材の設計](xyz-space-learning-design_ja.md) §5

## 3. 言語と出力先

最後は、それぞれのコンテンツをScratch、Python、Rustの3つの言語で並べる。12月は、ScratchとPythonの整理と洗練を先にする。

- Pyxel：Pythonの出力先として、①と②に加える
- Rust：12月の中では、②と③に入れる。③は、Rust Client Libraryの最初の縦slice（`2026-11-26-02`④）で書く（human owner
  2026-11-26「12月中にRustは、モンテカルロ法、に滑り込みで、第1弾スライスでのマイクラ課題。」）。①へのRustは、その後
- 出力先：Scratchのステージ、pygame、Pyxel、マイクラ、Unity箱庭。Unity箱庭ができたので、マイクラ課題の外でも、出力先として
  気軽に使う。出力先を学習の内容と別の軸にする考えは、[学習支援の設計](ai-learning-design_ja.md)の`REAL`／`PREVIEW`／
  `PYGAME`と同じ

## 4. 気をつけること

- フォント「なつめもじ」は再配布が禁止されている（`dotmatrix_font`のREADME）。カリキュラムには入れず、使う人が配布元から
  取ってくる。2026-11-26の時点で、公開repoの`pygame_samples`と`pygame_mcpi_LCD_7seg`には`fonts/natumemozi.ttf`が入っている
- マイクラに映すこれまでのコードは、ラズパイのマイクラのAPI（mcpi）で書かれている（`pygame_mcpi_LCD_7seg`）。今の
  `minecraft-remote-api`へ移す
- ScratchのデザイナーとScratchの時計は、ターボモードで動かす
- Making Games with Python & Pygameのコードを、Pyxelなどへ移して配るときは、元の著作権の表示とSimplified BSDの文を残す

## 5. これまでの教材

①の実物（2026-11-26に、human ownerが場所を示した）。

- Scratch「Dot-matrix font designer」（<https://scratch.mit.edu/projects/940437151/>）：5×7のフォントを作り、`font.txt`へ書き出す
- Scratch「dotmatrix clock with date」（<https://scratch.mit.edu/projects/964087643/>）：デザイナーで作ったフォントで日付と時刻を出す
- 文書「ドットマトリクス フォントデザイナーの使い方（Scratch版）」（2024-03-10、
  <https://docs.google.com/document/d/1NTJy3wi17OK3HYSi3LhD30ClbH4GGFLRV2HxO-vr3_k/edit>）：human ownerのGoogle Docs
- スライド「ドットマトリクスフォント ― LCDフォントをデザインする ―」（2024、
  <https://drive.google.com/file/d/1Bo0ORbCIisVWQGSw4meRVjQMwItSoCZi/view>）：human ownerのGoogle DriveのPDF。行と列の
  パラメーター、フォントの作り方、ASCIIの表、Pythonのクラスと実体、Scratchのデザイナー、7セグの0〜F、VS Codeのショートカット
- `Naohiro2g/dotmatrix_font`：pygame-ceのデザイナー（v1.2.0）。pygameとマイクラで表示する
- `Naohiro2g/pygame_samples`：`lcd_font_pg.py`、`seven_seg_pg.py`。スライドがコードの取得先にしている
- `Naohiro2g/pygame_mcpi_LCD_7seg`（2021）：LCDフォントと7セグを、pygameとラズパイのマイクラに映す

## 6. まだ決めていないこと

- カリキュラムの置き場所（human owner 2026-11-26「まだきまっていない」）
- 12月末に何がそろえば完成とするか
- `pygame_samples`と`pygame_mcpi_LCD_7seg`の「なつめもじ」をどうするか（human ownerが決める）
