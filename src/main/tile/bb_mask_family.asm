; Original-register Boss background tile bitmap put/invalidation routines.
; Operate on 24x23 tile bits in a 128-byte per-cel segmented bitmap.
.386
.model large
locals
include types.inc
include symbols.inc

main_01 group TILE_BB_MASK_TEXT
TILE_BB_MASK_TEXT segment byte public 'CODE' use16
assume cs:main_01, ds:DGROUP
public @TILES_BB_PUT_RAW$QI, @TILES_BB_INVALIDATE_RAW$QI
public tile_bb_mask_end

@TILES_BB_PUT_RAW$QI proc near
@@top equ word ptr [bp-6]
@@left equ word ptr [bp-4]
@@row_tiles_left equ byte ptr [bp-2]
@@shiftreg equ byte ptr [bp-1]
@@cel equ word ptr [bp+4]
    enter 6, 0
    push di
    push GRCG_RMW
    mov al, _tiles_bb_col
    mov ah, 0
    push ax
    call GRCG_SETCOLOR
    mov ax, _tiles_bb_seg
    mov fs, ax
    mov di, @@cel
    shl di, BB_CEL_BYTES_SHIFT
    mov @@top, PLAYFIELD_TOP
@@row_loop:
    mov @@left, PLAYFIELD_LEFT
    mov @@row_tiles_left, TILE_COLUMNS
@@new_byte:
    mov al, fs:[di]
    mov @@shiftreg, al
@@next_tile:
    test @@shiftreg, 80h
    jz short @@skip_tile
    mov ax, @@left
    mov dx, @@top
    cmp _scroll_active, 0
    jz short @@roll_check
    add dx, _scroll_line
@@roll_check:
    cmp dx, SCREEN_HEIGHT
    jl short @@put
    sub dx, SCREEN_HEIGHT
@@put:
    call grcg_tile_bb_put_8
@@skip_tile:
    shl @@shiftreg, 1
    add @@left, TILE_WIDTH
    dec @@row_tiles_left
    jz short @@next_row
    test @@row_tiles_left, 7
    jnz short @@next_tile
    inc di
    jmp short @@new_byte
@@next_row:
    add di, 2
    add @@top, TILE_HEIGHT
    cmp @@top, PLAYFIELD_BOTTOM
    jb short @@row_loop
    mov dx, GRCG_MODE_PORT
    mov al, 0
    out dx, al
    pop di
    leave
    ret 2
@TILES_BB_PUT_RAW$QI endp

@TILES_BB_INVALIDATE_RAW$QI proc near
@@center_x equ word ptr [bp-6]
@@center_y equ word ptr [bp-4]
@@tiles_left equ byte ptr [bp-2]
@@shiftreg equ byte ptr [bp-1]
@@cel equ word ptr [bp+4]
    enter 6, 0
    push di
    mov dword ptr _tile_invalidate_box, ((DIRTY_TILE_SIZE shl 16) or DIRTY_TILE_SIZE)
    mov ax, _bb_boss_seg
    mov fs, ax
    mov di, @@cel
    shl di, BB_CEL_BYTES_SHIFT
    mov @@center_y, TILE_CENTER_SUBPIXELS
@@row_loop:
    mov @@center_x, TILE_CENTER_SUBPIXELS
    mov @@tiles_left, TILE_COLUMNS
@@new_byte:
    mov al, fs:[di]
    mov @@shiftreg, al
@@next_tile:
    test @@shiftreg, 80h
    jnz short @@skip_tile
    push dword ptr [bp-6]
    call tiles_invalidate_around
@@skip_tile:
    shl @@shiftreg, 1
    add @@center_x, TILE_SUBPIXELS
    dec @@tiles_left
    jz short @@next_row
    test @@tiles_left, 7
    jnz short @@next_tile
    inc di
    jmp short @@new_byte
@@next_row:
    add di, 2
    add @@center_y, TILE_SUBPIXELS
    cmp @@center_y, PLAYFIELD_HEIGHT_SUBPIXELS
    jb short @@row_loop
    pop di
    leave
    ret 2
@TILES_BB_INVALIDATE_RAW$QI endp
tile_bb_mask_end label byte
TILE_BB_MASK_TEXT ends
end
