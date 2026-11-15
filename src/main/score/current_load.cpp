// scoredat_load_for_cur(). -O- keeps the compiler from merging the early
// return on a failed open with the final RET, which the original keeps apart.
#pragma option -zCSCORE_IO_TEXT -zPmain_01 -k- -O-
#include "src/main/score/current.hpp"
#pragma codeseg SCORE_IO_TEXT main_01
#include "src/main/score/current_seek.inl"
#include "src/main/score/current_load.inl"
