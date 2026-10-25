// Complete on-disk MAP records and true allocated-segment interface.
// Provenance: ReC98 b6ba5b0a th04/formats/map.hpp and maintained TH04
// src/main/formats/map.hpp/map.cpp, independently checked against TH05.
#ifndef TH05_MAP_FREE_HPP
#define TH05_MAP_FREE_HPP
#include "src/shared/abi.hpp"

static const unsigned int MAP_ROWS_PER_SECTION = 5;
static const unsigned int MAP_TILES_MEMORY_X = 32;
struct map_header_t {
    uint16_t size;
    int section_count; // Unused by the game, genuinely present in the file.
    int unknown[2];
};
struct map_section_tiles_t {
    // Signed word offsets into the VRAM tile image, including8 unused columns.
    int row[MAP_ROWS_PER_SECTION][MAP_TILES_MEMORY_X];
};
extern map_section_tiles_t __seg *map_seg;

#pragma codeseg _TEXT
extern "C" void pascal far hmem_free(void __seg *memseg);
#pragma codeseg MAP_FREE_TEXT main_01
void near map_free(void);
#pragma codeseg

typedef char map_header_is_8[(sizeof(map_header_t) == 8) ? 1 : -1];
typedef char map_header_size_at_0[(offsetof(map_header_t, size) == 0) ? 1 : -1];
typedef char map_header_count_at_2[(offsetof(map_header_t, section_count) == 2) ? 1 : -1];
typedef char map_header_unknown_at_4[(offsetof(map_header_t, unknown) == 4) ? 1 : -1];
typedef char map_section_is_320[(sizeof(map_section_tiles_t) == 320) ? 1 : -1];
typedef char map_tile_row_is_64[(sizeof(((map_section_tiles_t *)0)->row[0]) == 64) ? 1 : -1];
typedef char map_segment_handle_is_word[(sizeof(map_seg) == 2) ? 1 : -1];
#endif
