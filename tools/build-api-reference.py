#!/usr/bin/env python3
"""ホームページのAPI一覧（`30-広告宣伝/homepage/api/`）を生成する（`2026-09-30-05`）。

契約の中身（params、応答、備考、error reason）は`10-protocol/wire-format-design_ja.md`の§4コマンド表と§7.3 error表から
読む。`10-protocol/api-reference-metadata.json`は、載せる版、分類、一行の用途だけを持つ。wireの表とmetadataのmethodが
一致しなければ、生成せずに失敗する。`--check`は、生成済みのfileが今の入力から作り直したものと同じかを確かめる。
"""

from __future__ import annotations

import argparse
import html
import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
DEFAULT_WIRE = ROOT / "10-protocol" / "wire-format-design_ja.md"
DEFAULT_METADATA = ROOT / "10-protocol" / "api-reference-metadata.json"
DEFAULT_OUT = ROOT / "30-広告宣伝" / "homepage" / "api"
WIRE_URL = "https://github.com/Naohiro2g/mc-remote-knowledge/blob/main/10-protocol/wire-format-design_ja.md"


class BuildError(Exception):
    pass


def split_row(line: str) -> list[str]:
    body = line.strip().strip("|").replace("\\|", "\0")
    return [cell.strip().replace("\0", "|") for cell in body.split("|")]


def table_after(lines: list[str], heading_prefix: str) -> list[list[str]]:
    start = next((i for i, line in enumerate(lines) if line.startswith(heading_prefix)), None)
    if start is None:
        raise BuildError(f"見出しが見つかりません: {heading_prefix}")
    rows: list[list[str]] = []
    in_table = False
    for line in lines[start + 1:]:
        if line.startswith("#"):
            break
        if line.startswith("|"):
            in_table = True
            rows.append(split_row(line))
        elif in_table:
            break
    if len(rows) < 2:
        raise BuildError(f"表が見つかりません: {heading_prefix}")
    return rows[2:]


def unquote(cell: str) -> str:
    match = re.fullmatch(r"`([^`]+)`", cell)
    return match.group(1) if match else cell


def parse_wire(text: str) -> tuple[dict[str, dict[str, str]], list[dict[str, str]]]:
    lines = text.splitlines()
    commands: dict[str, dict[str, str]] = {}
    for row in table_after(lines, "## 4. コマンド表"):
        if len(row) != 4:
            raise BuildError(f"コマンド表の列数が4ではありません: {row}")
        method = unquote(row[0])
        commands[method] = {"params": row[1], "response": row[2], "notes": row[3]}
    errors: list[dict[str, str]] = []
    family = code = ""
    for row in table_after(lines, "### 7.3 "):
        if len(row) != 5:
            raise BuildError(f"error表の列数が5ではありません: {row}")
        family = row[0] or family
        code = row[1] or code
        errors.append({"family": family, "code": code, "reason": unquote(row[2]), "meaning": row[3], "introduced": row[4]})
    return commands, errors


def build_data(commands: dict[str, dict[str, str]], errors: list[dict[str, str]], meta: dict) -> dict:
    categories = {c["id"] for c in meta["categories"]}
    listed = [m["method"] for m in meta["methods"]]
    excluded = {e["method"] for e in meta.get("excluded", [])}
    problems: list[str] = []
    for method in commands:
        if method not in listed and method not in excluded:
            problems.append(f"wireの表にあるがmetadataに無いmethod: {method}")
    for entry in meta["methods"]:
        if entry["method"] not in commands:
            problems.append(f"metadataにあるがwireの表に無いmethod: {entry['method']}")
        if entry["category"] not in categories:
            problems.append(f"知らない分類: {entry['category']}（{entry['method']}）")
    if len(set(listed)) != len(listed):
        problems.append("metadataのmethodが重複しています")
    reasons = {e["reason"] for e in errors}
    excluded_reasons = {e["reason"] for e in meta.get("excluded_reasons", [])}
    for reason in sorted(excluded_reasons - reasons):
        problems.append(f"metadataで除外したreasonがwireのerror表に無い: {reason}")
    if problems:
        raise BuildError("\n".join(problems))
    methods = [
        {"method": e["method"], "category": e["category"], "purpose": e["purpose"], **commands[e["method"]]}
        for e in meta["methods"]
    ]
    return {
        "schema": "mc-remote.api-reference",
        "schema_version": 1,
        "release": meta["release"],
        "source": {"wire": "10-protocol/wire-format-design_ja.md §4, §7.3", "metadata": "10-protocol/api-reference-metadata.json"},
        "categories": meta["categories"],
        "methods": methods,
        "auth": meta.get("auth", {"methods": []}),
        "errors": [e for e in errors if e["reason"] not in excluded_reasons],
    }


def inline(text: str) -> str:
    escaped = html.escape(text, quote=False)
    escaped = re.sub(r"`([^`]+)`", r"<code>\1</code>", escaped)
    return re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", escaped)


def render_html(data: dict) -> str:
    release = data["release"]
    parts: list[str] = []
    for category in data["categories"]:
        rows = [m for m in data["methods"] if m["category"] == category["id"]]
        if not rows:
            continue
        body = "\n".join(
            "\t\t\t\t\t<tr>"
            f"<td class=\"method\"><code>{html.escape(m['method'])}</code></td>"
            f"<td>{inline(m['purpose'])}</td>"
            f"<td>{inline(m['params'])}</td>"
            f"<td>{inline(m['response'])}</td>"
            f"<td class=\"notes\">{inline(m['notes'])}</td>"
            "</tr>"
            for m in rows
        )
        parts.append(
            f"\t\t\t<h2 id=\"{category['id']}\">{html.escape(category['title'])}</h2>\n"
            "\t\t\t<div class=\"table-wrap\"><table>\n"
            "\t\t\t\t<thead><tr><th>method</th><th>用途</th><th>params</th><th>応答</th><th>備考（wireの記述）</th></tr></thead>\n"
            f"\t\t\t\t<tbody>\n{body}\n\t\t\t\t</tbody>\n\t\t\t</table></div>"
        )
    auth = data["auth"]
    auth_rows = "\n".join(
        f"\t\t\t\t\t<tr><td class=\"method\"><code>{html.escape(m['method'])}</code></td><td>{inline(m['purpose'])}</td></tr>"
        for m in auth.get("methods", [])
    )
    error_rows = "\n".join(
        "\t\t\t\t\t<tr>"
        f"<td><code>{html.escape(e['reason'])}</code></td><td>{inline(e['code'])}</td><td>{inline(e['family'])}</td>"
        f"<td>{inline(e['meaning'])}</td><td>{inline(e['introduced'])}</td></tr>"
        for e in data["errors"]
    )
    toc = " ／ ".join(
        f"<a href=\"#{c['id']}\">{html.escape(c['title'])}</a>"
        for c in data["categories"] if any(m["category"] == c["id"] for m in data["methods"])
    )
    title = f"API一覧（{release['label']} / protocol {release['protocol']}）"
    return f"""<!DOCTYPE html>
<html lang="ja">

<head>
	<meta charset="UTF-8" />
	<meta name="viewport" content="width=device-width, initial-scale=1.0" />
	<meta name="robots" content="index, follow" />
	<meta name="description" content="マイクラリモコン（mc-remote）の公開済みProtocol APIの一覧。{html.escape(release['label'])}（protocol {html.escape(release['protocol'])}）。" />
	<title>{html.escape(title)} — マイクラリモコン (mc-remote)</title>
	<link rel="stylesheet" href="../styles.css" />
	<style>
		.api-page {{ padding: 32px 0 64px; }}
		.api-page h2 {{ margin-top: 40px; }}
		.api-note {{ color: #475569; font-size: 0.9rem; }}
		.api-toc {{ margin: 16px 0 8px; line-height: 2; }}
		.table-wrap {{ overflow-x: auto; }}
		.api-page table {{ border-collapse: collapse; width: 100%; font-size: 0.9rem; }}
		.api-page th, .api-page td {{ border: 1px solid #cbd5e1; padding: 6px 8px; text-align: left; vertical-align: top; }}
		.api-page th {{ background: #f1f5f9; white-space: nowrap; }}
		.api-page td.method {{ white-space: nowrap; }}
		.api-page td.notes {{ color: #475569; }}
		.api-page code {{ word-break: break-word; }}
	</style>
</head>

<body>

	<header>
		<div class="container nav-container">
			<a href="../" class="brand-group">
				<img src="../images/mc-remote_com_logo.png" alt="Minecraft Remote" class="brand-logo" />
			</a>
			<nav>
				<ul>
					<li><a href="../#quickstart">はじめる</a></li>
					<li><a href="../#ecosystem">エコシステム</a></li>
					<li><a href="../#roadmap">ロードマップ</a></li>
					<li><a href="../#releases">リリース</a></li>
				</ul>
			</nav>
		</div>
	</header>

	<main class="api-page">
		<div class="container">
			<h1>{html.escape(title)}</h1>
			<p>公開済みのrelease {html.escape(release['label'])}（protocol {html.escape(release['protocol'])}、artifact {html.escape(release['artifact'])}、
				Minecraft {html.escape(release['minecraft'])}、{html.escape(release['published'])}公開）で使えるProtocol APIの一覧です。
				各言語のClient Libraryでの書き方は、それぞれのリポジトリを見てください。</p>
			<p class="api-note">このページは、仕様の正本<a href="{WIRE_URL}" target="_blank" rel="noopener">wire-format-design</a>の§4コマンド表と§7.3 error表から
				自動生成しています。正確な条件、検証の順序、上限は正本を見てください。<a href="api.json">機械可読版（api.json）</a></p>
			<p class="api-toc">{toc} ／ <a href="#auth">認証</a> ／ <a href="#errors">error reason</a></p>
{chr(10).join(parts)}
			<h2 id="auth">認証</h2>
			<p class="api-note">ペアリングとcredential管理は、表とは別に正本の{html.escape(auth.get('wire_sections', ''))}で定めています。</p>
			<div class="table-wrap"><table>
				<thead><tr><th>method</th><th>用途</th></tr></thead>
				<tbody>
{auth_rows}
				</tbody>
			</table></div>
			<h2 id="errors">error reason</h2>
			<p class="api-note">失敗したときは、JSON-RPCのerrorの<code>data.reason</code>で理由を見分けます。</p>
			<div class="table-wrap"><table>
				<thead><tr><th>reason</th><th>code</th><th>分類</th><th>意味</th><th>導入</th></tr></thead>
				<tbody>
{error_rows}
				</tbody>
			</table></div>
		</div>
	</main>

</body>

</html>
"""


def render_json(data: dict) -> str:
    return json.dumps(data, ensure_ascii=False, indent=2) + "\n"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="ホームページのAPI一覧を生成する")
    parser.add_argument("--wire", type=Path, default=DEFAULT_WIRE)
    parser.add_argument("--metadata", type=Path, default=DEFAULT_METADATA)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--check", action="store_true", help="生成済みのfileが最新かを確かめるだけで、書き込まない")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        commands, errors = parse_wire(args.wire.read_text(encoding="utf-8"))
        meta = json.loads(args.metadata.read_text(encoding="utf-8"))
        data = build_data(commands, errors, meta)
    except (BuildError, OSError, KeyError, json.JSONDecodeError) as error:
        print(f"FAIL: {error}", file=sys.stderr)
        return 1
    outputs = {"index.html": render_html(data), "api.json": render_json(data)}
    if args.check:
        stale = [name for name, content in outputs.items()
                 if not (args.out / name).exists() or (args.out / name).read_text(encoding="utf-8") != content]
        if stale:
            print(f"FAIL: 生成済みのfileが古い: {', '.join(stale)}（tools/build-api-reference.pyを実行する）", file=sys.stderr)
            return 1
        print(f"OK api reference methods={len(data['methods'])} errors={len(data['errors'])}")
        return 0
    args.out.mkdir(parents=True, exist_ok=True)
    for name, content in outputs.items():
        (args.out / name).write_text(content, encoding="utf-8")
    print(f"OK wrote {args.out} methods={len(data['methods'])} errors={len(data['errors'])}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
