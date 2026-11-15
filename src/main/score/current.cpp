// Loading and saving the current character's and rank's section of
// GENSOU.SCR through raw INT 21h calls, both in one file. The original load
// function is only reproduced by current_load.cpp (see NOTES.md); save is
// built from current_save.cpp. All three share the bodies in the .inl files.
#pragma option -zCSCORE_IO_TEXT -zPmain_01 -k-
#include "src/main/score/current.hpp"
#pragma codeseg SCORE_IO_TEXT main_01

#include "src/main/score/current_seek.inl"
#include "src/main/score/current_load.inl"
#include "src/main/score/current_save.inl"
