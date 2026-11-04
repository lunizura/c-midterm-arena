# syllabus_part2.py
# Q035 - Q050: TOPIC_CONDITIONALS (if, if-else, switch-case)
# Q051 - Q068: TOPIC_LOOPS (for, while, do-while, break, continue)
# Pedagogically upgraded with balanced keys, verified GCC code, aligned traps,
# in-depth multi-paragraph deep dives, multi-step execution traces with memory snapshots,
# and rigorous distractor rationales.

def load_part2(add_q):
    # =========================================================================
    # TOPIC_CONDITIONALS (Q035 - Q050)
    # =========================================================================
    # Q035: Assignment (=) in If Condition
    add_q(
        35, 'TOPIC_CONDITIONALS', 'Easy', 'Assignment (=) in If Condition',
        'What is the output of the following program?',
        '#include <stdio.h>\nint main() {\n    int x = 0;\n    if (x = 5) {\n        printf("TRUE %d\\n", x);\n    } else {\n        printf("FALSE %d\\n", x);\n    }\n    return 0;\n}',
        4, 'if (x = 5)', '= is ASSIGNMENT, not comparison (==)! x is assigned 5. Since 5 is non-zero, condition is TRUE!',
        [
            ('A', 'FALSE 0', False, 'Thought x == 5 was tested; since x was initialized to 0, assumed condition evaluated to false.', "The single '=' is assignment, not equality '=='. It mutates x to 5 and yields 5, which tests as true."),
            ('B', 'Compile error', False, 'Believed assignment inside an if condition is illegal syntax in C.', 'In C, assignment is an expression that yields a value, making it completely legal inside controlling expressions.'),
            ('C', 'TRUE 5', True, "The single '=' operator assigns 5 to x; the value of the assignment expression is 5 (non-zero/true), so the then-branch prints 'TRUE 5'.", ''),
            ('D', 'TRUE 0', False, 'Thought the condition succeeded but x remained 0.', "The assignment operator '=' explicitly mutates the variable; x is 5 when printf executes.")
        ],
        'An assignment expression has the value of the left operand after assignment. x = 5 yields 5 (true).',
        'ISO/IEC 9899:1999 §6.5.16 (Assignment operators) & §6.8.4.1 (The if statement)',
        "In C, '=' is the assignment operator, whereas '==' is the relational equality operator. An assignment expression has the value of the left operand after the assignment (ISO C99 §6.5.16#3).\n\nIn 'if (x = 5)':\n1. 5 is assigned to the variable 'x'.\n2. The expression itself yields the assigned value 5.\n3. The if statement tests whether the controlling expression compares unequal to 0 (§6.8.4.1).\nBecause 5 != 0, the condition is true. The then-branch executes, printing 'TRUE 5'.\n\nThis is perhaps the most notorious source of logic errors in C. Most modern compilers issue a warning ('suggest parentheses around assignment used as truth value') under -Wall, but it remains strictly conforming C code.",
        [
            (1, 3, 'Initialize local variable int x = 0 on stack.', {'x': 0}, {'stack': [{'name': 'x', 'type': 'int', 'address': '0x7ffd10', 'value': '0'}]}),
            (2, 4, 'Execute assignment x = 5: mutates x to 5; expression yields 5 (non-zero/true).', {'x': 5, 'condition_val': 5}, {'stack': [{'name': 'x', 'type': 'int', 'address': '0x7ffd10', 'value': '5'}]}),
            (3, 5, "Condition is true: enter then-branch; printf prints 'TRUE 5\\n'.", {'stdout': 'TRUE 5'}, {'stack': [{'name': 'x', 'type': 'int', 'address': '0x7ffd10', 'value': '5'}]})
        ]
    )

    # Q036: Assignment of 0 in If Condition
    add_q(
        36, 'TOPIC_CONDITIONALS', 'Easy', 'Assignment of 0 in If Condition',
        'What is the output of the following program?',
        '#include <stdio.h>\nint main() {\n    int x = 5;\n    if (x = 0) {\n        printf("TRUE %d\\n", x);\n    } else {\n        printf("FALSE %d\\n", x);\n    }\n    return 0;\n}',
        4, 'if (x = 0)', 'x = 0 assigns 0 to x and produces value 0. In C, 0 represents FALSE, so the else branch executes with x = 0!',
        [
            ('A', 'TRUE 5', False, 'Thought assignment succeeded and therefore counted as true.', 'The truthiness of an assignment expression depends on the assigned value. Assigning 0 yields 0 (false).'),
            ('B', 'FALSE 5', False, 'Thought the condition failed without modifying x.', 'Assignment always mutates the variable; x was updated from 5 to 0 before the branch decision.'),
            ('C', 'TRUE 0', False, 'Thought any assignment expression is truthy.', '0 is strictly false in C; an assignment that yields 0 evaluates to false.'),
            ('D', 'FALSE 0', True, "x = 0 assigns 0 to x and produces expression value 0 (false). The else branch executes and prints 'FALSE 0'.", '')
        ],
        'x = 0 assigns 0 to x and produces value 0. In C, 0 is false, so else executes.',
        'ISO/IEC 9899:1999 §6.5.16 & §6.8.4.1',
        'Just as in Q035, \'x = 0\' is an assignment expression. The value 0 is stored into \'x\', and the expression itself evaluates to 0.\n\nIn C control flow statements, any scalar expression comparing equal to 0 is treated as false. Because the condition evaluates to 0, the then-branch is bypassed, and control transfers to the else-branch.\n\nInside the else-branch, \'x\' holds the newly assigned value 0. Therefore, \'printf("FALSE %d\\n", x)\' prints \'FALSE 0\'. This reinforces that the assignment side effect happens unconditionally before the branch decision.',
        [
            (1, 3, 'Initialize int x = 5 on the stack.', {'x': 5}, {'stack': [{'name': 'x', 'type': 'int', 'address': '0x7ffd10', 'value': '5'}]}),
            (2, 4, 'Execute assignment x = 0: mutates x to 0; expression yields 0 (false).', {'x': 0, 'condition_val': 0}, {'stack': [{'name': 'x', 'type': 'int', 'address': '0x7ffd10', 'value': '0'}]}),
            (3, 7, "Condition is false (0): jump to else-branch; printf prints 'FALSE 0\\n'.", {'stdout': 'FALSE 0'}, {'stack': [{'name': 'x', 'type': 'int', 'address': '0x7ffd10', 'value': '0'}]})
        ]
    )

    # Q037: Accidental Semicolon After if-Statement
    add_q(
        37, 'TOPIC_CONDITIONALS', 'Easy', 'Accidental Semicolon After if-Statement',
        'What is the output of the following program?',
        '#include <stdio.h>\nint main() {\n    int x = 3;\n    if (x > 5); {\n        printf("BIG\\n");\n    }\n    return 0;\n}',
        4, 'if (x > 5);', "The semicolon immediately after if (x > 5) acts as an EMPTY NULL STATEMENT! The following block { printf('BIG'); } executes UNCONDITIONALLY!",
        [
            ('A', 'BIG', True, 'The semicolon creates a null statement as the if-body. The subsequent compound block { ... } is independent and executes unconditionally.', ''),
            ('B', 'No output', False, "Thought the block { printf('BIG\\n'); } was controlled by the if-statement (and since 3 > 5 is false, skipped).", 'The semicolon terminates the if-statement immediately with a null body. The subsequent { ... } is a standalone compound statement.'),
            ('C', 'Compile error', False, 'Thought placing a semicolon directly after an if condition is illegal.', 'A semicolon forms a valid null statement (§6.8.3) in C; compilers accept it without error.'),
            ('D', 'Undefined behavior', False, 'Thought empty statements produce undefined behavior.', 'Null statements are completely defined in ISO C.')
        ],
        'A semicolon after if creates a null statement as the body. The following block executes unconditionally.',
        'ISO/IEC 9899:1999 §6.8.3 (Expression and null statements) & §6.8.4.1',
        'In C syntax (§6.8.4.1), an if statement has the form:\n\'if ( expression ) statement\'\n\nA single semicolon \';\' is syntactically a null statement (§6.8.3). Therefore, writing \'if (x > 5);\' constitutes a complete if statement whose controlled body is the null statement (which does nothing).\n\nThe subsequent brace-enclosed block:\n\'{ printf("BIG\\n"); }\'\nis parsed as an entirely separate compound statement at block scope that follows the if statement sequentially. Because it is not governed by the if statement, it executes unconditionally, printing \'BIG\'.',
        [
            (1, 3, 'Initialize int x = 3 on the stack.', {'x': 3}, {'stack': [{'name': 'x', 'type': 'int', 'address': '0x7ffd10', 'value': '3'}]}),
            (2, 4, "Evaluate if (x > 5): 3 > 5 is false (0); null statement ';' body is skipped.", {'condition': 0}, {'stack': [{'name': 'x', 'type': 'int', 'address': '0x7ffd10', 'value': '3'}]}),
            (3, 4, "Enter subsequent standalone compound block { ... }; printf prints 'BIG\\n'.", {'stdout': 'BIG'}, {'stack': [{'name': 'x', 'type': 'int', 'address': '0x7ffd10', 'value': '3'}]})
        ]
    )

    # Q038: Dangling Else Association Rule
    add_q(
        38, 'TOPIC_CONDITIONALS', 'Tricky', 'Dangling Else Association Rule',
        'What is the output of the following program?',
        '#include <stdio.h>\nint main() {\n    int a = 1, b = 0;\n    if (a == 1)\n        if (b == 1)\n            printf("BOTH\\n");\n    else\n        printf("ELSE\\n");\n    return 0;\n}',
        7, 'else', "In C, an 'else' binds to the CLOSEST preceding 'if' that does not have an else! Indentation is ignored by the compiler!",
        [
            ('A', 'No output', False, "Thought the 'else' associated with 'if (a == 1)' based on indentation, and since a == 1, else was skipped.", "C is free-form and ignores indentation. The 'else' grammatically binds to 'if (b == 1)', not 'if (a == 1)'."),
            ('B', 'ELSE', True, "In C grammar, an 'else' associates with the lexically closest preceding unmatched 'if' (here, 'if (b == 1)'). Since b == 0, that else executes.", ''),
            ('C', 'BOTH', False, 'Thought both branches executed.', "b == 1 is false (0), so 'BOTH' is not printed."),
            ('D', 'Compile error', False, 'Thought ambiguous nested ifs require braces.', 'The C grammar disambiguates dangling else unambiguously: else attaches to the nearest if.')
        ],
        'An else is associated with the lexically nearest preceding if without an else. Binds to if (b == 1).',
        'ISO/IEC 9899:1999 §6.8.4.1#3 (The if statement - dangling else rule)',
        'The dangling-else ambiguity is solved in C by an explicit grammar rule in ISO C99 §6.8.4.1#3:\n\'An else is associated with the lexically nearest preceding if that is allowed by the syntax.\'\n\nAlthough the programmer indented the \'else\' to match the outer \'if (a == 1)\', the C compiler is whitespace-insensitive. The nearest preceding unmatched \'if\' is \'if (b == 1)\'. Thus, the code is parsed as:\nif (a == 1) {\n    if (b == 1) {\n        printf("BOTH\\n");\n    } else {\n        printf("ELSE\\n");\n    }\n}\n\nExecution:\n1. \'a == 1\' is true (1), so we enter the outer if body.\n2. \'b == 1\' (0 == 1) is false (0).\n3. The associated else-branch executes, printing \'ELSE\'.',
        [
            (1, 3, 'Initialize a = 1, b = 0 on the stack.', {'a': 1, 'b': 0}, {'stack': [{'name': 'a', 'type': 'int', 'address': '0x7ffd10', 'value': '1'}, {'name': 'b', 'type': 'int', 'address': '0x7ffd14', 'value': '0'}]}),
            (2, 4, 'Evaluate outer if (a == 1) -> 1 == 1 is true; enter outer if block.', {'outer_cond': 1}, {'stack': [{'name': 'a', 'type': 'int', 'address': '0x7ffd10', 'value': '1'}, {'name': 'b', 'type': 'int', 'address': '0x7ffd14', 'value': '0'}]}),
            (3, 5, 'Evaluate inner if (b == 1) -> 0 == 1 is false (0).', {'inner_cond': 0}, {'stack': [{'name': 'a', 'type': 'int', 'address': '0x7ffd10', 'value': '1'}, {'name': 'b', 'type': 'int', 'address': '0x7ffd14', 'value': '0'}]}),
            (4, 8, "Dangling else binds to inner if: execute else branch; printf prints 'ELSE\\n'.", {'stdout': 'ELSE'}, {'stack': [{'name': 'a', 'type': 'int', 'address': '0x7ffd10', 'value': '1'}, {'name': 'b', 'type': 'int', 'address': '0x7ffd14', 'value': '0'}]})
        ]
    )

    # Q039: Truthiness of Non-Zero Values in C
    add_q(
        39, 'TOPIC_CONDITIONALS', 'Easy', 'Truthiness of Non-Zero Values in C',
        'What is the output of the following program?',
        '#include <stdio.h>\nint main() {\n    int x = -1;\n    if (x) {\n        printf("TRUE\\n");\n    } else {\n        printf("FALSE\\n");\n    }\n    return 0;\n}',
        4, 'if (x)', 'In C, ANY non-zero value is TRUE—including negative numbers like -1! Only 0 is false!',
        [
            ('A', 'FALSE', False, 'Assumed negative numbers are treated as false or invalid in C.', 'In C, truthiness is tested via comparison with zero (x != 0). Since -1 != 0, it evaluates strictly to true.'),
            ('B', 'Compile error', False, 'Thought conditions require explicit boolean comparison operators (e.g. x != 0).', 'Any scalar expression can serve directly as a controlling expression in C.'),
            ('C', 'Undefined behavior', False, 'Thought evaluating negative integers in an if statement is undefined.', 'The standard explicitly defines non-zero values as true.'),
            ('D', 'TRUE', True, 'In C, any non-zero integer (including negative numbers like -1) evaluates to true in a boolean context.', '')
        ],
        'An expression is true if its value compares unequal to 0. -1 != 0, so if (x) is true.',
        'ISO/IEC 9899:1999 §6.8.4.1#1 (The if statement - controlling expression truthiness)',
        "In C, there was historically no native boolean type (prior to C99's _Bool and <stdbool.h>). The language's fundamental definition of truthiness (§6.8.4.1) is:\n'the first substatement is executed if the expression compares unequal to 0.'\n\nTherefore:\n- Value 0 is false.\n- ANY value unequal to 0 (such as 1, 42, -1, -999, 0.5) is true.\n\nSince 'x = -1' compares unequal to 0 (-1 != 0), the condition evaluates to true, and the then-branch executes, printing 'TRUE'.\n\nNovices coming from other environments sometimes believe only positive numbers are true or that -1 signifies an error state that evaluates to false.",
        [
            (1, 3, 'Initialize int x = -1 on stack.', {'x': -1}, {'stack': [{'name': 'x', 'type': 'int', 'address': '0x7ffd10', 'value': '-1'}]}),
            (2, 4, 'Evaluate if (x): test whether x != 0 -> (-1 != 0) is true (1).', {'condition': 1}, {'stack': [{'name': 'x', 'type': 'int', 'address': '0x7ffd10', 'value': '-1'}]}),
            (3, 5, "Condition is true: execute then-branch; printf prints 'TRUE\\n'.", {'stdout': 'TRUE'}, {'stack': [{'name': 'x', 'type': 'int', 'address': '0x7ffd10', 'value': '-1'}]})
        ]
    )

    # Q040: Switch Case Fallthrough Without Break
    add_q(
        40, 'TOPIC_CONDITIONALS', 'Easy', 'Switch Case Fallthrough Without Break',
        'What is the output of the following program?',
        '#include <stdio.h>\nint main() {\n    int val = 2;\n    switch (val) {\n        case 1: printf("ONE ");\n        case 2: printf("TWO ");\n        case 3: printf("THREE ");\n        default: printf("DEF ");\n    }\n    printf("\\n");\n    return 0;\n}',
        6, 'case 2:', 'Without break statements, switch cases FALL THROUGH sequentially! Matching case 2 executes case 2, case 3, and default!',
        [
            ('A', 'TWO ', False, 'Assumed only the matching case executes and switch automatically terminates.', "C switch statements feature fall-through semantics; without 'break', execution continues into subsequent cases unconditionally."),
            ('B', 'ONE TWO THREE DEF ', False, 'Thought switch executes all cases from the top.', 'Switch jumps directly to the matching case label (case 2); earlier cases are bypassed.'),
            ('C', 'TWO THREE DEF ', True, "Execution jumps to matching 'case 2'. Because there are no break statements, execution falls through all subsequent cases including default.", ''),
            ('D', 'DEF ', False, 'Thought default overrides cases.', 'Default only matches initially if no case matches; here case 2 matches.')
        ],
        'Switch statements in C feature fall-through semantics. Flow continues until a break is encountered.',
        'ISO/IEC 9899:1999 §6.8.4.2 (The switch statement)',
        "Case labels inside a switch statement are merely entry jump targets, similar to goto labels (ISO C99 §6.8.4.2). Once execution jumps to a matching case label, the processor executes instructions sequentially downwards until it encounters an explicit 'break' statement or reaches the end of the switch block.\n\nHere, 'val = 2':\n1. The switch jumps directly to 'case 2:', printing 'TWO '.\n2. Because there is no 'break', control falls through into 'case 3:', printing 'THREE '.\n3. Control falls through into 'default:', printing 'DEF '.\nTotal printed output is 'TWO THREE DEF '.\n\nFall-through can be useful for grouping multiple values, but omitting 'break' unintentionally is one of the classic bugs in systems programming.",
        [
            (1, 3, 'Initialize int val = 2.', {'val': 2}, {'stack': [{'name': 'val', 'type': 'int', 'address': '0x7ffd10', 'value': '2'}]}),
            (2, 4, "switch(val) evaluates val = 2: jumps directly to label 'case 2:'.", {'target': 'case 2'}, {'stack': [{'name': 'val', 'type': 'int', 'address': '0x7ffd10', 'value': '2'}]}),
            (3, 6, "Execute case 2: printf prints 'TWO '. No break -> fall through to case 3.", {'stdout': 'TWO '}, {'stack': [{'name': 'val', 'type': 'int', 'address': '0x7ffd10', 'value': '2'}]}),
            (4, 7, "Fall-through into case 3: printf prints 'THREE '. No break -> fall through to default.", {'stdout': 'TWO THREE '}, {'stack': [{'name': 'val', 'type': 'int', 'address': '0x7ffd10', 'value': '2'}]}),
            (5, 8, "Fall-through into default: printf prints 'DEF '. Switch terminates.", {'stdout': 'TWO THREE DEF '}, {'stack': [{'name': 'val', 'type': 'int', 'address': '0x7ffd10', 'value': '2'}]})
        ]
    )

    # Q041: Switch Default at Beginning with Fallthrough
    add_q(
        41, 'TOPIC_CONDITIONALS', 'Medium', 'Switch Default at Beginning with Fallthrough',
        'What is the output of the following program?',
        '#include <stdio.h>\nint main() {\n    int x = 2;\n    switch (x) {\n        default: printf("DEF ");\n        case 1: printf("ONE ");\n        case 2: printf("TWO ");\n        case 3: printf("THREE ");\n    }\n    printf("\\n");\n    return 0;\n}',
        5, 'default:', 'default label can be anywhere inside switch! Since case 2 matches x=2, execution jumps directly to case 2 (skipping default), then falls through to case 3!',
        [
            ('A', 'TWO THREE ', True, "The switch jumps directly to the matching 'case 2' label, bypassing default and case 1, then falls through to case 3.", ''),
            ('B', 'DEF ONE TWO THREE ', False, 'Thought execution starts at the top of the switch body simply because default is listed first.', "Switch evaluates all case labels first regardless of where 'default' is placed; default is only taken if no case matches."),
            ('C', 'TWO ', False, 'Assumed switch cases do not fall through into case 3 without break.', 'Because there is no break after case 2, control falls through into case 3.'),
            ('D', 'DEF ', False, 'Thought placing default first forces default execution.', 'Case matching takes priority over default.')
        ],
        'The default label can be placed anywhere in switch. If a case matches, it jumps directly to that case. Falls through to case 3.',
        'ISO/IEC 9899:1999 §6.8.4.2#5 (The switch statement - label order)',
        "In C, the position of the 'default' label inside a switch statement does not dictate its evaluation priority. Under ISO C99 §6.8.4.2:\n1. The controlling expression is evaluated (here, x = 2).\n2. The compiler searches for a case label with a matching constant value.\n3. If a match is found, control jumps directly to that case statement, regardless of where default is positioned.\n4. Only if NO case matches does control transfer to the default label.\n\nBecause 'x = 2' matches 'case 2:', execution begins at line 7, printing 'TWO '. Due to the absence of a 'break' statement, execution falls through into 'case 3:', printing 'THREE '. Total output: 'TWO THREE '.",
        [
            (1, 3, 'Initialize int x = 2.', {'x': 2}, {'stack': [{'name': 'x', 'type': 'int', 'address': '0x7ffd10', 'value': '2'}]}),
            (2, 4, 'switch(x) matches case 2: jump directly to line 7 (skipping default and case 1).', {'target': 'case 2'}, {'stack': [{'name': 'x', 'type': 'int', 'address': '0x7ffd10', 'value': '2'}]}),
            (3, 7, "Execute case 2: printf prints 'TWO '. No break -> fall through to case 3.", {'stdout': 'TWO '}, {'stack': [{'name': 'x', 'type': 'int', 'address': '0x7ffd10', 'value': '2'}]}),
            (4, 8, "Fall-through into case 3: printf prints 'THREE '. Switch block terminates.", {'stdout': 'TWO THREE '}, {'stack': [{'name': 'x', 'type': 'int', 'address': '0x7ffd10', 'value': '2'}]})
        ]
    )

    # Q042: Variable in Switch Case Label
    add_q(
        42, 'TOPIC_CONDITIONALS', 'Medium', 'Variable in Switch Case Label',
        'What happens when attempting to compile this program?',
        '#include <stdio.h>\nint main() {\n    int x = 2;\n    int y = 2;\n    switch (x) {\n        case y: printf("TWO\\n"); break;\n        default: printf("DEF\\n");\n    }\n    return 0;\n}',
        6, 'case y:', "Switch case labels MUST be compile-time integer CONSTANT expressions! A variable like 'y' causes a compile error!",
        [
            ('A', 'TWO', False, 'Assumed the runtime compares x against the variable value y (2 == 2).', 'C switch statements generate jump tables at compile time; case labels cannot be variables, even if initialized with constants.'),
            ('B', 'Compilation error', True, "The expression following 'case' must be an integer constant expression known at compile time. Variable 'y' is a non-constant lvalue.", ''),
            ('C', 'DEF', False, 'Thought the variable was ignored and jumped to default.', 'Constraint violation causes compilation to fail; the code never runs.'),
            ('D', 'Undefined behavior', False, 'Thought it compiles but behaves unpredictably.', 'Compilers must reject non-constant case labels with a diagnostic error.')
        ],
        "The expression of each case label shall be an integer constant expression. Variable 'y' causes a compile error.",
        'ISO/IEC 9899:1999 §6.8.4.2#3 (The switch statement - constant expression constraint)',
        "ISO C99 §6.8.4.2#3 sets forth a strict constraint:\n'The expression of each case label shall be an integer constant expression and no two of the case constant expressions in the same switch statement shall have the same value after conversion.'\n\nAn integer constant expression (§6.6) can contain integer literals, character constants, sizeof expressions, and enumeration constants. It CANNOT contain variables, even if declared 'const int' in C (in C, const variables are read-only variables, not true integer constant expressions).\n\nBecause 'y' is a variable, GCC emits: 'error: case label does not reduce to an integer constant'. This is a very common exam trap distinguishing C from languages like Python or JavaScript.",
        [
            (1, 4, 'Compiler parses declarations int x = 2, int y = 2.', {'x': 2, 'y': 2}, {'stack': []}),
            (2, 6, "Compiler checks case label 'case y:': 'y' is a variable, not an integer constant expression.", {'check': 'non-constant case label'}, {'stack': []}),
            (3, 6, "Constraint violation (§6.8.4.2#3): compilation halts with 'case label does not reduce to an integer constant'.", {'compiler_error': 'case label does not reduce to an integer constant'}, {'stack': []})
        ]
    )

    # Q043: Floating-Point in Switch Statement
    add_q(
        43, 'TOPIC_CONDITIONALS', 'Easy', 'Floating-Point in Switch Statement',
        'What happens when attempting to compile this program?',
        '#include <stdio.h>\nint main() {\n    float f = 2.0f;\n    switch (f) {\n        case 2: printf("TWO\\n"); break;\n        default: printf("DEF\\n");\n    }\n    return 0;\n}',
        4, 'switch (f)', 'The controlling expression of a switch statement MUST be an INTEGER type! float/double is illegal in switch!',
        [
            ('A', 'TWO', False, 'Thought float 2.0f is automatically cast to integer 2.', 'The compiler does not implicitly truncate floating-point switch expressions; it rejects the construct with a constraint violation.'),
            ('B', 'DEF', False, 'Thought float mismatches all cases and executes default.', 'Compilation fails before any executable code can be generated.'),
            ('C', 'Compilation error', True, 'The controlling expression of a switch statement must have an integer type; floating-point types (float, double) are forbidden.', ''),
            ('D', 'Undefined behavior', False, 'Thought floating-point switch causes undefined behavior.', 'The C standard explicitly diagnoses non-integer switch expressions at compile time.')
        ],
        'The controlling expression of a switch statement shall have integer type. float is a constraint violation.',
        'ISO/IEC 9899:1999 §6.8.4.2#1 (The switch statement - controlling expression constraint)',
        "Section §6.8.4.2#1 of the ISO C standard mandates:\n'The controlling expression of a switch statement shall have integer type.'\n\nFloating-point types (float, double, long double) have representation inaccuracies and cannot be cleanly indexed in compiler jump tables. Therefore, using a float as the switch controlling expression is a constraint violation.\n\nGCC emits: 'error: switch quantity not an integer'. If you need to branch on floating-point values in C, you must either cast the float to int ('switch ((int)f)') or use an if-else ladder with appropriate tolerance checks (e.g. fabs(f - 2.0f) < 1e-6).",
        [
            (1, 3, 'Compiler parses declaration float f = 2.0f.', {'f': 2.0}, {'stack': []}),
            (2, 4, "Compiler validates switch controlling expression 'switch (f)': checks if type is integer.", {'check_type': 'float (non-integer)'}, {'stack': []}),
            (3, 4, "Constraint violation (§6.8.4.2#1): compilation fails with 'switch quantity not an integer'.", {'compiler_error': 'switch quantity not an integer'}, {'stack': []})
        ]
    )

    # Q044: Duplicate Case Labels in Switch
    add_q(
        44, 'TOPIC_CONDITIONALS', 'Easy', 'Duplicate Case Labels in Switch',
        'What happens when attempting to compile this program?',
        '#include <stdio.h>\nint main() {\n    int x = 1;\n    switch (x) {\n        case 1: printf("FIRST "); break;\n        case 1: printf("SECOND "); break;\n        default: printf("DEF ");\n    }\n    return 0;\n}',
        6, 'SECOND', 'No two case constant expressions in the same switch statement may have the same value! Duplicate case 1 causes a compile error!',
        [
            ('A', 'FIRST ', False, 'Thought only the first matching case 1 is used and the second is ignored.', 'The compiler detects duplicate labels as a syntax error rather than silently ignoring the duplicate.'),
            ('B', 'SECOND ', False, 'Thought the second case 1 overwrote the first.', 'Case labels must be mutually unique within a switch block.'),
            ('C', 'FIRST SECOND ', False, 'Thought both cases execute sequentially.', 'The program will not compile because duplicate case labels are a constraint violation.'),
            ('D', 'Compilation error', True, "ISO C forbids duplicate case values in the same switch statement; having two 'case 1:' labels is a constraint violation.", '')
        ],
        'No two case constant expressions in the same switch shall have the same value. Duplicate case 1 is a compile error.',
        'ISO/IEC 9899:1999 §6.8.4.2#3 (The switch statement - unique case values constraint)',
        "ISO C99 §6.8.4.2#3 explicitly specifies:\n'no two of the case constant expressions in the same switch statement shall have the same value after conversion.'\n\nA switch statement is compiled into an indexed dispatch table or balanced binary search tree of target addresses. Duplicate case labels introduce an irreconcilable ambiguity in jump target resolution.\n\nWhen GCC encounters duplicate case values, it halts compilation with: 'error: duplicate case value' and references the previous definition. This rule also applies if two distinct expressions evaluate to the same value (e.g. 'case 1:' and 'case 2 - 1:').",
        [
            (1, 5, "Compiler registers first label 'case 1:' in switch jump table.", {'registered_labels': [1]}, {'stack': []}),
            (2, 6, "Compiler encounters duplicate label 'case 1:': detects collision in jump table.", {'duplicate': 1}, {'stack': []}),
            (3, 6, "Constraint violation (§6.8.4.2#3): compilation fails with 'duplicate case value 1'.", {'compiler_error': 'duplicate case value'}, {'stack': []})
        ]
    )

    # Q045: Grouping Multiple Case Labels
    add_q(
        45, 'TOPIC_CONDITIONALS', 'Easy', 'Grouping Multiple Case Labels',
        'What is the output of the following program?',
        '#include <stdio.h>\nint main() {\n    char grade = \'b\';\n    switch (grade) {\n        case \'A\':\n        case \'a\': printf("EXCELLENT\\n"); break;\n        case \'B\':\n        case \'b\': printf("GOOD\\n"); break;\n        default: printf("OTHER\\n");\n    }\n    return 0;\n}',
        8, "case 'b':", 'Stacking case labels without statements between them is the standard idiom for logical OR in switch statements!',
        [
            ('A', 'GOOD', True, "Stacking case 'B': and case 'b': without intervening code allows 'b' to jump directly to line 8 and print 'GOOD'.", ''),
            ('B', 'EXCELLENT', False, "Thought case 'a' matched or fallthrough occurred.", "grade is 'b', which matches case 'b' on line 8."),
            ('C', 'OTHER', False, 'Thought lowercase letters are not supported in switch.', 'Character literals are integers and fully supported as case constants.'),
            ('D', 'EXCELLENT GOOD', False, 'Thought all cases fall through.', 'A break statement terminates the block after printing GOOD.')
        ],
        "Cases without statements fall through directly to the next case. Stacking case 'B': and 'b': groups both under GOOD.",
        'ISO/IEC 9899:1999 §6.8.4.2 (The switch statement - case grouping)',
        'In C, case labels are labels attached to statements. When multiple case labels precede a statement without any intervening statements (such as \'case \'B\': case \'b\': printf(...); break;\'), both values share that statement as their target.\n\nThis is the standard, idiomatic C pattern for simulating logical OR (\'if (grade == \'B\' || grade == \'b\')\') inside a switch statement.\n\nWhen grade = \'b\':\n1. The switch matches \'case \'b\':\'.\n2. Execution executes \'printf("GOOD\n");\'.\n3. The \'break\' statement terminates the switch block immediately.\nThe output is \'GOOD\'.',
        [
            (1, 3, "Initialize char grade = 'b' (ASCII 98).", {'grade': "'b'"}, {'stack': [{'name': 'grade', 'type': 'char', 'address': '0x7ffd10', 'value': "'b'"}]}),
            (2, 4, "switch(grade) matches label 'case 'b':': jumps to line 8.", {'target': "case 'b'"}, {'stack': [{'name': 'grade', 'type': 'char', 'address': '0x7ffd10', 'value': "'b'"}]}),
            (3, 8, "Execute printf('GOOD\\\\n'); then break terminates switch.", {'stdout': 'GOOD'}, {'stack': [{'name': 'grade', 'type': 'char', 'address': '0x7ffd10', 'value': "'b'"}]})
        ]
    )

    # Q046: Missing Braces Indentation Illusion
    add_q(
        46, 'TOPIC_CONDITIONALS', 'Medium', 'Missing Braces Indentation Illusion',
        'What is the output of the following program?',
        '#include <stdio.h>\nint main() {\n    int x = 5;\n    if (x > 10)\n        printf("A ");\n        printf("B ");\n    printf("C\\n");\n    return 0;\n}',
        6, 'printf("B ");', "Without curly braces {}, an if statement controls ONLY THE SINGLE NEXT STATEMENT! printf('B ') is OUTSIDE the if and executes unconditionally!",
        [
            ('A', 'C', False, "Thought both printf('A ') and printf('B ') were controlled by if (x > 10) due to indentation.", 'C completely ignores indentation. Without braces {}, only the single statement immediately following the if condition is controlled.'),
            ('B', 'B C', True, "Without braces, only printf('A ') is governed by the if statement. printf('B ') and printf('C') execute unconditionally.", ''),
            ('C', 'A B C', False, 'Thought condition x > 10 (5 > 10) was true.', "5 > 10 is false, so printf('A ') is skipped."),
            ('D', 'A C', False, "Thought printf('B ') was skipped but printf('A ') executed.", "printf('A ') is the only statement controlled by the if.")
        ],
        "An if statement without braces controls only the single following statement. printf('B ') executes unconditionally.",
        'ISO/IEC 9899:1999 §6.8.4.1 (The if statement - single substatement syntax)',
        'In C grammar (§6.8.4.1), the syntax of an if statement is:\n\'if ( expression ) statement\'\n\nNotice that \'statement\' is singular. If braces \'{ }\' are omitted, only the single statement immediately following the condition belongs to the if body. Indentation is purely cosmetic in C and completely ignored by the compiler.\n\nTherefore, the code is parsed as:\nif (x > 10) {\n    printf("A ");\n}\nprintf("B ");\nprintf("C\n");\n\nSince \'x = 5\', \'5 > 10\' is false, so \'printf("A ")\' is skipped. Execution continues with the subsequent statements, printing \'B C\'. This trap (famous from Apple\'s \'goto fail\' SSL vulnerability) highlights why good style guides mandate braces on all control structures.',
        [
            (1, 3, 'Initialize int x = 5 on the stack.', {'x': 5}, {'stack': [{'name': 'x', 'type': 'int', 'address': '0x7ffd10', 'value': '5'}]}),
            (2, 4, "Evaluate if (x > 10) -> (5 > 10) is false (0); skip controlled statement printf('A ').", {'condition': 0}, {'stack': [{'name': 'x', 'type': 'int', 'address': '0x7ffd10', 'value': '5'}]}),
            (3, 6, "Execute unconditional statement printf('B '); outputs 'B '.", {'stdout': 'B '}, {'stack': [{'name': 'x', 'type': 'int', 'address': '0x7ffd10', 'value': '5'}]}),
            (4, 7, "Execute unconditional statement printf('C\\n'); outputs 'C'. Total output: 'B C'.", {'stdout': 'B C'}, {'stack': [{'name': 'x', 'type': 'int', 'address': '0x7ffd10', 'value': '5'}]})
        ]
    )

    # Q047: Character in Switch Expression
    add_q(
        47, 'TOPIC_CONDITIONALS', 'Easy', 'Character in Switch Expression',
        'What is the output of the following program?',
        '#include <stdio.h>\nint main() {\n    char code = \'B\';\n    switch (code) {\n        case \'A\': printf("EXCELLENT\\n"); break;\n        case \'B\': printf("GOOD\\n"); break;\n        default: printf("UNKNOWN\\n");\n    }\n    return 0;\n}',
        6, "case 'B':", 'In C, char is an integer type! Character constants promote to int, making char perfectly valid in switch statements!',
        [
            ('A', 'EXCELLENT', False, "Thought switch matches case 'A' first.", "Execution jumps directly to the matching label case 'B':."),
            ('B', 'UNKNOWN', False, 'Thought char was not recognized and triggered default.', "The character literal 'B' matches case 'B' exactly, executing that branch rather than default."),
            ('C', 'Compilation error', False, 'Thought switch statements only accept numeric int variables and reject char.', 'In C, char is an integer type (§6.2.5#3) and is completely valid in switch controlling expressions.'),
            ('D', 'GOOD', True, "char is an integral type that undergoes integer promotion in switch expressions; 'B' matches case 'B': and prints 'GOOD'.", '')
        ],
        'Character constants promote to int and are valid switch case expressions. Prints GOOD.',
        'ISO/IEC 9899:1999 §6.8.4.2 & §6.4.4.4 (Character constants in switch)',
        'In C, the char type is defined as an integer type (§6.2.5#3). When passed to a switch statement, a char variable undergoes integer promotion (§6.3.1.1) to int.\n\nCharacter constants such as \'A\' and \'B\' are also integer constants of type int (§6.4.4.4).\n\nTherefore, \'switch (code)\' with \'code = \'B\'\' evaluates the integer value 66. It matches \'case \'B\':\' (constant 66), executes \'printf("GOOD\n");\', and hits \'break;\', which exits the switch block, printing \'GOOD\'.',
        [
            (1, 3, "Initialize char code = 'B' (ASCII integer value 66).", {'code': "'B' (66)"}, {'stack': [{'name': 'code', 'type': 'char', 'address': '0x7ffd10', 'value': "'B'"}]}),
            (2, 4, "switch(code) promotes 'B' to int 66: matches label 'case 'B':' on line 6.", {'target': "case 'B'"}, {'stack': [{'name': 'code', 'type': 'char', 'address': '0x7ffd10', 'value': "'B'"}]}),
            (3, 6, "Execute printf('GOOD\\\\n'); break exits switch.", {'stdout': 'GOOD'}, {'stack': [{'name': 'code', 'type': 'char', 'address': '0x7ffd10', 'value': "'B'"}]})
        ]
    )

    # Q048: Nested If-Else Boundary Evaluation
    add_q(
        48, 'TOPIC_CONDITIONALS', 'Medium', 'Nested If-Else Boundary Evaluation',
        'What grade is printed by this code for score = 85?',
        '#include <stdio.h>\nint main() {\n    int score = 85;\n    if (score >= 90) {\n        printf("A\\n");\n    } else if (score >= 70) {\n        printf("B\\n");\n    } else if (score >= 80) {\n        printf("B+\\n");\n    } else {\n        printf("C\\n");\n    }\n    return 0;\n}',
        6, 'else if (score >= 70)', "In an if-else ladder, branches are checked IN ORDER! Because 85 >= 70 is TRUE, it prints 'B' and skips the more specific >= 80 branch!",
        [
            ('A', 'B+', False, 'Assumed the compiler finds the most specific or closest matching condition (85 >= 80).', 'C evaluates conditions sequentially in lexical order; once score >= 70 matches, the rest of the ladder is completely skipped.'),
            ('B', 'A', False, 'Thought score matched >= 90.', '85 is less than 90, so the first branch is false.'),
            ('C', 'B', True, "In an if-else-if ladder, the FIRST condition that evaluates to true executes. Since 85 >= 70 is true, it prints 'B' and skips all subsequent branches.", ''),
            ('D', 'C', False, 'Selected the fallback else branch.', 'The ladder already exited at the score >= 70 branch.')
        ],
        'In an if-else ladder, the first matching branch executes and skips the rest. 85 >= 70 matches first, printing B.',
        'ISO/IEC 9899:1999 §6.8.4.1 (The if-else ladder evaluation order)',
        "An if-else-if ladder is simply a chain of nested if-else statements:\nif (c1) s1 else { if (c2) s2 else { if (c3) s3 ... } }\n\nBecause of this nested structure, conditions are evaluated strictly in sequential order from top to bottom. The moment any condition evaluates to non-zero (true), its corresponding block executes, and the entire remainder of the ladder (contained in the else clause) is bypassed.\n\nHere, for score = 85:\n1. 'score >= 90' is false.\n2. 'score >= 70' is TRUE (85 >= 70).\n3. The block for 'score >= 70' prints 'B'.\n4. The remaining branches—including 'else if (score >= 80)'—are inside the skipped else branch and are never checked.\n\nThis is a classic bug in grading algorithms: boundary conditions must always be ordered from most restrictive to least restrictive.",
        [
            (1, 3, 'Initialize int score = 85 on the stack.', {'score': 85}, {'stack': [{'name': 'score', 'type': 'int', 'address': '0x7ffd10', 'value': '85'}]}),
            (2, 4, 'Evaluate first condition score >= 90: (85 >= 90) is false (0).', {'cond1': 0}, {'stack': [{'name': 'score', 'type': 'int', 'address': '0x7ffd10', 'value': '85'}]}),
            (3, 6, 'Evaluate second condition score >= 70: (85 >= 70) is true (1).', {'cond2': 1}, {'stack': [{'name': 'score', 'type': 'int', 'address': '0x7ffd10', 'value': '85'}]}),
            (4, 7, "Execute then-branch for condition 2: printf prints 'B\n'; skip all remaining branches.", {'stdout': 'B'}, {'stack': [{'name': 'score', 'type': 'int', 'address': '0x7ffd10', 'value': '85'}]})
        ]
    )

    # Q049: Testing Variable Against Zero with Assignment
    add_q(
        49, 'TOPIC_CONDITIONALS', 'Medium', 'Testing Variable Against Zero with Assignment',
        'What is the output of the following program?',
        '#include <stdio.h>\nint main() {\n    int is_logged_in = 1;\n    if (is_logged_in = 0) {\n        printf("LOGGED IN\\n");\n    } else {\n        printf("LOGGED OUT\\n");\n    }\n    return 0;\n}',
        4, 'if (is_logged_in = 0)', "Single '=' assigns 0 to is_logged_in, overwriting 1! The assignment yields 0 (false), so else executes!",
        [
            ('A', 'LOGGED IN', False, 'Assumed the condition checked if is_logged_in was 0 (thinking it evaluated equality).', "The single '=' is assignment. It assigns 0 to is_logged_in, which evaluates to 0 (false)."),
            ('B', 'LOGGED OUT', True, "The '=' assignment operator sets is_logged_in to 0 and evaluates to 0 (false), directing execution to the else block.", ''),
            ('C', 'Compilation error', False, 'Thought assignment is forbidden in boolean condition checks.', 'Assignment expressions are syntactically valid everywhere expressions are permitted in C.'),
            ('D', 'Undefined behavior', False, 'Thought assigning within if causes undefined behavior.', 'It is fully defined behavior; the assignment occurs and yields the assigned value.')
        ],
        'Assignment operator (=) sets the variable to 0. 0 is false, so else executes.',
        'ISO/IEC 9899:1999 §6.5.16 & §6.8.4.1',
        "This question targets the dangerous side effect of using '=' instead of '==' in authentication or validation logic.\n\n1. Variable 'is_logged_in' is initialized to 1.\n2. In 'if (is_logged_in = 0)', the value 0 is assigned into 'is_logged_in', overwriting its previous value.\n3. The value of an assignment expression is the value assigned (§6.5.16#3), which is 0.\n4. In an if statement, 0 evaluates to false.\n5. Control immediately branches to the else statement, printing 'LOGGED OUT'.\n\nTo prevent this catastrophic class of bugs, seasoned C developers historically used 'Yoda conditions' (writing 'if (0 == is_logged_in)'), where an accidental '=' causes a compile error because 0 is not a modifiable lvalue.",
        [
            (1, 3, 'Initialize int is_logged_in = 1.', {'is_logged_in': 1}, {'stack': [{'name': 'is_logged_in', 'type': 'int', 'address': '0x7ffd10', 'value': '1'}]}),
            (2, 4, 'Execute assignment is_logged_in = 0: mutates variable to 0; yields 0 (false).', {'is_logged_in': 0, 'condition_val': 0}, {'stack': [{'name': 'is_logged_in', 'type': 'int', 'address': '0x7ffd10', 'value': '0'}]}),
            (3, 7, "Condition is false (0): execute else-branch; printf prints 'LOGGED OUT\n'.", {'stdout': 'LOGGED OUT'}, {'stack': [{'name': 'is_logged_in', 'type': 'int', 'address': '0x7ffd10', 'value': '0'}]})
        ]
    )

    # Q050: Variable Declaration Directly in Switch Case
    add_q(
        50, 'TOPIC_CONDITIONALS', 'Tricky', 'Variable Declaration Directly in Switch Case',
        'What happens when attempting to compile this program under C99/C11 standards?',
        '#include <stdio.h>\nint main() {\n    int opt = 1;\n    switch (opt) {\n        case 1:\n            int val = 10;\n            printf("%d\\n", val);\n            break;\n        default:\n            printf("DEF\\n");\n    }\n    return 0;\n}',
        6, 'int val = 10;', 'In C, a label can only prefix a STATEMENT, not a declaration! Declaring a variable directly after case 1: causes a compile error!',
        [
            ('A', 'Compilation error', True, "In C grammar (§6.8.1), a label can only precede a statement, not a declaration. Declaring 'int val = 10;' directly after a case label is a syntax error.", ''),
            ('B', '10', False, 'Assumed declaring a variable immediately following a case label is valid C syntax.', 'In C99, declarations may be mixed with statements inside compound blocks, but a label must be immediately followed by a statement, not a declaration.'),
            ('C', 'DEF', False, 'Thought the compilation error only affected case 1.', 'Compilation errors prevent the entire program from compiling.'),
            ('D', 'Undefined behavior', False, 'Thought jumping over initialization is undefined at runtime.', 'It is rejected at compile time by the grammar parser.')
        ],
        'A label shall be followed by a statement. A declaration is not a statement. Causes a compile-time error.',
        'ISO/IEC 9899:1999 §6.8.1 (Labeled statements - constraint)',
        "Under ISO C99 §6.8.1, the grammar for a labeled statement is:\n'labeled-statement:\n    case constant-expression : statement\n    default : statement'\n\nNotice that a label MUST be followed by a 'statement'. In C grammar, a 'declaration' is NOT a statement (statements and declarations are distinct syntactic productions). Therefore, placing 'int val = 10;' directly after 'case 1:' violates the grammar.\n\nGCC produces: 'error: a label can only be part of a statement and a declaration is not a statement'.\n\nTo declare variables local to a switch case in C, the programmer must enclose the case in braces to form a compound statement:\ncase 1: {\n    int val = 10;\n    ...\n    break;\n}\nor place a null statement ';' directly after the label.",
        [
            (1, 4, 'Compiler parses switch header and enters switch compound block.', {'opt': 1}, {'stack': []}),
            (2, 6, "Parser encounters label 'case 1:' followed immediately by declaration 'int val = 10;'.", {'grammar_check': 'label followed by declaration'}, {'stack': []}),
            (3, 6, 'Syntax error (§6.8.1): a label can only be part of a statement, not a declaration. Compilation fails.', {'compiler_error': 'a label can only be part of a statement and a declaration is not a statement'}, {'stack': []})
        ]
    )

    # =========================================================================
    # TOPIC_LOOPS (Q051 - Q068)
    # =========================================================================
    # Q051: For Loop Iteration Bound
    add_q(
        51, 'TOPIC_LOOPS', 'Easy', 'For Loop Iteration Bound',
        'What is the output of the following program?',
        '#include <stdio.h>\nint main() {\n    int count = 0;\n    for (int i = 0; i < 5; i++) {\n        count++;\n    }\n    printf("%d\\n", count);\n    return 0;\n}',
        4, 'for (int i = 0; i < 5; i++)', 'i starts at 0 and increments while i < 5: it runs for i in {0, 1, 2, 3, 4}, executing EXACTLY 5 times!',
        [
            ('A', '4', False, 'Made an off-by-one error by counting 1 through 4 instead of 0 through 4.', 'Because the loop starts at index 0, the iterations are 0, 1, 2, 3, 4—which is 5 total iterations.'),
            ('B', '6', False, 'Thought the loop condition was i <= 5.', "The relational operator is strict '<', which terminates when i reaches 5."),
            ('C', '5', True, "A 0-indexed loop 'for (int i = 0; i < N; i++)' iterates exactly N times (0, 1, 2, 3, 4), resulting in count = 5.", ''),
            ('D', '0', False, 'Thought the loop body never executed.', 'Initial condition 0 < 5 is true, so the body executes.')
        ],
        'for (i = 0; i < 5; i++) executes for i in {0,1,2,3,4}, exactly 5 iterations.',
        'ISO/IEC 9899:1999 §6.8.5.3 (The for statement)',
        "The standard 0-indexed for-loop 'for (i = 0; i < N; i++)' is the quintessential idiom in C programming. Under ISO C99 §6.8.5.3:\n1. Clause-1: 'int i = 0' initializes 'i' to 0.\n2. Clause-2: 'i < 5' is evaluated before each iteration. If true, the body executes.\n3. Clause-3: 'i++' executes after each body execution.\n\nThe sequence of values for 'i' during body executions is:\nIteration 1: i = 0, count becomes 1\nIteration 2: i = 1, count becomes 2\nIteration 3: i = 2, count becomes 3\nIteration 4: i = 3, count becomes 4\nIteration 5: i = 4, count becomes 5\nThen i increments to 5; '5 < 5' is false (0), terminating the loop. 'count' is 5.",
        [
            (1, 3, 'Initialize count = 0 on stack.', {'count': 0}, {'stack': [{'name': 'count', 'type': 'int', 'address': '0x7ffd10', 'value': '0'}]}),
            (2, 4, 'Loop runs for i = 0, 1, 2, 3, 4; count increments each time from 0 up to 5.', {'i': 5, 'count': 5}, {'stack': [{'name': 'count', 'type': 'int', 'address': '0x7ffd10', 'value': '5'}, {'name': 'i', 'type': 'int', 'address': '0x7ffd14', 'value': '5'}]}),
            (3, 7, "Loop terminates (5 < 5 is false); printf prints '5\n'.", {'stdout': '5'}, {'stack': [{'name': 'count', 'type': 'int', 'address': '0x7ffd10', 'value': '5'}]})
        ]
    )

    # Q052: Accidental Semicolon After for-Loop Header
    add_q(
        52, 'TOPIC_LOOPS', 'Medium', 'Accidental Semicolon After for-Loop Header',
        'What is the output of the following program?',
        '#include <stdio.h>\nint main() {\n    int i;\n    for (i = 0; i < 5; i++);\n    printf("%d\\n", i);\n    return 0;\n}',
        4, 'for (i = 0; i < 5; i++);', 'The semicolon at the end of the for header makes the loop body an EMPTY NULL STATEMENT! The loop spins until i=5, then printf runs ONCE with i=5!',
        [
            ('A', '0 1 2 3 4', False, 'Thought printf was the body of the loop.', "The semicolon ';' after the for-header forms an empty loop body. printf is not inside the loop and executes only once."),
            ('B', '4', False, 'Thought i stopped at the last valid index 4.', 'For the loop condition i < 5 to become false, i must increment to 5.'),
            ('C', 'Compile error', False, 'Thought a semicolon immediately after for(...) is illegal syntax.', 'A semicolon is a valid null statement (§6.8.3); the compiler accepts it.'),
            ('D', '5', True, 'The semicolon terminates the loop body as a null statement. The loop runs 5 times doing nothing; after termination, i equals 5.', '')
        ],
        "The for-loop body is the null statement ';'. It loops until i = 5, then prints 5.",
        'ISO/IEC 9899:1999 §6.8.3 & §6.8.5.3 (For loop with null statement)',
        'In C, a loop construct controls exactly one statement. A single semicolon \';\' represents an empty null statement (§6.8.3).\n\nIn \'for (i = 0; i < 5; i++);\', the loop body is the null statement. The processor executes:\ni = 0; while (i < 5) { /* nothing */ i++; }\n\nThe variable \'i\' iterates through 0, 1, 2, 3, 4. At the end of the 5th iteration, \'i++\' increments \'i\' to 5. The condition \'5 < 5\' evaluates to false, and the loop exits.\n\nControl then passes to the subsequent statement: \'printf("%d\n", i);\'. Since \'i\' is 5, it prints \'5\'. This is one of the most frustrating typos for beginners because the code compiles cleanly without errors.',
        [
            (1, 3, 'Declare int i on the stack.', {'i': 'uninitialized'}, {'stack': [{'name': 'i', 'type': 'int', 'address': '0x7ffd10', 'value': 'uninitialized'}]}),
            (2, 4, 'Loop with null body executes 5 times: i increments from 0 to 5; condition 5 < 5 fails.', {'i': 5}, {'stack': [{'name': 'i', 'type': 'int', 'address': '0x7ffd10', 'value': '5'}]}),
            (3, 5, "Execute printf after loop termination: prints '5\n'.", {'stdout': '5'}, {'stack': [{'name': 'i', 'type': 'int', 'address': '0x7ffd10', 'value': '5'}]})
        ]
    )

    # Q053: C99 For-Loop Variable Scope
    add_q(
        53, 'TOPIC_LOOPS', 'Medium', 'C99 For-Loop Variable Scope',
        'What happens when attempting to compile this program under C99/C11 standards?',
        '#include <stdio.h>\nint main() {\n    for (int i = 0; i < 5; i++) {\n        // do nothing\n    }\n    printf("%d\\n", i);\n    return 0;\n}',
        6, 'printf', 'In C99, variables declared inside the for-loop header (for (int i = ...)) have BLOCK SCOPE that ends when the loop terminates! Accessing i outside causes a compile error!',
        [
            ('A', '5', False, "Assumed 'i' remains in scope after the loop finishes with value 5.", 'In C99 (§6.8.5.3), loop header declarations are scoped strictly to the loop; i ceases to exist outside the loop.'),
            ('B', 'Compilation error', True, "Variables declared in the for-loop header have block scope restricted to the loop; 'i' is undeclared outside the loop.", ''),
            ('C', '4', False, "Assumed 'i' stopped at 4 and was accessible.", "'i' is not in scope outside the loop."),
            ('D', 'Undefined behavior', False, 'Thought it compiles but accesses an out-of-scope variable.', 'Undeclared identifiers are diagnosed at compile time by the compiler.')
        ],
        'Names declared in the for-loop header have block scope terminating at the end of the loop. Compile error.',
        'ISO/IEC 9899:1999 §6.8.5.3#1 (For-loop header variable block scope)',
        'C99 introduced the ability to declare variables directly inside the clause-1 of a for-loop: \'for (int i = 0; ...)\'.\n\nISO C99 §6.8.5.3#1 explicitly defines the scope of such variables:\n\'If clause-1 is a declaration, the scope of any identifier it declares in its declaration list shall be the remainder of the declaration and the entire loop, including the other two clauses; it is reached in the order of execution before the first evaluation of the controlling expression.\'\n\nThe loop body and the for statement itself constitute a single block scope (§6.2.1). Once the loop terminates, the block scope ends and the identifier \'i\' goes out of scope.\n\nAttempting to access \'i\' in the subsequent \'printf("%d\n", i);\' triggers a compile error: \'error: \'i\' undeclared (first use in this function)\'. To access \'i\' after the loop, it must be declared before the loop.',
        [
            (1, 3, "Compiler enters for-loop block scope; declares loop variable 'i' initialized to 0.", {'scope': 'for-loop block', 'i': 0}, {'stack': [{'name': 'i', 'type': 'int', 'address': '0x7ffd10', 'value': '0'}]}),
            (2, 5, "Loop finishes; for-loop block scope closes; identifier 'i' is destroyed.", {'scope': 'main block', 'i': 'out-of-scope'}, {'stack': []}),
            (3, 6, "Compiler encounters printf call: 'i' is undeclared in this scope -> compilation error.", {'compiler_error': "'i' undeclared (first use in this function)"}, {'stack': []})
        ]
    )

    # Q054: Postfix Decrement in While Condition
    add_q(
        54, 'TOPIC_LOOPS', 'Medium', 'Postfix Decrement in While Condition',
        'What is the output of the following program?',
        '#include <stdio.h>\nint main() {\n    int x = 3;\n    while (x-- > 0) {\n        printf("%d ", x);\n    }\n    printf("\\n");\n    return 0;\n}',
        4, 'while (x-- > 0)', 'x-- tests the value BEFORE decrementing, but decrements BEFORE entering the body! When x is 3, condition tests 3 > 0 (true), then x becomes 2 inside body!',
        [
            ('A', '2 1 0 ', True, 'Postfix x-- > 0 tests the unincremented value against 0, but decrements x before the loop body executes, printing 2, 1, 0.', ''),
            ('B', '3 2 1 ', False, 'Assumed x was not decremented until the end of the loop body.', 'The side effect of postfix decrement completes at the sequence point at the end of the while condition, before the body executes.'),
            ('C', '3 2 1 0 ', False, 'Thought x printed its initial value and also printed 0.', 'x is decremented to 2 before the first printf.'),
            ('D', '2 1 ', False, 'Thought the loop stopped when x reached 0 before printing.', 'When x=1, 1 > 0 is true, x decrements to 0, and 0 is printed.')
        ],
        'The condition tests value before decrement, then decrements before body. 3 tests true -> body sees 2, then 1, then 0.',
        'ISO/IEC 9899:1999 §6.5.2.4 & §6.8.5.1 (While condition sequence point)',
        "In 'while (x-- > 0)':\nThere is a sequence point after the complete evaluation of the controlling expression (ISO C99 §6.8.5.1). This means all side effects of the condition—including the decrement of 'x'—are fully applied before the first statement of the loop body executes.\n\nStep-by-step trace starting with x = 3:\n1. Condition 1: 'x-- > 0'. Postfix yields 3. 3 > 0 is TRUE. Side effect sets x = 2.\n   Body executes: prints '2 '.\n2. Condition 2: 'x-- > 0'. Postfix yields 2. 2 > 0 is TRUE. Side effect sets x = 1.\n   Body executes: prints '1 '.\n3. Condition 3: 'x-- > 0'. Postfix yields 1. 1 > 0 is TRUE. Side effect sets x = 0.\n   Body executes: prints '0 '.\n4. Condition 4: 'x-- > 0'. Postfix yields 0. 0 > 0 is FALSE. Side effect sets x = -1.\n   Loop exits.\nTotal output: '2 1 0 '.",
        [
            (1, 3, 'Initialize int x = 3 on stack.', {'x': 3}, {'stack': [{'name': 'x', 'type': 'int', 'address': '0x7ffd10', 'value': '3'}]}),
            (2, 4, "Iter 1: condition tests 3 > 0 (true); x decrements to 2; body prints '2 '.", {'x': 2, 'stdout': '2 '}, {'stack': [{'name': 'x', 'type': 'int', 'address': '0x7ffd10', 'value': '2'}]}),
            (3, 4, "Iter 2: condition tests 2 > 0 (true); x decrements to 1; body prints '1 '.", {'x': 1, 'stdout': '2 1 '}, {'stack': [{'name': 'x', 'type': 'int', 'address': '0x7ffd10', 'value': '1'}]}),
            (4, 4, "Iter 3: condition tests 1 > 0 (true); x decrements to 0; body prints '0 '.", {'x': 0, 'stdout': '2 1 0 '}, {'stack': [{'name': 'x', 'type': 'int', 'address': '0x7ffd10', 'value': '0'}]}),
            (5, 4, 'Iter 4: condition tests 0 > 0 (false); x decrements to -1; loop terminates.', {'x': -1, 'stdout': '2 1 0 '}, {'stack': [{'name': 'x', 'type': 'int', 'address': '0x7ffd10', 'value': '-1'}]})
        ]
    )

    # Q055: Prefix Decrement in While Condition
    add_q(
        55, 'TOPIC_LOOPS', 'Medium', 'Prefix Decrement in While Condition',
        'What is the output of the following program?',
        '#include <stdio.h>\nint main() {\n    int x = 3;\n    while (--x > 0) {\n        printf("%d ", x);\n    }\n    printf("\\n");\n    return 0;\n}',
        4, 'while (--x > 0)', '--x decrements BEFORE the condition check! When x is 1, --x makes it 0, which fails 0 > 0 immediately, stopping before printing 0!',
        [
            ('A', '2 1 0 ', False, 'Confused prefix --x with postfix x--.', 'With prefix --x, when x is 1, it decrements to 0 first; 0 > 0 is false, so 0 is never printed.'),
            ('B', '3 2 1 ', False, 'Assumed x was not decremented before entering the loop.', 'Prefix -- decrements before evaluating the condition.'),
            ('C', '2 1 ', True, 'Prefix --x decrements x first, then tests the decremented value against 0. When x decrements to 0, 0 > 0 is false, so only 2 and 1 are printed.', ''),
            ('D', '3 2 1 0 ', False, 'Thought loop ran 4 times.', 'Initial decrement produces 2, not 3.')
        ],
        '--x decrements x, then yields the decremented value for comparison. Prints 2 1 .',
        'ISO/IEC 9899:1999 §6.5.3.1 & §6.8.5.1 (Prefix decrement in while)',
        "Contrasting with Q054, here the prefix decrement operator '--x' is used. Under ISO C99 §6.5.3.1, the operand is decremented first, and the value of the expression is the new decremented value.\n\nStarting with x = 3:\n1. Iteration 1:\n   - '--x' decrements 'x' from 3 to 2.\n   - Condition evaluates: '2 > 0' is TRUE.\n   - Body prints '2 '.\n2. Iteration 2:\n   - '--x' decrements 'x' from 2 to 1.\n   - Condition evaluates: '1 > 0' is TRUE.\n   - Body prints '1 '.\n3. Iteration 3:\n   - '--x' decrements 'x' from 1 to 0.\n   - Condition evaluates: '0 > 0' is FALSE (0).\n   - Loop exits immediately without entering the body.\n\nThe final printed output is '2 1 '.",
        [
            (1, 3, 'Initialize int x = 3 on stack.', {'x': 3}, {'stack': [{'name': 'x', 'type': 'int', 'address': '0x7ffd10', 'value': '3'}]}),
            (2, 4, "Iter 1: prefix --x decrements x to 2; tests 2 > 0 (true); body prints '2 '.", {'x': 2, 'stdout': '2 '}, {'stack': [{'name': 'x', 'type': 'int', 'address': '0x7ffd10', 'value': '2'}]}),
            (3, 4, "Iter 2: prefix --x decrements x to 1; tests 1 > 0 (true); body prints '1 '.", {'x': 1, 'stdout': '2 1 '}, {'stack': [{'name': 'x', 'type': 'int', 'address': '0x7ffd10', 'value': '1'}]}),
            (4, 4, 'Iter 3: prefix --x decrements x to 0; tests 0 > 0 (false); loop terminates.', {'x': 0, 'stdout': '2 1 '}, {'stack': [{'name': 'x', 'type': 'int', 'address': '0x7ffd10', 'value': '0'}]})
        ]
    )

    # Q056: Do-While Minimum Execution Guarantee
    add_q(
        56, 'TOPIC_LOOPS', 'Easy', 'Do-While Minimum Execution Guarantee',
        'What is the output of the following program?',
        '#include <stdio.h>\nint main() {\n    int x = 10;\n    do {\n        printf("%d\\n", x);\n        x++;\n    } while (x < 5);\n    return 0;\n}',
        7, '} while (x < 5);', 'do-while loops test their condition at the END of the loop! The body is GUARANTEED to execute at least ONCE even if the condition is false!',
        [
            ('A', 'No output', False, 'Confused do-while with while loop (assuming pre-test skipped the body because 10 < 5 is false).', 'do-while is a post-tested loop; the condition is not evaluated until after the first pass through the body.'),
            ('B', '10 11', False, 'Thought the loop executed twice.', 'After printing 10, x becomes 11; 11 < 5 is false, terminating the loop after 1 iteration.'),
            ('C', 'Compile error', False, 'Thought x < 5 being false at start is rejected by the compiler.', 'Loop conditions are evaluated dynamically at runtime.'),
            ('D', '10', True, 'A do-while loop evaluates its controlling expression after the body executes. It executes at least once, printing 10, then 11 < 5 terminates.', '')
        ],
        'The controlling expression of a do statement is evaluated after each execution of the body, guaranteeing >= 1 run.',
        'ISO/IEC 9899:1999 §6.8.5.2 (The do statement)',
        'Unlike \'while\' and \'for\' loops which are pre-tested, the \'do-while\' loop is post-tested (ISO C99 §6.8.5.2):\n\'The controlling expression of a do statement is evaluated after each execution of the loop body.\'\n\nBecause the test is at the bottom:\n1. \'x\' is initialized to 10.\n2. Control enters the loop body unconditionally.\n3. \'printf("%d\n", x)\' prints 10.\n4. \'x++\' increments \'x\' to 11.\n5. The condition \'while (x < 5)\' is evaluated: \'11 < 5\' is false (0).\n6. The loop terminates.\n\nThus, a do-while loop is mathematically guaranteed to execute its body at least once, regardless of the initial truth value of the controlling expression.',
        [
            (1, 3, 'Initialize int x = 10 on the stack.', {'x': 10}, {'stack': [{'name': 'x', 'type': 'int', 'address': '0x7ffd10', 'value': '10'}]}),
            (2, 4, "Enter do-while body unconditionally: printf prints '10\n'; x increments to 11.", {'x': 11, 'stdout': '10'}, {'stack': [{'name': 'x', 'type': 'int', 'address': '0x7ffd10', 'value': '11'}]}),
            (3, 6, 'Evaluate post-condition while (x < 5): 11 < 5 is false (0); loop terminates.', {'condition': 0}, {'stack': [{'name': 'x', 'type': 'int', 'address': '0x7ffd10', 'value': '11'}]})
        ]
    )

    # Q057: Do-While Trailing Semicolon Requirement
    add_q(
        57, 'TOPIC_LOOPS', 'Easy', 'Do-While Trailing Semicolon Requirement',
        'What happens when attempting to compile this program?',
        '#include <stdio.h>\nint main() {\n    int x = 0;\n    do {\n        x++;\n    } while (x < 3)\n    printf("%d\\n", x);\n    return 0;\n}',
        6, '} while (x < 3)', 'The do-while loop syntax MANDATES a trailing semicolon after while(...);! Omitting the semicolon causes a syntax error!',
        [
            ('A', 'Compilation error', True, "The grammar for a do-while loop strictly requires a terminating semicolon: 'do statement while ( expression ) ;'. Omitting it is a syntax error.", ''),
            ('B', '3', False, 'Assumed the compiler infers the semicolon before printf.', 'C grammar does not feature automatic semicolon insertion like JavaScript; the trailing semicolon is grammatically mandatory.'),
            ('C', '0', False, 'Thought the loop was bypassed.', 'The code cannot be compiled or executed.'),
            ('D', 'Undefined behavior', False, 'Thought missing punctuation causes undefined behavior.', 'Syntax errors are diagnosed and rejected by the compiler at compile time.')
        ],
        'The syntax for a do-while loop is: do statement while ( expr ) ;. Missing semicolon is a syntax error.',
        'ISO/IEC 9899:1999 §6.8.5.2 (The do statement - syntax)',
        "In ISO C99 §6.8.5, the grammar for iteration statements is specified as:\niteration-statement:\n    while ( expression ) statement\n    do statement while ( expression ) ;\n    for ( expression_opt ; expression_opt ; expression_opt ) statement\n\nNotice the explicit semicolon ';' at the end of the do-while production. Unlike while or for loops which end with a statement/block, a do-while loop ends with the parenthesized expression 'while ( expression )' and MUST be terminated by a semicolon.\n\nBecause line 6 lacks the semicolon, the parser cannot determine where the iteration statement ends and encounters 'printf' unexpectedly, emitting: 'error: expected ';' before 'printf''. This is a classic syntax check on introductory exams.",
        [
            (1, 4, "Compiler parses 'do {' and parses loop body block '{ x++; }'.", {'state': 'do-body parsed'}, {'stack': []}),
            (2, 6, "Parser expects closing ';' after 'while (x < 3)', but finds identifier 'printf'.", {'token_found': 'printf', 'expected': ';'}, {'stack': []}),
            (3, 6, "Grammar error (§6.8.5.2): compilation fails with 'expected ';' before 'printf''.", {'compiler_error': "expected ';' before 'printf'"}, {'stack': []})
        ]
    )

    # Q058: Break Exiting Innermost Loop Only
    add_q(
        58, 'TOPIC_LOOPS', 'Medium', 'Break Exiting Innermost Loop Only',
        'What is the output of the following program?',
        '#include <stdio.h>\nint main() {\n    for (int i = 0; i < 2; i++) {\n        for (int j = 0; j < 3; j++) {\n            if (j == 1) break;\n            printf("%d%d ", i, j);\n        }\n    }\n    printf("\\n");\n    return 0;\n}',
        5, 'if (j == 1) break;', 'A break statement terminates ONLY the innermost enclosing loop! The outer loop continues running!',
        [
            ('A', '00 ', False, 'Assumed break broke out of BOTH loops entirely.', 'In C, break only exits the innermost enclosing loop statement; it does not break multi-level loops.'),
            ('B', '00 10 ', True, 'A break statement terminates only the smallest enclosing loop (the inner j loop). The outer i loop continues, printing 00 for i=0 and 10 for i=1.', ''),
            ('C', '00 01 10 11 ', False, 'Thought break only skipped one iteration like continue.', 'break completely terminates the inner loop for that iteration of the outer loop.'),
            ('D', '00 01 02 10 11 12 ', False, 'Thought break had no effect.', 'When j reaches 1, the inner loop terminates immediately.')
        ],
        'A break statement terminates execution of the smallest enclosing switch or loop. Breaks inner loop only.',
        'ISO/IEC 9899:1999 §6.8.6.3 (The break statement)',
        "Under ISO C99 §6.8.6.3#2:\n'A break statement terminates execution of the smallest enclosing switch or iteration statement.'\n\nIn nested loops:\n1. Outer loop i = 0:\n   - j = 0: 'j == 1' is false; prints '00 '.\n   - j = 1: 'j == 1' is true; 'break' executes, terminating the inner j-loop immediately.\n2. Outer loop advances to i = 1:\n   - j = 0: 'j == 1' is false; prints '10 '.\n   - j = 1: 'j == 1' is true; 'break' executes, terminating the inner j-loop.\n3. Outer loop finishes.\n\nTotal printed output is '00 10 '. To break out of nested loops simultaneously in C, one must use a 'goto' to an outer label or set a boolean flag variable.",
        [
            (1, 3, 'Outer loop i = 0: inner loop begins with j = 0.', {'i': 0, 'j': 0}, {'stack': [{'name': 'i', 'type': 'int', 'address': '0x7ffd10', 'value': '0'}, {'name': 'j', 'type': 'int', 'address': '0x7ffd14', 'value': '0'}]}),
            (2, 6, "i = 0, j = 0: printf prints '00 '. j increments to 1.", {'stdout': '00 '}, {'stack': [{'name': 'i', 'type': 'int', 'address': '0x7ffd10', 'value': '0'}, {'name': 'j', 'type': 'int', 'address': '0x7ffd14', 'value': '1'}]}),
            (3, 5, 'i = 0, j = 1: if (j == 1) break executes; inner loop terminates. Outer loop advances to i = 1.', {'i': 1, 'j': 0}, {'stack': [{'name': 'i', 'type': 'int', 'address': '0x7ffd10', 'value': '1'}, {'name': 'j', 'type': 'int', 'address': '0x7ffd14', 'value': '0'}]}),
            (4, 6, "i = 1, j = 0: printf prints '10 '. j increments to 1; break terminates inner loop. Total: '00 10 '.", {'stdout': '00 10 '}, {'stack': [{'name': 'i', 'type': 'int', 'address': '0x7ffd10', 'value': '1'}]})
        ]
    )

    # Q059: Continue Skipping to Update Expression
    add_q(
        59, 'TOPIC_LOOPS', 'Easy', 'Continue Skipping to Update Expression',
        'What is the output of the following program?',
        '#include <stdio.h>\nint main() {\n    for (int i = 0; i < 4; i++) {\n        if (i == 2) continue;\n        printf("%d ", i);\n    }\n    printf("\\n");\n    return 0;\n}',
        4, 'if (i == 2) continue;', 'In a for-loop, continue skips the rest of the body and jumps DIRECTLY to the update expression (i++)! Only i=2 is skipped!',
        [
            ('A', '0 1 ', False, 'Confused continue with break (assuming the loop terminated when i == 2).', 'break exits the loop, whereas continue merely skips the remainder of the current iteration.'),
            ('B', '0 1 2 3 ', False, 'Thought continue had no effect.', 'When i == 2, continue skips the printf statement entirely.'),
            ('C', 'Infinite loop', False, 'Thought i was not incremented when continue executed.', 'In a for-loop, continue explicitly jumps to clause-3 (i++), so i increments normally.'),
            ('D', '0 1 3 ', True, "In a for loop, 'continue' bypasses the remainder of the body and jumps directly to the increment clause (i++). Iteration 2 is skipped.", '')
        ],
        'In a for statement, continue causes the loop continuation portion (clause-3) to be evaluated. Skips 2, prints 0 1 3.',
        'ISO/IEC 9899:1999 §6.8.6.2 (The continue statement - for loop behavior)',
        "ISO C99 §6.8.6.2 specifies that a 'continue' statement terminates execution of the current iteration of the innermost enclosing loop.\n\nCrucially, in a 'for' loop, continue transfers control directly to the loop continuation portion (clause-3, here 'i++'):\n1. i = 0: prints '0 '.\n2. i = 1: prints '1 '.\n3. i = 2: 'if (i == 2) continue;' executes. The printf on line 5 is skipped, and control jumps directly to 'i++'.\n4. 'i++' increments 'i' to 3.\n5. i = 3: prints '3 '.\n6. 'i++' increments 'i' to 4; '4 < 4' is false, and the loop exits.\nThe output is '0 1 3 '.",
        [
            (1, 3, "Start loop at i = 0; prints '0 '; i increments to 1; prints '1 '.", {'i': 1, 'stdout': '0 1 '}, {'stack': [{'name': 'i', 'type': 'int', 'address': '0x7ffd10', 'value': '1'}]}),
            (2, 4, 'Iteration i = 2: if (i == 2) continue executes; jumps directly to i++; printf is skipped.', {'i': 2, 'stdout': '0 1 '}, {'stack': [{'name': 'i', 'type': 'int', 'address': '0x7ffd10', 'value': '2'}]}),
            (3, 4, "Iteration i = 3: prints '3 '. i increments to 4; 4 < 4 terminates loop. Output: '0 1 3 '.", {'i': 4, 'stdout': '0 1 3 '}, {'stack': [{'name': 'i', 'type': 'int', 'address': '0x7ffd10', 'value': '4'}]})
        ]
    )

    # Q060: Continue Skipping While Loop Increment
    add_q(
        60, 'TOPIC_LOOPS', 'Tricky', 'Continue Skipping While Loop Increment',
        'What happens when this program is executed?',
        '#include <stdio.h>\nint main() {\n    int i = 0;\n    while (i < 3) {\n        if (i == 1) continue;\n        printf("%d ", i);\n        i++;\n    }\n    return 0;\n}',
        5, 'if (i == 1) continue;', 'In a WHILE loop, continue jumps to the condition check! The increment i++ is SKIPPED, leaving i stuck at 1 forever in an INFINITE LOOP!',
        [
            ('A', '0 2 ', False, 'Assumed i was somehow incremented when continue executed.', 'Unlike for loops, while loops have no automatic update clause. Skipping i++ leaves i at 1 forever.'),
            ('B', '0 1 2 ', False, 'Thought continue did not skip anything.', 'When i == 1, continue skips printf and i++.'),
            ('C', 'Infinite loop (prints 0 then hangs)', True, 'In a while loop, continue jumps to the condition check; because the increment i++ is in the body below continue, i remains 1 forever.', ''),
            ('D', '0 ', False, 'Thought the program terminated after printing 0.', 'The while loop condition 1 < 3 remains true forever; it does not terminate.')
        ],
        'In a while statement, continue passes control directly to the condition. Because i++ is skipped, i remains 1 forever.',
        'ISO/IEC 9899:1999 §6.8.6.2 (The continue statement - while loop behavior)',
        "A critical difference between 'for' and 'while' loops in C is how 'continue' interacts with loop increments:\n- In a 'for' loop, 'continue' jumps to the update clause (clause-3).\n- In a 'while' loop, 'continue' jumps directly to the controlling expression (§6.8.6.2).\n\nTrace:\n1. i = 0: 'i == 1' is false; prints '0 '; 'i++' updates i to 1.\n2. i = 1: 'i < 3' is true. 'if (i == 1) continue;' executes!\n3. Control jumps directly to 'while (i < 3)'.\n4. Notice that 'i++' on line 7 was skipped!\n5. In the next check, 'i' is STILL 1.\n6. '1 < 3' is true; 'if (i == 1) continue;' executes again.\n7. This cycle repeats indefinitely: the program hangs in an infinite loop, having printed only '0 '.",
        [
            (1, 3, 'Initialize int i = 0 on stack.', {'i': 0}, {'stack': [{'name': 'i', 'type': 'int', 'address': '0x7ffd10', 'value': '0'}]}),
            (2, 4, "Iteration 1: i = 0; prints '0 '; i increments to 1.", {'i': 1, 'stdout': '0 '}, {'stack': [{'name': 'i', 'type': 'int', 'address': '0x7ffd10', 'value': '1'}]}),
            (3, 5, 'Iteration 2: i = 1; if (i == 1) continue jumps to while condition, skipping i++.', {'i': 1, 'stdout': '0 '}, {'stack': [{'name': 'i', 'type': 'int', 'address': '0x7ffd10', 'value': '1'}]}),
            (4, 4, 'i is still 1; while(1 < 3) is true; continue runs again -> Infinite loop.', {'i': 1, 'state': 'infinite loop'}, {'stack': [{'name': 'i', 'type': 'int', 'address': '0x7ffd10', 'value': '1'}]})
        ]
    )

    # Q061: Nested Loop Total Iteration Count
    add_q(
        61, 'TOPIC_LOOPS', 'Easy', 'Nested Loop Total Iteration Count',
        'What is the value of total printed by this program?',
        '#include <stdio.h>\nint main() {\n    int total = 0;\n    for (int i = 0; i < 3; i++) {\n        for (int j = 0; j < 4; j++) {\n            total++;\n        }\n    }\n    printf("%d\\n", total);\n    return 0;\n}',
        5, 'for (int j = 0; j < 4; j++)', 'Nested loops multiply! Outer loop runs 3 times; for each pass, inner loop runs 4 times: 3 * 4 = 12 total iterations!',
        [
            ('A', '12', True, 'Nested loops multiply their iteration counts: outer loop runs 3 times, inner loop runs 4 times per outer pass -> 3 * 4 = 12.', ''),
            ('B', '7', False, 'Added the loop bounds (3 + 4 = 7) instead of multiplying.', 'Nested loops execute multiplicatively, not additively: for each of the 3 outer passes, the inner loop executes 4 times.'),
            ('C', '9', False, 'Calculated 3 * 3.', 'The inner loop runs for j = 0, 1, 2, 3 (4 iterations).'),
            ('D', '16', False, 'Calculated 4 * 4.', 'The outer loop runs for i = 0, 1, 2 (3 iterations).')
        ],
        'Multiplicative property of nested loops: N_outer * N_inner = 3 * 4 = 12 total iterations.',
        'ISO/IEC 9899:1999 §6.8.5 (Iteration statements - nesting)',
        "Nested loops follow the fundamental counting principle: if an outer loop executes N times, and for each iteration of the outer loop an inner loop executes M times, the inner loop body executes N * M times in total.\n\nHere:\n- Outer loop 'for (int i = 0; i < 3; i++)' iterates for i in {0, 1, 2} (3 iterations).\n- Inner loop 'for (int j = 0; j < 4; j++)' iterates for j in {0, 1, 2, 3} (4 iterations).\nTotal executions of 'total++' = 3 * 4 = 12.\nprintf prints '12'.",
        [
            (1, 3, 'Initialize total = 0 on stack.', {'total': 0}, {'stack': [{'name': 'total', 'type': 'int', 'address': '0x7ffd10', 'value': '0'}]}),
            (2, 4, 'Outer loop i = 0: inner loop j runs 4 times (total becomes 4).', {'i': 0, 'total': 4}, {'stack': [{'name': 'total', 'type': 'int', 'address': '0x7ffd10', 'value': '4'}]}),
            (3, 4, 'Outer loop i = 1: inner loop j runs 4 times (total becomes 8).', {'i': 1, 'total': 8}, {'stack': [{'name': 'total', 'type': 'int', 'address': '0x7ffd10', 'value': '8'}]}),
            (4, 4, 'Outer loop i = 2: inner loop j runs 4 times (total becomes 12). Loop completes.', {'i': 2, 'total': 12}, {'stack': [{'name': 'total', 'type': 'int', 'address': '0x7ffd10', 'value': '12'}]}),
            (5, 9, "printf prints '12\n'.", {'stdout': '12'}, {'stack': [{'name': 'total', 'type': 'int', 'address': '0x7ffd10', 'value': '12'}]})
        ]
    )

    # Q062: Unsigned Integer Non-Terminating Loop
    add_q(
        62, 'TOPIC_LOOPS', 'Tricky', 'Unsigned Integer Non-Terminating Loop',
        'What happens when executing this program?',
        '#include <stdio.h>\nint main() {\n    for (unsigned int i = 3; i >= 0; i--) {\n        printf("%u ", i);\n    }\n    return 0;\n}',
        3, 'i >= 0', 'Because i is UNSIGNED, i >= 0 is ALWAYS TRUE! When i reaches 0, 0 - 1 wraps to UINT_MAX (4,294,967,295), creating an INFINITE LOOP!',
        [
            ('A', 'Terminates after printing 3 2 1 0', False, 'Thought i decrements from 0 to -1, making -1 >= 0 false and terminating naturally.', 'Unsigned types cannot represent negative numbers. In C modular arithmetic, 0u - 1 wraps to UINT_MAX (4294967295), which is >= 0.'),
            ('B', 'Compilation error', False, 'Thought comparing unsigned int against 0 with >= is a syntax error.', 'The comparison is syntactically valid C; compilers may issue a warning like -Wtype-limits, but it compiles cleanly.'),
            ('C', 'Segmentation fault', False, 'Thought underflowing an integer causes a memory crash.', 'Integer underflow in unsigned types is well-defined modular arithmetic and never causes segmentation faults.'),
            ('D', 'Infinite loop (i is unsigned, so i >= 0 is always true and wraps to UINT_MAX)', True, 'Unsigned integers can never be negative; condition i >= 0 is a tautology (always true). When i = 0 decrements, it wraps to UINT_MAX.', '')
        ],
        'Unsigned integers represent non-negative values. i >= 0 is always true. 0 decrements to UINT_MAX -> infinite loop.',
        'ISO/IEC 9899:1999 §6.2.5#9 (Unsigned integer modulo arithmetic) & §6.8.5',
        "Under ISO C99 §6.2.5#9:\n'A computation involving unsigned operands can never overflow, because a result that cannot be represented by the resulting unsigned integer type is reduced modulo the number that is one greater than the largest value that can be represented by the resulting type.'\n\nFor a 32-bit unsigned int, the range of representable values is strictly [0, 4294967295].\nBecause all possible values of an unsigned int are greater than or equal to 0, the controlling expression 'i >= 0' is a tautology: it evaluates to 1 (true) for every possible value of 'i'.\n\nTrace:\n1. i = 3: prints '3 '.\n2. i = 2: prints '2 '.\n3. i = 1: prints '1 '.\n4. i = 0: prints '0 '.\n5. 'i--' executes: 0 - 1 wraps modulo 2^32 to UINT_MAX (4,294,967,295).\n6. '4294967295 >= 0' is still true!\n7. The loop continues printing indefinitely. This is a classic systems programming defect when replacing signed loop indices with unsigned size_t.",
        [
            (1, 3, 'Initialize unsigned int i = 3.', {'i': 3}, {'stack': [{'name': 'i', 'type': 'unsigned int', 'address': '0x7ffd10', 'value': '3'}]}),
            (2, 4, "Loop prints '3 2 1 0 '; i reaches 0.", {'i': 0, 'stdout': '3 2 1 0 '}, {'stack': [{'name': 'i', 'type': 'unsigned int', 'address': '0x7ffd10', 'value': '0'}]}),
            (3, 3, 'i-- executes at i = 0: unsigned underflow wraps to UINT_MAX (4294967295).', {'i': 4294967295}, {'stack': [{'name': 'i', 'type': 'unsigned int', 'address': '0x7ffd10', 'value': '4294967295'}]}),
            (4, 3, 'Condition 4294967295 >= 0 is true; loop never terminates (Infinite Loop).', {'state': 'infinite loop'}, {'stack': [{'name': 'i', 'type': 'unsigned int', 'address': '0x7ffd10', 'value': '4294967295'}]})
        ]
    )

    # Q063: Floating Point Equality in Loop Condition
    add_q(
        63, 'TOPIC_LOOPS', 'Tricky', 'Floating Point Equality in Loop Condition',
        "Why is 'while (f != 1.0f)' dangerous when incrementing f += 0.1f in C?",
        '#include <stdio.h>\nint main() {\n    float f = 0.0f;\n    while (f != 1.0f) {\n        f += 0.1f;\n    }\n    return 0;\n}',
        4, 'while (f != 1.0f)', '0.1f cannot be represented exactly in binary floating point! Accumulated roundoff error causes f to SKIP exact 1.0f, causing an INFINITE LOOP!',
        [
            ('A', 'Terminates after exactly 10 iterations', False, 'Assumed decimal arithmetic where 10 * 0.1 = 1.0 exactly.', 'Computers use base-2 binary floating point; 0.1 has an infinite repeating binary fraction and accumulates roundoff errors.'),
            ('B', 'Compilation error', False, 'Thought testing float equality with != is illegal syntax.', 'Comparing floating-point values with != is valid C syntax, but numerically hazardous.'),
            ('C', 'Infinite loop due to floating-point representation error skipping exact 1.0f', True, '0.1 cannot be represented exactly in IEEE 754 binary floating-point. Repeated addition accumulates roundoff error, so f skips exact 1.0f and loops forever.', ''),
            ('D', 'Terminates immediately', False, 'Thought 0.0f == 1.0f.', 'f starts at 0.0f and increments continuously.')
        ],
        'Never use exact equality (!= or ==) as termination conditions for floating-point loops. Roundoff causes infinite loop.',
        'ISO/IEC 9899:1999 §6.8.5 & IEC 60559 (IEEE 754 floating-point accuracy)',
        "In IEEE 754 single-precision floating point, numbers are stored as base-2 fractions. Just as 1/3 cannot be written as a finite decimal, decimal 0.1 is an infinite repeating fraction in binary:\n0.0001100110011001100110011..._2\n\nThe nearest 32-bit float value to 0.1 is approximately 0.100000001490116119384765625.\nWhen you repeatedly add this value:\nAfter 9 additions:  f ≈ 0.900000095\nAfter 10 additions: f ≈ 1.000000119\nBecause 1.000000119 != 1.000000000, the condition 'f != 1.0f' evaluates to TRUE!\n\nThe variable 'f' has hopped right over 1.0f without ever landing on it exactly. The loop runs indefinitely. This demonstrates the cardinal rule of numerical computing: never use exact equality (== or !=) on floating-point numbers; always use inequality bounds with an epsilon tolerance (e.g. 'while (f < 1.0f - EPSILON)').",
        [
            (1, 3, 'Initialize float f = 0.0f on the stack.', {'f': 0.0}, {'stack': [{'name': 'f', 'type': 'float', 'address': '0x7ffd10', 'value': '0.0f'}]}),
            (2, 5, 'After 9 additions: f accumulates rounding error to ~0.9000001.', {'f': 0.9000001}, {'stack': [{'name': 'f', 'type': 'float', 'address': '0x7ffd10', 'value': '0.9000001f'}]}),
            (3, 5, '10th addition: f becomes ~1.00000012, which is NOT EQUAL to 1.0f.', {'f': 1.00000012}, {'stack': [{'name': 'f', 'type': 'float', 'address': '0x7ffd10', 'value': '1.00000012f'}]}),
            (4, 4, 'Condition 1.00000012f != 1.0f is true; loop skips termination and runs infinitely.', {'state': 'infinite loop'}, {'stack': [{'name': 'f', 'type': 'float', 'address': '0x7ffd10', 'value': '1.00000012f'}]})
        ]
    )

    # Q064: Multiple Control Variables in For Loop
    add_q(
        64, 'TOPIC_LOOPS', 'Medium', 'Multiple Control Variables in For Loop',
        'What is the output of the following program?',
        '#include <stdio.h>\nint main() {\n    int i, j;\n    for (i = 0, j = 4; i < j; i++, j--) {\n        printf("%d%d ", i, j);\n    }\n    printf("\\n");\n    return 0;\n}',
        4, 'for (i = 0, j = 4; i < j; i++, j--)', 'i increases while j decreases until i and j cross at 2: prints 04 then 13!',
        [
            ('A', '04 13 22 ', False, 'Thought the termination condition was i <= j.', "The condition is strict inequality 'i < j'. When i=2 and j=2, 2 < 2 is false, so 22 is never printed."),
            ('B', '04 13 ', True, 'The loop initializes i=0, j=4. In pass 1: prints 04, then i=1, j=3. In pass 2: prints 13, then i=2, j=2. 2 < 2 is false, terminating the loop.', ''),
            ('C', '04 ', False, 'Thought the loop executed only once.', 'After i=1, j=3, 1 < 3 is true, so a second iteration executes.'),
            ('D', 'Compilation error', False, 'Thought multiple variables cannot be updated in a for-loop header.', 'The comma operator allows multiple initializations and updates in for headers.')
        ],
        'The comma operator allows multiple initializations and updates in for headers. Prints 04 13.',
        'ISO/IEC 9899:1999 §6.8.5.3 & §6.5.17 (Comma operator in for loop)',
        "C for loops allow complex expressions in clause-1 and clause-3 by utilizing the comma operator (§6.5.17).\n\nTrace of 'for (i = 0, j = 4; i < j; i++, j--)':\n1. Initialization: i is set to 0, j is set to 4.\n2. Iteration 1:\n   - Condition '0 < 4' is TRUE.\n   - Body prints '04 '.\n   - Update: 'i++' -> i = 1; 'j--' -> j = 3.\n3. Iteration 2:\n   - Condition '1 < 3' is TRUE.\n   - Body prints '13 '.\n   - Update: 'i++' -> i = 2; 'j--' -> j = 2.\n4. Iteration 3:\n   - Condition '2 < 2' is FALSE (0).\n   - Loop exits.\nOutput is '04 13 '.",
        [
            (1, 4, 'Initialize i = 0, j = 4 in for-loop header.', {'i': 0, 'j': 4}, {'stack': [{'name': 'i', 'type': 'int', 'address': '0x7ffd10', 'value': '0'}, {'name': 'j', 'type': 'int', 'address': '0x7ffd14', 'value': '4'}]}),
            (2, 5, "Iteration 1: 0 < 4 is true; prints '04 '; update clause: i becomes 1, j becomes 3.", {'i': 1, 'j': 3, 'stdout': '04 '}, {'stack': [{'name': 'i', 'type': 'int', 'address': '0x7ffd10', 'value': '1'}, {'name': 'j', 'type': 'int', 'address': '0x7ffd14', 'value': '3'}]}),
            (3, 5, "Iteration 2: 1 < 3 is true; prints '13 '; update clause: i becomes 2, j becomes 2.", {'i': 2, 'j': 2, 'stdout': '04 13 '}, {'stack': [{'name': 'i', 'type': 'int', 'address': '0x7ffd10', 'value': '2'}, {'name': 'j', 'type': 'int', 'address': '0x7ffd14', 'value': '2'}]}),
            (4, 4, "Condition check: 2 < 2 is false; loop terminates. Total output: '04 13 '.", {'stdout': '04 13 '}, {'stack': [{'name': 'i', 'type': 'int', 'address': '0x7ffd10', 'value': '2'}, {'name': 'j', 'type': 'int', 'address': '0x7ffd14', 'value': '2'}]})
        ]
    )

    # Q065: Omitting Clauses in For Loop Header
    add_q(
        65, 'TOPIC_LOOPS', 'Easy', 'Omitting Clauses in For Loop Header',
        'In C, what does a for-loop with all three expressions omitted, like for (;;), represent?',
        '#include <stdio.h>\nint main() {\n    int count = 0;\n    for (;;) {\n        count++;\n        if (count == 3) break;\n    }\n    printf("%d\\n", count);\n    return 0;\n}',
        4, 'for (;;)', 'In C, an omitted condition-2 in a for loop is treated as a constant non-zero value (TRUE), creating an infinite loop by default!',
        [
            ('A', 'A compilation error', False, 'Thought for-loops require all three expressions.', 'All three expressions in a C for-loop are optional; omitting them is valid standard C.'),
            ('B', 'A loop that executes zero times', False, 'Thought an omitted condition defaults to false.', 'The standard explicitly mandates that an omitted clause-2 is replaced with a non-zero constant (true).'),
            ('C', 'An infinite loop by default (clause-2 defaults to a non-zero constant true), unless terminated by break/return', True, 'ISO C §6.8.5.3 explicitly specifies that an omitted condition-2 in for(;;) is replaced by a constant non-zero value, running indefinitely unless broken.', ''),
            ('D', 'A loop that executes once', False, 'Thought omitting expressions causes a single pass.', 'Without a break statement, for(;;) iterates endlessly.')
        ],
        'Both clause-1 and clause-3 can be omitted; an omitted clause-2 is replaced by a nonzero constant true.',
        'ISO/IEC 9899:1999 §6.8.5.3#2 (The for statement - omitted expressions)',
        "Under ISO C99 §6.8.5.3#2:\n'An omitted expression-2 is replaced by a nonzero constant.'\n\nIn C, all three components of a for-loop header are optional:\n- Omitting clause-1 means no loop initialization is performed.\n- Omitting clause-2 replaces the test with a non-zero constant integer (1), meaning the condition is unconditionally true.\n- Omitting clause-3 means no post-iteration update expression is evaluated.\n\nTherefore, 'for (;;)' is identical to 'while (1)' in semantics and is widely considered the idiomatic C way to express an infinite loop. In this question's snippet, the loop is terminated intentionally after 3 iterations by 'if (count == 3) break;', printing 3.",
        [
            (1, 3, 'Initialize int count = 0 on the stack.', {'count': 0}, {'stack': [{'name': 'count', 'type': 'int', 'address': '0x7ffd10', 'value': '0'}]}),
            (2, 4, 'for(;;) begins: omitted clause-2 defaults to non-zero constant true (infinite loop).', {'condition': 1}, {'stack': [{'name': 'count', 'type': 'int', 'address': '0x7ffd10', 'value': '0'}]}),
            (3, 6, 'count increments across iterations (1, 2, 3); when count == 3, break executes.', {'count': 3}, {'stack': [{'name': 'count', 'type': 'int', 'address': '0x7ffd10', 'value': '3'}]}),
            (4, 8, "printf prints '3\n'.", {'stdout': '3'}, {'stack': [{'name': 'count', 'type': 'int', 'address': '0x7ffd10', 'value': '3'}]})
        ]
    )

    # Q066: While Loop False Initial Condition
    add_q(
        66, 'TOPIC_LOOPS', 'Easy', 'While Loop False Initial Condition',
        'How many times does this while loop execute its body?',
        '#include <stdio.h>\nint main() {\n    int x = 10;\n    while (x < 5) {\n        printf("RUN\\n");\n        x++;\n    }\n    return 0;\n}',
        4, 'while (x < 5)', 'A while loop tests its condition BEFORE entering the body! Since 10 < 5 is false, it executes ZERO times!',
        [
            ('A', '0 times (body is never entered)', True, 'A while loop is a pre-tested loop. Since the initial condition 10 < 5 is false (0), the body is skipped entirely.', ''),
            ('B', '1 time', False, 'Confused while loop with do-while loop.', 'A while loop tests before entering; unlike do-while, it does not guarantee a minimum of 1 execution.'),
            ('C', '5 times', False, 'Subtracted 10 - 5 = 5.', 'The body is never entered because 10 < 5 is false at the very first check.'),
            ('D', 'Infinite times', False, 'Assumed x was incremented indefinitely.', 'The condition evaluates to false immediately; nothing runs.')
        ],
        'A while loop tests the controlling expression before each execution of the body. 10 < 5 is false -> 0 runs.',
        'ISO/IEC 9899:1999 §6.8.5.1 (The while statement)',
        "Under ISO C99 §6.8.5.1:\n'The evaluation of the controlling expression takes place before each execution of the loop body.'\n\nExecution:\n1. 'x' is initialized to 10.\n2. The controlling expression 'x < 5' is evaluated: '10 < 5' is 0 (false).\n3. The body statement (the compound block) is completely bypassed.\n4. Program control jumps immediately to 'return 0;'.\n\nThe body executes zero times, and nothing is printed to stdout.",
        [
            (1, 3, 'Initialize int x = 10 on the stack.', {'x': 10}, {'stack': [{'name': 'x', 'type': 'int', 'address': '0x7ffd10', 'value': '10'}]}),
            (2, 4, 'Evaluate while condition (x < 5) -> (10 < 5) is false (0).', {'condition': 0}, {'stack': [{'name': 'x', 'type': 'int', 'address': '0x7ffd10', 'value': '10'}]}),
            (3, 8, 'Body is completely skipped; function returns 0. Total iterations: 0.', {'stdout': ''}, {'stack': [{'name': 'x', 'type': 'int', 'address': '0x7ffd10', 'value': '10'}]})
        ]
    )

    # Q067: Tracing Nested Loop Indices
    add_q(
        67, 'TOPIC_LOOPS', 'Medium', 'Tracing Nested Loop Indices',
        'What is the output of the following program?',
        '#include <stdio.h>\nint main() {\n    for (int i = 1; i <= 2; i++) {\n        for (int j = 1; j <= 2; j++) {\n            printf("%d ", i * j);\n        }\n    }\n    printf("\\n");\n    return 0;\n}',
        5, 'printf("%d ", i * j);', 'i=1: j=1 (1), j=2 (2). i=2: j=1 (2), j=2 (4). Outputs 1 2 2 4!',
        [
            ('A', '1 2 3 4 ', False, 'Assumed sequential numbers were printed without computing the multiplication.', '2 * 1 = 2, so the third printed number is 2, not 3.'),
            ('B', '2 4 ', False, 'Thought only the outer loop i = 2 was printed.', 'Both outer iterations (i = 1 and i = 2) execute fully.'),
            ('C', '1 4 ', False, 'Missed the off-diagonal products (1*2 and 2*1).', 'All 4 product pairs are computed and printed.'),
            ('D', '1 2 2 4 ', True, "Nested loops evaluate all pairs (i, j): (1,1)->1, (1,2)->2, (2,1)->2, (2,2)->4. Outputs '1 2 2 4 '.", '')
        ],
        'Nested loop execution: i=1 gives 1, 2; i=2 gives 2, 4. Prints 1 2 2 4.',
        'ISO/IEC 9899:1999 §6.8.5 (Nested iteration tracing)',
        "Tracing nested loops step by step:\nOuter loop variable 'i' runs for values 1 and 2:\n- When i = 1:\n  - Inner loop j = 1: i * j = 1 * 1 = 1. Prints '1 '.\n  - Inner loop j = 2: i * j = 1 * 2 = 2. Prints '2 '.\n- When i = 2:\n  - Inner loop j = 1: i * j = 2 * 1 = 2. Prints '2 '.\n  - Inner loop j = 2: i * j = 2 * 2 = 4. Prints '4 '.\n\nConcatenating the output produces '1 2 2 4 '.",
        [
            (1, 3, "Outer loop i = 1 begins: inner loop runs for j = 1 (prints '1 ') and j = 2 (prints '2 ').", {'i': 1, 'j': 2, 'stdout': '1 2 '}, {'stack': [{'name': 'i', 'type': 'int', 'address': '0x7ffd10', 'value': '1'}, {'name': 'j', 'type': 'int', 'address': '0x7ffd14', 'value': '2'}]}),
            (2, 3, "Outer loop i = 2 begins: inner loop runs for j = 1 (prints '2 ') and j = 2 (prints '4 ').", {'i': 2, 'j': 2, 'stdout': '1 2 2 4 '}, {'stack': [{'name': 'i', 'type': 'int', 'address': '0x7ffd10', 'value': '2'}, {'name': 'j', 'type': 'int', 'address': '0x7ffd14', 'value': '2'}]}),
            (3, 8, "Both loops complete; printf('\\n') outputs newline. Total output: '1 2 2 4 '.", {'stdout': '1 2 2 4 '}, {'stack': []})
        ]
    )

    # Q068: Comma Operator in Loop Termination Condition
    add_q(
        68, 'TOPIC_LOOPS', 'Tricky', 'Comma Operator in Loop Termination Condition',
        'What are the final values of i and j printed by this program?',
        '#include <stdio.h>\nint main() {\n    int i = 0, j = 0;\n    while (i < 2, j < 4) {\n        i++;\n        j++;\n    }\n    printf("%d %d\\n", i, j);\n    return 0;\n}',
        4, 'while (i < 2, j < 4)', 'The comma operator discards i < 2! The loop condition is governed EXCLUSIVELY by the rightmost expression j < 4!',
        [
            ('A', '2 2', False, 'Assumed comma acted like logical AND (&&), stopping when i reached 2.', 'The comma operator is NOT logical AND; it evaluates and discards i < 2 completely, leaving j < 4 as the sole controlling test.'),
            ('B', '4 4', True, 'The comma operator evaluates left-to-right and discards the left operand (i < 2). The condition is determined solely by j < 4, iterating 4 times.', ''),
            ('C', '2 4', False, 'Thought i stopped incrementing when i reached 2.', 'Both i++ and j++ are in the loop body and increment together on every iteration.'),
            ('D', 'Infinite loop', False, 'Thought comma in loop condition causes non-termination.', 'j reaches 4, making j < 4 false, so the loop terminates normally.')
        ],
        'The comma operator evaluates left-to-right and discards left result. j < 4 controls termination, printing 4 4.',
        'ISO/IEC 9899:1999 §6.5.17 (Comma operator in controlling expressions)',
        "In 'while (i < 2, j < 4)', the controlling expression contains the comma operator (§6.5.17).\n\nUnder ISO C99 §6.5.17:\n'The left operand of a comma operator is evaluated as a void expression; there is a sequence point after its evaluation. Then the right operand is evaluated; the result has its type and value.'\n\nTherefore:\n1. 'i < 2' is evaluated, and its result is completely discarded. It has zero effect on whether the loop continues or exits!\n2. 'j < 4' is evaluated, and its value alone determines whether the while body executes.\n\nBecause 'i' and 'j' start at 0 and increment together:\n- Iteration 1: i=1, j=1\n- Iteration 2: i=2, j=2\n- Iteration 3: i=3, j=3\n- Iteration 4: i=4, j=4\nNow 'j < 4' (4 < 4) evaluates to false (0), and the loop terminates.\nBoth variables hold 4, printing '4 4'.",
        [
            (1, 3, 'Initialize int i = 0, j = 0 on stack.', {'i': 0, 'j': 0}, {'stack': [{'name': 'i', 'type': 'int', 'address': '0x7ffd10', 'value': '0'}, {'name': 'j', 'type': 'int', 'address': '0x7ffd14', 'value': '0'}]}),
            (2, 4, 'Loop checks condition (i < 2, j < 4): i < 2 is discarded; j < 4 controls loop.', {'controlling_test': 'j < 4'}, {'stack': [{'name': 'i', 'type': 'int', 'address': '0x7ffd10', 'value': '0'}, {'name': 'j', 'type': 'int', 'address': '0x7ffd14', 'value': '0'}]}),
            (3, 5, 'Loop iterates 4 times: i and j both increment from 0 to 4.', {'i': 4, 'j': 4}, {'stack': [{'name': 'i', 'type': 'int', 'address': '0x7ffd10', 'value': '4'}, {'name': 'j', 'type': 'int', 'address': '0x7ffd14', 'value': '4'}]}),
            (4, 8, "Condition 4 < 4 is false; loop exits; printf prints '4 4\n'.", {'stdout': '4 4'}, {'stack': [{'name': 'i', 'type': 'int', 'address': '0x7ffd10', 'value': '4'}, {'name': 'j', 'type': 'int', 'address': '0x7ffd14', 'value': '4'}]})
        ]
    )

print("syllabus_part2 loaded (34 questions, total 68).")
