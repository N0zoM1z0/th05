; Source owns only the complete MAINE score filename/text DATA declarations.
.386
.model large
_TEXT segment word public 'CODE' use16
org 0a540h
_TEXT ends
SCORE_RESOURCE_TEXT segment byte public 'CODE' use16
org (0e800h - 0a540h)
SCORE_RESOURCE_TEXT ends
group_01 group SCORE_RESOURCE_TEXT
SHARED segment para public 'CODE' use16
org (10110h - 0e800h)
SHARED ends
_DATA segment word public 'DATA' use16
org 01524h
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end
