/* BOX_TILES: the three dither patterns that fade a dialog box in, from 1/4
 * to 3/4 coverage. Each tile is four rows of one 16-pixel word. */
#pragma option -zCDIALOG_TILE_MASKS_TEXT -zPmain_01
#ifdef __cplusplus
#error Build this file as C
#endif
#include "src/shared/abi.hpp"

/* Row [phase] of the tile with [count] of every four pixels set: a 4-pixel
 * nibble repeated across the word, rotated one pixel right on each row. */
#define DIALOG_COVERAGE_BASE(count) (((1U << (count)) - 1U) << (4 - (count)))
#define DIALOG_ROW_NIBBLE(count, phase) ( \
    ((DIALOG_COVERAGE_BASE(count) >> (phase)) | \
     (DIALOG_COVERAGE_BASE(count) << (4 - (phase)))) & 15U)
#define DIALOG_ROW_WORD(count, phase) (DIALOG_ROW_NIBBLE(count, phase) * 0x1111U)
#define DIALOG_ROW_BYTES(count, phase) \
    ((unsigned char)(DIALOG_ROW_WORD(count, phase) & 0xffU)), \
    ((unsigned char)((DIALOG_ROW_WORD(count, phase) >> 8) & 0xffU))

const unsigned char near BOX_TILES[3 * 4 * 2] = {
    DIALOG_ROW_BYTES(1, 0), DIALOG_ROW_BYTES(1, 1),
    DIALOG_ROW_BYTES(1, 2), DIALOG_ROW_BYTES(1, 3),
    DIALOG_ROW_BYTES(2, 0), DIALOG_ROW_BYTES(2, 1),
    DIALOG_ROW_BYTES(2, 2), DIALOG_ROW_BYTES(2, 3),
    DIALOG_ROW_BYTES(3, 0), DIALOG_ROW_BYTES(3, 1),
    DIALOG_ROW_BYTES(3, 2), DIALOG_ROW_BYTES(3, 3)
};

typedef char dialog_coverage_size24[(sizeof(BOX_TILES) == 24) ? 1 : -1];

#undef DIALOG_ROW_BYTES
#undef DIALOG_ROW_WORD
#undef DIALOG_ROW_NIBBLE
#undef DIALOG_COVERAGE_BASE
