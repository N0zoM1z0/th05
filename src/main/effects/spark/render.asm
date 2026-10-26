; Private mask writer: AX=left, DX=ring top, CX=animation cel, ES=VRAM.
.386
.model large
locals
include types.inc
include symbols.inc
SPARK_DRAW_ROWS equ SPARK_H

; Keep source rows contiguous when the destination wraps around row400.
BLIT_SPARK_ROWS macro rows
 cmp bx, (VRAM_HEIGHT - rows)
 ja short @@roll
 mov cx, rows
 xor bx, bx
 jmp short @@row
@@roll:
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
 jz short @@copied
 sub di, VRAM_PLANE_BYTES
 xchg cx, bx
 jmp short @@row
@@copied:
endm

main_01 group MAIN_01_TEXT
MAIN_01_TEXT segment word public 'CODE' use16
assume cs:main_01, ds:DGROUP
public @spark_render
@spark_render proc near
 push si
 push di
 mov si, ax
 mov bx, dx
 sar ax, 3
 shl dx, 6
 add ax, dx
 shr dx, 2
 add ax, dx
 mov di, ax
 and si, (SPARK_SHIFTS - 1)
 mov ax, si
 shl si, 7
 add si, offset _sSPARKS
 and cx, (SPARK_CELS - 1)
 shl cx, 4
 add si, cx
 BLIT_SPARK_ROWS SPARK_DRAW_ROWS
 pop di
 pop si
 ret
@spark_render endp
 even
public spark_render_end
spark_render_end label byte
MAIN_01_TEXT ends
end
