; Foreign frames and complete score records only, without initialized payload.
.386
.model large
_TEXT segment word public 'CODE' use16
org 0a390h
_TEXT ends
SCORE_DECODE_PREFIX segment byte public 'CODE' use16
org (0c7d5h - 0a390h)
SCORE_DECODE_PREFIX ends
SCORE_TEXT segment byte public 'CODE' use16
SCORE_TEXT ends
SCORE_DECODE_TAIL segment byte public 'CODE' use16
org (0d300h - 0c87eh)
SCORE_DECODE_TAIL ends
op_01 group SCORE_DECODE_PREFIX, SCORE_TEXT, SCORE_DECODE_TAIL
SHARED segment para public 'CODE' use16
org (0efe0h - 0d300h)
SHARED ends
_DATA segment word public 'DATA' use16
public _hi, _hi2
org 05060h
_hi label byte
org 050c0h
_hi2 label byte
org 05120h
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end
