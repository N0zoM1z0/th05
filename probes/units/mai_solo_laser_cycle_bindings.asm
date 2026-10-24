; Genuine state/code context for the distinct461-byte Mai laser-cycle provider.
; No callbacks, tables, initial values or instructions supplied as owned code.
.386
.model large
_TEXT segment word public 'CODE' use16
org 0ae10h
_TEXT ends
YUKI_SOLO_RENDER_TEXT segment byte public 'CODE' use16
YUKI_SOLO_RENDER_TEXT ends
MAI_CYCLE_MAIN01_SPACE segment byte public 'CODE' use16
org 09ca0h
MAI_CYCLE_MAIN01_SPACE ends
main_01 group YUKI_SOLO_RENDER_TEXT, MAI_CYCLE_MAIN01_SPACE
SHARED segment byte public 'CODE' use16
org 07c0h
SHARED ends
MAI_ADV_TEXT segment byte public 'CODE' use16
MAI_ADV_TEXT ends
MAIN_035_TEXT segment byte public 'CODE' use16
assume cs:MAIN_035_TEXT
public @randring2_next16$qv, @RANDRING2_NEXT16_AND$QUI
public @BOSS_FLYSTEP_RANDOM$QI, @mai_solo_rotating_fans$qv
org 002ch
@randring2_next16$qv label near
org 003ah
@RANDRING2_NEXT16_AND$QUI label near
org (15914h - 15270h)
@BOSS_FLYSTEP_RANDOM$QI label near
org (18ea9h - 15270h)
@mai_solo_rotating_fans$qv label near
org (1935eh - 15270h)
MAIN_035_TEXT ends
LASER_SC_TEXT segment byte public 'CODE' use16
assume cs:LASER_SC_TEXT
public @LASER_MANUAL_FIXED_SPAWN$QI, @LASER_MANUAL_GROW$QI
org (1a74bh - 1952bh)
@LASER_MANUAL_FIXED_SPAWN$QI label near
org (1a7a5h - 1952bh)
@LASER_MANUAL_GROW$QI label near
org (209d0h - 1952bh)
LASER_SC_TEXT ends
main_03 group MAI_ADV_TEXT, MAIN_035_TEXT, LASER_SC_TEXT
_DATA segment word public 'DATA' use16
public _mai_solo_laser_patterns, _mai_solo_laser_count, _mai_solo_laser_speed
public _mai_solo_laser_fraction, _mai_solo_laser_pattern
public _stage_frame_mod2, _rank, _lasers, _laser_template, _boss, _boss_statebyte
org 1976h
_mai_solo_laser_patterns label word
org 4432h
_mai_solo_laser_count label word
org 4434h
_mai_solo_laser_speed label word
org 4436h
_mai_solo_laser_fraction label word
org 443ah
_mai_solo_laser_pattern label word
org 5766h
_stage_frame_mod2 label byte
org 576fh
_rank label byte
org 578ch
_lasers label byte
org 5a8ch
_laser_template label byte
org 5abah
_boss label byte
org 0c682h
_boss_statebyte label byte
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end
