; Symbol-only context; every origin hole is outside compiled C++ code.
.386
.model large
.stack 80h
_TEXT segment word public 'CODE' use16
assume cs:_TEXT
public SUPER_ROLL_PUT_1PLANE, SUPER_ROLL_PUT
org 02e1ah
SUPER_ROLL_PUT_1PLANE label far
org 02fe0h
SUPER_ROLL_PUT label far
org 0ae10h
_TEXT ends
MAIN__TEXT segment word public 'CODE' use16
assume cs:MAIN__TEXT
public SCROLL_SUBPIXEL_Y_TO_VRAM_SEG1
org 03118h
SCROLL_SUBPIXEL_Y_TO_VRAM_SEG1 label near
org 03140h
MAIN__TEXT ends
HUD_OVRL_TEXT segment word public 'CODE' use16
HUD_OVRL_TEXT ends
main_01 group MAIN__TEXT, HUD_OVRL_TEXT
; The complete source ends at E01F. Separate holes anchor real DGROUP at209D.
ENEMY_RENDER_GAP_A segment byte public 'CODE' use16
org 0f000h
ENEMY_RENDER_GAP_A ends
ENEMY_RENDER_GAP_B segment byte public 'CODE' use16
org 039b1h
ENEMY_RENDER_GAP_B ends
_DATA segment word public 'DATA' use16
public _enemies
org 093fah
_enemies label byte
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end
