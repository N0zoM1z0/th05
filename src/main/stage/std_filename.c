// Filename of the stage script (.STD) file. std_load() refers to it as std_fn
// and replaces the second digit with the stage number.
#pragma option -zCSTD_FILENAME_TEXT -zPmain_01
#ifdef __cplusplus
#error This file must be compiled as C
#endif
#include "src/main/stage/std_filename_c.h"
MainStdFilename near main_std_filename = { "ST00.STD" };
