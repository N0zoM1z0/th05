; TH05 ZUN.COM -M memory check, maintained original-style assembly candidate.
; Origin is inferred from the bare COM entry, private register calling
; convention and complete FLAGS/general-register preservation. This is not a
; claim to recover literal historical source. See README.md.
;
; Maintained text is UTF-8; replay converts assembler input to CP932 explicitly.

.186
.model tiny
.code
org 100h

DOS_RESIZE_BLOCK       equ 4ah
DOS_ALLOCATE_BLOCK     equ 48h
DOS_PRINT_STRING       equ 09h
DOS_PRINT_CHARACTER    equ 02h
DOS_EXIT_PROCESS       equ 4ch
PARAGRAPH_SHIFT        equ 4
EXTRA_STACK_PARAGRAPHS equ 16
ROUND_UP_PARAGRAPHS    equ 1
MIN_FREE_PARAGRAPHS    equ 32500       ; 520000 conventional-memory bytes
DECIMAL_BASE           equ 10
DECIMAL_TEN_THOUSAND   equ 10000
DECIMAL_THOUSAND       equ 1000
LOW_MEMORY_EXIT_CODE   equ 0ffh

public MEMORY_CHECK_START
public MEMORY_PRINT_DECIMAL_CHUNK

; DOS COM entry: CS=DS=ES=SS point at the PSP; execution begins at 0100h.
; No CRT or C argument frame is present. DOS INT 21h/4Ch terminates the child.
MEMORY_CHECK_START proc near
    mov bx, offset memory_image_end
    shr bx, PARAGRAPH_SHIFT
    add bx, EXTRA_STACK_PARAGRAPHS + ROUND_UP_PARAGRAPHS
    mov ah, DOS_RESIZE_BLOCK
    int 21h
    shl bx, PARAGRAPH_SHIFT
    mov sp, bx

    mov dx, offset memory_intro
    mov ah, DOS_PRINT_STRING
    int 21h

    ; An impossible conventional allocation asks DOS to return the largest
    ; available contiguous block in BX. Preserve the original unchecked CF.
    mov bx, 0ffffh
    mov ah, DOS_ALLOCATE_BLOCK
    int 21h

    mov di, offset memory_ready
    cmp bx, MIN_FREE_PARAGRAPHS
    jnb memory_capacity_selected
    mov di, offset memory_insufficient
    mov memory_exit_code, LOW_MEMORY_EXIT_CODE

memory_capacity_selected:
    xor dx, dx
    mov ax, (1 shl PARAGRAPH_SHIFT)
    mul bx
    mov cx, DECIMAL_TEN_THOUSAND
    div cx
    mov cx, DECIMAL_BASE
    call MEMORY_PRINT_DECIMAL_CHUNK
    mov ax, dx
    mov cx, DECIMAL_THOUSAND
    call MEMORY_PRINT_DECIMAL_CHUNK

    mov dx, offset memory_bytes_suffix
    mov ah, DOS_PRINT_STRING
    int 21h
    mov dx, di
    mov ah, DOS_PRINT_STRING
    int 21h
    mov ah, DOS_EXIT_PROCESS
    mov al, memory_exit_code
    int 21h
MEMORY_CHECK_START endp

; Input AX: unsigned value. Input CX: highest decimal place to print.
; Used with CX=10 for two digits and CX=1000 for four digits. This is not a
; general unbounded integer formatter: higher places are consumed but hidden.
; Preserves FLAGS and every general register with PUSHF/PUSHA and POPA/POPF.
; Scratch roles: BX=remainder, SI=decimal divisor, DX=division/output scratch.
MEMORY_PRINT_DECIMAL_CHUNK proc near
    pushf
    pusha
    mov bx, ax
    mov si, DECIMAL_TEN_THOUSAND

memory_decimal_place:
    xor dx, dx
    mov ax, bx
    div si
    mov bx, dx
    cmp cx, si
    jb memory_decimal_skip_output
    mov dl, al
    add dl, '0'
    mov ah, DOS_PRINT_CHARACTER
    int 21h

memory_decimal_skip_output:
    xor dx, dx
    mov ax, si
    mov si, DECIMAL_BASE
    div si
    mov si, ax
    cmp si, 0
    jnz memory_decimal_place
    popa
    popf
    ret
MEMORY_PRINT_DECIMAL_CHUNK endp

; Original user-visible text is represented as text, not encoded byte arrays.
; INT 21h/09h consumes DS:DX through the terminating dollar character.
memory_intro        db 'あなたのメインメモリ空き容量は $'
memory_bytes_suffix db ' バイトですの',13,10,'$'
memory_insufficient db 'ちょっと、メモリが足りないかも',13,10
                    db 'このゲームは空きメインメモリは 520000 バイトは必要ですわ',13,10,'$'
memory_ready        db 'それでは頑張って下さいね☆',13,10,'$'
memory_exit_code    db 0
memory_image_end label byte

end MEMORY_CHECK_START
