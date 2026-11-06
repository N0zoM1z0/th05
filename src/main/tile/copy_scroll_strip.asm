; Copy the newly exposed scrolling strip, splitting at a tile row and VRAM wrap.
; Procedure name is descriptive; the historical public name is unknown.
.386
.model large
locals
include types.inc
include symbols.inc
TILE_STRIP_COLUMNS equ TILE_VISIBLE_COLUMNS

; AX retains the cache index, DH the second fragment's height, DL the columns.
; BP is the EGC transfer word, not a stack frame. BL tracks the pending fragment.
COPY_SCROLL_COLUMN macro
 local next_line, finished, source_ready
 mov di, _tile_strip_destination
 add si, _tile_strip_source_skip
 add _tile_strip_destination, TILE_VRAM_WORD_BYTES
 mov bl, dh
next_line:
 mov bp, es:[si]
 mov es:[di], bp
 add si, TILE_VRAM_ROW_BYTES
 add di, TILE_VRAM_ROW_BYTES
 loop next_line
 or bl, bl
 jz short finished
 mov cl, bl
 mov bx, ax
 add bx, TILE_CACHE_ROW_BYTES
 cmp di, (400 * TILE_VRAM_ROW_BYTES)
 jb short source_ready
 sub di, (400 * TILE_VRAM_ROW_BYTES)
 sub bx, TILE_CACHE_BYTES
source_ready:
 mov si, _tile_ring[bx]
 xor bx, bx
 jmp short next_line
finished:
 mov cx, _tile_strip_first_rows
 add ax, TILE_WORD_BYTES
 mov bx, ax
 mov si, _tile_ring[bx]
endm

main_01 group TILE_STRIP_TEXT
TILE_STRIP_TEXT segment word public 'CODE' use16
assume cs:main_01, ds:DGROUP
public _tiles_copy_scroll_strip
_tiles_copy_scroll_strip proc near
 push bp
 push si
 push di
 mov ax, TILE_B_SEGMENT
 mov es, ax
 mov dx, _scroll_line

 ; Destination is scroll_line * 80 + playfield_left / 8.
 mov ax, TILE_VRAM_LEFT
 mov cx, dx
 shl cx, 6
 add ax, cx
 shr cx, 2
 add ax, cx
 mov _tile_strip_destination, ax

 ; The cache row is scroll_line / 16; its WORD stride is 64 bytes.
 mov ax, dx
 shr ax, 4
 shl ax, 6
 mov bx, ax
 mov si, _tile_ring[bx]

 ; Skip the already visible scanlines in the first tile row.
 mov bx, dx
 and bx, (TILE_H - 1)
 mov cx, bx
 shl cx, 6
 mov dx, cx
 shr cx, 2
 add dx, cx
 mov _tile_strip_source_skip, dx

 ; Split the requested height at the next tile boundary; no bounds checks.
 xor ch, ch
 mov cl, _tile_strip_height
 mov bh, bl
 add bl, cl
 cmp bl, TILE_H
 jbe short @@single_fragment
 sub bl, TILE_H
 mov cl, TILE_H
 sub cl, bh
 mov dh, bl
 jmp short @@fragments_ready
@@single_fragment:
 xor dh, dh
@@fragments_ready:
 mov dl, TILE_STRIP_COLUMNS
 mov _tile_strip_first_rows, cx
@@next_column:
 COPY_SCROLL_COLUMN
 dec dl
 jnz short @@next_column
 pop di
 pop si
 pop bp
 ret
_tiles_copy_scroll_strip endp
public tile_copy_scroll_strip_end
tile_copy_scroll_strip_end label byte
TILE_STRIP_TEXT ends
end
