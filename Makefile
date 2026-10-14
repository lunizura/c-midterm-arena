CC = gcc
CFLAGS = -O2 -std=c99 -Wall
CLI_TARGET = c_arena_cli.exe
DESKTOP_TARGET = c_arena_desktop.exe

all: $(CLI_TARGET) $(DESKTOP_TARGET)

$(CLI_TARGET): src/main_cli.c src/questions.c src/questions.h
	$(CC) $(CFLAGS) src/main_cli.c src/questions.c -o $(CLI_TARGET)

$(DESKTOP_TARGET): src/app_launcher.c
	$(CC) $(CFLAGS) -mwindows src/app_launcher.c -o $(DESKTOP_TARGET)

clean:
	rm -f $(CLI_TARGET) $(DESKTOP_TARGET) *.o
