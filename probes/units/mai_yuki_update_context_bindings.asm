; Genuine outside-contribution context for final patterns and shared update.
; No instruction bytes, callback entries, strings, state values or internal holes.
.386
.model large
MAIN01_BASE equ 0ae10h
SHARED_BASE equ 14ab0h
MAIN03_BASE equ 15270h
UNIT_START equ 17c30h
AFTER_BASE equ 183e0h
DGROUP_BASE equ 209d0h

_TEXT segment word public 'CODE' use16
assume cs:_TEXT
public SUPER_CONVERT_TINY
org 035a2h
SUPER_CONVERT_TINY label far
org MAIN01_BASE
_TEXT ends

MY_UPDATE_MAIN01_TEXT segment byte public 'CODE' use16
assume cs:MY_UPDATE_MAIN01_TEXT
public @TILES_RENDER_ALL$QV, @MAI_YUKI_SURVIVOR_RENDER$QV
public @MAI_YUKI_BG_RENDER$QV, @OVERLAY_BOSS_BGM_UPDATE_AND_REND$QV
public CHEETOS_RENDER, @DIALOG_LOAD$QNXC, @dialog_animate$qv
org 00ddch
@TILES_RENDER_ALL$QV label near
org 05b2fh
@MAI_YUKI_SURVIVOR_RENDER$QV label near
org 05d87h
@MAI_YUKI_BG_RENDER$QV label near
org 0732ah
@OVERLAY_BOSS_BGM_UPDATE_AND_REND$QV label near
org 0811bh
CHEETOS_RENDER label near
org 08b1bh
@DIALOG_LOAD$QNXC label far
org 09048h
@dialog_animate$qv label far
org (SHARED_BASE - MAIN01_BASE)
MY_UPDATE_MAIN01_TEXT ends
main_01 group MY_UPDATE_MAIN01_TEXT

SHARED segment byte public 'CODE' use16
assume cs:SHARED
public SND_SE_PLAY
org 0232h
SND_SE_PLAY label far
org (MAIN03_BASE - SHARED_BASE)
SHARED ends

MAIN_035_TEXT segment byte public 'CODE' use16
assume cs:MAIN_035_TEXT
public @BOSS_EXPLODE_SMALL$Q16EXPLOSION_TYPE_T, @BOSS2_EXPLODE_SMALL$QUI
public @boss_explode_big_circle$qv, @boss2_explode_big_circle$qv
public @YUKI_HITTEST_SHOTS_DAMAGE$QIII, @mai_yuki_hittest_shots$qv
public @MAI_YUKI_FLYSTEP_RANDOM$QI, @mai_pattern_update$qv, @yuki_pattern_update$qv
public @mai_pattern_random_crosses$qv, @mai_pattern_tracking_laser$qv
public @boss_hittest_shots_invincible$qv
public @randring2_next16$qv, @RANDRING2_NEXT16_AND$QUI
public @PLAYER_ANGLE_FROM$Q20%SUBPIXELBASE$TI$TI%T1UC
public _bullets_add_regular, _bullets_add_special
org 002ch
@randring2_next16$qv label near
org 003ah
@RANDRING2_NEXT16_AND$QUI label near
org (171cch - MAIN03_BASE)
@PLAYER_ANGLE_FROM$Q20%SUBPIXELBASE$TI$TI%T1UC label near
org (17204h - MAIN03_BASE)
_bullets_add_regular label near
org (17218h - MAIN03_BASE)
_bullets_add_special label near
org (176ddh - MAIN03_BASE)
@BOSS_EXPLODE_SMALL$Q16EXPLOSION_TYPE_T label near
org (1775dh - MAIN03_BASE)
@BOSS2_EXPLODE_SMALL$QUI label near
org (1778bh - MAIN03_BASE)
@boss_explode_big_circle$qv label near
org (177c7h - MAIN03_BASE)
@boss2_explode_big_circle$qv label near
org (177f0h - MAIN03_BASE)
@YUKI_HITTEST_SHOTS_DAMAGE$QIII label near
org (1782ch - MAIN03_BASE)
@mai_yuki_hittest_shots$qv label near
org (17937h - MAIN03_BASE)
@MAI_YUKI_FLYSTEP_RANDOM$QI label near
org (17957h - MAIN03_BASE)
@mai_pattern_update$qv label near
org (179b4h - MAIN03_BASE)
@yuki_pattern_update$qv label near
org (179ech - MAIN03_BASE)
@mai_pattern_random_crosses$qv label near
org (17b76h - MAIN03_BASE)
@mai_pattern_tracking_laser$qv label near
org (UNIT_START - MAIN03_BASE)
MAIN_035_TEXT ends

; Entire real callback and both compiler tables occupy the source contribution.
; Independent paragraph context follows original full end183D5 at183E0.
LASER_SC_TEXT segment para public 'CODE' use16
assume cs:LASER_SC_TEXT
public YUKI_UPDATE, MAI_UPDATE, @LASER_STOP$QI
public @cheetos_update$qv, @HUD_HP_UPDATE_AND_RENDER$QII
org (18a05h - AFTER_BASE)
YUKI_UPDATE label far
org (1952bh - AFTER_BASE)
MAI_UPDATE label far
org (1a7ceh - AFTER_BASE)
@LASER_STOP$QI label near
public @cheetos_add$qv
org (1a82eh - AFTER_BASE)
@cheetos_add$qv label near
org (1a8cdh - AFTER_BASE)
@cheetos_update$qv label near
org (1c4f6h - AFTER_BASE)
@HUD_HP_UPDATE_AND_RENDER$QII label near
org (1fafah - AFTER_BASE)
@boss_hittest_shots_invincible$qv label near
org (DGROUP_BASE - AFTER_BASE)
LASER_SC_TEXT ends
main_03 group MAIN_035_TEXT, LASER_SC_TEXT

_DATA segment word public 'DATA' use16
public _MAI_PATTERNS_FIRST, _MAI_PATTERNS_FINAL
public _YUKI_PATTERNS_FIRST, _YUKI_PATTERNS_LASER, _YUKI_PATTERNS_FINAL
public _MY_DIALOG_YUKI, _MY_BGM_TITLE_YUKI, _MY_DIALOG_MAI, _MY_BGM_TITLE_MAI
public _PaletteTone, _bg_render_bombing_func, _playfield_shake_x, _playfield_shake_y
public _player_invincibility_time, _homing_target, _bullet_zap, _bullet_clear_time
public _mai_pattern_current, _yuki_pattern_current, _overlay1, _boss_bgm_title
public _stage_frame_mod2, _stage_frame_mod4, _slowdown_factor, _palette_changed
public _lasers, _boss, _boss2, _gather_template
public _boss_update, _boss_fg_render, _boss_custombullets_render
org 003dah
_PaletteTone label word
org 18e6h
_MAI_PATTERNS_FIRST label word
org 18eeh
_MAI_PATTERNS_FINAL label word
org 18feh
_YUKI_PATTERNS_FIRST label word
org 1906h
_YUKI_PATTERNS_LASER label word
org 190eh
_YUKI_PATTERNS_FINAL label word
org 1916h
_MY_DIALOG_YUKI label byte
org 1920h
_MY_BGM_TITLE_YUKI label byte
org 193eh
_MY_DIALOG_MAI label byte
org 1948h
_MY_BGM_TITLE_MAI label byte
org 350ah
_bg_render_bombing_func label word
org 351ch
_playfield_shake_x label word
org 351eh
_playfield_shake_y label word
org 36eeh
_player_invincibility_time label byte
org 3f8ah
_homing_target label byte
org 3f96h
_bullet_zap label byte
org 3f97h
_bullet_clear_time label byte
public _bullet_template_tune
org 41deh
_bullet_template_tune label word
org 442eh
_mai_pattern_current label word
org 4430h
_yuki_pattern_current label word
org 4abeh
_overlay1 label word
org 4ad0h
_boss_bgm_title label dword
org 5766h
_stage_frame_mod2 label byte
org 5767h
_stage_frame_mod4 label byte
org 576ah
_slowdown_factor label word
org 576dh
_palette_changed label byte
public _bullet_template
org 577eh
_bullet_template label byte
org 578ch
_lasers label byte
org 5abah
_boss label byte
org 5ad2h
_boss2 label byte
org 9ea6h
_gather_template label byte
public _custom_entities
org 0b3f4h
_custom_entities label byte
org 0c672h
_boss_update label dword
org 0c676h
_boss_fg_render label word
org 0c678h
_boss_custombullets_render label word
public _boss_statebyte
org 0c682h
_boss_statebyte label byte
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end
