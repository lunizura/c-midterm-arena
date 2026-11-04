"""
run_all_tests.py
Master test runner for the C Midterm Arena automated test suite.

Executes all test suites across:
- tests/test_question_schema.py (Tier 1 & Tier 2: Schema, Balances, Traces, Memory)
- tests/test_c_snippets.py (Tier 1 & Tier 2: GCC C99 Compilation, Compiler Errors, Runtime Faults)
- tests/test_build_pipeline.py (Tier 1: Bundling, Artifact Generation, SHA-256 Sync)
- tests/test_html_integrity.py (Tier 1-4: Control Chars, Deep Dives, Timers, Shortcuts, Escaping)

Exit Code Semantics:
- 0: All tests pass (100% test suite success).
- 1: One or more test suites failed (defects detected).
"""

import io
import os
import sys
import time
import unittest

# Ensure Windows terminal handles UTF-8 cleanly
if sys.platform == "win32" and hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

SUITE_MODULES = [
    ("Question Schema & Pedagogy (Tiers 1 & 2)", "tests.test_question_schema"),
    ("C Snippets GCC Compilation (Tiers 1 & 2)", "tests.test_c_snippets"),
    ("Build & Asset Pipeline (Tier 1)", "tests.test_build_pipeline"),
    ("HTML Deliverable Integrity & UX (Tiers 1-4)", "tests.test_html_integrity"),
]


def run_suite(module_name):
    """Loads and executes a single test module, returning (result, elapsed_seconds)."""
    import importlib
    loader = unittest.TestLoader()
    mod = importlib.import_module(module_name)
    suite = loader.loadTestsFromModule(mod)

    # Use a string buffer to capture standard unittest dot output
    buf = io.StringIO()
    runner = unittest.TextTestRunner(stream=buf, verbosity=1)
    start_time = time.time()
    result = runner.run(suite)
    elapsed = time.time() - start_time
    return result, elapsed


def print_banner():
    print("=" * 80)
    print("           C MIDTERM ARENA — MASTER E2E AUTOMATED TEST RUNNER           ")
    print("=" * 80)
    print(f"Repository Root : {REPO_ROOT}")
    print(f"Python Runtime  : {sys.version.split()[0]}")
    print("=" * 80)
    print()


def main():
    print_banner()

    suite_results = []
    total_tests = 0
    total_passed = 0
    total_failed = 0
    total_errors = 0
    total_skipped = 0
    total_elapsed = 0.0

    all_failures_detail = []

    for suite_desc, mod_path in SUITE_MODULES:
        print(f"Running: {suite_desc} ...", flush=True)
        res, elapsed = run_suite(mod_path)
        total_elapsed += elapsed

        run_count = res.testsRun
        fail_count = len(res.failures)
        err_count = len(res.errors)
        skip_count = len(res.skipped)
        pass_count = run_count - (fail_count + err_count + skip_count)

        total_tests += run_count
        total_passed += pass_count
        total_failed += fail_count
        total_errors += err_count
        total_skipped += skip_count

        status_str = "PASS" if (fail_count == 0 and err_count == 0) else "DEFECTS DETECTED"
        suite_results.append({
            "desc": suite_desc,
            "module": mod_path,
            "tests": run_count,
            "passed": pass_count,
            "failed": fail_count,
            "errors": err_count,
            "skipped": skip_count,
            "elapsed": elapsed,
            "status": status_str,
        })

        if res.failures or res.errors:
            for test_case, trace in res.failures:
                # Find the AssertionError line and its message
                reason = ""
                trace_lines = trace.strip().splitlines()
                for idx, line in enumerate(trace_lines):
                    if line.startswith("AssertionError:"):
                        rest = line[len("AssertionError:"):].strip()
                        if rest:
                            reason = line
                        else:
                            # Look at subsequent non-empty lines
                            for next_idx in range(idx + 1, len(trace_lines)):
                                if trace_lines[next_idx].strip():
                                    reason = f"AssertionError: {trace_lines[next_idx].strip()}"
                                    break
                            if not reason:
                                reason = line
                        break
                    elif "Error:" in line or "Exception:" in line:
                        reason = line
                        break
                if not reason:
                    reason = trace.strip().splitlines()[-1] if trace.strip() else "Assertion failed"
                all_failures_detail.append((suite_desc, str(test_case), "FAILURE", reason))
            for test_case, trace in res.errors:
                reason = trace.strip().splitlines()[-1] if trace.strip() else "Error occurred"
                all_failures_detail.append((suite_desc, str(test_case), "ERROR", reason))

    # Print Summary Table
    print("\n" + "=" * 80)
    print("                        TEST SUITE EXECUTION SUMMARY                    ")
    print("=" * 80)
    print(f"{'Suite':<45} | {'Tests':>5} | {'Pass':>5} | {'Fail':>5} | {'Status':<16}")
    print("-" * 80)

    for r in suite_results:
        print(f"{r['desc']:<45} | {r['tests']:>5} | {r['passed']:>5} | {r['failed']:>5} | {r['status']:<16}")

    print("-" * 80)
    overall_status = "ALL TESTS PASSED" if (total_failed == 0 and total_errors == 0) else "DEFECTS ESCALATED"
    print(f"{'OVERALL TOTALS':<45} | {total_tests:>5} | {total_passed:>5} | {total_failed:>5} | {overall_status:<16}")
    print("=" * 80)
    print(f"Total Duration: {total_elapsed:.2f} seconds\n")

    # If there are failures, print summary of defects
    if all_failures_detail:
        print("=" * 80)
        print("                 CATALOG OF DETECTED IMPLEMENTATION DEFECTS              ")
        print("=" * 80)
        for i, (suite_name, test_name, fail_type, trace) in enumerate(all_failures_detail, 1):
            # Extract the assertion message or last line of trace
            last_line = trace.strip().splitlines()[-1] if trace.strip() else ""
            print(f"[{i}] {test_name}")
            print(f"    Suite  : {suite_name}")
            print(f"    Result : {fail_type}")
            print(f"    Reason : {last_line}")
            print()
        print("=" * 80)

    if total_failed > 0 or total_errors > 0:
        print(f"Execution finished with {total_failed} failure(s) and {total_errors} error(s).")
        return 1
    else:
        print("Execution finished: 100% of tests passed successfully.")
        return 0


if __name__ == "__main__":
    sys.exit(main())
