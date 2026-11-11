; TH05 OP/MAINE joystick state: far Pascal sensor and separate SAJOUT helper.
; The original single trailing zero after SAJOUT is NOT part of either PROC.
.386
.model large
include types.inc
include symbols.inc
_TEXT segment word public 'CODE' use16
assume cs:_TEXT, ds:DGROUP
public JS_SENSE, SAJOUT
JS_SENSE proc far
    pushf
    cli
    mov bl, JOY_PLAYER_ONE_SELECT
    call SOUND_JOY
    and ax, JOY_BUTTON_DIRECTION_BITS
    popf
    retf
JS_SENSE endp
SAJOUT proc near
    xchg dx, bx
    out dx, al
    xchg dx, bx
    in al, dx
    not al
    ret
SAJOUT endp
_TEXT ends
end
