// Real DOS INT 21h registers are the file API, not local algorithm registers.
#pragma option -zCSCORE_IO_TEXT -zPmain_01 -k-
#include "src/main/score/current.hpp"
#pragma codeseg SCORE_IO_TEXT main_01

#include "src/main/score/current_seek.inl"
#include "src/main/score/current_load.inl"
#include "src/main/score/current_save.inl"
