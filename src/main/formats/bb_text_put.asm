; Raw TH05 bitmap-text renderer: FS/DS transfer and 400-line VRAM wrap.
; The caller selects the GRCG mode and ES destination; this code only copies.
.386
.model large
locals
include types.inc
include symbols.inc

main_01 group BB_TEXT_PUT_TEXT
BB_TEXT_PUT_TEXT segment byte public 'CODE' use16
assume cs:main_01, ds:DGROUP
public @bb_txt_put_8_raw$quiui, bb_txt_put_end
@bb_txt_put_8_raw$quiui proc near
    push si
    push di
    push ds
    mov bx, dx
    sar ax, BB_PIXELS_PER_BYTE_SHIFT
    shl dx, BB_VRAM_Y_SHIFT_HIGH
    add ax, dx
    shr dx, BB_VRAM_Y_SHIFT_LOW
    add ax, dx
    mov di, ax
    shl cx, BB_SPRITE_BYTE_SHIFT
    mov si, cx
    mov ax, _bb_txt_seg
    mov ds, ax
    cmp bx, (SCREEN_LINES - BB_TEXT_ROWS)
    ja short @@roll_needed
    mov cx, BB_TEXT_ROWS
    even
@@no_roll_loop:
    lodsd
    or eax, eax
    jz short @@skip_blank
    stosd
    add di, (VRAM_ROW_BYTES - BB_TEXT_ROW_BYTES)
    loop @@no_roll_loop
    jmp short @@done
@@skip_blank:
    add di, VRAM_ROW_BYTES
    loop @@no_roll_loop
    jmp short @@done
@@roll_needed:
    mov ax, BB_TEXT_ROWS
    mov cx, SCREEN_LINES
    sub cx, bx
    sub ax, cx
@@roll_first_page:
    movsd
    add di, (VRAM_ROW_BYTES - BB_TEXT_ROW_BYTES)
    loop @@roll_first_page
    sub di, VRAM_PLANE_BYTES
    mov cx, ax
@@roll_second_page:
    movsd
    add di, (VRAM_ROW_BYTES - BB_TEXT_ROW_BYTES)
    loop @@roll_second_page
@@done:
    pop ds
    pop di
    pop si
    ret
@bb_txt_put_8_raw$quiui endp
    even
bb_txt_put_end label byte
BB_TEXT_PUT_TEXT ends
end
