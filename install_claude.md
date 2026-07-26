## apt で入れる

  sudo apt update
  sudo apt install -y curl ca-certificates gnupg git

  sudo install -d -m 0755 /etc/apt/keyrings
  sudo curl -fsSL https://downloads.claude.ai/keys/claude-code.asc \
    -o /etc/apt/keyrings/claude-code.asc

  gpg --show-keys /etc/apt/keyrings/claude-code.asc

  fingerprint がこれと一致することを確認します。
  31DD DE24 DDFA B679 F42D 7BD2 BAA9 29FF 1A7E CACE


  stable 版を入れるなら:

  echo "deb [signed-by=/etc/apt/keyrings/claude-code.asc] https://downloads.claude.ai/claude-code/apt/stable stable main" \
    | sudo tee /etc/apt/sources.list.d/claude-code.list

  sudo apt update
  sudo apt install -y claude-code

  確認:

  claude --version
  claude doctor

  ヘッドレスでログイン

  claude

  ブラウザが開けない SSH / headless 環境では、表示されたログイン URL を手元のPCのブラウザで開きます。ログイン後にコードが表示された場合は、ターミナルの Paste code here if prompted に貼り付
  けます。

