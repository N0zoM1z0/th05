; Foreign filename, mask bank and segment frames only; no initialized payload.
.386
.model large
_TEXT segment word public 'CODE' use16
org 0ae10h
_TEXT ends
BB_LOAD_TEXT segment byte public 'CODE' use16
BB_LOAD_TEXT ends
BB_CHEETO_LOAD_TEXT segment byte public 'CODE' use16
org (0de58h - 0ae10h)
BB_CHEETO_LOAD_TEXT ends
BB_CHEETO_TAIL segment byte public 'CODE' use16
org (014ab0h - 0de71h)
BB_CHEETO_TAIL ends
main_01 group BB_LOAD_TEXT, BB_CHEETO_LOAD_TEXT, BB_CHEETO_TAIL
SHARED segment para public 'CODE' use16
org (0209d0h - 014ab0h)
SHARED ends
_DATA segment word public 'DATA' use16
public _bb_cheeto_fn
org 0149bh
_bb_cheeto_fn label byte
public _bb_cheeto
org 0378ah
_bb_cheeto label byte
org (0378ah + 2048)
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end
