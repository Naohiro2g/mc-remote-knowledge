Ubuntu 24.04 のヘッドレスに、Codex CLI をインストール

　0．デバイスコード認証を有効に

　　ブラウザでclaude.aiを開き、
　　設定で、セキュリティとログイン／Codex に対してデバイスコード認証を有効にする　をスイッチオン。

  1. 依存パッケージ準備（以降、ターミナルで）

  sudo apt update
  sudo apt install -y curl ca-certificates git bubblewrap apparmor-profiles apparmor-utils
  sudo install -m 0644 /usr/share/apparmor/extra-profiles/bwrap-userns-restrict /etc/apparmor.d/bwrap-userns-restrict
  sudo apparmor_parser -r /etc/apparmor.d/bwrap-userns-restrict

  2. Codex CLI をインストール

  curl -fsSL https://chatgpt.com/codex/install.sh | CODEX_NON_INTERACTIVE=1 sh
  export PATH="$HOME/.local/bin:$PATH"

  確認:

  codex --version
  codex doctor

  3. ヘッドレス device code 認証でログイン

  codex login --device-auth

  表示された URL をクリックして、手元のブラウザで開き、コードを入力。
