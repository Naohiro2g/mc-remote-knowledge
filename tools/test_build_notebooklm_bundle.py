#!/usr/bin/env python3
"""Gemini Notebookバンドルのpublic SSOT投影・再現性ガード。"""

from __future__ import annotations

import hashlib
import importlib.util
import subprocess
import tempfile
import unittest
from pathlib import Path


TOOLS_DIR = Path(__file__).resolve().parent
SCRIPT_PATH = TOOLS_DIR / "build-notebooklm-bundle.py"
SPEC = importlib.util.spec_from_file_location(
    "build_notebooklm_bundle",
    SCRIPT_PATH,
)
assert SPEC and SPEC.loader
BUNDLE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(BUNDLE)


class HeadingExtractionTests(unittest.TestCase):
    def test_extracts_one_heading_section_verbatim(self) -> None:
        text = "# root\n\n## 現在地\n\nbody\n\n### child\nchild body\n\n## next\n"
        actual = BUNDLE.extract_heading_section(
            text,
            source_path="sample.md",
            level=2,
            title="現在地",
        )
        self.assertEqual(
            actual,
            "## 現在地\n\nbody\n\n### child\nchild body",
        )

    def test_missing_or_duplicate_heading_fails_closed(self) -> None:
        with self.assertRaises(BUNDLE.BundleBuildError):
            BUNDLE.extract_heading_section(
                "# root\n",
                source_path="sample.md",
                level=2,
                title="現在地",
            )
        with self.assertRaises(BUNDLE.BundleBuildError):
            BUNDLE.extract_heading_section(
                "## 現在地\nA\n## 現在地\nB\n",
                source_path="sample.md",
                level=2,
                title="現在地",
            )


class IndexSummaryTests(unittest.TestCase):
    def test_parses_public_code_path_rows(self) -> None:
        text = (
            "| Path | 役割 |\n"
            "| --- | --- |\n"
            "| `00-hub/example_ja.md` | public概要 |\n"
        )
        self.assertEqual(
            BUNDLE.parse_index_summaries(text),
            {"00-hub/example_ja.md": "public概要"},
        )

    def test_parses_legacy_relative_link_rows(self) -> None:
        text = "| [example](example_ja.md) | legacy概要 |\n"
        self.assertEqual(
            BUNDLE.parse_index_summaries(text),
            {"00-hub/example_ja.md": "legacy概要"},
        )


class CommitProjectionTests(unittest.TestCase):
    def test_capsule_contains_public_sections_verbatim(self) -> None:
        commit = BUNDLE.resolve_commit("HEAD")
        sections = BUNDLE.read_current_state_sources(commit)
        iso, sha = BUNDLE.snapshot_meta(commit)
        capsule = BUNDLE.render_current_state_capsule(iso, sha, sections)
        self.assertEqual(
            [path for path, _section in sections],
            [BUNDLE.ROADMAP_PATH, BUNDLE.ROADMAP_PATH],
        )
        self.assertIn("## 現在地", sections[0][1])
        self.assertIn("## 4. 現在の横断優先", sections[1][1])
        for path, section in sections:
            self.assertIn(
                f"<!-- source-begin: {path} -->\n{section}\n",
                capsule,
            )
        self.assertNotIn("scratch-plan_ja.md", capsule)

    def test_collection_uses_tracked_commit_tree(self) -> None:
        commit = BUNDLE.resolve_commit("HEAD")
        files = BUNDLE.collect_md_files(commit, [])
        self.assertIn("00-hub/grand-design-roadmap_ja.md", files)
        self.assertNotIn("tools/README_ja.md", files)
        self.assertNotIn("install_codex.md", files)

    def test_same_commit_produces_identical_files(self) -> None:
        commit = BUNDLE.resolve_commit("HEAD")
        with tempfile.TemporaryDirectory() as first:
            with tempfile.TemporaryDirectory() as second:
                for source_ref, output in (("HEAD", first), (commit, second)):
                    completed = subprocess.run(
                        [
                            "python3",
                            str(SCRIPT_PATH),
                            "--source-ref",
                            source_ref,
                            "--out",
                            output,
                        ],
                        cwd=TOOLS_DIR.parent,
                        capture_output=True,
                        text=True,
                        check=False,
                    )
                    self.assertEqual(
                        completed.returncode,
                        0,
                        completed.stderr,
                    )
                self.assertEqual(
                    self._hashes(Path(first)),
                    self._hashes(Path(second)),
                )

    @staticmethod
    def _hashes(root: Path) -> dict[str, str]:
        return {
            path.name: hashlib.sha256(path.read_bytes()).hexdigest()
            for path in sorted(root.glob("*.md"))
        }


class OutputSafetyTests(unittest.TestCase):
    def test_unknown_markdown_is_not_deleted(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            out_dir = Path(directory)
            unknown = out_dir / "keep.md"
            unknown.write_text("# user file\n", encoding="utf-8")
            with self.assertRaises(BUNDLE.BundleBuildError):
                BUNDLE.write_outputs(out_dir, {"bundle.md": "generated"})
            self.assertEqual(
                unknown.read_text(encoding="utf-8"),
                "# user file\n",
            )


if __name__ == "__main__":
    unittest.main()
