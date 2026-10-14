# bank_part2.py: Q033 to Q058 (CAT_INT_PROM & CAT_STR_LIT)

def load_part2(add_q):
    # =========================================================================
    # CAT_INT_PROM (Q033 - Q046)
    # =========================================================================

    # Q033: Integer Division Truncation
    add_q(
        33, "CAT_INT_PROM", "Easy", "Integer Division Truncation",
        "What is the output of the following program?",
        """#include <stdio.h>
int main() {
    double res = 5 / 2;
    printf("%.1f\\n", res);
    return 0;
}""",
        4, "5 / 2", "Both 5 and 2 are integers, so integer division truncates to 2 BEFORE assignment to double res!",
        [
            ("A", "2.0", True, "5 / 2 evaluates to integer 2, which is then promoted to 2.0.", ""),
            ("B", "2.5", False, "Expected algebraic division.", "In C, dividing two integers truncates toward zero; 5/2 is integer 2."),
            ("C", "3.0", False, "Thought it rounded up.", "C integer division truncates (discards fractional part), never rounds."),
            ("D", "Compile error", False, "Thought double cannot hold integer division.", "Implicit promotion from int to double is valid.")
        ],
        "When both operands of / are integers, integer division is performed, truncating any fractional part toward zero.",
        "ISO/IEC 9899 §6.5.5#6",
        "5 / 2 produces integer 2. Storing 2 in double variable res yields 2.0.",
        [
            (1, 4, "Integer division: 5 / 2 evaluates to integer 2.", {"temp": 2}, None),
            (2, 4, "Promotion: integer 2 converted to double 2.0.", {"res": 2.0}, None),
            (3, 5, "printf prints 2.0.", {"stdout": "2.0"}, None)
        ]
    )

    # Q034: Cast After Division vs Before
    add_q(
        34, "CAT_INT_PROM", "Medium", "Cast Precedence: (double)(5 / 2)",
        "What is printed by this code?",
        """#include <stdio.h>
int main() {
    double a = (double)(5 / 2);
    double b = (double)5 / 2;
    printf("%.1f %.1f\\n", a, b);
    return 0;
}""",
        4, "(double)(5 / 2)", "Parentheses force 5 / 2 to truncate to 2 first! In (double)5 / 2, 5 becomes double 5.0 first, yielding 2.5!",
        [
            ("A", "2.0 2.5", True, "a truncates before the cast (2.0); b casts 5 to 5.0 before division (2.5).", ""),
            ("B", "2.5 2.5", False, "Thought the cast inside a converted the operands to double.", "The cast applies to the RESULT of the parenthesized expression (5/2)."),
            ("C", "2.0 2.0", False, "Thought b also truncated.", "In b, double / int promotes 2 to 2.0, giving 2.5."),
            ("D", "2.5 2.0", False, "Inverted the results.", "Check parenthesis grouping carefully.")
        ],
        "In (double)(5 / 2), the division 5 / 2 evaluates first to 2, then casts to 2.0. In (double)5 / 2, the cast has higher precedence than /, making 5.0 / 2 = 2.5.",
        "ISO/IEC 9899 §6.5.4 & §6.5.5",
        "Output is 2.0 2.5.",
        [
            (1, 4, "(5 / 2) truncates to 2. (double)2 yields 2.0.", {"a": 2.0}, None),
            (2, 5, "(double)5 yields 5.0. 5.0 / 2 yields 2.5.", {"b": 2.5}, None)
        ]
    )

    # Q035: Signed vs Unsigned Comparison Trap (-1 < 1U)
    add_q(
        35, "CAT_INT_PROM", "Nightmare", "Signed vs Unsigned Relational Promotion Trap",
        "What is the output of the following program on a 32-bit machine?",
        """#include <stdio.h>
int main() {
    int a = -1;
    unsigned int b = 1;
    if (a < b) {
        printf("LESS\\n");
    } else {
        printf("NOT LESS\\n");
    }
    return 0;
}""",
        6, "a < b", "Usual Arithmetic Conversions: a is converted to unsigned int, turning -1 into 4294967295 (UINT_MAX)!",
        [
            ("A", "NOT LESS", True, "-1 promoted to unsigned int is 4294967295, which is GREATER than 1!", ""),
            ("B", "LESS", False, "Mathematical intuition: -1 is less than 1.", "In C, comparing signed and unsigned integers promotes the signed operand to unsigned!"),
            ("C", "Compile error", False, "Thought comparing signed and unsigned is illegal.", "C permits mixed comparisons (generates -Wsign-compare warning)."),
            ("D", "Undefined Behavior", False, "Thought signed overflow occurred.", "Conversion to unsigned is strictly defined by modular arithmetic (wraps to 2^32 - 1).")
        ],
        "Usual arithmetic conversions specify that if an int and unsigned int are compared, the signed int is converted to unsigned int.",
        "ISO/IEC 9899 §6.3.1.8#1",
        "-1 converted to unsigned int on a 32-bit system is 0xFFFFFFFF (4,294,967,295). Since 4294967295 < 1 is false, it prints NOT LESS.",
        [
            (1, 6, "Usual Arithmetic Conversions: a (-1) converted to unsigned int (4294967295U).", {"(unsigned)a": 4294967295}, None),
            (2, 6, "4294967295U < 1U is FALSE.", {"condition": 0}, None),
            (3, 9, "else branch executes: prints NOT LESS.", {"stdout": "NOT LESS"}, None)
        ]
    )

    # Q036: Char Sign Extension (char c = 0x80)
    add_q(
        36, "CAT_INT_PROM", "Tricky", "Char Sign Extension during Comparison",
        "On systems where char is signed (8-bit), what is printed?",
        """#include <stdio.h>
int main() {
    char c = 0x80;
    if (c == 0x80) {
        printf("EQUAL\\n");
    } else {
        printf("NOT EQUAL\\n");
    }
    return 0;
}""",
        5, "c == 0x80", "c is signed, so 0x80 is sign-extended to int -128 (0xFFFFFF80), which does NOT equal integer 128 (0x00000080)!",
        [
            ("A", "NOT EQUAL", True, "c sign-extends to -128, while literal 0x80 is positive 128. They are not equal!", ""),
            ("B", "EQUAL", False, "Assumed c retains 0x80 and matches literal 0x80.", "Operands of == undergo integer promotion. Signed char promotes with sign bit extension."),
            ("C", "Compile error", False, "Thought hex literal is invalid for char.", "0x80 is a valid int literal."),
            ("D", "Undefined Behavior", False, "Thought sign extension is undefined.", "Sign representation on two's complement is standard.")
        ],
        "Integer promotion promotes char c to int. Because 0x80 has the MSB set, signed char promotes to negative int -128 (0xFFFFFF80). The literal 0x80 is positive int 128 (0x00000080).",
        "ISO/IEC 9899 §6.3.1.1#2",
        "-128 != 128, so the equality check fails and NOT EQUAL is printed.",
        [
            (1, 4, "c = 0x80 (stored as -128 in signed 8-bit).", {"c": -128}, None),
            (2, 5, "c promoted to int: -128. Compared with literal 128. -128 == 128 is FALSE.", {"c_promoted": -128, "literal": 128}, None),
            (3, 8, "Prints NOT EQUAL.", {"stdout": "NOT EQUAL"}, None)
        ]
    )

    # Q037: Float Literal Equality (0.1f == 0.1)
    add_q(
        37, "CAT_INT_PROM", "Tricky", "Float vs Double Literal Precision Mismatch",
        "What is the output of the following program?",
        """#include <stdio.h>
int main() {
    float f = 0.1f;
    if (f == 0.1) {
        printf("EQUAL\\n");
    } else {
        printf("NOT EQUAL\\n");
    }
    return 0;
}""",
        5, "f == 0.1", "Literal 0.1 without suffix is of type DOUBLE! Because 0.1 has no exact binary representation, float and double roundings differ!",
        [
            ("A", "NOT EQUAL", True, "0.1f (float) and 0.1 (double) have different binary precision roundings, so f == 0.1 evaluates to FALSE.", ""),
            ("B", "EQUAL", False, "Thought 0.1 and 0.1f represent the same mathematical decimal number.", "Floating-point numbers are base-2 binary fractions; 0.1 is an infinite repeating binary fraction."),
            ("C", "Compile error", False, "Thought comparing float and double is a type error.", "float promotes to double for the comparison, but precision bits differ."),
            ("D", "Undefined Behavior", False, "Thought floating point comparisons are undefined.", "Floating point comparisons are strictly defined by IEEE 754.")
        ],
        "In C, floating constants without a suffix are double. 0.1 cannot be represented exactly in binary floating point. When float f (24 bits precision) is promoted to double, its trailing bits do not match 0.1 (53 bits precision).",
        "ISO/IEC 9899 §6.4.4.2 & §6.3.1.8",
        "Because 0.10000000149011612... != 0.10000000000000000..., it prints NOT EQUAL.",
        [
            (1, 4, "f stored with 24-bit precision (0.10000000149...).", None, None),
            (2, 5, "0.1 literal has 53-bit precision. Promoted f != 0.1.", None, None),
            (3, 8, "Prints NOT EQUAL.", {"stdout": "NOT EQUAL"}, None)
        ]
    )

    # Q038: Unsigned Integer Underflow Wrap
    add_q(
        38, "CAT_INT_PROM", "Medium", "Unsigned Integer Underflow Guarantee",
        "What is the output of the following program?",
        """#include <stdio.h>
int main() {
    unsigned int x = 0;
    x--;
    if (x > 0) {
        printf("WRAP_AROUND\\n");
    } else {
        printf("ZERO_OR_LESS\\n");
    }
    return 0;
}""",
        5, "x--", "Unsigned integer arithmetic NEVER overflows or underflows in C: it wraps modulo 2^N, yielding UINT_MAX!",
        [
            ("A", "WRAP_AROUND", True, "0 - 1 on unsigned int wraps around to UINT_MAX (4,294,967,295), which is > 0.", ""),
            ("B", "ZERO_OR_LESS", False, "Thought x became -1.", "Unsigned types cannot represent negative numbers; 0 - 1 wraps to the maximum unsigned value."),
            ("C", "Undefined Behavior", False, "Confused unsigned wrap with signed overflow.", "Signed overflow is UB, but unsigned modular wrap is guaranteed by the C standard!"),
            ("D", "Runtime crash", False, "Thought an exception was thrown.", "C does not throw hardware exceptions on integer wrap.")
        ],
        "A computation involving unsigned operands can never produce an overflow; the result is reduced modulo 2^N.",
        "ISO/IEC 9899 §6.2.5#9",
        "0 - 1 produces UINT_MAX (4294967295), so x > 0 evaluates to true.",
        [
            (1, 5, "x (0) decremented: wraps modulo 2^32 to 4294967295.", {"x": 4294967295}, None),
            (2, 6, "4294967295 > 0 is TRUE.", {"condition": 1}, None),
            (3, 7, "Prints WRAP_AROUND.", {"stdout": "WRAP_AROUND"}, None)
        ]
    )

    # Q039: Octal Literal Trap (012)
    add_q(
        39, "CAT_INT_PROM", "Tricky", "Leading Zero Octal Literal Trap",
        "What is the output of the following program?",
        """#include <stdio.h>
int main() {
    int a = 012;
    int b = 10;
    printf("%d %d\\n", a, a + b);
    return 0;
}""",
        4, "int a = 012;", "A leading zero in an integer literal means OCTAL (base 8)! 012 in octal is (1*8 + 2) = 10 decimal!",
        [
            ("A", "10 20", True, "012 is octal for 10. 10 + 10 = 20.", ""),
            ("B", "12 22", False, "Treated 012 as decimal 12.", "In C, integer literals starting with '0' are parsed in octal (base 8)."),
            ("C", "Compile error", False, "Thought leading zero is a syntax error.", "Leading zeros are valid syntax for octal numbers."),
            ("D", "0 10", False, "Thought leading zero resets the number.", "012 is a single numeric token.")
        ],
        "An integer constant beginning with 0 is an octal constant. Digits represent powers of 8.",
        "ISO/IEC 9899 §6.4.4.1",
        "012 base 8 = 1 * 8^1 + 2 * 8^0 = 10 base 10. a + b = 10 + 10 = 20.",
        [
            (1, 4, "012 parsed as octal: 1*8 + 2 = 10 decimal.", {"a": 10}, None),
            (2, 6, "printf prints 10 and 10 + 10 = 20.", {"stdout": "10 20"}, None)
        ]
    )

    # Q040: Modulo with Negative Numbers (-7 % 3)
    add_q(
        40, "CAT_INT_PROM", "Tricky", "Modulo with Negative Operands (C99 Standard)",
        "What is the output of the following program under C99 / C11?",
        """#include <stdio.h>
int main() {
    int a = -7 % 3;
    int b = 7 % -3;
    printf("%d %d\\n", a, b);
    return 0;
}""",
        4, "-7 % 3", "In C99, integer division truncates toward zero, and (a/b)*b + a%b == a. Therefore, the sign of a%b ALWAYS matches the sign of the dividend (a)!",
        [
            ("A", "-1 1", True, "In C99+, sign of modulo result strictly matches the left operand (dividend): -7 % 3 = -1, and 7 % -3 = 1.", ""),
            ("B", "2 1", False, "Confused C modulo with Python modulo (which uses floor division).", "Python gives 2, but C uses truncation toward zero, giving -1."),
            ("C", "-1 -1", False, "Thought modulo is always negative with negative operands.", "Sign depends strictly on the left operand."),
            ("D", "1 1", False, "Thought modulo result is always positive.", "In C, negative dividend yields negative remainder.")
        ],
        "C99 §6.5.5#6 specifies that integer division truncates toward zero: -7 / 3 = -2. Since (a/b)*b + a%b = a, (-2)*3 + a%b = -7 => a%b = -1.",
        "ISO/IEC 9899:1999 §6.5.5#6",
        "-7 % 3 is -1. 7 % -3 is 1.",
        [
            (1, 4, "-7 / 3 = -2. Remainder = -7 - (-2 * 3) = -1.", {"a": -1}, None),
            (2, 5, "7 / -3 = -2. Remainder = 7 - (-2 * -3) = 1.", {"b": 1}, None),
            (3, 6, "printf prints -1 1.", {"stdout": "-1 1"}, None)
        ]
    )

    # Q041: Integer Promotion in Arithmetic Expressions
    add_q(
        41, "CAT_INT_PROM", "Medium", "Integer Promotion of Sub-int Types",
        "What is sizeof(c1 + c2) when c1 and c2 are char variables?",
        """#include <stdio.h>
int main() {
    char c1 = 'a', c2 = 'b';
    printf("%zu\\n", sizeof(c1 + c2));
    return 0;
}""",
        5, "sizeof(c1 + c2)", "In arithmetic expressions (+), types smaller than int undergo Integer Promotion to INT! sizeof(c1 + c2) is sizeof(int) (4 bytes)!",
        [
            ("A", "4", True, "c1 and c2 are promoted to int before addition. sizeof(int) is 4 on typical systems.", ""),
            ("B", "1", False, "Thought the addition of two chars produces a char.", "Sub-int types (char, short) are automatically promoted to int in expressions."),
            ("C", "2", False, "Thought it summed 1 + 1 byte.", "sizeof returns type size, not sum of operand sizes."),
            ("D", "Compile error", False, "Thought adding chars is invalid.", "Chars are arithmetic integer types.")
        ],
        "The integer promotions specify that types with conversion rank less than int are converted to int or unsigned int.",
        "ISO/IEC 9899 §6.3.1.1#2",
        "The type of (c1 + c2) is int, so sizeof(c1 + c2) returns 4.",
        [
            (1, 5, "c1 and c2 promoted to int. Result has type int. sizeof(int) = 4.", {"sizeof": 4}, None)
        ]
    )

    # Q042: Format Specifier Mismatch (%d with float)
    add_q(
        42, "CAT_INT_PROM", "Tricky", "Format Specifier Mismatch (%d on float)",
        "What happens when passing a float to printf with %d?",
        """#include <stdio.h>
int main() {
    float f = 5.0f;
    printf("%d\\n", f);
    return 0;
}""",
        5, "printf(\"%d\\n\", f);", "Passing a float to %d is UNDEFINED BEHAVIOR! printf expects an int and reads float bits/registers as an integer!",
        [
            ("A", "Undefined Behavior (Prints garbage value or unexpected number)", True, "Variadic arguments undergo default argument promotions (float -> double). %d expects int, causing format specifier mismatch UB.", ""),
            ("B", "Prints 5", False, "Thought printf automatically converts float 5.0 to integer 5.", "printf does not inspect types; it blindly reads raw stack/register bits according to the format string."),
            ("C", "Compile error", False, "Thought format mismatch stops compilation.", "Standard C compilers emit a warning, not an error."),
            ("D", "Prints 5.0", False, "Thought %d formats floats.", "%d is strictly for decimal integer.")
        ],
        "If a conversion specification is invalid or an argument is not of the expected type, the behavior is undefined.",
        "ISO/IEC 9899 §7.21.6.1#9",
        "In x86-64 ABI, float arguments are passed in XMM registers while %d reads from integer register (ESI), reading garbage.",
        [
            (1, 5, "Format specifier mismatch: %d on floating argument -> UB.", None, None)
        ]
    )

    # Q043: Division by Zero
    add_q(
        43, "CAT_INT_PROM", "Easy", "Integer Division by Zero",
        "What happens at runtime when executing integer division by zero?",
        """#include <stdio.h>
int main() {
    int a = 10, b = 0;
    int c = a / b;
    printf("%d\\n", c);
    return 0;
}""",
        5, "a / b", "Dividing by zero in C is Undefined Behavior and triggers a hardware floating-point exception (SIGFPE) / crash on modern CPUs!",
        [
            ("A", "Runtime Crash (Floating Point Exception / SIGFPE)", True, "Integer division by zero causes CPU hardware fault.", ""),
            ("B", "Prints Infinity", False, "Confused integer division with IEEE floating point division.", "Only floating point division by zero yields Infinity; integer division faults."),
            ("C", "Prints 0", False, "Thought division by zero yields 0.", "Hardware registers trap on zero divisor."),
            ("D", "Compilation Error", False, "Thought compiler catches division by variable.", "Compiler cannot know runtime value of b without optimization.")
        ],
        "The result of the / operator is the quotient. If the value of the second operand is zero, the behavior is undefined.",
        "ISO/IEC 9899 §6.5.5#5",
        "The OS sends SIGFPE (or STATUS_INTEGER_DIVIDE_BY_ZERO on Windows), killing the process.",
        [
            (1, 5, "CPU encounters IDIV with divisor 0 -> Hardware trap SIGFPE.", None, None)
        ]
    )

    # Q044: Hexadecimal Representation and Bitwise NOT
    add_q(
        44, "CAT_INT_PROM", "Medium", "Bitwise NOT with Integer Promotion",
        "What is the output of the following program?",
        """#include <stdio.h>
int main() {
    unsigned char a = 0;
    printf("%d\\n", ~a == 255);
    return 0;
}""",
        5, "~a == 255", "Because of integer promotion, ~a promotes a to int 0, then ~0 produces int -1 (0xFFFFFFFF), which does NOT equal 255!",
        [
            ("A", "0", True, "~a promotes to int -1 (0xFFFFFFFF). -1 == 255 is false (0).", ""),
            ("B", "1", False, "Assumed ~a remained unsigned char with value 0xFF (255).", "~ promotes its operand to int first; the result is of type int."),
            ("C", "255", False, "Thought printf printed the value of ~a.", "The expression tested is (~a == 255), which yields 0 or 1."),
            ("D", "Compile error", False, "Thought ~ cannot be applied to unsigned char.", "Valid syntax.")
        ],
        "The operand of ~ undergoes integer promotion to int. ~0 in two's complement is -1. -1 == 255 evaluates to 0 (false).",
        "ISO/IEC 9899 §6.5.3.3",
        "To get 255, one must cast: (unsigned char)~a.",
        [
            (1, 5, "a promoted to int 0. ~0 = -1 (0xFFFFFFFF).", {"~a": -1}, None),
            (2, 5, "-1 == 255 is 0 (false).", {"res": 0}, None),
            (3, 5, "printf prints 0.", {"stdout": "0"}, None)
        ]
    )

    # Q045: Char Arithmetic Overflow
    add_q(
        45, "CAT_INT_PROM", "Medium", "Signed Char Overflow Wrap",
        "On a platform where char is 8-bit signed (-128 to 127), what is printed by this code?",
        """#include <stdio.h>
int main() {
    signed char c = 127;
    c++;
    printf("%d\\n", c);
    return 0;
}""",
        5, "c++", "Signed integer overflow is technically Undefined Behavior, but on two's complement it wraps to -128!",
        [
            ("A", "-128", True, "In 8-bit two's complement, binary 01111111 (127) + 1 becomes 10000000 (-128).", ""),
            ("B", "128", False, "Thought signed char can hold 128.", "8-bit signed char maximum value is 127."),
            ("C", "0", False, "Thought it reset to zero.", "Two's complement wraps from max positive to min negative."),
            ("D", "127", False, "Thought it saturated.", "C does not have saturating arithmetic.")
        ],
        "127 in binary is 01111111. Adding 1 yields 10000000, which in two's complement signed representation is -128.",
        "ISO/IEC 9899 §6.2.6.2",
        "When passed to printf, -128 is printed as a signed decimal integer.",
        [
            (1, 5, "127 + 1 = binary 10000000 = -128.", {"c": -128}, None),
            (2, 6, "printf prints -128.", {"stdout": "-128"}, None)
        ]
    )

    # Q046: Comma Operator in While Loop Condition
    add_q(
        46, "CAT_INT_PROM", "Tricky", "Comma Operator in Loop Termination Condition",
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
        5, "while (i < 2, j < 4)", "The comma operator discards i < 2! The loop condition depends EXCLUSIVELY on j < 4!",
        [
            ("A", "4 4", True, "i < 2 is evaluated and discarded. Only j < 4 controls loop termination, running 4 times.", ""),
            ("B", "2 2", False, "Assumed the comma acted like logical AND (&&).", "Comma operator discards the left operand and only uses the right operand!"),
            ("C", "2 4", False, "Thought i stopped incrementing while j continued.", "Both increment statements inside the loop body run together."),
            ("D", "Infinite loop", False, "Thought condition is invalid.", "Valid loop condition.")
        ],
        "In a comma expression (E1, E2), E1 is evaluated and its result is discarded. E2 controls the while condition.",
        "ISO/IEC 9899 §6.5.17",
        "j iterates from 0, 1, 2, 3 (4 times) until j = 4, exiting with i = 4, j = 4.",
        [
            (1, 5, "Loop checks j < 4 (i < 2 is discarded). Runs for j = 0, 1, 2, 3.", {"i": 4, "j": 4}, None),
            (2, 9, "printf prints 4 4.", {"stdout": "4 4"}, None)
        ]
    )

    # =========================================================================
    # CAT_STR_LIT (Q047 - Q058)
    # =========================================================================

    # Q047: Modifying String Literal (Read-Only Memory)
    add_q(
        47, "CAT_STR_LIT", "Medium", "String Literal Immutability (.rodata Crash)",
        "What happens when compiling and running this code?",
        """#include <stdio.h>
int main() {
    char *s = "hello";
    s[0] = 'H';
    printf("%s\\n", s);
    return 0;
}""",
        5, "s[0] = 'H';", "String literal \"hello\" is stored in read-only memory (.rodata)! Modifying it causes a Segmentation Fault!",
        [
            ("A", "Runtime Crash (Segmentation Fault)", True, "Modifying string literal memory triggers a memory protection violation.", ""),
            ("B", "Prints Hello", False, "Assumed char *s behaves like a mutable array char s[].", "char *s points to .rodata (read-only). To modify, declare char s[] = \"hello\";"),
            ("C", "Compilation Error", False, "Thought compiler requires const char *.", "In C (unlike C++), string literals have type char[] for backward compatibility, so it compiles."),
            ("D", "Prints hello", False, "Thought the write failed silently.", "MMU raises a hardware fault on write to read-only page.")
        ],
        "String literals have static storage duration and may be placed in read-only memory. Attempting to modify a string literal results in Undefined Behavior (typically SIGSEGV).",
        "ISO/IEC 9899 §6.4.5#7",
        "The OS terminates the program.",
        [
            (1, 4, "s points to read-only string literal in .rodata.", {"s": "0x00405000"}, None),
            (2, 5, "Attempt to write 'H' triggers SIGSEGV.", None, None)
        ]
    )

    # Q048: Mutable Stack Array String
    add_q(
        48, "CAT_STR_LIT", "Easy", "Mutable Stack Array String",
        "What is the output of the following program?",
        """#include <stdio.h>
int main() {
    char s[] = "hello";
    s[0] = 'H';
    printf("%s\\n", s);
    return 0;
}""",
        5, "s[0] = 'H';", "s is a stack-allocated array initialized with a copy of \"hello\"! It is fully mutable, outputting Hello!",
        [
            ("A", "Hello", True, "char s[] copies the characters to the local stack frame, where modifications are safe.", ""),
            ("B", "Segmentation Fault", False, "Confused char s[] with char *s.", "char s[] is an array on the stack, not a pointer to .rodata."),
            ("C", "hello", False, "Thought array was read-only.", "Stack arrays are fully mutable."),
            ("D", "Compile error", False, "Thought string assignment to array is invalid.", "Initializing char s[] with a string literal is standard C.")
        ],
        "char s[] = \"hello\"; allocates 6 bytes on the stack and copies 'h','e','l','l','o','\\0' into it. Modifying elements is valid and safe.",
        "ISO/IEC 9899 §6.7.9#14",
        "s[0] is changed to 'H', and printf prints Hello.",
        [
            (1, 4, "Array s allocated on stack: {'h','e','l','l','o','\\0'}.", None, None),
            (2, 5, "s[0] changed to 'H'.", {"s[0]": "H"}, None),
            (3, 6, "printf prints Hello.", {"stdout": "Hello"}, None)
        ]
    )

    # Q049: Missing Null Terminator (char s[5] = "hello")
    add_q(
        49, "CAT_STR_LIT", "Tricky", "Missing Null Terminator in Sized Array",
        "What is the consequence of declaring char s[5] = \"hello\"; ?",
        """#include <stdio.h>
#include <string.h>
int main() {
    char s[5] = "hello";
    printf("%zu\\n", strlen(s));
    return 0;
}""",
        5, "char s[5] = \"hello\";", "In C, this is valid syntax, but NO SPACE remains for '\\0'! strlen(s) will read past array bounds until it randomly finds a 0 byte!",
        [
            ("A", "Undefined Behavior (Buffer overread searching for '\\0')", True, "s contains 5 chars without '\\0'. strlen walks past the end of the array.", ""),
            ("B", "Prints 5", False, "Thought strlen stops at the array boundary.", "strlen does not know array sizes; it scans memory until it hits a zero byte ('\\0')."),
            ("C", "Compilation Error: string too long", False, "Thought the compiler rejects omitting '\\0'.", "ISO C §6.7.9#14 explicitly permits omitting '\\0' if the array size exactly equals string length!"),
            ("D", "Prints 4", False, "Thought it truncated the last character.", "All 5 characters 'h','e','l','l','o' are copied.")
        ],
        "An array of character type may be initialized by a string literal. If the array has fixed size, the trailing null character is discarded if size equals length.",
        "ISO/IEC 9899 §6.7.9#14",
        "Without '\\0', calling strlen or %s causes an out-of-bounds read (Undefined Behavior).",
        [
            (1, 5, "s allocated with 5 bytes: {'h','e','l','l','o'}. No '\\0' appended.", None, None),
            (2, 6, "strlen scans past s[4] into adjacent stack garbage searching for 0.", None, None)
        ]
    )

    # Q050: sizeof vs strlen on String
    add_q(
        50, "CAT_STR_LIT", "Easy", "Difference between sizeof and strlen",
        "What is printed by this program?",
        """#include <stdio.h>
#include <string.h>
int main() {
    char s[] = "world";
    printf("%zu %zu\\n", sizeof(s), strlen(s));
    return 0;
}""",
        6, "sizeof(s), strlen(s)", "sizeof counts the allocated bytes INCLUDING '\\0' (6). strlen counts visible characters EXCLUDING '\\0' (5)!",
        [
            ("A", "6 5", True, "sizeof counts the null byte '\\0' (6 bytes). strlen counts characters before '\\0' (5).", ""),
            ("B", "5 5", False, "Forgot that string literals include the terminating '\\0'.", "sizeof(s) includes the hidden null terminator."),
            ("C", "5 6", False, "Inverted sizeof and strlen.", "sizeof is always greater than or equal to strlen for null-terminated arrays."),
            ("D", "8 5", False, "Confused array with pointer size.", "s is an array, not a pointer variable.")
        ],
        "sizeof evaluates the total memory footprint of the array object (5 letters + 1 null terminator = 6 bytes). strlen computes string length up to the first null character.",
        "ISO/IEC 9899 §6.5.3.4 & §7.24.6.3",
        "Output is 6 5.",
        [
            (1, 5, "s allocated as 6 bytes on stack: 'w','o','r','l','d','\\0'.", None, None),
            (2, 6, "sizeof(s) = 6. strlen(s) = 5.", {"sizeof": 6, "strlen": 5}, None)
        ]
    )

    # Q051: sizeof on Pointer to String
    add_q(
        51, "CAT_STR_LIT", "Medium", "sizeof on Pointer to String vs Array",
        "On a 64-bit architecture, what is printed by this program?",
        """#include <stdio.h>
int main() {
    char *p = "supercalifragilistic";
    printf("%zu\\n", sizeof(p));
    return 0;
}""",
        5, "sizeof(p)", "p is a POINTER variable! sizeof(p) returns the pointer size (8 bytes on 64-bit), NOT the string length!",
        [
            ("A", "8", True, "p is of type char*, so sizeof(p) is 8 bytes on a 64-bit platform.", ""),
            ("B", "21", False, "Counted the characters in the string literal plus null terminator.", "sizeof(p) inspects the pointer variable itself, not the memory it points to!"),
            ("C", "20", False, "Counted the string length without null terminator.", "Use strlen(p) to measure string length."),
            ("D", "1", False, "Thought it returned sizeof(char).", "p is a pointer, not a char.")
        ],
        "sizeof applied to a pointer yields the size of the pointer itself (8 bytes on 64-bit systems), regardless of the size of the data it points to.",
        "ISO/IEC 9899 §6.5.3.4",
        "To get string length from a pointer, call strlen(p).",
        [
            (1, 5, "p is char*. On 64-bit arch, sizeof(char*) = 8.", {"sizeof(p)": 8}, None)
        ]
    )

    # Q052: strncpy Non-Termination Trap
    add_q(
        52, "CAT_STR_LIT", "Tricky", "strncpy Lack of Null-Termination",
        "What is the output of the following program?",
        """#include <stdio.h>
#include <string.h>
int main() {
    char dest[6] = "XXXXX";
    strncpy(dest, "abc", 2);
    printf("%s\\n", dest);
    return 0;
}""",
        6, "strncpy(dest, \"abc\", 2);", "strncpy copies exactly 2 bytes ('a', 'b') without adding a null terminator! The rest of dest remains 'XXX'!",
        [
            ("A", "abXXX", True, "strncpy wrote 'a' and 'b' into indices 0 and 1, leaving indices 2, 3, 4 as 'X' and index 5 as '\\0'.", ""),
            ("B", "ab", False, "Assumed strncpy always appends a null terminator.", "If src length >= n, strncpy does NOT append a '\\0'!"),
            ("C", "abc", False, "Thought n=2 was ignored and whole string was copied.", "strncpy stops after copying n=2 characters."),
            ("D", "Segmentation Fault", False, "Thought memory was corrupted.", "dest[5] was initialized with '\\0', keeping the string safely terminated.")
        ],
        "strncpy copies no more than n characters. If there is no null character among the first n characters of src, dest will not be null-terminated.",
        "ISO/IEC 9899 §7.24.2.4",
        "dest initially: 'X','X','X','X','X','\\0'. After copying 2 chars: 'a','b','X','X','X','\\0'. Prints abXXX.",
        [
            (1, 5, "dest initialized to: {'X','X','X','X','X','\\0'}.", None, None),
            (2, 6, "strncpy writes 'a','b' into dest[0] and dest[1]. Does not touch remaining bytes.", None, None),
            (3, 7, "printf prints abXXX.", {"stdout": "abXXX"}, None)
        ]
    )

    # Q053: String Comparison with == Operator
    add_q(
        53, "CAT_STR_LIT", "Easy", "String Comparison with == vs strcmp",
        "What is the output of the following program?",
        """#include <stdio.h>
int main() {
    char s1[] = "apple";
    char s2[] = "apple";
    if (s1 == s2) {
        printf("SAME\\n");
    } else {
        printf("DIFFERENT\\n");
    }
    return 0;
}""",
        6, "s1 == s2", "In C, == compares MEMORY ADDRESSES, not string contents! s1 and s2 are distinct stack arrays with different addresses!",
        [
            ("A", "DIFFERENT", True, "s1 and s2 have distinct stack addresses (&s1 != &s2). Use strcmp(s1, s2) == 0 to compare contents.", ""),
            ("B", "SAME", False, "Assumed == compares character contents like in high-level languages (Python).", "In C, arrays decay to pointers, so == compares pointer values."),
            ("C", "Compile error", False, "Thought comparing array names is illegal.", "Array names decay to pointers, so comparing them is syntactically valid."),
            ("D", "Undefined Behavior", False, "Thought pointer comparison is undefined.", "Comparing pointers for equality (==) is always well-defined.")
        ],
        "s1 and s2 decay into pointers to their respective base elements. Since they are distinct stack arrays, their addresses are different, so s1 == s2 is 0.",
        "ISO/IEC 9899 §6.5.9",
        "Prints DIFFERENT.",
        [
            (1, 6, "s1 decays to 0x1000; s2 decays to 0x1020. 0x1000 == 0x1020 is FALSE.", None, None),
            (2, 9, "Prints DIFFERENT.", {"stdout": "DIFFERENT"}, None)
        ]
    )

    # Q054: String Subscripting ("hello"[1])
    add_q(
        54, "CAT_STR_LIT", "Medium", "Subscripting String Literal Directly",
        "What is the output of the following program?",
        """#include <stdio.h>
int main() {
    printf("%c\\n", "hello"[1]);
    return 0;
}""",
        4, "\"hello\"[1]", "A string literal is a character array! \"hello\"[1] evaluates to *(\"hello\" + 1), which is 'e'!",
        [
            ("A", "e", True, "Index 1 of \"hello\" is the character 'e'.", ""),
            ("B", "h", False, "Thought index 1 is the first character.", "Arrays are 0-indexed: index 0 is 'h', index 1 is 'e'."),
            ("C", "Compile error", False, "Thought indexing string literals directly is invalid syntax.", "String literals are array objects and can be indexed directly."),
            ("D", "Segmentation fault", False, "Thought accessing string literal crashes.", "Reading from string literals is completely safe.")
        ],
        "A string literal evaluates to a pointer to its first character. Applying the subscript operator [1] offsets the pointer by 1 char and dereferences it.",
        "ISO/IEC 9899 §6.5.2.1",
        "Yields 'e'.",
        [
            (1, 4, "\"hello\" decays to char*. Index [1] accesses character 'e'.", {"val": "e"}, None),
            (2, 4, "printf prints e.", {"stdout": "e"}, None)
        ]
    )

    # Q055: String Slicing via Pointer Addition
    add_q(
        55, "CAT_STR_LIT", "Easy", "String Pointer Offset Slicing",
        "What is the output of the following program?",
        """#include <stdio.h>
int main() {
    char *s = "examination";
    printf("%s\\n", s + 4);
    return 0;
}""",
        5, "s + 4", "s + 4 advances the pointer by 4 characters, starting the string from 'i' (\"ination\")!",
        [
            ("A", "ination", True, "Offsetting the pointer by 4 bytes advances past 'e','x','a','m'.", ""),
            ("B", "minaton", False, "Off-by-one error counting characters.", "'e'(0), 'x'(1), 'a'(2), 'm'(3), 'i'(4)."),
            ("C", "exam", False, "Thought s + 4 truncated to first 4 characters.", "Pointer addition moves the start pointer forward."),
            ("D", "i", False, "Confused %s with %c.", "%s prints all characters from the pointer until '\\0'.")
        ],
        "s + 4 points to s[4] ('i'). printf with %s prints from that address up to the terminating null byte, outputting 'ination'.",
        "ISO/IEC 9899 §7.21.6.1",
        "Output is ination.",
        [
            (1, 5, "s + 4 points to 'i'. %s prints from 'i' to null byte.", {"stdout": "ination"}, None)
        ]
    )

    # Q056: Character Constant Type in C (sizeof('a'))
    add_q(
        56, "CAT_STR_LIT", "Tricky", "Character Constant Type in C vs C++",
        "On a standard 32-bit/64-bit C compiler, what is sizeof('a')?",
        """#include <stdio.h>
int main() {
    printf("%zu\\n", sizeof('a'));
    return 0;
}""",
        4, "sizeof('a')", "In C (unlike C++), character constants like 'a' have type INT! Therefore, sizeof('a') == sizeof(int) == 4!",
        [
            ("A", "4", True, "In ISO C, 'a' is an integer character constant with type int, whose size is 4 bytes.", ""),
            ("B", "1", False, "Confused C with C++. In C++, 'a' is type char (1 byte); in C, it is type int (4 bytes)!", "In C, §6.4.4.4#10 explicitly defines character constants as type int."),
            ("C", "2", False, "Confused with UTF-16 wchar_t.", "'a' is an ASCII char constant."),
            ("D", "Compile error", False, "Thought sizeof on literals is invalid.", "sizeof on any expression is valid.")
        ],
        "An integer character constant has type int. Accordingly, sizeof('a') equals sizeof(int), typically 4 bytes.",
        "ISO/IEC 9899 §6.4.4.4#10",
        "This is one of the classic differences between C and C++.",
        [
            (1, 4, "'a' has type int. sizeof(int) = 4.", {"sizeof": 4}, None)
        ]
    )

    # Q057: Null Terminator Embedded in Middle of String
    add_q(
        57, "CAT_STR_LIT", "Medium", "Embedded Null Terminator in String Literal",
        "What is printed by this program?",
        """#include <stdio.h>
#include <string.h>
int main() {
    char s[] = "abc\\0def";
    printf("%zu %zu\\n", strlen(s), sizeof(s));
    return 0;
}""",
        6, "strlen(s), sizeof(s)", "strlen stops at the first '\\0' (3). sizeof counts ALL allocated bytes including both null terminators (8 bytes)!",
        [
            ("A", "3 8", True, "strlen stops at the first '\\0' (length 3). sizeof includes 'a','b','c','\\0','d','e','f','\\0' (8 bytes).", ""),
            ("B", "6 8", False, "Thought strlen skipped the embedded '\\0'.", "strlen stops unconditionally at the first null byte encountered."),
            ("C", "3 7", False, "Forgot the trailing automatic '\\0'.", "String literals always append an implicit '\\0' at the end."),
            ("D", "7 8", False, "Counted visible letters.", "strlen is 3.")
        ],
        "strlen scans characters until the first '\\0', finding 3 ('a','b','c'). The array contains 8 bytes total: 'a','b','c','\\0','d','e','f','\\0'.",
        "ISO/IEC 9899 §7.24.6.3 & §6.4.5",
        "Output is 3 8.",
        [
            (1, 5, "s initialized with 8 bytes: 'a','b','c','\\0','d','e','f','\\0'.", None, None),
            (2, 6, "strlen finds '\\0' after 'c' -> 3. sizeof = 8.", {"strlen": 3, "sizeof": 8}, None)
        ]
    )

    # Q058: Character Pointer Reassignment vs Array Mutation
    add_q(
        58, "CAT_STR_LIT", "Medium", "Reassigning Array Name vs Reassigning Pointer",
        "What happens when compiling this code?",
        """#include <stdio.h>
int main() {
    char str[] = "hello";
    str = "world";
    printf("%s\\n", str);
    return 0;
}""",
        5, "str = \"world\";", "An array name is NOT an lvalue! You CANNOT reassign an array name like str = ...! This is a COMPILATION ERROR!",
        [
            ("A", "Compilation Error: assignment to expression with array type", True, "Array identifiers cannot be used as the left-hand operand of an assignment.", ""),
            ("B", "Prints world", False, "Assumed str is a pointer variable.", "str is an array, not a pointer variable. You must use strcpy(str, \"world\");."),
            ("C", "Prints hello", False, "Thought assignment failed silently.", "The compiler strictly forbids assigning to an array."),
            ("D", "Runtime crash", False, "Thought it crashes at runtime.", "Fails during compilation.")
        ],
        "An array name designates an object, but it is not a modifiable lvalue. An array cannot be the target of an assignment operator.",
        "ISO/IEC 9899 §6.5.16#2",
        "The compiler emits: error: assignment to expression with array type.",
        [
            (1, 5, "Compiler error: array type 'char [6]' is not assignable.", None, None)
        ]
    )

print("bank_part2 loaded (26 questions, total 58).")
