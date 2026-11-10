ifdef BINDINGS_AFTER
; Exact original-order THREE source functions with real before/after near Pascal relaxation.
.386
.model large
DEMO_TEXT segment byte public 'CODE' use16
assume cs:DEMO_TEXT
public _stage_session_free, _pause, @ems_allocate_and_preload_eyecatc$qv, @grcg_setmode_rmw$qv, @scroll_driver$qv
public @playfield_shake_update_and_rende$qv, @player_update$qv, PLAYER_RENDER, @GAMEEXECL$QNXC, PLAYPERF_RAISE
public @score_update_and_render$qv, @ENEMIES_RENDER$QV, _sparks_update, _sparks_render, POINTNUMS_UPDATE
public POINTNUMS_RENDER, @circles_update$qv, @circles_render$qv, @cfg_load_resident_ptr$qv, @lasers_update$qv
public @lasers_render$qv, BULLETS_RENDER, @shots_update$qv, @shots_render$qv, ITEMS_RENDER
public @hiscore_load$qv, @score_reset$qv, BB_TXT_LOAD, @BOMB_REIMU$QV, @BOMB_MARISA$QV
public @BOMB_MIMA$QV, @BOMB_YUUKA$QV, @stage_runtime_init$qv, @demo_load$qv, @DemoPlay$qv
public @bomb_bg_load__ems_preload_playch$qv, @EMS_PRELOAD_BOSS_FACESET$QNXC, @eyecatch_animate$qv, TILES_FILL_INITIAL, @TILES_RENDER_ALL$QV
public @tiles_activate$qv, NULLFUNC_NEAR, @std_load$qv, @hud_put$qv, BB_CHEETO_LOAD
public @shot_level_update$qv, MPN_LOAD, @map_load$qv, BB_PLAYCHAR_LOAD, @clear_blue_vram_pages$qv
public @SHINKI_BG_RENDER$QV, @overlay_wipe$qv, @overlay_black$qv, @OVERLAY_STAGE_ENTER_UPDATE_AND_R$QV, @dialog_load$qv
public @STAGE1_SETUP$QV, @STAGE2_SETUP$QV, @STAGE3_SETUP$QV, @STAGE4_SETUP$QV, @STAGE5_SETUP$QV
public @STAGE6_SETUP$QV, @STAGEX_SETUP$QV
org 00000h
@stage_runtime_init$qv label near
org 000aeh
_stage_session_free label near
org 000ddh
_pause label near
org 001fch
@demo_load$qv label near
org 0025ah
@DemoPlay$qv label near
org 002cch
@ems_allocate_and_preload_eyecatc$qv label near
org 00367h
@bomb_bg_load__ems_preload_playch$qv label near
org 00472h
@EMS_PRELOAD_BOSS_FACESET$QNXC label near
org 0050ch
@eyecatch_animate$qv label near
org 00644h
TILES_FILL_INITIAL label near
org 00692h
@TILES_RENDER_ALL$QV label near
org 00835h
@tiles_activate$qv label far
org 00c9eh
@grcg_setmode_rmw$qv label near
org 00fach
@scroll_driver$qv label near
org 0101fh
@playfield_shake_update_and_rende$qv label near
org 011e4h
NULLFUNC_NEAR label near
org 011e8h
@std_load$qv label near
org 0144ah
@hiscore_load$qv label near
org 016e3h
@player_update$qv label near
org 017fch
PLAYER_RENDER label near
org 01968h
@GAMEEXECL$QNXC label far
org 01a20h
PLAYPERF_RAISE label far
org 01a6ch
@score_reset$qv label near
org 01dc9h
@hud_put$qv label far
org 01f98h
@score_update_and_render$qv label near
org 028feh
BB_CHEETO_LOAD label near
org 029f6h
@ENEMIES_RENDER$QV label near
org 02b2ch
_sparks_update label near
org 02b78h
_sparks_render label near
org 02c4ch
POINTNUMS_UPDATE label near
org 02cbch
POINTNUMS_RENDER label near
org 02dc8h
@circles_update$qv label near
org 02dfeh
@circles_render$qv label near
org 02e88h
@shot_level_update$qv label far
org 02f5ch
BB_TXT_LOAD label near
org 03022h
MPN_LOAD label near
org 03068h
@map_load$qv label near
org 030c4h
@cfg_load_resident_ptr$qv label near
org 04811h
@BOMB_REIMU$QV label near
org 04a5dh
@BOMB_MARISA$QV label near
org 04c80h
@BOMB_MIMA$QV label near
org 04e17h
@BOMB_YUUKA$QV label near
org 04ed8h
BB_PLAYCHAR_LOAD label near
org 05070h
@clear_blue_vram_pages$qv label near
org 05eb7h
@SHINKI_BG_RENDER$QV label near
org 067f6h
@overlay_wipe$qv label near
org 06818h
@overlay_black$qv label near
org 06839h
@OVERLAY_STAGE_ENTER_UPDATE_AND_R$QV label near
org 07653h
@lasers_update$qv label near
org 0778bh
@lasers_render$qv label near
org 07c2bh
BULLETS_RENDER label near
org 07e81h
@shots_update$qv label near
org 08019h
@shots_render$qv label near
org 0838ah
ITEMS_RENDER label near
org 08461h
@dialog_load$qv label near
org 08fe2h
@STAGE1_SETUP$QV label near
org 090b1h
@STAGE2_SETUP$QV label near
org 0916eh
@STAGE3_SETUP$QV label near
org 0923dh
@STAGE4_SETUP$QV label near
org 09317h
@STAGE5_SETUP$QV label near
org 09414h
@STAGE6_SETUP$QV label near
org 094a4h
@STAGEX_SETUP$QV label near
org 09556h
DEMO_TEXT ends
RUNTIME_MAIN01_TEXT segment byte public 'CODE' use16
RUNTIME_MAIN01_TEXT ends
SESSION_MAIN01_TEXT segment byte public 'CODE' use16
SESSION_MAIN01_TEXT ends
SESSION_INIT_TEXT segment byte public 'CODE' use16
SESSION_INIT_TEXT ends
STAGE_SESSION_TEXT segment byte public 'CODE' use16
STAGE_SESSION_TEXT ends
main_01 group DEMO_TEXT, RUNTIME_MAIN01_TEXT, SESSION_MAIN01_TEXT, SESSION_INIT_TEXT, STAGE_SESSION_TEXT
SHARED segment para public 'CODE' use16
assume cs:SHARED
public SND_DETERMINE_MODES, _snd_se_update, SND_LOAD, @GAME_INIT_MAIN$QNXUC, @input_reset_sense$qv
public @input_sense$qv, @FRAME_DELAY$QI, SND_KAJA_INTERRUPT
org 00124h
SND_DETERMINE_MODES label far
org 0026ch
_snd_se_update label far
org 003f4h
SND_LOAD label far
org 004ach
SND_KAJA_INTERRUPT label far
org 004cah
@GAME_INIT_MAIN$QNXUC label far
org 00512h
@input_reset_sense$qv label far
org 0051ah
@input_sense$qv label far
org 00652h
@FRAME_DELAY$QI label far
org 007c0h
SHARED ends
RUNTIME_MAIN03_FOREIGN segment byte public 'CODE' use16
assume cs:RUNTIME_MAIN03_FOREIGN
public ENEMIES_UPDATE, @gather_update$qv, @gather_render$qv, @bullets_update$qv, ITEMS_UPDATE
public BULLET_TEMPLATE_TUNE_EASY, BULLET_TEMPLATE_TUNE_NORMAL, BULLET_TEMPLATE_TUNE_HARD, BULLET_TEMPLATE_TUNE_LUNATIC, @midboss_reset$qv
org 01977h
ENEMIES_UPDATE label far
org 01e32h
@gather_update$qv label far
org 01ed0h
@gather_render$qv label far
org 0242ch
BULLET_TEMPLATE_TUNE_EASY label near
org 02434h
BULLET_TEMPLATE_TUNE_NORMAL label near
org 02438h
BULLET_TEMPLATE_TUNE_HARD label near
org 02440h
BULLET_TEMPLATE_TUNE_LUNATIC label near
org 06e6fh
@bullets_update$qv label far
org 07231h
@midboss_reset$qv label far
org 07e3dh
ITEMS_UPDATE label far
org 0b760h
RUNTIME_MAIN03_FOREIGN ends
RUNTIME_MAIN03_TEXT segment byte public 'CODE' use16
RUNTIME_MAIN03_TEXT ends
BULLET_A_TEXT segment byte public 'CODE' use16
BULLET_A_TEXT ends
STAGE_SESSION_MAIN03_CONTEXT segment byte public 'CODE' use16
STAGE_SESSION_MAIN03_CONTEXT ends
main_03 group RUNTIME_MAIN03_FOREIGN, RUNTIME_MAIN03_TEXT, BULLET_A_TEXT, STAGE_SESSION_MAIN03_CONTEXT
_DATA segment word public 'DATA' use16
public _debug_frame_step, _debug_frame_step_enabled, _main_pf_fn, _se_fn, _op_fn
public _random_seed, _mem_assign_paras, _total_slow_frames, _total_frames, _input_sense_hook
public _vsync_Count1, _key_det, _bg_render_not_bombing, _bg_render_bombing, _player_is_hit
public _stage_vm, _resident, _bombing, _playchar_bomb_func, _stage_render
public _overlay1, _overlay2, _page_back, _page_front, _frames_unused
public _stage_frame, _stage_frame_mod2, _stage_frame_mod4, _stage_frame_mod8, _stage_frame_mod16
public _slowdown_factor, _quit, _palette_changed, _slowdown_caused_by_bullets, _midboss_update
public _midboss_render, _std_update, _boss_update, _boss_fg_render, _boss_custombullets_render
public _SHOT_FUNCS, _playchar_speed_aligned, _playchar_speed_diagonal, _power, _dream
public _score, _graze_score, _bullet_template_tune, _lives, _bombs
public _stage_id, _rank, _playperf, _playperf_max, _playperf_min
public _playchar, _turbo_mode, _playchar_shot_funcs, _item_point_score_at_full_dream, _load_playchar_resources
public _stage_bgm_name, _SESSION_EYE_RGB, _SESSION_REIMU_BFT, _SESSION_MARI_BFT, _SESSION_MIMA_BFT
public _SESSION_YUKA_BFT, _SESSION_MIKOD_BFT, _SESSION_MIKO32_BFT, _SESSION_REIMU16_BFT, _SESSION_MARI16_BFT
public _SESSION_MIMA16_BFT, _SESSION_YUKA16_BFT, _SESSION_MIKO16_BFT, _SESSION_BOMB_YUUKA_BFT, _SESSION_BOMB_BFT
public _SESSION_BSS0_CD2, _SESSION_ST00_BFT, _SESSION_ST00_MPN, _SESSION_BSS1_CD2, _SESSION_ST01_BFT
public _SESSION_ST01_MPN, _SESSION_BSS2_CD2, _SESSION_ST02_BFT, _SESSION_ST02_MPN, _SESSION_BSS3_CD2
public _SESSION_ST03_BFT, _SESSION_ST03_MPN, _SESSION_BSS4_CD2, _SESSION_ST04_BFT, _SESSION_ST04_MPN
public _SESSION_BSS4_CD2_REPEAT, _SESSION_ST04_BFT_REPEAT, _SESSION_BSS6_CD2, _SESSION_ST06_BFT, _SESSION_ST06_MPN
public _PaletteTone, _vsync_Count2, _bg_render_bombing_func, _pellet_bottom_col
org 00090h
_debug_frame_step label byte
org 00091h
_debug_frame_step_enabled label byte
org 000a0h
_load_playchar_resources label word
org 000a2h
_stage_bgm_name label dword
org 000b2h
_main_pf_fn label byte
org 000beh
_se_fn label byte
org 000c3h
_op_fn label byte
org 000cbh
_SESSION_EYE_RGB label byte
org 000d3h
_SESSION_REIMU_BFT label byte
org 000ddh
_SESSION_MARI_BFT label byte
org 000e6h
_SESSION_MIMA_BFT label byte
org 000efh
_SESSION_YUKA_BFT label byte
org 000f8h
_SESSION_MIKOD_BFT label byte
org 00102h
_SESSION_MIKO32_BFT label byte
org 0010dh
_SESSION_REIMU16_BFT label byte
org 00119h
_SESSION_MARI16_BFT label byte
org 00124h
_SESSION_MIMA16_BFT label byte
org 0012fh
_SESSION_YUKA16_BFT label byte
org 0013ah
_SESSION_MIKO16_BFT label byte
org 00145h
_SESSION_BOMB_YUUKA_BFT label byte
org 0014fh
_SESSION_BOMB_BFT label byte
org 00159h
_SESSION_BSS0_CD2 label byte
org 00162h
_SESSION_ST00_BFT label byte
org 0016bh
_SESSION_ST00_MPN label byte
org 00174h
_SESSION_BSS1_CD2 label byte
org 0017dh
_SESSION_ST01_BFT label byte
org 00186h
_SESSION_ST01_MPN label byte
org 0018fh
_SESSION_BSS2_CD2 label byte
org 00198h
_SESSION_ST02_BFT label byte
org 001a1h
_SESSION_ST02_MPN label byte
org 001aah
_SESSION_BSS3_CD2 label byte
org 001b3h
_SESSION_ST03_BFT label byte
org 001bch
_SESSION_ST03_MPN label byte
org 001c5h
_SESSION_BSS4_CD2 label byte
org 001ceh
_SESSION_ST04_BFT label byte
org 001d7h
_SESSION_ST04_MPN label byte
org 001e0h
_SESSION_BSS4_CD2_REPEAT label byte
org 001e9h
_SESSION_ST04_BFT_REPEAT label byte
org 001f2h
_SESSION_BSS6_CD2 label byte
org 001fbh
_SESSION_ST06_BFT label byte
org 00204h
_SESSION_ST06_MPN label byte
org 003dah
_PaletteTone label word
org 00418h
_random_seed label dword
org 00824h
_mem_assign_paras label word
org 01d70h
_SHOT_FUNCS label byte
org 01ec2h
_total_slow_frames label dword
org 01ec6h
_total_frames label dword
org 0261ch
_input_sense_hook label word
org 0267ah
_vsync_Count1 label word
org 0267ch
_vsync_Count2 label word
org 03064h
_key_det label word
org 03506h
_bg_render_not_bombing label word
org 03508h
_bg_render_bombing label word
org 0350ah
_bg_render_bombing_func label word
org 036deh
_playchar_speed_aligned label word
org 036e2h
_playchar_speed_diagonal label word
org 036f0h
_power label byte
org 036f3h
_player_is_hit label byte
org 036f6h
_dream label byte
org 03702h
_score label byte
org 03f8eh
_stage_vm label dword
org 03f9ah
_graze_score label word
org 041deh
_bullet_template_tune label word
org 041fch
_resident label dword
org 04206h
_bombing label byte
org 04208h
_playchar_bomb_func label word
org 04a88h
_stage_render label word
org 04abeh
_overlay1 label word
org 04ac0h
_overlay2 label word
org 04ad4h
_lives label byte
org 04ad5h
_bombs label byte
org 04ad6h
_page_back label byte
org 04ad7h
_page_front label byte
org 05760h
_frames_unused label dword
org 05764h
_stage_frame label word
org 05766h
_stage_frame_mod2 label byte
org 05767h
_stage_frame_mod4 label byte
org 05768h
_stage_frame_mod8 label byte
org 05769h
_stage_frame_mod16 label byte
org 0576ah
_slowdown_factor label word
org 0576ch
_quit label byte
org 0576dh
_palette_changed label byte
org 0576eh
_stage_id label byte
org 0576fh
_rank label byte
org 05770h
_playperf label byte
org 05771h
_playperf_max label byte
org 05772h
_playperf_min label byte
org 05773h
_playchar label byte
org 05776h
_turbo_mode label byte
org 0577ch
_slowdown_caused_by_bullets label byte
org 0c33eh
_pellet_bottom_col label word
org 0c4aeh
_midboss_update label dword
org 0c4b2h
_midboss_render label word
org 0c4beh
_playchar_shot_funcs label word
org 0c652h
_item_point_score_at_full_dream label word
org 0c656h
_std_update label word
org 0c672h
_boss_update label dword
org 0c676h
_boss_fg_render label word
org 0c678h
_boss_custombullets_render label word
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end
else
; Exact original-order THREE source functions with real before/after near Pascal relaxation.
.386
.model large
_TEXT segment word public 'CODE' use16
assume cs:_TEXT
public PALETTE_SHOW, TEXT_CLEAR, PALETTE_BLACK_OUT, PALETTE_ENTRY_RGB, TEXT_FILLCA
public SUPER_ENTRY_BFNT, SUPER_CONVERT_TINY
org 00644h
PALETTE_BLACK_OUT label far
org 02158h
PALETTE_SHOW label far
org 023f0h
PALETTE_ENTRY_RGB label far
org 024f6h
TEXT_CLEAR label far
org 02508h
TEXT_FILLCA label far
org 02d16h
SUPER_ENTRY_BFNT label far
org 035a2h
SUPER_CONVERT_TINY label far
org 0ae10h
_TEXT ends
DEMO_TEXT segment word public 'CODE' use16
assume cs:DEMO_TEXT
public @slowdown_frame_delay$qv
org 0000eh
@slowdown_frame_delay$qv label near
org 00028h
DEMO_TEXT ends
main_01 group DEMO_TEXT
end
endif
