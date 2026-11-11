; Original CDG resource loader / single-image reader / batch-loader / free.
; Semantics from ReC98 th04/formats/cdg_load.asm and th03/formats/cdg.inc.
; Full record and every original file/memory provider remain authentic.
.386
.model large
locals
include types.inc
include symbols.inc

SHARED segment byte public 'CODE' use16
assume cs:SHARED, ds:DGROUP
public CDG_LOAD_SINGLE_NOALPHA, CDG_LOAD_SINGLE
public CDG_LOAD_ALL_NOALPHA, CDG_LOAD_ALL, CDG_FREE

CDG_LOAD_SINGLE_NOALPHA label byte
    mov _cdg_noalpha, CDG_NOALPHA_ON
    even
CDG_LOAD_SINGLE proc far
    push bp
    mov bp, sp
    push si
    push di
    mov di, word ptr [bp+12]
    push di
    ; ReC98 th04/formats/cdg_load.asm preserves this original compiler
    ; relaxation NOP before the same-CS FAR CDG_FREE call.
    nop
    call CDG_FREE
    shl di, 4
    add di, offset _cdg_slots
    push dword ptr [bp+8]
    call FILE_ROPEN
    push ds
    push di
    push CDG_RECORD_BYTES
    call FILE_READ
    mov ax, word ptr [di+CDG_PLANE_BYTES]
    mov dx, ax
    cmp byte ptr [di+CDG_PLANE_LAYOUT], CDG_COLORS
    je short @@read_offset
    shl ax, 2
    cmp byte ptr [di+CDG_PLANE_LAYOUT], CDG_ALPHA_ONLY
    je short @@read_offset
    add ax, dx
@@read_offset:
    mul word ptr [bp+6]
    movzx eax, ax
    push eax
    push 1
    call FILE_SEEK
    call CDG_READ_SINGLE
    call FILE_CLOSE
    mov _cdg_noalpha, CDG_NOALPHA_OFF
    pop di
    pop si
    pop bp
    retf 8
CDG_LOAD_SINGLE endp
    even

CDG_READ_SINGLE proc near
    mov al, byte ptr [di+CDG_PLANE_LAYOUT]
    or al, al
    je short @@colors
    cmp al, CDG_ALPHA_ONLY
    je short @@alpha
    cmp _cdg_noalpha, CDG_NOALPHA_OFF
    jne short @@skip_alpha
@@alpha:
    push word ptr [di+CDG_PLANE_BYTES]
    call HMEM_ALLOCBYTE
    mov word ptr [di+CDG_ALPHA_SEG], ax
    push ax
    push 0
    push word ptr [di+CDG_PLANE_BYTES]
    call FILE_READ
    jmp short @@colors
@@skip_alpha:
    movzx eax, word ptr [di+CDG_PLANE_BYTES]
    push eax
    push 1
    call FILE_SEEK
@@colors:
    cmp byte ptr [di+CDG_PLANE_LAYOUT], CDG_ALPHA_ONLY
    je short @@done
    mov ax, word ptr [di+CDG_PLANE_BYTES]
    shl ax, 2
    push ax
    call HMEM_ALLOCBYTE
    mov word ptr [di+CDG_COLOR_SEG], ax
    push ax
    push 0
    mov ax, word ptr [di+CDG_PLANE_BYTES]
    shl ax, 2
    push ax
    call FILE_READ
@@done:
    ret
CDG_READ_SINGLE endp

CDG_LOAD_ALL_NOALPHA label byte
    mov _cdg_noalpha, CDG_NOALPHA_ON
    even
CDG_LOAD_ALL proc far
    push bp
    mov bp, sp
    push si
    push di
    push dword ptr [bp+6]
    call FILE_ROPEN
    mov di, word ptr [bp+10]
    shl di, 4
    add di, offset _cdg_slots
    push ds
    push di
    push CDG_RECORD_BYTES
    call FILE_READ
    mov si, di
    mov bp, word ptr [bp+10]
    mov al, byte ptr [si+CDG_IMAGE_COUNT]
    mov _cdg_images_to_load, al
    push ds
    pop es
@@next_image:
    push bp
    call CDG_FREE
    mov cx, CDG_COPY_STRUCT_DWORDS
    rep movsd
    sub si, CDG_ALPHA_SEG
    sub di, CDG_ALPHA_SEG
    call CDG_READ_SINGLE
    inc bp
    add di, CDG_RECORD_BYTES
    dec _cdg_images_to_load
    jne short @@next_image
    call FILE_CLOSE
    mov _cdg_noalpha, CDG_NOALPHA_OFF
    pop di
    pop si
    pop bp
    retf 6
CDG_LOAD_ALL endp

CDG_FREE proc far
    mov bx, sp
    push di
    mov di, word ptr ss:[bx+4]
    shl di, 4
    add di, offset _cdg_slots + CDG_ALPHA_SEG
    cmp word ptr [di], 0
    je short @@colors
    push word ptr [di]
    call HMEM_FREE
    mov word ptr [di], 0
@@colors:
    add di, 2
    cmp word ptr [di], 0
    je short @@done
    push word ptr [di]
    call HMEM_FREE
    mov word ptr [di], 0
@@done:
    pop di
    retf 2
CDG_FREE endp
    even
public cdg_load_family_end
cdg_load_family_end label byte
SHARED ends
end
