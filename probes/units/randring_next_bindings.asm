; Original byte ring/cursor and outside-only native frames, without payload.
.386
.model large
_TEXT segment word public 'CODE' use16
org 0ae10h
_TEXT ends
RANDRING_NEXT_TEXT segment byte public 'CODE' use16
org (0c700h - 0ae10h)
RANDRING_NEXT_TEXT ends
RANDRING_NEXT_MAIN01_TAIL segment byte public 'CODE' use16
org (14ab0h - 0c70dh)
RANDRING_NEXT_MAIN01_TAIL ends
main_01 group RANDRING_NEXT_TEXT, RANDRING_NEXT_MAIN01_TAIL
SHARED segment para public 'CODE' use16
org (209d0h - 14ab0h)
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
