// Verdict bitmap transfers, as in ReC98's th05/end/verdict_bitmap.asm.
// The loops are inline assembly; the compiler generates the stack frame and
// saves SI/DI because the asm blocks use them. Saving them manually again
// would add eight bytes. Compiled by Turbo C++'s built-in assembler, the XOR
// instructions also get the original opcode direction, unlike with TASM.

// Copies a single verdict screen from
//	(0, 0) - (320, 352)
// on the E plane in VRAM to ([verdict_bitmap] + [bitmap_offset]).
void pascal near verdict_bitmap_snap(size_t bitmap_offset)
{
    asm {
        push ds
        push ds
        pop es
        mov ax, 0e000h  // E plane
        mov ds, ax
        xor si, si
        mov di, bitmap_offset
        add di, offset verdict_bitmap
        mov ax, 352
    bitmap_snap_row:
        mov cx, 20      // 40 bytes = 320 pixels
        rep movsw
        add si, 40      // skip the other half of the 80-byte VRAM row
        dec ax
        jnz bitmap_snap_row
        pop ds
    }
}
// Blits a single verdict screen starting at
// ([verdict_bitmap] + [bitmap_offset]) to
//	(0, 0) - (320, 352)
// in VRAM: first clears the area to color 1 in TDW mode, then sets the
// bitmap's dots in color 13 in RMW mode.
void pascal near verdict_bitmap_put(size_t bitmap_offset)
{
    grcg_setcolor(0x80, 1);
    asm {
        mov ax, 0a800h  // B plane; with the GRCG on, writes go to all planes
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
        mov dx, 07ch    // grcg_off()
        mov al, 0
        out dx, al
    }
}
