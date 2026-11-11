; Native TH05 player invalidation and 20-case movement dispatch, full 16-bit ABI.
; Register and bounds semantics from original controls; not target byte data.
.386
.model large
locals
include types.inc
include symbols.inc

main_01 group PLAYER_REGISTER_TEXT
PLAYER_REGISTER_TEXT segment byte public 'CODE' use16
assume cs:main_01, ds:DGROUP
public player_invalidate, player_move, player_region_register_end
player_invalidate proc near
    mov word ptr _tile_invalidate_box+2, PLAYER_H
    cmp _miss_time, 0
    jz short @@alive
    push di
    mov word ptr _tile_invalidate_box, MISS_EXPLOSION_W
    mov di, _miss_explosion_radius
    add di, -MISS_EXPLOSION_RADIUS_VELOCITY
    mov al, _miss_explosion_angle
    add al, -MISS_EXPLOSION_ANGLE_VELOCITY
    mov ah, MISS_EXPLOSION_COUNT
@@explosion_loop:
    cmp ah, (MISS_EXPLOSION_COUNT / 2)
    jnz short @@invalidate
    shr di, 1
    neg al
@@invalidate:
    push ax
    push offset _drawpoint
    push word ptr _player_pos+PLAYER_POS_CUR_X
    push word ptr _player_pos+PLAYER_POS_CUR_Y
    push di
    push ax
    call VECTOR2_AT
    cmp word ptr _drawpoint+2, CLIP_TOP_Y
    jl short @@next_explosion
    cmp word ptr _drawpoint+2, CLIP_BOTTOM_Y
    jge short @@next_explosion
    cmp word ptr _drawpoint, CLIP_LEFT_X
    jl short @@next_explosion
    cmp word ptr _drawpoint, CLIP_RIGHT_X
    jge short @@next_explosion
    push dword ptr _drawpoint
    call TILES_INVALIDATE_AROUND
@@next_explosion:
    pop ax
    add al, MISS_EXPLOSION_ANGLE_STEP
    dec ah
    jnz short @@explosion_loop
    pop di
    jmp short @@done
@@alive:
    mov word ptr _tile_invalidate_box, PLAYER_W
    push dword ptr _player_pos+PLAYER_POS_PREV
    call TILES_INVALIDATE_AROUND
    mov word ptr _tile_invalidate_box, PLAYER_PLUS_OPTIONS_W
    mov word ptr _tile_invalidate_box+2, PLAYER_OPTION_H
    push dword ptr _player_option_pos_prev
    call TILES_INVALIDATE_AROUND
@@done:
    ret
player_invalidate endp
    even

player_move proc near
    mov bx, sp
    mov bx, ss:[bx+2]
    cmp bl, MOVEMENT_LOW_MAX
    ja short @@invalid
    mov cx, _playchar_speed_diagonal
    mov ax, cx
    mov dx, _playchar_speed_aligned
    and bh, MOVEMENT_HIGH_MASK
    jz short @@switch
    or bl, bl
    jnz short @@invalid
    shr bx, 8
    cmp bl, MOVEMENT_HIGH_MAX
    ja short @@invalid
    add bl, MOVEMENT_HIGH_CASE_OFFSET
@@switch:
    add bx, bx
    jmp word ptr cs:@@switch_table[bx]
@@up:
    neg dx
@@down:
    mov word ptr _player_pos+PLAYER_POS_VEL_Y, dx
    jmp short @@moved
@@left:
    neg dx
@@right:
    mov word ptr _player_pos+PLAYER_POS_VEL_X, dx
    jmp short @@moved
@@up_right:
    neg cx
    jmp short @@down_right
@@up_left:
    neg cx
@@down_left:
    neg ax
@@down_right:
    mov word ptr _player_pos+PLAYER_POS_VEL_X, ax
    mov word ptr _player_pos+PLAYER_POS_VEL_Y, cx
    jmp short @@moved
@@standing_still:
    mov al, MOVE_NOINPUT
    jmp short @@return
@@invalid:
    xor al, al
    jmp short @@return
@@moved:
    mov al, MOVE_VALID
@@return:
    ret 2
@@switch_table label word
    dw @@standing_still, @@up, @@down, @@invalid
    dw @@left, @@up_left, @@down_left, @@invalid
    dw @@right, @@up_right, @@down_right, @@invalid
    dw @@up_left, @@up_right, @@invalid, @@down_left
    dw @@invalid, @@invalid, @@invalid, @@down_right
player_move endp
player_region_register_end label byte
PLAYER_REGISTER_TEXT ends
end
