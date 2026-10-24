; Symbol-only true foreign frames around three complete EX-Alice functions.
.386
.model large
MAIN01_BASE equ 0ae10h
SHARED_BASE equ 14ab0h
MAIN03_BASE equ 15270h
UNIT_START equ 1989bh
AFTER_BASE equ 199e0h
DGROUP_BASE equ 209d0h
_TEXT segment word public 'CODE' use16
org MAIN01_BASE
_TEXT ends
HUD_OVRL_TEXT segment byte public 'CODE' use16
HUD_OVRL_TEXT ends
X_MAIN01_SPACE segment byte public 'CODE' use16
org (SHARED_BASE - MAIN01_BASE)
X_MAIN01_SPACE ends
main_01 group HUD_OVRL_TEXT, X_MAIN01_SPACE
SHARED segment byte public 'CODE' use16
assume cs:SHARED
public SND_SE_PLAY
org 0232h
SND_SE_PLAY label far
org (MAIN03_BASE - SHARED_BASE)
SHARED ends
X_MAIN03_CONTEXT segment byte public 'CODE' use16
assume cs:X_MAIN03_CONTEXT
public @RANDRING2_NEXT16_AND$QUI, @BOSS_FLYSTEP_RANDOM$QI
public @GATHER_ADD_ONLY_3STACK$QIUIUI
public _bullets_add_regular, _bullets_add_special
org (152aah - MAIN03_BASE)
@RANDRING2_NEXT16_AND$QUI label near
org (15914h - MAIN03_BASE)
@BOSS_FLYSTEP_RANDOM$QI label near
org (1705dh - MAIN03_BASE)
@GATHER_ADD_ONLY_3STACK$QIUIUI label near
org (17204h - MAIN03_BASE)
_bullets_add_regular label near
org (17218h - MAIN03_BASE)
_bullets_add_special label near
org (UNIT_START - MAIN03_BASE)
X_MAIN03_CONTEXT ends
EXALICE_PAT_TEXT segment byte public 'CODE' use16
EXALICE_PAT_TEXT ends
X_MAIN03_TAIL segment para public 'CODE' use16
org (DGROUP_BASE - AFTER_BASE)
X_MAIN03_TAIL ends
main_03 group X_MAIN03_CONTEXT, EXALICE_PAT_TEXT, X_MAIN03_TAIL
_DATA segment word public 'DATA' use16
public _bullet_special, _exalice_pattern, _bullet_template, _boss, _boss_statebyte
org 3f94h
_bullet_special label byte
org 4a9eh
_exalice_pattern label word
org 577eh
_bullet_template label byte
org 5abah
_boss label byte
org 0c682h
_boss_statebyte label byte
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end
