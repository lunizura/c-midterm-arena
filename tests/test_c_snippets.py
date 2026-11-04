"""
test_c_snippets.py
Comprehensive GCC compilation and syntax verification for C code snippets across:
- Primary Syllabus Bank (syllabus_part1..3)
- Deep Alternative Bank (bank_part1..4)

Authoritative Requirements:
- ORIGINAL_REQUEST.md: R1 (Resolve unexpected compilation errors while preserving intentional compile errors),
  Acceptance Criteria (All C snippets compile and execute in accordance with premise).
- PROJECT.md: Feature 2 (C Snippet GCC/Clang Validity - fix naked fragments and verify all snippets compile).
- TEST_INFRA.md: Tier 1 (Clean C compilation under GCC, intentional compiler errors tagged).
"""

import os
import sys
import shutil
import tempfile
import subprocess
import unittest

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

from tests.test_question_schema import _load_bank

# Known questions designed specifically to test compiler errors in syllabus bank
SYLLABUS_INTENTIONAL_COMPILE_ERRORS = {
    "Q010": "assignment of read-only variable",
    "Q021": "invalid operands to binary %",
    "Q042": "case label does not reduce to an integer constant",
    "Q043": "switch quantity not an integer",
    "Q044": "duplicate case value",
    "Q050": "a label can only be part of a statement and a declaration is not a statement",
    "Q053": "'i' undeclared",
    "Q057": "expected ';' before 'return'",
}

# Known questions designed specifically to test runtime crashes, infinite loops, or UB
SYLLABUS_INTENTIONAL_RUNTIME_FAULTS = {
    "Q014": "scanf format string without address operator (&num) triggers SIGSEGV / crash",
    "Q060": "continue before increment in while loop causes infinite loop",
    "Q063": "float precision accumulation (f != 1.0f) causes infinite loop",
    "Q078": "unbounded recursive function call without base case causes stack overflow",
}

# Known questions designed specifically to test compiler errors in alternative bank
BANK_INTENTIONAL_COMPILE_ERRORS = {
    "Q025": "invalid use of void expression (*void)",
    "Q032": "invalid operands to binary - (mismatched pointer types)",
    "Q058": "assignment to expression with array type (str = 'world')",
    "Q095": "'else' without a previous 'if' (macro expansion hazard)",
    "Q099": "missing include header file without mock header",
    "Q100": "invalid type argument of unary '*' (macro with trailing semicolon)",
}

BANK_INTENTIONAL_RUNTIME_FAULTS = {
    "Q026": "NULL pointer dereference (SIGSEGV)",
    "Q043": "integer division by zero (SIGFPE)",
    "Q047": "modifying string literal in read-only section (SIGSEGV)",
    "Q061": "dangling pointer to expired stack frame",
    "Q069": "infinite recursion stack overflow",
}


def _run_gcc_compile(c_code, flags=None, extra_files=None):
    """
    Compiles a C code snippet with GCC to an object file in a temporary directory.
    Returns (returncode, stdout, stderr).
    """
    if flags is None:
        flags = ["-std=c99", "-c"]

    temp_dir = tempfile.mkdtemp(prefix="c_arena_test_")
    c_file = os.path.join(temp_dir, "snippet.c")
    obj_file = os.path.join(temp_dir, "snippet.o")

    try:
        # Write any extra files needed for compilation (e.g. dummy headers)
        if extra_files:
            for fname, fcontent in extra_files.items():
                with open(os.path.join(temp_dir, fname), "w", encoding="utf-8") as f:
                    f.write(fcontent)

        with open(c_file, "w", encoding="utf-8") as f:
            f.write(c_code)

        cmd = ["gcc"] + flags + [c_file, "-o", obj_file]
        res = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=15,
            cwd=temp_dir
        )
        return res.returncode, res.stdout, res.stderr
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)


class TestSyllabusCSnippetsCompilation(unittest.TestCase):
    """Verifies that normal syllabus C snippets compile cleanly and intentional compile errors fail as expected."""

    @classmethod
    def setUpClass(cls):
        # Verify GCC presence
        gcc_path = shutil.which("gcc")
        if not gcc_path:
            raise unittest.SkipTest("GCC is not available in the test environment.")

        cls.syllabus_questions = _load_bank(
            "generate_syllabus_questions",
            ["syllabus_part1", "syllabus_part2", "syllabus_part3"]
        )

    # -------------------------------------------------------------------------
    # Syllabus Question Bank Compilation Tests
    # -------------------------------------------------------------------------

    def test_syllabus_intentional_compile_errors_fail(self):
        """
        Verify that all questions designated as testing compiler errors in syllabus bank
        actually fail compilation under GCC with informative error diagnostics.
        """
        for q in self.syllabus_questions:
            qid = q["id"]
            if qid in SYLLABUS_INTENTIONAL_COMPILE_ERRORS:
                retcode, stdout, stderr = _run_gcc_compile(q["code"])
                self.assertNotEqual(
                    retcode, 0,
                    f"[{qid}] Expected intentional compile error, but GCC compiled successfully with exit code 0!\nCode:\n{q['code']}"
                )
                self.assertTrue(
                    len(stderr.strip()) > 0,
                    f"[{qid}] Expected compiler error diagnostics in stderr, got empty stderr."
                )

    def test_syllabus_normal_snippets_compile_cleanly(self):
        """
        All questions in syllabus that are NOT intentional compiler errors
        must compile cleanly under GCC with exit code 0.
        Catches uncompilable syntax fragments (such as naked Q065, Q076, Q085, Q094).
        """
        failures = []
        for q in self.syllabus_questions:
            qid = q["id"]
            if qid in SYLLABUS_INTENTIONAL_COMPILE_ERRORS:
                continue

            retcode, stdout, stderr = _run_gcc_compile(q["code"])
            if retcode != 0:
                failures.append({
                    "id": qid,
                    "title": q["title"],
                    "retcode": retcode,
                    "stderr": stderr.strip(),
                    "code": q["code"]
                })

        if failures:
            msg_lines = [f"Total normal snippets failing GCC compilation: {len(failures)}"]
            for f in failures:
                msg_lines.append(f"\n--- [{f['id']}] {f['title']} (exit code {f['retcode']}) ---")
                msg_lines.append(f"Error diagnostics:\n{f['stderr']}")
                msg_lines.append(f"Snippet Code:\n{f['code']}")
            self.fail("\n".join(msg_lines))

    def test_syllabus_runtime_fault_documentation(self):
        """
        Questions with intentional runtime faults (SIGSEGV, infinite loops, stack overflow)
        must document the fault in options or explanation.
        """
        for q in self.syllabus_questions:
            qid = q["id"]
            if qid in SYLLABUS_INTENTIONAL_RUNTIME_FAULTS:
                full_text = (
                    q["prompt"] + " " +
                    q["explanation"]["summary"] + " " +
                    q["explanation"]["deepDive"] + " " +
                    " ".join(opt["text"] for opt in q["options"])
                ).lower()

                has_mention = any(
                    term in full_text
                    for term in ["infinite loop", "crash", "segmentation fault", "stack overflow", "hang", "undefined behavior", "runtime error"]
                )
                self.assertTrue(
                    has_mention,
                    f"[{qid}] Question tests runtime fault ({SYLLABUS_INTENTIONAL_RUNTIME_FAULTS[qid]}), but neither explanation nor options document the crash/hang."
                )

class TestAlternativeBankCSnippetsCompilation(unittest.TestCase):
    """Verifies that normal alternative bank C snippets compile cleanly and intentional compile errors fail as expected."""

    @classmethod
    def setUpClass(cls):
        # Verify GCC presence
        gcc_path = shutil.which("gcc")
        if not gcc_path:
            raise unittest.SkipTest("GCC is not available in the test environment.")

        cls.bank_questions = _load_bank(
            "generate_questions",
            ["bank_part1", "bank_part2", "bank_part3", "bank_part4"]
        )

    # -------------------------------------------------------------------------
    # Alternative Question Bank (bank_part1..4) Compilation Tests
    # -------------------------------------------------------------------------

    def test_bank_intentional_compile_errors_fail(self):
        """
        Verify that all questions designated as compiler errors in bank_part1..4
        actually fail compilation under GCC.
        """
        for q in self.bank_questions:
            qid = q["id"]
            if qid in BANK_INTENTIONAL_COMPILE_ERRORS:
                retcode, stdout, stderr = _run_gcc_compile(q["code"])
                self.assertNotEqual(
                    retcode, 0,
                    f"[{qid}] Expected intentional compile error, but GCC compiled successfully with exit code 0!\nCode:\n{q['code']}"
                )

    def test_bank_normal_snippets_compile_cleanly(self):
        """
        All questions in bank_part1..4 that are NOT intentional compile errors
        must compile cleanly under GCC with exit code 0.
        """
        failures = []
        for q in self.bank_questions:
            qid = q["id"]
            if qid in BANK_INTENTIONAL_COMPILE_ERRORS:
                continue

            retcode, stdout, stderr = _run_gcc_compile(q["code"])
            if retcode != 0:
                failures.append({
                    "id": qid,
                    "title": q["title"],
                    "retcode": retcode,
                    "stderr": stderr.strip(),
                    "code": q["code"]
                })

        if failures:
            msg_lines = [f"Total normal snippets in alternative bank failing GCC compilation: {len(failures)}"]
            for f in failures:
                msg_lines.append(f"\n--- [{f['id']}] {f['title']} (exit code {f['retcode']}) ---")
                msg_lines.append(f"Error diagnostics:\n{f['stderr']}")
            self.fail("\n".join(msg_lines))

    def test_bank_runtime_fault_documentation(self):
        """
        Questions with intentional runtime faults in bank_part1..4
        must document the fault in options or explanation.
        """
        for q in self.bank_questions:
            qid = q["id"]
            if qid in BANK_INTENTIONAL_RUNTIME_FAULTS:
                full_text = (
                    q["prompt"] + " " +
                    q["explanation"]["summary"] + " " +
                    q["explanation"]["deepDive"] + " " +
                    " ".join(opt["text"] for opt in q["options"])
                ).lower()

                has_mention = any(
                    term in full_text
                    for term in ["infinite loop", "crash", "segmentation fault", "stack overflow", "dangling pointer", "undefined behavior", "runtime error", "sigsegv", "sigfpe"]
                )
                self.assertTrue(
                    has_mention,
                    f"[{qid}] Question tests runtime fault ({BANK_INTENTIONAL_RUNTIME_FAULTS[qid]}), but neither explanation nor options document it."
                )


if __name__ == "__main__":
    unittest.main()
