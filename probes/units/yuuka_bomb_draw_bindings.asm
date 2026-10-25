; Address-only context for the complete120-byte Yuuka bomb drawing callback.
.386
.model large
MAIN01_BASE equ 0ae10h
UNIT_START equ 102f9h
UNIT_END equ 10371h
SHARED_BASE equ 14ab0h
DGROUP_BASE equ 209d0h
_TEXT segment word public 'CODE' use16
assume cs:_TEXT
public PALETTE_SHOW
org 02158h
PALETTE_SHOW label far
org MAIN01_BASE
_TEXT ends
YUUKA_DRAW_TEXT segment byte public 'CODE' use16
assume cs:YUUKA_DRAW_TEXT
public @yuuka_heart_update_and_render$qv
org (1027bh - MAIN01_BASE)
@yuuka_heart_update_and_render$qv label near
org (UNIT_START - MAIN01_BASE)
YUUKA_DRAW_TEXT ends
YUUKA_DRAW_AFTER_TEXT segment byte public 'CODE' use16
assume cs:YUUKA_DRAW_AFTER_TEXT
public @yuuka_bomb_backdrop_render$qv
org (10596h - UNIT_END)
@yuuka_bomb_backdrop_render$qv label near
org (SHARED_BASE - UNIT_END)
YUUKA_DRAW_AFTER_TEXT ends
main_01 group YUUKA_DRAW_TEXT, YUUKA_DRAW_AFTER_TEXT
SHARED segment byte public 'CODE' use16
assume cs:SHARED
public CDG_PUT_NOALPHA_8, SND_SE_PLAY
org 01c0h
CDG_PUT_NOALPHA_8 label far
org 0232h
SND_SE_PLAY label far
org (DGROUP_BASE - SHARED_BASE)
SHARED ends
_DATA segment word public 'DATA' use16
public _PaletteTone, _circles_color, _bomb_frame, _palette_changed
org 03dah
_PaletteTone label word
org 41dah
_circles_color label byte
org 4207h
_bomb_frame label byte
org 576dh
_palette_changed label byte
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end
