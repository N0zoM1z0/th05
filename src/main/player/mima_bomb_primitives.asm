; Mima bomb drawing primitives and generic 16-row BB column painter.
; Original near-register / PC-98 GRCG protocol; source owns no assets.
.386
.model large
locals
include types.inc
include symbols.inc

main_01 group MIMA_BOMB_PRIM_TEXT
MIMA_BOMB_PRIM_TEXT segment byte public 'CODE' use16
assume cs:main_01, ds:DGROUP
public GRCG_TILE_BB_PUT_8
public MIMA_BOMB_BARS_WHITE, MIMA_BOMB_BARS_ALTERNATE
public mima_bomb_primitives_end

GRCG_TILE_BB_PUT_8 proc near
    push di
    mov bx, dx
    sar ax, PIXELS_PER_BYTE_SHIFT
    shl dx, VRAM_Y_SHIFT_HIGH
    add ax, dx
    shr dx, VRAM_Y_SHIFT_LOW
    add ax, dx
    mov di, ax
    mov ax, VRAM_SEGMENT
    mov es, ax
    cmp bx, SCREEN_HEIGHT - TILE_HEIGHT
    ja short @@roll_needed
    mov cx, TILE_HEIGHT
    xor bx, bx
    jmp short @@fill_loop
@@roll_needed:
    mov cx, SCREEN_HEIGHT
    sub cx, bx
    mov bx, TILE_HEIGHT
    sub bx, cx
@@fill_loop:
    stosw
    add di, VRAM_ROW_BYTES - WORD_BYTES
    loop @@fill_loop
    or bx, bx
    jz short @@done
    sub di, VRAM_PLANE_BYTES
    xchg cx, bx
    jmp short @@fill_loop
@@done:
    pop di
    ret
GRCG_TILE_BB_PUT_8 endp

MIMA_BOMB_BARS_WHITE proc near
    push di
    pushf
    cli
    mov al, GRCG_TDW
    out GRCG_MODE_PORT, al
    mov dx, GRCG_TILE_PORT
    mov al, GRCG_WHITE
    out dx, al
    out dx, al
    out dx, al
    out dx, al
    popf
    mov ax, BOMB_BAR_VRAM_SEG
    mov es, ax
    mov di, BOMB_BARS_BOTTOM_LEFT
@@draw_row:
    mov dword ptr es:[di + WHITE_FAR_DWORD_OFFSET], eax
    stosd
    mov word ptr es:[di + WHITE_FAR_WORD_OFFSET], ax
    stosw
    sub di, BARS_WHITE_ROW_BACKSTEP
    jge short @@draw_row
    pop di
    xor al, al
    out GRCG_MODE_PORT, al
    ret
MIMA_BOMB_BARS_WHITE endp

MIMA_BOMB_BARS_ALTERNATE proc near
    push di
    pushf
    cli
    mov al, GRCG_TDW
    out GRCG_MODE_PORT, al
    mov dx, GRCG_TILE_PORT
    mov al, GRCG_WHITE
    out dx, al
    not al
    out dx, al
    out dx, al
    out dx, al
    popf
    mov ax, BOMB_BAR_VRAM_SEG
    mov es, ax
    mov di, BOMB_BARS_BOTTOM_LEFT
@@draw_row:
    mov dword ptr es:[di + ALT_FAR_DWORD_FIRST], eax
    mov dword ptr es:[di + ALT_FAR_DWORD_SECOND], eax
    stosd
    stosd
    mov word ptr es:[di + ALT_FAR_WORD_OFFSET], ax
    stosw
    sub di, BARS_ALT_ROW_BACKSTEP
    jge short @@draw_row
    pop di
    xor al, al
    out GRCG_MODE_PORT, al
    ret
MIMA_BOMB_BARS_ALTERNATE endp
    even
mima_bomb_primitives_end label byte
MIMA_BOMB_PRIM_TEXT ends
end
