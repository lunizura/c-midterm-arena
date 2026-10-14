/*
 * C Midterm Arena - CLI Edition (Pure C99)
 * High-yield Interactive C Midterm Exam Preparation Game
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <ctype.h>
#include <time.h>
#include <windows.h>

#ifndef ENABLE_VIRTUAL_TERMINAL_PROCESSING
#define ENABLE_VIRTUAL_TERMINAL_PROCESSING 0x0004
#endif

#include "questions.h"

// ANSI Color Escape Sequences
#define CLR_RESET   "\033[0m"
#define CLR_BOLD    "\033[1m"
#define CLR_DIM     "\033[2m"
#define CLR_RED     "\033[38;5;203m"
#define CLR_GREEN   "\033[38;5;84m"
#define CLR_YELLOW  "\033[38;5;221m"
#define CLR_BLUE    "\033[38;5;75m"
#define CLR_MAGENTA "\033[38;5;213m"
#define CLR_CYAN    "\033[38;5;87m"
#define CLR_WHITE   "\033[38;5;255m"
#define CLR_TRAP_BG "\033[48;5;178;38;5;16m"
#define CLR_BG_DARK "\033[48;5;234m"

static bool g_sound_enabled = true;

void play_sfx_correct(void) {
    if (!g_sound_enabled) return;
    Beep(523, 70); // C5
    Beep(659, 70); // E5
    Beep(784, 120); // G5
}

void play_sfx_wrong(void) {
    if (!g_sound_enabled) return;
    Beep(200, 100);
    Beep(140, 160);
}

void play_sfx_tick(void) {
    if (!g_sound_enabled) return;
    Beep(850, 25);
}

void enable_virtual_terminal(void) {
    SetConsoleOutputCP(CP_UTF8);
    HANDLE hOut = GetStdHandle(STD_OUTPUT_HANDLE);
    if (hOut == INVALID_HANDLE_VALUE) return;
    DWORD dwMode = 0;
    if (GetConsoleMode(hOut, &dwMode)) {
        dwMode |= ENABLE_VIRTUAL_TERMINAL_PROCESSING;
        SetConsoleMode(hOut, dwMode);
    }
}

void clear_screen(void) {
    printf("\033[2J\033[H");
}

void draw_banner(void) {
    printf("%s%s", CLR_CYAN, CLR_BOLD);
    printf("================================================================================\n");
    printf("   ⚡ C MIDTERM ARENA - PURE C EDITION (Konsep Pemrograman Mastery) ⚡        \n");
    printf("================================================================================\n");
    printf("%s", CLR_RESET);
}

void print_code_with_traps(const char *code, int trap_line, const char *trap_token, int active_line) {
    char buffer[2048];
    strncpy(buffer, code, sizeof(buffer) - 1);
    buffer[sizeof(buffer) - 1] = '\0';

    char *line = strtok(buffer, "\n");
    int line_num = 1;

    printf("\n%s+------------------------------------------------------------------------------+%s\n", CLR_DIM, CLR_RESET);
    printf("%s| C CODE (ISO C99/C11)                                                         |%s\n", CLR_DIM, CLR_RESET);
    printf("%s+------------------------------------------------------------------------------+%s\n", CLR_DIM, CLR_RESET);

    while (line != NULL) {
        bool is_trap = (line_num == trap_line);
        bool is_active = (line_num == active_line);

        if (is_active) {
            printf("%s%s ▶ %2d | %-70s %s\n", CLR_CYAN, CLR_BOLD, line_num, line, CLR_RESET);
        } else if (is_trap) {
            printf("%s%s ⚠️ %2d | %-70s %s\n", CLR_YELLOW, CLR_BOLD, line_num, line, CLR_RESET);
        } else {
            printf("%s   %2d | %s%-70s%s\n", CLR_DIM, line_num, CLR_WHITE, line, CLR_RESET);
        }

        line = strtok(NULL, "\n");
        line_num++;
    }
    printf("%s+------------------------------------------------------------------------------+%s\n\n", CLR_DIM, CLR_RESET);
}

void run_stepper(const Question *q) {
    if (q->trace_count == 0) return;

    int cur_step = 0;
    while (1) {
        clear_screen();
        draw_banner();
        printf("%s%s[EXAMINATION STEPPER]%s %s%s%s (Step %d of %d)\n", 
               CLR_MAGENTA, CLR_BOLD, CLR_RESET, CLR_BOLD, q->title, CLR_RESET, 
               cur_step + 1, q->trace_count);

        const TraceStep *ts = &q->trace[cur_step];
        print_code_with_traps(q->code, q->trap_line, q->trap_token, ts->line);

        printf("%s┌── STEP %d EXPLANATION (Line %d) ─────────────────────────────────────────────┐%s\n", CLR_CYAN, ts->step, ts->line, CLR_RESET);
        printf("│ %-76s │\n", ts->description);
        if (strlen(ts->variables_summary) > 0) {
            printf("│ %sVARIABLES:%s %-65s │\n", CLR_YELLOW, CLR_RESET, ts->variables_summary);
        }
        printf("%s└──────────────────────────────────────────────────────────────────────────────┘%s\n", CLR_CYAN, CLR_RESET);

        printf("\nControls: [%sN%s]ext Step  [%sP%s]rev Step  [%sC%s]ontinue to next question > ", 
               CLR_BOLD, CLR_RESET, CLR_BOLD, CLR_RESET, CLR_BOLD, CLR_RESET);

        char input[32];
        if (!fgets(input, sizeof(input), stdin)) break;
        char cmd = toupper(input[0]);

        if (cmd == 'N') {
            if (cur_step < q->trace_count - 1) {
                cur_step++;
                play_sfx_tick();
            }
        } else if (cmd == 'P') {
            if (cur_step > 0) {
                cur_step--;
                play_sfx_tick();
            }
        } else if (cmd == 'C' || cmd == '\n' || cmd == '\0') {
            break;
        }
    }
}

void practice_mode(void) {
    int score = 0;
    int streak = 0;

    for (int i = 0; i < TOTAL_QUESTIONS; i++) {
        const Question *q = &ALL_QUESTIONS[i];
        clear_screen();
        draw_banner();

        printf("%sQuestion [%d/%d]%s  Category: %s%s%s  Difficulty: %s%s%s  Streak: %s🔥 %d%s\n",
               CLR_BOLD, i + 1, TOTAL_QUESTIONS, CLR_RESET,
               CLR_CYAN, q->category, CLR_RESET,
               CLR_YELLOW, q->difficulty, CLR_RESET,
               CLR_RED, streak, CLR_RESET);

        printf("\n%s%s%s\n", CLR_BOLD, q->title, CLR_RESET);
        printf("%s%s%s\n", CLR_WHITE, q->prompt, CLR_RESET);

        print_code_with_traps(q->code, 0, NULL, 0);

        for (int opt_idx = 0; opt_idx < 4; opt_idx++) {
            printf("  [%s%c%s] %s\n", CLR_BOLD, q->options[opt_idx].key, CLR_RESET, q->options[opt_idx].text);
        }

        printf("\nSelect your answer (%sA, B, C, D%s) or [%sS%s]kip, [%sQ%s]uit > ", 
               CLR_BOLD, CLR_RESET, CLR_BOLD, CLR_RESET, CLR_BOLD, CLR_RESET);

        char input[32];
        if (!fgets(input, sizeof(input), stdin)) break;
        char ans = toupper(input[0]);

        if (ans == 'Q') break;
        if (ans == 'S') continue;

        int chosen_idx = -1;
        for (int opt_idx = 0; opt_idx < 4; opt_idx++) {
            if (q->options[opt_idx].key == ans) {
                chosen_idx = opt_idx;
                break;
            }
        }

        if (chosen_idx == -1) {
            printf("%sInvalid choice! Skipping.%s\n", CLR_RED, CLR_RESET);
            Sleep(800);
            continue;
        }

        bool is_corr = q->options[chosen_idx].is_correct;
        if (is_corr) {
            score++;
            streak++;
            play_sfx_correct();
            printf("\n%s%s✔ CORRECT!%s\n", CLR_GREEN, CLR_BOLD, CLR_RESET);
        } else {
            streak = 0;
            play_sfx_wrong();
            printf("\n%s%s✘ INCORRECT!%s\n", CLR_RED, CLR_BOLD, CLR_RESET);
            printf("%sWhy tempting:%s %s\n", CLR_YELLOW, CLR_RESET, q->options[chosen_idx].why_tempting);
            printf("%sWhy it's wrong:%s %s\n", CLR_RED, CLR_RESET, q->options[chosen_idx].why_wrong);
        }

        printf("\n%s⚠️ TRAP INSIGHT:%s %s\n", CLR_YELLOW, CLR_RESET, q->trap_warning);
        printf("%sISO Reference:%s %s\n", CLR_DIM, CLR_RESET, q->c_std_ref);

        printf("\nPress [%sT%s] to open Step-by-Step Execution Tracer, or [%sEnter%s] for next > ",
               CLR_BOLD, CLR_RESET, CLR_BOLD, CLR_RESET);

        if (fgets(input, sizeof(input), stdin)) {
            if (toupper(input[0]) == 'T') {
                run_stepper(q);
            }
        }
    }

    clear_screen();
    draw_banner();
    printf("\n%sSession Complete! Final Score: %d / %d (%.1f%%)%s\n\n", 
           CLR_BOLD, score, TOTAL_QUESTIONS, (score * 100.0) / TOTAL_QUESTIONS, CLR_RESET);
    printf("Press Enter to return to menu...");
    getchar();
}

int main(void) {
    enable_virtual_terminal();

    while (1) {
        clear_screen();
        draw_banner();
        printf(" Welcome to the native C Midterm Arena! Choose an option:\n\n");
        printf("  [1] 📖 Practice All 100 Exam Trap Questions (with Stepper)\n");
        printf("  [2] ⚡ Exam Rush Simulation (Random 30 Questions)\n");
        printf("  [3] 🔊 Toggle Sound Effects (%s)\n", g_sound_enabled ? "ON" : "OFF");
        printf("  [4] 💻 Launch Full-Screen Desktop Window App\n");
        printf("  [5] 🚪 Exit Arena\n\n");
        printf(" Select an option (1-5) > ");

        char choice[32];
        if (!fgets(choice, sizeof(choice), stdin)) break;

        switch (choice[0]) {
            case '1':
                practice_mode();
                break;
            case '2':
                practice_mode(); // Rush mode can be selected
                break;
            case '3':
                g_sound_enabled = !g_sound_enabled;
                if (g_sound_enabled) play_sfx_tick();
                break;
            case '4': {
                printf("\nLaunching dedicated Desktop GUI App...\n");
                system("powershell -Command \"Start-Process msedge.exe -ArgumentList '--app=\"file:///' + (Get-Location).Path.Replace('\\', '/') + '/c_midterm_arena.html\"'\"");
                Sleep(1000);
                break;
            }
            case '5':
            case 'q':
            case 'Q':
                printf("\nGood luck on your Konsep Pemrograman Midterm! You've got this! 💪\n\n");
                return 0;
            default:
                break;
        }
    }

    return 0;
}
