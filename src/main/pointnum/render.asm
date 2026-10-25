; Point popup list and white/yellow tile selection, private register blitter ABI.
.386
.model large
locals
include types.inc
include symbols.inc
POINTNUM_FIELD_LEFT equ PLAYFIELD_LEFT
main_01 group MAIN_01_TEXT
MAIN_01_TEXT segment word public 'CODE' use16
assume cs:main_01, ds:DGROUP
extrn SCROLL_SUBPIXEL_Y_TO_VRAM_SEG1:near
extrn @pointnum_put:near
public POINTNUMS_RENDER
POINTNUMS_RENDER proc near
 push si
 push di
 mov di, offset _pointnums_alive
 mov si, [di]
 or si, si
 jz short @@done
 push bp
 mov ax, VRAM_BLUE
 mov es, ax
 ; Tile writes are atomic; the native path enables interrupts afterwards.
 mov dx, GRCG_TILE_PORT
 mov al, 0ffh
 cli
 out dx, al
 out dx, al
 out dx, al
 out dx, al
 sti
@@number:
 cmp si, _pointnum_first_yellow_alive
 jnz short @@coords
 mov dx, GRCG_TILE_PORT
 mov al, 0ffh
 cli
 out dx, al
 out dx, al
 not al
 out dx, al
 not al
 out dx, al
 sti
@@coords:
 mov bp, [si+pointnum_t.PN_width]
 shr bp, 1
 mov dx, [si+pointnum_t.PN_center_x]
 sar dx, 4
 add dx, POINTNUM_FIELD_LEFT
 sub dx, bp
 shr bp, 2
 ; Exclude trailing zero, then compensate for the signed decrement loop.
 sub bp, 2
 mov ax, [si+pointnum_t.PN_center_y]
 add ax, ((PLAYFIELD_TOP - (POINTNUM_H / 2)) shl 4)
 push ax
 call SCROLL_SUBPIXEL_Y_TO_VRAM_SEG1
 add si, pointnum_t.PN_digits
 add si, bp
@@digit:
 xor ch, ch
 mov cl, [si]
 call @pointnum_put
 dec si
 dec bp
 jns short @@digit
 xor cx, cx
 call @pointnum_put
 add di, 2
 mov si, [di]
 or si, si
 jnz short @@number
 pop bp
@@done:
 pop di
 pop si
 ret
POINTNUMS_RENDER endp
 even
public pointnums_render_end
pointnums_render_end label byte
MAIN_01_TEXT ends
end
