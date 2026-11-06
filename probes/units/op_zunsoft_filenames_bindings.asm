; Actual empty CODE frames and DATA prefix; all six strings are compiler-owned.
.386
.model large
_TEXT segment word public 'CODE' use16
org 0a390h
_TEXT ends
ZUNSOFT_DATA_TEXT segment byte public 'CODE' use16
ZUNSOFT_DATA_TEXT ends
ZUNSOFT_DATA_TAIL segment byte public 'CODE' use16
org (0d300h - 0a390h)
ZUNSOFT_DATA_TAIL ends
op_01 group ZUNSOFT_DATA_TEXT, ZUNSOFT_DATA_TAIL
SHARED segment para public 'CODE' use16
org (0efe0h - 0d300h)
SHARED ends
_DATA segment word public 'DATA' use16
org 0eeah
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end
