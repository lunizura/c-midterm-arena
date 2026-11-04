# syllabus_part1.py
# Q001 - Q016: TOPIC_DATATYPES (Data Types & Variables)
# Q017 - Q034: TOPIC_OPERATORS (Operators & Expressions)
# Pedagogically upgraded with balanced keys, verified GCC code, aligned traps,
# in-depth multi-paragraph deep dives, multi-step execution traces with memory snapshots,
# and rigorous distractor rationales.

def load_part1(add_q):
    # =========================================================================
    # TOPIC_DATATYPES (Q001 - Q016)
    # =========================================================================
    # Q001: Integer Division vs Floating-Point Result
    add_q(
        1, 'TOPIC_DATATYPES', 'Easy', 'Integer Division vs Floating-Point Result',
        'What is the output of the following program?',
        '#include <stdio.h>\nint main() {\n    double res = 5 / 2;\n    printf("%.1f\\n", res);\n    return 0;\n}',
        3, '5 / 2', 'Both 5 and 2 are integer literals, so 5 / 2 truncates to integer 2 BEFORE storing in double res!',
        [
            ('A', '2.5', False, "Assumed standard real mathematical division occurred because the variable 'res' is declared as double.", 'In C, the type of the variable receiving the assignment has zero effect on the subexpression evaluation. Because both operands (5 and 2) are of type int, integer division is performed first, truncating the fractional part.'),
            ('B', '3.0', False, 'Thought integer division rounds to the nearest whole integer (rounding up 2.5 to 3).', 'ISO C requires integer division to truncate toward zero (discarding fractional digits entirely), never round to the nearest integer.'),
            ('C', '2.0', True, '5 / 2 truncates to integer 2, which is then implicitly converted to 2.0 upon assignment to double.', ''),
            ('D', 'Compile error', False, 'Thought dividing two integers cannot be assigned to a floating-point variable.', 'C supports implicit numeric promotion. The integer result 2 is seamlessly promoted to double 2.0 by the assignment operator.')
        ],
        'When both operands of / are integers, integer division truncates toward zero. 5 / 2 yields 2, which is converted to 2.0.',
        'ISO/IEC 9899:1999 §6.5.5#6 (Multiplicative operators)',
        "In C, binary operators determine their computation mode strictly from the types of their operands, entirely independent of the surrounding context or the destination variable. Here, both 5 and 2 are integer constants of type int. According to ISO C99 §6.5.5#6, when integers are divided, the result is truncated toward zero, discarding any fractional component. Thus, 5 / 2 evaluates to the integer 2.\n\nOnly after the division operator completes does the assignment operator (=) execute. The integer 2 is implicitly converted to double (2.0) to match the storage type of 'res'. The destination type cannot retroactively change how the right-hand expression was evaluated.\n\nA classic novice trap is assuming that declaring 'double res' forces the entire right-hand expression into floating-point arithmetic. To obtain 2.5, at least one operand must be explicitly a floating-point type, such as 5.0 / 2 or (double)5 / 2.",
        [
            (1, 3, 'Evaluate subexpression 5 / 2: both operands are int, truncating toward zero to integer 2.', {'temp_div': 2}, {'stack': [{'name': 'res', 'type': 'double', 'address': '0x7ffd10', 'value': 'uninitialized'}]}),
            (2, 3, "Implicitly convert integer 2 to double 2.0 and assign into local variable 'res'.", {'res': 2.0}, {'stack': [{'name': 'res', 'type': 'double', 'address': '0x7ffd10', 'value': '2.0'}]}),
            (3, 4, "printf formats 'res' with %.1f specifier, outputting '2.0\\n' to stdout.", {'stdout': '2.0'}, {'stack': [{'name': 'res', 'type': 'double', 'address': '0x7ffd10', 'value': '2.0'}]})
        ]
    )

    # Q002: Cast Precedence: (double)(5 / 2)
    add_q(
        2, 'TOPIC_DATATYPES', 'Medium', 'Cast Precedence: (double)(5 / 2)',
        'What is printed by this code?',
        '#include <stdio.h>\nint main() {\n    double a = (double)(5 / 2);\n    double b = (double)5 / 2;\n    printf("%.1f %.1f\\n", a, b);\n    return 0;\n}',
        3, '(double)(5 / 2)', 'Parentheses force (5 / 2) to truncate to 2 first! In (double)5 / 2, 5 is cast to 5.0 first, yielding 2.5!',
        [
            ('A', '2.0 2.5', True, "In 'a', parentheses force integer division (5/2 = 2) before the cast. In 'b', cast binds to 5 first, giving 5.0 / 2 = 2.5.", ''),
            ('B', '2.5 2.5', False, 'Thought casting (double) distributes inside parentheses to make both operands double.', 'C casts never distribute across parentheses. The parenthesized expression (5 / 2) is evaluated completely as integer division before the cast operator receives its operand.'),
            ('C', '2.0 2.0', False, "Thought the cast in 'b' has lower precedence than division, causing 5 / 2 to truncate first.", "Unary cast operators have higher precedence than binary multiplicative operators (*, /, %). In 'b', (double) binds directly to 5 before the division occurs."),
            ('D', '2.5 2.0', False, 'Inverted the evaluation order between parenthesized cast and prefix cast.', 'Remember that parentheses () override operator precedence; grouping (5 / 2) forces integer truncation first.')
        ],
        'Parentheses have higher precedence than casting. In (double)(5/2), 5/2 evaluates to 2 first. In (double)5 / 2, the cast applies to 5 first.',
        'ISO/IEC 9899:1999 §6.5.4 (Cast operators) & §6.5.1 (Primary expressions)',
        "Operator precedence and associativity strictly govern expression binding in C. Primary expressions enclosed in parentheses '()' have the highest precedence (precedence level 1). Consequently, in '(double)(5 / 2)', the subexpression '(5 / 2)' must be fully resolved first. Since both 5 and 2 are integers, integer truncation yields 2. The cast operator '(double)' then converts 2 to 2.0.\n\nConversely, in '(double)5 / 2', the unary cast operator '(type-name)' has higher precedence (level 2) than the binary division operator '/' (level 3). Thus, the cast binds tightly to 5, converting it to double 5.0. Next, under the Usual Arithmetic Conversions (§6.3.1.8), the second operand 2 is promoted to double 2.0, producing 5.0 / 2.0 = 2.5.\n\nThis contrast is a quintessential midterm examination question designed to test whether students truly understand syntactic binding versus runtime conversion order.",
        [
            (1, 3, "Evaluate inner parentheses (5 / 2) -> integer 2; then cast (double)2 -> 2.0, stored in 'a'.", {'a': 2.0}, {'stack': [{'name': 'a', 'type': 'double', 'address': '0x7ffd10', 'value': '2.0'}, {'name': 'b', 'type': 'double', 'address': '0x7ffd18', 'value': 'uninitialized'}]}),
            (2, 4, "Cast binds to 5: (double)5 -> 5.0; then 5.0 / 2.0 -> 2.5, stored in 'b'.", {'a': 2.0, 'b': 2.5}, {'stack': [{'name': 'a', 'type': 'double', 'address': '0x7ffd10', 'value': '2.0'}, {'name': 'b', 'type': 'double', 'address': '0x7ffd18', 'value': '2.5'}]}),
            (3, 5, "printf outputs '2.0 2.5\\n'.", {'stdout': '2.0 2.5'}, {'stack': [{'name': 'a', 'type': 'double', 'address': '0x7ffd10', 'value': '2.0'}, {'name': 'b', 'type': 'double', 'address': '0x7ffd18', 'value': '2.5'}]})
        ]
    )

    # Q003: Float vs Double Literal Precision
    add_q(
        3, 'TOPIC_DATATYPES', 'Tricky', 'Float vs Double Literal Precision',
        'What is the output of the following program?',
        '#include <stdio.h>\nint main() {\n    float f = 0.1f;\n    if (f == 0.1) {\n        printf("EQUAL\\n");\n    } else {\n        printf("NOT EQUAL\\n");\n    }\n    return 0;\n}',
        4, 'f == 0.1', 'Literal 0.1 without a suffix is of type DOUBLE! 0.1 cannot be represented exactly in binary, so float and double roundings differ!',
        [
            ('A', 'EQUAL', False, 'Assumed 0.1 decimal is identical regardless of whether it is stored in a float or double.', '0.1 is an infinite repeating fraction in base-2 binary (0.0001100110011...). Float stores 24 bits of mantissa, while double stores 53 bits; when float is widened to double, the missing bits are zeroed, which does not match the extra precision bits of the double literal.'),
            ('B', 'NOT EQUAL', True, '0.1f (float) and unsuffixed 0.1 (double) have different binary precision roundings, so f == 0.1 evaluates to false.', ''),
            ('C', 'Compile error', False, 'Thought comparing float with double using == is illegal in C.', "C permits mixed-precision comparisons through Usual Arithmetic Conversions; float 'f' is automatically promoted to double before comparison."),
            ('D', 'Undefined Behavior', False, 'Thought comparing floating-point numbers triggers undefined behavior.', 'Floating-point comparisons are fully defined by IEEE 754 and the C standard; it is merely mathematically inexact due to finite representation.')
        ],
        'Floating constants without a suffix are double. Float f has 24 bits of mantissa; double literal 0.1 has 53 bits.',
        'ISO/IEC 9899:1999 §6.4.4.2 (Floating constants) & §6.3.1.8 (Usual arithmetic conversions)',
        "In C, floating-point literals without a suffix (such as 0.1) have type double by default; only literals ending in 'f' or 'F' (like 0.1f) have type float. Decimal 0.1 cannot be represented exactly as a terminating binary fraction; in binary, it is the repeating pattern 0.0001100110011...\n\nWhen stored in a 32-bit single-precision float (IEEE 754), it has 24 bits of precision (approximately 0.10000000149011612). A 64-bit double literal has 53 bits of precision (approximately 0.10000000000000000555).\n\nWhen evaluating 'f == 0.1', Usual Arithmetic Conversions promote 'f' to double. Widening a float to double simply pads the lower 29 mantissa bits with zeros. Consequently, the promoted float value is not bitwise equal to the double constant 0.1, making the condition false and printing NOT EQUAL.",
        [
            (1, 3, 'Initialize float f = 0.1f (stores single-precision binary approximation ~0.1000000015).', {'f': '0.1f (~0.1000000015)'}, {'stack': [{'name': 'f', 'type': 'float', 'address': '0x7ffd10', 'value': '0.1000000015'}]}),
            (2, 4, 'Compare f (promoted to double with zero-padded bits) with double literal 0.1: bits differ, result 0 (false).', {'condition': 0}, {'stack': [{'name': 'f', 'type': 'float', 'address': '0x7ffd10', 'value': '0.1000000015'}]}),
            (3, 7, "Condition is false; control jumps to else branch, printing 'NOT EQUAL\\n'.", {'stdout': 'NOT EQUAL'}, {'stack': [{'name': 'f', 'type': 'float', 'address': '0x7ffd10', 'value': '0.1000000015'}]})
        ]
    )

    # Q004: sizeof('A') in C vs C++
    add_q(
        4, 'TOPIC_DATATYPES', 'Tricky', "sizeof('A') in C vs C++",
        "In ISO C, what is the value of sizeof('A') on a typical 32-bit/64-bit system?",
        '#include <stdio.h>\nint main() {\n    printf("%zu\\n", sizeof(\'A\'));\n    return 0;\n}',
        3, "sizeof('A')", "In C (unlike C++), character constants like 'A' have type INT! Therefore, sizeof('A') == sizeof(int) == 4!",
        [
            ('A', '1', False, "Confused C with C++. In C++, 'A' has type char (1 byte); but in C, it is strictly type int.", 'ISO C §6.4.4.4#10 explicitly defines an integer character constant as having type int. Only in C++ was this changed to type char.'),
            ('B', '2', False, "Thought 'A' was stored as a 16-bit short or Unicode UTF-16 code point.", 'C character literals represent basic character set values promoted to int, which is 4 bytes on standard ILP32 and LP64 systems.'),
            ('C', '8', False, 'Thought sizeof returned the 64-bit pointer/word size.', 'The operand is an int expression, not a pointer or 64-bit long.'),
            ('D', '4', True, "In C, character constants have type int (not char), so sizeof('A') equals sizeof(int), which is 4 bytes on typical architectures.", '')
        ],
        "An integer character constant in C has type int. Accordingly, sizeof('A') is sizeof(int), which is 4 bytes.",
        'ISO/IEC 9899:1999 §6.4.4.4#10 (Character constants)',
        'One of the most celebrated differences between C and C++ is the type of a character literal. In C, an integer character constant such as \'A\' has type int (ISO C99 §6.4.4.4#10). In C++, by contrast, \'A\' has type char. Because sizeof operator evaluates the storage size of its operand\'s type, in C sizeof(\'A\') is identical to sizeof(int).\n\nOn almost all modern 32-bit and 64-bit architectures (ILP32 and LP64 models), sizeof(int) is 4 bytes. Therefore, printf("%zu\\n", sizeof(\'A\')) prints 4.\n\nStudents frequently fall into this trap because variables declared as \'char c = \'A\';\' have sizeof(c) == 1, leading them to falsely conclude that the literal \'A\' itself must also occupy 1 byte.',
        [
            (1, 3, "Evaluate character literal 'A': by ISO C rules, 'A' has type int with ASCII integer value 65.", {'literal_type': 'int', 'ascii_val': 65}, {'stack': []}),
            (2, 3, "sizeof('A') evaluates at compile time to sizeof(int), which is 4 bytes.", {'sizeof_result': 4}, {'stack': []}),
            (3, 4, "printf prints '4\\n' to stdout using the %zu size_t format specifier.", {'stdout': '4'}, {'stack': []})
        ]
    )

    # Q005: Character Arithmetic with ASCII Offsets
    add_q(
        5, 'TOPIC_DATATYPES', 'Easy', 'Character Arithmetic with ASCII Offsets',
        'What is the output of the following program?',
        '#include <stdio.h>\nint main() {\n    char ch = \'a\';\n    ch = ch + 3;\n    printf("%c\\n", ch);\n    return 0;\n}',
        4, 'ch = ch + 3;', "Characters in C are small integers! 'a' (ASCII 97) + 3 = 100, which is the ASCII code for 'd'!",
        [
            ('A', 'd', True, "In C, char is an integral type. 'a' has ASCII 97. 97 + 3 = 100, which prints as character 'd'.", ''),
            ('B', 'c', False, 'Miscounted the offset as 2 instead of 3.', "'a' + 1 is 'b', 'a' + 2 is 'c', and 'a' + 3 is 'd'."),
            ('C', '100', False, 'Thought %c prints the numerical integer value instead of the character.', "The format specifier %c instructs printf to interpret the integer byte as an ASCII character glyph, printing 'd', whereas %d would print 100."),
            ('D', 'Compile error', False, 'Believed arithmetic operations cannot be performed directly on character variables.', 'In C, char is a first-class integer type that undergoes standard integer promotion during arithmetic operations.')
        ],
        "In C, char is an integral type. 'a' has ASCII value 97. 97 + 3 = 100, which corresponds to 'd'.",
        'ISO/IEC 9899:1999 §6.2.5#3 (Types - integer types)',
        "In C, the char type is simply an integer type small enough to hold any character from the basic execution character set (typically an 8-bit byte). The literal 'a' has the integer value 97 under ASCII encoding.\n\nWhen evaluating 'ch + 3', integer promotions (§6.3.1.1) promote 'ch' to int. The addition yields 97 + 3 = 100 (type int). During assignment back to 'ch', the value 100 is converted to char without loss.\n\nFinally, printf is called with the '%c' conversion specifier. Unlike '%d' which outputs decimal digits, '%c' takes the unsigned char conversion of the argument and writes the corresponding character glyph ('d') to stdout.",
        [
            (1, 3, "Initialize char variable 'ch' with literal 'a' (ASCII integer value 97).", {'ch': "'a' (97)"}, {'stack': [{'name': 'ch', 'type': 'char', 'address': '0x7ffd10', 'value': "'a'"}]}),
            (2, 4, "Promote 'ch' to int, evaluate 97 + 3 = 100, and assign back to 'ch' (ASCII 'd').", {'ch': "'d' (100)"}, {'stack': [{'name': 'ch', 'type': 'char', 'address': '0x7ffd10', 'value': "'d'"}]}),
            (3, 5, "printf format specifier %c prints character glyph 'd\\n'.", {'stdout': 'd'}, {'stack': [{'name': 'ch', 'type': 'char', 'address': '0x7ffd10', 'value': "'d'"}]})
        ]
    )

    # Q006: Lowercase to Uppercase Conversion Logic
    add_q(
        6, 'TOPIC_DATATYPES', 'Medium', 'Lowercase to Uppercase Conversion Logic',
        'What character is printed by this program?',
        '#include <stdio.h>\nint main() {\n    char lower = \'c\';\n    char upper = lower - \'a\' + \'A\';\n    printf("%c\\n", upper);\n    return 0;\n}',
        4, "lower - 'a' + 'A'", "lower - 'a' computes the 0-based index (2), then adding 'A' shifts to uppercase 'C'!",
        [
            ('A', 'c', False, "Thought subtracting 'a' and adding 'A' leaves the lowercase character unchanged.", "'A' (65) and 'a' (97) differ by 32. Subtracting 97 and adding 65 shifts the character value from the lowercase to uppercase ASCII block."),
            ('B', 'C', True, "'c' - 'a' gives the alphabetical offset 2; adding 'A' produces the corresponding uppercase letter 'C'.", ''),
            ('C', 'B', False, 'Made an off-by-one indexing error.', "'c' - 'a' is exactly 2. 'A' + 2 = 'C', not 'B'."),
            ('D', '67', False, 'Thought the arithmetic expression forces numeric printing.', "The format specifier is %c, which prints the character 'C' rather than its ASCII integer code 67.")
        ],
        "ASCII ensures sequential ordering of letters. 'c' - 'a' is 2; 'A' + 2 is 'C'.",
        'ISO/IEC 9899:1999 §5.2.1 (Character sets) & §6.2.5#3',
        "The ASCII character encoding guarantees that lowercase letters ('a' through 'z') and uppercase letters ('A' through 'Z') each form contiguous, sequential numeric ranges. Therefore, subtracting 'a' from any lowercase letter yields its 0-indexed position in the alphabet: 'c' - 'a' evaluates to 99 - 97 = 2.\n\nAdding this offset (2) to the base uppercase character 'A' (65) produces 65 + 2 = 67, which is the exact ASCII code for 'C'. This idiom is the canonical C implementation of the toupper() function without library dependencies.\n\nA common pitfall is attempting to memorize magic constants like 32 instead of understanding relative character offsets. Relative subtraction 'ch - 'a' + 'A'' is clearer, portable across ASCII environments, and immune to sign-inversion bugs.",
        [
            (1, 3, "Initialize char lower = 'c' (ASCII value 99).", {'lower': "'c' (99)"}, {'stack': [{'name': 'lower', 'type': 'char', 'address': '0x7ffd10', 'value': "'c'"}, {'name': 'upper', 'type': 'char', 'address': '0x7ffd11', 'value': 'uninitialized'}]}),
            (2, 4, "Calculate offset: 'c' - 'a' = 2; add 'A' (65) -> 67 ('C'); store into 'upper'.", {'lower': "'c'", 'upper': "'C' (67)"}, {'stack': [{'name': 'lower', 'type': 'char', 'address': '0x7ffd10', 'value': "'c'"}, {'name': 'upper', 'type': 'char', 'address': '0x7ffd11', 'value': "'C'"}]}),
            (3, 5, "printf with %c specifier prints 'C\\n'.", {'stdout': 'C'}, {'stack': [{'name': 'lower', 'type': 'char', 'address': '0x7ffd10', 'value': "'c'"}, {'name': 'upper', 'type': 'char', 'address': '0x7ffd11', 'value': "'C'"}]})
        ]
    )

    # Q007: Leading Zero Octal Constant
    add_q(
        7, 'TOPIC_DATATYPES', 'Tricky', 'Leading Zero Octal Constant',
        'What is the output of the following program?',
        '#include <stdio.h>\nint main() {\n    int x = 015;\n    printf("%d\\n", x);\n    return 0;\n}',
        3, 'int x = 015;', 'In C, an integer literal starting with 0 is OCTAL (base 8)! 015 = 1*8 + 5 = 13 in decimal!',
        [
            ('A', '15', False, 'Read 015 as standard decimal 15, ignoring the leading zero prefix.', "In C syntax, any integer literal beginning with '0' followed by digits is parsed in base-8 octal notation, not decimal."),
            ('B', '015', False, 'Thought printf preserves the leading zero formatting.', 'The format specifier %d formats the stored numeric value in standard decimal representation without leading zeros.'),
            ('C', '13', True, 'A leading 0 denotes an octal literal in C. 015 base 8 equals 1 * 8^1 + 5 * 8^0 = 13 in decimal.', ''),
            ('D', 'Compile error', False, 'Thought leading zeros on integers are illegal syntax.', 'Leading zeros have been valid octal literal syntax in C since its inception (K&R C and ANSI C).')
        ],
        'An integer constant beginning with 0 is interpreted in octal (base 8). 015 in octal is (1 * 8) + 5 = 13 decimal.',
        'ISO/IEC 9899:1999 §6.4.4.1 (Integer constants - octal constants)',
        'In C lexical grammar (§6.4.4.1), an integer constant that begins with the digit \'0\' is defined as an octal constant. Its digits must be between \'0\' and \'7\'. The literal 015 is therefore parsed in base 8: 1 * 8^1 + 5 * 8^0 = 13 in decimal.\n\nWhen passed to printf("%d\\n", x), the \'%d\' format specifier outputs the internal binary integer value formatted as a base-10 decimal string, producing 13.\n\nThis is a notorious source of bugs in real-world C code, particularly when programmers attempt to format numbers with aligned columns (e.g. 001, 002, ..., 010). If a number contains 8 or 9 (like 018), the compiler emits a syntax error because 8 is invalid in octal.',
        [
            (1, 3, "Stack frame allocated for main(); storage for local int 'x' reserved.", {'x': 'uninitialized'}, {'stack': [{'name': 'x', 'type': 'int', 'address': '0x7ffd10', 'value': 'uninitialized'}]}),
            (2, 3, "Parser recognizes leading 0: evaluates octal constant 015 as base-8 integer (1*8 + 5 = 13); assigns to 'x'.", {'x': 13}, {'stack': [{'name': 'x', 'type': 'int', 'address': '0x7ffd10', 'value': '13'}]}),
            (3, 4, "printf formats the integer 13 using decimal specifier %d, printing '13\\n'.", {'stdout': '13'}, {'stack': [{'name': 'x', 'type': 'int', 'address': '0x7ffd10', 'value': '13'}]})
        ]
    )

    # Q008: Hexadecimal Literal Evaluation
    add_q(
        8, 'TOPIC_DATATYPES', 'Easy', 'Hexadecimal Literal Evaluation',
        'What is the output of the following program?',
        '#include <stdio.h>\nint main() {\n    int val = 0x1F;\n    printf("%d\\n", val);\n    return 0;\n}',
        3, 'int val = 0x1F;', 'Prefix 0x indicates hexadecimal (base 16)! 0x1F = 1*16 + 15 = 31 decimal!',
        [
            ('A', '15', False, "Looked only at the hex digit 'F' (which is 15), ignoring the leading digit '1'.", "The hex digit '1' is in the 16s place (16^1), contributing 16 to the total value."),
            ('B', '19', False, "Confused the hexadecimal letter 'F' with decimal 9.", 'In hexadecimal notation, digits extend from A (10) through F (15).'),
            ('C', '16', False, "Forgot to add the units place 'F'.", '1 * 16 = 16, plus F (15) equals 31.'),
            ('D', '31', True, '0x1F is base 16: (1 * 16^1) + (15 * 16^0) = 16 + 15 = 31 decimal.', '')
        ],
        'Hex literals start with 0x. F represents 15. (1 * 16) + 15 = 31.',
        'ISO/IEC 9899:1999 §6.4.4.1 (Integer constants - hexadecimal constants)',
        "In C, hexadecimal constants begin with the prefix '0x' or '0X' (§6.4.4.1). Hexadecimal is base 16, where letters 'a'-'f' or 'A'-'F' represent values 10 through 15.\n\nIn the literal 0x1F, the '1' occupies the 16^1 place and 'F' occupies the 16^0 place:\nValue = (1 * 16) + (15 * 1) = 31.\n\nThe '%d' specifier in printf formats this integer into standard base-10 ASCII digits, outputting 31. Hex literals are widely used in low-level systems programming for bitmasks, memory addresses, and byte manipulation.",
        [
            (1, 3, "Stack frame allocated for main(); storage for local int 'val' reserved.", {'val': 'uninitialized'}, {'stack': [{'name': 'val', 'type': 'int', 'address': '0x7ffd10', 'value': 'uninitialized'}]}),
            (2, 3, "Evaluate hex literal 0x1F: (1 * 16) + 15 = 31 decimal; assign to local variable 'val'.", {'val': 31}, {'stack': [{'name': 'val', 'type': 'int', 'address': '0x7ffd10', 'value': '31'}]}),
            (3, 4, "printf formats decimal integer 31 using %d, printing '31\\n'.", {'stdout': '31'}, {'stack': [{'name': 'val', 'type': 'int', 'address': '0x7ffd10', 'value': '31'}]})
        ]
    )

    # Q009: Floating-Point to Integer Cast Truncation
    add_q(
        9, 'TOPIC_DATATYPES', 'Easy', 'Floating-Point to Integer Cast Truncation',
        'What is the output of the following program?',
        '#include <stdio.h>\nint main() {\n    int x = (int)3.99;\n    printf("%d\\n", x);\n    return 0;\n}',
        3, '(int)3.99', 'Casting a float/double to int TRUNCATES toward zero, discarding the fractional part! It does NOT round!',
        [
            ('A', '4', False, 'Assumed the cast rounds to the nearest whole integer (3.99 -> 4).', 'C language type conversion rules mandate truncation toward zero; rounding is never performed automatically. To round, one must call round() from <math.h>.'),
            ('B', '3', True, 'Converting a real floating-point type to an integer discards the entire fractional part (truncation toward zero), yielding 3.', ''),
            ('C', '3.99', False, 'Thought the int variable retains the fractional value.', 'An int cannot represent non-integer values; fractional bits are permanently stripped upon conversion.'),
            ('D', 'Compile error', False, 'Thought explicit casting from double to int requires a library function.', "Explicit casting '(int)' is a core language feature in C.")
        ],
        'Conversion of a float to an integer type discards the fractional portion (truncation toward zero).',
        'ISO/IEC 9899:1999 §6.3.1.4#1 (Real floating and integer)',
        "Under ISO C99 §6.3.1.4#1, when a finite value of real floating type is converted to an integer type, the fractional part is completely discarded. This operation is defined as truncation toward zero. Thus, positive 3.99 becomes 3, and negative -3.99 becomes -3.\n\nThe CPU achieves this directly via hardware conversion instructions (e.g., CVTTSD2SI in x86-64, where the 'TT' stands for Truncate).\n\nA very common mistake on midterm exams is assuming standard mathematical rounding rules apply. If you need nearest-integer rounding in C, you must explicitly use library functions such as round() or lround() from <math.h>, or manually add 0.5 before casting positive numbers.",
        [
            (1, 3, "Stack frame allocated for main(); storage for local int 'x' reserved.", {'x': 'uninitialized'}, {'stack': [{'name': 'x', 'type': 'int', 'address': '0x7ffd10', 'value': 'uninitialized'}]}),
            (2, 3, "Evaluate double literal 3.99 and apply (int) cast: fractional part .99 is truncated to 3; assign to 'x'.", {'x': 3}, {'stack': [{'name': 'x', 'type': 'int', 'address': '0x7ffd10', 'value': '3'}]}),
            (3, 4, "printf prints '3\\n'.", {'stdout': '3'}, {'stack': [{'name': 'x', 'type': 'int', 'address': '0x7ffd10', 'value': '3'}]})
        ]
    )

    # Q010: const Qualifier Immutability
    add_q(
        10, 'TOPIC_DATATYPES', 'Easy', 'const Qualifier Immutability',
        'What happens when attempting to compile and run this code?',
        '#include <stdio.h>\nint main() {\n    const int MAX = 100;\n    MAX = 200;\n    printf("%d\\n", MAX);\n    return 0;\n}',
        4, 'MAX = 200;', 'MAX is declared with the const qualifier! Modifying a const-qualified object is a constraint violation and causes a compile error!',
        [
            ('A', '100', False, 'Thought the compiler quietly ignores the assignment and preserves 100.', 'C is a strongly typed compiled language; the compiler does not silently ignore illegal assignments—it rejects the program with a diagnostic error.'),
            ('B', '200', False, 'Thought const in C is merely a recommendation and allows reassignment.', 'The const type qualifier strictly enforces read-only access on the lvalue; assigning to a const-qualified type violates §6.5.16.1.'),
            ('C', 'Compilation error', True, 'The const qualifier designates an object whose value cannot be modified through that identifier; assigning to it is a constraint violation.', ''),
            ('D', 'Undefined Behavior at runtime', False, 'Thought it compiles cleanly but crashes during execution.', 'Constraint violations must be diagnosed at compile time by any conforming C compiler.')
        ],
        'The const qualifier specifies that an identifier cannot be assigned to. Modifying it causes a compile-time error.',
        'ISO/IEC 9899:1999 §6.7.3 (Type qualifiers) & §6.5.16.1 (Simple assignment)',
        "The const type qualifier (§6.7.3) declares that an object is non-modifiable through that lvalue. In C grammar, the left operand of an assignment operator must be a 'modifiable lvalue' (§6.5.16). A const-qualified object is an lvalue, but it is explicitly NOT a modifiable lvalue.\n\nAttempting to assign 'MAX = 200;' violates the syntax constraints of simple assignment (§6.5.16.1#1). Section §5.1.1.3 requires any conforming C compiler to produce a diagnostic message (compile-time error) when a constraint is violated. GCC outputs: 'error: assignment of read-only variable MAX'.\n\nExam writers frequently test whether students realize that constness in C is enforced at compile time rather than causing a silent runtime failure or crash.",
        [
            (1, 3, "Compiler allocates read-only automatic variable 'MAX' initialized with constant 100.", {'MAX': 100}, {'stack': [{'name': 'MAX', 'type': 'const int', 'address': '0x7ffd10', 'value': '100'}]}),
            (2, 4, "Assignment expression 'MAX = 200' evaluated: compiler checks if MAX is a modifiable lvalue.", {'check_lvalue': 'MAX is const-qualified'}, {'stack': [{'name': 'MAX', 'type': 'const int', 'address': '0x7ffd10', 'value': '100'}]}),
            (3, 4, "Constraint violation detected (§6.5.16.1): compiler emits fatal error 'assignment of read-only variable MAX'.", {'compiler_error': "assignment of read-only variable 'MAX'"}, {'stack': [{'name': 'MAX', 'type': 'const int', 'address': '0x7ffd10', 'value': '100'}]})
        ]
    )

    # Q011: Uninitialized Automatic Local Variable
    add_q(
        11, 'TOPIC_DATATYPES', 'Easy', 'Uninitialized Automatic Local Variable',
        'What is the output of the following program?',
        '#include <stdio.h>\nint main() {\n    int x;\n    printf("%d\\n", x);\n    return 0;\n}',
        3, 'int x;', 'Local variables with automatic storage duration are NOT initialized by default! x contains indeterminate/garbage memory!',
        [
            ('A', 'Indeterminate / Garbage value', True, 'Automatic local variables without initializers have indeterminate values (whatever leftover bits were on the stack).', ''),
            ('B', '0', False, 'Assumed C automatically zeroes out local variables like Java or C# do.', "Unlike Java, C does not zero-initialize automatic local variables. Doing so would incur runtime overhead, which C leaves to the programmer's discretion."),
            ('C', 'Compile error', False, 'Thought reading an uninitialized variable is rejected by the compiler.', 'Standard C permits uninitialized declarations; modern compilers may issue a warning (e.g. -Wuninitialized), but it is syntactically valid C.'),
            ('D', 'NULL', False, 'Confused primitive integer initialization with pointer nullness.', 'NULL is a pointer constant, not a valid value for an int variable, and uninitialized integers hold arbitrary stack bits.')
        ],
        'Automatic storage duration objects without initializers have indeterminate values (garbage memory).',
        'ISO/IEC 9899:1999 §6.7.8#10 (Initialization of objects)',
        "In C, storage duration dictates how and when memory is initialized (§6.2.4, §6.7.8#10). Variables declared inside a block without the static keyword have automatic storage duration. The C standard explicitly states that if an object with automatic storage duration is not initialized explicitly, its value is indeterminate.\n\nAt the machine level, automatic variables reside on the call stack. Allocating space for 'x' merely decrements the stack pointer (%rsp). The 4 bytes allocated for 'x' contain whatever random bit pattern was left behind by previous function calls or OS operations.\n\nAccessing an indeterminate value of an object that does not have its address taken can even produce undefined behavior or trap representations on architectures with parity checks. Always initialize your local variables!",
        [
            (1, 3, "Stack pointer decremented to allocate 4 bytes for automatic variable 'x'.", {'x': 'indeterminate'}, {'stack': [{'name': 'x', 'type': 'int', 'address': '0x7ffd10', 'value': '0x7f4a2108 (garbage)'}]}),
            (2, 3, 'No initializer provided; memory holds uninitialized stack garbage bytes.', {'x': 'indeterminate'}, {'stack': [{'name': 'x', 'type': 'int', 'address': '0x7ffd10', 'value': '0x7f4a2108 (garbage)'}]}),
            (3, 4, "printf reads indeterminate bits from 'x' and prints unpredictable garbage integer to stdout.", {'stdout': '<garbage integer>'}, {'stack': [{'name': 'x', 'type': 'int', 'address': '0x7ffd10', 'value': '0x7f4a2108 (garbage)'}]})
        ]
    )

    # Q012: Uninitialized Global Variable Default
    add_q(
        12, 'TOPIC_DATATYPES', 'Easy', 'Uninitialized Global Variable Default',
        'What is the output of the following program?',
        '#include <stdio.h>\nint global_count;\nint main() {\n    printf("%d\\n", global_count);\n    return 0;\n}',
        2, 'int global_count;', 'Global variables have static storage duration and are GUARANTEED to be initialized to zero by the runtime!',
        [
            ('A', 'Indeterminate / Garbage value', False, 'Confused global variables with automatic local variables.', 'While local stack variables receive garbage, global variables reside in the .bss segment and are zero-initialized by the executable loader before main() executes.'),
            ('B', 'Compile error', False, 'Thought global variables must have explicit initializers.', 'Uninitialized global variables are valid tentative definitions in C; they default to zero.'),
            ('C', '-1', False, 'Thought default sentinel value is -1.', 'The C standard mandates zero-initialization, never -1.'),
            ('D', '0', True, 'Variables with static storage duration (global or static) without explicit initializers are guaranteed to be initialized to zero (or null pointer).', '')
        ],
        'Objects with static storage duration not initialized explicitly are initialized to zero by default.',
        'ISO/IEC 9899:1999 §6.7.8#10 (Initialization of objects with static storage duration)',
        "Unlike automatic local variables, objects declared at file scope have static storage duration (§6.2.4#3). Their lifetime spans the entire execution of the program.\n\nUnder ISO C99 §6.7.8#10, if an object with static storage duration is not initialized explicitly, it is initialized by default: arithmetic types are initialized to positive zero, pointers are initialized to NULL, and aggregate members are recursively zero-initialized.\n\nIn compiled ELF binaries, uninitialized globals are placed in the '.bss' section (Block Started by Symbol). The operating system loader allocates pages for .bss that are backed by zero-filled memory on launch, guaranteeing zero initialization with zero binary file size overhead.",
        [
            (1, 2, "Global variable 'global_count' allocated in .bss segment by compiler.", {'global_count': 'allocated'}, {'stack': [], 'data_segment': [{'name': 'global_count', 'type': 'int', 'address': '0x601040', 'value': '0'}]}),
            (2, 2, 'Program startup loader zeroes out .bss pages; global_count initialized to 0.', {'global_count': 0}, {'stack': [], 'data_segment': [{'name': 'global_count', 'type': 'int', 'address': '0x601040', 'value': '0'}]}),
            (3, 4, "printf reads static variable global_count and prints guaranteed '0\\n'.", {'stdout': '0'}, {'stack': [], 'data_segment': [{'name': 'global_count', 'type': 'int', 'address': '0x601040', 'value': '0'}]})
        ]
    )

    # Q013: printf Precision Specifier (%.2f)
    add_q(
        13, 'TOPIC_DATATYPES', 'Easy', 'printf Precision Specifier (%.2f)',
        'What is the output of the following program?',
        '#include <stdio.h>\nint main() {\n    double pi = 3.14159;\n    printf("%.2f\\n", pi);\n    return 0;\n}',
        4, 'printf("%.2f\\n", pi);', 'The precision modifier .2 rounds and formats to exactly two decimal places, producing 3.14!',
        [
            ('A', '3.14', True, "The precision modifier '.2' in '%.2f' specifies exactly 2 digits following the decimal point, rounding 3.14159 to 3.14.", ''),
            ('B', '3.14159', False, 'Thought %f prints all digits of the double literal regardless of precision.', 'Without precision specified, %f defaults to 6 decimal places. When .2 is supplied, printf truncates/rounds formatting to exactly 2 digits.'),
            ('C', '3.15', False, 'Thought the third decimal digit (1) rounded the preceding 4 up to 5.', 'The digit immediately following the second decimal place is 1; since 1 < 5, standard rounding rounds down to 3.14.'),
            ('D', '3', False, 'Thought .2 meant a field width of 2, truncating the fractional part.', "In printf syntax, the dot '.' designates precision (decimal places), whereas a number before the dot specifies minimum field width.")
        ],
        'The precision modifier .N in %f specifies the number of digits to appear after the decimal point, rounded appropriately.',
        'ISO/IEC 9899:1999 §7.19.6.1#4 (The fprintf function - precision specifiers)',
        "The printf family of functions uses format specifiers with optional flags, width, and precision components: '%[flags][width][.precision]specifier'.\n\nFor floating-point conversion specifiers ('f', 'F'), the precision specification indicates the exact number of digits to appear after the decimal-point character (ISO C99 §7.19.6.1#4). If the precision is specified as '.2', printf formats the floating-point number to two decimal places, rounding to the nearest representable decimal value.\n\nHere, 'pi = 3.14159'. The first two decimal digits are 1 and 4, followed by 1. Because the following digit (1) is less than 5, the number rounds down to '3.14'.",
        [
            (1, 3, "Initialize double variable 'pi' with value 3.14159.", {'pi': 3.14159}, {'stack': [{'name': 'pi', 'type': 'double', 'address': '0x7ffd10', 'value': '3.14159'}]}),
            (2, 4, "printf parses format specifier '%.2f': targets 2 digits after the decimal point.", {'precision': 2}, {'stack': [{'name': 'pi', 'type': 'double', 'address': '0x7ffd10', 'value': '3.14159'}]}),
            (3, 4, "Rounds 3.14159 to nearest 2 decimal places -> '3.14', printing '3.14\\n'.", {'stdout': '3.14'}, {'stack': [{'name': 'pi', 'type': 'double', 'address': '0x7ffd10', 'value': '3.14159'}]})
        ]
    )

    # Q014: Omitting & in scanf for Integer
    add_q(
        14, 'TOPIC_DATATYPES', 'Medium', 'Omitting & in scanf for Integer',
        'What typically happens when this program is executed?',
        '#include <stdio.h>\nint main() {\n    int num = 0;\n    scanf("%d", num);\n    return 0;\n}',
        4, 'scanf("%d", num);', 'scanf requires the ADDRESS of the variable (&num)! Passing num (value 0) causes scanf to treat 0 as a memory address, causing a Segmentation Fault!',
        [
            ('A', 'The program reads input normally', False, 'Assumed C passes variables by reference automatically.', "C is strictly pass-by-value. Passing 'num' passes the integer copy 0, not a memory reference."),
            ('B', 'Compile error', False, 'Thought the compiler blocks passing an int where a pointer is required.', "Because scanf is a variadic function (using '...'), the compiler historically cannot enforce type safety without non-standard format attribute extensions; it compiles with a warning."),
            ('C', 'Runtime Crash / Segmentation Fault', True, 'scanf expects a pointer (address) to write into; passing the value 0 causes scanf to dereference the NULL address (0x0), triggering a fatal segmentation fault.', ''),
            ('D', 'num is assigned the input value', False, "Thought scanf can determine where 'num' is stored in caller's stack frame.", 'Functions in C have isolated stack frames and cannot access caller variables without receiving explicit pointers.')
        ],
        'scanf requires pointers to variables where input should be stored. Passing an int value causes it to dereference an invalid memory address.',
        'ISO/IEC 9899:1999 §7.19.6.2#12 (The fscanf function - pointer arguments)',
        'C is strictly a call-by-value language (§6.5.2.2). When a function is called, copies of its argument values are pushed onto the call stack or passed in registers. For a function like scanf to modify a variable in the caller\'s stack frame, it must be provided with the memory address of that variable via the address-of operator \'&\' (&num).\n\nIn this snippet, the programmer writes \'scanf("%d", num);\' instead of \'&num\'. The value of \'num\' (0) is passed directly to scanf. Inside scanf, the \'%d\' specifier expects a pointer argument of type \'int *\'.\n\nscanf interprets the passed integer 0 as the memory address 0x0 (the NULL pointer). When scanf attempts to write the parsed input to \'*ptr\' (dereferencing address 0), the Memory Management Unit (MMU) detects an unmapped page access and raises an invalid page fault exception, which the operating system translates into a SIGSEGV (Segmentation Fault / Runtime Crash).',
        [
            (1, 3, "Allocate and initialize local int 'num' = 0 on stack at address 0x7ffd10.", {'num': 0}, {'stack': [{'name': 'num', 'type': 'int', 'address': '0x7ffd10', 'value': '0'}]}),
            (2, 4, 'Call scanf: value 0 is passed to variadic parameter instead of address &num (0x7ffd10).', {'arg_passed': 0}, {'stack': [{'name': 'num', 'type': 'int', 'address': '0x7ffd10', 'value': '0'}]}),
            (3, 4, 'scanf dereferences address 0x0 to store user input -> MMU hardware fault -> SIGSEGV crash.', {'signal': 'SIGSEGV (Segmentation fault)'}, {'stack': [{'name': 'num', 'type': 'int', 'address': '0x7ffd10', 'value': '0'}]})
        ]
    )

    # Q015: Implicit Type Promotion in Arithmetic
    add_q(
        15, 'TOPIC_DATATYPES', 'Medium', 'Implicit Type Promotion in Arithmetic',
        'What is the output of the following program?',
        '#include <stdio.h>\nint main() {\n    double res = 10 / 4.0;\n    printf("%.2f\\n", res);\n    return 0;\n}',
        3, '10 / 4.0', 'Because 4.0 is a double, the integer 10 is promoted to double (10.0) before division, giving exact 2.50!',
        [
            ('A', '2.00', False, 'Thought integer truncation occurred because the first operand 10 is an integer.', 'Integer division occurs ONLY when BOTH operands are integers. If either operand is floating-point, promotion converts the other to floating-point.'),
            ('B', '2.50', True, 'When one operand of a binary operator is double, Usual Arithmetic Conversions promote the other operand to double, performing floating-point division.', ''),
            ('C', '2', False, 'Thought %f formats without decimals when the answer has zero trailing decimals.', "The format string '%.2f' strictly prints two decimal places, producing '2.50'."),
            ('D', 'Compile error', False, 'Thought mixing int and double in division is a type mismatch error.', 'C inherently permits mixed arithmetic through its Usual Arithmetic Conversions rule.')
        ],
        'Under Usual Arithmetic Conversions, if either operand is double, the other is converted to double. 10 / 4.0 = 2.5.',
        'ISO/IEC 9899:1999 §6.3.1.8 (Usual arithmetic conversions)',
        "The C standard establishes a systematic hierarchy of type conversions for binary operators known as the 'Usual Arithmetic Conversions' (ISO C99 §6.3.1.8). The purpose of these conversions is to determine a common real type for the operands and result.\n\nThe hierarchy states:\n1. If either operand has type long double, the other is converted to long double.\n2. Otherwise, if either operand has type double, the other is converted to double.\n3. Otherwise, if either operand has type float, the other is converted to float.\n4. Otherwise, integer promotions are performed on both operands.\n\nIn the expression '10 / 4.0', 10 has type int and 4.0 has type double. By rule 2, the integer 10 is promoted to double 10.0. The division is performed using 64-bit floating-point division instructions (e.g. DIVSD in x86), yielding double 2.50, which prints as 2.50.",
        [
            (1, 3, 'Usual Arithmetic Conversions detect double operand 4.0; promote int operand 10 to double 10.0.', {'operand1': 10.0, 'operand2': 4.0}, {'stack': [{'name': 'res', 'type': 'double', 'address': '0x7ffd10', 'value': 'uninitialized'}]}),
            (2, 3, "Perform floating-point division 10.0 / 4.0 = 2.5; assign 2.5 to 'res'.", {'res': 2.5}, {'stack': [{'name': 'res', 'type': 'double', 'address': '0x7ffd10', 'value': '2.5'}]}),
            (3, 4, "printf formats 2.5 with %.2f specifier, printing '2.50\\n'.", {'stdout': '2.50'}, {'stack': [{'name': 'res', 'type': 'double', 'address': '0x7ffd10', 'value': '2.5'}]})
        ]
    )

    # Q016: Format Specifier Mismatch (%d on float)
    add_q(
        16, 'TOPIC_DATATYPES', 'Tricky', 'Format Specifier Mismatch (%d on float)',
        'What happens when executing this code on a standard architecture?',
        '#include <stdio.h>\nint main() {\n    float f = 5.5f;\n    printf("%d\\n", f);\n    return 0;\n}',
        4, 'printf("%d\\n", f);', 'Format specifier %d expects an int, but receives a promoted double! Mismatch causes undefined behavior and prints garbage or 0!',
        [
            ('A', '5', False, 'Thought printf automatically casts floating-point arguments to int.', 'printf is a variadic function that cannot perform semantic type conversions based on format strings; it reads raw bits from ABI registers.'),
            ('B', '5.5', False, 'Thought %d would detect the float and display it as 5.5.', '%d strictly expects an int; it has no mechanism to dynamically rewrite its formatting logic.'),
            ('C', 'Compile error', False, 'Thought the compiler halts compilation when a format mismatch occurs.', 'In standard C, format mismatches in variadic functions are not syntax errors, although modern compilers may emit warnings like -Wformat.'),
            ('D', 'Undefined behavior (prints garbage or incorrect integer)', True, 'Passing a floating-point argument to %d violates the format contract, causing undefined behavior due to ABI register calling convention mismatch.', '')
        ],
        'If an argument to printf is not of the expected type specified by the conversion specifier, the behavior is undefined.',
        'ISO/IEC 9899:1999 §7.19.6.1#9 (The fprintf function - undefined behavior on type mismatch)',
        "Section §7.19.6.1#9 of the ISO C standard explicitly states: 'If any argument is not the correct type for the corresponding conversion specification, the behavior is undefined.'\n\nTo understand why this produces garbage at the hardware level, consider modern calling conventions (such as System V AMD64 ABI or Microsoft x64). In variadic function calls, default argument promotions (§6.5.2.2#6) promote float 'f' to double.\n\nFloating-point arguments (float/double) are placed in XMM registers (e.g. %xmm0). However, the '%d' conversion specifier instructs printf to read an integer from an integer register (e.g. %esi or %edx on Linux, %rdx on Windows). Because no integer argument was passed, printf reads whatever leftover garbage bits happen to reside in that integer register!",
        [
            (1, 3, 'Initialize float f = 5.5f in local stack frame.', {'f': 5.5}, {'stack': [{'name': 'f', 'type': 'float', 'address': '0x7ffd10', 'value': '5.5f'}]}),
            (2, 4, 'Variadic call promotion: float 5.5f promoted to double and loaded into XMM floating-point register.', {'xmm0': 5.5}, {'stack': [{'name': 'f', 'type': 'float', 'address': '0x7ffd10', 'value': '5.5f'}]}),
            (3, 4, 'printf reads %d from integer register (%rsi/edx) instead of XMM: prints garbage value (Undefined Behavior).', {'stdout': '<unpredictable garbage integer>'}, {'stack': [{'name': 'f', 'type': 'float', 'address': '0x7ffd10', 'value': '5.5f'}]})
        ]
    )

    # =========================================================================
    # TOPIC_OPERATORS (Q017 - Q034)
    # =========================================================================
    # Q017: Prefix vs Postfix Increment Timing
    add_q(
        17, 'TOPIC_OPERATORS', 'Easy', 'Prefix vs Postfix Increment Timing',
        'What is the output of the following program?',
        '#include <stdio.h>\nint main() {\n    int a = 5, b = 5;\n    int x = a++;\n    int y = ++b;\n    printf("%d %d\\n", x, y);\n    return 0;\n}',
        4, 'int x = a++;', 'Postfix a++ yields the ORIGINAL value (5) before incrementing, while prefix ++b increments FIRST and yields the new value (6)!',
        [
            ('A', '5 5', False, 'Thought prefix ++b also evaluates to the old value before incrementing.', 'Prefix ++ increments the operand first, and the resulting expression value is the new incremented value (6).'),
            ('B', '5 6', True, 'Postfix a++ yields the value prior to increment (5), while prefix ++b increments b first and yields the new value (6).', ''),
            ('C', '6 6', False, 'Thought postfix a++ increments before yielding its value.', 'Postfix ++ evaluates to the current value of the operand before the side effect of incrementing occurs; x receives 5.'),
            ('D', '6 5', False, 'Inverted the mechanics of postfix and prefix operators.', 'Remember: postfix (a++) evaluates old then increments; prefix (++b) increments then evaluates new.')
        ],
        'Postfix ++ yields the value prior to increment. Prefix ++ yields the value after increment.',
        'ISO/IEC 9899:1999 §6.5.2.4 (Postfix increment) & §6.5.3.1 (Prefix increment)',
        "The distinction between postfix and prefix increment operators lies in the value produced by the expression versus the timing of the side effect. Under ISO C99 §6.5.2.4, the result of the postfix ++ operator is the value of the operand before incrementing; after the result is obtained, the value of the operand is incremented.\n\nConversely, under §6.5.3.1, the prefix ++ operator increments the value of the operand first, and the value of the expression is the new incremented value.\n\nIn this code, 'x = a++;' evaluates to 5, which is assigned to 'x', and 'a' is then updated to 6. Next, 'y = ++b;' increments 'b' to 6 first, and evaluates to 6, which is assigned to 'y'. Thus, 'x' is 5 and 'y' is 6.",
        [
            (1, 3, "Initialize local variables: a = 5, b = 5 in main's stack frame.", {'a': 5, 'b': 5}, {'stack': [{'name': 'a', 'type': 'int', 'address': '0x7ffd10', 'value': '5'}, {'name': 'b', 'type': 'int', 'address': '0x7ffd14', 'value': '5'}]}),
            (2, 4, 'Evaluate postfix a++: yields 5 (stored in x), then side effect increments a from 5 to 6.', {'a': 6, 'b': 5, 'x': 5}, {'stack': [{'name': 'a', 'type': 'int', 'address': '0x7ffd10', 'value': '6'}, {'name': 'b', 'type': 'int', 'address': '0x7ffd14', 'value': '5'}, {'name': 'x', 'type': 'int', 'address': '0x7ffd18', 'value': '5'}]}),
            (3, 5, 'Evaluate prefix ++b: increments b from 5 to 6 first, then yields 6 (stored in y).', {'a': 6, 'b': 6, 'x': 5, 'y': 6}, {'stack': [{'name': 'a', 'type': 'int', 'address': '0x7ffd10', 'value': '6'}, {'name': 'b', 'type': 'int', 'address': '0x7ffd14', 'value': '6'}, {'name': 'x', 'type': 'int', 'address': '0x7ffd18', 'value': '5'}, {'name': 'y', 'type': 'int', 'address': '0x7ffd1c', 'value': '6'}]}),
            (4, 6, "printf formats and prints '5 6\\n'.", {'stdout': '5 6'}, {'stack': [{'name': 'a', 'type': 'int', 'address': '0x7ffd10', 'value': '6'}, {'name': 'b', 'type': 'int', 'address': '0x7ffd14', 'value': '6'}, {'name': 'x', 'type': 'int', 'address': '0x7ffd18', 'value': '5'}, {'name': 'y', 'type': 'int', 'address': '0x7ffd1c', 'value': '6'}]})
        ]
    )

    # Q018: Increment in Compound Expression
    add_q(
        18, 'TOPIC_OPERATORS', 'Medium', 'Increment in Compound Expression',
        'What is the output of the following program?',
        '#include <stdio.h>\nint main() {\n    int x = 5;\n    int y = x++ + 10;\n    printf("%d %d\\n", y, x);\n    return 0;\n}',
        4, 'x++ + 10', 'x++ evaluates to the old value 5 for the addition: 5 + 10 = 15! Afterwards x becomes 6!',
        [
            ('A', '15 6', True, 'x++ evaluates to 5 in the addition (5 + 10 = 15 assigned to y), and the side effect updates x to 6.', ''),
            ('B', '16 6', False, 'Assumed x was incremented before being used in the addition (6 + 10 = 16).', 'Postfix ++ has higher precedence than +, but the value yielded by postfix ++ is the unincremented operand (5).'),
            ('C', '15 5', False, 'Thought x was not incremented or the side effect was discarded.', 'The side effect of ++ is guaranteed to take effect before the sequence point at the end of the full expression statement (;).'),
            ('D', '16 5', False, 'Thought x was incremented for the calculation but reverted back.', 'Variables do not revert; x permanently holds 6 after the expression completes.')
        ],
        "Postfix ++ yields its operand's old value for surrounding operations, then increments the operand.",
        'ISO/IEC 9899:1999 §6.5.2.4 (Postfix increment) & §6.5 (Expressions)',
        "In C expression evaluation, precedence governs which operands bind to which operators, but it does NOT alter the value that an operator produces. The postfix '++' operator binds tighter to 'x' than binary '+' does, so the expression parses as '(x++) + 10'.\n\nHowever, the semantic definition of postfix '++' (§6.5.2.4) dictates that the value of '(x++)' is 5 (the value of 'x' before incrementing). This value 5 is then added to 10, producing 15, which is stored in 'y'.\n\nAt the sequence point at the end of the full expression (the semicolon on line 4), the side effect of incrementing 'x' is fully applied, leaving 'x' with the value 6. Printing 'y' then 'x' yields '15 6'.",
        [
            (1, 3, 'Initialize int x = 5 on the stack.', {'x': 5}, {'stack': [{'name': 'x', 'type': 'int', 'address': '0x7ffd10', 'value': '5'}]}),
            (2, 4, 'Evaluate (x++) + 10: x++ yields 5 -> 5 + 10 = 15; x increments to 6; y assigned 15.', {'x': 6, 'y': 15}, {'stack': [{'name': 'x', 'type': 'int', 'address': '0x7ffd10', 'value': '6'}, {'name': 'y', 'type': 'int', 'address': '0x7ffd14', 'value': '15'}]}),
            (3, 5, "printf outputs '15 6\\n'.", {'stdout': '15 6'}, {'stack': [{'name': 'x', 'type': 'int', 'address': '0x7ffd10', 'value': '6'}, {'name': 'y', 'type': 'int', 'address': '0x7ffd14', 'value': '15'}]})
        ]
    )

    # Q019: Integer Modulo Remainder
    add_q(
        19, 'TOPIC_OPERATORS', 'Easy', 'Integer Modulo Remainder',
        'What is the output of the following program?',
        '#include <stdio.h>\nint main() {\n    int r = 17 % 5;\n    printf("%d\\n", r);\n    return 0;\n}',
        3, '17 % 5', 'The modulo operator % returns the integer remainder of division: 17 = 3*5 + 2, so the remainder is 2!',
        [
            ('A', '3', False, 'Confused the modulo remainder with the integer division quotient.', '17 / 5 yields the quotient 3, whereas 17 % 5 yields the remainder 2.'),
            ('B', '3.4', False, 'Thought % returned the fractional floating-point division result.', 'Modulo operator % only operates on integers and returns an integer remainder.'),
            ('C', '2', True, '17 divided by 5 equals 3 with a remainder of 2. The % operator yields the remainder 2.', ''),
            ('D', '1', False, 'Made an arithmetic subtraction error.', '5 * 3 = 15; 17 - 15 = 2, not 1.')
        ],
        '% yields the remainder from the division of the first operand by the second: 17 % 5 = 2.',
        'ISO/IEC 9899:1999 §6.5.5#5 (Multiplicative operators - remainder)',
        "The binary '%' operator produces the remainder from the division of the first operand by the second operand (ISO C99 §6.5.5#5). Both operands must have integer types.\n\nThe algebraic relationship enforced by the standard is:\n(a / b) * b + (a % b) == a\nFor positive numbers, integer division truncates toward zero: 17 / 5 = 3. Substituting into the formula:\n(3 * 5) + (17 % 5) = 17 ==> 15 + (17 % 5) = 17 ==> 17 % 5 = 2.\n\nModulo is ubiquitous in programming for bounds wrapping, circular queues, hashing, and determining even/odd divisibility.",
        [
            (1, 3, 'Integer division computes quotient: 17 / 5 = 3.', {'quotient': 3}, {'stack': [{'name': 'r', 'type': 'int', 'address': '0x7ffd10', 'value': 'uninitialized'}]}),
            (2, 3, "Remainder computed: 17 - (3 * 5) = 17 - 15 = 2; assign 2 to 'r'.", {'r': 2}, {'stack': [{'name': 'r', 'type': 'int', 'address': '0x7ffd10', 'value': '2'}]}),
            (3, 4, "printf prints '2\\n'.", {'stdout': '2'}, {'stack': [{'name': 'r', 'type': 'int', 'address': '0x7ffd10', 'value': '2'}]})
        ]
    )

    # Q020: Sign of Modulo Result in C99
    add_q(
        20, 'TOPIC_OPERATORS', 'Tricky', 'Sign of Modulo Result in C99',
        'In standard C99/C11, what is the output of the following program?',
        '#include <stdio.h>\nint main() {\n    int r = -17 % 5;\n    printf("%d\\n", r);\n    return 0;\n}',
        3, '-17 % 5', 'In C99, integer division truncates toward zero (-17 / 5 = -3), which forces the remainder to take the sign of the numerator: -2!',
        [
            ('A', '3', False, 'Assumed mathematical modulo where the remainder is always strictly non-negative in [0, b-1].', 'In Python or discrete math, remainder is defined as non-negative (3). But in C99, modulo preserves the sign of the dividend (-2).'),
            ('B', '2', False, 'Thought the negative sign was discarded (taking absolute value).', 'C99 §6.5.5#6 strictly mandates that (a/b)*b + a%b = a. (-3)*5 + a%b = -17 requires a%b = -2.'),
            ('C', '-3', False, 'Confused quotient with remainder.', '-3 is the truncated quotient (-17 / 5), not the remainder.'),
            ('D', '-2', True, "In C99, the sign of the remainder a % b is guaranteed to match the sign of the dividend 'a'. Since a is -17, the remainder is -2.", '')
        ],
        'C99 §6.5.5#6 states (a/b)*b + a%b = a. Integer division truncates toward zero (-3), so -17 % 5 = -2.',
        'ISO/IEC 9899:1999 §6.5.5#6 (Multiplicative operators - algebraic quotient relation)',
        "Prior to C99, C89 permitted compiler implementations to truncate negative quotients toward negative infinity or toward zero, making the sign of modulo implementation-defined.\n\nC99 eliminated this ambiguity in §6.5.5#6: integer division MUST truncate toward zero.\nFor a = -17, b = 5:\n-17 / 5 truncates toward zero to -3.\nBy the mandatory invariant (a / b) * b + (a % b) == a:\n(-3 * 5) + (a % b) = -17\n-15 + (a % b) = -17\na % b = -2.\n\nRule to remember: In C99 and C11, 'a % b' always takes the sign of 'a' (the dividend/numerator), regardless of the sign of 'b'.",
        [
            (1, 3, 'Compute -17 / 5 = -3 (truncate toward zero).', {'quotient': -3}, {'stack': [{'name': 'r', 'type': 'int', 'address': '0x7ffd10', 'value': 'uninitialized'}]}),
            (2, 3, "Compute remainder: -17 - (-3 * 5) = -17 - (-15) = -2; store in 'r'.", {'r': -2}, {'stack': [{'name': 'r', 'type': 'int', 'address': '0x7ffd10', 'value': '-2'}]}),
            (3, 4, "printf prints '-2\\n'.", {'stdout': '-2'}, {'stack': [{'name': 'r', 'type': 'int', 'address': '0x7ffd10', 'value': '-2'}]})
        ]
    )

    # Q021: Modulo Operator Operand Type Constraint
    add_q(
        21, 'TOPIC_OPERATORS', 'Easy', 'Modulo Operator Operand Type Constraint',
        'What happens when attempting to compile this program?',
        '#include <stdio.h>\nint main() {\n    double r = 5.5 % 2;\n    printf("%.1f\\n", r);\n    return 0;\n}',
        3, '5.5 % 2', 'The modulo operator % requires BOTH operands to be integers! Using % on float/double is a syntax error!',
        [
            ('A', 'Compilation error', True, 'The modulo operator % requires operands of integer type. Using % with floating-point 5.5 is a constraint violation.', ''),
            ('B', '1.5', False, 'Thought C allows modulo on floating-point numbers directly with %.', 'The % operator is strictly forbidden on floating types in C. To compute floating-point remainder, one must use fmod() from <math.h>.'),
            ('C', '1.0', False, 'Thought 5.5 was truncated to 5 before modulo (5 % 2 = 1.0).', 'The compiler does not implicitly cast operands to make an illegal operator valid; it rejects the syntax directly.'),
            ('D', 'Undefined behavior', False, 'Thought it compiles but produces erratic runtime results.', 'Constraint violations must be caught at compile time by the compiler, not at runtime.')
        ],
        'The operands of the % operator shall have integer type. 5.5 % 2 is a compile-time constraint violation.',
        'ISO/IEC 9899:1999 §6.5.5#2 (Multiplicative operators - constraints)',
        "ISO C99 §6.5.5#2 states under Constraints: 'Each of the operands shall have arithmetic type. The operands of the % operator shall have integer type.'\n\nIn the expression '5.5 % 2', the left operand is a double constant. Because double is not an integer type, this directly violates a syntactic language constraint. By §5.1.1.3, the compiler is obligated to issue a diagnostic error and halt. GCC reports: 'error: invalid operands to binary % (have double and int)'.\n\nTo perform remainder operations on floating-point values in C, the programmer must include <math.h> and call 'fmod(5.5, 2.0)' or 'remainder(5.5, 2.0)'.",
        [
            (1, 3, "Compiler encounters binary modulo operator '%'.", {'operator': '%'}, {'stack': []}),
            (2, 3, 'Check operand types: left operand is 5.5 (double), right operand is 2 (int).', {'left_type': 'double', 'right_type': 'int'}, {'stack': []}),
            (3, 3, 'Constraint violation (§6.5.5#2): % requires integer types; compiler halts with diagnostic error.', {'compiler_error': 'invalid operands to binary %'}, {'stack': []})
        ]
    )

    # Q022: Chained Relational Comparison Fallacy
    add_q(
        22, 'TOPIC_OPERATORS', 'Tricky', 'Chained Relational Comparison Fallacy',
        'What is the output of the following program?',
        '#include <stdio.h>\nint main() {\n    int x = 25;\n    if (1 < x < 10) {\n        printf("TRUE\\n");\n    } else {\n        printf("FALSE\\n");\n    }\n    return 0;\n}',
        4, '1 < x < 10', 'In C, 1 < x < 10 associates left-to-right as (1 < x) < 10! (1 < 25) is 1. Then 1 < 10 is 1 (TRUE), even though 25 is NOT < 10!',
        [
            ('A', 'FALSE', False, 'Treated the expression as mathematical range check 1 < x AND x < 10 (since 25 is not < 10, assumed false).', 'C does not have chained mathematical inequalities. It parses strictly as (1 < x) < 10; 1 < 25 yields 1, and 1 < 10 is true!'),
            ('B', 'Compile error', False, 'Thought chaining relational operators is a syntax error in C.', 'Chained relational operators are completely valid syntax; they just evaluate with left-associative boolean promotion.'),
            ('C', 'TRUE', True, 'Relational operators associate left-to-right: (1 < 25) evaluates to 1, then 1 < 10 evaluates to 1 (true), so the if-branch executes.', ''),
            ('D', 'Undefined behavior', False, 'Thought comparison chaining causes undefined behavior.', 'The evaluation order and semantics are strictly and deterministically specified by §6.5.8.')
        ],
        '< associates left-to-right. (1 < x) is 1. 1 < 10 is 1 (true). Outputs TRUE.',
        'ISO/IEC 9899:1999 §6.5.8 (Relational operators - associativity and semantics)',
        "In mathematics and Python, '1 < x < 10' represents a conjunction tests that x is strictly between 1 and 10. However, in C, relational operators have left-to-right associativity (§6.5.8#3).\n\nTherefore, '1 < x < 10' is parsed and grouped strictly as:\n((1 < x) < 10)\nFirst, '1 < x' (1 < 25) evaluates to integer 1 (representing true).\nNext, that boolean result 1 is compared against 10: '1 < 10'.\nSince 1 is strictly less than 10, the condition evaluates to 1 (true)!\n\nThis is one of the most famous trap questions on undergraduate C exams. To correctly express range membership in C, one must use logical AND: '1 < x && x < 10'.",
        [
            (1, 3, 'Initialize int x = 25.', {'x': 25}, {'stack': [{'name': 'x', 'type': 'int', 'address': '0x7ffd10', 'value': '25'}]}),
            (2, 4, 'Left associative evaluation: evaluate 1 < x (1 < 25) -> yields integer boolean result 1.', {'temp_cmp': 1}, {'stack': [{'name': 'x', 'type': 'int', 'address': '0x7ffd10', 'value': '25'}]}),
            (3, 4, 'Evaluate 1 < 10: 1 < 10 is true (1); if-condition succeeds.', {'condition': 1}, {'stack': [{'name': 'x', 'type': 'int', 'address': '0x7ffd10', 'value': '25'}]}),
            (4, 5, "Execute then-branch: printf prints 'TRUE\\n'.", {'stdout': 'TRUE'}, {'stack': [{'name': 'x', 'type': 'int', 'address': '0x7ffd10', 'value': '25'}]})
        ]
    )

    # Q023: Short-Circuit with Logical OR (||)
    add_q(
        23, 'TOPIC_OPERATORS', 'Tricky', 'Short-Circuit with Logical OR (||)',
        'What is the output of the following program?',
        '#include <stdio.h>\nint main() {\n    int a = 1, b = 5;\n    if (a++ || b++) {\n        printf("%d %d\\n", a, b);\n    }\n    return 0;\n}',
        4, 'a++ || b++', 'Because a++ evaluates to 1 (non-zero/true), logical OR short-circuits: b++ is NEVER evaluated!',
        [
            ('A', '2 6', False, 'Assumed both sides of || are always evaluated.', 'Logical OR || is a sequence point and guarantees short-circuiting: if the left operand is non-zero, the right operand is strictly NOT evaluated.'),
            ('B', '2 5', True, 'a++ yields 1 (true) and increments a to 2. Because the left side of || is true, b++ is short-circuited and skipped, leaving b = 5.', ''),
            ('C', '1 5', False, 'Thought a++ did not increment before printf.', 'Postfix a++ increments a before entering the if block body.'),
            ('D', '1 6', False, 'Thought a was unincremented and b was incremented.', 'Left operand is evaluated first; right operand is skipped.')
        ],
        'The || operator guarantees left-to-right evaluation; if the first operand is non-zero, the second operand is not evaluated.',
        'ISO/IEC 9899:1999 §6.5.14#4 (Logical OR operator - short-circuit behavior)',
        "Unlike bitwise operators (| and &), the logical operators (|| and &&) introduce sequence points and guarantee strict left-to-right evaluation with short-circuit behavior (ISO C99 §6.5.14#4).\n\nUnder the standard: 'if the first operand compares unequal to 0, the second operand is not evaluated.'\n\nIn 'if (a++ || b++)':\n1. The left expression 'a++' is evaluated. It yields the current value of 'a' (1).\n2. The side effect increments 'a' from 1 to 2.\n3. Because 1 is non-zero (true), the logical OR condition is already fully satisfied.\n4. The right expression 'b++' is completely bypassed and never executed.\nConsequently, 'b' remains untouched at 5, and printf outputs '2 5'.",
        [
            (1, 3, 'Initialize a = 1, b = 5 in stack frame.', {'a': 1, 'b': 5}, {'stack': [{'name': 'a', 'type': 'int', 'address': '0x7ffd10', 'value': '1'}, {'name': 'b', 'type': 'int', 'address': '0x7ffd14', 'value': '5'}]}),
            (2, 4, 'Evaluate left operand a++: yields 1 (true); side effect updates a = 2.', {'a': 2, 'b': 5, 'left_val': 1}, {'stack': [{'name': 'a', 'type': 'int', 'address': '0x7ffd10', 'value': '2'}, {'name': 'b', 'type': 'int', 'address': '0x7ffd14', 'value': '5'}]}),
            (3, 4, 'Short-circuit: left operand is true (1), so b++ is skipped; condition evaluates to 1.', {'condition': 1}, {'stack': [{'name': 'a', 'type': 'int', 'address': '0x7ffd10', 'value': '2'}, {'name': 'b', 'type': 'int', 'address': '0x7ffd14', 'value': '5'}]}),
            (4, 5, "printf outputs '2 5\\n'.", {'stdout': '2 5'}, {'stack': [{'name': 'a', 'type': 'int', 'address': '0x7ffd10', 'value': '2'}, {'name': 'b', 'type': 'int', 'address': '0x7ffd14', 'value': '5'}]})
        ]
    )

    # Q024: Short-Circuit with Logical AND (&&)
    add_q(
        24, 'TOPIC_OPERATORS', 'Tricky', 'Short-Circuit with Logical AND (&&)',
        'What is the output of the following program?',
        '#include <stdio.h>\nint main() {\n    int a = 0, b = 10;\n    if (a && ++b) {\n        printf("YES\\n");\n    }\n    printf("%d %d\\n", a, b);\n    return 0;\n}',
        4, 'a && ++b', 'Because a is 0 (false), logical AND short-circuits: ++b is NEVER evaluated!',
        [
            ('A', '0 11', False, 'Assumed prefix ++b executed before the logical AND evaluation.', 'Logical AND evaluates strictly left-to-right; because the left operand is false (0), the right operand is never evaluated.'),
            ('B', 'YES followed by 0 11', False, 'Thought the condition succeeded.', '0 && anything is false (0), so the if-body is bypassed.'),
            ('C', '1 10', False, 'Thought a was incremented.', 'Variable a was never incremented.'),
            ('D', '0 10', True, 'a is 0 (false), so logical AND short-circuits immediately. ++b is skipped, leaving b = 10.', '')
        ],
        'The && operator guarantees left-to-right evaluation; if the first operand is 0, the second operand is not evaluated.',
        'ISO/IEC 9899:1999 §6.5.13#4 (Logical AND operator - short-circuit behavior)',
        "Under ISO C99 §6.5.13#4, the '&&' operator guarantees left-to-right evaluation with a sequence point after the first operand. If the first operand compares equal to 0, the second operand is NOT evaluated.\n\nIn 'if (a && ++b)':\n1. Variable 'a' is evaluated. Its value is 0 (false).\n2. The overall result of the logical AND must be 0 regardless of the second operand.\n3. By the short-circuit rule, the subexpression '++b' is skipped entirely.\n4. The if-body is not executed.\n5. In the subsequent printf, 'a' is still 0 and 'b' is still 10.\n\nShort-circuiting in C is critical for safety patterns such as 'if (ptr != NULL && *ptr == 42)', where evaluating the right operand without short-circuiting would cause a null-pointer dereference crash.",
        [
            (1, 3, 'Initialize a = 0, b = 10 on the stack.', {'a': 0, 'b': 10}, {'stack': [{'name': 'a', 'type': 'int', 'address': '0x7ffd10', 'value': '0'}, {'name': 'b', 'type': 'int', 'address': '0x7ffd14', 'value': '10'}]}),
            (2, 4, "Evaluate left operand 'a': value is 0 (false).", {'left_operand': 0}, {'stack': [{'name': 'a', 'type': 'int', 'address': '0x7ffd10', 'value': '0'}, {'name': 'b', 'type': 'int', 'address': '0x7ffd14', 'value': '10'}]}),
            (3, 4, 'Short-circuit: right operand ++b is skipped; overall condition is 0.', {'condition': 0}, {'stack': [{'name': 'a', 'type': 'int', 'address': '0x7ffd10', 'value': '0'}, {'name': 'b', 'type': 'int', 'address': '0x7ffd14', 'value': '10'}]}),
            (4, 7, "printf prints '0 10\\n'.", {'stdout': '0 10'}, {'stack': [{'name': 'a', 'type': 'int', 'address': '0x7ffd10', 'value': '0'}, {'name': 'b', 'type': 'int', 'address': '0x7ffd14', 'value': '10'}]})
        ]
    )

    # Q025: Precedence of Logical AND over Logical OR
    add_q(
        25, 'TOPIC_OPERATORS', 'Tricky', 'Precedence of Logical AND over Logical OR',
        'What is the value of res?',
        '#include <stdio.h>\nint main() {\n    int a = 1, b = 0, c = 1;\n    int res = a || b && !c;\n    printf("%d\\n", res);\n    return 0;\n}',
        4, 'a || b && !c', 'Precedence: ! binds first, then &&, then ||. Parsed as a || (b && (!c)). Since a is 1, short-circuit returns 1!',
        [
            ('A', '1', True, '&& has higher precedence than ||, grouping as a || (b && !c). Because a = 1, || short-circuits and yields 1.', ''),
            ('B', '0', False, 'Thought operators evaluated strictly left-to-right: (a || b) && !c = (1 || 0) && !1 = 1 && 0 = 0.', '&& has strictly higher precedence than || in C grammar! It parses as a || (b && !c), NOT (a || b) && !c.'),
            ('C', 'Compile error', False, 'Thought mixing logical operators without explicit parentheses is a syntax error.', 'C grammar has fully unambiguous operator precedence for all boolean operators.'),
            ('D', '-1', False, 'Thought boolean operations in C can yield negative results.', 'Logical operators in C strictly yield integer 0 or 1.')
        ],
        '&& has higher precedence than ||. The expression groups as a || (b && !c). Because a is 1, || short-circuits to 1.',
        'ISO/IEC 9899:1999 §6.5.13 & §6.5.14 (Logical AND and OR precedence)',
        "In C's operator precedence table:\n1. Logical NOT (!) has unary precedence (level 2).\n2. Logical AND (&&) has precedence level 11.\n3. Logical OR (||) has precedence level 12 (lower than &&).\n\nTherefore, the unparenthesized expression 'a || b && !c' is grouped as:\na || (b && (!c))\n\nNext, evaluation proceeds left-to-right. The left operand of '||' is 'a'. Because 'a == 1' (true), the '||' operator short-circuits immediately. The entire right operand '(b && !c)' is never evaluated, and the expression yields 1.",
        [
            (1, 3, 'Initialize a = 1, b = 0, c = 1.', {'a': 1, 'b': 0, 'c': 1}, {'stack': [{'name': 'a', 'type': 'int', 'address': '0x7ffd10', 'value': '1'}, {'name': 'b', 'type': 'int', 'address': '0x7ffd14', 'value': '0'}, {'name': 'c', 'type': 'int', 'address': '0x7ffd18', 'value': '1'}]}),
            (2, 4, "Grammar groups expression as a || (b && !c); evaluate left operand 'a' (value 1).", {'left_operand': 1}, {'stack': [{'name': 'res', 'type': 'int', 'address': '0x7ffd1c', 'value': 'uninitialized'}]}),
            (3, 4, "Short-circuit: since left operand is 1, || yields 1; assign 1 to 'res'.", {'res': 1}, {'stack': [{'name': 'res', 'type': 'int', 'address': '0x7ffd1c', 'value': '1'}]}),
            (4, 5, "printf prints '1\\n'.", {'stdout': '1'}, {'stack': [{'name': 'res', 'type': 'int', 'address': '0x7ffd1c', 'value': '1'}]})
        ]
    )

    # Q026: Basic Ternary Conditional Evaluation
    add_q(
        26, 'TOPIC_OPERATORS', 'Easy', 'Basic Ternary Conditional Evaluation',
        'What is the output of the following program?',
        '#include <stdio.h>\nint main() {\n    int x = 10, y = 20;\n    int max = (x > y) ? x : y;\n    printf("%d\\n", max);\n    return 0;\n}',
        4, '(x > y) ? x : y', 'x > y (10 > 20) is false, so the expression evaluates to the second branch y (20)!',
        [
            ('A', '10', False, 'Thought x was selected.', 'The second operand (x) is selected only if the condition evaluates to true. Since 10 > 20 is false, y is selected.'),
            ('B', '20', True, "Condition 10 > 20 is false (0), so the ternary operator evaluates and yields the third operand 'y' (20).", ''),
            ('C', '1', False, 'Thought ternary returns a boolean truth value.', 'The ternary operator yields the value of the selected branch expression, not a boolean.'),
            ('D', '0', False, 'Thought ternary returns 0 on false condition.', 'Ternary operator returns the value of the expression following the colon (y = 20).')
        ],
        'The conditional operator evaluates the first operand. If false, it evaluates and yields the third operand (y = 20).',
        'ISO/IEC 9899:1999 §6.5.15 (Conditional operator)',
        "The conditional operator '? :' is C's only ternary operator (§6.5.15). Its syntax is:\ncondition ? expr1 : expr2\n\nEvaluation proceeds as follows:\n1. The first operand (condition) is evaluated.\n2. There is a sequence point after the evaluation of the first operand.\n3. If condition != 0 (true), expr1 is evaluated and expr2 is skipped.\n4. If condition == 0 (false), expr2 is evaluated and expr1 is skipped.\n\nHere, 'x = 10' and 'y = 20'. The condition 'x > y' (10 > 20) evaluates to 0 (false). Therefore, expr2 ('y') is evaluated, producing 20, which is assigned to 'max'.",
        [
            (1, 3, 'Initialize x = 10, y = 20.', {'x': 10, 'y': 20}, {'stack': [{'name': 'x', 'type': 'int', 'address': '0x7ffd10', 'value': '10'}, {'name': 'y', 'type': 'int', 'address': '0x7ffd14', 'value': '20'}]}),
            (2, 4, "Evaluate condition (x > y) -> (10 > 20) = 0 (false); select branch 'y' (20); store in 'max'.", {'max': 20}, {'stack': [{'name': 'max', 'type': 'int', 'address': '0x7ffd18', 'value': '20'}]}),
            (3, 5, "printf prints '20\\n'.", {'stdout': '20'}, {'stack': [{'name': 'max', 'type': 'int', 'address': '0x7ffd18', 'value': '20'}]})
        ]
    )

    # Q027: Chained Ternary Associativity
    add_q(
        27, 'TOPIC_OPERATORS', 'Medium', 'Chained Ternary Associativity',
        'What is the output of the following program?',
        '#include <stdio.h>\nint main() {\n    int x = 1 ? 2 : 3 ? 4 : 5;\n    printf("%d\\n", x);\n    return 0;\n}',
        3, '1 ? 2 : 3 ? 4 : 5', 'Ternary operator associates RIGHT-TO-LEFT: 1 ? 2 : (3 ? 4 : 5). Since 1 is true, result is 2!',
        [
            ('A', '4', False, 'Assumed left-to-right grouping: (1 ? 2 : 3) ? 4 : 5 = 2 ? 4 : 5 = 4.', "In C, '? :' associates strictly from right to left, NOT left to right!"),
            ('B', '5', False, 'Thought the fallback branch was chosen.', 'The first condition is 1 (true), so the entire right branch is skipped.'),
            ('C', 'Compile error', False, 'Thought chaining ternary operators without parentheses is illegal.', 'Chained ternaries are standard C syntax with right-to-left associativity.'),
            ('D', '2', True, 'The conditional operator is right-associative: 1 ? 2 : (3 ? 4 : 5). Since condition 1 is true, it yields 2 and skips the right expression.', '')
        ],
        'The conditional operator associates from right to left: a ? b : (c ? d : e). Outputs 2.',
        'ISO/IEC 9899:1999 §6.5.15 (Conditional operator - associativity)',
        "Unlike most binary operators which associate left-to-right, assignment operators and the conditional operator '? :' associate from right to left (ISO C99 §6.5.15).\n\nThus, '1 ? 2 : 3 ? 4 : 5' parses strictly as:\n1 ? 2 : (3 ? 4 : 5)\n\nWhen executed:\n1. The leftmost condition '1' is evaluated. It is non-zero (true).\n2. The operator yields the middle expression '2'.\n3. The right-hand expression '(3 ? 4 : 5)' is never evaluated due to short-circuiting.\nThe result assigned to 'x' is 2.\n\nHad C been left-associative like PHP, it would have evaluated to '(1 ? 2 : 3) ? 4 : 5' = '2 ? 4 : 5' = 4. This grammatical contrast is a classic exam question.",
        [
            (1, 3, 'Grammar groups right-associatively: 1 ? 2 : (3 ? 4 : 5).', {'grouping': '1 ? 2 : (3 ? 4 : 5)'}, {'stack': []}),
            (2, 3, "Condition '1' is non-zero (true) -> yields 2; right subexpression skipped; assign 2 to x.", {'x': 2}, {'stack': [{'name': 'x', 'type': 'int', 'address': '0x7ffd10', 'value': '2'}]}),
            (3, 4, "printf prints '2\\n'.", {'stdout': '2'}, {'stack': [{'name': 'x', 'type': 'int', 'address': '0x7ffd10', 'value': '2'}]})
        ]
    )

    # Q028: Comma Operator Value Extraction
    add_q(
        28, 'TOPIC_OPERATORS', 'Easy', 'Comma Operator Value Extraction',
        'What is the value of x after execution?',
        '#include <stdio.h>\nint main() {\n    int x = (10, 20, 30);\n    printf("%d\\n", x);\n    return 0;\n}',
        3, '(10, 20, 30)', 'The comma operator evaluates operands left-to-right and discards them, returning the LAST operand (30)!',
        [
            ('A', '10', False, 'Thought the comma operator returns the first operand.', 'The left operand of a comma operator is evaluated as a void expression and discarded; only the rightmost value is returned.'),
            ('B', '60', False, 'Thought the comma operator sums the elements like in a tuple.', 'The comma operator is not an accumulator; it performs sequential evaluation and value selection.'),
            ('C', '30', True, 'The comma operator evaluates its operands from left to right and yields the value of the rightmost operand (30).', ''),
            ('D', 'Compile error', False, 'Thought multiple values in parentheses is a syntax error.', 'The comma operator is a fundamental language operator in C (§6.5.17).')
        ],
        'The comma operator evaluates left-to-right; the result has the type and value of the right operand (30).',
        'ISO/IEC 9899:1999 §6.5.17 (Comma operator)',
        "The comma operator ',' has the lowest precedence of all C operators (§6.5.17). A comma expression consists of two expressions separated by a comma: 'expr1 , expr2'.\n\nThe left operand 'expr1' is evaluated, its value is discarded, and there is a sequence point. Then 'expr2' is evaluated, and the result of the entire expression has the type and value of 'expr2'.\n\nIn '(10, 20, 30)', this operator chains left-to-right:\n1. 10 is evaluated and discarded.\n2. 20 is evaluated and discarded.\n3. 30 is evaluated and returned as the final value.\nThus, 'x' is assigned 30.",
        [
            (1, 3, 'Evaluate left operand 10: value discarded.', {'discarded': 10}, {'stack': []}),
            (2, 3, 'Evaluate second operand 20: value discarded.', {'discarded': 20}, {'stack': []}),
            (3, 3, "Evaluate final operand 30: yields 30; assign 30 to 'x'.", {'x': 30}, {'stack': [{'name': 'x', 'type': 'int', 'address': '0x7ffd10', 'value': '30'}]}),
            (4, 4, "printf prints '30\\n'.", {'stdout': '30'}, {'stack': [{'name': 'x', 'type': 'int', 'address': '0x7ffd10', 'value': '30'}]})
        ]
    )

    # Q029: Comma Operator vs Assignment Precedence
    add_q(
        29, 'TOPIC_OPERATORS', 'Tricky', 'Comma Operator vs Assignment Precedence',
        'What is the output of the following program?',
        '#include <stdio.h>\nint main() {\n    int a;\n    a = 1, 2, 3;\n    printf("%d\\n", a);\n    return 0;\n}',
        4, 'a = 1, 2, 3;', 'Assignment (=) has higher precedence than comma (,). This parses as: (a = 1), 2, 3; so a gets 1!',
        [
            ('A', '3', False, 'Confused with a = (1, 2, 3) where parentheses force the comma operator to evaluate first.', 'Without parentheses, assignment (=) binds tighter than comma (,). Only 1 is assigned to a; 2 and 3 are evaluated and discarded.'),
            ('B', '1', True, 'Assignment (=) has higher precedence than comma (,). The expression parses as ((a = 1), 2), 3, assigning 1 to a.', ''),
            ('C', '2', False, 'Picked the middle value.', 'No operator in C selects the middle operand.'),
            ('D', 'Compile error', False, 'Thought multiple commas without parentheses are forbidden in expression statements.', 'Comma expressions are valid anywhere an expression is permitted.')
        ],
        '= has higher precedence than the comma operator. Parsed as ((a = 1), 2), 3. Outputs 1.',
        'ISO/IEC 9899:1999 §6.5.16 & §6.5.17 (Assignment vs comma precedence)',
        "The comma operator possesses the absolute lowest precedence in the entire C grammar (precedence level 15). The simple assignment operator '=' has precedence level 14, which is higher than the comma operator.\n\nWithout enclosing parentheses, 'a = 1, 2, 3;' is parsed as:\n((a = 1), 2), 3;\n\n1. The first subexpression '(a = 1)' is evaluated: 1 is assigned to 'a'.\n2. The comma operator discards the result of '(a = 1)'.\n3. The next expression '2' is evaluated and discarded.\n4. The final expression '3' is evaluated and discarded.\nBecause 'a' was assigned 1 in the first step, 'a' retains the value 1. To assign 3 to 'a', explicit parentheses are mandatory: 'a = (1, 2, 3);'.",
        [
            (1, 3, "Declare local uninitialized variable 'a'.", {'a': 'uninitialized'}, {'stack': [{'name': 'a', 'type': 'int', 'address': '0x7ffd10', 'value': 'uninitialized'}]}),
            (2, 4, "Precedence groups assignment first: (a = 1) executes, assigning 1 to 'a'.", {'a': 1}, {'stack': [{'name': 'a', 'type': 'int', 'address': '0x7ffd10', 'value': '1'}]}),
            (3, 4, 'Remaining comma operands 2 and 3 are evaluated as statements and discarded.', {'discarded': [2, 3]}, {'stack': [{'name': 'a', 'type': 'int', 'address': '0x7ffd10', 'value': '1'}]}),
            (4, 5, "printf prints '1\\n'.", {'stdout': '1'}, {'stack': [{'name': 'a', 'type': 'int', 'address': '0x7ffd10', 'value': '1'}]})
        ]
    )

    # Q030: Compound Assignment Right-Hand Precedence
    add_q(
        30, 'TOPIC_OPERATORS', 'Tricky', 'Compound Assignment Right-Hand Precedence',
        'What is the output of the following program?',
        '#include <stdio.h>\nint main() {\n    int x = 5;\n    x *= 2 + 3;\n    printf("%d\\n", x);\n    return 0;\n}',
        4, 'x *= 2 + 3;', 'Compound assignment evaluates the ENTIRE right-hand expression first: x = x * (2 + 3) = 5 * 5 = 25, NOT 13!',
        [
            ('A', '25', True, 'E1 op= E2 is strictly equivalent to E1 = E1 op (E2). The right-hand side 2 + 3 evaluates to 5 first; then 5 * 5 = 25.', ''),
            ('B', '13', False, 'Assumed multiplication executed first: (x * 2) + 3 = (5 * 2) + 3 = 10 + 3 = 13.', 'Compound assignment has lower precedence than addition! The entire right-hand expression (2 + 3) is parenthesized before multiplication.'),
            ('C', '10', False, 'Forgot to add 3.', 'The full right-hand expression 2 + 3 = 5 is multiplied with x.'),
            ('D', '15', False, 'Arithmetic calculation error.', '5 multiplied by 5 equals 25; 15 is an arithmetic calculation error.')
        ],
        'E1 op= E2 is equivalent to E1 = E1 op (E2). The right-hand side has implicit parentheses: x = 5 * (2 + 3) = 25.',
        'ISO/IEC 9899:1999 §6.5.16.2 (Compound assignment)',
        "A compound assignment operator of the form 'E1 op= E2' is defined by ISO C99 §6.5.16.2 as equivalent to:\nE1 = E1 op (E2)\nexcept that E1 is evaluated only once.\n\nNotice the crucial parentheses around '(E2)'. In 'x *= 2 + 3;', E1 is 'x' and E2 is '2 + 3'.\nTherefore, this statement expands to:\nx = x * (2 + 3)\n\nThe right-hand side '2 + 3' evaluates first, producing 5. Then 'x * 5' evaluates to '5 * 5 = 25', which is assigned back to 'x'.\n\nThis is an extremely popular trap on midterm exams because students see '*' and recall that multiplication has higher precedence than addition, falsely computing (5 * 2) + 3 = 13.",
        [
            (1, 3, 'Initialize int x = 5 on the stack.', {'x': 5}, {'stack': [{'name': 'x', 'type': 'int', 'address': '0x7ffd10', 'value': '5'}]}),
            (2, 4, 'Evaluate RHS expression (2 + 3) -> 5; then compute x * 5 = 5 * 5 = 25; assign to x.', {'rhs': 5, 'x': 25}, {'stack': [{'name': 'x', 'type': 'int', 'address': '0x7ffd10', 'value': '25'}]}),
            (3, 5, "printf prints '25\\n'.", {'stdout': '25'}, {'stack': [{'name': 'x', 'type': 'int', 'address': '0x7ffd10', 'value': '25'}]})
        ]
    )

    # Q031: Bitwise AND vs Logical AND
    add_q(
        31, 'TOPIC_OPERATORS', 'Medium', 'Bitwise AND vs Logical AND',
        'What is the output of the following program?',
        '#include <stdio.h>\nint main() {\n    int a = 4, b = 2; // binary: 100 and 010\n    int r1 = a && b;\n    int r2 = a & b;\n    printf("%d %d\\n", r1, r2);\n    return 0;\n}',
        5, 'int r2 = a & b;', 'Logical AND (&&) checks truthiness: both 4 and 2 are non-zero, yielding 1. Bitwise AND (&) compares bits: 100 & 010 = 0!',
        [
            ('A', '1 1', False, 'Confused bitwise & with logical &&, assuming both test truthiness.', 'Bitwise & checks individual binary bits; since 4 (100 in binary) and 2 (010 in binary) share no common 1 bits, the result is 0.'),
            ('B', '0 0', False, 'Thought logical && failed because bitwise & was 0.', 'Logical && tests whether operands are non-zero; because 4 != 0 and 2 != 0, a && b is 1.'),
            ('C', '6 0', False, 'Confused bitwise & with bitwise OR (|).', '4 | 2 would be 6, but & is bitwise AND.'),
            ('D', '1 0', True, 'Logical && checks truthiness: both 4 and 2 are non-zero (true), yielding 1. Bitwise & performs bitwise AND: 100 & 010 = 0.', '')
        ],
        '&& yields 1 if both operands are non-zero. & computes bitwise conjunction (100 & 010 = 0). Outputs 1 0.',
        'ISO/IEC 9899:1999 §6.5.10 (Bitwise AND) & §6.5.13 (Logical AND)',
        "Logical AND (&&) and Bitwise AND (&) serve entirely different purposes in C:\n\n1. Logical AND (&&): Treats operands as boolean conditions (0 is false, non-zero is true). Both 'a = 4' and 'b = 2' are non-zero, so 'a && b' evaluates to integer 1 (§6.5.13).\n\n2. Bitwise AND (&): Operates on the binary bit representations of the operands bit by bit (§6.5.10):\na = 4  -->  00000100 (binary)\nb = 2  -->  00000010 (binary)\n-----------------------------\na & b  -->  00000000 (binary) = 0 decimal.\n\nConsequently, 'r1' is 1 and 'r2' is 0, printing '1 0'.",
        [
            (1, 3, 'Initialize a = 4 (binary 100) and b = 2 (binary 010).', {'a': 4, 'b': 2}, {'stack': [{'name': 'a', 'type': 'int', 'address': '0x7ffd10', 'value': '4'}, {'name': 'b', 'type': 'int', 'address': '0x7ffd14', 'value': '2'}]}),
            (2, 4, 'Logical AND: 4 != 0 (true) and 2 != 0 (true) -> r1 = 1.', {'r1': 1}, {'stack': [{'name': 'r1', 'type': 'int', 'address': '0x7ffd18', 'value': '1'}]}),
            (3, 5, 'Bitwise AND: 0b100 & 0b010 = 0b000 (0) -> r2 = 0.', {'r2': 0}, {'stack': [{'name': 'r2', 'type': 'int', 'address': '0x7ffd1c', 'value': '0'}]}),
            (4, 6, "printf prints '1 0\\n'.", {'stdout': '1 0'}, {'stack': [{'name': 'r1', 'type': 'int', 'address': '0x7ffd18', 'value': '1'}, {'name': 'r2', 'type': 'int', 'address': '0x7ffd1c', 'value': '0'}]})
        ]
    )

    # Q032: Bitwise Shift vs Addition Precedence
    add_q(
        32, 'TOPIC_OPERATORS', 'Tricky', 'Bitwise Shift vs Addition Precedence',
        'What is the output of the following program?',
        '#include <stdio.h>\nint main() {\n    int x = 1 << 2 + 3;\n    printf("%d\\n", x);\n    return 0;\n}',
        3, '1 << 2 + 3', 'Addition (+) has higher precedence than bitwise shift (<<)! Evaluates as 1 << (2 + 3) = 1 << 5 = 32!',
        [
            ('A', '7', False, 'Thought << evaluated before +: (1 << 2) + 3 = 4 + 3 = 7.', 'Arithmetic operators (+, -) have higher precedence than shift operators (<<, >>). The addition executes first.'),
            ('B', '8', False, 'Thought 1 << 2 = 4 and then multiplied by 2.', 'Shift count is 5; 1 << 5 is 2^5 = 32.'),
            ('C', '32', True, 'Arithmetic addition (+) binds tighter than bitwise shift (<<). Thus 2 + 3 = 5 evaluates first, followed by 1 << 5 = 32.', ''),
            ('D', '12', False, 'Calculated (1 + 2) << 3 or made an arithmetic mistake.', 'Operator precedence strictly dictates 1 << (2 + 3).')
        ],
        '+ and - have higher precedence than << and >>. Groups as 1 << (2 + 3) = 1 << 5 = 32.',
        'ISO/IEC 9899:1999 §6.5.6 (Additive operators) & §6.5.7 (Bitwise shift operators)',
        "In C's operator precedence hierarchy:\n- Additive operators (+ and -) reside at precedence level 4.\n- Shift operators (<< and >>) reside at precedence level 5 (lower than additive).\n\nBecause addition has higher precedence, '1 << 2 + 3' parses as:\n1 << (2 + 3)\n\nFirst, '2 + 3' evaluates to 5.\nThen '1 << 5' shifts the binary bit 1 left by 5 bit positions:\n1 in binary:  00000001\n1 << 5:       00100000 (which is 2^5 = 32).\nThus, 'x' becomes 32.\n\nThis is a classic trap because programmers often mentally associate bitwise shifts with multiplication (*), expecting them to have higher precedence than addition.",
        [
            (1, 3, 'Precedence check: + (level 4) binds tighter than << (level 5); evaluate 2 + 3 = 5.', {'rhs_sum': 5}, {'stack': []}),
            (2, 3, "Compute bitwise left shift: 1 << 5 = 32; assign 32 to local variable 'x'.", {'x': 32}, {'stack': [{'name': 'x', 'type': 'int', 'address': '0x7ffd10', 'value': '32'}]}),
            (3, 4, "printf prints '32\\n'.", {'stdout': '32'}, {'stack': [{'name': 'x', 'type': 'int', 'address': '0x7ffd10', 'value': '32'}]})
        ]
    )

    # Q033: Unary Minus Operator Inversion
    add_q(
        33, 'TOPIC_OPERATORS', 'Easy', 'Unary Minus Operator Inversion',
        'What is the output of the following program?',
        '#include <stdio.h>\nint main() {\n    int x = -5;\n    int y = -x;\n    printf("%d %d\\n", x, y);\n    return 0;\n}',
        4, 'int y = -x;', 'Unary minus inverts the sign of x: -(-5) becomes +5! x itself remains -5!',
        [
            ('A', '-5 5', True, "Unary minus yields the arithmetic negation of its operand: -(-5) = 5. The operand 'x' itself is not modified (-5).", ''),
            ('B', '-5 -5', False, 'Thought unary minus applied to a negative number produces a negative number.', 'Unary minus negates the numeric value; the negative of -5 is positive 5.'),
            ('C', '5 5', False, 'Thought -x modified variable x in place.', 'Unary - is an expression operator, not an assignment; it yields a new value without modifying x.'),
            ('D', '0 0', False, 'Assumed negating cancelled out the numbers to zero.', 'Unary negation yields +5, not zero; signs invert normally.')
        ],
        'The unary - operator yields the negative of its operand: -(-5) = 5. x is unchanged.',
        'ISO/IEC 9899:1999 §6.5.3.3#3 (Unary arithmetic operators)',
        "Under ISO C99 §6.5.3.3#3, the result of the unary '-' operator is the negative of its (promoted) operand. The integer promotions are performed on the operand.\n\nGiven 'x = -5':\nEvaluating '-x' negates -5, which algebraically yields +5.\nImportantly, the unary minus operator does NOT possess side effects—it does not alter the value stored in 'x'.\n\nTherefore, 'x' remains -5, and 'y' receives the positive value 5. The output of printf is '-5 5'.",
        [
            (1, 3, 'Initialize int x = -5.', {'x': -5}, {'stack': [{'name': 'x', 'type': 'int', 'address': '0x7ffd10', 'value': '-5'}]}),
            (2, 4, "Evaluate unary minus: -(-5) yields positive 5; assign 5 to 'y'.", {'x': -5, 'y': 5}, {'stack': [{'name': 'x', 'type': 'int', 'address': '0x7ffd10', 'value': '-5'}, {'name': 'y', 'type': 'int', 'address': '0x7ffd14', 'value': '5'}]}),
            (3, 5, "printf outputs '-5 5\\n'.", {'stdout': '-5 5'}, {'stack': [{'name': 'x', 'type': 'int', 'address': '0x7ffd10', 'value': '-5'}, {'name': 'y', 'type': 'int', 'address': '0x7ffd14', 'value': '5'}]})
        ]
    )

    # Q034: Logical NOT Operator Behavior
    add_q(
        34, 'TOPIC_OPERATORS', 'Easy', 'Logical NOT Operator Behavior',
        'What is the output of the following program?',
        '#include <stdio.h>\nint main() {\n    int a = 42;\n    int b = 0;\n    printf("%d %d\\n", !a, !b);\n    return 0;\n}',
        5, 'printf("%d %d\\n", !a, !b);', '! on any non-zero value yields 0. ! on 0 yields 1!',
        [
            ('A', '0 0', False, 'Thought ! on 0 yields 0.', '! inverts truthiness: since 0 is false, !0 is true (1).'),
            ('B', '0 1', True, 'In C, logical NOT (!) evaluates to 0 if its operand is non-zero, and 1 if its operand equals 0.', ''),
            ('C', '1 0', False, 'Inverted the results.', '!42 is 0 because 42 is non-zero; !0 is 1 because 0 is false.'),
            ('D', '-42 0', False, 'Confused logical NOT (!) with bitwise NOT (~) or unary minus (-).', '! is a boolean logical operator that strictly produces integer 0 or 1.')
        ],
        'The ! operator yields 0 if operand is non-zero, and 1 if operand is zero: !42 is 0, !0 is 1.',
        'ISO/IEC 9899:1999 §6.5.3.3#5 (Logical negation operator)',
        "Under ISO C99 §6.5.3.3#5:\n'The result of the logical negation operator ! is 0 if the value of its operand compares unequal to 0, 1 if the value of its operand compares equal to 0. The result has type int.'\n\nIn C, truthiness is binary:\n- Any non-zero numeric value (positive or negative) evaluates to true.\n- Exactly zero (0 or 0.0 or NULL) evaluates to false.\n\nFor 'a = 42', 42 != 0, so '!a' evaluates to 0.\nFor 'b = 0', 0 == 0, so '!b' evaluates to 1.\nprintf outputs '0 1'.",
        [
            (1, 3, 'Initialize a = 42, b = 0.', {'a': 42, 'b': 0}, {'stack': [{'name': 'a', 'type': 'int', 'address': '0x7ffd10', 'value': '42'}, {'name': 'b', 'type': 'int', 'address': '0x7ffd14', 'value': '0'}]}),
            (2, 5, 'Evaluate !a: 42 != 0 (true) -> !42 evaluates to 0.', {'not_a': 0}, {'stack': [{'name': 'a', 'type': 'int', 'address': '0x7ffd10', 'value': '42'}, {'name': 'b', 'type': 'int', 'address': '0x7ffd14', 'value': '0'}]}),
            (3, 5, 'Evaluate !b: 0 == 0 (false) -> !0 evaluates to 1.', {'not_b': 1}, {'stack': [{'name': 'a', 'type': 'int', 'address': '0x7ffd10', 'value': '42'}, {'name': 'b', 'type': 'int', 'address': '0x7ffd14', 'value': '0'}]}),
            (4, 5, "printf prints '0 1\\n'.", {'stdout': '0 1'}, {'stack': [{'name': 'a', 'type': 'int', 'address': '0x7ffd10', 'value': '42'}, {'name': 'b', 'type': 'int', 'address': '0x7ffd14', 'value': '0'}]})
        ]
    )

print("syllabus_part1 loaded (34 questions).")
