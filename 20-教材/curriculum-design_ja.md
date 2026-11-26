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

## 6. これまでの記録とのつながり

- [学習支援の設計](ai-learning-design_ja.md)の「12. APIを最終成果にする3年間カリキュラム」（`2026-07-16-05`）：2027年4月から
  の講座の道筋。共通のPythonの基盤と、選べるマイクラリモコンの層に分け、依存、package、testは後の段で少しずつ見せる。
  このカリキュラムは、その手前の教材を整える
- 同じ文書の緑の旗の扱い：最初は足場（方便）として旗を使い、イベントを学んだ後に、対等なイベントの一つとして捉え直す。
  最初に支えて後で外す形は、§1と同じ
- 同じ文書の「全ては投影で扱う」（2026-06-30）：合わせる単位は人ではなく「テーマ × 現在地 × 作業」
- カリキュラムは、テーマごとの勾配を時間の軸に伸ばしたもの（2026-06-23のNOTES。アーカイブから持ち出した）：貢献者に
  合わせることと、Scratch → Python → API → server／clientを登る学習者に合わせることは、同じ問題である。表現の合わせ方、
  貢献者の参加、学習カリキュラムを、別々に持たずに一本にまとめる
- 学習カリキュラムは強くオープンにする（2026-06-22のNOTES。アーカイブから持ち出した）：ノウハウが外へ出ることより、
  広まることを取る。新しい方向は自分たちで見つけ、付加価値を付けられるという前提

アーカイブから持ち出した2つと、§7の教材プールの案は、どれもNOTESの段階の案で、決定ではない。今も合うかは、置き場所を
決めるときに一緒に問う。

## 7. まだ決めていないこと

- カリキュラムの置き場所（human owner 2026-11-26「まだきまっていない」）。候補：
  - `mc_remote_samples`：同じconceptを言語ごとに比べる学習面（`2026-08-30-01`、
    [Client sampleの配置と多言語学習UX](client-sample-learning-ux_ja.md)）
  - 教材プール（2026-06-29のNOTES。アーカイブから持ち出した）：教材の実物の正本を「教材プールrepo」に集め、トピックと
    カリキュラムの軸で並べ、Scratch、Pythonなどのclientはタグにする。dev repoのexamplesとブログは、そこから選んで写した
    もの（投影）にする。却下していたのは、dev repoを教材の正本にする案（横断する題材の置き場が無くなる）と、教材の本体を
    knowledgeに置く案（結論ものの境界が崩れる）
- 12月末に何がそろえば完成とするか
- `pygame_samples`と`pygame_mcpi_LCD_7seg`の「なつめもじ」をどうするか（human ownerが決める）
