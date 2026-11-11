; Master PC-98 GRCG clear-current-VRAM helper (from graph_clear.asm).
; The caller's two video parameters are original DS foreign words, not data
; embedded in this bounded source.
graph_VramSeg equ 0185Ch
graph_VramWords equ 0185Eh
public GRAPH_CLEAR
GRAPH_CLEAR proc near
    mov al, 080h       ; GRCG tile-direct writing of zero to all planes
    pushf
    cli
    out 07Ch, al
    popf
    xor ax, ax
    mov dx, 07Eh
    out dx, al
    out dx, al
    out dx, al
    out dx, al
    mov bx, di
    xor di, di
    mov cx, word ptr ds:[graph_VramWords]
    mov es, word ptr ds:[graph_VramSeg]
    rep stosw
    mov di, bx
    out 07Ch, al       ; return GRCG to OFF
    ret
GRAPH_CLEAR endp
    even
