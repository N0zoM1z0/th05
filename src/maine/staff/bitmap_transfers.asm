; TH05 MAINE verdict bitmap: PC-98 display-plane capture and mask restore.
; Unaccepted native-language candidate: strict XOR encoding and fixup-order
; comparisons remain unresolved. Independent semantic device reconstruction.
; The bitmap
; storage and GRCG driver are foreign; this file owns only these two kernels.
; ReC98 th05/end/verdict_bitmap.asm documents the original semantics.
.386
.model large
locals
include types.inc
include symbols.inc

STAFF_BITMAP_TEXT segment byte public 'CODE' use16
assume cs:STAFF_BITMAP_TEXT, ds:DGROUP
group_01 group STAFF_BITMAP_TEXT

public @VERDICT_BITMAP_SNAP$QUI
@VERDICT_BITMAP_SNAP$QUI proc near
@@bitmap_offset equ word ptr [bp+4]
    push bp
    mov bp, sp
    push si
    push di
    push ds
    push ds
    pop es
    mov ax, PLANE_E_SEGMENT
    mov ds, ax
    xor si, si
    mov di, @@bitmap_offset
    add di, offset _verdict_bitmap
    mov ax, VERDICT_ROWS
@@copy_row:
    mov cx, VERDICT_WORDS
    rep movsw
    add si, ROW_SKIP
    dec ax
    jnz short @@copy_row
    pop ds
    pop di
    pop si
    pop bp
    ret 2
@VERDICT_BITMAP_SNAP$QUI endp

public @VERDICT_BITMAP_PUT$QUI
@VERDICT_BITMAP_PUT$QUI proc near
@@bitmap_offset equ word ptr [bp+4]
    push bp
    mov bp, sp
    push si
    push di
    push ((GRCG_TDW_MODE shl 16) or GRCG_TILE_COLOR)
    call GRCG_SETCOLOR
    mov ax, PLANE_B_SEGMENT
    mov es, ax
    xor di, di
    mov dx, VERDICT_ROWS
@@clear_row:
    mov cx, VERDICT_WORDS
    rep stosw
    add di, ROW_SKIP
    dec dx
    jnz short @@clear_row
    push ((GRCG_RMW_MODE shl 16) or GRCG_MASK_COLOR)
    call GRCG_SETCOLOR
    xor di, di
    mov si, @@bitmap_offset
    add si, offset _verdict_bitmap
    mov dx, VERDICT_ROWS
@@mask_row:
    mov cx, VERDICT_WORDS
    rep movsw
    add di, ROW_SKIP
    dec dx
    jnz short @@mask_row
    mov dx, GRCG_CONTROL_PORT
    mov al, 0
    out dx, al
    pop di
    pop si
    pop bp
    ret 2
@VERDICT_BITMAP_PUT$QUI endp

public staff_bitmap_transfers_end
staff_bitmap_transfers_end label byte
STAFF_BITMAP_TEXT ends
end
