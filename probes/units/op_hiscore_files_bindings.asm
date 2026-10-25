; Compiler owns all53 readable filename bytes atDS2818..284D.
; No CODE, filenames, padding or initialized values supplied by this context.
.386
.model large
_TEXT segment word public 'CODE' use16
org 0efe0h
_TEXT ends
_DATA segment word public 'DATA' use16
org 02818h
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end
