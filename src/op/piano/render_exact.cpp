// Native OP Music Room PMD state renderer, preserving 16-bit register ABI.
#pragma option -zCSHARED -k-
#include <dos.h>
#include "src/shared/sound/pmd_part.hpp"
static const unsigned int PIANO_TOP = 64;
static const unsigned int PIANO_PART_H = 18;
static const unsigned int VRAM_ROW_BYTES = 80;
extern "C" void near piano_part_keys_put_raw(void);
extern "C" void __fastcall near piano_fm_part_put_raw(int unused_ax,int unused_dx,PmdPart near *near *part);
extern "C" unsigned char __fastcall near piano_current_note_from(int unused_ax,int unused_dx,PmdPart near *near *part);
extern "C" void __fastcall near piano_pressed_key_put(unsigned char note);
extern void near grcg_setcolor_direct_raw(void);
extern unsigned int pmd_workadr[2];
#pragma codeseg SHARED
#define PIANO_FM_PART(n) { _DI = ((PIANO_TOP+(n)*PIANO_PART_H)*VRAM_ROW_BYTES); _SI=(n); piano_fm_part_put_raw(_AX,_DX,reinterpret_cast<PmdPart near *near *>(_BX)); }
#define PIANO_NOTE_CUR() piano_current_note_from(_AX,_DX,reinterpret_cast<PmdPart near *near *>(_BX))
void far piano_render(void)
{
    asm { push ds }
    asm { push ds }
    asm { pop fs }
    _AL = 0xC0;
    asm { out 07ch, al }
    _ES = 0xA800;
    _DI = ((PIANO_TOP+5*PIANO_PART_H)*VRAM_ROW_BYTES);
    piano_part_keys_put_raw();
    asm { lds bx, dword ptr pmd_workadr }
    _DI = (PIANO_TOP * VRAM_ROW_BYTES);
    asm { mov si, 0 }
    piano_fm_part_put_raw(_AX,_DX,reinterpret_cast<PmdPart near *near *>(_BX));
    _BX += 2;
    PIANO_FM_PART(1); _BX += 2;
    PIANO_FM_PART(2); _BX += 2;
    PIANO_FM_PART(3); _BX += 2;
    PIANO_FM_PART(4);
    _AH = 5;
    grcg_setcolor_direct_raw();
    _DI = ((PIANO_TOP+5*PIANO_PART_H)*VRAM_ROW_BYTES);
    _BX += 4;
    piano_pressed_key_put(PIANO_NOTE_CUR());
    _BX += 2;
    piano_pressed_key_put(PIANO_NOTE_CUR());
    _AL ^= _AL;
    asm { out 07ch, al }
    asm { pop ds }
}
