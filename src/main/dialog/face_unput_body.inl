// dialog_face_unput_8(): restores the 128x128 face area at (left / 8 * 8, top)
// on the current VRAM page with the same pixels from the other page, using
// the EGC and the same copy loop as playfield_copy_front_to_back().
#define FACE_BOTTOM_ROW_OFFSET (127 * (640 / 8))
#define FACE_ROW_STEP ((640 + 128) / 8)   // back to the previous row

void near egc_start_copy_noframe(void);
extern "C" void pascal far egc_off(void);
extern unsigned char page_back;
void pascal near dialog_face_unput_8(uscreen_x_t left, uvram_y_t top)
{
    egc_start_copy_noframe();

    // ES = 0xA800 + (top * 5): the segment of row [top], as one 80-byte row
    // is 5 paragraphs.
    _AX = top;
    asm { mov bx, ax; }   // Turbo C++ would encode `_BX = _AX` differently
    _AX <<= 2;
    asm { add ax, bx; }
    _AX += 0xa800;
    _ES = _AX;

    _DI = FACE_BOTTOM_ROW_OFFSET;
    _AX = left;
    _AX >>= 3;
    asm { add di, ax; }
    _DX = 0xa6;
    _AL = page_back;
    face_copy_next_row:
        _CX = 8;   // 128 pixels
    face_copy_next_word:
        // Read from one page into the EGC, write to the other.
        outportb(_DX, _AL);
        _AL ^= 1;
        _BX = *reinterpret_cast<unsigned short __es *>(_DI);
        outportb(_DX, _AL);
        _AL ^= 1;
        *reinterpret_cast<unsigned short __es *>(_DI) = _BX;
        _DI += 2;
        asm { loop face_copy_next_word; }
        asm {
            sub di, FACE_ROW_STEP
            jge face_copy_next_row
        }
    egc_off();
}

#undef FACE_ROW_STEP
#undef FACE_BOTTOM_ROW_OFFSET
