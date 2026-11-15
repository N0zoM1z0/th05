// piano_render(): redraws the Music Room piano with the notes currently played
// by the five FM parts and the first two SSG parts. Based on ReC98
// th05/op/piano_c.cpp. The helpers are assembly functions (keys.asm, fm.asm)
// that take their parameters in registers, hence all the pseudo-registers.
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
// PMD's work area, as returned by piano_setup_and_put_initial(). Starts with
// the near pointers to all FM and SSG part records.
extern unsigned int pmd_workadr[2];
#pragma codeseg SHARED

// Draws FM part [n] at its VRAM row, with DS:BX pointing to its part pointer.
#define piano_fm_part_put(n) { \
	_DI = ((PIANO_TOP+(n)*PIANO_PART_H)*VRAM_ROW_BYTES); \
	_SI=(n); \
	piano_fm_part_put_raw(_AX,_DX,reinterpret_cast<PmdPart near *near *>(_BX)); \
}
#define piano_current_note() \
	piano_current_note_from(_AX,_DX,reinterpret_cast<PmdPart near *near *>(_BX))

void far piano_render(void)
{
    // FS keeps the game's data segment while DS points to PMD's work area.
    asm { push ds }
    asm { push ds }
    asm { pop fs }
    _AL = 0xC0; // GRCG RMW mode
    asm { out 07ch, al }
    _ES = 0xA800; // B plane
    _DI = ((PIANO_TOP+5*PIANO_PART_H)*VRAM_ROW_BYTES);
    piano_part_keys_put_raw();
    asm { lds bx, dword ptr pmd_workadr } // BX = FMPart[0]
    _DI = (PIANO_TOP * VRAM_ROW_BYTES);

    // `_SI = 0` would compile to the shorter XOR SI, SI.
    asm { mov si, 0 }
    piano_fm_part_put_raw(_AX,_DX,reinterpret_cast<PmdPart near *near *>(_BX));
    _BX += 2;
    piano_fm_part_put(1); _BX += 2;
    piano_fm_part_put(2); _BX += 2;
    piano_fm_part_put(3); _BX += 2;
    piano_fm_part_put(4);

    // SSG parts 1 and 2 share the last keyboard
    _AH = 5;
    grcg_setcolor_direct_raw();
    _DI = ((PIANO_TOP+5*PIANO_PART_H)*VRAM_ROW_BYTES);
    _BX += 4; // BX = SSGPart[0]
    piano_pressed_key_put(piano_current_note());
    _BX += 2; // BX = SSGPart[1]
    piano_pressed_key_put(piano_current_note());
    _AL ^= _AL; // GRCG off
    asm { out 07ch, al }
    asm { pop ds }
}
