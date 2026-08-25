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
| ブロックスタック | ブラウザ保存スプライト内で整理・再利用する | 初期 scope では独立ファイル化しない |

ブロックスタック単位の OS clipboard 移送は候補として残すが、先にブラウザ保存スプライトをスニペット棚として
評価する。1スプライト内へcomment付きの複数stackを置き、同じEditor originの別作品で読込・編集・再保存できる。

```text
作品全体
├─ ブラウザ保存作品 ── 作業継続・直近状態の復元
└─ .sb3 ファイル ───── 利用者管理の可搬コピー・長期保管手段

スプライト
├─ ブラウザ保存スプライト ── 同じ Editor origin 内で別作品へ再利用
└─ .sprite3 ファイル ─────── origin・browser・端末を越える移送

ブロックスタック
├─ ブラウザ保存スプライト ── 同じ Editor origin 内の整理・再利用
└─ OS clipboard 候補 ─────── 別 origin／stack単位移送の未充足時だけ再検討
```

同じ作品内のスプライト間 copy／paste は既存 Scratch の操作であり、新規 track ではない。別browser tab・別作品間は、
まずブラウザ保存スプライトで扱う。OS clipboard候補だけが持つ差は、Editor originを越えられることと、スプライト全体を
経由せずstack単位で移せることである。

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
| ブロックスタック | 同一originはブラウザ保存スプライトで評価。別origin／stack単位はOS clipboard候補を保留 |
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

## 7. ブロックスタックの copy／paste（保留）

OS clipboardによるblock stack移送は`deferred`とする。2026-08-25の実機確認では、ブラウザ保存スプライトを
別tabの作品で読込・確認・編集・再保存し、元tabの作品へ再読込できた。1スプライトへcomment付きstackを複数置けば、
カテゴリ別のスニペット棚として使える。現行Backpackの代替と、当初想定した同一origin内のtab／作品間移送を
一つの既存概念で満たせる可能性が高いため、先にこの運用を評価する。

現行のScratch／Blockly内copy状態はtab内memoryに閉じ、OS clipboardを使わない。OS clipboard案は削除せず、
次のいずれかが評価で実需として残った時に再開する。

- stable／alpha／beta等、異なるEditor origin間でstackを直接移す必要がある
- sprite全体の保存・読込ではstack単位の反復利用が明確に煩雑である
- `.sprite3`を介さず別browser profile／browserへ短時間で移す利用行動が成立する

再開時のcontractは、利用者の明示的なcopy／paste、server非経由、秘密非収容、有限bundle、strict検証を維持する。

- copy 元と paste 先の明示操作を必要とする
- copy 元から無関係なタブへ自動挿入しない
- server へ送らず、reload 後の永続性を要求しない
- account、Minecraft identity、Minecraft 接続を必要としない
- credential、接続先、token、WireScope data を含めない
- copy 元を変更・削除せず、Ctrl-X は初期 scope に含めない
- 欠落依存や unsupported block を黙って削除・別参照へ結び替えない

clipboard へ書き込む block transfer bundle は format identity、schema version、byte／block数／深さ上限、
strict 入力検証、block ID 再生成規則、依存関係、失敗表示を持つ。2026-08時点の技術調査では、web custom
clipboard formatはChromium 104以降で利用できる一方、全対象browserで共通の前提にはできない。再開時の
portable baselineは`text/plain`にmagic prefix付きのversioned JSON bundleを入れる方式とし、custom formatは
対応browserだけのprogressive enhancement候補とする。permissionと実browser matrixはprototype時に検証する。

外部根拠は[Chromeのweb custom format解説](https://developer.chrome.com/blog/web-custom-formats-for-the-async-clipboard-api)、
[WebKit standards position #43](https://github.com/WebKit/standards-positions/issues/43)、
[Mozilla standards position #525](https://github.com/mozilla/standards-positions/issues/525)を参照する。standards positionと
実装済みを同一視せず、WebKit側はposition未確定、Mozilla側はpositive positionだが実装可否はprototypeで確認する。

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

必要な利用行動は browser storage、`.sprite3`、`.sb3`でまず満たし、未充足時だけOS clipboardを再検討する。ブロック、スプライト、
作品を一つの棚 schema へ押し込まず、利用者へ新しい保存概念を増やさない。将来具体的な要求が成立した場合は、
旧計画の残作業としてでなく、新しい横断決定から再検討する。

Tutorial／Debug の既存 Scratch surface 再利用方針は維持する。

## 12. 実装順序

1. **ファイル互換 fixture**：`.sb3`／`.sprite3` の現行挙動、McRemote block、dependency、semantic
   round-trip、runtime 情報の非収容を固定する。
2. **ブラウザ保存作品**：IndexedDB lifecycle、quota、migration、破損表示等の共通基盤を作る。
3. **ブラウザ保存スプライト**：1 の `.sprite3` fixture と 2 の IndexedDB 基盤を入力にする。
4. **ブラウザタブ間 copy／paste（保留）**：3の運用評価で再開条件を満たした時だけ、OS clipboard prototypeと
   versioned transfer bundleを固定する。
5. **審査済み教材 artifact**：内容・権利・license・version・更新／撤回を確認して配布する。

各 track は独立に検収できるが、共有 contract を片方だけで独自に固定しない。`2026-08-21-02`／
`2026-08-25-04`により、1と2はb5 completion gateから外した独立entry gateとする。ここでいう
「b5後・b6 API本実装前」は依存と時期の目安であり、別trackのb6 API完了を待つ条件ではない。
同一slice内で1→2の依存を満たした後、3を続けて実装でき、b6 API実装と並行してよい。3は2の
IndexedDB databaseを共有してobject storeを分け、別の保存基盤を作らない。4は`2026-08-26-01`により
`deferred`とし、3の評価で別originまたはstack単位の未充足需要が観測された時だけ再開する。5は独立trackのまま
維持し、entry gate／b6へ自動追加しない。R3〜R5の意味と日程への配置は最後のR整理が所有する。

2026-08-25時点でscratch-editor `agent/wirescope-session-artifact@7d112a544e48391c70c627fd0c7f7572cf6810d6`は、
1〜3を同一sliceで実装し、deterministic testとlocalhost実browserでの人間確認まで完了したcandidateである。
作品の一覧／復元／削除はFile menu、個別スプライトの保存は右クリックmenu、保存済みスプライトの
一覧／復元／削除はFile menuに置く。これは搬送元の実装・観測範囲であり、正式evidence、default branch統合、
公開artifact、release完了を意味しない。

ブラウザ保存は耐久性を保証しない。WebKitは7日間のSafari利用中に該当siteへのuser interactionがなければ
script-writable storageを削除すると説明しており、Home Screen web appは別扱いとする。
`navigator.storage.persist()`もUAが許可した時だけpersistentに
なるため、唯一の退避策にしない。重要な作品／スプライトの`.sb3`／`.sprite3`退避を常に残す。外部根拠は
[WebKitのTracking Prevention](https://webkit.org/tracking-prevention/)と
[WHATWG Storage Standard](https://storage.spec.whatwg.org/)を参照する。

## 13. 未確定事項

- block transfer bundle schema、ID 再生成、dependency semantics
- `.sprite3` の browser 保存形式
- IndexedDB schema、quota、migration
- iPad Safari／Chromeでの作品・スプライト保存、一覧、復元、削除と、user interactionがない期間のeviction実測
- Home Screen追加時の保存挙動・Safariとのstorage分離の実測
- `navigator.storage.persist()`／`persisted()`のbrowser・profile・配信形態別の実効性と、状態表示・定期checkのUX
- unknown extension recovery と legacy minecraft migration
- `.sb3`／`.sprite3` McRemote compatibility fixture の実結果
- 教材 artifact の配布 profile
- provenance／attribution の将来設計

2026-08-26の搬送票では、scratch-editorの未commit worktreeで`storage_persist_enabled`とFile menuの永続化状態表示を
実装し、関連7 suite／76 testsとlintをPASSしたと報告された。Chrome／localhostでは`persist()`実行後も
`persisted()`が`false`で、bookmark、reload、再accessでも変わらなかったというlive-human観測がある。これは
その環境で永続化を前提にできない証拠であり、他browserで常に拒否される証明ではない。source commit identity、
7日間無操作の実地検証、iPad browser matrix、Home Screen差分、定期check routineは未確定のまま残す。

一般UGC hosting、`mc-remote-storage`、Backpack は継続作業として park しない。
