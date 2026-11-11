; Load one complete 128-byte/tile MPN bank from a DOS file.
; The file's six-byte header gives the inclusive highest image index,
; followed by a 48-byte palette and then the contiguous image planes.
.386
.model large
include types.inc
include symbols.inc

_TEXT segment word public 'CODE' use16
assume cs:_TEXT, ds:DGROUP
public MPN_LOAD_INNER
MPN_LOAD_INNER proc far
    ; The adjacent MPN_FREE far function has the same CS. Preserve the
    ; far return frame while using the directly known same-segment target.
    push cs
    call near ptr mpn_free
    mov bx, sp
    push si
    push di
    push ds
    mov ax, DOS_FN_OPEN_READ
    lds dx, ss:[bx+MPN_ARG_FILENAME]
    int 21h
    pop ds
    mov bx, ax
    mov si, bx
    mov ah, DOS_FN_READ
    mov dx, offset Palettes
    mov cx, MPN_HEADER_BYTES
    int 21h
    mov di, word ptr Palettes+MPN_HEADER_MAX_INDEX_OFFSET
    mov ah, DOS_FN_READ
    mov dx, offset Palettes
    mov cx, MPN_PALETTE_BYTES
    int 21h
    mov mpn_last_image, di
    inc di
    shl di, MPN_IMAGE_SHIFT
    push di
    call HMEM_ALLOCBYTE
    mov mpn_images_seg, ax
    mov bx, si
    push ds
    mov ds, ax
    xor dx, dx
    mov ah, DOS_FN_READ
    mov cx, di
    int 21h
    pop ds
    mov ah, DOS_FN_CLOSE
    int 21h
    call PALETTE_SHOW
    pop di
    pop si
    retf 4
MPN_LOAD_INNER endp
; Real foreign neighbor at the next instruction address. No code or data is
; supplied here; the compiled loader's known endpoint anchors its far callee.
public mpn_free
mpn_free label far
_TEXT ends
end
