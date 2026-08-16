# Scratch 作品の保存・移送設計

この文書は、Scratch 作品とスプライトをどこへ保存し、どう別の作品・ブラウザ・端末へ移すかを説明する。
一般利用者の作品を McRemote が預かって公開する service は持たない。作品共有の責任分界、一般利用者 account の
非所有、保存・移送モデルの拘束は `2026-08-16-01`〜`2026-08-16-03` を正本とする。

## 1. 骨格

McRemote が提供するのは、**利用者の手元で作品を残し、必要な粒度で持ち運ぶ経路**である。
一般利用者の作品を集める投稿 community や cloud project store は提供しない。

保存は「対象」と「媒体」の二軸で見る。

| 保存対象 | ブラウザ保存 | ファイル保存 |
| --- | --- | --- |
| 作品全体 | IndexedDB 内のブラウザ保存作品 | `.sb3` |
| スプライト | IndexedDB 内のブラウザ保存スプライト | `.sprite3` |
| ブロックスタック | 永続保存しない | 初期 scope では独立ファイル化しない |

ブロックスタックは OS clipboard を介した明示的な copy／paste で一時的に移す。

```text
作品全体
├─ ブラウザ保存作品 ── 作業継続・直近状態の復元
└─ .sb3 ファイル ───── 利用者管理の可搬コピー・長期保管手段

スプライト
├─ ブラウザ保存スプライト ── 同じ Editor origin 内で別作品へ再利用
└─ .sprite3 ファイル ─────── origin・browser・端末を越える移送

ブロックスタック
└─ OS clipboard による copy／paste ── 対応 McRemote Editor 間の一時移送
```

同じ作品内のスプライト間 copy／paste は既存 Scratch の操作であり、新規 track ではない。新規候補は、
別ブラウザタブで開いた対応 McRemote Editor 間の copy／paste である。

## 2. 作品共有の責任分界

作品共有または提出に必要な管理を、子ども本人だけへ負わせない。共有手段を選択・運用する保護者、学校、
教室運営者、団体または成人利用者が、少なくとも次を管理する。

- 使用を認める提出・共有手段
- 作品内容の確認
- 著作権、利用許諾、credit
- 写真、録音音声、肖像、個人情報
- 保存期間と削除方法
- 問題発生時の連絡先と対応者

McRemote は一般 UGC hosting または提出 service を提供して、この管理を代行しない。一方、McRemote 自身は
次を所有する。

- runtime secret を作品・スプライト・clipboard bundle へ含めない
- 保存・移送形式の互換境界を説明する
- browser storage の origin／profile 境界を説明する
- 外部共有でも内容・権利確認が必要であることを説明する
- teacher checklist へ責任分界を投影する
- McRemote 自身が提供する教材 artifact を審査する

教室内の作品提出という利用行動は撤回しない。学校または運営者が認めた手段で `.sb3`、`.sprite3`、画像等を
受け渡せるが、McRemote 独自の提出 server は作らない。特定の外部 provider を正典共有先にせず、Editor から
特定 provider へ直接 upload する経路や、その account／credential を扱う経路も作らない。

外部 provider の利用は、権利、privacy、内容確認の問題自体を解消しない。本節は法域別の法的義務を最終判断
するものではなく、McRemote product が所有する機能と運用責務を示す。

## 3. 一般利用者 account を持たない

McRemote は一般利用者向け独自 account、作品投稿者 account、公開 profile、作品共有 community を所有しない。
ただし、次の目的限定 identity／capability は維持できる。

- deployment 単位の HTTP 認証
- 学校・運営者が所有する access control
- 教室内の短命・限定的 capability
- operator 管理面
- Minecraft pairing identity と McRemote credential
- WireScope target／stream／display alias
- browser-local project／sprite identity

これらを作品作者 identity、公開 profile、作品共有 account、server-side owner identity へ昇格させない。
将来一般利用者 account が必要になった場合は、旧 cloud 計画の再開ではなく、新しい要求・横断決定・人間批准から
始める。

## 4. browser storage の境界

ブラウザ保存作品とブラウザ保存スプライトは、同一 browser storage partition かつ同一 Editor origin に閉じる。
境界を決めるのは Minecraft 接続先ではなく、Scratch Editor を配信する origin である。

- 同じ Editor origin では、Minecraft 接続先を変更しても同じ保存物を参照する
- browser-local project／sprite identity を Minecraft 接続先へ binding しない
- stable／alpha／beta が別 origin なら、保存物は自動共有されない
- 別 browser profile、private mode、別端末へ自動同期しない
- browser storage を account 保存、永久保存、端末間同期と説明しない

origin 境界を越える正式な移送手段は次とする。

| 移送対象 | 手段 |
| --- | --- |
| ブロックスタック | OS clipboard による copy／paste |
| スプライト | `.sprite3` |
| 作品全体 | `.sb3` |

## 5. ブラウザ保存作品

ブラウザ保存作品は、IndexedDB 内に作品 snapshot を保持する。目的は自動保存、作業継続、直近状態の復元、
複数作品の管理である。

- browser eviction や quota の影響を受け得ることを表示する
- 大切な作品は `.sb3` へ退避できるようにする
- credential、接続先、token、WireScope data を含めない
- serialization 失敗時に last-known-good snapshot を壊さない
- quota 不足時に既存作品を暗黙削除しない

本節は contract であり、実装済みを意味しない。IndexedDB schema、autosave lifecycle、migration、破損表示、
Safari を含む E2E は Scratch 実装側で固定する。

## 6. ブラウザ保存スプライト

利用者が明示的に選んだスプライトを、同じ browser storage partition・Editor origin 内で別作品へ再利用できる
ように保存する。

- browser-local、account 不要、server 同期なし
- 公開一覧・第三者共有を持たない
- 一覧、読込、名前変更、削除を可能にする
- quota 不足時に既存スプライトを暗黙削除しない
- eviction され得ることを説明する
- 重要なスプライトは `.sprite3` へ退避できる
- credential、接続先、token、WireScope data を含めない

保存形式は `.sprite3` 相当の serialization を第一候補とする。ただし、既存 export／import 経路をそのまま
利用できるとは fixture 前に確定しない。

作品保存とスプライト保存は IndexedDB lifecycle、quota、migration、破損表示等の基盤を共有する。一方、
作品 snapshot とスプライトを同じ schema へ押し込まず、object store または record kind を分離する。

## 7. ブロックスタックの copy／paste

対応する McRemote Editor 間で、利用者が明示的に copy したブロックスタックを OS clipboard を介して別作品へ
paste できることを目標とする。同一 origin だけでなく、stable／alpha／beta 等の別 origin で配信される対応
McRemote Editor 間を扱える contract とする。

- copy 元と paste 先の明示操作を必要とする
- copy 元から無関係なタブへ自動挿入しない
- server へ送らず、reload 後の永続性を要求しない
- account、Minecraft identity、Minecraft 接続を必要としない
- credential、接続先、token、WireScope data を含めない
- copy 元を変更・削除せず、Ctrl-X は初期 scope に含めない
- 欠落依存や unsupported block を黙って削除・別参照へ結び替えない

clipboard へ書き込む block transfer bundle は format identity、schema version、byte／block数／深さ上限、
strict 入力検証、block ID 再生成規則、依存関係、失敗表示を持つ。具体的な Clipboard API、custom MIME、
text fallback、permission、browser compatibility は prototype と fixture で後続確定する。

現行公式 Scratch は OS clipboard へ block data を書き込まないため、公式 Scratch との直接 copy／paste は
初期 contract に含めない。

## 8. `.sprite3` と `.sb3`

### `.sprite3`

標準的な `.sprite3` export／import 経路を、スプライトを origin・browser・端末の外へ持ち出す手段として使う。
コード、sprite-local state、costume、sound をまとめられるが、stage、他 sprite、project-global dependency が
必要な場合がある。完全に自己完結した作品とは説明しない。

McRemote 独自 wrapper や独自拡張子へ包まず、credential、接続先、token、WireScope session を含めない。
既存機能の存在と McRemote 互換合格を同一視せず、McRemote block、入力値、comment、変数、list、broadcast、
custom block、costume、sound、ID 衝突、再 import を fixture で確認する。

### `.sb3`

`.sb3` は作品全体を利用者が所有し、移送する出口である。Scratch 3 の通常 container を使い、McRemote 独自
wrapperを作らない。credential、接続先、token、WireScope data を含めず、対応する McRemote Editor へ
持ち込み直せることを fixture で支える。

McRemote block を含む作品が公式 Scratch で必ず開けるとは保証しない。ファイル保存は長期保管に利用できるが、
消失しないことを McRemote が保証するものではない。

## 9. ロックイン回避

ロックイン回避を、公式 Scratch との完全互換だけへ預けない。次を一組として支える。

- 利用者が `.sb3`／`.sprite3` を所有できる
- McRemote fork と対応 source が公開されている
- 再現可能な構築手順がある
- 互換 fixture がある
- 独立した運営者が private archive や個別の暗黙知なしに再構築できる

全利用者が self-host することは前提にしない。ただし、独立した運営者が公開手順だけで setup・開始・復旧
できない場合は、ロックイン回避の gate を満たしたとはみなさない。この実測は `2026-07-16-05` の共通基盤・
支援者 gate と接続する。

## 10. 来歴・license・remix

save／load、copy／paste、スプライト移送が、元作品との関係や作者情報を自動保存するとはみなさない。
これらは技術的な保存・移送であり、remix lineage、作者・出典の自動判定、再配布権、新しい license の付与、
ファイル保有者と作者の同一性を保証しない。

維持できる既存 comment や明示的 credit を黙って削除しない。McRemote が公開する審査済み教材 artifact は
一般利用者の保存物と分け、内容、作者・作成主体、素材の権利、license／credit、対応 version、artifact identity、
更新・撤回方法を確認する。

現行 Scratch 利用規約だけから、他利用者の作品を McRemote 上で保存・再配布する包括的権利を導出しない。
外部事実は `F-scratch-user-content-license`、project 内の license 表示・配布 gate は `2026-07-21-02`／
`2026-08-11-01`を参照する。

## 11. Backpack と cloud project store を持たない

`2026-07-12-07` で決めた IndexedDB＋BroadcastChannel の検索・pin棚としての Backpack 方向は撤回する。
一般UGC hosting、匿名 cloud snapshot、`/project/<id>`、`mc-remote-storage` も現行計画から撤回する。

必要な利用行動は browser storage、OS clipboard、`.sprite3`、`.sb3` で個別に満たせる。ブロック、スプライト、
作品を一つの棚 schema へ押し込まず、利用者へ新しい保存概念を増やさない。将来具体的な要求が成立した場合は、
旧計画の残作業としてでなく、新しい横断決定から再検討する。

Tutorial／Debug の既存 Scratch surface 再利用方針は維持する。

## 12. 実装順序

1. **ファイル互換 fixture**：`.sb3`／`.sprite3` の現行挙動、McRemote block、dependency、semantic
   round-trip、runtime 情報の非収容を固定する。
2. **ブラウザ保存作品**：IndexedDB lifecycle、quota、migration、破損表示等の共通基盤を作る。
3. **ブラウザ保存スプライト**：1 の `.sprite3` fixture と 2 の IndexedDB 基盤を入力にする。
4. **ブラウザタブ間 copy／paste**：OS clipboard prototype と versioned transfer bundle を固定する。
5. **審査済み教材 artifact**：内容・権利・license・version・更新／撤回を確認して配布する。

各 track は独立に検収できるが、共有 contract を片方だけで独自に固定しない。`2026-08-16-09`により、
1と2をb5、3をb6へ配置する。b6はb5のIndexedDB lifecycle、quota、migration、破損表示を再利用し、
スプライト用に別の保存基盤を作らない。4と5は独立trackのまま維持し、b5／b6へ自動追加しない。
R3〜R5の意味と日程への配置は最後のR整理が所有する。

## 13. 未確定事項

- Clipboard API、custom MIME、text fallback、browser compatibility
- block transfer bundle schema、ID 再生成、dependency semantics
- `.sprite3` の browser 保存形式
- IndexedDB schema、quota、migration
- unknown extension recovery と legacy minecraft migration
- `.sb3`／`.sprite3` McRemote compatibility fixture の実結果
- 教材 artifact の配布 profile
- provenance／attribution の将来設計

一般UGC hosting、`mc-remote-storage`、Backpack は継続作業として park しない。
