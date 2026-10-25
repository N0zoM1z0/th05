// Readable, complete original semantic pool. No image/font/score payload.
#pragma option -zCSCORE_FILES_TEXT -zPop_01
#include "src/op/hiscore/files.hpp"

// Prior extern declaration preserves actual external const linkage.
const hiscore_filenames_t near hi_filenames = {
    "GENSOU.SCR",
    "name",
    "hi01.pi",
    "op1.pi",
    "op",
    "scnum.bft",
    "hi_m.bft"
};
