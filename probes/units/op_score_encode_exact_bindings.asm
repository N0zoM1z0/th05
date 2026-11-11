.386
.model large
_TEXT segment word public 'CODE' use16
assume cs:_TEXT
public IRAND
org 01C5Eh
IRAND label far
org 0A390h
_TEXT ends
ENC_PREFIX segment byte public 'CODE' use16
org (0C87Eh-0A390h)
ENC_PREFIX ends
SCORE_ENCODE_TEXT segment byte public 'CODE' use16
SCORE_ENCODE_TEXT ends
ENC_TAIL segment byte public 'CODE' use16
org (0D300h-0C8E2h)
ENC_TAIL ends
op_01 group ENC_PREFIX,SCORE_ENCODE_TEXT,ENC_TAIL
SHARED segment para public 'CODE' use16
org (0EFE0h-0D300h)
SHARED ends
_DATA segment word public 'DATA' use16
public _hi
org 05060h
_hi label byte
org 05137h
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA,_BSS
end
