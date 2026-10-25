; Real provider/frame context only, no input implementation or initialized data.
.386
.model large
_TEXT segment word public 'CODE' use16
org 0ae10h
_TEXT ends
FOREIGN_MAIN segment byte public 'CODE' use16
org 09ca0h
FOREIGN_MAIN ends
SHARED segment para public 'CODE' use16
assume cs:SHARED
public @input_reset_sense$qv
org 00512h
@input_reset_sense$qv label far
public @input_sense$qv
org 0051ah
@input_sense$qv label far
org 00618h
SHARED ends
FOREIGN_SHARED_TAIL segment byte public 'CODE' use16
org 0b8f8h
FOREIGN_SHARED_TAIL ends
_DATA segment word public 'DATA' use16
; Independently accepted foreign allocation bound; no supplied values.
org 0c4c8h
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end
