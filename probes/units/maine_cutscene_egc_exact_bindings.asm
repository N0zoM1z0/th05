.386
.model large
_TEXT segment word public 'CODE' use16
assume cs:_TEXT
public EGC_ON
org 00824h
EGC_ON label far
org 0A540h
_TEXT ends
CUTSCENE_EGC_PREFIX segment byte public 'CODE' use16
org (0A6D1h-0A540h)
CUTSCENE_EGC_PREFIX ends
CUTSCENE_EGC_TEXT segment byte public 'CODE' use16
CUTSCENE_EGC_TEXT ends
CUTSCENE_EGC_TAIL segment byte public 'CODE' use16
org (0E800h-0A705h)
CUTSCENE_EGC_TAIL ends
group_01 group CUTSCENE_EGC_PREFIX,CUTSCENE_EGC_TEXT,CUTSCENE_EGC_TAIL
SHARED segment para public 'CODE' use16
org (010110h-0E800h)
SHARED ends
_DATA segment word public 'DATA' use16
org 02E88h
_DATA ends
_BSS segment word public 'BSS' use16
org 02086h
_BSS ends
DGROUP group _DATA,_BSS
end
