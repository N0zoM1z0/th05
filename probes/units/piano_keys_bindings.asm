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
org 00730h
SHARED ends
FOREIGN_SHARED_TAIL segment byte public 'CODE' use16
assume cs:FOREIGN_SHARED_TAIL
public PIANO_KEY_PRESSED_TOP
org 00000h
PIANO_KEY_PRESSED_TOP label byte
public @grcg_setcolor_direct_raw$qv
org 00020h
@grcg_setcolor_direct_raw$qv label near
org 014dfh
FOREIGN_SHARED_TAIL ends
_DATA segment word public 'DATA' use16
public _PIANO_KEYS_BLACK
org 009eeh
_PIANO_KEYS_BLACK label byte
org 03e96h
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end
