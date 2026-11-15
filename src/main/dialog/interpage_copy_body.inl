// playfield_copy_front_to_back(): copies the 384x368 playfield from the front
// to the back VRAM page with the EGC, one 16-pixel word at a time, from the
// bottom row upwards. Port 0xA6 selects the VRAM page that the CPU accesses.
//
// ZUN bloat: dialog only needs the back page to restore the pixels behind the
// two faces, so copying the whole playfield is overkill.
#define SEG_PLAYFIELD_TOP (0xA800 + ((16 * (640 / 8)) / 16))   // row 16
#define PLAYFIELD_BOTTOM_ROW_OFFSET ((367 * (640 / 8)) + (32 / 8))
#define PLAYFIELD_ROW_STEP ((640 + 384) / 8)   // back to the previous row

void near egc_start_copy_noframe(void);
extern "C" void pascal far egc_off(void);
extern unsigned char page_front;
void near playfield_copy_front_to_back(void)
{
    egc_start_copy_noframe();
    _ES = SEG_PLAYFIELD_TOP;
    _DI = PLAYFIELD_BOTTOM_ROW_OFFSET;
    _DX = 0xa6;
    _AL = page_front;
    box_copy_next_row:
        _CX = 24;   // 384 pixels
    box_copy_next_word:
        // Read from one page into the EGC, write to the other.
        outportb(_DX, _AL);
        _AL ^= 1;
        _BX = *reinterpret_cast<unsigned short __es *>(_DI);
        outportb(_DX, _AL);
        _AL ^= 1;
        *reinterpret_cast<unsigned short __es *>(_DI) = _BX;
        _DI += 2;
        asm { loop box_copy_next_word; }
        asm {
            sub di, PLAYFIELD_ROW_STEP
            jge box_copy_next_row
        }

    // The loop ends with the back page selected for CPU access; switch back
    // to the front page that the caller draws the dialog on.
    outportb(_DX, _AL);
    egc_off();
}

#undef PLAYFIELD_ROW_STEP
#undef PLAYFIELD_BOTTOM_ROW_OFFSET
#undef SEG_PLAYFIELD_TOP
