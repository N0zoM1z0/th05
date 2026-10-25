// Complete TH05 persistent statistics and actual process-handoff interfaces.
#ifndef TH05_HANDOFF_HPP
#define TH05_HANDOFF_HPP
#include "src/main/hud/resident.hpp"

#if GAME != 5 || BINARY != 'M'
#error This producer implements the TH05 MAIN process handoff
#endif

extern score_lebcd_t score;
extern uint16_t Ems;
extern unsigned int total_std_frames;
extern unsigned int items_spawned;
extern unsigned int items_collected;
extern unsigned int total_point_items_collected;
extern unsigned int total_max_valued_point_items_collected;
extern unsigned int enemies_gone;
extern unsigned int enemies_killed;
extern unsigned long total_slow_frames;
extern unsigned long total_frames;

#pragma codeseg _TEXT
#include <process.h>
extern "C" {
    int pascal far ems_free(unsigned int handle);
    void pascal far super_free(void);
    void pascal far graph_hide(void);
    void pascal far text_clear(void);
}
#pragma codeseg SHARED
extern "C" void pascal far cdg_free_all(void);
void far game_exit(void);
#pragma codeseg HANDOFF_FOREIGN_TEXT main_01
void near score_reset(void);
extern "C" void pascal near bb_txt_free(void);
void near bb_boss_free(void);
void near dialog_free(void);
extern "C" void pascal near bb_playchar_free(void);
void near std_free(void);
void near map_free(void);
#pragma codeseg HANDOFF_TEXT main_01
void near game_state_save_score(void);
int pascal far GameExecl(const char far *binary_fn);
#pragma codeseg

typedef char handoff_score_is_8[(sizeof(score_lebcd_t) == 8) ? 1 : -1];
typedef char handoff_far_string_is_4[(sizeof(const char far *) == 4) ? 1 : -1];
typedef char handoff_null_argument_is_4[(sizeof(NULL) == 4) ? 1 : -1];
typedef char handoff_items_at_46[(offsetof(resident_t, items_spawned) == 46) ? 1 : -1];
typedef char handoff_collected_at_48[(offsetof(resident_t, items_collected) == 48) ? 1 : -1];
typedef char handoff_points_at_50[(offsetof(resident_t, point_items_collected) == 50) ? 1 : -1];
typedef char handoff_max_points_at_52[(offsetof(resident_t, max_valued_point_items_collected) == 52) ? 1 : -1];
typedef char handoff_gone_at_54[(offsetof(resident_t, enemies_gone) == 54) ? 1 : -1];
typedef char handoff_killed_at_56[(offsetof(resident_t, enemies_killed) == 56) ? 1 : -1];
#endif
