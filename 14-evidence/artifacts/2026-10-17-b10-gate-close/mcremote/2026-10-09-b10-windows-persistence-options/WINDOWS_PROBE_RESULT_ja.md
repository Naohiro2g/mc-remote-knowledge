# Windows DirectoryForceProbe の実機結果

- knowledge contract path: `00-hub/b10-gate-live-test-instructions_ja.md` Windows の診断、`00-hub/release-gate-notes_ja.md` b10。
- knowledge contract commit: `8c3a31a967731a81c91645b08ecff62f620d0fe4`。
- test class: live-human。human owner による実機操作報告。agent による Windows 操作ではない。
- 受領日: 2026-10-09。

human owner の報告:

> Windows実機で診断しました（Windows 11、Microsoft Build of OpenJDK 21.0.12.1+1-LTS、使用JARはcandidateと同じ60ca6e17…3ef7）。DirectoryForceProbeはstage=open-directory-read、java.nio.file.AccessDeniedException（WindowsFileSystemProvider.newFileChannel）で、静的点検の原因候補が確定しました。

実機 JAR が candidate SHA-256 `60ca6e17fb89ed8474e2341d710c23ab62f4ddfd366c49afc1d233f6526c3ef7` と同じ、という human owner の照合報告として扱う。agent が Windows 上の bytes を独立取得・再 hash したものではない。

静的点検で挙げた directory READ open の Windows 非互換が実機診断でも再現された。OS の保護／mise／Java 21 と 25 の取り違えを直接原因として扱わない。正常化済みの報告ではない。

probe の raw 全出力、exact Windows build、Paper exact build はこの追記では未受領。正式 evidence の配置・ID 採番は knowledge coordinator に返す。
