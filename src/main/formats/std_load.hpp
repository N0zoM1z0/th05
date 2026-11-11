// Real TH05 STD file parser state and near/FAR call ABIs.
#ifndef TH05_MAIN_FORMATS_STD_LOAD_HPP
#define TH05_MAIN_FORMATS_STD_LOAD_HPP
#include <dos.h>
#include "src/main/formats/std_free.hpp"
extern unsigned char stage_id;
extern char std_fn[];
extern unsigned int std_size_in_data_segment;
extern void near *std_enemy_scripts[32];
extern void far *std_ip;
extern char far *stage_title;
extern char far *stage_bgm_title;
extern char far *boss_bgm_title;
extern unsigned int std_map_section_p;
extern unsigned char tile_row_in_section;
extern unsigned char near *std_scroll_speed;
extern unsigned char scroll_speed;
struct StageVmCodeAddress { unsigned int offset; unsigned int segment; };
extern StageVmCodeAddress stage_vm;
#pragma codeseg _TEXT
extern "C" void __seg *pascal far hmem_allocbyte(unsigned int bytesize);
#pragma codeseg STD_FREE_TEXT main_01
void near std_free(void);
#pragma codeseg STD_RUN_TEXT main_03
void pascal near std_run(void);
#pragma codeseg STD_LOAD_TEXT main_01
void near std_load(void);
#pragma codeseg
#endif
