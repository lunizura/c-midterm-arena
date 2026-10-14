# bank_part3.py: Q059 to Q080 (CAT_SCOPE_LIFETIME & CAT_SEQ_UB)

def load_part3(add_q):
    # =========================================================================
    # CAT_SCOPE_LIFETIME (Q059 - Q070)
    # =========================================================================

    # Q059: Static Local Variable Value Retention
    add_q(
        59, "CAT_SCOPE_LIFETIME", "Easy", "Static Local Variable Value Retention",
        "What is the output of the following program?",
        """#include <stdio.h>
void counter() {
    static int count = 0;
    count++;
    printf("%d ", count);
}
int main() {
    counter();
    counter();
    counter();
    printf("\\n");
    return 0;
}""",
        4, "static int count = 0;", "static local variables have static storage duration: they persist throughout program lifetime and retain values across function calls!",
        [
            ("A", "1 2 3", True, "count is initialized once and retains its incremented value across successive calls.", ""),
            ("B", "1 1 1", False, "Thought count was re-initialized to 0 on every call.", "static variables are only initialized once when program execution begins."),
            ("C", "0 1 2", False, "Thought printf printed before count++.", "count++ runs before printf."),
            ("D", "Compile error", False, "Thought static cannot be used inside functions.", "static inside functions specifies static storage duration.")
        ],
        "Static local variables persist in the data segment across function calls. Their lifetime spans the entire program execution.",
        "ISO/IEC 9899 §6.2.4#3",
        "Calls output 1, 2, 3.",
        [
            (1, 4, "Initial load: count = 0.", {"count": 0}, None),
            (2, 5, "Call 1: count++ -> 1. Prints 1.", {"count": 1}, None),
            (3, 5, "Call 2: count retained at 1. count++ -> 2. Prints 2.", {"count": 2}, None),
            (4, 5, "Call 3: count retained at 2. count++ -> 3. Prints 3.", {"count": 3}, None)
        ]
    )

    # Q060: Static Local Initialization with Function Call
    add_q(
        60, "CAT_SCOPE_LIFETIME", "Tricky", "Static Initialization Evaluated Once Only",
        "What is the output of the following program?",
        """#include <stdio.h>
void func(int x) {
    static int val = 10;
    val += x;
    printf("%d ", val);
}
int main() {
    func(5);
    func(10);
    printf("\\n");
    return 0;
}""",
        4, "static int val = 10;", "static int val = 10 is performed only ONCE at compile/startup, NOT on subsequent invocations of func!",
        [
            ("A", "15 25", True, "First call: 10 + 5 = 15. Second call: 15 + 10 = 25.", ""),
            ("B", "15 20", False, "Thought val reset to 10 on the second call (10 + 10 = 20).", "static variables are NOT re-initialized on subsequent function calls."),
            ("C", "5 10", False, "Thought val started at 0.", "val starts at 10."),
            ("D", "10 20", False, "Random calculation error.", "val accumulates each call.")
        ],
        "All objects with static storage duration are initialized before program startup. The initializer is not re-evaluated.",
        "ISO/IEC 9899 §6.7.9#4",
        "First call adds 5 (15). Second call adds 10 to existing 15 (25).",
        [
            (1, 4, "val initialized to 10 at startup.", {"val": 10}, None),
            (2, 5, "func(5): val becomes 15.", {"val": 15}, None),
            (3, 5, "func(10): val becomes 15 + 10 = 25.", {"val": 25}, None)
        ]
    )

    # Q061: Dangling Pointer Returning Stack Address
    add_q(
        61, "CAT_SCOPE_LIFETIME", "Medium", "Returning Address of Local Stack Variable",
        "What is wrong with the following function?",
        """#include <stdio.h>
int* get_number() {
    int x = 42;
    return &x;
}
int main() {
    int *p = get_number();
    printf("%d\\n", *p);
    return 0;
}""",
        5, "return &x;", "x is an automatic local variable destroyed when get_number() returns! p becomes a DANGLING POINTER (Undefined Behavior)!",
        [
            ("A", "Undefined Behavior: Dereferencing a dangling pointer to an expired stack frame", True, "x ceases to exist when get_number() returns. *p dereferences invalid stack memory.", ""),
            ("B", "Guaranteed to print 42", False, "Thought stack memory remains intact indefinitely.", "Subsequent function calls overwrite stack frames; reading expired stack is UB."),
            ("C", "Compilation Error: cannot return pointer", False, "Thought returning pointers is illegal.", "Returning pointers is valid; returning addresses of local automatic variables is dangerous."),
            ("D", "Memory Leak", False, "Confused stack allocation with malloc.", "Stack memory is automatically deallocated.")
        ],
        "The lifetime of an automatic object extends from entry into the block until execution of that block ends. Accessing it after lifetime ends is Undefined Behavior.",
        "ISO/IEC 9899 §6.2.4#6",
        "Compilers issue a warning: function returns address of local variable.",
        [
            (1, 4, "x created on stack of get_number.", None, None),
            (2, 5, "get_number returns; stack frame popped. Address &x is now invalid.", None, None),
            (3, 9, "*p accesses reclaimed stack frame -> Undefined Behavior.", None, None)
        ]
    )

    # Q062: Block Scope Variable Shadowing
    add_q(
        62, "CAT_SCOPE_LIFETIME", "Medium", "Inner Block Scope Variable Shadowing",
        "What is the output of the following program?",
        """#include <stdio.h>
int main() {
    int x = 10;
    {
        int x = 20;
        printf("%d ", x);
    }
    printf("%d\\n", x);
    return 0;
}""",
        6, "int x = 20;", "The inner x shadows the outer x within { ... }. Once the inner block exits, the outer x (10) is restored!",
        [
            ("A", "20 10", True, "Inner block prints inner x (20). Outer block prints outer x (10).", ""),
            ("B", "20 20", False, "Thought inner assignment modified outer x.", "inner x is a completely distinct variable in a nested scope."),
            ("C", "10 10", False, "Thought inner declaration was ignored.", "Inner declaration shadows the outer name."),
            ("D", "Compilation Error: duplicate variable x", False, "Thought re-declaring x in nested block is illegal.", "C explicitly permits variable shadowing in nested scopes.")
        ],
        "An identifier declared in an inner block hides any declaration of the same identifier in an enclosing block until the inner block terminates.",
        "ISO/IEC 9899 §6.2.1#4",
        "Inner prints 20, outer prints 10.",
        [
            (1, 4, "Outer x = 10.", {"outer_x": 10}, None),
            (2, 6, "Inner x = 20 created, shadowing outer x. Prints 20.", {"inner_x": 20}, None),
            (3, 8, "Inner block exits; inner x destroyed.", None, None),
            (4, 9, "Outer x printed (10).", {"stdout": "20 10"}, None)
        ]
    )

    # Q063: Global vs Local Shadowing
    add_q(
        63, "CAT_SCOPE_LIFETIME", "Easy", "Global Variable Shadowing by Local Variable",
        "What is the output of the following program?",
        """#include <stdio.h>
int val = 100;
void test() {
    printf("%d ", val);
}
int main() {
    int val = 50;
    test();
    printf("%d\\n", val);
    return 0;
}""",
        8, "int val = 50;", "test() accesses the file-scope GLOBAL val (100). main() prints its own LOCAL val (50)!",
        [
            ("A", "100 50", True, "test() has no local val, so it sees global 100. main() has local val 50.", ""),
            ("B", "50 50", False, "Thought local val in main affected test().", "Local variables in main are not visible to other functions."),
            ("C", "100 100", False, "Thought local val had no effect.", "Local val shadows global val inside main's scope."),
            ("D", "Compile error", False, "Thought global and local names cannot collide.", "Shadowing is fully standard.")
        ],
        "Identifiers declared outside any block have file scope. Identifiers declared inside a block have block scope. test() resolves to file scope val (100).",
        "ISO/IEC 9899 §6.2.1",
        "Output is 100 50.",
        [
            (1, 2, "Global val = 100.", {"global_val": 100}, None),
            (2, 8, "main declares local val = 50.", {"main_val": 50}, None),
            (3, 4, "test() prints global val = 100.", {"stdout": "100 "}, None),
            (4, 10, "main prints local val = 50.", {"stdout": "100 50"}, None)
        ]
    )

    # Q064: Static Global Variable (Internal Linkage)
    add_q(
        64, "CAT_SCOPE_LIFETIME", "Medium", "Static at File Scope (Internal Linkage)",
        "What does the static keyword mean when applied to a global variable outside all functions?",
        """static int secret_key = 42;
int main() {
    return 0;
}""",
        1, "static int secret_key = 42;", "static at file scope gives the identifier INTERNAL LINKAGE, making it invisible to other translation units (.c files)!",
        [
            ("A", "It limits the variable's visibility strictly to this translation unit (source file)", True, "static at file scope restricts linkage to internal only.", ""),
            ("B", "It prevents the variable from ever being modified (like const)", False, "Confused static with const.", "static variables are fully mutable."),
            ("C", "It causes the variable to be allocated on the stack", False, "Global variables are always in data/BSS segment.", "static changes linkage, not storage segment."),
            ("D", "It makes the variable thread-safe", False, "static has no synchronization properties.", "C does not add thread-safety with static.")
        ],
        "If the declaration of an identifier for an object has file scope and contains the storage-class specifier static, the identifier has internal linkage.",
        "ISO/IEC 9899 §6.2.2#3",
        "Other files cannot access secret_key via extern.",
        [
            (1, 1, "secret_key declared with internal linkage. Visible only within this .c file.", None, None)
        ]
    )

    # Q065: Extern Variable Declaration
    add_q(
        65, "CAT_SCOPE_LIFETIME", "Medium", "extern Variable Declaration vs Definition",
        "Which of the following is true about: extern int x; ?",
        """extern int x;
int main() {
    return 0;
}""",
        1, "extern int x;", "extern int x; is a DECLARATION only! It allocates NO storage and tells the compiler x is defined elsewhere!",
        [
            ("A", "It declares x without allocating memory, informing the compiler that x is defined elsewhere", True, "extern declaration informs the linker without reserving memory.", ""),
            ("B", "It allocates memory for x and initializes it to 0", False, "Declarations with extern and no initializer do not allocate storage.", "Storage must be allocated by a definition: int x;"),
            ("C", "It makes x a local variable in all functions", False, "extern refers to an external identifier.", "Has file scope."),
            ("D", "It is a syntax error without an initializer", False, "Adding an initializer converts it into a definition.", "extern int x; is valid declaration.")
        ],
        "extern declares an identifier with external linkage without defining storage (unless an initializer is provided).",
        "ISO/IEC 9899 §6.7#5",
        "The linker resolves x to a definition in another translation unit.",
        [
            (1, 1, "Declaration of x with external linkage. Storage allocated in another translation unit.", None, None)
        ]
    )

    # Q066: Uninitialized Automatic Local Variable
    add_q(
        66, "CAT_SCOPE_LIFETIME", "Easy", "Uninitialized Local Automatic Variable Value",
        "What is the value of an uninitialized local variable int x; ?",
        """#include <stdio.h>
int main() {
    int x;
    printf("%d\\n", x);
    return 0;
}""",
        4, "int x;", "Automatic local variables are NOT initialized by default! They hold indeterminate GARBAGE values from the stack!",
        [
            ("A", "Indeterminate (garbage value from stack memory)", True, "Local automatic variables are not zero-initialized; reading them produces indeterminate values.", ""),
            ("B", "Always 0", False, "Confused local variables with global/static variables.", "Only static and global variables are automatically initialized to 0."),
            ("C", "Compilation error", False, "Thought C forbids uninitialized variables.", "Compilers emit a warning, not an error."),
            ("D", "NULL", False, "x is an int, not a pointer.", "Scalar integers hold garbage bytes.")
        ],
        "If an object that has automatic storage duration is not initialized explicitly, its value is indeterminate.",
        "ISO/IEC 9899 §6.7.9#10",
        "Accessing an indeterminate value is Undefined Behavior.",
        [
            (1, 4, "x allocated on stack with existing stack garbage bits.", None, None)
        ]
    )

    # Q067: Uninitialized Global and Static Variables
    add_q(
        67, "CAT_SCOPE_LIFETIME", "Easy", "Default Initialization of Global and Static Variables",
        "What is the guaranteed default value of an uninitialized global variable in C?",
        """#include <stdio.h>
int global_num;
int main() {
    printf("%d\\n", global_num);
    return 0;
}""",
        3, "int global_num;", "Variables with static storage duration (globals and static locals) are GUARANTEED by ISO C to be initialized to ZERO!",
        [
            ("A", "Guaranteed to be 0", True, "Static storage duration objects without explicit initializers are zero-initialized (placed in .bss segment).", ""),
            ("B", "Indeterminate (garbage value)", False, "Confused global variables with local automatic variables.", "Automatic locals are garbage, but globals are strictly 0."),
            ("C", "-1", False, "Random guess.", "C standard mandates zero-initialization."),
            ("D", "Compilation error", False, "Globals do not require initializers.", "Valid C syntax.")
        ],
        "If an object that has static storage duration is not initialized explicitly, then if it has arithmetic type, it is initialized to (positive or unsigned) zero.",
        "ISO/IEC 9899 §6.7.9#10",
        "Placed into the BSS segment, zeroed out by the OS loader at process start.",
        [
            (1, 2, "global_num allocated in .bss; initialized to 0 by runtime.", {"global_num": 0}, None),
            (2, 4, "printf prints 0.", {"stdout": "0"}, None)
        ]
    )

    # Q068: Variable Lifetime Inside Loop Body
    add_q(
        68, "CAT_SCOPE_LIFETIME", "Medium", "Automatic Variable Lifetime Inside Loop Iterations",
        "What is the output of the following program?",
        """#include <stdio.h>
int main() {
    for (int i = 0; i < 3; i++) {
        int count = 0;
        count++;
        printf("%d ", count);
    }
    printf("\\n");
    return 0;
}""",
        5, "int count = 0;", "count is an automatic variable whose lifetime begins and ends WITH EACH ITERATION! It is re-initialized to 0 every time!",
        [
            ("A", "1 1 1", True, "count is created anew and set to 0 on each loop iteration, incrementing to 1.", ""),
            ("B", "1 2 3", False, "Assumed count preserved its value like a static variable.", "Without the static keyword, automatic variables are destroyed at block exit."),
            ("C", "0 0 0", False, "Thought count++ had no effect before printf.", "count becomes 1 each time."),
            ("D", "Compile error", False, "Thought declaring variables inside for-loop body is illegal.", "Valid in C99 and later.")
        ],
        "The scope and lifetime of count are restricted to the block of the for-loop. With each iteration, count is created, initialized to 0, and destroyed.",
        "ISO/IEC 9899 §6.2.4#6",
        "Prints 1 1 1.",
        [
            (1, 5, "Iteration 1: count initialized to 0 -> count++ -> 1. Prints 1.", {"count": 1}, None),
            (2, 5, "Iteration 2: count re-initialized to 0 -> count++ -> 1. Prints 1.", {"count": 1}, None),
            (3, 5, "Iteration 3: count re-initialized to 0 -> count++ -> 1. Prints 1.", {"count": 1}, None)
        ]
    )

    # Q069: Infinite Recursion Stack Overflow
    add_q(
        69, "CAT_SCOPE_LIFETIME", "Easy", "Missing Base Case in Recursion",
        "What happens when calling a recursive function with no base case?",
        """#include <stdio.h>
void recurse(int n) {
    printf("%d ", n);
    recurse(n + 1);
}
int main() {
    recurse(1);
    return 0;
}""",
        4, "recurse(n + 1);", "Without a base case, recursive stack frames consume all stack memory, causing a STACK OVERFLOW (SIGSEGV)!",
        [
            ("A", "Runtime Crash (Stack Overflow / Segmentation Fault)", True, "Each call pushes a new stack frame until the process stack limit is exceeded.", ""),
            ("B", "Prints numbers indefinitely forever", False, "Physical call stacks are finite in size (typically 1MB to 8MB).", "Infinite recursion always crashes when stack is exhausted."),
            ("C", "Compilation error", False, "Thought compiler detects infinite recursion.", "Compilers do not halt compilation on runaway recursion."),
            ("D", "Stops when integer overflows", False, "Stack space runs out long before integer reaches INT_MAX.", "Stack exhaustion occurs within ~10,000 to 100,000 frames.")
        ],
        "Each recursive invocation pushes return addresses and parameters onto the execution stack. Unbounded recursion exhausts stack memory, triggering SIGSEGV.",
        "ISO/IEC 9899 §6.5.2.2",
        "Process is terminated by the OS.",
        [
            (1, 4, "Stack frames pile up: recurse(1) -> recurse(2) -> ... -> Stack exhaustion.", None, None)
        ]
    )

    # Q070: Recursive Trace Prediction
    add_q(
        70, "CAT_SCOPE_LIFETIME", "Medium", "Recursive Function Execution Trace",
        "What is the return value of mystery(4)?",
        """#include <stdio.h>
int mystery(int n) {
    if (n <= 1) return 1;
    return n + mystery(n - 2);
}
int main() {
    printf("%d\\n", mystery(4));
    return 0;
}""",
        4, "return n + mystery(n - 2);", "mystery(4) = 4 + mystery(2) = 4 + (2 + mystery(0)) = 4 + 2 + 1 = 7!",
        [
            ("A", "7", True, "mystery(4) = 4 + mystery(2); mystery(2) = 2 + mystery(0); mystery(0) = 1. Total = 4 + 2 + 1 = 7.", ""),
            ("B", "10", False, "Calculated sum of 4 + 3 + 2 + 1 (decrement by 1 instead of 2).", "The recursive call steps by n - 2, skipping odd numbers."),
            ("C", "6", False, "Forgot to add the base case return value 1.", "mystery(0) returns 1 (n <= 1)."),
            ("D", "1", False, "Returned base case alone.", "Accumulates n + recursive call.")
        ],
        "Trace: mystery(4) -> 4 + mystery(2). mystery(2) -> 2 + mystery(0). Since 0 <= 1, mystery(0) returns 1. Result = 4 + 2 + 1 = 7.",
        "ISO/IEC 9899 §6.5.2.2",
        "Prints 7.",
        [
            (1, 4, "mystery(4): returns 4 + mystery(2).", None, None),
            (2, 4, "mystery(2): returns 2 + mystery(0).", None, None),
            (3, 3, "mystery(0): returns 1 (base case).", None, None),
            (4, 7, "Total: 4 + 2 + 1 = 7.", {"result": 7}, None)
        ]
    )

    # =========================================================================
    # CAT_SEQ_UB (Q071 - Q080)
    # =========================================================================

    # Q071: Unsequenced Modification (i = i++)
    add_q(
        71, "CAT_SEQ_UB", "Nightmare", "Unsequenced Modification (i = i++)",
        "What does the C standard (C99 / C11) say about the statement: i = i++; ?",
        """#include <stdio.h>
int main() {
    int i = 5;
    i = i++;
    printf("%d\\n", i);
    return 0;
}""",
        4, "i = i++;", "Modifying variable i more than once between sequence points (unsequenced side effect and value computation) is UNDEFINED BEHAVIOR!",
        [
            ("A", "Undefined Behavior", True, "Modifying a scalar object twice without an intervening sequence point is strictly undefined behavior in ISO C.", ""),
            ("B", "Guaranteed to print 5", False, "Thought postfix increment happens after assignment.", "Standard states behavior is undefined; different compilers produce 5, 6, or garbage."),
            ("C", "Guaranteed to print 6", False, "Thought increment takes precedence.", "Undefined behavior means no guarantee exists."),
            ("D", "Compilation Error", False, "Thought compiler forbids i = i++.", "Compilers issue a -Wunsequenced warning but compile the code.")
        ],
        "Between the previous and next sequence point an object shall have its stored value modified at most once by the evaluation of an expression.",
        "ISO/IEC 9899:1999 §6.5#2 & C11 §6.5#2",
        "Violating this constraint produces Undefined Behavior. The compiler may emit any assembly instruction order.",
        [
            (1, 4, "i is modified by assignment and by ++ with no sequence point -> Undefined Behavior.", None, None)
        ]
    )

    # Q072: Unsequenced Modification in Array Subscript (a[i] = i++)
    add_q(
        72, "CAT_SEQ_UB", "Nightmare", "Unsequenced Subscript Indexing (a[i] = i++)",
        "What is the status of the expression: arr[i] = i++; ?",
        """#include <stdio.h>
int main() {
    int arr[5] = {0};
    int i = 1;
    arr[i] = i++;
    return 0;
}""",
        5, "arr[i] = i++;", "Reading i to determine subscript and modifying i via i++ without an intervening sequence point is UNDEFINED BEHAVIOR!",
        [
            ("A", "Undefined Behavior", True, "The prior value of i is read to determine the array index, but i is also modified by i++ unsequenced.", ""),
            ("B", "arr[1] is guaranteed to be 1", False, "Assumed left-hand side index is evaluated first.", "Order of evaluation between LHS and RHS of = is unspecified, producing UB."),
            ("C", "arr[2] is guaranteed to be 1", False, "Assumed RHS evaluated first.", "Evaluation order is not defined."),
            ("D", "Compilation Error", False, "Valid syntax, semantic flaw.", "Produces warning, not error.")
        ],
        "The prior value shall be read only to determine the value to be stored. Reading i for the subscript while modifying i produces Undefined Behavior.",
        "ISO/IEC 9899 §6.5#2",
        "Whether arr[1] or arr[2] is modified depends on compiler optimization choices.",
        [
            (1, 5, "Unsequenced read and write of scalar i -> Undefined Behavior.", None, None)
        ]
    )

    # Q073: Multiple Side Effects in Argument List (printf("%d %d", ++i, ++i))
    add_q(
        73, "CAT_SEQ_UB", "Nightmare", "Unspecified Argument Evaluation Order",
        "What is the output of: printf(\"%d %d\\n\", ++i, ++i); with int i = 1?",
        """#include <stdio.h>
int main() {
    int i = 1;
    printf("%d %d\\n", ++i, ++i);
    return 0;
}""",
        4, "printf(\"%d %d\\n\", ++i, ++i);", "In C, the order of evaluation of function arguments is UNSPECIFIED! Modifying i twice is unsequenced Undefined Behavior!",
        [
            ("A", "Undefined Behavior (Unspecified evaluation order)", True, "The C standard does not specify left-to-right or right-to-left argument evaluation; modifying i twice produces UB.", ""),
            ("B", "Guaranteed to print 2 3", False, "Assumed arguments are evaluated strictly left-to-right.", "C standard §6.5.2.2#10 explicitly states argument evaluation order is unspecified."),
            ("C", "Guaranteed to print 3 2", False, "Assumed arguments are evaluated strictly right-to-left (x86 cdecl).", "Calling convention is an ABI detail, not a language guarantee."),
            ("D", "Compilation Error", False, "Compiles with warning.", "Not rejected by compiler.")
        ],
        "The order of evaluation of arguments in a function call is unspecified. Modifying the same scalar object multiple times without sequence points is Undefined Behavior.",
        "ISO/IEC 9899 §6.5.2.2#10",
        "GCC on x86 may print '3 2', Clang may print '2 3', or unexpected values.",
        [
            (1, 4, "Arguments ++i and ++i are evaluated in unspecified order without sequence point -> UB.", None, None)
        ]
    )

    # Q074: Signed Integer Overflow (INT_MAX + 1)
    add_q(
        74, "CAT_SEQ_UB", "Tricky", "Signed vs Unsigned Overflow Semantics",
        "What does the C standard dictate regarding: INT_MAX + 1 for signed 32-bit int?",
        """#include <stdio.h>
#include <limits.h>
int main() {
    int x = INT_MAX;
    printf("%d\\n", x + 1);
    return 0;
}""",
        5, "x + 1", "In ISO C, SIGNED integer overflow is UNDEFINED BEHAVIOR! (Unlike unsigned integer overflow, which wraps modulo 2^N)!",
        [
            ("A", "Undefined Behavior", True, "ISO C explicitly states signed integer overflow produces undefined behavior (allowing aggressive compiler optimizations).", ""),
            ("B", "Guaranteed to wrap to INT_MIN (-2147483648)", False, "Confused hardware two's complement behavior with language standard specification.", "While x86 hardware wraps, C standard classifies it as UB; compilers may optimize away overflow checks."),
            ("C", "Guaranteed to throw an exception", False, "C does not throw software exceptions on integer overflow.", "Hardware traps only occur on division by zero."),
            ("D", "Saturates at INT_MAX", False, "C does not support saturating arithmetic.", "Standard classifies as UB.")
        ],
        "If an exceptional condition occurs during the evaluation of an expression (that is, if the result is not mathematically defined or not in the range of representable values), the behavior is undefined.",
        "ISO/IEC 9899 §6.5#5",
        "Because signed overflow is UB, GCC may optimize 'if (x + 1 < x)' to false assuming overflow never happens.",
        [
            (1, 5, "INT_MAX + 1 exceeds maximum representable signed int -> Undefined Behavior.", None, None)
        ]
    )

    # Q075: Bit Shift by Greater than Type Width (1 << 32)
    add_q(
        75, "CAT_SEQ_UB", "Tricky", "Bitwise Shift Exceeding Bit Width",
        "On a system with 32-bit int, what is the behavior of: 1 << 32 ?",
        """#include <stdio.h>
int main() {
    int x = 1 << 32;
    printf("%d\\n", x);
    return 0;
}""",
        4, "1 << 32", "Shifting by a count that is negative or GREATER THAN OR EQUAL TO the width of the promoted type is UNDEFINED BEHAVIOR!",
        [
            ("A", "Undefined Behavior", True, "In C, shifting by >= bit-width (32 for a 32-bit int) is strictly undefined behavior.", ""),
            ("B", "Guaranteed to be 0", False, "Assumed all bits were shifted out.", "On x86 CPUs, shift count is masked with 0x1F (modulo 32), meaning 1 << 32 executes as 1 << 0 = 1!"),
            ("C", "Guaranteed to be 1", False, "Confused CPU instruction masking with C standard guarantee.", "The standard states it is UB, not guaranteed 1."),
            ("D", "Compilation error", False, "Compiles with warning.", "Valid syntax.")
        ],
        "If the value of the right operand is negative or is greater than or equal to the width of the promoted left operand, the behavior is undefined.",
        "ISO/IEC 9899 §6.5.7#3",
        "On x86, SHL masks shift operand by 31, yielding 1; on other CPUs, it yields 0. C standard declares it UB.",
        [
            (1, 4, "Shift count 32 >= width of int (32 bits) -> Undefined Behavior.", None, None)
        ]
    )

    # Q076: Modifying Const Object via Pointer Cast
    add_q(
        76, "CAT_SEQ_UB", "Tricky", "Casting Away Constness to Modify Object",
        "What happens when modifying a const variable via pointer cast?",
        """#include <stdio.h>
int main() {
    const int x = 10;
    int *p = (int*)&x;
    *p = 20;
    printf("%d\\n", x);
    return 0;
}""",
        5, "*p = 20;", "Attempting to modify an object declared with CONST-qualified type through a non-const pointer is UNDEFINED BEHAVIOR!",
        [
            ("A", "Undefined Behavior (May crash, print 10, or print 20)", True, "Modifying an originally const object through cast pointer is strictly undefined behavior.", ""),
            ("B", "Guaranteed to print 20", False, "Thought casting away const makes mutation valid.", "The compiler may place const variables in read-only memory or constant-propagate 10 into printf."),
            ("C", "Compilation Error", False, "Thought explicit cast is forbidden.", "C allows the cast (int*)&x, but the resulting write is illegal at runtime."),
            ("D", "Guaranteed to print 10", False, "Thought write is ignored.", "Undefined behavior provides no guarantees.")
        ],
        "If an attempt is made to modify an object defined with a const-qualified type through use of an lvalue with non-const-qualified type, the behavior is undefined.",
        "ISO/IEC 9899 §6.7.3#6",
        "Compilers frequently optimize printf to print constant 10 directly without reloading x from memory.",
        [
            (1, 4, "x declared const int.", None, None),
            (2, 5, "Writing to const object via *p -> Undefined Behavior.", None, None)
        ]
    )

    # Q077: Use-After-Free
    add_q(
        77, "CAT_SEQ_UB", "Medium", "Accessing Memory After free()",
        "What is the status of accessing memory after free(ptr)?",
        """#include <stdio.h>
#include <stdlib.h>
int main() {
    int *p = malloc(sizeof(int));
    *p = 100;
    free(p);
    printf("%d\\n", *p);
    return 0;
}""",
        7, "*p", "Accessing memory after calling free() is USE-AFTER-FREE, which is UNDEFINED BEHAVIOR!",
        [
            ("A", "Undefined Behavior (Dangling pointer / Use-after-free)", True, "Once free() is called, the memory is released back to the heap manager. Dereferencing is UB.", ""),
            ("B", "Guaranteed to print 100", False, "Thought free() leaves memory untouched.", "Heap allocator may zero, poison, or reassign that memory chunk immediately."),
            ("C", "Guaranteed to print 0", False, "Thought free() zeroes out memory.", "free() does not zero memory."),
            ("D", "Compilation error", False, "Compiler does not track runtime free() calls.", "Valid syntax.")
        ],
        "The value of a pointer that refers to deallocated space becomes indeterminate. Dereferencing it is Undefined Behavior.",
        "ISO/IEC 9899 §7.22.3#4",
        "Can cause data corruption or arbitrary code execution vulnerabilities.",
        [
            (1, 6, "free(p) deallocates memory. p is now a dangling pointer.", None, None),
            (2, 7, "*p dereferences deallocated heap memory -> Use-after-free UB.", None, None)
        ]
    )

    # Q078: Double Free Bug
    add_q(
        78, "CAT_SEQ_UB", "Easy", "Calling free() Twice on Same Pointer",
        "What happens when free() is called twice on the same allocated pointer?",
        """#include <stdlib.h>
int main() {
    int *p = malloc(sizeof(int));
    free(p);
    free(p);
    return 0;
}""",
        5, "free(p);", "Calling free() twice on the same pointer is a DOUBLE FREE, leading to Undefined Behavior and heap corruption crash!",
        [
            ("A", "Undefined Behavior (Heap corruption / Process crash)", True, "Deallocating already freed memory corrupts the heap metadata.", ""),
            ("B", "Second free is safely ignored", False, "Only free(NULL) is safely ignored. free() on non-null already-freed pointer is fatal.", "To prevent double free, set p = NULL after free(p);"),
            ("C", "Compilation error", False, "Compiler cannot track dynamic free calls.", "Compiles without error."),
            ("D", "Memory leak", False, "Memory was freed.", "Heap corruption occurs.")
        ],
        "If a pointer to freed memory is passed to free, the behavior is undefined. Modern allocators detect this and abort with 'double free detected'.",
        "ISO/IEC 9899 §7.22.3.3#2",
        "Process terminates with SIGABRT.",
        [
            (1, 4, "p freed.", None, None),
            (2, 5, "p freed again -> Heap corruption abort.", None, None)
        ]
    )

    # Q079: free(NULL) Guarantee
    add_q(
        79, "CAT_SEQ_UB", "Easy", "Passing NULL to free()",
        "What does the C standard guarantee when calling free(NULL)?",
        """#include <stdlib.h>
int main() {
    int *p = NULL;
    free(p);
    return 0;
}""",
        4, "free(p);", "ISO C explicitly guarantees that free(NULL) performs NO ACTION and is completely safe!",
        [
            ("A", "It performs no action and safely returns without error", True, "The C standard explicitly guarantees free(NULL) is a safe no-op.", ""),
            ("B", "It crashes with a Segmentation Fault", False, "Confused free(NULL) with dereferencing *NULL.", "free checks for NULL internally before deallocating."),
            ("C", "It causes Undefined Behavior", False, "free(NULL) is strictly standard-defined.", "Guaranteed safe by §7.22.3.3."),
            ("D", "Compilation error", False, "Passing NULL pointer to free is valid C.", "Standard practice.")
        ],
        "If ptr is a null pointer, no action occurs.",
        "ISO/IEC 9899 §7.22.3.3#2",
        "Checking 'if (p != NULL) free(p);' is redundant because free(NULL) is guaranteed safe.",
        [
            (1, 4, "free(NULL) called: standard guarantees safe no-op.", None, None)
        ]
    )

    # Q080: Out-of-Bounds Pointer Arithmetic vs Dereference
    add_q(
        80, "CAT_SEQ_UB", "Nightmare", "One-Past-the-End Pointer Legality",
        "Given int arr[5]; which pointer arithmetic expression is strictly legal in C?",
        """#include <stdio.h>
int main() {
    int arr[5];
    int *p1 = arr + 5; // one past the end
    int *p2 = arr + 6; // two past the end
    return 0;
}""",
        4, "arr + 5", "In C, computing a pointer ONE past the end (arr + 5) is LEGAL! Computing TWO past the end (arr + 6) is UNDEFINED BEHAVIOR!",
        [
            ("A", "arr + 5 is valid to compute (but not dereference); arr + 6 is Undefined Behavior", True, "ISO C explicitly guarantees one-past-the-end pointer arithmetic. Beyond that is UB.", ""),
            ("B", "Both arr + 5 and arr + 6 are Undefined Behavior", False, "One-past-the-end is legal for loop termination comparisons.", "C standard §6.5.6#8 explicitly guarantees one-past-the-end."),
            ("C", "Both are valid as long as neither is dereferenced", False, "Merely computing arr + 6 is UB.", "Pointer computation beyond one-past-the-end violates §6.5.6#8."),
            ("D", "arr + 5 can be dereferenced safely", False, "Dereferencing one-past-the-end is UB.", "Address can be stored and compared, but not dereferenced.")
        ],
        "If the pointer operand and the result point to elements of the same array object, or one past the last element of the array object, the evaluation shall not produce an overflow; otherwise, the behavior is undefined.",
        "ISO/IEC 9899 §6.5.6#8",
        "arr + 5 is valid for comparison; arr + 6 is UB immediately upon computation.",
        [
            (1, 4, "arr + 5 points to one-past-the-end -> LEGAL.", None, None),
            (2, 5, "arr + 6 exceeds one-past-the-end -> UNDEFINED BEHAVIOR.", None, None)
        ]
    )

print("bank_part3 loaded (22 questions, total 80).")
