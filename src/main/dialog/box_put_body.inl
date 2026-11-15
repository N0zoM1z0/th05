// dialog_box_put(): fills a BOX_W x BOX_H dialog box at (left, top) with one
// of the BOX_TILES dither patterns, in color 1 through the GRCG. Calling it
// with tiles 0, 1 and 2 in turn fades the box in.
//
// ZUN wrote this with Turbo C++ pseudo-registers. The inline instructions are
// the ones Turbo C++ would otherwise encode differently: it uses the other
// encoding for the additions and the register move, tests the row counter
// through AX, and shortens `test bx, 7` to `test bl, 7`.
#define GC_RMW 0xC0
#define SEG_PLANE_B 0xA800
#define ROW_SIZE (640 / 8)
#define BOX_VRAM_W (320 / 8)
#define BOX_TILE_SIZE 8   // 4 rows of one 16-pixel word

extern "C" void pascal far grcg_setcolor(int mode, int color);
extern const unsigned char BOX_TILES[24];
void pascal near dialog_box_put(uscreen_x_t left, uvram_y_t top, int tile)
{
    grcg_setcolor(GC_RMW, 1);
    _ES = SEG_PLANE_B;

    // DI = (top * ROW_SIZE) + (left / 8), as (top << 6) + (top << 4).
    _AX = left;
    _DX = top;
    _AX >>= 3;
    _DX <<= 6;
    asm { add ax, dx; }
    _DX >>= 2;
    asm { add ax, dx; }
    asm { mov di, ax; }

    // BX = byte offset of the current tile row within BOX_TILES.
    _BX = tile;
    _BX <<= 3;   // * BOX_TILE_SIZE
    _DX = 48;   // BOX_H rows
    box_tile_row:
    {
        _CX = (BOX_VRAM_W / 2);
        _AX = *reinterpret_cast<const unsigned short near *>(BOX_TILES + _BX);
        asm { rep stosw; }

        // Next tile row, wrapping around after the fourth one.
        _BX += 2;
        asm {
            test bx, (BOX_TILE_SIZE - 1)
            jne box_tile_not_wrapped
            sub bx, BOX_TILE_SIZE
        box_tile_not_wrapped:
        }
        _DI += (ROW_SIZE - BOX_VRAM_W);
        asm {
            dec dx
            jne box_tile_row
        }
    }

    // GRCG off
    _DX = 0x7c;
    _AL = 0;
    outportb(_DX, _AL);
}

#undef BOX_TILE_SIZE
#undef BOX_VRAM_W
#undef ROW_SIZE
#undef SEG_PLANE_B
#undef GC_RMW
