# syllabus_part2.py
# Q035 - Q050: TOPIC_CONDITIONALS (if, if-else, switch-case)
# Q051 - Q068: TOPIC_LOOPS (for, while, do-while, break, continue)

def load_part2(add_q):
    # =========================================================================
    # TOPIC_CONDITIONALS (Q035 - Q050)
    # =========================================================================

    # Q035: Assignment in If Condition (if (x = 5))
    add_q(
        35, "TOPIC_CONDITIONALS", "Easy", "Assignment (=) in If Condition",
        "What is the output of the following program?",
        """#include <stdio.h>
int main() {
    int x = 0;
    if (x = 5) {
        printf("TRUE %d\\n", x);
    } else {
        printf("FALSE %d\\n", x);
    }
    return 0;
}""",
        5, "if (x = 5)", "= is ASSIGNMENT, not comparison (==)! x is assigned 5. Since 5 is non-zero, condition is TRUE!",
        [
            ("A", "TRUE 5", True, "x is assigned 5. The expression evaluates to 5 (true), printing TRUE 5.", ""),
            ("B", "FALSE 0", False, "Thought it checked x == 5 (since x was 0, it would be false).", "= modifies x and yields the assigned value."),
            ("C", "Compile error", False, "Assignment inside if is valid C syntax.", "Compilers issue a warning, but it compiles."),
            ("D", "TRUE 0", False, "x was modified to 5.", "Value is 5.")
        ],
        "An assignment expression has the value of the left operand after assignment. x = 5 yields 5 (true).",
        "ISO/IEC 9899 §6.5.16 & §6.8.4.1",
        "Prints TRUE 5.",
        [(1, 5, "x is assigned 5. Condition evaluates to 5 (true).", {"x": 5}, None),
         (2, 6, "printf prints TRUE 5.", {"stdout": "TRUE 5"}, None)]
    )

    # Q036: Assignment of Zero in If Condition (if (x = 0))
    add_q(
        36, "TOPIC_CONDITIONALS", "Easy", "Assignment of 0 in If Condition",
        "What is the output of the following program?",
        """#include <stdio.h>
int main() {
    int x = 10;
    if (x = 0) {
        printf("YES\\n");
    } else {
        printf("NO %d\\n", x);
    }
    return 0;
}""",
        5, "if (x = 0)", "x is assigned 0. The expression evaluates to 0 (false), so execution enters the else branch with x = 0!",
        [
            ("A", "NO 0", True, "x is assigned 0. 0 is false, executing the else block with x = 0.", ""),
            ("B", "YES", False, "Thought x was originally 10 so it was true.", "x was overwritten by 0."),
            ("C", "NO 10", False, "Thought x was not modified.", "x is assigned 0."),
            ("D", "Compile error", False, "Valid C syntax.", "Assignment inside if compiles.")
        ],
        "x = 0 assigns 0 to x and produces value 0. In C, 0 represents false.",
        "ISO/IEC 9899 §6.5.16",
        "Prints NO 0.",
        [(1, 5, "x assigned 0. Expression value 0 is false.", {"x": 0}, None),
         (2, 8, "else branch executes: prints NO 0.", {"stdout": "NO 0"}, None)]
    )

    # Q037: Semicolon after If Statement
    add_q(
        37, "TOPIC_CONDITIONALS", "Easy", "Accidental Semicolon After if-Statement",
        "What is the output of the following program?",
        """#include <stdio.h>
int main() {
    int x = 2;
    if (x > 5); {
        printf("GREATER\\n");
    }
    return 0;
}""",
        5, "if (x > 5);", "The semicolon terminates the if-statement immediately! The block { printf(...); } is an independent block that ALWAYS runs!",
        [
            ("A", "GREATER", True, "The semicolon acts as an empty statement for the if condition. The braced block executes unconditionally.", ""),
            ("B", "No output", False, "Assumed { printf(...); } was controlled by if (x > 5).", "The semicolon on line 5 ends the if statement prematurely."),
            ("C", "Compile error", False, "A lone semicolon is a valid null statement in C.", "Valid C syntax."),
            ("D", "Undefined Behavior", False, "Completely well-defined behavior.", "Always runs the block.")
        ],
        "A semicolon after if creates a null statement as the conditional body. The block after it runs unconditionally.",
        "ISO/IEC 9899 §6.8.4.1",
        "Prints GREATER.",
        [(1, 5, "if (x > 5); evaluates to false, terminating the null statement.", None, None),
         (2, 5, "Independent block entered: prints GREATER.", {"stdout": "GREATER"}, None)]
    )

    # Q038: Dangling Else Association
    add_q(
        38, "TOPIC_CONDITIONALS", "Tricky", "Dangling Else Association Rule",
        "What is the output of the following program?",
        """#include <stdio.h>
int main() {
    int a = 0, b = 1;
    if (a == 1)
        if (b == 1)
            printf("BOTH\\n");
    else
        printf("ELSE\\n");
    return 0;
}""",
        9, "else", "In C, an else ALWAYS binds to the NEAREST preceding unmatched if, regardless of visual indentation! The else belongs to if (b == 1)!",
        [
            ("A", "No output", True, "The else belongs to if (b == 1). Because outer if (a == 1) is false, the entire nested if-else is skipped!", ""),
            ("B", "ELSE", False, "Deceived by visual indentation. Indentation has no syntactic meaning in C.", "The else binds to the nearest if (b == 1), NOT outer if (a == 1)."),
            ("C", "BOTH", False, "a is 0, so condition fails.", "First condition fails."),
            ("D", "Compile error", False, "Dangling else is resolved by standard grammar rules.", "Valid C syntax.")
        ],
        "An else is associated with the lexically nearest preceding if that does not already have an else.",
        "ISO/IEC 9899 §6.8.4.1#3",
        "Outer condition a == 1 is false (0 == 1), so nothing is printed.",
        [(1, 5, "Outer condition a == 1 is false.", None, None),
         (2, 5, "Nested if and its else are both skipped. No output.", None, None)]
    )

    # Q039: Truthiness of Negative Numbers
    add_q(
        39, "TOPIC_CONDITIONALS", "Easy", "Truthiness of Non-Zero Values in C",
        "What is the output of the following program?",
        """#include <stdio.h>
int main() {
    int x = -10;
    if (x) {
        printf("TRUE\\n");
    } else {
        printf("FALSE\\n");
    }
    return 0;
}""",
        5, "if (x)", "In C, ANY non-zero value (including negative numbers like -10) evaluates to TRUE! Only 0 is false!",
        [
            ("A", "TRUE", True, "-10 is non-zero, so condition evaluates to true.", ""),
            ("B", "FALSE", False, "Thought negative numbers are false.", "In C, only 0 is false; all non-zero values are true."),
            ("C", "Compile error", False, "Integer expressions in if conditions are standard.", "Valid C syntax."),
            ("D", "Undefined Behavior", False, "Condition evaluation is strictly defined.", "Prints TRUE.")
        ],
        "An expression is true if its value compares unequal to 0.",
        "ISO/IEC 9899 §6.8.4.1",
        "Prints TRUE.",
        [(1, 5, "x is -10 (non-zero) -> true.", None, None),
         (2, 6, "printf prints TRUE.", {"stdout": "TRUE"}, None)]
    )

    # Q040: Switch Fallthrough Without Break
    add_q(
        40, "TOPIC_CONDITIONALS", "Easy", "Switch Case Fallthrough Without Break",
        "What is the output of the following program?",
        """#include <stdio.h>
int main() {
    int x = 2;
    switch (x) {
        case 1: printf("ONE ");
        case 2: printf("TWO ");
        case 3: printf("THREE ");
        default: printf("DEFAULT\\n");
    }
    return 0;
}""",
        8, "case 2: printf(\"TWO \");", "There are NO break statements! Once execution enters case 2, it FALLS THROUGH all subsequent cases!",
        [
            ("A", "TWO THREE DEFAULT", True, "Execution jumps to case 2 and falls through case 3 and default due to missing break statements.", ""),
            ("B", "TWO", False, "Assumed switch cases automatically break like in Go or Swift.", "In C, switch cases fall through by default unless break is used."),
            ("C", "ONE TWO THREE DEFAULT", False, "Thought all cases executed.", "Jumps directly to matching case 2."),
            ("D", "DEFAULT", False, "Thought default overrode matched cases.", "default executes only on fallthrough or if no case matches.")
        ],
        "Switch statements in C feature fall-through semantics. Flow of control continues until a break is hit.",
        "ISO/IEC 9899 §6.8.4.2",
        "Prints TWO THREE DEFAULT.",
        [(1, 6, "x = 2 matches case 2.", None, None),
         (2, 7, "Prints TWO . Falls through into case 3.", {"stdout": "TWO "}, None),
         (3, 8, "Prints THREE . Falls through into default.", {"stdout": "TWO THREE "}, None),
         (4, 9, "Prints DEFAULT.", {"stdout": "TWO THREE DEFAULT"}, None)]
    )

    # Q041: Switch Default at Top With Fallthrough
    add_q(
        41, "TOPIC_CONDITIONALS", "Medium", "Switch Default at Beginning with Fallthrough",
        "What is the output when x = 5 (no matching case)?",
        """#include <stdio.h>
int main() {
    int x = 5;
    switch (x) {
        default: printf("DEF ");
        case 1: printf("ONE ");
        case 2: printf("TWO\\n");
    }
    return 0;
}""",
        6, "default: printf(\"DEF \");", "When no case matches, execution jumps to default at the top and FALLS THROUGH case 1 and case 2!",
        [
            ("A", "DEF ONE TWO", True, "default matches x = 5. Because there is no break, it falls through case 1 and case 2.", ""),
            ("B", "DEF", False, "Assumed default breaks automatically.", "default requires break just like any case."),
            ("C", "No output", False, "Thought default must be at the end.", "default can appear anywhere inside a switch block."),
            ("D", "Compile error", False, "Placement of default at the top is valid C.", "Standard C syntax.")
        ],
        "The default label can be placed anywhere inside the switch body. If no case matches, execution jumps to default and continues sequentially.",
        "ISO/IEC 9899 §6.8.4.2",
        "Prints DEF ONE TWO.",
        [(1, 6, "No case matches x = 5. Jumps to default.", None, None),
         (2, 6, "Prints DEF . Falls into case 1.", {"stdout": "DEF "}, None),
         (3, 7, "Prints ONE . Falls into case 2.", {"stdout": "DEF ONE "}, None),
         (4, 8, "Prints TWO.", {"stdout": "DEF ONE TWO"}, None)]
    )

    # Q042: Switch Case Label Must Be Constant
    add_q(
        42, "TOPIC_CONDITIONALS", "Medium", "Variable in Switch Case Label",
        "What happens when compiling this code?",
        """#include <stdio.h>
int main() {
    int x = 2, y = 2;
    switch (x) {
        case y: printf("MATCH\\n"); break;
        default: printf("DEF\\n");
    }
    return 0;
}""",
        6, "case y:", "In C, case labels MUST be compile-time integer constant expressions! Using a variable y causes a COMPILATION ERROR!",
        [
            ("A", "Compilation Error: case label does not reduce to an integer constant", True, "In C, case labels must be compile-time integer constants, not variables.", ""),
            ("B", "Prints MATCH", False, "Thought variable y (val 2) matched x.", "C syntax strictly forbids variables in case labels."),
            ("C", "Prints DEF", False, "Thought it jumped to default.", "Compiler rejects the code before running."),
            ("D", "Undefined Behavior", False, "Fails at compile time.", "Constraint violation.")
        ],
        "The expression of each case label shall be an integer constant expression.",
        "ISO/IEC 9899 §6.8.4.2#3",
        "Use literal constants or enum values in case labels.",
        [(1, 6, "Compiler error: case label does not reduce to an integer constant.", None, None)]
    )

    # Q043: Switch Floating Point Case Prohibited
    add_q(
        43, "TOPIC_CONDITIONALS", "Easy", "Floating-Point in Switch Statement",
        "What happens when passing a float to a switch statement?",
        """#include <stdio.h>
int main() {
    float f = 2.5f;
    switch (f) {
        case 2: printf("TWO\\n"); break;
    }
    return 0;
}""",
        5, "switch (f)", "In C, the controlling expression of a switch statement MUST have integer type! float/double is a COMPILATION ERROR!",
        [
            ("A", "Compilation Error: switch quantity not an integer", True, "The switch controlling expression must have an integer type (or char/enum). Floats are forbidden.", ""),
            ("B", "Truncates float to 2 and prints TWO", False, "Thought C automatically cast float to int in switch.", "C does not allow floating point switch expressions."),
            ("C", "Runtime crash", False, "Fails at compile time.", "Compiler rejects non-integer switch expressions."),
            ("D", "Undefined Behavior", False, "Syntax error.", "Constraint violation.")
        ],
        "The controlling expression of a switch statement shall have integer type.",
        "ISO/IEC 9899 §6.8.4.2#1",
        "Compiler emits: error: switch quantity not an integer.",
        [(1, 5, "Compiler error: switch quantity not an integer.", None, None)]
    )

    # Q044: Switch Duplicate Case Labels
    add_q(
        44, "TOPIC_CONDITIONALS", "Easy", "Duplicate Case Labels in Switch",
        "What happens when compiling this code?",
        """#include <stdio.h>
int main() {
    int x = 1;
    switch (x) {
        case 1: printf("FIRST "); break;
        case 1: printf("SECOND "); break;
    }
    return 0;
}""",
        7, "case 1: printf(\"SECOND \");", "Duplicate case labels within the same switch block are strictly FORBIDDEN and cause a COMPILATION ERROR!",
        [
            ("A", "Compilation Error: duplicate case value", True, "No two case labels in the same switch statement may have the same constant value.", ""),
            ("B", "Prints FIRST", False, "Thought compiler picked the first match.", "Compiler halts on duplicate case values."),
            ("C", "Prints SECOND", False, "Thought second case overwrote first.", "Duplicate case values are illegal."),
            ("D", "Undefined Behavior", False, "Fails at compile time.", "Constraint violation.")
        ],
        "No two of the case constant expressions in the same switch statement shall have the same value.",
        "ISO/IEC 9899 §6.8.4.2#3",
        "Compiler emits: error: duplicate case value.",
        [(1, 7, "Compiler error: duplicate case value 1.", None, None)]
    )

    # Q045: Multiple Case Labels for One Action
    add_q(
        45, "TOPIC_CONDITIONALS", "Easy", "Grouping Multiple Case Labels",
        "What is the output of the following program?",
        """#include <stdio.h>
int main() {
    char ch = 'b';
    switch (ch) {
        case 'a':
        case 'b':
        case 'c':
            printf("LOW\\n");
            break;
        default:
            printf("OTHER\\n");
    }
    return 0;
}""",
        7, "case 'b':", "Stacking case labels without break allows multiple cases to share the same execution block! 'b' prints LOW!",
        [
            ("A", "LOW", True, "ch matches 'b' and executes the shared printf(\"LOW\\n\"); break; block.", ""),
            ("B", "OTHER", False, "Thought missing code between case 'a' and 'b' skipped to default.", "Fallthrough allows grouping cases."),
            ("C", "Compile error", False, "Stacking case labels is standard C idiom.", "Valid C syntax."),
            ("D", "LOW OTHER", False, "break prevents fallthrough into default.", "Exits on break.")
        ],
        "Cases without statements fall through directly to the next case statement, enabling multi-value matching.",
        "ISO/IEC 9899 §6.8.4.2",
        "Prints LOW.",
        [(1, 7, "ch = 'b' matches case 'b'. Falls into printf('LOW'). break exits switch.", {"stdout": "LOW"}, None)]
    )

    # Q046: Indentation Illusion Without Braces
    add_q(
        46, "TOPIC_CONDITIONALS", "Medium", "Missing Braces Indentation Illusion",
        "What is the output of the following program?",
        """#include <stdio.h>
int main() {
    int x = 2;
    if (x == 5)
        printf("A ");
        printf("B ");
        printf("C\\n");
    return 0;
}""",
        7, "printf(\"B \");", "Without braces {}, ONLY the first statement (printf(\"A \")) is governed by if (x == 5)! Statements B and C ALWAYS execute!",
        [
            ("A", "B C", True, "Only 'A' is inside the if statement. 'B' and 'C' execute unconditionally.", ""),
            ("B", "No output", False, "Deceived by visual indentation (Python-style).", "In C, indentation is ignored; only braces {} group statements."),
            ("C", "A B C", False, "x is 2, not 5, so 'A' does not print.", "Condition fails."),
            ("D", "Compile error", False, "Indentation without braces is valid C.", "Common beginner logic bug.")
        ],
        "An if statement without braces controls only the single following statement. Indentation has no syntactic meaning in C.",
        "ISO/IEC 9899 §6.8.4.1",
        "Prints B C.",
        [(1, 5, "x == 5 is false. Statement 1 (printf 'A') is skipped.", None, None),
         (2, 7, "printf 'B ' runs unconditionally.", {"stdout": "B "}, None),
         (3, 8, "printf 'C' runs unconditionally.", {"stdout": "B C"}, None)]
    )

    # Q047: Switch Expression with Character
    add_q(
        47, "TOPIC_CONDITIONALS", "Easy", "Character in Switch Expression",
        "What is printed by this code?",
        """#include <stdio.h>
int main() {
    char grade = 'B';
    switch (grade) {
        case 'A': printf("EXCELLENT\\n"); break;
        case 'B': printf("GOOD\\n"); break;
        default: printf("POOR\\n");
    }
    return 0;
}""",
        7, "case 'B': printf(\"GOOD\\n\"); break;", "Characters in C are integral types and match their ASCII values in switch statements, printing GOOD!",
        [
            ("A", "GOOD", True, "grade matches 'B' and prints GOOD.", ""),
            ("B", "EXCELLENT", False, "grade is 'B', not 'A'.", "Matches case 'B'."),
            ("C", "POOR", False, "grade matched an explicit case.", "default is skipped."),
            ("D", "Compile error", False, "Characters are integral types valid in switch.", "Standard C syntax.")
        ],
        "Character constants promote to int and are valid switch cases.",
        "ISO/IEC 9899 §6.8.4.2",
        "Prints GOOD.",
        [(1, 7, "grade matches 'B'. Prints GOOD.", {"stdout": "GOOD"}, None)]
    )

    # Q048: Nested If-Else Boolean Logic
    add_q(
        48, "TOPIC_CONDITIONALS", "Medium", "Nested If-Else Boundary Evaluation",
        "What is printed when score = 75?",
        """#include <stdio.h>
int main() {
    int score = 75;
    if (score >= 80)
        printf("A\\n");
    else if (score >= 70)
        printf("B\\n");
    else if (score >= 60)
        printf("C\\n");
    else
        printf("D\\n");
    return 0;
}""",
        7, "else if (score >= 70)", "score >= 80 is false (75 < 80). First else-if (75 >= 70) is TRUE, printing B and terminating the chain!",
        [
            ("A", "B", True, "75 is not >= 80, but is >= 70, so B is printed.", ""),
            ("B", "B C D", False, "Thought subsequent else-if blocks ran.", "else-if chain terminates as soon as one condition succeeds."),
            ("C", "A", False, "75 is not >= 80.", "First condition fails."),
            ("D", "C", False, "75 is >= 70.", "B matched first.")
        ],
        "In an if-else-if ladder, the first matching branch executes and the remaining branches are bypassed.",
        "ISO/IEC 9899 §6.8.4.1",
        "Prints B.",
        [(1, 5, "score >= 80 is false.", None, None),
         (2, 7, "score >= 70 is true. Prints B.", {"stdout": "B"}, None)]
    )

    # Q049: Accidental Equality vs Assignment in If
    add_q(
        49, "TOPIC_CONDITIONALS", "Medium", "Testing Variable Against Zero with Assignment",
        "What is the output of the following program?",
        """#include <stdio.h>
int main() {
    int is_logged_in = 1;
    if (is_logged_in = 0) {
        printf("WELCOME\\n");
    } else {
        printf("DENIED %d\\n", is_logged_in);
    }
    return 0;
}""",
        5, "if (is_logged_in = 0)", "Programmer meant == 0, but wrote = 0! Variable is overwritten with 0 (false), printing DENIED 0!",
        [
            ("A", "DENIED 0", True, "is_logged_in is set to 0. Condition evaluates to 0 (false), running the else branch.", ""),
            ("B", "WELCOME", False, "Thought it checked if is_logged_in was originally 1.", "Assignment overwrites value."),
            ("C", "DENIED 1", False, "Thought variable was not modified.", "Assignment modifies variable."),
            ("D", "Compile error", False, "Assignment inside if is valid C.", "Standard beginner trap.")
        ],
        "Assignment operator (=) sets the variable to 0. 0 is false.",
        "ISO/IEC 9899 §6.5.16",
        "Prints DENIED 0.",
        [(1, 5, "is_logged_in assigned 0. 0 is false.", {"is_logged_in": 0}, None),
         (2, 8, "else branch prints DENIED 0.", {"stdout": "DENIED 0"}, None)]
    )

    # Q050: Switch Variable Scoping Without Braces
    add_q(
        50, "TOPIC_CONDITIONALS", "Tricky", "Variable Declaration Directly in Switch Case",
        "What happens when compiling this code in C99?",
        """#include <stdio.h>
int main() {
    int x = 1;
    switch (x) {
        case 1:
            int val = 10; // Declaration right after case label
            printf("%d\\n", val);
            break;
    }
    return 0;
}""",
        7, "int val = 10;", "In C, a label (like case 1:) cannot be directly followed by a declaration without an intervening statement or enclosing braces { ... }!",
        [
            ("A", "Compilation Error: a label can only be part of a statement and a declaration is not a statement", True, "In ISO C, case labels cannot directly precede a variable declaration unless enclosed in { } or after a statement.", ""),
            ("B", "Prints 10", False, "Assumed C99 allows declarations anywhere.", "C grammar restricts declarations directly after labels. Wrapping in { int val = 10; ... } fixes it."),
            ("C", "Prints 0", False, "Fails at compile time.", "Grammar constraint violation."),
            ("D", "Undefined Behavior", False, "Compiler rejects it.", "Compilation error.")
        ],
        "A label shall be followed by a statement. A declaration is not a statement in C grammar.",
        "ISO/IEC 9899 §6.8.1",
        "Fix: enclose in braces: case 1: { int val = 10; ... }.",
        [(1, 7, "Compiler error: a label can only be part of a statement and a declaration is not a statement.", None, None)]
    )

    # =========================================================================
    # TOPIC_LOOPS (Q051 - Q068)
    # =========================================================================

    # Q051: Basic For Loop Counting
    add_q(
        51, "TOPIC_LOOPS", "Easy", "For Loop Iteration Bound",
        "How many times does this loop iterate?",
        """#include <stdio.h>
int main() {
    int count = 0;
    for (int i = 0; i < 5; i++) {
        count++;
    }
    printf("%d\\n", count);
    return 0;
}""",
        5, "for (int i = 0; i < 5; i++)", "i starts at 0 and increments while i < 5: takes values 0, 1, 2, 3, 4 (EXACTLY 5 TIMES)!",
        [
            ("A", "5", True, "Loop runs for i = 0, 1, 2, 3, 4 (5 iterations). count = 5.", ""),
            ("B", "4", False, "Counted 1 to 4, forgetting 0.", "i starts at 0."),
            ("C", "6", False, "Thought it stopped when i <= 5.", "Strict < 5 condition stops before 5."),
            ("D", "0", False, "Loop executes.", "Standard for loop.")
        ],
        "for (i = 0; i < 5; i++) executes for i in {0,1,2,3,4}.",
        "ISO/IEC 9899 §6.8.5.3",
        "Prints 5.",
        [(1, 5, "Runs for i = 0, 1, 2, 3, 4. count increments to 5.", {"count": 5}, None)]
    )

    # Q052: Semicolon After For Loop Header
    add_q(
        52, "TOPIC_LOOPS", "Medium", "Accidental Semicolon After for-Loop Header",
        "What is the output of the following program?",
        """#include <stdio.h>
int main() {
    int i;
    for (i = 0; i < 5; i++);
    {
        printf("%d\\n", i);
    }
    return 0;
}""",
        5, "for (i = 0; i < 5; i++);", "The semicolon after for(...) makes the loop execute an EMPTY statement 5 times! When loop finishes, i is 5, printing 5 ONCE!",
        [
            ("A", "5", True, "The loop completes all 5 iterations doing nothing. When i reaches 5, loop exits and prints 5 once.", ""),
            ("B", "0 1 2 3 4", False, "Assumed the block was inside the loop.", "The semicolon on line 5 ends the loop body."),
            ("C", "4", False, "Thought i was 4 upon loop termination.", "Loop terminates when i < 5 is false (at i = 5)."),
            ("D", "0", False, "Loop executed 5 times.", "i is 5.")
        ],
        "The for-loop body is the null statement ';'. It loops until i = 5. The subsequent block runs once.",
        "ISO/IEC 9899 §6.8.5.3",
        "Prints 5.",
        [(1, 5, "Loop iterates null body for i = 0, 1, 2, 3, 4. Exits with i = 5.", {"i": 5}, None),
         (2, 7, "Block executes once: prints 5.", {"stdout": "5"}, None)]
    )

    # Q053: For Loop Header Scope in C99
    add_q(
        53, "TOPIC_LOOPS", "Medium", "C99 For-Loop Variable Scope",
        "What happens when compiling this code?",
        """#include <stdio.h>
int main() {
    for (int i = 0; i < 3; i++) {
        printf("%d ", i);
    }
    printf("%d\\n", i); // Note: i accessed outside
    return 0;
}""",
        7, "printf(\"%d\\n\", i);", "In C99, variables declared inside the for-loop header (for (int i = 0; ...)) are SCOPED TO THE LOOP! Accessing i outside causes a COMPILATION ERROR!",
        [
            ("A", "Compilation Error: 'i' undeclared", True, "In C99+, variable i declared in the for-loop header is destroyed when the loop terminates.", ""),
            ("B", "Prints 0 1 2 3", False, "Assumed i survives loop exit.", "i is strictly block-scoped to the loop."),
            ("C", "Prints 0 1 2 2", False, "i does not exist outside the loop.", "Scope ends at closing brace."),
            ("D", "Prints 0 1 2 0", False, "Fails at compile time.", "Identifier undeclared.")
        ],
        "Names declared in the for-loop header have block scope terminating at the end of the for statement.",
        "ISO/IEC 9899 §6.8.5.3#1",
        "Compiler emits: error: 'i' undeclared.",
        [(1, 7, "Compiler error: 'i' undeclared (first use in this function).", None, None)]
    )

    # Q054: While Loop Postfix Decrement in Condition
    add_q(
        54, "TOPIC_LOOPS", "Medium", "Postfix Decrement in While Condition",
        "What is the output of the following program?",
        """#include <stdio.h>
int main() {
    int x = 3;
    while (x-- > 0) {
        printf("%d ", x);
    }
    printf("\\n");
    return 0;
}""",
        5, "while (x-- > 0)", "Postfix x-- tests the old value > 0, then decrements immediately before entering the loop body! The body sees x = 2, 1, 0!",
        [
            ("A", "2 1 0", True, "Test 3 > 0 (x becomes 2, prints 2); Test 2 > 0 (x becomes 1, prints 1); Test 1 > 0 (x becomes 0, prints 0); Test 0 > 0 (x becomes -1, exits).", ""),
            ("B", "3 2 1", False, "Thought decrement happened after the loop body.", "Postfix side effect completes before body executes."),
            ("C", "3 2 1 0", False, "Counted 4 iterations.", "Test fails when x was 0."),
            ("D", "2 1", False, "Missed the 0 iteration.", "When old x is 1, 1 > 0 is true, x decrements to 0 and prints 0.")
        ],
        "The condition tests value before decrement, then decrements x before the body executes.",
        "ISO/IEC 9899 §6.5.2.4 & §6.8.5.1",
        "Prints 2 1 0.",
        [(1, 5, "x-- tests 3 > 0 (true). x becomes 2. Prints 2.", {"x": 2}, None),
         (2, 5, "x-- tests 2 > 0 (true). x becomes 1. Prints 1.", {"x": 1}, None),
         (3, 5, "x-- tests 1 > 0 (true). x becomes 0. Prints 0.", {"x": 0}, None),
         (4, 5, "x-- tests 0 > 0 (false). x becomes -1. Loop exits.", {"x": -1}, None)]
    )

    # Q055: While Loop Prefix Decrement in Condition
    add_q(
        55, "TOPIC_LOOPS", "Medium", "Prefix Decrement in While Condition",
        "What is the output of the following program?",
        """#include <stdio.h>
int main() {
    int x = 3;
    while (--x > 0) {
        printf("%d ", x);
    }
    printf("\\n");
    return 0;
}""",
        5, "while (--x > 0)", "--x decrements BEFORE comparison: x becomes 2 (test 2 > 0, prints 2), then 1 (test 1 > 0, prints 1), then 0 (test 0 > 0 is false, loop exits)!",
        [
            ("A", "2 1", True, "Iteration 1: x becomes 2, prints 2. Iteration 2: x becomes 1, prints 1. Iteration 3: x becomes 0, loop terminates.", ""),
            ("B", "2 1 0", False, "Confused prefix with postfix decrement.", "Prefix decrements before testing; 0 > 0 is false, so 0 is never printed."),
            ("C", "3 2 1", False, "Thought x started at 3.", "x is decremented to 2 before first test."),
            ("D", "1 0", False, "Missed first iteration.", "First test is 2 > 0.")
        ],
        "--x decrements x, then yields the decremented value for the > 0 comparison.",
        "ISO/IEC 9899 §6.5.3.1 & §6.8.5.1",
        "Prints 2 1.",
        [(1, 5, "--x decrements to 2. 2 > 0 is true. Prints 2.", {"x": 2}, None),
         (2, 5, "--x decrements to 1. 1 > 0 is true. Prints 1.", {"x": 1}, None),
         (3, 5, "--x decrements to 0. 0 > 0 is false. Loop exits.", {"x": 0}, None)]
    )

    # Q056: Do-While Execution Guarantee
    add_q(
        56, "TOPIC_LOOPS", "Easy", "Do-While Minimum Execution Guarantee",
        "How many times does the body of this do-while loop execute?",
        """#include <stdio.h>
int main() {
    int x = 10;
    do {
        printf("RUN\\n");
    } while (x < 5);
    return 0;
}""",
        7, "} while (x < 5);", "A do-while loop evaluates its condition AFTER the body runs! It is GUARANTEED to execute at least ONCE even if condition is false!",
        [
            ("A", "1 time", True, "do-while executes the body first, tests 10 < 5 (false), and exits.", ""),
            ("B", "0 times", False, "Confused do-while with while loop.", "A standard while loop tests before body; do-while tests after body."),
            ("C", "Infinite times", False, "Condition 10 < 5 is false, exiting immediately.", "Does not loop infinitely."),
            ("D", "Compile error", False, "Valid do-while syntax.", "Requires trailing semicolon.")
        ],
        "The controlling expression of a do statement is evaluated after each execution of the loop body.",
        "ISO/IEC 9899 §6.8.5.2",
        "Prints RUN once.",
        [(1, 5, "Body executes first: prints RUN.", {"stdout": "RUN"}, None),
         (2, 7, "Condition 10 < 5 evaluates to false. Loop exits.", None, None)]
    )

    # Q057: Do-While Semicolon Requirement
    add_q(
        57, "TOPIC_LOOPS", "Easy", "Do-While Trailing Semicolon Requirement",
        "What happens if the trailing semicolon is omitted from a do-while loop?",
        """#include <stdio.h>
int main() {
    int x = 0;
    do {
        x++;
    } while (x < 3) // Missing semicolon here
    return 0;
}""",
        7, "} while (x < 3)", "In C grammar, the do-while loop explicitly REQUIRES a terminating semicolon after while(condition);! Omitting it is a COMPILATION ERROR!",
        [
            ("A", "Compilation Error: expected ';' before 'return'", True, "Unlike for and while loops, do-while statements must end with a semicolon.", ""),
            ("B", "Compiles and runs normally", False, "Semicolons are mandatory in C statement grammar.", "Compiler syntax error."),
            ("C", "Infinite loop", False, "Fails at compile time.", "Does not run."),
            ("D", "Undefined Behavior", False, "Syntax error.", "Rejected by compiler.")
        ],
        "The syntax for a do-while loop is: do statement while ( expression ) ;",
        "ISO/IEC 9899 §6.8.5",
        "Compiler emits: error: expected ';' before 'return'.",
        [(1, 7, "Compiler error: expected ';' before 'return'.", None, None)]
    )

    # Q058: Break Statement Scope
    add_q(
        58, "TOPIC_LOOPS", "Medium", "Break Exiting Innermost Loop Only",
        "What is the output of the following nested loop program?",
        """#include <stdio.h>
int main() {
    for (int i = 0; i < 2; i++) {
        for (int j = 0; j < 3; j++) {
            if (j == 1) break;
            printf("%d%d ", i, j);
        }
    }
    printf("\\n");
    return 0;
}""",
        6, "if (j == 1) break;", "break exits ONLY the INNERMOST loop! The outer loop continues executing!",
        [
            ("A", "00 10", True, "In each outer iteration, j = 0 prints, then j = 1 breaks inner loop. Outer loop runs for i = 0 and i = 1.", ""),
            ("B", "00", False, "Thought break exited both loops.", "break exits only the enclosing innermost loop."),
            ("C", "00 01 10 11", False, "j == 1 broke before printing.", "Prints only when j = 0."),
            ("D", "00 01 02", False, "Outer loop also ran.", "Outer loop runs twice.")
        ],
        "A break statement terminates execution of the smallest enclosing switch or iteration statement.",
        "ISO/IEC 9899 §6.8.6.3",
        "Prints 00 10.",
        [(1, 5, "i = 0, j = 0: prints 00. j = 1: break inner.", {"stdout": "00 "}, None),
         (2, 5, "i = 1, j = 0: prints 10. j = 1: break inner.", {"stdout": "00 10"}, None)]
    )

    # Q059: Continue Statement in For Loop
    add_q(
        59, "TOPIC_LOOPS", "Easy", "Continue Skipping to Update Expression",
        "What is the output of the following program?",
        """#include <stdio.h>
int main() {
    for (int i = 0; i < 4; i++) {
        if (i == 2) continue;
        printf("%d ", i);
    }
    printf("\\n");
    return 0;
}""",
        5, "if (i == 2) continue;", "continue skips the REST of the loop body and jumps directly to the update expression (i++)! i = 2 is skipped!",
        [
            ("A", "0 1 3", True, "When i is 2, continue skips printf. Loop resumes with i = 3, printing 0 1 3.", ""),
            ("B", "0 1", False, "Confused continue with break.", "break exits the loop; continue only skips the current iteration."),
            ("C", "0 1 2 3", False, "Thought continue had no effect.", "printf was bypassed for i = 2."),
            ("D", "2", False, "Inverted the logic.", "2 was skipped.")
        ],
        "In a for statement, continue causes the loop continuation portion (clause-3) to be evaluated next.",
        "ISO/IEC 9899 §6.8.6.2",
        "Prints 0 1 3.",
        [(1, 5, "i = 0, 1 printed. When i = 2, continue skips printf. i = 3 printed.", {"stdout": "0 1 3"}, None)]
    )

    # Q060: Continue in While Loop Infinite Loop Trap
    add_q(
        60, "TOPIC_LOOPS", "Tricky", "Continue Skipping While Loop Increment",
        "What happens when running this code?",
        """#include <stdio.h>
int main() {
    int i = 0;
    while (i < 3) {
        if (i == 1) continue;
        printf("%d ", i);
        i++;
    }
    return 0;
}""",
        6, "if (i == 1) continue;", "continue in a while loop jumps to the condition test, SKIPPING i++! i remains 1 FOREVER, causing an INFINITE LOOP!",
        [
            ("A", "Infinite Loop (prints 0, then hangs forever at i = 1)", True, "When i becomes 1, continue skips the i++ statement. The condition (1 < 3) repeats forever.", ""),
            ("B", "Prints 0 2", False, "In while loops, continue skips to the test, NOT an automatic increment.", "i is never incremented past 1."),
            ("C", "Prints 0 1 2", False, "1 is never printed.", "Skips printf."),
            ("D", "Compile error", False, "Valid syntax, runtime infinite loop.", "Logic bug.")
        ],
        "In a while statement, continue passes control directly to the conditional test. Unlike a for loop, there is no automatic step expression.",
        "ISO/IEC 9899 §6.8.6.2",
        "Hang/infinite loop.",
        [(1, 5, "i = 0: prints 0, i becomes 1.", {"stdout": "0 "}, None),
         (2, 6, "i = 1: continue jumps to while (1 < 3). i++ is bypassed -> Infinite loop.", None, None)]
    )

    # Q061: Nested Loop Iteration Count
    add_q(
        61, "TOPIC_LOOPS", "Easy", "Nested Loop Total Iteration Count",
        "How many times is 'HELLO' printed?",
        """#include <stdio.h>
int main() {
    int count = 0;
    for (int i = 0; i < 3; i++) {
        for (int j = 0; j < 4; j++) {
            count++;
        }
    }
    printf("%d\\n", count);
    return 0;
}""",
        6, "for (int j = 0; j < 4; j++)", "Outer loop runs 3 times; inner loop runs 4 times for each outer iteration: 3 * 4 = 12 total iterations!",
        [
            ("A", "12", True, "Total iterations = 3 * 4 = 12.", ""),
            ("B", "7", False, "Added 3 + 4 instead of multiplying.", "Nested loops multiply."),
            ("C", "9", False, "3 * 3.", "Inner runs 4 times."),
            ("D", "16", False, "4 * 4.", "Outer runs 3 times.")
        ],
        "Multiplicative property of nested loops: N_outer * N_inner.",
        "ISO/IEC 9899 §6.8.5",
        "Prints 12.",
        [(1, 6, "count = 3 * 4 = 12.", {"count": 12}, None)]
    )

    # Q062: Unsigned Underflow Loop Trap
    add_q(
        62, "TOPIC_LOOPS", "Tricky", "Unsigned Integer Non-Terminating Loop",
        "What happens when running this loop?",
        """#include <stdio.h>
int main() {
    unsigned int i;
    for (i = 3; i >= 0; i--) {
        printf("%u ", i);
        if (i == 0) break; // If this break were omitted?
    }
    return 0;
}""",
        5, "i >= 0", "Without the break, because i is UNSIGNED, i >= 0 is ALWAYS TRUE! 0 decrements to UINT_MAX, causing an INFINITE LOOP!",
        [
            ("A", "Without the break, it is an infinite loop because unsigned int is always >= 0", True, "Unsigned integers cannot be negative. 0 - 1 wraps to UINT_MAX (4,294,967,295), which is >= 0.", ""),
            ("B", "It terminates naturally after printing 0", False, "Thought 0 decremented to -1.", "Unsigned integers wrap around to positive UINT_MAX."),
            ("C", "Compile error", False, "i >= 0 on unsigned compiles with warning.", "Valid C syntax."),
            ("D", "Segmentation fault", False, "Integer looping does not fault memory.", "Runs continuously.")
        ],
        "Unsigned integers represent non-negative values. i >= 0 is a tautology (always true) for unsigned types.",
        "ISO/IEC 9899 §6.2.5#9",
        "Wraps to UINT_MAX -> infinite loop.",
        [(1, 5, "i = 3, 2, 1, 0. If decremented past 0, wraps to 4294967295 -> Infinite loop.", None, None)]
    )

    # Q063: Floating-Point Loop Termination Fallacy
    add_q(
        63, "TOPIC_LOOPS", "Tricky", "Floating Point Equality in Loop Condition",
        "Why is while (f != 1.0) dangerous when incrementing f += 0.1 ?",
        """#include <stdio.h>
int main() {
    float f = 0.0f;
    while (f != 1.0f) {
        f += 0.1f;
    }
    return 0;
}""",
        5, "while (f != 1.0f)", "0.1 cannot be represented exactly in binary floating point! Accumulated roundoff error causes f to SKIP exact 1.0f, causing an INFINITE LOOP!",
        [
            ("A", "Infinite loop due to floating-point representation error skipping exact 1.0f", True, "Repeated addition of 0.1f accumulates rounding errors; f becomes 0.999999... then 1.0000001..., never exactly 1.0f.", ""),
            ("B", "Terminates after 10 iterations", False, "Assumed 10 * 0.1 = 1.0 exactly in IEEE 754 float.", "Binary cannot represent 0.1 exactly."),
            ("C", "Compile error", False, "while (f != 1.0f) is valid syntax.", "Compiles cleanly."),
            ("D", "Terminates immediately", False, "f starts at 0.0f.", "Runs infinitely.")
        ],
        "Never use exact equality (!= or ==) as termination conditions for floating-point loops.",
        "ISO/IEC 9899 §6.8.5",
        "Infinite loop.",
        [(1, 5, "Accumulated rounding error: f skips exact 1.0f -> Infinite loop.", None, None)]
    )

    # Q064: Multiple Loop Expressions (for (i=0, j=5; ...))
    add_q(
        64, "TOPIC_LOOPS", "Medium", "Multiple Control Variables in For Loop",
        "What is the output of the following program?",
        """#include <stdio.h>
int main() {
    int i, j;
    for (i = 0, j = 4; i < j; i++, j--) {
        printf("%d%d ", i, j);
    }
    printf("\\n");
    return 0;
}""",
        5, "for (i = 0, j = 4; i < j; i++, j--)", "i increases while j decreases until i and j cross at 2: prints 04 then 13!",
        [
            ("A", "04 13", True, "Iter 1: i=0, j=4 (0 < 4). Iter 2: i=1, j=3 (1 < 3). Iter 3: i=2, j=2 (2 < 2 is false, loop exits).", ""),
            ("B", "04 13 22", False, "Thought condition was i <= j.", "Condition is strict i < j; 2 < 2 is false."),
            ("C", "04", False, "Loop ran twice.", "1 < 3 was also true."),
            ("D", "Compile error", False, "Multiple initializations with comma are valid.", "Standard C idiom.")
        ],
        "The comma operator allows multiple initializations and updates in for headers.",
        "ISO/IEC 9899 §6.8.5.3",
        "Prints 04 13.",
        [(1, 5, "Iter 1: 04. Iter 2: 13. Iter 3: 2 < 2 is false.", {"stdout": "04 13"}, None)]
    )

    # Q065: Infinite Loop with for(;;)
    add_q(
        65, "TOPIC_LOOPS", "Easy", "Omitting Clauses in For Loop Header",
        "What is the behavior of: for (;;) ?",
        """for (;;) {
    // code
}""",
        1, "for (;;)", "In C, an omitted condition in a for loop is treated as non-zero (CONSTANT TRUE), creating an infinite loop!",
        [
            ("A", "An infinite loop (equivalent to while(1))", True, "ISO C §6.8.5.3 explicitly specifies that an omitted condition-2 in for(;;) is replaced by a constant non-zero value.", ""),
            ("B", "A compilation error", False, "All three clauses of a for loop are optional.", "Standard C infinite loop idiom."),
            ("C", "A loop that executes zero times", False, "Omitted condition defaults to true, not false.", "Executes infinitely."),
            ("D", "A loop that executes once", False, "Continues forever.", "Infinite loop.")
        ],
        "Both clause-1 and clause-3 can be omitted; an omitted clause-2 is replaced by a nonzero constant.",
        "ISO/IEC 9899 §6.8.5.3#2",
        "Infinite loop.",
        [(1, 1, "for(;;) has omitted test -> defaults to true -> Infinite loop.", None, None)]
    )

    # Q066: While Loop with False Initial Condition
    add_q(
        66, "TOPIC_LOOPS", "Easy", "While Loop False Initial Condition",
        "How many times does this while loop execute?",
        """#include <stdio.h>
int main() {
    int x = 10;
    while (x < 5) {
        printf("RUN\\n");
        x++;
    }
    return 0;
}""",
        5, "while (x < 5)", "A while loop tests its condition BEFORE entering the body! Since 10 < 5 is false, it executes ZERO times!",
        [
            ("A", "0 times (body is never entered)", True, "While loops test condition first; 10 < 5 is false, so body never runs.", ""),
            ("B", "1 time", False, "Confused while loop with do-while loop.", "do-while runs once; while pre-tests."),
            ("C", "5 times", False, "x starts at 10.", "Never entered."),
            ("D", "Infinite times", False, "Condition is immediately false.", "Terminates instantly.")
        ],
        "A while loop tests the controlling expression before each execution of the loop body.",
        "ISO/IEC 9899 §6.8.5.1",
        "No output.",
        [(1, 5, "x = 10 < 5 is false. Body skipped completely.", None, None)]
    )

    # Q067: Nested Loop Coordinate Output
    add_q(
        67, "TOPIC_LOOPS", "Medium", "Tracing Nested Loop Indices",
        "What is the output of the following program?",
        """#include <stdio.h>
int main() {
    for (int i = 1; i <= 2; i++) {
        for (int j = 1; j <= 2; j++) {
            printf("%d ", i * j);
        }
    }
    printf("\\n");
    return 0;
}""",
        6, "printf(\"%d \", i * j);", "i=1: j=1 (1), j=2 (2). i=2: j=1 (2), j=2 (4). Outputs 1 2 2 4!",
        [
            ("A", "1 2 2 4", True, "i=1,j=1 -> 1. i=1,j=2 -> 2. i=2,j=1 -> 2. i=2,j=2 -> 4.", ""),
            ("B", "1 2 3 4", False, "Arithmetic error.", "2 * 1 = 2, not 3."),
            ("C", "2 4", False, "Only counted i=2.", "i=1 also ran."),
            ("D", "1 4", False, "Missed cross products.", "All 4 combinations execute.")
        ],
        "Nested loop execution: i=1 gives 1, 2; i=2 gives 2, 4.",
        "ISO/IEC 9899 §6.8.5",
        "Prints 1 2 2 4.",
        [(1, 5, "i=1, j=1..2: prints 1 2.", {"stdout": "1 2 "}, None),
         (2, 5, "i=2, j=1..2: prints 2 4.", {"stdout": "1 2 2 4"}, None)]
    )

    # Q068: Loop with Comma Condition
    add_q(
        68, "TOPIC_LOOPS", "Tricky", "Comma Operator in Loop Termination Condition",
        "How many times does this loop iterate?",
        """#include <stdio.h>
int main() {
    int i = 0, j = 0;
    while (i < 2, j < 4) {
        i++;
        j++;
    }
    printf("%d %d\\n", i, j);
    return 0;
}""",
        5, "while (i < 2, j < 4)", "The comma operator discards i < 2! The loop condition is governed EXCLUSIVELY by j < 4!",
        [
            ("A", "4 4", True, "i < 2 is evaluated and discarded. Only j < 4 controls loop termination, running 4 times.", ""),
            ("B", "2 2", False, "Assumed comma acted like logical AND (&&).", "Comma operator discards the left operand!"),
            ("C", "2 4", False, "Both i and j increment together inside the body.", "i++ and j++ both run 4 times."),
            ("D", "Infinite loop", False, "j reaches 4 and terminates the loop.", "Valid loop condition.")
        ],
        "The comma operator evaluates left-to-right and discards left result. j < 4 controls termination.",
        "ISO/IEC 9899 §6.5.17",
        "Prints 4 4.",
        [(1, 5, "Loop checks j < 4 (i < 2 is discarded). Runs 4 times.", {"i": 4, "j": 4}, None),
         (2, 9, "printf prints 4 4.", {"stdout": "4 4"}, None)]
    )

print("syllabus_part2 loaded (34 questions, total 68).")
