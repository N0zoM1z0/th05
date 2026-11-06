// MAP section geometry, corroborated by the complete map_section_tiles_t.
#ifndef TH05_TILE_SECTION_OFFSETS_H
#define TH05_TILE_SECTION_OFFSETS_H

#define TILE_SECTION_COUNT 32
#define TILE_SECTION_ROWS 5
#define TILE_SECTION_COLUMNS 32
#define TILE_SECTION_BYTES (TILE_SECTION_ROWS * TILE_SECTION_COLUMNS * sizeof(unsigned int))

#ifdef __cplusplus
extern "C" {
#endif
extern const unsigned int TILE_SECTION_OFFSETS[TILE_SECTION_COUNT];
#ifdef __cplusplus
}
#endif

typedef char tile_section_offset_word_is_2[(sizeof(unsigned int) == 2) ? 1 : -1];
typedef char tile_section_stride_is_320[(TILE_SECTION_BYTES == 320) ? 1 : -1];
typedef char tile_section_offsets_is_64[(sizeof(TILE_SECTION_OFFSETS) == 64) ? 1 : -1];
#endif
