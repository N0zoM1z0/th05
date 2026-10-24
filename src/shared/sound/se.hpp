// TH05 sound-effect state and driver API. Natural source provenance:
// ReC98 b6ba5b0a529edbb31efdf8c0e939263804f8ee47, th02/snd/se.cpp,
// th04/snd/snd.h and th04/snd/se_priority[data].asm.
#ifndef TH05_SHARED_SOUND_SE_HPP
#define TH05_SHARED_SOUND_SE_HPP
#include "src/shared/abi.hpp"
#if GAME != 5
#error This owner is the TH05 sound-effect controller
#endif

enum snd_se_mode_t {
    SND_SE_OFF = 0,
    SND_SE_FM = 1,
    SND_SE_BEEP = 2,
    SND_SE_MODE_COUNT = 3,
    _snd_se_mode_t_FORCE_INT16 = 0x7FFF
};
static const unsigned char SE_NONE = 0xFF;
static const unsigned int SE_PRIORITY_COUNT = 17;
static const unsigned char PMD_SE_PLAY = 0x0C;
#define SE_PMD_INTERRUPT 0x60

extern "C" {
    extern unsigned char snd_se_mode;
    extern unsigned char snd_se_playing;
    extern unsigned char snd_se_frame;
    extern unsigned char snd_se_priorities[SE_PRIORITY_COUNT];
    extern unsigned char snd_se_priority_frames[SE_PRIORITY_COUNT];
    int pascal far bgm_sound(int effect);
    void pascal far snd_se_play(int new_se);
    void far snd_se_update(void);
}
typedef char th05_se_mode_enum_is_2[(sizeof(snd_se_mode_t) == 2) ? 1 : -1];
typedef char th05_se_priority_table_is_17[(sizeof(snd_se_priorities) == 17) ? 1 : -1];
typedef char th05_se_priority_frames_is_17[(sizeof(snd_se_priority_frames) == 17) ? 1 : -1];
#endif
