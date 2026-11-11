; MAIN far Pascal joystick state, using the original resident near reader.
; SAJOUT immediately follows this near different *vendor* source owner.
.386
.model large
include types.inc
include symbols.inc
_TEXT segment word public 'CODE' use16
assume cs:_TEXT, ds:DGROUP
public JS_SENSE
JS_SENSE proc far
    pushf
    cli
    mov bl, JOY_PLAYER_ONE_SELECT
    call SOUND_JOY
    and ax, JOY_BUTTON_DIRECTION_BITS
    popf
    retf
JS_SENSE endp
_TEXT ends
end
