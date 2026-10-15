# syllabus_part1.py
# Q001 - Q016: TOPIC_DATATYPES (Data Types & Variables)
# Q017 - Q034: TOPIC_OPERATORS (Operators & Expressions)

def load_part1(add_q):
    # =========================================================================
    # TOPIC_DATATYPES (Q001 - Q016)
    # =========================================================================

    # Q001: Integer Division Truncation
    add_q(
        1, "TOPIC_DATATYPES", "Easy", "Integer Division vs Floating-Point Result",
        "What is the output of the following program?",
        """#include <stdio.h>
int main() {
    double res = 5 / 2;
    printf("%.1f\\n", res);
    return 0;
}""",
        4, "5 / 2", "Both 5 and 2 are integer literals, so 5 / 2 truncates to integer 2 BEFORE storing in double res!",
        [
            ("A", "2.0", True, "5 / 2 truncates to integer 2, which is then assigned as 2.0 to double.", ""),
            ("B", "2.5", False, "Assumed standard mathematical division.", "In C, dividing two ints performs integer truncation toward zero."),
            ("C", "3.0", False, "Thought it rounded up.", "C integer division truncates fractional parts, never rounds."),
            ("D", "Compile error", False, "Thought int division cannot be stored in double.", "Implicit promotion from int to double is standard C.")
        ],
        "When both operands of / are integers, integer division truncates toward zero. 5 / 2 yields 2, which becomes 2.0.",
        "ISO/IEC 9899 §6.5.5#6",
        "To get 2.5, at least one operand must be a float/double: 5.0 / 2 or (double)5 / 2.",
        [(1, 4, "Integer division 5 / 2 evaluates to integer 2.", {"temp": 2}, None),
         (2, 4, "Integer 2 promoted to double 2.0 and stored in res.", {"res": 2.0}, None),
         (3, 5, "printf prints 2.0.", {"stdout": "2.0"}, None)]
    )

    # Q002: Explicit Casting Order with Division
    add_q(
        2, "TOPIC_DATATYPES", "Medium", "Cast Precedence: (double)(5 / 2)",
        "What is printed by this code?",
        """#include <stdio.h>
int main() {
    double a = (double)(5 / 2);
    double b = (double)5 / 2;
    printf("%.1f %.1f\\n", a, b);
    return 0;
}""",
        4, "(double)(5 / 2)", "Parentheses force (5 / 2) to truncate to 2 first! In (double)5 / 2, 5 is cast to 5.0 first, yielding 2.5!",
        [
            ("A", "2.0 2.5", True, "In 'a', division runs first (2), then casts to 2.0. In 'b', 5 becomes 5.0 first, so 5.0 / 2 = 2.5.", ""),
            ("B", "2.5 2.5", False, "Thought the cast inside 'a' changed the operands.", "The cast applies to the result of the parenthesized expression (5/2)."),
            ("C", "2.0 2.0", False, "Thought 'b' also truncated.", "In 'b', double / int promotes 2 to 2.0."),
            ("D", "2.5 2.0", False, "Inverted the results.", "Check parentheses carefully.")
        ],
        "Parentheses have higher precedence than casting. In (double)(5/2), 5/2 evaluates to 2 first. In (double)5 / 2, the cast applies to 5 first.",
        "ISO/IEC 9899 §6.5.4",
        "Outputs 2.0 2.5.",
        [(1, 4, "(5 / 2) truncates to 2 -> (double)2 is 2.0.", {"a": 2.0}, None),
         (2, 5, "(double)5 evaluates to 5.0 -> 5.0 / 2 is 2.5.", {"b": 2.5}, None)]
    )

    # Q003: Float Literal Precision Trap (0.1f == 0.1)
    add_q(
        3, "TOPIC_DATATYPES", "Tricky", "Float vs Double Literal Precision",
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
        5, "f == 0.1", "Literal 0.1 without a suffix is of type DOUBLE! 0.1 cannot be represented exactly in binary, so float and double roundings differ!",
        [
            ("A", "NOT EQUAL", True, "0.1f (float) and 0.1 (double) have different binary precision roundings, so f == 0.1 is false.", ""),
            ("B", "EQUAL", False, "Assumed 0.1 and 0.1f are identical decimal values.", "Floating point numbers are base-2 binary fractions; 0.1 is an infinite repeating binary fraction."),
            ("C", "Compile error", False, "Thought comparing float and double is a syntax error.", "float promotes to double, but precision bits differ."),
            ("D", "Undefined Behavior", False, "Thought comparison was undefined.", "Comparison is strictly defined by IEEE 754.")
        ],
        "Floating constants without a suffix are double. Float f has 24 bits of mantissa; double literal 0.1 has 53 bits.",
        "ISO/IEC 9899 §6.4.4.2",
        "Prints NOT EQUAL.",
        [(1, 5, "f promoted to double. Binary mantissa bits differ from 0.1 double literal.", None, None),
         (2, 8, "else branch executes: prints NOT EQUAL.", {"stdout": "NOT EQUAL"}, None)]
    )

    # Q004: Character vs String Literal Size
    add_q(
        4, "TOPIC_DATATYPES", "Tricky", "sizeof('A') in C vs C++",
        "In ISO C, what is the value of sizeof('A') on a typical 32-bit/64-bit system?",
        """#include <stdio.h>
int main() {
    printf("%zu\\n", sizeof('A'));
    return 0;
}""",
        4, "sizeof('A')", "In C (unlike C++), character constants like 'A' have type INT! Therefore, sizeof('A') == sizeof(int) == 4!",
        [
            ("A", "4", True, "In C, character constants have type int, so sizeof('A') is 4 bytes.", ""),
            ("B", "1", False, "Confused C with C++. In C++, 'A' is type char (1 byte); in C, it is type int (4 bytes)!", "ISO C §6.4.4.4#10 explicitly defines character constants as type int."),
            ("C", "2", False, "Confused with 16-bit wchar_t.", "'A' is an ASCII character constant."),
            ("D", "Compile error", False, "Thought sizeof cannot be applied to character literals.", "sizeof on any literal is valid C.")
        ],
        "An integer character constant has type int. Accordingly, sizeof('A') equals sizeof(int), typically 4 bytes.",
        "ISO/IEC 9899 §6.4.4.4#10",
        "In contrast, sizeof((char)'A') is 1.",
        [(1, 4, "'A' has type int in C. sizeof(int) = 4.", {"sizeof": 4}, None)]
    )

    # Q005: Character Arithmetic (ASCII Math)
    add_q(
        5, "TOPIC_DATATYPES", "Easy", "Character Arithmetic with ASCII Offsets",
        "What is printed by this program?",
        """#include <stdio.h>
int main() {
    char ch = 'a';
    ch = ch + 3;
    printf("%c %d\\n", ch, ch);
    return 0;
}""",
        5, "ch = ch + 3;", "Characters are small integers! ASCII value of 'a' (97) + 3 = 100, which is character 'd'!",
        [
            ("A", "d 100", True, "'a' + 3 is 'd' (ASCII code 100). %c prints 'd' and %d prints 100.", ""),
            ("B", "a3 97", False, "Thought it concatenated strings.", "C performs numeric arithmetic on char types."),
            ("C", "d d", False, "Thought %d also printed character.", "%d formats as signed integer."),
            ("D", "100 100", False, "Thought %c printed integer.", "%c formats as ASCII character.")
        ],
        "In C, char is an integral type. 'a' has ASCII value 97. 97 + 3 = 100 ('d').",
        "ISO/IEC 9899 §6.2.5",
        "Prints d 100.",
        [(1, 4, "ch = 'a' (97).", {"ch": "a (97)"}, None),
         (2, 5, "ch = 97 + 3 = 100 ('d').", {"ch": "d (100)"}, None),
         (3, 6, "printf prints d 100.", {"stdout": "d 100"}, None)]
    )

    # Q006: Case Conversion Formula
    add_q(
        6, "TOPIC_DATATYPES", "Medium", "Lowercase to Uppercase Conversion Logic",
        "What does the expression ('c' - 'a' + 'A') evaluate to?",
        """#include <stdio.h>
int main() {
    char result = 'c' - 'a' + 'A';
    printf("%c\\n", result);
    return 0;
}""",
        4, "'c' - 'a' + 'A'", "'c' - 'a' yields the 0-indexed alphabet offset (2). Adding 'A' shifts to uppercase 'C'!",
        [
            ("A", "C", True, "'c' - 'a' is 2. 'A' (65) + 2 is 'C' (67).", ""),
            ("B", "c", False, "Thought the formula cancelled out.", "It maps lowercase to uppercase."),
            ("C", "A", False, "Thought offset was discarded.", "Offset 2 is added to 'A'."),
            ("D", "Compile error", False, "Thought subtracting chars is invalid.", "Chars are integers.")
        ],
        "ASCII ensures sequential ordering of letters. 'c' - 'a' is 2. 'A' + 2 is 'C'.",
        "ISO/IEC 9899 §6.2.5",
        "Prints C.",
        [(1, 4, "'c' - 'a' = 2. 'A' + 2 = 'C'.", {"result": "C"}, None)]
    )

    # Q007: Octal Literal Trap (015)
    add_q(
        7, "TOPIC_DATATYPES", "Tricky", "Leading Zero Octal Constant",
        "What is the output of the following program?",
        """#include <stdio.h>
int main() {
    int x = 015;
    printf("%d\\n", x);
    return 0;
}""",
        4, "int x = 015;", "A leading zero specifies an OCTAL (base 8) literal! 015 in octal is (1*8 + 5) = 13 decimal!",
        [
            ("A", "13", True, "015 is octal: 1 * 8^1 + 5 * 8^0 = 13 decimal.", ""),
            ("B", "15", False, "Treated 015 as decimal 15.", "In C, a leading 0 means octal (base 8)."),
            ("C", "0", False, "Thought leading zero reset the value.", "015 is a valid octal literal."),
            ("D", "Compile error", False, "Thought leading zero is a syntax error.", "Leading zero is standard octal syntax.")
        ],
        "An integer constant beginning with 0 is interpreted in octal (base 8). 015 = 13 decimal.",
        "ISO/IEC 9899 §6.4.4.1",
        "Prints 13.",
        [(1, 4, "015 in octal = 1*8 + 5 = 13 decimal.", {"x": 13}, None),
         (2, 5, "printf prints 13.", {"stdout": "13"}, None)]
    )

    # Q008: Hexadecimal Literal (0x1F)
    add_q(
        8, "TOPIC_DATATYPES", "Easy", "Hexadecimal Literal Evaluation",
        "What decimal value is printed by this code?",
        """#include <stdio.h>
int main() {
    int val = 0x1F;
    printf("%d\\n", val);
    return 0;
}""",
        4, "int val = 0x1F;", "Prefix 0x indicates hexadecimal (base 16)! 0x1F = 1*16 + 15 = 31 decimal!",
        [
            ("A", "31", True, "0x1F = 1 * 16^1 + 15 * 16^0 = 31 decimal.", ""),
            ("B", "15", False, "Looked only at 'F'.", "1 is in the 16s place."),
            ("C", "19", False, "Confused F with 9.", "In hex, F = 15."),
            ("D", "0", False, "Random guess.", "Valid hex literal.")
        ],
        "Hex literals start with 0x. F represents 15. (1 * 16) + 15 = 31.",
        "ISO/IEC 9899 §6.4.4.1",
        "Prints 31.",
        [(1, 4, "0x1F = 1*16 + 15 = 31.", {"val": 31}, None)]
    )

    # Q009: Explicit Casting Truncation ((int)3.99)
    add_q(
        9, "TOPIC_DATATYPES", "Easy", "Floating-Point to Integer Cast Truncation",
        "What is the output of the following program?",
        """#include <stdio.h>
int main() {
    int x = (int)3.99;
    printf("%d\\n", x);
    return 0;
}""",
        4, "(int)3.99", "Casting a float/double to int TRUNCATES toward zero, discarding the fractional part! It does NOT round!",
        [
            ("A", "3", True, "Floating-to-integer conversion always truncates toward zero, yielding 3.", ""),
            ("B", "4", False, "Thought (int) rounded to the nearest integer.", "C conversion never rounds automatically; 3.99 truncates to 3."),
            ("C", "3.99", False, "x is an int, cannot store fractional values.", "Fractional part is discarded."),
            ("D", "Compile error", False, "Casting float to int is valid.", "Standard explicit cast.")
        ],
        "Conversion of a float to an integer type discards the fractional portion (truncation toward zero).",
        "ISO/IEC 9899 §6.3.1.4#1",
        "Prints 3.",
        [(1, 4, "3.99 truncated toward zero -> 3.", {"x": 3}, None)]
    )

    # Q010: Const Variable Modification Attempt
    add_q(
        10, "TOPIC_DATATYPES", "Easy", "const Qualifier Immutability",
        "What happens when compiling this code?",
        """#include <stdio.h>
int main() {
    const int MAX = 100;
    MAX = 200;
    printf("%d\\n", MAX);
    return 0;
}""",
        5, "MAX = 200;", "A const variable is read-only! Reassigning a const variable causes a COMPILATION ERROR!",
        [
            ("A", "Compilation Error: assignment of read-only variable", True, "Variables declared with const cannot be modified after initialization.", ""),
            ("B", "Prints 200", False, "Thought const can be overridden.", "const guarantees immutability."),
            ("C", "Prints 100", False, "Thought assignment failed silently.", "The compiler strictly rejects modifying const objects."),
            ("D", "Runtime crash", False, "Fails at compile time.", "Compiler catches this before running.")
        ],
        "The const qualifier specifies that an identifier cannot be assigned to after declaration.",
        "ISO/IEC 9899 §6.7.3",
        "Compiler emits: error: assignment of read-only variable 'MAX'.",
        [(1, 5, "Compiler error: assignment of read-only variable 'MAX'.", None, None)]
    )

    # Q011: Uninitialized Local Variable
    add_q(
        11, "TOPIC_DATATYPES", "Easy", "Uninitialized Automatic Local Variable",
        "What is the initial value of an uninitialized local variable int x; ?",
        """#include <stdio.h>
int main() {
    int x;
    printf("%d\\n", x);
    return 0;
}""",
        4, "int x;", "Local automatic variables are NOT automatically zeroed! They contain indeterminate GARBAGE values from the stack!",
        [
            ("A", "Indeterminate (garbage value from stack memory)", True, "Local variables have indeterminate values until explicitly initialized.", ""),
            ("B", "Always 0", False, "Confused local variables with global/static variables.", "Only global and static variables default to 0."),
            ("C", "NULL", False, "x is an int, not a pointer.", "Scalar int holds garbage bytes."),
            ("D", "Compile error", False, "Uninitialized variables compile (with warning).", "Valid C syntax.")
        ],
        "Automatic storage duration objects without initializers have indeterminate values. Reading them is undefined behavior.",
        "ISO/IEC 9899 §6.7.9#10",
        "Always initialize local variables before use.",
        [(1, 4, "x holds indeterminate stack garbage bits.", None, None)]
    )

    # Q012: Uninitialized Global Variable
    add_q(
        12, "TOPIC_DATATYPES", "Easy", "Uninitialized Global Variable Default",
        "What is the guaranteed default value of an uninitialized global variable in C?",
        """#include <stdio.h>
int global_count;
int main() {
    printf("%d\\n", global_count);
    return 0;
}""",
        3, "int global_count;", "Variables with static storage duration (globals) are GUARANTEED by the C standard to be initialized to ZERO!",
        [
            ("A", "Guaranteed to be 0", True, "Global variables reside in the .bss segment and are automatically initialized to 0.", ""),
            ("B", "Indeterminate garbage value", False, "Confused globals with local automatic variables.", "Automatic locals are garbage, but globals are strictly 0."),
            ("C", "-1", False, "Random guess.", "C specifies zero-initialization."),
            ("D", "Compile error", False, "Globals do not require initializers.", "Valid C syntax.")
        ],
        "Objects with static storage duration not initialized explicitly are initialized to zero.",
        "ISO/IEC 9899 §6.7.9#10",
        "Prints 0.",
        [(1, 2, "global_count zero-initialized in BSS segment.", {"global_count": 0}, None),
         (2, 4, "printf prints 0.", {"stdout": "0"}, None)]
    )

    # Q013: Format Specifier Precision (%.2f)
    add_q(
        13, "TOPIC_DATATYPES", "Easy", "printf Precision Specifier (%.2f)",
        "What is printed by this printf statement?",
        """#include <stdio.h>
int main() {
    float pi = 3.14159;
    printf("%.2f\\n", pi);
    return 0;
}""",
        5, "printf(\"%.2f\\n\", pi);", "%.2f rounds and formats the floating-point number to exactly 2 decimal places (3.14)!",
        [
            ("A", "3.14", True, "%.2f specifies 2 digits after the decimal point, outputting 3.14.", ""),
            ("B", "3.141590", False, "Default %f prints 6 decimal places.", "The .2 modifier overrides default precision."),
            ("C", "3.1", False, "That would be %.1f.", "Precision is 2 digits."),
            ("D", "3", False, "That would be %.0f.", "Prints 2 decimal places.")
        ],
        "The precision modifier .N in %f specifies the number of digits to appear after the decimal-point character.",
        "ISO/IEC 9899 §7.21.6.1",
        "Prints 3.14.",
        [(1, 5, "pi formatted to 2 decimal places: 3.14.", {"stdout": "3.14"}, None)]
    )

    # Q014: scanf Address Operator (&) Omission Trap
    add_q(
        14, "TOPIC_DATATYPES", "Medium", "Omitting & in scanf for Integer",
        "What is the danger of writing: scanf(\"%d\", num); instead of scanf(\"%d\", &num); ?",
        """#include <stdio.h>
int main() {
    int num = 0;
    scanf("%d", num); // Note: missing &
    return 0;
}""",
        5, "scanf(\"%d\", num);", "scanf expects a MEMORY ADDRESS! Passing num (value 0) makes scanf attempt to write to address 0x0, causing a SEGMENTATION FAULT!",
        [
            ("A", "Runtime Crash (Segmentation Fault / Access Violation)", True, "scanf interprets num's value (0) as a memory address and attempts to write to NULL.", ""),
            ("B", "Works normally", False, "num passes its value, not its address.", "scanf requires a pointer (&num) to store input."),
            ("C", "Compilation error", False, "In standard C, format string parameter mismatch is a warning, not a hard error.", "Compiles with warning and crashes at runtime."),
            ("D", "num is assigned 0", False, "Process crashes before completion.", "Memory protection fault.")
        ],
        "scanf requires pointers to variables where input should be stored. Passing an int value causes it to dereference an arbitrary address.",
        "ISO/IEC 9899 §7.21.6.2",
        "Always pass &variable for primitive types in scanf.",
        [(1, 5, "scanf treats value 0 as address 0x0 -> SIGSEGV.", None, None)]
    )

    # Q015: Implicit Promotion in Mixed Arithmetic
    add_q(
        15, "TOPIC_DATATYPES", "Medium", "Implicit Type Promotion in Arithmetic",
        "What is the type and value of (10 / 4.0)?",
        """#include <stdio.h>
int main() {
    printf("%.2f\\n", 10 / 4.0);
    return 0;
}""",
        4, "10 / 4.0", "When combining int (10) and double (4.0), int is implicitly promoted to double (10.0), yielding double 2.50!",
        [
            ("A", "2.50", True, "Usual Arithmetic Conversions promote 10 to 10.0. 10.0 / 4.0 = 2.50.", ""),
            ("B", "2.00", False, "Thought integer truncation occurred.", "Because 4.0 is double, floating-point division is used."),
            ("C", "2", False, "Result is of type double.", "Formatted with %.2f."),
            ("D", "Compile error", False, "Mixed arithmetic is standard in C.", "Implicit promotion is applied.")
        ],
        "Under Usual Arithmetic Conversions, if either operand is double, the other is converted to double.",
        "ISO/IEC 9899 §6.3.1.8",
        "Prints 2.50.",
        [(1, 4, "10 promoted to double 10.0. 10.0 / 4.0 = 2.50.", {"stdout": "2.50"}, None)]
    )

    # Q016: Format Specifier Mismatch (%d with float)
    add_q(
        16, "TOPIC_DATATYPES", "Tricky", "Format Specifier Mismatch (%d on float)",
        "What happens when passing a float to printf using %d?",
        """#include <stdio.h>
int main() {
    float f = 5.0f;
    printf("%d\\n", f);
    return 0;
}""",
        5, "printf(\"%d\\n\", f);", "Format specifier mismatch is UNDEFINED BEHAVIOR! printf blindly reads integer registers/stack bytes, printing garbage!",
        [
            ("A", "Undefined Behavior (Prints garbage value or unexpected number)", True, "%d expects an int, but receives a float/double. printf reads mismatched register bits.", ""),
            ("B", "Prints 5", False, "Thought printf automatically converted float to int.", "printf does not inspect runtime types; it trusts the format string."),
            ("C", "Compile error", False, "Compilers issue a warning, not a hard compile error.", "Valid C syntax."),
            ("D", "Prints 5.0", False, "%d is strictly for decimal integers.", "Format specifier mismatch.")
        ],
        "If an argument to printf is not of the expected type specified by the conversion specifier, behavior is undefined.",
        "ISO/IEC 9899 §7.21.6.1#9",
        "Use %f for float/double.",
        [(1, 5, "Mismatched format specifier: %d reads raw float bits -> UB.", None, None)]
    )

    # =========================================================================
    # TOPIC_OPERATORS (Q017 - Q034)
    # =========================================================================

    # Q017: Prefix vs Postfix Increment
    add_q(
        17, "TOPIC_OPERATORS", "Easy", "Prefix vs Postfix Increment Timing",
        "What is the output of the following program?",
        """#include <stdio.h>
int main() {
    int a = 5, b = 5;
    int x = a++;
    int y = ++b;
    printf("%d %d %d %d\\n", a, b, x, y);
    return 0;
}""",
        5, "int x = a++;", "a++ yields the OLD value (5) for x, then increments a to 6. ++b increments b to 6 FIRST, then yields 6 for y!",
        [
            ("A", "6 6 5 6", True, "Both a and b become 6. x receives old a (5); y receives new b (6).", ""),
            ("B", "6 6 6 6", False, "Thought postfix increment returns the new value.", "Postfix returns value BEFORE increment."),
            ("C", "5 6 5 6", False, "Thought a was not incremented.", "Both a and b are incremented."),
            ("D", "6 6 5 5", False, "Thought ++b returned old value.", "Prefix increments before value is used.")
        ],
        "Postfix ++ yields the value prior to increment. Prefix ++ yields the value after increment.",
        "ISO/IEC 9899 §6.5.2.4 & §6.5.3.1",
        "Prints 6 6 5 6.",
        [(1, 5, "a++ assigns old 5 to x, then a becomes 6.", {"a": 6, "x": 5}, None),
         (2, 6, "++b increments b to 6, then assigns 6 to y.", {"b": 6, "y": 6}, None),
         (3, 7, "printf prints 6 6 5 6.", {"stdout": "6 6 5 6"}, None)]
    )

    # Q018: Increment in Arithmetic Expression
    add_q(
        18, "TOPIC_OPERATORS", "Medium", "Increment in Compound Expression",
        "What is the output of the following program?",
        """#include <stdio.h>
int main() {
    int x = 5;
    int res = x++ + 10;
    printf("%d %d\\n", x, res);
    return 0;
}""",
        5, "x++ + 10", "x++ yields 5 for the addition (5 + 10 = 15), then x increments to 6!",
        [
            ("A", "6 15", True, "res = 5 + 10 = 15. x is incremented to 6.", ""),
            ("B", "6 16", False, "Thought x++ incremented before addition.", "Postfix ++ uses old value in the expression."),
            ("C", "5 15", False, "Thought x was not incremented.", "x is permanently incremented to 6."),
            ("D", "5 16", False, "Incorrect combination.", "Postfix rules apply.")
        ],
        "Postfix ++ has higher precedence, but yields its operand's original value for the addition.",
        "ISO/IEC 9899 §6.5.2.4",
        "Prints 6 15.",
        [(1, 5, "x++ yields 5. res = 5 + 10 = 15. x becomes 6.", {"x": 6, "res": 15}, None),
         (2, 6, "printf prints 6 15.", {"stdout": "6 15"}, None)]
    )

    # Q019: Modulo Arithmetic Rules
    add_q(
        19, "TOPIC_OPERATORS", "Easy", "Integer Modulo Remainder",
        "What is the result of 17 % 5?",
        """#include <stdio.h>
int main() {
    printf("%d\\n", 17 % 5);
    return 0;
}""",
        4, "17 % 5", "17 divided by 5 is 3 with a REMAINDER of 2!",
        [
            ("A", "2", True, "17 = (3 * 5) + 2. Remainder is 2.", ""),
            ("B", "3", False, "That is the quotient (17 / 5), not remainder.", "% gives the remainder."),
            ("C", "3.4", False, "Modulo operates only on integers and yields an integer.", "Remainder is an int."),
            ("D", "1", False, "Arithmetic error.", "17 - 15 = 2.")
        ],
        "% yields the remainder from the division of the first operand by the second.",
        "ISO/IEC 9899 §6.5.5",
        "Prints 2.",
        [(1, 4, "17 % 5 evaluates to 2.", {"stdout": "2"}, None)]
    )

    # Q020: Modulo with Negative Dividend (-17 % 5)
    add_q(
        20, "TOPIC_OPERATORS", "Tricky", "Sign of Modulo Result in C99",
        "What is the output of the following program under standard C99/C11?",
        """#include <stdio.h>
int main() {
    int a = -17 % 5;
    int b = 17 % -5;
    printf("%d %d\\n", a, b);
    return 0;
}""",
        4, "-17 % 5", "In C99+, the sign of the modulo result ALWAYS matches the sign of the dividend (left operand)!",
        [
            ("A", "-2 2", True, "-17 % 5 is -2 (sign of -17). 17 % -5 is 2 (sign of 17).", ""),
            ("B", "3 2", False, "Confused C with Python modulo (which uses floor division).", "C uses truncation toward zero: -17 / 5 = -3, remainder = -2."),
            ("C", "-2 -2", False, "Thought modulo was always negative when any operand is negative.", "Sign depends strictly on left operand."),
            ("D", "2 2", False, "Thought remainder is always positive.", "Negative dividend yields negative remainder.")
        ],
        "C99 §6.5.5#6 states (a/b)*b + a%b = a. Integer division truncates toward zero: -17 / 5 = -3. (-3)*5 + (-2) = -17.",
        "ISO/IEC 9899 §6.5.5#6",
        "Prints -2 2.",
        [(1, 4, "-17 % 5 = -2.", {"a": -2}, None),
         (2, 5, "17 % -5 = 2.", {"b": 2}, None)]
    )

    # Q021: Modulo on Floating-Point Invalid
    add_q(
        21, "TOPIC_OPERATORS", "Easy", "Modulo Operator Operand Type Constraint",
        "What happens when compiling: double r = 5.5 % 2; ?",
        """#include <stdio.h>
int main() {
    double r = 5.5 % 2;
    return 0;
}""",
        4, "5.5 % 2", "In C, the modulo operator (%) REQUIRES integer operands! Using % on float/double is a COMPILATION ERROR!",
        [
            ("A", "Compilation Error: invalid operands to binary %", True, "The % operator requires both operands to have integer types.", ""),
            ("B", "Evaluates to 1.5", False, "Thought % works on floats.", "For floating-point remainder, use fmod() from <math.h>."),
            ("C", "Evaluates to 1", False, "Thought 5.5 truncated to 5.", "Compiler rejects the expression."),
            ("D", "Undefined Behavior", False, "Fails at compile time.", "Constraint violation.")
        ],
        "The operands of the % operator shall have integer type.",
        "ISO/IEC 9899 §6.5.5#2",
        "To compute float remainder, use fmod(5.5, 2).",
        [(1, 4, "Compiler error: invalid operands to binary % (have 'double' and 'int').", None, None)]
    )

    # Q022: Relational Chaining Fallacy (1 < x < 10)
    add_q(
        22, "TOPIC_OPERATORS", "Tricky", "Chained Relational Comparison Fallacy",
        "What is the output of the following program?",
        """#include <stdio.h>
int main() {
    int x = 25;
    if (1 < x < 10) {
        printf("TRUE\\n");
    } else {
        printf("FALSE\\n");
    }
    return 0;
}""",
        5, "1 < x < 10", "Relational operators associate left-to-right! (1 < 25) evaluates to 1, then (1 < 10) evaluates to TRUE!",
        [
            ("A", "TRUE", True, "(1 < 25) evaluates to 1. Then (1 < 10) evaluates to 1 (true).", ""),
            ("B", "FALSE", False, "Thought it tested if x is between 1 and 10 (25 is not < 10).", "C does not support mathematical chained comparisons; use (1 < x && x < 10)."),
            ("C", "Compile error", False, "Valid syntax, but a classic logic trap.", "Chained comparisons compile without error."),
            ("D", "Undefined Behavior", False, "Completely well-defined by associativity.", "Left-to-right evaluation.")
        ],
        "< associates left-to-right. (1 < x) is 1. 1 < 10 is 1 (true).",
        "ISO/IEC 9899 §6.5.8#6",
        "Prints TRUE.",
        [(1, 5, "Left-to-right: 1 < 25 is 1.", {"step1": 1}, None),
         (2, 5, "1 < 10 is 1 (true). Condition passes.", {"condition": 1}, None),
         (3, 6, "printf prints TRUE.", {"stdout": "TRUE"}, None)]
    )

    # Q023: Short-Circuit Logical OR
    add_q(
        23, "TOPIC_OPERATORS", "Tricky", "Short-Circuit with Logical OR (||)",
        "What is the output of the following program?",
        """#include <stdio.h>
int main() {
    int a = 1, b = 5;
    if (a++ || b++) {
        printf("%d %d\\n", a, b);
    }
    return 0;
}""",
        5, "a++ || b++", "Because a++ evaluates to 1 (non-zero/true), logical OR short-circuits: b++ is NEVER evaluated!",
        [
            ("A", "2 5", True, "a becomes 2. Because a++ is true, b++ is skipped, leaving b as 5.", ""),
            ("B", "2 6", False, "Assumed both sides of || always execute.", "Logical OR guarantees right side is skipped if left side is true."),
            ("C", "1 5", False, "Thought a++ did not execute.", "a++ is evaluated first."),
            ("D", "1 6", False, "Incorrect combination.", "Short-circuit prevents b++ from running.")
        ],
        "The || operator guarantees left-to-right evaluation; if the first operand compares unequal to 0, the second operand is not evaluated.",
        "ISO/IEC 9899 §6.5.14#4",
        "Prints 2 5.",
        [(1, 5, "a++ yields 1 (true), increments a to 2.", {"a": 2}, None),
         (2, 5, "Short-circuit: b++ is skipped. b remains 5.", {"b": 5}, None),
         (3, 6, "printf prints 2 5.", {"stdout": "2 5"}, None)]
    )

    # Q024: Short-Circuit Logical AND
    add_q(
        24, "TOPIC_OPERATORS", "Tricky", "Short-Circuit with Logical AND (&&)",
        "What is the output of the following program?",
        """#include <stdio.h>
int main() {
    int a = 0, b = 10;
    if (a && ++b) {
        printf("YES\\n");
    }
    printf("%d %d\\n", a, b);
    return 0;
}""",
        5, "a && ++b", "Because a is 0 (false), logical AND short-circuits: ++b is NEVER evaluated!",
        [
            ("A", "0 10", True, "a is 0, so condition fails immediately. ++b is skipped, leaving b = 10.", ""),
            ("B", "0 11", False, "Assumed ++b ran before the comparison.", "&& evaluates strictly left-to-right and skips right side if left is false."),
            ("C", "YES followed by 0 11", False, "0 && anything is false.", "Body is not entered."),
            ("D", "1 10", False, "a was not modified.", "Prints 0 10.")
        ],
        "The && operator guarantees left-to-right evaluation; if the first operand compares equal to 0, the second operand is not evaluated.",
        "ISO/IEC 9899 §6.5.13#4",
        "Prints 0 10.",
        [(1, 5, "a is 0 (false). Short-circuit: ++b skipped.", {"b": 10}, None),
         (2, 8, "printf prints 0 10.", {"stdout": "0 10"}, None)]
    )

    # Q025: Precedence of && over ||
    add_q(
        25, "TOPIC_OPERATORS", "Tricky", "Precedence of Logical AND over Logical OR",
        "What is the value of res?",
        """#include <stdio.h>
int main() {
    int a = 1, b = 0, c = 1;
    int res = a || b && !c;
    printf("%d\\n", res);
    return 0;
}""",
        5, "a || b && !c", "Precedence: ! binds first, then &&, then ||. Parsed as a || (b && (!c)). Since a is 1, short-circuit returns 1!",
        [
            ("A", "1", True, "Grouped as a || (b && (!c)). Since a is 1, the entire expression evaluates to 1.", ""),
            ("B", "0", False, "Thought it evaluated left-to-right as (a || b) && !c = 1 && 0 = 0.", "&& has higher precedence than ||!"),
            ("C", "Compile error", False, "Valid boolean expression.", "Standard C operator hierarchy."),
            ("D", "-1", False, "Boolean results in C are strictly 0 or 1.", "Cannot be negative.")
        ],
        "&& has higher precedence than ||. The expression groups as a || (b && !c). Because a is 1, || short-circuits to 1.",
        "ISO/IEC 9899 §6.5.13 & §6.5.14",
        "Prints 1.",
        [(1, 5, "Grouped as a || (b && !c). a is 1 -> result is 1.", {"res": 1}, None)]
    )

    # Q026: Ternary Conditional Operator
    add_q(
        26, "TOPIC_OPERATORS", "Easy", "Basic Ternary Conditional Evaluation",
        "What is the output of the following program?",
        """#include <stdio.h>
int main() {
    int x = 10, y = 20;
    int max = (x > y) ? x : y;
    printf("%d\\n", max);
    return 0;
}""",
        5, "(x > y) ? x : y", "x > y (10 > 20) is false, so the expression evaluates to the second branch y (20)!",
        [
            ("A", "20", True, "Condition is false, so y (20) is selected.", ""),
            ("B", "10", False, "That is x, selected only if x > y is true.", "10 is not > 20."),
            ("C", "1", False, "Thought it returned boolean true/false.", "Returns the branch expression value."),
            ("D", "0", False, "Returns selected operand.", "y is 20.")
        ],
        "The conditional operator evaluates the first operand. If false, it evaluates and yields the third operand.",
        "ISO/IEC 9899 §6.5.15",
        "Prints 20.",
        [(1, 5, "10 > 20 is false -> yields y (20).", {"max": 20}, None)]
    )

    # Q027: Chained Ternary Right-Associativity
    add_q(
        27, "TOPIC_OPERATORS", "Medium", "Chained Ternary Associativity",
        "What is the output of the following program?",
        """#include <stdio.h>
int main() {
    int x = 1 ? 2 : 3 ? 4 : 5;
    printf("%d\\n", x);
    return 0;
}""",
        4, "1 ? 2 : 3 ? 4 : 5", "Ternary operator associates RIGHT-TO-LEFT: 1 ? 2 : (3 ? 4 : 5). Since 1 is true, result is 2!",
        [
            ("A", "2", True, "Right-associative grouping: 1 ? 2 : (3 ? 4 : 5). Condition 1 is true, yielding 2.", ""),
            ("B", "4", False, "Thought it grouped left-to-right as (1 ? 2 : 3) ? 4 : 5.", "In C, ?: groups right-to-left."),
            ("C", "5", False, "Selected fallback branch.", "Condition 1 is true."),
            ("D", "Compile error", False, "Chaining ternaries is valid.", "Standard C syntax.")
        ],
        "The conditional operator associates from right to left: a ? b : (c ? d : e).",
        "ISO/IEC 9899 §6.5.15",
        "Prints 2.",
        [(1, 4, "1 is true -> yields 2. Right ternary skipped.", {"x": 2}, None)]
    )

    # Q028: Comma Operator in Parentheses
    add_q(
        28, "TOPIC_OPERATORS", "Easy", "Comma Operator Value Extraction",
        "What is the value of x after execution?",
        """#include <stdio.h>
int main() {
    int x = (10, 20, 30);
    printf("%d\\n", x);
    return 0;
}""",
        4, "(10, 20, 30)", "The comma operator evaluates operands left-to-right and discards them, returning the LAST operand (30)!",
        [
            ("A", "30", True, "The comma operator yields the value of the rightmost expression (30).", ""),
            ("B", "10", False, "Thought it took the first operand.", "Left operands are evaluated and discarded."),
            ("C", "60", False, "Thought it summed the numbers.", "Comma is an operator, not an adder."),
            ("D", "Compile error", False, "Comma expressions are valid.", "Standard C operator.")
        ],
        "The comma operator evaluates left-to-right; the result has the type and value of the right operand.",
        "ISO/IEC 9899 §6.5.17",
        "Prints 30.",
        [(1, 4, "10 evaluated -> 20 evaluated -> 30 returned to x.", {"x": 30}, None)]
    )

    # Q029: Comma Operator vs Assignment Precedence
    add_q(
        29, "TOPIC_OPERATORS", "Tricky", "Comma Operator vs Assignment Precedence",
        "What is the output of the following program?",
        """#include <stdio.h>
int main() {
    int a;
    a = 1, 2, 3;
    printf("%d\\n", a);
    return 0;
}""",
        5, "a = 1, 2, 3;", "Assignment (=) has higher precedence than comma (,). This parses as: (a = 1), 2, 3;",
        [
            ("A", "1", True, "Assignment binds first: a = 1. Then 2 and 3 are evaluated and discarded.", ""),
            ("B", "3", False, "Confused with a = (1, 2, 3). Without parentheses, = binds tighter than comma.", "Parentheses are required to assign the result of a comma expression."),
            ("C", "2", False, "Picked middle operand.", "No operator returns the middle."),
            ("D", "Compile error", False, "Expression statement with comma is valid C.", "Standard compliant.")
        ],
        "= has higher precedence than the comma operator. Parsed as ((a = 1), 2), 3.",
        "ISO/IEC 9899 §6.5.16 & §6.5.17",
        "Prints 1.",
        [(1, 5, "a = 1 executes first. 2 and 3 evaluated and discarded.", {"a": 1}, None)]
    )

    # Q030: Compound Assignment Precedence (x *= 2 + 3)
    add_q(
        30, "TOPIC_OPERATORS", "Tricky", "Compound Assignment Right-Hand Precedence",
        "What is the output of the following program?",
        """#include <stdio.h>
int main() {
    int x = 5;
    x *= 2 + 3;
    printf("%d\\n", x);
    return 0;
}""",
        5, "x *= 2 + 3;", "Compound assignment evaluates the ENTIRE right-hand expression first: x = x * (2 + 3) = 5 * 5 = 25, NOT 13!",
        [
            ("A", "25", True, "Right-hand side evaluates first: 2 + 3 = 5. Then x = 5 * 5 = 25.", ""),
            ("B", "13", False, "Thought x *= 2 executed first (10) + 3 = 13.", "Compound assignment is equivalent to x = x * (expr), with implicit parentheses around the right side!"),
            ("C", "10", False, "Forgot + 3.", "Full expression is evaluated."),
            ("D", "15", False, "Arithmetic mistake.", "5 * 5 = 25.")
        ],
        "E1 op= E2 is equivalent to E1 = E1 op (E2). The right-hand side has implicit parentheses.",
        "ISO/IEC 9899 §6.5.16.2",
        "Prints 25.",
        [(1, 5, "RHS evaluates first: 2 + 3 = 5. x = 5 * 5 = 25.", {"x": 25}, None)]
    )

    # Q031: Bitwise AND (&) vs Logical AND (&&)
    add_q(
        31, "TOPIC_OPERATORS", "Medium", "Bitwise AND vs Logical AND",
        "What is the output of the following program?",
        """#include <stdio.h>
int main() {
    int a = 4, b = 2; // binary: 100 and 010
    int r1 = a && b;
    int r2 = a & b;
    printf("%d %d\\n", r1, r2);
    return 0;
}""",
        6, "int r2 = a & b;", "Logical AND (&&) checks truthiness: both 4 and 2 are non-zero, yielding 1. Bitwise AND (&) compares bits: 100 & 010 = 0!",
        [
            ("A", "1 0", True, "4 && 2 is true (1). 4 & 2 in binary (100 & 010) has no common bits, giving 0.", ""),
            ("B", "1 1", False, "Confused bitwise & with logical &&.", "& computes bitwise intersection."),
            ("C", "0 0", False, "Both 4 and 2 are non-zero, so && is true.", "Logical truthiness check."),
            ("D", "6 0", False, "Confused with bitwise OR (|).", "& is AND.")
        ],
        "&& yields 1 if both operands are non-zero. & computes bitwise conjunction.",
        "ISO/IEC 9899 §6.5.10 & §6.5.13",
        "Prints 1 0.",
        [(1, 5, "4 && 2 evaluates to 1.", {"r1": 1}, None),
         (2, 6, "4 & 2 (100 & 010) evaluates to 0.", {"r2": 0}, None)]
    )

    # Q032: Bitwise Shift vs Addition Precedence
    add_q(
        32, "TOPIC_OPERATORS", "Tricky", "Bitwise Shift vs Addition Precedence",
        "What is the output of the following program?",
        """#include <stdio.h>
int main() {
    int x = 1 << 2 + 3;
    printf("%d\\n", x);
    return 0;
}""",
        4, "1 << 2 + 3", "Addition (+) has higher precedence than bitwise shift (<<)! Evaluates as 1 << (2 + 3) = 1 << 5 = 32!",
        [
            ("A", "32", True, "2 + 3 evaluates first to 5, then 1 << 5 evaluates to 32.", ""),
            ("B", "7", False, "Thought << evaluated first: (1 << 2) + 3 = 4 + 3 = 7.", "Arithmetic operators (+, -) bind tighter than shift operators (<<, >>)!"),
            ("C", "8", False, "Calculated 2^3.", "Shift operator shifts binary bits."),
            ("D", "12", False, "Random calculation error.", "Precedence is explicitly + over <<.")
        ],
        "+ and - have higher precedence than << and >>. Groups as 1 << (2 + 3).",
        "ISO/IEC 9899 §6.5.6 & §6.5.7",
        "Prints 32.",
        [(1, 4, "2 + 3 evaluates to 5. 1 << 5 = 32.", {"x": 32}, None)]
    )

    # Q033: Unary Plus and Minus
    add_q(
        33, "TOPIC_OPERATORS", "Easy", "Unary Minus Operator Inversion",
        "What is the output of the following program?",
        """#include <stdio.h>
int main() {
    int x = -5;
    int y = -x;
    printf("%d %d\\n", x, y);
    return 0;
}""",
        5, "int y = -x;", "Unary minus inverts the sign of x: -(-5) becomes +5!",
        [
            ("A", "-5 5", True, "x is -5. -(-5) evaluates to positive 5.", ""),
            ("B", "-5 -5", False, "Thought -x remained negative.", "Minus of a negative is positive."),
            ("C", "5 5", False, "x itself was not modified.", "Unary minus does not modify operand."),
            ("D", "0 0", False, "Random guess.", "Signs invert.")
        ],
        "The unary - operator yields the negative of its operand.",
        "ISO/IEC 9899 §6.5.3.3",
        "Prints -5 5.",
        [(1, 5, "-(-5) = 5.", {"y": 5}, None)]
    )

    # Q034: Logical NOT Truthiness
    add_q(
        34, "TOPIC_OPERATORS", "Easy", "Logical NOT Operator Behavior",
        "What is the output of the following program?",
        """#include <stdio.h>
int main() {
    int a = 42;
    int b = 0;
    printf("%d %d\\n", !a, !b);
    return 0;
}""",
        5, "printf(\"%d %d\\n\", !a, !b);", "! on any non-zero value yields 0. ! on 0 yields 1!",
        [
            ("A", "0 1", True, "!42 is 0 (false). !0 is 1 (true).", ""),
            ("B", "1 0", False, "Inverted the results.", "! inverts boolean truthiness."),
            ("C", "-42 0", False, "Confused logical NOT (!) with unary minus (-).", "! produces boolean 0 or 1."),
            ("D", "1 1", False, "Thought ! on numbers is always true.", "42 is non-zero, so !42 is 0.")
        ],
        "The ! operator yields 0 if operand is non-zero, and 1 if operand is zero.",
        "ISO/IEC 9899 §6.5.3.3",
        "Prints 0 1.",
        [(1, 5, "!42 evaluates to 0. !0 evaluates to 1.", {"stdout": "0 1"}, None)]
    )

print("syllabus_part1 loaded (34 questions).")
