// TH04 MAP records are retained; TH05 reads them through the raw DOS API.
#ifndef TH05_MAP_LOAD_HPP
#define TH05_MAP_LOAD_HPP
#include "src/main/formats/map_free.hpp"

extern char map_fn[];
extern map_header_t map_header;
extern uint8_t stage_id;

#pragma codeseg _TEXT
extern "C" void __seg *pascal far hmem_allocbyte(unsigned bytesize);
#pragma codeseg MAP_LOAD_TEXT main_01
void near map_load(void);
#pragma codeseg
#endif
