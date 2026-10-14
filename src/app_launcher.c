/*
 * c_arena_desktop - Native Windows C Desktop Launcher
 * Launches the full-screen C Midterm Arena standalone desktop application window
 */

#include <windows.h>
#include <stdio.h>
#include <stdlib.h>

int WINAPI WinMain(HINSTANCE hInstance, HINSTANCE hPrevInstance, LPSTR lpCmdLine, int nCmdShow) {
    char currentDir[MAX_PATH];
    GetCurrentDirectoryA(MAX_PATH, currentDir);

    char htmlPath[MAX_PATH + 64];
    snprintf(htmlPath, sizeof(htmlPath), "%s\\c_midterm_arena.html", currentDir);

    // Try launching Microsoft Edge in standalone PWA / App Mode (no URL bar, no tabs)
    char cmdLine[1024];
    snprintf(cmdLine, sizeof(cmdLine), "msedge.exe --app=\"file:///%s\"", htmlPath);

    STARTUPINFOA si;
    PROCESS_INFORMATION pi;
    ZeroMemory(&si, sizeof(si));
    si.cb = sizeof(si);
    ZeroMemory(&pi, sizeof(pi));

    if (CreateProcessA(NULL, cmdLine, NULL, NULL, FALSE, 0, NULL, NULL, &si, &pi)) {
        CloseHandle(pi.hProcess);
        CloseHandle(pi.hThread);
        return 0;
    }

    // Fallback: Default system browser
    ShellExecuteA(NULL, "open", htmlPath, NULL, NULL, SW_SHOWNORMAL);
    return 0;
}
