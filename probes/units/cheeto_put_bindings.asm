; Native frames and foreign bank extent only; no initialized payload or stack.
.386
.model large
_TEXT segment word public 'CODE' use16
org 0ae10h
_TEXT ends
MAIN_01_TEXT segment word public 'CODE' use16
org (0de72h - 0ae10h)
MAIN_01_TEXT ends
FOREIGN_CHEETO_TAIL segment byte public 'CODE' use16
org (014ab0h - 0df28h)
FOREIGN_CHEETO_TAIL ends
main_01 group MAIN_01_TEXT, FOREIGN_CHEETO_TAIL
SHARED segment para public 'CODE' use16
org (015270h - 014ab0h)
SHARED ends
FOREIGN_CHEETO_MAIN03 segment word public 'CODE' use16
org (0209d0h - 015270h)
FOREIGN_CHEETO_MAIN03 ends
main_03 group FOREIGN_CHEETO_MAIN03
_DATA segment word public 'DATA' use16
public _bb_cheeto
org 0378ah
_bb_cheeto label byte
org (0378ah + 2048)
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end
