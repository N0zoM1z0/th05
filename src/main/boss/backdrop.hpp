// Boss backdrop rendering. Each boss sets [boss_backdrop_colorfill] to a
// function that fills the playfield area outside the backdrop image.
#ifndef TH05_MAIN_BOSS_BACKDROP_HPP
#define TH05_MAIN_BOSS_BACKDROP_HPP
#include "src/main/boss/background.hpp"

typedef void (near pascal *near BackdropColorfill)(void);
extern BackdropColorfill boss_backdrop_colorfill;

// The CDG and GRCG functions themselves are declared in background.hpp.
typedef char backdrop_color_callback_is_2[
    (sizeof(boss_backdrop_colorfill) == 2) ? 1 : -1];
typedef char backdrop_color_argument_is_1[(sizeof(vc_t) == 1) ? 1 : -1];
#endif
