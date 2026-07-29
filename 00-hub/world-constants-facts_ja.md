# マイクラの世界定数

- y_groundは地面に立つプレイヤーの下半身の標高
- y_sea, y_lavaはそのひとつ下のブロックの標高
- y_cloudは雲（厚さ4ブロック）の最下段ブロックの標高
- steve_min_y, steve_max_yはプレイヤー下半身の標高の最小値・最大値
- steve_max_yは（今の所）常にy_max + 1である。
- **スーパーフラットは非対応**：Paper サーバ API では稼働中ワールドが superflat かどうかを高信頼に自己判定できず、hello の `world_constants` は world_type を問わず通常世代表（`overworld.modern` 等）の該当行のみを返す。`overworld_superflat` 系列の行は非対応系列の参考値であり、superflat を使う利用者は Y オフセット等の食い違いを自分で扱う（`2026-07-30-02`）。

コーディングの際は基本的にこれらの実値そのものを意識する必要はないが、クライアント側に通知されて、実ファイル化などによりIDEで補完可能状態になっていれば、知りたいときに確認できるようになる。
人間がこのファイルを直接読めば良い、ということかも知れない。

{
  "minecraft_world_constants": {
    "overworld": {
      "modern": {
        "description": "1.18 - latest",
        "y_steve_max": 320,
        "y_max": 319,
        "y_cloud": 192,
        "y_ground": 63,
        "y_sea": 62,
        "y_min": -64,
        "y_steve_min": -64
      },
      "legacy": {
        "description": "1.12.2 - 1.17",
        "y_steve_max": 256,
        "y_max": 255,
        "y_cloud": 128,
        "y_ground": 63,
        "y_sea": 62,
        "y_min": 0,
        "y_steve_min": 0
      },
      "mcpi": {
        "description": "Raspberry Pi Edition",
        "y_steve_max": 64,
        "y_cloud": 64,
        "y_max": 63,
        "y_ground": 0,
        "y_sea": -1,
        "y_min": -64,
        "y_steve_min": -64
      }
    },
    "overworld_superflat": {
      "modern": {
        "description": "1.18 - latest - classic",
        "y_steve_max": 320,
        "y_max": 319,
        "y_cloud": 192,
        "y_ground": -60,
        "y_sea": null,
        "y_min": -64,
        "y_steve_min": -64
      },
      "legacy": {
        "description": "1.12.2 - 1.17 - classic",
        "y_steve_max": 256,
        "y_max": 255,
        "y_cloud": 128,
        "y_ground": 4,
        "y_sea": null,
        "y_min": 0,
        "y_steve_min": 0
      },
      "mcpi": null
    },
    "nether": {
      "modern": {
        "description": "1.18 - latest",
        "y_steve_max": 256,
        "y_max": 255,
        "y_cloud": null,
        "y_ground": 32,
        "y_lava": 31,
        "y_min": 0,
        "y_steve_min": 0
      },
      "legacy": {
        "description": "1.12.2 - 1.17",
        "y_steve_max": 256,
        "y_max": 255,
        "y_cloud": null,
        "y_ground": 32,
        "y_lava": 31,
        "y_min": 0,
        "y_steve_min": 0
      },
      "mcpi": null
    },
    "the_end": {
      "modern": {
        "description": "1.18 - latest",
        "y_steve_max": 256,
        "y_max": 255,
        "y_cloud": null,
        "y_ground": null,
        "y_fluid": null,
        "y_min": 0,
        "y_steve_min": 0
      },
      "legacy": {
        "description": "1.12.2 - 1.17",
        "y_steve_max": 256,
        "y_max": 255,
        "y_cloud": null,
        "y_ground": null,
        "y_fluid": null,
        "y_min": 0,
        "y_steve_min": 0
      },
      "mcpi": null
    }
  }
}
