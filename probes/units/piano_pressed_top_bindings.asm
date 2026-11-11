; Foreign-only OP native CODE frames. No sprite or executable bytes supplied.
.386
.model large
_TEXT segment word public 'CODE' use16
org 0A390h
_TEXT ends
FOREIGN_MAIN segment byte public 'CODE' use16
org (0D300h - 0A390h)
FOREIGN_MAIN ends
SHARED segment para public 'CODE' use16
org 00801h
SHARED ends
FOREIGN_SHARED_TAIL segment byte public 'CODE' use16
org (0EFE0h - 0DB0Dh)
FOREIGN_SHARED_TAIL ends
_DATA segment word public 'DATA' use16
org 03E96h
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA,_BSS
end
