// File and song names used by the High Score viewer and its menu.
#pragma option -zCSCORE_FILES_TEXT -zPop_01
#include "src/op/hiscore/files.hpp"

// Declared `extern` in files.hpp first, so that this const object gets
// external linkage.
const hiscore_filenames_t near hi_filenames = {
    "GENSOU.SCR",
    "name",
    "hi01.pi",
    "op1.pi",
    "op",
    "scnum.bft",
    "hi_m.bft"
};
