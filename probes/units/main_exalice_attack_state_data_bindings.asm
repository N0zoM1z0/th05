; Only foreign CODE frames and original DS:1998 initialized-DATA origin.
; No initialized DATA values, code bodies or target-derived bytes are emitted.
.386
.model large
_TEXT segment word public 'CODE' use16
org 0ae10h
_TEXT ends
EXALICE_ATTACK_STATE_TEXT segment byte public 'CODE' use16
org (14ab0h - 0ae10h)
EXALICE_ATTACK_STATE_TEXT ends
main_01 group EXALICE_ATTACK_STATE_TEXT
SHARED segment para public 'CODE' use16
org (15270h - 14ab0h)
SHARED ends
EXALICE_MAIN03_FOREIGN segment byte public 'CODE' use16
org (209d0h - 15270h)
EXALICE_MAIN03_FOREIGN ends
main_03 group EXALICE_MAIN03_FOREIGN
_DATA segment word public 'DATA' use16
org 01998h
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA,_BSS
end
