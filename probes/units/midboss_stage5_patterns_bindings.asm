; Symbol-only original context for the five natural stage-five prefix functions.
; All code in the source slot comes from C++; no owned DATA or inside holes.
.386
.model large
MAIN01_BASE equ 0ae10h
SHARED_BASE equ 14ab0h
MAIN03_BASE equ 15270h
UNIT_START equ 16724h
AFTER_BASE equ 16900h
DGROUP_BASE equ 209d0h

_TEXT segment word public 'CODE' use16
org MAIN01_BASE
_TEXT ends
MB5_PAT_MAIN01_CONTEXT segment byte public 'CODE' use16
org (SHARED_BASE - MAIN01_BASE)
MB5_PAT_MAIN01_CONTEXT ends
main_01 group MB5_PAT_MAIN01_CONTEXT
SHARED segment byte public 'CODE' use16
assume cs:SHARED
public SND_SE_PLAY
org 0232h
SND_SE_PLAY label far
org (MAIN03_BASE - SHARED_BASE)
SHARED ends

MAIN_036_TEXT segment byte public 'CODE' use16
assume cs:MAIN_036_TEXT
public @PlayfieldMotion@update_seg3$qv, @randring2_next16$qv
public @RANDRING2_NEXT16_MOD$QUI
org (1527ch - MAIN03_BASE)
@PlayfieldMotion@update_seg3$qv label near
org (1529ch - MAIN03_BASE)
@randring2_next16$qv label near
org (152c0h - MAIN03_BASE)
@RANDRING2_NEXT16_MOD$QUI label near
org (UNIT_START - MAIN03_BASE)
MAIN_036_TEXT ends

; Separate paragraph context after the complete natural462-byte contribution.
; Actual original end168F2 rounds to16900 outside all five functions.
MB5_PAT_AFTER_TEXT segment para public 'CODE' use16
assume cs:MB5_PAT_AFTER_TEXT
public @GATHER_ADD_ONLY_3STACK$QIUIUI
public @PLAYER_ANGLE_FROM$Q20%SUBPIXELBASE$TI$TI%T1UC
public _bullets_add_regular
org (1705dh - AFTER_BASE)
@GATHER_ADD_ONLY_3STACK$QIUIUI label near
org (171cch - AFTER_BASE)
@PLAYER_ANGLE_FROM$Q20%SUBPIXELBASE$TI$TI%T1UC label near
org (17204h - AFTER_BASE)
_bullets_add_regular label near
org (DGROUP_BASE - AFTER_BASE)
MB5_PAT_AFTER_TEXT ends
main_03 group MAIN_036_TEXT, MB5_PAT_AFTER_TEXT

_DATA segment word public 'DATA' use16
public _MIDBOSS5_PATTERNS, _midboss5_pattern_func
public _bullet_template, _midboss, _boss_statebyte
org 1490h
_MIDBOSS5_PATTERNS label word
org 3788h
_midboss5_pattern_func label word
org 577eh
_bullet_template label byte
org 5aa4h
_midboss label byte
org 0c682h
_boss_statebyte label byte
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end
