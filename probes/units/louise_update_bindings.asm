; Real address-only context for the complete natural Louise update callback.
; No instructions, initialized values or holes inside the compiler extent.
.386
.model large
MAIN01_BASE equ 0ae10h
SHARED_BASE equ 14ab0h
MAIN03_BASE equ 15270h
UNIT_START equ 1dd40h
AFTER_BASE equ 1df90h
DGROUP_BASE equ 209d0h

_TEXT segment word public 'CODE' use16
org MAIN01_BASE
_TEXT ends
LOUISE_UPDATE_MAIN01_TEXT segment byte public 'CODE' use16
assume cs:LOUISE_UPDATE_MAIN01_TEXT
public @LOUISE_BG_RENDER$QV
org 05c6fh
@LOUISE_BG_RENDER$QV label near
org (SHARED_BASE - MAIN01_BASE)
LOUISE_UPDATE_MAIN01_TEXT ends
; Actual zero compiler segments merge at the real main_01 context boundary.
LOUISE_MAIN01_CONTEXT segment byte public 'CODE' use16
LOUISE_MAIN01_CONTEXT ends
GENERIC_BOSS_MAIN01_TEXT segment byte public 'CODE' use16
GENERIC_BOSS_MAIN01_TEXT ends
main_01 group LOUISE_UPDATE_MAIN01_TEXT, LOUISE_MAIN01_CONTEXT, GENERIC_BOSS_MAIN01_TEXT
SHARED segment byte public 'CODE' use16
assume cs:SHARED
public SND_SE_PLAY
org 0232h
SND_SE_PLAY label far
org (MAIN03_BASE - SHARED_BASE)
SHARED ends

; Match the canonical laser header's empty source segment at the real main03
; prefix. Its foreign labels all retain the actual1527 near group frame.
LASER_SC_TEXT segment byte public 'CODE' use16
assume cs:LASER_SC_TEXT
public @HUD_HP_UPDATE_AND_RENDER$QII, @BOSS_SCORE_BONUS$QUI
public @LOUISE_FLYSTEP$QII
public @louise_pattern_blue_spreads$qv, @louise_pattern_red_stacks$qv
public @louise_pattern_mirrored_fans$qv, @louise_pattern_sweeping_lasers$qv
public @louise_pattern_turning_rings$qv, @louise_pattern_aimed_pellets$qv
org (1c4f6h - MAIN03_BASE)
@HUD_HP_UPDATE_AND_RENDER$QII label near
org (1c5b8h - MAIN03_BASE)
@BOSS_SCORE_BONUS$QUI label near
org (1d8beh - MAIN03_BASE)
@LOUISE_FLYSTEP$QII label near
org (1d99ah - MAIN03_BASE)
@louise_pattern_blue_spreads$qv label near
org (1da5ah - MAIN03_BASE)
@louise_pattern_red_stacks$qv label near
org (1dae5h - MAIN03_BASE)
@louise_pattern_mirrored_fans$qv label near
org (1dbc3h - MAIN03_BASE)
@louise_pattern_sweeping_lasers$qv label near
org (1dc62h - MAIN03_BASE)
@louise_pattern_turning_rings$qv label near
org (1dce8h - MAIN03_BASE)
@louise_pattern_aimed_pellets$qv label near
org (UNIT_START - MAIN03_BASE)
LASER_SC_TEXT ends
B4_UPDATE_TEXT segment byte public 'CODE' use16
B4_UPDATE_TEXT ends

; All compiler instructions/table/zero occupy the source contribution alone.
; The separate real paragraph begins1DF90 after original full end1DF86.
BOSS_TEXT segment para public 'CODE' use16
assume cs:BOSS_TEXT
public @boss_hittest_shots$qv, @boss_hittest_shots_invincible$qv
public @BOSS_PHASE_NEXT$Q16EXPLOSION_TYPE_TI, @BOSS_DEFEAT_UPDATE$QUI
org (1fad0h - AFTER_BASE)
@boss_hittest_shots$qv label near
org (1fafah - AFTER_BASE)
@boss_hittest_shots_invincible$qv label near
org (1fb61h - AFTER_BASE)
@BOSS_PHASE_NEXT$Q16EXPLOSION_TYPE_TI label near
org (1fbb1h - AFTER_BASE)
@BOSS_DEFEAT_UPDATE$QUI label near
org (DGROUP_BASE - AFTER_BASE)
BOSS_TEXT ends
main_03 group LASER_SC_TEXT, B4_UPDATE_TEXT, BOSS_TEXT

_DATA segment word public 'DATA' use16
public _bg_render_bombing_func, _homing_target, _bullet_template
public _boss, _gather_template, _boss_statebyte
org 350ah
_bg_render_bombing_func label word
org 3f8ah
_homing_target label byte
org 577eh
_bullet_template label byte
org 5abah
_boss label byte
org 9ea6h
_gather_template label byte
org 0c682h
_boss_statebyte label byte
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end
