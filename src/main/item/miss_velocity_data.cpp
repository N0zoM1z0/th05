// Velocities of the five items dropped when losing a life, depending on
// whether the player is in the left, center or right third of the playfield.
#pragma option -zCITEM_MISS_DATA_CONTEXT -zPmain_01
#include "src/main/item/miss_velocity_data.hpp"

// In subpixels per frame. Each field lists the five Y velocities, then the
// five X velocities.
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
