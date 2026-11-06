; Game-adapted Master tiny renderer, with hybrid near entry and blank third
; byte omission. Koizuka/ZUN ancestry: ReC98 b6ba5b0a
; th04/formats/z_super_roll_put_tiny.asm and primary Master0.23 SUPERRPT.ASM.
.386
.model large
locals
include types.inc
include symbols.inc
TINY_PIXEL_MASK equ (TINY_PIXEL_PHASES - 1)

; The even path always writes its word, omitting only an empty carry byte.
TINY16_EVEN_ROW macro
 local carry_blank
 lodsw
 ror ax, cl
 mov dh, al
 and al, dl
 mov es:[di], ax
 xor al, dh
 jz short carry_blank
 mov es:[di+2], al
carry_blank:
endm

; The odd path always writes both its leading byte and following word.
TINY16_ODD_ROW macro
 lodsw
 ror ax, cl
 mov dh, al
 and al, dl
 mov es:[di], al
 xor al, dh
 xchg ah, al
 mov es:[di+1], ax
endm

; Repeat the fixed-height color plane, splitting once at the VRAM ring edge.
TINY16_RING_ROWS macro draw_row
 local before_wrap, after_wrap
 mov ch, TINY16_H
 mov di, bx
 cmp di, ((TINY_SCREEN_H - TINY16_H + 1) * TINY_ROW_BYTES)
 jb short after_wrap
 even
before_wrap:
 draw_row
 add di, TINY_ROW_BYTES
 dec ch
 cmp di, TINY_PLANE_BYTES
 jb short before_wrap
 sub di, TINY_PLANE_BYTES
 even
after_wrap:
 draw_row
 add di, TINY_ROW_BYTES
 dec ch
 jnz short after_wrap
endm

main_01 group TINY16_TEXT
TINY16_TEXT segment word public 'CODE' use16
assume cs:main_01, ds:DGROUP
public Z_SUPER_ROLL_PUT_TINY_16X16_RAW
Z_SUPER_ROLL_PUT_TINY_16X16_RAW proc near
 TINY_ENTER
 xor si, si
 lodsw
 cmp al, TINY_COLOR_MARKER
 jnz short @@even_return
 mov dl, 0ffh
 shr dl, cl
 test bl, 1
 jnz short @@odd_color
 even
@@even_color:
 TINY_SET_COLOR
 TINY16_RING_ROWS TINY16_EVEN_ROW
 lodsw
 cmp al, TINY_COLOR_MARKER
 jz short @@even_color
@@even_return:
 TINY_RETURN
 even
@@odd_color:
 TINY_SET_COLOR
 TINY16_RING_ROWS TINY16_ODD_ROW
 lodsw
 cmp al, TINY_COLOR_MARKER
 jz short @@odd_color
 TINY_RETURN
Z_SUPER_ROLL_PUT_TINY_16X16_RAW endp
public tiny16_end
tiny16_end label byte
TINY16_TEXT ends
end
