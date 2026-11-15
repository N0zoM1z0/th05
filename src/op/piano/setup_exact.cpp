// piano_setup_and_put_initial(): draws the six empty piano keyboards and their
// "FM1".."FM5"/"SSG" labels, then retrieves PMD's work area address for
// piano_render(). Based on ReC98 th05/op/piano_c.cpp.
#pragma option -zCSHARED -k-
#include <dos.h>
static const unsigned int PIANO_TOP = 64;
static const unsigned int PIANO_PART_H = 18;
static const unsigned int VRAM_ROW_BYTES = 80;
static const unsigned int PIANO_LABEL_LEFT_BYTES = (384 - 32) / 8;
static const unsigned int PIANO_LABEL_TOP_PADDING = 4;
static const unsigned char PIANO_LABEL_F=0, PIANO_LABEL_M=1;
static const unsigned char PIANO_LABEL_1=2,PIANO_LABEL_2=3,PIANO_LABEL_3=4;
static const unsigned char PIANO_LABEL_4=5,PIANO_LABEL_5=6;
static const unsigned char PIANO_LABEL_S=7,PIANO_LABEL_G=8;

extern "C" void near piano_part_keys_put_raw(void);
extern "C" void __fastcall near piano_label_put_raw(unsigned char glyph);
extern void near grcg_setcolor_direct_raw(void);
extern unsigned int pmd_workadr[2];
#pragma codeseg SHARED

// Draws the empty keyboard of part [n].
#define piano_part_keys_put(n) { \
	_DI = ((PIANO_TOP + (n) * PIANO_PART_H) * VRAM_ROW_BYTES); \
	piano_part_keys_put_raw(); \
}
// Draws label character [glyph] at column [col] of the label for part [row].
#define piano_label_putc(row, col, glyph) { \
	_AL = (glyph); \
	_DI = ((PIANO_TOP + PIANO_LABEL_TOP_PADDING + (row)*PIANO_PART_H) * VRAM_ROW_BYTES + PIANO_LABEL_LEFT_BYTES + (col)); \
	piano_label_put_raw(_AL); \
}

void far piano_setup_and_put_initial(void)
{
    _AL = 0xC0; // GRCG RMW mode
    asm { out 07ch, al }
    _ES = 0xA800; // B plane

    // The original saves and restores SI without using it. This assignment
    // makes Borland do the same.
    _SI = _SI;

    piano_part_keys_put(0);
    piano_part_keys_put(1);
    piano_part_keys_put(2);
    piano_part_keys_put(3);
    piano_part_keys_put(4);
    piano_part_keys_put(5);
    _AH = 5;
    grcg_setcolor_direct_raw();
    piano_label_putc(0,0,PIANO_LABEL_F);
    piano_label_putc(0,1,PIANO_LABEL_M);
    piano_label_putc(0,2,PIANO_LABEL_1);
    piano_label_putc(1,0,PIANO_LABEL_F);
    piano_label_putc(1,1,PIANO_LABEL_M);
    piano_label_putc(1,2,PIANO_LABEL_2);
    piano_label_putc(2,0,PIANO_LABEL_F);
    piano_label_putc(2,1,PIANO_LABEL_M);
    piano_label_putc(2,2,PIANO_LABEL_3);
    piano_label_putc(3,0,PIANO_LABEL_F);
    piano_label_putc(3,1,PIANO_LABEL_M);
    piano_label_putc(3,2,PIANO_LABEL_4);
    piano_label_putc(4,0,PIANO_LABEL_F);
    piano_label_putc(4,1,PIANO_LABEL_M);
    piano_label_putc(4,2,PIANO_LABEL_5);
    piano_label_putc(5,0,PIANO_LABEL_S);
    piano_label_putc(5,1,PIANO_LABEL_S);
    piano_label_putc(5,2,PIANO_LABEL_G);
    _AL ^= _AL; // GRCG off
    asm { out 07ch, al }

    // PMD function 10h: Get work area address, returned in DS:DX
    asm { push ds }
    _AH = 0x10;
    geninterrupt(0x60);
    _AX = _DS;
    asm { pop ds }
    pmd_workadr[0] = _DX;
    pmd_workadr[1] = _AX;
}
