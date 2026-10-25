// STD owns an allocated real-mode segment, not a far pointer or DOS handle.
// Provenance: ReC98 b6ba5b0a th04/formats/std.hpp, th05/formats/std.cpp;
// maintained TH04 src/main/stage/std.cpp supplies the natural release body.
#ifndef TH05_STD_FREE_HPP
#define TH05_STD_FREE_HPP
#include "src/shared/abi.hpp"

extern uint8_t __seg *std_seg;
#pragma codeseg _TEXT
extern "C" void pascal far hmem_free(void __seg *memseg);
#pragma codeseg STD_FREE_TEXT main_01
void near std_free(void);
#pragma codeseg

typedef char std_segment_handle_is_word[(sizeof(std_seg) == 2) ? 1 : -1];
#endif
