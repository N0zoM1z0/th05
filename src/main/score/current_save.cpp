// Real DOS write interface for the current character/rank score section.
#pragma option -zCSCORE_IO_TEXT -zPmain_01 -k-
#include "src/main/score/current.hpp"
#pragma codeseg SCORE_IO_TEXT main_01
#include "src/main/score/current_seek.inl"
#include "src/main/score/current_save.inl"
