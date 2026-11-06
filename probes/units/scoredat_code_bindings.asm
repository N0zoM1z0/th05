; Original frames and foreign symbols only; no codec bytes, DATA or stack.
.386
.model large
_TEXT segment word public 'CODE' use16
assume cs:_TEXT
public IRAND
org 023c6h
IRAND label far
org 0ae10h
_TEXT ends
SCORE_CODE_TEXT segment word public 'CODE' use16
org (0c812h - 0ae10h)
SCORE_CODE_TEXT ends
SCORE_CODE_MAIN01_TAIL segment byte public 'CODE' use16
org (14ab0h - 0c882h)
SCORE_CODE_MAIN01_TAIL ends
main_01 group SCORE_CODE_TEXT, SCORE_CODE_MAIN01_TAIL
SHARED segment para public 'CODE' use16
org (209d0h - 14ab0h)
SHARED ends
_DATA segment word public 'DATA' use16
public _hi
org 0366eh
_hi label byte
org (0366eh + 96)
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end
