; Original-representation near-Pascal signed vector rotation.
; Input stack: length signed WORD, angle BYTE in WORD slot, SPPoint* near.
; All products are signed 32-bit and shifted before the low WORD stores.
.386
.model large
locals
include types.inc
include symbols.inc

VECTOR2_NEAR_TEXT segment word public 'CODE' use16
assume cs:VECTOR2_NEAR_TEXT, ds:DGROUP
public VECTOR2_NEAR
VECTOR2_NEAR proc near
    push bp
    mov bp, sp
    movsx edx, word ptr [bp + 4]
    mov bl, byte ptr [bp + 6]
    mov bh, 0
    add bx, bx
    movsx eax, word ptr _CosTable8[bx]
    movsx ecx, word ptr _SinTable8[bx]
    imul eax, edx
    sar eax, VECTOR2_TRIG_FRAC_BITS
    imul edx, ecx
    sar edx, VECTOR2_TRIG_FRAC_BITS
    mov bx, word ptr [bp + 8]
    mov word ptr [bx], ax
    mov word ptr [bx + 2], dx
    pop bp
    ret 6
VECTOR2_NEAR endp
public vector2_near_end
vector2_near_end label byte
VECTOR2_NEAR_TEXT ends
end
