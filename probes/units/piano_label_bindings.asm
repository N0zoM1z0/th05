; Real foreign frames and external symbols only; no initialized payload.
.386
.model large
_TEXT segment word public 'CODE' use16
org 0a390h
_TEXT ends
FOREIGN_MAIN segment byte public 'CODE' use16
org (0d300h-0a390h)
FOREIGN_MAIN ends
SHARED segment para public 'CODE' use16
org 0080dh
SHARED ends
FOREIGN_SHARED_TAIL segment byte public 'CODE' use16
assume cs:FOREIGN_SHARED_TAIL
org 014bfh
FOREIGN_SHARED_TAIL ends
_DATA segment word public 'DATA' use16
public _sPIANO_LABEL_FONT
org 00a0ah
_sPIANO_LABEL_FONT label byte
org 03e96h
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end
