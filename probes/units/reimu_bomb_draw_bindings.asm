; Address-only context for the complete84-byte Reimu bomb drawing callback.
.386
.model large
MAIN01_BASE equ 0ae10h
UNIT_START equ 0fd17h
UNIT_END equ 0fd6bh
SHARED_BASE equ 14ab0h
DGROUP_BASE equ 209d0h
_TEXT segment word public 'CODE' use16
org MAIN01_BASE
_TEXT ends
REIMU_DRAW_TEXT segment byte public 'CODE' use16
assume cs:REIMU_DRAW_TEXT
public @reimu_stars_update_and_render$qv
org (0fb44h - MAIN01_BASE)
@reimu_stars_update_and_render$qv label near
org (UNIT_START - MAIN01_BASE)
REIMU_DRAW_TEXT ends
REIMU_DRAW_AFTER_TEXT segment byte public 'CODE' use16
assume cs:REIMU_DRAW_AFTER_TEXT
public @reimu_bomb_backdrop_render$qv
org (1049eh - UNIT_END)
@reimu_bomb_backdrop_render$qv label near
org (SHARED_BASE - UNIT_END)
REIMU_DRAW_AFTER_TEXT ends
main_01 group REIMU_DRAW_TEXT, REIMU_DRAW_AFTER_TEXT
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
public _PaletteTone, _circles_color, _bomb_frame, _stage_frame_mod4, _palette_changed
org 03dah
_PaletteTone label word
org 41dah
_circles_color label byte
org 4207h
_bomb_frame label byte
org 5767h
_stage_frame_mod4 label byte
org 576dh
_palette_changed label byte
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end
