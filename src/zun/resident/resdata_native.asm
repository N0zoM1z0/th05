; Master library's original 8086 resident-data search and allocation routines.
; Retained from ReC98/libs/master.lib/resdata.asm by Akihiko Koizuka.
; Target is ZUN.COM's -S tiny-memory-model near-Pascal helper contribution.
; Complete GRCG clear + two original near-Pascal resident-data functions.
.8086
.model tiny
.code
org 0100h
resident_source_base label byte
org 05B6h
include graph_clear_native.inc
org 05DAh

MCB_KIND equ 0
MCB_OWNER equ 1
MCB_PARAGRAPHS equ 3
NEAR_RETURN_WORDS equ 1
RESDATA_ARG_LENGTH equ 6
RESDATA_ARG_IDENTIFIER equ 8
RESDATA_ARG_PARAGRAPHS equ 4
DOS_MEMORY_CONTROL_INT equ 021h
DOS_LIST_OF_LISTS equ 052h
DOS_GET_ALLOC_POLICY equ 05800h
DOS_SET_ALLOC_POLICY equ 05801h
DOS_ALLOCATE_BLOCK equ 048h
DOS_RELEASE_BLOCK equ 049h

public RESDATA_EXIST, RESDATA_CREATE
public resdata_end

RESDATA_EXIST proc near
    push bp
    mov bp, sp
    push si
    push di

    ; Walk the DOS memory-control-block chain from the List of Lists.
    mov ah, DOS_LIST_OF_LISTS
    int DOS_MEMORY_CONTROL_INT
    cld
    mov bx, es:[bx-2]
@@find:
    mov es, bx
    inc bx                  ; MCB is one paragraph before the block
    mov ax, es:[MCB_OWNER]
    or ax, ax
    je short @@skip
    mov ax, es:[MCB_PARAGRAPHS]
    cmp ax, [bp+RESDATA_ARG_PARAGRAPHS]
    jne short @@skip
    mov cx, [bp+RESDATA_ARG_LENGTH]
    mov si, [bp+RESDATA_ARG_IDENTIFIER]
    mov di, 010h
    repe cmpsb
    je short @@found
@@skip:
    mov ax, es:[MCB_PARAGRAPHS]
    add bx, ax
    mov al, es:[MCB_KIND]
    cmp al, 'M'
    je short @@find
    mov bx, 0
@@found:
    mov ax, bx
    pop di
    pop si
    pop bp
    ret 6
RESDATA_EXIST endp
    even

RESDATA_CREATE proc near
    push bp
    mov bp, sp
    push si
    push di
    push word ptr [bp+RESDATA_ARG_IDENTIFIER]
    push word ptr [bp+RESDATA_ARG_LENGTH]
    push word ptr [bp+RESDATA_ARG_PARAGRAPHS]
    call RESDATA_EXIST
    or ax, ax
    jnz short @@done

    ; Try the low-memory allocator first; fall back to the last-fit policy
    ; if DOS allocated the block above the current ZUN resident stub.
    mov ax, DOS_GET_ALLOC_POLICY
    int DOS_MEMORY_CONTROL_INT
    mov dx, ax
    mov ax, DOS_SET_ALLOC_POLICY
    mov bx, 1
    int DOS_MEMORY_CONTROL_INT
    mov ah, DOS_ALLOCATE_BLOCK
    mov bx, [bp+RESDATA_ARG_PARAGRAPHS]
    int DOS_MEMORY_CONTROL_INT
    mov cx, 0
    jc short @@restore_policy
    mov bx, cs
    cmp bx, ax
    jnb short @@allocated
    mov es, ax
    mov ah, DOS_RELEASE_BLOCK
    int DOS_MEMORY_CONTROL_INT
    mov ax, DOS_SET_ALLOC_POLICY
    mov bx, 2
    int DOS_MEMORY_CONTROL_INT
    mov ah, DOS_ALLOCATE_BLOCK
    mov bx, [bp+RESDATA_ARG_PARAGRAPHS]
    int DOS_MEMORY_CONTROL_INT
@@allocated:
    mov cx, ax
    push ax
    dec cx
    mov es, cx
    mov ax, -1
    mov es:[MCB_OWNER], ax
    inc cx
    mov es, cx
    xor di, di
    mov cx, [bp+RESDATA_ARG_LENGTH]
    mov si, [bp+RESDATA_ARG_IDENTIFIER]
    rep movsb
    pop cx
@@restore_policy:
    mov ax, DOS_SET_ALLOC_POLICY
    mov bx, dx
    int DOS_MEMORY_CONTROL_INT
    mov ax, cx
@@done:
    pop di
    pop si
    pop bp
    ret 6
RESDATA_CREATE endp
    even
resdata_end label byte

end resident_source_base
