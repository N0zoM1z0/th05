; Real provider/frame context only, no input implementation or initialized data.
.386
.model large
_TEXT segment word public 'CODE' use16
org 0a540h
_TEXT ends
FOREIGN_MAIN segment byte public 'CODE' use16
org 042c0h
FOREIGN_MAIN ends
SHARED segment para public 'CODE' use16
assume cs:SHARED
public @input_reset_sense$qv
org 00902h
@input_reset_sense$qv label far
public @input_sense$qv
org 0090ah
@input_sense$qv label far
org 00a08h
SHARED ends
FOREIGN_SHARED_TAIL segment byte public 'CODE' use16
org 00ef8h
FOREIGN_SHARED_TAIL ends
_DATA segment word public 'DATA' use16
; Independently accepted foreign allocation bound; no supplied values.
org 04f0eh
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end
