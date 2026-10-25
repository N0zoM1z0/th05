; Real foreign providers/state only; no instructions or inside-owner holes.
.386
.model large
MAIN01_BASE equ 0AE10h
SHARED_BASE equ 14AB0h
MAIN03_BASE equ 15270h
UNIT_START equ 177F0h
UNIT_SIZE equ 06Fh
UNIT_END equ (UNIT_START + UNIT_SIZE)
DGROUP_BASE equ 209D0h

_TEXT segment word public 'CODE' use16
org MAIN01_BASE
_TEXT ends

SHOT_HIT_TEXT segment byte public 'CODE' use16
assume cs:SHOT_HIT_TEXT
public @shots_hittest$qv
org (13683h - MAIN01_BASE)
@shots_hittest$qv label far
org (SHARED_BASE - MAIN01_BASE)
SHOT_HIT_TEXT ends
main_01 group SHOT_HIT_TEXT

SHARED segment byte public 'CODE' use16
assume cs:SHARED
public SND_SE_PLAY
org 0232h
SND_SE_PLAY label far
org (MAIN03_BASE - SHARED_BASE)
SHARED ends

MAIN_035_TEXT segment byte public 'CODE' use16
org (UNIT_START - MAIN03_BASE)
MAIN_035_TEXT ends

BOSS_TEXT segment byte public 'CODE' use16
assume cs:BOSS_TEXT
public @boss_hittest_shots$qv
org (1FAD0h - UNIT_END)
@boss_hittest_shots$qv label near
org (DGROUP_BASE - UNIT_END)
BOSS_TEXT ends
main_03 group MAIN_035_TEXT, BOSS_TEXT

_DATA segment word public 'DATA' use16
public _shots_hittest_against_boss
org 01DC0h
_shots_hittest_against_boss label byte
public _boss2
org 05AD2h
_boss2 label byte
public _shot_hitbox_center
org 0C4C0h
_shot_hitbox_center label dword
public _shot_hitbox_radius
org 0C4C4h
_shot_hitbox_radius label dword
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end
