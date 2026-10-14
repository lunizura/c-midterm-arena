# bank_part1.py: Q001 to Q032 (CAT_PREC_EVAL & CAT_PTR_ARR)

def load_part1(add_q):
    # =========================================================================
    # CAT_PREC_EVAL (Q001 - Q014)
    # =========================================================================
    
    # Q001: *p++
    add_q(
        1, "CAT_PREC_EVAL", "Tricky", "Post-Increment Dereference (*p++)",
        "What is the output of the following program?",
        """#include <stdio.h>
int main() {
    int arr[] = {10, 20, 30};
    int *p = arr;
    int x = *p++;
    printf("%d %d\\n", x, *p);
    return 0;
}""",
        5, "*p++", "Postfix ++ binds tighter than unary *, incrementing p, NOT the value at *p!",
        [
            ("A", "10 20", True, "Recognized that postfix ++ increments pointer p after fetching arr[0].", ""),
            ("B", "11 20", False, "Believed ++ increments the integer 10 to 11.", "To increment the integer, you need parentheses: (*p)++."),
            ("C", "10 10", False, "Thought p has not yet advanced when printf runs.", "The post-increment side-effect completes at the statement's sequence point."),
            ("D", "11 10", False, "Assumed both that *p was incremented and p never moved.", "Confuses both operator precedence and pointer mutation.")
        ],
        "Postfix ++ has higher precedence than unary *. Hence, *p++ evaluates as *(p++).",
        "ISO/IEC 9899 §6.5.2.4 & §6.5.3.2",
        "The expression yields the original pointer for dereferencing (arr[0]=10), and as a side-effect advances pointer p to arr[1].",
        [
            (1, 4, "Array arr initialized with {10, 20, 30}. p points to arr[0].", {"*p": 10, "p_addr": "0x1000"}, {"stack": [{"name":"arr[0]","val":10,"addr":"0x1000"},{"name":"arr[1]","val":20,"addr":"0x1004"},{"name":"p","val":"0x1000","pointsTo":"0x1000"}]}),
            (2, 5, "*p++ evaluated: value 10 assigned to x. Pointer p increments from 0x1000 to 0x1004.", {"x": 10, "*p": 20, "p_addr": "0x1004"}, {"stack": [{"name":"x","val":10},{"name":"p","val":"0x1004","pointsTo":"0x1004"}]}),
            (3, 6, "printf prints x (10) and *p (20).", {"stdout": "10 20"}, None)
        ]
    )

    # Q002: (*p)++
    add_q(
        2, "CAT_PREC_EVAL", "Medium", "Parenthesized Post-Increment ((*p)++)",
        "What is the output of the following program?",
        """#include <stdio.h>
int main() {
    int arr[] = {10, 20, 30};
    int *p = arr;
    int x = (*p)++;
    printf("%d %d %d\\n", x, arr[0], *p);
    return 0;
}""",
        5, "(*p)++", "Parentheses force dereference first, so ++ modifies the array element, not the pointer!",
        [
            ("A", "10 11 11", True, "Correctly saw that the value 10 is returned for x, then arr[0] is incremented to 11 while p remains at arr[0].", ""),
            ("B", "11 11 11", False, "Thought postfix ++ returns the incremented value.", "Postfix ++ yields the OLD value prior to increment."),
            ("C", "10 10 20", False, "Confused (*p)++ with *p++ and thought p advanced to arr[1].", "Parentheses override precedence; p does not change address."),
            ("D", "10 11 20", False, "Thought both the element was incremented and the pointer advanced.", "Only one increment occurs, and it applies strictly to the int.")
        ],
        "Parentheses force * to bind before ++. The value at arr[0] is read (10) for x, then incremented to 11.",
        "ISO/IEC 9899 §6.5.2.4",
        "Because p itself is never incremented, both arr[0] and *p evaluate to 11.",
        [
            (1, 4, "Array arr initialized. p points to arr[0].", {"*p": 10}, None),
            (2, 5, "(*p)++ evaluated: old value 10 stored in x, then arr[0] becomes 11. p is unchanged.", {"x": 10, "arr[0]": 11, "*p": 11}, None),
            (3, 6, "printf prints x (10), arr[0] (11), and *p (11).", {"stdout": "10 11 11"}, None)
        ]
    )

    # Q003: *++p
    add_q(
        3, "CAT_PREC_EVAL", "Medium", "Pre-Increment Dereference (*++p)",
        "What is the output of the following program?",
        """#include <stdio.h>
int main() {
    int arr[] = {10, 20, 30};
    int *p = arr;
    int x = *++p;
    printf("%d %d\\n", x, *p);
    return 0;
}""",
        5, "*++p", "Prefix ++ increments the pointer BEFORE dereferencing!",
        [
            ("A", "20 20", True, "p advances to arr[1] first, then dereferences to 20.", ""),
            ("B", "10 20", False, "Confused prefix ++ with postfix ++.", "Prefix ++ increments before returning the value."),
            ("C", "11 11", False, "Thought ++ applied to the integer value 10.", "Without parentheses, prefix ++ still binds to p because unary operators associate right-to-left."),
            ("D", "20 10", False, "Thought *p reverted back to arr[0].", "Pointer mutation is permanent.")
        ],
        "Both * and ++ are unary operators associating right-to-left: *(++p). Pointer p moves to arr[1] before dereference.",
        "ISO/IEC 9899 §6.5.3.1",
        "p is incremented from &arr[0] to &arr[1], so dereferencing yields 20, which is assigned to x.",
        [
            (1, 5, "++p increments p to &arr[1]. Dereference *p then evaluates to 20.", {"p_target": "arr[1]", "x": 20}, None),
            (2, 6, "printf prints x (20) and *p (20).", {"stdout": "20 20"}, None)
        ]
    )

    # Q004: ++*p
    add_q(
        4, "CAT_PREC_EVAL", "Medium", "Pre-Increment Dereferenced Value (++*p)",
        "What is the output of the following program?",
        """#include <stdio.h>
int main() {
    int arr[] = {10, 20, 30};
    int *p = arr;
    int x = ++*p;
    printf("%d %d %d\\n", x, arr[0], *p);
    return 0;
}""",
        5, "++*p", "Right-to-left associativity: ++(*p). The integer value at arr[0] is incremented to 11 first!",
        [
            ("A", "11 11 11", True, "arr[0] is pre-incremented to 11, so x, arr[0], and *p are all 11.", ""),
            ("B", "10 11 11", False, "Confused prefix with postfix increment.", "Prefix ++ returns the NEW incremented value."),
            ("C", "20 10 20", False, "Thought p advanced to arr[1].", "p is never incremented, only the value it points to."),
            ("D", "10 10 10", False, "Thought no mutation occurred.", "arr[0] is modified in place.")
        ],
        "Unary operators associate right-to-left, so ++*p is ++(*p). arr[0] becomes 11 and evaluates to 11.",
        "ISO/IEC 9899 §6.5.3.1",
        "p remains pointing at arr[0], whose value has been modified to 11.",
        [
            (1, 5, "*p is dereferenced (10) and pre-incremented to 11. x receives 11.", {"arr[0]": 11, "x": 11, "*p": 11}, None),
            (2, 6, "printf prints 11 11 11.", {"stdout": "11 11 11"}, None)
        ]
    )

    # Q005: Short-Circuit OR
    add_q(
        5, "CAT_PREC_EVAL", "Tricky", "Short-Circuit Evaluation with Logical OR",
        "What is the output of the following program?",
        """#include <stdio.h>
int main() {
    int a = 1, b = 2;
    if (a++ || b++) {
        printf("%d %d\\n", a, b);
    }
    return 0;
}""",
        5, "a++ || b++", "Because a++ evaluates to non-zero (1), logical OR short-circuits: b++ is NEVER evaluated!",
        [
            ("A", "2 2", True, "a is incremented to 2, but b++ was short-circuited and remains 2.", ""),
            ("B", "2 3", False, "Assumed both sides of || always execute.", "In C, || guarantees that if the left operand is non-zero, the right operand is skipped."),
            ("C", "1 2", False, "Thought a++ did not take effect.", "a++ increments immediately after its value (1) is retrieved."),
            ("D", "1 3", False, "Thought a was skipped and only b executed.", "Left-to-right evaluation guarantees left operand executes first.")
        ],
        "Logical OR (||) has guaranteed left-to-right evaluation and short-circuits if the left operand is true (non-zero).",
        "ISO/IEC 9899 §6.5.14#4",
        "a++ evaluates to 1 (true), so the entire condition is true. The right operand b++ is never evaluated, leaving b = 2.",
        [
            (1, 5, "Left operand a++ evaluates to 1 (true). Side effect increments a from 1 to 2.", {"a": 2}, None),
            (2, 5, "Short-circuit: Right operand b++ is skipped entirely. b remains 2.", {"b": 2}, None),
            (3, 6, "printf prints a (2) and b (2).", {"stdout": "2 2"}, None)
        ]
    )

    # Q006: Short-Circuit AND
    add_q(
        6, "CAT_PREC_EVAL", "Tricky", "Short-Circuit Evaluation with Logical AND",
        "What is the output of the following program?",
        """#include <stdio.h>
int main() {
    int a = 0, b = 5;
    if (a && ++b) {
        printf("TRUE\\n");
    }
    printf("%d %d\\n", a, b);
    return 0;
}""",
        5, "a && ++b", "Because a is 0 (false), logical AND short-circuits: ++b is NEVER evaluated!",
        [
            ("A", "0 5", True, "a is 0 so ++b never runs; b stays 5.", ""),
            ("B", "0 6", False, "Assumed ++b executed before the AND comparison.", "&& evaluates strictly left-to-right and skips right side when left is 0."),
            ("C", "TRUE followed by 0 6", False, "Thought 0 && anything could be true.", "0 is false in C."),
            ("D", "1 5", False, "Thought a was incremented.", "a was not modified.")
        ],
        "Logical AND (&&) guarantees left-to-right evaluation. If left operand is 0, right operand is not evaluated.",
        "ISO/IEC 9899 §6.5.13#4",
        "Since a is 0 (false), ++b is bypassed. The body of the if is skipped and b remains 5.",
        [
            (1, 5, "a is 0 (false). Condition fails immediately. ++b is skipped.", {"b": 5}, None),
            (2, 8, "printf prints a (0) and b (5).", {"stdout": "0 5"}, None)
        ]
    )

    # Q007: Nested Precedence (&& over ||)
    add_q(
        7, "CAT_PREC_EVAL", "Tricky", "Precedence of Logical AND vs Logical OR",
        "What is the output of the following program?",
        """#include <stdio.h>
int main() {
    int a = 1, b = 0, c = 0;
    int res = a || b && c++;
    printf("%d %d\\n", res, c);
    return 0;
}""",
        5, "a || b && c++", "&& has higher precedence than ||, grouping as: a || (b && c++). Since a is 1, short-circuit skips (b && c++)!",
        [
            ("A", "1 0", True, "res is 1, and c++ is skipped due to short-circuit on ||.", ""),
            ("B", "1 1", False, "Thought && executed first and evaluated c++.", "Precedence determines grouping, but || still controls execution order left-to-right."),
            ("C", "0 0", False, "Thought the expression evaluated to false.", "1 || anything is 1 (true)."),
            ("D", "0 1", False, "Thought result was 0 and c was incremented.", "Incorrect evaluation of both operators.")
        ],
        "&& binds tighter than ||, meaning the expression is parsed as a || (b && c++). However, || evaluates left-to-right with short-circuiting.",
        "ISO/IEC 9899 §6.5.14",
        "Because a is 1 (true), the entire right-hand expression (b && c++) is skipped, leaving c as 0.",
        [
            (1, 5, "Parsed as a || (b && c++). Left side 'a' is 1.", {"a": 1}, None),
            (2, 5, "Short-circuit: (b && c++) skipped. res = 1.", {"res": 1, "c": 0}, None),
            (3, 6, "printf prints 1 0.", {"stdout": "1 0"}, None)
        ]
    )

    # Q008: Comma Operator in Parentheses
    add_q(
        8, "CAT_PREC_EVAL", "Easy", "Comma Operator Value Extraction",
        "What is the value of x after execution?",
        """#include <stdio.h>
int main() {
    int x = (10, 20, 30);
    printf("%d\\n", x);
    return 0;
}""",
        4, "(10, 20, 30)", "The comma operator evaluates each expression and yields the value of the LAST expression!",
        [
            ("A", "30", True, "The comma operator discards left values and evaluates to the rightmost value (30).", ""),
            ("B", "10", False, "Thought the comma operator takes the first value.", "Comma operator evaluates left-to-right and produces the final operand."),
            ("C", "60", False, "Thought it summed the numbers.", "Comma is an operator, not an adder."),
            ("D", "Compile error", False, "Thought multiple commas inside parentheses are illegal.", "Comma is a valid operator in C expressions.")
        ],
        "The comma operator has lowest precedence. Inside parentheses, expressions are evaluated left-to-right, returning the last.",
        "ISO/IEC 9899 §6.5.17",
        "10 is evaluated and discarded, 20 is evaluated and discarded, 30 is evaluated and returned, so x = 30.",
        [
            (1, 4, "10 discarded -> 20 discarded -> 30 assigned to x.", {"x": 30}, None),
            (2, 5, "printf prints 30.", {"stdout": "30"}, None)
        ]
    )

    # Q009: Comma Operator vs Assignment Precedence
    add_q(
        9, "CAT_PREC_EVAL", "Tricky", "Comma Operator vs Assignment Precedence",
        "What is the output of the following program?",
        """#include <stdio.h>
int main() {
    int a, b;
    a = 1, 2, 3;
    printf("%d\\n", a);
    return 0;
}""",
        5, "a = 1, 2, 3;", "Assignment (=) has higher precedence than comma (,). This parses as (a = 1), 2, 3;",
        [
            ("A", "1", True, "Because = binds tighter than comma, 'a = 1' executes, then 2 and 3 are evaluated and discarded.", ""),
            ("B", "3", False, "Confused with a = (1, 2, 3). Without parentheses, = binds to 1.", "Parentheses are required to assign the result of the comma operator."),
            ("C", "2", False, "Picked middle operand.", "No operator returns the middle operand."),
            ("D", "Compile error", False, "Thought a statement cannot contain unparenthesized commas.", "Comma expressions as statements are valid C.")
        ],
        "= has higher precedence than the comma operator. The expression parses as ((a = 1), 2), 3.",
        "ISO/IEC 9899 §6.5.16 & §6.5.17",
        "a is assigned 1, then the rest of the comma expression runs with no effect on a.",
        [
            (1, 5, "Grouped as (a = 1), 2, 3. a becomes 1.", {"a": 1}, None),
            (2, 6, "printf prints 1.", {"stdout": "1"}, None)
        ]
    )

    # Q010: Right-Associativity of Ternary Operator
    add_q(
        10, "CAT_PREC_EVAL", "Medium", "Chained Ternary Associativity",
        "What is the output of the following program?",
        """#include <stdio.h>
int main() {
    int x = 1 ? 2 : 3 ? 4 : 5;
    printf("%d\\n", x);
    return 0;
}""",
        4, "1 ? 2 : 3 ? 4 : 5", "The conditional (ternary) operator associates RIGHT-TO-LEFT: 1 ? 2 : (3 ? 4 : 5).",
        [
            ("A", "2", True, "Since 1 is true, the first branch (2) is returned immediately.", ""),
            ("B", "4", False, "Thought it grouped left-to-right as (1 ? 2 : 3) ? 4 : 5.", "In C, ?: groups right-to-left."),
            ("C", "5", False, "Picked the final fallback branch.", "1 is true, so fallback is not reached."),
            ("D", "Compile error", False, "Thought chaining ternary operators is illegal in C.", "Chained ternaries are fully valid syntax.")
        ],
        "The conditional operator ?: associates from right to left: a ? b : (c ? d : e).",
        "ISO/IEC 9899 §6.5.15",
        "Condition 1 is true (non-zero), so the result is 2, and the right-hand ternary (3 ? 4 : 5) is skipped.",
        [
            (1, 4, "Grouped as 1 ? 2 : (3 ? 4 : 5). Condition 1 is true -> yields 2.", {"x": 2}, None),
            (2, 5, "printf prints 2.", {"stdout": "2"}, None)
        ]
    )

    # Q011: Shift Operator vs Addition Precedence
    add_q(
        11, "CAT_PREC_EVAL", "Tricky", "Bitwise Shift vs Arithmetic Addition Precedence",
        "What is the output of the following program?",
        """#include <stdio.h>
int main() {
    int x = 1 << 2 + 3;
    printf("%d\\n", x);
    return 0;
}""",
        4, "1 << 2 + 3", "Addition (+) has higher precedence than bitwise shift (<<)! It evaluates as 1 << (2 + 3) = 1 << 5 = 32.",
        [
            ("A", "32", True, "2 + 3 is evaluated first to 5, then 1 << 5 gives 32.", ""),
            ("B", "7", False, "Assumed left-to-right evaluation: (1 << 2) + 3 = 4 + 3 = 7.", "Arithmetic operators (+, -) have higher precedence than shift operators (<<, >>)."),
            ("C", "8", False, "Calculated 2^3.", "Shift operator shifts binary bits."),
            ("D", "12", False, "Random calculation error.", "Precedence is explicitly + over <<.")
        ],
        "Addition and subtraction (+, -) have higher precedence than bitwise shift operators (<<, >>).",
        "ISO/IEC 9899 §6.5.6 & §6.5.7",
        "The expression is grouped as 1 << (2 + 3). 2 + 3 is 5. 1 left-shifted by 5 bits is 32.",
        [
            (1, 4, "Addition evaluates first: 2 + 3 = 5.", {"temp": 5}, None),
            (2, 4, "Shift evaluates next: 1 << 5 = 32.", {"x": 32}, None),
            (3, 5, "printf prints 32.", {"stdout": "32"}, None)
        ]
    )

    # Q012: Relational Chaining Trap (1 < x < 10)
    add_q(
        12, "CAT_PREC_EVAL", "Tricky", "Mathematical Relational Chaining Fallacy",
        "What is the output of the following program?",
        """#include <stdio.h>
int main() {
    int x = 20;
    if (1 < x < 10) {
        printf("INSIDE\\n");
    } else {
        printf("OUTSIDE\\n");
    }
    return 0;
}""",
        5, "1 < x < 10", "Relational operators associate left-to-right: (1 < x) evaluates to 1, then 1 < 10 evaluates to TRUE!",
        [
            ("A", "INSIDE", True, "(1 < 20) is 1 (true). Then (1 < 10) is 1 (true), so the if-block executes!", ""),
            ("B", "OUTSIDE", False, "Thought it checked if x was between 1 and 10 (20 is not < 10).", "C does NOT support chained mathematical comparisons; use (1 < x && x < 10)."),
            ("C", "Compile error", False, "Thought chained comparisons cause syntax errors.", "Chained comparisons are syntactically valid but logically deceptive."),
            ("D", "Undefined Behavior", False, "Thought relational chaining is undefined.", "The behavior is strictly defined by left-to-right associativity.")
        ],
        "< associates left-to-right. (1 < x) evaluates to 1. Then (1 < 10) evaluates to 1 (true).",
        "ISO/IEC 9899 §6.5.8#6",
        "Even though 20 is not less than 10, the intermediate boolean result 1 IS less than 10, printing INSIDE.",
        [
            (1, 5, "Left-to-right: 1 < 20 evaluates to 1 (true).", {"step1": 1}, None),
            (2, 5, "Next: 1 < 10 evaluates to 1 (true). Condition passes.", {"condition": 1}, None),
            (3, 6, "printf prints INSIDE.", {"stdout": "INSIDE"}, None)
        ]
    )

    # Q013: Bitwise AND (&) vs Logical AND (&&) Precedence
    add_q(
        13, "CAT_PREC_EVAL", "Tricky", "Bitwise AND Precedence with Equality",
        "What is the output of the following program?",
        """#include <stdio.h>
int main() {
    int x = 6; // binary 110
    if (x & 1 == 0) {
        printf("YES\\n");
    } else {
        printf("NO\\n");
    }
    return 0;
}""",
        5, "x & 1 == 0", "Equality (==) has higher precedence than bitwise AND (&)! This evaluates as x & (1 == 0) = x & 0 = 0 (FALSE).",
        [
            ("A", "NO", True, "1 == 0 evaluates to 0 first, then 6 & 0 evaluates to 0 (false), triggering the else block.", ""),
            ("B", "YES", False, "Assumed it checked if x is even via (x & 1) == 0.", "Equality operators (==, !=) bind tighter than bitwise (&, |, ^). Parentheses are required!"),
            ("C", "Compile error", False, "Thought & and == cannot be mixed without parentheses.", "Valid syntax, but a notorious logic bug."),
            ("D", "1", False, "Picked a numeric value.", "The printf outputs YES or NO.")
        ],
        "Equality operators (==, !=) have higher precedence than bitwise AND (&).",
        "ISO/IEC 9899 §6.5.9 & §6.5.10",
        "The condition evaluates as x & (1 == 0) -> 6 & 0 -> 0. The if condition is false, printing NO.",
        [
            (1, 5, "== has higher precedence: 1 == 0 evaluates to 0.", {"eq_result": 0}, None),
            (2, 5, "Bitwise AND evaluates: 6 & 0 evaluates to 0 (false).", {"condition": 0}, None),
            (3, 8, "else branch taken: prints NO.", {"stdout": "NO"}, None)
        ]
    )

    # Q014: Postfix vs Prefix Combination
    add_q(
        14, "CAT_PREC_EVAL", "Tricky", "Increment in Expression Output",
        "What is the output of the following program?",
        """#include <stdio.h>
int main() {
    int a = 5;
    int b = ++a + 10;
    int c = a++ + 10;
    printf("%d %d %d\\n", a, b, c);
    return 0;
}""",
        6, "a++ + 10", "++a increments immediately to 6 before addition; a++ uses current value (6) then increments to 7.",
        [
            ("A", "7 16 16", True, "b = 6 + 10 = 16. c = 6 + 10 = 16. a is incremented twice to 7.", ""),
            ("B", "7 15 16", False, "Miscalculated ++a.", "Prefix ++ increments before value is used."),
            ("C", "6 16 17", False, "Thought a was only incremented once.", "Both ++a and a++ increment variable a."),
            ("D", "7 16 17", False, "Thought a++ incremented before addition in c.", "Postfix ++ yields the old value before increment.")
        ],
        "++a increments a from 5 to 6, then adds 10 to give b = 16. Next, a++ yields 6 for c = 6 + 10 = 16, then increments a to 7.",
        "ISO/IEC 9899 §6.5.2.4 & §6.5.3.1",
        "At the end of line 6, a has been incremented twice, reaching 7.",
        [
            (1, 5, "++a increments a to 6. b = 6 + 10 = 16.", {"a": 6, "b": 16}, None),
            (2, 6, "a++ yields 6. c = 6 + 10 = 16. a increments to 7.", {"a": 7, "c": 16}, None),
            (3, 7, "printf prints 7 16 16.", {"stdout": "7 16 16"}, None)
        ]
    )

    # =========================================================================
    # CAT_PTR_ARR (Q015 - Q032)
    # =========================================================================

    # Q015: Array Decay in Function Parameter
    add_q(
        15, "CAT_PTR_ARR", "Tricky", "Array Decay to Pointer in Function Parameter",
        "What is printed when this program runs on a 64-bit architecture?",
        """#include <stdio.h>
void func(int arr[10]) {
    printf("%zu\\n", sizeof(arr));
}
int main() {
    int arr[10];
    func(arr);
    return 0;
}""",
        3, "sizeof(arr)", "In function parameter lists, int arr[10] is purely syntactic sugar for int *arr! sizeof(arr) returns pointer size (8 bytes)!",
        [
            ("A", "8", True, "On 64-bit systems, pointers are 8 bytes. The array decays into a pointer parameter.", ""),
            ("B", "40", False, "Thought sizeof(arr) returns 10 * sizeof(int) = 40 bytes.", "Arrays cannot be passed by value in C; the parameter decays to a pointer."),
            ("C", "10", False, "Thought it returns the element count 10.", "sizeof returns byte size, not element count."),
            ("D", "4", False, "Thought it returned sizeof(int).", "Pointers on 64-bit systems are 8 bytes.")
        ],
        "Array parameters in C functions decay into pointers. 'int arr[10]' in a parameter list is rewritten by the compiler as 'int *arr'.",
        "ISO/IEC 9899 §6.7.6.3#7",
        "Inside func, arr is a local pointer variable of type int*, so sizeof(arr) yields sizeof(int*), which is 8 bytes on a 64-bit target.",
        [
            (1, 7, "In main: arr is allocated as 10 ints on stack (40 bytes).", {"sizeof(main_arr)": 40}, None),
            (2, 8, "func(arr) is called. Address of arr[0] is passed.", None, None),
            (3, 3, "In func: arr parameter has decayed to type int*. sizeof(arr) evaluates to sizeof(int*) = 8.", {"sizeof(arr)": 8}, None)
        ]
    )

    # Q016: arr vs &arr Pointer Arithmetic
    add_q(
        16, "CAT_PTR_ARR", "Nightmare", "Difference between arr and &arr Stride",
        "What is printed by this program?",
        """#include <stdio.h>
int main() {
    int arr[5] = {1, 2, 3, 4, 5};
    int *p1 = (int*)(arr + 1);
    int *p2 = (int*)(&arr + 1);
    printf("%d %d\\n", *p1, *(p2 - 1));
    return 0;
}""",
        5, "&arr + 1", "arr + 1 advances by 1 int (4 bytes). &arr + 1 advances by the ENTIRE ARRAY of 5 ints (20 bytes)!",
        [
            ("A", "2 5", True, "p1 points to arr[1] (val 2). p2 points past arr[4], so *(p2 - 1) points back to arr[4] (val 5).", ""),
            ("B", "2 2", False, "Thought &arr + 1 also advanced by only 1 int.", "&arr has type int (*)[5]; adding 1 advances by 5 ints (20 bytes)."),
            ("C", "1 5", False, "Thought arr + 1 stayed at arr[0].", "arr + 1 points to arr[1]."),
            ("D", "Undefined Behavior", False, "Thought p2 - 1 is illegal pointer arithmetic.", "p2 points to one-past-the-end, so p2 - 1 safely points to the last element.")
        ],
        "arr decays to int* (stride 4 bytes). &arr has type pointer-to-array 'int (*)[5]' (stride 5 * 4 = 20 bytes).",
        "ISO/IEC 9899 §6.5.6",
        "&arr + 1 points directly past the 5th element. Subtracting 1 int pointer step (p2 - 1) lands exactly on arr[4], whose value is 5.",
        [
            (1, 4, "arr + 1 moves forward by 1 int -> points to arr[1] (2).", {"*p1": 2}, None),
            (2, 5, "&arr + 1 moves forward by 5 ints -> points past the end of arr.", {"p2_target": "past_end"}, None),
            (3, 6, "p2 - 1 steps back 1 int -> points to arr[4] (5).", {"*(p2-1)": 5}, None)
        ]
    )

    # Q017: Commutative Array Indexing 3[arr]
    add_q(
        17, "CAT_PTR_ARR", "Tricky", "Commutative Array Indexing (i[arr])",
        "What is the output of the following program?",
        """#include <stdio.h>
int main() {
    int arr[] = {10, 20, 30, 40, 50};
    printf("%d\\n", 3[arr]);
    return 0;
}""",
        4, "3[arr]", "By definition in C, E1[E2] is identical to (*((E1) + (E2))). Addition is commutative, so 3[arr] == arr[3]!",
        [
            ("A", "40", True, "3[arr] is identical to arr[3], which is 40.", ""),
            ("B", "30", False, "Off-by-one index error.", "Arrays are 0-indexed: index 3 is the 4th element (40)."),
            ("C", "Compile error", False, "Believed putting an integer before brackets is invalid syntax.", "The C standard explicitly defines E1[E2] as *((E1)+(E2)), making it valid."),
            ("D", "Garbage value", False, "Thought memory access was corrupt.", "Fully standard compliant access.")
        ],
        "The subscript operator [] is defined such that E1[E2] is identical to (*((E1) + (E2))). Because addition is commutative, 3[arr] == *(3 + arr) == *(arr + 3) == arr[3].",
        "ISO/IEC 9899 §6.5.2.1#2",
        "arr[3] is the 4th element: 10 (idx 0), 20 (idx 1), 30 (idx 2), 40 (idx 3).",
        [
            (1, 4, "3[arr] parsed as *(3 + arr) == *(arr + 3). Evaluates to arr[3] = 40.", {"val": 40}, None),
            (2, 4, "printf prints 40.", {"stdout": "40"}, None)
        ]
    )

    # Q018: Negative Array Indexing
    add_q(
        18, "CAT_PTR_ARR", "Medium", "Negative Array Indexing with Offset Pointer",
        "What is the output of the following program?",
        """#include <stdio.h>
int main() {
    int arr[] = {10, 20, 30, 40, 50};
    int *p = &arr[2];
    printf("%d %d\\n", p[-1], p[1]);
    return 0;
}""",
        5, "p[-1]", "p[-1] evaluates to *(p - 1), which accesses the preceding element arr[1] (20)!",
        [
            ("A", "20 40", True, "p points to arr[2] (30). p[-1] is arr[1] (20), and p[1] is arr[3] (40).", ""),
            ("B", "30 40", False, "Thought p[-1] was an invalid index returning 0 or unchanged.", "p[-1] steps backwards by 1 element in memory."),
            ("C", "Compile error", False, "Thought negative indices are forbidden in C.", "Pointers allow negative indexing as long as the target address is within array bounds."),
            ("D", "10 50", False, "Thought it jumped to beginning and end.", "Indices -1 and +1 are single offsets from p.")
        ],
        "p[-1] is defined as *(p + (-1)) == *(p - 1). Since p points to arr[2], p - 1 points to arr[1].",
        "ISO/IEC 9899 §6.5.2.1",
        "arr[1] is 20 and arr[3] is 40. The output is 20 40.",
        [
            (1, 4, "p points to arr[2] (30).", {"*p": 30}, None),
            (2, 5, "p[-1] accesses *(p - 1) = arr[1] (20). p[1] accesses *(p + 1) = arr[3] (40).", {"p[-1]": 20, "p[1]": 40}, None)
        ]
    )

    # Q019: Pointer Subtraction Scaling
    add_q(
        19, "CAT_PTR_ARR", "Medium", "Pointer Subtraction Scaling by sizeof(type)",
        "What is printed when subtracting two pointers into the same int array?",
        """#include <stdio.h>
int main() {
    int arr[5] = {1, 2, 3, 4, 5};
    int *p1 = &arr[0];
    int *p2 = &arr[4];
    printf("%td\\n", p2 - p1);
    return 0;
}""",
        6, "p2 - p1", "Pointer subtraction yields the difference in ELEMENTS (ptrdiff_t), NOT raw bytes!",
        [
            ("A", "4", True, "p2 is 4 elements ahead of p1. The result is 4.", ""),
            ("B", "16", False, "Multiplied 4 elements by 4 bytes/int to get 16 bytes.", "In C, subtracting two pointers automatically divides the byte distance by sizeof(*p)."),
            ("C", "5", False, "Counted total elements inclusive of both ends.", "Index 4 - Index 0 = 4."),
            ("D", "Undefined Behavior", False, "Thought subtracting pointers is undefined.", "Subtracting pointers within the same array object is well-defined.")
        ],
        "When two pointers to elements of the same array are subtracted, the result is the difference of their subscripts, of type ptrdiff_t.",
        "ISO/IEC 9899 §6.5.6#9",
        "Byte difference is 16 bytes. Divided by sizeof(int) (4) = 4 elements.",
        [
            (1, 6, "Address delta: 0x1010 - 0x1000 = 16 bytes. Scaled by sizeof(int) = 4.", {"p2 - p1": 4}, None)
        ]
    )

    # Q020: Array of Pointers vs Pointer to Array
    add_q(
        20, "CAT_PTR_ARR", "Tricky", "Array of Pointers vs Pointer to Array Syntax",
        "What is the type and meaning of: int (*p)[5]; ?",
        """#include <stdio.h>
int main() {
    int (*p)[5];
    return 0;
}""",
        3, "int (*p)[5]", "Parentheses force * to bind to p: p is a single pointer to an array of 5 integers!",
        [
            ("A", "p is a pointer to an array of 5 integers", True, "Parentheses around *p make p a pointer to an array of 5 ints.", ""),
            ("B", "p is an array of 5 pointers to integers", False, "That would be written without parentheses: int *p[5];", "Array brackets [] have higher precedence than *."),
            ("C", "p is a function returning a pointer", False, "Functions use argument parentheses, not dimension brackets.", "Syntax for function pointer is int (*f)(int)."),
            ("D", "Compile error: invalid syntax", False, "Thought declaration is invalid.", "This is standard C array pointer declaration.")
        ],
        "[] has higher precedence than *. Parentheses (*p) ensure * binds to p first, declaring p as a pointer to an array of 5 ints.",
        "ISO/IEC 9899 §6.7.6.2",
        "Contrast with 'int *p[5]' which is an array of 5 pointers to int.",
        [
            (1, 3, "Parsed as pointer to array of 5 ints. sizeof(*p) == 5 * sizeof(int).", None, None)
        ]
    )

    # Q021: 2D Array Row Pointer Decay
    add_q(
        21, "CAT_PTR_ARR", "Tricky", "2D Array Row Pointer Arithmetic Stride",
        "What is the output of the following program?",
        """#include <stdio.h>
int main() {
    int m[2][3] = {{1, 2, 3}, {4, 5, 6}};
    int *p = (int*)(m + 1);
    printf("%d\\n", *p);
    return 0;
}""",
        4, "m + 1", "m has type int[2][3]. Adding 1 to m advances by an entire ROW (3 ints = 12 bytes), landing on 4!",
        [
            ("A", "4", True, "m + 1 advances past row 0 to the start of row 1 (element 4).", ""),
            ("B", "2", False, "Thought m + 1 advanced by only 1 int (to element 2).", "m decays to int (*)[3], so stride is 3 ints."),
            ("C", "1", False, "Thought m + 1 had no effect.", "m + 1 advances one full sub-array row."),
            ("D", "5", False, "Picked middle element of row 1.", "Lands at the first element of row 1 (4).")
        ],
        "A 2D array decays into a pointer to its first row: int (*)[3]. Adding 1 advances by sizeof(int[3]) = 3 * sizeof(int).",
        "ISO/IEC 9899 §6.5.6",
        "m + 1 points to m[1], so casting to int* and dereferencing gives m[1][0] = 4.",
        [
            (1, 4, "m decays to int (*)[3]. m + 1 points to m[1] (starting at 4).", {"*p": 4}, None),
            (2, 5, "printf prints 4.", {"stdout": "4"}, None)
        ]
    )

    # Q022: Double Dereference on 2D Array (*(*(m + i) + j))
    add_q(
        22, "CAT_PTR_ARR", "Tricky", "Pointer Equivalence for 2D Array Subscripts",
        "Which of the following is equivalent to m[1][2]?",
        """#include <stdio.h>
int main() {
    int m[2][3] = {{10, 20, 30}, {40, 50, 60}};
    printf("%d\\n", *(*(m + 1) + 2));
    return 0;
}""",
        4, "*(*(m + 1) + 2)", "By subscript definition: m[1][2] == (*(m + 1))[2] == *(*(m + 1) + 2) == 60.",
        [
            ("A", "*(*(m + 1) + 2)", True, "Exact formal expansion of m[1][2].", ""),
            ("B", "*(m + 1 + 2)", False, "This adds 3 rows to m, exceeding array bounds.", "Row offset and column offset cannot be directly added without dereference."),
            ("C", "**(m + 1) + 2", False, "This dereferences m[1][0] (40) and adds integer 2, giving 42.", "Parentheses must enclose the column pointer."),
            ("D", "*(m + 1)[2]", False, "Invalid operator grouping.", "Subscript binds tighter than unary *.")
        ],
        "m[i][j] is formally defined as *(*(m + i) + j). (m + 1) points to row 1; *(m + 1) decays to int* pointing to m[1][0]; adding 2 points to m[1][2].",
        "ISO/IEC 9899 §6.5.2.1",
        "Dereferencing yields 60.",
        [
            (1, 4, "*(m + 1) yields pointer to row 1. Adding 2 yields pointer to element 2. Dereferencing gives 60.", {"val": 60}, None)
        ]
    )

    # Q023: Pass-by-Value Pointer Trap
    add_q(
        23, "CAT_PTR_ARR", "Tricky", "Passing Pointer by Value (Failed Allocation)",
        "What happens when the following code runs?",
        """#include <stdio.h>
#include <stdlib.h>
void allocate(int *p) {
    p = malloc(sizeof(int));
    *p = 42;
}
int main() {
    int *ptr = NULL;
    allocate(ptr);
    if (ptr == NULL) {
        printf("STILL NULL\\n");
    } else {
        printf("%d\\n", *ptr);
    }
    return 0;
}""",
        5, "allocate(ptr)", "Pointers in C are passed BY VALUE! allocate modifies its local copy p, leaving main's ptr STILL NULL (and leaking memory)!",
        [
            ("A", "STILL NULL", True, "Pointer parameter p is a local copy; modifying p does not modify ptr in main.", ""),
            ("B", "42", False, "Assumed passing a pointer allows modifying the pointer variable itself in the caller.", "To modify a pointer in the caller, you must pass a pointer-to-pointer (int **)."),
            ("C", "Compile error", False, "Thought malloc cannot be assigned to pointer parameter.", "The code is syntactically valid C."),
            ("D", "Segmentation fault", False, "Thought it crashed on dereference.", "The if (ptr == NULL) check handles NULL safely.")
        ],
        "All function arguments in C are passed by value. The parameter p receives a copy of the pointer ptr. Changing p inside allocate does not alter ptr in main.",
        "ISO/IEC 9899 §6.5.2.2",
        "ptr in main remains NULL, so 'STILL NULL' is printed.",
        [
            (1, 10, "ptr in main is NULL.", {"ptr": "NULL"}, None),
            (2, 4, "allocate called: parameter p is a local copy initialized to NULL.", {"p": "NULL"}, None),
            (3, 5, "p allocated new heap address. ptr in main is untouched.", {"p": "0x5000", "ptr": "NULL"}, None),
            (4, 11, "ptr is STILL NULL. Prints 'STILL NULL'.", {"stdout": "STILL NULL"}, None)
        ]
    )

    # Q024: Pointer to Pointer (int**) Solution
    add_q(
        24, "CAT_PTR_ARR", "Medium", "Modifying Caller Pointer via Pointer-to-Pointer",
        "What is the output of the following program?",
        """#include <stdio.h>
void set_val(int **pp, int *target) {
    *pp = target;
}
int main() {
    int a = 10, b = 20;
    int *p = &a;
    set_val(&p, &b);
    printf("%d\\n", *p);
    return 0;
}""",
        4, "*pp = target;", "Dereferencing the double pointer (*pp) directly updates the pointer p in main to point to b!",
        [
            ("A", "20", True, "p was modified via &p to point to b (val 20).", ""),
            ("B", "10", False, "Thought p still pointed to a.", "*pp modified p directly."),
            ("C", "Compile error", False, "Thought &p is invalid.", "&p produces an int**."),
            ("D", "Address of b", False, "Thought printf printed the pointer.", "printf prints *p (an integer).")
        ],
        "Passing &p passes the address of pointer p (type int**). *pp accesses the variable p in main and assigns &b to it.",
        "ISO/IEC 9899 §6.5.3.2",
        "After set_val returns, p points to b. *p evaluates to 20.",
        [
            (1, 9, "p points to a (10).", {"*p": 10}, None),
            (2, 10, "set_val(&p, &b) updates p to point to b.", {"*p": 20}, None),
            (3, 11, "printf prints 20.", {"stdout": "20"}, None)
        ]
    )

    # Q025: Void Pointer Dereference
    add_q(
        25, "CAT_PTR_ARR", "Easy", "Dereferencing a Void Pointer",
        "What happens when compiling this code with a strict C compiler?",
        """#include <stdio.h>
int main() {
    int x = 10;
    void *ptr = &x;
    printf("%d\\n", *ptr);
    return 0;
}""",
        5, "*ptr", "void* has an incomplete type with no size! Dereferencing a void* without casting is an ERROR in standard C!",
        [
            ("A", "Compilation Error", True, "In ISO C, void has no size, so *ptr cannot be dereferenced without an explicit cast like *(int*)ptr.", ""),
            ("B", "Prints 10", False, "Thought C automatically infers the underlying int type.", "void* loses all type information."),
            ("C", "Prints address of x", False, "Thought *ptr prints the address.", "Dereferencing attempts to fetch a value, not an address."),
            ("D", "Segmentation Fault", False, "Thought it compiles but crashes.", "The compiler rejects it at compile time.")
        ],
        "The type void is an incomplete type that cannot be completed. The unary * operator cannot be applied to an incomplete type.",
        "ISO/IEC 9899 §6.5.3.2#2",
        "To fix, cast to the appropriate pointer type: *(int*)ptr.",
        [
            (1, 5, "Compiler error: dereferencing 'void *' pointer.", None, None)
        ]
    )

    # Q026: Null Pointer Dereference
    add_q(
        26, "CAT_PTR_ARR", "Easy", "Null Pointer Dereference Behavior",
        "What happens at runtime when executing this code?",
        """#include <stdio.h>
int main() {
    int *p = NULL;
    printf("%d\\n", *p);
    return 0;
}""",
        4, "*p", "Dereferencing NULL accesses address 0x0, which causes an immediate Segmentation Fault / Access Violation!",
        [
            ("A", "Runtime Crash (Segmentation Fault)", True, "Address 0x0 is not mapped to user space. MMU triggers a fault.", ""),
            ("B", "Prints 0", False, "Assumed NULL evaluates to integer 0 on dereference.", "Dereferencing NULL is undefined behavior and crashes on modern OSes."),
            ("C", "Compilation Error", False, "Thought compiler forbids assigning NULL to a pointer.", "NULL is a valid pointer value, but dereferencing it is invalid."),
            ("D", "Prints (null)", False, "Confused %d with %s printing NULL string pointer.", "%d expects an int value from a valid memory address.")
        ],
        "Dereferencing a null pointer is undefined behavior. On virtual memory architectures, page 0 is unmapped, resulting in SIGSEGV.",
        "ISO/IEC 9899 §6.5.3.2",
        "The OS terminates the process immediately.",
        [
            (1, 4, "Dereferencing address 0x0 triggers page fault -> SIGSEGV.", None, None)
        ]
    )

    # Q027: Pointer Swap Function
    add_q(
        27, "CAT_PTR_ARR", "Medium", "Classic Pointer Swap Implementation",
        "What is the output of the following program?",
        """#include <stdio.h>
void swap(int *x, int *y) {
    int temp = *x;
    *x = *y;
    *y = temp;
}
int main() {
    int a = 5, b = 10;
    swap(&a, &b);
    printf("%d %d\\n", a, b);
    return 0;
}""",
        10, "swap(&a, &b);", "Addresses of a and b are passed, and values are swapped correctly in memory via dereferencing.",
        [
            ("A", "10 5", True, "Values in a and b are successfully swapped.", ""),
            ("B", "5 10", False, "Thought pass-by-value prevented the swap.", "Because pointers to a and b were passed, mutation affects the caller's variables."),
            ("C", "10 10", False, "Thought one value overwrote the other without temp.", "temp preserves *x before overwrite."),
            ("D", "Compile error", False, "Thought swap signature is invalid.", "Standard textbook swap function.")
        ],
        "Pointers allow simulated pass-by-reference. *x and *y modify the memory storage of a and b directly.",
        "ISO/IEC 9899 §6.5.3.2",
        "a becomes 10, b becomes 5.",
        [
            (1, 4, "temp = 5.", {"temp": 5}, None),
            (2, 5, "*x (a) = 10.", {"a": 10}, None),
            (3, 6, "*y (b) = 5.", {"b": 5}, None),
            (4, 11, "printf prints 10 5.", {"stdout": "10 5"}, None)
        ]
    )

    # Q028: Multi-level Dereferencing (***ppp)
    add_q(
        28, "CAT_PTR_ARR", "Medium", "Triple Pointer Dereferencing Chain",
        "What is the output of the following program?",
        """#include <stdio.h>
int main() {
    int x = 100;
    int *p = &x;
    int **pp = &p;
    int ***ppp = &pp;
    ***ppp = 200;
    printf("%d %d\\n", x, **pp);
    return 0;
}""",
        7, "***ppp = 200;", "***ppp follows the 3-step pointer chain straight down to x, setting x = 200!",
        [
            ("A", "200 200", True, "x is modified to 200, and **pp dereferences to x (200).", ""),
            ("B", "100 200", False, "Thought x was not modified.", "***ppp targets x directly."),
            ("C", "200 100", False, "Thought **pp cached old value.", "Pointers read live memory."),
            ("D", "Compile error", False, "Thought triple pointers are not supported in C.", "C supports arbitrarily nested pointer indirection.")
        ],
        "***ppp dereferences ppp -> pp -> p -> x. Assigning 200 overwrites x directly.",
        "ISO/IEC 9899 §6.5.3.2",
        "Both x and **pp reflect the new value 200.",
        [
            (1, 7, "***ppp resolves to x; x set to 200.", {"x": 200}, None),
            (2, 8, "printf prints 200 200.", {"stdout": "200 200"}, None)
        ]
    )

    # Q029: Function Pointer Invocation
    add_q(
        29, "CAT_PTR_ARR", "Tricky", "Function Pointer Declaration and Invocation",
        "What is the output of the following program?",
        """#include <stdio.h>
int add(int a, int b) { return a + b; }
int sub(int a, int b) { return a - b; }
int main() {
    int (*fp)(int, int) = add;
    printf("%d ", fp(10, 5));
    fp = sub;
    printf("%d\\n", fp(10, 5));
    return 0;
}""",
        5, "int (*fp)(int, int) = add;", "fp is a function pointer initially pointing to add, then reassigned to sub.",
        [
            ("A", "15 5", True, "First call executes add(10, 5) = 15; second call executes sub(10, 5) = 5.", ""),
            ("B", "15 15", False, "Thought function pointers cannot be reassigned.", "Function pointers are mutable variables."),
            ("C", "Compile error", False, "Thought parentheses around (*fp) are illegal.", "Parentheses are required to declare a function pointer."),
            ("D", "5 15", False, "Inverted order of calls.", "add runs before sub.")
        ],
        "Function pointer syntax: return_type (*func_ptr_name)(param_types). Calling fp(...) invokes the currently referenced function.",
        "ISO/IEC 9899 §6.7.6.3",
        "add returns 15, sub returns 5.",
        [
            (1, 6, "fp points to add. 10 + 5 = 15.", {"stdout": "15 "}, None),
            (2, 7, "fp reassigned to sub. 10 - 5 = 5.", {"stdout": "15 5"}, None)
        ]
    )

    # Q030: Array Bounds Overread (Off-by-One)
    add_q(
        30, "CAT_PTR_ARR", "Medium", "Array Out-of-Bounds Subscript Access",
        "What happens when executing arr[5] on an array of size 5?",
        """#include <stdio.h>
int main() {
    int arr[5] = {1, 2, 3, 4, 5};
    printf("%d\\n", arr[5]);
    return 0;
}""",
        4, "arr[5]", "Array indices are 0 to 4! arr[5] accesses memory outside the array bounds, causing Undefined Behavior!",
        [
            ("A", "Undefined Behavior (Accesses stack garbage or crashes)", True, "Valid indices are 0 through 4. C does not perform runtime bounds checks.", ""),
            ("B", "Compilation Error: Array index out of bounds", False, "Thought C compilers catch array bounds errors at compile-time.", "Standard C does not require bounds checking; it compiles without error."),
            ("C", "Prints 5", False, "Thought arr[5] is the 5th element.", "arr[4] is the 5th element (0-indexed)."),
            ("D", "Prints 0", False, "Thought out-of-bounds memory is zero-filled.", "Stack memory beyond the array contains indeterminate garbage.")
        ],
        "In C, array subscripting is unchecked pointer arithmetic (*(arr + 5)). Accessing beyond the allocated bounds violates §6.5.6 and is Undefined Behavior.",
        "ISO/IEC 9899 §6.5.6#8",
        "At runtime, this reads whatever garbage data exists adjacent on the stack.",
        [
            (1, 4, "arr[5] reads memory at &arr[0] + 5 * 4 bytes. Access outside bounds -> UB.", None, None)
        ]
    )

    # Q031: Pointer Comparison between Different Objects
    add_q(
        31, "CAT_PTR_ARR", "Nightmare", "Relational Comparison of Unrelated Pointers",
        "What does the C standard state about comparing pointers to two different local variables?",
        """#include <stdio.h>
int main() {
    int a = 10;
    int b = 20;
    if (&a < &b) {
        printf("A\\n");
    } else {
        printf("B\\n");
    }
    return 0;
}""",
        5, "&a < &b", "Relational comparison (<, <=, >, >=) between pointers to UNRELATED objects is Undefined Behavior in ISO C!",
        [
            ("A", "Undefined Behavior", True, "ISO C specifies relational operators are only defined when comparing pointers into the same array/object.", ""),
            ("B", "Always prints A", False, "Assumed stack growth direction guarantees a is at a lower address.", "Stack growth and layout of unrelated variables are unspecified and undefined to compare with <."),
            ("C", "Always prints B", False, "Assumed opposite stack layout.", "Still undefined behavior."),
            ("D", "Compile error", False, "Thought comparing pointers is a syntax error.", "Pointers of compatible types can syntactically be compared, but semantics are undefined.")
        ],
        "When two pointers are compared using relational operators (<, >, <=, >=), both must point to the same object or aggregate. Otherwise, the behavior is undefined.",
        "ISO/IEC 9899 §6.5.8#5",
        "While equality (==, !=) is defined, relational ordering between independent objects is strictly Undefined Behavior.",
        [
            (1, 5, "Comparing pointers to unrelated objects a and b violates §6.5.8#5.", None, None)
        ]
    )

    # Q032: Subtraction of Different Pointer Types
    add_q(
        32, "CAT_PTR_ARR", "Easy", "Subtracting Incompatible Pointer Types",
        "What happens when compiling this code?",
        """#include <stdio.h>
int main() {
    int a = 10;
    double d = 20.0;
    int *p1 = &a;
    double *p2 = &d;
    printf("%td\\n", p2 - p1);
    return 0;
}""",
        7, "p2 - p1", "Subtracting pointers of different types (double* and int*) is a COMPILATION ERROR!",
        [
            ("A", "Compilation Error", True, "In C, pointer subtraction is only valid between two pointers of compatible types pointing to the same object.", ""),
            ("B", "Prints byte difference", False, "Thought it subtracted raw addresses.", "Pointer subtraction requires identical base types to scale by sizeof."),
            ("C", "Prints 0", False, "Random guess.", "Does not compile."),
            ("D", "Runtime crash", False, "Thought it failed at runtime.", "Rejected by compiler.")
        ],
        "ISO C requires both operands of pointer subtraction to be pointers to qualified or unqualified versions of compatible complete object types.",
        "ISO/IEC 9899 §6.5.6#9",
        "Because int and double are incompatible types, compilation fails.",
        [
            (1, 7, "Error: invalid operands to binary - (have 'double *' and 'int *').", None, None)
        ]
    )

print("bank_part1 loaded (32 questions).")
