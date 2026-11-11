// Stage and boss initialization adapted from natural C++ in nmlgc/ReC98
// b6ba5b0a529edbb31efdf8c0e939263804f8ee47: th05/main014.cpp,
// th04/main/boss/reset.cpp, th04/formats/bb_boss.cpp, th05/main/stage/setup.cpp.
// Candidate: rank selection is expressed as real typed C++ calls; no original
// instruction macro is retained. Only the first ten main014 functions belong
// to this reviewed continuous target range; score_delta_commit is excluded.
#pragma option -zCmain_01_TEXT -zPmain_01 -d-
#include "src/main/stage/setup.hpp"

// Original stage scheduling / Boss HP protocol: seven distinct stage
// initializers share the same 22-byte midboss and 24-byte Boss structures.
// These values are not stage numbers or guessed gameplay tuning; they are
// the exact per-stage event trigger and original HP boundaries.
static const unsigned int STAGE1_MIDBOSS_TRIGGER_FRAME = 2500;
static const unsigned int STAGE2_MIDBOSS_TRIGGER_FRAME = 2750;
static const unsigned int STAGE3_MIDBOSS_TRIGGER_FRAME = 5750;
static const unsigned int STAGE4_MIDBOSS_TRIGGER_FRAME = 3900;
static const unsigned int STAGE5_MIDBOSS_TRIGGER_FRAME = 4800;
static const unsigned int STAGE6_MIDBOSS_DISABLED_FRAMES = 30000;
static const unsigned int STAGEX_MIDBOSS_TRIGGER_FRAME = 5800;
static const int STAGE1_MIDBOSS_INITIAL_HP = 1000;
static const int STAGE2_MIDBOSS_INITIAL_HP = 1400;
static const int STAGE3_MIDBOSS_INITIAL_HP = 1400;
static const int STAGE4_MIDBOSS_INITIAL_HP = 1100;
static const int STAGE5_MIDBOSS_INITIAL_HP = 1550;
static const int STAGEX_MIDBOSS_INITIAL_HP = 3000;
// Stage 5's first two bytes of Boss scratch are rank-adjusted attack
// delays, not separate per-Boss mutable variables.
static const int STAGE5_RANK_BASE_EASY = 20;
static const int STAGE5_RANK_BASE_NORMAL = 10;
static const int STAGE5_RANK_BASE_HARD = 6;
static const int STAGE5_RANK_BASE_LUNATIC = 6;
static const int STAGE5_RANK_REPEAT_EASY = 48;
static const int STAGE5_RANK_REPEAT_NORMAL = 32;
static const int STAGE5_RANK_REPEAT_HARD = 24;
static const int STAGE5_RANK_REPEAT_LUNATIC = 24;

bool boss_phase_timed_out = false;

void near boss_reset(void)
{
	boss_update = nullfunc_far;
	boss_fg_render = nullfunc_near;
	boss_custombullets_render = nullfunc_near;

	boss.phase = PHASE_HP_FILL;
	boss.mode = 0;
	boss.phase_state.patterns_seen = 0;
	boss.phase_frame = 0;
	STAGE_POINT_SET(boss.pos.velocity, 0, 0);
	boss.damage_this_frame = 0;
	explosions_small_reset();
	boss_phase_timed_out = true;
}

void pascal near bb_boss_load(const char far *fn)
{
	bb_boss_seg = bb_load(fn);

}

void near bb_boss_free(void)

{
	if(bb_boss_seg) {
		hmem_free(reinterpret_cast<void __seg *>(bb_boss_seg));
		bb_boss_seg = 0;
	}
}

/* ReC98
 * -----
 * TH05 stage initialization
 */


void pascal near stage1_setup(void)
{
	midboss_update_func = midboss1_update;
	midboss_render_func = midboss1_render;
	midboss.frames_until = STAGE1_MIDBOSS_TRIGGER_FRAME;
	STAGE_POINT_SET(midboss.pos. cur, (PLAYFIELD_W / 2), ((PLAYFIELD_H * 6) / 23));
	STAGE_POINT_SET(midboss.pos.prev, (PLAYFIELD_W / 2), ((PLAYFIELD_H * 6) / 23));
	STAGE_POINT_SET(midboss.pos.velocity, 0, 0);
	midboss.hp = STAGE1_MIDBOSS_INITIAL_HP;
	midboss.sprite = 200;

	boss_reset();
	STAGE_MOTION_INIT(boss.pos, 192, 64);
	boss_bg_render_func = sara_bg_render;
	boss_update_func = sara_update;
	boss_fg_render_func = sara_fg_render;
	boss.sprite = PAT_SARA_STAY;
	STAGE_POINT_SET(boss_hitbox_radius, 24, 24);
	boss_sprite_left = PAT_SARA_LEFT;
	boss_sprite_right = PAT_SARA_RIGHT;
	boss_sprite_stay = PAT_SARA_STAY;
	boss_backdrop_colorfill = sara_backdrop_colorfill;

	super_entry_bfnt("st00.bmt");
	cdg_load_all_noalpha(CDG_BG_BOSS, "st00bk.cdg");
	bb_boss_load("st00.bb");

	stage_render = nullfunc_near;
	stage_invalidate = nullfunc_near;
}

void pascal near stage2_setup(void)
{
	midboss_update_func = midboss2_update;
	midboss_render_func = midboss2_render;
	midboss.frames_until = STAGE2_MIDBOSS_TRIGGER_FRAME;
	STAGE_MOTION_INIT(midboss.pos, 192, -32);
	STAGE_POINT_SET(midboss.pos.velocity, 0.0f, 0.5f);
	midboss.hp = STAGE2_MIDBOSS_INITIAL_HP;
	midboss.sprite = 202;

	boss_reset();
	STAGE_MOTION_INIT(boss.pos, 192, 64);
	boss_bg_render_func = louise_bg_render;
	boss_update_func = louise_update;
	boss_fg_render_func = louise_fg_render;
	boss.sprite = 180;
	STAGE_POINT_SET(boss_hitbox_radius, 24, 24);
	boss_backdrop_colorfill = louise_backdrop_colorfill;

	super_entry_bfnt("st01.bmt");
	cdg_load_all_noalpha(CDG_BG_BOSS, "st01bk.cdg");
	bb_boss_load("st01.bb");

	stage_render = stage2_update;
	stage_invalidate = stage2_invalidate;
}

void pascal near stage3_setup(void)
{
	midboss_update_func = midboss3_update;
	midboss_render_func = midboss3_render;
	midboss.frames_until = STAGE3_MIDBOSS_TRIGGER_FRAME;
	STAGE_MOTION_INIT(midboss.pos, 192, -32);
	STAGE_POINT_SET(midboss.pos.velocity, 0.0f, 0.5f);
	midboss.hp = STAGE3_MIDBOSS_INITIAL_HP;
	midboss.sprite = 208;

	boss_reset();
	STAGE_MOTION_INIT(boss.pos, 192, 64);
	boss_bg_render_func = alice_bg_render;
	boss_update_func = alice_update;
	boss_fg_render_func = alice_fg_render;
	boss.sprite = 180;
	STAGE_POINT_SET(boss_hitbox_radius, 24, 24);
	boss_backdrop_colorfill = alice_backdrop_colorfill;
	boss_sprite_left = 188;
	boss_sprite_right = 186;
	boss_sprite_stay = 180;

	super_entry_bfnt("st02.bmt");
	cdg_load_all_noalpha(CDG_BG_BOSS, "st02bk.cdg");
	bb_boss_load("st02.bb");

	stage_render = nullfunc_near;
	stage_invalidate = nullfunc_near;
}

void pascal near stage4_setup(void)
{
	midboss_update_func = midboss4_update;
	midboss_render_func = midboss4_render;
	midboss.frames_until = STAGE4_MIDBOSS_TRIGGER_FRAME;
	STAGE_MOTION_INIT(midboss.pos, 192, -32);
	STAGE_POINT_SET(midboss.pos.velocity, 0.0f, 0.5f);
	midboss.hp = STAGE4_MIDBOSS_INITIAL_HP;
	midboss.sprite = 208;

	boss_reset();
	STAGE_MOTION_INIT(boss.pos,  96, 64);
	STAGE_MOTION_INIT(yuki.pos, 288, 64);
	boss_bg_render_func = mai_yuki_bg_render;
	boss_update_func = mai_yuki_update;
	boss_fg_render_func = mai_yuki_fg_render;
	boss.sprite = 180;
	yuki.sprite = 180;
	STAGE_POINT_SET(boss_hitbox_radius, 24, 24);
	boss_backdrop_colorfill = mai_yuki_backdrop_colorfill;

	super_entry_bfnt("st03.bmt");
	cdg_load_all_noalpha(CDG_BG_BOSS, "st03bk.cdg");
	bb_boss_load("st03.bb");

	stage_render = nullfunc_near;
	stage_invalidate = nullfunc_near;
}

void pascal near stage5_setup(void)
{
	midboss_update_func = midboss5_update;
	midboss_render_func = midboss5_render;
	midboss.frames_until = STAGE5_MIDBOSS_TRIGGER_FRAME;
	STAGE_MOTION_INIT(midboss.pos, 192, -32);
	STAGE_POINT_SET(midboss.pos.velocity, 0.0f, 0.5f);
	midboss.hp = STAGE5_MIDBOSS_INITIAL_HP;
	midboss.sprite = 212;

	boss_reset();
	STAGE_MOTION_INIT(boss.pos, 96, 64);
	STAGE_MOTION_INIT(boss2.pos, 192, 64);
	boss_bg_render_func = yumeko_bg_render;
	boss_update_func = yumeko_update;
	boss_fg_render_func = yumeko_fg_render;
	boss.sprite = 180;
	STAGE_POINT_SET(boss_hitbox_radius, 24, 24);
	boss_backdrop_colorfill = yumeko_backdrop_colorfill;

	super_entry_bfnt("st04.bmt");
	cdg_load_all_noalpha(CDG_BG_BOSS, "st04bk.cdg");
	bb_boss_load("st04.bb");

	boss_statebyte[0] = select_for_rank(STAGE5_RANK_BASE_EASY, STAGE5_RANK_BASE_NORMAL, STAGE5_RANK_BASE_HARD, STAGE5_RANK_BASE_LUNATIC);
	boss_statebyte[1] = select_for_rank(STAGE5_RANK_REPEAT_EASY, STAGE5_RANK_REPEAT_NORMAL, STAGE5_RANK_REPEAT_HARD, STAGE5_RANK_REPEAT_LUNATIC);

	stage_render = nullfunc_near;
	stage_invalidate = nullfunc_near;
}

void pascal near stage6_setup(void)
{
	midboss_update_func = nullfunc_far;
	midboss_render_func = nullfunc_near;
	midboss.frames_until = STAGE6_MIDBOSS_DISABLED_FRAMES;

	boss_reset();
	STAGE_MOTION_INIT(boss.pos, (PLAYFIELD_W / 2), ((PLAYFIELD_H * 4) / 23));
	boss_bg_render_func = shinki_bg_render;
	boss_update_func = shinki_update;
	boss_fg_render_func = shinki_fg_render;
	boss.sprite = PAT_SHINKI_STILL;
	STAGE_POINT_SET(boss_hitbox_radius, BOSS_HITBOX_DEFAULT_W, BOSS_HITBOX_DEFAULT_H);
	boss_backdrop_colorfill = shinki_stage_backdrop_colorfill;

	cdg_load_all_noalpha(CDG_BG_BOSS, "st05bk.cdg");
	cdg_load_all_noalpha(CDG_BG_2, "st05bk2.cdg");
	bb_boss_load("st05.bb");

	stage_render = nullfunc_near;
	stage_invalidate = nullfunc_near;
}

void pascal near stagex_setup(void)
{
	midboss_update_func = midbossx_update;
	midboss_render_func = midbossx_render;
	midboss.frames_until = STAGEX_MIDBOSS_TRIGGER_FRAME;
	STAGE_MOTION_INIT(midboss.pos, 192, -16);
	midboss.angle = +0x40;
	midboss.hp = STAGEX_MIDBOSS_INITIAL_HP;
	midboss.sprite = 220;

	boss_reset();
	STAGE_MOTION_INIT(boss.pos, 192, 64);
	boss_bg_render_func = exalice_bg_render;
	boss_update_func = exalice_update;
	boss_fg_render_func = exalice_fg_render;
	boss.sprite = 180;
	STAGE_POINT_SET(boss_hitbox_radius, 24, 24);
	// Yup, inconsistent, but also unused.
	boss_backdrop_colorfill = shinki_stage_backdrop_colorfill;

	super_entry_bfnt("st06.bmt");
	bb_boss_load("st03.bb");

	stage_render = nullfunc_near;
	stage_invalidate = nullfunc_near;
}
