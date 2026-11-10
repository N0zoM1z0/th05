; Mark the tile flags under a possibly clipped, scroll-wrapped hit box.
; Full near Pascal Point (x,y): two original stack words, RET 4.
; The native conditional/raster loops are based on the real tile geometry,
; not a target instruction listing or prepared bitmap payload.
.386
.model large
locals
include types.inc
include symbols.inc

main_01 group TILE_INVALIDATE_AROUND_TEXT
TILE_INVALIDATE_AROUND_TEXT segment byte public 'CODE' use16
assume cs:main_01, ds:DGROUP
public TILES_INVALIDATE_AROUND
TILES_INVALIDATE_AROUND proc near
    ; BX snapshots the entry SP for the two stack words; no BP frame.
    mov bx, sp
    mov dx, word ptr _tile_invalidate_box
    shr dx, 1
    mov ax, word ptr ss:[bx + 2]
    sar ax, 4
    sub ax, dx
    cmp ax, PLAYFIELD_WIDTH_PIXELS
    jl short @@left_edge
@@outside:
    ret 4
@@left_edge:
    mov cx, ax
    or ax, ax
    js short @@left_clip
    and ax, (TILE_WIDTH_PIXELS - 1)
@@left_clip:
    add ax, word ptr _tile_invalidate_box
    dec ax
    js short @@outside
    sar cx, 4
    jns short @@save_left
    xor cx, cx
@@save_left:
    mov _invalidate_left_x_tile, cx
    shr ax, 4
    inc ax
    mov cx, ax
    mov dx, word ptr _tile_invalidate_box + 2
    sar dx, 1
    mov ax, word ptr ss:[bx + 4]
    sar ax, 4
    add ax, TILE_HEIGHT_PIXELS
    sub ax, dx
    jns short @@check_bottom
    mov dx, word ptr _tile_invalidate_box + 2
    add dx, ax
    or dx, dx
    jle short @@outside
@@check_bottom:
    cmp ax, (PLAYFIELD_HEIGHT_PIXELS + TILE_HEIGHT_PIXELS)
    jge short @@outside
    mov bh, 0
    mov bl, _page_back
    add bx, bx
    add ax, _scroll_line_on_page[bx]
    jns short @@wrap_check
    add ax, HARDWARE_SCREEN_HEIGHT
    jmp short @@mark
@@wrap_check:
    cmp ax, HARDWARE_SCREEN_HEIGHT
    jl short @@mark
    sub ax, HARDWARE_SCREEN_HEIGHT
@@mark:
    mov dx, ax
    and dx, (DIRTY_ROW_HEIGHT_PIXELS - 1)
    add dx, word ptr _tile_invalidate_box + 2
    mov bx, dx
    add bx, ax
    shr ax, 3
    shl ax, 5
    push si
    push di
    push ds
    pop es
    mov di, ax
    add di, _invalidate_left_x_tile
    add di, offset _halftiles_dirty
    mov si, DIRTY_ROW_COLUMNS
    sub si, cx
    mov ah, cl
    mov al, 1
    cmp bx, HARDWARE_SCREEN_HEIGHT
    jl short @@nowrap
    mov bx, offset _halftiles_dirty_end
@@wrap:
    mov cl, ah
    rep stosb
    sub dx, DIRTY_ROW_HEIGHT_PIXELS
    add di, si
    cmp di, bx
    jl short @@wrap
    sub di, DIRTY_MAP_TOTAL_BYTES
@@nowrap:
    mov cl, ah
    rep stosb
    add di, si
    sub dx, DIRTY_ROW_HEIGHT_PIXELS
    jg short @@nowrap
    pop di
    pop si
    ret 4
TILES_INVALIDATE_AROUND endp
public tile_invalidate_around_end
tile_invalidate_around_end label byte
TILE_INVALIDATE_AROUND_TEXT ends
end
