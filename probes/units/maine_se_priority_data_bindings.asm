; Original code frames and outside DATA prefix only. No values or bodies.
.386
.model large
_TEXT segment word public 'CODE' use16
org 0a540h
_TEXT ends
SE_PRIORITY_DATA_TEXT segment byte public 'CODE' use16
org (0e800h - 0a540h)
SE_PRIORITY_DATA_TEXT ends
group_01 group SE_PRIORITY_DATA_TEXT
SHARED segment para public 'CODE' use16
org (010110h - 0e800h)
SHARED ends
_DATA segment word public 'DATA' use16
org 065eh
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end
