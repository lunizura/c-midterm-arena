"""
test_build_pipeline.py
Automated testing for the C Midterm Arena build and bundling pipeline.

Authoritative Requirements:
- ORIGINAL_REQUEST.md: R3 (Web Application Rebuild and Deliverable Synchronization,
  python build_html.py runs to completion with exit code 0, c_midterm_arena.html and
  index.html are regenerated and fully in sync).
- PROJECT.md: Feature 16 (Deliverable Synchronization), Build Output Contract.
- TEST_INFRA.md: Tier 1 (build_html.py executes with exit code 0, SHA-256 hash match).
"""

import os
import sys
import hashlib
import subprocess
import unittest

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)


class TestBuildPipeline(unittest.TestCase):
    """Tests the build and asset bundling pipeline for C Midterm Arena."""

    @classmethod
    def setUpClass(cls):
        cls.build_script = os.path.join(REPO_ROOT, "build_html.py")
        cls.index_html = os.path.join(REPO_ROOT, "index.html")
        cls.arena_html = os.path.join(REPO_ROOT, "c_midterm_arena.html")
        cls.export_c_script = os.path.join(REPO_ROOT, "export_c_header.py")

    def test_build_html_execution_exit_code_zero(self):
        """
        Executing 'python build_html.py' must complete with exit code 0
        and output generation confirmation.
        """
        self.assertTrue(os.path.isfile(self.build_script), "build_html.py not found in repo root")

        res = subprocess.run(
            [sys.executable, self.build_script],
            cwd=REPO_ROOT,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=30
        )

        self.assertEqual(
            res.returncode, 0,
            f"build_html.py failed with exit code {res.returncode}.\nStderr:\n{res.stderr}\nStdout:\n{res.stdout}"
        )
        self.assertIn(
            "index.html", res.stdout.lower(),
            f"build_html.py output did not confirm index.html generation:\n{res.stdout}"
        )

    def test_deliverable_files_exist_and_non_empty(self):
        """Both index.html and c_midterm_arena.html must exist and be non-empty (>50KB)."""
        for filepath in [self.index_html, self.arena_html]:
            self.assertTrue(
                os.path.isfile(filepath),
                f"Deliverable file '{os.path.basename(filepath)}' does not exist"
            )
            file_size = os.path.getsize(filepath)
            self.assertGreater(
                file_size, 50000,
                f"Deliverable file '{os.path.basename(filepath)}' is too small ({file_size} bytes, expected > 50KB)"
            )

    def test_deliverables_sha256_hash_synchronization(self):
        """
        index.html and c_midterm_arena.html must have IDENTICAL SHA-256 hashes,
        proving that the web application and release deliverable are in 100% lockstep.
        """
        with open(self.index_html, "rb") as f:
            index_hash = hashlib.sha256(f.read()).hexdigest()

        with open(self.arena_html, "rb") as f:
            arena_hash = hashlib.sha256(f.read()).hexdigest()

        self.assertEqual(
            index_hash, arena_hash,
            f"SHA-256 mismatch between index.html and c_midterm_arena.html!\nindex.html:         {index_hash}\nc_midterm_arena.html: {arena_hash}"
        )

    def test_c_header_export_pipeline(self):
        """
        Verifies that export_c_header.py executes cleanly and updates src/questions.h and src/questions.c.
        """
        if not os.path.isfile(self.export_c_script):
            self.skipTest("export_c_header.py not present in repository")

        res = subprocess.run(
            [sys.executable, self.export_c_script],
            cwd=REPO_ROOT,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=20
        )
        self.assertEqual(
            res.returncode, 0,
            f"export_c_header.py failed with exit code {res.returncode}.\nStderr:\n{res.stderr}"
        )

        h_path = os.path.join(REPO_ROOT, "src", "questions.h")
        c_path = os.path.join(REPO_ROOT, "src", "questions.c")
        self.assertTrue(os.path.isfile(h_path), "src/questions.h missing after export")
        self.assertTrue(os.path.isfile(c_path), "src/questions.c missing after export")


if __name__ == "__main__":
    unittest.main()
