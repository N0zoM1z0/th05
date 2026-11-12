; Actual OP CODE frames and original DATA prefix, no candidate mask words.
.386
.model large
_TEXT segment word public 'CODE' use16
org 0a390h
_TEXT ends
OP_PI_MASK_DATA_TEXT segment byte public 'CODE' use16
org (0d300h - 0a390h)
OP_PI_MASK_DATA_TEXT ends
op_01 group OP_PI_MASK_DATA_TEXT
SHARED segment para public 'CODE' use16
org (0efe0h - 0d300h)
SHARED ends
_DATA segment word public 'DATA' use16
org 00a64h
_DATA ends
; Original downstream DATA suffix is outside this entire 32-byte bank.
; Its real extent supplies the SS:SP memory floor for the isolated MZ build.
OP_PI_MASK_FOREIGN_DATA_TAIL segment word public 'DATA' use16
org (02817h - 00a84h)
OP_PI_MASK_FOREIGN_DATA_TAIL ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, OP_PI_MASK_FOREIGN_DATA_TAIL, _BSS
end
