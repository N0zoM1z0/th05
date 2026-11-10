; Copy the actual 14-byte Gather bullet template into the shared live template.
; Source semantics preserved in ReC98 th04/main/gather.cpp with
; copy_near_struct_member(..., prepare_di_si): near Pascal gather_t*.
.386
.model large
locals
include types.inc
include symbols.inc

main_03 group GATHER_COPY_FROM_TEXT
GATHER_COPY_FROM_TEXT segment byte public 'CODE' use16
assume cs:main_03, ds:DGROUP
public SET_BULLET_TEMPLATE_TO_GATHER_TEMPLATE
SET_BULLET_TEMPLATE_TO_GATHER_TEMPLATE proc near
    push bp
    mov bp, sp
    push si
    push di
    mov cx, GATHER_BULLET_WORDS
    push ds
    pop es
    mov di, offset _bullet_template
    mov si, word ptr [bp + 4]
    add si, GATHER_BULLET_OFFSET
    rep movsw
    pop di
    pop si
    pop bp
    ret 2
SET_BULLET_TEMPLATE_TO_GATHER_TEMPLATE endp
public gather_copy_from_end
gather_copy_from_end label byte
GATHER_COPY_FROM_TEXT ends
end
