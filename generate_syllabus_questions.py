# generate_syllabus_questions.py
# Exactly aligned with the 6 Konsep Pemrograman Midterm modules:
# 1. Data Types & Variables (16 Qs)
# 2. Operators & Expressions (18 Qs)
# 3. Conditionals (if-else, switch-case) (16 Qs)
# 4. Loops (for, while, do-while, break/continue) (18 Qs)
# 5. Functions and Procedures (pass-by-value, scope, static, recursion) (16 Qs)
# 6. Arrays (1D arrays, 2D matrices, char arrays/strings) (16 Qs)
# Total = 100 Questions

import json

questions = []

def add_q(id_num, category, difficulty, title, prompt, code, trap_line, trap_token, trap_warning, 
          options_tuples, summary, std_ref, deep_dive, trace_steps):
    opts = []
    for k, text, corr, tempting, wrong in options_tuples:
        opt_obj = {
            "key": k,
            "text": str(text),
            "isCorrect": bool(corr),
            "whyTempting": tempting
        }
        if not corr:
            opt_obj["whyWrong"] = wrong
        opts.append(opt_obj)
        
    trace = []
    for s_num, l_num, desc, v_dict, m_dict in trace_steps:
        step_obj = {
            "step": s_num,
            "line": l_num,
            "description": desc,
            "variables": v_dict or {}
        }
        if m_dict:
            step_obj["memorySnapshots"] = m_dict
        trace.append(step_obj)
        
    q = {
        "id": f"Q{id_num:03d}",
        "category": category,
        "difficulty": difficulty,
        "title": title,
        "prompt": prompt,
        "code": code.strip(),
        "trapInfo": {
            "line": trap_line,
            "token": trap_token,
            "shortWarning": trap_warning
        },
        "options": opts,
        "explanation": {
            "summary": summary,
            "cStandardRef": std_ref,
            "deepDive": deep_dive
        },
        "executionTrace": trace
    }
    questions.append(q)

print("Base syllabus question generator ready.")
