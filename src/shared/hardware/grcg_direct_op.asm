; OP's original direct GRCG tile color helper, using AH four-bit nibble.
.386
.model large
locals
include types.inc
include symbols.inc
SHARED segment byte public 'CODE' use16
assume cs:SHARED, ds:DGROUP
public @grcg_setcolor_direct_raw$qv, grcg_direct_op_end
@grcg_setcolor_direct_raw$qv proc near
    cli
    mov dx, GRCG_TILE_PORT
    rept 4
        shr ah, 1
        sbb al, al
        out dx, al
    endm
    sti
    ret
@grcg_setcolor_direct_raw$qv endp
grcg_direct_op_end label byte
SHARED ends
end
