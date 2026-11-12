// Four 7+sentinel far-pointer groups and their quarter-screen selectors.
#ifndef TH05_MAINE_ALLCAST_BACKGROUND_INDEX_HPP
#define TH05_MAINE_ALLCAST_BACKGROUND_INDEX_HPP
#include "src/shared/abi.hpp"
// C-defined original filenames keep their C ABI across the native C++ index.
extern "C" char allcast_background_filenames[4][7][10];
extern const char far *BG_FN[4][8];
extern int BG_QUARTER[4][8];
#endif
