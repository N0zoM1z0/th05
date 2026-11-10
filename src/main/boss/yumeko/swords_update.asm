; Original TH05 Yumeko sword lifecycle, 63 native sword_t entities.
; Historical algorithm preserved by ReC98 th05/main/bullet/swords_add_update.asm.
; C++ source remains a separate, inexact experimental lowering.
.386
.model large
locals
include types.inc
include symbols.inc

B5_UPDATE_TEXT segment byte public 'CODE' use16
assume cs:B5_UPDATE_TEXT, ds:DGROUP
main_03 group B5_UPDATE_TEXT
public SWORDS_UPDATE
SWORDS_UPDATE proc near
    push bp
    mov bp, sp
    push si
    push di
    mov si, offset _custom_entities + SWORD_SIZE
    mov di, 1
    jmp @@more
@@loop:
    cmp byte ptr [si+SWORD_FLAG], SWORD_FREE
    je @@next
    cmp _bullet_clear_time, 0
    je short @@still_twirling
    cmp byte ptr [si+SWORD_FLAG], SWORD_ALIVE
    jne short @@still_twirling
    mov byte ptr [si+SWORD_FLAG], SWORD_REMOVE
    mov word ptr [si+SWORD_TWIRL_TIME], 0
@@still_twirling:
    cmp word ptr [si+SWORD_TWIRL_TIME], 0
    jbe short @@no_twirl
    dec word ptr [si+SWORD_TWIRL_TIME]
    cmp word ptr [si+SWORD_TWIRL_TIME], 0
    jne short @@twirl
    push SWORD_PAT_BASE
    push word ptr [si+SWORD_ANGLE]
    call @BULLET_PATNUM_FOR_ANGLE$QUIUC
    mov ah, 0
    mov word ptr [si+SWORD_PATNUM_TINY], ax
    push 3
    call SND_SE_PLAY
    jmp short @@no_twirl
@@twirl:
    test di, 1
    je short @@counterclockwise
    add word ptr [si+SWORD_PATNUM_TINY], SWORD_TWIRL_STEP
    cmp word ptr [si+SWORD_PATNUM_TINY], (SWORD_PAT_BASE + SWORD_CELS)
    jl @@next
    sub word ptr [si+SWORD_PATNUM_TINY], SWORD_CELS
    jmp @@next
@@counterclockwise:
    sub word ptr [si+SWORD_PATNUM_TINY], SWORD_TWIRL_STEP
    cmp word ptr [si+SWORD_PATNUM_TINY], SWORD_PAT_BASE
    jge @@next
    add word ptr [si+SWORD_PATNUM_TINY], SWORD_CELS
    jmp @@next
@@no_twirl:
    lea ax, [si+SWORD_POS]
    push ax
    call @PlayfieldMotion@update_seg3$qv
    cmp ax, -SWORD_CLIP_MARGIN
    jle short @@clip
    cmp ax, (SWORD_PLAYFIELD_W + 16)*16
    jge short @@clip
    cmp dx, -SWORD_CLIP_MARGIN
    jle short @@clip
    cmp dx, (SWORD_PLAYFIELD_H + 16)*16
    jl short @@hittest
@@clip:
    jmp short @@remove
@@hittest:
    cmp byte ptr [si+SWORD_FLAG], SWORD_REMOVE
    je short @@decay
    sub ax, word ptr _player_pos
    sub dx, word ptr _player_pos+2
    add ax, SWORD_PLAYER_RADIUS
    cmp ax, SWORD_PLAYER_DIAMETER
    ja short @@nohit
    add dx, SWORD_PLAYER_RADIUS
    cmp dx, SWORD_PLAYER_DIAMETER
    ja short @@nohit
    mov _player_is_hit, 1
    mov byte ptr [si+SWORD_FLAG], SWORD_REMOVE
    jmp short @@next
@@nohit:
    jmp short @@next
@@decay:
    cmp word ptr [si+SWORD_PATNUM_TINY], SWORD_PAT_DECAY
    jge short @@aging
    mov word ptr [si+SWORD_PATNUM_TINY], SWORD_PAT_DECAY
    mov ax, [si+SWORD_VELOCITY_X]
    cwd
    sub ax, dx
    sar ax, 1
    mov [si+SWORD_VELOCITY_X], ax
    mov ax, [si+SWORD_VELOCITY_Y]
    cwd
    sub ax, dx
    sar ax, 1
    mov [si+SWORD_VELOCITY_Y], ax
    mov word ptr [si+SWORD_DECAY_FRAME], 0
    jmp short @@next
@@aging:
    inc word ptr [si+SWORD_DECAY_FRAME]
    mov ax, [si+SWORD_DECAY_FRAME]
    mov bx, SWORD_DECAY_CELS
    cwd
    idiv bx
    or dx, dx
    jne short @@next
    inc word ptr [si+SWORD_PATNUM_TINY]
    cmp word ptr [si+SWORD_PATNUM_TINY], (SWORD_PAT_DECAY + SWORD_DECAY_CELS)
    jl short @@next
@@remove:
    mov byte ptr [si+SWORD_FLAG], SWORD_FREE
@@next:
    inc di
    add si, SWORD_SIZE
@@more:
    cmp di, (1 + SWORD_COUNT)
    jl @@loop
    pop di
    pop si
    pop bp
    ret
SWORDS_UPDATE endp
public swords_update_end
swords_update_end label byte
B5_UPDATE_TEXT ends
end
