; Address-only context for the complete three-pattern Alice contribution.
; Empty foreign compiler segments retain the actual containing group frame.
.386
.model large
MAIN01_BASE equ 0ae10h
SHARED_BASE equ 14ab0h
MAIN03_BASE equ 15270h
UNIT_START equ 1e764h
AFTER_BASE equ 1e960h
DGROUP_BASE equ 209d0h

_TEXT segment word public 'CODE' use16
assume cs:_TEXT
public IATAN2
org 01f3ah
IATAN2 label far
org MAIN01_BASE
_TEXT ends

MAIN_01_TEXT segment byte public 'CODE' use16
org (SHARED_BASE - MAIN01_BASE)
MAIN_01_TEXT ends
main_01 group MAIN_01_TEXT

SHARED segment byte public 'CODE' use16
assume cs:SHARED
public SND_SE_PLAY
org 0232h
SND_SE_PLAY label far
org (MAIN03_BASE - SHARED_BASE)
SHARED ends

B4_UPDATE_TEXT segment byte public 'CODE' use16
B4_UPDATE_TEXT ends

LASER_SC_TEXT segment byte public 'CODE' use16
assume cs:LASER_SC_TEXT
public @GATHER_ADD_ONLY_3STACK$QIUIUI
public _bullets_add_regular
public @lasers_shootout_add$qv
org (1705dh - MAIN03_BASE)
@GATHER_ADD_ONLY_3STACK$QIUIUI label near
org (17204h - MAIN03_BASE)
_bullets_add_regular label near
org (1a66eh - MAIN03_BASE)
@lasers_shootout_add$qv label near
org (UNIT_START - MAIN03_BASE)
LASER_SC_TEXT ends

ALICE_CHG_TEXT segment byte public 'CODE' use16
ALICE_CHG_TEXT ends
ALICE_CHG_AFTER_TEXT segment para public 'CODE' use16
org (DGROUP_BASE - AFTER_BASE)
ALICE_CHG_AFTER_TEXT ends
main_03 group B4_UPDATE_TEXT, LASER_SC_TEXT, ALICE_CHG_TEXT, ALICE_CHG_AFTER_TEXT

_DATA segment word public 'DATA' use16
public _player_pos, _bullet_template_tune, _bullet_template
public _laser_template, _boss, _boss_statebyte
org 36d2h
_player_pos label byte
org 41deh
_bullet_template_tune label word
org 577eh
_bullet_template label byte
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
