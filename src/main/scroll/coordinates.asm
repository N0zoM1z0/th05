; Convert a world-space subpixel Y into the active PC-98 VRAM scroll origin.
; The genuine near Pascal entry has one word argument and RET 2.
; The 400-line correction is intentionally applied only once.
.386
.model large
locals
include types.inc
include symbols.inc
SCROLL_RING_HEIGHT equ 400

main_01 group SCROLL_COORDINATE_TEXT
SCROLL_COORDINATE_TEXT segment word public 'CODE' use16
assume cs:main_01, ds:DGROUP
public SCROLL_SUBPIXEL_Y_TO_VRAM_SEG1
SCROLL_SUBPIXEL_Y_TO_VRAM_SEG1 proc near
    mov bx, sp
    mov ax, word ptr ss:[bx+2]
    sar ax, SCROLL_FRACTION_BITS
    cmp _scroll_active, 0
    je short @@do_wrap
    add ax, _scroll_line
@@do_wrap:
    or ax, ax
    jge short @@nonnegative
    add ax, SCROLL_RING_HEIGHT
    jmp short @@return
@@nonnegative:
    cmp ax, SCROLL_RING_HEIGHT
    jl short @@return
    sub ax, SCROLL_RING_HEIGHT
@@return:
    ret 2
SCROLL_SUBPIXEL_Y_TO_VRAM_SEG1 endp
public scroll_coordinate_end
scroll_coordinate_end label byte
SCROLL_COORDINATE_TEXT ends
end
