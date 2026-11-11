; Mima bombing backdrop: hardware GRCG strips, playfield columns and page fill.
; The first procedure calls the independently reconstructed near band worker.
; All drawing is performed by PC-98 GRCG/VRAM instructions in the native ABI.
.386
.model large
locals
include types.inc
include symbols.inc

main_01 group MIMA_BACKDROP_TEXT
MIMA_BACKDROP_TEXT segment byte public 'CODE' use16
assume cs:main_01, ds:DGROUP
public mima_backdrop_white_bands, mima_backdrop_black_columns
public mima_backdrop_clear_pages, grcg_fill_playfield_rows
public mima_backdrop_end

mima_backdrop_white_bands proc near
    push di
    pushf
    cli
    mov al, GRCG_TILE_DIRECT
    out GRCG_MODE_PORT, al
    mov dx, GRCG_TILE_PORT
    mov al, GRCG_WHITE
    out dx, al
    not al
    out dx, al
    out dx, al
    out dx, al
    popf
    mov ax, VRAM_BAND_BOTTOM
    mov es, ax
    call mima_bomb_bands_fill
    mov ax, VRAM_PLAYFIELD_TOP
    mov es, ax
    call mima_bomb_bands_fill
    mov ax, VRAM_BAND_CENTER
    mov es, ax
    mov di, (CENTER_LAST_ROW * VRAM_ROW_BYTES) + PLAYFIELD_LEFT_BYTE
@@center_row:
    mov es:[di], eax
    mov es:[di+RIGHT_STRIP_BYTE], eax
    sub di, VRAM_ROW_BYTES
    jge short @@center_row
    pushf
    cli
    mov dx, GRCG_TILE_PORT
    mov al, GRCG_WHITE
    out dx, al
    out dx, al
    out dx, al
    out dx, al
    popf
    mov ax, VRAM_BAND_BOTTOM
    mov es, ax
    mov di, (BAND_LAST_ROW * VRAM_ROW_BYTES) + BAND_RIGHT_BYTE
@@bottom_row:
    stosd
    sub di, VRAM_ROW_BYTES + DWORD_BYTES
    jge short @@bottom_row
    mov ax, VRAM_PLAYFIELD_TOP
    mov es, ax
    mov di, (BAND_LAST_ROW * VRAM_ROW_BYTES) + BAND_RIGHT_BYTE
@@top_row:
    stosd
    sub di, VRAM_ROW_BYTES + DWORD_BYTES
    jge short @@top_row
    pop di
    xor al, al
    out GRCG_MODE_PORT, al
    ret
mima_backdrop_white_bands endp
    even

mima_backdrop_black_columns proc near
    push di
    pushf
    cli
    mov al, GRCG_TILE_DIRECT
    out GRCG_MODE_PORT, al
    mov dx, GRCG_TILE_PORT
    xor al, al
    out dx, al
    not al
    out dx, al
    out dx, al
    out dx, al
    popf
    mov ax, VRAM_PLAYFIELD_TOP
    mov es, ax
    mov di, ((PLAYFIELD_H - 1) * VRAM_ROW_BYTES) + PLAYFIELD_LEFT_BYTE
@@column_row:
    mov es:[di+BLACK_COLUMN_1], eax
    mov es:[di+BLACK_COLUMN_2], eax
    stosd
    stosd
    sub di, VRAM_ROW_BYTES + (DWORD_BYTES * 2)
    jge short @@column_row
    pop di
    xor al, al
    out GRCG_MODE_PORT, al
    ret
mima_backdrop_black_columns endp

mima_backdrop_clear_pages proc near
    cli
    mov al, GRCG_TILE_DIRECT
    out GRCG_MODE_PORT, al
    mov dx, GRCG_TILE_PORT
    mov al, GRCG_WHITE
    out dx, al
    xor al, al
    out dx, al
    out dx, al
    out dx, al
    sti
    push di
    mov ax, VRAM_MAIN
    mov es, ax
    mov ax, 1
    out VRAM_PAGE_SELECT_PORT, ax
    xor di, di
    mov cx, VRAM_PLANE_DWORDS
    rep stosd
    xor ax, ax
    out VRAM_PAGE_SELECT_PORT, ax
    mov cx, VRAM_PLANE_DWORDS
    xor di, di
    rep stosd
    pop di
    xor al, al
    out GRCG_MODE_PORT, al
    ret
mima_backdrop_clear_pages endp

grcg_fill_playfield_rows proc near
@@fill_row:
    mov cx, PLAYFIELD_VISIBLE_DWORDS
    rep stosd
    sub di, VRAM_ROW_BYTES + PLAYFIELD_VISIBLE_BYTES
    jge short @@fill_row
    ret
grcg_fill_playfield_rows endp
    even
mima_backdrop_end label byte
MIMA_BACKDROP_TEXT ends
end
