# b10 Windows live-human 障害の追記（knowledge／McRemote向け）

- knowledge contract path: `00-hub/b10-gate-live-test-instructions_ja.md`、`00-hub/release-gate-notes_ja.md` b10、`15-wirescope/wirescope-deployment-design_ja.md` §5・§6
- knowledge contract commit: `7d1b3809b0987f7fc0e5c5c2f365a42e9046e240`
- 搬送元: scratch-editor `agent/b10-scratch-local@c717d0c2ed9b045b8c3bb925b0e1fcd8ee33010b`
- test class: human ownerのWindows操作報告はlive-human。ZIP内部の調査はstatic inspection。
- Scratch identity: CI run `37808012407`、artifact ID `11563852835`、Windows ZIP 260361934 bytes／SHA-256 `08340c801c1196c30a1227a7e495feb32131a95e4816ffbb29278557cadab9c1`
- McRemote: human ownerはb10と報告。今回のWindows実使用JARのhashは未採取。実施票のcandidateは282260 bytes／SHA-256 `60ca6e17fb89ed8474e2341d710c23ab62f4ddfd366c49afc1d233f6526c3ef7`。

## 1. credential初期化と認証ONでの接続（McRemote担当への調査依頼）

- Windows 11、Paper 1.21.11。human ownerがランチャーで初回起動し、警告は出なかったと報告。Smart App Controlの状態、ブラウザ、exact OS／Paper buildは未採取。
- pair codeが発行され、認証された旨の表示になるが、Scratchの接続は完了しないとの報告。
- server startup logはsnapshotとauthority_manifestの欠如、新domainの初期化開始、その後のfail-closed intermediate state、credential domain `UNHEALTHY`を示す。
- configの認証をOFFにして試すと接続し、hello worldの送信に成功したとの報告。wire hello payloadは未採取。認証ONが実施条件なので、この迂回で認証試験のPASSとはしない。
- 原因の分かる例外／stack trace、credential fileの状態と初期化失敗の理由はこの3行には無い。Windows file操作や権限が原因と断定しない。credential実値は搬送しない。
- 依頼: McRemote担当でWindowsの新domain初期化失敗を調査し、認証ONで正常化する手順または修正の必要性を返してほしい。Scratch担当はcredential fileの削除・初期化や他repo変更を実施していない。
- 素材: `WINDOWS_CREDENTIAL_STARTUP_SANITIZED.txt`（home pathを`~`へ置換）。

## 2. 独立WireScopeリンクが出ない（Scratch担当の調査結果）

- human ownerが認証OFFで接続・hello world成功後、WireScopeへのリンクが表示されないと報告。
- 固定Windows ZIP本体のbytes／SHA-256／sourceを再照合し一致。内部`app/launcher.mjs`のruntime configに`wirescope_url`が無い。
- GUIは接続済み・display aliasあり・WireScope URLありのときにリンクを表示する。未指定URLはnullになるため、現在のScratch Localではリンクが出ない。
- ZIP builderはGUI、Bridge、Nodeとlauncherを収めるが、独立WireScope appを取得・同梱していない。3 OSの固定ZIPでも同じ欠落を静的に確認した。実機でのリンク欠落の報告はWindowsのみ。
- 修正案: lockで固定済みの共通WireScopeを同梱し、Scratchとは別のloopback originで配信、runtime configにURLを設定する。共通appの別origin handoffをそのまま使い、common toolingのowner sourceやwireを変えない。
- 修正後はZIPのbytes／SHA-256とcandidate sourceが変わる。coordinatorに新candidateと実施票の更新を返す。既存の初回警告観測を引き継ぐかはcoordinatorの判断とする。
- 素材: `WINDOWS_LOCAL_STATIC_INSPECTION.json`、`LOCAL_WIRESCOPE_STATIC_INSPECTION.json`。

## 現在の境界

- 固定candidateと3 ZIPを変更していない。公開・deploy・tag・Releaseなし。
- 認証ONでの接続、独立WireScopeの実画面、Windows再起動／LAN、macOS／UbuntuのScratch Local操作は未確認。
- 正式evidenceのauthoring・配置と横断gate判定はknowledge coordinatorへ返す。本directoryは観測素材である。
