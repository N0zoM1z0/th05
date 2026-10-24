; Symbol-only real context for the entire161-byte yumeko foreground callback.
; No instructions, ownedbytes, DATA values or stack allocation.
.386
.model large
UNIT_START equ 14422h
UNIT_END equ 144c3h
_TEXT segment word public 'CODE' use16
assume cs:_TEXT
public SUPER_LARGE_PUT, SUPER_PUT_1PLANE, SUPER_PUT_RECT, SUPER_PUT, SUPER_PUT_8
org 02048h
SUPER_LARGE_PUT label far
org 02adah
SUPER_PUT_1PLANE label far
org 031fch
SUPER_PUT_RECT label far
org 033f0h
SUPER_PUT label far
org 040e6h
SUPER_PUT_8 label far
org 0ae10h
_TEXT ends
SHINKI_FG_TEXT segment byte public 'CODE' use16
SHINKI_FG_TEXT ends
LATE_FG_CONTEXT segment byte public 'CODE' use16
assume cs:LATE_FG_CONTEXT
public @explosions_small_update_and_rend$qv, @explosions_big_update_and_render$qv
org (1060eh - 0ae10h)
@explosions_small_update_and_rend$qv label near
org (106d8h - 0ae10h)
@explosions_big_update_and_render$qv label near
org (UNIT_START - 0ae10h)
LATE_FG_CONTEXT ends
YUMEKO_FG_TEXT segment byte public 'CODE' use16
YUMEKO_FG_TEXT ends
LATE_FG_TAIL segment byte public 'CODE' use16
org (14ab0h - UNIT_END)
LATE_FG_TAIL ends
main_01 group SHINKI_FG_TEXT, LATE_FG_CONTEXT, YUMEKO_FG_TEXT, LATE_FG_TAIL
SHARED segment byte public 'CODE' use16
org 07c0h
SHARED ends
LATE_FG_MAIN03_SPACE segment byte public 'CODE' use16
org (209d0h - 15270h)
LATE_FG_MAIN03_SPACE ends
main_03 group LATE_FG_MAIN03_SPACE
_DATA segment word public 'DATA' use16
public _stage_frame_mod16, _boss, _boss2
org 05769h
_stage_frame_mod16 label byte
org 05abah
_boss label byte
org 05ad2h
_boss2 label byte
org 05aeah
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end
