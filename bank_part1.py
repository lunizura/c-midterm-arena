# bank_part1.py: Q001 to Q032 (CAT_PREC_EVAL & CAT_PTR_ARR)
# High-Yield C Midterm Exam Question Bank - Part 1
# Thoroughly upgraded with ISO C99/C11 compliance, balanced answer keys (A/B/C/D),
# granular execution traces, visual stack/pointer memory snapshots, and deep pedagogical rationales.

def load_part1(add_q):
    # =========================================================================
    # CAT_PREC_EVAL (Q001 - Q014): Operator Precedence & Evaluation Order
    # =========================================================================

    # Q001: Post-Increment Dereference (*p++) -> Key A
    add_q(
        1, "CAT_PREC_EVAL", "Tricky", "Post-Increment Dereference (*p++)",
        "What is the output of the following program?",
        r"""#include <stdio.h>
int main() {
    int arr[] = {10, 20, 30};
    int *p = arr;
    int x = *p++;
    printf("%d %d\n", x, *p);
    return 0;
}""",
        5, "*p++", "Postfix ++ binds tighter than unary *, incrementing pointer p, NOT the integer value at *p!",
        [
            ("A", "10 20", True, "Recognized that postfix ++ has higher precedence than unary *, so p is incremented after its previous address is dereferenced.", ""),
            ("B", "11 20", False, "Believed ++ increments the integer 10 to 11 before assigning to x.", "To increment the pointed-to integer, parentheses are strictly required: (*p)++. Here ++ binds directly to pointer p."),
            ("C", "10 10", False, "Thought p has not yet advanced when printf runs.", "The post-increment side-effect completes at the statement's sequence point (the semicolon), so p points to arr[1] by the time printf executes."),
            ("D", "11 10", False, "Assumed both that the integer was incremented and that pointer p never moved.", "Confuses both operator precedence and pointer mutation mechanics.")
        ],
        "Postfix ++ has higher precedence than unary *. Hence, *p++ evaluates as *(p++).",
        "ISO/IEC 9899:1999 §6.5.2.4 & §6.5.3.2",
        "In C operator precedence, postfix operators ([], (), postfix ++, postfix --) bind tighter than prefix unary operators (*, &, ++, --). Thus, *p++ is grouped by the parser as *(p++).\n\nExecution Mechanics:\n1. The postfix expression p++ yields the current value of p (the address of arr[0], 0x1000).\n2. The unary dereference operator * is applied to that address, yielding the integer 10, which is assigned to x.\n3. As a side effect, p is incremented by sizeof(int) (4 bytes), advancing p to point to arr[1] (0x1004).\n4. When printf is reached, x contains 10, and *p reads arr[1], yielding 20.\n\nExam Trap: Never confuse *p++ with (*p)++ or *++p. Remember that postfix ++ always applies to the pointer variable itself unless shielded by parentheses.",
        [
            (1, 4, "Array arr allocated on stack: {10, 20, 30}. Pointer p initialized to &arr[0] (0x1000).", {"*p": 10, "p": "0x1000"}, {"stack": [{"name":"arr[0]","addr":"0x1000","val":10},{"name":"arr[1]","addr":"0x1004","val":20},{"name":"arr[2]","addr":"0x1008","val":30},{"name":"p","addr":"0x1010","val":"0x1000","pointsTo":"arr[0]"}]}),
            (2, 5, "p++ yields 0x1000 for dereferencing. Value 10 is copied into x.", {"x": 10}, {"stack": [{"name":"x","addr":"0x1014","val":10},{"name":"p","addr":"0x1010","val":"0x1000","pointsTo":"arr[0]"}]}),
            (3, 5, "Sequence point reached: side-effect executes, advancing p by sizeof(int) (0x1000 -> 0x1004).", {"p": "0x1004", "*p": 20}, {"stack": [{"name":"x","addr":"0x1014","val":10},{"name":"p","addr":"0x1010","val":"0x1004","pointsTo":"arr[1]"}]}),
            (4, 6, "printf prints x (10) and *p (20).", {"stdout": "10 20"}, {"stack": [{"name":"x","val":10},{"name":"*p","val":20}]})
        ]
    )

    # Q002: Parenthesized Post-Increment ((*p)++) -> Key B
    add_q(
        2, "CAT_PREC_EVAL", "Medium", "Parenthesized Post-Increment ((*p)++)",
        "What is the output of the following program?",
        r"""#include <stdio.h>
int main() {
    int arr[] = {10, 20, 30};
    int *p = arr;
    int x = (*p)++;
    printf("%d %d %d\n", x, arr[0], *p);
    return 0;
}""",
        5, "(*p)++", "Parentheses force dereference first, so ++ modifies the array element, not the pointer!",
        [
            ("A", "11 11 11", False, "Thought postfix ++ returns the incremented value.", "Postfix ++ always evaluates to the OLD value prior to the increment; prefix ++ would return 11."),
            ("B", "10 11 11", True, "Parentheses force *p to be evaluated first; postfix ++ returns old value 10 for x, then increments arr[0] to 11 in place while p remains pointing to arr[0].", ""),
            ("C", "10 10 20", False, "Confused (*p)++ with *p++ and thought pointer p advanced to arr[1].", "Parentheses strictly override precedence; pointer p does not advance its address."),
            ("D", "10 11 20", False, "Thought both the element was incremented and the pointer advanced.", "Only a single increment operator is present, and its operand is (*p), not p.")
        ],
        "Parentheses force * to bind before ++. The value at arr[0] is read (10) for x, then incremented to 11.",
        "ISO/IEC 9899:1999 §6.5.2.4",
        "Parentheses explicitly override natural operator precedence. In (*p)++, the subexpression (*p) is evaluated first, producing an lvalue designating the object arr[0].\n\nStep-by-step Evaluation:\n1. The dereference *p accesses arr[0] whose value is currently 10.\n2. The postfix ++ operator applied to this lvalue yields its current value (10) as the value of the overall assignment expression, which is stored in x.\n3. Before the sequence point at the semicolon, the value stored in arr[0] is incremented from 10 to 11.\n4. Pointer p itself was never modified; it still contains 0x1000 (&arr[0]).\n5. Thus, arr[0] is 11, *p is 11, and x is 10.\n\nExam Trap: Contrast (*p)++ with *p++ and ++*p. Always check where the parentheses reside to determine whether memory content or pointer address is mutating.",
        [
            (1, 4, "Array arr initialized. Pointer p points to arr[0] (0x1000).", {"p": "0x1000", "*p": 10}, {"stack": [{"name":"arr[0]","addr":"0x1000","val":10},{"name":"arr[1]","addr":"0x1004","val":20},{"name":"p","addr":"0x1010","val":"0x1000","pointsTo":"arr[0]"}]}),
            (2, 5, "Dereference *p evaluated: reads arr[0] (10). Postfix ++ yields 10 for assignment to x.", {"x": 10}, {"stack": [{"name":"x","addr":"0x1014","val":10}]}),
            (3, 5, "Side-effect applied to arr[0]: incremented from 10 to 11. Pointer p remains unchanged at 0x1000.", {"arr[0]": 11, "*p": 11, "p": "0x1000"}, {"stack": [{"name":"arr[0]","addr":"0x1000","val":11},{"name":"p","addr":"0x1010","val":"0x1000","pointsTo":"arr[0]"}]}),
            (4, 6, "printf prints x (10), arr[0] (11), and *p (11).", {"stdout": "10 11 11"}, {"stack": [{"name":"stdout","val":"10 11 11"}]})
        ]
    )

    # Q003: Pre-Increment Dereference (*++p) -> Key C
    add_q(
        3, "CAT_PREC_EVAL", "Medium", "Pre-Increment Dereference (*++p)",
        "What is the output of the following program?",
        r"""#include <stdio.h>
int main() {
    int arr[] = {10, 20, 30};
    int *p = arr;
    int x = *++p;
    printf("%d %d\n", x, *p);
    return 0;
}""",
        5, "*++p", "Prefix ++ increments the pointer BEFORE dereferencing!",
        [
            ("A", "10 20", False, "Confused prefix ++ with postfix ++.", "Prefix ++ increments before returning the evaluated pointer value, unlike postfix ++."),
            ("B", "11 11", False, "Thought ++ applied to the integer value 10.", "Without parentheses, prefix ++ still binds to p because unary operators associate right-to-left: *(++p)."),
            ("C", "20 20", True, "p is incremented first to point to arr[1] (address 0x1004), then dereferencing yields 20, which is stored in x.", ""),
            ("D", "20 10", False, "Thought *p reverted back to arr[0].", "Pointer mutation in C is permanent; p remains at &arr[1].")
        ],
        "Both * and ++ are unary operators associating right-to-left: *(++p). Pointer p moves to arr[1] before dereference.",
        "ISO/IEC 9899:1999 §6.5.3.1 & §6.5.3.2",
        "Both prefix ++ and unary * are prefix unary operators. In C, prefix unary operators share the same precedence level and associate from right to left: *(++p).\n\nExecution Trace:\n1. The operand of prefix ++ is p. Pointer p is incremented by sizeof(int) (4 bytes), advancing from &arr[0] (0x1000) to &arr[1] (0x1004).\n2. The expression ++p yields the NEW pointer value (0x1004).\n3. Unary * dereferences this new address, accessing arr[1] with value 20.\n4. 20 is assigned to x.\n5. printf outputs x (20) and *p (20).\n\nExam Trap: Compare *++p with ++*p. In *++p the pointer moves; in ++*p the integer in memory increments.",
        [
            (1, 4, "Array arr initialized. Pointer p points to arr[0] (0x1000).", {"p": "0x1000", "*p": 10}, {"stack": [{"name":"arr[0]","addr":"0x1000","val":10},{"name":"arr[1]","addr":"0x1004","val":20},{"name":"p","addr":"0x1010","val":"0x1000","pointsTo":"arr[0]"}]}),
            (2, 5, "Prefix ++ increments p to &arr[1] (0x1004) before value computation.", {"p": "0x1004"}, {"stack": [{"name":"p","addr":"0x1010","val":"0x1004","pointsTo":"arr[1]"}]}),
            (3, 5, "Dereference *p reads arr[1] (20), assigned to x.", {"x": 20, "*p": 20}, {"stack": [{"name":"x","addr":"0x1014","val":20},{"name":"p","addr":"0x1010","val":"0x1004","pointsTo":"arr[1]"}]}),
            (4, 6, "printf prints x (20) and *p (20).", {"stdout": "20 20"}, {"stack": [{"name":"stdout","val":"20 20"}]})
        ]
    )

    # Q004: Pre-Increment Dereferenced Value (++*p) -> Key D
    add_q(
        4, "CAT_PREC_EVAL", "Medium", "Pre-Increment Dereferenced Value (++*p)",
        "What is the output of the following program?",
        r"""#include <stdio.h>
int main() {
    int arr[] = {10, 20, 30};
    int *p = arr;
    int x = ++*p;
    printf("%d %d %d\n", x, arr[0], *p);
    return 0;
}""",
        5, "++*p", "Right-to-left associativity: ++(*p). The integer value at arr[0] is incremented to 11 first!",
        [
            ("A", "10 11 11", False, "Confused prefix ++ with postfix ++.", "Prefix ++ increments before returning the value; postfix would have returned 10."),
            ("B", "20 10 20", False, "Thought p advanced to arr[1].", "p is never incremented here; the increment applies to the dereferenced integer object."),
            ("C", "10 10 10", False, "Thought no mutation occurred in the array.", "arr[0] is modified in place via the pointer lvalue."),
            ("D", "11 11 11", True, "++*p groups right-to-left as ++(*p). arr[0] is incremented from 10 to 11, yielding 11 for x, while p stays at arr[0].", "")
        ],
        "Unary operators associate right-to-left: ++(*p). The integer at arr[0] is incremented to 11, and that value is assigned to x.",
        "ISO/IEC 9899:1999 §6.5.3.1",
        "Prefix ++ and unary * have equal precedence and associate from right to left. Therefore, ++*p is syntactically equivalent to ++(*p).\n\nMechanics:\n1. The unary dereference *p evaluates to the lvalue arr[0] (which currently holds 10).\n2. Prefix ++ increments the object designated by *p (arr[0]) in place by 1, updating its value to 11.\n3. The prefix ++ expression yields the newly incremented value (11).\n4. x is assigned 11.\n5. Since pointer p was never modified, p still points to arr[0]. Both arr[0] and *p evaluate to 11.\n\nExam Trap: Notice the distinction between ++*p (all 11s) and *++p (reads next array element 20).",
        [
            (1, 4, "Array arr initialized with {10, 20, 30}. p points to arr[0] (0x1000).", {"p": "0x1000", "*p": 10}, {"stack": [{"name":"arr[0]","addr":"0x1000","val":10},{"name":"arr[1]","addr":"0x1004","val":20},{"name":"p","addr":"0x1010","val":"0x1000","pointsTo":"arr[0]"}]}),
            (2, 5, "Dereference *p identifies arr[0]. Prefix ++ increments arr[0] from 10 to 11 in place.", {"arr[0]": 11, "*p": 11}, {"stack": [{"name":"arr[0]","addr":"0x1000","val":11}]}),
            (3, 5, "New value 11 is assigned to x. Pointer p unchanged at 0x1000.", {"x": 11, "p": "0x1000"}, {"stack": [{"name":"x","addr":"0x1014","val":11},{"name":"p","addr":"0x1010","val":"0x1000","pointsTo":"arr[0]"}]}),
            (4, 6, "printf prints x (11), arr[0] (11), and *p (11).", {"stdout": "11 11 11"}, {"stack": [{"name":"stdout","val":"11 11 11"}]})
        ]
    )

    # Q005: Short-Circuit Evaluation with Logical OR -> Key A
    add_q(
        5, "CAT_PREC_EVAL", "Tricky", "Short-Circuit Evaluation with Logical OR",
        "What is the output of the following program?",
        r"""#include <stdio.h>
int main() {
    int a = 1, b = 2;
    if (a++ || b++) {
        printf("%d %d\n", a, b);
    }
    return 0;
}""",
        5, "a++ || b++", "Because a++ evaluates to non-zero (1), logical OR short-circuits: b++ is NEVER evaluated!",
        [
            ("A", "2 2", True, "a++ evaluates to 1 (true) and increments a to 2; because 1 is true, || short-circuits and skips b++, leaving b at 2.", ""),
            ("B", "2 3", False, "Assumed both sides of logical OR (||) always execute.", "In ISO C, || guarantees short-circuit evaluation: if the left operand is non-zero, the right operand is strictly skipped."),
            ("C", "1 2", False, "Thought a++ did not take effect before entering the if block.", "Postfix increment side effect completes at the sequence point immediately following the condition test."),
            ("D", "1 3", False, "Thought a was skipped and only b executed.", "Logical operators evaluate strictly from left to right.")
        ],
        "|| evaluates left-to-right. A sequence point occurs after the left operand. Since a++ is 1 (true), b++ is never evaluated.",
        "ISO/IEC 9899:1999 §6.5.14#4",
        "The logical OR operator (||) guarantees left-to-right evaluation and introduces a sequence point between operands.\n\nDetailed Analysis:\n1. The left operand expression is a++. Postfix ++ yields the current value of a (1) and schedules an increment of a to 2.\n2. The sequence point after the first operand ensures that a becomes 2 immediately after the left operand is evaluated.\n3. Because 1 is non-zero (truthy in C), the logical OR condition is already determined to be true.\n4. By ISO C §6.5.14#4, if the first operand compares unequal to 0, the second operand is NOT evaluated (short-circuit).\n5. Thus, b++ is entirely bypassed, and b retains its initial value of 2.\n6. The body executes: printf prints 2 2.\n\nExam Trap: Many students mistakenly believe compiler optimization decides short-circuiting; it is actually a mandatory semantic guarantee of the C language.",
        [
            (1, 4, "Variables initialized on stack: a = 1, b = 2.", {"a": 1, "b": 2}, {"stack": [{"name":"a","addr":"0x1000","val":1},{"name":"b","addr":"0x1004","val":2}]}),
            (2, 5, "Left operand a++ evaluated: yields 1 (truthy). a increments to 2 at the sequence point.", {"a": 2, "left_result": 1}, {"stack": [{"name":"a","addr":"0x1000","val":2},{"name":"b","addr":"0x1004","val":2}]}),
            (3, 5, "Short-circuit triggered: right operand b++ is NOT evaluated. b remains 2.", {"b": 2, "branch": "taken"}, {"stack": [{"name":"b","addr":"0x1004","val":2}]}),
            (4, 6, "printf prints a (2) and b (2).", {"stdout": "2 2"}, {"stack": [{"name":"stdout","val":"2 2"}]})
        ]
    )

    # Q006: Short-Circuit Evaluation with Logical AND -> Key B
    add_q(
        6, "CAT_PREC_EVAL", "Tricky", "Short-Circuit Evaluation with Logical AND",
        "What is the output of the following program?",
        r"""#include <stdio.h>
int main() {
    int a = 0, b = 5;
    if (a && ++b) {
        printf("TRUE\n");
    }
    printf("%d %d\n", a, b);
    return 0;
}""",
        5, "a && ++b", "Because a is 0 (false), logical AND short-circuits: ++b is NEVER evaluated!",
        [
            ("A", "0 6", False, "Assumed ++b executed before or during the AND comparison.", "&& evaluates strictly left-to-right with short-circuiting; when the left operand is 0, the right operand is bypassed."),
            ("B", "0 5", True, "a is 0 (false), so logical AND short-circuits immediately. ++b never executes, leaving b at 5.", ""),
            ("C", "TRUE followed by 0 6", False, "Thought 0 && anything could evaluate to true.", "In C, 0 is false; 0 && anything is always 0."),
            ("D", "1 5", False, "Thought a was incremented.", "Variable a is never incremented in the code.")
        ],
        "&& evaluates left-to-right with short-circuit behavior. Since a == 0, ++b is never executed, preserving b = 5.",
        "ISO/IEC 9899:1999 §6.5.13#4",
        "The logical AND operator (&&) guarantees left-to-right evaluation and introduces a sequence point between the evaluation of its first and second operands.\n\nEvaluation Steps:\n1. Left operand a is evaluated. Since a is 0, its truth value is false (0).\n2. Under ISO C §6.5.13#4, if the first operand compares equal to 0, the second operand is NOT evaluated.\n3. Therefore, the prefix increment ++b is skipped completely, and no side effect occurs on b.\n4. The if condition evaluates to false (0), so the if-block is bypassed.\n5. Execution moves to line 8: printf prints a (0) and b (5).\n\nExam Trap: Look for side effects inside conditionals. Any side effect in the right-hand operand of && is skipped if the left operand is false.",
        [
            (1, 4, "Variables initialized on stack: a = 0, b = 5.", {"a": 0, "b": 5}, {"stack": [{"name":"a","addr":"0x1000","val":0},{"name":"b","addr":"0x1004","val":5}]}),
            (2, 5, "Left operand of && is evaluated: a is 0 (false).", {"left_cond": 0}, {"stack": [{"name":"a","addr":"0x1000","val":0}]}),
            (3, 5, "Short-circuit: right operand ++b is completely skipped. b remains 5.", {"b": 5, "if_cond": 0}, {"stack": [{"name":"b","addr":"0x1004","val":5}]}),
            (4, 8, "printf prints a (0) and b (5).", {"stdout": "0 5"}, {"stack": [{"name":"stdout","val":"0 5"}]})
        ]
    )

    # Q007: Precedence of Logical AND vs Logical OR -> Key C
    add_q(
        7, "CAT_PREC_EVAL", "Tricky", "Precedence of Logical AND vs Logical OR",
        "What is the output of the following program?",
        r"""#include <stdio.h>
int main() {
    int a = 1, b = 0, c = 0;
    int res = a || b && c++;
    printf("%d %d\n", res, c);
    return 0;
}""",
        5, "a || b && c++", "&& has higher precedence than ||, grouping as: a || (b && c++). Since a is 1, short-circuit skips (b && c++)!",
        [
            ("A", "1 1", False, "Thought && executed first chronologically and evaluated c++.", "Precedence dictates grammar grouping (AST construction), but operator evaluation order is strictly governed by ||."),
            ("B", "0 0", False, "Thought the expression evaluated to false.", "Since a is 1, 1 || anything evaluates to 1 (true)."),
            ("C", "1 0", True, "&& binds tighter than ||, parsing as a || (b && c++). But || evaluates left-to-right; since a is 1, the entire right side (b && c++) is short-circuited and c remains 0.", ""),
            ("D", "0 1", False, "Thought the result was 0 and c was incremented.", "Combines both incorrect precedence logic and missed short-circuiting.")
        ],
        "&& binds tighter than ||, meaning the expression is parsed as a || (b && c++). However, || evaluates left-to-right with short-circuiting.",
        "ISO/IEC 9899:1999 §6.5.13 & §6.5.14",
        "A classic computer science misconception is confusing operator precedence with execution order.\n\nPrecedence vs Order of Evaluation:\n- Precedence determines how operands group with operators in the Abstract Syntax Tree (AST). Because && has higher precedence than ||, the expression parses as: a || (b && c++).\n- However, execution order is determined by the semantics of the operators. The || operator evaluates its left operand first (a).\n- Since a == 1 (true), the logical OR is already satisfied.\n- The language specification mandates that the entire right-hand operand (b && c++) is NOT evaluated.\n- Hence, neither b nor c++ is ever touched. c remains 0, and res is 1.\n\nExam Trap: Never evaluate a subexpression just because it has higher precedence. The controlling short-circuit operator determines whether the subexpression even runs.",
        [
            (1, 4, "Variables initialized on stack: a = 1, b = 0, c = 0.", {"a": 1, "b": 0, "c": 0}, {"stack": [{"name":"a","val":1},{"name":"b","val":0},{"name":"c","val":0}]}),
            (2, 5, "Expression parsed as a || (b && c++). Left operand a (1) is evaluated first.", {"a": 1}, {"stack": [{"name":"a","val":1}]}),
            (3, 5, "Because a is 1, || short-circuits. Entire subexpression (b && c++) is skipped.", {"res": 1, "c": 0}, {"stack": [{"name":"res","val":1},{"name":"c","val":0}]}),
            (4, 6, "printf prints res (1) and c (0).", {"stdout": "1 0"}, {"stack": [{"name":"stdout","val":"1 0"}]})
        ]
    )

    # Q008: Comma Operator Value Extraction -> Key D
    add_q(
        8, "CAT_PREC_EVAL", "Easy", "Comma Operator Value Extraction",
        "What is the value of x after execution?",
        r"""#include <stdio.h>
int main() {
    int x = (10, 20, 30);
    printf("%d\n", x);
    return 0;
}""",
        4, "(10, 20, 30)", "The comma operator evaluates each expression and yields the value of the LAST expression!",
        [
            ("A", "10", False, "Thought the comma operator takes the first value.", "The comma operator evaluates sequentially from left to right and discards all but the rightmost result."),
            ("B", "60", False, "Thought it summed the numbers.", "Comma is an expression sequencing operator, not an arithmetic sum."),
            ("C", "Compile error", False, "Thought multiple commas inside parentheses are illegal in C.", "The comma operator is fully valid inside parentheses."),
            ("D", "30", True, "In (10, 20, 30), the comma operators evaluate 10 (discarded), then 20 (discarded), and finally yield 30 to assign to x.", "")
        ],
        "The comma operator has lowest precedence. Inside parentheses, expressions are evaluated left-to-right, returning the last.",
        "ISO/IEC 9899:1999 §6.5.17",
        "The comma operator (,) has the lowest precedence of all operators in the C language.\n\nC Standard Semantics:\n- In a comma expression E1, E2, the left expression E1 is evaluated as a void expression (its value is discarded).\n- There is a sequence point after the evaluation of E1.\n- Then E2 is evaluated, and its type and value become the result of the entire expression.\n\nExecution Details:\nIn (10, 20, 30):\n1. 10 is evaluated and discarded.\n2. 20 is evaluated and discarded.\n3. 30 is evaluated and returned as the result of the parenthesized expression.\n4. 30 is stored in integer variable x.\n\nExam Trap: Parentheses are mandatory when using the comma operator in an assignment; otherwise, the assignment operator binds tighter than the comma (as seen in Q009).",
        [
            (1, 4, "Expression (10, 20, 30) begins evaluation inside parentheses.", None, {"stack": []}),
            (2, 4, "Left operand 10 evaluated and discarded; middle operand 20 evaluated and discarded.", {"temp_discarded": [10, 20]}, {"stack": []}),
            (3, 4, "Rightmost operand 30 evaluated and returned; x is assigned 30.", {"x": 30}, {"stack": [{"name":"x","addr":"0x1000","val":30}]}),
            (4, 5, "printf prints 30.", {"stdout": "30"}, {"stack": [{"name":"stdout","val":"30"}]})
        ]
    )

    # Q009: Comma Operator vs Assignment Precedence -> Key A (Fixed unused variable b)
    add_q(
        9, "CAT_PREC_EVAL", "Tricky", "Comma Operator vs Assignment Precedence",
        "What is the output of the following program?",
        r"""#include <stdio.h>
int main() {
    int a;
    a = 1, 2, 3;
    printf("%d\n", a);
    return 0;
}""",
        5, "a = 1, 2, 3;", "Assignment (=) has higher precedence than comma (,). This parses as (a = 1), 2, 3;",
        [
            ("A", "1", True, "Because = has higher precedence than comma, 'a = 1' executes first, assigning 1 to a; then 2 and 3 are evaluated and discarded.", ""),
            ("B", "3", False, "Confused with a = (1, 2, 3). Without parentheses, = binds to 1.", "Parentheses are required to assign the result of the comma operator to a variable."),
            ("C", "2", False, "Selected the middle operand.", "The comma operator never yields a middle operand."),
            ("D", "Compile error", False, "Thought an unparenthesized comma expression is invalid C syntax.", "Comma expressions as statements are valid C; the compiler evaluates each and discards unused values.")
        ],
        "Assignment (=) has higher precedence (level 14) than comma (level 16). Hence, 'a = 1' executes first, then 2 and 3 are discarded.",
        "ISO/IEC 9899:1999 §6.5.16 & §6.5.17",
        "In the C operator hierarchy, assignment operators (=, +=, etc.) reside at precedence level 14, whereas the comma operator (,) sits at the very bottom (precedence level 16).\n\nParsing & Evaluation:\n1. Without enclosing parentheses, the expression a = 1, 2, 3; is parsed by the C grammar as:\n   (a = 1), 2, 3;\n2. First, the assignment subexpression a = 1 evaluates, placing 1 into variable a.\n3. At the sequence point of the first comma, a is 1.\n4. Next, 2 is evaluated as a discarded void expression.\n5. Next, 3 is evaluated as a discarded void expression.\n6. printf prints the value of a, which is 1.\n\nContrast:\n- a = 1, 2, 3; assigns 1 to a.\n- a = (1, 2, 3); assigns 3 to a.\n\nCode Hygiene Note: The unused variable declaration was cleaned up to ensure zero compiler warnings under -Wall -Wextra.",
        [
            (1, 4, "Integer a declared on the stack.", {"a": "uninitialized"}, {"stack": [{"name":"a","addr":"0x1000","val":"?"}]}),
            (2, 5, "Assignment a = 1 binds first due to precedence. a is set to 1.", {"a": 1}, {"stack": [{"name":"a","addr":"0x1000","val":1}]}),
            (3, 5, "Comma operator sequentially evaluates 2 and 3 as discarded expressions.", {"discarded": [2, 3]}, {"stack": [{"name":"a","addr":"0x1000","val":1}]}),
            (4, 6, "printf prints a (1).", {"stdout": "1"}, {"stack": [{"name":"stdout","val":"1"}]})
        ]
    )

    # Q010: Chained Ternary Associativity -> Key B
    add_q(
        10, "CAT_PREC_EVAL", "Medium", "Chained Ternary Associativity",
        "What is the output of the following program?",
        r"""#include <stdio.h>
int main() {
    int a = 1, b = 2, c = 3;
    int res = a ? b : c ? 10 : 20;
    printf("%d\n", res);
    return 0;
}""",
        5, "a ? b : c ? 10 : 20", "The conditional ternary operator associates RIGHT-TO-LEFT: a ? b : (c ? 10 : 20)!",
        [
            ("A", "10", False, "Assumed left-to-right associativity: (a ? b : c) ? 10 : 20, where 2 is true, yielding 10.", "The conditional operator associates right-to-left in C, not left-to-right."),
            ("B", "2", True, "Ternary operator associates right-to-left: a ? b : (c ? 10 : 20). Since a is 1 (true), b (2) is chosen immediately, and the nested ternary is never evaluated.", ""),
            ("C", "20", False, "Thought c evaluated to false.", "The entire right-hand branch is bypassed because a is true."),
            ("D", "3", False, "Selected c directly.", "c is part of the bypassed alternate branch.")
        ],
        "The conditional operator associates right-to-left: a ? b : (c ? 10 : 20). Because a is non-zero, b (2) is returned.",
        "ISO/IEC 9899:1999 §6.5.15",
        "The conditional operator (?:) is one of the few C operators that associates right-to-left.\n\nGrammar and AST Construction:\n- An expression of the form: E1 ? E2 : E3 ? E4 : E5\n- Parses strictly as: E1 ? E2 : (E3 ? E4 : E5)\n\nExecution Details:\n1. First, E1 (variable a) is evaluated.\n2. Since a == 1 (non-zero / true), the conditional operator selects its first alternative expression (E2, variable b).\n3. The value of b is 2, which becomes the final result of the entire expression and is assigned to res.\n4. By ISO C §6.5.15#4, exactly one of the second and third operands is evaluated. The entire subexpression (c ? 10 : 20) is NOT evaluated.\n5. printf outputs 2.\n\nExam Trap: In languages with left-associative ternary operators (like PHP), this would evaluate as (a ? b : c) ? 10 : 20 = 2 ? 10 : 20 = 10. In C and C++, it is always right-associative.",
        [
            (1, 4, "Variables initialized on stack: a = 1, b = 2, c = 3.", {"a": 1, "b": 2, "c": 3}, {"stack": [{"name":"a","val":1},{"name":"b","val":2},{"name":"c","val":3}]}),
            (2, 5, "Right-to-left grouping parses as a ? b : (c ? 10 : 20). Condition a is evaluated: 1 (true).", {"cond_a": 1}, {"stack": [{"name":"a","val":1}]}),
            (3, 5, "True branch b (2) evaluated and assigned to res. False branch (c ? 10 : 20) skipped.", {"res": 2}, {"stack": [{"name":"res","val":2}]}),
            (4, 6, "printf prints res (2).", {"stdout": "2"}, {"stack": [{"name":"stdout","val":"2"}]})
        ]
    )

    # Q011: Bitwise Shift vs Arithmetic Addition Precedence -> Key C
    add_q(
        11, "CAT_PREC_EVAL", "Tricky", "Bitwise Shift vs Arithmetic Addition Precedence",
        "What is the output of the following program?",
        r"""#include <stdio.h>
int main() {
    int x = 1 << 2 + 3;
    printf("%d\n", x);
    return 0;
}""",
        4, "1 << 2 + 3", "Arithmetic + has HIGHER precedence than bitwise <<! This evaluates as 1 << (2 + 3) = 1 << 5 = 32!",
        [
            ("A", "7", False, "Assumed left-to-right evaluation: (1 << 2) + 3 = 4 + 3 = 7.", "Arithmetic addition (+) has higher precedence than bitwise shift (<<)."),
            ("B", "11", False, "Miscalculated bit shifting arithmetic.", "1 << 5 equals 2^5 = 32."),
            ("C", "32", True, "+ binds tighter than <<, so 2 + 3 evaluates to 5 first; then 1 << 5 evaluates to 32.", ""),
            ("D", "5", False, "Thought 1 << 2 was 2, plus 3 = 5.", "1 << 2 is 4, but precedence forces 2 + 3 first.")
        ],
        "Arithmetic addition (+) has higher precedence (level 4) than bitwise shift (<<, level 5). 1 << 2 + 3 evaluates as 1 << (2 + 3) = 1 << 5 = 32.",
        "ISO/IEC 9899:1999 §6.5.6 & §6.5.7",
        "A notorious pitfall in C system programming is the precedence hierarchy of bitwise operators relative to arithmetic operators.\n\nPrecedence Comparison:\n- Level 4: Additive operators (+, -)\n- Level 5: Shift operators (<<, >>)\n\nStep-by-step Evaluation:\n1. The compiler parses 1 << 2 + 3 as 1 << (2 + 3).\n2. The addition 2 + 3 is computed first, yielding 5.\n3. The bitwise left-shift operation 1 << 5 is computed next.\n4. 1 in binary is 00000001; shifting left by 5 bit positions produces 00100000 (binary) = 32 (decimal).\n5. 32 is stored in x and printed.\n\nExam Trap: Dennis Ritchie noted that bitwise operators were given lower precedence than arithmetic operators early in C's history. Always use explicit parentheses for bitwise logic: (1 << 2) + 3 if you intended 7.",
        [
            (1, 4, "Expression 1 << 2 + 3 parsed with + taking precedence over <<: 1 << (2 + 3).", None, {"stack": []}),
            (2, 4, "Arithmetic addition computes 2 + 3 = 5.", {"add_res": 5}, {"stack": []}),
            (3, 4, "Bitwise left shift computes 1 << 5 = 32. Assigned to x.", {"x": 32}, {"stack": [{"name":"x","addr":"0x1000","val":32}]}),
            (4, 5, "printf prints 32.", {"stdout": "32"}, {"stack": [{"name":"stdout","val":"32"}]})
        ]
    )

    # Q012: Mathematical Relational Chaining Fallacy -> Key D
    add_q(
        12, "CAT_PREC_EVAL", "Tricky", "Mathematical Relational Chaining Fallacy",
        "What is the output of the following program?",
        r"""#include <stdio.h>
int main() {
    int x = 25;
    if (10 < x < 20) {
        printf("INSIDE\n");
    } else {
        printf("OUTSIDE\n");
    }
    return 0;
}""",
        5, "10 < x < 20", "Relational operators associate LEFT-TO-RIGHT: (10 < 25) evaluates to 1 (true), then 1 < 20 is TRUE!",
        [
            ("A", "OUTSIDE", False, "Assumed mathematical interval check 10 < 25 < 20 (which is false).", "C does not support mathematical chained inequalities; it evaluates (10 < x) < 20."),
            ("B", "Compile error", False, "Thought chaining < operators is illegal syntax in C.", "Chained relational operators are syntactically valid C expressions."),
            ("C", "Undefined Behavior", False, "Thought chained comparisons cause undefined behavior.", "The behavior is completely well-defined by the standard, though logically flawed."),
            ("D", "INSIDE", True, "Relational < associates left-to-right: (10 < x) evaluates to 1 (true); then 1 < 20 evaluates to 1 (true), so the if-branch executes.", "")
        ],
        "Relational operators associate left-to-right. (10 < x) evaluates to 1 (true). Then 1 < 20 evaluates to 1 (true).",
        "ISO/IEC 9899:1999 §6.5.8",
        "In mathematics, 10 < x < 20 asserts that x is strictly between 10 and 20. In C, this is NOT an interval test!\n\nRelational Semantics in C:\n- Relational operators (<, <=, >, >=) have left-to-right associativity.\n- The expression 10 < x < 20 is grouped as: (10 < x) < 20.\n\nEvaluation Trace:\n1. Left relational check: 10 < x with x = 25.\n2. 10 < 25 is mathematically true, so the < operator yields integer 1.\n3. The expression becomes: 1 < 20.\n4. 1 < 20 is true, so the second < operator yields integer 1.\n5. The if condition receives 1 (truthy), taking the if-branch.\n6. Output is INSIDE, even though 25 is outside (10, 20)!\n\nCorrect Idiom: To check an interval in C, use logical AND: (10 < x && x < 20).",
        [
            (1, 4, "x initialized to 25 on the stack.", {"x": 25}, {"stack": [{"name":"x","addr":"0x1000","val":25}]}),
            (2, 5, "Left subexpression evaluated: 10 < 25 yields integer 1.", {"step1": "(10 < 25) == 1"}, {"stack": [{"name":"x","val":25}]}),
            (3, 5, "Right subexpression evaluated: 1 < 20 yields integer 1 (true). Condition passes.", {"step2": "(1 < 20) == 1", "branch": "if"}, {"stack": [{"name":"x","val":25}]}),
            (4, 6, "printf prints INSIDE.", {"stdout": "INSIDE"}, {"stack": [{"name":"stdout","val":"INSIDE"}]})
        ]
    )

    # Q013: Bitwise AND Precedence with Equality -> Key A
    add_q(
        13, "CAT_PREC_EVAL", "Tricky", "Bitwise AND Precedence with Equality",
        "What is the output of the following program?",
        r"""#include <stdio.h>
int main() {
    int flag = 4;
    if (flag & 4 == 4) {
        printf("YES\n");
    } else {
        printf("NO\n");
    }
    return 0;
}""",
        5, "flag & 4 == 4", "Equality == has HIGHER precedence than bitwise &! This evaluates as flag & (4 == 4) -> 4 & 1 -> 0 (false)!",
        [
            ("A", "NO", True, "== binds tighter than &, parsing as flag & (4 == 4). 4 == 4 is 1; flag & 1 is 4 & 1 = 0 (false), so the else branch prints NO.", ""),
            ("B", "YES", False, "Assumed (flag & 4) == 4, where 4 == 4 is true.", "Equality (==) has higher precedence than bitwise AND (&)."),
            ("C", "Compile error", False, "Thought mixing bitwise and equality operators without parentheses is illegal.", "Valid C syntax; compilers may emit a -Wparentheses warning."),
            ("D", "Undefined Behavior", False, "Thought expression caused undefined behavior.", "Expression has strictly standard-defined deterministic behavior.")
        ],
        "== has higher precedence (level 7) than bitwise & (level 8). The expression parses as flag & (4 == 4) = 4 & 1 = 0.",
        "ISO/IEC 9899:1999 §6.5.9 & §6.5.10",
        "This is one of the most frequent security bugs and exam traps in C programming.\n\nPrecedence Levels:\n- Level 7: Equality operators (==, !=)\n- Level 8: Bitwise AND (&)\n\nExecution Details:\n1. The parser groups flag & 4 == 4 as flag & (4 == 4).\n2. The equality check 4 == 4 evaluates first, producing 1.\n3. The expression becomes flag & 1.\n4. Since flag is 4 (binary 00000100), bitwise AND with 1 (00000001) produces 0.\n5. The if condition receives 0 (false), directing control to the else branch.\n6. printf prints NO.\n\nCorrect Pattern: Always place parentheses around bitwise operations: if ((flag & 4) == 4).",
        [
            (1, 4, "flag initialized to 4 (binary 00000100).", {"flag": 4}, {"stack": [{"name":"flag","addr":"0x1000","val":4}]}),
            (2, 5, "Equality == evaluated first due to precedence: (4 == 4) evaluates to 1.", {"eq_result": 1}, {"stack": [{"name":"flag","val":4}]}),
            (3, 5, "Bitwise & evaluated: flag & 1 = 4 & 1 = 0 (false). Else branch taken.", {"cond": 0, "branch": "else"}, {"stack": [{"name":"flag","val":4}]}),
            (4, 8, "printf prints NO.", {"stdout": "NO"}, {"stack": [{"name":"stdout","val":"NO"}]})
        ]
    )

    # Q014: Increment in Expression Output -> Key B
    add_q(
        14, "CAT_PREC_EVAL", "Tricky", "Increment in Expression Output",
        "What is the output of the following program?",
        r"""#include <stdio.h>
int main() {
    int a = 5;
    int b = ++a + 10;
    int c = a++ + 10;
    printf("%d %d %d\n", a, b, c);
    return 0;
}""",
        6, "a++ + 10", "++a increments immediately to 6 before addition; a++ uses current value (6) then increments to 7.",
        [
            ("A", "7 16 17", False, "Thought a++ incremented before addition in c.", "Postfix a++ yields its un-incremented value (6) to the addition, so c = 6 + 10 = 16."),
            ("B", "7 16 16", True, "In b: ++a increments a to 6, b = 6 + 10 = 16. In c: a++ yields 6, c = 6 + 10 = 16, then a increments to 7. Output is 7 16 16.", ""),
            ("C", "6 16 16", False, "Forgot that a++ increments a after line 6.", "a undergoes two increments across lines 5 and 6, ending at 7."),
            ("D", "7 15 16", False, "Thought ++a returned old value 5.", "Prefix ++ increments before returning the value.")
        ],
        "Line 5: ++a increments a to 6, b = 6 + 10 = 16. Line 6: a++ yields 6 for c = 6 + 10 = 16, then increments a to 7.",
        "ISO/IEC 9899:1999 §6.5.2.4 & §6.5.3.1",
        "This question isolates the difference between prefix and postfix increment across separate statements with distinct sequence points.\n\nStep-by-Step Analysis:\n1. Line 4: a is initialized to 5.\n2. Line 5: ++a is evaluated. Prefix ++ increments a from 5 to 6 and yields 6. 6 + 10 = 16 is stored in b.\n3. Sequence point at semicolon: a is 6, b is 16.\n4. Line 6: a++ + 10 is evaluated. Postfix ++ yields the current value of a (6) for the addition expression. 6 + 10 = 16 is stored in c.\n5. Sequence point at semicolon: side effect of a++ takes effect, incrementing a from 6 to 7.\n6. Line 7: printf prints a (7), b (16), and c (16).\n\nExam Note: Because these increments occur in separate statements separated by sequence points, this code is 100% well-defined and exhibits zero undefined behavior.",
        [
            (1, 4, "a initialized to 5 on stack.", {"a": 5}, {"stack": [{"name":"a","addr":"0x1000","val":5}]}),
            (2, 5, "++a increments a to 6, then adds 10 -> b = 16.", {"a": 6, "b": 16}, {"stack": [{"name":"a","addr":"0x1000","val":6},{"name":"b","addr":"0x1004","val":16}]}),
            (3, 6, "a++ yields 6 for addition with 10 -> c = 16. At semicolon, a increments to 7.", {"a": 7, "c": 16}, {"stack": [{"name":"a","addr":"0x1000","val":7},{"name":"b","addr":"0x1004","val":16},{"name":"c","addr":"0x1008","val":16}]}),
            (4, 7, "printf prints a (7), b (16), c (16).", {"stdout": "7 16 16"}, {"stack": [{"name":"stdout","val":"7 16 16"}]})
        ]
    )

    # =========================================================================
    # CAT_PTR_ARR (Q015 - Q032): Pointers, Arrays, and Memory Layout
    # =========================================================================

    # Q015: Array Decay to Pointer in Function Parameter -> Key C
    add_q(
        15, "CAT_PTR_ARR", "Tricky", "Array Decay to Pointer in Function Parameter",
        "On a 64-bit architecture, what is the output of the following program?",
        r"""#include <stdio.h>
void func(int arr[10]) {
    printf("%zu\n", sizeof(arr));
}
int main() {
    int arr[10];
    func(arr);
    return 0;
}""",
        3, "sizeof(arr)", "In function parameter lists, int arr[10] is purely syntactic sugar for int *arr! sizeof(arr) returns pointer size (8 bytes)!",
        [
            ("A", "40", False, "Thought sizeof(arr) calculates 10 * sizeof(int) = 40 bytes.", "In function parameter declarations, arrays decay into pointers; sizeof yields the size of the pointer itself."),
            ("B", "10", False, "Thought sizeof returns the element count 10.", "sizeof yields byte size, never array length, and arr is a pointer here."),
            ("C", "8", True, "In C function parameters, int arr[10] is adjusted by the compiler to int *arr. On 64-bit systems, sizeof(int*) is 8 bytes.", ""),
            ("D", "4", False, "Thought pointers are 4 bytes or confused with sizeof(int).", "On 64-bit architectures, pointers are 8 bytes wide (LP64 / LLP64).")
        ],
        "In function parameters, array syntax decays to a pointer (int *arr). On a 64-bit architecture, sizeof(int*) is 8 bytes.",
        "ISO/IEC 9899:1999 §6.7.5.3#7",
        "Array Parameter Decay Rule:\nUnder ISO C §6.7.5.3#7, a declaration of a parameter as 'array of type' is automatically adjusted by the compiler to 'qualified pointer to type'.\n\nCompilation Adjustment:\n- void func(int arr[10]) is rewritten by the compiler identically as:\n  void func(int *arr)\n- The dimension 10 is completely ignored by the compiler for sizing.\n- Inside func, arr is a local pointer variable of type int*.\n- sizeof(arr) therefore evaluates to sizeof(int*).\n- On a 64-bit target (x86-64), pointers are 8 bytes in size.\n- Contrast with main(): inside main(), sizeof(arr) is 10 * sizeof(int) = 40 bytes because arr has not decayed.\n\nExam Note: To pass array size safely to functions in C, you must always pass the length as a second parameter: void func(int *arr, size_t n).",
        [
            (1, 7, "In main(): arr allocated as true array of 10 ints (40 bytes at 0x2000).", {"main_arr_size": 40}, {"stack": [{"name":"main.arr","addr":"0x2000","size":40,"type":"int[10]"}]}),
            (2, 8, "func(arr) called: array name decays to pointer &arr[0] (0x2000). Passed into func's stack frame.", {"param_arr": "0x2000"}, {"stack": [{"name":"func.arr","addr":"0x1FF0","val":"0x2000","pointsTo":"main.arr[0]","type":"int*"}]}),
            (3, 3, "Inside func: arr is int*. sizeof(arr) queries pointer width on 64-bit architecture -> 8 bytes.", {"sizeof_param": 8}, {"stack": [{"name":"func.arr","size":8}]}),
            (4, 4, "printf prints 8.", {"stdout": "8"}, {"stack": [{"name":"stdout","val":"8"}]})
        ]
    )

    # Q016: Difference between arr and &arr Stride -> Key D
    add_q(
        16, "CAT_PTR_ARR", "Nightmare", "Difference between arr and &arr Stride",
        "What is the output of the following program?",
        r"""#include <stdio.h>
int main() {
    int arr[5] = {1, 2, 3, 4, 5};
    int *p1 = (int*)(arr + 1);
    int *p2 = (int*)(&arr + 1);
    printf("%d %d\n", *p1, *(p2 - 1));
    return 0;
}""",
        5, "&arr + 1", "arr + 1 advances by 1 int (4 bytes). &arr + 1 advances by the ENTIRE ARRAY of 5 ints (20 bytes)!",
        [
            ("A", "2 2", False, "Thought &arr and arr have identical pointer types and strides.", "While arr and &arr have the same numerical memory address, their types differ: int* vs int(*)[5]."),
            ("B", "1 5", False, "Thought arr + 1 stayed at index 0.", "arr + 1 points to arr[1], whose value is 2."),
            ("C", "2 1", False, "Thought p2 - 1 pointed back to the beginning of the array.", "p2 is past index 4, so p2 - 1 points to arr[4] (5)."),
            ("D", "2 5", True, "arr + 1 advances by 1 int to arr[1] (2). &arr has type int(*)[5], so &arr + 1 strides by 5 ints to one-past-the-end. (p2 - 1) points to arr[4] (5).", "")
        ],
        "arr decays to int*, so arr + 1 advances by sizeof(int). &arr is pointer to array of 5 ints, so &arr + 1 strides by 5 * sizeof(int).",
        "ISO/IEC 9899:1999 §6.3.2.1#3 & §6.5.6",
        "This question tests the critical distinction between pointer values and pointer types.\n\nAddress vs Type:\n- arr decays to a pointer to its first element: type int*, value 0x1000.\n- &arr is a pointer to the entire array: type int(*)[5], value 0x1000.\n- Both evaluate to the exact same numerical memory address, but their stride scales differently under pointer arithmetic!\n\nPointer Arithmetic Details:\n1. arr + 1: Stride is 1 * sizeof(int) = 4 bytes. Address is 0x1004 (&arr[1]). *p1 dereferences arr[1], yielding 2.\n2. &arr + 1: Stride is 1 * sizeof(int[5]) = 20 bytes. Address is 0x1000 + 20 = 0x1014 (one past the end of the array, just after arr[4]).\n3. Cast to int* stores 0x1014 in p2.\n4. p2 - 1: Stride of int* subtraction is 1 * sizeof(int) = 4 bytes. Address becomes 0x1014 - 4 = 0x1010 (&arr[4]).\n5. *(p2 - 1) dereferences arr[4], yielding 5.\n6. printf prints 2 5.",
        [
            (1, 4, "Array arr allocated at 0x1000 with elements {1, 2, 3, 4, 5}.", {"arr": [1, 2, 3, 4, 5]}, {"stack": [{"name":"arr[0]","addr":"0x1000","val":1},{"name":"arr[1]","addr":"0x1004","val":2},{"name":"arr[2]","addr":"0x1008","val":3},{"name":"arr[3]","addr":"0x100C","val":4},{"name":"arr[4]","addr":"0x1010","val":5}]}),
            (2, 5, "arr + 1 advances by sizeof(int) (4 bytes) to 0x1004. p1 points to arr[1].", {"p1": "0x1004", "*p1": 2}, {"stack": [{"name":"p1","addr":"0x1020","val":"0x1004","pointsTo":"arr[1]"}]}),
            (3, 6, "&arr + 1 advances by sizeof(int[5]) (20 bytes) to 0x1014. Cast to int* -> p2 = 0x1014.", {"p2": "0x1014"}, {"stack": [{"name":"p2","addr":"0x1028","val":"0x1014","pointsTo":"arr[5] (one-past-end)"}]}),
            (4, 7, "p2 - 1 steps backward by 4 bytes to 0x1010 (&arr[4]). *(p2 - 1) yields 5.", {"*(p2-1)": 5, "stdout": "2 5"}, {"stack": [{"name":"p2-1","val":"0x1010","pointsTo":"arr[4]"}]})
        ]
    )

    # Q017: Commutative Array Indexing (i[arr]) -> Key A
    add_q(
        17, "CAT_PTR_ARR", "Tricky", "Commutative Array Indexing (i[arr])",
        "What is the output of the following program?",
        r"""#include <stdio.h>
int main() {
    int arr[] = {10, 20, 30, 40, 50};
    printf("%d\n", 3[arr]);
    return 0;
}""",
        4, "3[arr]", "By definition in C, E1[E2] is identical to (*((E1) + (E2))). Addition is commutative, so 3[arr] == arr[3]!",
        [
            ("A", "40", True, "In C, E1[E2] is strictly defined as (*((E1) + (E2))). Since addition is commutative, 3[arr] == *(3 + arr) == *(arr + 3) == arr[3] = 40.", ""),
            ("B", "30", False, "Off-by-one count: 0, 1, 2, 3.", "Index 3 corresponds to the fourth element: 10 (0), 20 (1), 30 (2), 40 (3)."),
            ("C", "Compile error", False, "Thought placing an integer before brackets is invalid syntax.", "The C grammar explicitly permits any expression before the subscript brackets."),
            ("D", "Undefined Behavior", False, "Thought 3[arr] causes memory corruption.", "Standard C guarantees 3[arr] is identical to arr[3].")
        ],
        "The subscript operator [] is defined as E1[E2] == (*((E1) + (E2))). Commutativity of pointer-integer addition makes 3[arr] == arr[3].",
        "ISO/IEC 9899:1999 §6.5.2.1#2",
        "Subscript Definition in ISO C:\nSection 6.5.2.1 paragraph 2 states verbatim:\n'A postfix expression followed by an expression in square brackets [] is a subscripted designation of an element of an array object. The definition of the subscript operator [] is that E1[E2] is identical to (*((E1)+(E2)))'\n\nMathematical Symmetry:\n- Under pointer arithmetic rules, adding an integer to a pointer is commutative: (arr + 3) produces the exact same address as (3 + arr).\n- Therefore:\n  arr[3] == *(arr + 3)\n  3[arr] == *(3 + arr)\n- Since *(arr + 3) == *(3 + arr), 3[arr] accesses arr[3].\n- In the array {10, 20, 30, 40, 50}:\n  Index 0 = 10\n  Index 1 = 20\n  Index 2 = 30\n  Index 3 = 40\n- The output is 40.\n\nExam Note: While 3[arr] is valid C, using it in production is bad style. However, exam questions frequently test this exact identity to verify your understanding of array subscript definition.",
        [
            (1, 4, "Array arr initialized on stack: arr[0]=10, arr[1]=20, arr[2]=30, arr[3]=40, arr[4]=50.", {"arr[3]": 40}, {"stack": [{"name":"arr[0]","addr":"0x1000","val":10},{"name":"arr[1]","addr":"0x1004","val":20},{"name":"arr[2]","addr":"0x1008","val":30},{"name":"arr[3]","addr":"0x100C","val":40},{"name":"arr[4]","addr":"0x1010","val":50}]}),
            (2, 4, "Subscript expansion: 3[arr] expands to *((3) + (arr)).", {"expansion": "*(3 + arr)"}, {"stack": []}),
            (3, 4, "Commutative addition: 3 + arr == arr + 3 -> address 0x100C (&arr[3]).", {"target_addr": "0x100C"}, {"stack": []}),
            (4, 5, "Dereference *(0x100C) yields 40. printf prints 40.", {"stdout": "40"}, {"stack": [{"name":"stdout","val":"40"}]})
        ]
    )

    # Q018: Negative Array Indexing with Offset Pointer -> Key B
    add_q(
        18, "CAT_PTR_ARR", "Medium", "Negative Array Indexing with Offset Pointer",
        "What is the output of the following program?",
        r"""#include <stdio.h>
int main() {
    int arr[] = {10, 20, 30, 40, 50};
    int *p = &arr[2];
    printf("%d %d\n", p[-1], p[1]);
    return 0;
}""",
        5, "p[-1]", "p[-1] evaluates to *(p - 1), which accesses the preceding element arr[1] (20)!",
        [
            ("A", "30 40", False, "Thought p[-1] was ignored or clamped to 0.", "Negative indices are legal on pointers; p[-1] steps back one element."),
            ("B", "20 40", True, "p points to arr[2] (30). p[-1] expands to *(p - 1) = arr[1] (20); p[1] expands to *(p + 1) = arr[3] (40).", ""),
            ("C", "10 50", False, "Jumped to extreme ends of the array.", "Indices -1 and 1 step by exactly 1 element backward and forward."),
            ("D", "Compile error", False, "Thought negative subscripts are a compilation error in C.", "Subscripts can be negative as long as the computed address remains within the allocated array bounds.")
        ],
        "p[-1] is defined as *(p - 1). Since p points to arr[2], *(p - 1) is arr[1] (20) and *(p + 1) is arr[3] (40).",
        "ISO/IEC 9899:1999 §6.5.2.1",
        "Negative Subscripts in C:\nBecause E1[E2] is strictly defined as *(E1 + E2), negative index values are completely valid as long as the resulting pointer points to an element within the same array object.\n\nMemory Analysis:\n1. Array arr has elements: arr[0]=10, arr[1]=20, arr[2]=30, arr[3]=40, arr[4]=50.\n2. Pointer p is initialized to &arr[2] (address 0x1008).\n3. p[-1] evaluates as *(p + (-1)) = *(p - 1). Subtracting 1 int advances backward by 4 bytes to 0x1004 (&arr[1]). The value is 20.\n4. p[1] evaluates as *(p + 1). Adding 1 int advances forward by 4 bytes to 0x100C (&arr[3]). The value is 40.\n5. printf outputs 20 40.\n\nSafety Constraint: Calling arr[-1] directly on the base array address is undefined behavior because it computes an address before the start of the array. But on an offset pointer p = &arr[2], p[-1] is safely within bounds.",
        [
            (1, 4, "Array arr initialized at 0x1000.", {"arr": [10, 20, 30, 40, 50]}, {"stack": [{"name":"arr[0]","addr":"0x1000","val":10},{"name":"arr[1]","addr":"0x1004","val":20},{"name":"arr[2]","addr":"0x1008","val":30},{"name":"arr[3]","addr":"0x100C","val":40},{"name":"arr[4]","addr":"0x1010","val":50}]}),
            (2, 5, "p initialized to &arr[2] (0x1008).", {"p": "0x1008", "*p": 30}, {"stack": [{"name":"p","addr":"0x1020","val":"0x1008","pointsTo":"arr[2]"}]}),
            (3, 6, "p[-1] expands to *(0x1008 - 4) = *(0x1004) -> 20. p[1] expands to *(0x1008 + 4) = *(0x100C) -> 40.", {"p[-1]": 20, "p[1]": 40}, {"stack": [{"name":"p[-1]","val":20},{"name":"p[1]","val":40}]}),
            (4, 7, "printf prints 20 40.", {"stdout": "20 40"}, {"stack": [{"name":"stdout","val":"20 40"}]})
        ]
    )

    # Q019: Pointer Subtraction Scaling by sizeof(type) -> Key C
    add_q(
        19, "CAT_PTR_ARR", "Medium", "Pointer Subtraction Scaling by sizeof(type)",
        "What is the output of the following program?",
        r"""#include <stdio.h>
int main() {
    int arr[5] = {1, 2, 3, 4, 5};
    int *p1 = &arr[0];
    int *p2 = &arr[4];
    printf("%td\n", p2 - p1);
    return 0;
}""",
        6, "p2 - p1", "Pointer subtraction yields the difference in ELEMENTS (ptrdiff_t), NOT raw bytes!",
        [
            ("A", "16", False, "Calculated the difference in raw bytes: 4 elements * 4 bytes = 16 bytes.", "Pointer subtraction is automatically scaled by sizeof(type); it yields element count, not byte count."),
            ("B", "5", False, "Counted the total number of elements in the array.", "p2 - p1 measures index distance: 4 - 0 = 4."),
            ("C", "4", True, "Subtracting two pointers to elements of the same array yields the number of elements separating them: 4 - 0 = 4 (of type ptrdiff_t, printed with %td).", ""),
            ("D", "Undefined Behavior", False, "Thought subtracting pointers is undefined.", "Subtracting pointers within the same array is strictly standard and defined by §6.5.6#9.")
        ],
        "Pointer subtraction (p2 - p1) yields the difference in array elements, not raw bytes. (0x1010 - 0x1000) / sizeof(int) = 4.",
        "ISO/IEC 9899:1999 §6.5.6#9",
        "Pointer Subtraction Rules:\nUnder ISO C §6.5.6#9, when two pointers to elements of the same array object are subtracted, the result is the difference of the subscripts of the two array elements.\n\nFormula:\n  ptrdiff = (address(p2) - address(p1)) / sizeof(type)\n\nExecution Details:\n1. arr[0] is at address 0x1000 (p1 = 0x1000).\n2. arr[4] is at address 0x1010 (p2 = 0x1010).\n3. The raw byte difference is 0x1010 - 0x1000 = 16 bytes.\n4. The compiler automatically divides this byte difference by sizeof(int) (4 bytes):\n   16 / 4 = 4 elements.\n5. The result has type ptrdiff_t (defined in <stddef.h>), which is correctly formatted using the %td format specifier.\n6. printf prints 4.\n\nExam Trap: Never multiply by sizeof(type) when calculating pointer distance in C. The compiler already scales pointer arithmetic automatically.",
        [
            (1, 4, "Array arr allocated at 0x1000: arr[0] at 0x1000, arr[4] at 0x1010.", {"arr[0]": 1, "arr[4]": 5}, {"stack": [{"name":"arr[0]","addr":"0x1000","val":1},{"name":"arr[4]","addr":"0x1010","val":5}]}),
            (2, 5, "p1 points to arr[0] (0x1000); p2 points to arr[4] (0x1010).", {"p1": "0x1000", "p2": "0x1010"}, {"stack": [{"name":"p1","val":"0x1000"},{"name":"p2","val":"0x1010"}]}),
            (3, 6, "p2 - p1 computed: (0x1010 - 0x1000) / sizeof(int) = 16 / 4 = 4 elements (ptrdiff_t).", {"diff": 4}, {"stack": []}),
            (4, 7, "printf prints 4 via %td.", {"stdout": "4"}, {"stack": [{"name":"stdout","val":"4"}]})
        ]
    )

    # Q020: Array of Pointers vs Pointer to Array Syntax -> Key D
    add_q(
        20, "CAT_PTR_ARR", "Tricky", "Array of Pointers vs Pointer to Array Syntax",
        "What is the type of variable p declared as: int (*p)[5]; ?",
        r"""#include <stdio.h>
int main() {
    int (*p)[5];
    return 0;
}""",
        3, "int (*p)[5]", "Parentheses force * to bind to p: p is a single pointer to an array of 5 integers!",
        [
            ("A", "An array of 5 pointers to integers", False, "Confused int (*p)[5] with int *p[5].", "Without parentheses, [] has higher precedence, making int *p[5] an array of pointers."),
            ("B", "A pointer to a function returning an array", False, "Confused with function pointer syntax.", "Function pointer syntax uses empty or typed argument parentheses: int (*fp)(int)."),
            ("C", "A syntax error", False, "Thought this declaration was invalid syntax.", "Valid standard C declaration."),
            ("D", "p is a pointer to an array of 5 integers", True, "Parentheses force the dereference operator * to associate with p first, making p a pointer to an array of 5 ints.", "")
        ],
        "Parentheses group * with p first, creating a pointer to an array of 5 ints. Without parentheses (int *p[5]), it is an array of 5 pointers.",
        "ISO/IEC 9899:1999 §6.7.5.2",
        "Right-Left Rule for C Declarations:\nTo decipher complex declarations in C, start from the identifier and read outwards, prioritizing parentheses and brackets according to precedence.\n\nComparing the Two Classic Declarations:\n1. int *p[5];\n   - [] has higher precedence than *.\n   - p is an array of 5 elements.\n   - Looking left, each element is a pointer to int (int*).\n   - Total size: 5 * sizeof(int*) = 40 bytes on 64-bit.\n\n2. int (*p)[5];\n   - Parentheses force * to bind to p first.\n   - p is a pointer.\n   - Looking right, it points to an array of 5 elements.\n   - Looking left, each array element is an int.\n   - Total size: sizeof(pointer) = 8 bytes on 64-bit.\n\nStride Impact:\n- If you perform p + 1 on int (*p)[5], the address advances by 5 * sizeof(int) = 20 bytes (an entire row of 5 ints)!\n- This type is essential when passing 2D arrays to functions: void process(int (*matrix)[5]).",
        [
            (1, 3, "Parser encounters identifier p.", {"identifier": "p"}, {"stack": []}),
            (2, 3, "Parentheses bind * to p: p is declared as a pointer.", {"type_partial": "pointer to ..."}, {"stack": [{"name":"p","type":"int(*)[5]"}]}),
            (3, 3, "Brackets [5] specify target type: array of 5 elements of type int.", {"type_full": "pointer to array of 5 ints"}, {"stack": [{"name":"p","stride":"5 * sizeof(int)"}]}),
            (4, 4, "Function returns 0.", {"return": 0}, {"stack": []})
        ]
    )

    # Q021: 2D Array Row Pointer Arithmetic Stride -> Key A
    add_q(
        21, "CAT_PTR_ARR", "Tricky", "2D Array Row Pointer Arithmetic Stride",
        "What is the output of the following program?",
        r"""#include <stdio.h>
int main() {
    int m[2][3] = {{1, 2, 3}, {4, 5, 6}};
    int *p = (int*)(m + 1);
    printf("%d\n", *p);
    return 0;
}""",
        4, "m + 1", "m has type int[2][3]. Adding 1 to m advances by an entire ROW (3 ints = 12 bytes), landing on 4!",
        [
            ("A", "4", True, "m has type int[2][3], which decays to int(*)[3]. Adding 1 advances by sizeof(int[3]) = 12 bytes to row 1 ({4, 5, 6}), so *p dereferences 4.", ""),
            ("B", "2", False, "Thought m + 1 advanced by only 1 integer (4 bytes) to m[0][1].", "m is an array of arrays; its element type is int[3], so its stride is an entire row."),
            ("C", "1", False, "Thought m + 1 had no effect.", "Pointer arithmetic advances the memory address."),
            ("D", "Compilation Error", False, "Thought 2D array arithmetic cannot be cast to int*.", "Explicit cast (int*) makes this valid C.")
        ],
        "m decays to a pointer to its first row (type int(*)[3]). Adding 1 steps forward by 3 * sizeof(int) (12 bytes), pointing to m[1][0] (4).",
        "ISO/IEC 9899:1999 §6.3.2.1#3 & §6.5.6#2",
        "Multidimensional Array Strides in Memory:\nIn C, multidimensional arrays are laid out in contiguous row-major order.\n\nMemory Representation of m[2][3]:\n- Row 0: m[0][0]=1 (0x1000), m[0][1]=2 (0x1004), m[0][2]=3 (0x1008)\n- Row 1: m[1][0]=4 (0x100C), m[1][1]=5 (0x1010), m[1][2]=6 (0x1014)\n\nType Decay and Pointer Arithmetic:\n1. The 2D array m has type int[2][3]. In expressions, m decays to a pointer to its first element: type int(*)[3].\n2. The element of m is an array of 3 ints (sizeof = 3 * 4 = 12 bytes).\n3. Therefore, evaluating m + 1 advances the address by 1 * 12 bytes = 0x100C.\n4. 0x100C is the exact start address of Row 1 (m[1][0]).\n5. Casting (int*)(m + 1) assigns 0x100C to int *p.\n6. Dereferencing *p reads the integer at 0x100C, which is 4.\n\nExam Trap: Never think 2D array arithmetic steps by single scalar elements. The stride is always determined by the row size.",
        [
            (1, 3, "m[2][3] allocated contiguously in row-major order: Row 0 at 0x1000, Row 1 at 0x100C.", {"m[0]": [1, 2, 3], "m[1]": [4, 5, 6]}, {"stack": [{"name":"m[0][0]","addr":"0x1000","val":1},{"name":"m[0][1]","addr":"0x1004","val":2},{"name":"m[0][2]","addr":"0x1008","val":3},{"name":"m[1][0]","addr":"0x100C","val":4},{"name":"m[1][1]","addr":"0x1010","val":5},{"name":"m[1][2]","addr":"0x1014","val":6}]}),
            (2, 4, "m decays to int(*)[3]. m + 1 advances by sizeof(int[3]) = 12 bytes from 0x1000 to 0x100C.", {"m+1": "0x100C"}, {"stack": []}),
            (3, 4, "Cast to int* assigns 0x100C to p. p points to m[1][0] (4).", {"p": "0x100C", "*p": 4}, {"stack": [{"name":"p","addr":"0x1020","val":"0x100C","pointsTo":"m[1][0]"}]}),
            (4, 5, "printf prints *p (4).", {"stdout": "4"}, {"stack": [{"name":"stdout","val":"4"}]})
        ]
    )

    # Q022: Pointer Equivalence for 2D Array Subscripts -> Key B
    add_q(
        22, "CAT_PTR_ARR", "Tricky", "Pointer Equivalence for 2D Array Subscripts",
        "Which pointer expression is strictly equivalent to m[1][2] for int m[2][3]?",
        r"""#include <stdio.h>
int main() {
    int m[2][3] = {{10, 20, 30}, {40, 50, 60}};
    printf("%d\n", *(*(m + 1) + 2));
    return 0;
}""",
        4, "*(*(m + 1) + 2)", "By subscript definition: m[1][2] == (*(m + 1))[2] == *(*(m + 1) + 2) == 60.",
        [
            ("A", "*((m + 1) + 2)", False, "Missing an inner dereference operator.", "(m + 1) produces a pointer to array; you must dereference it to decay into an int* before adding column offset 2."),
            ("B", "*(*(m + 1) + 2)", True, "m[1][2] expands by subscript definition to (*(m + 1))[2], which further expands to *(*(m + 1) + 2).", ""),
            ("C", "*(m + 1 + 2)", False, "Adds offsets directly without dimensionality stride.", "1 + 2 = 3 strides by 3 rows, exceeding array dimensions."),
            ("D", "**(m + 1 + 2)", False, "Incorrect pointer dereference layering.", "Combines bad stride addition with premature double dereference.")
        ],
        "By applying E1[E2] == * (E1 + E2) iteratively: m[1][2] == (*(m + 1))[2] == *(*(m + 1) + 2).",
        "ISO/IEC 9899:1999 §6.5.2.1",
        "Iterative Subscript Expansion Rule:\nEvery array subscript in C is an alias for pointer addition followed by dereference.\n\nTwo-Step Derivation of m[1][2]:\n1. Outer Subscript Expansion:\n   Treating m[1] as an array object X, X[2] becomes *(X + 2).\n   Substituting m[1] for X gives: (*(m[1] + 2)).\n2. Inner Subscript Expansion:\n   Now expand the inner subscript m[1]:\n   m[1] becomes *(m + 1).\n3. Combine Both:\n   Substituting *(m + 1) into the expression gives:\n   *(*(m + 1) + 2).\n\nType and Pointer Walkthrough:\n- m has type int[2][3] (decays to int(*)[3]).\n- (m + 1) advances to Row 1 (address of m[1]).\n- *(m + 1) dereferences the row pointer, yielding the row array m[1] (type int[3]), which decays into an int* pointing to m[1][0].\n- *(m + 1) + 2 adds 2 integers, pointing to m[1][2].\n- *(*(m + 1) + 2) dereferences that address, yielding 60.",
        [
            (1, 3, "m[2][3] initialized with 6 elements. m[1][2] is 60.", {"m[1][2]": 60}, {"stack": [{"name":"m[1][2]","addr":"0x1014","val":60}]}),
            (2, 4, "Inner step: (m + 1) points to Row 1. *(m + 1) decays to int* pointing to m[1][0].", {"*(m+1)": "0x100C (&m[1][0])"}, {"stack": []}),
            (3, 4, "Column offset: *(m + 1) + 2 advances by 2 ints to 0x1014 (&m[1][2]).", {"target": "0x1014"}, {"stack": []}),
            (4, 4, "Outer dereference *(*(m + 1) + 2) reads integer 60. printf prints 60.", {"stdout": "60"}, {"stack": [{"name":"stdout","val":"60"}]})
        ]
    )

    # Q023: Passing Pointer by Value (Failed Allocation) -> Key C
    add_q(
        23, "CAT_PTR_ARR", "Tricky", "Passing Pointer by Value (Failed Allocation)",
        "What is the output of the following program?",
        r"""#include <stdio.h>
#include <stdlib.h>
void allocate(int *p) {
    p = malloc(sizeof(int));
    *p = 42;
}
int main() {
    int *ptr = NULL;
    allocate(ptr);
    if (ptr == NULL) {
        printf("STILL NULL\n");
    } else {
        printf("%d\n", *ptr);
    }
    return 0;
}""",
        10, "allocate(ptr)", "Pointers in C are passed BY VALUE! allocate modifies its local copy p, leaving main's ptr STILL NULL (and leaking memory)!",
        [
            ("A", "42", False, "Thought allocate modified the caller's ptr pointer variable.", "In C, all arguments are passed by value; changing the parameter pointer has no effect on the caller."),
            ("B", "Runtime Crash", False, "Thought dereferencing NULL caused a crash.", "The if check (ptr == NULL) protects against dereference, taking the true branch."),
            ("C", "STILL NULL", True, "Pointers are passed by value; the local copy p in allocate receives the heap address, but main's ptr remains NULL, leaking 4 bytes of heap memory.", ""),
            ("D", "Compilation Error", False, "Thought passing a NULL pointer is illegal.", "Passing NULL to a function expecting int* is completely valid standard C.")
        ],
        "C passes all function arguments by value. Modifying parameter p inside allocate only changes its local copy on allocate's stack frame.",
        "ISO/IEC 9899:1999 §6.9.1",
        "Pass-by-Value Mechanics in C:\nEvery function parameter in C is a distinct local variable initialized with a copy of the argument's value.\n\nCall Trace & Memory Isolation:\n1. main() creates local variable ptr initialized to NULL (0x0).\n2. When allocate(ptr) is called, allocate receives a copy of ptr (0x0) stored in its local parameter variable p on allocate's stack frame.\n3. malloc allocates 4 bytes on the heap (e.g. at 0x5000) and returns 0x5000.\n4. p is reassigned to 0x5000, and *p stores 42 in heap memory.\n5. allocate terminates! Its stack frame (including parameter p) is popped and destroyed.\n6. Back in main(): ptr was never touched! ptr is STILL NULL.\n7. The allocated 4 bytes at 0x5000 are orphaned (memory leak).\n8. The if condition (ptr == NULL) evaluates to true, printing STILL NULL.\n\nHow to Fix: To allow a function to modify the caller's pointer, you must pass the address of the pointer (a pointer to pointer): void allocate(int **pp).",
        [
            (1, 9, "main(): ptr initialized to NULL (0x0) at stack address 0x2000.", {"main.ptr": "NULL"}, {"stack": [{"name":"main.ptr","addr":"0x2000","val":"0x0 (NULL)"}]}),
            (2, 4, "allocate(ptr) called: parameter p is a copy (val=0x0) at stack address 0x1FE0.", {"param.p": "NULL"}, {"stack": [{"name":"main.ptr","addr":"0x2000","val":"0x0"},{"name":"allocate.p","addr":"0x1FE0","val":"0x0"}]}),
            (3, 4, "malloc allocates 4 bytes at heap address 0x5000. allocate.p set to 0x5000; *p = 42.", {"p": "0x5000", "*p": 42}, {"stack": [{"name":"allocate.p","val":"0x5000"}], "heap": [{"addr":"0x5000","size":4,"val":42}]}),
            (4, 5, "allocate returns: stack frame popped. main.ptr remains 0x0 (NULL). Heap 0x5000 leaked.", {"main.ptr": "NULL"}, {"stack": [{"name":"main.ptr","val":"0x0 (NULL)"}], "heap": [{"addr":"0x5000","size":4,"val":42,"status":"leaked"}]}),
            (5, 11, "if (ptr == NULL) is true. printf prints STILL NULL.", {"stdout": "STILL NULL"}, {"stack": [{"name":"stdout","val":"STILL NULL"}]})
        ]
    )

    # Q024: Modifying Caller Pointer via Pointer-to-Pointer -> Key D
    add_q(
        24, "CAT_PTR_ARR", "Medium", "Modifying Caller Pointer via Pointer-to-Pointer",
        "What is the output of the following program?",
        r"""#include <stdio.h>
void set_val(int **pp, int *target) {
    *pp = target;
}
int main() {
    int a = 10, b = 20;
    int *p = &a;
    set_val(&p, &b);
    printf("%d\n", *p);
    return 0;
}""",
        4, "*pp = target;", "Dereferencing the double pointer (*pp) directly updates the pointer p in main to point to b!",
        [
            ("A", "10", False, "Thought p in main remained pointing to a.", "Passing &p allows set_val to modify pointer p directly via dereference."),
            ("B", "0", False, "Thought memory was zeroed.", "Target points to b which holds 20."),
            ("C", "Runtime Crash", False, "Thought double pointer manipulation causes a crash.", "Valid double pointer indirection."),
            ("D", "20", True, "Passing &p passes the address of pointer p. In set_val, *pp accesses p and updates it to point to b, so *p prints 20.", "")
        ],
        "Passing &p (address of pointer) allows set_val to modify the caller's pointer variable. *pp = target redirects p to &b.",
        "ISO/IEC 9899:1999 §6.5.3.2",
        "Double Pointer Indirection Mechanics:\nTo mutate a variable of type T inside a function, the caller must pass a pointer of type T*. When the variable to be mutated is itself a pointer (int*), the caller must pass a pointer to that pointer: int**.\n\nExecution Trace:\n1. main() creates integers a = 10 (0x1000) and b = 20 (0x1004).\n2. Pointer p (at address 0x1010) is initialized to &a (0x1000).\n3. set_val(&p, &b) is invoked:\n   - pp receives 0x1010 (the address of variable p in main).\n   - target receives 0x1004 (&b).\n4. Inside set_val: *pp dereferences address 0x1010, which designates the storage of variable p in main.\n5. *pp = target assigns 0x1004 directly into p in main.\n6. set_val returns.\n7. In main(): p now holds 0x1004 (&b).\n8. *p reads the integer at 0x1004, which is 20.\n9. printf prints 20.",
        [
            (1, 7, "main(): a=10 at 0x1000, b=20 at 0x1004. p at 0x1010 points to &a (0x1000).", {"a": 10, "b": 20, "p": "0x1000"}, {"stack": [{"name":"a","addr":"0x1000","val":10},{"name":"b","addr":"0x1004","val":20},{"name":"p","addr":"0x1010","val":"0x1000","pointsTo":"a"}]}),
            (2, 8, "set_val(&p, &b) called: pp = 0x1010 (&p), target = 0x1004 (&b).", {"pp": "0x1010", "target": "0x1004"}, {"stack": [{"name":"set_val.pp","addr":"0x1FE0","val":"0x1010","pointsTo":"main.p"},{"name":"set_val.target","addr":"0x1FE8","val":"0x1004","pointsTo":"main.b"}]}),
            (3, 4, "*pp = target executes: writes 0x1004 into main.p (at 0x1010).", {"main.p": "0x1004"}, {"stack": [{"name":"main.p","addr":"0x1010","val":"0x1004","pointsTo":"b"}]}),
            (4, 9, "Back in main(): *p dereferences b (20). printf prints 20.", {"stdout": "20"}, {"stack": [{"name":"stdout","val":"20"}]})
        ]
    )

    # Q025: Dereferencing a Void Pointer -> Key A
    add_q(
        25, "CAT_PTR_ARR", "Easy", "Dereferencing a Void Pointer",
        "What happens when compiling and running the following code?",
        r"""#include <stdio.h>
int main() {
    int x = 10;
    void *ptr = &x;
    printf("%d\n", *ptr);
    return 0;
}""",
        5, "*ptr", "void* has an incomplete type with no size! Dereferencing a void* without casting is an ERROR in standard C!",
        [
            ("A", "Compilation Error", True, "void is an incomplete type that cannot be completed; dereferencing a void* without an explicit cast is forbidden in ISO C.", ""),
            ("B", "Prints 10", False, "Thought the compiler remembers the underlying int type.", "void* erases all compile-time type information; the compiler does not know how many bytes to read or how to interpret them."),
            ("C", "Prints address of x", False, "Thought *ptr prints the address.", "Dereference * attempts to read value, not address."),
            ("D", "Segmentation Fault", False, "Thought it crashes at runtime.", "The code fails at compile time and never produces an executable.")
        ],
        "void* is a pointer to an incomplete type. Because void has no size, dereferencing *ptr is an illegal operation that produces a compilation error.",
        "ISO/IEC 9899:1999 §6.2.5#19 & §6.5.3.2#2",
        "Incomplete Type Constraint in ISO C:\nIn C, void represents an incomplete type that cannot be completed. An object of type void has no size, no alignment, and no value representation.\n\nCompiler Rejection:\n- The unary dereference operator * requires its operand to be a pointer to an object type (§6.5.3.2#2).\n- Because void is not an object type with a defined size, the compiler cannot determine:\n  1. How many bytes to read from memory (1, 2, 4, or 8 bytes?).\n  2. How to interpret the bit pattern (integer, floating-point, struct?).\n- GCC emits: error: dereferencing 'void *' pointer.\n\nProper Solution: Cast ptr to the concrete pointer type before dereferencing: *(int*)ptr.",
        [
            (1, 3, "x allocated on stack with value 10.", {"x": 10}, {"stack": [{"name":"x","addr":"0x1000","val":10}]}),
            (2, 4, "void *ptr initialized with &x (0x1000). Type information erased.", {"ptr": "0x1000 (void*)"}, {"stack": [{"name":"ptr","addr":"0x1008","val":"0x1000"}]}),
            (3, 5, "Compiler attempts to evaluate *ptr. void has incomplete type with unknown size -> COMPILATION ERROR.", {"compiler_error": "dereferencing 'void *' pointer"}, {"stack": []})
        ]
    )

    # Q026: Null Pointer Dereference Behavior -> Key B
    add_q(
        26, "CAT_PTR_ARR", "Easy", "Null Pointer Dereference Behavior",
        "What happens when running the following program?",
        r"""#include <stdio.h>
int main() {
    int *p = NULL;
    printf("%d\n", *p);
    return 0;
}""",
        4, "*p", "Dereferencing NULL accesses address 0x0, which causes an immediate Segmentation Fault / Access Violation!",
        [
            ("A", "Prints 0", False, "Thought NULL pointer contains integer 0 as its value.", "NULL is an invalid address constant, not an integer value at that address."),
            ("B", "Runtime Crash (Segmentation Fault)", True, "Dereferencing a NULL pointer attempts to read from address 0x0 (an unmapped memory page), triggering a hardware page fault (SIGSEGV / Access Violation).", ""),
            ("C", "Compilation Error", False, "Thought the compiler forbids dereferencing NULL.", "Compilers cannot always detect null dereferences at compile time; it compiles and crashes at runtime."),
            ("D", "Prints garbage value", False, "Thought it reads whatever was at address 0.", "Address 0 is protected by OS virtual memory management to catch null pointer bugs.")
        ],
        "Dereferencing a null pointer is undefined behavior in ISO C. On virtual-memory OSes, page 0 is unmapped, triggering a SIGSEGV / Access Violation.",
        "ISO/IEC 9899:1999 §6.5.3.2#4",
        "Virtual Memory and Null Pointer Dereference:\nIn C, NULL is an implementation-defined null pointer constant, typically defined as ((void*)0).\n\nHardware and OS Response:\n1. In modern operating systems (Linux, Windows, macOS), the virtual address space maps page 0 (addresses 0x00000000 to 0x00000FFF) as strictly non-accessible (no read, no write, no execute permissions).\n2. When CPU instruction mov eax, [p] attempts to read memory at address 0x0, the Memory Management Unit (MMU) raises a hardware page fault exception.\n3. The operating system kernel intercepts the fault, identifies an invalid memory access, and dispatches signal SIGSEGV (Linux) or STATUS_ACCESS_VIOLATION (Windows) to the process.\n4. The process is aborted immediately without executing the return statement.\n\nExam Trap: In ISO C, null pointer dereference is technically Undefined Behavior, but on virtually all modern systems it is guaranteed to terminate with a crash.",
        [
            (1, 3, "p initialized to NULL (address 0x00000000) on the stack.", {"p": "0x0 (NULL)"}, {"stack": [{"name":"p","addr":"0x1000","val":"0x0 (NULL)"}]}),
            (2, 4, "Attempt to evaluate *p dereferences address 0x0.", {"target_addr": "0x00000000"}, {"stack": [{"name":"p","val":"0x0"}]}),
            (3, 4, "MMU detects access to unmapped zero-page. Kernel raises SIGSEGV / Access Violation -> Process terminated.", {"signal": "SIGSEGV (Exit 139 / Crash)"}, {"stack": []})
        ]
    )

    # Q027: Classic Pointer Swap Implementation -> Key C
    add_q(
        27, "CAT_PTR_ARR", "Medium", "Classic Pointer Swap Implementation",
        "What is the output of the following program?",
        r"""#include <stdio.h>
void swap(int *x, int *y) {
    int temp = *x;
    *x = *y;
    *y = temp;
}
int main() {
    int a = 5, b = 10;
    swap(&a, &b);
    printf("%d %d\n", a, b);
    return 0;
}""",
        10, "swap(&a, &b);", "Addresses of a and b are passed, and values are swapped correctly in memory via dereferencing.",
        [
            ("A", "5 10", False, "Thought arguments were passed by value without modifying a and b.", "Addresses &a and &b were passed, enabling in-place memory mutation."),
            ("B", "10 10", False, "Thought one value overwrote the other without temp preservation.", "Variable temp correctly preserved *x before *x was overwritten."),
            ("C", "10 5", True, "swap receives pointers to a and b; using temp, it exchanges the integer values in the caller's stack frame, printing 10 5.", ""),
            ("D", "5 5", False, "Thought *y overwrote *x and copied back.", "Correct 3-step swap algorithm.")
        ],
        "Addresses of a and b are passed as pointers. swap dereferences them to exchange their values in place: a becomes 10, b becomes 5.",
        "ISO/IEC 9899:1999 §6.2.4 & §6.5.3.2",
        "Classic Call-by-Reference Simulation in C:\nBecause C is strictly pass-by-value, passing the addresses &a and &b allows swap() to access and mutate the caller's memory locations.\n\nStep-by-step Trace:\n1. main() stack frame holds a = 5 (0x1000) and b = 10 (0x1004).\n2. swap(&a, &b) pushes pointers x = 0x1000 and y = 0x1004 onto swap's stack frame.\n3. int temp = *x reads the value at 0x1000 (5) and stores it in temp.\n4. *x = *y reads value at 0x1004 (10) and writes it into 0x1000 (variable a in main). a is now 10.\n5. *y = temp writes 5 into 0x1004 (variable b in main). b is now 5.\n6. swap returns; its stack frame is discarded.\n7. In main(), a is 10 and b is 5. printf prints 10 5.\n\nExam Trap: If the function header were void swap(int x, int y), the swap would only affect the local parameter copies, leaving a and b untouched as 5 10.",
        [
            (1, 9, "main(): a = 5 at 0x1000, b = 10 at 0x1004.", {"a": 5, "b": 10}, {"stack": [{"name":"main.a","addr":"0x1000","val":5},{"name":"main.b","addr":"0x1004","val":10}]}),
            (2, 3, "swap(&a, &b) called: x = 0x1000 (&a), y = 0x1004 (&b). temp = *x = 5.", {"temp": 5, "x": "0x1000", "y": "0x1004"}, {"stack": [{"name":"swap.x","val":"0x1000","pointsTo":"main.a"},{"name":"swap.y","val":"0x1004","pointsTo":"main.b"},{"name":"swap.temp","val":5}]}),
            (3, 4, "*x = *y writes 10 into main.a (0x1000). *y = temp writes 5 into main.b (0x1004).", {"main.a": 10, "main.b": 5}, {"stack": [{"name":"main.a","addr":"0x1000","val":10},{"name":"main.b","addr":"0x1004","val":5}]}),
            (4, 11, "swap returns. printf prints a (10) and b (5).", {"stdout": "10 5"}, {"stack": [{"name":"stdout","val":"10 5"}]})
        ]
    )

    # Q028: Triple Pointer Dereferencing Chain -> Key D
    add_q(
        28, "CAT_PTR_ARR", "Medium", "Triple Pointer Dereferencing Chain",
        "What is the output of the following program?",
        r"""#include <stdio.h>
int main() {
    int x = 100;
    int *p = &x;
    int **pp = &p;
    int ***ppp = &pp;
    ***ppp = 200;
    printf("%d %d\n", x, **pp);
    return 0;
}""",
        7, "***ppp = 200;", "***ppp follows the 3-step pointer chain straight down to x, setting x = 200!",
        [
            ("A", "100 200", False, "Thought x was not modified by ***ppp.", "***ppp reaches the underlying integer x directly through three dereferences."),
            ("B", "100 100", False, "Thought assignment failed.", "x is mutated to 200."),
            ("C", "200 100", False, "Thought **pp read a cached copy.", "**pp reads from x via p; both evaluate to 200."),
            ("D", "200 200", True, "***ppp traverses the pointer chain ppp -> pp -> p -> x, modifying x to 200. Both x and **pp evaluate to 200.", "")
        ],
        "***ppp dereferences three levels of indirection: ppp -> pp -> p -> x. Modifying ***ppp writes 200 directly into x.",
        "ISO/IEC 9899:1999 §6.5.3.2",
        "Multi-Level Pointer Indirection Chains:\nIn C, each asterisk * in an expression strips away one level of pointer indirection.\n\nMemory Hierarchy Trace:\n1. x is an int with value 100 at address 0x1000.\n2. p is an int* with value 0x1000 at address 0x1010 (points to x).\n3. pp is an int** with value 0x1010 at address 0x1020 (points to p).\n4. ppp is an int*** with value 0x1020 at address 0x1030 (points to pp).\n\nDereference Chain:\n- *ppp reads value at 0x1030 -> yields 0x1010 (address of p).\n- **ppp reads value at 0x1010 -> yields 0x1000 (address of x).\n- ***ppp reads/writes memory at 0x1000 -> accesses object x.\n- Assignment ***ppp = 200 writes 200 into x.\n- **pp evaluates *(*pp) = *(0x1000) = 200.\n- printf prints 200 200.",
        [
            (1, 6, "Pointer chain established on stack: ppp (0x1030) -> pp (0x1020) -> p (0x1010) -> x (0x1000, val=100).", {"x": 100}, {"stack": [{"name":"x","addr":"0x1000","val":100},{"name":"p","addr":"0x1010","val":"0x1000","pointsTo":"x"},{"name":"pp","addr":"0x1020","val":"0x1010","pointsTo":"p"},{"name":"ppp","addr":"0x1030","val":"0x1020","pointsTo":"pp"}]}),
            (2, 7, "***ppp traverses 3 levels of pointers and writes 200 into x (at 0x1000).", {"x": 200}, {"stack": [{"name":"x","addr":"0x1000","val":200}]}),
            (3, 8, "**pp traverses 2 levels: *pp yields 0x1000; *(0x1000) yields 200.", {"**pp": 200}, {"stack": []}),
            (4, 9, "printf prints x (200) and **pp (200).", {"stdout": "200 200"}, {"stack": [{"name":"stdout","val":"200 200"}]})
        ]
    )

    # Q029: Function Pointer Declaration and Invocation -> Key A
    add_q(
        29, "CAT_PTR_ARR", "Tricky", "Function Pointer Declaration and Invocation",
        "What is the output of the following program?",
        r"""#include <stdio.h>
int add(int a, int b) { return a + b; }
int sub(int a, int b) { return a - b; }
int main() {
    int (*fp)(int, int) = add;
    printf("%d ", fp(10, 5));
    fp = sub;
    printf("%d\n", fp(10, 5));
    return 0;
}""",
        5, "int (*fp)(int, int) = add;", "fp is a function pointer initially pointing to add, then reassigned to sub.",
        [
            ("A", "15 5", True, "fp is declared as a pointer to a function taking two ints and returning int. First fp(10, 5) calls add (15); then fp is reassigned to sub, and fp(10, 5) calls sub (5).", ""),
            ("B", "15 15", False, "Thought fp could not be reassigned after initialization.", "Function pointers in C are mutable variables and can be freely reassigned to compatible functions."),
            ("C", "5 15", False, "Inverted the execution order.", "add was assigned first, then sub."),
            ("D", "Compilation Error", False, "Thought calling a function pointer requires (*fp)(10, 5).", "In ISO C, both fp(10, 5) and (*fp)(10, 5) are completely valid and equivalent.")
        ],
        "fp is a function pointer. Calling fp(10, 5) invokes add (15). Reassigning fp = sub causes the second call to invoke sub (5).",
        "ISO/IEC 9899:1999 §6.5.2.2 & §6.7.5.3",
        "Function Pointer Semantics in C:\nIn C, function names decay into pointers to their entry-point code in the text (.text) segment.\n\nDeclaration Syntax:\n  int (*fp)(int, int);\n- The identifier fp is enclosed with * in parentheses, meaning fp is a pointer.\n- (int, int) indicates it points to a function taking two int parameters.\n- Leading int indicates the function returns int.\n\nInvocation Equivalence:\nUnder ISO C §6.5.2.2, a function pointer can be invoked with or without explicit dereferencing:\n- fp(10, 5) is standard and idiomatic.\n- (*fp)(10, 5) is equally valid and supported.\n\nTrace:\n1. fp is initialized with address of add. fp(10, 5) calls add(10, 5) -> returns 15.\n2. fp is reassigned to sub. fp(10, 5) calls sub(10, 5) -> returns 5.\n3. Output is 15 5.",
        [
            (1, 5, "Function pointer fp declared and initialized to address of add function in .text segment.", {"fp": "&add"}, {"stack": [{"name":"fp","addr":"0x1000","val":"&add","pointsTo":"function add(int, int)"}]}),
            (2, 6, "fp(10, 5) invokes add(10, 5) -> returns 15. Printed with trailing space.", {"stdout": "15 "}, {"stack": []}),
            (3, 7, "fp reassigned to address of sub function.", {"fp": "&sub"}, {"stack": [{"name":"fp","addr":"0x1000","val":"&sub","pointsTo":"function sub(int, int)"}]}),
            (4, 8, "fp(10, 5) invokes sub(10, 5) -> returns 5. printf prints 5.", {"stdout": "15 5"}, {"stack": [{"name":"stdout","val":"15 5"}]})
        ]
    )

    # Q030: Array Out-of-Bounds Subscript Access -> Key B
    add_q(
        30, "CAT_PTR_ARR", "Medium", "Array Out-of-Bounds Subscript Access",
        'What does the C standard dictate regarding the statement printf("%d\\n", arr[5]); for int arr[5] = {1, 2, 3, 4, 5};?',
        r"""#include <stdio.h>
int main() {
    int arr[5] = {1, 2, 3, 4, 5};
    printf("%d\n", arr[5]);
    return 0;
}""",
        4, "arr[5]", "Array indices are 0 to 4! arr[5] accesses memory outside the array bounds, causing Undefined Behavior!",
        [
            ("A", "Guaranteed to print 0", False, "Thought out-of-bounds stack memory is automatically zeroed.", "C does not initialize or zero adjacent stack memory; reads produce garbage or faults."),
            ("B", "Undefined Behavior (Accesses stack garbage or crashes)", True, "Valid array indices are 0 through 4. Computing and dereferencing arr[5] accesses memory beyond the allocated array object, which is strictly Undefined Behavior in ISO C.", ""),
            ("C", "Compilation Error: array index out of bounds", False, "Thought C compilers enforce mandatory boundary checks at compile time.", "C standard does not require runtime or compile-time bounds checking; code compiles without error."),
            ("D", "Guaranteed to print 5", False, "Confused index 5 with element 5.", "Element 5 is at arr[4]; arr[5] is past the end.")
        ],
        "Valid indices for int arr[5] are 0..4. arr[5] accesses memory outside the array bounds, which is Undefined Behavior.",
        "ISO/IEC 9899:1999 §6.5.6#8",
        "Lack of Bounds Checking in C:\nThe C language was designed for raw performance and systems programming; it deliberately omits runtime bounds checking on array subscripts.\n\nMemory Analysis:\n- int arr[5] reserves 5 * sizeof(int) = 20 bytes on the stack (indices 0, 1, 2, 3, 4).\n- arr[5] evaluates to *(arr + 5).\n- Under ISO C §6.5.6#8, while computing the address arr + 5 (one past the end) is permitted, dereferencing it with * or [] violates the standard and invokes Undefined Behavior.\n\nConsequences of Undefined Behavior:\n1. On typical desktop architectures, arr[5] reads whatever raw bytes happen to follow arr on the stack (saved frame pointer, compiler padding, or another local variable).\n2. If the address crosses into an unmapped or write-protected memory page, a Segmentation Fault occurs.\n3. Optimizing compilers (GCC -O3) may assume out-of-bounds accesses never occur and optimize away surrounding code unexpectedly.",
        [
            (1, 3, "arr[5] allocated on stack at addresses 0x1000..0x1013 (elements 0 to 4).", {"arr": [1, 2, 3, 4, 5]}, {"stack": [{"name":"arr[0..4]","addr":"0x1000..0x1013","val":"{1,2,3,4,5}"}]}),
            (2, 4, "arr[5] evaluates as *(arr + 5) at address 0x1014 (beyond array boundary).", {"oob_addr": "0x1014"}, {"stack": [{"name":"adjacent_stack","addr":"0x1014","val":"[garbage/canary]"}]}),
            (3, 4, "Dereferencing one-past-the-end is strictly UNDEFINED BEHAVIOR under ISO C §6.5.6#8.", {"status": "Undefined Behavior"}, {"stack": []})
        ]
    )

    # Q031: Relational Comparison of Unrelated Pointers -> Key C
    add_q(
        31, "CAT_PTR_ARR", "Nightmare", "Relational Comparison of Unrelated Pointers",
        "What does the C standard dictate about: if (&a < &b) where a and b are separate local variables?",
        r"""#include <stdio.h>
int main() {
    int a = 10;
    int b = 20;
    if (&a < &b) {
        printf("A\n");
    } else {
        printf("B\n");
    }
    return 0;
}""",
        5, "&a < &b", "Relational comparison (<, <=, >, >=) between pointers to UNRELATED objects is Undefined Behavior in ISO C!",
        [
            ("A", "Guaranteed to print A because a was declared first", False, "Thought stack allocation order is guaranteed by declaration order.", "The C standard specifies no relationship between declaration order and memory address order."),
            ("B", "Guaranteed to print B because stack grows downward", False, "Assumed stack growth direction is a language guarantee.", "Stack layout and architecture direction are implementation details, not language guarantees."),
            ("C", "Undefined Behavior", True, "In ISO C, relational comparisons (<, <=, >, >=) are only defined between pointers to elements of the SAME array or struct object; comparing addresses of unrelated objects is Undefined Behavior.", ""),
            ("D", "Compilation Error", False, "Thought comparing pointers is syntactically invalid.", "Pointers of compatible type can be syntactically compared with <, but standard semantics declare it UB.")
        ],
        "ISO C §6.5.8#5 explicitly states that relational comparison (<, >, <=, >=) between pointers to unrelated objects is Undefined Behavior.",
        "ISO/IEC 9899:1999 §6.5.8#5",
        "Pointer Relational Comparison Constraints:\nUnder ISO C §6.5.8 paragraph 5, relational operators (<, <=, >, >=) on pointers are strictly constrained:\n- Pointers may be compared if they point to elements of the same array object, or one past the end.\n- Pointers may be compared if they point to members of the same structure object.\n- 'In all other cases, the behavior is undefined.'\n\nWhy This Matters:\n1. Variable Allocation Independence: The compiler is free to place local variables a and b in any order, in registers, in different stack positions, or eliminate them entirely via dead code elimination.\n2. Segmented Architectures: On segmented architectures (x86 16-bit real mode), two pointers might have different segment bases where comparing offsets is completely meaningless.\n3. Equality vs Relational: Notice that equality comparisons (&a == &b or &a != &b) are legal and well-defined between any pointers of compatible type. Only relational comparisons (<, >) require pointers to share the same underlying object.",
        [
            (1, 3, "Variable a allocated on stack at address 0x1004.", {"a": 10}, {"stack": [{"name":"a","addr":"0x1004","val":10}]}),
            (2, 4, "Variable b allocated on stack at address 0x1000 (compiler chose lower address).", {"b": 20}, {"stack": [{"name":"b","addr":"0x1000","val":20}]}),
            (3, 5, "Relational comparison (&a < &b) between unrelated distinct objects -> UNDEFINED BEHAVIOR under §6.5.8#5.", {"status": "Undefined Behavior"}, {"stack": []})
        ]
    )

    # Q032: Subtracting Incompatible Pointer Types -> Key D
    add_q(
        32, "CAT_PTR_ARR", "Easy", "Subtracting Incompatible Pointer Types",
        "What happens when attempting to compile the following program?",
        r"""#include <stdio.h>
int main() {
    int a = 10;
    double d = 20.0;
    int *p1 = &a;
    double *p2 = &d;
    printf("%td\n", p2 - p1);
    return 0;
}""",
        7, "p2 - p1", "Subtracting pointers of different types (double* and int*) is a COMPILATION ERROR!",
        [
            ("A", "Prints 2", False, "Thought byte difference was divided by sizeof(double) / sizeof(int).", "Pointer subtraction cannot divide by conflicting type sizes."),
            ("B", "Prints difference in raw bytes", False, "Thought compiler falls back to byte subtraction.", "C never implicitly casts pointer types for subtraction."),
            ("C", "Undefined Behavior", False, "Thought it compiles and invokes undefined behavior at runtime.", "This is a constraint violation caught at compile time."),
            ("D", "Compilation Error", True, "ISO C requires both operands of pointer subtraction to point to compatible types belonging to the same array object; subtracting double* and int* fails compilation.", "")
        ],
        "Pointer subtraction requires both operands to point to compatible types. Subtracting double* and int* violates ISO C §6.5.6#9 and causes a compilation error.",
        "ISO/IEC 9899:1999 §6.5.6#9",
        "Type Safety in Pointer Subtraction:\nUnder ISO C §6.5.6 paragraph 9, the constraint for binary operator - on pointers is explicitly defined:\n'For subtraction, one of the following shall hold: both operands are pointers to qualified or unqualified versions of compatible complete object types'\n\nWhy the Compiler Rejects This:\n1. Pointer subtraction is fundamentally defined as dividing the address delta by the size of the pointed-to object: (p2 - p1) / sizeof(*p).\n2. Here, p2 points to double (8 bytes) while p1 points to int (4 bytes).\n3. The compiler cannot determine which type size to scale by (4 or 8).\n4. GCC immediately emits: error: invalid operands to binary - (have 'double *' and 'int *').\n5. Compilation fails; no binary executable is generated.",
        [
            (1, 3, "a (int) and d (double) allocated on stack.", {"a": 10, "d": 20.0}, {"stack": [{"name":"a","type":"int","val":10},{"name":"d","type":"double","val":20.0}]}),
            (2, 5, "p1 is int* (address of a); p2 is double* (address of d).", {"p1": "&a", "p2": "&d"}, {"stack": [{"name":"p1","type":"int*"},{"name":"p2","type":"double*"}]}),
            (3, 7, "Expression p2 - p1 violates ISO C §6.5.6#9: operands have incompatible types (double* and int*) -> COMPILATION ERROR.", {"compiler_error": "invalid operands to binary -"}, {"stack": []})
        ]
    )

    print("bank_part1 loaded (32 questions).")