; Original code frames and outside DATA prefix only. No values or bodies.
.386
.model large
_TEXT segment word public 'CODE' use16
org 0a540h
_TEXT ends
REG_CURSOR_INIT_TEXT segment byte public 'CODE' use16
org (0e800h - 0a540h)
REG_CURSOR_INIT_TEXT ends
group_01 group REG_CURSOR_INIT_TEXT
SHARED segment para public 'CODE' use16
org (010110h - 0e800h)
SHARED ends
_DATA segment word public 'DATA' use16
org 01521h
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end
