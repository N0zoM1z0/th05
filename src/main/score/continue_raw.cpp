// hiscore_continue_enter_raw(): finds the place of the current score in [hi],
// moves the lower entries down by one, enters the score under the name
// CONTINUE together with the current stage, and saves the score file.
//
// ZUN bloat: micro-optimized with pseudo-registers and inline ASM; plain C
// would do (see ReC98's th05/main/hiscore.cpp). Turbo C++'s built-in assembler
// rejects the 386 MOVSD instruction, so this file is built through `tcc -S`
// and TASM32 instead of being compiled directly to an object.
#pragma option -zCSCORE_RAW_TEXT -zPmain_01 -k-
#include <dos.h>
#include "src/op/hiscore/view.hpp"

#pragma codeseg SCORE_IO_TEXT main_01
void near scoredat_save_cur(void);
#pragma codeseg SCORE_RAW_TEXT main_01

extern score_lebcd_t score;
extern unsigned char stage_id;
extern unsigned char unnecessary_shift_place_copy;
extern const unsigned char near gCONTINUE[SCOREDAT_NAME_LEN + 1];

#define STAGE_EXTRA 6

void near hiscore_continue_enter_raw(void)
{
    // DX = place to compare against, from the lowest one upward. The saved
    // digits are gaiji, the current ones plain numbers. The unsigned compares
    // avoid TH04's sorting bug with overflowed scores.
    _DX = SCOREDAT_PLACES - 1;
    do {
        _SI = _DX;
        _SI <<= 3;
        _SI += FP_OFF(hi.score.g_score[0].digits + SCORE_DIGITS - 1);
        _BX = FP_OFF(&score.digits[SCORE_DIGITS - 1]);
        _CX = SCORE_DIGITS;
        compare_digit:
        asm {
            mov al, [si]
            sub al, 0a0h
            cmp al, [bx]
            jb next_place
            ja place_found
            dec bx
            dec si
            loop compare_digit
        }
    next_place:
        _DX--;
    } while(!(_FLAGS & 0x80)); // until DX becomes negative
place_found:
    // DX = place of the new entry, or SCOREDAT_PLACES if it isn't high enough.
    _DX++;
    unnecessary_shift_place_copy = _DL;
    if(_DX >= SCOREDAT_PLACES) {
        return;
    }

    // Move every entry from DX on down by one place. Names are 9 bytes with
    // the terminator, of which only the 8 characters are copied.
    asm { push ds }
    asm { pop es }
    for(_BX = SCOREDAT_PLACES - 2; static_cast<int>(_BX) >= static_cast<int>(_DX); _BX--) {
        asm { imul di, bx, 9 }
        _SI = _DI;
        _SI += FP_OFF(hi.score.g_name[0]);
        _DI += FP_OFF(hi.score.g_name[1]);
        asm { movsd }
        asm { movsd }

        _DI = _BX;
        _DI <<= 3;
        _SI = _DI;
        _SI += FP_OFF(hi.score.g_score[0].digits);
        _DI += FP_OFF(hi.score.g_score[1].digits);
        asm { movsd }
        asm { movsd }
        hi.score.g_stage[_BX + 1] = hi.score.g_stage[_BX];
    }

    // Enter the name and score, then turn the copied digits into gaiji.
    asm { imul di, dx, 9 }
    _DI += FP_OFF(hi.score.g_name[0]);
    _SI = FP_OFF(gCONTINUE);
    asm { movsd }
    asm { movsd }

    _DI = _DX;
    _DI <<= 3;
    _DI += FP_OFF(hi.score.g_score[0].digits);
    _SI = FP_OFF(score.digits);
    asm { movsd }
    asm { movsd }

    _DI -= SCORE_DIGITS;
    _CX = SCORE_DIGITS;
    convert_digit:
        *reinterpret_cast<unsigned char __ds *>(_DI++) += gb_0;
        asm { loop convert_digit }

    // The stage is stored as a gaiji digit from 1. The Extra Stage is stored
    // like stage 1.
    _AL = stage_id;
    if(_AL == STAGE_EXTRA) {
        _AL ^= _AL;
    }
    _DI = _DX;
    hi.score.g_stage[_DI] = (gb_1 + _AL);
    scoredat_save_cur();
}

#undef STAGE_EXTRA
