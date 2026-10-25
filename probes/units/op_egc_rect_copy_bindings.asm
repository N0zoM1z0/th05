; Actual foreign frames and provider addresses only; no initialized payload.
.386
.model large
_TEXT segment word public 'CODE' use16
assume cs:_TEXT
public EGC_OFF
org 0082ch
EGC_OFF label far
org 0a390h
_TEXT ends
FOREIGN_MAIN segment byte public 'CODE' use16
org 02f70h
FOREIGN_MAIN ends
SHARED segment para public 'CODE' use16
org 00fd8h
SHARED ends
FOREIGN_SHARED_TAIL segment byte public 'CODE' use16
assume cs:FOREIGN_SHARED_TAIL
public EGC_RECT_SETUP
EGC_RECT_SETUP label near
org 00c8ch
FOREIGN_SHARED_TAIL ends
_DATA segment word public 'DATA' use16
public _egcrect_w
org 03f1eh
_egcrect_w label word
org 03f20h
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end
