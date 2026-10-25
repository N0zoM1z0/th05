; Maintained semantic PI row/palette/free family, explicit private stack contracts.
; Candidate: pinned ReC98 b6ba5b0a th05/formats/pi_asm_2.asm.
.386
.model use16 large SHARED
locals
include types.inc
include symbols.inc

PALETTE_COPY_COLORS equ 16
NORMALIZE_BUFFER macro
 mov ax, si
 shr ax, 4
 mov dx, es
 add dx, ax
 mov es, dx
 and si, 0Fh
endm

.code SHARED
public pi_plain_rows, @PI_PUT_8_ROWLOOP$QIIIUI
@PI_PUT_8_ROWLOOP$QIIIUI label near
pi_plain_rows proc near
 ; Hidden ES:SI packed buffer and DI height; BP is the incoming SP, not saved.
 @@stride equ word ptr [bp+2]
 @@width equ word ptr [bp+4]
 @@top equ word ptr [bp+6]
 @@left equ word ptr [bp+8]
 mov bp, sp
@@put_row:
 push es
 push @@left
 push @@top
 push es
 push si
 push @@width
 call GRAPH_PACK_PUT_8_NOCLIP
 pop es
 inc @@top
 cmp @@top, RES_Y
 jb short @@source_advance
 sub @@top, RES_Y
@@source_advance:
 add si, @@stride
 NORMALIZE_BUFFER
 dec di
 jnz short @@put_row
 ret 8
pi_plain_rows endp
 even

public pi_palette_apply, @PI_PALETTE_APPLY$QI
@PI_PALETTE_APPLY$QI label far
pi_palette_apply proc far
 ; BX captures SP before saving SI/DI; a far return occupies four bytes.
 mov bx, sp
 push si
 push di
 mov si, ss:[bx+4]
 imul si, size pi_header_t
 add si, (offset _pi_headers+pi_header_t.palette)
 mov di, offset Palettes
 mov ax, ds
 mov es, ax
 mov cx, ((PALETTE_COPY_COLORS*size rgb8_t)/4)
 rep movsd
 call PALETTE_SHOW
 pop di
 pop si
 retf 2
 even
pi_palette_apply endp

public pi_free, @PI_FREE$QI
@PI_FREE$QI label far
pi_free proc far
 mov bx, sp
 mov bx, ss:[bx+4]
 mov ax, bx
 shl bx, 2
 add bx, offset _pi_buffers
 cmp dword ptr [bx], 0
 jz short @@ret
 imul ax, size pi_header_t
 add ax, offset _pi_headers
 ; Both header and image are real far pointers; clear the slot before freeing.
 push ds
 push ax
 push word ptr [bx+2]
 push word ptr [bx]
 mov dword ptr [bx], 0
 call GRAPH_PI_FREE
@@ret:
 retf 2
 even
pi_free endp
public pi_rows_palette_free_end
pi_rows_palette_free_end label byte
end
