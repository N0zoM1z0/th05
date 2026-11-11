; ZUN.COM outer COMCSTM packaging wrapper, based on Pipeline/cstmstub.asm
; and original `comcstm.c` header semantics. The inner 17,745-byte program
; is a foreign ORG hole: this module does not reproduce/own child bytes.
.8086
.model tiny
.code
org 100h

ORIGINAL_TIMESTAMP equ 02579AF64h
ORIGINAL_INNER_SIZE equ 17745
DOS_WRITESTDOUT equ 040h
DOS_EXIT_OK equ 04C00h
PSP_COMMAND_LENGTH equ 080h
PSP_COMMAND_WORD equ 082h
PSP_RUNTIME_START equ 0100h

public outer_header, outer_usage, inner_program_start, outer_entry
public outer_copy_up, outer_end

outer_header label byte
    jmp near ptr outer_entry
    dw outer_usage
    dw (inner_program_start - outer_usage)
    dw ORIGINAL_INNER_SIZE
    dd ORIGINAL_TIMESTAMP
    db 'comcstm (c)O.Morikawa 1996'

outer_usage label byte
    ; Real CP932 help text from the maintained UTF-8 source, generated only
    ; in the private replay directory to avoid committing binary text.
    include usage_private.inc

inner_program_start label byte
    org $+ORIGINAL_INNER_SIZE

outer_entry:
    cmp byte ptr ds:[PSP_COMMAND_LENGTH], 0
    jz short outer_copy_up
    mov ax, word ptr ds:[PSP_COMMAND_WORD]
    cmp ax, 03F2Dh     ; `-?`
    jz short @@print_help
    cmp ax, 00D3Fh     ; `?` + carriage return
    jnz short outer_copy_up
@@print_help:
    mov bx, 1          ; DOS standard output
    mov dx, word ptr ds:[103h]  ; header usage-text pointer
    mov cx, word ptr ds:[105h]  ; header usage-text length
    mov ah, DOS_WRITESTDOUT
    int 21h
    mov ax, DOS_EXIT_OK
    int 21h
outer_copy_up:
    mov di, PSP_RUNTIME_START
    push di
    mov si, word ptr ds:[103h]
    add si, word ptr ds:[105h]
    mov cx, word ptr ds:[107h]  ; inner COM length from original header
    inc cx
    shr cx, 1
    rep movsw
    mov ax, cx
    mov si, ax
    mov di, ax
    retn
outer_end label byte

end outer_header
