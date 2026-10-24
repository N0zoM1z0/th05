; Symbol-only playfield-shake context. No target code or global values.
; Every ORG hole surrounds the complete natural 273-byte C++ contribution.
.386
.model large

MAIN01_BASE equ 0ae10h
UNIT_START equ 0c579h
UNIT_SIZE equ 0111h
UNIT_END equ (UNIT_START + UNIT_SIZE)
MAIN03_BASE equ 15270h
DGROUP_BASE equ 209d0h

_TEXT segment word public 'CODE' use16
assume cs:_TEXT
public EGC_SHIFT_DOWN, EGC_SHIFT_LEFT, EGC_SHIFT_RIGHT, EGC_SHIFT_UP
org 08aah
EGC_SHIFT_DOWN label far
org 09b0h
EGC_SHIFT_LEFT label far
org 0ab2h
EGC_SHIFT_RIGHT label far
org 0bc2h
EGC_SHIFT_UP label far
org MAIN01_BASE
_TEXT ends

PLAYFLD_TEXT segment word public 'CODE' use16
assume cs:PLAYFLD_TEXT
public @tiles_invalidate_all$qv
org (0bd38h - MAIN01_BASE)
@tiles_invalidate_all$qv label near
org (UNIT_START - MAIN01_BASE)
PLAYFLD_TEXT ends
main_01 group PLAYFLD_TEXT

; Independent outside-code extents stay below the 64-KiB segment limit.
PLAYFIELD_FOREIGN_GAP_1 segment byte public 'CODE' use16
org (MAIN03_BASE - UNIT_END)
PLAYFIELD_FOREIGN_GAP_1 ends
PLAYFIELD_FOREIGN_GAP_2 segment byte public 'CODE' use16
org (DGROUP_BASE - MAIN03_BASE)
PLAYFIELD_FOREIGN_GAP_2 ends

_DATA segment word public 'DATA' use16
public _playfield_shake_redraw_time, _scroll_line
public _playfield_shake_x, _playfield_shake_y, _playfield_shake_anim_time
public _stage_frame_mod2, _stage_frame_mod4
org 0f4ah
_playfield_shake_redraw_time label byte
org 3516h
_scroll_line label word
org 351ch
_playfield_shake_x label word
org 351eh
_playfield_shake_y label word
org 3520h
_playfield_shake_anim_time label word
org 5766h
_stage_frame_mod2 label byte
org 5767h
_stage_frame_mod4 label byte
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end
