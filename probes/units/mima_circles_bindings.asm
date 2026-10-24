; Address-only context; no owned instructions, objects or in-scope padding.
.386
.model large
_TEXT segment word public 'CODE' use16
assume cs:_TEXT
public GRCG_CIRCLEFILL
org 0100eh
GRCG_CIRCLEFILL label far
org 0ae10h
_TEXT ends
MIMA_CIRCLES_TEXT segment byte public 'CODE' use16
assume cs:MIMA_CIRCLES_TEXT
public @randring1_next16$qv
org (0c700h - 0ae10h)
@randring1_next16$qv label near
org (10058h - 0ae10h)
MIMA_CIRCLES_TEXT ends
MIMA_CIRCLES_TAIL segment byte public 'CODE' use16
org (14ab0h - 1010dh)
MIMA_CIRCLES_TAIL ends
main_01 group MIMA_CIRCLES_TEXT, MIMA_CIRCLES_TAIL
SHARED segment byte public 'CODE' use16
assume cs:SHARED
public VECTOR2_AT
org 03b0h
VECTOR2_AT label far
org (209d0h - 14ab0h)
SHARED ends
_DATA segment word public 'DATA' use16
public _PaletteTone, _player_pos, _bomb_frame, _bomb_anim, _palette_changed
org 03dah
_PaletteTone label word
org 036d2h
_player_pos label byte
org 04207h
_bomb_frame label byte
org 0420eh
_bomb_anim label byte
org 0576dh
_palette_changed label byte
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end
