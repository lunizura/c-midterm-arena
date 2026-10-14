@echo off
echo =======================================================
echo   Compiling C Midterm Arena (CLI + Desktop Windows)
echo =======================================================

echo [1/3] Exporting questions data into C headers...
python export_c_header.py

echo [2/3] Compiling CLI Edition (c_arena_cli.exe)...
gcc -O2 -std=c99 src/main_cli.c src/questions.c -o c_arena_cli.exe
if %errorlevel% neq 0 (
    echo [ERROR] Failed to compile c_arena_cli.exe
    exit /b 1
)
echo      -^> c_arena_cli.exe successfully built!

echo [3/3] Compiling Desktop Window Launcher (c_arena_desktop.exe)...
gcc -O2 -mwindows src/app_launcher.c -o c_arena_desktop.exe
if %errorlevel% neq 0 (
    echo [ERROR] Failed to compile c_arena_desktop.exe
    exit /b 1
)
echo      -^> c_arena_desktop.exe successfully built!

echo =======================================================
echo   BUILD COMPLETE!
echo   Run: .\c_arena_cli.exe     (for Terminal Game)
echo   Run: .\c_arena_desktop.exe (for Desktop Window App)
echo =======================================================
