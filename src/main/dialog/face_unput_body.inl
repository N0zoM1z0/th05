// Real original-register PC-98 graphics function, shared with dialog context.
void near egc_start_copy_noframe(void);
extern "C" void pascal far egc_off(void);
extern unsigned char page_back;
void pascal near dialog_face_unput_8(uscreen_x_t left, uvram_y_t top)
{
    egc_start_copy_noframe();
    _AX = top;
    asm { mov bx, ax; }
    _AX <<= 2;
    asm { add ax, bx; }
    _AX += 0xa800;
    _ES = _AX;
    _DI = 0x27b0;
    _AX = left;
    _AX >>= 3;
    asm { add di, ax; }
    _DX = 0xa6;
    _AL = page_back;
    face_copy_next_row:
        _CX = 8;
    face_copy_next_word:
        outportb(_DX, _AL);
        _AL ^= 1;
        _BX = *reinterpret_cast<unsigned short __es *>(_DI);
        outportb(_DX, _AL);
        _AL ^= 1;
        *reinterpret_cast<unsigned short __es *>(_DI) = _BX;
        _DI += 2;
        asm { loop face_copy_next_word; }
        asm {
            sub di, 0x60
            jge face_copy_next_row
        }
    egc_off();
}
