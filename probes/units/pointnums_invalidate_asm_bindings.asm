; Real MAIN01 physical prefix, tile invalidation provider and DGROUP globals.
.386
.model large
_TEXT segment word public 'CODE' use16
org 0ae10h
_TEXT ends
POINTNUM_INV_PREFIX segment byte public 'CODE' use16
assume cs:POINTNUM_INV_PREFIX
public TILES_INVALIDATE_AROUND
org (0bad2h - 0ae10h)
TILES_INVALIDATE_AROUND label near
org (0e17ah - 0ae10h)
POINTNUM_INV_PREFIX ends
POINTNUM_INV_TEXT segment byte public 'CODE' use16
POINTNUM_INV_TEXT ends
POINTNUM_INV_TAIL segment para public 'CODE' use16
org (014ab0h - 0e1b0h)
POINTNUM_INV_TAIL ends
main_01 group POINTNUM_INV_PREFIX, POINTNUM_INV_TEXT, POINTNUM_INV_TAIL
POINTNUM_INV_SHARED segment byte public 'CODE' use16
org (015270h - 014ab0h)
POINTNUM_INV_SHARED ends
POINTNUM_INV_MAIN03 segment byte public 'CODE' use16
org (0209d0h - 015270h)
POINTNUM_INV_MAIN03 ends
main_03 group POINTNUM_INV_MAIN03
_DATA segment word public 'DATA' use16
public _tile_invalidate_box, _pointnums
org 03502h
_tile_invalidate_box label byte
org 09f04h
_pointnums label byte
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end
