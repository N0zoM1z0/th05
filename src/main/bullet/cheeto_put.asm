; AX=pixel left, DX=ring top, BX=cel; caller supplies ES and GRCG state.
.386
.model large
locals
include types.inc
include symbols.inc
CHEETO_DRAW_ROWS equ CHEETO_H

; The row worker returns its remaining-row test in ZF (DEC CH).
; Only a sprite intersecting the bottom needs per-row wrap checks.
CHEETO_RING_PASS macro row_worker
 local before_wrap, after_wrap
 mov ch, CHEETO_DRAW_ROWS
 cmp di, ((VRAM_HEIGHT - CHEETO_DRAW_ROWS + 1) * VRAM_ROW_BYTES)
 jb short after_wrap
before_wrap:
 call row_worker
 cmp di, VRAM_PLANE_BYTES
 jb short before_wrap
 sub di, VRAM_PLANE_BYTES
 even
after_wrap:
 call row_worker
 jnz short after_wrap
endm

; Emit the two shifted words of EAX, carrying each low-byte overflow in BL.
; BH counts words, DL masks the first byte, CL supplies the pixel phase.
CHEETO_SHIFT_WORDS macro
 local next_word
next_word:
 ror ax, cl
 mov dh, al
 and al, dl
 xor dh, al
 or al, bl
 mov bl, dh
 stosw
 shr eax, WORD_BITS
 dec bh
 jnz short next_word
endm

main_01 group MAIN_01_TEXT
MAIN_01_TEXT segment word public 'CODE' use16
assume cs:main_01, ds:DGROUP
public @cheeto_put
@cheeto_put proc near
 push si
 push di
 shl bx, CHEETO_CEL_SHIFT
 mov si, bx
 add si, offset _bb_cheeto
 mov di, dx
 shl di, 2
 add di, dx
 shl di, 4
 mov cl, al
 and cl, (BYTE_BITS - 1)
 shr ax, 3
 add di, ax
 mov dl, 0ffh
 shr dl, cl
 test di, 1
 jnz short @@odd
 even
 CHEETO_RING_PASS @@row_even
 jmp short @@done
 even
@@odd:
 CHEETO_RING_PASS @@row_odd
@@done:
 pop di
 pop si
 ret

; An even destination starts with a word and needs a final carry byte.
@@row_even:
 xor bl, bl
 mov bh, CHEETO_ROW_WORDS
 lodsd
 CHEETO_SHIFT_WORDS
 mov es:[di], bl
 add di, (VRAM_ROW_BYTES - CHEETO_ROW_BYTES)
 dec ch
 ret

; An odd destination peels one byte before the aligned word stores.
@@row_odd:
 mov bh, CHEETO_ROW_WORDS
 lodsd
 ror al, cl
 mov bl, al
 and al, dl
 stosb
 xor bl, al
 shr eax, BYTE_BITS
 CHEETO_SHIFT_WORDS
 add di, (VRAM_ROW_BYTES - CHEETO_ROW_BYTES - 1)
 dec ch
 ret
@cheeto_put endp
public cheeto_put_end
cheeto_put_end label byte
MAIN_01_TEXT ends
end
