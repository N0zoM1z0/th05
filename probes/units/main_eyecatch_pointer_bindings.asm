; Actual MAIN frames; only foreign filename public, not its bytes.
.386
.model large
_TEXT segment word public 'CODE' use16
org 0ae10h
_TEXT ends
EYECATCH_POINTER_TEXT segment byte public 'CODE' use16
org 09ca0h
EYECATCH_POINTER_TEXT ends
main_01 group EYECATCH_POINTER_TEXT
SHARED segment byte public 'CODE' use16
org 07c0h
SHARED ends
EYEPOINTER_MAIN03 segment byte public 'CODE' use16
org 0b760h
EYEPOINTER_MAIN03 ends
main_03 group EYEPOINTER_MAIN03
_DATA segment word public 'DATA' use16
org 009ch
_DATA ends
EYECATCH_POINTER_FOREIGN_DATA segment byte public 'DATA' use16
public _EYECATCH_FN
org 000ah
_EYECATCH_FN label byte
EYECATCH_POINTER_FOREIGN_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, EYECATCH_POINTER_FOREIGN_DATA, _BSS
end
