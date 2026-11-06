// Full .BB payload and the real near Pascal far-filename/segment-result API.
#ifndef TH05_BB_LOAD_HPP
#define TH05_BB_LOAD_HPP
#include "src/shared/abi.hpp"

typedef uint8_t bb_tiles8_t;
static const unsigned int BB_SIZE = 2048;
extern bb_tiles8_t __seg *bb_load_seg;

#pragma codeseg _TEXT
extern "C" void __seg *pascal far hmem_allocbyte(unsigned bytesize);
#pragma codeseg BB_LOAD_TEXT main_01
bb_tiles8_t __seg *pascal near bb_load(const char far *filename);
#pragma codeseg

typedef char bb_segment_result_is_2[(sizeof(bb_tiles8_t __seg *) == 2) ? 1 : -1];
#endif
