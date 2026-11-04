"""
test_question_schema.py
Comprehensive test suite validating question data schemas across:
- Primary Syllabus Bank (syllabus_part1.py, syllabus_part2.py, syllabus_part3.py)
- Deep Alternative Bank (bank_part1.py, bank_part2.py, bank_part3.py, bank_part4.py)

Authoritative Requirements:
- ORIGINAL_REQUEST.md: R1 (Correct answer keys, balanced options), R2 (In-depth explanations, execution traces, memory layout, distractor rationales)
- PROJECT.md: Interface Contracts - Question Data Schema
- TEST_INFRA.md: Tier 1 (Feature Coverage), Tier 2 (Boundary & Corner Cases)
"""

import os
import sys
import unittest
from collections import Counter

# Ensure c-midterm-arena root is in sys.path
REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)


def _load_bank(generator_module_name, part_module_names):
    """Dynamically load questions from specified generator and bank modules without side-effects."""
    import importlib
    
    # Reload generator module to ensure clean question list
    gen_mod = importlib.import_module(generator_module_name)
    questions = []
    
    def capture_add_q(id_num, category, difficulty, title, prompt, code,
                      trap_line, trap_token, trap_warning,
                      options_tuples, summary, std_ref, deep_dive, trace_steps):
        opts = []
        for k, text, corr, tempting, wrong in options_tuples:
            opt_obj = {
                "key": k,
                "text": str(text),
                "isCorrect": bool(corr),
                "whyTempting": tempting
            }
            if not corr:
                opt_obj["whyWrong"] = wrong
            opts.append(opt_obj)

        trace = []
        for s_num, l_num, desc, v_dict, m_dict in trace_steps:
            step_obj = {
                "step": s_num,
                "line": l_num,
                "description": desc,
                "variables": v_dict or {}
            }
            if m_dict:
                step_obj["memorySnapshots"] = m_dict
            trace.append(step_obj)

        q = {
            "id": f"Q{id_num:03d}",
            "category": category,
            "difficulty": difficulty,
            "title": title,
            "prompt": prompt,
            "code": code.strip(),
            "trapInfo": {
                "line": trap_line,
                "token": trap_token,
                "shortWarning": trap_warning
            },
            "options": opts,
            "explanation": {
                "summary": summary,
                "cStandardRef": std_ref,
                "deepDive": deep_dive
            },
            "executionTrace": trace
        }
        questions.append(q)

    for part_name in part_module_names:
        part_mod = importlib.import_module(part_name)
        # Find load function in part module (e.g. load_part1, load_part2, etc.)
        load_funcs = [getattr(part_mod, f) for f in dir(part_mod) if f.startswith("load_part")]
        for lf in load_funcs:
            lf(capture_add_q)

    return questions


class TestSyllabusQuestionSchema(unittest.TestCase):
    """Validates the 100-question syllabus curriculum bank (syllabus_part1..3)."""

    @classmethod
    def setUpClass(cls):
        cls.questions = _load_bank(
            "generate_syllabus_questions",
            ["syllabus_part1", "syllabus_part2", "syllabus_part3"]
        )

    def test_total_question_count(self):
        """Assert exactly 100 questions exist in the primary syllabus bank."""
        self.assertEqual(
            len(self.questions), 100,
            f"Expected exactly 100 questions in syllabus bank, found {len(self.questions)}"
        )

    def test_question_ids_unique_and_formatted(self):
        """Verify question IDs are sequential Q001..Q100 and strictly unique."""
        ids = [q["id"] for q in self.questions]
        self.assertEqual(len(ids), len(set(ids)), f"Duplicate question IDs found: {[x for x in ids if ids.count(x) > 1]}")
        expected_ids = [f"Q{i:03d}" for i in range(1, 101)]
        self.assertEqual(ids, expected_ids, "Question IDs must be sequentially ordered Q001 to Q100")

    def test_required_fields_present_and_non_empty(self):
        """Every question must conform strictly to the required dictionary schema."""
        required_keys = [
            "id", "category", "difficulty", "title", "prompt", "code",
            "trapInfo", "options", "explanation", "executionTrace"
        ]
        for q in self.questions:
            qid = q.get("id", "UNKNOWN")
            for k in required_keys:
                self.assertIn(k, q, f"[{qid}] Missing required field '{k}'")
                if k not in ("code", "executionTrace"):
                    self.assertTrue(q[k], f"[{qid}] Field '{k}' must not be empty or falsy")
            self.assertIsInstance(q["code"], str, f"[{qid}] 'code' must be a string")
            self.assertGreater(len(q["code"].strip()), 0, f"[{qid}] 'code' cannot be empty")

    def test_options_cardinality_and_keys(self):
        """Every question must have exactly 4 options with keys A, B, C, D."""
        for q in self.questions:
            qid = q["id"]
            opts = q["options"]
            self.assertEqual(len(opts), 4, f"[{qid}] Expected exactly 4 options, found {len(opts)}")
            keys = [o["key"] for o in opts]
            self.assertEqual(keys, ["A", "B", "C", "D"], f"[{qid}] Option keys must be ['A', 'B', 'C', 'D']")
            for opt in opts:
                self.assertTrue(opt["text"], f"[{qid}] Option {opt['key']} text is empty")
                self.assertTrue(opt["whyTempting"], f"[{qid}] Option {opt['key']} whyTempting is empty")

    def test_exactly_one_correct_option(self):
        """Every question must have exactly one correct option (isCorrect=True)."""
        for q in self.questions:
            qid = q["id"]
            correct_opts = [o for o in q["options"] if o.get("isCorrect") is True]
            self.assertEqual(
                len(correct_opts), 1,
                f"[{qid}] Expected exactly 1 correct option, found {len(correct_opts)}: {[o['key'] for o in correct_opts]}"
            )

    def test_distractor_rationales_complete(self):
        """Every incorrect option must have an explicit 'whyWrong' rationale addressing misconceptions."""
        for q in self.questions:
            qid = q["id"]
            for opt in q["options"]:
                if not opt["isCorrect"]:
                    self.assertIn(
                        "whyWrong", opt,
                        f"[{qid}] Distractor option {opt['key']} lacks 'whyWrong' field"
                    )
                    why_wrong = str(opt.get("whyWrong", "")).strip()
                    self.assertTrue(
                        why_wrong,
                        f"[{qid}] Distractor option {opt['key']} has empty 'whyWrong' rationale"
                    )
                    # Verify rationale is substantive (not just 1-2 words like 'Syntax error.')
                    self.assertGreater(
                        len(why_wrong), 10,
                        f"[{qid}] Distractor option {opt['key']} whyWrong is overly brief: '{why_wrong}'"
                    )

    def test_answer_keys_balanced(self):
        """
        Keys A, B, C, D must be balanced across the 100 questions (~25% each).
        Fails if any single key exceeds 45% (detecting the all-A monoculture defect).
        """
        correct_keys = [next(o["key"] for o in q["options"] if o["isCorrect"]) for q in self.questions]
        distribution = Counter(correct_keys)
        # Check no key dominates the bank
        for k in ["A", "B", "C", "D"]:
            self.assertGreaterEqual(
                distribution[k], 15,
                f"Key '{k}' is underrepresented in syllabus bank: only {distribution[k]} questions (expected ~25)"
            )
            self.assertLessEqual(
                distribution[k], 35,
                f"Key '{k}' is overrepresented in syllabus bank: {distribution[k]} questions (expected ~25)"
            )

    def test_pedagogical_deep_dive_quality(self):
        """
        Explanation must contain summary, cStandardRef, and an in-depth pedagogical deepDive.
        Fails on short stub deepDives (e.g. under 40 characters).
        """
        for q in self.questions:
            qid = q["id"]
            expl = q["explanation"]
            self.assertTrue(expl.get("summary"), f"[{qid}] explanation.summary is empty")
            self.assertTrue(expl.get("cStandardRef"), f"[{qid}] explanation.cStandardRef is empty")
            deep_dive = str(expl.get("deepDive", "")).strip()
            self.assertGreater(
                len(deep_dive), 40,
                f"[{qid}] explanation.deepDive is a stub or too short ({len(deep_dive)} chars): '{deep_dive}'"
            )

    def test_execution_traces_and_line_mapping(self):
        """Execution traces must be present with valid steps and line numbers."""
        for q in self.questions:
            qid = q["id"]
            traces = q.get("executionTrace", [])
            self.assertGreaterEqual(
                len(traces), 1,
                f"[{qid}] executionTrace must have at least 1 step"
            )
            code_lines = len(q["code"].splitlines())
            for step in traces:
                self.assertIn("step", step, f"[{qid}] Trace step missing 'step'")
                self.assertIn("line", step, f"[{qid}] Trace step missing 'line'")
                self.assertIn("description", step, f"[{qid}] Trace step missing 'description'")
                self.assertIsInstance(step.get("variables"), dict, f"[{qid}] Step variables must be a dict")
                # Line number should be within reasonable bounds of the code snippet
                line_no = step["line"]
                self.assertGreaterEqual(line_no, 1, f"[{qid}] Trace step line {line_no} must be >= 1")
                self.assertLessEqual(
                    line_no, code_lines + 2,
                    f"[{qid}] Trace step line {line_no} exceeds code snippet line count ({code_lines})"
                )

    def test_trap_info_alignment_and_token(self):
        """
        Trap token must be present in snippet, and line offset must be valid.
        """
        for q in self.questions:
            qid = q["id"]
            trap = q.get("trapInfo", {})
            self.assertIn("line", trap, f"[{qid}] trapInfo missing 'line'")
            self.assertIn("token", trap, f"[{qid}] trapInfo missing 'token'")
            self.assertIn("shortWarning", trap, f"[{qid}] trapInfo missing 'shortWarning'")

            code = q["code"]
            token = trap["token"]
            self.assertTrue(token, f"[{qid}] trapInfo.token cannot be empty")
            self.assertIn(
                token, code,
                f"[{qid}] trap token '{token}' not found anywhere in code snippet:\n{code}"
            )

    def test_memory_snapshots_coverage(self):
        """
        Questions dealing with pointers, arrays, or variable memory layout should
        contain memorySnapshots in at least some of their trace steps.
        """
        mem_snapshot_count = sum(
            1 for q in self.questions
            if any("memorySnapshots" in step for step in q.get("executionTrace", []))
        )
        # Check that memory snapshots are populated across the bank
        self.assertGreaterEqual(
            mem_snapshot_count, 15,
            f"Expected at least 15 questions with memorySnapshots in syllabus bank, found only {mem_snapshot_count}"
        )


class TestAlternativeBankQuestionSchema(unittest.TestCase):
    """Validates the 100-question deep alternative bank (bank_part1..4)."""

    @classmethod
    def setUpClass(cls):
        cls.questions = _load_bank(
            "generate_questions",
            ["bank_part1", "bank_part2", "bank_part3", "bank_part4"]
        )

    def test_total_question_count(self):
        """Assert exactly 100 questions exist in the alternative bank."""
        self.assertEqual(
            len(self.questions), 100,
            f"Expected exactly 100 questions in bank_part1..4, found {len(self.questions)}"
        )

    def test_question_ids_unique_and_formatted(self):
        """Verify question IDs are sequential Q001..Q100 and strictly unique."""
        ids = [q["id"] for q in self.questions]
        self.assertEqual(len(ids), len(set(ids)), f"Duplicate question IDs found: {[x for x in ids if ids.count(x) > 1]}")
        expected_ids = [f"Q{i:03d}" for i in range(1, 101)]
        self.assertEqual(ids, expected_ids, "Question IDs must be sequentially ordered Q001 to Q100")

    def test_required_fields_present_and_non_empty(self):
        """Every question must conform strictly to the required dictionary schema."""
        required_keys = [
            "id", "category", "difficulty", "title", "prompt", "code",
            "trapInfo", "options", "explanation", "executionTrace"
        ]
        for q in self.questions:
            qid = q.get("id", "UNKNOWN")
            for k in required_keys:
                self.assertIn(k, q, f"[{qid}] Missing required field '{k}'")
                if k not in ("code", "executionTrace"):
                    self.assertTrue(q[k], f"[{qid}] Field '{k}' must not be empty or falsy")
            self.assertIsInstance(q["code"], str, f"[{qid}] 'code' must be a string")
            self.assertGreater(len(q["code"].strip()), 0, f"[{qid}] 'code' cannot be empty")

    def test_options_cardinality_and_keys(self):
        """Every question must have exactly 4 options with keys A, B, C, D."""
        for q in self.questions:
            qid = q["id"]
            opts = q["options"]
            self.assertEqual(len(opts), 4, f"[{qid}] Expected exactly 4 options, found {len(opts)}")
            keys = [o["key"] for o in opts]
            self.assertEqual(keys, ["A", "B", "C", "D"], f"[{qid}] Option keys must be ['A', 'B', 'C', 'D']")

    def test_exactly_one_correct_option(self):
        """Every question must have exactly one correct option (isCorrect=True)."""
        for q in self.questions:
            qid = q["id"]
            correct_opts = [o for o in q["options"] if o.get("isCorrect") is True]
            self.assertEqual(
                len(correct_opts), 1,
                f"[{qid}] Expected exactly 1 correct option, found {len(correct_opts)}"
            )

    def test_distractor_rationales_complete(self):
        """Every incorrect option must have an explicit 'whyWrong' rationale addressing misconceptions."""
        for q in self.questions:
            qid = q["id"]
            for opt in q["options"]:
                if not opt["isCorrect"]:
                    self.assertIn(
                        "whyWrong", opt,
                        f"[{qid}] Distractor option {opt['key']} lacks 'whyWrong' field"
                    )
                    why_wrong = str(opt.get("whyWrong", "")).strip()
                    self.assertTrue(
                        why_wrong,
                        f"[{qid}] Distractor option {opt['key']} has empty 'whyWrong' rationale"
                    )

    def test_answer_keys_balanced(self):
        """
        Keys A, B, C, D must be balanced across the 100 questions (~25% each).
        Fails if any single key exceeds 45% (detecting the all-A monoculture defect).
        """
        correct_keys = [next(o["key"] for o in q["options"] if o["isCorrect"]) for q in self.questions]
        distribution = Counter(correct_keys)
        for k in ["A", "B", "C", "D"]:
            self.assertGreaterEqual(
                distribution[k], 15,
                f"Key '{k}' is underrepresented in alternative bank: only {distribution[k]} questions (expected ~25)"
            )
            self.assertLessEqual(
                distribution[k], 35,
                f"Key '{k}' is overrepresented in alternative bank: {distribution[k]} questions (expected ~25)"
            )

    def test_pedagogical_deep_dive_quality(self):
        """
        Explanation must contain summary, cStandardRef, and an in-depth pedagogical deepDive.
        Fails on short stub deepDives (e.g. under 40 characters).
        """
        for q in self.questions:
            qid = q["id"]
            expl = q["explanation"]
            self.assertTrue(expl.get("summary"), f"[{qid}] explanation.summary is empty")
            self.assertTrue(expl.get("cStandardRef"), f"[{qid}] explanation.cStandardRef is empty")
            deep_dive = str(expl.get("deepDive", "")).strip()
            self.assertGreater(
                len(deep_dive), 40,
                f"[{qid}] explanation.deepDive is too short ({len(deep_dive)} chars): '{deep_dive}'"
            )

    def test_memory_snapshots_coverage(self):
        """Check that memory snapshots are populated for pointer and array operations."""
        mem_snapshot_count = sum(
            1 for q in self.questions
            if any("memorySnapshots" in step for step in q.get("executionTrace", []))
        )
        self.assertGreaterEqual(
            mem_snapshot_count, 15,
            f"Expected at least 15 questions with memorySnapshots in alternative bank, found only {mem_snapshot_count}"
        )


if __name__ == "__main__":
    unittest.main()
