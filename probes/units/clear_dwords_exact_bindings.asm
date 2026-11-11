; Original MAIN01 code location and true DGROUP, foreign-only reservation.
.386
.model large
_TEXT segment word public 'CODE' use16
org 0AE10h
_TEXT ends
CLEAR_DWORDS_PREFIX segment byte public 'CODE' use16
org (0CF62h - 0AE10h)
CLEAR_DWORDS_PREFIX ends
CLEAR_DWORDS_TEXT segment byte public 'CODE' use16
CLEAR_DWORDS_TEXT ends
CLEAR_DWORDS_TAIL segment byte public 'CODE' use16
org (014AB0h - 0CF79h)
CLEAR_DWORDS_TAIL ends
main_01 group CLEAR_DWORDS_PREFIX,CLEAR_DWORDS_TEXT,CLEAR_DWORDS_TAIL
SHARED segment para public 'CODE' use16
org (0209D0h - 014AB0h)
SHARED ends
_DATA segment word public 'DATA' use16
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA,_BSS
end
