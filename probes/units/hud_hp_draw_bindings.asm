; Outside-only original frame/symbol context. No owned instructions or values.
.386
.model large
_TEXT segment word public 'CODE' use16
assume cs:_TEXT
public GAIJI_PUTSA
org 01dbeh
GAIJI_PUTSA label far
org 0ae10h
_TEXT ends
HP_DRAW_PREFIX segment byte public 'CODE' use16
org (0d28bh - 0ae10h)
HP_DRAW_PREFIX ends
HUD_HP_DRAW_TEXT segment byte public 'CODE' use16
HUD_HP_DRAW_TEXT ends
HUD_HP_BAR_API_TEXT segment byte public 'CODE' use16
assume cs:HUD_HP_BAR_API_TEXT
public HUD_BAR_PUT
org (0d474h - 0d323h)
HUD_BAR_PUT label near
org (014ab0h - 0d323h)
HUD_HP_BAR_API_TEXT ends
main_01 group HP_DRAW_PREFIX, HUD_HP_DRAW_TEXT, HUD_HP_BAR_API_TEXT
HP_DRAW_SHARED_SPACE segment byte public 'CODE' use16
org 07c0h
HP_DRAW_SHARED_SPACE ends
HP_DRAW_MAIN03_SPACE segment byte public 'CODE' use16
org 0b760h
HP_DRAW_MAIN03_SPACE ends
main_03 group HP_DRAW_MAIN03_SPACE
_DATA segment word public 'DATA' use16
public _gsENEMY
org 013c4h
_gsENEMY label byte
public _gHUD_HP_BLANK
org 013e2h
_gHUD_HP_BLANK label byte
public _HUD_HP_COLORS
org 013ebh
_HUD_HP_COLORS label byte
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end
