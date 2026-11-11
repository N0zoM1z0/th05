; GRCG color control and gather-pellet bitmap blitter in original main_03.
; Full native register contracts: AH=color, AX=left, DX=top, ES=video page.
.386
.model large
locals
include types.inc
include symbols.inc

main_03 group GATHER_RASTER_TEXT
GATHER_RASTER_TEXT segment byte public 'CODE' use16
assume cs:main_03, ds:DGROUP
public GATHER_GRCG_COLOR_DIRECT, GATHER_GRCG_MODE_RMW
public @gather_point_render$qii, gather_raster_end

GATHER_GRCG_COLOR_DIRECT proc near
    cli
    mov dx, GRCG_TILE_PORT
    rept 4
        shr ah, 1
        sbb al, al
        out dx, al
    endm
    sti
    ret
GATHER_GRCG_COLOR_DIRECT endp

GATHER_GRCG_MODE_RMW proc near
    mov al, GRCG_RMW
    out GRCG_MODE_PORT, al
    ret
GATHER_GRCG_MODE_RMW endp
    even

@gather_point_render$qii proc near
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
    and si, PIXEL_SHIFT_MASK
    mov ax, si
    shl si, RASTER_SHIFT_BYTES
    add si, offset _sPELLET
    mov cx, GATHER_POINT_H
    cmp bx, (SCREEN_HEIGHT - GATHER_POINT_H)
    ja short @@roll_needed
    xor dx, dx
    jmp short @@no_roll
@@roll_needed:
    mov dx, cx
    mov cx, SCREEN_HEIGHT
    sub cx, bx
    sub dx, cx
@@no_roll:
    or ax, ax
    jz short @@byte_aligned_loop
    nop
@@word_loop:
    movsw
    add di, VRAM_ROW_BYTES - WORD_BYTES
    loop @@word_loop
@@roll_check:
    or dx, dx
    jz short @@done
    sub di, VRAM_PLANE_BYTES
    xchg cx, dx
    jmp short @@word_loop
@@byte_aligned_loop:
    movsb
    add di, VRAM_ROW_BYTES - BYTE_BYTES
    inc si
    loop @@byte_aligned_loop
    jmp short @@roll_check
@@done:
    pop di
    pop si
    ret
@gather_point_render$qii endp
gather_raster_end label byte
GATHER_RASTER_TEXT ends
end
