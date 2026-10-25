; Complete TH05 page-1 to page-0 EGC rectangle-copy procedure.
; Semantic original-ASM reconstruction; private setup provider remains unowned.
.386
.model use16 large SHARED
locals
include types.inc
include symbols.inc

VISIBLE_ROWS equ 400
PLANE_BYTES equ (ROW_BYTES * VISIBLE_ROWS)

EGC_WRITE macro reg, value
 mov dx, reg
 mov ax, value
 out dx, ax
endm

; EGC latches read page 1 and write page 0 at the same video offset.
COPY_INTERPAGE_WORD macro
 mov al, 1
 out PAGE_PORT, al
 mov dx, es:[di]
 xor ax, ax
 out PAGE_PORT, al
 mov es:[di], dx
endm

.code SHARED
public egc_rect_copy, @EGC_COPY_RECT_1_TO_0_16$QIIII
@EGC_COPY_RECT_1_TO_0_16$QIIII label far
egc_rect_copy proc far
 ; Far Pascal (left, top, width, height), four word arguments.
 arg @@height:word, @@width:word, @@top:word, @@left:word
 push bp
 mov bp, sp
 push di
 call EGC_RECT_SETUP
 EGC_WRITE EGC_MODE_ROP_REG, 29F0h
 mov ax, @@left
 mov dx, @@top
 mov bx, ax
 sar bx, 4
 shl bx, 1
 shl dx, 6
 add bx, dx
 shr dx, 2
 add bx, dx
 mov di, bx
 and ax, 0Fh
 mov cx, ax
 add ax, @@width
 shr ax, 4
 or cx, cx
 jz short @@aligned_left
 inc ax
@@aligned_left:
 mov _egcrect_w, ax
 mov cx, (ROW_BYTES/2)
 sub cx, ax
 shl cx, 1
 mov bx, @@height
 ; All argument reads are complete. BP becomes the next-row byte stride.
 mov bp, cx
 mov ax, SEG_PLANE_B
 mov es, ax
@@next_row:
 mov cx, _egcrect_w
@@next_word:
 or di, di
 js short @@skip_word
 cmp di, PLANE_BYTES
 jnb short @@skip_word
 COPY_INTERPAGE_WORD
@@skip_word:
 add di, 2
 loop @@next_word
 add di, bp
 dec bx
 jns short @@next_row
 call EGC_OFF
 pop di
 pop bp
 retf 8
egc_rect_copy endp
 even
public egc_rect_copy_end
egc_rect_copy_end label byte
end
