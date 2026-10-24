; Original-address symbols only for main-scroll-convert. No bodies, values or .stack.
.386
.model large
MAIN01_BASE equ 0ae10h
SHARED_BASE equ 14ab0h
MAIN03_BASE equ 15270h
DGROUP_BASE equ 209d0h
UNIT_START equ 016a30h
UNIT_SIZE equ 049h
UNIT_END equ (UNIT_START + UNIT_SIZE)
_TEXT segment word public 'CODE' use16
org MAIN01_BASE
_TEXT ends
SMALL_MAIN01_CONTEXT segment byte public 'CODE' use16
SMALL_MAIN01_CONTEXT ends
SMALL_MAIN01_SPACE segment byte public 'CODE' use16
assume cs:SMALL_MAIN01_SPACE
org (SHARED_BASE - MAIN01_BASE)
SMALL_MAIN01_SPACE ends
main_01 group SMALL_MAIN01_CONTEXT, SMALL_MAIN01_SPACE
SMALL_SHARED_SPACE segment para public 'CODE' use16
org (MAIN03_BASE - SHARED_BASE)
SMALL_SHARED_SPACE ends
SCROLLY3_TEXT segment byte public 'CODE' use16
org (UNIT_START - MAIN03_BASE)
SCROLLY3_TEXT ends
SMALL_MAIN03_TAIL segment byte public 'CODE' use16
org (DGROUP_BASE - UNIT_END)
SMALL_MAIN03_TAIL ends
main_03 group SCROLLY3_TEXT, SMALL_MAIN03_TAIL
_DATA segment word public 'DATA' use16
public _scroll_line
org 03516h
_scroll_line label word
public _scroll_active
org 0351ah
_scroll_active label byte
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end
