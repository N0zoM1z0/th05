; Only foreign native frames and the complete ring/cursor, without payload.
.386
.model large
_TEXT segment word public 'CODE' use16
org 0ae10h
_TEXT ends
RANDRING_1_TEXT segment word public 'CODE' use16
org (0c700h - 0ae10h)
RANDRING_1_TEXT ends
FOREIGN_RING1_TAIL segment byte public 'CODE' use16
org (014ab0h - 0c73eh)
FOREIGN_RING1_TAIL ends
main_01 group RANDRING_1_TEXT, FOREIGN_RING1_TAIL
SHARED segment para public 'CODE' use16
org (0209d0h - 014ab0h)
SHARED ends
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
