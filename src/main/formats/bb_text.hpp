// Two text-dissolve .BB payloads share one allocated segment.
#ifndef TH05_BB_TEXT_HPP
#define TH05_BB_TEXT_HPP
#include "src/main/formats/bb_load.hpp"

extern bb_tiles8_t __seg *bb_txt_seg;
extern char bb_txt_fn[8];

#pragma codeseg _TEXT
extern "C" void pascal far hmem_free(void __seg *block);
#pragma codeseg BB_TEXT_LOAD_TEXT main_01
extern "C" void pascal near bb_txt_load(void);
extern "C" void pascal near bb_txt_free(void);
#pragma codeseg
#endif
