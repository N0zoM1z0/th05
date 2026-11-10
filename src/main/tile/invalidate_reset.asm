; Restore the complete 50 x 32 dirty flag bank to zero.
; Original typed helper uses ES:DI and a 32-bit string operation.
.386
.model large
locals
include types.inc
include symbols.inc
DIRTY_RESET_DWORDS equ DIRTY_MAP_DWORDS

main_01 group TILE_INVALIDATE_RESET_TEXT
TILE_INVALIDATE_RESET_TEXT segment byte public 'CODE' use16
assume cs:main_01, ds:DGROUP
public @TILES_INVALIDATE_RESET$QV
@TILES_INVALIDATE_RESET$QV proc near
    push di
    mov ax, ds
    mov es, ax
    mov di, offset _halftiles_dirty
    xor eax, eax
    mov cx, DIRTY_RESET_DWORDS
    rep stosd
    pop di
    ret
@TILES_INVALIDATE_RESET$QV endp
    even
public tile_invalidate_reset_end
tile_invalidate_reset_end label byte
TILE_INVALIDATE_RESET_TEXT ends
end
