ifdef BINDINGS_AFTER
; Genuine original 1826+1400 contiguous C++ source, foreign public addresses only.
.386
.model large
DEMO_TEXT segment byte public 'CODE' use16
assume cs:DEMO_TEXT
DEMO_TEXT ends
LIFECYCLE_TEXT segment byte public 'CODE' use16
assume cs:LIFECYCLE_TEXT
LIFECYCLE_TEXT ends
MAIN01_FOREIGN_AFTER segment byte public 'CODE' use16
assume cs:MAIN01_FOREIGN_AFTER
public TILES_FILL_INITIAL, @TILES_RENDER_ALL$QV, @tiles_invalidate_reset$qv, @tiles_activate$qv
public @std_free$qv, @grcg_setmode_rmw$qv, @scroll_driver$qv, @playfield_shake_update_and_rende$qv
public @randring_fill$qv, NULLFUNC_NEAR, @std_load$qv, @hiscore_load$qv
public @player_update$qv, PLAYER_RENDER, @GAMEEXECL$QNXC, PLAYPERF_RAISE
public @score_reset$qv, @hud_put$qv, HUD_SCORE_PUT, @score_update_and_render$qv
public @map_free$qv, BB_CHEETO_LOAD, @ENEMIES_RENDER$QV, _sparks_update
public _sparks_render, _sparks_init, POINTNUMS_INIT, POINTNUMS_UPDATE
public POINTNUMS_RENDER, @circles_update$qv, @circles_render$qv, @shot_level_update$qv
public SHOT_LEVEL_UPDATE, BB_TXT_LOAD, MPN_LOAD, @map_load$qv
public @cfg_load_resident_ptr$qv, @bomb_reset$qv, @BOMB_REIMU$QV, @BOMB_MARISA$QV
public @BOMB_MIMA$QV, @BOMB_YUUKA$QV, BB_PLAYCHAR_LOAD, @clear_blue_vram_pages$qv
public @SHINKI_BG_RENDER$QV, @overlay_wipe$qv, @overlay_black$qv, @OVERLAY_STAGE_ENTER_UPDATE_AND_R$QV
public _stage_state_init, @lasers_update$qv, @lasers_render$qv, @dialog_free$qv
public BULLETS_RENDER, @shots_update$qv, @shots_render$qv, ITEMS_RENDER
public @dialog_load$qv, @std_update_frames_then_animate_d$qv, @bb_boss_free$qv, @STAGE1_SETUP$QV
public @STAGE2_SETUP$QV, @STAGE3_SETUP$QV, @STAGE4_SETUP$QV, @STAGE5_SETUP$QV
public @STAGE6_SETUP$QV, @STAGEX_SETUP$QV
org 000cch
TILES_FILL_INITIAL label near
org 0011ah
@TILES_RENDER_ALL$QV label near
org 00252h
@tiles_invalidate_reset$qv label near
org 002bdh
@tiles_activate$qv label far
org 003e2h
@std_free$qv label near
org 00726h
@grcg_setmode_rmw$qv label near
org 00a34h
@scroll_driver$qv label near
org 00aa7h
@playfield_shake_update_and_rende$qv label near
org 00c16h
@randring_fill$qv label near
org 00c6ch
NULLFUNC_NEAR label near
org 00c70h
@std_load$qv label near
org 00ed2h
@hiscore_load$qv label near
org 0116bh
@player_update$qv label near
org 01284h
PLAYER_RENDER label near
org 013f0h
@GAMEEXECL$QNXC label far
org 014a8h
PLAYPERF_RAISE label far
org 014f4h
@score_reset$qv label near
org 01851h
@hud_put$qv label far
org 019eeh
HUD_SCORE_PUT label near
org 01a20h
@score_update_and_render$qv label near
org 021eeh
@map_free$qv label near
org 02386h
BB_CHEETO_LOAD label near
org 0247eh
@ENEMIES_RENDER$QV label near
org 025b4h
_sparks_update label near
org 02600h
_sparks_render label near
org 02662h
_sparks_init label near
org 0269ch
POINTNUMS_INIT label near
org 026d4h
POINTNUMS_UPDATE label near
org 02744h
POINTNUMS_RENDER label near
org 02850h
@circles_update$qv label near
org 02886h
@circles_render$qv label near
org 02910h
@shot_level_update$qv label far
SHOT_LEVEL_UPDATE label far
org 029e4h
BB_TXT_LOAD label near
org 02aaah
MPN_LOAD label near
org 02af0h
@map_load$qv label near
org 02b4ch
@cfg_load_resident_ptr$qv label near
org 03f7eh
@bomb_reset$qv label near
org 04299h
@BOMB_REIMU$QV label near
org 044e5h
@BOMB_MARISA$QV label near
org 04708h
@BOMB_MIMA$QV label near
org 0489fh
@BOMB_YUUKA$QV label near
org 04960h
BB_PLAYCHAR_LOAD label near
org 04af8h
@clear_blue_vram_pages$qv label near
org 0593fh
@SHINKI_BG_RENDER$QV label near
org 0627eh
@overlay_wipe$qv label near
org 062a0h
@overlay_black$qv label near
org 062c1h
@OVERLAY_STAGE_ENTER_UPDATE_AND_R$QV label near
org 06ff2h
_stage_state_init label near
org 070dbh
@lasers_update$qv label near
org 07213h
@lasers_render$qv label near
org 075beh
@dialog_free$qv label near
org 076b3h
BULLETS_RENDER label near
org 07909h
@shots_update$qv label near
org 07aa1h
@shots_render$qv label near
org 07e12h
ITEMS_RENDER label near
org 07ee9h
@dialog_load$qv label near
org 07f2ah
@std_update_frames_then_animate_d$qv label near
org 08109h
@bb_boss_free$qv label near
org 08a6ah
@STAGE1_SETUP$QV label near
org 08b39h
@STAGE2_SETUP$QV label near
org 08bf6h
@STAGE3_SETUP$QV label near
org 08cc5h
@STAGE4_SETUP$QV label near
org 08d9fh
@STAGE5_SETUP$QV label near
org 08e9ch
@STAGE6_SETUP$QV label near
org 08f2ch
@STAGEX_SETUP$QV label near
org 08fdeh
MAIN01_FOREIGN_AFTER ends
main_01 group DEMO_TEXT, LIFECYCLE_TEXT, MAIN01_FOREIGN_AFTER
EMS_SHARED_PROVIDER segment para public 'CODE' use16
assume cs:EMS_SHARED_PROVIDER
public SND_DETERMINE_MODES, CDG_PUT_NOALPHA_8, _snd_se_update, SND_LOAD
public SND_KAJA_INTERRUPT, @GAME_INIT_MAIN$QNXUC, @input_reset_sense$qv, @input_sense$qv
public @input_reset_sense_held$qv, @INPUT_WAIT_FOR_CHANGE$QI, @FRAME_DELAY$QI, CDG_LOAD_SINGLE_NOALPHA
public CDG_LOAD_ALL_NOALPHA, CDG_LOAD_ALL, CDG_FREE
org 00124h
SND_DETERMINE_MODES label far
org 001c0h
CDG_PUT_NOALPHA_8 label far
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
org 00618h
@input_reset_sense_held$qv label far
org 00628h
@INPUT_WAIT_FOR_CHANGE$QI label far
org 00652h
@FRAME_DELAY$QI label far
org 00668h
CDG_LOAD_SINGLE_NOALPHA label far
org 00726h
CDG_LOAD_ALL_NOALPHA label far
org 0072ch
CDG_LOAD_ALL label far
org 00788h
CDG_FREE label far
org 007c0h
EMS_SHARED_PROVIDER ends
MAIN03_FOREIGN segment byte public 'CODE' use16
assume cs:MAIN03_FOREIGN
public ENEMIES_UPDATE, @gather_update$qv, @gather_render$qv, BULLET_TEMPLATE_TUNE_EASY
public BULLET_TEMPLATE_TUNE_NORMAL, BULLET_TEMPLATE_TUNE_HARD, BULLET_TEMPLATE_TUNE_LUNATIC, @bullets_update$qv
public @midboss_reset$qv, @items_init$qv, ITEMS_UPDATE
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
org 0799eh
@items_init$qv label far
org 07e3dh
ITEMS_UPDATE label far
org 0b760h
MAIN03_FOREIGN ends
main_03 group MAIN03_FOREIGN
_DATA segment word public 'DATA' use16
public _debug_frame_step, _debug_frame_step_enabled, _gsCHUUDAN, _gsSAIKAI
public _gsSHUURYOU, _eyename, _load_playchar_resources, _stage_bgm_name
public _bbname, _main_pf_fn, _se_fn, _op_fn
public _SESSION_EYE_RGB, _SESSION_REIMU_BFT, _SESSION_MARI_BFT, _SESSION_MIMA_BFT
public _SESSION_YUKA_BFT, _SESSION_MIKOD_BFT, _SESSION_MIKO32_BFT, _SESSION_REIMU16_BFT
public _SESSION_MARI16_BFT, _SESSION_MIMA16_BFT, _SESSION_YUKA16_BFT, _SESSION_MIKO16_BFT
public _SESSION_BOMB_YUUKA_BFT, _SESSION_BOMB_BFT, _SESSION_BSS0_CD2, _SESSION_ST00_BFT
public _SESSION_ST00_MPN, _SESSION_BSS1_CD2, _SESSION_ST01_BFT, _SESSION_ST01_MPN
public _SESSION_BSS2_CD2, _SESSION_ST02_BFT, _SESSION_ST02_MPN, _SESSION_BSS3_CD2
public _SESSION_ST03_BFT, _SESSION_ST03_MPN, _SESSION_BSS4_CD2, _SESSION_ST04_BFT
public _SESSION_ST04_MPN, _SESSION_BSS4_CD2_REPEAT, _SESSION_ST04_BFT_REPEAT, _SESSION_BSS6_CD2
public _SESSION_ST06_BFT, _SESSION_ST06_MPN, _aGAME_PAUSE_SPACES_1, _aGAME_PAUSE_SPACES_2
public _aGAME_PAUSE_SPACES_3, _demo_fn, _DEMOPLAY_BINARY_OP, _EMS_NAME
public _FACESET_REIMU_FN_0, _FACESET_MARISA_FN_0, _FACESET_MIMA_FN, _FACESET_YUUKA_FN
public _PaletteTone, _random_seed, _mem_assign_paras, _SHOT_FUNCS
public _total_slow_frames, _total_frames, _input_sense_hook, _vsync_Count1
public _vsync_Count2, _key_det, _shiftkey, _cdg_slots
public _scroll_row_advance_current, _scroll_line_on_page, _bg_render_not_bombing, _bg_render_bombing
public _bg_render_bombing_func, _scroll_row_advance_previous, _tile_ring_scroll_row_prev, _scroll_subpixel_line
public _scroll_line, _scroll_active, _playfield_shake_x, _playfield_shake_y
public _player_pos, _playchar_speed_aligned, _playchar_speed_diagonal, _player_invincibility_time
public _player_miss_animation_frame, _power, _shot_time, _player_is_hit
public _miss_time, _stage_point_items_collected, _dream, _score
public _stage_vm, _graze_score, _bullet_template_tune, _resident
public _bombing, _playchar_bomb_func, _stage_render, _overlay1
public _overlay2, _lives, _bombs, _page_back
public _page_front, _frames_unused, _stage_frame, _stage_frame_mod2
public _stage_frame_mod4, _stage_frame_mod8, _stage_frame_mod16, _slowdown_factor
public _quit, _palette_changed, _stage_id, _rank
public _playperf, _playperf_max, _playperf_min, _playchar
public _Ems, _turbo_mode, _DemoBuf, _slowdown_caused_by_bullets
public _pellet_bottom_col, _midboss_update, _midboss_render, _bombing_disabled
public _playchar_shot_funcs, _item_point_score_at_full_dream, _std_update, _boss_update
public _boss_fg_render, _boss_custombullets_render
org 00090h
_debug_frame_step label byte
org 00091h
_debug_frame_step_enabled label byte
org 00092h
_gsCHUUDAN label byte
org 00095h
_gsSAIKAI label byte
org 00098h
_gsSHUURYOU label byte
org 0009ch
_eyename label dword
org 000a0h
_load_playchar_resources label word
org 000a2h
_stage_bgm_name label dword
org 000a6h
_bbname label dword
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
org 0020dh
_aGAME_PAUSE_SPACES_1 label byte
org 00212h
_aGAME_PAUSE_SPACES_2 label byte
org 00217h
_aGAME_PAUSE_SPACES_3 label byte
org 0021ch
_demo_fn label byte
org 00226h
_DEMOPLAY_BINARY_OP label byte
org 00229h
_EMS_NAME label byte
org 0023ah
_FACESET_REIMU_FN_0 label byte
org 00243h
_FACESET_MARISA_FN_0 label byte
org 0024ch
_FACESET_MIMA_FN label byte
org 00255h
_FACESET_YUUKA_FN label byte
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
org 03066h
_shiftkey label byte
org 0306ch
_cdg_slots label byte
org 034f6h
_scroll_row_advance_current label byte
org 034feh
_scroll_line_on_page label word
org 03506h
_bg_render_not_bombing label word
org 03508h
_bg_render_bombing label word
org 0350ah
_bg_render_bombing_func label word
org 03510h
_scroll_row_advance_previous label byte
org 03512h
_tile_ring_scroll_row_prev label word
org 03514h
_scroll_subpixel_line label byte
org 03516h
_scroll_line label word
org 0351ah
_scroll_active label byte
org 0351ch
_playfield_shake_x label word
org 0351eh
_playfield_shake_y label word
org 036d2h
_player_pos label byte
org 036deh
_playchar_speed_aligned label word
org 036e2h
_playchar_speed_diagonal label word
org 036eeh
_player_invincibility_time label byte
org 036efh
_player_miss_animation_frame label byte
org 036f0h
_power label byte
org 036f2h
_shot_time label byte
org 036f3h
_player_is_hit label byte
org 036f4h
_miss_time label byte
org 036f5h
_stage_point_items_collected label byte
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
org 05774h
_Ems label word
org 05776h
_turbo_mode label byte
org 05778h
_DemoBuf label dword
org 0577ch
_slowdown_caused_by_bullets label byte
org 0c33eh
_pellet_bottom_col label word
org 0c4aeh
_midboss_update label dword
org 0c4b2h
_midboss_render label word
org 0c4bah
_bombing_disabled label byte
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
org 0c678h
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end
else
; Genuine original 1826+1400 contiguous C++ source, foreign public addresses only.
.386
.model large
_TEXT segment word public 'CODE' use16
assume cs:_TEXT
public PALETTE_BLACK_IN, PALETTE_BLACK_OUT, FILE_CLOSE, FILE_READ
public FILE_ROPEN, GAIJI_PUTSA, PALETTE_SHOW, PALETTE_ENTRY_RGB
public TEXT_CLEAR, TEXT_FILLCA, TEXT_PUTSA, HMEM_ALLOCBYTE
public HMEM_FREE, SUPER_ENTRY_BFNT, SUPER_CLEAN, SUPER_CONVERT_TINY
public EMS_READ, EMS_ALLOCATE, EMS_EXIST, EMS_SETNAME
public EMS_WRITE, EMS_SPACE
org 00600h
PALETTE_BLACK_IN label far
org 00644h
PALETTE_BLACK_OUT label far
org 00d2eh
FILE_CLOSE label far
org 00d3eh
FILE_READ label far
org 00df2h
FILE_ROPEN label far
org 01dbeh
GAIJI_PUTSA label far
org 02158h
PALETTE_SHOW label far
org 023f0h
PALETTE_ENTRY_RGB label far
org 024f6h
TEXT_CLEAR label far
org 02508h
TEXT_FILLCA label far
org 02598h
TEXT_PUTSA label far
org 0281ah
HMEM_ALLOCBYTE label far
org 0291eh
HMEM_FREE label far
org 02d16h
SUPER_ENTRY_BFNT label far
org 02df0h
SUPER_CLEAN label far
org 035a2h
SUPER_CONVERT_TINY label far
org 03f6ah
EMS_READ label far
org 03fcch
EMS_ALLOCATE label far
org 04000h
EMS_EXIST label far
org 04052h
EMS_SETNAME label far
org 0406ch
EMS_WRITE label far
org 040ceh
EMS_SPACE label far
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
