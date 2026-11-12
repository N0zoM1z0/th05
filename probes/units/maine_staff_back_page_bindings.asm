; Authentic MAINE group_01 / SHARED original CODE frames and DATA prefix only.
.386
.model large
_TEXT segment word public 'CODE' use16
org 0a540h
_TEXT ends
STAFF_1_STATE_TEXT segment byte public 'CODE' use16
org (0e800h - 0a540h)
STAFF_1_STATE_TEXT ends
group_01 group STAFF_1_STATE_TEXT
SHARED segment para public 'CODE' use16
org (10110h - 0e800h)
SHARED ends
_DATA segment word public 'DATA' use16
org 173ah
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end
