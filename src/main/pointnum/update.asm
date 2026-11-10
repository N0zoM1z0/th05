; Update the real 280 point popups, compact survivors and select yellow.
; Source semantics from the original 16-byte pointnum_t and TH04 inv_upd.
.386
.model large
locals
include types.inc
include symbols.inc
POINTNUM_POPUP_AGE equ 24
POINTNUM_RISE_PER_FRAME equ ((12 * 16) / POINTNUM_POPUP_AGE)
POINTNUM_EXPIRE_AGE equ 36
POINTNUM_CLIP_BOTTOM equ (-((POINTNUM_H / 2) * 16))
POINTNUM_FREE equ 0
POINTNUM_REMOVED equ 2

main_01 group POINTNUM_UPDATE_TEXT
POINTNUM_UPDATE_TEXT segment byte public 'CODE' use16
assume cs:main_01, ds:DGROUP
public POINTNUMS_UPDATE
POINTNUMS_UPDATE proc near
    push si
    push di
    mov word ptr _pointnum_first_yellow_alive, 0
    mov bx, offset _pointnums_alive
    mov si, offset _pointnums
    mov di, POINTNUM_COUNT
@@next_record:
    cmp byte ptr [si + pointnum_t.PN_flag], POINTNUM_FREE
    je short @@advance
    cmp byte ptr [si + pointnum_t.PN_flag], POINTNUM_REMOVED
    jne short @@alive
    mov byte ptr [si + pointnum_t.PN_flag], POINTNUM_FREE
    jmp short @@advance
@@alive:
    mov cl, [si + pointnum_t.PN_age]
    mov ax, [si + pointnum_t.PN_center_y]
    mov [si + pointnum_t.PN_prev_y], ax
    cmp cl, POINTNUM_POPUP_AGE
    jb short @@store_y
    sub ax, POINTNUM_RISE_PER_FRAME
@@store_y:
    mov [si + pointnum_t.PN_center_y], ax
    cmp ax, POINTNUM_CLIP_BOTTOM
    jg short @@not_clipped
    mov byte ptr [si + pointnum_t.PN_flag], POINTNUM_REMOVED
    jmp short @@advance
@@not_clipped:
    inc cl
    mov [si + pointnum_t.PN_age], cl
    cmp cl, POINTNUM_EXPIRE_AGE
    jbe short @@save_survivor
    mov byte ptr [si + pointnum_t.PN_flag], POINTNUM_REMOVED
    jmp short @@advance
@@save_survivor:
    mov [bx], si
    cmp di, POINTNUM_YELLOW_COUNT
    ja short @@next_survivor
    cmp word ptr _pointnum_first_yellow_alive, 0
    jne short @@next_survivor
    mov _pointnum_first_yellow_alive, si
@@next_survivor:
    add bx, 2
@@advance:
    add si, size pointnum_t
    dec di
    jne short @@next_record
    mov word ptr [bx], 0
    pop di
    pop si
    ret
POINTNUMS_UPDATE endp
    even
public pointnums_update_end
pointnums_update_end label byte
POINTNUM_UPDATE_TEXT ends
end
