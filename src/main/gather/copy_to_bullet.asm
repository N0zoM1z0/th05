; Original near-Pascal source-register gather.bullet_template copy.
; ReC98 th04/main/gather.cpp's copy_near_struct_member(...,prepare_si_di)
; preserves the real 7-word DS-to-ES REP MOVSW algorithm.
.386
.model large
locals
include types.inc
include symbols.inc

main_03 group GATHER_COPY_TO_TEXT
GATHER_COPY_TO_TEXT segment word public 'CODE' use16
assume cs:main_03, ds:DGROUP
public SET_GATHER_TEMPLATE_TO_BULLET_TEMPLATE
SET_GATHER_TEMPLATE_TO_BULLET_TEMPLATE proc near
    push bp
    mov bp, sp
    push si
    push di
    mov cx, GATHER_BULLET_WORDS
    push ds
    pop es
    mov si, offset _bullet_template
    mov di, word ptr [bp + 4]
    add di, GATHER_BULLET_OFFSET
    rep movsw
    pop di
    pop si
    pop bp
    ret 2
SET_GATHER_TEMPLATE_TO_BULLET_TEMPLATE endp
public gather_copy_to_end
gather_copy_to_end label byte
GATHER_COPY_TO_TEXT ends
end
