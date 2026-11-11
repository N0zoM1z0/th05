; TH05 ZUN.COM -O: original-register PMD/ADPCM RAM diagnostic.
; This is a semantic register/port reconstruction, not historical source.
.386
.model tiny
locals
.code
org 100h

DOS_INT equ 021h
DOS_EXIT equ 04Ch
PC98_SOUND_PORT_PRIMARY equ 088h
PC98_SOUND_PORT_EXTENSION equ 0188h
PC98_SOUND_PIO_SELECT equ 0A460h
PC98_SOUND_DIP_SELECT equ 0A66Eh
PC98_SOUND_CONTROL_PORT equ 05Fh
BIOS_BOARD_ID_SEG equ 0FD80h
BIOS_BOARD_ID_MARK equ 02A27h
BOARD_EXTENDED_MODEL_MIN equ 06h
FM_REGISTER_DELAY equ 100
ADPCM_WORDS equ 32
ADPCM_TEST_LENGTH equ 020h
ADPCM_TIMEOUT equ 02710h

public ADPCM_DIAGNOSTIC_ENTRY, CHECK_BOARD, TRY_EXTENDED_BOARD
public TRY_CLASSIC_BOARD, CHECK_RAM, ADPCM_SETUP
public ADPCM_DRAIN, ADPCM_RECEIVE_ONCE, CHECK_RAM_SIGNATURE, WRITE_ADPCM_REGISTER

ADPCM_DIAGNOSTIC_ENTRY proc near
    cld
    mov ax, cs
    mov ds, ax
    mov es, ax
    mov byte ptr access_extended, 0
    mov si, 080h
@@skip_spaces:
    lodsb
    cmp al, ' '
    jz short @@skip_spaces
    cmp al, '8'
    jnz short @@run_test
    mov byte ptr access_extended, 1
@@run_test:
    call CHECK_BOARD
    mov ah, DOS_EXIT
    mov al, exit_status
    int DOS_INT
ADPCM_DIAGNOSTIC_ENTRY endp

CHECK_BOARD proc near
    cmp access_extended, 1
    jz short @@extended_first
    call TRY_CLASSIC_BOARD
    jnb @@check_second_bank
@@extended_first:
    call TRY_EXTENDED_BOARD
    jnb @@check_second_bank
    cmp access_extended, 1
    jnz short @@no_fallback
    call TRY_CLASSIC_BOARD
    jnb @@check_second_bank
@@no_fallback:
    mov exit_status, 1
    mov ah, 4
    mov dx, PC98_SOUND_PORT_PRIMARY
    cmp byte ptr preferred_board_port, 0FFh
    je short @@loop_sound_port
    mov dh, preferred_board_port
    mov ah, 1
@@loop_sound_port:
    cli
    mov cx, FM_REGISTER_DELAY
@@wait_before_index:
    loop @@wait_before_index
    mov al, 0Bh
    out dx, al
    mov cx, FM_REGISTER_DELAY
@@wait_index:
    loop @@wait_index
    add dx, 2
    mov al, 0AAh
    out dx, al
    mov cx, FM_REGISTER_DELAY
@@wait_data:
    loop @@wait_data
    in al, dx
    sti
    sub dx, 2
    cmp al, 0AAh
    jnz short @@wrong_sound_port
    jmp BOARD_PROBE_SUCCESS
@@wrong_sound_port:
    dec ah
    jnz short @@next_board
    jmp BOARD_PROBE_FAILURE
@@next_board:
    add dx, 0100h
    jmp short @@loop_sound_port
@@check_second_bank:
    cmp exit_status, 2
    jb short @@finish
    call CHECK_RAM
    jb short @@finish
    add exit_status, 2
@@finish:
    clc
    ret
CHECK_BOARD endp

TRY_CLASSIC_BOARD proc near
    mov exit_status, 3
    mov card_has_extended_bios, 0
    mov ax, BIOS_BOARD_ID_SEG
    mov es, ax
    cmp word ptr es:[2], BIOS_BOARD_ID_MARK
    jne short @@probe_io
    mov card_has_extended_bios, 1
    cmp byte ptr es:[4], BOARD_EXTENDED_MODEL_MIN
    jae short @@probe_io
    jmp BOARD_PROBE_FAILURE
@@probe_io:
    mov dx, PC98_SOUND_PIO_SELECT
    in al, dx
    cmp al, 0FFh
    jne short @@config_io
    jmp BOARD_PROBE_FAILURE
@@config_io:
    out PC98_SOUND_CONTROL_PORT, al
    and al, 0FCh
    out dx, al
    mov ah, 2
    mov dx, PC98_SOUND_PORT_EXTENSION
    cmp preferred_board_port, 0FFh
    je short @@loop_port
    mov dh, preferred_board_port
    mov ah, 1
@@loop_port:
    cli
    mov al, 0FFh
    mov cx, FM_REGISTER_DELAY
@@wait_addr:
    loop @@wait_addr
    out dx, al
    add dx, 2
    mov cx, FM_REGISTER_DELAY
@@wait_recv:
    loop @@wait_recv
    in al, dx
    sti
    sub dx, 2
    dec al
    jnz short @@read_failed
    add dx, 4
    in al, dx
    mov bl, al
    add dx, 2
    in al, dx
    sub dx, 6
    and al, bl
    inc al
    jz short @@program_board
@@read_failed:
    dec ah
    jnz short @@try_next
    jmp BOARD_PROBE_FAILURE
@@try_next:
    inc dh
    jmp short @@loop_port
@@program_board:
    push dx
    mov dx, PC98_SOUND_PIO_SELECT
    cli
    in al, dx
    out PC98_SOUND_CONTROL_PORT, al
    and al, 0FCh
    or al, 1
    out dx, al
    mov dx, PC98_SOUND_DIP_SELECT
    in al, dx
    out PC98_SOUND_CONTROL_PORT, al
    and al, 0FEh
    out dx, al
    cmp card_has_extended_bios, 0
    je short @@keep_board
    mov al, 1
    out 06Eh, al
@@keep_board:
    sti
    pop dx
    jmp short BOARD_PROBE_SUCCESS
TRY_CLASSIC_BOARD endp

TRY_EXTENDED_BOARD proc near
    mov exit_status, 2
    mov card_has_extended_bios, 0
    mov ax, BIOS_BOARD_ID_SEG
    mov es, ax
    cmp word ptr es:[2], BIOS_BOARD_ID_MARK
    jne short @@probe_io
    mov card_has_extended_bios, 1
    cmp byte ptr es:[4], BOARD_EXTENDED_MODEL_MIN
    jb short @@start_port
@@probe_io:
    mov dx, PC98_SOUND_PIO_SELECT
    in al, dx
    cmp al, 0FFh
    je short @@start_port
    out PC98_SOUND_CONTROL_PORT, al
    and al, 0FCh
    out dx, al
@@start_port:
    mov ah, 4
    mov dx, PC98_SOUND_PORT_PRIMARY
    cmp preferred_board_port, 0FFh
    je short @@loop_port
    mov dh, preferred_board_port
    mov ah, 1
@@loop_port:
    cli
    mov al, 0FFh
    mov cx, FM_REGISTER_DELAY
@@wait_addr:
    loop @@wait_addr
    out dx, al
    add dx, 2
    mov cx, FM_REGISTER_DELAY
@@wait_recv:
    loop @@wait_recv
    in al, dx
    sti
    sub dx, 2
    dec al
    jnz short @@port_failed
    add dx, 4
    in al, dx
    mov bl, al
    add dx, 2
    in al, dx
    sub dx, 6
    and al, bl
    inc al
    jnz short BOARD_PROBE_SUCCESS
@@port_failed:
    dec ah
    jz short BOARD_PROBE_FAILURE
    add dx, 0100h
    jmp short @@loop_port
TRY_EXTENDED_BOARD endp

BOARD_PROBE_SUCCESS label near
    mov io_address_port, dx
    add dx, 2
    mov io_data_port, dx
    add dx, 2
    mov io_status_port, dx
    add dx, 2
    mov io_transfer_port, dx
    clc
    ret
BOARD_PROBE_FAILURE label near
    mov exit_status, 0
    stc
    ret

CHECK_RAM proc near
    mov ax, cs
    mov ds, ax
    mov es, ax
    call ADPCM_SETUP
    jc short @@fail
    call ADPCM_DRAIN
    call CHECK_RAM_SIGNATURE
    jz short @@ok
@@fail:
    stc
    ret
@@ok:
    clc
    ret
CHECK_RAM endp

ADPCM_SETUP proc near
    mov dx, 0001h
    call WRITE_ADPCM_REGISTER
    mov dx, 01017h
    call WRITE_ADPCM_REGISTER
    mov dx, 01080h
    call WRITE_ADPCM_REGISTER
    mov dx, 00060h
    call WRITE_ADPCM_REGISTER
    mov dx, 00102h
    call WRITE_ADPCM_REGISTER
    mov dx, 00CFFh
    call WRITE_ADPCM_REGISTER
    inc dh
    call WRITE_ADPCM_REGISTER
    mov bx, 01FFFh
    mov dh, 2
    mov dl, bl
    call WRITE_ADPCM_REGISTER
    inc dh
    mov dl, bh
    call WRITE_ADPCM_REGISTER
    mov dx, 004FFh
    call WRITE_ADPCM_REGISTER
    inc dh
    call WRITE_ADPCM_REGISTER
    mov si, offset ram_signature
    mov cx, ADPCM_WORDS
    mov dx, io_status_port
    mov bx, io_transfer_port
@@transfer_loop:
    cli
    in al, dx
@@wait_ready:
    in al, dx
    or al, al
    js short @@wait_ready
    mov al, 8
    out dx, al
    push cx
    mov cx, FM_REGISTER_DELAY
@@wait_delay:
    loop @@wait_delay
    pop cx
    xchg bx, dx
    lodsb
    out dx, al
    sti
    xchg dx, bx
    push cx
    mov cx, ADPCM_TIMEOUT
    in al, dx
@@poll_done:
    in al, dx
    test al, 8
    jnz short @@ready
    loop @@poll_done
    pop cx
    stc
    ret
@@ready:
    pop cx
    in al, dx
@@read_status:
    in al, dx
    test al, al
    jns short @@reset_transfer
    in al, dx
    jmp short @@read_status
@@reset_transfer:
    mov al, 010h
    cli
    out dx, al
    push cx
    mov cx, FM_REGISTER_DELAY
@@wait_reset:
    loop @@wait_reset
    pop cx
    xchg dx, bx
    mov al, 080h
    out dx, al
    sti
    xchg dx, bx
    loop @@transfer_loop
    mov dx, 01000h
    call WRITE_ADPCM_REGISTER
    mov dx, 01080h
    call WRITE_ADPCM_REGISTER
    mov dx, 0001h
    call WRITE_ADPCM_REGISTER
    clc
    ret
ADPCM_SETUP endp

ADPCM_DRAIN proc near
    mov dx, 0001h
    call WRITE_ADPCM_REGISTER
    mov dx, 01000h
    call WRITE_ADPCM_REGISTER
    mov dx, 01080h
    call WRITE_ADPCM_REGISTER
    mov dx, 00020h
    call WRITE_ADPCM_REGISTER
    mov dx, 00102h
    call WRITE_ADPCM_REGISTER
    mov dx, 00CFFh
    call WRITE_ADPCM_REGISTER
    inc dh
    call WRITE_ADPCM_REGISTER
    mov bx, 01FFFh
    mov dh, 2
    mov dl, bl
    call WRITE_ADPCM_REGISTER
    mov dh, 3
    mov dl, bh
    call WRITE_ADPCM_REGISTER
    mov dx, 004FFh
    call WRITE_ADPCM_REGISTER
    inc dh
    call WRITE_ADPCM_REGISTER
    call ADPCM_RECEIVE_ONCE
    call ADPCM_RECEIVE_ONCE
    mov cx, ADPCM_WORDS
    mov di, offset ram_readback
@@read_loop:
    mov dx, io_status_port
    cli
@@wait_status:
    in al, dx
    test al, al
    js short @@wait_status
    mov al, 8
    out dx, al
    in al, dx
@@wait_transfer:
    in al, dx
    test al, 8
    jz short @@wait_transfer
    in al, dx
@@wait_data:
    in al, dx
    or al, al
    js short @@wait_data
    mov dx, io_transfer_port
    in al, dx
    sti
    stosb
    mov dx, 01080h
    call WRITE_ADPCM_REGISTER
    loop @@read_loop
    mov dx, 0001h
    call WRITE_ADPCM_REGISTER
    ret
ADPCM_DRAIN endp

ADPCM_RECEIVE_ONCE proc near
    cli
    mov dx, io_status_port
@@wait_status:
    in al, dx
    test al, al
    js short @@wait_status
    mov al, 8
    out dx, al
    push cx
    mov cx, FM_REGISTER_DELAY
@@wait_delay:
    loop @@wait_delay
    pop cx
    mov dx, io_transfer_port
    in al, dx
    sti
    mov dx, 01080h
    call WRITE_ADPCM_REGISTER
    ret
ADPCM_RECEIVE_ONCE endp

CHECK_RAM_SIGNATURE proc near
    mov si, offset ram_signature
    mov di, offset ram_readback
    mov cx, ADPCM_WORDS
    repe cmpsb
    ret
CHECK_RAM_SIGNATURE endp

WRITE_ADPCM_REGISTER proc near
    push ax
    push bx
    push dx
    mov bx, dx
    mov dx, io_status_port
    pushf
    cli
    in al, dx
@@wait_ready:
    in al, dx
    or al, al
    js short @@wait_ready
    mov al, bh
    out dx, al
    push cx
    mov cx, FM_REGISTER_DELAY
@@wait_delay:
    loop @@wait_delay
    pop cx
    mov dx, io_transfer_port
    mov al, bl
    out dx, al
    popf
    pop dx
    pop bx
    pop ax
    ret
WRITE_ADPCM_REGISTER endp

.data
ram_signature db '*+=-PMD ADPCM RAM Check Data-=+*'
preferred_board_port db 0FFh
exit_status db 0

.data?
io_address_port dw ?
io_data_port dw ?
io_status_port dw ?
io_transfer_port dw ?
card_has_extended_bios db ?
access_extended db ?
ram_readback db ADPCM_WORDS dup (?)

end ADPCM_DIAGNOSTIC_ENTRY
