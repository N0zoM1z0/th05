; Original code frames and outside DATA prefix only. No values or bodies.
.386
.model large
_TEXT segment word public 'CODE' use16
org 0ae10h
_TEXT ends
LOAD_PLAYCHAR_INIT_TEXT segment byte public 'CODE' use16
org (014ab0h - 0ae10h)
LOAD_PLAYCHAR_INIT_TEXT ends
main_01 group LOAD_PLAYCHAR_INIT_TEXT
SHARED segment para public 'CODE' use16
org (0209d0h - 014ab0h)
SHARED ends
_DATA segment word public 'DATA' use16
org 00a0h
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end
