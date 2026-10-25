; Private AX=top, DX=left, CX=mask ID; ES=VRAM, DS=foreign mask bank.
.386
.model large
locals
include types.inc
include symbols.inc
POINTNUM_DRAW_ROWS equ POINTNUM_H

; Skip blank right bytes and blank words while preserving the VRAM row ring.
BLIT_MASK_ROWS macro rows
 cmp bx, (VRAM_HEIGHT - rows)
 ja short @@wrap_needed
 mov cx, rows
 xor bx, bx
 jmp short @@row
@@wrap_needed:
 mov cx, VRAM_HEIGHT
 sub cx, bx
 mov bx, rows
 sub bx, cx
 even
@@row:
 lodsw
 or ah, ah
 jz short @@left_only
 mov es:[di], ax
 jmp short @@advance
@@left_only:
 or al, al
 jz short @@advance
 mov es:[di], al
@@advance:
 add di, VRAM_ROW_BYTES
 loop @@row
 or bx, bx
 jz short @@rows_done
 sub di, VRAM_PLANE_BYTES
 xchg cx, bx
 jmp short @@row
@@rows_done:
endm

main_01 group MAIN_01_TEXT
MAIN_01_TEXT segment word public 'CODE' use16
assume cs:main_01, ds:DGROUP
public @pointnum_put
@pointnum_put proc near
 push si
 push di
 push ax
 push dx
 mov si, dx
 mov bx, ax
 sar dx, 3
 shl ax, 6
 add dx, ax
 shr ax, 2
 add dx, ax
 mov di, dx
 and si, (POINTNUM_SHIFTS - 1)
 mov ax, si
 shl si, 4
 add si, offset _sPOINTNUMS
 shl cx, 7
 add si, cx
 BLIT_MASK_ROWS POINTNUM_DRAW_ROWS
 pop dx
 pop ax
 add dx, POINTNUM_W
 pop di
 pop si
 ret
@pointnum_put endp
public pointnum_put_end
pointnum_put_end label byte
MAIN_01_TEXT ends
end
