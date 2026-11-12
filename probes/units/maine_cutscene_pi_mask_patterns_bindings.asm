; Foreign MAINE frames and outside DATA prefix only; no PI mask payload.
.386
.model large
_TEXT segment word public 'CODE' use16
org 0a540h
_TEXT ends
CUTSCENE_PI_MASK_DATA_TEXT segment byte public 'CODE' use16
org (0e800h - 0a540h)
CUTSCENE_PI_MASK_DATA_TEXT ends
group_01 group CUTSCENE_PI_MASK_DATA_TEXT
SHARED segment para public 'CODE' use16
org (10110h - 0e800h)
SHARED ends
_DATA segment word public 'DATA' use16
org 006deh
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end
