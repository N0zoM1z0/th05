// Packed sound-file extensions and initial driver mode state.
#include <stddef.h>

typedef struct {
    char se_extension[4];
    char fm26_extension[4];
    char fm86_midi_strings[7];
    unsigned char se_mode;
    unsigned char bgm_mode;
    unsigned char midi_possible;
} sound_load_resources_t;

sound_load_resources_t sound_load_resources = {
    "efc", "m", "m2\0mmd", 0, 0, 0
};

typedef char sound_load_resources_is_18[(sizeof(sound_load_resources_t) == 18) ? 1 : -1];
typedef char sound_mode_at_15[(offsetof(sound_load_resources_t, se_mode) == 15) ? 1 : -1];
typedef char sound_bgm_mode_at_16[(offsetof(sound_load_resources_t, bgm_mode) == 16) ? 1 : -1];
typedef char sound_midi_possible_at_17[(offsetof(sound_load_resources_t, midi_possible) == 17) ? 1 : -1];
