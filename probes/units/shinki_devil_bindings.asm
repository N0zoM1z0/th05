; Genuine foreign-only context for the complete 802-byte devil pattern.
; No own-function labels, game bytes, artificial prefix or .stack.
.386
.model large
_TEXT segment word public 'CODE' use16
org 0ae10h
_TEXT ends
MAIN_0_TEXT segment byte public 'CODE' use16
assume cs:MAIN_0_TEXT
public SELECT_FOR_RANK
org 021a2h
SELECT_FOR_RANK label far
org 09ca0h
MAIN_0_TEXT ends
BOSS_BG_TEXT segment byte public 'CODE' use16
BOSS_BG_TEXT ends
main_01 group MAIN_0_TEXT, BOSS_BG_TEXT
SHARED segment para public 'CODE' use16
assume cs:SHARED
public SND_SE_PLAY
org 0232h
SND_SE_PLAY label far
org 07c0h
SHARED ends
BULLET_A_TEXT segment byte public 'CODE' use16
BULLET_A_TEXT ends
LASER_SC_TEXT segment byte public 'CODE' use16
assume cs:LASER_SC_TEXT
public @RANDRING2_NEXT16_MOD$QUI
org 050h
@RANDRING2_NEXT16_MOD$QUI label near
public @PLAYER_ANGLE_FROM$Q20%SUBPIXELBASE$TI$TI%T1UC
org 01f5ch
@PLAYER_ANGLE_FROM$Q20%SUBPIXELBASE$TI$TI%T1UC label near
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
public @b6balls_add$qv
org 0580eh
@b6balls_add$qv label near
org (1b244h - 15270h)
LASER_SC_TEXT ends
B6_BALLS_TEXT segment byte public 'CODE' use16
B6_BALLS_TEXT ends
B6_PATTERN_A_TEXT segment byte public 'CODE' use16
B6_PATTERN_A_TEXT ends
B6_UPDATE_TEXT segment byte public 'CODE' use16
B6_UPDATE_TEXT ends
B6_DEVIL_TEXT segment byte public 'CODE' use16
B6_DEVIL_TEXT ends
DEVIL_MAIN03_TAIL segment byte public 'CODE' use16
org (209d0h - 1b566h)
DEVIL_MAIN03_TAIL ends
main_03 group BULLET_A_TEXT, LASER_SC_TEXT, B6_BALLS_TEXT, B6_PATTERN_A_TEXT, B6_UPDATE_TEXT, B6_DEVIL_TEXT, DEVIL_MAIN03_TAIL
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
