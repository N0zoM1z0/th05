// Curved-bullet masks: sixteen 32x32 monochrome sprites in one .BB payload.
#ifndef TH05_BB_CHEETO_HPP
#define TH05_BB_CHEETO_HPP
#include "src/main/formats/bb_load.hpp"

extern bb_tiles8_t bb_cheeto[BB_SIZE];
extern char bb_cheeto_fn[8];

#pragma codeseg BB_CHEETO_LOAD_TEXT main_01
extern "C" void pascal near bb_cheeto_load(void);
#pragma codeseg
#endif
