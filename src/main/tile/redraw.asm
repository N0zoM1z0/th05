; Redraw only dirty 16x8 halves, clearing each flag before the EGC copy.
; Candidate algorithm: ReC98 b6ba5b0a th04/main/tile/redraw.asm.
.386
.model large
locals
include types.inc
include symbols.inc
TILE_REDRAW_COLUMNS equ TILE_VISIBLE_COLUMNS
HALFTILE_H equ (TILE_H / 2)
HALFTILE_ROWS equ (TILE_SCREEN_ROWS * 2)

; SI is a cache index outside this macro and a VRAM offset inside it.
COPY_DIRTY_HALF macro
 local top_half, next_line
 push si
 mov byte ptr [bx], 0
 mov si, _tile_ring[si]
 test dh, 1
 jnz short top_half
 add si, (HALFTILE_H * TILE_VRAM_ROW_BYTES)
top_half:
 mov cx, HALFTILE_H
next_line:
 mov ax, es:[si]
 mov es:[di], ax
 add si, TILE_VRAM_ROW_BYTES
 add di, TILE_VRAM_ROW_BYTES
 loop next_line
 sub di, (HALFTILE_H * TILE_VRAM_ROW_BYTES)
 pop si
endm

main_01 group TILE_REDRAW_TEXT
TILE_REDRAW_TEXT segment word public 'CODE' use16
assume cs:main_01, ds:DGROUP
public @TILES_REDRAW_INVALIDATED$QV
@TILES_REDRAW_INVALIDATED$QV proc near
 push si
 push di
 call @egc_start_copy_noframe$qv
 mov ax, TILE_B_SEGMENT
 mov es, ax
 mov bx, offset _halftiles_dirty + ((HALFTILE_ROWS - 1) * TILE_CACHE_COLUMNS)
 mov di, (((400 - HALFTILE_H) * TILE_VRAM_ROW_BYTES) + TILE_VRAM_LEFT)
 mov dh, HALFTILE_ROWS
 mov si, ((TILE_SCREEN_ROWS - 1) * TILE_CACHE_ROW_BYTES)
@@next_row:
 mov dl, TILE_REDRAW_COLUMNS
@@next_tile:
 cmp byte ptr [bx], 0
 jz short @@clean
 COPY_DIRTY_HALF
@@clean:
 add di, TILE_VRAM_WORD_BYTES
 add si, TILE_WORD_BYTES
 inc bx
 dec dl
 jnz short @@next_tile
 test dh, 1
 jnz short @@same_cache_row
 add si, TILE_CACHE_ROW_BYTES
@@same_cache_row:
 sub si, ((TILE_CACHE_COLUMNS + TILE_REDRAW_COLUMNS) * TILE_WORD_BYTES)
 dec dh
 sub bx, (TILE_CACHE_COLUMNS + TILE_REDRAW_COLUMNS)
 sub di, ((TILE_REDRAW_COLUMNS * TILE_VRAM_WORD_BYTES) + (HALFTILE_H * TILE_VRAM_ROW_BYTES))
 jge short @@next_row
 call EGC_OFF
 pop di
 pop si
 ret
@TILES_REDRAW_INVALIDATED$QV endp
public tile_redraw_end
tile_redraw_end label byte
TILE_REDRAW_TEXT ends
end
