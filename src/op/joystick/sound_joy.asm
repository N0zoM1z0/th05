; TH05 OP SOUND_JOY: read the original PC-98 PSG joystick input register.
.386
.model large
include types.inc
include symbols.inc
JOY_PSG_INPUT_REGISTER equ 0eh
_TEXT segment word public 'CODE' use16
assume cs:_TEXT, ds:DGROUP
public SOUND_JOY
SOUND_JOY proc near
    mov bh, 0fh
    call SOUND_O
    mov dx, JOY_SOUND_STATUS_PORT
    mov al, JOY_PSG_INPUT_REGISTER
    out dx, al
    inc dx
    inc dx
    in al, dx
    not al
    ret
SOUND_JOY endp
    even
_TEXT ends
end
