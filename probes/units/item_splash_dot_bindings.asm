; Actual MAIN main_01 CS AE10 and DS 209D0, foreign CODE holes only.
.386
.model large
_TEXT segment word public 'CODE' use16
org 0AE10h
_TEXT ends
ITEM_SPLASH_DOT_PREFIX segment byte public 'CODE' use16
org (0E152h - 0AE10h)
ITEM_SPLASH_DOT_PREFIX ends
ITEM_SPLASH_DOT_TEXT segment byte public 'CODE' use16
ITEM_SPLASH_DOT_TEXT ends
ITEM_SPLASH_DOT_TAIL segment byte public 'CODE' use16
org (014AB0h - 0E16Eh)
ITEM_SPLASH_DOT_TAIL ends
main_01 group ITEM_SPLASH_DOT_PREFIX, ITEM_SPLASH_DOT_TEXT, ITEM_SPLASH_DOT_TAIL
SHARED segment para public 'CODE' use16
org (0209D0h - 014AB0h)
SHARED ends
_DATA segment word public 'DATA' use16
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end
