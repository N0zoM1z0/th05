// Real Louise movement provider for the frozen accepted callback interface.
#ifndef TH05_MAIN_BOSS_LOUISE_FLYSTEP_HPP
#define TH05_MAIN_BOSS_LOUISE_FLYSTEP_HPP
#include "src/main/boss/louise/update.hpp"

#pragma codeseg SHARED
extern "C" void pascal far vector2(int &ret_x, int &ret_y,
    unsigned char angle, int length);
#pragma codeseg B4_UPDATE_TEXT main_03

#endif
