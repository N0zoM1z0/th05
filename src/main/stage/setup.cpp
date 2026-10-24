// Stage and boss initialization adapted from natural C++ in nmlgc/ReC98
// b6ba5b0a529edbb31efdf8c0e939263804f8ee47: th05/main014.cpp,
// th04/main/boss/reset.cpp, th04/formats/bb_boss.cpp, th05/main/stage/setup.cpp.
// Candidate: rank selection is expressed as real typed C++ calls; no original
// instruction macro is retained. Only the first ten main014 functions belong
// to this reviewed continuous target range; score_delta_commit is excluded.
#pragma option -zCmain_01_TEXT -zPmain_01 -d-
#include "src/main/stage/setup.hpp"

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
	midboss.frames_until = 2500;
	STAGE_POINT_SET(midboss.pos. cur, (PLAYFIELD_W / 2), ((PLAYFIELD_H * 6) / 23));
	STAGE_POINT_SET(midboss.pos.prev, (PLAYFIELD_W / 2), ((PLAYFIELD_H * 6) / 23));
	STAGE_POINT_SET(midboss.pos.velocity, 0, 0);
	midboss.hp = 1000;
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
	midboss.frames_until = 2750;
	STAGE_MOTION_INIT(midboss.pos, 192, -32);
	STAGE_POINT_SET(midboss.pos.velocity, 0.0f, 0.5f);
	midboss.hp = 1400;
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
	midboss.frames_until = 5750;
	STAGE_MOTION_INIT(midboss.pos, 192, -32);
	STAGE_POINT_SET(midboss.pos.velocity, 0.0f, 0.5f);
	midboss.hp = 1400;
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
	midboss.frames_until = 3900;
	STAGE_MOTION_INIT(midboss.pos, 192, -32);
	STAGE_POINT_SET(midboss.pos.velocity, 0.0f, 0.5f);
	midboss.hp = 1100;
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
	midboss.frames_until = 4800;
	STAGE_MOTION_INIT(midboss.pos, 192, -32);
	STAGE_POINT_SET(midboss.pos.velocity, 0.0f, 0.5f);
	midboss.hp = 1550;
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

	boss_statebyte[0] = select_for_rank(20, 10, 6, 6);
	boss_statebyte[1] = select_for_rank(48, 32, 24, 24);

	stage_render = nullfunc_near;
	stage_invalidate = nullfunc_near;
}

void pascal near stage6_setup(void)
{
	midboss_update_func = nullfunc_far;
	midboss_render_func = nullfunc_near;
	midboss.frames_until = 30000;

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
	midboss.frames_until = 5800;
	STAGE_MOTION_INIT(midboss.pos, 192, -16);
	midboss.angle = +0x40;
	midboss.hp = 3000;
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
