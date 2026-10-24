; TH05 Shinki original-address symbol-only context.
; No helperbodies, callbacktable values, gameplay state or .stack.
.386
.model large
MAIN01_BASE equ 0ae10h
SHARED_BASE equ 14ab0h
SHARED_END equ (SHARED_BASE + 03b0h)
MAIN03_BASE equ 15270h
UNIT_START equ 1aa7eh
BALLS_CODE_SIZE equ 0129h ; observed natural81+216, not original301
FOREIGN_BALLS_REMAINDER equ 4 ; outside accepted complete-function scopes
PATTERN_A_START equ 1ababh
PATTERN_A_CODE_SIZE equ 010fh
SUFFIX_START equ 1acbah
SUFFIX_CODE_SIZE equ 0de0h
UNIT_END equ (SUFFIX_START + SUFFIX_CODE_SIZE)
DGROUP_BASE equ 209d0h

_TEXT segment word public 'CODE' use16
assume cs:_TEXT
public SUPER_CONVERT_TINY
org 035a2h
SUPER_CONVERT_TINY label far
org MAIN01_BASE
_TEXT ends

MAIN_0_TEXT segment byte public 'CODE' use16
assume cs:MAIN_0_TEXT
public @SELECT_FOR_PLAYCHAR$QIIII
org 0219ch
@SELECT_FOR_PLAYCHAR$QIIII label far
public SELECT_FOR_RANK
org 021a2h
SELECT_FOR_RANK label far
public @SHINKI_BG_RENDER$QV
org 06601h
@SHINKI_BG_RENDER$QV label near
public @SHINKI_CUSTOMBULLETS_RENDER$QV
org 081e5h
@SHINKI_CUSTOMBULLETS_RENDER$QV label near
MAIN_0_TEXT ends
BOSS_BG_TEXT segment byte public 'CODE' use16
BOSS_BG_TEXT ends
SHINKI_MAIN01_TAIL segment byte public 'CODE' use16
org (SHARED_BASE - (MAIN01_BASE + 081e5h))
SHINKI_MAIN01_TAIL ends
main_01 group MAIN_0_TEXT, BOSS_BG_TEXT, SHINKI_MAIN01_TAIL

SHINKI_SHARED_TEXT segment para public 'CODE' use16
assume cs:SHINKI_SHARED_TEXT
public SND_SE_PLAY
org 0232h
SND_SE_PLAY label far
public VECTOR2_AT
org 03b0h
VECTOR2_AT label far
SHINKI_SHARED_TEXT ends
SHINKI_SHARED_TAIL segment byte public 'CODE' use16
org (MAIN03_BASE - SHARED_END)
SHINKI_SHARED_TAIL ends

BULLET_A_TEXT segment byte public 'CODE' use16
BULLET_A_TEXT ends
LASER_SC_TEXT segment byte public 'CODE' use16
assume cs:LASER_SC_TEXT
public @PlayfieldMotion@update_seg3$qv
org 0ch
@PlayfieldMotion@update_seg3$qv label near
public @randring2_next16$qv
org 02ch
@randring2_next16$qv label near
public @RANDRING2_NEXT16_AND$QUI
org 03ah
@RANDRING2_NEXT16_AND$QUI label near
public @RANDRING2_NEXT16_MOD$QUI
org 050h
@RANDRING2_NEXT16_MOD$QUI label near
public VECTOR2_NEAR
org 06ah
VECTOR2_NEAR label near
public @BOSS_FLYSTEP_RANDOM$QI
org 06a4h
@BOSS_FLYSTEP_RANDOM$QI label near
public @BOSS_FLYSTEP_TOWARDS$QII
org 0797h
@BOSS_FLYSTEP_TOWARDS$QII label near
public @GATHER_ADD_ONLY_3STACK$QIUIUI
org 01dedh
@GATHER_ADD_ONLY_3STACK$QIUIUI label near
public @PLAYER_ANGLE_FROM$Q20%SUBPIXELBASE$TI$TI%T1UC
org 01f5ch
@PLAYER_ANGLE_FROM$Q20%SUBPIXELBASE$TI$TI%T1UC label near
public @playperf_speedtune
org 01f7ah
@playperf_speedtune label near
public _bullets_add_regular
org 01f94h
_bullets_add_regular label near
public _bullets_add_special
org 01fa8h
_bullets_add_special label near
public _bullets_add_regular_fixedspeed
org 01fc6h
_bullets_add_regular_fixedspeed label near
public @BOSS_EXPLODE_SMALL$Q16EXPLOSION_TYPE_T
org 0246dh
@BOSS_EXPLODE_SMALL$Q16EXPLOSION_TYPE_T label near
public @LASER_MANUAL_FIXED_SPAWN$QI
org 054dbh
@LASER_MANUAL_FIXED_SPAWN$QI label near
public @LASER_MANUAL_GROW$QI
org 05535h
@LASER_MANUAL_GROW$QI label near
public @LASER_STOP$QI
org 0555eh
@LASER_STOP$QI label near
public @cheetos_add$qv
org 055beh
@cheetos_add$qv label near
public @cheetos_update$qv
org 0565dh
@cheetos_update$qv label near
org (UNIT_START - MAIN03_BASE)
LASER_SC_TEXT ends
B6_BALLS_TEXT segment byte public 'CODE' use16
B6_BALLS_TEXT ends

; Entire original b6balls_update remains unaccepted. This four-byte external
; extent bridges the observed natural216-byte body to its original220-byte
; boundary. It is neither source padding nor authored code; no bytes supplied.
SHINKI_BALLS_FOREIGN_REMAINDER segment byte public 'CODE' use16
org FOREIGN_BALLS_REMAINDER
SHINKI_BALLS_FOREIGN_REMAINDER ends

; Two complete pattern functions end at the genuine even boundary1ACBA.
B6_PATTERN_A_TEXT segment byte public 'CODE' use16
B6_PATTERN_A_TEXT ends

B6_UPDATE_TEXT segment byte public 'CODE' use16
B6_UPDATE_TEXT ends

SHINKI_MAIN03_TAIL segment byte public 'CODE' use16
assume cs:SHINKI_MAIN03_TAIL
public @HUD_HP_UPDATE_AND_RENDER$QII
org (MAIN03_BASE + 07286h - UNIT_END)
@HUD_HP_UPDATE_AND_RENDER$QII label near
public @BOSS_SCORE_BONUS$QUI
org (MAIN03_BASE + 07348h - UNIT_END)
@BOSS_SCORE_BONUS$QUI label near
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
SHINKI_MAIN03_TAIL ends
main_03 group BULLET_A_TEXT, LASER_SC_TEXT, B6_BALLS_TEXT, SHINKI_BALLS_FOREIGN_REMAINDER, B6_PATTERN_A_TEXT, B6_UPDATE_TEXT, SHINKI_MAIN03_TAIL

_DATA segment word public 'DATA' use16
public _PaletteTone
org 03dah
_PaletteTone label word
public _SHINKI_PATTERNS_PHASE_2_3
org 01a50h
_SHINKI_PATTERNS_PHASE_2_3 label byte
public _shinki_devil_laser_grow_delay
org 01a58h
_shinki_devil_laser_grow_delay label word
public _shinki_float_direction
org 01a5ah
_shinki_float_direction label byte
public _Palettes
org 0264ah
_Palettes label byte
public _bg_render_bombing_func
org 0350ah
_bg_render_bombing_func label word
public _playfield_shake_anim_time
org 03520h
_playfield_shake_anim_time label word
public _player_pos
org 036d2h
_player_pos label byte
public _player_is_hit
org 036f3h
_player_is_hit label byte
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
public _bullet_zap
org 03f96h
_bullet_zap label byte
public _bullet_clear_time
org 03f97h
_bullet_clear_time label byte
public _bullet_template_tune
org 041deh
_bullet_template_tune label word
public _bombing
org 04206h
_bombing label byte
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
public _palette_changed
org 0576dh
_palette_changed label byte
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
public _custom_entities
org 0b3f4h
_custom_entities label byte
public _shinki_phase_2_3_pattern
org 0c33ah
_shinki_phase_2_3_pattern label word
public _shinki_wing_pattern
org 0c33ch
_shinki_wing_pattern label word
public _boss_custombullets_render
org 0c678h
_boss_custombullets_render label word
public _boss_statebyte
org 0c682h
_boss_statebyte label byte
public _boss_hitbox_radius
org 0c694h
_boss_hitbox_radius label byte
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end
