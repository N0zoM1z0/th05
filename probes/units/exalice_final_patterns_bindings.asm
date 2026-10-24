; Real symbols and outside holes for all four complete809-byte patterns.
.386
.model large
MAIN01_BASE equ 0ae10h
SHARED_BASE equ 14ab0h
MAIN03_BASE equ 15270h
UNIT_START equ 19eb2h
AFTER_BASE equ 1a1dbh
DGROUP_BASE equ 209d0h
_TEXT segment word public 'CODE' use16
org MAIN01_BASE
_TEXT ends
X_FINAL_MAIN01_SPACE segment byte public 'CODE' use16
org (SHARED_BASE - MAIN01_BASE)
X_FINAL_MAIN01_SPACE ends
main_01 group X_FINAL_MAIN01_SPACE
SHARED segment byte public 'CODE' use16
assume cs:SHARED
public SND_SE_PLAY, @POLAR$QIII
org 0232h
SND_SE_PLAY label far
org 0394h
@POLAR$QIII label far
org (MAIN03_BASE - SHARED_BASE)
SHARED ends
EXALICE_PAT_TEXT segment byte public 'CODE' use16
assume cs:EXALICE_PAT_TEXT
public @randring2_next16$qv, @BOSS_FLYSTEP_RANDOM$QI
public @gather_add_only$qv, @GATHER_ADD_ONLY_3STACK$QIUIUI
public @PLAYER_ANGLE_FROM$Q20%SUBPIXELBASE$TI$TI%T1UC
public _bullets_add_regular, _bullets_add_regular_fixedspeed
org (1529ch - MAIN03_BASE)
@randring2_next16$qv label near
org (15914h - MAIN03_BASE)
@BOSS_FLYSTEP_RANDOM$QI label near
org (16ff5h - MAIN03_BASE)
@gather_add_only$qv label near
org (1705dh - MAIN03_BASE)
@GATHER_ADD_ONLY_3STACK$QIUIUI label near
org (171cch - MAIN03_BASE)
@PLAYER_ANGLE_FROM$Q20%SUBPIXELBASE$TI$TI%T1UC label near
org (17204h - MAIN03_BASE)
_bullets_add_regular label near
org (17236h - MAIN03_BASE)
_bullets_add_regular_fixedspeed label near
org (UNIT_START - MAIN03_BASE)
EXALICE_PAT_TEXT ends
EXALICE_FIN_TEXT segment byte public 'CODE' use16
EXALICE_FIN_TEXT ends
X_FINAL_MAIN03_TAIL segment byte public 'CODE' use16
assume cs:X_FINAL_MAIN03_TAIL
public @cheetos_add$qv
org (1a82eh - AFTER_BASE)
@cheetos_add$qv label near
org (DGROUP_BASE - AFTER_BASE)
X_FINAL_MAIN03_TAIL ends
main_03 group EXALICE_PAT_TEXT, EXALICE_FIN_TEXT, X_FINAL_MAIN03_TAIL
_DATA segment word public 'DATA' use16
public _SinTable8, _exalice_sweep_x, _player_pos, _bullet_template, _boss
public _gather_template, _custom_entities, _boss_statebyte
org 041ch
_SinTable8 label word
org 199ah
_exalice_sweep_x label word
org 36d2h
_player_pos label byte
org 577eh
_bullet_template label byte
org 5abah
_boss label byte
org 9ea6h
_gather_template label byte
org 0b3f4h
_custom_entities label byte
org 0c682h
_boss_statebyte label byte
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end
