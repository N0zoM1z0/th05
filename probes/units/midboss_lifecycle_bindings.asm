; Complete real six-function family: foreign addresses only, no bytes/stack.
.386
.model large
MAIN01_BASE equ 0ae10h
MAIN03_BASE equ 15270h
UNIT_START equ 1c4a1h
UNIT_END equ 1c669h
DGROUP_BASE equ 209d0h
_TEXT segment word public 'CODE' use16
org MAIN01_BASE
_TEXT ends
MAI_TEXT segment word public 'CODE' use16
assume cs:MAI_TEXT
public NULLFUNC_NEAR, NULLFUNC_FAR, @HUD_HP_PUT$QI, @MIDBOSS_INVALIDATE_FUNC$QV
org 192eh
NULLFUNC_NEAR label near
org 1930h
NULLFUNC_FAR label far
org 247bh
@HUD_HP_PUT$QI label far
org 5badh
@MIDBOSS_INVALIDATE_FUNC$QV label near
org (MAIN03_BASE - MAIN01_BASE)
MAI_TEXT ends
main_01 group MAI_TEXT
MIDBOSS_FAMILY_TEXT segment byte public 'CODE' use16
assume cs:MIDBOSS_FAMILY_TEXT
public @RANDRING2_NEXT16_MOD$QUI, @POINTNUMS_ADD_YELLOW$QIIUI
org (152c0h - MAIN03_BASE)
@RANDRING2_NEXT16_MOD$QUI label near
org (16e28h - MAIN03_BASE)
@POINTNUMS_ADD_YELLOW$QIIUI label near
org (UNIT_START - MAIN03_BASE)
MIDBOSS_FAMILY_TEXT ends
main_03 group MIDBOSS_FAMILY_TEXT
MIDBOSS_LIFECYCLE_DGROUP_GAP segment byte public 'CODE' use16
org (DGROUP_BASE - UNIT_END)
MIDBOSS_LIFECYCLE_DGROUP_GAP ends
_DATA segment word public 'DATA' use16
public _pointnum_times_2, _hud_hp_bar_value_prev, _boss_phase_timed_out
public _playfield_shake_anim_time, _score_delta, _stage_frame, _midboss, _boss
public _midboss_active, _midboss_invalidate, _midboss_update, _midboss_render
public _midboss_update_func, _midboss_render_func
org 18aah
_pointnum_times_2 label byte
org 1a5eh
_hud_hp_bar_value_prev label word
org 1fc8h
_boss_phase_timed_out label byte
org 3520h
_playfield_shake_anim_time label word
org 3712h
_score_delta label dword
org 5764h
_stage_frame label word
org 5aa4h
_midboss label byte
org 5abah
_boss label byte
org 0c4aah
_midboss_active label byte
org 0c4ach
_midboss_invalidate label word
org 0c4aeh
_midboss_update label dword
org 0c4b2h
_midboss_render label word
org 0c4b4h
_midboss_update_func label dword
org 0c4b8h
_midboss_render_func label word
org 0c4bah
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end
