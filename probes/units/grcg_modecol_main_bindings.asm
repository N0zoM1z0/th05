.386
.model large
_TEXT segment word public 'CODE' use16
org 0AE10h
_TEXT ends
GRCG_MODECOL_PREFIX segment byte public 'CODE' use16
org (0C1F8h - 0AE10h)
GRCG_MODECOL_PREFIX ends
GRCG_MODECOL_TEXT segment byte public 'CODE' use16
GRCG_MODECOL_TEXT ends
GRCG_MODECOL_TAIL segment byte public 'CODE' use16
org (014AB0h - 0C21Eh)
GRCG_MODECOL_TAIL ends
main_01 group GRCG_MODECOL_PREFIX, GRCG_MODECOL_TEXT, GRCG_MODECOL_TAIL
SHARED segment para public 'CODE' use16
org (0209D0h - 014AB0h)
SHARED ends
_DATA segment word public 'DATA' use16
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end
