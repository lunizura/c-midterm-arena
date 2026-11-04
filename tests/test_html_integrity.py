"""
test_html_integrity.py
Automated tests validating the web application HTML5 deliverable integrity,
DOM elements, safety guards, and offline completeness.

Authoritative Requirements:
- ORIGINAL_REQUEST.md: R1 (Timer, navigation, and state-handling defects), R2 (Pedagogical deep dives),
  R3 (Deliverable synchronization and clean rendering without syntax errors or display glitches).
- PROJECT.md: Features 7, 8, 9, 10, 11, 12, 13, 14, 15.
- TEST_INFRA.md: Tier 1, Tier 2 (Boundary & Corner Cases), Tier 3 (Cross-Feature Combinations), Tier 4.
"""

import os
import re
import sys
import unittest

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)


class TestHtmlIntegrity(unittest.TestCase):
    """Verifies that the generated HTML deliverables meet all integrity, pedagogical, and UX requirements."""

    @classmethod
    def setUpClass(cls):
        cls.index_path = os.path.join(REPO_ROOT, "index.html")
        cls.arena_path = os.path.join(REPO_ROOT, "c_midterm_arena.html")
        
        # Read content of index.html
        if os.path.isfile(cls.index_path):
            with open(cls.index_path, "r", encoding="utf-8", errors="replace") as f:
                cls.index_content = f.read()
        else:
            cls.index_content = ""

    def test_no_control_character_corruption(self):
        """
        Deliverable files must NOT contain raw \u0001 (\x01) or \u0002 (\x02) characters,
        which occur when multiline Python strings corrupt RegExp backreferences like \\1 and \\2.
        """
        for path, name in [(self.index_path, "index.html"), (self.arena_path, "c_midterm_arena.html")]:
            if not os.path.isfile(path):
                continue
            with open(path, "r", encoding="utf-8", errors="replace") as f:
                content = f.read()

            count_u0001 = content.count("\u0001")
            count_u0002 = content.count("\u0002")

            self.assertEqual(
                count_u0001, 0,
                f"[{name}] Contains {count_u0001} corrupt '\\u0001' control characters (RegExp escaping defect)!"
            )
            self.assertEqual(
                count_u0002, 0,
                f"[{name}] Contains {count_u0002} corrupt '\\u0002' control characters (RegExp escaping defect)!"
            )

    def test_deep_dive_pedagogical_rendering(self):
        """
        The web arena UI must interpolate and render the in-depth pedagogical deepDive
        explanation (Feature 9, R2).
        """
        self.assertTrue(self.index_content, "index.html is empty or not found")
        
        # Check that deepDive is referenced in the frontend scripts
        has_deep_dive_ref = (
            "deepDive" in self.index_content or
            "deep-dive" in self.index_content or
            "pane-locked" in self.index_content or
            "locked-pane-card" in self.index_content
        )
        self.assertTrue(
            has_deep_dive_ref,
            "index.html does not reference 'deepDive' or provide a deep-dive pedagogical container!"
        )

    def test_exam_rush_timer_presence(self):
        """
        Exam Rush mode must include a countdown timer element and timer state mechanics (Feature 10).
        """
        self.assertTrue(self.index_content, "index.html is empty or not found")
        
        has_timer = any(
            marker in self.index_content.lower()
            for marker in ["timer", "countdown", "setinterval", "time-remaining", "exam-timer"]
        )
        self.assertTrue(
            has_timer,
            "index.html lacks countdown timer elements or mechanics for Exam Rush mode!"
        )

    def test_question_palette_and_jump_navigation(self):
        """
        The web arena must include a question palette or grid navigation modal
        allowing direct jumping across all questions (Feature 11).
        """
        self.assertTrue(self.index_content, "index.html is empty or not found")
        
        has_palette = any(
            marker in self.index_content.lower()
            for marker in ["palette", "question-grid", "modal-palette", "palette-modal", "jump to question", "openpalette"]
        )
        self.assertTrue(
            has_palette,
            "index.html lacks a question palette or grid navigation modal for jumping across questions!"
        )

    def test_html_entity_escaping_safety(self):
        """
        Explanation and distractor rendering must safely escape HTML entities such as
        '<math.h>' or '<stdio.h>' so that the browser parser does not swallow them as DOM tags.
        """
        self.assertTrue(self.index_content, "index.html is empty or not found")

        # In Q021, option B mentions <math.h>. In the embedded JSON or UI template,
        # escapeHTML should be applied to dynamic distractor texts.
        has_escape_function = "escapeHTML" in self.index_content or "escapeHtml" in self.index_content
        self.assertTrue(
            has_escape_function,
            "index.html lacks an 'escapeHTML' helper to sanitize dynamic explanation text."
        )

    def test_survival_mode_negative_lives_boundary(self):
        """
        Survival mode must guard against negative lives when answering incorrectly at 0 lives (Feature 15).
        """
        self.assertTrue(self.index_content, "index.html is empty or not found")
        
        # Check that State.lives has boundary check <= 0 or game over guard
        has_boundary_guard = (
            "lives <= 0" in self.index_content or
            "lives < 1" in self.index_content or
            "State.lives <= 0" in self.index_content or
            "gameOver" in self.index_content or
            "isGameOver" in self.index_content
        )
        self.assertTrue(
            has_boundary_guard,
            "index.html lacks boundary guard for survival mode lives <= 0 to prevent negative life counter."
        )

    def test_keyboard_shortcut_mapping_no_conflicts(self):
        """
        Pressing 'b' or 'B' must select Option B and not be hijacked exclusively by bookmarking (Feature 13).
        """
        self.assertTrue(self.index_content, "index.html is empty or not found")

        # Verify whether 'b' is blocked from selecting option B:
        # e.g. "e.key !== 'b'" was a defect that prevented lowercase 'b' from selecting Option B
        has_lowercase_b_block = "e.key !== 'b'" in self.index_content
        self.assertFalse(
            has_lowercase_b_block,
            "index.html contains conflicting shortcut logic: 'e.key !== 'b'' prevents lowercase 'b' from selecting Option B!"
        )

    def test_standalone_deliverable_offline_completeness(self):
        """
        index.html must be completely standalone without dependencies on external CDN resources
        (no <script src='http...'> or <link rel='stylesheet' href='http...'>).
        """
        self.assertTrue(self.index_content, "index.html is empty or not found")

        # Search for external script tags
        external_scripts = re.findall(r'<script[^>]+src=["\'](https?://[^"\']+)["\']', self.index_content, re.IGNORECASE)
        self.assertEqual(
            len(external_scripts), 0,
            f"index.html contains external remote scripts that break offline air-gapped usage: {external_scripts}"
        )

        external_css = re.findall(r'<link[^>]+href=["\'](https?://[^"\']+)["\']', self.index_content, re.IGNORECASE)
        self.assertEqual(
            len(external_css), 0,
            f"index.html contains external remote stylesheets that break offline air-gapped usage: {external_css}"
        )


if __name__ == "__main__":
    unittest.main()
