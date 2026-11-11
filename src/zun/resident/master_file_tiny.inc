; The real Master library TASM 3.x macro ABI under .MODEL TINY.
; The source keeps the preserved library register instructions, not a copied
; target-image byte table. Tiny model has near RET and near DATA parameters.
RETSIZE equ 1
DATASIZE equ 1
LDATA equ 0
func macro symbol
    public symbol
    even
    symbol proc near
    endfunc macro
        even
        symbol endp
    endm
endm
nopcall macro symbol
    call symbol
endm
