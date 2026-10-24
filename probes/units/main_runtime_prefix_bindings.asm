; Original outside-only context for natural MAIN entry/gameplay prefix.
; No implementation, NOP, resource payload or stack is supplied here.
.386
.model large
_TEXT segment word public 'CODE' use16
assume cs:_TEXT
public PALETTE_SHOW
org 02158h
PALETTE_SHOW label far
public TEXT_CLEAR
org 024f6h
TEXT_CLEAR label far
org 0ae10h
_TEXT ends
DEMO_TEXT segment word public 'CODE' use16
assume cs:DEMO_TEXT
public @slowdown_frame_delay$qv
org 0eh
@slowdown_frame_delay$qv label near
org 028h
DEMO_TEXT ends
RUNTIME_MAIN01_TEXT segment byte public 'CODE' use16
assume cs:RUNTIME_MAIN01_TEXT
public @stage_session_init$qv
org 01d4h
@stage_session_init$qv label near
public _stage_session_free
org 05a5h
_stage_session_free label near
public _pause
org 05d4h
_pause label near
public @ems_allocate_and_preload_eyecatc$qv
org 07c3h
@ems_allocate_and_preload_eyecatc$qv label near
public @grcg_setmode_rmw$qv
org 01195h
@grcg_setmode_rmw$qv label near
public @scroll_driver$qv
org 014a3h
@scroll_driver$qv label near
public @playfield_shake_update_and_rende$qv
org 01516h
@playfield_shake_update_and_rende$qv label near
public @player_update$qv
org 01bdah
@player_update$qv label near
public PLAYER_RENDER
org 01cf3h
PLAYER_RENDER label near
public @GAMEEXECL$QNXC
org 01e5fh
@GAMEEXECL$QNXC label far
public PLAYPERF_RAISE
org 01f17h
PLAYPERF_RAISE label far
public @score_update_and_render$qv
org 0248fh
@score_update_and_render$qv label near
public @ENEMIES_RENDER$QV
org 02eedh
@ENEMIES_RENDER$QV label near
public _sparks_update
org 03023h
_sparks_update label near
public _sparks_render
org 0306fh
_sparks_render label near
public POINTNUMS_UPDATE
org 03143h
POINTNUMS_UPDATE label near
public POINTNUMS_RENDER
org 031b3h
POINTNUMS_RENDER label near
public @circles_update$qv
org 032bfh
@circles_update$qv label near
public @circles_render$qv
org 032f5h
@circles_render$qv label near
public @cfg_load_resident_ptr$qv
org 035bbh
@cfg_load_resident_ptr$qv label near
public @lasers_update$qv
org 07b4ah
@lasers_update$qv label near
public @lasers_render$qv
org 07c82h
@lasers_render$qv label near
public BULLETS_RENDER
org 08122h
BULLETS_RENDER label near
public @shots_update$qv
org 08378h
@shots_update$qv label near
public @shots_render$qv
org 08510h
@shots_render$qv label near
public ITEMS_RENDER
org 08881h
ITEMS_RENDER label near
org 09a4dh
RUNTIME_MAIN01_TEXT ends
main_01 group DEMO_TEXT, RUNTIME_MAIN01_TEXT
SHARED segment para public 'CODE' use16
assume cs:SHARED
public SND_DETERMINE_MODES
org 0124h
SND_DETERMINE_MODES label far
public _snd_se_update
org 026ch
_snd_se_update label far
public SND_LOAD
org 03f4h
SND_LOAD label far
public @GAME_INIT_MAIN$QNXUC
org 04cah
@GAME_INIT_MAIN$QNXUC label far
public @input_reset_sense$qv
org 0512h
@input_reset_sense$qv label far
public @input_sense$qv
org 051ah
@input_sense$qv label far
public @FRAME_DELAY$QI
org 0652h
@FRAME_DELAY$QI label far
org 07c0h
SHARED ends
RUNTIME_MAIN03_TEXT segment byte public 'CODE' use16
assume cs:RUNTIME_MAIN03_TEXT
public ENEMIES_UPDATE
org 01977h
ENEMIES_UPDATE label far
public @gather_update$qv
org 01e32h
@gather_update$qv label far
public @gather_render$qv
org 01ed0h
@gather_render$qv label far
public @bullets_update$qv
org 06e6fh
@bullets_update$qv label far
public ITEMS_UPDATE
org 07e3dh
ITEMS_UPDATE label far
org 0b760h
RUNTIME_MAIN03_TEXT ends
main_03 group RUNTIME_MAIN03_TEXT
_DATA segment word public 'DATA' use16
public _debug_frame_step
org 090h
_debug_frame_step label byte
public _debug_frame_step_enabled
org 091h
_debug_frame_step_enabled label byte
public _main_pf_fn
org 0b2h
_main_pf_fn label byte
public _se_fn
org 0beh
_se_fn label byte
public _op_fn
org 0c3h
_op_fn label byte
public _random_seed
org 0418h
_random_seed label dword
public _mem_assign_paras
org 0824h
_mem_assign_paras label word
public _total_slow_frames
org 01ec2h
_total_slow_frames label dword
public _total_frames
org 01ec6h
_total_frames label dword
public _input_sense_hook
org 0261ch
_input_sense_hook label word
public _vsync_Count1
org 0267ah
_vsync_Count1 label word
public _key_det
org 03064h
_key_det label word
public _bg_render_not_bombing
org 03506h
_bg_render_not_bombing label word
public _bg_render_bombing
org 03508h
_bg_render_bombing label word
public _player_is_hit
org 036f3h
_player_is_hit label byte
public _stage_vm
org 03f8eh
_stage_vm label dword
public _resident
org 041fch
_resident label dword
public _bombing
org 04206h
_bombing label byte
public _playchar_bomb_func
org 04208h
_playchar_bomb_func label word
public _stage_render
org 04a88h
_stage_render label word
public _overlay1
org 04abeh
_overlay1 label word
public _overlay2
org 04ac0h
_overlay2 label word
public _page_back
org 04ad6h
_page_back label byte
public _page_front
org 04ad7h
_page_front label byte
public _frames_unused
org 05760h
_frames_unused label dword
public _stage_frame
org 05764h
_stage_frame label word
public _stage_frame_mod2
org 05766h
_stage_frame_mod2 label byte
public _stage_frame_mod4
org 05767h
_stage_frame_mod4 label byte
public _stage_frame_mod8
org 05768h
_stage_frame_mod8 label byte
public _stage_frame_mod16
org 05769h
_stage_frame_mod16 label byte
public _slowdown_factor
org 0576ah
_slowdown_factor label word
public _quit
org 0576ch
_quit label byte
public _palette_changed
org 0576dh
_palette_changed label byte
public _slowdown_caused_by_bullets
org 0577ch
_slowdown_caused_by_bullets label byte
public _midboss_update
org 0c4aeh
_midboss_update label dword
public _midboss_render
org 0c4b2h
_midboss_render label word
public _std_update
org 0c656h
_std_update label word
public _boss_update
org 0c672h
_boss_update label dword
public _boss_fg_render
org 0c676h
_boss_fg_render label word
public _boss_custombullets_render
org 0c678h
_boss_custombullets_render label word
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end
