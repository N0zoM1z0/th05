// Natural default rewards and defeat update adapted from nmlgc/ReC98
// b6ba5b0a529edbb31efdf8c0e939263804f8ee47: th05/mb_dft.cpp ->
// th04/main/midboss/defeat.cpp, GAME=5. The final reset is a genuine typed call,
// not the reference's instruction macro. Exact call relaxation is unproven.
#pragma option -zCMB_DFT_TEXT -zPmain_03
#include "src/main/midboss/default.hpp"

static const subpixel_t BONUS_AREA_W = (PLAYFIELD_W / 3) * 16;
static const subpixel_t BONUS_AREA_H = (PLAYFIELD_W / 3) * 16;

#define bonus_pointnum_add(base_left, base_top, points) { \
    subpixel_t center_x = (base_left + randring2_next16_mod(BONUS_AREA_W)); \
    if(center_x < 0) { \
        center_x = 0; \
    } else if(center_x > (PLAYFIELD_W * 16)) { \
        center_x = (PLAYFIELD_W * 16); \
    } \
    pointnums_add_yellow( \
        center_x, (base_top + randring2_next16_mod(BONUS_AREA_H)), points \
    ); \
}

#define score_bonus(units, value, center) { \
    score_delta += (units * value); \
    pointnum_times_2 = false; \
    subpixel_t base_left = (center.x.v - (BONUS_AREA_W / 2)); \
    subpixel_t base_top = (center.y.v - (BONUS_AREA_H / 2)); \
    for(unsigned int i = 0; i < units; i++) { \
        bonus_pointnum_add(base_left, base_top, value); \
    } \
}

void pascal near midboss_score_bonus(unsigned int units)
{
    score_bonus(units, MIDBOSS_BONUS_UNIT_VALUE, midboss.pos.cur);
}

void pascal near boss_score_bonus(unsigned int units)
{
    score_bonus(units, BOSS_BONUS_UNIT_VALUE, boss.pos.cur);
    boss_phase_timed_out = false;
}

void near midboss_defeat_update(void)
{
    if(midboss.phase == PHASE_EXPLODE_BIG) {
        if(midboss.phase_frame == 1) {
            playfield_shake_anim_time = 10;
            midboss_active = false;
        }
        if((midboss.phase_frame % 16) == 0) {
            midboss.sprite++;
            if(midboss.sprite >= (PAT_ENEMY_KILL_last + 1)) {
                midboss.phase = PHASE_NONE;
            }
        }
    } else {
        midboss_reset();
    }
}
