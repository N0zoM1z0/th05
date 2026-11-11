.386
.model large
_TEXT segment word public 'CODE' use16
org 0ae10h
_TEXT ends
EGC_SETUP_PREFIX segment byte public 'CODE' use16
org (0bc2eh - 0ae10h)
EGC_SETUP_PREFIX ends
EGC_SETUP_TEXT segment byte public 'CODE' use16
EGC_SETUP_TEXT ends
EGC_SETUP_TAIL segment byte public 'CODE' use16
org (014ab0h - 0bc6dh)
EGC_SETUP_TAIL ends
main_01 group EGC_SETUP_PREFIX, EGC_SETUP_TEXT, EGC_SETUP_TAIL
SHARED segment para public 'CODE' use16
org (0209d0h - 014ab0h)
SHARED ends
_DATA segment word public 'DATA' use16
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end
