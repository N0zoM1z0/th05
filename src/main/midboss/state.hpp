// Midboss scalar state and callback ABI from ReC98 th04/main/midboss/midboss.hpp.
#ifndef TH05_MAIN_MIDBOSS_STATE_HPP
#define TH05_MAIN_MIDBOSS_STATE_HPP

#pragma codeseg MIDBOSS_TEXT main_03
void far midboss_reset(void);
void far midboss_activate_if_stage_frame_is_midboss_start_frame(void);

// Preserve the complete canonical 22-byte midboss and real callback types.
// First declarations of rendering callbacks belong to their actual main_01.
#pragma codeseg MAI_TEXT main_01
#include "src/main/stage/setup.hpp"
void pascal near midboss_invalidate_func(void);

#pragma codeseg MIDBOSS_TEXT main_03
extern unsigned int stage_frame;
extern bool midboss_active;
extern nearfunc_t_near midboss_invalidate;
extern nearfunc_t_near midboss_render;
extern func_t_near midboss_update;

void far midboss_reset(void);
void far midboss_activate_if_stage_frame_is_midboss_start_frame(void);

#endif
