; Symbol-only foreign context. No lifecycle code, storage or padding emitted.
.386
.model large
MAIN01_BASE equ 0ae10h
SHARED_BASE equ 14ab0h
MAIN03_BASE equ 15270h
UNIT_START equ 0e16eh
AFTER_BASE equ 0e220h
DGROUP_BASE equ 209d0h
_TEXT segment word public 'CODE' use16
assume cs:_TEXT
org MAIN01_BASE
_TEXT ends
POINTNUM_LIFE_PREFIX segment byte public 'CODE' use16
assume cs:POINTNUM_LIFE_PREFIX
public TILES_INVALIDATE_AROUND
org (0bad2h - MAIN01_BASE)
TILES_INVALIDATE_AROUND label near
org (UNIT_START - MAIN01_BASE)
POINTNUM_LIFE_PREFIX ends
POINTNUM_LIFE_TEXT segment byte public 'CODE' use16
POINTNUM_LIFE_TEXT ends
POINTNUM_LIFE_AFTER segment para public 'CODE' use16
org (SHARED_BASE - AFTER_BASE)
POINTNUM_LIFE_AFTER ends
main_01 group POINTNUM_LIFE_PREFIX, POINTNUM_LIFE_TEXT, POINTNUM_LIFE_AFTER
POINTNUM_LIFE_SHARED segment para public 'CODE' use16
org (MAIN03_BASE - SHARED_BASE)
POINTNUM_LIFE_SHARED ends
POINTNUM_LIFE_MAIN03 segment byte public 'CODE' use16
org (DGROUP_BASE - MAIN03_BASE)
POINTNUM_LIFE_MAIN03 ends
main_03 group POINTNUM_LIFE_MAIN03
_DATA segment word public 'DATA' use16
public _tile_invalidate_box, _pointnum_white_p, _pointnum_yellow_p
public _pointnums_alive, _pointnum_first_yellow_alive, _pointnums
org 3502h
_tile_invalidate_box label byte
org 3fa4h
_pointnum_white_p label byte
org 3fa5h
_pointnum_yellow_p label byte
org 3fa6h
_pointnums_alive label word
org 41d8h
_pointnum_first_yellow_alive label word
org 9f04h
_pointnums label byte
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end
