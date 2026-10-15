# syllabus_part3.py
# Q069 - Q084: TOPIC_FUNCTIONS (Functions and Procedures)
# Q085 - Q100: TOPIC_ARRAYS (Arrays, 2D Arrays, Strings as Char Arrays)

def load_part3(add_q):
    # =========================================================================
    # TOPIC_FUNCTIONS (Q069 - Q084)
    # =========================================================================

    # Q069: Pass-by-Value Primitive Protection
    add_q(
        69, "TOPIC_FUNCTIONS", "Easy", "Pass-by-Value Variable Modification",
        "What is the output of the following program?",
        """#include <stdio.h>
void modify(int x) {
    x = 100;
}
int main() {
    int a = 10;
    modify(a);
    printf("%d\\n", a);
    return 0;
}""",
        4, "x = 100;", "In C, arguments are passed BY VALUE! Parameter x is a separate local copy; modifying x does NOT modify a in main!",
        [
            ("A", "10", True, "In C, all basic types are passed by value. 'a' in main remains 10.", ""),
            ("B", "100", False, "Assumed C passes parameters by reference like in other languages.", "C is strictly pass-by-value. To modify 'a', its address (&a) must be passed."),
            ("C", "0", False, "a was initialized to 10.", "Value does not change."),
            ("D", "Compile error", False, "Pass-by-value is standard C.", "Valid C syntax.")
        ],
        "C uses call-by-value for function arguments. The called function receives copies of the arguments in its own local stack frame.",
        "ISO/IEC 9899 §6.5.2.2",
        "Prints 10.",
        [(1, 7, "In main: a = 10.", {"a": 10}, None),
         (2, 3, "modify called: parameter x is initialized with copy 10. x = 100 modifies copy only.", {"x": 100, "a": 10}, None),
         (3, 9, "Back in main: a is unchanged (10).", {"stdout": "10"}, None)]
    )

    # Q070: Failed Swap Function Without Pointers
    add_q(
        70, "TOPIC_FUNCTIONS", "Medium", "Failed Swap Implementation (Pass-by-Value)",
        "What is the output of the following program?",
        """#include <stdio.h>
void swap(int x, int y) {
    int temp = x;
    x = y;
    y = temp;
}
int main() {
    int a = 5, b = 10;
    swap(a, b);
    printf("%d %d\\n", a, b);
    return 0;
}""",
        10, "swap(a, b);", "swap modifies only its local copies x and y. The original variables a and b in main are UNCHANGED (5 10)!",
        [
            ("A", "5 10", True, "x and y are local to swap. When swap returns, its stack frame is destroyed, leaving a and b unchanged.", ""),
            ("B", "10 5", False, "Assumed swap worked.", "Without pointers, swap cannot affect variables in the caller's stack frame!"),
            ("C", "5 5", False, "Variables were not overwritten.", "Values remain intact."),
            ("D", "10 10", False, "temp preserved values inside swap.", "No mutation occurred in main.")
        ],
        "Parameters x and y are local variables initialized with copies of a and b. Swapping x and y does not affect a and b.",
        "ISO/IEC 9899 §6.5.2.2",
        "Prints 5 10.",
        [(1, 10, "swap(5, 10) called: copies x and y swapped inside function frame.", None, None),
         (2, 11, "printf prints original a (5) and b (10).", {"stdout": "5 10"}, None)]
    )

    # Q071: Function Prototype Declaration Requirement
    add_q(
        71, "TOPIC_FUNCTIONS", "Medium", "Function Prototype Declaration Necessity",
        "What is the purpose of a function prototype declaration: int add(int, int); ?",
        """int add(int, int); // Prototype
int main() {
    return add(2, 3);
}
int add(int a, int b) {
    return a + b;
}""",
        1, "int add(int, int);", "A prototype informs the compiler about the function's name, return type, and parameter types BEFORE its actual definition!",
        [
            ("A", "It informs the compiler of the function's signature before its call, enabling type checking", True, "Prototypes allow calling functions defined later in the file and enforce type safety.", ""),
            ("B", "It allocates memory for the function body", False, "Prototypes do not allocate code memory.", "Memory is defined in the implementation."),
            ("C", "It automatically exports the function to the operating system", False, "Has nothing to do with OS export.", "Compiler declaration."),
            ("D", "It causes the function to execute immediately", False, "Declarations do not execute code.", "Type declaration only.")
        ],
        "A function prototype declarator declares the return type and parameter types of a function.",
        "ISO/IEC 9899 §6.7.6.3",
        "Prevents implicit int return type warnings and ensures argument checking.",
        [(1, 1, "add declared with signature (int, int) -> int.", None, None)]
    )

    # Q072: Void Procedure Return Behavior
    add_q(
        72, "TOPIC_FUNCTIONS", "Easy", "Void Procedure Early Return",
        "What is printed when check_num(0) is called?",
        """#include <stdio.h>
void check_num(int n) {
    if (n <= 0) {
        printf("ZERO_OR_LESS\\n");
        return;
    }
    printf("POSITIVE\\n");
}
int main() {
    check_num(0);
    return 0;
}""",
        6, "return;", "The return statement immediately exits the void function! 'POSITIVE' is NEVER printed!",
        [
            ("A", "ZERO_OR_LESS", True, "The if condition (0 <= 0) passes, prints ZERO_OR_LESS, and return exits the function.", ""),
            ("B", "ZERO_OR_LESS POSITIVE", False, "Thought execution continued after return.", "return terminates function execution immediately."),
            ("C", "POSITIVE", False, "0 <= 0 is true.", "Entered if branch."),
            ("D", "Compile error", False, "Bare return; in void functions is standard.", "Valid C syntax.")
        ],
        "A return statement with no expression shall have appeared only in a function whose return type is void.",
        "ISO/IEC 9899 §6.8.6.4",
        "Prints ZERO_OR_LESS.",
        [(1, 4, "n <= 0 (0 <= 0) is true. Prints ZERO_OR_LESS.", {"stdout": "ZERO_OR_LESS"}, None),
         (2, 6, "return exits function immediately.", None, None)]
    )

    # Q073: Global vs Local Variable Shadowing
    add_q(
        73, "TOPIC_FUNCTIONS", "Medium", "Global Variable Shadowing by Local Variable",
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
        8, "int val = 50;", "test() accesses the global val (100). main() prints its own local val (50) which shadowed the global inside main!",
        [
            ("A", "100 50", True, "test() has no local val, so it resolves to global 100. main() resolves to local 50.", ""),
            ("B", "50 50", False, "Thought local val in main modified test().", "Local variables in main are not visible to test()."),
            ("C", "100 100", False, "Thought local val had no effect.", "Local val shadows global inside main."),
            ("D", "Compile error", False, "Variable shadowing across scopes is valid C.", "Standard scope resolution.")
        ],
        "Identifiers declared inside a block hide any declaration of the same identifier in outer or file scope.",
        "ISO/IEC 9899 §6.2.1",
        "Prints 100 50.",
        [(1, 2, "Global val = 100.", {"global_val": 100}, None),
         (2, 4, "test() accesses global val (100). Prints 100.", {"stdout": "100 "}, None),
         (3, 10, "main() accesses local val (50). Prints 50.", {"stdout": "100 50"}, None)]
    )

    # Q074: Static Local Variable Value Retention
    add_q(
        74, "TOPIC_FUNCTIONS", "Easy", "Static Local Variable Value Retention",
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
            ("A", "1 2 3", True, "count is initialized once and retains its value across calls, incrementing 1, 2, 3.", ""),
            ("B", "1 1 1", False, "Thought count reset to 0 on every call.", "static variables are initialized only once at program start."),
            ("C", "0 1 2", False, "count++ runs before printf.", "First print is 1."),
            ("D", "Compile error", False, "static locals are standard C.", "Valid C syntax.")
        ],
        "Static local variables persist in the data segment across function calls.",
        "ISO/IEC 9899 §6.2.4#3",
        "Prints 1 2 3.",
        [(1, 5, "Call 1: count becomes 1.", {"count": 1}, None),
         (2, 5, "Call 2: count retained at 1 -> becomes 2.", {"count": 2}, None),
         (3, 5, "Call 3: count retained at 2 -> becomes 3.", {"count": 3}, None)]
    )

    # Q075: Static Variable Initialization Timing
    add_q(
        75, "TOPIC_FUNCTIONS", "Tricky", "Static Variable Initialized Once Only",
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
        4, "static int val = 10;", "static int val = 10 is evaluated only ONCE at program startup, NOT on subsequent invocations of func!",
        [
            ("A", "15 25", True, "Call 1: val = 10 + 5 = 15. Call 2: val = 15 + 10 = 25.", ""),
            ("B", "15 20", False, "Thought val reset to 10 on second call (10 + 10 = 20).", "static variables are NOT re-initialized on subsequent calls."),
            ("C", "5 10", False, "val starts at 10.", "Initial value is 10."),
            ("D", "10 20", False, "val accumulates on each call.", "Prints 15 25.")
        ],
        "All objects with static storage duration are initialized before program startup.",
        "ISO/IEC 9899 §6.7.9#4",
        "Prints 15 25.",
        [(1, 5, "func(5): val becomes 10 + 5 = 15.", {"val": 15}, None),
         (2, 5, "func(10): val becomes 15 + 10 = 25.", {"val": 25}, None)]
    )

    # Q076: Local Variable Destruction at Return
    add_q(
        76, "TOPIC_FUNCTIONS", "Easy", "Automatic Local Variable Lifetime",
        "When does the lifetime of a regular (non-static) local variable end?",
        """void calculate() {
    int temp = 42;
    // ...
} // What happens to temp here?""",
        4, "} // What happens to temp here?", "Automatic local variables are destroyed when their enclosing function block exits!",
        [
            ("A", "It is deallocated when the function returns (stack frame is popped)", True, "Automatic local variables exist only during function execution.", ""),
            ("B", "It stays in memory until the entire program terminates", False, "Confused automatic variables with static/global variables.", "Automatic variables are stack-allocated and ephemeral."),
            ("C", "It becomes a global variable", False, "Scope and lifetime do not change dynamically.", "Scope remains local."),
            ("D", "It causes a memory leak if not freed", False, "Stack memory is automatically reclaimed by CPU stack pointer adjustment.", "No manual free needed.")
        ],
        "The lifetime of an automatic object extends from entry into the block until execution of that block ends.",
        "ISO/IEC 9899 §6.2.4#6",
        "Stack memory is reclaimed automatically.",
        [(1, 4, "temp lifetime ends at function block exit.", None, None)]
    )

    # Q077: Recursive Factorial Trace
    add_q(
        77, "TOPIC_FUNCTIONS", "Easy", "Recursive Factorial Function Call Trace",
        "What is the return value of factorial(4)?",
        """#include <stdio.h>
int factorial(int n) {
    if (n <= 1) return 1;
    return n * factorial(n - 1);
}
int main() {
    printf("%d\\n", factorial(4));
    return 0;
}""",
        4, "return n * factorial(n - 1);", "factorial(4) = 4 * factorial(3) = 4 * 3 * 2 * 1 = 24!",
        [
            ("A", "24", True, "4 * 3 * 2 * 1 = 24.", ""),
            ("B", "10", False, "Added 4 + 3 + 2 + 1 instead of multiplying.", "Factorial is product, not sum."),
            ("C", "12", False, "Calculation error.", "4 * 6 = 24."),
            ("D", "1", False, "Base case only.", "Multiplies through call stack.")
        ],
        "Trace: fact(4) -> 4 * fact(3) -> 4 * 3 * fact(2) -> 4 * 3 * 2 * fact(1) = 24.",
        "ISO/IEC 9899 §6.5.2.2",
        "Prints 24.",
        [(1, 4, "fact(4) = 4 * fact(3).", None, None),
         (2, 4, "fact(3) = 3 * fact(2).", None, None),
         (3, 4, "fact(2) = 2 * fact(1) = 2 * 1 = 2.", None, None),
         (4, 7, "Total: 4 * 3 * 2 = 24.", {"result": 24}, None)]
    )

    # Q078: Missing Recursion Base Case Stack Overflow
    add_q(
        78, "TOPIC_FUNCTIONS", "Easy", "Missing Base Case in Recursion",
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
        4, "recurse(n + 1);", "Without a base case, recursive stack frames pile up until stack memory is exhausted, causing a STACK OVERFLOW (SIGSEGV)!",
        [
            ("A", "Runtime Crash (Stack Overflow / Segmentation Fault)", True, "Each call pushes a new stack frame until available stack memory is exhausted.", ""),
            ("B", "Loops infinitely without crashing", False, "Stack space is finite (typically 1MB to 8MB).", "Exhaustion crashes the program."),
            ("C", "Compile error", False, "Compiler does not detect infinite recursion.", "Compiles cleanly."),
            ("D", "Stops when integer overflows", False, "Stack memory runs out long before reaching INT_MAX.", "Crashes after ~10,000 to 50,000 calls.")
        ],
        "Unbounded recursion consumes stack frames until a stack overflow occurs.",
        "ISO/IEC 9899 §6.5.2.2",
        "Process terminated by OS.",
        [(1, 4, "Recursive calls without base case exhaust stack -> SIGSEGV.", None, None)]
    )

    # Q079: Recursive Countdown Print Order
    add_q(
        79, "TOPIC_FUNCTIONS", "Medium", "Print Order in Recursive Call (Before vs After)",
        "What is the output of the following program?",
        """#include <stdio.h>
void count(int n) {
    if (n == 0) return;
    count(n - 1);
    printf("%d ", n);
}
int main() {
    count(3);
    printf("\\n");
    return 0;
}""",
        5, "printf(\"%d \", n);", "printf is AFTER the recursive call! The calls unwind from the deepest frame (n=1) up to n=3, printing 1 2 3!",
        [
            ("A", "1 2 3", True, "Calls: count(3) -> count(2) -> count(1) -> count(0) returns. Unwinds and prints 1, then 2, then 3.", ""),
            ("B", "3 2 1", False, "Thought printf executed before the recursive call.", "printf is located after count(n-1), so it runs during stack unwinding!"),
            ("C", "3 2 1 0", False, "0 hit base case return before printf.", "0 is never printed."),
            ("D", "0 1 2 3", False, "0 returned immediately.", "Prints 1 2 3.")
        ],
        "Statements placed after recursive calls execute in reverse (LIFO) call order as frames are popped from the stack.",
        "ISO/IEC 9899 §6.5.2.2",
        "Prints 1 2 3.",
        [(1, 4, "count(3) calls count(2) -> count(1) -> count(0).", None, None),
         (2, 5, "Unwinding: count(1) prints 1. count(2) prints 2. count(3) prints 3.", {"stdout": "1 2 3"}, None)]
    )

    # Q080: Recursive Fibonacci Trace
    add_q(
        80, "TOPIC_FUNCTIONS", "Medium", "Recursive Fibonacci Call Tree",
        "What does fib(4) return?",
        """#include <stdio.h>
int fib(int n) {
    if (n <= 1) return n;
    return fib(n - 1) + fib(n - 2);
}
int main() {
    printf("%d\\n", fib(4));
    return 0;
}""",
        4, "return fib(n - 1) + fib(n - 2);", "fib(0)=0, fib(1)=1, fib(2)=1, fib(3)=2, fib(4)=3!",
        [
            ("A", "3", True, "fib(4) = fib(3) + fib(2) = 2 + 1 = 3.", ""),
            ("B", "4", False, "fib(4) is 3 in 0-indexed Fibonacci sequence (0, 1, 1, 2, 3).", "Sequence: 0, 1, 1, 2, 3, 5..."),
            ("C", "5", False, "That is fib(5).", "fib(4) is 3."),
            ("D", "2", False, "That is fib(3).", "fib(4) = 2 + 1 = 3.")
        ],
        "fib(4) expands to fib(3) + fib(2) = (1 + 1) + 1 = 3.",
        "ISO/IEC 9899 §6.5.2.2",
        "Prints 3.",
        [(1, 4, "fib(4) = fib(3) + fib(2) = 2 + 1 = 3.", {"result": 3}, None)]
    )

    # Q081: Function Call As Expression Operand
    add_q(
        81, "TOPIC_FUNCTIONS", "Easy", "Combining Function Return Values in Expression",
        "What is the output of the following program?",
        """#include <stdio.h>
int square(int x) {
    return x * x;
}
int main() {
    int res = square(3) + square(4);
    printf("%d\\n", res);
    return 0;
}""",
        7, "int res = square(3) + square(4);", "square(3) is 9, square(4) is 16. 9 + 16 = 25!",
        [
            ("A", "25", True, "3*3 = 9. 4*4 = 16. 9 + 16 = 25.", ""),
            ("B", "49", False, "Calculated (3 + 4)^2 = 7^2 = 49.", "Functions are evaluated individually first."),
            ("C", "12", False, "Multiplied 3 * 4.", "Adds the squared values."),
            ("D", "7", False, "3 + 4.", "Squares before adding.")
        ],
        "Function calls are postfix expressions with higher precedence than addition.",
        "ISO/IEC 9899 §6.5.2",
        "Prints 25.",
        [(1, 7, "square(3) = 9. square(4) = 16. 9 + 16 = 25.", {"res": 25}, None)]
    )

    # Q082: Nested Function Call Evaluation
    add_q(
        82, "TOPIC_FUNCTIONS", "Easy", "Nested Function Call Evaluation Order",
        "What is the output of the following program?",
        """#include <stdio.h>
int add_two(int x) { return x + 2; }
int mult_three(int x) { return x * 3; }
int main() {
    int res = add_two(mult_three(4));
    printf("%d\\n", res);
    return 0;
}""",
        5, "add_two(mult_three(4))", "Inner call mult_three(4) evaluates FIRST to 12. Then add_two(12) evaluates to 14!",
        [
            ("A", "14", True, "mult_three(4) = 12. add_two(12) = 14.", ""),
            ("B", "18", False, "Evaluated add_two first: (4 + 2) * 3 = 18.", "Inner arguments evaluate before outer function call!"),
            ("C", "12", False, "Forgot add_two.", "Outer call adds 2."),
            ("D", "6", False, "Arithmetic error.", "12 + 2 = 14.")
        ],
        "Arguments to a function call are evaluated before the function is called.",
        "ISO/IEC 9899 §6.5.2.2",
        "Prints 14.",
        [(1, 5, "mult_three(4) returns 12. add_two(12) returns 14.", {"res": 14}, None)]
    )

    # Q083: Variable Shadowing Inside Nested Block
    add_q(
        83, "TOPIC_FUNCTIONS", "Medium", "Block Scope Variable Shadowing",
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
            ("C", "10 10", False, "Thought inner declaration was ignored.", "Inner declaration shadows outer name."),
            ("D", "Compile error", False, "Variable shadowing in nested blocks is valid C.", "Standard C scope rule.")
        ],
        "An identifier declared in an inner block hides any declaration of the same identifier in an enclosing block.",
        "ISO/IEC 9899 §6.2.1#4",
        "Prints 20 10.",
        [(1, 4, "Outer x = 10.", {"outer_x": 10}, None),
         (2, 6, "Inner x = 20 created, shadowing outer x. Prints 20.", {"inner_x": 20}, None),
         (3, 8, "Inner block exits; inner x destroyed. Outer x is 10.", {"stdout": "20 10"}, None)]
    )

    # Q084: Recursion Countdown Print Sequence
    add_q(
        84, "TOPIC_FUNCTIONS", "Medium", "Pre-Order Print in Recursion",
        "What is the output of the following program?",
        """#include <stdio.h>
void print_down(int n) {
    if (n == 0) return;
    printf("%d ", n);
    print_down(n - 1);
}
int main() {
    print_down(3);
    printf("\\n");
    return 0;
}""",
        4, "printf(\"%d \", n);", "printf is BEFORE the recursive call! It prints n BEFORE calling print_down(n - 1), outputting 3 2 1!",
        [
            ("A", "3 2 1", True, "printf executes on the way DOWN the recursion: prints 3, calls print_down(2), prints 2, calls print_down(1), prints 1.", ""),
            ("B", "1 2 3", False, "Confused pre-order print with post-order print.", "Because printf is before the recursive call, it prints in descending order."),
            ("C", "3 2 1 0", False, "0 returns at base case without printing.", "0 is not printed."),
            ("D", "0 1 2 3", False, "Inverted order.", "Prints 3 2 1.")
        ],
        "Statements executed before recursive calls execute in top-down (call) order.",
        "ISO/IEC 9899 §6.5.2.2",
        "Prints 3 2 1.",
        [(1, 4, "Prints 3 -> calls print_down(2) -> prints 2 -> calls print_down(1) -> prints 1.", {"stdout": "3 2 1"}, None)]
    )

    # =========================================================================
    # TOPIC_ARRAYS (Q085 - Q100)
    # =========================================================================

    # Q085: 1D Array 0-Indexed Bounds
    add_q(
        85, "TOPIC_ARRAYS", "Easy", "Array 0-Indexed Subscript Bounds",
        "For an array declared as int arr[5]; which indices are valid?",
        """int arr[5];""",
        1, "int arr[5];", "In C, arrays are 0-indexed! An array of size 5 has valid indices 0, 1, 2, 3, 4! Index 5 is OUT OF BOUNDS!",
        [
            ("A", "0 to 4", True, "C arrays are 0-indexed. Indices run from 0 to N-1 (0 to 4).", ""),
            ("B", "1 to 5", False, "Confused with 1-based indexing in languages like MATLAB or Fortran.", "C arrays always start at index 0."),
            ("C", "0 to 5", False, "Index 5 is the 6th element, exceeding array bounds.", "Valid indices are 0 through 4."),
            ("D", "1 to 4", False, "Forgot index 0.", "0 is the first element.")
        ],
        "An array of size N has elements indexed 0 through N-1.",
        "ISO/IEC 9899 §6.5.2.1",
        "Valid indices are 0 to 4.",
        [(1, 1, "arr[0] through arr[4] are valid.", None, None)]
    )

    # Q086: Array Partial Initialization
    add_q(
        86, "TOPIC_ARRAYS", "Medium", "Partial Initialization Zero-Padding",
        "What is the output of the following program?",
        """#include <stdio.h>
int main() {
    int arr[5] = {1, 2};
    printf("%d %d %d\\n", arr[0], arr[1], arr[2]);
    return 0;
}""",
        4, "int arr[5] = {1, 2};", "If an array initializer has fewer elements than the array size, ALL remaining elements are automatically initialized to ZERO!",
        [
            ("A", "1 2 0", True, "arr[0]=1, arr[1]=2. Remaining elements arr[2], arr[3], arr[4] are automatically set to 0.", ""),
            ("B", "1 2 garbage", False, "Thought uninitialized elements retain garbage values.", "Partial initialization guarantees remaining elements are set to 0!"),
            ("C", "1 2 1", False, "Thought pattern repeated.", "Remaining elements are strictly 0."),
            ("D", "Compile error", False, "Partial initialization is standard C idiom.", "Valid C syntax.")
        ],
        "If there are fewer initializers in a brace-enclosed list than there are elements, the remainder of the aggregate shall be initialized to zero.",
        "ISO/IEC 9899 §6.7.9#21",
        "Prints 1 2 0.",
        [(1, 4, "arr[0]=1, arr[1]=2. arr[2..4] zeroed.", {"arr[0]": 1, "arr[1]": 2, "arr[2]": 0}, None),
         (2, 5, "printf prints 1 2 0.", {"stdout": "1 2 0"}, None)]
    )

    # Q087: Array Initialization Without Size
    add_q(
        87, "TOPIC_ARRAYS", "Easy", "Inferred Array Size from Initializer",
        "What is sizeof(arr) / sizeof(arr[0]) for: int arr[] = {10, 20, 30, 40}; ?",
        """#include <stdio.h>
int main() {
    int arr[] = {10, 20, 30, 40};
    int count = sizeof(arr) / sizeof(arr[0]);
    printf("%d\\n", count);
    return 0;
}""",
        5, "sizeof(arr) / sizeof(arr[0])", "4 elements initialized, so array size is deduced as 4! sizeof(arr) / sizeof(arr[0]) evaluates to 4!",
        [
            ("A", "4", True, "The compiler infers size 4 from the initializer list. sizeof(arr)/sizeof(arr[0]) = 16 / 4 = 4.", ""),
            ("B", "16", False, "16 is the byte size, not element count.", "Divided by sizeof(int) gives 4."),
            ("C", "1", False, "Thought pointer decay occurred.", "In main, sizeof(arr) measures the array object."),
            ("D", "Compile error", False, "Omitting dimension with initializer is standard C.", "Valid C syntax.")
        ],
        "An array of unknown size initialized with a list adopts the size specified by the number of elements in the list.",
        "ISO/IEC 9899 §6.7.9#22",
        "Prints 4.",
        [(1, 4, "arr size inferred as 4 ints (16 bytes). 16 / 4 = 4 elements.", {"count": 4}, None)]
    )

    # Q088: Array Out-of-Bounds Subscript
    add_q(
        88, "TOPIC_ARRAYS", "Medium", "Array Out-of-Bounds Subscripting",
        "What happens when executing arr[5] on an array of size 5?",
        """#include <stdio.h>
int main() {
    int arr[5] = {1, 2, 3, 4, 5};
    printf("%d\\n", arr[5]);
    return 0;
}""",
        4, "arr[5]", "Valid indices are 0 to 4! arr[5] accesses memory outside array bounds, resulting in UNDEFINED BEHAVIOR (garbage or crash)!",
        [
            ("A", "Undefined Behavior (Accesses stack garbage or crashes)", True, "C does not perform runtime array bounds checking. arr[5] reads unallocated stack memory.", ""),
            ("B", "Compilation Error: Array index out of bounds", False, "Thought C compilers reject out-of-bounds indices.", "Standard C does not require bounds checking; it compiles without error."),
            ("C", "Prints 5", False, "arr[4] is the 5th element (0-indexed).", "arr[5] is past the end."),
            ("D", "Prints 0", False, "Out-of-bounds stack memory is not zeroed.", "Contains stack garbage.")
        ],
        "Array indexing in C is unchecked. Subscripting beyond array bounds violates §6.5.6 and produces Undefined Behavior.",
        "ISO/IEC 9899 §6.5.6#8",
        "Reads stack garbage bits.",
        [(1, 4, "arr[5] accesses index 5 (valid: 0..4) -> Undefined Behavior.", None, None)]
    )

    # Q089: Finding Maximum Element Algorithm Trace
    add_q(
        89, "TOPIC_ARRAYS", "Easy", "Finding Maximum in Array Algorithm",
        "What is the output of the following program?",
        """#include <stdio.h>
int main() {
    int arr[] = {14, 5, 29, 11, 8};
    int max = arr[0];
    for (int i = 1; i < 5; i++) {
        if (arr[i] > max) {
            max = arr[i];
        }
    }
    printf("%d\\n", max);
    return 0;
}""",
        7, "max = arr[i];", "The loop scans through the array: 29 is the largest element, so max ends at 29!",
        [
            ("A", "29", True, "29 > 14 becomes the new max, which is never surpassed.", ""),
            ("B", "14", False, "That is initial value.", "29 replaced 14."),
            ("C", "8", False, "That is the last element.", "Max is 29."),
            ("D", "5", False, "That is the minimum element.", "Algorithm finds max.")
        ],
        "Standard linear scan for maximum element.",
        "ISO/IEC 9899 §6.8.5",
        "Prints 29.",
        [(1, 5, "max initialized to arr[0] (14).", {"max": 14}, None),
         (2, 7, "i=2: arr[2] (29) > 14 -> max updated to 29.", {"max": 29}, None),
         (3, 11, "printf prints 29.", {"stdout": "29"}, None)]
    )

    # Q090: Array Linear Search Trace
    add_q(
        90, "TOPIC_ARRAYS", "Easy", "Array Linear Search Index",
        "What index is printed when searching for target = 40?",
        """#include <stdio.h>
int main() {
    int arr[5] = {10, 20, 30, 40, 50};
    int target = 40, found_idx = -1;
    for (int i = 0; i < 5; i++) {
        if (arr[i] == target) {
            found_idx = i;
            break;
        }
    }
    printf("%d\\n", found_idx);
    return 0;
}""",
        7, "found_idx = i; break;", "40 is at index 3: arr[0]=10, arr[1]=20, arr[2]=30, arr[3]=40! Outputs 3!",
        [
            ("A", "3", True, "40 is the 4th element, which is index 3 (0-indexed).", ""),
            ("B", "4", False, "1-indexed confusion.", "In 0-indexed C, 40 is at index 3."),
            ("C", "-1", False, "Target 40 was found in array.", "found_idx updated to 3."),
            ("D", "40", False, "Printed index, not value.", "found_idx is 3.")
        ],
        "Linear search inspects indices sequentially; breaks at index 3.",
        "ISO/IEC 9899 §6.8.5",
        "Prints 3.",
        [(1, 7, "i = 3: arr[3] (40) == target (40). found_idx = 3.", {"found_idx": 3}, None)]
    )

    # Q091: Array Element Mutation in Loop
    add_q(
        91, "TOPIC_ARRAYS", "Medium", "Sequential Array Accumulation Mutation",
        "What is the output of the following program?",
        """#include <stdio.h>
int main() {
    int a[4] = {1, 2, 3, 4};
    for (int i = 1; i < 4; i++) {
        a[i] += a[i - 1];
    }
    printf("%d %d %d %d\\n", a[0], a[1], a[2], a[3]);
    return 0;
}""",
        6, "a[i] += a[i - 1];", "Prefix sums: a[1]=2+1=3. a[2]=3+3=6. a[3]=4+6=10. Outputs 1 3 6 10!",
        [
            ("A", "1 3 6 10", True, "a[0]=1; a[1]=2+1=3; a[2]=3+3=6; a[3]=4+6=10.", ""),
            ("B", "1 2 3 4", False, "Thought array was not modified.", "Elements mutate in place."),
            ("C", "1 3 5 7", False, "Used original array values instead of accumulated mutations.", "a[i-1] uses updated value."),
            ("D", "10 10 10 10", False, "Incorrect calculation.", "Running prefix sum.")
        ],
        "Running sum mutates array elements sequentially in place.",
        "ISO/IEC 9899 §6.5.16.2",
        "Prints 1 3 6 10.",
        [(1, 6, "i=1: a[1] = 2 + 1 = 3.", {"a[1]": 3}, None),
         (2, 6, "i=2: a[2] = 3 + 3 = 6.", {"a[2]": 6}, None),
         (3, 6, "i=3: a[3] = 4 + 6 = 10.", {"a[3]": 10}, None)]
    )

    # Q092: 2D Array Row and Column Indexing
    add_q(
        92, "TOPIC_ARRAYS", "Easy", "2D Array Subscript Coordinates (Row, Column)",
        "Given int m[2][3] = {{10, 20, 30}, {40, 50, 60}}; what is m[1][2]?",
        """#include <stdio.h>
int main() {
    int m[2][3] = {{10, 20, 30}, {40, 50, 60}};
    printf("%d\\n", m[1][2]);
    return 0;
}""",
        4, "m[1][2]", "m[row][col]: row 1 is {40, 50, 60}; column 2 is the 3rd element (60)!",
        [
            ("A", "60", True, "Row index 1, column index 2 is element 60.", ""),
            ("B", "50", False, "Column 2 is the 3rd element (0, 1, 2). 50 is at col 1.", "m[1][1] is 50."),
            ("C", "30", False, "30 is at row 0, col 2 (m[0][2]).", "Row index is 1."),
            ("D", "40", False, "40 is at m[1][0].", "Col index is 2.")
        ],
        "In m[i][j], i is the row index and j is the column index.",
        "ISO/IEC 9899 §6.5.2.1",
        "Prints 60.",
        [(1, 4, "Row 1: {40, 50, 60}. Column 2 accesses 60.", {"val": 60}, None)]
    )

    # Q093: 2D Array Nested Loop Sum
    add_q(
        93, "TOPIC_ARRAYS", "Medium", "2D Array Matrix Elements Summation",
        "What is the output of the following program?",
        """#include <stdio.h>
int main() {
    int m[2][2] = {{1, 2}, {3, 4}};
    int sum = 0;
    for (int r = 0; r < 2; r++) {
        for (int c = 0; c < 2; c++) {
            sum += m[r][c];
        }
    }
    printf("%d\\n", sum);
    return 0;
}""",
        8, "sum += m[r][c];", "Sum of all 4 matrix elements: 1 + 2 + 3 + 4 = 10!",
        [
            ("A", "10", True, "1 + 2 + 3 + 4 = 10.", ""),
            ("B", "6", False, "Added only diagonal (1 + 4 = 5) or one row.", "Sums all 4 elements."),
            ("C", "7", False, "Arithmetic error.", "Sum is 10."),
            ("D", "4", False, "Only counted last element.", "Full traversal.")
        ],
        "Nested loops traverse rows and columns to sum all elements.",
        "ISO/IEC 9899 §6.8.5",
        "Prints 10.",
        [(1, 8, "sum = 1 + 2 + 3 + 4 = 10.", {"sum": 10}, None)]
    )

    # Q094: 2D Array Memory Contiguity
    add_q(
        94, "TOPIC_ARRAYS", "Medium", "Row-Major Contiguous Storage of 2D Arrays",
        "How are elements of a 2D array stored in physical RAM in C?",
        """int m[2][3];""",
        1, "int m[2][3];", "In C, multidimensional arrays are stored in ROW-MAJOR order: all elements of row 0 consecutively, followed immediately by row 1!",
        [
            ("A", "Row-major order (row 0 elements consecutively, then row 1 elements)", True, "C stores multidimensional arrays in contiguous row-major order.", ""),
            ("B", "Column-major order (column 0 elements, then column 1 elements)", False, "Column-major is used by Fortran/MATLAB, not C.", "C is strictly row-major."),
            ("C", "Scattered in random heap memory blocks", False, "2D arrays are contiguous memory blocks.", "Contiguous layout."),
            ("D", "Linked list of pointer rows", False, "int m[2][3] is a flat array, not an array of pointers.", "Single contiguous buffer.")
        ],
        "Multidimensional arrays in C are stored in row-major order: m[0][0], m[0][1], m[0][2], m[1][0], m[1][1], m[1][2].",
        "ISO/IEC 9899 §6.5.2.1",
        "Row-major order.",
        [(1, 1, "Stored contiguously in memory as row 0 followed by row 1.", None, None)]
    )

    # Q095: Strings as Char Arrays and Null-Terminator
    add_q(
        95, "TOPIC_ARRAYS", "Easy", "String Null Terminator in Character Arrays",
        "What is the size of the array char s[] = \"apple\"; ?",
        """#include <stdio.h>
int main() {
    char s[] = "apple";
    printf("%zu\\n", sizeof(s));
    return 0;
}""",
        4, "char s[] = \"apple\";", "\"apple\" has 5 visible characters + 1 implicit NULL TERMINATOR ('\\0') = 6 BYTES!",
        [
            ("A", "6", True, "String literals in C always append a trailing null terminator '\\0'. 5 letters + 1 '\\0' = 6 bytes.", ""),
            ("B", "5", False, "Counted only visible characters. Forgot '\\0'.", "C string literals include the terminating null character."),
            ("C", "4", False, "Confused array with pointer size.", "s is an array object."),
            ("D", "7", False, "Miscounted characters.", "5 + 1 = 6.")
        ],
        "A string literal includes an implicit null character '\\0' at the end. sizeof(s) evaluates to 6.",
        "ISO/IEC 9899 §6.4.5",
        "Prints 6.",
        [(1, 4, "'a','p','p','l','e','\\0' = 6 bytes.", {"sizeof": 6}, None)]
    )

    # Q096: sizeof vs strlen on Char Array
    add_q(
        96, "TOPIC_ARRAYS", "Easy", "Difference Between sizeof and strlen",
        "What is printed by this program?",
        """#include <stdio.h>
#include <string.h>
int main() {
    char str[] = "hello";
    printf("%zu %zu\\n", sizeof(str), strlen(str));
    return 0;
}""",
        6, "sizeof(str), strlen(str)", "sizeof measures total allocated bytes including '\\0' (6). strlen counts visible characters before '\\0' (5)!",
        [
            ("A", "6 5", True, "sizeof is 6 (includes '\\0'). strlen is 5 (excludes '\\0').", ""),
            ("B", "5 5", False, "Forgot that sizeof counts the null terminator.", "sizeof counts all array bytes."),
            ("C", "5 6", False, "Inverted sizeof and strlen.", "sizeof >= strlen."),
            ("D", "6 6", False, "strlen does not count null byte.", "strlen stops before '\\0'.")
        ],
        "sizeof evaluates total array size (6). strlen computes string length up to first null character (5).",
        "ISO/IEC 9899 §6.5.3.4 & §7.24.6.3",
        "Prints 6 5.",
        [(1, 6, "sizeof(str) = 6. strlen(str) = 5.", {"sizeof": 6, "strlen": 5}, None)]
    )

    # Q097: Missing Null Terminator Overflow Trap
    add_q(
        97, "TOPIC_ARRAYS", "Tricky", "Missing Null Terminator in Sized Array",
        "What happens when declaring: char s[5] = \"hello\"; and calling strlen(s)?",
        """#include <stdio.h>
#include <string.h>
int main() {
    char s[5] = "hello";
    printf("%zu\\n", strlen(s));
    return 0;
}""",
        5, "char s[5] = \"hello\";", "In C, this is valid syntax, but NO ROOM remains for '\\0'! strlen(s) reads past array bounds until it randomly finds a 0 byte (UNDEFINED BEHAVIOR)!",
        [
            ("A", "Undefined Behavior (Buffer overread searching for '\\0')", True, "s contains 5 chars without '\\0'. strlen scans past array memory searching for 0.", ""),
            ("B", "Prints 5", False, "Thought strlen stops at array bounds.", "strlen does not know array size; it scans until it hits '\\0'."),
            ("C", "Compilation Error", False, "ISO C §6.7.9#14 explicitly permits omitting '\\0' if array size equals string length!", "Compiles without error."),
            ("D", "Prints 4", False, "All 5 characters are stored.", "Missing '\\0'.")
        ],
        "If the array size equals string length, trailing null character is discarded. strlen causes an out-of-bounds read (Undefined Behavior).",
        "ISO/IEC 9899 §6.7.9#14",
        "Buffer overread UB.",
        [(1, 5, "s allocated 5 bytes: {'h','e','l','l','o'}. No '\\0' appended.", None, None)]
    )

    # Q098: Mutating Char Array String
    add_q(
        98, "TOPIC_ARRAYS", "Easy", "Mutating Elements in Character Array",
        "What is the output of the following program?",
        """#include <stdio.h>
int main() {
    char word[] = "cat";
    word[0] = 'b';
    printf("%s\\n", word);
    return 0;
}""",
        5, "word[0] = 'b';", "word is a mutable stack array initialized with {'c','a','t','\\0'}. Modifying word[0] to 'b' produces \"bat\"!",
        [
            ("A", "bat", True, "word[0] is changed from 'c' to 'b'. Output is bat.", ""),
            ("B", "cat", False, "Thought strings cannot be mutated in C.", "Stack-allocated char arrays are fully mutable!"),
            ("C", "Segmentation Fault", False, "Confused char word[] with char *word = \"cat\".", "char word[] is on the stack, not read-only memory."),
            ("D", "Compile error", False, "Modifying char array element is valid C.", "Standard array assignment.")
        ],
        "char word[] allocates a mutable buffer on the stack. Changing word[0] yields 'b','a','t','\\0'.",
        "ISO/IEC 9899 §6.7.9",
        "Prints bat.",
        [(1, 5, "word[0] changed from 'c' to 'b'. word becomes 'bat'.", {"word": "bat"}, None)]
    )

    # Q099: Embedded Null Terminator in Char Array
    add_q(
        99, "TOPIC_ARRAYS", "Medium", "Embedded Null Terminator String Truncation",
        "What is printed by this printf statement?",
        """#include <stdio.h>
int main() {
    char str[] = "pro\\0gram";
    printf("%s\\n", str);
    return 0;
}""",
        4, "char str[] = \"pro\\0gram\";", "%s stops printing at the FIRST null terminator ('\\0')! It outputs \"pro\" and ignores the rest!",
        [
            ("A", "pro", True, "printf with %s stops output as soon as it hits the '\\0' character.", ""),
            ("B", "program", False, "Thought '\\0' was ignored or removed.", "Null terminator marks end of string in C."),
            ("C", "pro program", False, "Output terminates at '\\0'.", "Stops at '\\0'."),
            ("D", "Compile error", False, "Embedded null bytes in string literals are valid C.", "Standard escape sequence.")
        ],
        "%s writes characters from the array up to (but not including) the terminating null character.",
        "ISO/IEC 9899 §7.21.6.1",
        "Prints pro.",
        [(1, 4, "printf encounters '\\0' after 'o' and terminates output.", {"stdout": "pro"}, None)]
    )

    # Q100: Array Passed to Function Decays to Base Address
    add_q(
        100, "TOPIC_ARRAYS", "Medium", "Modifying Array Elements Inside Function",
        "What is the output of the following program?",
        """#include <stdio.h>
void double_first(int arr[]) {
    arr[0] *= 2;
}
int main() {
    int nums[3] = {5, 10, 15};
    double_first(nums);
    printf("%d\\n", nums[0]);
    return 0;
}""",
        4, "arr[0] *= 2;", "When an array is passed to a function, its BASE ADDRESS is passed! Modifications to arr[0] modify the original array in main (5 becomes 10)!",
        [
            ("A", "10", True, "Passing an array passes a reference to its first element. arr[0] *= 2 modifies nums[0] in main.", ""),
            ("B", "5", False, "Thought arrays were copied by value.", "Arrays in C cannot be passed by value; they decay to a pointer to their first element!"),
            ("C", "0", False, "nums[0] was 5, multiplied by 2 gives 10.", "Result is 10."),
            ("D", "Compile error", False, "Passing array to function is standard C.", "Valid C syntax.")
        ],
        "An array expression passed as an argument decays into a pointer to its first element. Changes to elements inside the function affect the original array.",
        "ISO/IEC 9899 §6.3.2.1#3",
        "Prints 10.",
        [(1, 4, "arr[0] (nums[0]) multiplied by 2 -> 10.", {"nums[0]": 10}, None),
         (2, 9, "printf prints 10.", {"stdout": "10"}, None)]
    )

print("syllabus_part3 loaded (32 questions, total 100).")
