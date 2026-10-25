; Semantic original-ASM reconstruction: 16x16 monochrome ring blit.
; Candidate algorithm: pinned ReC98 b6ba5b0a th05/formats/super_roll_put_16x16_m.asm.
.386
.model large
locals
include types.inc
include symbols.inc

; A shifted row at an even destination byte: word followed by its carry byte.
SHIFTED_EVEN_ROW macro
 local word_blank, carry_blank
 lodsw
 ror ax, cl
 mov bl, al
 and al, dl
 or ax, ax
 jz short word_blank
 mov es:[di], ax
word_blank:
 and bl, dh
 jz short carry_blank
 mov es:[di+2], bl
carry_blank:
endm

; Byte-aligned rows need no rotation or third destination byte.
ALIGNED_ROW macro
 local blank
 lodsw
 or ax, ax
 jz short blank
 mov es:[di], ax
blank:
endm

; An odd destination byte uses a leading byte and then an aligned word.
SHIFTED_ODD_ROW macro
 local first_blank, word_blank
 lodsw
 ror ax, cl
 mov bh, al
 and al, dl
 jz short first_blank
 mov es:[di], al
first_blank:
 and bh, dh
 mov bl, ah
 or bx, bx
 jz short word_blank
 mov es:[di+1], bx
word_blank:
endm

; Split at the video ring boundary, leaving the remaining rows a simple loop.
BLIT_ROWS macro draw_row
 local before_wrap, remaining
 cmp di, (RES_Y - SPRITE16_H + 1) * ROW_SIZE
 jb short remaining
 even
before_wrap:
 draw_row
 add di, ROW_SIZE
 dec ch
 cmp di, PLANE_SIZE
 jb short before_wrap
 sub di, PLANE_SIZE
 even
remaining:
 draw_row
 add di, ROW_SIZE
 dec ch
 jnz short remaining
endm

main_01 group SPRITE16_TEXT
SPRITE16_TEXT segment word public 'CODE' use16
assume cs:main_01
public Z_SUPER_ROLL_PUT_16X16_MONO_RAW
Z_SUPER_ROLL_PUT_16X16_MONO_RAW proc near
 ; Hybrid graphics ABI: AX=top, CX=left, stack word=pattern; ES and DF incoming.
 mov bx, sp
 push ds
 push si
 push di
 ; One row occupies 80 bytes; the pattern bank holds segment handles.
 mov di, ax
 shl ax, 2
 add di, ax
 shl di, 4
 mov ax, cx
 shr ax, 3
 add di, ax
 mov bx, ss:[bx+NEAR_RETURN_BYTES]
 shl bx, 1
 mov ds, _super_patdata[bx]
 xor si, si
 mov ch, SPRITE16_H
 and cl, 7
 jz short @@aligned
 ; DL selects the leading bits; DH selects the rotated carry bits.
 mov dx, 0FFFFh
 shr dl, cl
 xor dh, dl
 test al, 1
 jnz short @@odd
 BLIT_ROWS SHIFTED_EVEN_ROW
 jmp short @@done
@@aligned:
 BLIT_ROWS ALIGNED_ROW
 jmp short @@done
@@odd:
 BLIT_ROWS SHIFTED_ODD_ROW
@@done:
 pop di
 pop si
 pop ds
 ret NEAR_RETURN_BYTES
Z_SUPER_ROLL_PUT_16X16_MONO_RAW endp
 even
public super_roll_16x16_end
super_roll_16x16_end label byte
SPRITE16_TEXT ends
end
