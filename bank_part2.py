# bank_part2.py: Q033 to Q058 (CAT_INT_PROM & CAT_STR_LIT)
# High-Yield C Midterm Exam Question Bank - Part 2
# Thoroughly upgraded with ISO C99/C11 compliance, balanced answer keys (A/B/C/D),
# granular execution traces, visual stack/pointer memory snapshots, and deep pedagogical rationales.

def load_part2(add_q):
    # =========================================================================
    # CAT_INT_PROM (Q033 - Q046): Integer Promotion, Conversion & Arithmetic
    # =========================================================================

    # Q033: Integer Division Truncation -> Key A
    add_q(
        33, 'CAT_INT_PROM', 'Easy', 'Integer Division Truncation',
        'What is the output of the following program?',
        r"""#include <stdio.h>
int main() {
    double res = 5 / 2;
    printf("%.1f\n", res);
    return 0;
}""",
        4, '5 / 2', 'Both 5 and 2 are integer literals, so integer division truncates to 2 BEFORE assignment to double res!',
        [
            ('A', '2.0', True, 'Integer division 5 / 2 truncates toward zero to yield integer 2; assigning 2 to double res implicitly promotes it to 2.0.', ''),
            ('B', '2.5', False, 'Expected algebraic real-number division.', 'In C, when both operands of / are integers, integer division is performed and the fractional part is truncated toward zero prior to assignment.'),
            ('C', '3.0', False, 'Assumed standard mathematical rounding up.', 'C integer division truncates strictly toward zero; it never rounds to the nearest integer.'),
            ('D', 'Compile error', False, 'Believed assigning an integer division result to a double variable is illegal.', 'Implicit conversion from int to double upon assignment is standard C.')
        ],
        'When both operands of / are integers, integer division is performed, truncating any fractional part toward zero.',
        'ISO/IEC 9899:1999 §6.5.5#6 & §6.3.1.8',
        'Under ISO C §6.5.5 paragraph 6, the result of the / operator is the quotient. When both operands are integers, the result is also an integer; if the quotient cannot be represented exactly, the fractional part is truncated toward zero (e.g. 5 / 2 = 2).\n\nEvaluation Order & Type Promotion:\n1. The binary operator / has operands 5 and 2, both of type int. No floating-point promotion occurs on the operands.\n2. 5 / 2 evaluates to the integer temporary 2.\n3. In the assignment double res = 2;, the integer value 2 is implicitly converted to double (yielding 2.0) per §6.3.1.4.\n4. printf("%.1f\\n", res) formats 2.0 with one decimal digit, printing 2.0.\n\nExam Trap: To obtain 2.5, at least one operand must be of floating type: 5.0 / 2, 5 / 2.0, or (double)5 / 2.',
        [
            (1, 4, 'Integer literals 5 and 2 evaluated. Binary operator / performs integer division, yielding integer 2.', {'temp': 2}, {'stack': [{'name': 'temp', 'type': 'int', 'val': 2}]}),
            (2, 4, 'Assignment to double res: integer 2 is converted to double 2.0.', {'res': 2.0}, {'stack': [{'name': 'res', 'type': 'double', 'addr': '0x1000', 'val': 2.0}]}),
            (3, 5, 'printf formats res as float with 1 decimal place: 2.0.', {'stdout': '2.0'}, {'stack': [{'name': 'res', 'val': 2.0}]}),
        ]
    )

    # Q034: Cast Precedence: (double)(5 / 2) -> Key B
    add_q(
        34, 'CAT_INT_PROM', 'Medium', 'Cast Precedence: (double)(5 / 2)',
        'What is printed by this code?',
        r"""#include <stdio.h>
int main() {
    double a = (double)(5 / 2);
    double b = (double)5 / 2;
    printf("%.1f %.1f\n", a, b);
    return 0;
}""",
        4, '(double)(5 / 2)', 'Parentheses force 5 / 2 to truncate to 2 first! In (double)5 / 2, unary cast has higher precedence than /, casting 5 to 5.0 first!',
        [
            ('A', '2.5 2.5', False, 'Thought the cast inside a converted the operands to double before division.', 'Parentheses force (5 / 2) to evaluate as integer division first, yielding 2; the cast then converts 2 to 2.0.'),
            ('B', '2.0 2.5', True, 'In a, (5 / 2) evaluates first to integer 2, then casts to 2.0. In b, (double)5 casts 5 to 5.0 first, and 5.0 / 2 yields 2.5 via usual arithmetic conversions.', ''),
            ('C', '2.0 2.0', False, 'Thought b also performed integer division before the cast.', 'Unary cast operator (type) has higher precedence than multiplicative operator /, so (double)5 binds before / 2.'),
            ('D', '2.5 2.0', False, 'Inverted the evaluation rules of parenthesized expression vs operator precedence.', 'Carefully trace parenthesis binding: (5 / 2) truncates first.')
        ],
        'In (double)(5 / 2), the division 5 / 2 evaluates first to 2, then casts to 2.0. In (double)5 / 2, the cast binds to 5, making 5.0 / 2 = 2.5.',
        'ISO/IEC 9899:1999 §6.5.4 & §6.5.5',
        "Operator Precedence vs Parenthesized Grouping:\n1. Variable a: In (double)(5 / 2), parentheses have higher precedence than the cast operator. The subexpression (5 / 2) is evaluated first. Both 5 and 2 are int, so integer division truncates to integer 2. Then (double)2 converts 2 to 2.0. Hence a = 2.0.\n2. Variable b: In (double)5 / 2, the unary cast operator (double) has higher precedence than the binary division operator /. Therefore, (double)5 is evaluated first, producing the double value 5.0.\n3. Usual Arithmetic Conversions (§6.3.1.8): For 5.0 / 2, the second operand 2 (int) is promoted to double (2.0), and floating-point division 5.0 / 2.0 produces double 2.5. Hence b = 2.5.\n4. printf outputs '2.0 2.5'.\n\nExam Trap: Never write (double)(a / b) expecting floating division; always cast an operand directly: ((double)a / b) or (a / (double)b).",
        [
            (1, 4, 'Expression (5 / 2) evaluates as int division -> 2. Cast (double)2 yields 2.0. Stored in a.', {'a': 2.0}, {'stack': [{'name': 'a', 'type': 'double', 'addr': '0x1000', 'val': 2.0}]}),
            (2, 5, 'Cast (double)5 binds first -> 5.0. 5.0 / 2 promotes 2 to 2.0 -> 5.0 / 2.0 = 2.5. Stored in b.', {'b': 2.5}, {'stack': [{'name': 'a', 'val': 2.0}, {'name': 'b', 'type': 'double', 'addr': '0x1008', 'val': 2.5}]}),
            (3, 6, 'printf outputs a and b formatted to 1 decimal place: 2.0 2.5.', {'stdout': '2.0 2.5'}, {'stack': [{'name': 'a', 'val': 2.0}, {'name': 'b', 'val': 2.5}]}),
        ]
    )

    # Q035: Signed vs Unsigned Relational Promotion Trap -> Key C
    add_q(
        35, 'CAT_INT_PROM', 'Nightmare', 'Signed vs Unsigned Relational Promotion Trap',
        'What is the output of the following program?',
        r"""#include <stdio.h>
int main() {
    int a = -1;
    unsigned int b = 1;
    if (a < b) {
        printf("LESS\n");
    } else {
        printf("NOT LESS\n");
    }
    return 0;
}""",
        6, 'a < b', 'Usual arithmetic conversions promote signed int a to unsigned int! -1 becomes UINT_MAX (4,294,967,295), which is NOT less than 1!',
        [
            ('A', 'LESS', False, 'Assumed standard mathematical comparison where -1 is less than 1.', 'In C, comparing signed int with unsigned int of the same rank promotes the signed int to unsigned int; -1 becomes UINT_MAX (4,294,967,295), which is greater than 1.'),
            ('B', 'Compile error', False, 'Thought comparing signed and unsigned integers causes a compiler syntax error.', 'Mixed signed/unsigned comparison is syntactically valid in C; compilers issue a warning (-Wsign-compare) but compile the code.'),
            ('C', 'NOT LESS', True, "Under ISO C §6.3.1.8, signed int a is converted to unsigned int. Two's complement -1 converts to UINT_MAX (4294967295), so (UINT_MAX < 1) is false, executing the else branch.", ''),
            ('D', 'Undefined Behavior', False, 'Thought comparing signed and unsigned types is Undefined Behavior.', 'The conversion rules are strictly well-defined by the ISO C standard, even though the result defies elementary arithmetic intuition.')
        ],
        'When a signed int is compared with an unsigned int of the same conversion rank, the signed int is promoted to unsigned int. -1 becomes UINT_MAX, so the comparison evaluates to false.',
        'ISO/IEC 9899:1999 §6.3.1.8#1 & §6.3.1.3',
        "The Usual Arithmetic Conversions (§6.3.1.8):\nWhen a binary operator has operands of different types, common types are determined through a fixed hierarchy:\n1. If both operands have the same integer conversion rank, and one is unsigned int while the other is signed int, the signed int operand is converted to unsigned int.\n2. Converting signed int to unsigned int (§6.3.1.3): The value is converted to unsigned by repeatedly adding 2^N (where N is the bit width of unsigned int). On a 32-bit system, -1 + 2^32 = 4,294,967,295 (UINT_MAX, hex 0xFFFFFFFF).\n3. The condition (a < b) therefore becomes (4294967295U < 1U), which evaluates to 0 (false).\n4. The else block executes, printing 'NOT LESS'.\n\nExam Trap: This is one of the most celebrated trap questions in C midterm exams and technical interviews. Always check for unsigned types in loop bounds, array sizes (size_t), and comparisons.",
        [
            (1, 4, "int a = -1 (two's complement 0xFFFFFFFF) and unsigned int b = 1 allocated on stack.", {'a': -1, 'b': 1}, {'stack': [{'name': 'a', 'type': 'int', 'addr': '0x1000', 'val': -1, 'hex': '0xFFFFFFFF'}, {'name': 'b', 'type': 'unsigned int', 'addr': '0x1004', 'val': 1, 'hex': '0x00000001'}]}),
            (2, 6, 'Usual arithmetic conversions: signed int a promoted to unsigned int -> UINT_MAX (4294967295U).', {'a_promoted': '4294967295U'}, {'stack': [{'name': 'temp_a', 'val': '4294967295U'}]}),
            (3, 6, 'Comparison: 4294967295U < 1U evaluates to 0 (false). Control branches to else.', {'condition': 0}, {'stack': []}),
            (4, 9, "printf in else branch executes, printing 'NOT LESS'.", {'stdout': 'NOT LESS'}, {'stack': [{'name': 'stdout', 'val': 'NOT LESS'}]}),
        ]
    )

    # Q036: Char Sign Extension during Comparison -> Key D
    add_q(
        36, 'CAT_INT_PROM', 'Tricky', 'Char Sign Extension during Comparison',
        'What is the output of the following program on an x86 architecture where char is signed by default?',
        r"""#include <stdio.h>
int main() {
    char c = 0x80;
    if (c == 0x80) {
        printf("EQUAL\n");
    } else {
        printf("NOT EQUAL\n");
    }
    return 0;
}""",
        5, 'c == 0x80', 'On systems where char is signed, 0x80 (-128) undergoes SIGN EXTENSION to int -128 (0xFFFFFF80), which does NOT equal positive 0x80 (+128)!',
        [
            ('A', 'EQUAL', False, 'Thought c retains the exact bit pattern 0x80 and matches literal 0x80.', 'char is promoted to signed int before comparison; because the sign bit (bit 7) is 1, sign extension produces -128 (0xFFFFFF80), while 0x80 is positive 128 (0x00000080).'),
            ('B', 'Compile error', False, 'Thought assigning hex literal 0x80 to char is illegal.', 'Hex literals fitting within type ranges or truncated to byte width are legal in C.'),
            ('C', 'Undefined Behavior', False, 'Thought comparing char with int is undefined.', 'Integer promotion of char to int is strictly defined by ISO C §6.3.1.1.'),
            ('D', 'NOT EQUAL', True, 'Signed char 0x80 represents -128; upon integer promotion, sign extension expands it to int -128 (0xFFFFFF80). The literal 0x80 is positive int 128 (0x00000080). -128 == 128 is false, so it prints NOT EQUAL.', '')
        ],
        'When a signed char with its high bit set (0x80 = -128) is promoted to int, sign extension produces -128 (0xFFFFFF80). The integer literal 0x80 is positive 128 (0x00000080). They are not equal.',
        'ISO/IEC 9899:1999 §6.3.1.1#2 & §6.4.4.1',
        "Integer Promotion and Sign Extension:\n1. On x86 and most typical platforms, char is signed by default (-128 to +127).\n2. The bit pattern 0x80 in 8-bit two's complement has the most significant bit (bit 7) set to 1, representing negative decimal -128.\n3. In the equality comparison (c == 0x80), C applies integer promotions (§6.3.1.1):\n   - char c is promoted to int. Because it is signed and negative, sign extension fills the upper 24 bits with 1s, producing 0xFFFFFF80 (decimal -128).\n   - The literal 0x80 is a hexadecimal integer constant. Under §6.4.4.1, its type is int, and its value is positive 128 (0x00000080).\n4. The comparison (-128 == 128) is false (0).\n5. The else block executes, printing 'NOT EQUAL'.\n\nExam Trap: If you need to store and compare raw bytes without sign extension traps, always declare variables as unsigned char.",
        [
            (1, 4, 'char c = 0x80 stored on stack. On signed char systems, 0x80 represents -128.', {'c': -128}, {'stack': [{'name': 'c', 'type': 'char', 'addr': '0x1000', 'val': -128, 'byte': '0x80'}]}),
            (2, 5, 'c promoted to int: sign extension expands 0x80 to 32-bit int 0xFFFFFF80 (-128).', {'promoted_c': -128}, {'stack': [{'name': 'promoted_c', 'val': -128, 'hex': '0xFFFFFF80'}]}),
            (3, 5, 'Literal 0x80 is int 128 (0x00000080). Comparison -128 == 128 evaluates to 0 (false).', {'condition': 0}, {'stack': []}),
            (4, 8, "printf in else branch executes, printing 'NOT EQUAL'.", {'stdout': 'NOT EQUAL'}, {'stack': [{'name': 'stdout', 'val': 'NOT EQUAL'}]}),
        ]
    )

    # Q037: Float vs Double Literal Precision Mismatch -> Key A
    add_q(
        37, 'CAT_INT_PROM', 'Tricky', 'Float vs Double Literal Precision Mismatch',
        'What is the output of the following program?',
        r"""#include <stdio.h>
int main() {
    float f = 0.1f;
    if (f == 0.1) {
        printf("EQUAL\n");
    } else {
        printf("NOT EQUAL\n");
    }
    return 0;
}""",
        5, 'f == 0.1', 'Literal 0.1 has type double! 0.1 cannot be represented exactly in binary floating-point, so float 0.1f and double 0.1 differ in extended precision bits!',
        [
            ('A', 'NOT EQUAL', True, "0.1 is not exactly representable in binary floating-point. The literal 0.1 has type double (53-bit mantissa); float f has only 24 bits. When f is promoted to double for comparison, the padded bits do not match 0.1's higher precision mantissa.", ''),
            ('B', 'EQUAL', False, 'Assumed 0.1f and 0.1 represent the exact same decimal number 0.1.', 'In IEEE-754 binary floating-point, 0.1 is a repeating fraction (0.000110011..._2). A double holds more repeating bits than a float, causing a mismatch.'),
            ('C', 'Compile error', False, 'Thought comparing float and double is a type error.', 'C automatically promotes float to double during binary comparisons with double.'),
            ('D', 'Undefined Behavior', False, 'Thought floating-point inequality is undefined.', 'Floating-point comparisons are strictly well-defined under IEEE-754 / ISO C §6.5.9.')
        ],
        '0.1 cannot be represented exactly in binary. The literal 0.1 has type double. When float f is promoted to double, its 24-bit precision padded with zeros does not equal double 0.1.',
        'ISO/IEC 9899:1999 §6.4.4.2 & §6.3.1.8',
        "Binary Representation of Decimal Fractions:\n1. In binary, 0.1 decimal is the repeating binary fraction 0.0001100110011..._2.\n2. In IEEE-754 single precision (float, 32 bits):\n   - Mantissa has 24 bits (1 implicit + 23 stored).\n   - 0.1f stored value is approx 0.100000001490116119384765625.\n3. In IEEE-754 double precision (double, 64 bits):\n   - Mantissa has 53 bits (1 implicit + 52 stored).\n   - 0.1 (without f suffix) is of type double per §6.4.4.2.\n   - Stored value is approx 0.10000000000000000555111512312578...\n4. Usual Arithmetic Conversions (§6.3.1.8): In (f == 0.1), float f is converted to double by zero-padding the least significant 29 bits. The resulting double does NOT match the more accurate double literal 0.1.\n5. The comparison evaluates to 0 (false), printing 'NOT EQUAL'.\n\nExam Trap: In C, unadorned floating constants like 3.14 or 0.1 are always double, NEVER float. Use suffix f (0.1f) to create a float constant.",
        [
            (1, 4, 'float f = 0.1f initialized. IEEE-754 single precision stores ~0.10000000149.', {'f': '0.10000000149f'}, {'stack': [{'name': 'f', 'type': 'float', 'addr': '0x1000', 'val': '0.10000000149'}]}),
            (2, 5, 'Equality test: f promoted to double (~0.10000000149) compared with double literal 0.1 (~0.1000000000000000055).', {'f_as_double': 0.10000000149, 'literal_double': 0.1}, {'stack': []}),
            (3, 5, 'Values differ at 8th decimal place -> condition evaluates to 0 (false). Branches to else.', {'condition': 0}, {'stack': []}),
            (4, 8, "printf in else branch executes, printing 'NOT EQUAL'.", {'stdout': 'NOT EQUAL'}, {'stack': [{'name': 'stdout', 'val': 'NOT EQUAL'}]}),
        ]
    )

    # Q038: Unsigned Integer Underflow Guarantee -> Key B
    add_q(
        38, 'CAT_INT_PROM', 'Medium', 'Unsigned Integer Underflow Guarantee',
        'What is the output of the following program?',
        r"""#include <stdio.h>
int main() {
    unsigned int x = 0;
    x--;
    if (x > 0) {
        printf("WRAP_AROUND\n");
    } else {
        printf("ZERO_OR_LESS\n");
    }
    return 0;
}""",
        5, 'x--', 'ISO C guarantees that unsigned arithmetic NEVER overflows or underflows; it strictly wraps around modulo 2^N! 0-- yields UINT_MAX!',
        [
            ('A', 'ZERO_OR_LESS', False, 'Assumed x became -1 and -1 is not greater than 0.', 'unsigned int cannot store negative numbers; in C, unsigned types wrap around modulo 2^N, so 0-- produces UINT_MAX (4,294,967,295), which is > 0.'),
            ('B', 'WRAP_AROUND', True, 'Under ISO C §6.2.5#9, computations involving unsigned operands can never overflow or underflow; they wrap around modulo 2^N. 0-- yields UINT_MAX (4294967295), which is > 0, so it prints WRAP_AROUND.', ''),
            ('C', 'Undefined Behavior', False, 'Confused unsigned arithmetic with signed integer overflow.', 'Signed integer overflow is Undefined Behavior, but unsigned overflow/underflow is strictly well-defined modular arithmetic.'),
            ('D', 'Runtime crash', False, 'Thought decrementing below zero triggers a CPU fault.', 'CPUs handle unsigned wrap silently in hardware using status flags.')
        ],
        'Unsigned integer arithmetic is defined by ISO C to be modulo 2^N. Decrementing 0 yields UINT_MAX (4,294,967,295 on 32-bit), which is greater than 0.',
        'ISO/IEC 9899:1999 §6.2.5#9',
        "Guaranteed Modular Arithmetic in C:\nISO C §6.2.5 paragraph 9 provides a fundamental language guarantee:\n'A computation involving unsigned operands can never overflow, because a result that cannot be represented by the resulting unsigned integer type is reduced modulo the number that is one greater than the largest value that can be represented by the resulting type.'\n\nExecution Step-by-Step:\n1. unsigned int x is initialized to 0 (hex 0x00000000).\n2. The statement x--; decrements x by 1.\n3. By the modular rule (0 - 1) mod 2^32 = 4,294,967,295 (UINT_MAX, hex 0xFFFFFFFF).\n4. In the conditional if (x > 0), 4294967295 > 0 is evaluated, which is true (1).\n5. The if block prints 'WRAP_AROUND'.\n\nExam Trap: This rule explains why an unsigned loop like for (unsigned int i = 5; i >= 0; i--) is an infinite loop—i >= 0 is permanently true!",
        [
            (1, 4, 'unsigned int x initialized to 0 (0x00000000) on stack.', {'x': 0}, {'stack': [{'name': 'x', 'type': 'unsigned int', 'addr': '0x1000', 'val': 0}]}),
            (2, 5, 'x-- executes: modular underflow (0 - 1 mod 2^32) produces UINT_MAX (4294967295, 0xFFFFFFFF).', {'x': 4294967295}, {'stack': [{'name': 'x', 'type': 'unsigned int', 'addr': '0x1000', 'val': 4294967295, 'hex': '0xFFFFFFFF'}]}),
            (3, 6, 'Condition (x > 0) evaluates 4294967295 > 0 -> true (1).', {'condition': 1}, {'stack': []}),
            (4, 7, "printf prints 'WRAP_AROUND'.", {'stdout': 'WRAP_AROUND'}, {'stack': [{'name': 'stdout', 'val': 'WRAP_AROUND'}]}),
        ]
    )

    # Q039: Leading Zero Octal Literal Trap -> Key C
    add_q(
        39, 'CAT_INT_PROM', 'Tricky', 'Leading Zero Octal Literal Trap',
        'What is the output of the following program?',
        r"""#include <stdio.h>
int main() {
    int a = 012;
    int b = 20;
    printf("%d %d\n", a, b);
    return 0;
}""",
        4, 'int a = 012;', 'A leading zero in an integer constant denotes an OCTAL (base 8) literal! 012 in octal is (1*8 + 2) = 10 decimal!',
        [
            ('A', '12 22', False, 'Assumed 012 is simply decimal 12 with a decorative zero.', 'In C, a leading 0 designates an octal literal. 012 is base 8, which equals decimal 10.'),
            ('B', '0 10', False, 'Thought the leading 0 was discarded or caused a truncation.', '012 is parsed as a whole token in base 8.'),
            ('C', '10 20', True, "In C, an integer constant beginning with '0' (and not '0x') is interpreted as an octal (base 8) number. 012 base 8 is 1 * 8^1 + 2 * 8^0 = 10 in decimal. printf with %d prints decimal 10 and 20.", ''),
            ('D', 'Compile error', False, 'Thought leading zeroes in integer declarations are forbidden syntax.', 'Leading zeroes are explicitly defined in the C grammar to signify octal constants.')
        ],
        'An integer constant beginning with 0 is an octal constant. 012 in base 8 = 1*8 + 2 = 10 decimal. %d prints decimal values.',
        'ISO/IEC 9899:1999 §6.4.4.1',
        'Integer Constant Syntax in ISO C (§6.4.4.1):\n1. Decimal constant: starts with a non-zero digit (1-9), e.g., 20.\n2. Octal constant: starts with digit 0 followed by octal digits (0-7), e.g., 012.\n   - Digit value: 1 * 8^1 + 2 * 8^0 = 8 + 2 = 10 decimal.\n3. Hexadecimal constant: starts with 0x or 0X, e.g., 0x12 (decimal 18).\n\nExecution:\n- Variable a is assigned the decimal value 10.\n- Variable b is assigned the decimal value 20.\n- printf("%d %d\\n", a, b) formats integers in decimal, printing \'10 20\'.\n\nExam Trap: Watch out for invalid octal literals like 018 or 079—they cause compilation errors because 8 and 9 are not valid octal digits!',
        [
            (1, 4, 'Constant 012 parsed in octal: 1*8 + 2 = 10. Stored in a as binary integer 10.', {'a': 10}, {'stack': [{'name': 'a', 'type': 'int', 'addr': '0x1000', 'val': 10}]}),
            (2, 5, 'Constant 20 parsed in decimal: stored in b.', {'b': 20}, {'stack': [{'name': 'a', 'val': 10}, {'name': 'b', 'type': 'int', 'addr': '0x1004', 'val': 20}]}),
            (3, 6, "printf formats a and b with %d (decimal): prints '10 20'.", {'stdout': '10 20'}, {'stack': [{'name': 'stdout', 'val': '10 20'}]}),
        ]
    )

    # Q040: Modulo with Negative Operands (C99 Standard) -> Key D
    add_q(
        40, 'CAT_INT_PROM', 'Tricky', 'Modulo with Negative Operands (C99 Standard)',
        'What is the output of the following program under ISO C99 / C11?',
        r"""#include <stdio.h>
int main() {
    int r1 = -7 % 3;
    int r2 = 7 % -3;
    printf("%d %d\n", r1, r2);
    return 0;
}""",
        4, '-7 % 3', 'In C99, integer division truncates toward zero: (a/b)*b + a%b == a. The sign of a % b matches the sign of the LEFT operand (dividend a)!',
        [
            ('A', '2 1', False, 'Applied Python-style mathematical modulo where the remainder shares the sign of the divisor.', 'In Python, -7 % 3 is 2. In C99, the remainder strictly takes the sign of the dividend (left operand).'),
            ('B', '-1 -1', False, 'Assumed both operations produce negative results.', "The second operand's sign has no effect on the remainder in C; 7 % -3 yields positive 1."),
            ('C', '1 1', False, 'Assumed remainder is always positive (Euclidean division).', 'C does not use Euclidean division; it uses truncated division where -7 % 3 is -1.'),
            ('D', '-1 1', True, 'Under ISO C99 §6.5.5#6, integer division truncates toward zero, and the algebraic identity (a / b) * b + a % b == a is guaranteed. Therefore, -7 / 3 = -2 with remainder -1; and 7 / -3 = -2 with remainder +1.', '')
        ],
        'In C99, the sign of a % b equals the sign of the dividend (a). -7 % 3 yields -1, while 7 % -3 yields 1.',
        'ISO/IEC 9899:1999 §6.5.5#6',
        "Algebraic Axiom of Division in C99:\nIn C89, integer division with negative operands was implementation-defined. C99 standardized this rigorously in §6.5.5 paragraph 6:\n1. Truncation toward zero: Division truncates toward zero: -7 / 3 = -2, and 7 / -3 = -2.\n2. Fundamental identity: (a / b) * b + a % b == a.\n   - For -7 % 3: (-2) * 3 + remainder = -7 ==> -6 + remainder = -7 ==> remainder = -1.\n   - For 7 % -3: (-2) * (-3) + remainder = 7 ==> 6 + remainder = 7 ==> remainder = +1.\n3. Rule of Thumb: The sign of the remainder a % b ALWAYS matches the sign of the dividend (a), completely independent of the sign of the divisor (b).\n4. printf outputs '-1 1'.\n\nExam Trap: Python and C differ fundamentally here: in Python -7 % 3 is 2, whereas in C it is -1. Never mix up the two on an exam!",
        [
            (1, 4, '-7 / 3 truncates to -2. Identity (-2)*3 + r1 == -7 yields r1 = -1.', {'r1': -1}, {'stack': [{'name': 'r1', 'type': 'int', 'addr': '0x1000', 'val': -1}]}),
            (2, 5, '7 / -3 truncates to -2. Identity (-2)*(-3) + r2 == 7 yields r2 = 1.', {'r2': 1}, {'stack': [{'name': 'r1', 'val': -1}, {'name': 'r2', 'type': 'int', 'addr': '0x1004', 'val': 1}]}),
            (3, 6, "printf formats r1 and r2: prints '-1 1'.", {'stdout': '-1 1'}, {'stack': [{'name': 'stdout', 'val': '-1 1'}]}),
        ]
    )

    # Q041: Integer Promotion of Sub-int Types -> Key A
    add_q(
        41, 'CAT_INT_PROM', 'Medium', 'Integer Promotion of Sub-int Types',
        'What is the output of the following program on a platform with 32-bit int?',
        r"""#include <stdio.h>
int main() {
    char c1 = 10, c2 = 20;
    printf("%zu\n", sizeof(c1 + c2));
    return 0;
}""",
        5, 'sizeof(c1 + c2)', 'In any arithmetic expression, types smaller than int (char, short) undergo INTEGER PROMOTION to int! sizeof(c1 + c2) is sizeof(int) = 4!',
        [
            ('A', '4', True, 'Under ISO C §6.3.1.1, in any arithmetic expression, char operands undergo integer promotion to int. Therefore, c1 + c2 evaluates as an int addition, and sizeof(int) is 4 bytes.', ''),
            ('B', '1', False, 'Thought the result of adding two chars remains a char (1 byte).', 'C does not perform arithmetic on char types directly; they are always promoted to int first.'),
            ('C', '2', False, 'Thought it promoted to short.', 'Integer promotion always targets int (or unsigned int if int cannot represent all values), never short.'),
            ('D', 'Compile error', False, 'Thought sizeof on an addition expression is invalid.', 'sizeof accepts any valid C expression and evaluates its type at compile time without runtime evaluation.')
        ],
        'Operands of type char are promoted to int before addition. The result of (c1 + c2) has type int, whose sizeof is 4.',
        'ISO/IEC 9899:1999 §6.3.1.1#2 & §6.5.3.4',
        "Integer Promotion Rules in ISO C:\n1. Under §6.3.1.1 paragraph 2: 'If an int can represent all values of the original type, the value is converted to an int; otherwise, it is converted to an unsigned int. These are called the integer promotions.'\n2. Because signed char (-128 to 127) fits comfortably inside a 32-bit int (-2^31 to 2^31-1), both c1 and c2 are promoted to int before the binary + operator evaluates.\n3. The type of the expression (c1 + c2) is therefore int.\n4. sizeof(expr) yields the size in bytes of the type of the expression.\n5. On a 32-bit int architecture, sizeof(int) is 4.\n6. Notice that sizeof does NOT evaluate the expression at runtime (§6.5.3.4#2); it inspects the expression's static type at compile time.\n\nExam Trap: Compare sizeof(c1 + c2) (which is 4) with sizeof(c1) (which is 1).",
        [
            (1, 4, 'char c1 = 10 and char c2 = 20 allocated on stack (1 byte each).', {'c1': 10, 'c2': 20}, {'stack': [{'name': 'c1', 'type': 'char', 'addr': '0x1000', 'val': 10}, {'name': 'c2', 'type': 'char', 'addr': '0x1001', 'val': 20}]}),
            (2, 5, 'In expression c1 + c2, both chars undergo integer promotion to int. Type of expression is int.', {'type': 'int'}, {'stack': []}),
            (3, 5, 'sizeof(int) evaluated at compile-time: yields 4.', {'sizeof_result': 4}, {'stack': []}),
            (4, 5, 'printf prints 4.', {'stdout': '4'}, {'stack': [{'name': 'stdout', 'val': '4'}]}),
        ]
    )

    # Q042: Format Specifier Mismatch (%d on float) -> Key B
    add_q(
        42, 'CAT_INT_PROM', 'Tricky', 'Format Specifier Mismatch (%d on float)',
        'What is the behavior of the following program?',
        r"""#include <stdio.h>
int main() {
    float f = 5.0f;
    printf("%d\n", f);
    return 0;
}""",
        5, 'printf("%d\\n", f);', 'Passing a float to %d is a format specifier mismatch! Variadic functions promote float to double, but %d reads an int, causing UNDEFINED BEHAVIOR!',
        [
            ('A', 'Prints 5', False, 'Thought printf automatically casts floating-point numbers to integer values.', 'printf is a variadic function; it receives raw bytes according to the calling convention and relies strictly on the format string to interpret them. No implicit typecasting occurs.'),
            ('B', 'Undefined Behavior (Prints garbage value or unexpected number)', True, 'Under ISO C §7.19.6.1#9, if any argument is not the correct type for the format specifier, the behavior is Undefined Behavior. In variadic calls, float is promoted to double (passed in an XMM floating register on x86-64), whereas %d reads an integer register (such as ESI/RDX), reading unrelated stack/register data.', ''),
            ('C', 'Compile error', False, 'Thought format specifier mismatches are hard compiler errors.', 'In standard C, format string errors generate compiler warnings (-Wformat), not compilation errors.'),
            ('D', 'Prints 5.0', False, '%d is for decimal integers, not floats.', '%d interprets bits as an integer, not a floating-point representation.')
        ],
        'Using %d with a float argument violates the type contract of printf, causing Undefined Behavior under ISO C §7.19.6.1#9.',
        'ISO/IEC 9899:1999 §7.19.6.1#9 & §6.5.2.2#6',
        "Calling Convention and Variadic Mechanics:\n1. Default Argument Promotions (§6.5.2.2#6): In a call to a variadic function (like printf), arguments in the variable argument list undergo default promotions:\n   - float arguments are promoted to double.\n2. ABI Calling Conventions (e.g. System V AMD64 or Windows x64):\n   - Floating-point arguments (double) are passed in SSE/vector registers (XMM0, XMM1...).\n   - Integer arguments (int) expected by %d are read from general-purpose registers (RSI/RDX or RDX/R8).\n3. When printf encounters %d, it reads an integer register that was never populated with f's value, extracting unrelated garbage data.\n4. Even on a pure stack-based 32-bit cdecl calling convention, double occupies 8 bytes while %d reads 4 bytes, desynchronizing the stack pointer for subsequent arguments.\n5. ISO C §7.19.6.1#9 explicitly states: 'If any argument is not the correct type for the corresponding conversion specification, the behavior is undefined.'",
        [
            (1, 4, 'float f = 5.0f initialized on stack.', {'f': 5.0}, {'stack': [{'name': 'f', 'type': 'float', 'addr': '0x1000', 'val': 5.0}]}),
            (2, 5, 'Variadic call default argument promotion: float f is promoted to double (8 bytes). Passed in XMM register.', {'promoted_f': 'double 5.0'}, {'registers': [{'reg': 'XMM1', 'val': '5.0 (double)'}]}),
            (3, 5, 'printf parses %d: expects int in general-purpose register (e.g. ESI/EDX). Reads uninitialized/garbage data -> UNDEFINED BEHAVIOR.', {'output': 'garbage'}, {'stack': []}),
        ]
    )

    # Q043: Integer Division by Zero -> Key C
    add_q(
        43, 'CAT_INT_PROM', 'Easy', 'Integer Division by Zero',
        'What happens when the following program is executed?',
        r"""#include <stdio.h>
int main() {
    int a = 5;
    int b = 0;
    int c = a / b;
    printf("%d\n", c);
    return 0;
}""",
        5, 'a / b', 'Dividing by zero in integer arithmetic is UNDEFINED BEHAVIOR in C, causing the CPU to raise SIGFPE and CRASH the program!',
        [
            ('A', 'Prints Infinity', False, 'Confused integer division with IEEE-754 floating-point division (where 5.0 / 0.0 = +Inf).', 'Integer division has no representation for Infinity; the hardware ALU raises an interrupt.'),
            ('B', 'Prints 0', False, 'Thought dividing by zero evaluates to zero.', 'Division by zero is mathematically undefined and cannot return zero.'),
            ('C', 'Runtime Crash (Floating Point Exception / SIGFPE)', True, 'Under ISO C §6.5.5#5, if the value of the second operand of / or % is zero, the behavior is undefined. On typical hardware, the CPU raises an arithmetic fault (SIGFPE) causing abnormal termination.', ''),
            ('D', 'Compilation Error', False, 'Thought division by zero is caught by the compiler.', 'Because b is a variable, the division is evaluated at runtime, resulting in a runtime crash.')
        ],
        'Integer division by zero is undefined behavior under ISO C §6.5.5#5. The CPU raises a division-by-zero hardware exception (SIGFPE), terminating the process.',
        'ISO/IEC 9899:1999 §6.5.5#5',
        "Hardware and Standard Semantics of Division by Zero:\n1. ISO C Standard §6.5.5 paragraph 5 states:\n   'The result of the / operator is the quotient from the division of the first operand by the second; the result of the % operator is the remainder. If the value of the second operand is zero, the behavior is undefined.'\n2. Hardware Execution on x86/x86-64:\n   - Integer division is implemented by the IDIV instruction.\n   - When the divisor operand in the register is 0, the CPU hardware generates an internal interrupt (Interrupt 0: Divide Error Exception).\n   - The operating system kernel intercepts this hardware fault and dispatches a signal (SIGFPE: Floating Point Exception—historical Unix naming includes integer divide errors) to the process.\n   - Unless a signal handler is installed, the default action terminates the process immediately with an abnormal exit code.\n\nExam Trap: Distinguish integer division (crash/SIGFPE) from floating-point division (5.0 / 0.0), which yields Infinity under IEEE-754 without crashing.",
        [
            (1, 4, 'int a = 5 and int b = 0 allocated on stack.', {'a': 5, 'b': 0}, {'stack': [{'name': 'a', 'type': 'int', 'addr': '0x1000', 'val': 5}, {'name': 'b', 'type': 'int', 'addr': '0x1004', 'val': 0}]}),
            (2, 5, 'CPU executes IDIV with divisor register holding 0.', {'divisor': 0}, {'registers': [{'reg': 'EAX', 'val': 5}, {'reg': 'ECX', 'val': 0}]}),
            (3, 5, 'CPU raises Hardware Exception 0 (Divide Error). OS signals SIGFPE. Process aborted immediately.', {'status': 'CRASH (SIGFPE)'}, {'stack': []}),
        ]
    )

    # Q044: Bitwise NOT with Integer Promotion -> Key D
    add_q(
        44, 'CAT_INT_PROM', 'Medium', 'Bitwise NOT with Integer Promotion',
        'What is the output of the following program on a system with 32-bit int?',
        r"""#include <stdio.h>
int main() {
    unsigned char a = 0;
    if (~a == 255) {
        printf("1\n");
    } else {
        printf("0\n");
    }
    return 0;
}""",
        5, '~a == 255', 'Unary ~ promotes unsigned char a to int! ~0 is -1 (0xFFFFFFFF), which does NOT equal 255 (0x000000FF)!',
        [
            ('A', '1', False, 'Thought ~0 on unsigned char inverts 8 bits to 0xFF (255).', 'Before applying bitwise NOT (~), unsigned char undergoes integer promotion to int (32 bits). ~0 becomes 0xFFFFFFFF (-1), not 255.'),
            ('B', '255', False, 'Selected the inverted value directly.', 'The code prints either 1 or 0 from the if branches.'),
            ('C', 'Compile error', False, 'Thought ~ cannot be applied to unsigned char.', 'Bitwise operators on integer types are fully valid.'),
            ('D', '0', True, 'Due to integer promotion (§6.3.1.1), unsigned char a (0) is promoted to signed int (0x00000000). The bitwise NOT operator ~ flips all 32 bits, producing 0xFFFFFFFF (-1). -1 does not equal 255, so the else branch prints 0.', '')
        ],
        '~ promotes unsigned char to int before inverting. ~0 yields 32-bit 0xFFFFFFFF (-1), which does not equal 255 (0x000000FF).',
        'ISO/IEC 9899:1999 §6.5.3.3#4 & §6.3.1.1#2',
        "Integer Promotion with Bitwise Operators:\n1. Unary ~ operator specification (§6.5.3.3#4):\n   'The result of the ~ operator is the bitwise complement of its operand (that is, each bit in the result is set if and only if the corresponding bit in the converted operand is not set). The integer promotions are performed on the operand, and the result has the promoted type.'\n2. Trace:\n   - unsigned char a = 0 (8 bits: 00000000_2).\n   - Integer promotion: converts a to int (32 bits: 0x00000000).\n   - Bitwise NOT: ~0x00000000 produces 32-bit 0xFFFFFFFF (decimal -1 in two's complement).\n   - The integer constant 255 is 0x000000FF (decimal 255).\n   - Comparison: 0xFFFFFFFF == 0x000000FF evaluates to false (0).\n3. The else block executes, printing '0'.\n\nExam Trap: To keep the operation within 8 bits, an explicit cast or bitmask is required: (unsigned char)~a == 255 or (~a & 0xFF) == 255.",
        [
            (1, 4, 'unsigned char a = 0 stored in 1 byte on stack.', {'a': 0}, {'stack': [{'name': 'a', 'type': 'unsigned char', 'addr': '0x1000', 'val': 0, 'hex': '0x00'}]}),
            (2, 5, 'Integer promotion: a converted to 32-bit int 0x00000000. ~ flips all 32 bits to 0xFFFFFFFF (-1).', {'promoted_not_a': -1}, {'stack': [{'name': 'temp', 'val': -1, 'hex': '0xFFFFFFFF'}]}),
            (3, 5, 'Comparison: -1 == 255 (0xFFFFFFFF == 0x000000FF) evaluates to 0 (false). Branches to else.', {'condition': 0}, {'stack': []}),
            (4, 8, "printf in else branch executes, printing '0'.", {'stdout': '0'}, {'stack': [{'name': 'stdout', 'val': '0'}]}),
        ]
    )

    # Q045: Signed Char Overflow Wrap -> Key A
    add_q(
        45, 'CAT_INT_PROM', 'Medium', 'Signed Char Overflow Wrap',
        'What is the output of the following program on an x86 system with signed 8-bit char?',
        r"""#include <stdio.h>
int main() {
    char c = 127;
    c++;
    printf("%d\n", c);
    return 0;
}""",
        5, 'c++', "Signed 8-bit char ranges from -128 to +127. Incrementing 127 wraps around to -128 in two's complement!",
        [
            ('A', '-128', True, "In 8-bit two's complement arithmetic, 127 is 01111111_2. Incrementing by 1 produces 10000000_2, which represents -128. printf with %d sign-extends -128 to print -128.", ''),
            ('B', '128', False, 'Assumed char is unsigned or accommodates values up to 255.', 'On x86 GCC, char is signed by default (-128 to 127); it cannot represent +128.'),
            ('C', '0', False, 'Thought overflow resets to 0.', "Two's complement overflow wraps to the minimum negative value (-128)."),
            ('D', '127', False, 'Thought the value saturated at maximum.', 'C arithmetic does not saturate unless explicitly implemented with clamping logic.')
        ],
        "Signed 8-bit char holds values from -128 to 127. In two's complement, 127 (0x7F) + 1 wraps to -128 (0x80).",
        'ISO/IEC 9899:1999 §6.2.6.2 & §6.3.1.3',
        'Two\'s Complement Representation and Byte Overflow:\n1. On x86/GCC, char is signed by default, occupying 1 byte (8 bits).\n2. Maximum signed 8-bit value is 2^7 - 1 = 127 (binary 01111111, hex 0x7F).\n3. When c++ executes:\n   - 01111111 + 1 = 10000000 (hex 0x80).\n   - In two\'s complement representation, a leading 1 in the sign bit signifies a negative number.\n   - Value is -2^7 = -128.\n4. When passed to printf("%d\\n", c):\n   - char undergoes integer promotion to int.\n   - Sign extension expands 0x80 to 32-bit 0xFFFFFF80 (-128 decimal).\n5. printf outputs \'-128\'.\n\nExam Trap: While signed int overflow is technically Undefined Behavior in ISO C, signed char assignment/conversion is implementation-defined wrap (§6.3.1.3), consistently yielding -128 across all standard PC compilers.',
        [
            (1, 4, 'char c initialized to 127 (0x7F, 01111111_2) on stack.', {'c': 127}, {'stack': [{'name': 'c', 'type': 'char', 'addr': '0x1000', 'val': 127, 'hex': '0x7F'}]}),
            (2, 5, "c++ executes: 0x7F + 1 = 0x80 (10000000_2). In 8-bit signed two's complement, this is -128.", {'c': -128}, {'stack': [{'name': 'c', 'type': 'char', 'addr': '0x1000', 'val': -128, 'hex': '0x80'}]}),
            (3, 6, "printf formats c with %d: sign extension converts -128 to int -128. Prints '-128'.", {'stdout': '-128'}, {'stack': [{'name': 'stdout', 'val': '-128'}]}),
        ]
    )

    # Q046: Comma Operator in Loop Termination Condition -> Key B
    add_q(
        46, 'CAT_INT_PROM', 'Tricky', 'Comma Operator in Loop Termination Condition',
        'What is the output of the following program?',
        r"""#include <stdio.h>
int main() {
    int i = 0, j = 0;
    while (i < 2, j < 4) {
        i++;
        j++;
    }
    printf("%d %d\n", i, j);
    return 0;
}""",
        5, 'while (i < 2, j < 4)', 'The comma operator discards the result of i < 2! The loop termination condition is determined ENTIRELY by the rightmost expression j < 4!',
        [
            ('A', '2 2', False, 'Thought the loop stopped when i reached 2 because of i < 2.', 'The comma operator evaluates i < 2, discards the result, and uses j < 4 as the sole controlling expression. i continues incrementing beyond 2.'),
            ('B', '4 4', True, 'In (i < 2, j < 4), the comma operator evaluates i < 2, discards its value, and evaluates j < 4 as the condition. The loop continues until j reaches 4. Since both i and j increment in lockstep, both end at 4.', ''),
            ('C', '2 4', False, 'Thought i stopped at 2 while j continued to 4.', 'Both i and j increment together in each iteration.'),
            ('D', 'Infinite loop', False, 'Thought comma expression creates an invalid loop test that never terminates.', 'j increments each iteration and terminates when j = 4.')
        ],
        'The comma operator evaluates left-to-right and yields the value of the rightmost operand. The while condition evaluates to (j < 4), running 4 iterations.',
        'ISO/IEC 9899:1999 §6.5.17 & §6.8.5',
        "Comma Operator Semantics in Controlling Expressions:\n1. The controlling condition of the while loop is: (i < 2, j < 4).\n2. Under ISO C §6.5.17 paragraph 2:\n   'The left operand of a comma operator is evaluated as a void expression; there is a sequence point after its evaluation. Then the right operand is evaluated; the result has its type and value.'\n3. In every loop iteration:\n   - i < 2 is evaluated (yielding 1 or 0), and immediately discarded.\n   - j < 4 is evaluated, and its truth value governs the loop.\n4. Iterations trace:\n   - Iter 0: i=0, j=0. j < 4 (true). i becomes 1, j becomes 1.\n   - Iter 1: i=1, j=1. j < 4 (true). i becomes 2, j becomes 2.\n   - Iter 2: i=2, j=2. i < 2 is false (0, discarded!), but j < 4 is true! i becomes 3, j becomes 3.\n   - Iter 3: i=3, j=3. j < 4 (true). i becomes 4, j becomes 4.\n   - Iter 4: j=4. j < 4 is false (0). Loop terminates.\n5. printf outputs '4 4'.\n\nExam Trap: Never confuse a comma operator in a condition with logical AND (&&). If the programmer intended both conditions to hold, they needed (i < 2 && j < 4).",
        [
            (1, 4, 'i = 0, j = 0 allocated on stack.', {'i': 0, 'j': 0}, {'stack': [{'name': 'i', 'addr': '0x1000', 'val': 0}, {'name': 'j', 'addr': '0x1004', 'val': 0}]}),
            (2, 5, 'Iterations 1-2: i and j increment to 2. (i < 2) is now false, but comma operator discards it; (j < 4) continues the loop.', {'i': 2, 'j': 2}, {'stack': [{'name': 'i', 'val': 2}, {'name': 'j', 'val': 2}]}),
            (3, 5, 'Iterations 3-4: i and j increment to 4. When j reaches 4, (j < 4) evaluates to false. Loop terminates.', {'i': 4, 'j': 4}, {'stack': [{'name': 'i', 'val': 4}, {'name': 'j', 'val': 4}]}),
            (4, 9, "printf prints i and j: '4 4'.", {'stdout': '4 4'}, {'stack': [{'name': 'stdout', 'val': '4 4'}]}),
        ]
    )

    # =========================================================================
    # CAT_STR_LIT (Q047 - Q058): Strings, Literals & Buffer Management
    # =========================================================================

    # Q047: String Literal Immutability (.rodata Crash) -> Key C
    add_q(
        47, 'CAT_STR_LIT', 'Medium', 'String Literal Immutability (.rodata Crash)',
        'What happens when executing the following program on modern operating systems?',
        r"""#include <stdio.h>
int main() {
    char *s = "hello";
    s[0] = 'H';
    printf("%s\n", s);
    return 0;
}""",
        5, "s[0] = 'H';", 'String literals reside in READ-ONLY memory (.rodata)! Modifying a string literal via pointer dereference is UNDEFINED BEHAVIOR, causing a SIGSEGV segmentation fault!',
        [
            ('A', 'Prints Hello', False, 'Assumed string literals can be modified in place.', 'String literals are placed in write-protected memory pages (.rodata). In-place modification is forbidden.'),
            ('B', 'Prints hello', False, 'Thought the write was silently ignored without error.', 'Modern operating systems use MMU page tables to enforce write-protection; unauthorized writes trigger a hardware trap.'),
            ('C', 'Runtime Crash (Segmentation Fault)', True, 'Under ISO C §6.4.5#6, modifying a string literal is Undefined Behavior. On modern operating systems, string literals are placed in the read-only data segment (.rodata). Writing to read-only memory causes the OS/MMU to raise SIGSEGV, crashing the process.', ''),
            ('D', 'Compilation Error', False, "Thought char *s = 'hello' is rejected by the compiler.", 'For historical C compatibility, string literals have type char[] (not const char[]), allowing implicit assignment to char* without a compile error.')
        ],
        'String literals reside in read-only memory (.rodata). Modifying them is Undefined Behavior under ISO C §6.4.5#6, causing a Segmentation Fault.',
        'ISO/IEC 9899:1999 §6.4.5#6',
        'Memory Segmentation and String Literal Protection:\n1. Memory Segments:\n   - Pointer s is an automatic variable allocated on the runtime stack.\n   - The string literal "hello" is stored in the read-only data segment (.rodata or text section) by the linker.\n   - Pointer s holds the virtual address of the string literal in .rodata (e.g. 0x00405000).\n2. Standard Mandate (§6.4.5#6):\n   \'If the program attempts to modify such an array, the behavior is undefined.\'\n3. Hardware & OS Protection:\n   - Modern operating systems (Windows, Linux, macOS) configure page table entries for .rodata with Read-Only permissions (R bit set, W bit cleared).\n   - When s[0] = \'H\' executes, the CPU attempts a write instruction to a write-protected page.\n   - The Memory Management Unit (MMU) generates a Page Fault exception.\n   - The kernel translates this fault into a SIGSEGV (or STATUS_ACCESS_VIOLATION on Windows), immediately terminating the program.\n\nExam Trap: If you need a mutable string, declare it as an array: char s[] = "hello"; which copies the characters onto the mutable stack frame.',
        [
            (1, 4, "Literal 'hello' located in .rodata at 0x00405000. Pointer s allocated on stack pointing to .rodata.", {'s': '0x00405000'}, {'stack': [{'name': 's', 'type': 'char*', 'addr': '0x1000', 'val': '0x00405000', 'pointsTo': '.rodata'}], 'rodata': [{'addr': '0x00405000', 'val': 'hello\\0', 'access': 'READ_ONLY'}]}),
            (2, 5, "Attempt to write 'H' to s[0] (0x00405000). MMU detects write-protection violation on .rodata page.", {'fault_addr': '0x00405000'}, {'stack': []}),
            (3, 5, 'OS dispatches SIGSEGV (Segmentation Fault). Process terminates abnormally.', {'status': 'CRASH (SIGSEGV)'}, {'stack': []}),
        ]
    )

    # Q048: Mutable Stack Array String -> Key D
    add_q(
        48, 'CAT_STR_LIT', 'Easy', 'Mutable Stack Array String',
        'What is the output of the following program?',
        r"""#include <stdio.h>
int main() {
    char s[] = "hello";
    s[0] = 'H';
    printf("%s\n", s);
    return 0;
}""",
        5, "s[0] = 'H';", 'Because s is declared as an ARRAY (char s[]), the string literal is COPIED onto the STACK at initialization! Stack memory is writable, so s[0] modifies successfully!',
        [
            ('A', 'Segmentation Fault', False, 'Confused char s[] with char *s.', 'char *s points to read-only .rodata; char s[] creates an array on the stack initialized with a copy of the string, which is fully mutable.'),
            ('B', 'hello', False, 'Thought array elements cannot be modified.', 'Array elements in C are mutable variables unless declared with the const qualifier.'),
            ('C', 'Compile error', False, "Thought char s[] = 'hello' requires explicit array bounds.", "The compiler automatically sizes char s[] to 6 bytes (including the null terminator '\\0')."),
            ('D', 'Hello', True, 'char s[] = "hello" allocates a 6-byte array on the stack and copies the characters into it. Because stack memory is read-write, assigning s[0] = \'H\' cleanly mutates the first element to \'H\', printing \'Hello\'.', '')
        ],
        'Declaring char s[] allocates mutable stack memory and copies the literal into it. Modifying s[0] safely updates the stack array, outputting Hello.',
        'ISO/IEC 9899:1999 §6.7.8#14',
        'Array Initialization vs Pointer to Literal:\n1. Under ISO C §6.7.8 paragraph 14:\n   \'An array of character type may be initialized by a character string literal, optionally enclosed in braces. Successive characters of the character string literal (including the terminating null character if there is room or if the array is of unknown size) initialize the elements of the array.\'\n2. Key Architectural Difference:\n   - char *s = "hello"; points directly to the read-only .rodata segment.\n   - char s[] = "hello"; reserves 6 bytes on the active stack frame and executes a memcpy from .rodata to stack during function entry.\n3. The stack memory region is marked with Read-Write permissions.\n4. When s[0] = \'H\' executes, byte 0 on the stack changes from \'h\' (0x68) to \'H\' (0x48).\n5. printf("%s\\n", s) reads the mutated stack array: \'Hello\'.\n\nExam Trap: Always distinguish char s[] (mutable stack copy) from char *s (immutable pointer to .rodata).',
        [
            (1, 4, "Array s allocated on stack (6 bytes: 'h','e','l','l','o','\\0'). Initialized by copy from .rodata.", {'s': 'hello'}, {'stack': [{'name': 's[0]', 'addr': '0x1000', 'val': "'h'"}, {'name': 's[1]', 'addr': '0x1001', 'val': "'e'"}, {'name': 's[2]', 'addr': '0x1002', 'val': "'l'"}, {'name': 's[3]', 'addr': '0x1003', 'val': "'l'"}, {'name': 's[4]', 'addr': '0x1004', 'val': "'o'"}, {'name': 's[5]', 'addr': '0x1005', 'val': "'\\0'"}]}),
            (2, 5, "s[0] = 'H' mutates stack byte at 0x1000 from 'h' to 'H'. Stack write succeeds.", {'s[0]': "'H'"}, {'stack': [{'name': 's[0]', 'addr': '0x1000', 'val': "'H'"}]}),
            (3, 6, "printf formats string s from stack address 0x1000: outputs 'Hello'.", {'stdout': 'Hello'}, {'stack': [{'name': 's', 'val': 'Hello'}]}),
        ]
    )

    # Q049: Missing Null Terminator in Sized Array -> Key A
    add_q(
        49, 'CAT_STR_LIT', 'Tricky', 'Missing Null Terminator in Sized Array',
        'What is the behavior of the following program?',
        r"""#include <stdio.h>
#include <string.h>
int main() {
    char s[5] = "hello";
    printf("%zu\n", strlen(s));
    return 0;
}""",
        5, 'char s[5] = "hello";', 'The array size is 5, but "hello" requires 6 bytes (including \'\\0\')! C allows this truncation, but s has NO null terminator, causing strlen() to read out-of-bounds into UNDEFINED BEHAVIOR!',
        [
            ('A', "Undefined Behavior (Buffer overread searching for '\\0')", True, 'In C, char s[5] = "hello" fits exactly 5 characters (\'h\',\'e\',\'l\',\'l\',\'o\') without storing the null terminator \'\\0\'. Calling strlen(s) scans past the array bounds on the stack until it encounters a random zero byte in memory, invoking Undefined Behavior.', ''),
            ('B', 'Prints 5', False, 'Thought strlen stops at the array boundary.', "strlen does not know array sizes; it increments a pointer until it finds a '\\0' byte in memory."),
            ('C', 'Compilation Error: string too long', False, 'Thought C compilers reject string initializers that omit the null terminator.', "In ISO C §6.7.8#14, if the array size matches the number of characters excluding '\\0', the null terminator is silently omitted without compile error (unlike C++)."),
            ('D', 'Prints 4', False, "Thought the compiler truncated the string to 'hell\\0'.", "All 5 characters are copied; no '\\0' is appended.")
        ],
        'char s[5] = "hello" initializes s without a null terminator. Calling strlen(s) reads past array bounds, invoking Undefined Behavior.',
        'ISO/IEC 9899:1999 §6.7.8#14 & §7.21.6.3',
        'C vs C++ String Initialization Rules:\n1. In C (ISO C §6.7.8#14):\n   - An array of characters may be initialized by a string literal without room for the terminating null character.\n   - char s[5] = "hello"; is valid C syntax! It initializes s[0]=\'h\', s[1]=\'e\', s[2]=\'l\', s[3]=\'l\', s[4]=\'o\'. The \'\\0\' is discarded.\n   - (Note: In C++, this is a compilation error: \'initializer-string for array of chars is too long\').\n2. The strlen() Contract (§7.21.6.3):\n   - \'The strlen function computes the length of the string pointed to by s... stopping at the first null character.\'\n3. Memory Analysis:\n   - Array s contains 5 non-zero characters on the stack.\n   - strlen(s) loops while (*p != \'\\0\') p++;\n   - Because s[5] is outside the array, strlen reads adjacent uninitialized stack memory (saved frame pointers, padding, local variables).\n   - Accessing beyond the allocated bounds of an object is Undefined Behavior.\n\nExam Trap: Never pass a non-null-terminated char array to printf("%s"), strlen(), or strcpy().',
        [
            (1, 5, 'char s[5] allocated on stack (5 bytes). Stack memory reserved for indices 0 through 4.', {'s': 'uninitialized'}, {'stack': [{'name': 's[0..4]', 'addr': '0x1000-0x1004'}]}),
            (2, 5, "Characters 'h','e','l','l','o' copied into s[0..4]. Null terminator '\\0' is omitted due to explicit array size 5.", {'s': 'hello (unterminated)'}, {'stack': [{'name': 's[0]', 'addr': '0x1000', 'val': "'h'"}, {'name': 's[1]', 'addr': '0x1001', 'val': "'e'"}, {'name': 's[2]', 'addr': '0x1002', 'val': "'l'"}, {'name': 's[3]', 'addr': '0x1003', 'val': "'l'"}, {'name': 's[4]', 'addr': '0x1004', 'val': "'o'"}, {'name': 'adjacent_stack', 'addr': '0x1005', 'val': '0x3F (garbage)'}]}),
            (3, 6, "strlen(s) called: loops through s[0..4] searching for '\\0'. Finds no null terminator within array bounds.", {'scanned_bytes': 5}, {'stack': []}),
            (4, 6, 'strlen continues scanning past 0x1004, reading adjacent unallocated/garbage stack bytes -> UNDEFINED BEHAVIOR.', {'overread_bytes': 12}, {'stack': []}),
        ]
    )

    # Q050: Difference between sizeof and strlen -> Key B
    add_q(
        50, 'CAT_STR_LIT', 'Easy', 'Difference between sizeof and strlen',
        'What is the output of the following program?',
        r"""#include <stdio.h>
#include <string.h>
int main() {
    char s[] = "hello";
    printf("%zu %zu\n", sizeof(s), strlen(s));
    return 0;
}""",
        6, 'sizeof(s), strlen(s)', "sizeof counts total array bytes INCLUDING the '\\0' (6 bytes)! strlen counts characters EXCLUDING the '\\0' (5 characters)!",
        [
            ('A', '5 5', False, 'Thought sizeof also excludes the null terminator.', "sizeof evaluates the total memory footprint of the array, which includes the trailing '\\0' byte."),
            ('B', '6 5', True, 'char s[] = "hello" has 5 letters plus 1 terminating null character \'\\0\', so sizeof(s) is 6 bytes. strlen(s) counts characters up to (but not including) the \'\\0\', returning 5.', ''),
            ('C', '5 6', False, 'Inverted the meanings of sizeof and strlen.', 'sizeof measures total allocated bytes; strlen measures character count.'),
            ('D', '8 5', False, 'Confused array s with a pointer variable (which might be 8 bytes on 64-bit).', 's is an array, not a pointer; sizeof(s) yields array byte count (6).')
        ],
        "sizeof(s) returns total array storage (6 bytes including '\\0'). strlen(s) returns string length (5 characters excluding '\\0').",
        'ISO/IEC 9899:1999 §6.5.3.4 & §7.21.6.3',
        'Compile-time sizeof vs Runtime strlen:\n1. sizeof operator (§6.5.3.4):\n   - Evaluated at compile-time by the compiler frontend.\n   - Applied to array variable char s[], it calculates the full allocated extent: 5 characters + 1 null terminator = 6 bytes.\n2. strlen() library function (§7.21.6.3):\n   - Evaluated at runtime (unless optimized by compiler constant folding).\n   - Scans characters starting at address s until reaching \'\\0\'.\n   - Returns the number of characters preceding the null terminator = 5.\n3. printf outputs \'6 5\'.\n\nExam Trap: If s is declared as char *s = "hello";, sizeof(s) becomes sizeof(char*) (8 bytes on 64-bit, 4 on 32-bit), while strlen(s) remains 5!',
        [
            (1, 5, "Array s allocated on stack: 6 bytes {'h','e','l','l','o','\\0'}.", {'s': 'hello'}, {'stack': [{'name': 's', 'type': 'char[6]', 'addr': '0x1000', 'size': 6, 'val': 'hello\\0'}]}),
            (2, 6, 'sizeof(s) evaluates array type footprint at compile-time -> 6 bytes.', {'sizeof_s': 6}, {'stack': []}),
            (3, 6, "strlen(s) scans characters until '\\0' -> 5 characters.", {'strlen_s': 5}, {'stack': []}),
            (4, 6, "printf formats results: prints '6 5'.", {'stdout': '6 5'}, {'stack': [{'name': 'stdout', 'val': '6 5'}]}),
        ]
    )

    # Q051: sizeof on Pointer to String vs Array -> Key C
    add_q(
        51, 'CAT_STR_LIT', 'Medium', 'sizeof on Pointer to String vs Array',
        'What is the output of the following program on a 64-bit architecture?',
        r"""#include <stdio.h>
int main() {
    char *p = "Hello, world!";
    printf("%zu\n", sizeof(p));
    return 0;
}""",
        5, 'sizeof(p)', 'p is a POINTER, not an array! sizeof(p) returns the size of the pointer itself (8 bytes on 64-bit), NOT the string length or buffer size!',
        [
            ('A', '14', False, "Calculated string length including '\\0' (13 + 1 = 14).", 'sizeof on a pointer variable evaluates sizeof(char*), completely ignoring the pointed-to object.'),
            ('B', '13', False, 'Counted characters like strlen.', 'sizeof does not calculate string length; it checks pointer type width.'),
            ('C', '8', True, 'p is declared as a pointer (char*). On a 64-bit architecture, all memory pointers occupy exactly 8 bytes (64 bits), regardless of what they point to. Therefore, sizeof(p) is 8.', ''),
            ('D', '1', False, 'Thought sizeof returned sizeof(char).', 'p is a pointer (char*), not a single char dereference (*p).')
        ],
        'p is a pointer variable. On a 64-bit system, sizeof(char*) is 8 bytes, regardless of the pointed-to string length.',
        'ISO/IEC 9899:1999 §6.5.3.4',
        'Pointer Size vs Array Size in C:\n1. Type Distinction:\n   - In char *p = "Hello, world!";, p is an object of type char* (pointer to char).\n   - In char arr[] = "Hello, world!";, arr is an object of type char[14] (array of 14 chars).\n2. Architecture & Pointer Width:\n   - On modern 64-bit CPUs (x86-64, AArch64), virtual addresses are 64 bits wide, meaning all object pointers (char*, int*, void*) occupy 8 bytes.\n   - On 32-bit CPUs (x86-32, ARMv7), pointers occupy 4 bytes.\n3. Because p is a pointer, sizeof(p) evaluates at compile-time to sizeof(char*) = 8.\n\nExam Trap: This is a classic exam trick: students count the characters in "Hello, world!" (13 characters) and answer 13 or 14. Always check whether the variable is an array or a pointer!',
        [
            (1, 4, 'Pointer p allocated on stack (8 bytes on 64-bit). Points to string literal in .rodata at 0x00405000.', {'p': '0x00405000'}, {'stack': [{'name': 'p', 'type': 'char*', 'addr': '0x1000', 'size': 8, 'val': '0x00405000', 'pointsTo': '.rodata'}], 'rodata': [{'addr': '0x00405000', 'val': 'Hello, world!\\0'}]}),
            (2, 5, 'sizeof(p) evaluates sizeof(char*) on 64-bit architecture -> 8.', {'sizeof_p': 8}, {'stack': []}),
            (3, 5, 'printf prints 8.', {'stdout': '8'}, {'stack': [{'name': 'stdout', 'val': '8'}]}),
        ]
    )

    # Q052: strncpy Lack of Null-Termination -> Key D
    add_q(
        52, 'CAT_STR_LIT', 'Tricky', 'strncpy Lack of Null-Termination',
        'What is the output of the following program?',
        r"""#include <stdio.h>
#include <string.h>
int main() {
    char dest[6] = "XXXXX";
    strncpy(dest, "abc", 2);
    printf("%s\n", dest);
    return 0;
}""",
        6, 'strncpy(dest, "abc", 2);', "strncpy(dest, src, n) does NOT null-terminate if src length is >= n! It overwrites only 2 bytes ('a','b'), leaving the remaining 'XXX' and '\\0' intact!",
        [
            ('A', 'ab', False, "Assumed strncpy automatically appends a null terminator '\\0'.", "If the copy count n is reached before reading '\\0' from src, strncpy does NOT append a '\\0'."),
            ('B', 'abc', False, 'Thought it copied the entire string.', 'The third argument n is 2, so exactly 2 bytes are copied.'),
            ('C', 'Segmentation Fault', False, 'Thought lack of null terminator crashes printf.', 'dest already had a \'\\0\' at index 5 from "XXXXX", so printf stops safely at dest[5].'),
            ('D', 'abXXX', True, "dest is initialized to {'X','X','X','X','X','\\0'}. strncpy with n=2 copies exactly 2 characters ('a','b') into dest[0] and dest[1] without adding a null terminator. dest becomes {'a','b','X','X','X','\\0'}, printing 'abXXX'.", '')
        ],
        "When src length exceeds n, strncpy does not add a null terminator. It overwrites dest[0..1] with 'ab', leaving 'XXX' and '\\0' behind it.",
        'ISO/IEC 9899:1999 §7.21.2.4',
        'strncpy Pitfall and Mechanics:\n1. ISO C Specification §7.21.2.4:\n   \'The strncpy function copies not more than n characters... from the array pointed to by s2 to the array pointed to by s1. If the array pointed to by s2 is a string that is shorter than n characters, null characters are appended...\'\n2. Crucial Constraint: If src has n or more characters (here strlen("abc") = 3 >= 2), NO null character is written to dest.\n3. Memory State Trace:\n   - Initial dest: {\'X\', \'X\', \'X\', \'X\', \'X\', \'\\0\'} (indices 0..5).\n   - strncpy(dest, "abc", 2) overwrites dest[0]=\'a\' and dest[1]=\'b\'.\n   - dest[2], dest[3], dest[4] remain \'X\'.\n   - dest[5] remains \'\\0\'.\n4. printf("%s\\n", dest) prints characters until \'\\0\', outputting \'abXXX\'.\n\nExam Trap: strncpy was originally designed for fixed-width Unix directory entries, NOT for safe null-terminated string handling! Modern code uses snprintf(dest, sizeof(dest), "%s", src) or strlcpy.',
        [
            (1, 5, "dest initialized on stack: {'X','X','X','X','X','\\0'}.", {'dest': 'XXXXX'}, {'stack': [{'name': 'dest[0]', 'addr': '0x1000', 'val': "'X'"}, {'name': 'dest[1]', 'addr': '0x1001', 'val': "'X'"}, {'name': 'dest[2]', 'addr': '0x1002', 'val': "'X'"}, {'name': 'dest[3]', 'addr': '0x1003', 'val': "'X'"}, {'name': 'dest[4]', 'addr': '0x1004', 'val': "'X'"}, {'name': 'dest[5]', 'addr': '0x1005', 'val': "'\\0'"}]}),
            (2, 6, 'strncpy(dest, "abc", 2): writes dest[0]=\'a\', dest[1]=\'b\'. No null terminator appended.', {'dest': 'abXXX'}, {'stack': [{'name': 'dest[0]', 'val': "'a'"}, {'name': 'dest[1]', 'val': "'b'"}, {'name': 'dest[2]', 'val': "'X'"}, {'name': 'dest[3]', 'val': "'X'"}, {'name': 'dest[4]', 'val': "'X'"}, {'name': 'dest[5]', 'val': "'\\0'"}]}),
            (3, 7, "printf prints null-terminated buffer from 0x1000: 'abXXX'.", {'stdout': 'abXXX'}, {'stack': [{'name': 'stdout', 'val': 'abXXX'}]}),
        ]
    )

    # Q053: String Comparison with == vs strcmp -> Key A
    add_q(
        53, 'CAT_STR_LIT', 'Easy', 'String Comparison with == vs strcmp',
        'What is the output of the following program?',
        r"""#include <stdio.h>
int main() {
    char s1[] = "hello";
    char s2[] = "hello";
    if (s1 == s2) {
        printf("SAME\n");
    } else {
        printf("DIFFERENT\n");
    }
    return 0;
}""",
        6, 's1 == s2', 'Operator == compares POINTER ADDRESSES, not string contents! s1 and s2 are distinct array objects on the stack with different addresses!',
        [
            ('A', 'DIFFERENT', True, 'In C, array names s1 and s2 decay to pointers to their first elements (&s1[0] and &s2[0]). Because s1 and s2 are two distinct stack arrays, they reside at different memory addresses. &s1[0] == &s2[0] is false, so it prints DIFFERENT.', ''),
            ('B', 'SAME', False, 'Assumed == compares string contents (like in Python or Java).', 'In C, == on arrays/pointers compares memory addresses, not string text. To compare contents, use strcmp(s1, s2) == 0.'),
            ('C', 'Compile error', False, 'Thought comparing two arrays with == is illegal syntax.', 'Arrays decay to pointers, making pointer comparison valid C syntax.'),
            ('D', 'Undefined Behavior', False, 'Thought comparing array addresses is undefined.', 'Comparing pointers for equality (==) is well-defined under ISO C §6.5.9.')
        ],
        '== on arrays compares their decayed pointer addresses. s1 and s2 occupy distinct stack allocations, so s1 == s2 is false, printing DIFFERENT.',
        'ISO/IEC 9899:1999 §6.3.2.1#3 & §6.5.9',
        "Array Decay and Equality Semantics:\n1. Array Decay (§6.3.2.1#3):\n   - When an array appears as an operand to an equality operator (==), it decays into a pointer to its initial element (type char*).\n   - s1 decays to &s1[0] (e.g. 0x1000).\n   - s2 decays to &s2[0] (e.g. 0x1006).\n2. Equality Comparison (§6.5.9):\n   - The expression (s1 == s2) compares the two memory addresses: 0x1000 == 0x1006.\n   - Because s1 and s2 are separate local variables with distinct storage, their addresses are never equal.\n   - The expression evaluates to 0 (false).\n3. The else branch executes, printing 'DIFFERENT'.\n\nExam Trap: Never compare strings with == in C! Always use strcmp(s1, s2) == 0 from <string.h>.",
        [
            (1, 4, "char s1[6] allocated on stack at address 0x1000: 'hello\\0'.", {'&s1[0]': '0x1000'}, {'stack': [{'name': 's1', 'addr': '0x1000', 'val': 'hello\\0'}]}),
            (2, 5, "char s2[6] allocated on stack at address 0x1006: 'hello\\0'.", {'&s2[0]': '0x1006'}, {'stack': [{'name': 's1', 'addr': '0x1000', 'val': 'hello\\0'}, {'name': 's2', 'addr': '0x1006', 'val': 'hello\\0'}]}),
            (3, 6, 's1 == s2 compares pointer addresses: 0x1000 == 0x1006 -> 0 (false). Branches to else.', {'condition': 0}, {'stack': []}),
            (4, 9, "printf in else branch executes, printing 'DIFFERENT'.", {'stdout': 'DIFFERENT'}, {'stack': [{'name': 'stdout', 'val': 'DIFFERENT'}]}),
        ]
    )

    # Q054: Subscripting String Literal Directly -> Key B
    add_q(
        54, 'CAT_STR_LIT', 'Medium', 'Subscripting String Literal Directly',
        'What is the output of the following program?',
        r"""#include <stdio.h>
int main() {
    char c = "hello"[1];
    printf("%c\n", c);
    return 0;
}""",
        4, '"hello"[1]', 'A string literal has type char[] and decays to a pointer to its first character! Subscripting "hello"[1] accesses index 1: \'e\'!',
        [
            ('A', 'h', False, 'Thought index 1 references the first character.', "C uses 0-based indexing; index 0 is 'h', index 1 is 'e'."),
            ('B', 'e', True, 'In C, string literal "hello" decays to a char* pointer to its first character. The array subscript E1[E2] is defined as (*((E1) + (E2))). Therefore, "hello"[1] evaluates to *("hello" + 1), which dereferences the second character \'e\'.', ''),
            ('C', 'Compile error', False, 'Thought subscripting a string literal directly is illegal syntax in C.', 'String literals are array expressions; subscripting any array expression is completely valid C.'),
            ('D', 'Segmentation fault', False, 'Thought indexing a literal causes a memory violation.', 'Reading from read-only .rodata is fully permitted; only writing causes a fault.')
        ],
        'String literals decay to char* pointers. "hello"[1] evaluates to *("hello" + 1), cleanly accessing character \'e\'.',
        'ISO/IEC 9899:1999 §6.5.2.1 & §6.4.5',
        'String Literals as Array Expressions:\n1. In C, a string literal is an unnamed array of static storage duration with type char[N] (§6.4.5#5).\n2. Array Subscript Definition (§6.5.2.1#2):\n   \'A postfix expression followed by an expression in square brackets [] is a subscripted designation of an element of an array object... The expression E1[E2] is identical to (*((E1)+(E2)))\'\n3. Trace:\n   - "hello"[1] ==> *("hello" + 1).\n   - "hello" decays to pointer to \'h\' (e.g. 0x00405000).\n   - Adding 1 advances the pointer by sizeof(char) to 0x00405001 (pointing to \'e\').\n   - Dereferencing yields the char value \'e\'.\n   - Assigned to c.\n4. printf("%c\\n", c) outputs \'e\'.\n\nExam Trap: Because E1[E2] == (*((E1)+(E2))) == E2[E1], 1["hello"] is also valid C syntax and yields \'e\'!',
        [
            (1, 4, "Literal 'hello' located in .rodata at 0x00405000: {'h','e','l','l','o','\\0'}.", {'rodata_addr': '0x00405000'}, {'rodata': [{'addr': '0x00405000', 'val': "'h'"}, {'addr': '0x00405001', 'val': "'e'"}, {'addr': '0x00405002', 'val': "'l'"}, {'addr': '0x00405003', 'val': "'l'"}, {'addr': '0x00405004', 'val': "'o'"}, {'addr': '0x00405005', 'val': "'\\0'"}]}),
            (2, 4, 'Subscript "hello"[1] evaluates *("hello" + 1) -> reads byte at 0x00405001 (\'e\'). Stored in c.', {'c': "'e'"}, {'stack': [{'name': 'c', 'type': 'char', 'addr': '0x1000', 'val': "'e'"}]}),
            (3, 5, "printf formats c with %c: prints 'e'.", {'stdout': 'e'}, {'stack': [{'name': 'stdout', 'val': 'e'}]}),
        ]
    )

    # Q055: String Pointer Offset Slicing -> Key C
    add_q(
        55, 'CAT_STR_LIT', 'Easy', 'String Pointer Offset Slicing',
        'What is the output of the following program?',
        r"""#include <stdio.h>
int main() {
    char *s = "examination";
    printf("%s\n", s + 4);
    return 0;
}""",
        5, 's + 4', 'Pointer arithmetic s + 4 advances the start pointer by 4 characters (\'e\',\'x\',\'a\',\'m\'), printing from index 4: "ination"!',
        [
            ('A', 'exam', False, 'Thought s + 4 took the first 4 characters.', 'In C, s + 4 points to the remainder of the string starting at index 4; it does not truncate the suffix.'),
            ('B', 'minaton', False, 'Miscounted characters or misspelled suffix.', 'Index 0: e, 1: x, 2: a, 3: m, 4: i. Remaining is "ination".'),
            ('C', 'ination', True, 'Pointer arithmetic s + 4 advances 4 bytes past \'e\' (index 0), \'x\' (index 1), \'a\' (index 2), and \'m\' (index 3). The pointer passes address &s[4] (pointing to \'i\') to printf("%s"), printing "ination".', ''),
            ('D', 'i', False, 'Confused pointer arithmetic with single character dereference *(s + 4).', "%s expects a char* pointer and prints all characters until '\\0'; %c with *(s+4) would print 'i'.")
        ],
        'Pointer arithmetic s + 4 points to index 4 of "examination". printf("%s") prints from \'i\' to the end: ination.',
        'ISO/IEC 9899:1999 §6.5.6#8 & §7.19.6.1',
        'Pointer Arithmetic and %s String Printing:\n1. Pointer Representation:\n   - s points to base address 0x00405000 of "examination".\n   - Character indexing:\n     Index: 0 1 2 3 4 5 6 7 8 9 10\n     Char:  e x a m i n a t i o n\n2. Pointer Addition (s + 4):\n   - Adds 4 * sizeof(char) = 4 bytes to the base address.\n   - Resulting pointer points to index 4 (\'i\') at address 0x00405004.\n3. printf %s Contract:\n   - printf expects a pointer to char.\n   - It prints every character starting at that address until encountering the null terminator \'\\0\'.\n   - Characters printed: \'i\', \'n\', \'a\', \'t\', \'i\', \'o\', \'n\'.\n4. Output: \'ination\'.',
        [
            (1, 4, "Pointer s initialized to address of 'examination' in .rodata (0x00405000).", {'s': '0x00405000'}, {'stack': [{'name': 's', 'addr': '0x1000', 'val': '0x00405000'}], 'rodata': [{'addr': '0x00405000', 'val': 'examination\\0'}]}),
            (2, 5, "s + 4 advances pointer by 4 bytes to 0x00405004 (pointing to 'i').", {'s_plus_4': '0x00405004'}, {'stack': []}),
            (3, 5, "printf reads string starting from 0x00405004 to '\\0': prints 'ination'.", {'stdout': 'ination'}, {'stack': [{'name': 'stdout', 'val': 'ination'}]}),
        ]
    )

    # Q056: Character Constant Type in C vs C++ -> Key D
    add_q(
        56, 'CAT_STR_LIT', 'Tricky', 'Character Constant Type in C vs C++',
        'What is the output of the following C program on a platform with 32-bit int and 8-bit char?',
        r"""#include <stdio.h>
int main() {
    printf("%zu\n", sizeof('a'));
    return 0;
}""",
        4, "sizeof('a')", "In C, character constants like 'a' have type INT (4 bytes)! In C++, they have type char (1 byte)! This is a classic C vs C++ divergence!",
        [
            ('A', '1', False, 'Thought character constants have type char (1 byte).', "In C++, sizeof('a') is 1 (type char). But in C, character constants have type int, so sizeof('a') is 4."),
            ('B', '2', False, 'Confused with 16-bit wide character wchar_t.', "'a' is an ordinary character constant, not a wide character (L'a')."),
            ('C', 'Compile error', False, 'Thought sizeof on a character literal is invalid.', 'sizeof accepts any valid literal or expression.'),
            ('D', '4', True, "Under ISO C §6.4.4.4#10, an integer character constant has type int. On platforms with 32-bit int, sizeof(int) is 4 bytes. (Contrast with C++, where 'a' has type char and sizeof is 1).", '')
        ],
        "In C, character constants have type int (§6.4.4.4#10). On 32-bit int systems, sizeof('a') is sizeof(int) = 4.",
        'ISO/IEC 9899:1999 §6.4.4.4#10',
        "C vs C++ Fundamental Divergence on Character Literals:\n1. ISO C Standard §6.4.4.4 paragraph 10 states:\n   'An integer character constant has type int.'\n2. Consequently:\n   - In C: 'a' is an int literal with value 97 (ASCII 0x00000061). sizeof('a') == sizeof(int) == 4.\n   - In C++ (ISO/IEC 14882 §2.13.2): character literals have type char, so sizeof('a') == sizeof(char) == 1.\n3. Multi-character constants:\n   - This also explains why C permits multi-character constants like 'abcd', packing up to 4 bytes into an int (implementation-defined order).\n4. printf outputs '4'.\n\nExam Trap: This is one of the most frequently tested C-vs-C++ compatibility questions on university exams.",
        [
            (1, 4, "Character constant 'a' parsed by C compiler frontend: assigned type int with value 97.", {'literal_type': 'int', 'val': 97}, {'registers': [{'reg': 'val', 'val': 97, 'type': 'int'}]}),
            (2, 4, "sizeof('a') evaluates sizeof(int) at compile time -> 4.", {'sizeof_result': 4}, {'stack': []}),
            (3, 4, 'printf prints 4.', {'stdout': '4'}, {'stack': [{'name': 'stdout', 'val': '4'}]}),
        ]
    )

    # Q057: Embedded Null Terminator in String Literal -> Key A
    add_q(
        57, 'CAT_STR_LIT', 'Medium', 'Embedded Null Terminator in String Literal',
        'What is the output of the following program?',
        r"""#include <stdio.h>
#include <string.h>
int main() {
    char s[] = "abc\0def";
    printf("%zu %zu\n", strlen(s), sizeof(s));
    return 0;
}""",
        6, 'strlen(s), sizeof(s)', "strlen stops at the FIRST null byte '\\0' (3 chars)! sizeof counts the ENTIRE array buffer including embedded and trailing nulls (8 bytes)!",
        [
            ('A', '3 8', True, "strlen(s) scans characters until the first '\\0', finding 3 ('a','b','c'). sizeof(s) measures the total allocated array: 'a','b','c','\\0','d','e','f' plus the automatic trailing '\\0' = 8 bytes total.", ''),
            ('B', '6 8', False, 'Thought strlen skips embedded null characters and counts all letters.', "strlen stops immediately upon encountering the first null character ('\\0')."),
            ('C', '3 7', False, "Forgot that C always appends an implicit trailing '\\0' at the end of string literals.", '"abc\\0def" has 7 explicit characters plus 1 implicit trailing \'\\0\' = 8 bytes.'),
            ('D', '7 8', False, 'Confused strlen with non-null character count.', "strlen counts characters up to the first '\\0' only.")
        ],
        "strlen stops at the first '\\0' (3 chars). sizeof counts all 7 explicit bytes plus the implicit trailing '\\0', totaling 8 bytes.",
        'ISO/IEC 9899:1999 §6.4.5#5 & §7.21.6.3',
        'Embedded Null Characters in String Literals:\n1. Literal Parsing (§6.4.5#5):\n   - The literal "abc\\0def" contains the escape sequence \'\\0\'.\n   - Explicit bytes: \'a\' (0x61), \'b\' (0x62), \'c\' (0x63), \'\\0\' (0x00), \'d\' (0x64), \'e\' (0x65), \'f\' (0x66).\n   - In addition, the C compiler appends an implicit null byte at the end of every string literal.\n   - Total bytes in array: 7 + 1 = 8 bytes.\n2. sizeof(s) (§6.5.3.4):\n   - Applied to array s, sizeof evaluates the full array size = 8 bytes.\n3. strlen(s) (§7.21.6.3):\n   - strlen scans sequentially: \'a\' (1), \'b\' (2), \'c\' (3), \'\\0\' (stop!).\n   - Returns 3.\n4. printf outputs \'3 8\'.\n\nExam Trap: Never forget the implicit trailing \'\\0\' appended by the compiler when computing sizeof on string literals with embedded escape nulls.',
        [
            (1, 5, "Array s allocated on stack with 8 bytes: {'a','b','c','\\0','d','e','f','\\0'}.", {'s': 'abc\\0def\\0'}, {'stack': [{'name': 's[0..2]', 'val': "'a','b','c'"}, {'name': 's[3]', 'val': "'\\0' (embedded)"}, {'name': 's[4..6]', 'val': "'d','e','f'"}, {'name': 's[7]', 'val': "'\\0' (trailing)"}]}),
            (2, 6, "strlen(s) reads 'a','b','c' and halts at s[3] ('\\0') -> returns 3.", {'strlen': 3}, {'stack': []}),
            (3, 6, 'sizeof(s) evaluates total array size -> 8 bytes.', {'sizeof': 8}, {'stack': []}),
            (4, 6, "printf prints '3 8'.", {'stdout': '3 8'}, {'stack': [{'name': 'stdout', 'val': '3 8'}]}),
        ]
    )

    # Q058: Reassigning Array Name vs Reassigning Pointer -> Key B
    add_q(
        58, 'CAT_STR_LIT', 'Medium', 'Reassigning Array Name vs Reassigning Pointer',
        'What happens when attempting to compile the following program?',
        r"""#include <stdio.h>
int main() {
    char str[] = "hello";
    str = "world";
    printf("%s\n", str);
    return 0;
}""",
        5, 'str = "world";', 'An array name is NOT a modifiable lvalue! It cannot be reassigned with =; this causes a COMPILATION ERROR!',
        [
            ('A', 'Prints world', False, 'Thought array variables can be reassigned like pointer variables.', 'An array name designates fixed memory allocated on the stack; it is not a modifiable lvalue and cannot be reassigned with =.'),
            ('B', 'Compilation Error: assignment to expression with array type', True, "Under ISO C §6.5.16#1, the left operand of an assignment operator must be a modifiable lvalue. An array type is an lvalue but NOT a modifiable lvalue. GCC emits 'error: assignment to expression with array type'.", ''),
            ('C', 'Prints hello', False, 'Thought the reassignment is ignored at runtime.', 'The compiler rejects the program at compile-time; no binary is produced.'),
            ('D', 'Runtime crash', False, 'Thought it compiles and crashes at runtime.', 'This constraint violation is caught strictly at compile time.')
        ],
        'Array names are non-modifiable lvalues in C. Assigning str = "world" is a constraint violation and causes a Compilation Error.',
        'ISO/IEC 9899:1999 §6.3.2.1#1 & §6.5.16#1',
        'Modifiable Lvalues and Array Immutability:\n1. ISO C Definition of Lvalue (§6.3.2.1#1):\n   - An lvalue is an expression that designates an object.\n   - A \'modifiable lvalue\' is an lvalue that does not have array type, does not have an incomplete type, does not have a const-qualified type...\n2. Assignment Constraint (§6.5.16#1):\n   \'An assignment operator shall have a modifiable lvalue as its left operand.\'\n3. Because char str[] has array type (char[6]), it is an lvalue, but NOT a modifiable lvalue.\n4. When the compiler parses str = "world";, it detects an attempt to assign to an array type.\n5. GCC immediately emits a fatal compilation error:\n   error: assignment to expression with array type\n6. To change the contents of an array, strcpy(str, "world") must be used (provided the array is large enough).\n\nExam Trap: If str had been declared as char *str = "hello";, then str is a pointer variable (a modifiable lvalue), and str = "world"; compiles cleanly!',
        [
            (1, 4, "Array str declared on stack as char[6] initialized with 'hello\\0'. str is an array lvalue.", {'str': 'hello'}, {'stack': [{'name': 'str', 'type': 'char[6]', 'addr': '0x1000', 'val': 'hello\\0'}]}),
            (2, 5, 'Compiler parses str = "world": left operand str has array type -> NOT a modifiable lvalue under §6.5.16#1.', {'compiler_diagnostic': 'error: assignment to expression with array type'}, {'stack': []}),
            (3, 5, 'Compilation halted with exit code 1. No executable generated.', {'status': 'COMPILATION ERROR'}, {'stack': []}),
        ]
    )

    print("bank_part2 loaded (26 questions, total 58).")
