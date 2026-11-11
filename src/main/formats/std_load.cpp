// Natural TH05 STD loader from ReC98's typed game format semantics.
#pragma option -zCSTD_LOAD_TEXT -zPmain_01 -k-
#include "src/main/formats/std_load.hpp"
#pragma codeseg STD_LOAD_TEXT main_01
void near std_load(void)
{
    asm { push ds }
    std_free();
    std_fn[3] = '0' + stage_id;
    _DX = FP_OFF(std_fn);
    _AX = 0x3D00;
    geninterrupt(0x21);
    _BX = _AX;
    _DX = FP_OFF(&std_size_in_data_segment);
    _AH = 0x3F;
    _CX = 2;
    geninterrupt(0x21);
    asm { push bx }
    _SI = std_size_in_data_segment;
    std_seg = reinterpret_cast<unsigned char __seg *>(hmem_allocbyte(_SI));
    _DS = _AX;
    _ES = _AX;
    _DI = 0;
    asm { pop bx }
    _DX = _DI;
    _AH = 0x3F;
    _CX = _SI;
    geninterrupt(0x21);
    _AH = 0x3E;
    geninterrupt(0x21);
    asm { pop ds }
    stage_title = reinterpret_cast<char far *>(MK_FP(_ES,_DI));
    _AX = 0;
    _CX = 0xFFFF;
    asm { repne scasb }
    stage_bgm_title = reinterpret_cast<char far *>(MK_FP(_ES,_DI));
    asm { repne scasb }
    boss_bgm_title = reinterpret_cast<char far *>(MK_FP(_ES,_DI));
    asm { repne scasb }
    asm { lea ax, [di + 5] }
    std_map_section_p = _AX;
    tile_row_in_section = 0;
    asm { movzx ax, byte ptr es:[di] }
    _AX++;
    _DI += _AX;
    asm { lea ax, [di + 5] }
    std_scroll_speed = reinterpret_cast<unsigned char near *>(_AX);
    asm { movzx ax, byte ptr es:[di] }
    scroll_speed = _AL;
    _AX++;
    _DI += _AX;
    _DL = *reinterpret_cast<unsigned char __es *>(_DI);
    _DI++;
    _BX = FP_OFF(std_enemy_scripts);
script_next:
    asm { movzx ax, byte ptr es:[di] }
    _DI++;
    *reinterpret_cast<unsigned int __ds *>(_BX) = _DI;
    _BX += 2;
    _DI += _AX;
    asm { dec dl; jne script_next }
    _DI++;
    std_ip = reinterpret_cast<void far *>(MK_FP(_ES,_DI));
    asm { extrn @std_run$qv:far }
    asm { mov word ptr [stage_vm + 2], seg MAIN_03 }
    asm { mov word ptr [stage_vm], offset MAIN_03:@std_run$qv }
}
