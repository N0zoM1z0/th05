; Invalidate every active score-popup using its previous Y/current X position.
; Full real 280 x 16-byte canonical pointnum_t pool, near Pascal RET4 tile API.
.386
.model large
locals
include types.inc
include symbols.inc
POINTNUM_INVALIDATE_HEIGHT equ POINTNUM_H

main_01 group POINTNUM_INV_TEXT
POINTNUM_INV_TEXT segment byte public 'CODE' use16
assume cs:main_01, ds:DGROUP
public @POINTNUMS_INVALIDATE$QV
@POINTNUMS_INVALIDATE$QV proc near
    push si
    push di
    mov word ptr [_tile_invalidate_box + 2], POINTNUM_INVALIDATE_HEIGHT
    mov si, offset _pointnums
    mov di, POINTNUM_COUNT
@@next:
    cmp byte ptr [si + pointnum_t.PN_flag], 0
    jz short @@advance
    mov ax, [si + pointnum_t.PN_width]
    mov word ptr _tile_invalidate_box, ax
    mov ax, [si + pointnum_t.PN_center_x]
    push word ptr [si + pointnum_t.PN_prev_y]
    push ax
    call TILES_INVALIDATE_AROUND
@@advance:
    add si, size pointnum_t
    dec di
    jnz short @@next
    pop di
    pop si
    ret
@POINTNUMS_INVALIDATE$QV endp
public pointnums_invalidate_end
pointnums_invalidate_end label byte
POINTNUM_INV_TEXT ends
end
