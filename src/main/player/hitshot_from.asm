; Actual original HitShot state transfer preserved in ReC98 TH05 source.
; One near Pascal Shot* pointer; RET 2, invalidates Shot before attempting
; to occupy its circular hit-animation slot.
.386
.model large
locals
include types.inc
include symbols.inc

main_01 group HITSHOT_FROM_TEXT
HITSHOT_FROM_TEXT segment byte public 'CODE' use16
assume cs:main_01, ds:DGROUP
public HITSHOT_FROM
HITSHOT_FROM proc near
    push bp
    mov bp, sp
    push si
    push di
    mov di, word ptr [bp+4]
    mov ax, _hitshot_next_free_id
    imul ax, HITSHOT_RECORD_BYTES
    add ax, offset _hitshots
    mov si, ax
    cmp _hitshot_next_free_id, (HITSHOT_COUNT-1)
    jnb short @@wrap_index
    inc _hitshot_next_free_id
    jmp short @@convert_age
@@wrap_index:
    mov _hitshot_next_free_id, 0
@@convert_age:
    mov byte ptr [di+SHOT_FLAG], SHOT_REMOVE
    cmp byte ptr [si+HITSHOT_AGE], 0
    jnz short @@ret
    mov byte ptr [si+HITSHOT_AGE], HITSHOT_ACTIVE
    cmp byte ptr [di+SHOT_PATTERN_BASE], SHOT_REIMU_PATTERN
    jnz short @@other_pattern
    mov byte ptr [si+HITSHOT_PATTERN], HITSHOT_REIMU_PATTERN
    jmp short @@position_and_brake
@@other_pattern:
    mov byte ptr [si+HITSHOT_PATTERN], HITSHOT_OTHER_PATTERN
@@position_and_brake:
    mov eax, dword ptr [di+SHOT_CURRENT_POS]
    mov dword ptr [si+HITSHOT_CURRENT_POS], eax
    mov eax, dword ptr [di+SHOT_PREVIOUS_POS]
    mov dword ptr [si+HITSHOT_PREVIOUS_POS], eax
    mov ax, word ptr [di+SHOT_VELOCITY_X]
    mov bx, HITSHOT_BRAKE_DIVISOR
    cwd
    idiv bx
    mov word ptr [si+HITSHOT_VELOCITY_X], ax
    mov ax, word ptr [di+SHOT_VELOCITY_Y]
    cwd
    idiv bx
    mov word ptr [si+HITSHOT_VELOCITY_Y], ax
@@ret:
    pop di
    pop si
    pop bp
    ret 2
HITSHOT_FROM endp
public hitshot_from_end
hitshot_from_end label byte
HITSHOT_FROM_TEXT ends
end
