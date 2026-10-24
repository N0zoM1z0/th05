; Address-only foreign context for the full63-byte final-phase spread.
.386
.model large
MAIN01_BASE equ 0ae10h
SHARED_BASE equ 14ab0h
MAIN03_BASE equ 15270h
UNIT_START equ 1e957h
AFTER_BASE equ 1e9a0h
DGROUP_BASE equ 209d0h
_TEXT segment word public 'CODE' use16
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
assume cs:B4_UPDATE_TEXT
public _bullets_add_regular
org (17204h - MAIN03_BASE)
_bullets_add_regular label near
org (UNIT_START - MAIN03_BASE)
B4_UPDATE_TEXT ends
ALICE_FS_TEXT segment byte public 'CODE' use16
ALICE_FS_TEXT ends
ALICE_FS_AFTER_TEXT segment para public 'CODE' use16
org (DGROUP_BASE - AFTER_BASE)
ALICE_FS_AFTER_TEXT ends
main_03 group B4_UPDATE_TEXT, ALICE_FS_TEXT, ALICE_FS_AFTER_TEXT
_DATA segment word public 'DATA' use16
public _bullet_template_tune, _bullet_template, _boss
org 41deh
_bullet_template_tune label word
org 577eh
_bullet_template label byte
org 5abah
_boss label byte
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end
