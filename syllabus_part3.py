# syllabus_part3.py
# Q069 - Q084: TOPIC_FUNCTIONS (Functions and Procedures)
# Q085 - Q100: TOPIC_ARRAYS (Arrays, 2D Arrays, Strings as Char Arrays)
# Pedagogically upgraded with balanced keys, verified GCC code, aligned traps,
# in-depth multi-paragraph deep dives, multi-step execution traces with memory snapshots,
# and rigorous distractor rationales.

def load_part3(add_q):
    # =========================================================================
    # TOPIC_FUNCTIONS (Q069 - Q084)
    # =========================================================================
    # Q069: Pass-by-Value Variable Modification
    add_q(
        69, 'TOPIC_FUNCTIONS', 'Easy', 'Pass-by-Value Variable Modification',
        'What is the output of the following program?',
        '#include <stdio.h>\nvoid modify(int x) {\n    x = 100;\n}\nint main() {\n    int a = 10;\n    modify(a);\n    printf("%d\\n", a);\n    return 0;\n}',
        3, 'x = 100;', "In C, arguments are passed BY VALUE! Parameter x is a separate local copy; modifying x does NOT modify variable 'a' in main!",
        [
            ('A', '10', True, "C functions receive arguments by value; parameter 'x' is a separate stack copy. Modifying 'x' leaves 'a' in main untouched at 10.", ''),
            ('B', '100', False, 'Assumed C passes variables by reference like Python lists or C++ reference parameters.', "C is strictly call-by-value. To modify 'a', its address (&a) must be explicitly passed to a pointer parameter."),
            ('C', '0', False, 'Thought modifying a failed variable zeroes it out.', "Variable 'a' retains its initialized value 10."),
            ('D', 'Compilation error', False, 'Thought modifying a parameter inside a void function is illegal.', 'Parameters behave as local variables and can be freely assigned inside the function.')
        ],
        'C uses call-by-value for function arguments. The called function receives copies in its own stack frame.',
        'ISO/IEC 9899:1999 §6.5.2.2#4 (Function calls - call-by-value semantics)',
        "In C, all function arguments are passed strictly by value (ISO C99 §6.5.2.2#4). When 'modify(a)' is invoked:\n1. The expression 'a' is evaluated to 10.\n2. A new stack frame is allocated for 'modify'.\n3. The parameter 'x' is initialized with a copy of 10.\n4. The statement 'x = 100;' modifies the local parameter 'x' in modify's stack frame.\n5. When 'modify' returns, its stack frame is popped from the call stack and destroyed.\n\nVariable 'a' in main's stack frame occupies a completely different memory address and remains unchanged at 10. To allow a function to modify a caller variable, C requires passing the address of the variable ('&a') to a pointer parameter ('int *x') and dereferencing it ('*x = 100').",
        [
            (1, 7, 'In main: allocate int a = 10 at address 0x7ffd10.', {'a': 10}, {'stack': [{'name': 'a (main)', 'type': 'int', 'address': '0x7ffd10', 'value': '10'}]}),
            (2, 8, 'Call modify(a): push stack frame for modify; parameter x allocated at 0x7ffd00 initialized with copy 10.', {'a': 10, 'x': 10}, {'stack': [{'name': 'a (main)', 'type': 'int', 'address': '0x7ffd10', 'value': '10'}, {'name': 'x (modify)', 'type': 'int', 'address': '0x7ffd00', 'value': '10'}]}),
            (3, 3, "Inside modify: x = 100 mutates local copy at 0x7ffd00. 'a' at 0x7ffd10 is unaffected.", {'x': 100, 'a': 10}, {'stack': [{'name': 'a (main)', 'type': 'int', 'address': '0x7ffd10', 'value': '10'}, {'name': 'x (modify)', 'type': 'int', 'address': '0x7ffd00', 'value': '100'}]}),
            (4, 9, "modify returns; stack frame popped; printf in main outputs '10\\n'.", {'stdout': '10'}, {'stack': [{'name': 'a (main)', 'type': 'int', 'address': '0x7ffd10', 'value': '10'}]})
        ]
    )

    # Q070: Failed Swap Implementation (Pass-by-Value)
    add_q(
        70, 'TOPIC_FUNCTIONS', 'Medium', 'Failed Swap Implementation (Pass-by-Value)',
        'What is the output of the following program?',
        '#include <stdio.h>\nvoid swap(int x, int y) {\n    int temp = x;\n    x = y;\n    y = temp;\n}\nint main() {\n    int a = 5, b = 10;\n    swap(a, b);\n    printf("%d %d\\n", a, b);\n    return 0;\n}',
        9, 'swap(a, b);', 'Because swap takes int parameters instead of int pointers (int *), it swaps local copies on its own stack! a and b in main are NOT swapped!',
        [
            ('A', '10 5', False, 'Assumed swap successfully swapped a and b in main.', 'C is call-by-value; swap received copies of 5 and 10. Swapping local parameters does not affect variables in main.'),
            ('B', '5 10', True, "Parameters x and y are local copies. The swap logic swaps only x and y in swap's stack frame; a and b in main remain 5 and 10.", ''),
            ('C', '10 10', False, 'Thought one assignment overwrote both.', 'Variables a and b in main were never modified.'),
            ('D', 'Compilation error', False, 'Thought swap was missing a return statement.', 'void functions do not require a return statement.')
        ],
        'Parameters x and y are local variables initialized with copies. Swapping them does not affect a and b in main.',
        'ISO/IEC 9899:1999 §6.5.2.2#4 & §6.2.4 (Storage duration and pass-by-value)',
        "The 'naive swap' is the universal pedagogical demonstration of call-by-value in computer science education.\n\nWhen 'swap(a, b)' executes:\n- A new activation record (stack frame) is created for 'swap'.\n- Memory is allocated for local parameter 'x' (initialized to 5), local parameter 'y' (initialized to 10), and local variable 'temp'.\n- The swap algorithm exchanges 'x' and 'y': x becomes 10, y becomes 5.\n- The function terminates, and its entire stack frame is discarded.\n\nBack in 'main()', variables 'a' and 'b' remain at their original stack addresses with their original values 5 and 10. For a swap function to work in C, pointers must be used: 'void swap(int *x, int *y)' called as 'swap(&a, &b)'.",
        [
            (1, 8, 'In main: int a = 5 (0x7ffd10), b = 10 (0x7ffd14) allocated on stack.', {'a': 5, 'b': 10}, {'stack': [{'name': 'a (main)', 'type': 'int', 'address': '0x7ffd10', 'value': '5'}, {'name': 'b (main)', 'type': 'int', 'address': '0x7ffd14', 'value': '10'}]}),
            (2, 9, 'Call swap(a, b): copies 5 and 10 pushed into parameters x (0x7ffd00) and y (0x7ffd04).', {'x': 5, 'y': 10}, {'stack': [{'name': 'a (main)', 'type': 'int', 'address': '0x7ffd10', 'value': '5'}, {'name': 'b (main)', 'type': 'int', 'address': '0x7ffd14', 'value': '10'}, {'name': 'x (swap)', 'type': 'int', 'address': '0x7ffd00', 'value': '5'}, {'name': 'y (swap)', 'type': 'int', 'address': '0x7ffd04', 'value': '10'}]}),
            (3, 4, "Inside swap: x and y are exchanged (x=10, y=5). main's 'a' and 'b' remain untouched.", {'x': 10, 'y': 5, 'a': 5, 'b': 10}, {'stack': [{'name': 'a (main)', 'type': 'int', 'address': '0x7ffd10', 'value': '5'}, {'name': 'b (main)', 'type': 'int', 'address': '0x7ffd14', 'value': '10'}, {'name': 'x (swap)', 'type': 'int', 'address': '0x7ffd00', 'value': '10'}, {'name': 'y (swap)', 'type': 'int', 'address': '0x7ffd04', 'value': '5'}]}),
            (4, 10, "swap returns; stack frame popped; printf in main outputs '5 10\\n'.", {'stdout': '5 10'}, {'stack': [{'name': 'a (main)', 'type': 'int', 'address': '0x7ffd10', 'value': '5'}, {'name': 'b (main)', 'type': 'int', 'address': '0x7ffd14', 'value': '10'}]})
        ]
    )

    # Q071: Function Prototype Declaration Necessity
    add_q(
        71, 'TOPIC_FUNCTIONS', 'Medium', 'Function Prototype Declaration Necessity',
        "What is the purpose of the prototype 'int add(int, int);' before main()?",
        'int add(int, int);\n#include <stdio.h>\nint main() {\n    int res = add(3, 4);\n    printf("%d\\n", res);\n    return 0;\n}\nint add(int a, int b) {\n    return a + b;\n}',
        1, 'int add(int, int);', "In C, a function prototype informs the compiler of the function's name, return type, and parameter types BEFORE it is called!",
        [
            ('A', "To allocate memory for add's variables", False, 'Thought declaring a prototype reserves stack memory.', 'Prototypes are declarations, not definitions; they emit no code and allocate zero memory.'),
            ('B', 'To execute add before main runs', False, 'Confused declaration with execution.', 'Execution in C always starts at main(); declarations merely inform the compiler.'),
            ('C', "To inform the compiler of add's signature (return type and parameter types) before its call site", True, 'A prototype declares the function interface to the compiler, enabling compile-time type checking and argument conversions before the function body is defined.', ''),
            ('D', 'It is purely optional and has no effect on compilation', False, 'Assumed C compilers do not need prototypes.', 'In modern C (C99/C11), calling a function without a prior declaration is deprecated or an error; prototypes enforce type safety.')
        ],
        'A function prototype declares the return type and parameter types to the compiler before its first use.',
        'ISO/IEC 9899:1999 §6.7.5.3 (Function declarators - prototypes) & §6.5.2.2',
        "C is a single-pass language where identifiers must be declared before they are referenced. Under ISO C99 §6.7.5.3, a function prototype declarator specifies the return type and parameter types of a function.\n\nWhen 'main()' calls 'add(3, 4)' on line 4:\n- The compiler checks that exactly two arguments are provided.\n- It verifies that the arguments are convertible to int.\n- It knows that the return value is of type int, generating instructions to read the result from the integer return register (%eax on x86).\n\nWithout a prototype, older C standards (C89) defaulted to 'implicit int' return types and unprototyped calling conventions. C99 abolished implicit function declarations (§6.5.2.2). Prototypes are therefore fundamental to type safety in C.",
        [
            (1, 1, "Compiler registers prototype for 'add': expects two int arguments and returns int.", {'registered_prototype': 'int add(int, int)'}, {'stack': []}),
            (2, 4, 'In main: compiler validates call add(3, 4) against prototype; types match.', {'arg1': 3, 'arg2': 4}, {'stack': [{'name': 'res', 'type': 'int', 'address': '0x7ffd10', 'value': 'uninitialized'}]}),
            (3, 9, "Call add: computes 3 + 4 = 7; returns 7 to main; printf outputs '7\\n'.", {'res': 7, 'stdout': '7'}, {'stack': [{'name': 'res', 'type': 'int', 'address': '0x7ffd10', 'value': '7'}]})
        ]
    )

    # Q072: Void Procedure Early Return
    add_q(
        72, 'TOPIC_FUNCTIONS', 'Easy', 'Void Procedure Early Return',
        'What is the output of the following program?',
        '#include <stdio.h>\nvoid check(int n) {\n    if (n < 0) {\n        printf("NEG\\n");\n        return;\n    }\n    printf("POS\\n");\n}\nint main() {\n    check(-5);\n    return 0;\n}',
        5, 'return;', "In a void function, 'return;' immediately exits the function and returns control to the caller! The remaining code is SKIPPED!",
        [
            ('A', 'NEG followed by POS', False, 'Thought void functions cannot exit early with return.', "'return;' without an expression is valid in void functions and exits immediately."),
            ('B', 'POS', False, 'Thought the condition failed.', '-5 is less than 0, so the negative branch executes.'),
            ('C', 'Compilation error', False, 'Thought return statements are forbidden in void functions.', 'return without an expression is standard C syntax for early exit in void functions.'),
            ('D', 'NEG', True, "Since -5 < 0 is true, 'NEG' is printed. The 'return;' statement immediately exits the function, bypassing printf('POS').", '')
        ],
        'A return statement with no expression in a void function immediately terminates execution and returns control.',
        'ISO/IEC 9899:1999 §6.8.6.4#1 (The return statement in void functions)',
        'Under ISO C99 §6.8.6.4#1:\n\'A return statement without an expression shall appear only in a function whose return type is void.\'\n\nWhen \'return;\' is executed:\n1. Control immediately exits the current function.\n2. The current function\'s activation record is removed from the call stack.\n3. Execution resumes in the caller (\'main()\') immediately following the call site.\n\nHere, \'check(-5)\' is called. The condition \'n < 0\' (-5 < 0) evaluates to true (1). \'printf("NEG\\n")\' executes, followed immediately by \'return;\'. Control returns to \'main()\', completely skipping \'printf("POS\\n")\'. The output is \'NEG\'.',
        [
            (1, 10, 'In main: call check(-5); push stack frame for check with parameter n = -5.', {'n': -5}, {'stack': [{'name': 'n (check)', 'type': 'int', 'address': '0x7ffd00', 'value': '-5'}]}),
            (2, 3, 'Inside check: evaluate condition -5 < 0 -> true (1); enter then-branch.', {'condition': 1}, {'stack': [{'name': 'n (check)', 'type': 'int', 'address': '0x7ffd00', 'value': '-5'}]}),
            (3, 4, "printf prints 'NEG\\n'; execute return; statement: exit check() immediately.", {'stdout': 'NEG'}, {'stack': []}),
            (4, 11, 'Back in main: check() returned; main returns 0.', {'main_return': 0}, {'stack': []})
        ]
    )

    # Q073: Global Variable Shadowing by Local Variable
    add_q(
        73, 'TOPIC_FUNCTIONS', 'Medium', 'Global Variable Shadowing by Local Variable',
        'What is the output of the following program?',
        '#include <stdio.h>\nint val = 100;\nvoid display() {\n    printf("%d ", val);\n}\nint main() {\n    int val = 50;\n    display();\n    printf("%d\\n", val);\n    return 0;\n}',
        7, 'int val = 50;', "Local 'val = 50' in main shadows the global val ONLY inside main! Function display() accesses the global val (100)!",
        [
            ('A', '50 50', False, 'Thought the local variable in main modified or overrode global val for all functions.', "C uses static lexical scoping; display() cannot see variables declared inside main's local block."),
            ('B', '100 50', True, "display() has no local 'val', so it accesses global val (100). main() has a local 'val' (50) that shadows global val inside main.", ''),
            ('C', '100 100', False, 'Thought the global variable took precedence over the local variable in main.', 'An inner block declaration hides (shadows) any outer declaration of the same name within that block.'),
            ('D', 'Compilation error', False, 'Thought having a local variable with the same name as a global is illegal.', 'Variable shadowing is valid standard C (§6.2.1).')
        ],
        'Identifiers declared inside a block hide any outer declaration. display() sees global 100; main sees local 50.',
        'ISO/IEC 9899:1999 §6.2.1#4 (Scopes of identifiers - shadowing)',
        "C adheres to static (lexical) scoping rules (ISO C99 §6.2.1). Scope is determined by the lexical structure of the source code:\n\n1. Global 'val' is declared at file scope (§6.2.1#2). It is visible to all functions in the translation unit that do not declare an identifier named 'val'.\n2. Inside 'display()', there is no local declaration of 'val'. The compiler resolves 'val' to the file-scope global variable 'val' (100).\n3. Inside 'main()', 'int val = 50;' is declared at block scope (§6.2.1#4). Under §6.2.1#4: 'If an identifier designates two different entities in the same scope, or if an inner declaration hides an outer declaration... the inner declaration hides the outer declaration.'\n\nThus, inside 'main', references to 'val' access the local variable (50). The call 'display()' prints 100, and main's subsequent printf prints 50, outputting '100 50'.",
        [
            (1, 2, 'Global variable val = 100 initialized in .data segment at 0x601040.', {'global_val': 100}, {'stack': [], 'data_segment': [{'name': 'val (global)', 'type': 'int', 'address': '0x601040', 'value': '100'}]}),
            (2, 7, 'In main: allocate local variable val = 50 on stack at 0x7ffd10 (shadows global val inside main).', {'local_val': 50}, {'stack': [{'name': 'val (local main)', 'type': 'int', 'address': '0x7ffd10', 'value': '50'}], 'data_segment': [{'name': 'val (global)', 'type': 'int', 'address': '0x601040', 'value': '100'}]}),
            (3, 4, "Call display(): display resolves 'val' to file-scope global at 0x601040; prints '100 '.", {'stdout': '100 '}, {'stack': [{'name': 'val (local main)', 'type': 'int', 'address': '0x7ffd10', 'value': '50'}], 'data_segment': [{'name': 'val (global)', 'type': 'int', 'address': '0x601040', 'value': '100'}]}),
            (4, 9, "Back in main: printf references local val at 0x7ffd10; prints '50\\n'. Total: '100 50'.", {'stdout': '100 50'}, {'stack': [{'name': 'val (local main)', 'type': 'int', 'address': '0x7ffd10', 'value': '50'}]})
        ]
    )

    # Q074: Static Local Variable Value Retention
    add_q(
        74, 'TOPIC_FUNCTIONS', 'Easy', 'Static Local Variable Value Retention',
        'What is the output of the following program?',
        '#include <stdio.h>\nvoid counter() {\n    static int count = 0;\n    count++;\n    printf("%d ", count);\n}\nint main() {\n    counter();\n    counter();\n    counter();\n    printf("\\n");\n    return 0;\n}',
        3, 'static int count = 0;', 'STATIC local variables retain their values between function calls! count persists across calls: prints 1 2 3!',
        [
            ('A', '1 2 3 ', True, 'Static local variables have static storage duration and retain their values across function invocations, incrementing to 1, 2, 3.', ''),
            ('B', '1 1 1 ', False, "Thought 'static int count = 0;' reinitialized count to 0 on every call.", 'Static variables are initialized only once before program execution begins; re-entering the function does not re-initialize them.'),
            ('C', '0 1 2 ', False, 'Thought count printed before incrementing.', 'count++ increments before the printf statement.'),
            ('D', 'Compilation error', False, 'Thought static variables can only be declared at global file scope.', 'static is valid on local variables and gives them static storage duration with block scope.')
        ],
        'Static local variables persist in the data segment across function calls. Prints 1 2 3 .',
        'ISO/IEC 9899:1999 §6.2.4#3 (Static storage duration) & §6.7.8#10',
        "In C, the storage duration of an object dictates its lifetime (§6.2.4). When the 'static' storage-class specifier is applied to a local variable declaration inside a function:\n1. The variable receives static storage duration. Its lifetime extends across the entire execution of the program.\n2. The variable's scope remains block scope (§6.2.1#4), meaning it can only be accessed by name within that function.\n3. The initialization ('count = 0') occurs exactly once before program startup, stored in the program's initialized data segment (.data).\n\nWhen 'counter()' is called:\n- Call 1: count increments from 0 to 1; prints '1 '.\n- Call 2: count increments from 1 to 2; prints '2 '.\n- Call 3: count increments from 2 to 3; prints '3 '.\nThe output is '1 2 3 '.",
        [
            (1, 3, "Static variable 'count' initialized to 0 once at program startup in data segment at 0x601040.", {'count': 0}, {'data_segment': [{'name': 'count (static)', 'type': 'int', 'address': '0x601040', 'value': '0'}], 'stack': []}),
            (2, 4, "Call 1: count++ updates static count to 1; printf prints '1 '.", {'count': 1, 'stdout': '1 '}, {'data_segment': [{'name': 'count (static)', 'type': 'int', 'address': '0x601040', 'value': '1'}], 'stack': []}),
            (3, 4, "Call 2: count retains 1; count++ updates to 2; printf prints '2 '.", {'count': 2, 'stdout': '1 2 '}, {'data_segment': [{'name': 'count (static)', 'type': 'int', 'address': '0x601040', 'value': '2'}], 'stack': []}),
            (4, 4, "Call 3: count retains 2; count++ updates to 3; printf prints '3 '. Total: '1 2 3 '.", {'count': 3, 'stdout': '1 2 3 '}, {'data_segment': [{'name': 'count (static)', 'type': 'int', 'address': '0x601040', 'value': '3'}], 'stack': []})
        ]
    )

    # Q075: Static Variable Initialized Once Only
    add_q(
        75, 'TOPIC_FUNCTIONS', 'Tricky', 'Static Variable Initialized Once Only',
        'What is the output of the following program?',
        '#include <stdio.h>\nint func() {\n    static int val = 10;\n    val += 5;\n    return val;\n}\nint main() {\n    int x = func();\n    int y = func();\n    printf("%d %d\\n", x, y);\n    return 0;\n}',
        3, 'static int val = 10;', "The initialization 'val = 10' happens ONCE at program startup! On call 2, val is 15, adding 5 gives 20!",
        [
            ('A', '15 15', False, 'Thought val was re-initialized to 10 on the second call.', "Static variables are initialized once at compile/load time; the line 'static int val = 10;' is not re-executed on subsequent calls."),
            ('B', '10 15', False, 'Thought func returned before adding 5 in the first call.', 'val += 5 executes before the return statement on both calls.'),
            ('C', '20 20', False, 'Thought both calls shared the final value.', 'x captured the return value of call 1 (15) before call 2 executed.'),
            ('D', '15 20', True, 'In call 1, val starts at 10 and becomes 15. In call 2, val retains 15 and becomes 20. Thus, x = 15 and y = 20.', '')
        ],
        'All objects with static storage duration are initialized before program startup, not on each call.',
        'ISO/IEC 9899:1999 §6.7.8#4 (Initialization of static duration objects)',
        "Under ISO C99 §6.7.8#4:\n'All objects with static storage duration shall be initialized (either explicitly or by default) before program startup.'\n\nA static local variable does not reside on the function's call stack. Instead, the compiler places it in the read-write data segment with its initial value (10) embedded directly into the executable binary.\n\nExecution trace:\n1. Call 1: 'val' is 10. 'val += 5' sets 'val' to 15. 'func()' returns 15, which is assigned to 'x'.\n2. Call 2: 'val' is currently 15 in the data segment. 'val += 5' sets 'val' to 20. 'func()' returns 20, which is assigned to 'y'.\n3. printf prints 'x' and 'y': '15 20'.",
        [
            (1, 3, 'Static val = 10 allocated once in data segment at 0x601040 before main starts.', {'val': 10}, {'data_segment': [{'name': 'val (static)', 'type': 'int', 'address': '0x601040', 'value': '10'}]}),
            (2, 8, 'Call 1: val += 5 mutates static val to 15; returns 15; assigned to x in main.', {'x': 15, 'val': 15}, {'stack': [{'name': 'x', 'type': 'int', 'address': '0x7ffd10', 'value': '15'}], 'data_segment': [{'name': 'val (static)', 'type': 'int', 'address': '0x601040', 'value': '15'}]}),
            (3, 9, 'Call 2: val starts at 15; val += 5 mutates to 20; returns 20; assigned to y in main.', {'x': 15, 'y': 20, 'val': 20}, {'stack': [{'name': 'x', 'type': 'int', 'address': '0x7ffd10', 'value': '15'}, {'name': 'y', 'type': 'int', 'address': '0x7ffd14', 'value': '20'}], 'data_segment': [{'name': 'val (static)', 'type': 'int', 'address': '0x601040', 'value': '20'}]}),
            (4, 10, "printf prints '15 20\\n'.", {'stdout': '15 20'}, {'stack': [{'name': 'x', 'type': 'int', 'address': '0x7ffd10', 'value': '15'}, {'name': 'y', 'type': 'int', 'address': '0x7ffd14', 'value': '20'}]})
        ]
    )

    # Q076: Automatic Local Variable Lifetime
    add_q(
        76, 'TOPIC_FUNCTIONS', 'Easy', 'Automatic Local Variable Lifetime',
        "What is the lifetime of an automatic local variable like 'temp' declared inside calculate()?",
        '#include <stdio.h>\nvoid calculate() {\n    int temp = 42;\n    printf("%d\\n", temp);\n} // temp storage ends here\nint main() {\n    calculate();\n    return 0;\n}',
        3, 'int temp = 42;', 'Automatic local variables exist ONLY on the stack while the enclosing function/block is executing! When the function returns, its storage is destroyed!',
        [
            ('A', 'It persists throughout the entire execution of the program', False, 'Confused automatic storage duration with static storage duration.', "Only static and global variables persist for the program's entire run; automatic variables exist only while their block is active."),
            ('B', 'It persists until main() returns', False, 'Thought local variables persist until the caller terminates.', "A function's stack frame is popped as soon as that function returns, destroying its local variables."),
            ('C', 'Its lifetime begins on entry to calculate() and ends when calculate() returns', True, 'Automatic variables are allocated on the call stack upon block entry and deallocated when the block terminates.', ''),
            ('D', 'It must be manually freed using free()', False, 'Confused automatic stack variables with heap allocations from malloc().', 'Stack variables are managed automatically by the runtime; calling free() on a stack address causes undefined behavior.')
        ],
        'The lifetime of an automatic object extends from entry into the block to its termination. Storage is deallocated on return.',
        'ISO/IEC 9899:1999 §6.2.4#5 (Automatic storage duration lifetime)',
        "ISO C99 §6.2.4#5 defines automatic storage duration:\n'For such an object that does not have a variable length array type, its lifetime extends from entry into the block with which it is associated until execution of that block ends in any way.'\n\nWhen 'calculate()' is invoked:\n1. The CPU decrements the stack pointer (%rsp) to allocate memory for calculate's stack frame.\n2. The local variable 'temp' is placed at address 0x7ffd00 and initialized to 42.\n3. When the closing brace '}' is reached, the function returns.\n4. The stack frame is destroyed: the stack pointer is restored to caller's position.\nAny pointer to 'temp' becomes a dangling pointer; accessing it after return is undefined behavior.",
        [
            (1, 7, 'In main: invoke calculate(); CPU allocates stack frame for calculate().', {'stack_frame': 'calculate()'}, {'stack': []}),
            (2, 3, "Allocate automatic variable temp = 42 on stack; printf prints '42\\n'.", {'temp': 42, 'stdout': '42'}, {'stack': [{'name': 'temp', 'type': 'int', 'address': '0x7ffd00', 'value': '42'}]}),
            (3, 5, "calculate() finishes; stack frame popped; storage for 'temp' is deallocated. main resumes.", {'temp': 'destroyed'}, {'stack': []})
        ]
    )

    # Q077: Recursive Factorial Function Call Trace
    add_q(
        77, 'TOPIC_FUNCTIONS', 'Easy', 'Recursive Factorial Function Call Trace',
        'What is the output of the following program?',
        '#include <stdio.h>\nint factorial(int n) {\n    if (n <= 1) return 1;\n    return n * factorial(n - 1);\n}\nint main() {\n    printf("%d\\n", factorial(4));\n    return 0;\n}',
        4, 'return n * factorial(n - 1);', 'factorial(4) recurses down: 4 * factorial(3) -> 4 * 3 * factorial(2) -> 4 * 3 * 2 * 1 = 24!',
        [
            ('A', '24', True, 'Trace: factorial(4) = 4 * 3 * 2 * 1 = 24. Base case n <= 1 returns 1, unwinding the call stack to 24.', ''),
            ('B', '12', False, 'Calculated 4 * 3 without completing the recursion.', 'Recursion continues down to the base case: 4 * 3 * 2 * 1 = 24.'),
            ('C', '10', False, 'Added the numbers (4 + 3 + 2 + 1) instead of multiplying.', 'Factorial is multiplicative: 4 * 3 * 2 * 1 = 24.'),
            ('D', '0', False, 'Thought the base case returned 0, multiplying the whole product to 0.', 'The base case returns 1 (the multiplicative identity), not 0.')
        ],
        'Recursive trace: fact(4) -> 4 * fact(3) -> 4 * 3 * fact(2) -> 4 * 3 * 2 * 1 = 24.',
        'ISO/IEC 9899:1999 §6.5.2.2 (Recursive function calls)',
        "Recursion in C relies on the call stack. Each invocation of 'factorial' creates a distinct stack frame with its own independent parameter 'n'.\n\nCall stack expansion:\n1. factorial(4): returns 4 * factorial(3)\n2. factorial(3): returns 3 * factorial(2)\n3. factorial(2): returns 2 * factorial(1)\n4. factorial(1): 'n <= 1' matches base case; returns 1.\n\nCall stack unwinding:\n- factorial(2) computes 2 * 1 = 2\n- factorial(3) computes 3 * 2 = 6\n- factorial(4) computes 4 * 6 = 24\nprintf outputs '24'.",
        [
            (1, 8, 'Call factorial(4): allocates frame n=4; invokes factorial(3).', {'call': 'factorial(4)', 'n': 4}, {'stack': [{'name': 'n (frame 1)', 'type': 'int', 'address': '0x7ffd30', 'value': '4'}]}),
            (2, 4, 'Stack builds: factorial(3) -> factorial(2) -> factorial(1).', {'call_depth': 4}, {'stack': [{'name': 'n (frame 1)', 'type': 'int', 'address': '0x7ffd30', 'value': '4'}, {'name': 'n (frame 2)', 'type': 'int', 'address': '0x7ffd20', 'value': '3'}, {'name': 'n (frame 3)', 'type': 'int', 'address': '0x7ffd10', 'value': '2'}, {'name': 'n (frame 4)', 'type': 'int', 'address': '0x7ffd00', 'value': '1'}]}),
            (3, 3, 'factorial(1) hits base case n <= 1: returns 1; stack unwinds.', {'return_val': 1}, {'stack': [{'name': 'n (frame 1)', 'type': 'int', 'address': '0x7ffd30', 'value': '4'}, {'name': 'n (frame 2)', 'type': 'int', 'address': '0x7ffd20', 'value': '3'}, {'name': 'n (frame 3)', 'type': 'int', 'address': '0x7ffd10', 'value': '2'}]}),
            (4, 4, "Unwind: 2 * 1 = 2 -> 3 * 2 = 6 -> 4 * 6 = 24; printf prints '24\\n'.", {'stdout': '24'}, {'stack': []})
        ]
    )

    # Q078: Missing Base Case in Recursion
    add_q(
        78, 'TOPIC_FUNCTIONS', 'Easy', 'Missing Base Case in Recursion',
        'What happens when this recursive function is called?',
        '#include <stdio.h>\nvoid recurse(int n) {\n    recurse(n + 1);\n}\nint main() {\n    recurse(1);\n    return 0;\n}',
        3, 'recurse(n + 1);', 'Without a base case, recursion NEVER terminates! Each call pushes a new stack frame until stack memory is exhausted, causing a STACK OVERFLOW CRASH!',
        [
            ('A', 'The program terminates when n exceeds INT_MAX', False, 'Thought integer overflow stops the recursion.', 'The program will exhaust the physical stack memory (typically 1-8 MB) after a few tens of thousands of calls, crashing long before reaching INT_MAX (2 billion).'),
            ('B', 'Compilation error', False, 'Thought recursive functions without base cases are rejected by the compiler.', 'C compilers cannot solve the halting problem; infinite recursion is syntactically valid and compiles cleanly.'),
            ('C', 'Runtime Crash / Stack Overflow (infinite recursion)', True, 'The function lacks a base case. Unbounded recursive calls continuously allocate stack frames until call stack memory is exhausted, triggering a fatal stack overflow crash.', ''),
            ('D', 'Prints nothing and terminates normally', False, 'Thought the program silently exits.', 'The runtime terminates the process with a segmentation fault / stack overflow exception.')
        ],
        'Unbounded recursion consumes stack frames until a stack overflow occurs (Segmentation Fault).',
        'ISO/IEC 9899:1999 §6.5.2.2 & Annex J.2 (Stack exhaustion undefined behavior)',
        "Every function call in C pushes an activation record (stack frame) onto the call stack containing:\n- The return instruction address.\n- Saved registers and frame pointer (%rbp).\n- Local parameters and variables.\n\nA typical thread stack size on Linux or Windows is between 1 MB and 8 MB. In 'recurse(n + 1)':\n1. There is no base condition (stopping condition).\n2. 'recurse' calls itself indefinitely with n = 1, 2, 3, 4, ...\n3. Each call consumes stack bytes.\n4. When the stack pointer crosses the operating system's guard page boundary (the memory limit allocated for stack growth), the hardware MMU raises a page fault.\n5. Because the guard page is unmapped, the OS sends a fatal signal (SIGSEGV / EXCEPTION_STACK_OVERFLOW) and crashes the program.",
        [
            (1, 6, 'In main: call recurse(1); push frame 1 on call stack.', {'call': 'recurse(1)', 'stack_depth': 1}, {'stack': [{'name': 'n (frame 1)', 'type': 'int', 'address': '0x7ffd00', 'value': '1'}]}),
            (2, 3, 'recurse(1) calls recurse(2), which calls recurse(3), continuously pushing stack frames without returning.', {'stack_depth': 'thousands of frames'}, {'stack': [{'name': 'n (frame 1)', 'type': 'int', 'address': '0x7ffd00', 'value': '1'}, {'name': 'n (frame 2)', 'type': 'int', 'address': '0x7ffce0', 'value': '2'}, {'name': '...', 'type': '...', 'address': '...', 'value': '...'}]}),
            (3, 3, 'Call stack exceeds memory limit (hits guard page); OS raises SIGSEGV (Stack Overflow).', {'signal': 'SIGSEGV / Stack Overflow'}, {'stack': [{'name': 'status', 'type': 'crash', 'address': 'guard page', 'value': 'EXCEPTION_STACK_OVERFLOW'}]})
        ]
    )

    # Q079: Print Order in Recursive Call (Before vs After)
    add_q(
        79, 'TOPIC_FUNCTIONS', 'Medium', 'Print Order in Recursive Call (Before vs After)',
        'What is the output of the following program?',
        '#include <stdio.h>\nvoid print_down(int n) {\n    if (n == 0) return;\n    print_down(n - 1);\n    printf("%d ", n);\n}\nint main() {\n    print_down(3);\n    printf("\\n");\n    return 0;\n}',
        5, 'printf("%d ", n);', 'printf is AFTER the recursive call! The calls stack up down to 0, then print on the way BACK UP during unwinding: 1 2 3!',
        [
            ('A', '3 2 1 ', False, 'Assumed printf executed before the recursive call.', 'Because printf is located after the recursive call, it does not execute until the inner recursive calls return.'),
            ('B', '1 2 3 ', True, 'The recursive call occurs before printf. The function recurses until n=0, then prints during stack unwinding in reverse order: 1 2 3.', ''),
            ('C', '0 1 2 3 ', False, 'Thought n=0 was printed.', 'When n == 0, the function returns immediately without printing.'),
            ('D', '3 2 1 0 ', False, 'Inverted the order and included the base case.', 'Prints strictly ascending from 1 to 3 during recursive unwinding.')
        ],
        'Statements placed after recursive calls execute in reverse (LIFO stack unwinding order). Prints 1 2 3.',
        'ISO/IEC 9899:1999 §6.5.2.2 (Order of evaluation in recursive unwinding)',
        'The position of operations relative to a recursive call determines whether execution occurs on the forward journey (stack building) or on the return journey (stack unwinding):\n\n- Pre-recursive statements execute in normal order (FIFO / top-down).\n- Post-recursive statements execute in reverse order (LIFO / bottom-up), because the call stack is a Last-In, First-Out data structure.\n\nTrace for \'print_down(3)\':\n1. print_down(3) calls print_down(2) [line 5 not yet reached].\n2. print_down(2) calls print_down(1) [line 5 not yet reached].\n3. print_down(1) calls print_down(0) [line 5 not yet reached].\n4. print_down(0) hits \'if (n == 0) return;\' and returns immediately.\nUnwinding:\n- Back in print_down(1): executes printf("%d ", 1) -> outputs \'1 \'. Returns.\n- Back in print_down(2): executes printf("%d ", 2) -> outputs \'2 \'. Returns.\n- Back in print_down(3): executes printf("%d ", 3) -> outputs \'3 \'. Returns.\nTotal printed output is \'1 2 3 \'.',
        [
            (1, 4, 'print_down(3) calls (2), which calls (1), which calls (0). Stack reaches depth 4.', {'call_stack': [3, 2, 1, 0]}, {'stack': [{'name': 'n (frame 3)', 'type': 'int', 'address': '0x7ffd20', 'value': '3'}, {'name': 'n (frame 2)', 'type': 'int', 'address': '0x7ffd10', 'value': '2'}, {'name': 'n (frame 1)', 'type': 'int', 'address': '0x7ffd00', 'value': '1'}, {'name': 'n (frame 0)', 'type': 'int', 'address': '0x7ffcf0', 'value': '0'}]}),
            (2, 3, 'print_down(0) returns immediately without printing.', {'return': 0}, {'stack': [{'name': 'n (frame 3)', 'type': 'int', 'address': '0x7ffd20', 'value': '3'}, {'name': 'n (frame 2)', 'type': 'int', 'address': '0x7ffd10', 'value': '2'}, {'name': 'n (frame 1)', 'type': 'int', 'address': '0x7ffd00', 'value': '1'}]}),
            (3, 5, "Unwinding: frame 1 resumes and prints '1 '; frame 2 resumes and prints '2 '; frame 3 resumes and prints '3 '.", {'stdout': '1 2 3 '}, {'stack': []})
        ]
    )

    # Q080: Recursive Fibonacci Call Tree
    add_q(
        80, 'TOPIC_FUNCTIONS', 'Medium', 'Recursive Fibonacci Call Tree',
        'What is the output of the following program?',
        '#include <stdio.h>\nint fib(int n) {\n    if (n <= 0) return 0;\n    if (n == 1) return 1;\n    return fib(n - 1) + fib(n - 2);\n}\nint main() {\n    printf("%d\\n", fib(4));\n    return 0;\n}',
        5, 'return fib(n - 1) + fib(n - 2);', 'fib(4) expands as binary recursion tree: fib(3) + fib(2) = (fib(2) + fib(1)) + fib(2) = (1 + 1) + 1 = 3!',
        [
            ('A', '4', False, 'Confused the argument n (4) with the Fibonacci result.', 'F(4) = F(3) + F(2) = 2 + 1 = 3, not 4.'),
            ('B', '5', False, 'Calculated F(5) instead of F(4).', 'F(5) is 5, but the argument passed is 4.'),
            ('C', '2', False, 'Calculated F(3) instead of F(4).', 'F(3) is 2; adding F(2) yields 3.'),
            ('D', '3', True, 'Fibonacci sequence: F(0)=0, F(1)=1, F(2)=1, F(3)=2, F(4)=3. fib(4) evaluates to 3.', '')
        ],
        'fib(4) expands to fib(3) + fib(2) = 2 + 1 = 3. Standard binary tree recursion.',
        'ISO/IEC 9899:1999 §6.5.2.2 (Multiple recursive function invocations)',
        "The naive recursive Fibonacci implementation generates a binary call tree:\n                   fib(4)\n                  /      \\\n             fib(3)        fib(2)\n            /     \\       /     \\\n        fib(2)   fib(1)  fib(1) fib(0)\n        /    \\     [1]     [1]    [0]\n     fib(1) fib(0)\n       [1]    [0]\n\nEvaluating leaves:\n- fib(2) = fib(1) + fib(0) = 1 + 0 = 1\n- fib(3) = fib(2) + fib(1) = 1 + 1 = 2\n- Right branch fib(2) = fib(1) + fib(0) = 1 + 0 = 1\n- fib(4) = fib(3) + fib(2) = 2 + 1 = 3\n\nprintf outputs '3'. Notice that binary recursion without memoization has O(2^n) exponential time complexity because subproblems (like fib(2)) are repeatedly recomputed.",
        [
            (1, 8, 'In main: call fib(4); begins expansion of binary recursion tree.', {'call': 'fib(4)'}, {'stack': [{'name': 'n', 'type': 'int', 'address': '0x7ffd30', 'value': '4'}]}),
            (2, 5, 'Left subtree resolves: fib(3) computes fib(2) + fib(1) = 1 + 1 = 2.', {'fib_3': 2}, {'stack': [{'name': 'n', 'type': 'int', 'address': '0x7ffd20', 'value': '3'}]}),
            (3, 5, 'Right subtree resolves: fib(2) computes fib(1) + fib(0) = 1 + 0 = 1.', {'fib_2': 1}, {'stack': [{'name': 'n', 'type': 'int', 'address': '0x7ffd20', 'value': '2'}]}),
            (4, 5, "Sum results: fib(4) = fib(3) + fib(2) = 2 + 1 = 3; printf prints '3\\n'.", {'stdout': '3'}, {'stack': []})
        ]
    )

    # Q081: Combining Function Return Values in Expression
    add_q(
        81, 'TOPIC_FUNCTIONS', 'Easy', 'Combining Function Return Values in Expression',
        'What is the output of the following program?',
        '#include <stdio.h>\nint square(int x) {\n    return x * x;\n}\nint main() {\n    int res = square(3) + square(4);\n    printf("%d\\n", res);\n    return 0;\n}',
        6, 'int res = square(3) + square(4);', 'Function calls are evaluated first: square(3) is 9, square(4) is 16. 9 + 16 = 25!',
        [
            ('A', '25', True, 'Function calls are postfix expressions with higher precedence than addition: 3*3 = 9, 4*4 = 16. 9 + 16 = 25.', ''),
            ('B', '49', False, 'Thought it added 3 + 4 = 7 first, then squared: 7^2 = 49.', 'Function calls have higher precedence (level 1) than addition (level 4); square is evaluated for 3 and 4 individually before addition.'),
            ('C', '14', False, 'Added 3^2 + 4 = 9 + 4 = 13 or made arithmetic error.', 'Both square calls execute: 9 + 16 = 25.'),
            ('D', '12', False, 'Multiplied 3 * 4 = 12.', 'The functions compute squares and add their returns.')
        ],
        'Function calls are postfix expressions with higher precedence than addition. 9 + 16 = 25.',
        'ISO/IEC 9899:1999 §6.5.2 (Postfix operators - function calls)',
        "Function calls 'f()' are postfix expressions, which occupy the highest tier of operator precedence in C (§6.5.2).\n\nIn 'int res = square(3) + square(4);':\n1. The function calls 'square(3)' and 'square(4)' have higher precedence than the binary addition operator '+'.\n2. 'square(3)' is called: returns 3 * 3 = 9.\n3. 'square(4)' is called: returns 4 * 4 = 16.\n4. The binary addition operator '+' adds the two return values: 9 + 16 = 25.\n5. 25 is stored in 'res'.\n\nNote: The C standard does not specify the order of evaluation between operands of '+' (§6.5#3); the compiler may call square(3) before square(4) or vice versa, but since square() has no side effects, the result is deterministically 25.",
        [
            (1, 6, 'Evaluate square(3): push frame x=3; returns 3*3 = 9.', {'ret1': 9}, {'stack': [{'name': 'res', 'type': 'int', 'address': '0x7ffd10', 'value': 'uninitialized'}]}),
            (2, 6, 'Evaluate square(4): push frame x=4; returns 4*4 = 16.', {'ret2': 16}, {'stack': [{'name': 'res', 'type': 'int', 'address': '0x7ffd10', 'value': 'uninitialized'}]}),
            (3, 6, "Add return values: 9 + 16 = 25; assign 25 to 'res'.", {'res': 25}, {'stack': [{'name': 'res', 'type': 'int', 'address': '0x7ffd10', 'value': '25'}]}),
            (4, 7, "printf prints '25\\n'.", {'stdout': '25'}, {'stack': [{'name': 'res', 'type': 'int', 'address': '0x7ffd10', 'value': '25'}]})
        ]
    )

    # Q082: Nested Function Call Evaluation Order
    add_q(
        82, 'TOPIC_FUNCTIONS', 'Easy', 'Nested Function Call Evaluation Order',
        'What is the output of the following program?',
        '#include <stdio.h>\nint add_two(int x) { return x + 2; }\nint mult_three(int x) { return x * 3; }\nint main() {\n    int res = add_two(mult_three(4));\n    printf("%d\\n", res);\n    return 0;\n}',
        5, 'add_two(mult_three(4))', 'Innermost function arguments evaluate FIRST! mult_three(4) evaluates to 12 first, then add_two(12) produces 14!',
        [
            ('A', '18', False, 'Evaluated outer function first: (4 + 2) * 3 = 6 * 3 = 18.', 'Arguments must be fully evaluated before the receiving function can be called. Inner mult_three(4) runs first.'),
            ('B', '14', True, 'Innermost argument evaluates first: mult_three(4) = 4 * 3 = 12. Then add_two(12) = 12 + 2 = 14.', ''),
            ('C', '24', False, 'Calculated 4 * 3 * 2.', 'The operations are (4 * 3) + 2 = 14.'),
            ('D', '12', False, 'Forgot the outer add_two call.', 'add_two adds 2 to 12, yielding 14.')
        ],
        'Arguments to a function call are evaluated before the function is called. (4 * 3) + 2 = 14.',
        'ISO/IEC 9899:1999 §6.5.2.2#4 (Argument evaluation before function execution)',
        "Under ISO C99 §6.5.2.2#4, all arguments to a function call must be completely evaluated before the function itself is entered (applicative order evaluation).\n\nIn 'add_two(mult_three(4))':\n1. To call 'add_two', its argument 'mult_three(4)' must be evaluated to a concrete value first.\n2. 'mult_three(4)' is called: 4 * 3 = 12.\n3. Now 'add_two(12)' is called: 12 + 2 = 14.\n4. The result 14 is stored in 'res'.\n\nprintf prints '14'. Nested function calls always evaluate from inside out.",
        [
            (1, 5, 'Evaluate innermost call mult_three(4): invokes mult_three with x=4 -> returns 12.', {'mult_result': 12}, {'stack': [{'name': 'res', 'type': 'int', 'address': '0x7ffd10', 'value': 'uninitialized'}]}),
            (2, 5, 'Evaluate outer call add_two(12): invokes add_two with x=12 -> returns 14.', {'add_result': 14}, {'stack': [{'name': 'res', 'type': 'int', 'address': '0x7ffd10', 'value': 'uninitialized'}]}),
            (3, 5, "Assign 14 to local variable 'res'.", {'res': 14}, {'stack': [{'name': 'res', 'type': 'int', 'address': '0x7ffd10', 'value': '14'}]}),
            (4, 6, "printf prints '14\\n'.", {'stdout': '14'}, {'stack': [{'name': 'res', 'type': 'int', 'address': '0x7ffd10', 'value': '14'}]})
        ]
    )

    # Q083: Block Scope Variable Shadowing
    add_q(
        83, 'TOPIC_FUNCTIONS', 'Medium', 'Block Scope Variable Shadowing',
        'What is the output of the following program?',
        '#include <stdio.h>\nint main() {\n    int x = 10;\n    {\n        int x = 20;\n        printf("%d ", x);\n    }\n    printf("%d\\n", x);\n    return 0;\n}',
        5, 'int x = 20;', 'The inner block declares a NEW variable x=20 that shadows outer x! When the inner block closes, outer x (10) is restored: prints 20 10!',
        [
            ('A', '20 20', False, "Thought inner 'int x = 20;' permanently updated outer x to 20.", 'Inner x is a brand-new variable allocated in a separate stack location; when the inner block closes, it is destroyed, leaving outer x unchanged.'),
            ('B', '10 10', False, 'Thought the outer declaration prevented inner redeclaration.', 'C permits variable shadowing in nested blocks; inner x takes precedence within its block.'),
            ('C', 'Compilation error', False, "Thought redeclaring variable 'x' in a nested block is an error.", 'Redeclaring an identifier in an inner block is valid standard C (§6.2.1).'),
            ('D', '20 10', True, "The inner block declares a distinct variable 'x' that shadows outer 'x' within { }. Once the block ends, outer 'x' (10) is visible again.", '')
        ],
        'An identifier declared in an inner block hides outer declarations during that block. Prints 20 10.',
        'ISO/IEC 9899:1999 §6.2.1#4 (Block scope shadowing)',
        'In C, compound statements enclosed in braces \'{ ... }\' establish a new block scope (§6.2.1#4).\n\n1. In \'main\', outer \'x\' is allocated at address 0x7ffd10 and initialized to 10.\n2. The inner block \'{ ... }\' begins. Inside, \'int x = 20;\' declares a completely separate variable \'x\' at a different stack address (0x7ffd0c).\n3. The inner \'x\' hides (shadows) outer \'x\'.\n4. \'printf("%d ", x)\' prints the inner variable: \'20 \'.\n5. The inner block terminates: inner \'x\' goes out of scope and its storage is reclaimed.\n6. The outer printf accesses the original outer \'x\' (10), printing \'10\'.\n\nThe output is \'20 10\'. This is a frequent exam question testing understanding of lexical scope lifetimes.',
        [
            (1, 3, 'Outer block: allocate outer int x = 10 at address 0x7ffd10.', {'x_outer': 10}, {'stack': [{'name': 'x (outer)', 'type': 'int', 'address': '0x7ffd10', 'value': '10'}]}),
            (2, 5, 'Inner block entered: allocate inner int x = 20 at address 0x7ffd0c (shadows outer x).', {'x_inner': 20}, {'stack': [{'name': 'x (outer)', 'type': 'int', 'address': '0x7ffd10', 'value': '10'}, {'name': 'x (inner)', 'type': 'int', 'address': '0x7ffd0c', 'value': '20'}]}),
            (3, 6, "Inner printf prints inner x: '20 '.", {'stdout': '20 '}, {'stack': [{'name': 'x (outer)', 'type': 'int', 'address': '0x7ffd10', 'value': '10'}, {'name': 'x (inner)', 'type': 'int', 'address': '0x7ffd0c', 'value': '20'}]}),
            (4, 7, "Inner block closes: inner x is destroyed. Outer printf prints outer x (10): '10\\n'. Total: '20 10'.", {'stdout': '20 10'}, {'stack': [{'name': 'x (outer)', 'type': 'int', 'address': '0x7ffd10', 'value': '10'}]})
        ]
    )

    # Q084: Pre-Order Print in Recursion
    add_q(
        84, 'TOPIC_FUNCTIONS', 'Medium', 'Pre-Order Print in Recursion',
        'What is the output of the following program?',
        '#include <stdio.h>\nvoid countdown(int n) {\n    if (n == 0) return;\n    printf("%d ", n);\n    countdown(n - 1);\n}\nint main() {\n    countdown(3);\n    printf("\\n");\n    return 0;\n}',
        4, 'printf("%d ", n);', 'printf is BEFORE the recursive call! It prints BEFORE recursing on the way down: 3 2 1!',
        [
            ('A', '1 2 3 ', False, 'Confused pre-order printing with post-order unwinding.', 'Because printf is located before the recursive call, it executes in top-down forward order (3, then 2, then 1).'),
            ('B', '3 2 1 0 ', False, 'Thought n=0 was printed.', "When n == 0, the function hits 'return;' before reaching printf."),
            ('C', '3 2 1 ', True, 'printf executes before the recursive call countdown(n - 1), printing values in descending order as the stack builds: 3 2 1.', ''),
            ('D', '0 1 2 3 ', False, 'Inverted order and included base case.', 'Execution counts down from 3 to 1.')
        ],
        'Statements executed before recursive calls execute in top-down order as the call stack grows. Prints 3 2 1.',
        'ISO/IEC 9899:1999 §6.5.2.2 (Pre-order recursive execution trace)',
        'Contrasting directly with Q079, here \'printf("%d ", n);\' precedes the recursive call \'countdown(n - 1);\' (pre-order execution).\n\nTrace:\n1. countdown(3):\n   - \'n == 0\' is false.\n   - Executes printf: prints \'3 \'.\n   - Calls countdown(2).\n2. countdown(2):\n   - \'n == 0\' is false.\n   - Executes printf: prints \'2 \'.\n   - Calls countdown(1).\n3. countdown(1):\n   - \'n == 0\' is false.\n   - Executes printf: prints \'1 \'.\n   - Calls countdown(0).\n4. countdown(0):\n   - \'n == 0\' is true. Hits \'return;\' immediately.\n5. All frames unwind without executing any further code.\n\nTotal printed output: \'3 2 1 \'.',
        [
            (1, 4, "countdown(3): prints '3 '; calls countdown(2).", {'n': 3, 'stdout': '3 '}, {'stack': [{'name': 'n (frame 3)', 'type': 'int', 'address': '0x7ffd20', 'value': '3'}]}),
            (2, 4, "countdown(2): prints '2 '; calls countdown(1).", {'n': 2, 'stdout': '3 2 '}, {'stack': [{'name': 'n (frame 3)', 'type': 'int', 'address': '0x7ffd20', 'value': '3'}, {'name': 'n (frame 2)', 'type': 'int', 'address': '0x7ffd10', 'value': '2'}]}),
            (3, 4, "countdown(1): prints '1 '; calls countdown(0).", {'n': 1, 'stdout': '3 2 1 '}, {'stack': [{'name': 'n (frame 3)', 'type': 'int', 'address': '0x7ffd20', 'value': '3'}, {'name': 'n (frame 2)', 'type': 'int', 'address': '0x7ffd10', 'value': '2'}, {'name': 'n (frame 1)', 'type': 'int', 'address': '0x7ffd00', 'value': '1'}]}),
            (4, 3, "countdown(0): base case n==0 returns; all frames unwind. Total output: '3 2 1 '.", {'stdout': '3 2 1 '}, {'stack': []})
        ]
    )

    # =========================================================================
    # TOPIC_ARRAYS (Q085 - Q100)
    # =========================================================================
    # Q085: Array 0-Indexed Subscript Bounds
    add_q(
        85, 'TOPIC_ARRAYS', 'Easy', 'Array 0-Indexed Subscript Bounds',
        'For an array declared as int arr[5]; which subscript indices are valid according to C standards?',
        '#include <stdio.h>\nint main() {\n    int arr[5] = {10, 20, 30, 40, 50};\n    printf("%d to %d\\n", 0, 5 - 1);\n    return 0;\n}',
        3, 'int arr[5] = {10, 20, 30, 40, 50};', 'In C, arrays are 0-indexed! An array of size 5 has valid indices 0, 1, 2, 3, 4! Index 5 is OUT OF BOUNDS!',
        [
            ('A', '1 to 5', False, 'Confused with 1-based indexing used in Fortran, MATLAB, or mathematical notation.', 'C array indexing is strictly 0-based; index 5 is one past the end.'),
            ('B', '0 to 4', True, 'C arrays are 0-indexed. Indices run from 0 to N-1 (0 through 4).', ''),
            ('C', '0 to 5', False, 'Thought index 5 was included as the 5th element.', 'With 0-indexing, the 5 elements occupy indices 0, 1, 2, 3, 4; index 5 is the 6th element.'),
            ('D', '1 to 4', False, 'Forgot that index 0 is valid and holds the first element.', 'Index 0 is valid and stores the initial array element.')
        ],
        'An array of size N has valid subscript indices 0 through N-1. For size 5, valid indices are 0 to 4.',
        'ISO/IEC 9899:1999 §6.5.2.1#2 (Array subscripting and pointer equivalence)',
        "In C, array subscripting 'E1[E2]' is formally defined by ISO C99 §6.5.2.1#2 as identical to '(*((E1) + (E2)))'.\n\nBecause pointer arithmetic offset 0 refers to the initial element ('*(arr + 0) == arr[0]'), arrays in C are inherently 0-indexed:\n- The first element is stored at offset 0: 'arr[0]'.\n- The N-th element is stored at offset N-1: 'arr[N-1]'.\n\nFor 'int arr[5];', memory is allocated for exactly 5 contiguous integers. The valid subscript indices are 0, 1, 2, 3, and 4.\nAccessing 'arr[5]' attempts to dereference '*(arr + 5)', which addresses memory outside the allocated boundary of 'arr'. Subscripting past the bounds is undefined behavior (§6.5.6#8).",
        [
            (1, 3, 'Allocate int arr[5] on stack (5 elements: indices 0..4).', {'arr_bounds': '0..4'}, {'stack': [{'name': 'arr', 'type': 'int[5]', 'address': '0x7ffd10', 'value': '{10, 20, 30, 40, 50}'}]}),
            (2, 4, 'Compute bounds: 0 to 5 - 1 = 4.', {'lower': 0, 'upper': 4}, {'stack': [{'name': 'arr', 'type': 'int[5]', 'address': '0x7ffd10', 'value': '{10, 20, 30, 40, 50}'}]}),
            (3, 4, "printf prints '0 to 4\\n'.", {'stdout': '0 to 4'}, {'stack': [{'name': 'arr', 'type': 'int[5]', 'address': '0x7ffd10', 'value': '{10, 20, 30, 40, 50}'}]})
        ]
    )

    # Q086: Partial Initialization Zero-Padding
    add_q(
        86, 'TOPIC_ARRAYS', 'Medium', 'Partial Initialization Zero-Padding',
        'What is the output of the following program?',
        '#include <stdio.h>\nint main() {\n    int arr[5] = {1, 2};\n    printf("%d %d %d\\n", arr[0], arr[1], arr[2]);\n    return 0;\n}',
        3, 'int arr[5] = {1, 2};', 'If an array initializer list has fewer elements than the array size, ALL remaining elements are automatically zero-initialized!',
        [
            ('A', '1 2 0', True, 'arr[0]=1 and arr[1]=2 from the initializer. ISO C mandates that all remaining elements (arr[2] through arr[4]) are automatically initialized to 0.', ''),
            ('B', '1 2 followed by garbage value', False, 'Assumed unmentioned elements retain whatever garbage bits were on the stack.', 'C guarantees zero-initialization for aggregate elements omitted from an initializer list (§6.7.9#21).'),
            ('C', '1 2 1', False, 'Assumed the initializer pattern repeats cyclically across remaining slots.', 'Initializers do not repeat; uninitialized slots receive zero.'),
            ('D', 'Compilation error', False, 'Believed initializing fewer elements than the declared array size is invalid syntax.', 'Partial initialization is completely valid standard C idiom.')
        ],
        'Partial array initialization automatically initializes all remaining elements to zero. Prints 1 2 0.',
        'ISO/IEC 9899:1999 §6.7.9#21 (Initialization of remaining aggregate elements)',
        'Under ISO C99 §6.7.9#21, if an initializer list for an aggregate (array or struct) contains fewer initializers than there are elements, the remaining elements are automatically initialized to zero:\n\'If there are fewer initializers in a brace-enclosed list than there are elements or members of an aggregate... the remainder of the aggregate shall be initialized implicitly the same as objects that have static storage duration.\'\n\nFor arithmetic types like \'int\', static storage initialization means zero (0).\n\nIn this program:\n- \'arr[0]\' is initialized to 1.\n- \'arr[1]\' is initialized to 2.\n- \'arr[2]\', \'arr[3]\', and \'arr[4]\' are implicitly initialized to 0.\n\nTherefore, \'printf("%d %d %d\\n", arr[0], arr[1], arr[2])\' deterministically prints \'1 2 0\'. This is also why \'{0}\' is the canonical idiom to zero out an entire array.',
        [
            (1, 3, 'Allocate arr[5]; explicit initializers set arr[0]=1, arr[1]=2; implicit zeroing sets arr[2..4]=0.', {'arr[0]': 1, 'arr[1]': 2, 'arr[2]': 0}, {'stack': [{'name': 'arr', 'type': 'int[5]', 'address': '0x7ffd10', 'value': '{1, 2, 0, 0, 0}'}]}),
            (2, 4, 'Read arr[0], arr[1], arr[2] values: 1, 2, 0.', {'values': [1, 2, 0]}, {'stack': [{'name': 'arr', 'type': 'int[5]', 'address': '0x7ffd10', 'value': '{1, 2, 0, 0, 0}'}]}),
            (3, 4, "printf prints '1 2 0\\n'.", {'stdout': '1 2 0'}, {'stack': [{'name': 'arr', 'type': 'int[5]', 'address': '0x7ffd10', 'value': '{1, 2, 0, 0, 0}'}]})
        ]
    )

    # Q087: Inferred Array Size from Initializer
    add_q(
        87, 'TOPIC_ARRAYS', 'Easy', 'Inferred Array Size from Initializer',
        'What is sizeof(arr) / sizeof(arr[0]) for: int arr[] = {10, 20, 30, 40}; ?',
        '#include <stdio.h>\nint main() {\n    int arr[] = {10, 20, 30, 40};\n    int count = sizeof(arr) / sizeof(arr[0]);\n    printf("%d\\n", count);\n    return 0;\n}',
        4, 'sizeof(arr) / sizeof(arr[0])', 'The compiler counts 4 elements in the initializer list, so arr has type int[4] (16 bytes). 16 / 4 = 4 elements!',
        [
            ('A', '16', False, 'Computed total byte size sizeof(arr) assuming 4-byte integers, but forgot division by sizeof(arr[0]).', 'Dividing by sizeof(arr[0]) converts byte count to element count: 16 / 4 = 4.'),
            ('B', '1', False, 'Thought arr decayed to a pointer so sizeof(arr) was sizeof(int*).', 'In the scope of its declaration, an array name does not decay inside the sizeof operator (§6.5.3.4#2).'),
            ('C', '4', True, 'The compiler infers size 4 from the initializer list. Total size (16 bytes) divided by element size (4 bytes) yields 4.', ''),
            ('D', 'Compilation error', False, 'Thought declaring an array without explicit bounds (int arr[]) is illegal.', 'Omitting the size when providing an initializer list is valid C syntax (§6.7.9#22).')
        ],
        'The compiler infers array size from the initializer list count. sizeof(arr)/sizeof(arr[0]) = 16 / 4 = 4.',
        'ISO/IEC 9899:1999 §6.7.9#22 (Array size deduction from initializer) & §6.5.3.4',
        "When an array of incomplete type is initialized with a brace-enclosed list, ISO C99 §6.7.9#22 states:\n'If an array of unknown size is initialized, its size is determined by the largest indexed element with an explicit initializer.'\n\nHere, '{10, 20, 30, 40}' provides 4 initializers, so 'arr' is completed with type 'int[4]'.\n\nNext, the idiom 'sizeof(arr) / sizeof(arr[0])' determines the element count at compile time:\n1. Under §6.5.3.4#2, the 'sizeof' operator does NOT convert an array operand to a pointer. Thus, 'sizeof(arr)' evaluates to the total byte size of the array: '4 * sizeof(int) = 4 * 4 = 16' bytes (on standard 32/64-bit systems).\n2. 'sizeof(arr[0])' is the size of one element: 'sizeof(int) = 4' bytes.\n3. '16 / 4 = 4'.\n\nThe program outputs '4'. This compile-time pattern is the universal idiom in C for finding array lengths without hardcoding magic numbers.",
        [
            (1, 3, 'Compiler infers arr type as int[4]; initializes elements {10, 20, 30, 40}.', {'arr_len': 4}, {'stack': [{'name': 'arr', 'type': 'int[4]', 'address': '0x7ffd10', 'value': '{10, 20, 30, 40}'}]}),
            (2, 4, 'Compile-time evaluation: sizeof(arr)=16, sizeof(arr[0])=4; 16 / 4 = 4; assign 4 to count.', {'count': 4}, {'stack': [{'name': 'arr', 'type': 'int[4]', 'address': '0x7ffd10', 'value': '{10, 20, 30, 40}'}, {'name': 'count', 'type': 'int', 'address': '0x7ffd20', 'value': '4'}]}),
            (3, 5, "printf prints '4\\n'.", {'stdout': '4'}, {'stack': [{'name': 'arr', 'type': 'int[4]', 'address': '0x7ffd10', 'value': '{10, 20, 30, 40}'}, {'name': 'count', 'type': 'int', 'address': '0x7ffd20', 'value': '4'}]})
        ]
    )

    # Q088: Array Out-of-Bounds Subscripting
    add_q(
        88, 'TOPIC_ARRAYS', 'Medium', 'Array Out-of-Bounds Subscripting',
        'What happens when executing arr[5] on an array of size 5?',
        '#include <stdio.h>\nint main() {\n    int arr[5] = {1, 2, 3, 4, 5};\n    printf("%d\\n", arr[5]);\n    return 0;\n}',
        4, 'arr[5]', 'Valid indices are 0 to 4! arr[5] accesses the 6th element outside array bounds, resulting in UNDEFINED BEHAVIOR!',
        [
            ('A', 'Compilation error: array index out of bounds', False, 'Believed C compilers reject out-of-bounds indices at compile time.', 'ISO C does not require compile-time rejection of out-of-bounds subscripting; it compiles cleanly with possible warnings.'),
            ('B', '5', False, 'Assumed arr[5] corresponds to the 5th element.', 'Because C is 0-indexed, the 5th element is arr[4]; arr[5] is past the end.'),
            ('C', '0', False, 'Thought out-of-bounds stack memory is automatically zeroed by the operating system.', 'Stack memory outside the array contains arbitrary leftover bits (garbage).'),
            ('D', 'Undefined Behavior (Accesses stack garbage or crashes)', True, 'C does not perform runtime array bounds checking. arr[5] evaluates to *(arr + 5), reading unallocated stack memory or causing a segmentation fault.', '')
        ],
        'C does not perform runtime bounds checking. Subscripting past the allocated boundary produces Undefined Behavior.',
        'ISO/IEC 9899:1999 §6.5.6#8 (Additive operators and pointer bounds) & Annex J.2',
        "In C, array subscripting 'arr[5]' is syntactic sugar for '*(arr + 5)'.\n\nISO C99 §6.5.6#8 defines pointer arithmetic rules:\n'If both the pointer operand and the result point to elements of the same array object, or one past the last element of the array object, the evaluation shall not produce an overflow; otherwise, the behavior is undefined.'\n\nWhile a pointer can legally point one past the last element ('arr + 5'), dereferencing that pointer with '*' violates §6.5.6#8 and results in undefined behavior (Annex J.2).\n\nKey pedagogical takeaways:\n1. C prioritizes execution speed over memory safety and deliberately omits runtime bounds checking.\n2. The compiler generates simple offset addition instructions. Reading 'arr[5]' reads the 4 bytes immediately following the array on the call stack (which may contain caller saved frame pointers, return addresses, or uninitialized garbage).\n3. Modern sanitizers (-fsanitize=address) flag this runtime violation immediately.",
        [
            (1, 3, 'Allocate arr[5] on stack at 0x7ffd10 (offsets 0..4, bytes 0..19).', {'arr': [1, 2, 3, 4, 5]}, {'stack': [{'name': 'arr', 'type': 'int[5]', 'address': '0x7ffd10', 'value': '{1, 2, 3, 4, 5}'}]}),
            (2, 4, 'Compute *(arr + 5) at address 0x7ffd24 (offset 20 bytes, past end of array).', {'invalid_address': '0x7ffd24'}, {'stack': [{'name': 'arr', 'type': 'int[5]', 'address': '0x7ffd10', 'value': '{1, 2, 3, 4, 5}'}]}),
            (3, 4, 'Dereference out-of-bounds stack location -> Undefined Behavior (reads garbage or causes memory fault).', {'status': 'Undefined Behavior'}, {'stack': [{'name': 'arr', 'type': 'int[5]', 'address': '0x7ffd10', 'value': '{1, 2, 3, 4, 5}'}]})
        ]
    )

    # Q089: Finding Maximum in Array Algorithm
    add_q(
        89, 'TOPIC_ARRAYS', 'Easy', 'Finding Maximum in Array Algorithm',
        'What is the output of the following program?',
        '#include <stdio.h>\nint main() {\n    int arr[] = {14, 5, 29, 11, 8};\n    int max = arr[0];\n    for (int i = 1; i < 5; i++) {\n        if (arr[i] > max) {\n            max = arr[i];\n        }\n    }\n    printf("%d\\n", max);\n    return 0;\n}',
        7, 'max = arr[i];', 'The loop updates max whenever an element is strictly greater: arr[0]=14, arr[2]=29 replaces 14, no higher value found: max ends at 29!',
        [
            ('A', '29', True, 'The algorithm initializes max to 14. At i=2, arr[2]=29 > 14, so max updates to 29. No subsequent element exceeds 29, so it prints 29.', ''),
            ('B', '14', False, 'Thought max never updated after initialization.', 'At i=2, the condition arr[2] > max (29 > 14) is true, updating max to 29.'),
            ('C', '8', False, 'Thought max stores the last element processed by the loop.', 'The conditional if-check prevents overwriting max with smaller elements.'),
            ('D', '5', False, 'Confused maximum search with minimum search.', "The '>' operator selects the largest value, not the smallest.")
        ],
        'Linear scan updates max to 29 when inspecting arr[2], which remains the global maximum. Prints 29.',
        'ISO/IEC 9899:1999 §6.8.5 (Iteration statements) & §6.8.4.1 (The if statement)',
        'This question traces the standard linear scan algorithm for finding the maximum value in an array:\n\n1. Initialization: \'max = arr[0] = 14\'. Starting with the first element ensures correct behavior even if all elements are negative.\n2. Iteration:\n   - i = 1: \'arr[1] = 5\'. \'5 > 14\' is false; \'max\' remains 14.\n   - i = 2: \'arr[2] = 29\'. \'29 > 14\' is true; \'max\' updates to 29.\n   - i = 3: \'arr[3] = 11\'. \'11 > 29\' is false; \'max\' remains 29.\n   - i = 4: \'arr[4] = 8\'. \'8 > 29\' is false; \'max\' remains 29.\n3. Loop termination: \'i = 5\', condition \'5 < 5\' is false.\n4. Output: \'printf("%d\\n", max)\' prints \'29\'.\n\nThe algorithm runs in O(n) time and O(1) auxiliary space, performing exactly n-1 comparisons.',
        [
            (1, 4, 'Initialize max to arr[0] (14); i=1: arr[1]=5 > 14 is false.', {'max': 14, 'i': 1}, {'stack': [{'name': 'max', 'type': 'int', 'address': '0x7ffd20', 'value': '14'}]}),
            (2, 7, 'i=2: arr[2]=29 > 14 is true -> max updated to 29.', {'max': 29, 'i': 2}, {'stack': [{'name': 'max', 'type': 'int', 'address': '0x7ffd20', 'value': '29'}]}),
            (3, 5, 'i=3 (11) and i=4 (8): neither exceeds 29; loop terminates at i=5.', {'max': 29, 'i': 5}, {'stack': [{'name': 'max', 'type': 'int', 'address': '0x7ffd20', 'value': '29'}]}),
            (4, 10, "printf prints '29\\n'.", {'stdout': '29'}, {'stack': [{'name': 'max', 'type': 'int', 'address': '0x7ffd20', 'value': '29'}]})
        ]
    )

    # Q090: Array Linear Search Index
    add_q(
        90, 'TOPIC_ARRAYS', 'Easy', 'Array Linear Search Index',
        'What index is printed when searching for target = 40?',
        '#include <stdio.h>\nint main() {\n    int arr[5] = {10, 20, 30, 40, 50};\n    int target = 40, found_idx = -1;\n    for (int i = 0; i < 5; i++) {\n        if (arr[i] == target) {\n            found_idx = i;\n            break;\n        }\n    }\n    printf("%d\\n", found_idx);\n    return 0;\n}',
        7, 'found_idx = i;', '40 is the 4th element, which corresponds to index 3 in 0-indexed C! When found, the loop breaks immediately and prints 3!',
        [
            ('A', '4', False, 'Confused 0-based indexing with 1-based ordinal position (40 is the 4th element).', 'In 0-indexed C, the 4th element is stored at index 3.'),
            ('B', '-1', False, 'Thought target was not found or loop condition failed.', 'Target 40 exists at index 3, overwriting the default sentinel -1.'),
            ('C', '3', True, 'Target 40 matches arr[3] (indices: arr[0]=10, arr[1]=20, arr[2]=30, arr[3]=40). found_idx is assigned 3 and break exits immediately.', ''),
            ('D', '40', False, 'Mistook the variable printed as the element value rather than its index.', 'printf prints found_idx, not arr[found_idx].')
        ],
        'Linear search matches target 40 at index 3, sets found_idx = 3, and breaks. Prints 3.',
        'ISO/IEC 9899:1999 §6.8.6.3 (The break statement)',
        'This program implements linear search with early termination:\n\n1. Setup: \'arr\' holds {10, 20, 30, 40, 50}. \'target = 40\', \'found_idx = -1\' (sentinel value indicating not found).\n2. Loop iterations:\n   - i = 0: \'arr[0] = 10 == 40\' -> false.\n   - i = 1: \'arr[1] = 20 == 40\' -> false.\n   - i = 2: \'arr[2] = 30 == 40\' -> false.\n   - i = 3: \'arr[3] = 40 == 40\' -> true!\n     - \'found_idx = 3;\'\n     - \'break;\' terminates the innermost enclosing iteration statement immediately (§6.8.6.3).\n3. Subscripts 4 is never evaluated.\n4. \'printf("%d\\n", found_idx);\' prints \'3\'.\n\nThis demonstrates both C\'s 0-based subscript mapping and how \'break\' prevents unnecessary iterations once a target is found.',
        [
            (1, 4, 'Initialize target=40, found_idx=-1.', {'target': 40, 'found_idx': -1}, {'stack': [{'name': 'target', 'type': 'int', 'address': '0x7ffd20', 'value': '40'}, {'name': 'found_idx', 'type': 'int', 'address': '0x7ffd24', 'value': '-1'}]}),
            (2, 6, 'i=0, 1, 2: condition arr[i] == 40 is false; loop continues.', {'i': 2, 'found_idx': -1}, {'stack': [{'name': 'target', 'type': 'int', 'address': '0x7ffd20', 'value': '40'}, {'name': 'found_idx', 'type': 'int', 'address': '0x7ffd24', 'value': '-1'}]}),
            (3, 7, 'i=3: arr[3] (40) == target (40) is true; assign found_idx = 3; execute break.', {'found_idx': 3}, {'stack': [{'name': 'target', 'type': 'int', 'address': '0x7ffd20', 'value': '40'}, {'name': 'found_idx', 'type': 'int', 'address': '0x7ffd24', 'value': '3'}]}),
            (4, 11, "printf prints found_idx: '3\\n'.", {'stdout': '3'}, {'stack': [{'name': 'target', 'type': 'int', 'address': '0x7ffd20', 'value': '40'}, {'name': 'found_idx', 'type': 'int', 'address': '0x7ffd24', 'value': '3'}]})
        ]
    )

    # Q091: Sequential Array Accumulation Mutation
    add_q(
        91, 'TOPIC_ARRAYS', 'Medium', 'Sequential Array Accumulation Mutation',
        'What is the output of the following program?',
        '#include <stdio.h>\nint main() {\n    int a[4] = {1, 2, 3, 4};\n    for (int i = 1; i < 4; i++) {\n        a[i] += a[i - 1];\n    }\n    printf("%d %d %d %d\\n", a[0], a[1], a[2], a[3]);\n    return 0;\n}',
        5, 'a[i] += a[i - 1];', 'Prefix sum calculation: each step reads the ALREADY UPDATED previous element! a[1]=2+1=3, a[2]=3+3=6, a[3]=4+6=10: prints 1 3 6 10!',
        [
            ('A', '1 3 5 7', False, 'Computed using original array values instead of the in-place mutated values.', 'Because a[i-1] was updated in the prior iteration, each step accumulates all previous values.'),
            ('B', '1 3 6 10', True, 'In-place prefix sum: a[1]=2+1=3; then a[2]=3+3=6 (using newly updated a[1]); then a[3]=4+6=10. Outputs 1 3 6 10.', ''),
            ('C', '1 2 3 4', False, 'Thought the loop did not mutate array memory.', 'Array elements mutate in place on the stack.'),
            ('D', '10 10 10 10', False, 'Thought the final sum was broadcast across all elements.', 'Only subsequent elements accumulate earlier ones; a[0], a[1], a[2] retain their accumulated sums.')
        ],
        'In-place prefix accumulation mutates elements sequentially: a[1]=3, a[2]=6, a[3]=10. Prints 1 3 6 10.',
        'ISO/IEC 9899:1999 §6.5.16.2 (Compound assignment operators)',
        "This snippet computes the prefix sum (cumulative sum) in-place:\n\nInitially: a = {1, 2, 3, 4}.\nThe loop index starts at i = 1 (leaving a[0] = 1 untouched):\n- i = 1: 'a[1] += a[0]' -> 'a[1] = 2 + 1 = 3'.\n  Array is now: {1, 3, 3, 4}.\n- i = 2: 'a[2] += a[1]' -> 'a[2] = 3 + 3 = 6'.\n  Notice that this reads the NEW value of a[1] (3), not the original value (2)!\n  Array is now: {1, 3, 6, 4}.\n- i = 3: 'a[3] += a[2]' -> 'a[3] = 4 + 6 = 10'.\n  Reads the NEW value of a[2] (6).\n  Array is now: {1, 3, 6, 10}.\n- i = 4: loop terminates.\n\nThe printf statement outputs '1 3 6 10'. The critical trap is recognizing sequential data dependency: mutating elements in-place cascades forward into subsequent iterations.",
        [
            (1, 3, 'Initialize a[4] = {1, 2, 3, 4} on the stack.', {'a': [1, 2, 3, 4]}, {'stack': [{'name': 'a', 'type': 'int[4]', 'address': '0x7ffd10', 'value': '{1, 2, 3, 4}'}]}),
            (2, 5, 'i=1: a[1] += a[0] -> 2 + 1 = 3; array becomes {1, 3, 3, 4}.', {'a[1]': 3}, {'stack': [{'name': 'a', 'type': 'int[4]', 'address': '0x7ffd10', 'value': '{1, 3, 3, 4}'}]}),
            (3, 5, 'i=2: a[2] += a[1] -> 3 + 3 = 6; array becomes {1, 3, 6, 4}.', {'a[2]': 6}, {'stack': [{'name': 'a', 'type': 'int[4]', 'address': '0x7ffd10', 'value': '{1, 3, 6, 4}'}]}),
            (4, 5, 'i=3: a[3] += a[2] -> 4 + 6 = 10; array becomes {1, 3, 6, 10}.', {'a[3]': 10}, {'stack': [{'name': 'a', 'type': 'int[4]', 'address': '0x7ffd10', 'value': '{1, 3, 6, 10}'}]}),
            (5, 7, "printf prints '1 3 6 10\\n'.", {'stdout': '1 3 6 10'}, {'stack': [{'name': 'a', 'type': 'int[4]', 'address': '0x7ffd10', 'value': '{1, 3, 6, 10}'}]})
        ]
    )

    # Q092: 2D Array Subscript Coordinates (Row, Column)
    add_q(
        92, 'TOPIC_ARRAYS', 'Easy', '2D Array Subscript Coordinates (Row, Column)',
        'Given int m[2][3] = {{10, 20, 30}, {40, 50, 60}}; what is m[1][2]?',
        '#include <stdio.h>\nint main() {\n    int m[2][3] = {{10, 20, 30}, {40, 50, 60}};\n    printf("%d\\n", m[1][2]);\n    return 0;\n}',
        4, 'm[1][2]', 'm[row][col]: row 1 selects {40, 50, 60}; col 2 selects the 3rd element: 60!',
        [
            ('A', '50', False, 'Selected column 1 instead of column 2 (0-indexed: col 0=40, col 1=50, col 2=60).', 'm[1][1] is 50, whereas m[1][2] accesses 60.'),
            ('B', '30', False, 'Selected row 0 instead of row 1 (m[0][2] is 30).', 'Row index 1 accesses the second row.'),
            ('C', '40', False, 'Selected column 0 instead of column 2 (m[1][0] is 40).', 'Column index 2 selects the 3rd element.'),
            ('D', '60', True, 'In m[row][col], row index 1 selects the second row {40, 50, 60}, and column index 2 selects the third element (60).', '')
        ],
        'Row 1 is {40, 50, 60}; column 2 is 60. Prints 60.',
        'ISO/IEC 9899:1999 §6.5.2.1 (Multi-dimensional array subscripting)',
        "A 2D array in C is defined as an array of arrays (§6.5.2.1):\n'int m[2][3]' is an array of 2 elements, where each element is an 'int[3]'.\n\nInitialization assigns:\n- Row 0: 'm[0]' = {10, 20, 30} (indices: m[0][0]=10, m[0][1]=20, m[0][2]=30).\n- Row 1: 'm[1]' = {40, 50, 60} (indices: m[1][0]=40, m[1][1]=50, m[1][2]=60).\n\nEvaluation of 'm[1][2]':\n1. 'm[1]' evaluates to the array at index 1: '{40, 50, 60}'.\n2. '[2]' subscripts into that subarray, selecting index 2 (the 3rd element).\n3. 'm[1][2] = 60'.\n\nIn pointer arithmetic form: '*(*(m + 1) + 2)'.\nRow offset 1 jumps by '3 * sizeof(int)' (12 bytes), and column offset 2 jumps by '2 * sizeof(int)' (8 bytes), arriving at element 60.",
        [
            (1, 3, 'Allocate m[2][3] in row-major order: {10, 20, 30, 40, 50, 60}.', {'m': [[10, 20, 30], [40, 50, 60]]}, {'stack': [{'name': 'm', 'type': 'int[2][3]', 'address': '0x7ffd10', 'value': '{{10, 20, 30}, {40, 50, 60}}'}]}),
            (2, 4, 'Subscript m[1][2]: row offset 1 -> {40, 50, 60}; col offset 2 -> 60.', {'val': 60}, {'stack': [{'name': 'm', 'type': 'int[2][3]', 'address': '0x7ffd10', 'value': '{{10, 20, 30}, {40, 50, 60}}'}]}),
            (3, 4, "printf prints '60\\n'.", {'stdout': '60'}, {'stack': [{'name': 'm', 'type': 'int[2][3]', 'address': '0x7ffd10', 'value': '{{10, 20, 30}, {40, 50, 60}}'}]})
        ]
    )

    # Q093: 2D Array Matrix Elements Summation
    add_q(
        93, 'TOPIC_ARRAYS', 'Medium', '2D Array Matrix Elements Summation',
        'What is the output of the following program?',
        '#include <stdio.h>\nint main() {\n    int m[2][2] = {{1, 2}, {3, 4}};\n    int sum = 0;\n    for (int r = 0; r < 2; r++) {\n        for (int c = 0; c < 2; c++) {\n            sum += m[r][c];\n        }\n    }\n    printf("%d\\n", sum);\n    return 0;\n}',
        7, 'sum += m[r][c];', 'Nested loops visit all rows and columns: 1 + 2 + 3 + 4 = 10!',
        [
            ('A', '5', False, 'Only summed the main diagonal elements (1 + 4 = 5).', 'The inner loop runs for every column c (0 and 1), visiting all 4 elements.'),
            ('B', '6', False, 'Only summed row 1 (3 + 4 = 7) or column 1 (2 + 4 = 6).', 'Both rows r=0 and r=1 are accumulated into sum.'),
            ('C', '10', True, 'The nested loops iterate over all elements: (1 + 2) + (3 + 4) = 10.', ''),
            ('D', '4', False, 'Only captured the value of the last element m[1][1].', "sum accumulates all elements using '+='.")
        ],
        'Nested loops traverse all 4 matrix elements to compute 1 + 2 + 3 + 4 = 10. Prints 10.',
        'ISO/IEC 9899:1999 §6.8.5 (Iteration statements)',
        "This program demonstrates row-major 2D array traversal using nested loops:\n\nThe outer loop controls rows 'r' from 0 to 1.\nThe inner loop controls columns 'c' from 0 to 1.\n\nIteration trace:\n- r = 0, c = 0: 'sum += m[0][0]' -> 0 + 1 = 1.\n- r = 0, c = 1: 'sum += m[0][1]' -> 1 + 2 = 3.\n- r = 1, c = 0: 'sum += m[1][0]' -> 3 + 3 = 6.\n- r = 1, c = 1: 'sum += m[1][1]' -> 6 + 4 = 10.\n\nBecause the inner loop traverses columns ('c'), memory is accessed in sequential, contiguous order ('m[0][0]', 'm[0][1]', 'm[1][0]', 'm[1][1]'). This matches C's row-major memory layout and exhibits optimal CPU cache locality.",
        [
            (1, 4, 'Initialize sum = 0.', {'sum': 0}, {'stack': [{'name': 'sum', 'type': 'int', 'address': '0x7ffd20', 'value': '0'}]}),
            (2, 7, 'r=0: inner loop accumulates m[0][0]=1 and m[0][1]=2 -> sum = 3.', {'sum': 3, 'r': 0}, {'stack': [{'name': 'sum', 'type': 'int', 'address': '0x7ffd20', 'value': '3'}]}),
            (3, 7, 'r=1: inner loop accumulates m[1][0]=3 and m[1][1]=4 -> sum = 10.', {'sum': 10, 'r': 1}, {'stack': [{'name': 'sum', 'type': 'int', 'address': '0x7ffd20', 'value': '10'}]}),
            (4, 10, "printf prints '10\\n'.", {'stdout': '10'}, {'stack': [{'name': 'sum', 'type': 'int', 'address': '0x7ffd20', 'value': '10'}]})
        ]
    )

    # Q094: Row-Major Contiguous Storage of 2D Arrays
    add_q(
        94, 'TOPIC_ARRAYS', 'Medium', 'Row-Major Contiguous Storage of 2D Arrays',
        'How are multidimensional array elements laid out in physical memory in C?',
        '#include <stdio.h>\nint main() {\n    int m[2][3] = {{1, 2, 3}, {4, 5, 6}};\n    int *p = &m[0][0];\n    printf("%d %d\\n", *(p + 2), *(p + 3));\n    return 0;\n}',
        3, 'int m[2][3] = {{1, 2, 3}, {4, 5, 6}};', 'In C, multidimensional arrays are laid out in ROW-MAJOR order: row 0 elements are contiguous in RAM, followed immediately by row 1 elements: *(p+2)=3, *(p+3)=4!',
        [
            ('A', 'Row-major order (row 0 elements consecutively, then row 1 elements)', True, 'C specifies row-major layout: elements of a row are contiguous, and row 1 immediately follows row 0. Thus *(p+2)=3 and *(p+3)=4.', ''),
            ('B', 'Column-major order (column 0 elements consecutively, then column 1)', False, 'Confused C with Fortran, MATLAB, or Julia which store matrices column by column.', 'C language standard strictly mandates row-major contiguous storage.'),
            ('C', 'Scattered non-contiguous heap memory blocks', False, 'Assumed 2D arrays in C are arrays of heap pointers like in Java.', 'A 2D array in C is a single contiguous block of stack memory.'),
            ('D', 'An array of pointers pointing to separate row buffers', False, "Confused 'int m[2][3]' with 'int *m[2]'.", "'int m[2][3]' has zero pointer overhead; it is flat contiguous memory.")
        ],
        'C multidimensional arrays are laid out in contiguous row-major order: row 0 followed immediately by row 1.',
        'ISO/IEC 9899:1999 §6.2.5#20 & §6.5.2.1 (Contiguous row-major storage)',
        "ISO C99 §6.2.5#20 specifies that array types describe a contiguously allocated nonempty set of objects.\nFor multidimensional arrays ('arrays of arrays'), this guarantee enforces ROW-MAJOR order.\n\nFor 'int m[2][3] = {{1, 2, 3}, {4, 5, 6}}':\nMemory address order:\n- m[0][0] = 1 (address: base + 0)\n- m[0][1] = 2 (address: base + 4)\n- m[0][2] = 3 (address: base + 8)\n- m[1][0] = 4 (address: base + 12)  <-- Row 1 starts immediately after row 0!\n- m[1][1] = 5 (address: base + 16)\n- m[1][2] = 6 (address: base + 20)\n\nWhen a flat pointer 'int *p = &m[0][0]' traverses memory linearly:\n- '*(p + 2)' accesses the 3rd element: 'm[0][2] = 3'.\n- '*(p + 3)' crosses the row boundary and accesses 'm[1][0] = 4'.\n\nThe program outputs '3 4'. Understanding row-major ordering is fundamental for cache-friendly algorithms and pointer arithmetic.",
        [
            (1, 3, 'Allocate m[2][3] in contiguous row-major block of 6 ints (24 bytes).', {'m_layout': [1, 2, 3, 4, 5, 6]}, {'stack': [{'name': 'm', 'type': 'int[2][3]', 'address': '0x7ffd10', 'value': '{{1, 2, 3}, {4, 5, 6}}'}]}),
            (2, 4, 'Pointer p points to base address &m[0][0].', {'p': '0x7ffd10'}, {'stack': [{'name': 'p', 'type': 'int*', 'address': '0x7ffd30', 'value': '0x7ffd10', 'pointsTo': 'm[0][0]'}]}),
            (3, 5, '*(p + 2) reads m[0][2] (3); *(p + 3) crosses row boundary to read m[1][0] (4).', {'deref_2': 3, 'deref_3': 4}, {'stack': [{'name': 'p', 'type': 'int*', 'address': '0x7ffd30', 'value': '0x7ffd10', 'pointsTo': 'm[0][0]'}]}),
            (4, 5, "printf prints '3 4\\n'.", {'stdout': '3 4'}, {'stack': []})
        ]
    )

    # Q095: String Null Terminator in Character Arrays
    add_q(
        95, 'TOPIC_ARRAYS', 'Easy', 'String Null Terminator in Character Arrays',
        'What is the size of the array char s[] = "apple"; ?',
        '#include <stdio.h>\nint main() {\n    char s[] = "apple";\n    printf("%zu\\n", sizeof(s));\n    return 0;\n}',
        3, 'char s[] = "apple";', "In C, string literals automatically append a NULL TERMINATOR ('\\0')! 'apple' has 5 letters + 1 null terminator = 6 bytes!",
        [
            ('A', '5', False, "Counted only visible characters and forgot the terminating null character '\\0'.", "String literals in C always append '\\0'; sizeof counts all allocated bytes including '\\0'."),
            ('B', '4', False, 'Confused array size with sizeof(char*).', 's is an array object, not a pointer variable.'),
            ('C', '7', False, 'Thought an extra newline or alignment byte was included.', "Only the 5 letters plus '\\0' are allocated (6 bytes)."),
            ('D', '6', True, '"apple" contains 5 characters plus an implicit terminating null character \'\\0\', so sizeof(s) evaluates to 6 bytes.', '')
        ],
        "String literals automatically include a terminating '\\0'. 'apple' requires 5 + 1 = 6 bytes.",
        'ISO/IEC 9899:1999 §6.4.5#5 (String literal termination with null character)',
        'Under ISO C99 §6.4.5#5:\n\'In translation phase 7, a byte or code of value zero is appended to each multibyte character sequence that results from a string literal or literals.\'\n\nWhen initializing a character array of unknown size from a string literal (§6.7.9#14):\n\'char s[] = "apple";\'\n\nThe compiler deduces the size of \'s\' from the character count plus the appended null terminator \'\\0\':\n- Index 0: \'a\'\n- Index 1: \'p\'\n- Index 2: \'p\'\n- Index 3: \'l\'\n- Index 4: \'e\'\n- Index 5: \'\\0\'\n\nTotal elements = 6. Since \'sizeof(char)\' is strictly 1 byte by definition (§6.5.3.4#4), \'sizeof(s)\' is \'6 * 1 = 6\'.\n\nThe program outputs \'6\'. Neglecting the null terminator is the #1 cause of off-by-one buffer allocation bugs in C.',
        [
            (1, 3, "Deduce char s[6] = {'a', 'p', 'p', 'l', 'e', '\\0'} on the stack.", {'s_bytes': 6}, {'stack': [{'name': 's', 'type': 'char[6]', 'address': '0x7ffd10', 'value': '"apple\\0"'}]}),
            (2, 4, 'Compile-time evaluation: sizeof(s) = 6.', {'sizeof_s': 6}, {'stack': [{'name': 's', 'type': 'char[6]', 'address': '0x7ffd10', 'value': '"apple\\0"'}]}),
            (3, 4, "printf prints '6\\n'.", {'stdout': '6'}, {'stack': [{'name': 's', 'type': 'char[6]', 'address': '0x7ffd10', 'value': '"apple\\0"'}]})
        ]
    )

    # Q096: Difference Between sizeof and strlen
    add_q(
        96, 'TOPIC_ARRAYS', 'Easy', 'Difference Between sizeof and strlen',
        'What is printed by this program?',
        '#include <stdio.h>\n#include <string.h>\nint main() {\n    char str[] = "hello";\n    printf("%zu %zu\\n", sizeof(str), strlen(str));\n    return 0;\n}',
        5, 'sizeof(str), strlen(str)', "sizeof measures total allocated bytes including '\\0' (6); strlen counts characters up to (excluding) '\\0' (5)! Outputs 6 5!",
        [
            ('A', '5 5', False, 'Thought sizeof ignored the null terminator.', 'sizeof counts total storage allocated for the array (6 bytes).'),
            ('B', '6 5', True, "sizeof(str) evaluates to total array memory (6 bytes including '\\0'); strlen(str) scans for '\\0' and returns 5.", ''),
            ('C', '5 6', False, 'Inverted the roles of sizeof and strlen.', 'sizeof measures storage capacity (6); strlen measures string length (5).'),
            ('D', '6 6', False, 'Thought strlen counted the terminating null character.', 'strlen counts characters up to, but not including, the terminating null character.')
        ],
        "sizeof(str) gives total bytes (6); strlen(str) gives character count before '\\0' (5). Prints 6 5.",
        'ISO/IEC 9899:1999 §6.5.3.4 (sizeof) & §7.21.6.3 (strlen)',
        'This question highlights the fundamental distinction between \'sizeof\' and \'strlen\' in C:\n\n1. \'sizeof\' is a compile-time operator (§6.5.3.4):\n   - It inspects the type of the operand.\n   - \'str\' has type \'char[6]\' (5 letters + \'\\0\').\n   - \'sizeof(str)\' evaluates at compile time to 6.\n\n2. \'strlen\' is a runtime library function (§7.21.6.3):\n   - It receives a pointer to \'char\' (\'const char *s\').\n   - It iterates through memory starting at \'s\', incrementing a counter until it encounters the first \'\\0\' byte.\n   - For "hello\\0", it counts \'h\', \'e\', \'l\', \'l\', \'o\' (5 characters) and stops.\n   - \'strlen(str)\' returns 5.\n\nTherefore, \'printf("%zu %zu\\n", sizeof(str), strlen(str))\' outputs \'6 5\'.\nRemember: sizeof is storage capacity; strlen is current content length.',
        [
            (1, 4, "Allocate str[6] = {'h', 'e', 'l', 'l', 'o', '\\0'} on stack.", {'str_len': 6}, {'stack': [{'name': 'str', 'type': 'char[6]', 'address': '0x7ffd10', 'value': '"hello\\0"'}]}),
            (2, 5, 'Compile-time evaluation: sizeof(str) = 6.', {'sizeof': 6}, {'stack': [{'name': 'str', 'type': 'char[6]', 'address': '0x7ffd10', 'value': '"hello\\0"'}]}),
            (3, 5, "Runtime evaluation: strlen(str) scans 5 characters before hitting '\\0'; returns 5.", {'strlen': 5}, {'stack': [{'name': 'str', 'type': 'char[6]', 'address': '0x7ffd10', 'value': '"hello\\0"'}]}),
            (4, 5, "printf prints '6 5\\n'.", {'stdout': '6 5'}, {'stack': [{'name': 'str', 'type': 'char[6]', 'address': '0x7ffd10', 'value': '"hello\\0"'}]})
        ]
    )

    # Q097: Missing Null Terminator in Sized Array
    add_q(
        97, 'TOPIC_ARRAYS', 'Tricky', 'Missing Null Terminator in Sized Array',
        'What happens when declaring: char s[5] = "hello"; and calling strlen(s)?',
        '#include <stdio.h>\n#include <string.h>\nint main() {\n    char s[5] = "hello";\n    printf("%zu\\n", strlen(s));\n    return 0;\n}',
        4, 'char s[5] = "hello";', "In C, allocating char s[5] for 5 chars is VALID syntax, but leaves NO ROOM for '\\0'! strlen(s) overreads into adjacent stack memory: UNDEFINED BEHAVIOR!",
        [
            ('A', 'Compilation error', False, 'Thought the compiler rejects an array size that cannot fit the null terminator.', "ISO C99 §6.7.9#14 explicitly permits omitting '\\0' if the array size equals the string literal length; it is valid C!"),
            ('B', 'Prints 5', False, 'Thought strlen knows the array size is 5 and stops.', 'strlen accepts only a pointer and has no knowledge of array bounds; it scans until finding 0.'),
            ('C', "Undefined Behavior (Buffer overread searching for '\\0')", True, 's[5] stores all 5 characters without a null terminator. When strlen(s) is called, it scans past array bounds searching for 0, producing undefined behavior.', ''),
            ('D', 'Prints 0', False, 'Thought an un-null-terminated string returns length 0.', 'strlen only returns 0 if the initial character is null.')
        ],
        "Array size 5 fits 'h','e','l','l','o' but discards '\\0'. Calling strlen causes an out-of-bounds read (Undefined Behavior).",
        'ISO/IEC 9899:1999 §6.7.9#14 (Character array initialization without null terminator)',
        'A notorious trap in C:\nISO C99 §6.7.9#14 explicitly allows initializing a character array whose size equals the length of the string literal without the terminating null character:\n\'An array of character type may be initialized by a character string literal... Successive characters of the character string literal (including the terminating null character if there is room or if the array is of unknown size) initialize the elements of the array.\'\n\nNotice: \'if there is room\'! Here, \'s\' has size 5, and "hello" has 5 characters. There is NO ROOM for \'\\0\'.\nTherefore, \'s\' contains: {\'h\', \'e\', \'l\', \'l\', \'o\'} with NO trailing \'\\0\'.\n\nIn C, a \'string\' is defined as a contiguous sequence of characters terminated by the first null character (§7.1.1). Because \'s\' does not contain a null character, \'s\' is NOT a valid C string!\n\nWhen \'strlen(s)\' is called:\n1. \'strlen\' scans byte by byte searching for value 0.\n2. It reads past \'s[4]\', reading whatever random bytes lie next on the stack.\n3. This buffer overread violates memory safety and results in Undefined Behavior (Annex J.2). In practice, it may return 5 + garbage length or crash with a segmentation fault.',
        [
            (1, 4, "Allocate s[5] on stack initialized to {'h', 'e', 'l', 'l', 'o'}; no room for '\\0'.", {'s': ['h', 'e', 'l', 'l', 'o']}, {'stack': [{'name': 's', 'type': 'char[5]', 'address': '0x7ffd10', 'value': "{'h', 'e', 'l', 'l', 'o'}"}]}),
            (2, 5, "strlen(s) reads s[0] through s[4]; finds no '\\0'.", {'scanned': 5, 'null_found': False}, {'stack': [{'name': 's', 'type': 'char[5]', 'address': '0x7ffd10', 'value': "{'h', 'e', 'l', 'l', 'o'}"}]}),
            (3, 5, 'strlen continues reading past allocated bounds of s -> Undefined Behavior.', {'status': 'Undefined Behavior (Buffer overread)'}, {'stack': [{'name': 's', 'type': 'char[5]', 'address': '0x7ffd10', 'value': "{'h', 'e', 'l', 'l', 'o'}"}]})
        ]
    )

    # Q098: Mutating Elements in Character Array
    add_q(
        98, 'TOPIC_ARRAYS', 'Easy', 'Mutating Elements in Character Array',
        'What is the output of the following program?',
        '#include <stdio.h>\nint main() {\n    char word[] = "cat";\n    word[0] = \'b\';\n    printf("%s\\n", word);\n    return 0;\n}',
        4, "word[0] = 'b';", 'word is an ARRAY allocated on the stack, not a string literal pointer! Stack arrays are fully mutable: \'c\' becomes \'b\', printing "bat"!',
        [
            ('A', 'bat', True, 'word is an array allocated on the writable stack initialized with copy of "cat". Mutating word[0] to \'b\' changes the string to "bat".', ''),
            ('B', 'Segmentation fault (Crash)', False, 'Confused char word[] with char *word = "cat", which points to read-only memory.', "'char word[]' allocates a mutable stack buffer, whereas 'char *' points to immutable string literal storage."),
            ('C', 'cat', False, 'Thought string characters cannot be modified in C.', 'Stack-allocated arrays are completely mutable.'),
            ('D', 'Compilation error', False, 'Thought subscript assignment on char array is illegal syntax.', 'Subscript assignment on non-const arrays is standard valid C.')
        ],
        "Array declaration 'char word[]' creates a mutable stack copy. Mutating word[0] yields 'bat'.",
        'ISO/IEC 9899:1999 §6.7.9 (Array initialization) vs §6.4.5 (String literal modification)',
        'This question tests the critical difference between character arrays and string literal pointers:\n\n1. \'char *p = "cat";\':\n   - \'p\' points directly to the string literal stored in read-only memory (.rodata segment).\n   - Attempting \'p[0] = \'b\';\' triggers Undefined Behavior (typically a segmentation fault).\n\n2. \'char word[] = "cat";\':\n   - \'word\' is an array of 4 chars allocated on the local call STACK.\n   - The bytes \'c\', \'a\', \'t\', \'\\0\' are copied from read-only memory into this writable stack buffer during function entry.\n   - \'word[0] = \'b\';\' modifies the local stack memory at offset 0.\n   - \'word\' now contains \'b\', \'a\', \'t\', \'\\0\'.\n\nWhen \'printf("%s\\n", word);\' executes, it reads from the stack buffer and outputs \'bat\'.\nAlways remember: \'char arr[]\' is mutable stack memory; \'char *ptr = "..."\' points to immutable string literals.',
        [
            (1, 3, "Allocate char word[4] on stack initialized to {'c', 'a', 't', '\\0'}.", {'word': 'cat'}, {'stack': [{'name': 'word', 'type': 'char[4]', 'address': '0x7ffd10', 'value': '"cat\\0"'}]}),
            (2, 4, "word[0] = 'b': overwrite index 0 on stack buffer; word becomes {'b', 'a', 't', '\\0'}.", {'word': 'bat'}, {'stack': [{'name': 'word', 'type': 'char[4]', 'address': '0x7ffd10', 'value': '"bat\\0"'}]}),
            (3, 5, "printf prints string at word: 'bat\\n'.", {'stdout': 'bat'}, {'stack': [{'name': 'word', 'type': 'char[4]', 'address': '0x7ffd10', 'value': '"bat\\0"'}]})
        ]
    )

    # Q099: Embedded Null Terminator String Truncation
    add_q(
        99, 'TOPIC_ARRAYS', 'Medium', 'Embedded Null Terminator String Truncation',
        'What is printed by this printf statement?',
        '#include <stdio.h>\nint main() {\n    char str[] = "pro\\0gram";\n    printf("%s\\n", str);\n    return 0;\n}',
        3, 'char str[] = "pro\\0gram";', 'printf with %s stops printing at the FIRST null terminator (\'\\0\')! It outputs "pro" and ignores the rest of the array!',
        [
            ('A', 'program', False, "Thought '\\0' was ignored or treated as literal characters.", "'\\0' is the string terminator; C string functions terminate immediately upon encountering it."),
            ('B', 'pro program', False, 'Thought the string resumed after the null character.', 'Standard library string functions cannot see beyond the first null character.'),
            ('C', 'Compilation error', False, "Believed embedded '\\0' in a string literal is invalid syntax.", "Embedded escape sequences like '\\0' are completely valid standard C (§6.4.4.4)."),
            ('D', 'pro', True, "%s format specifier outputs characters sequentially until encountering the first '\\0' byte. It stops after 'pro'.", '')
        ],
        "%s stops output upon encountering the first '\\0' byte. Only 'pro' is printed.",
        'ISO/IEC 9899:1999 §7.1.1 (Definition of string) & §7.21.6.1 (%s conversion specifier)',
        'In C, a string is formally defined by ISO C99 §7.1.1:\n\'A string is a contiguous sequence of characters terminated by and including the first null character.\'\n\nIn this program:\n- \'char str[] = "pro\\0gram";\' allocates an array of 9 bytes:\n  {\'p\', \'r\', \'o\', \'\\0\', \'g\', \'r\', \'a\', \'m\', \'\\0\'}.\n- While the array has 9 elements, the \'string\' represented by \'str\' ends at index 3 (\'\\0\').\n\nWhen \'printf("%s\\n", str)\' executes:\n- The \'%s\' conversion specifier reads bytes starting from \'str\' until it encounters a null character (§7.21.6.1).\n- It outputs \'p\', \'r\', \'o\'.\n- At index 3, it reads \'\\0\' and immediately stops printing.\n- The remaining bytes (\'g\', \'r\', \'a\', \'m\', \'\\0\') remain in memory but are completely ignored by \'%s\'.\n\nThe output is \'pro\'. This demonstrates how C strings rely on in-band signaling (sentinel byte) rather than explicit length headers.',
        [
            (1, 3, "Allocate str[9] on stack: {'p', 'r', 'o', '\\0', 'g', 'r', 'a', 'm', '\\0'}.", {'str_bytes': 9}, {'stack': [{'name': 'str', 'type': 'char[9]', 'address': '0x7ffd10', 'value': "{'p','r','o','\\0','g','r','a','m','\\0'}"}]}),
            (2, 4, "printf %s prints 'p', 'r', 'o'; encounters '\\0' at index 3 and terminates printing.", {'printed': 'pro'}, {'stack': [{'name': 'str', 'type': 'char[9]', 'address': '0x7ffd10', 'value': "{'p','r','o','\\0','g','r','a','m','\\0'}"}]}),
            (3, 4, "printf outputs 'pro\\n'.", {'stdout': 'pro'}, {'stack': [{'name': 'str', 'type': 'char[9]', 'address': '0x7ffd10', 'value': "{'p','r','o','\\0','g','r','a','m','\\0'}"}]})
        ]
    )

    # Q100: Modifying Array Elements Inside Function
    add_q(
        100, 'TOPIC_ARRAYS', 'Medium', 'Modifying Array Elements Inside Function',
        'What is the output of the following program?',
        '#include <stdio.h>\nvoid double_first(int arr[]) {\n    arr[0] *= 2;\n}\nint main() {\n    int nums[3] = {5, 10, 15};\n    double_first(nums);\n    printf("%d\\n", nums[0]);\n    return 0;\n}',
        3, 'arr[0] *= 2;', 'When an array is passed as a function argument, it DECAYS to a pointer to its first element! Mutating arr[0] modifies nums[0] in main: 5 becomes 10!',
        [
            ('A', '5', False, 'Thought C passed arrays by value (making a copy of all elements).', 'Arrays cannot be passed by value in C; passing an array passes the base address, allowing in-place mutation.'),
            ('B', '10', True, 'Arrays decay to pointers when passed to functions. arr[0] *= 2 modifies the original array nums[0] in main (5 * 2 = 10).', ''),
            ('C', '0', False, 'Thought the pointer operation cleared the element.', '5 is multiplied by 2, yielding 10.'),
            ('D', 'Compilation error', False, 'Thought passing an array to a function parameter declared as int arr[] is invalid.', "Array parameter syntax 'int arr[]' is standard syntactic sugar for 'int *arr'.")
        ],
        'Array parameters decay to pointers to the first element. Mutating arr[0] modifies nums[0] in caller frame. Prints 10.',
        'ISO/IEC 9899:1999 §6.3.2.1#3 (Array decay to pointer) & §6.7.5.3#7 (Parameter adjustment)',
        'A central principle of C programming: arrays NEVER pass by value into functions.\n\n1. Array Decay (§6.3.2.1#3):\n   \'Except when it is the operand of sizeof... an expression that has type \'array of type\' is converted to an expression with type \'pointer to type\' that points to the initial element of the array object.\'\n\n2. Parameter Adjustment (§6.7.5.3#7):\n   In a function declaration, a parameter declared with array type \'int arr[]\' is automatically adjusted by the compiler to pointer type \'int *arr\'.\n\n3. Execution trace:\n   - In \'main\', \'nums\' is an array of 3 ints at stack address 0x7ffd10: {5, 10, 15}.\n   - Calling \'double_first(nums)\' passes \'&nums[0]\' (0x7ffd10).\n   - In \'double_first\', parameter \'arr\' is a pointer holding 0x7ffd10.\n   - \'arr[0] *= 2;\' evaluates to \'*arr = *arr * 2;\'.\n   - This writes directly into the memory of \'nums[0]\' at 0x7ffd10, changing 5 to 10.\n   - When \'double_first\' returns, \'nums[0]\' in main is 10.\n\n\'printf("%d\\n", nums[0])\' prints \'10\'. This is why arrays appear to pass \'by reference\' in C, even though C is technically strictly call-by-value (the address value is copied).',
        [
            (1, 6, 'In main: nums[3] = {5, 10, 15} allocated at stack address 0x7ffd10.', {'nums[0]': 5}, {'stack': [{'name': 'nums', 'type': 'int[3]', 'address': '0x7ffd10', 'value': '{5, 10, 15}'}]}),
            (2, 7, 'Call double_first(nums): nums decays to pointer 0x7ffd10 (&nums[0]) passed to parameter arr.', {'arr': '0x7ffd10'}, {'stack': [{'name': 'nums', 'type': 'int[3]', 'address': '0x7ffd10', 'value': '{5, 10, 15}'}, {'name': 'arr', 'type': 'int*', 'address': '0x7ffd00', 'value': '0x7ffd10', 'pointsTo': 'nums[0]'}]}),
            (3, 3, 'In double_first: arr[0] *= 2 dereferences 0x7ffd10; updates nums[0] to 10.', {'nums[0]': 10}, {'stack': [{'name': 'nums', 'type': 'int[3]', 'address': '0x7ffd10', 'value': '{10, 10, 15}'}, {'name': 'arr', 'type': 'int*', 'address': '0x7ffd00', 'value': '0x7ffd10', 'pointsTo': 'nums[0]'}]}),
            (4, 8, "Back in main: printf prints nums[0] (10): '10\\n'.", {'stdout': '10'}, {'stack': [{'name': 'nums', 'type': 'int[3]', 'address': '0x7ffd10', 'value': '{10, 10, 15}'}]})
        ]
    )

print("syllabus_part3 loaded (32 questions, total 100).")
