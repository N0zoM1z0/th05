; Original MAIN ring-fill function, real vendor provider and foreign state.
.386
.model large
_TEXT segment word public 'CODE' use16
assume cs:_TEXT
public IRAND
org 023c6h
IRAND label far
org 0ae10h
_TEXT ends
RANDRING_FILL_TEXT segment byte public 'CODE' use16
org (0c6e8h - 0ae10h)
RANDRING_FILL_TEXT ends
RANDRING_FILL_MAIN01_TAIL segment byte public 'CODE' use16
org (14ab0h - 0c700h)
RANDRING_FILL_MAIN01_TAIL ends
main_01 group RANDRING_FILL_TEXT, RANDRING_FILL_MAIN01_TAIL
SHARED segment para public 'CODE' use16
org (209d0h - 14ab0h)
SHARED ends
_DATA segment word public 'DATA' use16
public _randring, _randring_p
org 03526h
_randring label byte
org 03626h
_randring_p label word
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end
