; Game-adapted 32x32 color tiny blit. Candidate semantics: ReC98 b6ba5b0a
; th04/formats/z_super_roll_put_tiny.asm, derived from Koizuka's Master tiny
; renderer and adapted by ZUN. Literal historical source remains unproved.
.386
.model large
locals
include types.inc
include symbols.inc
TINY_PIXEL_MASK equ (TINY_PIXEL_PHASES - 1)

; A row worker preserves CL/DL, advances SI/DI and returns DEC CH in ZF.
TINY32_RING_ROWS macro row_worker
 local before_wrap, after_wrap
 mov ch, TINY32_H
 mov di, cs:srpt32x32_vram_topleft
 cmp di, ((TINY_SCREEN_H - TINY32_H + 1) * TINY_ROW_BYTES)
 jb short after_wrap
before_wrap:
 call row_worker
 cmp di, TINY_PLANE_BYTES
 jb short before_wrap
 sub di, TINY_PLANE_BYTES
 even
after_wrap:
 call row_worker
 jnz short after_wrap
endm

; Consume the next two source words, preserving each low-byte spill in BL.
; Skip blank words; a nonblank word still writes both bytes, including zeros.
TINY32_SHIFT_WORDS macro
 local next_word, blank
next_word:
 ror ax, cl
 mov dh, al
 and al, dl
 xor dh, al
 or al, bl
 mov bl, dh
 or ax, ax
 jz short blank
 mov es:[di], ax
blank:
 add di, 2
 shr eax, 16
 dec bh
 jnz short next_word
endm

main_01 group TINY32_TEXT
TINY32_TEXT segment word public 'CODE' use16
assume cs:main_01, ds:DGROUP
public Z_SUPER_ROLL_PUT_TINY_32X32_RAW
Z_SUPER_ROLL_PUT_TINY_32X32_RAW proc near
 TINY_ENTER
 ; This real writable CODE word is foreign to the complete procedure scope.
 mov cs:srpt32x32_vram_topleft, bx
 xor si, si
 lodsw
 cmp al, TINY_COLOR_MARKER
 jnz short @@even_return
 mov dl, 0ffh
 shr dl, cl
 test bl, 1
 jnz short @@odd_color
@@even_color:
 call @@set_color
 TINY32_RING_ROWS @@even_row
 lodsw
 cmp al, TINY_COLOR_MARKER
 jz short @@even_color
@@even_return:
 TINY_RETURN
@@odd_color:
 call @@set_color
 TINY32_RING_ROWS @@odd_row
 lodsw
 cmp al, TINY_COLOR_MARKER
 jz short @@odd_color
 TINY_RETURN

@@set_color:
 TINY_SET_COLOR
 ret
 even

; Even destination: two aligned words followed by a possible fifth byte.
@@even_row:
 xor bl, bl
 mov bh, (TINY32_W / 16)
 lodsd
 TINY32_SHIFT_WORDS
 or bl, bl
 jz short @@even_carry_blank
 mov es:[di], bl
@@even_carry_blank:
 add di, (TINY_ROW_BYTES - (TINY32_W / 8))
 dec ch
 ret
 even

; Odd destination: peel one byte, then use the same aligned word operation.
@@odd_row:
 mov bh, (TINY32_W / 16)
 lodsd
 ror al, cl
 mov bl, al
 and al, dl
 jz short @@odd_first_blank
 mov es:[di], al
@@odd_first_blank:
 xor bl, al
 inc di
 shr eax, 8
 TINY32_SHIFT_WORDS
 add di, (TINY_ROW_BYTES - (TINY32_W / 8) - 1)
 dec ch
 ret
Z_SUPER_ROLL_PUT_TINY_32X32_RAW endp
public tiny32_end
tiny32_end label byte
TINY32_TEXT ends
end
