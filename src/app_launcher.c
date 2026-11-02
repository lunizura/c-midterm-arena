/*
 * c_arena_desktop - Native Windows C Desktop Launcher
 * Launches the full-screen C Midterm Arena standalone desktop application window
 */

#include <windows.h>
#include <stdio.h>
#include <stdlib.h>

int WINAPI WinMain(HINSTANCE hInstance, HINSTANCE hPrevInstance, LPSTR lpCmdLine, int nCmdShow) {
    (void)hInstance; (void)hPrevInstance; (void)lpCmdLine; (void)nCmdShow;

    char exePath[MAX_PATH];
    GetModuleFileNameA(NULL, exePath, MAX_PATH);

    // Extract directory of current executable
    char *lastSlash = strrchr(exePath, '\\');
    if (lastSlash) {
        *lastSlash = '\0';
    }

    char htmlPath[MAX_PATH + 64];
    snprintf(htmlPath, sizeof(htmlPath), "%s\\c_midterm_arena.html", exePath);

    char targetUrl[MAX_PATH + 128];
    if (GetFileAttributesA(htmlPath) != INVALID_FILE_ATTRIBUTES) {
        snprintf(targetUrl, sizeof(targetUrl), "file:///%s", htmlPath);
    } else {
        snprintf(htmlPath, sizeof(htmlPath), "%s\\index.html", exePath);
        if (GetFileAttributesA(htmlPath) != INVALID_FILE_ATTRIBUTES) {
            snprintf(targetUrl, sizeof(targetUrl), "file:///%s", htmlPath);
        } else {
            // Check current working directory as tertiary fallback
            char currentDir[MAX_PATH];
            GetCurrentDirectoryA(MAX_PATH, currentDir);
            snprintf(htmlPath, sizeof(htmlPath), "%s\\c_midterm_arena.html", currentDir);
            if (GetFileAttributesA(htmlPath) != INVALID_FILE_ATTRIBUTES) {
                snprintf(targetUrl, sizeof(targetUrl), "file:///%s", htmlPath);
            } else {
                // Online hosted edition fallback for standalone releases
                snprintf(targetUrl, sizeof(targetUrl), "https://lunizura.github.io/c-midterm-arena/");
            }
        }
    }

    // Try launching Microsoft Edge in standalone PWA / App Mode (no URL bar, no tabs)
    char cmdLine[1024];
    snprintf(cmdLine, sizeof(cmdLine), "msedge.exe --app=\"%s\"", targetUrl);

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
    ShellExecuteA(NULL, "open", targetUrl, NULL, NULL, SW_SHOWNORMAL);
    return 0;
}
