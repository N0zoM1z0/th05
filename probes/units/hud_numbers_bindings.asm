; Symbol-only real frames; no buffer values, divisor data or foreign bodies.
.386
.model large
_TEXT segment word public 'CODE' use16
assume cs:_TEXT
public GAIJI_PUTSA
org 01dbeh
GAIJI_PUTSA label far
org 0ae10h
_TEXT ends
FOREIGN_HUD_NUMBERS_MAIN01 segment word public 'CODE' use16
org (014ab0h - 0ae10h)
FOREIGN_HUD_NUMBERS_MAIN01 ends
main_01 group FOREIGN_HUD_NUMBERS_MAIN01
SHARED segment para public 'CODE' use16
org (015270h - 014ab0h)
SHARED ends
MAIN_03_TEXT segment word public 'CODE' use16
org (0158aah - 015270h)
MAIN_03_TEXT ends
FOREIGN_HUD_NUMBERS_TAIL segment byte public 'CODE' use16
org (0209d0h - 015914h)
FOREIGN_HUD_NUMBERS_TAIL ends
main_03 group MAIN_03_TEXT, FOREIGN_HUD_NUMBERS_TAIL
_DATA segment word public 'DATA' use16
public _SEVEN_DIGIT_POWERS_OF_10, _hud_gaiji_row
org 01406h
_SEVEN_DIGIT_POWERS_OF_10 label dword
org 0142ch
_hud_gaiji_row label byte
org 0c4c8h
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end
