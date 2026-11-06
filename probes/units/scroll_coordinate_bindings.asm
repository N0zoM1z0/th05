; Foreign native frames and scroll words only, without initialized payload.
.386
.model large
_TEXT segment word public 'CODE' use16
org 0ae10h
_TEXT ends
SCROLL_COORDINATE_TEXT segment word public 'CODE' use16
org (0df28h - 0ae10h)
SCROLL_COORDINATE_TEXT ends
SMALL_MAIN01_CONTEXT segment byte public 'CODE' use16
SMALL_MAIN01_CONTEXT ends
FOREIGN_SCROLL_COORDINATE_TAIL segment byte public 'CODE' use16
org (014ab0h - 0df50h)
FOREIGN_SCROLL_COORDINATE_TAIL ends
main_01 group SCROLL_COORDINATE_TEXT, SMALL_MAIN01_CONTEXT, FOREIGN_SCROLL_COORDINATE_TAIL
SHARED segment para public 'CODE' use16
org (015270h - 014ab0h)
SHARED ends
FOREIGN_SCROLL_COORDINATE_MAIN03 segment word public 'CODE' use16
org (0209d0h - 015270h)
FOREIGN_SCROLL_COORDINATE_MAIN03 ends
main_03 group FOREIGN_SCROLL_COORDINATE_MAIN03
_DATA segment word public 'DATA' use16
public _scroll_line, _scroll_active
org 03516h
_scroll_line label word
org 0351ah
_scroll_active label byte
org 0351bh
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end
