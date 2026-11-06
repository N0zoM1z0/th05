; Outside-only native frames, including the foreign inter-entry alignment.
.386
.model large
_TEXT segment word public 'CODE' use16
org 0ae10h
_TEXT ends
NULL_NEAR_TEXT segment byte public 'CODE' use16
org (0c73eh - 0ae10h)
NULL_NEAR_TEXT ends
NULL_FAR_TEXT segment byte public 'CODE' use16
org 1
NULL_FAR_TEXT ends
FOREIGN_NULL_TAIL segment byte public 'CODE' use16
org (014ab0h - 0c741h)
FOREIGN_NULL_TAIL ends
main_01 group NULL_NEAR_TEXT, NULL_FAR_TEXT, FOREIGN_NULL_TAIL
SHARED segment para public 'CODE' use16
org (0209d0h - 014ab0h)
SHARED ends
_DATA segment word public 'DATA' use16
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end
