; Fill the visible cache columns from MAP sections in bottom-to-top order.
; Candidate: ReC98 b6ba5b0a th04/main/tile/fill_ini.asm, GAME5 branch.
.386
.model large
locals
include types.inc
include symbols.inc
TILE_FILL_COLUMNS equ TILE_VISIBLE_COLUMNS

; SI/DI end at the preceding MAP/cache row after each partial-row copy.
COPY_SECTION_ROWS macro
 local next_row
 mov ah, TILE_SECTION_ROWS
next_row:
 mov cx, ((TILE_FILL_COLUMNS * TILE_WORD_BYTES) / 4)
 rep movsd
 sub di, ((TILE_CACHE_COLUMNS + TILE_FILL_COLUMNS) * TILE_WORD_BYTES)
 sub si, ((TILE_CACHE_COLUMNS + TILE_FILL_COLUMNS) * TILE_WORD_BYTES)
 dec ah
 jnz short next_row
endm

main_01 group TILE_FILL_TEXT
TILE_FILL_TEXT segment word public 'CODE' use16
assume cs:main_01, ds:DGROUP
public TILES_FILL_INITIAL
TILES_FILL_INITIAL proc near
 push di
 push si
 push ds
 mov bx, _std_map_section_p
 sub bx, (TILE_SECTION_ROWS - 1)
 mov di, offset _tile_ring
 add di, ((TILE_SCREEN_ROWS - 1) * TILE_CACHE_ROW_BYTES)
 xor dx, dx
 mov ax, ds
 mov es, ax
 mov ax, _std_seg
 mov fs, ax
 mov ax, _map_seg
 mov ds, ax
 mov al, (TILE_SCREEN_ROWS / TILE_SECTION_ROWS)
@@next_section:
 xor dx, dx
 ; TH05 STD IDs already contain the WORD table's byte offset.
 mov dl, fs:[bx]
 mov si, dx
 mov si, es:_TILE_SECTION_OFFSETS[si]
 add si, ((TILE_SECTION_ROWS - 1) * TILE_CACHE_ROW_BYTES)
 COPY_SECTION_ROWS
 inc bx
 dec al
 jnz short @@next_section
 pop ds
 pop si
 pop di
 ret
TILES_FILL_INITIAL endp
 even
public tile_fill_initial_end
tile_fill_initial_end label byte
TILE_FILL_TEXT ends
end
