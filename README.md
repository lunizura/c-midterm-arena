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
| **🌐 Standalone Web Edition** (`c_midterm_arena.html`) | Single-file HTML5/CSS/JS (274 KB) | 100% offline, zero install, shareable via WhatsApp/Discord or hostable on GitHub Pages. |

---

## 📚 100 Exam Traps Across 8 Categories

College professors design multiple-choice C midterm exams around specific cognitive traps. Every single question in this arena is verified against ISO C standards (**ISO/IEC 9899**):

1. **Operator Precedence & Short-Circuiting (14 Qs)**: `*p++` vs `(*p)++`, `a++ || b++` skipping `b++`, `1 << 2 + 3`, ternary grouping.
2. **Pointer Arithmetic & Array Decay (18 Qs)**: `arr` vs `&arr` strides, `sizeof` decay in functions, commutative `i[arr]`, pointer differences.
3. **Integer Promotions & Truncation (14 Qs)**: `5 / 2` truncation, signed vs unsigned comparison (`-1 < 1U`), float literal precision (`0.1f == 0.1`).
4. **Strings & Null Terminators (12 Qs)**: String literal immutability (`.rodata` segfault), `sizeof` vs `strlen`, `char s[5] = "hello"` bounds overread.
5. **Scope, Storage Duration & Memory (12 Qs)**: `static` variable retention, dangling stack pointer returns, inner block shadowing.
6. **Sequence Points & Undefined Behavior (10 Qs)**: Unsequenced `i = i++`, unsequenced `arr[i] = i++`, signed overflow UB.
7. **Control Flow Quirks & Semicolons (10 Qs)**: Accidental `if (x > 5);`, `for (...);`, `switch` fallthrough without `break`, `if (x = 5)`.
8. **Preprocessor Macro Hazards (10 Qs)**: `SQUARE(2 + 3)` expanding to `2 + 3 * 2 + 3 = 11`, macro side effect duplication (`DOUBLE(x++)`).

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
