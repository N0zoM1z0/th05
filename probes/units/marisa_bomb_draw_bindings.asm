; Symbol-only context around the complete sixty-byte Marisa drawing callback.
.386
.model large
_TEXT segment word public 'CODE' use16
org 0ae10h
_TEXT ends
MARISA_DRAW_TEXT segment byte public 'CODE' use16
assume cs:MARISA_DRAW_TEXT
public @marisa_lasers_update_and_render$qv
org (0fe2ch - 0ae10h)
@marisa_lasers_update_and_render$qv label near
org (0ff7bh - 0ae10h)
MARISA_DRAW_TEXT ends
MARISA_DRAW_AFTER_TEXT segment byte public 'CODE' use16
assume cs:MARISA_DRAW_AFTER_TEXT
public @marisa_bomb_backdrop_render$qv
org (104ceh - 0ffb7h)
@marisa_bomb_backdrop_render$qv label near
org (14ab0h - 0ffb7h)
MARISA_DRAW_AFTER_TEXT ends
main_01 group MARISA_DRAW_TEXT, MARISA_DRAW_AFTER_TEXT
SHARED segment byte public 'CODE' use16
assume cs:SHARED
public CDG_PUT_NOALPHA_8
org 01c0h
CDG_PUT_NOALPHA_8 label far
org (209d0h - 14ab0h)
SHARED ends
_DATA segment word public 'DATA' use16
public _PaletteTone, _shot_time, _bomb_frame, _palette_changed
org 03dah
_PaletteTone label word
org 036f2h
_shot_time label byte
org 04207h
_bomb_frame label byte
org 0576dh
_palette_changed label byte
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end
