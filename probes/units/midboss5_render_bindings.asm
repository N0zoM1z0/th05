; Only original stage5 owner DD8F, not the stagex twin DD2A.
; External addresses only, no bodies/state/stack.
.386
.model large
_TEXT segment word public 'CODE' use16
assume cs:_TEXT
public SUPER_ROLL_PUT_1PLANE
org 02e1ah
SUPER_ROLL_PUT_1PLANE label far
public SUPER_ROLL_PUT
org 02fe0h
SUPER_ROLL_PUT label far
org 0ae10h
_TEXT ends
M5_RENDER_TEXT segment byte public 'CODE' use16
org 02f7fh
M5_RENDER_TEXT ends
M5_RENDER_MAIN01_TAIL segment byte public 'CODE' use16
assume cs:M5_RENDER_MAIN01_TAIL
public SCROLL_SUBPIXEL_Y_TO_VRAM_SEG1
org 0134h
SCROLL_SUBPIXEL_Y_TO_VRAM_SEG1 label near
public @midboss_defeat_render$qv
org 054dfh
@midboss_defeat_render$qv label near
org 06cbch
M5_RENDER_MAIN01_TAIL ends
main_01 group M5_RENDER_TEXT, M5_RENDER_MAIN01_TAIL
M5_RENDER_SHARED segment para public 'CODE' use16
org 07c0h
M5_RENDER_SHARED ends
M5_RENDER_MAIN03 segment byte public 'CODE' use16
org 0b760h
M5_RENDER_MAIN03 ends
main_03 group M5_RENDER_MAIN03
_DATA segment word public 'DATA' use16
public _midboss
org 05aa4h
_midboss label byte
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end
