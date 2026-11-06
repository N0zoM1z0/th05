; Copy the full tile ring to the visible playfield using the EGC latch.
; Candidate: ReC98 b6ba5b0a th04/main/tile/render_a.asm, renderer only.
.386
.model large
locals
include types.inc
include symbols.inc
TILE_RENDER_COLUMNS equ TILE_VISIBLE_COLUMNS

; The source and destination words are EGC latch operations across all planes.
COPY_TILE_COLUMN macro
 local next_line
 mov si, [bx]
 mov cx, TILE_H
 even
next_line:
 mov ax, es:[si]
 mov es:[di], ax
 add si, TILE_VRAM_ROW_BYTES
 add di, TILE_VRAM_ROW_BYTES
 loop next_line
 sub di, ((TILE_H * TILE_VRAM_ROW_BYTES) - TILE_VRAM_WORD_BYTES)
endm

main_01 group TILE_RENDER_TEXT
TILE_RENDER_TEXT segment word public 'CODE' use16
assume cs:main_01, ds:DGROUP
public @TILES_RENDER_ALL$QV
@TILES_RENDER_ALL$QV proc near
 push si
 push di
 call @egc_start_copy_noframe$qv
 mov di, (((400 - TILE_H) * TILE_VRAM_ROW_BYTES) + TILE_VRAM_LEFT)
 mov bx, offset _tile_ring + ((TILE_SCREEN_ROWS - 1) * TILE_CACHE_ROW_BYTES)
 mov ax, TILE_B_SEGMENT
 mov es, ax
@@next_row:
 mov dl, TILE_RENDER_COLUMNS
@@next_tile:
 COPY_TILE_COLUMN
 add bx, TILE_WORD_BYTES
 dec dl
 jnz short @@next_tile
 sub bx, ((TILE_CACHE_COLUMNS + TILE_RENDER_COLUMNS) * TILE_WORD_BYTES)
 sub di, ((TILE_H * TILE_VRAM_ROW_BYTES) + (TILE_VRAM_WORD_BYTES * TILE_RENDER_COLUMNS))
 jge short @@next_row
 call EGC_OFF
 pop di
 pop si
 ret
@TILES_RENDER_ALL$QV endp
public tile_render_all_end
tile_render_all_end label byte
TILE_RENDER_TEXT ends
end
