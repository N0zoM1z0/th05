; Address-only original context for the complete natural Stage3 prefix.
; No function bodies, initialized global values or inside-contribution holes.
.386
.model large
MAIN01_BASE equ 0ae10h
SHARED_BASE equ 14ab0h
MAIN03_BASE equ 15270h
UNIT_START equ 1ba9ah
AFTER_BASE equ 1bd10h
DGROUP_BASE equ 209d0h

_TEXT segment word public 'CODE' use16
org MAIN01_BASE
_TEXT ends
MIDBOSS3_PAT_MAIN01_CONTEXT segment byte public 'CODE' use16
assume cs:MIDBOSS3_PAT_MAIN01_CONTEXT
public SELECT_FOR_RANK
org 021a2h
SELECT_FOR_RANK label far
org (SHARED_BASE - MAIN01_BASE)
MIDBOSS3_PAT_MAIN01_CONTEXT ends
main_01 group MIDBOSS3_PAT_MAIN01_CONTEXT
SHARED segment byte public 'CODE' use16
assume cs:SHARED
public SND_SE_PLAY
org 0232h
SND_SE_PLAY label far
org (MAIN03_BASE - SHARED_BASE)
SHARED ends

B4_UPDATE_TEXT segment byte public 'CODE' use16
assume cs:B4_UPDATE_TEXT
public @GATHER_ADD_ONLY_3STACK$QIUIUI
public _bullets_add_regular
org (1705dh - MAIN03_BASE)
@GATHER_ADD_ONLY_3STACK$QIUIUI label near
org (17204h - MAIN03_BASE)
_bullets_add_regular label near
org (UNIT_START - MAIN03_BASE)
B4_UPDATE_TEXT ends

; Complete original source ends1BD02. This separate paragraph begins1BD10,
; outside all five functions. The real source size is never supplied here.
MB3_PAT_AFTER_TEXT segment para public 'CODE' use16
org (DGROUP_BASE - AFTER_BASE)
MB3_PAT_AFTER_TEXT ends
main_03 group B4_UPDATE_TEXT, MB3_PAT_AFTER_TEXT

_DATA segment word public 'DATA' use16
public _player_pos, _bullet_template_tune, _bullet_template
public _midboss, _boss_statebyte
org 36d2h
_player_pos label byte
org 41deh
_bullet_template_tune label word
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
