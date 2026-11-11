; TH05 ZUN.COM -I: resident PC-98 STOP/COPY interrupt guard.
; Original 8086/386 register protocols and DOS COM/PSP layout.
; Semantic, named control and natural CP932 messages; no binary image included.
.386
.model tiny
locals
.code
org 100h

DOS_INT equ 021h
PC98_BIOS_INT equ 018h
DOS_GET_VECTOR_6 equ 03506h
DOS_GET_VECTOR_5 equ 03505h
DOS_SET_VECTOR_6 equ 02506h
DOS_SET_VECTOR_5 equ 02505h
DOS_PRINT_STRING equ 09h
DOS_FREE_BLOCK equ 049h
DOS_TSR equ 03100h
DOS_EXIT_OK equ 04C00h
BIOS_HIDE_TEXT equ 041h
BIOS_RESTORE_TEXT equ 040h
BIOS_KEY_STATUS equ 04h
BIOS_KEYBOARD_COL equ 00Ch
BIOS_KANJI_ROM_PAGE equ 0A000h
BIOS_TEXT_ATTRIBUTE_PAGE equ 0A200h
BIOS_TEXT_ATTR equ 041h
INT6 equ 06h
INT5 equ 05h
CMD_PSP_START equ 081h
TOP_ROW equ 0650h
SECOND_ROW equ 06F0h
THIRD_ROW equ 0790h
NO_PENDING_GUARD equ 0
STOP_PENDING_GUARD equ 1
COPY_PENDING_GUARD equ 2

public START_I, INTERRUPT_STOP, INTERRUPT_COPY
public DRAW_KEY_WARNING, READ_GUARD_KEY, PRINT_KANJI_MSG
public INT_VECTOR_QUERY, INSTALL_DISPATCH

START_I proc near
    jmp near ptr INSTALL_DISPATCH
START_I endp
    even

INTERRUPT_STOP proc far
    cmp cs:guard_pending, NO_PENDING_GUARD
    jnz short @@return
    mov cs:guard_pending, STOP_PENDING_GUARD
    call DRAW_KEY_WARNING
@@return:
    iret
INTERRUPT_STOP endp

INTERRUPT_COPY proc far
    cmp cs:guard_pending, NO_PENDING_GUARD
    jnz short @@return
    mov cs:guard_pending, COPY_PENDING_GUARD
    call DRAW_KEY_WARNING
@@return:
    iret
INTERRUPT_COPY endp

DRAW_KEY_WARNING proc near
    pushf
    pusha
    push ds
    push es
    mov ah, BIOS_HIDE_TEXT
    int PC98_BIOS_INT
    mov di, offset stop_warning_1
    cmp cs:guard_pending, STOP_PENDING_GUARD
    jz short @@first_warning
    mov di, offset copy_warning_1
@@first_warning:
    mov ax, TOP_ROW
    call PRINT_KANJI_MSG
    add di, (stop_warning_2 - stop_warning_1)
    mov ax, SECOND_ROW
    call PRINT_KANJI_MSG
    add di, (stop_warning_3 - stop_warning_2)
    mov ax, THIRD_ROW
    call PRINT_KANJI_MSG
    mov bl, cs:guard_pending
@@wait_released:
    call READ_GUARD_KEY
    jnz short @@wait_released
@@wait_pressed:
    call READ_GUARD_KEY
    jz short @@wait_pressed
@@wait_release_again:
    call READ_GUARD_KEY
    jnz short @@wait_release_again
    mov ah, BIOS_RESTORE_TEXT
    int PC98_BIOS_INT
    mov di, offset blank_warning
    mov ax, TOP_ROW
    call PRINT_KANJI_MSG
    mov ax, SECOND_ROW
    call PRINT_KANJI_MSG
    mov ax, THIRD_ROW
    call PRINT_KANJI_MSG
    mov ah, INT6
    int PC98_BIOS_INT
    pop es
    pop ds
    popa
    popf
    mov cs:guard_pending, NO_PENDING_GUARD
    ret
DRAW_KEY_WARNING endp

READ_GUARD_KEY proc near
    mov ah, BIOS_KEY_STATUS
    mov al, BIOS_KEYBOARD_COL
    int PC98_BIOS_INT
    test ah, bl
    ret
READ_GUARD_KEY endp
    even

; Shift-JIS character bytes in AL/AH to PC-98 font code; caller flips pair.
SHIFTJIS_TO_PC98_FONT proc near
    shl ah, 1
    cmp al, 09Fh
    jnb short @@trail_converted
    cmp al, 080h
    adc ax, 0FEDFh
@@trail_converted:
    sbb ax, 0DFFEh
    and ax, 07F7Fh
    ret
SHIFTJIS_TO_PC98_FONT endp

PRINT_KANJI_MSG proc near
    push di
    mov bx, di
    mov dx, BIOS_KANJI_ROM_PAGE
    mov es, dx
    mov di, ax
    mov dx, ax
    xor ax, ax
    xor cx, cx
@@scan_message:
    mov ax, cs:[bx]
    cmp al, '$'
    jz short @@draw_color_attribute
    xchg ah, al
    call SHIFTJIS_TO_PC98_FONT
    xchg ah, al
    sub al, 020h
    stosw
    or ah, 080h
    stosw
    add bx, 2
    add cl, 2
    jmp short @@scan_message
@@draw_color_attribute:
    mov ax, BIOS_TEXT_ATTRIBUTE_PAGE
    mov es, ax
    mov di, dx
    mov ax, BIOS_TEXT_ATTR
@@fill_attr:
    stosw
    loop @@fill_attr
    pop di
    ret
PRINT_KANJI_MSG endp

; Original ZUN resident data magic and saved DOS vectors.
resident_magic dw 'ZU', 'NP'
old_int5 dd 0
old_int6 dd 0
stop_warning_1 db 'むやみにＳＴＯＰキー押したりしない$'
stop_warning_2 db '方がいいと思うの。（ゲーム中はね）$'
stop_warning_3 db '（ＳＴＯＰキーで戻れるよ、ねっ）　$'
copy_warning_1 db 'なんでＣＯＰＹキー押したりしてるの$'
copy_warning_2 db 'かな～。ふしぎ～。　　（もう一度、$'
copy_warning_3 db 'ＣＯＰＹキー押せば戻れるよ、ねっ）$'
blank_warning db '　　　　　　　　　　　　　　　　　$'
guard_pending db NO_PENDING_GUARD

INT_VECTOR_QUERY proc near
    mov dx, offset resident_header
    mov ah, DOS_PRINT_STRING
    int DOS_INT
    mov ax, DOS_GET_VECTOR_6
    int DOS_INT
    xor ax, ax
    cmp word ptr es:[resident_magic], 'ZU'
    jnz short @@return
    cmp word ptr es:[resident_magic+2], 'NP'
    jnz short @@return
    inc ax
@@return:
    ret
INT_VECTOR_QUERY endp

INSTALL_DISPATCH proc near
    mov si, CMD_PSP_START
@@command_loop:
    lodsb
    cmp al, 0Dh
    jz short @@check_installed
    cmp al, '/'
    jz short @@read_switch
    cmp al, '-'
    jz short @@read_switch
    cmp al, ' '
    jbe short @@command_loop
@@check_installed:
    call INT_VECTOR_QUERY
    test ax, ax
    jz short @@install
    jmp @@already_installed
@@read_switch:
    lodsb
    cmp al, ' '
    jbe near ptr @@bad_switch
    and al, 0DFh
    cmp al, 'R'
    jnz near ptr @@bad_switch
    call INT_VECTOR_QUERY
    test ax, ax
    jnz short @@remove
    jmp short @@not_installed
@@install:
    mov ax, DOS_GET_VECTOR_6
    int DOS_INT
    mov word ptr old_int6, bx
    mov word ptr old_int6+2, es
    mov dx, offset INTERRUPT_STOP
    mov ax, DOS_SET_VECTOR_6
    int DOS_INT
    mov ax, DOS_GET_VECTOR_5
    int DOS_INT
    mov word ptr old_int5, bx
    mov word ptr old_int5+2, es
    mov dx, offset INTERRUPT_COPY
    mov ax, DOS_SET_VECTOR_5
    int DOS_INT
    mov dx, offset resident_installed_text
    mov ah, DOS_PRINT_STRING
    int DOS_INT
    mov dx, offset INT_VECTOR_QUERY
    shr dx, 4
    inc dx
    mov ax, DOS_TSR
    int DOS_INT
@@remove:
    push ds
    lds dx, es:old_int6
    mov ax, DOS_SET_VECTOR_6
    int DOS_INT
    lds dx, es:old_int5
    mov ax, DOS_SET_VECTOR_5
    int DOS_INT
    pop ds
    push es
    mov es, word ptr es:[02Ch]
    mov ah, DOS_FREE_BLOCK
    int DOS_INT
    pop es
    mov ah, DOS_FREE_BLOCK
    int DOS_INT
    mov dx, offset resident_removed_text
    jnb short @@exit_message
    mov dx, offset resident_free_error
    jmp short @@exit_message
@@already_installed:
    mov dx, offset already_installed_text
    jmp short @@exit_message
@@not_installed:
    mov dx, offset not_installed_text
    jmp short @@exit_message
@@bad_switch:
    mov dx, offset bad_switch_text
@@exit_message:
    mov ah, DOS_PRINT_STRING
    int DOS_INT
    mov ax, DOS_EXIT_OK
    int DOS_INT
INSTALL_DISPATCH endp

resident_header db 0Dh,0Ah
    db 'INTvector set program  zuninit.com                      Version1.02 (c)zun 1998',0Dh,0Ah,'$'
resident_installed_text db 'ちょこっとお部屋かりるね☆',0Dh,0Ah,0Dh,0Ah,'$'
already_installed_text db 'すでに常駐してます～',0Dh,0Ah,0Dh,0Ah,'$'
resident_removed_text db '借りてたお部屋をお返ししますね。それではまた☆',0Dh,0Ah,0Dh,0Ah,'$'
not_installed_text db 'まだ、常駐してないです',0Dh,0Ah,0Dh,0Ah,'$'
bad_switch_text db '意味不明なオプションよぉ（オプションは -R : 解放 のみ）',0Dh,0Ah,'$'
resident_free_error db 'メモリ解放エラーです',0Dh,0Ah,'$'

end START_I
