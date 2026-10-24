; TH05 Sara update original-address symbol-only context.
; No instruction bodies, callbacktable values, globals or source-owned state.
.386
.model large
; No .stack.
MAIN01_BASE equ 0ae10h
SHARED_BASE equ 14ab0h
SHARED_END equ (SHARED_BASE + 0232h)
MAIN03_BASE equ 15270h
UNIT_START equ 1d19eh
UNIT_SIZE equ 0720h
UNIT_END equ (UNIT_START + UNIT_SIZE)
DGROUP_BASE equ 209d0h

_TEXT segment word public 'CODE' use16
org MAIN01_BASE
_TEXT ends

BOSS_BG_TEXT segment byte public 'CODE' use16
assume cs:BOSS_BG_TEXT
public SELECT_FOR_RANK
org 021a2h
SELECT_FOR_RANK label far
public @SARA_BG_RENDER$QV
org 05c07h
@SARA_BG_RENDER$QV label near
BOSS_BG_TEXT ends
SARA_MAIN01_TAIL segment byte public 'CODE' use16
org (SHARED_BASE - (MAIN01_BASE + 05c07h))
SARA_MAIN01_TAIL ends
main_01 group BOSS_BG_TEXT, SARA_MAIN01_TAIL

SARA_SHARED_TEXT segment para public 'CODE' use16
assume cs:SARA_SHARED_TEXT
public SND_SE_PLAY
org 0232h
SND_SE_PLAY label far
SARA_SHARED_TEXT ends
SARA_SHARED_TAIL segment byte public 'CODE' use16
org (MAIN03_BASE - SHARED_END)
SARA_SHARED_TAIL ends

LASER_SC_TEXT segment byte public 'CODE' use16
assume cs:LASER_SC_TEXT
public @randring2_next16$qv
org 02ch
@randring2_next16$qv label near
public @RANDRING2_NEXT16_AND$QUI
org 03ah
@RANDRING2_NEXT16_AND$QUI label near
public @RANDRING2_NEXT16_MOD$QUI
org 050h
@RANDRING2_NEXT16_MOD$QUI label near
public @BOSS_FLYSTEP_RANDOM$QI
org 06a4h
@BOSS_FLYSTEP_RANDOM$QI label near
public @gather_add_only$qv
org 01d85h
@gather_add_only$qv label near
public @GATHER_ADD_ONLY_3STACK$QIUIUI
org 01dedh
@GATHER_ADD_ONLY_3STACK$QIUIUI label near
public _bullets_add_regular
org 01f94h
_bullets_add_regular label near
public _bullets_add_special
org 01fa8h
_bullets_add_special label near
public @LASER_MANUAL_FIXED_SPAWN$QI
org 054dbh
@LASER_MANUAL_FIXED_SPAWN$QI label near
public @LASER_MANUAL_GROW$QI
org 05535h
@LASER_MANUAL_GROW$QI label near
public @LASER_STOP$QI
org 0555eh
@LASER_STOP$QI label near
public @HUD_HP_UPDATE_AND_RENDER$QII
org 07286h
@HUD_HP_UPDATE_AND_RENDER$QII label near
public @BOSS_SCORE_BONUS$QUI
org 07348h
@BOSS_SCORE_BONUS$QUI label near
org (UNIT_START - MAIN03_BASE)
LASER_SC_TEXT ends

B1_UPDATE_TEXT segment byte public 'CODE' use16
B1_UPDATE_TEXT ends

SARA_MAIN03_TAIL segment byte public 'CODE' use16
assume cs:SARA_MAIN03_TAIL
public @boss_hittest_shots$qv
org (MAIN03_BASE + 0a860h - UNIT_END)
@boss_hittest_shots$qv label near
public @boss_hittest_shots_invincible$qv
org (MAIN03_BASE + 0a88ah - UNIT_END)
@boss_hittest_shots_invincible$qv label near
public @BOSS_PHASE_NEXT$Q16EXPLOSION_TYPE_TI
org (MAIN03_BASE + 0a8f1h - UNIT_END)
@BOSS_PHASE_NEXT$Q16EXPLOSION_TYPE_TI label near
public @BOSS_DEFEAT_UPDATE$QUI
org (MAIN03_BASE + 0a941h - UNIT_END)
@BOSS_DEFEAT_UPDATE$QUI label near
org (DGROUP_BASE - UNIT_END)
SARA_MAIN03_TAIL ends
main_03 group LASER_SC_TEXT, B1_UPDATE_TEXT, SARA_MAIN03_TAIL

_DATA segment word public 'DATA' use16
public _SARA_PATTERNS_PHASE_2_3
org 01f6eh
_SARA_PATTERNS_PHASE_2_3 label byte
public _bg_render_bombing_func
org 0350ah
_bg_render_bombing_func label word
public _homing_target
org 03f8ah
_homing_target label byte
public _bullet_template_tune
org 041deh
_bullet_template_tune label word
public _stage_frame_mod16
org 05769h
_stage_frame_mod16 label byte
public _bullet_template
org 0577eh
_bullet_template label byte
public _lasers
org 0578ch
_lasers label byte
public _laser_template
org 05a8ch
_laser_template label byte
public _boss
org 05abah
_boss label byte
public _gather_template
org 09ea6h
_gather_template label byte
public _sara_phase_2_3_pattern
org 0c664h
_sara_phase_2_3_pattern label word
public _boss_statebyte
org 0c682h
_boss_statebyte label byte
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end
