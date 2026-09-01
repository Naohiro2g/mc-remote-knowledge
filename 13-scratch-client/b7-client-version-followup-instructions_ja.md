# b7 Scratch client version follow-up指示書

> status: 実行待ち。最初のowner artifactで発見したb6表示identityをb7へ揃える。

## 発見と判断

Scratch owner artifact set 1はsource、digest、archive、test結果の返却条件を満たした。一方、固定source
`develop@773e2984132d82bb6e740d6458107fe42ef68a0a`の`MCREMOTE_CLIENT_VERSION`は
`2300.0.0b6`のままだった。この値は単なる未使用定数ではなく、次へ投影される。

- hello `params.client.version`
- Scratch GUI noticeのversion／running表示とAbout link label

protocol `23.1.0`を使うb7 Scratch Clientが自分をb6と送信・表示するため、non-claimでは受理しない。owner artifact set 1は
bytesと検証履歴を保持するが、b7 release artifactとして失効する。

## 固定入力

- repository: `Naohiro2g/scratch-editor`
- base: `develop@773e2984132d82bb6e740d6458107fe42ef68a0a`
- base tree: `e48fe82916ec82a5d05b216f50e353bcbf87a6f4`
- protocol: `23.1.0`（変更しない）
- Scratch Client artifact version: `2301.0.0b7`
- fixture SHA-256: `586d24bf40136eec31f1827f23ef5b317f15100a17a635d7fe9f165e0af40dce`（変更しない）
- branch: `agent/b7-client-version-followup`
- knowledge: この指示書を含むcommit

## 変更範囲

次の現行値だけを`2300.0.0b6`から`2301.0.0b7`へ更新する。

1. `packages/scratch-vm/src/extensions/scratch3_mcremote/client-version.js`
2. `packages/scratch-vm/test/unit/extension_mcremote.js`のhello期待値
3. `packages/scratch-gui/test/unit/components/notice-overlay.test.jsx`の表示／link期待値

base上の`2300.0.0b6`は上記三file、7箇所である。履歴文書や別versionを一括置換しない。

## 検証

- 変更三fileに`2300.0.0b6`が0件、`2301.0.0b7`が期待箇所だけ存在
- Scratch VMのMcRemote extension対象test PASS
- Scratch GUI notice overlay対象test PASS
- 変更fileのlint／Prettier PASS
- protocol test／build PASS、fixture bytes／93 case不変
- root production build PASS
- build成果物内で`2301.0.0b7`がhello client versionとGUI noticeへ投影され、`2300.0.0b6`が残らない
- `git diff --check` PASS

## Commit／push

baseから専用branchを作り、上記三fileだけをcommit／pushする。`develop`へ直接push／mergeしない。既存dirty worktreeを
変更、stash、cleanしない。

## 返却

- branch／commit／parent／remote一致／clean状態
- 変更三fileと7箇所の機械確認
- targeted test、lint／format、protocol、root build結果
- fixture identity不変
- production build内のb7表示／hello投影確認
- source、lockfile、Protocol、Bridge、WireScope、runtime config、OCI、Pagesを変更していないnon-claim

このfollow-upではowner artifactを正式固定しない。candidateがcoordinator照合後にdefault branchへfast-forwardされたら、
Scratch ownerが新default commitからartifact生成指示書を再実行し、artifact set 2を返す。
