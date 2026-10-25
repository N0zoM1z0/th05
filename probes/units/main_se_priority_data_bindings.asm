; Original code frames and outside DATA prefix only. No values or bodies.
.386
.model large
_TEXT segment word public 'CODE' use16
org 0ae10h
_TEXT ends
SE_PRIORITY_DATA_TEXT segment byte public 'CODE' use16
org (014ab0h - 0ae10h)
SE_PRIORITY_DATA_TEXT ends
main_01 group SE_PRIORITY_DATA_TEXT
SHARED segment para public 'CODE' use16
org (0209d0h - 014ab0h)
SHARED ends
_DATA segment word public 'DATA' use16
org 0800h
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end
