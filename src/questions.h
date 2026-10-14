#ifndef QUESTIONS_H
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
