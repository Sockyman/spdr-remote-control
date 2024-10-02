// This program takes the scancode table written by hand in
// stdlib/getc.spdr and converts it from changing scancode -> character
// into character -> scancode.
// This is used for the keyboard emulator.

#include <stdio.h>
#include <string.h>

#define KEY_ENTER  "\x0a"
#define KEY_BSPC   "\x08"
#define KEY_INSERT  "\x19"
#define KEY_ESC    "\x1b"
#define KEY_LEFT   "\x11"
#define KEY_UP     "\x12"
#define KEY_RIGHT  "\x13"
#define KEY_DOWN   "\x14"
#define KEY_DELETE  "\x7f"

#define KEY_INVALID  '~'

#define MAP_SIZE 128

const char lowercaseAsciiMap[] = 
    "~~~~~~~~~~~~~ `~"
    "~~~~~q1~~~zsaw2~"
    "~cxde43~~ vftr5~"
    "~nbhgy6~~~mju78~"
    "~,kio09~~./l;p-~"
    "~~'~[=~~~~" KEY_ENTER "]~\\~~"
    "~~~~~~" KEY_BSPC "~~1~" KEY_LEFT "7~~~"
    KEY_INSERT KEY_DELETE KEY_DOWN "5" KEY_RIGHT KEY_UP KEY_ESC "~~+3-*9~~";

const char upercaseAsciiMap[] =
    "~~~~~~~~~~~~~ `~"
    "~~~~~Q!~~~ZSAW@~"
    "~CXDE$#~~ VFTR%~"
    "~NBHGY^~~~MJU&*~"
    "~<KIO)(~~>?L:P_~"
    "~~\"~{+~~~~" KEY_ENTER "}~|~~"
    "~~~~~~" KEY_BSPC "~~1~" KEY_LEFT "7~~~"
    KEY_INSERT KEY_DELETE KEY_DOWN "5" KEY_RIGHT KEY_UP KEY_ESC "~~+3_*9~~";

void appendTable(const char* asciiMap, unsigned char* scancodeMap, int offset) {
    for (int i = 0; i < MAP_SIZE; ++i) {
        char c = asciiMap[i];
        if (c == KEY_INVALID) {
            continue;
        }
        scancodeMap[c] = (char)(i + offset);
    }
}

int main() {
    unsigned char scancodeMap[MAP_SIZE * 2];
    memset(scancodeMap, 0, MAP_SIZE * 2);

    appendTable(lowercaseAsciiMap, scancodeMap, 0);
    appendTable(upercaseAsciiMap, scancodeMap, MAP_SIZE);

    for (int i = 0; i < MAP_SIZE * 2; ++i) {
        fprintf(stdout, "0x%x, ", scancodeMap[i]);
    }
    return 0;
}

