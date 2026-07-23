#!/usr/bin/env python3
"""Gemini Notebook（旧NotebookLM）取り込み用バンドルをcommit treeから生成する。"""

from __future__ import annotations

import argparse
import posixpath
import re
import subprocess
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = REPO_ROOT / "dist" / "notebooklm"
INDEX_PATH = "00-hub/INDEX_ja.md"
ROADMAP_PATH = "00-hub/grand-design-roadmap_ja.md"
CURRENT_STATE_CAPSULE_FILENAME = "00-current-state-capsule.md"
CURRENT_STATE_SECTIONS = (
    (2, "現在地"),
    (2, "4. 現在の横断優先"),
)

ALWAYS_EXCLUDE_DIRS = {".git", "dist", "tools", "node_modules"}
SUMMARY_ONLY_PATHS = {"memo_codex.md", "memo_codex_audit.md"}
SUMMARY_MAXLEN = 140
GENERATED_MARKERS = (
    "これは自動生成物です",
    "tools/build-notebooklm-bundle.py",
)


class BundleBuildError(RuntimeError):
    """正本投影または安全な出力を保証できないときの生成停止。"""


def git_output(*args: str) -> str:
    """Gitを実行し、失敗時はworking treeへフォールバックせず停止する。"""
    try:
        completed = subprocess.run(
            ["git", "-C", str(REPO_ROOT), *args],
            capture_output=True,
            text=True,
            check=True,
        )
    except FileNotFoundError as exc:
        raise BundleBuildError(
            "gitが見つからないため、commit treeから生成できません。"
        ) from exc
    except subprocess.CalledProcessError as exc:
        detail = exc.stderr.strip() or exc.stdout.strip() or "git command failed"
        raise BundleBuildError(f"git {' '.join(args)}: {detail}") from exc
    return completed.stdout.rstrip("\n")


def resolve_commit(source_ref: str) -> str:
    """tag・branch・SHAをimmutableなcommit SHAへ解決する。"""
    return git_output("rev-parse", "--verify", f"{source_ref}^{{commit}}")


def snapshot_meta(commit: str) -> tuple[str, str]:
    """commit由来のスナップショット日時と短縮SHAを返す。"""
    sha = git_output("rev-parse", "--short", commit)
    iso = git_output("show", "-s", "--format=%cI", commit)
    return iso, sha


def read_commit_text(commit: str, rel_posix: str) -> str:
    """working treeでなく指定commitのblobを読む。"""
    return git_output("show", f"{commit}:{rel_posix}") + "\n"


def parse_index_summaries(index_text: str) -> dict[str, str]:
    """INDEXのpath・役割表をrepo-root相対pathから概要への辞書にする。"""
    summaries: dict[str, str] = {}
    link_row = re.compile(
        r"^\|\s*\[[^\]]+\]\(([^)]+)\)\s*\|\s*([^|]+?)\s*\|"
    )
    code_row = re.compile(r"^\|\s*`([^`]+)`\s*\|\s*([^|]+?)\s*\|")
    for line in index_text.splitlines():
        match = link_row.match(line)
        if match:
            link, subject = match.group(1), match.group(2).strip()
            target = posixpath.normpath(
                posixpath.join(posixpath.dirname(INDEX_PATH), link)
            )
        else:
            match = code_row.match(line)
            if not match:
                continue
            target, subject = match.group(1), match.group(2).strip()
            target = posixpath.normpath(target)
        if target == ".." or target.startswith("../"):
            continue
        summaries[target] = subject
    return summaries


_BOILERPLATE_PREFIX = re.compile(
    r"^(関連|出典|結節点|運営|拠点|対象リポ|リポ)\s*[:：]"
)


def _is_boilerplate(text: str) -> bool:
    if _BOILERPLATE_PREFIX.match(text):
        return True
    if text.endswith("設計記録") and len(text) <= 45:
        return True
    if ("Code2CreateClub" in text or "mc-remote.com" in text) and len(text) <= 40:
        return True
    return False


def _truncate(text: str) -> str:
    one_line = " ".join(text.split())
    if len(one_line) <= SUMMARY_MAXLEN:
        return one_line
    return one_line[: SUMMARY_MAXLEN - 1] + "…"


def fallback_summary(text: str) -> str:
    """INDEXにない文書はH1直後の説明文、なければH1を一行概要にする。"""
    title = ""
    for raw in text.splitlines():
        line = raw.strip()
        if not line:
            continue
        if line.startswith("# ") and not title:
            title = line[2:].strip()
            continue
        if line in ("---", "***", "___") or line.startswith("#"):
            break
        cleaned = re.sub(r"^[>\-*\s]+", "", line).strip()
        if not cleaned or _is_boilerplate(cleaned):
            continue
        return _truncate(cleaned)
    return _truncate(title) if title else "(概要なし)"


def collect_md_files(commit: str, scopes: list[str]) -> list[str]:
    """指定commitのMarkdownをpath昇順で列挙する。"""
    tree_paths = git_output(
        "-c", "core.quotePath=false", "ls-tree", "-r", "--name-only", commit
    ).splitlines()
    normalized_scopes = [scope.strip("/") for scope in scopes]
    missing = [
        scope
        for scope in normalized_scopes
        if not any(
            path == scope or path.startswith(scope + "/") for path in tree_paths
        )
    ]
    if missing:
        raise BundleBuildError(
            f"指定commitに存在しないスコープ: {', '.join(missing)}"
        )

    found: list[str] = []
    for rel_posix in tree_paths:
        if not rel_posix.endswith(".md"):
            continue
        if any(part in ALWAYS_EXCLUDE_DIRS for part in rel_posix.split("/")):
            continue
        if normalized_scopes and not any(
            rel_posix == scope or rel_posix.startswith(scope + "/")
            for scope in normalized_scopes
        ):
            continue
        found.append(rel_posix)
    return sorted(found)


def group_key(rel_posix: str) -> str:
    """トップ階層ディレクトリをバンドル分割キーにする。"""
    parts = rel_posix.split("/")
    return parts[0] if len(parts) > 1 else "00-root"


def render_block(rel_posix: str, summary: str, body: str) -> str:
    return f"## path: {rel_posix}\n> {summary}\n\n{body.rstrip()}\n"


def render_summary_stub(rel_posix: str, summary: str) -> str:
    return (
        f"## path: {rel_posix}\n> {summary}\n\n"
        "（本文はバンドル非収録。会話ログ・非正本のため要約スタブのみ"
        f"収録する。正本が要るときは上流リポの`{rel_posix}`を参照する。）\n"
    )


def extract_heading_section(
    text: str,
    *,
    source_path: str,
    level: int,
    title: str,
) -> str:
    """指定見出しのセクションを原文のまま抽出する。"""
    lines = text.splitlines()
    heading_re = re.compile(r"^(#{1,6})\s+(.+?)\s*$")
    matches: list[int] = []
    for index, line in enumerate(lines):
        match = heading_re.match(line)
        if not match or len(match.group(1)) != level:
            continue
        if match.group(2) == title:
            matches.append(index)
    if len(matches) != 1:
        raise BundleBuildError(
            f"{source_path}: level={level} / title={title!r}の見出しが"
            f"{len(matches)}件（必ず1件であること）"
        )

    start = matches[0]
    end = len(lines)
    for index in range(start + 1, len(lines)):
        match = heading_re.match(lines[index])
        if match and len(match.group(1)) <= level:
            end = index
            break
    section = "\n".join(lines[start:end]).rstrip()
    if not section:
        raise BundleBuildError(f"{source_path}: {title!r}セクションが空です。")
    return section


def read_current_state_sources(commit: str) -> list[tuple[str, str]]:
    """public正本の低drift節を現在地カプセル用にverbatim取得する。"""
    roadmap = read_commit_text(commit, ROADMAP_PATH)
    return [
        (
            ROADMAP_PATH,
            extract_heading_section(
                roadmap,
                source_path=ROADMAP_PATH,
                level=level,
                title=title,
            ),
        )
        for level, title in CURRENT_STATE_SECTIONS
    ]


def render_current_state_capsule(
    iso: str,
    sha: str,
    source_sections: list[tuple[str, str]],
) -> str:
    lines = [
        "# mc-remote-knowledge 現在地カプセル",
        "",
        "> **これは自動生成物です（Gemini Notebook〔旧NotebookLM〕"
        "取り込み用の使い捨てスナップショット）。**",
        "> このファイルを直接編集しないこと。上流Markdownを直し、再生成する。",
        f"> スナップショット: commit `{sha}` / {iso}",
        "> 生成: tools/build-notebooklm-bundle.py",
        "",
        "## Current State Capsule",
        "",
        "以下のpublic正本投影を、このバンドルの最優先の時系列アンカーとして扱うこと。",
        "",
    ]
    for path, section in source_sections:
        lines.extend(
            [
                f"<!-- source-begin: {path} -->",
                section,
                f"<!-- source-end: {path} -->",
                "",
            ]
        )
    lines.extend(
        [
            "## 時制と実装状態の読み取りガード",
            "",
            "- 現在地と横断優先は、上の正本投影を優先する。",
            "- 決定済みでも未実装のものは、現在利用可能な機能として扱わない。",
            "- 将来計画・park・却下案・履歴は、その状態語とともに説明する。",
            "- `bN`は特定の版ではなく、後続の未採番beta段の総称である。",
            "- DECISIONSの過去行を、後続決定で改訂された現行仕様として紹介しない。",
            "",
        ]
    )
    return "\n".join(lines)


def render_notebook_guide() -> str:
    lines = [
        "## Gemini Notebook（旧NotebookLM）向け読み取りガイド",
        "",
        "このバンドルには現行仕様、決定済み設計、将来計画、検討メモ、履歴が混在する。",
        f"`{CURRENT_STATE_CAPSULE_FILENAME}`を最優先の時系列アンカーとして扱うこと。",
        "",
        "- 現在地と横断優先: 現在地カプセルのpublic正本投影を優先する。",
        "- 決定済みだが未実装: 今すぐ使える機能として扱わない。",
        "- 将来計画: 現在地が進むまでは予定として説明する。",
        "- 履歴・却下案: 判断理由として読み、現行仕様として紹介しない。",
        "- `bN`: 特定版でなく、後続の未採番beta段の総称として読む。",
        "- 個別repoの次の一手: このバンドルへ固定せず、現行SSOTから都度判断する。",
        "",
        "---",
        "",
        "",
    ]
    return "\n".join(lines)


def render_header(
    group: str,
    part: int,
    parts_total: int,
    iso: str,
    sha: str,
    files: list[str],
) -> str:
    part_label = f"（{part}/{parts_total}）" if parts_total > 1 else ""
    lines = [
        f"# mc-remote-knowledge バンドル: {group}{part_label}",
        "",
        "> **これは自動生成物です（Gemini Notebook〔旧NotebookLM〕"
        "取り込み用の使い捨てスナップショット）。**",
        "> このファイルを直接編集しないこと。上流Markdownを直し、再生成する。",
        f"> スナップショット: commit `{sha}` / {iso}",
        "> 生成: tools/build-notebooklm-bundle.py",
        "",
        f"収録ファイル（{len(files)}件）:",
        "",
    ]
    lines.extend(f"- {path}" for path in files)
    lines.extend(["", "---", "", ""])
    return "\n".join(lines) + render_notebook_guide()


def split_blocks(
    blocks: list[tuple[str, str, int]],
    max_bytes: int,
) -> list[list[tuple[str, str, int]]]:
    if max_bytes <= 0:
        return [blocks]
    parts: list[list[tuple[str, str, int]]] = []
    current: list[tuple[str, str, int]] = []
    current_size = 0
    for item in blocks:
        if current and current_size + item[2] > max_bytes:
            parts.append(current)
            current = []
            current_size = 0
        current.append(item)
        current_size += item[2]
    if current:
        parts.append(current)
    return parts


def is_generated_markdown(path: Path) -> bool:
    try:
        prefix = path.read_text(encoding="utf-8")[:4096]
    except (OSError, UnicodeError):
        return False
    return all(marker in prefix for marker in GENERATED_MARKERS)


def write_outputs(out_dir: Path, outputs: dict[str, str]) -> None:
    """未知Markdownを消さずに停止し、既知生成物だけを置換する。"""
    if out_dir.exists() and not out_dir.is_dir():
        raise BundleBuildError(f"出力先がdirectoryではありません: {out_dir}")
    out_dir.mkdir(parents=True, exist_ok=True)

    existing = sorted(out_dir.glob("*.md"))
    unknown = [path for path in existing if not is_generated_markdown(path)]
    if unknown:
        names = ", ".join(path.name for path in unknown)
        raise BundleBuildError(
            f"出力先に生成物と確認できないMarkdownがあります: {names}"
        )
    for old in existing:
        old.unlink()
    for filename, content in outputs.items():
        (out_dir / filename).write_text(content, encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Gemini Notebook用バンドル生成（使い捨て）"
    )
    parser.add_argument(
        "scopes",
        nargs="*",
        help="対象directory（例: 00-hub 10-protocol）。省略で全体。",
    )
    parser.add_argument(
        "--max-bytes",
        type=int,
        default=0,
        help="1バンドルの本文目安上限。0は分割しない。",
    )
    parser.add_argument(
        "--out",
        default=str(OUT_DIR),
        help="出力先directory。",
    )
    parser.add_argument(
        "--source-ref",
        default="HEAD",
        help="投影元のGit refまたはcommit。既定はHEAD。",
    )
    args = parser.parse_args()

    if args.max_bytes < 0:
        print("生成停止: --max-bytesは0以上で指定してください。", file=sys.stderr)
        return 2

    try:
        commit = resolve_commit(args.source_ref)
        iso, sha = snapshot_meta(commit)
        index_summaries = parse_index_summaries(
            read_commit_text(commit, INDEX_PATH)
        )
        current_state_sources = read_current_state_sources(commit)
        files = collect_md_files(commit, args.scopes)
    except BundleBuildError as exc:
        print(f"生成停止: {exc}", file=sys.stderr)
        return 2

    if not files:
        print("対象Markdownが見つかりませんでした。", file=sys.stderr)
        return 1

    groups: dict[str, list[tuple[str, str, int]]] = {}
    log_rows: list[tuple[str, str, str]] = []
    try:
        for rel_posix in files:
            body = read_commit_text(commit, rel_posix)
            if rel_posix in index_summaries:
                summary = index_summaries[rel_posix]
                summary_source = "INDEX"
            else:
                summary = fallback_summary(body)
                summary_source = "本文先頭"
            if rel_posix in SUMMARY_ONLY_PATHS:
                block = render_summary_stub(rel_posix, summary)
                summary_source += "/要約スタブ"
            else:
                block = render_block(rel_posix, summary, body)
            groups.setdefault(group_key(rel_posix), []).append(
                (rel_posix, block, len(block.encode("utf-8")))
            )
            log_rows.append((rel_posix, summary_source, summary))
    except BundleBuildError as exc:
        print(f"生成停止: {exc}", file=sys.stderr)
        return 2

    outputs: dict[str, str] = {}
    capsule = render_current_state_capsule(iso, sha, current_state_sources)
    outputs[CURRENT_STATE_CAPSULE_FILENAME] = capsule
    output_rows: list[tuple[str, int, int]] = [
        (
            CURRENT_STATE_CAPSULE_FILENAME,
            0,
            len(capsule.encode("utf-8")),
        )
    ]

    for group in sorted(groups):
        parts = split_blocks(groups[group], args.max_bytes)
        for index, part in enumerate(parts, start=1):
            file_list = [item[0] for item in part]
            header = render_header(
                group,
                index,
                len(parts),
                iso,
                sha,
                file_list,
            )
            content = header + "\n".join(item[1] for item in part)
            suffix = f"-{index:02d}" if len(parts) > 1 else ""
            filename = f"{group}{suffix}.md"
            outputs[filename] = content
            output_rows.append(
                (filename, len(part), len(content.encode("utf-8")))
            )

    out_dir = Path(args.out)
    try:
        write_outputs(out_dir, outputs)
    except BundleBuildError as exc:
        print(f"生成停止: {exc}", file=sys.stderr)
        return 2

    print("= Gemini Notebookバンドル生成 =")
    print(f"  source: {args.source_ref} -> {sha} / snapshot: {iso}")
    print("  現在地: public正本の指定セクションをverbatim投影")
    print(f"  スコープ: {args.scopes or ['(全体)']}")
    print(f"  出力先: {out_dir}")
    print(f"  対象ファイル: {len(files)}件")
    print()
    print("  概要の出所:")
    for rel_posix, source, summary in log_rows:
        print(f"    [{source}] {rel_posix}")
        print(f"            └ {summary}")
    print()
    print("  生成ソース:")
    for filename, count, size in output_rows:
        files_label = "  -" if count == 0 else f"{count:3d}"
        print(
            f"    {filename:32s} files={files_label}  {size / 1024:7.1f} KiB"
        )
    print()
    print(f"  → 合計{len(outputs)}ソース / {len(files)}上流ファイル収録")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
