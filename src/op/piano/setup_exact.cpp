// Original TH05 OP piano initial draw, six parts plus FM/SSG labels.
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

#define PIANO_PART_PUT(n) { _DI = ((PIANO_TOP + (n) * PIANO_PART_H) * VRAM_ROW_BYTES); piano_part_keys_put_raw(); }
#define PIANO_LABEL_PUT(row, col, glyph) { _AL = (glyph); _DI = ((PIANO_TOP + PIANO_LABEL_TOP_PADDING + (row)*PIANO_PART_H) * VRAM_ROW_BYTES + PIANO_LABEL_LEFT_BYTES + (col)); piano_label_put_raw(_AL); }

void far piano_setup_and_put_initial(void)
{
    _AL = 0xC0;
    asm { out 07ch, al }
    _ES = 0xA800;
    _SI = _SI;
    PIANO_PART_PUT(0);
    PIANO_PART_PUT(1);
    PIANO_PART_PUT(2);
    PIANO_PART_PUT(3);
    PIANO_PART_PUT(4);
    PIANO_PART_PUT(5);
    _AH = 5;
    grcg_setcolor_direct_raw();
    PIANO_LABEL_PUT(0,0,PIANO_LABEL_F);
    PIANO_LABEL_PUT(0,1,PIANO_LABEL_M);
    PIANO_LABEL_PUT(0,2,PIANO_LABEL_1);
    PIANO_LABEL_PUT(1,0,PIANO_LABEL_F);
    PIANO_LABEL_PUT(1,1,PIANO_LABEL_M);
    PIANO_LABEL_PUT(1,2,PIANO_LABEL_2);
    PIANO_LABEL_PUT(2,0,PIANO_LABEL_F);
    PIANO_LABEL_PUT(2,1,PIANO_LABEL_M);
    PIANO_LABEL_PUT(2,2,PIANO_LABEL_3);
    PIANO_LABEL_PUT(3,0,PIANO_LABEL_F);
    PIANO_LABEL_PUT(3,1,PIANO_LABEL_M);
    PIANO_LABEL_PUT(3,2,PIANO_LABEL_4);
    PIANO_LABEL_PUT(4,0,PIANO_LABEL_F);
    PIANO_LABEL_PUT(4,1,PIANO_LABEL_M);
    PIANO_LABEL_PUT(4,2,PIANO_LABEL_5);
    PIANO_LABEL_PUT(5,0,PIANO_LABEL_S);
    PIANO_LABEL_PUT(5,1,PIANO_LABEL_S);
    PIANO_LABEL_PUT(5,2,PIANO_LABEL_G);
    _AL ^= _AL;
    asm { out 07ch, al }
    asm { push ds }
    _AH = 0x10;
    geninterrupt(0x60);
    _AX = _DS;
    asm { pop ds }
    pmd_workadr[0] = _DX;
    pmd_workadr[1] = _AX;
}
