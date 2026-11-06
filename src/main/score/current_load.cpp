// DOS carry-return control flow requires the non-folding compiler profile.
#pragma option -zCSCORE_IO_TEXT -zPmain_01 -k- -O-
#include "src/main/score/current.hpp"
#pragma codeseg SCORE_IO_TEXT main_01
#include "src/main/score/current_seek.inl"
#include "src/main/score/current_load.inl"
