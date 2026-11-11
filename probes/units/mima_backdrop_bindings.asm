; Address-only native symbols, never source instructions or game state values.
.386
.model large
_TEXT segment word public 'CODE' use16
org 0ae10h
_TEXT ends
MIMA_BANDS_TEXT segment byte public 'CODE' use16
assume cs:MIMA_BANDS_TEXT
public mima_bomb_bands_fill
org (010508h - 0ae10h)
mima_bomb_bands_fill label near
org (01052ch - 0ae10h)
MIMA_BANDS_TEXT ends
MIMA_BACKDROP_TEXT segment byte public 'CODE' use16
MIMA_BACKDROP_TEXT ends
MIMA_BACKDROP_TAIL segment byte public 'CODE' use16
org (014ab0h - 01060eh)
MIMA_BACKDROP_TAIL ends
main_01 group MIMA_BANDS_TEXT, MIMA_BACKDROP_TEXT, MIMA_BACKDROP_TAIL
SHARED segment para public 'CODE' use16
org (0209d0h - 014ab0h)
SHARED ends
_DATA segment word public 'DATA' use16
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end
