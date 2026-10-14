# bank_part4.py: Q081 to Q100 (CAT_CONTROL_FLOW & CAT_MACRO_PREPROC)

def load_part4(add_q):
    # =========================================================================
    # CAT_CONTROL_FLOW (Q081 - Q090)
    # =========================================================================

    # Q081: Semicolon after If Statement
    add_q(
        81, "CAT_CONTROL_FLOW", "Easy", "Accidental Semicolon After if-Statement",
        "What is the output of the following program?",
        """#include <stdio.h>
int main() {
    int x = 2;
    if (x > 5); {
        printf("GREATER\\n");
    }
    return 0;
}""",
        5, "if (x > 5);", "The semicolon immediately terminates the if-statement! The block { printf(...); } is an independent compound block that ALWAYS executes!",
        [
            ("A", "GREATER", True, "The semicolon acts as an empty statement for the if condition. The braced block executes unconditionally.", ""),
            ("B", "No output", False, "Assumed { printf(...); } was the body controlled by if (x > 5).", "The semicolon on line 5 ends the if statement prematurely."),
            ("C", "Compilation error", False, "Thought semicolon after if is illegal.", "A lone semicolon is a valid null statement in C."),
            ("D", "Undefined Behavior", False, "Thought it creates an invalid construct.", "Completely well-defined behavior.")
        ],
        "A semicolon after an if condition creates a null statement as the conditional body. The subsequent block { ... } is simply an unconditioned inner block.",
        "ISO/IEC 9899 §6.8.4.1",
        "Because the block is independent, GREATER is printed regardless of x.",
        [
            (1, 5, "if (x > 5); evaluates to false, terminating the null statement.", None, None),
            (2, 5, "Independent block { ... } entered. printf prints GREATER.", {"stdout": "GREATER"}, None)
        ]
    )

    # Q082: Semicolon after For Loop
    add_q(
        82, "CAT_CONTROL_FLOW", "Medium", "Accidental Semicolon After for-Loop Header",
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
        5, "for (i = 0; i < 5; i++);", "The semicolon after for(...) makes the loop execute an EMPTY statement 5 times! When the loop finishes, i is 5, printing 5 ONCE!",
        [
            ("A", "5", True, "The loop completes all 5 iterations doing nothing. When i reaches 5, it exits and prints 5.", ""),
            ("B", "0 1 2 3 4", False, "Assumed the block was inside the loop body.", "The semicolon terminates the loop body; the block runs only once after loop completion."),
            ("C", "4", False, "Thought i was 4 upon loop termination.", "The loop exits when i < 5 is false, which occurs at i = 5."),
            ("D", "0", False, "Thought the loop did not execute.", "The loop iterated 5 times.")
        ],
        "The for-loop body is the null statement ';'. It loops from i = 0 to 4. When i becomes 5, i < 5 is false, exiting the loop. The subsequent block prints 5.",
        "ISO/IEC 9899 §6.8.5.3",
        "Output is 5.",
        [
            (1, 5, "Loop runs null body for i = 0, 1, 2, 3, 4. Exits with i = 5.", {"i": 5}, None),
            (2, 7, "Block executes once: prints 5.", {"stdout": "5"}, None)
        ]
    )

    # Q083: Assignment in If Condition (if (x = 5))
    add_q(
        83, "CAT_CONTROL_FLOW", "Easy", "Assignment (=) in Conditional Statement",
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
        5, "if (x = 5)", "= is an ASSIGNMENT, not comparison (==)! x is assigned 5, which evaluates to 5 (non-zero / true)!",
        [
            ("A", "TRUE 5", True, "x is assigned 5. Since 5 is non-zero, the condition is true, printing TRUE 5.", ""),
            ("B", "FALSE 0", False, "Assumed condition checked x == 5 (since x was 0, it would be false).", "= assigns; == compares. Assignment evaluates to the assigned value."),
            ("C", "Compilation error", False, "Thought assignment inside if is illegal.", "C permits assignments inside conditions."),
            ("D", "TRUE 0", False, "Thought x remained 0.", "x was updated to 5.")
        ],
        "An assignment expression has the value of the left operand after the assignment. x = 5 produces value 5, which is non-zero (true).",
        "ISO/IEC 9899 §6.5.16 & §6.8.4.1",
        "x becomes 5 and the true branch executes.",
        [
            (1, 5, "x assigned 5. Expression evaluates to 5 (true).", {"x": 5}, None),
            (2, 6, "printf prints TRUE 5.", {"stdout": "TRUE 5"}, None)
        ]
    )

    # Q084: Assignment of Zero in If Condition (if (x = 0))
    add_q(
        84, "CAT_CONTROL_FLOW", "Easy", "Assignment of Zero in If Condition",
        "What is the output of the following program?",
        """#include <stdio.h>
int main() {
    int x = 10;
    if (x = 0) {
        printf("BRANCH A\\n");
    } else {
        printf("BRANCH B %d\\n", x);
    }
    return 0;
}""",
        5, "if (x = 0)", "x is assigned 0. The expression evaluates to 0 (false), so execution branches to the else block with x = 0!",
        [
            ("A", "BRANCH B 0", True, "x is assigned 0. Since 0 is false, the else branch executes with x = 0.", ""),
            ("B", "BRANCH A 10", False, "Thought x was originally 10 so it was true.", "x was overwritten by 0."),
            ("C", "BRANCH B 10", False, "Thought x was not modified.", "Assignment modifies x to 0."),
            ("D", "Compile error", False, "Thought x = 0 is a syntax error.", "Valid syntax.")
        ],
        "x = 0 assigns 0 to x and yields 0. In C, 0 represents false. Execution takes the else branch.",
        "ISO/IEC 9899 §6.5.16",
        "Output is BRANCH B 0.",
        [
            (1, 5, "x assigned 0. Expression value 0 is false.", {"x": 0}, None),
            (2, 8, "else branch executes: prints BRANCH B 0.", {"stdout": "BRANCH B 0"}, None)
        ]
    )

    # Q085: Switch Fallthrough Without Break
    add_q(
        85, "CAT_CONTROL_FLOW", "Easy", "Switch Case Fallthrough without break",
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
            ("B", "TWO", False, "Assumed switch cases automatically break like in modern languages (Go, Swift).", "In C, switch cases fall through by default unless explicit break is used."),
            ("C", "ONE TWO THREE DEFAULT", False, "Thought all cases executed.", "Execution jumps directly to matching case 2."),
            ("D", "DEFAULT", False, "Thought default overrode matched cases.", "default only matches if no case matched, or via fallthrough.")
        ],
        "Switch statements in C feature fall-through semantics. Flow of control continues into subsequent cases until a break statement is hit.",
        "ISO/IEC 9899 §6.8.4.2",
        "Prints TWO THREE DEFAULT.",
        [
            (1, 6, "x = 2 matches case 2.", None, None),
            (2, 7, "Prints TWO . Falls through to case 3.", {"stdout": "TWO "}, None),
            (3, 8, "Prints THREE . Falls through to default.", {"stdout": "TWO THREE "}, None),
            (4, 9, "Prints DEFAULT.", {"stdout": "TWO THREE DEFAULT"}, None)
        ]
    )

    # Q086: Switch Default Placed at Top Without Break
    add_q(
        86, "CAT_CONTROL_FLOW", "Medium", "Switch Default at Beginning with Fallthrough",
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
            ("D", "Compile error", False, "Thought default at the top is invalid syntax.", "Placement of default is arbitrary.")
        ],
        "The default label can be placed anywhere inside the switch body. If no case matches, execution jumps to default and continues sequentially.",
        "ISO/IEC 9899 §6.8.4.2",
        "Prints DEF ONE TWO.",
        [
            (1, 6, "x = 5 has no case match. Jumps to default.", None, None),
            (2, 6, "Prints DEF . Falls into case 1.", {"stdout": "DEF "}, None),
            (3, 7, "Prints ONE . Falls into case 2.", {"stdout": "DEF ONE "}, None),
            (4, 8, "Prints TWO.", {"stdout": "DEF ONE TWO"}, None)
        ]
    )

    # Q087: Dangling Else Ambiguity
    add_q(
        87, "CAT_CONTROL_FLOW", "Tricky", "Dangling Else Association",
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
            ("B", "ELSE", False, "Fooled by visual indentation! Indentation has no syntactic meaning in C.", "The else binds to the nearest if (b == 1), NOT if (a == 1)."),
            ("C", "BOTH", False, "a is 0, not 1.", "First condition fails."),
            ("D", "Compile error", False, "Thought ambiguous else is rejected.", "Resolved unambiguously by standard grammar rules.")
        ],
        "An else is associated with the lexically nearest preceding if in the same block that does not already have an else.",
        "ISO/IEC 9899 §6.8.4.1#3",
        "Outer condition a == 1 is false (0 == 1), so inner (if-else) is bypassed entirely.",
        [
            (1, 5, "Outer condition a == 1 evaluates to false.", None, None),
            (2, 5, "Entire nested body (including the else belonging to inner if) is skipped. No output.", None, None)
        ]
    )

    # Q088: While Loop Decrement Condition (while (x-- > 0))
    add_q(
        88, "CAT_CONTROL_FLOW", "Medium", "Postfix Decrement in Loop Test",
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
            ("A", "2 1 0", True, "Test 3 > 0 (x becomes 2, prints 2); Test 2 > 0 (x becomes 1, prints 1); Test 1 > 0 (x becomes 0, prints 0); Test 0 > 0 (x becomes -1, loop exits).", ""),
            ("B", "3 2 1", False, "Thought x was decremented after the loop body.", "Postfix side effect completes at the condition's sequence point before body executes."),
            ("C", "3 2 1 0", False, "Counted 4 iterations.", "Test fails when x was 0."),
            ("D", "2 1", False, "Missed the 0 iteration.", "When old x is 1, 1 > 0 is true, x decrements to 0 and prints 0.")
        ],
        "The condition x-- > 0 checks the value before decrement, then decrements x before the body is entered.",
        "ISO/IEC 9899 §6.5.2.4 & §6.8.5.1",
        "Prints 2 1 0.",
        [
            (1, 5, "Iter 1: Test 3 > 0 (true). x becomes 2. Body prints 2.", {"x": 2}, None),
            (2, 5, "Iter 2: Test 2 > 0 (true). x becomes 1. Body prints 1.", {"x": 1}, None),
            (3, 5, "Iter 3: Test 1 > 0 (true). x becomes 0. Body prints 0.", {"x": 0}, None),
            (4, 5, "Iter 4: Test 0 > 0 (false). x becomes -1. Loop terminates.", {"x": -1}, None)
        ]
    )

    # Q089: do-while(0) Pattern
    add_q(
        89, "CAT_CONTROL_FLOW", "Easy", "do-while(0) Execution Guarantee",
        "How many times does the body of a do-while(0) statement execute?",
        """#include <stdio.h>
int main() {
    int count = 0;
    do {
        count++;
    } while (0);
    printf("%d\\n", count);
    return 0;
}""",
        5, "do { ... } while (0);", "A do-while loop evaluates its condition AFTER the body runs! It is GUARANTEED to execute at least ONCE!",
        [
            ("A", "Exactly once", True, "do-while executes the body first, then checks while (0) and exits immediately.", ""),
            ("B", "Zero times", False, "Confused do-while with while(0).", "while(0) executes 0 times; do-while(0) executes once."),
            ("C", "Infinite times", False, "0 is false, terminating the loop.", "Exits after condition check."),
            ("D", "Compile error", False, "Thought while(0) is invalid.", "do { ... } while(0) is standard C idiom for multi-statement macros.")
        ],
        "The controlling expression of a do statement is evaluated after each execution of the loop body. Condition 0 is false, so it exits after 1 iteration.",
        "ISO/IEC 9899 §6.8.5.2",
        "count is incremented to 1.",
        [
            (1, 5, "Body entered: count++ -> 1.", {"count": 1}, None),
            (2, 7, "Condition 0 evaluated: false. Loop exits.", None, None),
            (3, 8, "printf prints 1.", {"stdout": "1"}, None)
        ]
    )

    # Q090: Unsigned Loop Termination Trap
    add_q(
        90, "CAT_CONTROL_FLOW", "Tricky", "Unsigned Integer Non-Terminating Loop",
        "What happens when running this loop?",
        """#include <stdio.h>
int main() {
    unsigned int i;
    for (i = 3; i >= 0; i--) {
        printf("%u ", i);
        if (i == 0) break; // If this line were omitted?
    }
    return 0;
}""",
        5, "i >= 0", "Without the break, because i is UNSIGNED, i >= 0 is ALWAYS TRUE! 0 decrements to UINT_MAX, causing an INFINITE LOOP!",
        [
            ("A", "Without the break, it is an infinite loop because unsigned int is always >= 0", True, "Unsigned integers cannot be negative; 0 - 1 wraps to UINT_MAX (4294967295), which is >= 0.", ""),
            ("B", "It terminates naturally after printing 0", False, "Thought 0-- becomes -1.", "Unsigned numbers wrap around to positive UINT_MAX instead of becoming negative."),
            ("C", "It causes a compilation error", False, "i >= 0 on unsigned compiles (with compiler warning).", "Valid C code."),
            ("D", "It terminates with a segmentation fault", False, "Looping integers does not crash memory.", "Runs continuously.")
        ],
        "Unsigned integers represent only non-negative values. The condition i >= 0 is a tautology (always true) for unsigned types.",
        "ISO/IEC 9899 §6.2.5#9",
        "When i is 0, i-- wraps to UINT_MAX (4,294,967,295), maintaining i >= 0 forever.",
        [
            (1, 5, "i = 3, 2, 1, 0. If i decrements from 0, it wraps to 4294967295 -> Infinite loop.", None, None)
        ]
    )

    # =========================================================================
    # CAT_MACRO_PREPROC (Q091 - Q100)
    # =========================================================================

    # Q091: Unparenthesized Macro Parameters (SQUARE(x))
    add_q(
        91, "CAT_MACRO_PREPROC", "Easy", "Unparenthesized Macro Parameter Substitution",
        "What is the output of the following program?",
        """#include <stdio.h>
#define SQUARE(x) x * x
int main() {
    int res = SQUARE(2 + 3);
    printf("%d\\n", res);
    return 0;
}""",
        5, "SQUARE(2 + 3)", "Macros are pure TEXTUAL SUBSTITUTION! SQUARE(2 + 3) expands to 2 + 3 * 2 + 3 = 2 + 6 + 3 = 11, NOT 25!",
        [
            ("A", "11", True, "Expands literally as 2 + 3 * 2 + 3. Multiplication takes precedence: 2 + 6 + 3 = 11.", ""),
            ("B", "25", False, "Assumed SQUARE evaluated (2 + 3) first like a function call (5 * 5 = 25).", "The preprocessor does not evaluate arithmetic; it performs raw text substitution."),
            ("C", "10", False, "Calculated 2 * 5.", "Arithmetic error."),
            ("D", "Compile error", False, "Thought macro calls cannot take expressions.", "Expressions are valid macro arguments.")
        ],
        "The preprocessor replaces SQUARE(2 + 3) with 2 + 3 * 2 + 3. Multiplication (*) binds tighter than addition (+).",
        "ISO/IEC 9899 §6.10.3",
        "To get 25, the macro definition must enclose parameters in parentheses: #define SQUARE(x) ((x) * (x)).",
        [
            (1, 2, "Text replacement: SQUARE(2 + 3) -> 2 + 3 * 2 + 3.", None, None),
            (2, 5, "Operator precedence: 3 * 2 = 6. 2 + 6 + 3 = 11.", {"res": 11}, None),
            (3, 6, "printf prints 11.", {"stdout": "11"}, None)
        ]
    )

    # Q092: Unparenthesized Macro Expression (ADD(a, b) * 4)
    add_q(
        92, "CAT_MACRO_PREPROC", "Easy", "Unparenthesized Macro Expression Body",
        "What is the output of the following program?",
        """#include <stdio.h>
#define ADD(a, b) a + b
int main() {
    int res = ADD(2, 3) * 4;
    printf("%d\\n", res);
    return 0;
}""",
        5, "ADD(2, 3) * 4", "Expands textually to 2 + 3 * 4. Multiplication binds first: 2 + 12 = 14, NOT 20!",
        [
            ("A", "14", True, "ADD(2, 3) * 4 expands to 2 + 3 * 4 = 2 + 12 = 14.", ""),
            ("B", "20", False, "Assumed (2 + 3) * 4 = 20.", "Without parentheses around (a + b), multiplication binds to 3 only."),
            ("C", "24", False, "Multiplied 2 * 3 * 4.", "Arithmetic mistake."),
            ("D", "Compile error", False, "Thought macro syntax is invalid.", "Valid C syntax.")
        ],
        "Text replacement yields 2 + 3 * 4. * has higher precedence than +, yielding 14.",
        "ISO/IEC 9899 §6.10.3",
        "Fix by defining: #define ADD(a, b) ((a) + (b)).",
        [
            (1, 5, "Expansion: 2 + 3 * 4 -> 2 + 12 = 14.", {"res": 14}, None),
            (2, 6, "printf prints 14.", {"stdout": "14"}, None)
        ]
    )

    # Q093: Side Effect Duplication in Macros
    add_q(
        93, "CAT_MACRO_PREPROC", "Tricky", "Side Effect Duplication in Macro Arguments",
        "What is the output of the following program?",
        """#include <stdio.h>
#define DOUBLE(x) ((x) + (x))
int main() {
    int a = 5;
    int b = DOUBLE(a++);
    printf("%d %d\\n", a, b);
    return 0;
}""",
        6, "DOUBLE(a++)", "a++ is duplicated in text expansion: ((a++) + (a++))! a is incremented TWICE (Undefined Behavior in C)!",
        [
            ("A", "Undefined Behavior (Modifying a twice without sequence point)", True, "DOUBLE(a++) expands to ((a++) + (a++)), which modifies scalar a twice without sequence points.", ""),
            ("B", "7 10", False, "Thought a was incremented once.", "Argument a++ appears twice in expansion."),
            ("C", "6 10", False, "Assumed a++ evaluated once before passing to macro.", "Macros do not evaluate arguments prior to expansion."),
            ("D", "7 12", False, "Attempted to calculate two increments.", "Standard defines this as Undefined Behavior.")
        ],
        "Because macros perform text replacement, any argument with side effects (like ++ or --) is evaluated multiple times, creating unsequenced modifications.",
        "ISO/IEC 9899 §6.5#2 & §6.10.3",
        "Compilers emit -Wunsequenced warning.",
        [
            (1, 6, "Expands to ((a++) + (a++)). Unsequenced double modification -> UB.", None, None)
        ]
    )

    # Q094: MAX Macro Side Effect
    add_q(
        94, "CAT_MACRO_PREPROC", "Tricky", "Ternary Macro Double Evaluation",
        "What is the value of x after: int x = 5, y = 3; int m = MAX(x++, y); with MAX(a,b) ((a)>(b)?(a):(b))?",
        """#include <stdio.h>
#define MAX(a, b) ((a) > (b) ? (a) : (b))
int main() {
    int x = 5, y = 3;
    int m = MAX(x++, y);
    printf("%d %d\\n", x, m);
    return 0;
}""",
        6, "MAX(x++, y)", "Expands to ((x++) > (y) ? (x++) : (y)). Since 5 > 3 is true, x++ runs in the condition AND again in the true branch! x becomes 7!",
        [
            ("A", "7 6", True, "Condition evaluates 5 > 3 (x becomes 6). True branch evaluates 6 (x becomes 7, returning 6).", ""),
            ("B", "6 5", False, "Assumed x was incremented only once.", "x++ appears in both the condition and the selected branch of the ternary."),
            ("C", "6 6", False, "Thought x was incremented once after return.", "Increment executes twice across the sequence point of the ? operator."),
            ("D", "5 5", False, "Thought x was not incremented.", "x++ side effects occurred.")
        ],
        "The ternary operator has a sequence point after the first operand. (5 > 3) is true, incrementing x to 6. Then the true branch (x++) runs, yielding 6 and incrementing x to 7.",
        "ISO/IEC 9899 §6.5.15 & §6.10.3",
        "x ends at 7; m ends at 6.",
        [
            (1, 6, "Condition: (x++ > y) -> 5 > 3 (true). x becomes 6.", {"x": 6}, None),
            (2, 6, "True branch: (x++) -> returns 6 for m. x becomes 7.", {"x": 7, "m": 6}, None),
            (3, 7, "printf prints 7 6.", {"stdout": "7 6"}, None)
        ]
    )

    # Q095: Multi-Statement Macro Semicolon Trap
    add_q(
        95, "CAT_MACRO_PREPROC", "Tricky", "Dangling Else in Multi-Statement Macro",
        "Why is #define SWAP(a,b) int t=a; a=b; b=t; dangerous in if-else statements?",
        """#define SWAP(a, b) int t = a; a = b; b = t;
int main() {
    int x = 1, y = 2;
    if (x < y)
        SWAP(x, y);
    else
        x = 0;
    return 0;
}""",
        6, "SWAP(x, y);", "Without do { ... } while(0), the macro expands into multiple statements. The trailing semicolon terminates the if, causing a syntax error on else!",
        [
            ("A", "Compilation Error: 'else' without a previous 'if'", True, "After expansion, only 'int t = a;' is inside the if. Subsequent statements are outside, breaking the else link.", ""),
            ("B", "Variables are swapped properly", False, "Assumed macro creates a single compound block.", "Without braces or do-while, statements are loose."),
            ("C", "Runtime crash", False, "Fails at compile time.", "Grammar syntax error."),
            ("D", "Undefined Behavior", False, "Compilation fails before code runs.", "Syntax violation.")
        ],
        "Expanding SWAP(x,y); results in: if (x < y) int t = x; x = y; y = t;; else x = 0; The else has no matching if.",
        "ISO/IEC 9899 §6.8.4.1",
        "The standard solution is the do { ... } while(0) idiom without trailing semicolon.",
        [
            (1, 6, "Compiler error: expected statement before 'else'.", None, None)
        ]
    )

    # Q096: Stringification Operator (#)
    add_q(
        96, "CAT_MACRO_PREPROC", "Easy", "Stringification Operator (#) Behavior",
        "What is the output of the following program?",
        """#include <stdio.h>
#define PRINT_NAME(x) printf("%s = %d\\n", #x, x)
int main() {
    int total_score = 99;
    PRINT_NAME(total_score);
    return 0;
}""",
        6, "PRINT_NAME(total_score);", "The # operator in a macro STRIGIFIES its argument into a string literal: #x becomes \"total_score\"!",
        [
            ("A", "total_score = 99", True, "#x converts argument token into \"total_score\". x evaluates to 99.", ""),
            ("B", "x = 99", False, "Thought it literally printed \"x\".", "# replaces the parameter with the passed argument's name as a string."),
            ("C", "99 = 99", False, "Thought # evaluated the value as string.", "# stringifies the identifier token, not its value."),
            ("D", "Compile error", False, "Thought # is only for directives.", "# inside macro definitions is the standard stringification operator.")
        ],
        "In a function-like macro, if a parameter is preceded by a # token, both are replaced by a single string literal containing the parameter's argument spelling.",
        "ISO/IEC 9899 §6.10.3.2",
        "Prints total_score = 99.",
        [
            (1, 2, "#x replaced with \"total_score\". x replaced with total_score.", None, None),
            (2, 6, "printf prints total_score = 99.", {"stdout": "total_score = 99"}, None)
        ]
    )

    # Q097: Token Pasting Operator (##)
    add_q(
        97, "CAT_MACRO_PREPROC", "Medium", "Token Pasting Operator (##) Concatenation",
        "What is the output of the following program?",
        """#include <stdio.h>
#define CONCAT(a, b) a ## b
int main() {
    int xy = 42;
    printf("%d\\n", CONCAT(x, y));
    return 0;
}""",
        5, "CONCAT(x, y)", "The ## operator GLUES two tokens together into a single identifier: x ## y becomes token xy (val 42)!",
        [
            ("A", "42", True, "x ## y merges tokens into identifier xy, which evaluates to 42.", ""),
            ("B", "x y", False, "Thought it printed the tokens with space.", "Token pasting concatenates tokens into a single lexical token."),
            ("C", "Compile error: undefined identifier CONCAT", False, "CONCAT is defined as a macro.", "Expands to xy."),
            ("D", "0", False, "Random guess.", "Reads variable xy.")
        ],
        "The ## token-pasting operator concatenates two tokens into a single valid preprocessing token.",
        "ISO/IEC 9899 §6.10.3.3",
        "CONCAT(x, y) becomes xy. printf prints 42.",
        [
            (1, 2, "Tokens x and y pasted into single token xy.", None, None),
            (2, 5, "xy evaluates to 42. printf prints 42.", {"stdout": "42"}, None)
        ]
    )

    # Q098: Header Guard Mechanism (#ifndef)
    add_q(
        98, "CAT_MACRO_PREPROC", "Easy", "Purpose of Header Guards (#ifndef / #define)",
        "What is the primary purpose of header guards (#ifndef MY_HEADER_H ...)?",
        """#ifndef MY_HEADER_H
#define MY_HEADER_H
struct Point { int x, y; };
#endif""",
        1, "#ifndef MY_HEADER_H", "Header guards prevent REDEFINITION ERRORS when the same header file is included multiple times in a translation unit!",
        [
            ("A", "To prevent multiple inclusion of the same header causing duplicate type definitions", True, "Ensures the preprocessor includes the header contents at most once per translation unit.", ""),
            ("B", "To make the header private and prevent other programs from reading it", False, "Header guards do not protect file access permissions.", "Header guards are compile-time inclusion guards."),
            ("C", "To speed up internet download of headers", False, "Headers are local files.", "Nothing to do with networks."),
            ("D", "To automatically export functions as global symbols", False, "Header guards have no effect on symbol linkage.", "Standard preprocessor protection.")
        ],
        "If a header is included twice without guards, type definitions (like struct Point) appear twice, causing compilation error: redefinition of struct.",
        "ISO/IEC 9899 §6.10",
        "Guards skip header text on subsequent inclusions.",
        [
            (1, 1, "First include: MY_HEADER_H not defined -> defined. Second include: MY_HEADER_H defined -> skipped.", None, None)
        ]
    )

    # Q099: Include <> vs Include "" Search Order
    add_q(
        99, "CAT_MACRO_PREPROC", "Medium", "Difference between #include <file> and #include \"file\"",
        "What is the difference between #include <header.h> and #include \"header.h\"?",
        """#include <stdio.h>
#include "my_header.h"
int main() {
    return 0;
}""",
        2, "#include \"my_header.h\"", "\"header.h\" searches the CURRENT source directory first before system paths; <header.h> searches SYSTEM include paths first!",
        [
            ("A", "\"file\" searches the local/current directory first before system include directories; <file> searches system include paths directly", True, "Quoted includes prioritize user source directory; bracket includes prioritize system libraries.", ""),
            ("B", "<file> is for C library files only; \"file\" is for C++ library files", False, "Both are standard C syntax.", "Search directory precedence is the only difference."),
            ("C", "<file> compiles faster than \"file\"", False, "Compilation speed difference is negligible.", "Different directory lookup path."),
            ("D", "\"file\" copies file content; <file> creates a symbolic link", False, "Both perform text replacement.", "Identical inclusion mechanism.")
        ],
        "A #include directive with \"...\" searches in an implementation-defined manner (typically current directory first). If that fails, it searches as if written with <...>.",
        "ISO/IEC 9899 §6.10.2",
        "Used to prioritize local user headers over standard system libraries.",
        [
            (1, 2, "\"my_header.h\" searched in current folder first.", None, None)
        ]
    )

    # Q100: Macro with Trailing Semicolon
    add_q(
        100, "CAT_MACRO_PREPROC", "Medium", "Accidental Semicolon in Macro Definition",
        "What happens when compiling this code?",
        """#include <stdio.h>
#define PI 3.14;
int main() {
    double area = PI * 10 * 10;
    printf("%f\\n", area);
    return 0;
}""",
        2, "#define PI 3.14;", "The semicolon is included in the macro replacement text! It expands to: double area = 3.14; * 10 * 10;, causing a COMPILATION ERROR!",
        [
            ("A", "Compilation Error (Premature semicolon in expression)", True, "PI expands literally to '3.14;'. The statement becomes: double area = 3.14; * 10 * 10;, which is a syntax error.", ""),
            ("B", "Prints 314.000000", False, "Assumed the preprocessor strips semicolons from definitions.", "The preprocessor copies every character verbatim, including semicolons!"),
            ("C", "Prints 3.140000", False, "Thought it assigned 3.14 and ignored the rest.", "Syntax error halts compilation."),
            ("D", "Undefined Behavior", False, "Compilation fails before execution.", "Standard syntax error.")
        ],
        "Macro replacement does not strip trailing semicolons. 'PI * 10' becomes '3.14; * 10', producing an unexpected ';' mid-expression.",
        "ISO/IEC 9899 §6.10.3",
        "Compilers output: error: expected expression before '*' token.",
        [
            (1, 2, "PI defined as '3.14;' with trailing semicolon.", None, None),
            (2, 4, "Expands to: double area = 3.14; * 10 * 10; -> Syntax error.", None, None)
        ]
    )

print("bank_part4 loaded (20 questions, total 100).")
