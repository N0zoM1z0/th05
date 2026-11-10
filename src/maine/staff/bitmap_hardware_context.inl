// Original-register MAINE verdict bitmap capture and restore, 43+83 bytes.
// These hardware operations deliberately use 16-bit SI/DI and real PC-98
// GRCG calls. The compiler automatically saves those callee registers; no
// handwritten prologue or synthetic push/pop is needed.
// Original semantics are corroborated by ReC98 th05/end/verdict_bitmap.asm.
void pascal near verdict_bitmap_snap(size_t bitmap_offset)
{
    asm {
        push ds
        push ds
        pop es
        mov ax, 0e000h
        mov ds, ax
        xor si, si
        mov di, bitmap_offset
        add di, offset verdict_bitmap
        mov ax, 352
    bitmap_snap_row:
        mov cx, 20
        rep movsw
        add si, 40
        dec ax
        jnz bitmap_snap_row
        pop ds
    }
}
void pascal near verdict_bitmap_put(size_t bitmap_offset)
{
    grcg_setcolor(0x80, 1);
    asm {
        mov ax, 0a800h
        mov es, ax
        xor di, di
        mov dx, 352
    bitmap_clear_row:
        mov cx, 20
        rep stosw
        add di, 40
        dec dx
        jnz bitmap_clear_row
    }
    grcg_setcolor(0xc0, 13);
    asm {
        xor di, di
        mov si, bitmap_offset
        add si, offset verdict_bitmap
        mov dx, 352
    bitmap_put_row:
        mov cx, 20
        rep movsw
        add di, 40
        dec dx
        jnz bitmap_put_row
        mov dx, 07ch
        mov al, 0
        out dx, al
    }
}
