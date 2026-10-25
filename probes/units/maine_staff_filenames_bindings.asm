; Outside-only original DATA context. No file data, text contents, or code.
.386
.model large
_TEXT segment word public 'CODE' use16
org 0A540h
_TEXT ends
STAFF_FILES_DATA_TEXT segment byte public 'CODE' use16
org (0E800h - 0A540h)
STAFF_FILES_DATA_TEXT ends
group_01 group STAFF_FILES_DATA_TEXT
SHARED segment para public 'CODE' use16
org (10110h - 0E800h)
SHARED ends
_DATA segment word public 'DATA' use16
org 01752h
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end
