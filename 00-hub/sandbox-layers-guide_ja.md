# マイクラリモコンの「箱庭」とは何か

> 考え方の正本（`2026-11-28-01`⑤）。human ownerが2026-11-28に書いた「マイクラリモコンの「箱庭」とは何か」の日本語の部分。
> .NET箱庭のLTSの例（`dotnet-sb-lts.mc-remote.com`）は、マイクラ箱庭の行の形に合わせて足した（claude.aiの案）。英語の部分は、
> 言語方針の見直し（hub NOTES）を待つ。語の拘束は`00-hub/terms-glossary_ja.md`の「箱庭、参加アプリ、クライアント」。
> 公開の名前は`2026-11-28-02`、repoは`2026-11-28-03`。

**mc-remote（マイクラリモコン）** は、 **「箱庭」、「参加アプリ」、「クライアント（リモコン）」** の3層から構成されています。

## 3層構造の全体像

<table>
  <thead>
    <tr>
      <th>層</th>
      <th>役割</th>
      <th>本家マイクラ構成</th>
      <th>mc-remote構成</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>1. 箱庭</strong><br> (<code>Sandbox</code>)</td>
      <td>リモコン命令を受け付ける世界・サーバー</td>
      <td><strong>マイクラ箱庭</strong><br>（マイクラサーバー<br>＋<strong>mc-remoteサーバー</strong>）</td>
      <td><strong>.NET箱庭</strong><br>（.NETサーバー<br>＋<strong>mc-remoteサーバー</strong>）<br>※Rust箱庭 も検討中。</td>
    </tr>
    <tr>
      <td><strong>2. 参加アプリ</strong><br> (<code>App</code>)</td>
      <td>プレイヤーが箱庭に入って歩き回るためのアプリ</td>
      <td><strong>マイクラアプリ</strong><br>（Java版、統合版）</td>
      <td><strong>Unity Webアプリ</strong><br><strong>Bevy Webアプリ</strong><br> デスクトップ版も検討中。</td>
    </tr>
    <tr>
      <td><strong>3. クライアント</strong><br> (<code>Client</code>)</td>
      <td>ユーザーの建築コードを実行し、箱庭へ命令を送るリモコンツール</td>
      <td colspan="2" align="center"><strong>mc-remoteクライアント</strong><br>（Scratch / Python / Rust /<br> Java / TypeScript / C# など）</td>
    </tr>
  </tbody>
</table>

---

## 各用語の定義

### 1. 箱庭（世界・サーバー）

リモコン命令で自由にブロックを置いたり動かしたりできる「箱庭＝砂場＝ワールド」と、その状態を管理するサーバーを指します。

* **マイクラ箱庭** ：本家 Minecraft サーバーに、 **mc-remoteプラグイン（サーバー）** を導入した環境。<br>― C2CC（Code2Create.Club）公開環境の例： （最新版）`sb.mc-remote.com`, （LTS版）`sb-lts.mc-remote.com`
* **.NET箱庭** ：`.NET` で実装された独自の世界サーバーに、**mc-remoteサーバー機能** を統合した環境。<br>― C2CC（Code2Create.Club）公開環境の例： （最新版）`dotnet-sb.mc-remote.com`, （LTS版）`dotnet-sb-lts.mc-remote.com`
* **Rust箱庭** ：同様に、Rust実装も検討中。

### 2. 参加アプリ（描画・操作）

箱庭に接続し、3D空間の描画や視点移動・歩行を行うフロントエンドを指します。フロントエンドとはユーザーが直接操作する「端」のことで、一般的にはクライアントとも呼ばれますが、マイクラリモコンでは混乱を避けるため『アプリ』と呼びます。

* **マイクラアプリ**：本家 Minecraft アプリ。
* **mc-remoteアプリ**：`.NET箱庭` などの **mc-remote** 構成の箱庭へ接続するための描画アプリ。実装エンジンと配布形態で以下のように区別します。
  * **Unity Webアプリ**<br>― C2CC（Code2Create.Club）公開環境の例： （最新版）https://unity-app.mc-remote.com/, （LTS版）https://unity-app-lts.mc-remote.com/
  * **Unityデスクトップアプリ**
  * **Bevy Webアプリ**
  * **Bevyデスクトップアプリ**

### 3. mc-remoteクライアント・建築コード

* **クライアント**：箱庭へコマンドを送信するAPIライブラリ・実行環境（Scratch / Python / Rust / Java / TypeScript / C# など）。参加／描画側と区別するため、「クライアント」はこの層のみを指します。C2CC（Code2Create.Club）公開環境の場合、箱庭の `sb.mc-remote.com` や `dotnet-sb.mc-remote.com` などに接続します。
* **建築コード**：ユーザーが各言語のクライアントAPIを使って書くコード本体。接続先の箱庭（本家マイクラ／.NET箱庭）が変わっても、同じ建築コードをそのまま動かせることを目指します。

---
