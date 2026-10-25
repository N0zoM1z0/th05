; Original group context and foreign providers only, with no payload or stack.
.386
.model large
main_01 group MAIN_01_TEXT, FOREIGN_POINTNUM_RENDER_TAIL
_TEXT segment word public 'CODE' use16
org 0ae10h
_TEXT ends
MAIN_01_TEXT segment word public 'CODE' use16
assume cs:main_01
public @pointnum_put, SCROLL_SUBPIXEL_Y_TO_VRAM_SEG1
org (0be3ah - 0ae10h)
@pointnum_put label near
org (0df28h - 0ae10h)
SCROLL_SUBPIXEL_Y_TO_VRAM_SEG1 label near
org (0e216h - 0ae10h)
MAIN_01_TEXT ends
FOREIGN_POINTNUM_RENDER_TAIL segment byte public 'CODE' use16
org (014ab0h - 0e28ah)
FOREIGN_POINTNUM_RENDER_TAIL ends
SHARED segment para public 'CODE' use16
org (015270h - 014ab0h)
SHARED ends
FOREIGN_POINTNUM_RENDER_MAIN03 segment word public 'CODE' use16
org (0209d0h - 015270h)
FOREIGN_POINTNUM_RENDER_MAIN03 ends
main_03 group FOREIGN_POINTNUM_RENDER_MAIN03
_DATA segment word public 'DATA' use16
public _pointnums_alive, _pointnum_first_yellow_alive
org 03fa6h
_pointnums_alive label word
org 041d8h
_pointnum_first_yellow_alive label word
org 0c4c8h
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end
