# 世界定数をサーバーからクライアントに配る動機と展望

# 1. マイクラリモコンの歴史的変遷
ラズパイによるMCPIから始まり、Mod時代（1.12.2、1.16.5まで）を経て、現在はMcRemoteプラグイン（Paper+Geyser+ViaVersion）により、サーバーとクライアントの互換性と安定性が飛躍的に向上した。Mod時代およびプラグインによる前プロジェクト時代を通じて経験した教訓を活かし、環境依存の少ない基盤を構築している。

# 2. 開発哲学：安全な学習とデバッグの最適化
目指すのは「Scratchのようにエラーに阻まれず学べる環境」である。前述した各プロジェクト時代を通じて課題となっていたフィードバック不足に対し、適切なバランスを追求する。
具体的には、setBlock等のコマンドにデバッグスイッチを実装し、成功／失敗の理由を返信させる仕様を考える。サーバーからの全返信は建築の最高速を低下させるため、デバッグ時のみ返信を期待する「選択的デバッグ」を採用することで、パフォーマンスと学習の要点理解を両立させる。

# 3. ワールドデータ配布の核心：VS Codeでの自動補完と実ファイル化
世界定数をサーバーからクライアントへ配布する最大の動機は、開発者の体験最適化である。
VS Code等のIDEで強力な自動補完を享受するには、サーバーからデータを受け取るだけでは不十分である。クライアント側の環境において、世界定数が「実ファイル」として定数化・書き出されていることが不可欠である。この定数ファイルがIDEに認識されることで、初めて快適な自動補完が可能となる。

# 4. 環境スイッチング（熟練者向け特殊機能）
本プロジェクトでは、必要に応じて開発環境を切り替える「環境スイッチング」を新規導入する。
  - **基本仕様：**デフォルトでは、サーバー自身のバージョンに関する環境定数が提供され、ユーザーはその環境で開発を行う。
  - **応用仕様（熟練者向け）：**特定のプロジェクト要件（例えば、特定のModpack開発やマイグレーションテスト）により、サーバーに対して明示的なリクエストを送ることで、指定したバージョンの環境定数を取得・切り替えることが可能である。これにより、本来の対象外であるターゲットバージョンに対するマルチターゲット開発を実現する。

# 5. 今後の展望と戦略的選定基準
まずは、特定のツールで「快適な開発体験」を提供することが主眼である。
  - **言語展開の厳格な基準：**今後、Java、TS、Goなどの他言語展開を検討する際も、この「自動補完を含めた快適な環境」を提供できない場合は、その言語の採用を見送る。初学者が「余計な落とし穴」にはまらず、迷わずにコードを書ける環境を最優先する。
  - **インフラの未来：**箱庭サーバーの導入によりクライアントPCの負荷を低減させ、中高生の標準的なノートPCでも十分な開発環境を提供する。

# 6. LLM時代への展望
LLMアシスト時代において、最優先すべきは開発の効率や速度ではない。真の価値は、LLMが「解答を即座に提示するツール」から「学習を促す伴走者（メンター）」へと進化し、生徒の自律的な問題解決能力と論理的思考をいかに深く育めるかにある。本プロジェクトの環境情報を深く理解したLLMは、複雑なタスクに対しても単にコードを生成するのではなく、生徒が自力で答えに辿り着くための適切な示唆を与える役割を担う。また、現状の「VS Code等のIDEによる自動補完」への依存は、人間が快適に開発を行うための補助的な手段である。将来的には、LLMがプロジェクト全体の文脈を完全に把握することで、特定のIDEに縛られない「ツール・アグノスティック」な開発環境への移行を目指す。これは生徒がツールという「枠組み」から脱却し、プログラミングの本質に集中するための重要なステップとなる。今後も、現在の開発環境の品質を維持しつつ、LLMを教育的な伴走者として統合し、生徒の知的好奇心とエンジニアリングスキルの成長を支える環境構築を推進する。

# 7. LLM用コンテクスト
## Context for LLM
- Goal: Create an educational, error-free environment (Scratch-like) that fosters self-learning and problem-solving resilience.
- Target Users: Students acting as contributors to the open-source knowledge base; they require guidance over immediate solutions.
- Tech Stack: Paper + Geyser + ViaVersion (McRemote) with lightweight computational focus for student laptop environments.
- LLM Persona: Educational Mentor.
    - Priority: Guide students toward logical conclusions rather than providing instant code completions.
    - Error Handling: Transform errors into teaching moments; encourage "safe failure" exploration.
- Core Mechanism: Server-side world constants exported to client-side real files for IDE auto-completion.
- Advanced Capability: Multi-version environment switching.
- Language Policy: Must support high-quality auto-completion; LLM must adhere to project-wide efficient coding standards.
- Strategic Shift: From IDE-dependent (VS Code) development to Tool-agnostic (LLM-centric) development, ensuring students maintain core engineering skills.
