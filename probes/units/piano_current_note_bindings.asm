; Real OP CS/DGROUP context. No instructions, driver record or initialized data.
.386
.model large
_TEXT segment word public 'CODE' use16
org 0d300h
_TEXT ends
SHARED segment byte public 'CODE' use16
org 00712h
SHARED ends
; Paragraph boundary after the native function retains the true data frame.
FOREIGN_SHARED_TAIL segment para public 'CODE' use16
org 015b0h
FOREIGN_SHARED_TAIL ends
_DATA segment word public 'DATA' use16
org 02817h
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end
