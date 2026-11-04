# bank_part3.py: Q059 to Q080 (CAT_SCOPE_LIFETIME & CAT_SEQ_UB)
# High-Yield C Midterm Exam Question Bank - Part 3
# Thoroughly upgraded with ISO C99/C11 compliance, balanced answer keys (A/B/C/D),
# granular execution traces, visual stack/pointer memory snapshots, and deep pedagogical rationales.

def load_part3(add_q):
    # =========================================================================
    # CAT_SCOPE_LIFETIME (Q059 - Q070): Scope, Storage Duration & Recursion
    # =========================================================================

    # Q059: Static Local Variable Value Retention -> Key C
    add_q(
        59, 'CAT_SCOPE_LIFETIME', 'Easy', 'Static Local Variable Value Retention',
        'What is the output of the following program?',
        r"""#include <stdio.h>
void counter() {
    static int count = 0;
    count++;
    printf("%d ", count);
}
int main() {
    counter();
    counter();
    counter();
    printf("\n");
    return 0;
}""",
        4, 'static int count = 0;', 'static local variables have STATIC STORAGE DURATION! They are initialized only ONCE and retain their values across function calls!',
        [
            ('A', '1 1 1', False, 'Thought count is re-initialized to 0 on every call like an automatic local variable.', 'static local variables reside in the data segment, not on the stack; their lifetime extends across the entire program execution.'),
            ('B', '0 1 2', False, 'Thought printf printed before count++.', 'count++ executes before printf, so the first printed value is 1.'),
            ('C', '1 2 3', True, 'The static variable count is allocated in the data segment and initialized to 0 once at program startup. Each call increments count in place, producing 1, then 2, then 3.', ''),
            ('D', 'Compile error', False, 'Thought static variables are only allowed at file scope.', 'static storage-class specifier is fully valid on block-scope local variables.'),
        ],
        'static local variables have static storage duration. They persist across function calls in the data segment, incrementing to 1 2 3.',
        'ISO/IEC 9899:1999 §6.2.4#3 & §6.7.1',
        "Static Storage Duration Mechanics:\n1. Memory Allocation (§6.2.4#3):\n   - An object declared with static storage duration has its lifetime for the entire execution of the program.\n   - Unlike automatic variables allocated on the ephemeral runtime stack frame, static int count is allocated in the initialized data segment (.data).\n2. Initialization Rule (§6.7.8#10):\n   - All static objects are initialized only ONCE, prior to program startup (before main begins).\n   - Subsequent entries into function counter() skip the initialization statement static int count = 0;.\n3. Trace Across Invocations:\n   - Call 1: count is 0. count++ -> 1. Prints '1 '.\n   - Call 2: count is 1. count++ -> 2. Prints '2 '.\n   - Call 3: count is 2. count++ -> 3. Prints '3 '.\n4. Output: '1 2 3'.\n\nExam Trap: Contrast static local variables with automatic variables. Without static, int count = 0; would recreate and re-zero count on every stack frame push, printing 1 1 1.",
        [
            (1, 4, 'static int count initialized to 0 in .data segment prior to main() execution.', {'count': 0}, {'data_segment': [{'name': 'count', 'type': 'static int', 'addr': '0x00403000', 'val': 0}]}),
            (2, 5, "Call 1: counter() increments .data count to 1. Prints '1 '.", {'count': 1, 'stdout': '1 '}, {'data_segment': [{'name': 'count', 'val': 1}]}),
            (3, 5, "Call 2: counter() increments .data count to 2. Prints '2 '.", {'count': 2, 'stdout': '1 2 '}, {'data_segment': [{'name': 'count', 'val': 2}]}),
            (4, 5, "Call 3: counter() increments .data count to 3. Prints '3 '.", {'count': 3, 'stdout': '1 2 3 '}, {'data_segment': [{'name': 'count', 'val': 3}]}),
        ]
    )

    # Q060: Static Initialization Evaluated Once Only -> Key D
    add_q(
        60, 'CAT_SCOPE_LIFETIME', 'Tricky', 'Static Initialization Evaluated Once Only',
        'What is the output of the following program?',
        r"""#include <stdio.h>
int add(int x) {
    static int val = 10;
    val += x;
    return val;
}
int main() {
    printf("%d ", add(5));
    printf("%d\n", add(10));
    return 0;
}""",
        4, 'static int val = 10;', 'static int val = 10 is executed ONCE at compile/load time! On the second call add(10), val retains 15 and becomes 25!',
        [
            ('A', '15 20', False, 'Thought val reset to 10 on the second call (10 + 10 = 20).', 'static local variables never reset their values; val remains 15 after the first call.'),
            ('B', '5 10', False, 'Thought val was ignored.', 'val starts at 10 and accumulates inputs.'),
            ('C', '10 20', False, 'Thought val was returned before addition.', 'val += x updates val before returning.'),
            ('D', '15 25', True, "First call add(5): val initializes to 10 once, val += 5 becomes 15 and returns 15. Second call add(10): val retains 15, val += 10 becomes 25 and returns 25. Output is '15 25'.", ''),
        ],
        'static int val = 10 initializes once. First call produces 10 + 5 = 15; second call accumulates 15 + 10 = 25.',
        'ISO/IEC 9899:1999 §6.2.4#3 & §6.7.8#10',
        "Persistent Accumulation in Static Variables:\n1. Under ISO C §6.7.8 paragraph 10, static storage-class variables are initialized once prior to program entry.\n2. In function add(x):\n   - Memory location for val is fixed in the data segment (e.g. 0x00403004).\n   - First call add(5): val has initial value 10. val += 5 updates memory to 15. Returns 15.\n   - Second call add(10): The declaration line static int val = 10; is NOT executed again. val holds its current value 15. val += 10 updates memory to 25. Returns 25.\n3. printf formats output as '15 25'.\n\nExam Trap: Students often treat static initialization as an executable assignment that runs on every function entry. Remember: in C, static initialization is performed by the loader, not runtime control flow.",
        [
            (1, 4, 'static int val allocated in .data segment, initialized to 10.', {'val': 10}, {'data_segment': [{'name': 'val', 'addr': '0x00403004', 'val': 10}]}),
            (2, 5, 'Call 1: add(5) -> val += 5 updates .data to 15. Returns 15.', {'val': 15, 'ret1': 15}, {'data_segment': [{'name': 'val', 'val': 15}]}),
            (3, 5, 'Call 2: add(10) -> val (15) += 10 updates .data to 25. Returns 25.', {'val': 25, 'ret2': 25}, {'data_segment': [{'name': 'val', 'val': 25}]}),
            (4, 9, "printf prints results: '15 25'.", {'stdout': '15 25'}, {'stack': [{'name': 'stdout', 'val': '15 25'}]}),
        ]
    )

    # Q061: Returning Address of Local Stack Variable -> Key A
    add_q(
        61, 'CAT_SCOPE_LIFETIME', 'Medium', 'Returning Address of Local Stack Variable',
        'What is the fundamental flaw in the following program?',
        r"""#include <stdio.h>
int *get_value() {
    int x = 42;
    return &x;
}
int main() {
    int *p = get_value();
    printf("%d\n", *p);
    return 0;
}""",
        5, 'return &x;', 'x is an AUTOMATIC variable whose lifetime terminates when get_value() returns! Returning &x yields a DANGLING POINTER into dead stack memory, causing UNDEFINED BEHAVIOR!',
        [
            ('A', 'Undefined Behavior: Dereferencing a dangling pointer to an expired stack frame', True, 'Local variable x has automatic storage duration. Its lifetime ends as soon as get_value() returns. Returning &x and dereferencing *p accesses a destroyed stack frame, which is Undefined Behavior (may print garbage, old values, or crash).', ''),
            ('B', 'Guaranteed to print 42', False, 'Assumed stack memory persists after function return.', 'The stack frame is deallocated upon function return; subsequent function calls (like printf) overwrite that stack region.'),
            ('C', 'Compilation Error: cannot return pointer', False, 'Thought C forbids returning pointer types from functions.', 'Returning pointers (int*) is completely valid C syntax; the flaw is returning the address of an automatic local variable.'),
            ('D', 'Memory Leak', False, 'Confused stack deallocation with unfreed heap memory.', 'Automatic variables are automatically deallocated when their stack frame pops; no memory is leaked.'),
        ],
        'Automatic variables are destroyed when their scope ends. Returning &x returns a dangling pointer, causing Undefined Behavior on dereference.',
        'ISO/IEC 9899:1999 §6.2.4#5',
        "Stack Frame Lifecycle and Dangling Pointers:\n1. Automatic Storage Duration (§6.2.4#5):\n   - 'For such an object that does not have a variable length array type, its lifetime extends from entry into the block with which it is associated until execution of that block ends in any way.'\n2. Call Stack Dynamics:\n   - When get_value() is called, a stack frame is allocated (ESP/RSP decrements).\n   - Variable x is allocated on this stack frame at e.g. 0x0019FF10 and assigned 42.\n   - When get_value() executes return &x, the stack frame is deallocated (function epilogue pops EBP/RSP).\n   - Pointer p in main receives address 0x0019FF10.\n3. Stack Frame Overwriting:\n   - When printf() is called, its own stack frame is pushed onto the exact same stack region, immediately clobbering 0x0019FF10 with printf's internal local variables and return addresses.\n   - Dereferencing *p reads corrupted memory, yielding unpredictable behavior or a crash.\n\nExam Trap: Never return the address of a local automatic variable! To return memory safely, use dynamic heap allocation (malloc) or pass a caller-allocated buffer.",
        [
            (1, 4, 'get_value() stack frame allocated. Local x = 42 at stack address 0x0019FF10.', {'x': 42}, {'stack': [{'name': 'x', 'addr': '0x0019FF10', 'val': 42, 'scope': 'get_value'}]}),
            (2, 5, 'get_value() returns &x (0x0019FF10). Stack frame destroyed! Memory 0x0019FF10 is now unallocated.', {'p': '0x0019FF10'}, {'stack': [{'name': 'p', 'addr': '0x1000', 'val': '0x0019FF10', 'status': 'DANGLING'}]}),
            (3, 9, 'printf() executes, allocating its own frame and clobbering 0x0019FF10. Dereference *p accesses invalid stack -> UNDEFINED BEHAVIOR.', {'deref_p': 'corrupted'}, {'stack': []}),
        ]
    )

    # Q062: Inner Block Scope Variable Shadowing -> Key B
    add_q(
        62, 'CAT_SCOPE_LIFETIME', 'Medium', 'Inner Block Scope Variable Shadowing',
        'What is the output of the following program?',
        r"""#include <stdio.h>
int main() {
    int x = 10;
    {
        int x = 20;
        printf("%d ", x);
    }
    printf("%d\n", x);
    return 0;
}""",
        6, 'int x = 20;', 'The inner block declaration int x = 20 SHADOWS (hides) the outer x! When the inner block ends, the outer x (10) becomes visible again!',
        [
            ('A', '20 20', False, 'Thought the inner assignment modified the outer variable x.', 'int x = 20 in the inner block declares a NEW independent local variable, leaving outer x unchanged.'),
            ('B', '20 10', True, "Inside the nested block, inner x (20) shadows outer x, printing 20. When the nested block terminates, inner x is destroyed, and the outer x (10) is restored and printed, yielding '20 10'.", ''),
            ('C', '10 10', False, 'Thought the inner re-declaration was ignored by the compiler.', 'The inner declaration is fully valid and active throughout its enclosing block scope.'),
            ('D', 'Compilation Error: duplicate variable x', False, 'Thought declaring a variable with the same name in a nested block is illegal in C.', 'C explicitly allows variable shadowing across nested block scopes under §6.2.1#4.'),
        ],
        'Inner block scope variables shadow outer declarations. Inner prints 20; after block exit, outer x retains 10, printing 20 10.',
        'ISO/IEC 9899:1999 §6.2.1#4',
        'Block Scope and Identifier Shadowing:\n1. Scope Rule (§6.2.1#4):\n   \'If an identifier designates two different entities in the same name space, the scopes might be distinct or one might be nested within the other... If the prior declaration is in an outer block, the new declaration hides the prior declaration until the end of the inner block.\'\n2. Trace:\n   - Outer block: int x = 10 is allocated at stack offset 0. Outer x is in scope.\n   - Inner block entered ({): int x = 20 allocates a SEPARATE variable at stack offset 4. Any unqualified reference to x resolves to this inner variable.\n   - printf("%d ", x) outputs \'20 \'.\n   - Inner block exits (}): The inner variable\'s scope and lifetime terminate.\n   - Outer printf("%d\\n", x) references the outer variable, which was never touched and still contains 10.\n3. Output: \'20 10\'.\n\nExam Trap: Be careful not to confuse int x = 20; (shadowing a new variable) with x = 20; (mutating the outer variable!).',
        [
            (1, 4, 'Outer x allocated on stack at 0x1000 with value 10.', {'outer_x': 10}, {'stack': [{'name': 'outer_x', 'addr': '0x1000', 'val': 10}]}),
            (2, 6, 'Nested block entered: inner x allocated on stack at 0x1004 with value 20. Inner x shadows outer x.', {'inner_x': 20}, {'stack': [{'name': 'outer_x', 'addr': '0x1000', 'val': 10}, {'name': 'inner_x', 'addr': '0x1004', 'val': 20}]}),
            (3, 7, 'Inner printf prints inner x (20).', {'stdout': '20 '}, {'stack': []}),
            (4, 9, "Nested block exits: inner x destroyed. Outer printf prints outer x (10): outputs '20 10'.", {'stdout': '20 10'}, {'stack': [{'name': 'outer_x', 'addr': '0x1000', 'val': 10}]}),
        ]
    )

    # Q063: Global Variable Shadowing by Local Variable -> Key C
    add_q(
        63, 'CAT_SCOPE_LIFETIME', 'Easy', 'Global Variable Shadowing by Local Variable',
        'What is the output of the following program?',
        r"""#include <stdio.h>
int val = 100;
void test() {
    printf("%d ", val);
}
int main() {
    int val = 50;
    test();
    printf("%d\n", val);
    return 0;
}""",
        8, 'int val = 50;', 'test() has no local val, so it accesses the GLOBAL val (100)! main() prints its own LOCAL val (50) which shadows the global inside main()!',
        [
            ('A', '50 50', False, 'Thought local val in main modified or shadowed global val for function test().', 'Local variables in main are not in scope inside test(); test() resolves val in file scope (global 100).'),
            ('B', '100 100', False, 'Thought global val overrode the local variable in main.', 'Inside main(), the local variable val (50) shadows the global variable.'),
            ('C', '100 50', True, "test() accesses global val (100) because main's local variable is not visible outside main's block. Inside main(), local val (50) shadows global val. Output is '100 50'.", ''),
            ('D', 'Compile error', False, 'Thought having a global and local variable with the same identifier causes a naming collision error.', 'Shadowing between file scope and block scope is fully standard C.'),
        ],
        'test() resolves val at file scope (100). main() prints its block-scope local val (50). Output is 100 50.',
        'ISO/IEC 9899:1999 §6.2.1#2 & §6.2.1#4',
        "File Scope vs Block Scope Resolution:\n1. Identifier Resolution Rules (§6.2.1):\n   - Global variable int val = 100 is declared outside any block, giving it FILE SCOPE. It is accessible by all functions in the translation unit unless shadowed.\n   - In function test(), the compiler looks up identifier val: no block-scope declaration exists in test(), so it resolves to file-scope global val (100).\n   - In function main(), int val = 50 declares a BLOCK SCOPE variable. This shadows the file-scope identifier within main's block.\n2. Execution Flow:\n   - test() is called: prints global val (100) -> '100 '.\n   - Control returns to main().\n   - printf in main prints local val (50) -> '50'.\n3. Output: '100 50'.\n\nExam Trap: A local variable in one function can NEVER shadow variables inside another function. Scope is lexical, not dynamic!",
        [
            (1, 2, 'Global val allocated in .data segment at 0x00403000 with value 100.', {'global_val': 100}, {'data_segment': [{'name': 'val (global)', 'addr': '0x00403000', 'val': 100}]}),
            (2, 8, 'main() stack frame allocated. Local val = 50 created on stack at 0x1000.', {'main_val': 50}, {'stack': [{'name': 'val (local)', 'addr': '0x1000', 'val': 50}], 'data_segment': [{'name': 'val (global)', 'val': 100}]}),
            (3, 4, "test() called: resolves val in file scope -> reads 100. Prints '100 '.", {'stdout': '100 '}, {'stack': []}),
            (4, 10, "main() prints its local val (50): outputs '100 50'.", {'stdout': '100 50'}, {'stack': [{'name': 'val (local)', 'val': 50}]}),
        ]
    )

    # Q064: Static at File Scope (Internal Linkage) -> Key D
    add_q(
        64, 'CAT_SCOPE_LIFETIME', 'Medium', 'Static at File Scope (Internal Linkage)',
        'What does the static keyword mean when applied to a global variable outside all functions?',
        r"""static int secret_key = 42;
int main() {
    (void)secret_key;
    return 0;
}""",
        1, 'static int secret_key = 42;', 'static at file scope gives the identifier INTERNAL LINKAGE, restricting its visibility strictly to the current translation unit (.c file)!',
        [
            ('A', 'It causes the variable to be allocated on the runtime stack', False, 'Global variables are always stored in the data/BSS segment, never on the stack.', 'static alters linkage, not storage location.'),
            ('B', 'It makes the variable thread-safe and atomic', False, 'static has no multithreading or atomic synchronization properties.', 'C does not add thread-safety with static.'),
            ('C', 'It prevents the variable from ever being modified (like const)', False, 'Confused static with const.', 'static variables are fully mutable; const enforces immutability.'),
            ('D', "It limits the variable's visibility strictly to this translation unit (source file)", True, 'Under ISO C §6.2.2#3, if a file-scope declaration includes the static storage-class specifier, the identifier has internal linkage. It cannot be accessed by other translation units via extern declarations.', ''),
        ],
        'static at file scope gives internal linkage (§6.2.2#3). The variable is private to the current .c file and invisible to other object files.',
        'ISO/IEC 9899:1999 §6.2.2#3',
        "Linkage and the static Specifier in C:\n1. Linkage Concepts (§6.2.2):\n   - External Linkage: An identifier can be referenced across multiple translation units (source files) by declaring it with extern. Default for non-static global variables and functions.\n   - Internal Linkage: An identifier is private to the current translation unit. The compiler does not emit a global linker symbol for it.\n   - None: Block-scope local variables have no linkage.\n2. When static is placed on a file-scope variable:\n   - static int secret_key = 42;\n   - The symbol is marked as local/internal in the resulting object file (.o).\n   - If another file attempts extern int secret_key;, the linker will emit an 'undefined reference' error.\n3. Note on Code Hygiene: (void)secret_key; is used inside main() to suppress compiler unused-variable warnings under -Wall -Wextra while testing this exact language rule.\n\nExam Trap: static has two completely different meanings depending on context: inside a function, it extends lifetime (static storage duration); outside functions, it restricts visibility (internal linkage).",
        [
            (1, 1, 'secret_key declared at file scope with static: assigned INTERNAL LINKAGE.', {'linkage': 'internal'}, {'data_segment': [{'name': 'secret_key', 'val': 42, 'linkage': 'INTERNAL (local symbol)'}]}),
            (2, 3, '(void)secret_key suppresses unused-variable warnings cleanly without generating runtime instructions.', {'status': 'clean compile'}, {'stack': []}),
            (3, 4, 'Linker symbol table marks secret_key as STB_LOCAL. Invisible to external object files.', {'visibility': 'translation_unit_only'}, {'stack': []}),
        ]
    )

    # Q065: extern Variable Declaration vs Definition -> Key A
    add_q(
        65, 'CAT_SCOPE_LIFETIME', 'Medium', 'extern Variable Declaration vs Definition',
        'Which of the following is true regarding: extern int x; outside all functions?',
        r"""extern int x;
int main() {
    return 0;
}""",
        1, 'extern int x;', 'extern int x; is a PURE DECLARATION! It allocates NO storage and informs the compiler that x is defined in another translation unit!',
        [
            ('A', 'It declares x without allocating memory, informing the compiler that x is defined elsewhere', True, 'Under ISO C §6.7#5 and §6.2.2#4, an extern declaration without an initializer is a pure declaration that reserves no storage, deferring symbol resolution to the linker.', ''),
            ('B', 'It allocates memory for x in the BSS segment and initializes it to 0', False, 'Declarations with extern without an initializer do not allocate memory.', 'Storage must be allocated by an actual definition: int x;'),
            ('C', 'It makes x a local variable in all functions automatically', False, 'extern refers to an external identifier with file scope.', 'It does not create local variables.'),
            ('D', 'It is a syntax error without an explicit initializer', False, 'Adding an initializer (extern int x = 5;) would turn it into a definition.', 'extern int x; without initializer is standard declaration syntax.'),
        ],
        'extern int x; is a declaration that allocates no storage. It instructs the linker to resolve x from another translation unit.',
        'ISO/IEC 9899:1999 §6.7#5 & §6.9.2',
        "Declaration vs Definition in C:\n1. Distinction (§6.7#5):\n   - A declaration specifies the interpretation and attributes of a set of identifiers.\n   - A definition is a declaration that reserves storage for an object.\n2. extern Specifier (§6.9.2):\n   - extern int x; has external linkage and no initializer. It is NOT a definition; it allocates zero bytes of memory.\n   - The compiler emits an undefined external symbol reference in the object file symbol table.\n   - At link time, the linker resolves this symbol to a matching definition (int x;) in another object file.\n3. Exception: If an extern declaration has an initializer (extern int x = 10;), it becomes a definition, and storage is allocated in .data.\n\nExam Trap: Remember: 'extern int x;' declares without storage; 'int x;' is a tentative definition that allocates storage.",
        [
            (1, 1, 'extern int x; parsed: added to compiler symbol table as external reference. No memory allocated.', {'symbol': 'x', 'allocated_bytes': 0}, {'symbol_table': [{'name': 'x', 'type': 'int', 'status': 'UNDEFINED_EXTERNAL'}]}),
            (2, 2, 'Function main() defined: stack frame reserves 0 bytes for x.', {'local_alloc': 0}, {'stack': []}),
            (3, 3, 'main() executes return 0 cleanly without referencing x.', {'exit_code': 0}, {'stack': []}),
            (4, 3, 'Object file emits SHN_UNDEF symbol for x, deferring memory resolution to the linker.', {'status': 'pure_declaration'}, {'symbol_table': [{'name': 'x', 'linkage': 'EXTERNAL'}]}),
        ]
    )

    # Q066: Uninitialized Local Automatic Variable Value -> Key B
    add_q(
        66, 'CAT_SCOPE_LIFETIME', 'Easy', 'Uninitialized Local Automatic Variable Value',
        'What is the value of an uninitialized local variable with automatic storage duration in C?',
        r"""#include <stdio.h>
int main() {
    int x;
    printf("%d\n", x);
    return 0;
}""",
        4, 'int x;', 'Automatic variables are NOT initialized by default! They contain INDETERMINATE (garbage) values left over in stack memory!',
        [
            ('A', 'Guaranteed to be 0', False, 'Thought C zeroes all variables upon declaration.', 'Only global and static variables are zero-initialized; automatic local variables receive no default initialization.'),
            ('B', 'Indeterminate (garbage value from stack memory)', True, 'Under ISO C §6.7.8#10, if an object with automatic storage duration is not initialized explicitly, its value is indeterminate (containing leftover stack garbage).', ''),
            ('C', 'Compilation error', False, 'Thought the compiler rejects uninitialized variables.', 'The code is syntactically valid; compilers emit a warning (-Wuninitialized) but compile successfully.'),
            ('D', 'NULL', False, 'NULL is a pointer constant, not an integer initialization guarantee.', 'Scalar integers cannot be NULL.'),
        ],
        'Automatic variables are not zeroed. They contain indeterminate garbage values from stack memory under ISO C §6.7.8#10.',
        'ISO/IEC 9899:1999 §6.7.8#10',
        "Storage Duration and Default Initialization:\n1. Standard Specification (§6.7.8#10):\n   'If an object that has automatic storage duration is not initialized explicitly, its value is indeterminate.'\n2. Hardware and Stack Mechanics:\n   - When function main() executes its prologue, the stack pointer (ESP/RSP) is decremented to reserve space for local variable x.\n   - No CPU instructions are emitted to write zeroes to that stack slot (for performance reasons).\n   - Whatever bit pattern happened to be left in that stack memory location from prior function calls or OS setup becomes the value of x.\n3. Reading an uninitialized object with indeterminate value is a severe security and correctness hazard (leading to information disclosure or undefined behavior if it can be a trap representation).\n\nExam Trap: Always contrast automatic local variables (garbage/indeterminate) with static and global variables (guaranteed zero).",
        [
            (1, 4, 'Stack frame allocates 4 bytes for int x at 0x1000.', {'x': 'uninitialized'}, {'stack': [{'name': 'x', 'addr': '0x1000', 'val': '0xDEADBEEF (garbage)'}]}),
            (2, 4, 'No CPU instructions zero the stack slot. Previous bit pattern 0xDEADBEEF remains in memory.', {'x_bits': '0xDEADBEEF'}, {'stack': [{'name': 'x', 'addr': '0x1000', 'val': '0xDEADBEEF'}]}),
            (3, 5, 'printf reads uninitialized stack slot at 0x1000 -> outputs indeterminate garbage integer.', {'stdout': '<garbage>'}, {'stack': [{'name': 'x', 'val': '<indeterminate>'}]}),
        ]
    )

    # Q067: Default Initialization of Global and Static Variables -> Key C
    add_q(
        67, 'CAT_SCOPE_LIFETIME', 'Easy', 'Default Initialization of Global and Static Variables',
        'What is the value of an uninitialized variable declared at file scope (global)?',
        r"""#include <stdio.h>
int global_num;
int main() {
    printf("%d\n", global_num);
    return 0;
}""",
        3, 'int global_num;', 'Variables with STATIC storage duration (globals and static locals) are GUARANTEED by ISO C to be initialized to ZERO!',
        [
            ('A', 'Indeterminate (garbage value)', False, 'Confused global variables with automatic local variables.', 'Automatic variables are garbage; global variables are guaranteed to be zero-initialized.'),
            ('B', '-1', False, 'Thought -1 was used as a sentinel default.', 'Default initialization in C is strictly arithmetic zero.'),
            ('C', 'Guaranteed to be 0', True, 'Under ISO C §6.7.8#10, objects with static storage duration that are not initialized explicitly are guaranteed to be initialized to zero (arithmetic zero for integers, null pointer for pointers).', ''),
            ('D', 'Compilation error', False, 'Thought all global variables require explicit initializers.', 'Uninitialized globals are treated as tentative definitions and placed in the BSS segment.'),
        ],
        'Global and static variables are placed in the BSS segment and guaranteed by the C standard to be initialized to 0.',
        'ISO/IEC 9899:1999 §6.7.8#10',
        "BSS Segment and Static Zero-Initialization:\n1. Standard Guarantee (§6.7.8#10):\n   'If an object that has static storage duration is not initialized explicitly, then:\n    - if it has pointer type, it is initialized to a null pointer;\n    - if it has arithmetic type, it is initialized to (positive or unsigned) zero;\n    - if it is an aggregate, every member is initialized (recursively) according to these rules;'\n2. Operating System / Linker Implementation:\n   - Global uninitialized variables are assigned to the BSS (Block Started by Symbol) segment.\n   - The BSS segment does not consume space in the executable binary on disk; only its total size is recorded in the ELF/PE header.\n   - When the operating system loader maps the executable into memory, it maps the BSS pages from zero-filled system pages.\n3. Therefore, global_num is guaranteed to contain 0 when main() begins execution.\n4. printf outputs '0'.",
        [
            (1, 3, 'global_num allocated in BSS segment at 0x00404000. Header records BSS size.', {'global_num': 'unmapped'}, {'bss_segment': [{'name': 'global_num', 'addr': '0x00404000'}]}),
            (2, 3, 'Program loader zeroes all BSS segment pages before executing main().', {'global_num': 0}, {'bss_segment': [{'name': 'global_num', 'addr': '0x00404000', 'val': 0}]}),
            (3, 5, 'printf reads global_num from BSS: prints 0.', {'stdout': '0'}, {'stack': [{'name': 'stdout', 'val': '0'}]}),
        ]
    )

    # Q068: Automatic Variable Lifetime Inside Loop Iterations -> Key D
    add_q(
        68, 'CAT_SCOPE_LIFETIME', 'Medium', 'Automatic Variable Lifetime Inside Loop Iterations',
        'What is the output of the following program?',
        r"""#include <stdio.h>
int main() {
    for (int i = 0; i < 3; i++) {
        int count = 0;
        count++;
        printf("%d ", count);
    }
    printf("\n");
    return 0;
}""",
        5, 'int count = 0;', 'Automatic variable count is created and re-initialized to 0 on EVERY single loop iteration! It does NOT retain value across iterations!',
        [
            ('A', '1 2 3', False, 'Thought count retained its value across loop iterations like a static variable.', 'count has automatic storage duration scoped to the loop body; it is recreated and re-initialized to 0 on every iteration.'),
            ('B', '0 0 0', False, 'Thought printf printed before count++.', 'count++ runs before printf, so each iteration prints 1.'),
            ('C', 'Compile error', False, 'Thought declaring variables inside a for-loop body is illegal.', 'Declaring variables inside loop bodies has been standard C since C99.'),
            ('D', '1 1 1', True, "Because count is an automatic variable inside the for-loop body block, its lifetime begins afresh on each iteration, where it is initialized to 0, incremented to 1, and printed. Output is '1 1 1 '.", ''),
        ],
        'Automatic variables inside a loop body are created and initialized on every iteration. count is initialized to 0 each time, printing 1 1 1.',
        'ISO/IEC 9899:1999 §6.2.4#5 & §6.8.5',
        "Block Scope Lifetime in Iteration Statements:\n1. ISO C Specification (§6.2.4#5):\n   - The lifetime of an automatic variable begins upon entry into the block and ends when execution of that block terminates.\n   - Each iteration of a loop statement constitutes a distinct entry and exit of the loop body block.\n2. Iteration Trace:\n   - Iteration 0 (i=0): Block entered. Stack reserves count, initialized to 0. count++ -> 1. Prints '1 '. Block exits: count is deallocated.\n   - Iteration 1 (i=1): Block entered. A new instance of count is initialized to 0. count++ -> 1. Prints '1 '. Block exits.\n   - Iteration 2 (i=2): Block entered. A new instance of count is initialized to 0. count++ -> 1. Prints '1 '. Block exits.\n3. Output: '1 1 1 '.\n\nExam Trap: If you need a counter that accumulates across loop iterations, declare it outside the loop, or declare it as static int count = 0;.",
        [
            (1, 4, "Iter 0 (i=0): count allocated on stack, initialized to 0. count++ -> 1. Prints '1 '.", {'count': 1, 'stdout': '1 '}, {'stack': [{'name': 'i', 'val': 0}, {'name': 'count', 'addr': '0x1000', 'val': 1}]}),
            (2, 4, "Iter 1 (i=1): previous count destroyed. New count allocated on stack, initialized to 0. count++ -> 1. Prints '1 '.", {'count': 1, 'stdout': '1 1 '}, {'stack': [{'name': 'i', 'val': 1}, {'name': 'count', 'addr': '0x1000', 'val': 1}]}),
            (3, 4, "Iter 2 (i=2): previous count destroyed. New count allocated, initialized to 0. count++ -> 1. Prints '1 '.", {'count': 1, 'stdout': '1 1 1 '}, {'stack': [{'name': 'i', 'val': 2}, {'name': 'count', 'addr': '0x1000', 'val': 1}]}),
        ]
    )

    # Q069: Missing Base Case in Recursion -> Key A
    add_q(
        69, 'CAT_SCOPE_LIFETIME', 'Easy', 'Missing Base Case in Recursion',
        'What happens when executing the following program?',
        r"""#include <stdio.h>
void recurse(int n) {
    printf("%d ", n);
    recurse(n + 1);
}
int main() {
    recurse(1);
    return 0;
}""",
        4, 'recurse(n + 1);', 'There is NO BASE CASE! Unbounded recursion exhausts stack memory, causing a STACK OVERFLOW and Segmentation Fault!',
        [
            ('A', 'Runtime Crash (Stack Overflow / Segmentation Fault)', True, 'Every recursive call allocates a new stack frame for return address and parameters. Without a base case, recursion continues indefinitely until the process exceeds the OS stack limit (typically 1-8 MB), causing a stack overflow crash (SIGSEGV).', ''),
            ('B', 'Prints numbers indefinitely forever', False, 'Assumed infinite looping without memory limits.', 'Unlike while(1), recursion consumes stack memory on every call; it quickly exhausts memory and crashes.'),
            ('C', 'Compilation error', False, 'Thought the compiler detects missing base cases.', 'Compilers do not perform halting problem analysis; recursive functions compile without error.'),
            ('D', 'Stops when integer n overflows', False, 'Thought integer overflow terminates recursion.', 'Integer overflow wraps around in C and continues recursion until the stack crashes.'),
        ],
        'Unbounded recursion consumes stack frames without termination until stack memory is exhausted, causing a Stack Overflow crash.',
        'ISO/IEC 9899:1999 §6.2.4 & §6.5.2.2',
        'Call Stack Exhaustion and Stack Overflow Mechanics:\n1. Stack Frame Overhead:\n   - Each call to recurse(int n) creates an activation record on the stack:\n     - Return address (4 or 8 bytes)\n     - Saved frame pointer (EBP/RBP, 4 or 8 bytes)\n     - Parameter n (4 bytes)\n     - Total: at least 16 to 32 bytes per frame.\n2. Virtual Memory Limits:\n   - Modern operating systems allocate a fixed stack size per thread (typically 1 MB on Windows, 8 MB on Linux).\n   - Below the stack region lies an unmapped guard page.\n3. Exhaustion Trace:\n   - As n increments (1, 2, 3... ~40,000 to 250,000 frames), the stack pointer (RSP) grows downward.\n   - Eventually, RSP attempts to push into the guard page.\n   - The MMU triggers a Page Fault on the guard page.\n   - The OS detects that the stack limit was breached and terminates the process with SIGSEGV (or EXCEPTION_STACK_OVERFLOW on Windows).\n\nExam Trap: Contrast recursion with infinite loops: while(1) runs forever with O(1) memory; infinite recursion crashes rapidly with O(N) stack exhaustion.',
        [
            (1, 4, "recurse(1) called: frame 1 pushed on stack. Prints '1 '.", {'n': 1, 'depth': 1}, {'stack': [{'frame': 1, 'n': 1}]}),
            (2, 4, "recurse(2) called: frame 2 pushed. Prints '2 '.", {'n': 2, 'depth': 2}, {'stack': [{'frame': 1, 'n': 1}, {'frame': 2, 'n': 2}]}),
            (3, 4, 'Unbounded recursive calls exhaust stack capacity (~8 MB). Stack pointer hits guard page -> CRASH (Stack Overflow / SIGSEGV).', {'status': 'STACK OVERFLOW'}, {'stack': []}),
        ]
    )

    # Q070: Recursive Function Execution Trace -> Key B
    add_q(
        70, 'CAT_SCOPE_LIFETIME', 'Medium', 'Recursive Function Execution Trace',
        'What is the output of mystery(4)?',
        r"""#include <stdio.h>
int mystery(int n) {
    if (n <= 1) return 1;
    return n + mystery(n - 2);
}
int main() {
    printf("%d\n", mystery(4));
    return 0;
}""",
        4, 'return n + mystery(n - 2);', 'mystery(4) = 4 + mystery(2) = 4 + (2 + mystery(0)) = 4 + 2 + 1 = 7! Note the step is n - 2, NOT n - 1!',
        [
            ('A', '10', False, 'Calculated the sum of 4 + 3 + 2 + 1 (decrement by 1 instead of 2).', 'The recursive call steps by n - 2, skipping odd numbers: 4, 2, 0.'),
            ('B', '7', True, 'Trace: mystery(4) calls 4 + mystery(2). mystery(2) calls 2 + mystery(0). For n=0, the base case (n <= 1) returns 1. Unwinding: mystery(2) = 2 + 1 = 3; mystery(4) = 4 + 3 = 7.', ''),
            ('C', '6', False, 'Forgot to add the base case return value 1.', 'Base case returns 1 (not 0); 4 + 2 + 1 = 7.'),
            ('D', '1', False, 'Returned the base case alone without summing stack unwind values.', "Each unwinding frame adds n to the child's return value."),
        ],
        'mystery(4) = 4 + mystery(2) = 4 + (2 + mystery(0)) = 4 + 2 + 1 = 7.',
        'ISO/IEC 9899:1999 §6.5.2.2',
        'Call Stack Evolution and Recursive Unwinding:\n1. Forward Expansion Phase (Call Tree):\n   - Frame 1: mystery(4) called with n = 4.\n     - Condition 4 <= 1 is false.\n     - Evaluates 4 + mystery(2).\n   - Frame 2: mystery(2) called with n = 2.\n     - Condition 2 <= 1 is false.\n     - Evaluates 2 + mystery(0).\n   - Frame 3: mystery(0) called with n = 0.\n     - Condition 0 <= 1 is true!\n     - Base case returns 1.\n2. Backward Unwinding Phase:\n   - Frame 2 receives 1 from mystery(0): returns 2 + 1 = 3.\n   - Frame 1 receives 3 from mystery(2): returns 4 + 3 = 7.\n3. main() prints 7.\n\nExam Trap: Always identify the step size (n - 2 vs n - 1) and base case condition (n <= 1 vs n == 0) before calculating recursive sums.',
        [
            (1, 4, 'Frame 1: mystery(4) called: computes 4 + mystery(2).', {'n': 4}, {'stack': [{'frame': 'mystery(4)', 'n': 4}]}),
            (2, 4, 'Frame 2: mystery(2) called: computes 2 + mystery(0).', {'n': 2}, {'stack': [{'frame': 'mystery(4)', 'n': 4}, {'frame': 'mystery(2)', 'n': 2}]}),
            (3, 3, 'Frame 3: mystery(0) hits base case n <= 1: returns 1.', {'n': 0, 'ret': 1}, {'stack': [{'frame': 'mystery(4)', 'n': 4}, {'frame': 'mystery(2)', 'n': 2}, {'frame': 'mystery(0)', 'n': 0, 'ret': 1}]}),
            (4, 8, 'Unwinding: mystery(2) = 2 + 1 = 3; mystery(4) = 4 + 3 = 7. printf prints 7.', {'stdout': '7'}, {'stack': [{'name': 'stdout', 'val': '7'}]}),
        ]
    )

    # =========================================================================
    # CAT_SEQ_UB (Q071 - Q080): Sequence Points, Undefined Behavior & Memory
    # =========================================================================

    # Q071: Unsequenced Modification (i = i++) -> Key C
    add_q(
        71, 'CAT_SEQ_UB', 'Nightmare', 'Unsequenced Modification (i = i++)',
        'What does the ISO C standard (C99 / C11) dictate regarding the statement: i = i++; ?',
        r"""#include <stdio.h>
int main() {
    int i = 5;
    i = i++;
    printf("%d\n", i);
    return 0;
}""",
        4, 'i = i++;', 'Modifying scalar variable i more than once between sequence points (unsequenced write and write) is strictly UNDEFINED BEHAVIOR!',
        [
            ('A', 'Guaranteed to print 5', False, 'Thought postfix increment happens after assignment completes.', 'In ISO C, there is no sequence point between the assignment and the postfix increment; the behavior is completely undefined.'),
            ('B', 'Guaranteed to print 6', False, 'Thought increment takes precedence over assignment.', 'Undefined behavior means the standard guarantees no result; different compilers or optimization levels yield 5, 6, or corrupted registers.'),
            ('C', 'Undefined Behavior', True, 'Under ISO C99 §6.5#2 and C11 §6.5#2, modifying a scalar object more than once between sequence points (or unsequenced side-effects with respect to value computation) is strictly Undefined Behavior.', ''),
            ('D', 'Compilation Error', False, 'Thought the compiler strictly rejects i = i++.', 'Compilers typically emit a warning (-Wunsequenced) but will generate assembly code, leaving execution undefined.'),
        ],
        "Between consecutive sequence points, an object's stored value shall be modified at most once. i = i++ violates this constraint, producing Undefined Behavior.",
        'ISO/IEC 9899:1999 §6.5#2 & C11 §6.5#2',
        "Sequence Points and Unsequenced Modifications:\n1. The Core Standard Rule (C99 §6.5#2):\n   'Between the previous and next sequence point an object shall have its stored value modified at most once by the evaluation of an expression. Furthermore, the prior value shall be read only to determine the value to be stored.'\n   (In C11 §6.5#2, this is phrased: 'If a side effect on a scalar object is unsequenced relative to either a different side effect on the same scalar object or a value computation using the value of the same scalar object, the behavior is undefined.')\n2. Anatomy of the Violation:\n   - Expression: i = i++;\n   - Mutation 1: The postfix increment operator i++ has the side effect of modifying i (incrementing to 6).\n   - Mutation 2: The assignment operator = attempts to write the evaluated result (5) into i.\n   - Both modifications target the exact same scalar object i without an intervening sequence point.\n3. Compiler Code Generation Hazards:\n   - Clang may store 5 into i first, then increment to 6.\n   - GCC may evaluate the increment first, then overwrite with 5.\n   - Optimizing compilers may assume UB cannot occur and eliminate surrounding code entirely.\n\nExam Trap: Never write i = i++ or a[i] = i++. Any expression modifying a variable while simultaneously assigning to or reading it in the same statement without a sequence point is hazardous UB.",
        [
            (1, 4, 'int i = 5 allocated on stack.', {'i': 5}, {'stack': [{'name': 'i', 'addr': '0x1000', 'val': 5}]}),
            (2, 5, 'Unsequenced side effect (i++) and assignment write (=) compete on scalar object i without intervening sequence point.', {'violation': 'ISO C99 §6.5#2'}, {'stack': []}),
            (3, 5, 'Undefined Behavior invoked: compiler is permitted to emit arbitrary assembly sequence.', {'status': 'UNDEFINED BEHAVIOR'}, {'stack': []}),
        ]
    )

    # Q072: Unsequenced Subscript Indexing (a[i] = i++) -> Key D
    add_q(
        72, 'CAT_SEQ_UB', 'Nightmare', 'Unsequenced Subscript Indexing (a[i] = i++)',
        'What is the status of the expression: arr[i] = i++; in C?',
        r"""#include <stdio.h>
int main() {
    int arr[5] = {0};
    int i = 1;
    arr[i] = i++;
    (void)arr;
    return 0;
}""",
        5, 'arr[i] = i++;', 'Reading i to determine the array subscript while simultaneously modifying i with i++ without a sequence point is UNDEFINED BEHAVIOR!',
        [
            ('A', 'arr[1] is guaranteed to be 1', False, 'Assumed the left-hand side index arr[i] is evaluated before the right-hand side i++.', 'In C, the order of evaluation of the operands of the assignment operator = is unspecified.'),
            ('B', 'arr[2] is guaranteed to be 1', False, 'Assumed the right-hand side i++ is evaluated before the left-hand side subscript.', 'C does not guarantee right-to-left evaluation order for assignments.'),
            ('C', 'Compilation Error', False, 'Thought this semantic flaw is rejected by the compiler.', 'The syntax is valid; compilers issue warnings (-Wunsequenced) but compile the code.'),
            ('D', 'Undefined Behavior', True, 'Under ISO C §6.5#2, the prior value of a scalar object (i) shall be read only to determine the value to be stored. Here, i is read to determine the array subscript arr[i], while simultaneously being modified by i++, producing Undefined Behavior.', ''),
        ],
        'Reading i to determine the array index while modifying i with i++ is unsequenced, violating ISO C §6.5#2 and causing Undefined Behavior.',
        'ISO/IEC 9899:1999 §6.5#2',
        "Unsequenced Subscript Access Mechanics:\n1. Standard Constraint (§6.5#2):\n   'Furthermore, the prior value shall be read only to determine the value to be stored.'\n2. In the statement arr[i] = i++;:\n   - Value to be stored is computed by i++ (value 1, with side effect incrementing i to 2).\n   - Subscript index arr[i] reads i.\n   - Notice that reading i for the subscript is NOT for determining the value to be stored—it is determining WHERE to store the value!\n   - Reading a variable to determine an address while modifying that same variable without a sequence point directly violates §6.5#2.\n3. Evaluation Order Indeterminacy:\n   - The C standard does NOT specify whether the left operand or right operand of = is evaluated first.\n   - If LHS evaluates first: arr[1] = 1.\n   - If RHS evaluates first: arr[2] = 1.\n   - Because the standard declares this Undefined Behavior, the program cannot be relied upon to do either.\n4. Clean Code Hygiene: (void)arr; is included to prevent unused-variable compiler warnings.\n\nExam Trap: Never assume left-to-right evaluation across an assignment operator! Always separate the increment into its own statement: arr[i] = i; i++;.",
        [
            (1, 4, 'int arr[5] = {0} and int i = 1 allocated on stack.', {'arr': [0, 0, 0, 0, 0], 'i': 1}, {'stack': [{'name': 'arr', 'addr': '0x1000', 'val': '[0,0,0,0,0]'}, {'name': 'i', 'addr': '0x1014', 'val': 1}]}),
            (2, 5, 'Unsequenced evaluation: LHS reads i (address computation) while RHS modifies i (i++ side-effect).', {'violation': 'ISO C §6.5#2'}, {'stack': []}),
            (3, 5, 'Standard declares entire statement UNDEFINED BEHAVIOR.', {'status': 'UNDEFINED BEHAVIOR'}, {'stack': []}),
        ]
    )

    # Q073: Unspecified Argument Evaluation Order -> Key A
    add_q(
        73, 'CAT_SEQ_UB', 'Nightmare', 'Unspecified Argument Evaluation Order',
        'What is the behavior of: printf("%d %d\\n", ++i, ++i); with int i = 1?',
        r"""#include <stdio.h>
int main() {
    int i = 1;
    printf("%d %d\n", ++i, ++i);
    return 0;
}""",
        4, 'printf("%d %d\\n", ++i, ++i);', 'The evaluation order of function arguments is UNSPECIFIED! Modifying i twice without a sequence point between arguments is UNDEFINED BEHAVIOR!',
        [
            ('A', 'Undefined Behavior (Unspecified evaluation order)', True, 'Under ISO C §6.5.2.2#10, the order of evaluation of function arguments is unspecified. Furthermore, modifying i twice in the argument list without an intervening sequence point invokes Undefined Behavior under §6.5#2.', ''),
            ('B', 'Guaranteed to print 2 3', False, 'Assumed arguments are evaluated strictly from left to right.', 'In C, commas in function argument lists are NOT comma operators; they are punctuators with NO sequence point between argument evaluations.'),
            ('C', 'Guaranteed to print 3 2', False, 'Assumed arguments are evaluated strictly from right to left (like x86 cdecl stack pushing).', 'Calling convention is an implementation detail; the ISO C standard explicitly leaves argument evaluation order unspecified.'),
            ('D', 'Compilation Error', False, 'Thought passing multiple increments to printf is rejected by the compiler.', 'The code compiles with warnings (-Wunsequenced), but is not a syntax error.'),
        ],
        'Function argument evaluation order is unspecified (§6.5.2.2#10). Modifying i twice without a sequence point causes Undefined Behavior.',
        'ISO/IEC 9899:1999 §6.5.2.2#10 & §6.5#2',
        "Argument Punctuators vs Comma Operators:\n1. Syntax Distinction:\n   - In expressions like (a, b), the comma is an OPERATOR that introduces a sequence point between a and b.\n   - In function calls like func(arg1, arg2), the comma is merely a SYNTACTIC PUNCTUATOR separating arguments. There is NO sequence point between argument evaluations!\n2. Standard Specification (§6.5.2.2#10):\n   'The order of evaluation of the function designator, the actual arguments, and subexpressions within the actual arguments is unspecified, but there is a sequence point before the actual call.'\n3. Consequences:\n   - Both ++i expressions modify scalar object i.\n   - Because argument evaluations are unsequenced relative to each other, modifying i twice violates §6.5#2.\n   - The entire program exhibits Undefined Behavior.\n4. Real-world Divergence:\n   - GCC x86-64 may evaluate right-to-left, printing '3 2'.\n   - Clang or ARM GCC may evaluate left-to-right, printing '2 3' or '3 3'.\n\nExam Trap: Never introduce side effects (++ or --) in function call argument lists!",
        [
            (1, 4, 'int i = 1 initialized on stack.', {'i': 1}, {'stack': [{'name': 'i', 'addr': '0x1000', 'val': 1}]}),
            (2, 5, 'printf called: argument commas are punctuators, NOT sequence points. ++i and ++i are unsequenced.', {'evaluation_order': 'unspecified'}, {'stack': []}),
            (3, 5, 'Two modifications of scalar i without sequence point -> UNDEFINED BEHAVIOR.', {'status': 'UNDEFINED BEHAVIOR'}, {'stack': []}),
        ]
    )

    # Q074: Signed vs Unsigned Overflow Semantics -> Key B
    add_q(
        74, 'CAT_SEQ_UB', 'Tricky', 'Signed vs Unsigned Overflow Semantics',
        'What does the ISO C standard state regarding signed integer overflow (e.g. INT_MAX + 1)?',
        r"""#include <stdio.h>
#include <limits.h>
int main() {
    int x = INT_MAX;
    int y = x + 1;
    printf("%d\n", y);
    return 0;
}""",
        5, 'x + 1', 'In C, SIGNED integer overflow is UNDEFINED BEHAVIOR! (Contrast with unsigned integer overflow, which is guaranteed to wrap around modulo 2^N)!',
        [
            ('A', 'Guaranteed to wrap to INT_MIN (-2147483648)', False, "Assumed two's complement wrap is a language guarantee in C.", 'While most CPUs wrap in hardware, ISO C explicitly classifies signed overflow as Undefined Behavior, allowing optimizing compilers to assume it never occurs.'),
            ('B', 'Undefined Behavior', True, 'Under ISO C §6.5#5, if an exceptional condition occurs during the evaluation of an expression (such as signed arithmetic overflow), the behavior is strictly Undefined Behavior.', ''),
            ('C', 'Guaranteed to throw a hardware exception', False, 'Thought CPU interrupts halt execution on signed overflow.', 'CPUs do not raise exceptions on integer addition overflow by default.'),
            ('D', 'Saturates at INT_MAX', False, 'Thought C clamps arithmetic at maximum values.', 'C arithmetic does not saturate automatically.'),
        ],
        'Signed integer overflow is Undefined Behavior in ISO C (§6.5#5). Only unsigned integers are guaranteed to wrap around modulo 2^N.',
        'ISO/IEC 9899:1999 §6.5#5 & §6.2.5#9',
        "The Critical Distinction Between Signed and Unsigned Arithmetic:\n1. Standard Specification for Signed Arithmetic (§6.5#5):\n   'If an exceptional condition occurs during the evaluation of an expression (that is, if the result is not mathematically defined or not in the range of representable values for its type), the behavior is undefined.'\n2. Standard Specification for Unsigned Arithmetic (§6.2.5#9):\n   'A computation involving unsigned operands can never overflow... reduced modulo 2^N.'\n3. Why This Matters for Modern Optimizing Compilers (GCC -O2 / -O3):\n   - Because signed overflow is UB, the compiler assumes signed overflow CAN NEVER OCCUR in valid code.\n   - Given a check like if (x + 1 > x), GCC optimizes the entire condition to 1 (always true) and deletes the else branch completely!\n   - If the code later runs with x = INT_MAX, security checks may be bypassed unexpectedly.\n\nExam Trap: Midterm exams love to contrast signed int overflow (Undefined Behavior) with unsigned int overflow (Guaranteed modulo 2^N wrap-around).",
        [
            (1, 4, 'int x initialized to INT_MAX (2147483647, 0x7FFFFFFF) on stack.', {'x': 2147483647}, {'stack': [{'name': 'x', 'addr': '0x1000', 'val': 2147483647, 'hex': '0x7FFFFFFF'}]}),
            (2, 5, 'x + 1 evaluates: mathematical result 2147483648 exceeds representable range of 32-bit signed int.', {'overflow': True}, {'stack': []}),
            (3, 5, 'Signed arithmetic overflow is strictly UNDEFINED BEHAVIOR under ISO C §6.5#5.', {'status': 'UNDEFINED BEHAVIOR'}, {'stack': []}),
        ]
    )

    # Q075: Bitwise Shift Exceeding Bit Width -> Key C
    add_q(
        75, 'CAT_SEQ_UB', 'Tricky', 'Bitwise Shift Exceeding Bit Width',
        'What is the behavior of: 1 << 32 on a platform with 32-bit int?',
        r"""#include <stdio.h>
int main() {
    int x = 1 << 32;
    printf("%d\n", x);
    return 0;
}""",
        4, '1 << 32', "Shifting by a count GREATER THAN OR EQUAL TO the type's bit width (>= 32 for a 32-bit int) is strictly UNDEFINED BEHAVIOR!",
        [
            ('A', 'Guaranteed to be 0', False, 'Thought all bits were shifted out, leaving zero.', 'On x86 CPUs, the shift instruction masks the shift count to 5 bits (32 & 31 = 0), resulting in 1 << 0 = 1, NOT 0! The C standard declares it UB.'),
            ('B', 'Guaranteed to be 1', False, 'Assumed hardware x86 masking behavior is guaranteed by C.', 'x86 hardware masks counts, but other architectures (ARM, PowerPC) handle shifts differently. C declares it undefined.'),
            ('C', 'Undefined Behavior', True, 'Under ISO C §6.5.7#3, if the value of the right operand is negative or is greater than or equal to the width of the promoted left operand, the behavior is strictly Undefined Behavior.', ''),
            ('D', 'Compilation error', False, 'Thought shifting by bit width is rejected by the compiler.', 'Compilers issue a warning (-Wshift-count-overflow), but compile the code.'),
        ],
        'Shifting by a count >= width of the promoted left operand (32 bits) is Undefined Behavior under ISO C §6.5.7#3.',
        'ISO/IEC 9899:1999 §6.5.7#3',
        "Bitwise Shift Constraints in ISO C:\n1. Standard Specification (§6.5.7#3):\n   'If the value of the right operand is negative or is greater than or equal to the width of the promoted left operand, the behavior is undefined.'\n2. Hardware Implementation Divergence:\n   - On x86/x64 processors, the shift instructions (SHL, SHR) mask the count with 0x1F (31 decimal) for 32-bit operands. Thus, 1 << 32 executes as 1 << (32 & 31) = 1 << 0 = 1!\n   - On ARM processors, shift counts are masked differently, and counts >= 32 produce 0.\n   - Because hardware architectures diverge, the ISO C committee deliberately classified shifts by >= bit width as Undefined Behavior.\n3. Optimizing compilers may fold 1 << 32 to 0, 1, or remove branches entirely.\n\nExam Trap: For a 32-bit integer, valid shift counts are strictly 0 through 31. Shifting by 32 is NOT 0; it is Undefined Behavior!",
        [
            (1, 4, 'Expression 1 << 32 evaluated. Left operand has width 32 bits; right operand count is 32 (>= width).', {'shift_count': 32, 'bit_width': 32}, {'stack': []}),
            (2, 4, 'Constraint violation of ISO C §6.5.7#3: right operand >= bit width of promoted left operand.', {'violation': '§6.5.7#3'}, {'stack': []}),
            (3, 4, 'Expression invokes UNDEFINED BEHAVIOR.', {'status': 'UNDEFINED BEHAVIOR'}, {'stack': []}),
        ]
    )

    # Q076: Casting Away Constness to Modify Object -> Key D
    add_q(
        76, 'CAT_SEQ_UB', 'Tricky', 'Casting Away Constness to Modify Object',
        'What is the behavior of attempting to modify an originally const object via pointer casting?',
        r"""#include <stdio.h>
int main() {
    const int x = 10;
    int *p = (int *)&x;
    *p = 20;
    printf("%d\n", x);
    return 0;
}""",
        5, '*p = 20;', 'Casting away constness to modify an object ORIGINALLY DECLARED CONST is UNDEFINED BEHAVIOR under ISO C §6.7.3!',
        [
            ('A', 'Guaranteed to print 20', False, 'Thought casting to int* successfully bypasses const protection.', 'Casting bypasses compiler type-checking, but standard semantics declare the runtime write Undefined Behavior.'),
            ('B', 'Compilation Error', False, 'Thought the compiler blocks pointer casting from const int* to int*.', 'Explicit casting ((int*)&x) suppresses compiler type mismatch errors.'),
            ('C', 'Guaranteed to print 10', False, 'Thought const prevents runtime modification unconditionally.', 'Depending on optimization level, compiler constant propagation may print 10 while the memory at &x is modified or crashed.'),
            ('D', 'Undefined Behavior (May crash, print 10, or print 20)', True, 'Under ISO C §6.7.3#5, if an attempt is made to modify an object defined with a const-qualified type through use of an lvalue with non-const-qualified type, the behavior is strictly Undefined Behavior. If placed in read-only memory, it crashes; otherwise output depends on compiler constant propagation.', ''),
        ],
        'Modifying an object originally defined as const is Undefined Behavior under ISO C §6.7.3#5. The compiler may place it in .rodata or optimize x to constant 10.',
        'ISO/IEC 9899:1999 §6.7.3#5',
        'Const Qualifier Semantics and Optimization Hazards:\n1. Standard Specification (§6.7.3#5):\n   \'If an attempt is made to modify an object defined with a const-qualified type through use of an lvalue with non-const-qualified type, the behavior is undefined.\'\n2. Compiler Optimization Behaviors:\n   - Case 1: If const int x is placed in read-only memory (.rodata), the write *p = 20 triggers a Segmentation Fault (SIGSEGV) at runtime.\n   - Case 2: If x is placed on the stack, the memory at &x might be overwritten with 20, BUT the compiler\'s constant propagation optimization may replace printf("%d\\n", x) with printf("%d\\n", 10) directly at compile-time!\n   - In that scenario, printing x outputs 10, while printing *p outputs 20 from the exact same address!\n3. The standard explicitly declares this Undefined Behavior so compilers are free to optimize const objects aggressively.\n\nExam Trap: Distinguish casting away const on an originally non-const object (which is legal) vs an originally const object (which is UB).',
        [
            (1, 4, 'const int x = 10 declared. Stored in stack frame or .rodata with const qualifier.', {'x': 10}, {'stack': [{'name': 'x', 'addr': '0x1000', 'val': 10, 'const': True}]}),
            (2, 5, 'Cast (int*)&x bypasses compile-time type check. Pointer p holds &x without const qualifier.', {'p': '0x1000'}, {'stack': [{'name': 'p', 'addr': '0x1008', 'val': '0x1000', 'pointsTo': 'x'}]}),
            (3, 6, 'Write *p = 20 violates ISO C §6.7.3#5: modifying an originally const-qualified object -> UNDEFINED BEHAVIOR.', {'status': 'UNDEFINED BEHAVIOR'}, {'stack': []}),
        ]
    )

    # Q077: Accessing Memory After free() -> Key A
    add_q(
        77, 'CAT_SEQ_UB', 'Medium', 'Accessing Memory After free()',
        'What is the status of the following program?',
        r"""#include <stdio.h>
#include <stdlib.h>
int main() {
    int *p = malloc(sizeof(int));
    *p = 100;
    free(p);
    printf("%d\n", *p);
    return 0;
}""",
        7, '*p', 'free(p) releases the allocated memory back to the heap! Accessing *p afterwards is a USE-AFTER-FREE, causing UNDEFINED BEHAVIOR!',
        [
            ('A', 'Undefined Behavior (Dangling pointer / Use-after-free)', True, 'Under ISO C §7.20.3#1, deallocated memory becomes indeterminate and accessing it via *p is a Use-After-Free (Dangling Pointer) vulnerability that invokes Undefined Behavior.', ''),
            ('B', 'Guaranteed to print 100', False, 'Thought freed heap memory retains its content indefinitely.', 'The heap memory manager may immediately overwrite the freed block with freelist metadata pointers or return the page to the OS.'),
            ('C', 'Guaranteed to print 0', False, 'Thought free() zeroes the memory.', 'free() does not zero out heap memory for performance reasons.'),
            ('D', 'Compilation error', False, 'Thought the compiler detects use-after-free at compile-time.', 'Standard C compilers do not track heap lifetimes across function calls; code compiles cleanly.'),
        ],
        'Calling free(p) invalidates the pointer. Accessing *p after free is a Use-After-Free bug, invoking Undefined Behavior.',
        'ISO/IEC 9899:1999 §7.20.3#1',
        "Heap Deallocation and Use-After-Free Vulnerabilities:\n1. Standard Specification (§7.20.3#1):\n   'The value of a pointer that refers to deallocated space is indeterminate.'\n2. Heap Allocator Internals:\n   - malloc(sizeof(int)) allocates a chunk from the process heap (e.g. 0x00602010).\n   - *p = 100 stores integer 100 in the allocated heap chunk.\n   - free(p) returns the chunk to the glibc/ptmalloc freelist (or Windows heap).\n   - The memory allocator immediately repurposes the chunk's payload to store linked-list forward/backward pointers (fd/bk pointers) for heap binning.\n3. Consequences of Dereferencing *p:\n   - Accessing *p reads corrupted heap management metadata.\n   - If the memory page was unmapped via munmap/VirtualFree, a Segmentation Fault occurs.\n   - In cybersecurity, Use-After-Free (UAF) is a notorious vulnerability used to achieve arbitrary code execution.\n\nExam Trap: Best practice to prevent UAF: immediately set pointer to NULL after freeing: free(p); p = NULL;.",
        [
            (1, 5, 'malloc allocates 4 bytes on heap at 0x00602010. *p = 100.', {'p': '0x00602010', '*p': 100}, {'stack': [{'name': 'p', 'addr': '0x1000', 'val': '0x00602010'}], 'heap': [{'addr': '0x00602010', 'val': 100, 'status': 'ALLOCATED'}]}),
            (2, 7, 'free(p) deallocates heap chunk: returned to allocator freelist. Pointer p becomes DANGLING.', {'p': '0x00602010 (dangling)'}, {'heap': [{'addr': '0x00602010', 'status': 'FREED'}]}),
            (3, 8, 'printf reads *p: Use-After-Free access -> UNDEFINED BEHAVIOR.', {'status': 'UNDEFINED BEHAVIOR (UAF)'}, {'stack': []}),
        ]
    )

    # Q078: Calling free() Twice on Same Pointer -> Key B
    add_q(
        78, 'CAT_SEQ_UB', 'Easy', 'Calling free() Twice on Same Pointer',
        'What is the consequence of executing free(p) twice on the same dynamically allocated pointer?',
        r"""#include <stdlib.h>
int main() {
    int *p = malloc(sizeof(int));
    free(p);
    free(p);
    return 0;
}""",
        5, 'free(p);', 'Calling free() twice on the same heap pointer is a DOUBLE-FREE bug, causing heap corruption and UNDEFINED BEHAVIOR (abort / crash)!',
        [
            ('A', 'The second free is safely ignored as a no-op', False, 'Thought free() checks whether memory was already freed.', 'free() has no standard mechanism to detect already-freed pointers; double-freeing corrupts the internal heap bin linked list.'),
            ('B', 'Undefined Behavior (Heap corruption / Process crash)', True, 'Under ISO C §7.20.3.3#2, if free() is called with a pointer that does not match a currently allocated chunk, the behavior is Undefined Behavior. Modern allocators detect heap corruption and abort the program immediately.', ''),
            ('C', 'Compilation error', False, 'Thought calling free twice on the same variable is rejected by the compiler.', 'Compiler does not track dynamic memory lifecycle; compiles without error.'),
            ('D', 'Memory leak', False, 'Memory was freed, not leaked.', 'A double-free corrupts heap state, not leaks it.'),
        ],
        'Double-freeing a pointer corrupts heap management metadata, invoking Undefined Behavior (§7.20.3.3#2) and typically aborting the process.',
        'ISO/IEC 9899:1999 §7.20.3.3#2',
        "Double-Free Mechanics and Security Hazards:\n1. Standard Specification (§7.20.3.3#2):\n   'If the argument does not match a pointer earlier returned by the calloc, malloc, or realloc function, or if the space has been deallocated by a call to free or realloc, the behavior is undefined.'\n2. Heap Manager Double-Free Detection:\n   - When a chunk is freed, it is inserted into a freelist (e.g. tcache or fastbin in glibc).\n   - Calling free(p) a second time attempts to insert the same chunk into the freelist again, creating a cyclic loop in the singly linked list.\n   - Modern heap implementations (glibc, Windows Heap) include double-free sanity checks; when detected, they call abort() with an error message like: 'free(): double free detected in tcache 2'.\n3. In older systems, double-free vulnerabilities allowed attackers to hijack chunk forward pointers to write arbitrary memory.\n\nExam Trap: Always set p = NULL after freeing. Calling free(NULL) is guaranteed safe, completely preventing double-free crashes!",
        [
            (1, 4, 'malloc allocates 4 bytes at heap address 0x00602010.', {'p': '0x00602010'}, {'heap': [{'addr': '0x00602010', 'status': 'ALLOCATED'}]}),
            (2, 5, 'First free(p): chunk returned to heap freelist.', {'p': '0x00602010'}, {'heap': [{'addr': '0x00602010', 'status': 'FREED'}]}),
            (3, 6, 'Second free(p): deallocating an already-freed chunk -> DOUBLE FREE -> Heap corruption / Abort crash.', {'status': 'CRASH (DOUBLE FREE)'}, {'heap': []}),
        ]
    )

    # Q079: Passing NULL to free() -> Key C
    add_q(
        79, 'CAT_SEQ_UB', 'Easy', 'Passing NULL to free()',
        'What does the ISO C standard guarantee when calling free(NULL)?',
        r"""#include <stdlib.h>
int main() {
    int *p = NULL;
    free(p);
    return 0;
}""",
        4, 'free(p);', 'ISO C explicitly guarantees that free(NULL) performs NO ACTION and safely returns without error!',
        [
            ('A', 'It crashes with a Segmentation Fault', False, 'Confused calling free(NULL) with dereferencing a NULL pointer (*NULL).', 'free checks if the pointer is NULL internally before doing anything; it never crashes on NULL.'),
            ('B', 'It causes Undefined Behavior', False, 'Thought passing NULL to library functions is always undefined.', 'free(NULL) is explicitly standardized and guaranteed safe.'),
            ('C', 'It performs no action and safely returns without error', True, 'Under ISO C §7.20.3.3#2, if the argument passed to free() is a null pointer, no action occurs. It is guaranteed to be a safe no-op.', ''),
            ('D', 'Compilation error', False, 'Passing NULL to free is standard C idiom.', 'Valid syntax.'),
        ],
        'ISO C §7.20.3.3#2 guarantees that if ptr is a null pointer, no action occurs. free(NULL) is completely safe.',
        'ISO/IEC 9899:1999 §7.20.3.3#2',
        "The Safe free(NULL) Guarantee:\n1. ISO C Specification (§7.20.3.3#2):\n   'If ptr is a null pointer, no action occurs.'\n2. Implementation:\n   - Inside the C standard library, free() is implemented with an early guard check:\n     void free(void *ptr) {\n         if (ptr == NULL) return;\n         // deallocation logic...\n     }\n3. Coding Idiom Takeaway:\n   - Writing if (p != NULL) free(p); is redundant boilerplate.\n   - Calling free(p) directly is always clean and safe, even if p is NULL.\n   - Furthermore, initializing pointers to NULL (int *p = NULL;) ensures cleanup handlers can safely free them without risking undefined behavior.",
        [
            (1, 4, 'Pointer p initialized to NULL (0x00000000) on stack.', {'p': 'NULL'}, {'stack': [{'name': 'p', 'addr': '0x1000', 'val': 'NULL'}]}),
            (2, 5, 'free(NULL) called: standard library checks ptr == NULL and returns immediately.', {'action': 'NO-OP'}, {'stack': []}),
            (3, 6, 'main returns 0 cleanly.', {'exit_code': 0}, {'stack': []}),
        ]
    )

    # Q080: One-Past-the-End Pointer Legality -> Key D
    add_q(
        80, 'CAT_SEQ_UB', 'Nightmare', 'One-Past-the-End Pointer Legality',
        'Given int arr[5]; which pointer arithmetic expression is strictly legal according to the ISO C standard?',
        r"""#include <stdio.h>
int main() {
    int arr[5];
    int *p1 = arr + 5;
    int *p2 = arr + 6;
    (void)p1;
    (void)p2;
    return 0;
}""",
        4, 'arr + 5', 'In C, computing a pointer ONE past the end (arr + 5) is LEGAL! Computing TWO past the end (arr + 6) is UNDEFINED BEHAVIOR, even without dereferencing!',
        [
            ('A', 'Both arr + 5 and arr + 6 are Undefined Behavior', False, 'Thought pointer arithmetic outside array bounds is always undefined.', 'The C standard explicitly guarantees one-past-the-end pointer arithmetic for loop bounds.'),
            ('B', 'Both are valid as long as neither is dereferenced', False, 'Thought pointer computation alone is always legal.', 'Computing a pointer beyond one-past-the-end is Undefined Behavior immediately upon computation.'),
            ('C', 'arr + 5 can be dereferenced safely', False, 'Dereferencing one-past-the-end accesses unallocated memory, causing UB.', 'arr + 5 can only be computed and compared, never dereferenced.'),
            ('D', 'arr + 5 is valid to compute (but not dereference); arr + 6 is Undefined Behavior', True, 'Under ISO C §6.5.6#8, pointer arithmetic is legal if the result points to an element of the array object or ONE past the last element. Computing arr + 5 is valid. Computing arr + 6 points more than one past the end, invoking Undefined Behavior immediately upon address evaluation.', ''),
        ],
        'ISO C §6.5.6#8 permits computing pointers up to one-past-the-end (arr + 5). Computing beyond that (arr + 6) is Undefined Behavior.',
        'ISO/IEC 9899:1999 §6.5.6#8',
        "One-Past-the-End Pointer Arithmetic Rules:\n1. Standard Specification (§6.5.6#8):\n   'If both the pointer operand and the result point to elements of the same array object, or one past the last element of the array object, the evaluation shall not produce an overflow; otherwise, the behavior is undefined.'\n2. Why One-Past-the-End Exists:\n   - Standard C loop idiom:\n     for (int *p = arr; p < arr + 5; p++) { ... }\n   - To evaluate the loop termination condition when p reaches the end, the pointer must legally hold the address immediately following the last element (arr + 5).\n3. Limits of the Guarantee:\n   - arr + 5 may be computed and compared with relational operators (<, <=, ==, !=).\n   - arr + 5 may NEVER be dereferenced (*(arr + 5) is UB).\n   - Merely computing arr + 6 (two past the end) is Undefined Behavior immediately, even if never dereferenced (e.g. on segmented architectures where offset addition might wrap segment boundaries).\n4. Code Hygiene: (void)p1; (void)p2; suppresses compiler unused-variable warnings cleanly.",
        [
            (1, 4, 'int arr[5] allocated on stack (indices 0..4, addresses 0x1000..0x1010).', {'arr': '5 ints'}, {'stack': [{'name': 'arr[0..4]', 'addr': '0x1000-0x1010'}]}),
            (2, 5, 'arr + 5 evaluates to address 0x1014: one-past-the-end -> STRICTLY LEGAL under §6.5.6#8.', {'p1': '0x1014 (legal)'}, {'stack': [{'name': 'p1', 'val': '0x1014'}]}),
            (3, 6, 'arr + 6 evaluates to address 0x1018: exceeds one-past-the-end -> UNDEFINED BEHAVIOR immediately upon computation.', {'status': 'UNDEFINED BEHAVIOR'}, {'stack': []}),
        ]
    )

    print("bank_part3 loaded (22 questions, total 80).")
