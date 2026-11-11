; TH05 five-decimal-digit popup encoder, original register-frame source.
; Near Pascal: (number WORD, last_digit near WORD pointer) -> width in AX.
.386
.model large
locals
include types.inc
include symbols.inc

main_03 group POINTNUM_DIGITS_REGISTER_TEXT
POINTNUM_DIGITS_REGISTER_TEXT segment byte public 'CODE' use16
assume cs:main_03, ds:DGROUP
public POINTNUM_DIGITS_SET, pointnum_digits_register_end
POINTNUM_DIGITS_SET proc near
    push bp
    mov bp, sp
    mov dx, ss:[bp + NUMBER_ARGUMENT]
    mov bx, ss:[bp + LAST_DIGIT_ARGUMENT]
    push si
    xor bp, bp
    mov si, offset _FIVE_DIGIT_POWERS_OF_10
    mov cx, DECIMAL_QUOTIENT_COUNT
@@decimal_loop:
    mov ax, dx
    xor dx, dx
    div word ptr [si]
    mov byte ptr [bx], al
    or al, al
    jz short @@next_digit
    or bp, bp
    jnz short @@next_digit
    mov bp, cx
@@next_digit:
    dec bx
    add si, WORD_BYTES
    loop @@decimal_loop
    mov byte ptr [bx], dl
    add bp, DISPLAY_WIDTH_BASE_DIGITS
    shl bp, PIXEL_WIDTH_SHIFT
    mov ax, bp
    pop si
    pop bp
    ret 4
POINTNUM_DIGITS_SET endp
    even
pointnum_digits_register_end label byte
POINTNUM_DIGITS_REGISTER_TEXT ends
end
