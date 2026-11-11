; TH05 shot laser raster painter, original-register near ASM.
; AX=screen left; DX=VRAM top; BX=laser cel; SI=height in subpixels.
; ES selects the actual PC-98 plane; return restores SI and DI only.
.386
.model large
locals
include types.inc
include symbols.inc

main_01 group SHOT_LASER_PUT_TEXT
SHOT_LASER_PUT_TEXT segment byte public 'CODE' use16
assume cs:main_01, ds:DGROUP
public SHOT_LASER_PUT_RAW, shot_laser_put_end
SHOT_LASER_PUT_RAW proc near
    push si
    push di
    mov cx, ax
    sar ax, PIXELS_PER_BYTE_SHIFT
    mov di, ax
    and cl, PIXEL_SHIFT_MASK
    xor ah, ah
    mov al, _SHOT_LASER_DOTS[bx]
    ror ax, cl
    mov bx, dx
    shl dx, VRAM_Y_SHIFT1
    add di, dx
    shr dx, VRAM_Y_SHIFT2
    add di, dx
    mov dx, VRAM_SEGMENT
    mov es, dx
    shr si, SUBPIXELS_PER_PIXEL_SHIFT
    mov cx, si
    add cx, bx
    cmp cx, SCREEN_HEIGHT
    ja short @@roll_needed
    mov cx, si
    xor dx, dx
    jmp short @@blit_loop
@@roll_needed:
    mov cx, SCREEN_HEIGHT
    sub cx, bx
    mov dx, si
    sub dx, cx
@@blit_loop:
    or ah, ah
    jz short @@byte_loop
    even
@@word_loop:
    stosw
    add di, VRAM_ROW_BYTES - WORD_BYTES
    loop @@word_loop
    jmp short @@roll_check
@@byte_loop:
    stosb
    add di, VRAM_ROW_BYTES - BYTE_BYTES
    loop @@byte_loop
@@roll_check:
    or dx, dx
    jz short @@return
    sub di, VRAM_PLANE_BYTES
    xchg cx, dx
    jmp short @@blit_loop
@@return:
    pop di
    pop si
    ret
SHOT_LASER_PUT_RAW endp
    even
shot_laser_put_end label byte
SHOT_LASER_PUT_TEXT ends
end
