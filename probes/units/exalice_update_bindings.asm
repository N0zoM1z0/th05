; Real foreign frames and outside holes for the complete1060-byte callback.
.386
.model large
MAIN01_BASE equ 0ae10h
SHARED_BASE equ 14ab0h
MAIN03_BASE equ 15270h
UNIT_START equ 1a24ah
AFTER_BASE equ 1a66eh
DGROUP_BASE equ 209d0h
_TEXT segment word public 'CODE' use16
assume cs:_TEXT
public SUPER_CONVERT_TINY
org 035a2h
SUPER_CONVERT_TINY label far
org MAIN01_BASE
_TEXT ends
GENERIC_BOSS_MAIN01_TEXT segment byte public 'CODE' use16
assume cs:GENERIC_BOSS_MAIN01_TEXT
public NULLFUNC_NEAR, @EXALICE_BG_RENDER$QV, EXALICE_CUSTOMBULLETS_RENDER
org 0192eh
NULLFUNC_NEAR label near
org 06856h
@EXALICE_BG_RENDER$QV label near
org 06d69h
EXALICE_CUSTOMBULLETS_RENDER label near
org (SHARED_BASE - MAIN01_BASE)
GENERIC_BOSS_MAIN01_TEXT ends
BOSS_BG_TEXT segment byte public 'CODE' use16
BOSS_BG_TEXT ends
main_01 group GENERIC_BOSS_MAIN01_TEXT, BOSS_BG_TEXT
SHARED segment byte public 'CODE' use16
assume cs:SHARED
public SND_SE_PLAY
org 0232h
SND_SE_PLAY label far
org (MAIN03_BASE - SHARED_BASE)
SHARED ends
X_UPDATE_MAIN03_CONTEXT segment byte public 'CODE' use16
assume cs:X_UPDATE_MAIN03_CONTEXT
public @BOSS_FLYSTEP_RANDOM$QI
org (15914h - MAIN03_BASE)
@BOSS_FLYSTEP_RANDOM$QI label near
public @BOSS_FLYSTEP_TOWARDS$QII
org (15a07h - MAIN03_BASE)
@BOSS_FLYSTEP_TOWARDS$QII label near
public @BOSS_EXPLODE_SMALL$Q16EXPLOSION_TYPE_T
org (176ddh - MAIN03_BASE)
@BOSS_EXPLODE_SMALL$Q16EXPLOSION_TYPE_T label near
public @firewaves_update$qv
org (19871h - MAIN03_BASE)
@firewaves_update$qv label near
public @exalice_charge_update$qv
org (1989bh - MAIN03_BASE)
@exalice_charge_update$qv label near
public @exalice_pattern_random_fan$qv
org (198e3h - MAIN03_BASE)
@exalice_pattern_random_fan$qv label near
public @exalice_pattern_firewave_fans$qv
org (199d5h - MAIN03_BASE)
@exalice_pattern_firewave_fans$qv label near
public @exalice_pattern_gravity_stacks$qv
org (19b13h - MAIN03_BASE)
@exalice_pattern_gravity_stacks$qv label near
public @exalice_pattern_bouncing_rings$qv
org (19c2dh - MAIN03_BASE)
@exalice_pattern_bouncing_rings$qv label near
public @exalice_pattern_fixed_laser_fan$qv
org (19c95h - MAIN03_BASE)
@exalice_pattern_fixed_laser_fan$qv label near
public @exalice_pattern_sweeping_lasers$qv
org (19df0h - MAIN03_BASE)
@exalice_pattern_sweeping_lasers$qv label near
public @exalice_pattern_cross_cheetos$qv
org (19eb2h - MAIN03_BASE)
@exalice_pattern_cross_cheetos$qv label near
public @exalice_pattern_spiral_gather$qv
org (19faeh - MAIN03_BASE)
@exalice_pattern_spiral_gather$qv label near
public @exalice_pattern_final_fan$qv
org (1a0fch - MAIN03_BASE)
@exalice_pattern_final_fan$qv label near
public @exalice_hittest_shots$qv
org (1a1dbh - MAIN03_BASE)
@exalice_hittest_shots$qv label far
public @EXALICE_PHASE_NEXT$Q16EXPLOSION_TYPE_TI
org (1a1fch - MAIN03_BASE)
@EXALICE_PHASE_NEXT$Q16EXPLOSION_TYPE_TI label near
org (UNIT_START - MAIN03_BASE)
X_UPDATE_MAIN03_CONTEXT ends
BOSS_TEXT segment byte public 'CODE' use16
BOSS_TEXT ends
EXALICE_PHASE_TEXT segment byte public 'CODE' use16
EXALICE_PHASE_TEXT ends
EXALICE_PAT_TEXT segment byte public 'CODE' use16
EXALICE_PAT_TEXT ends
EXALICE_LAT_TEXT segment byte public 'CODE' use16
EXALICE_LAT_TEXT ends
EXALICE_LSR_TEXT segment byte public 'CODE' use16
EXALICE_LSR_TEXT ends
EXALICE_FIN_TEXT segment byte public 'CODE' use16
EXALICE_FIN_TEXT ends
LASER_SC_TEXT segment byte public 'CODE' use16
LASER_SC_TEXT ends
EXALICE_UPD_TEXT segment byte public 'CODE' use16
EXALICE_UPD_TEXT ends
X_UPDATE_MAIN03_TAIL segment byte public 'CODE' use16
assume cs:X_UPDATE_MAIN03_TAIL
public @cheetos_update$qv
org (1a8cdh - AFTER_BASE)
@cheetos_update$qv label near
public @HUD_HP_UPDATE_AND_RENDER$QII
org (1c4f6h - AFTER_BASE)
@HUD_HP_UPDATE_AND_RENDER$QII label near
public @BOSS_SCORE_BONUS$QUI
org (1c5b8h - AFTER_BASE)
@BOSS_SCORE_BONUS$QUI label near
public @boss_hittest_shots_invincible$qv
org (1fafah - AFTER_BASE)
@boss_hittest_shots_invincible$qv label near
public @BOSS_DEFEAT_UPDATE$QUI
org (1fbb1h - AFTER_BASE)
@BOSS_DEFEAT_UPDATE$QUI label near
org (DGROUP_BASE - AFTER_BASE)
X_UPDATE_MAIN03_TAIL ends
main_03 group X_UPDATE_MAIN03_CONTEXT, BOSS_TEXT, EXALICE_PHASE_TEXT, EXALICE_PAT_TEXT, EXALICE_LAT_TEXT, EXALICE_LSR_TEXT, EXALICE_FIN_TEXT, LASER_SC_TEXT, EXALICE_UPD_TEXT, X_UPDATE_MAIN03_TAIL
_DATA segment word public 'DATA' use16
public _boss_flystep_random_clamp
org 01436h
_boss_flystep_random_clamp label byte
public _exalice_patterns_by_phase
org 0199ch
_exalice_patterns_by_phase label word
public _bullet_zap_drop_point_items
org 01a5ch
_bullet_zap_drop_point_items label byte
public _Palettes
org 0264ah
_Palettes label byte
public _bg_render_bombing_func
org 0350ah
_bg_render_bombing_func label word
public _boss_sprite_left
org 0371ah
_boss_sprite_left label word
public _boss_sprite_right
org 0371ch
_boss_sprite_right label word
public _boss_sprite_stay
org 0371eh
_boss_sprite_stay label word
public _homing_target
org 03f8ah
_homing_target label byte
public _exalice_bomb_invincibility
org 04a8eh
_exalice_bomb_invincibility label byte
public _exalice_backdrop_patnum
org 04a9ch
_exalice_backdrop_patnum label word
public _exalice_pattern
org 04a9eh
_exalice_pattern label word
public _palette_changed
org 0576dh
_palette_changed label byte
public _bullet_template
org 0577eh
_bullet_template label byte
public _laser_template
org 05a8ch
_laser_template label byte
public _boss
org 05abah
_boss label byte
public _gather_template
org 09ea6h
_gather_template label byte
public _custom_entities
org 0b3f4h
_custom_entities label byte
public _pellet_bottom_col
org 0c33eh
_pellet_bottom_col label word
public _boss_custombullets_render
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
