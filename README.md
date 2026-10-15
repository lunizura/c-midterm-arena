# ⚡ C Midterm Arena

[![Language](https://img.shields.io/badge/Language-Pure%20C%20(C99%2FC11)-00599C?style=for-the-badge&logo=c)](https://en.wikipedia.org/wiki/C_(programming_language))
[![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20Web-0078D6?style=for-the-badge)](https://github.com/)
[![License](https://img.shields.io/badge/License-MIT-green.svg?style=for-the-badge)](LICENSE)
[![Questions](https://img.shields.io/badge/Question%20Bank-100%20Verified%20Traps-orange?style=for-the-badge)](src/questions.h)

> **The ultimate interactive desktop mastery game for university C midterm exams (*Konsep Pemrograman* / *Dasar Pemrograman* / CS101).**  
> Features 100 curated exam traps, line-by-line machine execution stepping, visual memory diagrams, cognitive distractor analysis, and procedural retro sound effects.

---

## 🎮 Dual Editions Included

This repository comes with **two complete editions**:

| Edition | Technology | Highlights |
|---|---|---|
| **🖥️ Desktop Window App** (`c_arena_desktop.exe`) | Native C Windows GUI Launcher + Cyber-Glass Engine | Translucent frosted glass, 60fps canvas particles, mechanical keyboard sound effects, interactive memory diagrams, and zero browser tabs/URL bars. |
| **⚡ Terminal CLI Edition** (`c_arena_cli.exe`) | 100% Pure C (`<stdio.h>`, `<windows.h>`) | ANSI color escape syntax highlighting, interactive line-by-line terminal debugger stepper, and hardware audio chimes via `Beep()`. |
| **🌐 Standalone Web Edition** (`c_midterm_arena.html`) | Single-file HTML5/CSS/JS (247 KB) | 100% offline, zero install, shareable via WhatsApp/Discord or hostable on GitHub Pages. |

---

## 📚 100 Exam Traps Strictly Calibrated to the 6 Course Modules

Every single question is strictly calibrated to the official university midterm syllabus for *Konsep Pemrograman*, testing real multiple-choice exam traps:

1. **Data Types & Variables (16 Qs)**: Primitive sizes & formats (`%d`, `%f`, `%c`, `%lf`), integer overflow & wrap-around, character ASCII mechanics (`'5' - '0'`), floating-point division (`5 / 2 = 2`), implicit type conversion, variable shadowing, and `const` qualifiers.
2. **Operators & Expressions (18 Qs)**: Precedence & associativity rules, post-increment vs pre-increment (`x++` vs `++x`), compound assignment quirks (`x *= y + 1`), logical short-circuit evaluation (`&&` and `||`), bitwise shifts (`<<`, `>>`, `&`, `|`, `^`), and modulo sign rules.
3. **Conditionals (if / switch) (16 Qs)**: The assignment bug in condition `if (x = 5)`, floating-point comparison pitfalls, dangling `else` binding to the nearest `if`, `switch` fallthrough without `break`, duplicate case constants, and ternary operator nesting.
4. **Loops (for / while / do-while) (18 Qs)**: The accidental semicolon trap (`for (...);` / `while (...);`), post-increment in loop tests, off-by-one boundary conditions, `break` vs `continue` behaviors in nested loops, and `do-while` guaranteed first execution.
5. **Functions & Procedures (16 Qs)**: Pass-by-value mechanics (local modifications do not affect caller), function declaration vs definition, implicit return values, recursive call stack unwinding & base case verification, and static local variable persistence across invocations.
6. **Arrays & Strings (16 Qs)**: 0-based indexing and buffer boundary traps (`arr[N]`), partial array initialization zero-padding, multidimensional matrix row-major storage `arr[row][col]`, string null terminators `\0`, `sizeof(arr)` vs length, and `char s[] = "hi"` vs character arrays.

---

## 🔍 Features

* **Line-by-Line Execution Stepper**: Scrub forward and backward line-by-line through the C code to watch variables update in real time.
* **Stack Memory & Pointer Architecture**: Visual memory boxes showing variable names, stack addresses (`0x1000`, `0x1004`), and pointer arrows.
* **The Trap Spotlight**: Highlights the exact offending token (`⚠️ *p++`, `;`, or `unsigned`) with a warning badge.
* **Distractor Psychology**: Explains *why* you were tempted to choose the wrong option and breaks down the underlying mental fallacy.
* **Audio Synthesizer**: Procedural audio without external audio files—tactile mechanical "thock" clicks, victory arpeggios, and error thuds.
* **Game Modes**:
  * 📖 **Study Mode**: Untimed, instant explanations and execution stepper.
  * ⚡ **Exam Rush**: 30 randomized questions under exam conditions.
  * 💀 **Survival Mode**: 3 lives, score multipliers, and streak tracking.

---

## 🚀 Quickstart & Building from Source

### Prerequisites
* Windows 10/11
* GCC compiler (MinGW, w64devkit, or MSYS2)
* Python 3.x (only used if modifying question data)

### 1-Click Build (Windows)
Double-click `build.bat` or run in PowerShell:
```cmd
.\build.bat
```

### Manual Compilation
```bash
# 1. Compile the Pure C Terminal CLI Game
gcc -O2 -std=c99 src/main_cli.c src/questions.c -o c_arena_cli.exe

# 2. Compile the Desktop Window App Launcher
gcc -O2 -mwindows src/app_launcher.c -o c_arena_desktop.exe
```

---

## ⌨️ Controls & Shortcuts

| Key | Action |
|---|---|
| `1`, `2`, `3`, `4` or `A`, `B`, `C`, `D` | Select Multiple Choice Option |
| `Space` or `Enter` | Next Question |
| `Left Arrow` / `Right Arrow` | Step Execution Back / Forward |
| `B` | Bookmark / Star Question for review |
| `M` | Mute / Unmute Audio Synthesizer |
| `T` (CLI mode) | Open Terminal Line-by-Line Stepper |

---

## 📤 How to Push to GitHub

To publish this project on your personal GitHub account:

1. **Create a new repository on GitHub** (e.g. `c-midterm-arena`).
2. Run the following commands in this directory:
   ```bash
   git init
   git add .
   git commit -m "Initial commit: C Midterm Arena v1.0.0"
   git branch -M main
   git remote add origin https://github.com/<YOUR-USERNAME>/c-midterm-arena.git
   git push -u origin main
   ```
3. *(Optional)* Turn on **GitHub Pages** in your repo settings (pointing to `main` branch root) to make the web edition playable online via a public link!

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).
