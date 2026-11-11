// Real original-register PC-98 graphics function, shared with dialog context.
void near egc_start_copy_noframe(void);
extern "C" void pascal far egc_off(void);
extern unsigned char page_front;
void near playfield_copy_front_to_back(void)
{
    egc_start_copy_noframe();
    _ES = 0xa850;
    _DI = 0x72b4;
    _DX = 0xa6;
    _AL = page_front;
    box_copy_next_row:
        _CX = 24;
    box_copy_next_word:
        outportb(_DX, _AL);
        _AL ^= 1;
        _BX = *reinterpret_cast<unsigned short __es *>(_DI);
        outportb(_DX, _AL);
        _AL ^= 1;
        *reinterpret_cast<unsigned short __es *>(_DI) = _BX;
        _DI += 2;
        asm { loop box_copy_next_word; }
        asm {
            sub di, 0x80
            jge box_copy_next_row
        }
    outportb(_DX, _AL);
    egc_off();
}
