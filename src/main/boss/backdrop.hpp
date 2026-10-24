// Real GAME5 backdrop interface and GRCG raw-helper contract.
// Natural provenance: ReC98 b6ba5b0a, boss/backdrop.cpp and hardware/grcg.hpp.
#ifndef TH05_MAIN_BOSS_BACKDROP_HPP
#define TH05_MAIN_BOSS_BACKDROP_HPP
#include "src/main/boss/background.hpp"

typedef void (near pascal *near BackdropColorfill)(void);
extern BackdropColorfill boss_backdrop_colorfill;

// background.hpp already declares the genuine near functions and far CDG
// service. Its GRCG color macro supplies AH to the real void raw helper.
typedef char backdrop_color_callback_is_2[
    (sizeof(boss_backdrop_colorfill) == 2) ? 1 : -1];
typedef char backdrop_color_argument_is_1[(sizeof(vc_t) == 1) ? 1 : -1];
#endif
