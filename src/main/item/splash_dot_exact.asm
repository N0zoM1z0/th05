; TH05 item splash dot draw at the hardware fastcall boundary.
; AX = signed screen X, DX = VRAM Y, ES = caller-selected plane.
.386
.model large
locals
include types.inc
include symbols.inc

main_01 group ITEM_SPLASH_DOT_TEXT
ITEM_SPLASH_DOT_TEXT segment byte public 'CODE' use16
assume cs:main_01, ds:DGROUP
public @item_splash_dot_render, item_splash_dot_end
@item_splash_dot_render proc near
    mov cx, ax
    sar ax, PIXEL_TO_BYTE_SHIFT
    shl dx, ROW_OFFSET_SHIFT_HIGH
    add ax, dx
    shr dx, ROW_OFFSET_SHIFT_LOW
    add ax, dx
    mov bx, ax
    mov al, TOP_PIXEL_BIT
    and cl, BYTE_PIXEL_MASK
    shr al, cl
    mov es:[bx], al
    ret
@item_splash_dot_render endp
item_splash_dot_end label byte
ITEM_SPLASH_DOT_TEXT ends
end
