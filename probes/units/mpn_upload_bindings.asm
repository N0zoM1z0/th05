; Actual far helper labels and CODE frames only; no supplied instructions.
.386
.model large
_TEXT segment word public 'CODE' use16
assume cs:_TEXT
public MPN_LOAD_INNER, MPN_FREE, MPN_PUT
org 041b2h
MPN_LOAD_INNER label far
org 0420eh
MPN_FREE label far
org 04226h
MPN_PUT label far
org 0ae10h
_TEXT ends
MPN_UPLOAD_TEXT segment byte public 'CODE' use16
org (0e57ch - 0ae10h)
MPN_UPLOAD_TEXT ends
FOREIGN_MPN_UPLOAD_TAIL segment byte public 'CODE' use16
org (014ab0h - 0e5c1h)
FOREIGN_MPN_UPLOAD_TAIL ends
main_01 group MPN_UPLOAD_TEXT, FOREIGN_MPN_UPLOAD_TAIL
SHARED segment para public 'CODE' use16
org (015270h - 014ab0h)
SHARED ends
FOREIGN_MPN_UPLOAD_MAIN03 segment word public 'CODE' use16
org (0209d0h - 015270h)
FOREIGN_MPN_UPLOAD_MAIN03 ends
main_03 group FOREIGN_MPN_UPLOAD_MAIN03
_DATA segment word public 'DATA' use16
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end
