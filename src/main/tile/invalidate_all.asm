; Rebuild the full 50 x 32 dirty half-tile flags from a semantic fill value.
; The reference's register-level REP STOSD routine is an assembly kernel;
; this owns no flag data, image/map bytes, table or extra padding.
.386
.model large
locals
include types.inc
include symbols.inc
DIRTY_FLAG_VALUE equ 1
DIRTY_DWORD_VALUE equ (DIRTY_FLAG_VALUE * 01010101h)

main_01 group TILE_INVALIDATE_TEXT
TILE_INVALIDATE_TEXT segment byte public 'CODE' use16
assume cs:main_01, ds:DGROUP
public @TILES_INVALIDATE_ALL$QV
@TILES_INVALIDATE_ALL$QV proc near
    push di
    mov ax, ds
    mov es, ax
    mov di, offset _halftiles_dirty
    mov eax, DIRTY_DWORD_VALUE
    mov cx, DIRTY_MAP_DWORDS
    rep stosd
    pop di
    ret
@TILES_INVALIDATE_ALL$QV endp
public tile_invalidate_all_end
tile_invalidate_all_end label byte
TILE_INVALIDATE_TEXT ends
end
