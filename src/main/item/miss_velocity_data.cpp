// Three real miss-drop fields, each Y/X axis and five item slots.
#pragma option -zCITEM_MISS_DATA_CONTEXT -zPmain_01
#include "src/main/item/miss_velocity_data.hpp"

// Each innermost brace initializes the real Subpixel aggregate's public v.
// Integer arithmetic expresses pixels/frame and fractional subpixel steps.
const Subpixel ITEM_MISS_VELOCITIES[MISS_FIELD_COUNT][2][ITEM_MISS_COUNT] = {
    { // MISS_FIELD_LEFT
        {
            { -3 * ITEM_DROP_SUBPIXELS_PER_PIXEL },
            { -3 * ITEM_DROP_SUBPIXELS_PER_PIXEL - 8 },
            { -4 * ITEM_DROP_SUBPIXELS_PER_PIXEL },
            { -4 * ITEM_DROP_SUBPIXELS_PER_PIXEL - 8 },
            { -5 * ITEM_DROP_SUBPIXELS_PER_PIXEL }
        },
        {
            { 0 },
            { 12 },
            { ITEM_DROP_SUBPIXELS_PER_PIXEL + 8 },
            { 2 * ITEM_DROP_SUBPIXELS_PER_PIXEL + 4 },
            { 3 * ITEM_DROP_SUBPIXELS_PER_PIXEL }
        }
    },
    { // MISS_FIELD_CENTER
        {
            { -3 * ITEM_DROP_SUBPIXELS_PER_PIXEL },
            { -3 * ITEM_DROP_SUBPIXELS_PER_PIXEL - 8 },
            { -4 * ITEM_DROP_SUBPIXELS_PER_PIXEL },
            { -3 * ITEM_DROP_SUBPIXELS_PER_PIXEL - 8 },
            { -3 * ITEM_DROP_SUBPIXELS_PER_PIXEL }
        },
        {
            { -ITEM_DROP_SUBPIXELS_PER_PIXEL - 8 },
            { -12 },
            { 0 },
            { 12 },
            { ITEM_DROP_SUBPIXELS_PER_PIXEL + 8 }
        }
    },
    { // MISS_FIELD_RIGHT
        {
            { -3 * ITEM_DROP_SUBPIXELS_PER_PIXEL },
            { -3 * ITEM_DROP_SUBPIXELS_PER_PIXEL - 8 },
            { -4 * ITEM_DROP_SUBPIXELS_PER_PIXEL },
            { -4 * ITEM_DROP_SUBPIXELS_PER_PIXEL - 8 },
            { -5 * ITEM_DROP_SUBPIXELS_PER_PIXEL }
        },
        {
            { 0 },
            { -12 },
            { -ITEM_DROP_SUBPIXELS_PER_PIXEL - 8 },
            { -2 * ITEM_DROP_SUBPIXELS_PER_PIXEL - 4 },
            { -3 * ITEM_DROP_SUBPIXELS_PER_PIXEL }
        }
    }
};
