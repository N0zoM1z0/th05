; Valid native CODE and DATA frame layout, no instruction/data payload.
.386
.model large
_TEXT segment word public 'CODE' use16
org 0AE10h
_TEXT ends
MIMA_BOMB_PRIM_PREFIX segment byte public 'CODE' use16
org (01045Ch - 0AE10h)
MIMA_BOMB_PRIM_PREFIX ends
MIMA_BOMB_PRIM_TEXT segment byte public 'CODE' use16
MIMA_BOMB_PRIM_TEXT ends
MIMA_BOMB_PRIM_TAIL segment byte public 'CODE' use16
org (014AB0h - 010508h)
MIMA_BOMB_PRIM_TAIL ends
main_01 group MIMA_BOMB_PRIM_PREFIX, MIMA_BOMB_PRIM_TEXT, MIMA_BOMB_PRIM_TAIL
SHARED segment para public 'CODE' use16
org (0209D0h - 014AB0h)
SHARED ends
_DATA segment word public 'DATA' use16
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end
