; Only foreign native frames and the complete ring/cursor, without payload.
.386
.model large
_TEXT segment word public 'CODE' use16
org 0ae10h
_TEXT ends
FOREIGN_RING2_MAIN01 segment byte public 'CODE' use16
org (014ab0h - 0ae10h)
FOREIGN_RING2_MAIN01 ends
main_01 group FOREIGN_RING2_MAIN01
SHARED segment para public 'CODE' use16
org (015270h - 014ab0h)
SHARED ends
RANDRING_2_TEXT segment word public 'CODE' use16
org (01529ch - 015270h)
RANDRING_2_TEXT ends
FOREIGN_RING2_TAIL segment byte public 'CODE' use16
org (0209d0h - 0152d9h)
FOREIGN_RING2_TAIL ends
main_03 group RANDRING_2_TEXT, FOREIGN_RING2_TAIL
_DATA segment word public 'DATA' use16
public _randring, _randring_p
org 03526h
_randring label byte
org 03626h
_randring_p label word
org 03628h
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end
