# export_c_header.py
import json
from generate_syllabus_questions import add_q, questions
from syllabus_part1 import load_part1
from syllabus_part2 import load_part2
from syllabus_part3 import load_part3

load_part1(add_q)
load_part2(add_q)
load_part3(add_q)

def c_escape(s):
    if s is None:
        return '""'
    return json.dumps(str(s))

header_content = """#ifndef QUESTIONS_H
#define QUESTIONS_H

#include <stdbool.h>

typedef struct {
    char key;
    const char *text;
    bool is_correct;
    const char *why_tempting;
    const char *why_wrong;
} Option;

typedef struct {
    int step;
    int line;
    const char *description;
    const char *variables_summary;
} TraceStep;

typedef struct {
    const char *id;
    const char *category;
    const char *difficulty;
    const char *title;
    const char *prompt;
    const char *code;
    int trap_line;
    const char *trap_token;
    const char *trap_warning;
    Option options[4];
    const char *explanation_summary;
    const char *c_std_ref;
    const char *deep_dive;
    TraceStep trace[8];
    int trace_count;
} Question;

#define TOTAL_QUESTIONS 100
extern const Question ALL_QUESTIONS[TOTAL_QUESTIONS];

#endif // QUESTIONS_H
"""

with open("src/questions.h", "w", encoding="utf-8") as f:
    f.write(header_content)

c_content = ['#include "questions.h"\n\nconst Question ALL_QUESTIONS[TOTAL_QUESTIONS] = {\n']

for q in questions:
    c_content.append('  {\n')
    c_content.append(f'    .id = {c_escape(q["id"])},\n')
    c_content.append(f'    .category = {c_escape(q["category"])},\n')
    c_content.append(f'    .difficulty = {c_escape(q["difficulty"])},\n')
    c_content.append(f'    .title = {c_escape(q["title"])},\n')
    c_content.append(f'    .prompt = {c_escape(q["prompt"])},\n')
    c_content.append(f'    .code = {c_escape(q["code"])},\n')
    c_content.append(f'    .trap_line = {q["trapInfo"]["line"]},\n')
    c_content.append(f'    .trap_token = {c_escape(q["trapInfo"]["token"])},\n')
    c_content.append(f'    .trap_warning = {c_escape(q["trapInfo"]["shortWarning"])},\n')
    
    # Options
    c_content.append('    .options = {\n')
    for opt in q["options"]:
        c_content.append(f'      {{ .key = \'{opt["key"]}\', .text = {c_escape(opt["text"])}, .is_correct = {"true" if opt["isCorrect"] else "false"}, .why_tempting = {c_escape(opt["whyTempting"])}, .why_wrong = {c_escape(opt.get("whyWrong", "")) } }},\n')
    c_content.append('    },\n')
    
    # Explanation
    c_content.append(f'    .explanation_summary = {c_escape(q["explanation"]["summary"])},\n')
    c_content.append(f'    .c_std_ref = {c_escape(q["explanation"]["cStandardRef"])},\n')
    c_content.append(f'    .deep_dive = {c_escape(q["explanation"]["deepDive"])},\n')
    
    # Trace
    traces = q.get("executionTrace", [])
    trace_cnt = min(8, len(traces))
    c_content.append('    .trace = {\n')
    for i in range(trace_cnt):
        t = traces[i]
        vars_str = ", ".join(f"{k}={v}" for k, v in t.get("variables", {}).items())
        c_content.append(f'      {{ .step = {t["step"]}, .line = {t["line"]}, .description = {c_escape(t["description"])}, .variables_summary = {c_escape(vars_str)} }},\n')
    for i in range(trace_cnt, 8):
        c_content.append('      { 0, 0, "", "" },\n')
    c_content.append('    },\n')
    c_content.append(f'    .trace_count = {trace_cnt}\n')
    c_content.append('  },\n')

c_content.append('};\n')

with open("src/questions.c", "w", encoding="utf-8") as f:
    f.writelines(c_content)

print("Exported src/questions.h and src/questions.c with syllabus questions successfully!")
