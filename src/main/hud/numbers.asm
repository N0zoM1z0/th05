; Two HUD number entries sharing one decimal/string-rendering tail.
; Reviewed native ASM inference; the divisor table and row remain foreign.
.386
.model large
locals
include types.inc
include symbols.inc

HUD_SMALL_LEADING_DIGITS equ (HUD_SMALL_DIGITS - 1)

MAIN_03_TEXT segment word public 'CODE' use16
assume cs:MAIN_03_TEXT, ds:DGROUP
public @HUD_5_DIGIT_PUT$QUIUIUIUI
@HUD_5_DIGIT_PUT$QUIUIUIUI proc far
 push bp
 mov bp, sp
 push di
 ; Keep these address computations as LEA, as in the semantic ASM donor.
 pushstate
 nosmart
 lea di, [_hud_gaiji_row + (HUD_SCORE_DIGITS - HUD_SMALL_DIGITS)]
 movzx edx, word ptr [bp+HUD_NUMBER_ARG_VALUE]
 lea bx, [_SEVEN_DIGIT_POWERS_OF_10 + (HUD_SCORE_DIVISOR_INDEX * HUD_DIVISOR_BYTES)]
 popstate
 mov ax, [bp+HUD_NUMBER_ARG_ATTRIBUTE]
 mov cx, HUD_SMALL_LEADING_DIGITS
 jmp short hud_number_digits
@HUD_5_DIGIT_PUT$QUIUIUIUI endp
 even

public @HUD_POINTS_PUT$QUIUIUL
@HUD_POINTS_PUT$QUIUIUL proc far
 push bp
 mov bp, sp
 push di
 mov edx, dword ptr [bp+HUD_POINTS_ARG_VALUE]
 mov di, offset _hud_gaiji_row
 mov ax, HUD_WHITE
 ; Score display always appends a zero in the continues-used column.
 mov _hud_gaiji_row[HUD_SCORE_DIGITS - 1], HUD_DIGIT_ZERO
 mov bx, offset _SEVEN_DIGIT_POWERS_OF_10
 mov cx, (HUD_SCORE_DIGITS - 2)

public hud_number_digits
hud_number_digits:
 push word ptr [bp+HUD_NUMBER_ARG_LEFT]
 push word ptr [bp+HUD_NUMBER_ARG_ROW]
 push ds
 push di
 push ax
 mov ax, ds
 mov es, ax
@@digit:
 mov eax, edx
 xor edx, edx
 div dword ptr [bx]
 ; CH accumulates previous nonzero digits; CL is the remaining loop count.
 or ch, al
 jz short @@leading_zero
 add al, HUD_DIGIT_ZERO
 jmp short @@store
@@leading_zero:
 mov al, HUD_NUMBER_EMPTY
@@store:
 stosb
 add bx, HUD_DIVISOR_BYTES
 dec cl
 jnz short @@digit
 ; The last remainder is the units digit, including for an all-zero number.
 add dl, HUD_DIGIT_ZERO
 mov [di], dl
 call GAIJI_PUTSA
 pop di
 pop bp
 retf HUD_NUMBER_ARGUMENT_BYTES
@HUD_POINTS_PUT$QUIUIUL endp
public hud_numbers_end
hud_numbers_end label byte
MAIN_03_TEXT ends
end
