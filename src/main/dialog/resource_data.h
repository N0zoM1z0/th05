/* Complete mutable dialog filename, tiny text-buffer and sequence state bank. */
#ifndef TH05_DIALOG_RESOURCE_DATA_H
#define TH05_DIALOG_RESOURCE_DATA_H
#include <stddef.h>

typedef struct DialogResourceBank {
    signed char sequence_id;
    char script_file[10];
    char kanji_buffer[3];
    char extra_bitmap_a[9];
    char extra_bitmap_b[9];
    char extra_bgm[6];
    char extra_replay[10];
    char return_binary[3];
    char boss_faceset[9];
    char playchar_faceset[9];
    char bomb_bg_reimu[8];
    char bomb_bg_marisa[8];
    char bomb_bg_mima[8];
    char bomb_bg_yuuka[8];
    char extra_sprites[12];
    char bomb_shape_yuuka[10];
    char bomb_shape_other[10];
} DialogResourceBank;

extern DialogResourceBank near dialog_resources;

typedef char dialog_bank_size[(sizeof(DialogResourceBank) == 133) ? 1 : -1];
typedef char dialog_bank_script[(offsetof(DialogResourceBank, script_file) == 1) ? 1 : -1];
typedef char dialog_bank_buffer[(offsetof(DialogResourceBank, kanji_buffer) == 11) ? 1 : -1];
typedef char dialog_bank_extra_bitmap[(offsetof(DialogResourceBank, extra_bitmap_a) == 14) ? 1 : -1];
typedef char dialog_bank_faceset[(offsetof(DialogResourceBank, boss_faceset) == 51) ? 1 : -1];
typedef char dialog_bank_bomb_bg[(offsetof(DialogResourceBank, bomb_bg_reimu) == 69) ? 1 : -1];
typedef char dialog_bank_last[(offsetof(DialogResourceBank, bomb_shape_other) == 123) ? 1 : -1];
#endif
