# generate_questions.py
# Generates all 100 high-yield C Midterm Exam questions with rigorous ISO C99/C11 compliance,
# execution traces, memory layouts, trap token locators, and distractor breakdowns.

import json

questions = []

def add_q(id_num, category, difficulty, title, prompt, code, trap_line, trap_token, trap_warning, 
          options_tuples, summary, std_ref, deep_dive, trace_steps):
    """
    options_tuples: list of (key, text, is_correct, why_tempting, why_wrong)
    trace_steps: list of (step_num, line_num, desc, vars_dict, mem_dict)
    """
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

print("Helper defined. Ready to populate questions.")
