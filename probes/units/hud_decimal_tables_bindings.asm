; Real code frames and outside DATA prefix only; no values or instructions.
.386
.model large
_TEXT segment word public 'CODE' use16
org 0ae10h
_TEXT ends
DECIMAL_TABLE_DATA_TEXT segment byte public 'CODE' use16
org (14ab0h - 0ae10h)
DECIMAL_TABLE_DATA_TEXT ends
main_01 group DECIMAL_TABLE_DATA_TEXT
SHARED segment para public 'CODE' use16
org (209d0h - 14ab0h)
SHARED ends
_DATA segment word public 'DATA' use16
org 01406h
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end
