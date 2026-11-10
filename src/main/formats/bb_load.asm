; Original near-Pascal .BB segment loader, matching ReC98 th05/formats/bb_load.asm.
; The real entry accepts a four-byte far filename and returns AX segment.
; All DOS open/read/close operations deliberately retain original unchecked behavior.
.386
.model large
locals
include types.inc
include symbols.inc

main_01 group BB_LOAD_TEXT
BB_LOAD_TEXT segment byte public 'CODE' use16
assume cs:main_01, ds:DGROUP
public BB_LOAD
BB_LOAD proc near
    push si
    push BB_LOAD_BYTES
    call HMEM_ALLOCBYTE
    mov _bb_load_seg, ax
    mov bx, sp
    mov si, ds
    mov ax, 03d00h
    lds dx, dword ptr ss:[bx + 4]
    int 021h
    mov bx, ax
    mov ds, si
    mov ds, _bb_load_seg
    mov cx, BB_LOAD_BYTES
    xor dx, dx
    mov ah, 03fh
    int 021h
    mov ah, 03eh
    int 021h
    mov ds, si
    pop si
    mov ax, _bb_load_seg
    ret 4
BB_LOAD endp
public bb_load_end
bb_load_end label byte
BB_LOAD_TEXT ends
end
