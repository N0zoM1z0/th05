; Maintained semantic reconstruction of TH05's complete masked PI row kernel.
; Candidate: pinned ReC98 b6ba5b0a, th05/formats/pi_asm_1.asm.
.386
.model use16 large SHARED
locals
include types.inc
include symbols.inc

TEMP_ROW equ RES_Y
MASK_SLOT_SHIFT equ 3 ; four word masks per slot

; Normalize the advanced packed-data pointer without changing its linear address.
NORMALIZE_BUFFER macro
 mov ax, si
 shr ax, 4
 mov dx, es
 add dx, ax
 mov es, dx
 and si, 0Fh
endm

.code SHARED
public pi_masked_rows, @PI_PUT_MASKED_8_ROWLOOP$QIIIUI
@PI_PUT_MASKED_8_ROWLOOP$QIIIUI label near
pi_masked_rows proc near
 ; Hidden ES:SI packed buffer, DI height, AX mask ID. No saved BP frame.
 ; Near Pascal words at original SP+2/+4/+6/+8: stride, width, top, left.
 @@stride equ word ptr [bp+2]
 @@width equ word ptr [bp+4]
 @@top equ word ptr [bp+6]
 @@left equ word ptr [bp+8]
 shl ax, MASK_SLOT_SHIFT
 add ax, offset _PI_MASKS
 mov _pi_mask_ptr, ax
 mov bp, sp
 mov dx, @@left
 shr dx, 3
 mov ax, @@top
 shl ax, 6
 add dx, ax
 shr ax, 2
 add dx, ax
 mov _pi_put_masked_vram_offset, dx
 mov _pi_mask_y, 0
@@put_row:
 push es
 ; Original row first goes to the off-screen scratch row; far Pascal 10 bytes.
 push 0
 push TEMP_ROW
 push es
 push si
 push @@width
 call GRAPH_PACK_PUT_8_NOCLIP
 push ds
 push di
 push si
 mov di, _pi_put_masked_vram_offset
 add _pi_put_masked_vram_offset, ROW_BYTES
 cmp _pi_put_masked_vram_offset, PLANE_BYTES
 jb short @@destination_ready
 sub _pi_put_masked_vram_offset, PLANE_BYTES
@@destination_ready:
 call @pi_mask_setup_egc_and_advance$qv
 mov ax, SEG_PLANE_B
 mov es, ax
 mov ds, ax
 mov si, (ROW_BYTES*TEMP_ROW)
 mov cx, @@width
 shr cx, 4
 rep movsw
 call EGC_OFF
 pop si
 pop di
 pop ds
 pop es
 add si, @@stride
 NORMALIZE_BUFFER
 dec di
 jnz short @@put_row
 ret 8
pi_masked_rows endp
public pi_masked_rows_end
pi_masked_rows_end label byte
end
