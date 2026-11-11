; TH05 MAINE: detect sound-board joystick support, then expose the original
; PSG joystick register helper immediately after the original far startup.
; This game-specific lean path intentionally omits the original Master's
; obsolete SAJ-98 search. The two sound register routines remain foreign.
.386
.model large
include types.inc
include symbols.inc

_TEXT segment word public 'CODE' use16
assume cs:_TEXT, ds:DGROUP
public JS_START, SOUND_JOY
JS_START proc far
    mov cx, JOY_POLL_COUNT
    mov dx, JOY_SOUND_STATUS_PORT
probe_board:
    in al, dx
    inc al
    jnz short board_present
    loop short probe_board
    xor ax, ax
    jmp short store_presence
board_present:
    pushf
    cli
    mov bh, JOY_PSG_REG_MIXER
    call SOUND_I
    and al, JOY_PSG_MIXER_LOW_BITS
    or al, JOY_PSG_ENABLE_JOYSTICK
    mov bl, al
    call SOUND_O
    popf
    mov ax, 1
store_presence:
    mov js_bexist, ax
    retf
JS_START endp
    even

; The native second procedure is a near function at _TEXT:2E70. It selects
; PSG joystick register 15 and reads the encoded state from port 018Ah.
SOUND_JOY proc near
    mov bh, 0fh
    call SOUND_O
    mov dx, JOY_SOUND_STATUS_PORT
    mov al, 0eh
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
