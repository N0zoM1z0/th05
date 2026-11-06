; Tiny sprites store a color/80h WORD, fixed-size monochrome rows, then the
; next color header. A header whose low byte differs from80h ends the sprite.
TINY16_W equ 16
TINY16_H equ 16
TINY32_W equ 32
TINY32_H equ 32
TINY_PIXEL_PHASES equ 8
TINY_COLOR_MARKER equ 080h
TINY_COLOR_PLANES equ 4
TINY_TILE_PORT equ 07eh
TINY_ROW_BYTES equ (640 / 8)
TINY_SCREEN_H equ 400
TINY_PLANE_BYTES equ (TINY_ROW_BYTES * TINY_SCREEN_H)
TINY_STACK_WORD equ 2

; Hybrid near Pascal entry: AX=left, DX=top, stack WORD=pattern, ES=VRAM.
TINY_ENTER macro
 mov bx, sp
 push ds
 push si
 push di
 mov bx, ss:[bx+TINY_STACK_WORD]
 shl bx, 1
 mov ds, _super_patdata[bx]
 mov bx, dx
 shl bx, 2
 add bx, dx
 shl bx, 4
 mov cx, ax
 and cx, TINY_PIXEL_MASK
 shr ax, 3
 add bx, ax
endm

; Expand AH's four color bits into the GRCG's four byte tile registers.
TINY_SET_COLOR macro
 rept TINY_COLOR_PLANES
  shr ah, 1
  sbb al, al
  out TINY_TILE_PORT, al
 endm
endm

TINY_RETURN macro
 pop di
 pop si
 pop ds
 ret TINY_STACK_WORD
 even
endm
