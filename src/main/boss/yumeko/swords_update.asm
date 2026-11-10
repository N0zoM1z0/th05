; Full original-register gameplay loop for the 63 Yumeko sword entities.
; ReC98 th05/main/bullet/swords_add_update.asm preserves the original
; branch labels, near motion ABI and far Pascal sound call.
.386
.model large
locals
include types.inc
include symbols.inc

main_03 group YUMEKO_SWORD_UPDATE_TEXT
YUMEKO_SWORD_UPDATE_TEXT segment byte public 'CODE' use16
assume cs:main_03, ds:DGROUP
public SWORDS_UPDATE
SWORDS_UPDATE proc near
    push bp
    mov bp, sp
    push si
    push di
    mov si, (offset _custom_entities + SWORD_RECORD_BYTES)
    mov di, 1
    jmp @@more
@@loop:
    cmp byte ptr [si], SWORD_FREE
    je @@next
    cmp byte ptr _bullet_clear_time, 0
    je short @@still_twirling
    cmp byte ptr [si], SWORD_ALIVE
    jne short @@still_twirling
    mov byte ptr [si], SWORD_REMOVE
    mov word ptr [si+SWORD_TWIRL_OFFSET], 0
@@still_twirling:
    cmp word ptr [si+SWORD_TWIRL_OFFSET], 0
    jbe short @@no_twirl
    dec word ptr [si+SWORD_TWIRL_OFFSET]
    cmp word ptr [si+SWORD_TWIRL_OFFSET], 0
    jne short @@twirl
    push SWORD_FIRST_PATTERN
    push word ptr [si+SWORD_ANGLE_OFFSET]
    call @BULLET_PATNUM_FOR_ANGLE$QUIUC
    mov ah, 0
    mov word ptr [si+SWORD_PATTERN_OFFSET], ax
    push 3
    call SND_SE_PLAY
    jmp short @@no_twirl
@@twirl:
    test di, 1
    je short @@twirl_counterclockwise
    add word ptr [si+SWORD_PATTERN_OFFSET], 2
    cmp word ptr [si+SWORD_PATTERN_OFFSET], (SWORD_FIRST_PATTERN+SWORD_VERTICAL_CELS)
    jl @@next
    sub word ptr [si+SWORD_PATTERN_OFFSET], SWORD_VERTICAL_CELS
    jmp @@next
@@twirl_counterclockwise:
    sub word ptr [si+SWORD_PATTERN_OFFSET], 2
    cmp word ptr [si+SWORD_PATTERN_OFFSET], SWORD_FIRST_PATTERN
    jge @@next
    add word ptr [si+SWORD_PATTERN_OFFSET], SWORD_VERTICAL_CELS
    jmp @@next
@@no_twirl:
    lea ax, [si+SWORD_POSITION_OFFSET]
    push ax
    call @PlayfieldMotion@update_seg3$qv
    cmp ax, -SWORD_CLIP_MARGIN_SP
    jle short @@clip
    cmp ax, (SWORD_PLAYFIELD_W_SP+SWORD_CLIP_MARGIN_SP)
    jge short @@clip
    cmp dx, -SWORD_CLIP_MARGIN_SP
    jle short @@clip
    cmp dx, (SWORD_PLAYFIELD_H_SP+SWORD_CLIP_MARGIN_SP)
    jl short @@hitbox_or_decay
@@clip:
    jmp short @@remove
@@hitbox_or_decay:
    cmp byte ptr [si], SWORD_REMOVE
    je short @@in_decay
    sub ax, word ptr _player_pos
    sub dx, word ptr _player_pos+2
    add ax, SWORD_PLAYER_RADIUS_SP
    cmp ax, (2*SWORD_PLAYER_RADIUS_SP)
    ja short @@not_hitting
    add dx, SWORD_PLAYER_RADIUS_SP
    cmp dx, (2*SWORD_PLAYER_RADIUS_SP)
    ja short @@not_hitting
    mov byte ptr _player_is_hit, 1
    mov byte ptr [si], SWORD_REMOVE
    jmp short @@next
@@not_hitting:
    jmp short @@next
@@in_decay:
    cmp word ptr [si+SWORD_PATTERN_OFFSET], SWORD_DECAY_FIRST_PATTERN
    jge short @@already_decaying
    mov word ptr [si+SWORD_PATTERN_OFFSET], SWORD_DECAY_FIRST_PATTERN
    mov ax, [si+SWORD_VELOCITY_X_OFFSET]
    cwd
    sub ax, dx
    sar ax, 1
    mov [si+SWORD_VELOCITY_X_OFFSET], ax
    mov ax, [si+SWORD_VELOCITY_Y_OFFSET]
    cwd
    sub ax, dx
    sar ax, 1
    mov [si+SWORD_VELOCITY_Y_OFFSET], ax
    mov word ptr [si+SWORD_DECAY_FRAME_OFFSET], 0
    jmp short @@next
@@already_decaying:
    inc word ptr [si+SWORD_DECAY_FRAME_OFFSET]
    mov ax, [si+SWORD_DECAY_FRAME_OFFSET]
    mov bx, SWORD_DECAY_MODULUS
    cwd
    idiv bx
    or dx, dx
    jne short @@next
    inc word ptr [si+SWORD_PATTERN_OFFSET]
    cmp word ptr [si+SWORD_PATTERN_OFFSET], (SWORD_DECAY_FIRST_PATTERN+SWORD_DECAY_CELS)
    jl short @@next
@@remove:
    mov byte ptr [si], SWORD_FREE
@@next:
    inc di
    add si, SWORD_RECORD_BYTES
@@more:
    cmp di, (1+SWORD_POOL_COUNT)
    jl @@loop
    pop di
    pop si
    pop bp
    ret
SWORDS_UPDATE endp
public swords_update_end
swords_update_end label byte
YUMEKO_SWORD_UPDATE_TEXT ends
end
