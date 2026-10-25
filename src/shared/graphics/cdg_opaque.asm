; Semantic original-ASM reconstruction of the complete opaque CDG plane blit.
; Candidate algorithm: pinned ReC98 b6ba5b0a th04/formats/cdg_p_na.cpp;
; its synthetic register-template C++ is not counted as recovered C++.
.386
.model use16 large SHARED
locals
include types.inc
include symbols.inc

PLANE_COUNT equ 4

; One bottom-to-top CDG row: copy its dwords, then step to the preceding row.
COPY_ROW_UP macro
 mov cx, bp
 rep movsd
 sub di, dx
endm

.code SHARED
public CDG_PUT_NOALPHA_8
CDG_PUT_NOALPHA_8 proc far
 ; Far Pascal (left, top, slot); BP becomes dword width after all arg reads.
 arg @@slot:word, @@top:word, @@left:word
 push bp
 mov bp, sp
 push si
 push di
 push ds
 ; Incorporate the vertical position into all four video segment bases.
 mov ax, @@top
 mov bx, ax
 shl ax, 2
 add ax, bx
 add ax, SEG_PLANE_B
 mov es, ax
 add ax, (SEG_PLANE_E-SEG_PLANE_B)
 push ax
 sub ax, SEG_PLANE_DIST_E
 push ax
 sub ax, SEG_PLANE_DIST_BRG
 push ax
 ; Select one complete16-byte slot and its signed-left bottom-row position.
 mov si, @@slot
 shl si, 4
 add si, offset _cdg_slots
 mov bx, @@left
 sar bx, 3
 add bx, [si+cdg_t.offset_at_bottom_left]
 mov ax, [si+cdg_t.vram_dword_w]
 mov bp, ax
 shl ax, 2
 add ax, ROW_SIZE
 mov dx, ax
 mov ax, [si+cdg_t.seg_colors]
 mov ds, ax
 xor si, si
 mov al, PLANE_COUNT
 cld
 even
@@next_plane:
 mov di, bx
@@next_row:
 COPY_ROW_UP
 jns short @@next_row
 dec al
 jz short @@done
 pop es
 jmp short @@next_plane
@@done:
 pop ds
 pop di
 pop si
 pop bp
 retf 6
CDG_PUT_NOALPHA_8 endp
 even
public cdg_opaque_end
cdg_opaque_end label byte
end
