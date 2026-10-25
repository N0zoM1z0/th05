; Symbol-only original code/data context. No foreign instructions or values.
.386
.model large
_TEXT segment word public 'CODE' use16
assume cs:_TEXT
public GAIJI_PUTSA
org 01dbeh
GAIJI_PUTSA label far
org 0ae10h
_TEXT ends
MAIN_01_TEXT segment word public 'CODE' use16
org (0d474h - 0ae10h)
MAIN_01_TEXT ends
FOREIGN_HUD_BAR_TAIL segment byte public 'CODE' use16
org (014ab0h - 0d4c0h)
FOREIGN_HUD_BAR_TAIL ends
main_01 group MAIN_01_TEXT, FOREIGN_HUD_BAR_TAIL
SHARED segment para public 'CODE' use16
org (015270h - 014ab0h)
SHARED ends
FOREIGN_HUD_BAR_MAIN03 segment word public 'CODE' use16
org (0209d0h - 015270h)
FOREIGN_HUD_BAR_MAIN03 ends
main_03 group FOREIGN_HUD_BAR_MAIN03
_DATA segment word public 'DATA' use16
public _hud_gaiji_row
org 0142ch
_hud_gaiji_row label byte
org 0c4c8h
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end
