; Main gameplay's original GRCG read/modify, tile-direct and direct-color I/O.
.386
.model large
locals
include types.inc
include symbols.inc
main_01 group GRCG_MODECOL_TEXT
GRCG_MODECOL_TEXT segment byte public 'CODE' use16
assume cs:main_01, ds:DGROUP
public @grcg_setmode_rmw$qv, @grcg_setmode_tdw$qv
public @grcg_setcolor_direct_raw$qv, grcg_modecol_end
@grcg_setmode_rmw$qv proc near
    mov al, GRCG_RMW
    out GRCG_MODE_PORT, al
    ret
@grcg_setmode_rmw$qv endp
    even
@grcg_setmode_tdw$qv proc near
    mov al, GRCG_TDW
    out GRCG_MODE_PORT, al
    ret
@grcg_setmode_tdw$qv endp
    even
@grcg_setcolor_direct_raw$qv proc near
    cli
    mov dx, GRCG_TILE_PORT
    rept 4
        shr ah, 1
        sbb al, al
        out dx, al
    endm
    sti
    ret
@grcg_setcolor_direct_raw$qv endp
grcg_modecol_end label byte
GRCG_MODECOL_TEXT ends
end
