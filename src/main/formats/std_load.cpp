// STD file loader: stage title, BGM titles, map section order, scroll speeds,
// enemy scripts and the stage timeline, read into one far segment.
//
// ZUN wrote this with Turbo C++ pseudo-registers; ReC98's th05/formats/std.cpp
// documents the same function. The file layout after the three titles is
//   u8 map_section_count, then the section IDs (pre-multiplied by 2)
//   u8 scroll_speed_count, then one speed per section
//   u8 enemy_script_count, then [u8 size, script bytes] per script
//   u8 padding, then the stage timeline (STD bytecode run by std_run()).
#pragma option -zCSTD_LOAD_TEXT -zPmain_01 -k-
#include "src/main/formats/std_load.hpp"
#pragma codeseg STD_LOAD_TEXT main_01

// The first sections already fill the 368-pixel playfield when the stage
// starts (23 tile rows, 5 rows per section), so both per-section pointers
// skip the count byte and those 4 entries.
#define STD_SECTIONS_ON_SCREEN_AT_START ((368 / 16) / 5)
#define STD_SECTION_DATA_OFFSET (1 + STD_SECTIONS_ON_SCREEN_AT_START)

void near std_load(void)
{
    #define enemy_scripts_remaining _DL
    #define enemy_script_p _BX

    asm { push ds }
    std_free();

    std_fn[3] = '0' + stage_id;

    // DOS file open (read-only). ZUN landmine: no error handling.
    _DX = FP_OFF(std_fn);
    _AX = 0x3D00;
    geninterrupt(0x21);
    _BX = _AX;

    // DOS file read: the 16-bit size that precedes the data.
    _DX = FP_OFF(&std_size_in_data_segment);
    _AH = 0x3F;
    _CX = sizeof(std_size_in_data_segment);
    geninterrupt(0x21);

    // Keep the file handle while allocating; DS and ES then point at the
    // new segment, so the size has to come from SI.
    asm { push bx }
    _SI = std_size_in_data_segment;
    std_seg = reinterpret_cast<unsigned char __seg *>(hmem_allocbyte(_SI));
    _DS = _AX;
    _ES = _AX;
    _DI = 0;
    asm { pop bx }

    // DOS file read of the whole file into DS:0, then close.
    _DX = _DI;
    _AH = 0x3F;
    _CX = _SI;
    geninterrupt(0x21);
    _AH = 0x3E;
    geninterrupt(0x21);
    asm { pop ds }

    // Three NUL-terminated titles. ZUN landmine: the direction flag is never
    // cleared, so this relies on it already being clear.
    stage_title = reinterpret_cast<char far *>(MK_FP(_ES,_DI));
    _AX = 0;
    _CX = 0xFFFF;
    asm { repne scasb }   // ES:DI = one byte past the terminating NUL
    stage_bgm_title = reinterpret_cast<char far *>(MK_FP(_ES,_DI));
    asm { repne scasb }
    boss_bgm_title = reinterpret_cast<char far *>(MK_FP(_ES,_DI));
    asm { repne scasb }

    // Map section order
    asm { lea ax, [di + STD_SECTION_DATA_OFFSET] }
    std_map_section_p = _AX;
    tile_row_in_section = 0;

    // Scroll speeds, one per map section
    asm { movzx ax, byte ptr es:[di] }
    _AX++;
    _DI += _AX;
    asm { lea ax, [di + STD_SECTION_DATA_OFFSET] }
    std_scroll_speed = reinterpret_cast<unsigned char near *>(_AX);
    asm { movzx ax, byte ptr es:[di] }

    // ZUN bloat: the speed *count* becomes the first frame's speed. The first
    // frame only needs a non-zero value before std_scroll_speed takes over.
    scroll_speed = _AL;

    // Enemy scripts: record a near pointer to each one.
    _AX++;
    _DI += _AX;
    enemy_scripts_remaining = *reinterpret_cast<unsigned char __es *>(_DI);
    _DI++;
    enemy_script_p = FP_OFF(std_enemy_scripts);
script_next:
    asm { movzx ax, byte ptr es:[di] }   // script size
    _DI++;
    *reinterpret_cast<unsigned int __ds *>(enemy_script_p) = _DI;
    enemy_script_p += 2;
    _DI += _AX;
    asm { dec dl; jne script_next }

    // The timeline follows a padding byte; std_run() interprets it.
    _DI++;
    std_ip = reinterpret_cast<void far *>(MK_FP(_ES,_DI));
    asm { extrn @std_run$qv:far }
    asm { mov word ptr [stage_vm + 2], seg MAIN_03 }
    asm { mov word ptr [stage_vm], offset MAIN_03:@std_run$qv }

    #undef enemy_script_p
    #undef enemy_scripts_remaining
}
