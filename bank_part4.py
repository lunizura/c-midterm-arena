# bank_part4.py: Q081 to Q100 (CAT_CONTROL_FLOW & CAT_MACRO_PREPROC)
# High-Yield C Midterm Exam Question Bank - Part 4
# Thoroughly upgraded with ISO C99/C11 compliance, balanced answer keys (A/B/C/D),
# granular execution traces, visual stack/pointer memory snapshots, and deep pedagogical rationales.

def load_part4(add_q):
    # =========================================================================
    # CAT_CONTROL_FLOW (Q081 - Q090): Conditionals, Loops & Branching Hazards
    # =========================================================================

    # Q081: Accidental Semicolon After if-Statement -> Key A
    add_q(
        81, 'CAT_CONTROL_FLOW', 'Easy', 'Accidental Semicolon After if-Statement',
        'What is the output of the following program?',
        r"""#include <stdio.h>
int main() {
    int x = 3;
    if (x > 5);
        printf("GREATER\n");
    return 0;
}""",
        5, 'if (x > 5);', 'The accidental semicolon immediately terminates the if-statement with a null statement! The printf block is completely UNCONDITIONAL and always executes!',
        [
            ('A', 'GREATER', True, 'In C, a semicolon immediately following the if condition acts as a null statement (an empty body). The subsequent printf statement is not part of the if block; it executes unconditionally regardless of x.', ''),
            ('B', 'No output', False, 'Assumed printf was controlled by if (x > 5).', 'The semicolon terminates the if-statement; the printf statement is independent and executes unconditionally.'),
            ('C', 'Compilation error', False, 'Thought a semicolon directly after if (...) is illegal syntax.', 'A standalone semicolon is a valid null statement in C grammar (§6.8.3).'),
            ('D', 'Undefined Behavior', False, 'Thought misplaced semicolons cause undefined behavior.', 'The syntax and control flow are fully standard and well-defined.'),
        ],
        'The semicolon terminates the if condition with a null statement. The subsequent printf executes unconditionally, printing GREATER.',
        'ISO/IEC 9899:1999 §6.8.3 & §6.8.4.1',
        'Null Statements and Selection Control Flow:\n1. Grammatical Structure (§6.8.4.1):\n   selection-statement: if ( expression ) statement\n2. Null Statement (§6.8.3):\n   \'A null statement consists of just a semicolon, and performs no operations.\'\n3. Code Analysis:\n   - In if (x > 5);, the statement associated with the if is the null statement (;).\n   - If (x > 5) is false (3 > 5 is 0), the null statement is skipped.\n   - Execution proceeds to the next statement in the compound sequence, which is printf("GREATER\\n");.\n   - Visual indentation in C has zero syntactic effect (unlike Python).\n4. printf outputs \'GREATER\'.\n\nExam Trap: Accidental semicolons after if, for, and while loops are among the most notorious bugs in student exams and production code.',
        [
            (1, 4, 'int x = 3 allocated on stack.', {'x': 3}, {'stack': [{'name': 'x', 'addr': '0x1000', 'val': 3}]}),
            (2, 5, "Condition (x > 5) evaluates to 0 (false). Body of if is null statement ';' (skipped).", {'condition': 0}, {'stack': []}),
            (3, 6, "printf statement is independent of if: executes unconditionally. Prints 'GREATER'.", {'stdout': 'GREATER'}, {'stack': [{'name': 'stdout', 'val': 'GREATER'}]}),
        ]
    )

    # Q082: Accidental Semicolon After for-Loop Header -> Key B
    add_q(
        82, 'CAT_CONTROL_FLOW', 'Medium', 'Accidental Semicolon After for-Loop Header',
        'What is the output of the following program?',
        r"""#include <stdio.h>
int main() {
    int i;
    for (i = 0; i < 5; i++);
        printf("%d\n", i);
    return 0;
}""",
        5, 'for (i = 0; i < 5; i++);', 'The semicolon at the end of the for header makes the loop body a NULL STATEMENT! The loop iterates 5 times doing nothing, and printf runs once when i = 5!',
        [
            ('A', '0 1 2 3 4', False, 'Assumed the for loop controlled the indented printf statement.', 'The semicolon after for(...) terminates the loop body with a null statement; printf executes once after loop termination.'),
            ('B', '5', True, 'The for-loop body is the null statement (;). The loop iterates 5 times, incrementing i from 0 to 5. When i reaches 5, the condition i < 5 fails, the loop terminates, and printf prints 5.', ''),
            ('C', '4', False, 'Thought i stopped at the last successful iteration value (4).', 'The loop terminates when i < 5 becomes false; i++ increments i to 5 before the termination check fails.'),
            ('D', '0', False, 'Thought the loop did not execute.', 'The loop runs all 5 iterations completely before printf executes.'),
        ],
        'The semicolon makes the for loop body a null statement. The loop runs until i = 5, then exits and printf prints 5.',
        'ISO/IEC 9899:1999 §6.8.5.3 & §6.8.3',
        'Iteration Statements with Null Bodies:\n1. For-Loop Syntax (§6.8.5.3):\n   for ( clause-1 ; expression-2 ; expression-3 ) statement\n2. Execution Flow:\n   - Clause 1 initializes: i = 0.\n   - Condition expression-2: i < 5 is tested.\n   - The loop body statement is the single semicolon (null statement ;).\n   - Expression-3: i++ executes.\n3. Loop Cycle:\n   - i = 0 -> test true -> do nothing -> i++ -> 1\n   - i = 1 -> test true -> do nothing -> i++ -> 2\n   - i = 2 -> test true -> do nothing -> i++ -> 3\n   - i = 3 -> test true -> do nothing -> i++ -> 4\n   - i = 4 -> test true -> do nothing -> i++ -> 5\n   - i = 5 -> test false -> loop exits.\n4. When the loop exits, control passes to printf("%d\\n", i), printing 5.\n\nExam Trap: Never place a semicolon after a for(...) or while(...) header unless you deliberately intend a delay/spin loop.',
        [
            (1, 4, 'int i allocated on stack.', {'i': 'uninitialized'}, {'stack': [{'name': 'i', 'addr': '0x1000', 'val': '?'}]}),
            (2, 5, 'for loop executes null statement 5 times. i increments: 0 -> 1 -> 2 -> 3 -> 4 -> 5.', {'i': 5}, {'stack': [{'name': 'i', 'addr': '0x1000', 'val': 5}]}),
            (3, 5, 'Condition 5 < 5 is false. Loop terminates with i = 5.', {'i': 5, 'condition': 0}, {'stack': [{'name': 'i', 'val': 5}]}),
            (4, 6, 'printf prints i (5).', {'stdout': '5'}, {'stack': [{'name': 'stdout', 'val': '5'}]}),
        ]
    )

    # Q083: Assignment (=) in Conditional Statement -> Key C
    add_q(
        83, 'CAT_CONTROL_FLOW', 'Easy', 'Assignment (=) in Conditional Statement',
        'What is the output of the following program?',
        r"""#include <stdio.h>
int main() {
    int x = 0;
    if (x = 5) {
        printf("TRUE %d\n", x);
    } else {
        printf("FALSE %d\n", x);
    }
    return 0;
}""",
        5, 'if (x = 5)', '= is ASSIGNMENT, not equality (==)! The assignment places 5 into x, and the expression yields 5 (non-zero / true), so the if-branch executes!',
        [
            ('A', 'FALSE 0', False, 'Thought it tested if x == 5, which would be false since x was 0.', 'The condition uses assignment (=), not comparison (==). x is overwritten with 5.'),
            ('B', 'Compilation error', False, 'Thought assignment inside an if condition is illegal in C.', 'In C, assignment is an expression that yields a value; using assignment in a condition is fully valid syntax.'),
            ('C', 'TRUE 5', True, "In C, = is the assignment operator. x = 5 assigns 5 to x and evaluates to 5. Because 5 is non-zero (true), the if branch executes and prints 'TRUE 5'.", ''),
            ('D', 'TRUE 0', False, 'Thought the old value of x was evaluated before assignment.', 'The assignment expression yields the value stored in the left operand after the assignment (5).'),
        ],
        'x = 5 assigns 5 to x and yields 5 (true). The if branch executes, printing TRUE 5.',
        'ISO/IEC 9899:1999 §6.5.16 & §6.8.4.1',
        'Assignment Expressions in Controlling Contexts:\n1. Expression Value of Assignment (§6.5.16#3):\n   \'An assignment operator stores a value in the object designated by the left operand. An assignment expression has the value of the left operand after the assignment.\'\n2. Evaluation Sequence:\n   - Expression: (x = 5)\n   - Value 5 is stored into integer object x.\n   - The overall expression yields the integer value 5.\n3. Truth Evaluation in C (§6.8.4.1):\n   - In C, any non-zero numeric value evaluates to true.\n   - Since 5 != 0, the if condition evaluates to true.\n4. Branch Execution:\n   - Control enters the if-block.\n   - printf("TRUE %d\\n", x) reads x (which is now 5), printing \'TRUE 5\'.\n\nExam Trap: The classic typo of using = instead of ==. To prevent accidental assignment, some developers write constants on the left: if (5 == x).',
        [
            (1, 4, 'int x = 0 allocated on stack.', {'x': 0}, {'stack': [{'name': 'x', 'addr': '0x1000', 'val': 0}]}),
            (2, 5, 'Assignment x = 5 writes 5 into x. Expression evaluates to 5 (non-zero -> true).', {'x': 5, 'condition': 5}, {'stack': [{'name': 'x', 'addr': '0x1000', 'val': 5}]}),
            (3, 6, "Control enters if branch: printf prints 'TRUE 5'.", {'stdout': 'TRUE 5'}, {'stack': [{'name': 'stdout', 'val': 'TRUE 5'}]}),
        ]
    )

    # Q084: Assignment of Zero in If Condition -> Key D
    add_q(
        84, 'CAT_CONTROL_FLOW', 'Easy', 'Assignment of Zero in If Condition',
        'What is the output of the following program?',
        r"""#include <stdio.h>
int main() {
    int x = 10;
    if (x = 0) {
        printf("BRANCH A %d\n", x);
    } else {
        printf("BRANCH B %d\n", x);
    }
    return 0;
}""",
        5, 'if (x = 0)', 'Assignment x = 0 overwrites x with 0 and evaluates to 0 (FALSE)! The condition fails and execution branches to the else block!',
        [
            ('A', 'BRANCH A 10', False, 'Thought it checked if x was 10.', 'x was overwritten with 0 by the assignment operator.'),
            ('B', 'BRANCH B 10', False, 'Thought x remained 10 in the else branch.', 'The assignment mutated x to 0 before the condition was evaluated.'),
            ('C', 'Compile error', False, 'Thought assigning zero in an if condition is forbidden.', 'Syntactically valid C expression.'),
            ('D', 'BRANCH B 0', True, "The assignment x = 0 stores 0 into x and yields 0. In C, 0 evaluates to false, so control branches to the else block. printf prints 'BRANCH B 0'.", ''),
        ],
        'x = 0 sets x to 0 and evaluates to 0 (false). The else branch executes and prints BRANCH B 0.',
        'ISO/IEC 9899:1999 §6.5.16 & §6.8.4.1',
        'Assignment to Zero and Falsy Branching:\n1. Trace:\n   - Initial state: x = 10.\n   - Condition: (x = 0).\n   - Assignment operator stores 0 into variable x.\n   - The expression evaluates to the assigned value: 0.\n2. Boolean Evaluation:\n   - Under ISO C, 0 is false.\n   - The condition is false, bypassing the if-block.\n3. Else Execution:\n   - Control branches to the else block.\n   - printf("BRANCH B %d\\n", x) formats x, which now contains 0.\n4. Output: \'BRANCH B 0\'.\n\nExam Trap: Notice that x was permanently mutated to 0 by the assignment inside the if condition.',
        [
            (1, 4, 'int x = 10 allocated on stack.', {'x': 10}, {'stack': [{'name': 'x', 'addr': '0x1000', 'val': 10}]}),
            (2, 5, 'Assignment x = 0 writes 0 into x. Expression evaluates to 0 (false). Branches to else.', {'x': 0, 'condition': 0}, {'stack': [{'name': 'x', 'addr': '0x1000', 'val': 0}]}),
            (3, 8, "else branch executes: printf prints 'BRANCH B 0'.", {'stdout': 'BRANCH B 0'}, {'stack': [{'name': 'stdout', 'val': 'BRANCH B 0'}]}),
        ]
    )

    # Q085: Switch Case Fallthrough without break -> Key A
    add_q(
        85, 'CAT_CONTROL_FLOW', 'Easy', 'Switch Case Fallthrough without break',
        'What is the output of the following program?',
        r"""#include <stdio.h>
int main() {
    int x = 2;
    switch (x) {
        case 1: printf("ONE ");
        case 2: printf("TWO ");
        case 3: printf("THREE ");
        default: printf("DEFAULT\n");
    }
    return 0;
}""",
        8, 'case 2: printf("TWO ");', 'There are NO break statements! Once execution enters case 2, it FALLS THROUGH all subsequent cases, printing TWO THREE DEFAULT!',
        [
            ('A', 'TWO THREE DEFAULT', True, "x matches case 2, so execution jumps to case 2 and prints 'TWO '. Because there are no break statements, control falls through case 3 ('THREE ') and default ('DEFAULT'). Output is 'TWO THREE DEFAULT'.", ''),
            ('B', 'TWO', False, 'Assumed switch cases automatically break upon reaching the next case label (like modern languages).', 'In C, switch cases fall through by default unless an explicit break statement terminates execution.'),
            ('C', 'ONE TWO THREE DEFAULT', False, 'Thought switch executes all cases from the top.', 'Execution jumps directly to the matching case label (case 2), skipping case 1.'),
            ('D', 'DEFAULT', False, 'Thought default always overrides preceding cases.', 'default is only jumped to if no case matches, or reached via fallthrough.'),
        ],
        'In C, switch statements fall through by default. Matching case 2 without breaks executes case 2, case 3, and default sequentially.',
        'ISO/IEC 9899:1999 §6.8.4.2',
        'Switch Statement Fallthrough Semantics:\n1. Switch Control Flow (§6.8.4.2):\n   - A switch statement evaluates its controlling expression (x = 2).\n   - Execution jumps directly to the case label whose constant equals the value of the controlling expression.\n   - Case labels are merely jump targets (like goto labels); they do NOT delimit blocks.\n2. Execution Sequence:\n   - Jump directly to case 2:.\n   - printf("TWO ") executes.\n   - There is no break statement; control continues sequentially into case 3:.\n   - printf("THREE ") executes.\n   - There is no break; control falls through into default:.\n   - printf("DEFAULT\\n") executes.\n3. Output: \'TWO THREE DEFAULT\'.\n\nExam Trap: Intentional fallthrough is sometimes used in C, but unintentional missing break statements are a leading source of logic errors.',
        [
            (1, 4, 'int x = 2 allocated on stack.', {'x': 2}, {'stack': [{'name': 'x', 'addr': '0x1000', 'val': 2}]}),
            (2, 5, 'switch(x) evaluates x (2): execution jumps to label case 2:.', {'target': 'case 2'}, {'stack': []}),
            (3, 7, "case 2 executes: prints 'TWO '. Falls through to case 3.", {'stdout': 'TWO '}, {'stack': []}),
            (4, 8, "case 3 executes: prints 'THREE '. Falls through to default.", {'stdout': 'TWO THREE '}, {'stack': []}),
            (5, 9, "default executes: prints 'DEFAULT'. Outputs 'TWO THREE DEFAULT'.", {'stdout': 'TWO THREE DEFAULT'}, {'stack': [{'name': 'stdout', 'val': 'TWO THREE DEFAULT'}]}),
        ]
    )

    # Q086: Switch Default at Beginning with Fallthrough -> Key B
    add_q(
        86, 'CAT_CONTROL_FLOW', 'Medium', 'Switch Default at Beginning with Fallthrough',
        'What is the output when x = 5 (no matching case label)?',
        r"""#include <stdio.h>
int main() {
    int x = 5;
    switch (x) {
        default: printf("DEF ");
        case 1: printf("ONE ");
        case 2: printf("TWO\n");
    }
    return 0;
}""",
        6, 'default: printf("DEF ");', 'When no case matches, execution jumps to default: at the top and FALLS THROUGH case 1 and case 2 because there are no break statements!',
        [
            ('A', 'DEF', False, 'Assumed default breaks automatically or terminates the switch.', 'default is just a label; without break, it falls through to subsequent case labels.'),
            ('B', 'DEF ONE TWO', True, "x = 5 matches none of the case labels, so execution jumps to default at the top of the switch body. Because there are no break statements, execution falls through case 1 ('ONE ') and case 2 ('TWO'), printing 'DEF ONE TWO'.", ''),
            ('C', 'No output', False, 'Thought default must be located at the end of the switch.', 'The C standard permits the default label to appear anywhere inside the switch body.'),
            ('D', 'Compile error', False, 'Thought placing default at the beginning is a syntax error.', 'default label position inside switch is completely arbitrary.'),
        ],
        'default can appear anywhere in the switch. When x = 5 matches default at the top, it falls through case 1 and case 2, printing DEF ONE TWO.',
        'ISO/IEC 9899:1999 §6.8.4.2',
        'Arbitrary Placement of Default Labels:\n1. ISO C Specification (§6.8.4.2):\n   \'There may be at most one default label in each switch statement. The default label may appear anywhere in the switch statement.\'\n2. Trace:\n   - Controlling expression evaluates to x = 5.\n   - No case matches 5.\n   - Execution branches to default:.\n   - default: is located on line 6: printf("DEF ") prints \'DEF \'.\n   - There is no break; control falls through to case 1: on line 7.\n   - printf("ONE ") prints \'ONE \'.\n   - No break; control falls through to case 2: on line 8.\n   - printf("TWO\\n") prints \'TWO\'.\n3. Output: \'DEF ONE TWO\'.\n\nExam Trap: Never assume default must be the last label in a switch statement!',
        [
            (1, 4, 'int x = 5 allocated on stack.', {'x': 5}, {'stack': [{'name': 'x', 'addr': '0x1000', 'val': 5}]}),
            (2, 5, 'switch(x) matches no case: jumps to default: label at top of block.', {'target': 'default'}, {'stack': []}),
            (3, 6, "default executes: prints 'DEF '. Falls through to case 1.", {'stdout': 'DEF '}, {'stack': []}),
            (4, 7, "case 1 executes: prints 'ONE '. Falls through to case 2.", {'stdout': 'DEF ONE '}, {'stack': []}),
            (5, 8, "case 2 executes: prints 'TWO'. Outputs 'DEF ONE TWO'.", {'stdout': 'DEF ONE TWO'}, {'stack': [{'name': 'stdout', 'val': 'DEF ONE TWO'}]}),
        ]
    )

    # Q087: Dangling Else Association -> Key C
    add_q(
        87, 'CAT_CONTROL_FLOW', 'Tricky', 'Dangling Else Association',
        'What is the output of the following program?',
        r"""#include <stdio.h>
int main() {
    int a = 0;
    int b = 1;
    if (a == 1)
        if (b == 1)
            printf("BOTH\n");
    else
        printf("ELSE\n");
    return 0;
}""",
        9, 'else', 'In C, an else ALWAYS binds to the NEAREST preceding unmatched if, regardless of visual indentation! The else belongs to if (b == 1), which is bypassed because a == 0!',
        [
            ('A', 'ELSE', False, 'Fooled by visual indentation! Indentation has no syntactic meaning in C.', 'The else binds to the nearest if (b == 1), not the outer if (a == 1).'),
            ('B', 'BOTH', False, 'a is 0, so a == 1 is false.', 'Outer condition fails.'),
            ('C', 'No output', True, 'Under ISO C §6.8.4.1#3, an else associates with the closest preceding unmatched if. Here, the else belongs to if (b == 1). Because the outer if (a == 1) is false (0 == 1), the entire nested if-else construct is bypassed, producing no output.', ''),
            ('D', 'Compile error', False, 'Thought ambiguous indentation triggers a compiler error.', 'C grammar unambiguously resolves dangling elses via the nearest-if rule.'),
        ],
        'An else binds to the nearest preceding unmatched if. The else belongs to inner if (b == 1); since outer if (a == 1) is false, nothing is printed.',
        'ISO/IEC 9899:1999 §6.8.4.1#3',
        'The Dangling Else Grammar Rule:\n1. Grammatical Ambiguity Resolution (§6.8.4.1#3):\n   \'An else is associated with the lexically nearest preceding if that is allowed by the syntax.\'\n2. AST Parsing:\n   The code parses as:\n   if (a == 1) {\n       if (b == 1) {\n           printf("BOTH\\n");\n       } else {\n           printf("ELSE\\n");\n       }\n   }\n3. Execution:\n   - Condition (a == 1) evaluates to (0 == 1) which is false (0).\n   - The entire statement controlled by the outer if is skipped.\n   - Because the else belongs to the inner if, the else block is also skipped!\n4. No output is produced.\n\nExam Trap: Always use braces ({ }) around if bodies in C to avoid dangling-else ambiguity and maintain clear control flow.',
        [
            (1, 4, 'int a = 0, b = 1 allocated on stack.', {'a': 0, 'b': 1}, {'stack': [{'name': 'a', 'addr': '0x1000', 'val': 0}, {'name': 'b', 'addr': '0x1004', 'val': 1}]}),
            (2, 5, 'Outer condition (a == 1) evaluates to 0 (false).', {'condition': 0}, {'stack': []}),
            (3, 5, 'Entire nested body (including inner if-else) is bypassed. Program outputs nothing.', {'stdout': ''}, {'stack': []}),
        ]
    )

    # Q088: Postfix Decrement in Loop Test -> Key D
    add_q(
        88, 'CAT_CONTROL_FLOW', 'Medium', 'Postfix Decrement in Loop Test',
        'What is the output of the following program?',
        r"""#include <stdio.h>
int main() {
    int x = 3;
    while (x-- > 0) {
        printf("%d ", x);
    }
    printf("\n");
    return 0;
}""",
        5, 'while (x-- > 0)', 'Postfix x-- tests the OLD value > 0, then decrements immediately before entering the loop body! The body sees x = 2, 1, 0!',
        [
            ('A', '3 2 1', False, 'Thought x was decremented after the loop body executed.', "Postfix side effect completes at the condition's sequence point before the body runs."),
            ('B', '3 2 1 0', False, 'Counted 4 iterations starting from 3.', 'Test checks old x, but body prints already-decremented x (2, 1, 0).'),
            ('C', '2 1', False, 'Thought x = 0 terminated the loop before printing 0.', 'When old x is 1, 1 > 0 is true, x decrements to 0, and the body prints 0.'),
            ('D', '2 1 0', True, "Iteration 1: test 3 > 0 (true), x decrements to 2, body prints 2. Iteration 2: test 2 > 0 (true), x decrements to 1, body prints 1. Iteration 3: test 1 > 0 (true), x decrements to 0, body prints 0. Iteration 4: test 0 > 0 (false), x decrements to -1, loop exits. Output: '2 1 0 '.", ''),
        ],
        'x-- tests old value > 0 and decrements x before body entry. The body prints x = 2, 1, 0.',
        'ISO/IEC 9899:1999 §6.5.2.4 & §6.8.5.1',
        "Sequence Points in While Loop Controlling Expressions:\n1. Execution Cycle (§6.8.5.1):\n   - The controlling expression (x-- > 0) is evaluated.\n   - There is a sequence point after the evaluation of the controlling expression, BEFORE the loop body executes.\n   - Therefore, the side-effect of x-- (decrementing x by 1) is fully applied before the body is entered.\n2. Iteration Trace:\n   - Start: x = 3.\n   - Iter 1: Evaluate 3 > 0 (true). Side effect: x becomes 2. Body prints 2.\n   - Iter 2: Evaluate 2 > 0 (true). Side effect: x becomes 1. Body prints 1.\n   - Iter 3: Evaluate 1 > 0 (true). Side effect: x becomes 0. Body prints 0.\n   - Iter 4: Evaluate 0 > 0 (false). Side effect: x becomes -1. Loop terminates.\n3. Output: '2 1 0 '.\n\nExam Trap: Notice that x ends with value -1 after the loop terminates.",
        [
            (1, 4, 'int x = 3 allocated on stack.', {'x': 3}, {'stack': [{'name': 'x', 'addr': '0x1000', 'val': 3}]}),
            (2, 5, "Iter 1: (3 > 0) is true -> x decrements to 2. Body prints '2 '.", {'x': 2, 'stdout': '2 '}, {'stack': [{'name': 'x', 'val': 2}]}),
            (3, 5, "Iter 2: (2 > 0) is true -> x decrements to 1. Body prints '1 '.", {'x': 1, 'stdout': '2 1 '}, {'stack': [{'name': 'x', 'val': 1}]}),
            (4, 5, "Iter 3: (1 > 0) is true -> x decrements to 0. Body prints '0 '.", {'x': 0, 'stdout': '2 1 0 '}, {'stack': [{'name': 'x', 'val': 0}]}),
            (5, 5, 'Iter 4: (0 > 0) is false -> x decrements to -1. Loop terminates.', {'x': -1}, {'stack': [{'name': 'x', 'val': -1}]}),
        ]
    )

    # Q089: do-while(0) Execution Guarantee -> Key A
    add_q(
        89, 'CAT_CONTROL_FLOW', 'Easy', 'do-while(0) Execution Guarantee',
        'How many times does the body of a do-while(0) statement execute?',
        r"""#include <stdio.h>
int main() {
    int count = 0;
    do {
        count++;
    } while (0);
    printf("%d\n", count);
    return 0;
}""",
        5, 'do { ... } while (0);', 'A do-while loop evaluates its condition AFTER executing the loop body! It is GUARANTEED to execute AT LEAST ONCE!',
        [
            ('A', 'Exactly once', True, 'Under ISO C §6.8.5.2, the body of a do statement executes first, and the controlling expression while(0) is evaluated after each execution. Because 0 is false, the loop exits immediately after running exactly once.', ''),
            ('B', 'Zero times', False, 'Confused do-while with while(0).', 'while(0) evaluates the condition first and executes 0 times; do-while evaluates after the body.'),
            ('C', 'Infinite times', False, '0 is false, not true.', 'The loop terminates immediately after checking while(0).'),
            ('D', 'Compile error', False, 'Thought while(0) is invalid syntax.', 'do { ... } while(0) is a standard, ubiquitous C idiom for multi-statement macros.'),
        ],
        'do-while evaluates condition after body execution. Condition 0 is false, exiting after exactly 1 execution.',
        'ISO/IEC 9899:1999 §6.8.5.2',
        "The do-while Loop Guarantee:\n1. Standard Specification (§6.8.5.2):\n   'The controlling expression of a do statement is evaluated after each execution of the loop body.'\n2. Trace:\n   - count starts at 0.\n   - Body executes: count++ updates count to 1.\n   - Controlling expression while(0) is evaluated: 0 is false.\n   - Loop terminates immediately.\n3. printf prints 1.\n\nExam Trap: This construct is the universal C idiom for defining multi-statement preprocessor macros (e.g. #define FOO() do { a(); b(); } while(0)), because it allows the macro to act syntactically like a single statement that safely accepts a trailing semicolon and pairs correctly with if-else statements.",
        [
            (1, 4, 'int count = 0 allocated on stack.', {'count': 0}, {'stack': [{'name': 'count', 'addr': '0x1000', 'val': 0}]}),
            (2, 6, 'Loop body executes unconditionally: count++ -> 1.', {'count': 1}, {'stack': [{'name': 'count', 'val': 1}]}),
            (3, 7, 'Condition while(0) evaluated: false (0). Loop exits immediately.', {'condition': 0}, {'stack': []}),
            (4, 8, 'printf prints count (1).', {'stdout': '1'}, {'stack': [{'name': 'stdout', 'val': '1'}]}),
        ]
    )

    # Q090: Unsigned Integer Non-Terminating Loop -> Key B
    add_q(
        90, 'CAT_CONTROL_FLOW', 'Tricky', 'Unsigned Integer Non-Terminating Loop',
        'What happens when executing the following loop?',
        r"""#include <stdio.h>
int main() {
    unsigned int i;
    for (i = 3; i >= 0; i--) {
        printf("%u ", i);
    }
    return 0;
}""",
        4, 'i >= 0', 'Because i is an UNSIGNED int, i >= 0 is PERMANENTLY TRUE! When i is 0, 0 - 1 wraps around to UINT_MAX (4,294,967,295), creating an INFINITE LOOP!',
        [
            ('A', 'It terminates naturally after printing 3 2 1 0', False, 'Thought i reached -1 and stopped.', 'unsigned int cannot represent negative numbers; 0 - 1 wraps to positive UINT_MAX (4,294,967,295), which is still >= 0.'),
            ('B', 'It is an infinite loop because unsigned int is always >= 0 (0 - 1 wraps to UINT_MAX)', True, 'Under ISO C §6.2.5#9, unsigned arithmetic never underflows; 0-- wraps to UINT_MAX (4294967295). Because an unsigned integer is always >= 0, the loop condition i >= 0 is permanently true, creating an infinite loop.', ''),
            ('C', 'It causes a compilation error: unsigned comparison >= 0 invalid', False, 'Thought compilers reject i >= 0 on unsigned variables.', 'Compilers issue a warning (-Wtype-limits), but compile the code cleanly.'),
            ('D', 'It terminates with a segmentation fault after printing 3', False, 'Looping integer printing does not violate memory bounds.', 'It continues printing indefinitely until interrupted.'),
        ],
        'Unsigned integers are always >= 0. When i = 0, i-- wraps to UINT_MAX (4294967295), making i >= 0 permanently true in an infinite loop.',
        'ISO/IEC 9899:1999 §6.2.5#9 & §6.8.5.3',
        "Unsigned Loop Termination Trap:\n1. Unsigned Modular Arithmetic (§6.2.5#9):\n   - An unsigned integer of N bits represents values in the closed range [0, 2^N - 1].\n   - By definition, an unsigned integer can NEVER be negative.\n   - The relational expression i >= 0 is a tautology: it evaluates to 1 (true) for every possible value of i.\n2. Iteration Trace:\n   - i = 3: prints '3 ' -> i-- becomes 2\n   - i = 2: prints '2 ' -> i-- becomes 1\n   - i = 1: prints '1 ' -> i-- becomes 0\n   - i = 0: prints '0 ' -> i-- wraps around to 4,294,967,295 (UINT_MAX)!\n   - i = 4294967295: condition 4294967295 >= 0 is TRUE! Prints 4294967295...\n   - The loop never terminates.\n\nExam Trap: This is a classic bug when programmers change signed int loop counters to unsigned int or size_t to silence compiler warnings.",
        [
            (1, 4, 'unsigned int i declared on stack.', {'i': 'uninitialized'}, {'stack': [{'name': 'i', 'addr': '0x1000', 'val': '?'}]}),
            (2, 5, 'Loop iterations: prints 3, 2, 1, 0.', {'i': 0, 'stdout': '3 2 1 0 '}, {'stack': [{'name': 'i', 'val': 0}]}),
            (3, 5, 'When i is 0, i-- wraps around to UINT_MAX (4294967295). Condition 4294967295 >= 0 is true. Loop runs infinitely.', {'i': 4294967295, 'infinite_loop': True}, {'stack': [{'name': 'i', 'val': 4294967295}]}),
        ]
    )

    # =========================================================================
    # CAT_MACRO_PREPROC (Q091 - Q100): Preprocessor Directives, Macros & Guards
    # =========================================================================

    # Q091: Unparenthesized Macro Parameter Substitution -> Key C
    add_q(
        91, 'CAT_MACRO_PREPROC', 'Easy', 'Unparenthesized Macro Parameter Substitution',
        'What is the output of the following program?',
        r"""#include <stdio.h>
#define SQUARE(x) x * x
int main() {
    int res = SQUARE(2 + 3);
    printf("%d\n", res);
    return 0;
}""",
        5, 'SQUARE(2 + 3)', 'Macros perform TEXTUAL SUBSTITUTION without parentheses! SQUARE(2 + 3) expands to 2 + 3 * 2 + 3 = 2 + 6 + 3 = 11, NOT 25!',
        [
            ('A', '25', False, 'Assumed SQUARE evaluated 2 + 3 = 5 first like a function, then squared 5 (5 * 5 = 25).', 'Macros are not functions; they perform raw lexical textual substitution before compiler parsing.'),
            ('B', '10', False, 'Thought it multiplied (2 + 3) * 2.', 'Arithmetic precedence dictates multiplication binds before addition.'),
            ('C', '11', True, 'SQUARE(2 + 3) expands textually to 2 + 3 * 2 + 3. By operator precedence, multiplication 3 * 2 evaluates first to 6, giving 2 + 6 + 3 = 11. printf outputs 11.', ''),
            ('D', 'Compile error', False, 'Thought macro parameter expressions require parentheses to compile.', 'The syntax is fully valid; the bug is purely logical.'),
        ],
        'Macros perform raw textual substitution. SQUARE(2 + 3) expands to 2 + 3 * 2 + 3 = 11 due to multiplication precedence.',
        'ISO/IEC 9899:1999 §6.10.3',
        "Textual Substitution Hazards in Function-like Macros:\n1. Preprocessing Semantics (§6.10.3):\n   - Preprocessor macros operate during Translation Phase 4, before any syntax analysis or type checking.\n   - Replacement tokens are substituted directly into the code stream.\n2. Expansion Trace:\n   - Macro definition: #define SQUARE(x) x * x\n   - Invocation: SQUARE(2 + 3)\n   - Argument token sequence: 2 + 3\n   - Replacement: 2 + 3 * 2 + 3\n3. Precedence in Compiler Parsing:\n   - Multiplication (*) has precedence level 3; addition (+) has precedence level 4.\n   - Parsed AST: 2 + (3 * 2) + 3\n   - Evaluation: 2 + 6 + 3 = 11.\n4. Output: '11'.\n\nExam Trap: Always enclose every macro parameter in parentheses: #define SQUARE(x) ((x) * (x)).",
        [
            (1, 2, 'Preprocessor expands SQUARE(2 + 3) -> 2 + 3 * 2 + 3.', {'macro_expansion': '2 + 3 * 2 + 3'}, {'preprocessor': [{'macro': 'SQUARE(2 + 3)', 'expansion': '2 + 3 * 2 + 3'}]}),
            (2, 5, 'Operator precedence binds 3 * 2 = 6 first. Addition: 2 + 6 + 3 = 11.', {'res': 11}, {'stack': [{'name': 'res', 'addr': '0x1000', 'val': 11}]}),
            (3, 6, 'printf prints res (11).', {'stdout': '11'}, {'stack': [{'name': 'stdout', 'val': '11'}]}),
        ]
    )

    # Q092: Unparenthesized Macro Expression Body -> Key D
    add_q(
        92, 'CAT_MACRO_PREPROC', 'Easy', 'Unparenthesized Macro Expression Body',
        'What is the output of the following program?',
        r"""#include <stdio.h>
#define ADD(a, b) a + b
int main() {
    int res = ADD(2, 3) * 4;
    printf("%d\n", res);
    return 0;
}""",
        5, 'ADD(2, 3) * 4', 'The macro body is unparenthesized! ADD(2, 3) * 4 expands textually to 2 + 3 * 4 = 2 + 12 = 14, NOT 20!',
        [
            ('A', '20', False, 'Assumed ADD(2, 3) evaluated to 5 first, then multiplied by 4 (5 * 4 = 20).', 'Macros do not isolate expression precedence unless the entire macro body is enclosed in parentheses: ((a) + (b)).'),
            ('B', '24', False, 'Thought it multiplied (2 * 4) + (3 * 4).', 'Multiplication binds only to the adjacent token 3.'),
            ('C', 'Compile error', False, 'Thought macros cannot be multiplied directly.', 'Syntactically valid C expression.'),
            ('D', '14', True, 'ADD(2, 3) * 4 expands textually to 2 + 3 * 4. Multiplication has higher precedence than addition, evaluating 3 * 4 = 12 first, giving 2 + 12 = 14. printf prints 14.', ''),
        ],
        'Without surrounding parentheses in the macro body, ADD(2, 3) * 4 expands to 2 + 3 * 4 = 14.',
        'ISO/IEC 9899:1999 §6.10.3',
        "Macro Body Parenthesization Rule:\n1. Expansion:\n   - Macro: #define ADD(a, b) a + b\n   - Code: ADD(2, 3) * 4\n   - Textual expansion: 2 + 3 * 4\n2. Parsing & Evaluation:\n   - Operator precedence groups: 2 + (3 * 4)\n   - 2 + 12 = 14.\n3. Safe Macro Construction Rule:\n   - Rule 1: Parenthesize every parameter: ((a) + (b))\n   - Rule 2: Parenthesize the ENTIRE macro replacement list: (((a) + (b)))\n   - This prevents outer operators from binding to internal macro terms.\n4. printf outputs '14'.",
        [
            (1, 2, 'Preprocessor expands ADD(2, 3) * 4 -> 2 + 3 * 4.', {'expansion': '2 + 3 * 4'}, {'preprocessor': [{'macro': 'ADD(2, 3) * 4', 'expansion': '2 + 3 * 4'}]}),
            (2, 5, 'Multiplication 3 * 4 = 12 evaluates first. 2 + 12 = 14. Stored in res.', {'res': 14}, {'stack': [{'name': 'res', 'addr': '0x1000', 'val': 14}]}),
            (3, 6, 'printf prints 14.', {'stdout': '14'}, {'stack': [{'name': 'stdout', 'val': '14'}]}),
        ]
    )

    # Q093: Side Effect Duplication in Macro Arguments -> Key A
    add_q(
        93, 'CAT_MACRO_PREPROC', 'Tricky', 'Side Effect Duplication in Macro Arguments',
        'What is the status of the following program?',
        r"""#include <stdio.h>
#define DOUBLE(x) ((x) + (x))
int main() {
    int a = 5;
    int res = DOUBLE(a++);
    printf("%d %d\n", res, a);
    return 0;
}""",
        6, 'DOUBLE(a++)', 'DOUBLE(a++) expands to ((a++) + (a++))! Modifying a twice in the same expression without a sequence point is UNDEFINED BEHAVIOR!',
        [
            ('A', 'Undefined Behavior (Modifying a twice without sequence point)', True, 'DOUBLE(a++) expands textually to ((a++) + (a++)). Modifying scalar variable a twice between sequence points violates ISO C §6.5#2, invoking Undefined Behavior.', ''),
            ('B', '7 10', False, 'Thought each increment occurred sequentially with defined intermediate values.', 'Binary addition (+) does not introduce a sequence point between operands.'),
            ('C', '6 10', False, 'Assumed only one increment took effect.', 'The token a++ is duplicated in the macro body, leading to double modification.'),
            ('D', '7 12', False, 'Random calculation guess.', 'Standard explicitly declares unsequenced modifications Undefined Behavior.'),
        ],
        'DOUBLE(a++) expands to ((a++) + (a++)). Modifying a twice without a sequence point is Undefined Behavior under ISO C §6.5#2.',
        'ISO/IEC 9899:1999 §6.10.3 & §6.5#2',
        "Argument Duplication and Unsequenced Side Effects:\n1. Expansion Mechanism:\n   - Parameter x appears twice in replacement list: ((x) + (x))\n   - Invocation: DOUBLE(a++)\n   - Textual expansion: ((a++) + (a++))\n2. Sequence Point Analysis:\n   - The binary + operator does NOT introduce a sequence point between its left and right operands.\n   - Both operands modify variable a via postfix increment (a++).\n   - Under ISO C §6.5#2: 'Between the previous and next sequence point an object shall have its stored value modified at most once...'\n   - Because a is modified twice without an intervening sequence point, the behavior is strictly Undefined Behavior.\n3. Real-world Divergence:\n   - Compilers produce unpredictable outputs (10, 11, 12, or corrupted registers).\n\nExam Trap: Never pass arguments with side effects (like i++, ++j, or getchar()) to function-like macros!",
        [
            (1, 5, 'int a = 5 allocated on stack.', {'a': 5}, {'stack': [{'name': 'a', 'addr': '0x1000', 'val': 5}]}),
            (2, 2, "Preprocessor expands DOUBLE(a++) -> ((a++) + (a++)). Argument token 'a++' duplicated in replacement.", {'expansion': '((a++) + (a++))'}, {'preprocessor': [{'macro': 'DOUBLE(a++)', 'expansion': '((a++) + (a++))'}]}),
            (3, 6, 'Binary + operator evaluates operands: both attempt unsequenced write modifications on scalar object a.', {'side_effects': ['a++', 'a++']}, {'stack': []}),
            (4, 6, 'Two modifications of scalar a without intervening sequence point -> UNDEFINED BEHAVIOR under ISO C §6.5#2.', {'status': 'UNDEFINED BEHAVIOR'}, {'stack': []}),
        ]
    )

    # Q094: Ternary Macro Double Evaluation -> Key B
    add_q(
        94, 'CAT_MACRO_PREPROC', 'Tricky', 'Ternary Macro Double Evaluation',
        'What is the output of the following program?',
        r"""#include <stdio.h>
#define MAX(a, b) ((a) > (b) ? (a) : (b))
int main() {
    int x = 5, y = 6;
    int res = MAX(x++, y);
    printf("%d %d\n", res, x);
    return 0;
}""",
        6, 'MAX(x++, y)', 'MAX(x++, y) expands to ((x++) > (y) ? (x++) : (y)). Because 5 > 6 is false, the true branch (second x++) is SKIPPED by ternary short-circuit!',
        [
            ('A', '6 7', False, 'Thought x was incremented twice regardless of condition.', 'Ternary operator ?: has sequence points after the condition and evaluates only the chosen branch.'),
            ('B', '6 6', True, "MAX(x++, y) expands to ((x++) > (y) ? (x++) : (y)). Condition tests 5 > 6 (false), incrementing x to 6 at the sequence point. Because the condition is false, the second branch (y) is selected, giving res = 6. Both res and x are 6, printing '6 6'.", ''),
            ('C', '5 6', False, 'Thought postfix increment did not affect res.', 'res receives y (6), not x.'),
            ('D', '7 6', False, 'Confused x and res output order.', 'res receives y (6), while x was incremented once to 6.'),
        ],
        'Ternary operator short-circuits. Condition 5 > 6 is false (x becomes 6). The false branch (y) is evaluated, returning 6. Prints 6 6.',
        'ISO/IEC 9899:1999 §6.5.15 & §6.10.3',
        "Ternary Conditional Sequence Points and Macro Hazards:\n1. Expansion:\n   - MAX(x++, y) expands to:\n     ((x++) > (y) ? (x++) : (y))\n2. Conditional Operator Sequence Points (§6.5.15#4):\n   - 'The first expression is evaluated; there is a sequence point after its evaluation. Then the second or third expression is evaluated (whichever is appropriate).'\n3. Trace:\n   - Condition: (x++) > (y) ==> 5 > 6. Evaluates to 0 (false).\n   - Sequence point: Postfix increment side-effect completes; x increments from 5 to 6.\n   - Because the condition is false, the false branch (y) is selected. The second (x++) expression is NEVER evaluated!\n   - False branch yields y = 6.\n   - res is assigned 6.\n4. When printf runs, res = 6 and x = 6.\n5. Output: '6 6'.\n\nExam Trap: If x had been 7 and y 6, condition 7 > 6 would be true, and the true branch (x++) would execute, incrementing x a SECOND time to 9!",
        [
            (1, 2, 'Expansion: ((x++) > (y) ? (x++) : (y)).', {'expansion': '((x++) > (y) ? (x++) : (y))'}, {'preprocessor': [{'macro': 'MAX(x++, y)', 'expansion': '((x++) > (y) ? (x++) : (y))'}]}),
            (2, 6, 'Condition (x++ > y): tests 5 > 6 (false). Sequence point increments x to 6.', {'x': 6, 'condition': 0}, {'stack': [{'name': 'x', 'val': 6}, {'name': 'y', 'val': 6}]}),
            (3, 6, 'False branch evaluated: yields y (6). Stored in res.', {'res': 6}, {'stack': [{'name': 'res', 'val': 6}]}),
            (4, 7, "printf prints res (6) and x (6): outputs '6 6'.", {'stdout': '6 6'}, {'stack': [{'name': 'stdout', 'val': '6 6'}]}),
        ]
    )

    # Q095: Dangling Else in Multi-Statement Macro -> Key C
    add_q(
        95, 'CAT_MACRO_PREPROC', 'Tricky', 'Dangling Else in Multi-Statement Macro',
        'What happens when attempting to compile the following program?',
        r"""#include <stdio.h>
#define SWAP(a, b) int t = a; a = b; b = t;
int main() {
    int x = 1, y = 2;
    if (x < y)
        SWAP(x, y);
    else
        printf("NO SWAP\n");
    return 0;
}""",
        6, 'SWAP(x, y);', 'SWAP contains multiple statements! Semicolon after SWAP separates the statements, leaving the else without an if, causing a COMPILATION ERROR!',
        [
            ('A', 'Variables are swapped properly and program prints nothing', False, 'Thought macro acted like a single compound statement block.', 'Without braces or do-while(0), macro expands to 3 separate statements; the first statement satisfies the if, and the second statement breaks the if-else pairing.'),
            ('B', 'Runtime crash', False, 'Thought variable re-declaration causes runtime failure.', 'Compiler rejects the code at compile-time.'),
            ('C', "Compilation Error: 'else' without a previous 'if'", True, "SWAP expands to: if (x < y) int t = x; x = y; y = t;; else ... The second statement (x = y;) terminates the if-construct. The subsequent 'else' has no matching 'if', causing GCC to emit 'error: else without a previous if'.", ''),
            ('D', 'Undefined Behavior', False, 'Thought preprocessor syntax errors are undefined behavior.', 'Grammar constraint violation detected at compile time.'),
        ],
        'Multi-statement macros without do-while(0) break if-else syntax. The second statement terminates the if, causing a Compilation Error on else.',
        'ISO/IEC 9899:1999 §6.8.4.1 & §6.10.3',
        'The Multi-Statement Macro Trap and the do-while(0) Solution:\n1. Macro Expansion Trace:\n   The preprocessor expands lines 6-9 to:\n   if (x < y)\n       int t = x; a = b; b = t;;\n   else\n       printf("NO SWAP\\n");\n2. Parsing Disaster:\n   - Statement 1: if (x < y) int t = x; (if body is a single statement: int t = x;)\n   - Statement 2: x = y; (standalone independent statement)\n   - Statement 3: y = t; (standalone independent statement)\n   - Statement 4: else ... (ERROR! An else cannot appear without a preceding if!)\n3. Compiler Diagnostic:\n   GCC halts immediately: error: \'else\' without a previous \'if\'\n4. Standard Idiom Resolution:\n   Wrap multi-statement macros in do { ... } while(0):\n   #define SWAP(a, b) do { int t = a; a = b; b = t; } while(0)\n   This forces the macro to behave as a single syntactic statement that cleanly accepts a trailing semicolon before else.\n\nExam Trap: This is the definitive motivation for the do-while(0) macro idiom taught in every systems programming course.',
        [
            (1, 2, 'Preprocessor expands SWAP into 3 semicolon-separated statements.', {'expansion': 'int t = a; a = b; b = t;'}, {'preprocessor': [{'macro': 'SWAP', 'expansion': 'int t = a; a = b; b = t;'}]}),
            (2, 6, "if body receives only 'int t = a;'. Next statement 'a = b;' disconnects the if.", {'grammar': 'if block closed'}, {'stack': []}),
            (3, 8, "Compiler encounters 'else' with no preceding active 'if' -> COMPILATION ERROR: 'else' without a previous 'if'.", {'compiler_error': 'else without a previous if'}, {'stack': []}),
        ]
    )

    # Q096: Stringification Operator (#) Behavior -> Key D
    add_q(
        96, 'CAT_MACRO_PREPROC', 'Easy', 'Stringification Operator (#) Behavior',
        'What is the output of the following program?',
        r"""#include <stdio.h>
#define PRINT_NAME(x) printf("%s = %d\n", #x, x)
int main() {
    int total_score = 99;
    PRINT_NAME(total_score);
    return 0;
}""",
        6, 'PRINT_NAME(total_score);', 'The # operator in a macro replacement list STRINGIFIES the actual argument tokens into a string literal: #x becomes "total_score"!',
        [
            ('A', 'x = 99', False, "Thought #x printed the parameter letter 'x'.", '# operates on the actual argument passed (total_score), producing "total_score".'),
            ('B', '99 = 99', False, 'Thought #x printed the value of total_score as a string ("99").', '# stringifies the identifier token itself, not its runtime value.'),
            ('C', 'Compile error', False, 'Thought # is only valid as preprocessor directive prefix.', 'Inside macro replacement lists, # is the official stringification operator.'),
            ('D', 'total_score = 99', True, 'Under ISO C §6.10.3.2, the unary # operator converts the argument tokens into a string literal. #x becomes "total_score". printf receives ("%s = %d\\n", "total_score", total_score), printing \'total_score = 99\'.', ''),
        ],
        'The # operator stringifies the passed argument token into a string literal. #x becomes "total_score", printing total_score = 99.',
        'ISO/IEC 9899:1999 §6.10.3.2',
        'The Preprocessor Stringification Operator (#):\n1. ISO C Specification (§6.10.3.2#2):\n   \'Each occurrence of # followed by a parameter in the replacement list begins a stringizing operator. It causes the parameter\'s corresponding argument in the invocation to be converted to a character string literal.\'\n2. Trace:\n   - Macro: #define PRINT_NAME(x) printf("%s = %d\\n", #x, x)\n   - Invocation: PRINT_NAME(total_score)\n   - Parameter x is bound to token total_score.\n   - #x transforms into string literal "total_score".\n   - Second x evaluates as ordinary variable token total_score.\n   - Expansion: printf("%s = %d\\n", "total_score", total_score);\n3. Execution:\n   - printf prints string "total_score", followed by " = ", followed by integer 99.\n4. Output: \'total_score = 99\'.\n\nExam Trap: Distinguish # (stringification) from ## (token pasting).',
        [
            (1, 2, 'Unary # operator binds to parameter x. Argument \'total_score\' stringified to \'"total_score"\'.', {'#x': '"total_score"'}, {'preprocessor': [{'macro': '#x', 'expansion': '"total_score"'}]}),
            (2, 6, 'Expanded statement: printf("%s = %d\\n", "total_score", total_score);', {'string_arg': 'total_score', 'int_arg': 99}, {'stack': [{'name': 'total_score', 'val': 99}]}),
            (3, 6, "printf formats output: 'total_score = 99'.", {'stdout': 'total_score = 99'}, {'stack': [{'name': 'stdout', 'val': 'total_score = 99'}]}),
        ]
    )

    # Q097: Token Pasting Operator (##) Concatenation -> Key A
    add_q(
        97, 'CAT_MACRO_PREPROC', 'Medium', 'Token Pasting Operator (##) Concatenation',
        'What is the output of the following program?',
        r"""#include <stdio.h>
#define CONCAT(a, b) a ## b
int main() {
    int xy = 42;
    printf("%d\n", CONCAT(x, y));
    return 0;
}""",
        5, 'CONCAT(x, y)', 'The ## operator PASTES (merges) tokens a and b together into a single token: x ## y merges to token xy, evaluating to 42!',
        [
            ('A', '42', True, 'Under ISO C §6.10.3.3, the ## operator concatenates two tokens into a single preprocessing token. x ## y merges to form the single identifier xy, which evaluates to 42. printf prints 42.', ''),
            ('B', 'x y', False, 'Thought it printed the tokens with a space.', 'Token pasting joins tokens together into a single identifier without spaces.'),
            ('C', 'Compile error: undefined identifier CONCAT', False, 'Thought CONCAT was not recognized.', 'CONCAT is properly defined as a macro.'),
            ('D', '0', False, 'Random guess.', 'Evaluates the value stored in variable xy (42).'),
        ],
        'The ## operator merges two tokens into a single identifier. CONCAT(x, y) becomes xy, accessing variable xy (42).',
        'ISO/IEC 9899:1999 §6.10.3.3',
        'Token Pasting (Token Concatenation) Operator (##):\n1. ISO C Specification (§6.10.3.3#2):\n   \'If, in the replacement list of a function-like macro, a parameter is immediately preceded or followed by a ## preprocessing token, the parameter is replaced by the corresponding argument\'s preprocessing tokens... and the ## operator is deleted and the preceding preprocessing token is concatenated with the following preprocessing token.\'\n2. Trace:\n   - Macro: #define CONCAT(a, b) a ## b\n   - Invocation: CONCAT(x, y)\n   - Token a is x; token b is y.\n   - Operator ## merges token \'x\' and token \'y\' into single identifier token \'xy\'.\n   - Expansion: printf("%d\\n", xy);\n3. Runtime Execution:\n   - Compiler looks up identifier xy in the local scope.\n   - xy is an int variable with value 42.\n4. Output: \'42\'.\n\nExam Trap: The concatenated result must form a valid C token! Concatenating tokens that form invalid syntax (e.g. 1 ## a) produces a preprocessing compilation error.',
        [
            (1, 2, "Preprocessor token pasting: token 'x' and token 'y' concatenated across ## into token 'xy'.", {'concatenated_token': 'xy'}, {'preprocessor': [{'macro': 'CONCAT(x, y)', 'expansion': 'xy'}]}),
            (2, 5, 'Expanded code: printf("%d\\n", xy); reads variable xy from stack (42).', {'xy': 42}, {'stack': [{'name': 'xy', 'addr': '0x1000', 'val': 42}]}),
            (3, 5, 'printf prints 42.', {'stdout': '42'}, {'stack': [{'name': 'stdout', 'val': '42'}]}),
        ]
    )

    # Q098: Purpose of Header Guards (#ifndef / #define) -> Key B
    add_q(
        98, 'CAT_MACRO_PREPROC', 'Easy', 'Purpose of Header Guards (#ifndef / #define)',
        'What is the primary purpose of header guards (#ifndef / #define / #endif) in C header files?',
        r"""#ifndef MY_HEADER_H
#define MY_HEADER_H
struct Point { int x, y; };
#endif""",
        1, '#ifndef MY_HEADER_H', 'Header guards prevent REDEFINITION ERRORS when the same header file is included multiple times within a single translation unit!',
        [
            ('A', 'To make the header private and prevent other source files from including it', False, 'Header guards do not protect file access permissions.', 'Header guards are compile-time inclusion idempotency guards.'),
            ('B', 'To prevent multiple inclusion of the same header causing duplicate type definitions', True, "In C, defining a struct or typedef twice in the same translation unit causes a fatal compilation error ('redefinition of struct'). Header guards ensure that after the first inclusion, subsequent #include directives for that file expand to empty text.", ''),
            ('C', 'To speed up internet download of headers', False, 'Headers are local disk files.', 'Preprocessor operates entirely locally on source files.'),
            ('D', 'To automatically export functions as global symbols', False, 'Header guards have no effect on symbol linkage.', 'Linkage is governed by storage-class specifiers.'),
        ],
        'Header guards ensure a header file is included at most once per translation unit, preventing duplicate struct/type redefinition errors.',
        'ISO/IEC 9899:1999 §6.10 & §6.7.2.1',
        "Header Guards and the One-Definition Rule in C:\n1. The Problem:\n   - If header A.h defines struct Point { int x, y; };\n   - If header B.h includes A.h, and file main.c includes both A.h and B.h:\n   - main.c receives two copies of struct Point { int x, y; };.\n   - Under ISO C §6.7.2.1, re-declaring the same struct tag with a new member body in the same scope is a fatal constraint violation: error: redefinition of 'struct Point'.\n2. The Guard Pattern:\n   - #ifndef MY_HEADER_H checks if macro is defined.\n   - On first include: not defined -> executes #define MY_HEADER_H and defines struct Point.\n   - On second include: MY_HEADER_H is already defined -> the entire block up to #endif is discarded by the preprocessor.\n3. Result: Clean, idempotent header inclusion.\n\nExam Trap: Contrast header guards with the non-standard (but widely supported) #pragma once directive.",
        [
            (1, 1, 'First include: MY_HEADER_H is not defined. Preprocessor proceeds past #ifndef.', {'guard_status': 'FIRST_INCLUDE'}, {'preprocessor': [{'macro': 'MY_HEADER_H', 'status': 'DEFINED'}]}),
            (2, 2, '#define MY_HEADER_H defines macro symbol. Struct Point is parsed.', {'struct_Point': 'defined'}, {'type_table': [{'name': 'struct Point'}]}),
            (3, 4, 'Subsequent include: MY_HEADER_H is defined -> preprocessor skips all text up to #endif. Redefinition prevented.', {'action': 'SKIPPED'}, {'stack': []}),
        ]
    )

    # Q099: Difference between #include <file> and #include "file" -> Key C
    add_q(
        99, 'CAT_MACRO_PREPROC', 'Medium', 'Difference between #include <file> and #include "file"',
        'What is the difference between #include <header.h> and #include "header.h" in C?',
        r"""#include <stdio.h>
#include "my_header.h"
int main() {
    return 0;
}""",
        2, '#include "my_header.h"', '"header.h" searches the LOCAL/CURRENT source directory first before system paths; <header.h> searches SYSTEM include paths directly!',
        [
            ('A', '<file> is for standard C library files only; "file" is strictly for third-party libraries', False, 'You can put any header in quotes or angle brackets; the difference is purely the directory search order.', 'Quotes allow including standard libraries as well.'),
            ('B', '<file> compiles faster than "file"', False, 'Search order differences do not affect compilation speed measurably.', 'Both copy the header text verbatim.'),
            ('C', '"file" searches the local/current directory first before system include directories; <file> searches system include paths directly', True, 'Under ISO C §6.10.2, quoted form #include "file" first searches an implementation-dependent directory (typically the directory containing the source file); if not found, it falls back to the system include search paths used by #include <file>.', ''),
            ('D', '"file" copies file content; <file> creates a symbolic link', False, 'Both directives perform identical textual inclusion of the target file.', 'Both copy content verbatim into the translation unit.'),
        ],
        '"header.h" searches the current source directory first before system paths; <header.h> searches system include paths directly.',
        'ISO/IEC 9899:1999 §6.10.2',
        'Source File Inclusion Search Paths in ISO C:\n1. Bracketed Include (§6.10.2#2):\n   \'A preprocessing directive of the form #include <h-char-sequence> searches a sequence of implementation-defined places for a header identified between the < and > delimiters.\'\n   - Searches system compiler directories (e.g. /usr/include, MinGW/include).\n2. Quoted Include (§6.10.2#3):\n   \'A preprocessing directive of the form #include "q-char-sequence" causes the replacement of that directive by the entire contents of the source file identified... The search for the file shall be supported in an implementation-dependent manner... if this search is not supported, or if the search fails, the directive is reprocessed as if it read #include <h-char-sequence>\'\n   - Step 1: Searches the local directory containing the source file.\n   - Step 2: If not found, falls back to the system include search path.\n\nExam Trap: Use "my_header.h" for project-specific headers, and <stdio.h> for standard C runtime headers.',
        [
            (1, 1, '#include <stdio.h>: preprocessor searches system include directories (e.g. /usr/include). Found and included.', {'stdio': 'system_path'}, {'include_paths': [{'type': 'system', 'path': '<stdio.h>'}]}),
            (2, 2, '#include "my_header.h": preprocessor searches current working directory first, then falls back to system paths.', {'my_header': 'local_then_system'}, {'include_paths': [{'type': 'local', 'path': '"my_header.h"'}]}),
            (3, 3, 'Without mock local header, compilation halts with: fatal error: my_header.h: No such file or directory.', {'status': 'INTENTIONAL_COMPILE_ERROR'}, {'stack': []}),
        ]
    )

    # Q100: Accidental Semicolon in Macro Definition -> Key D
    add_q(
        100, 'CAT_MACRO_PREPROC', 'Medium', 'Accidental Semicolon in Macro Definition',
        'What happens when attempting to compile the following program?',
        r"""#include <stdio.h>
#define PI 3.14;
int main() {
    double r = 10.0;
    double a = PI * r * r;
    printf("%f\n", a);
    return 0;
}""",
        2, '#define PI 3.14;', 'The semicolon at the end of #define PI 3.14; is included in the macro replacement! PI * r * r expands to 3.14; * r * r, causing a COMPILATION ERROR!',
        [
            ('A', 'Prints 314.000000', False, 'Thought the semicolon was ignored by the preprocessor.', 'The preprocessor does not discard trailing semicolons in #define; it copies them verbatim into the code.'),
            ('B', 'Prints 3.140000', False, 'Thought only PI was evaluated.', 'Code fails to compile due to syntax error.'),
            ('C', 'Undefined Behavior', False, 'Thought macro syntax errors are undefined behavior.', 'A premature semicolon inside an expression is a hard compilation syntax error.'),
            ('D', 'Compilation Error (Premature semicolon in expression)', True, "The preprocessor blindly copies the semicolon into the expansion: double a = 3.14; * r * r; The semicolon prematurely terminates the assignment statement, leaving '* r * r;' as an invalid expression statement, causing a compilation error.", ''),
        ],
        'Preprocessor directives do not use semicolons. #define PI 3.14; inserts a semicolon into PI * r * r, causing a fatal Compilation Error.',
        'ISO/IEC 9899:1999 §6.10.3',
        "The Semicolon in Macro Replacement Trap:\n1. Preprocessor Syntax Rules (§6.10.3):\n   - In C, preprocessor directives end at the newline character, NOT with a semicolon.\n   - Any character following the macro name (excluding leading whitespace) is part of the replacement token sequence.\n   - Therefore, #define PI 3.14; defines PI as the four-token sequence: 3 . 14 ;\n2. Expansion in Code:\n   - Original statement: double a = PI * r * r;\n   - Expanded statement: double a = 3.14; * r * r;\n3. Compiler Grammar Breakdown:\n   - Statement 1: double a = 3.14; (valid declaration)\n   - Statement 2: * r * r; (syntax error: unary * applied to r, then binary * has no left operand or invalid syntax).\n   - GCC emits: error: expected expression before '*' token.\n4. Result: Compilation halted with exit code 1; no executable generated.\n\nExam Trap: Never put a semicolon at the end of a #define line unless you explicitly want a semicolon inside the expanded text!",
        [
            (1, 2, "#define PI 3.14; parsed: replacement tokens are '3.14;'. Semicolon included in macro definition.", {'PI_expansion': '3.14;'}, {'preprocessor': [{'macro': 'PI', 'expansion': '3.14;'}]}),
            (2, 5, 'Expansion: double a = 3.14; * r * r; splits statement prematurely at semicolon.', {'syntax_break': 'double a = 3.14; * r * r;'}, {'stack': []}),
            (3, 5, "Compiler halts with syntax error: expected expression before '*' token -> COMPILATION ERROR.", {'status': 'COMPILATION ERROR'}, {'stack': []}),
        ]
    )

    print("bank_part4 loaded (20 questions, total 100).")
