; Dirty-tile invalidation for pellets, large bullets and gather rings.
; Semantic native ASM following the original TH04 family with TH05 fields.
.386
.model large
locals
include types.inc
include symbols.inc

main_01 group BULLET_GATHER_INV_TEXT
BULLET_GATHER_INV_TEXT segment byte public 'CODE' use16
assume cs:main_01, ds:DGROUP
public bullets_and_gather_invalidate, bullets_and_gather_invalidate_end
bullets_and_gather_invalidate proc near
    push si
    push di
    mov si, offset _bullets
    mov di, PELLET_COUNT
    mov dword ptr _tile_invalidate_box, ((PELLET_H shl 16) or PELLET_W)
    cmp _bullet_zap_active, 0
    jnz short @@pellets_decaying
    cmp _bullet_clear_time, 0
    jnz short @@pellets_decaying
@@pellet_loop:
    cmp byte ptr [si+BULLET_FLAG], ENTITY_FREE
    jz short @@pellet_next
    cmp byte ptr [si+BULLET_SPAWN_FLAG], BULLET_GRAZED
    jbe short @@pellet_normal
    shl dword ptr _tile_invalidate_box, 1
    push dword ptr [si+BULLET_POS_PREV]
    call tiles_invalidate_around
    shr dword ptr _tile_invalidate_box, 1
    jmp short @@pellet_next
@@pellet_normal:
    push dword ptr [si+BULLET_POS_PREV]
    call tiles_invalidate_around
@@pellet_next:
    add si, BULLET_RECORD_BYTES
    dec di
    jnz short @@pellet_loop
@@pellets_decaying:
    add di, BULLET16_COUNT
    shl dword ptr _tile_invalidate_box, 1
@@bullet16_loop:
    cmp byte ptr [si+BULLET_FLAG], ENTITY_FREE
    jz short @@bullet16_next
    cmp byte ptr [si+BULLET_SPAWN_FLAG], BULLET_GRAZED
    jbe short @@bullet16_normal
    shl dword ptr _tile_invalidate_box, 1
    push dword ptr [si+BULLET_POS_PREV]
    call tiles_invalidate_around
    shr dword ptr _tile_invalidate_box, 1
    jmp short @@bullet16_next
@@bullet16_normal:
    push dword ptr [si+BULLET_POS_PREV]
    call tiles_invalidate_around
@@bullet16_next:
    add si, BULLET_RECORD_BYTES
    dec di
    jnz short @@bullet16_loop
    mov si, offset _gather_circles
    mov di, GATHER_COUNT
@@gather_loop:
    cmp byte ptr [si+GATHER_FLAG], ENTITY_FREE
    jz short @@gather_next
    mov ax, [si+GATHER_RADIUS_CUR]
    shr ax, GATHER_RADIUS_TO_PIXELS
    add ax, GATHER_HALF_WIDTH_BASE
    mov word ptr _tile_invalidate_box, ax
    mov word ptr _tile_invalidate_box+2, ax
    push dword ptr [si+GATHER_POS_PREV]
    call tiles_invalidate_around
@@gather_next:
    add si, GATHER_RECORD_BYTES
    dec di
    jnz short @@gather_loop
    pop di
    pop si
    ret
bullets_and_gather_invalidate endp
bullets_and_gather_invalidate_end label byte
BULLET_GATHER_INV_TEXT ends
end
