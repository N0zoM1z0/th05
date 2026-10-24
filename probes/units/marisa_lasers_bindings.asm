; Address-only context; no owned instructions, objects or in-scope padding.
.386
.model large
_TEXT segment word public 'CODE' use16
assume cs:_TEXT
public GRCG_CIRCLEFILL, GRCG_BOXFILL, PALETTE_SHOW
org 00ea6h
GRCG_BOXFILL label far
org 0100eh
GRCG_CIRCLEFILL label far
org 02158h
PALETTE_SHOW label far
org 0ae10h
_TEXT ends
MARISA_LASERS_TEXT segment byte public 'CODE' use16
assume cs:MARISA_LASERS_TEXT
public @grcg_setmode_rmw$qv, @grcg_setcolor_direct_raw$qv
org (0c1f8h - 0ae10h)
@grcg_setmode_rmw$qv label near
org (0c204h - 0ae10h)
@grcg_setcolor_direct_raw$qv label near
org (0fe2ch - 0ae10h)
MARISA_LASERS_TEXT ends
MARISA_LASERS_TAIL segment byte public 'CODE' use16
org (14ab0h - 0ff7bh)
MARISA_LASERS_TAIL ends
main_01 group MARISA_LASERS_TEXT, MARISA_LASERS_TAIL
SHARED segment byte public 'CODE' use16
assume cs:SHARED
public SND_SE_PLAY
org 0232h
SND_SE_PLAY label far
org (15270h - 14ab0h)
SHARED ends
MAIN_BOMB_SPARKS segment byte public 'CODE' use16
assume cs:MAIN_BOMB_SPARKS
public @bomb_sparks_add_at_player$qv
org 02448h
@bomb_sparks_add_at_player$qv label far
org (209d0h - 15270h)
MAIN_BOMB_SPARKS ends
main_03 group MAIN_BOMB_SPARKS
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
