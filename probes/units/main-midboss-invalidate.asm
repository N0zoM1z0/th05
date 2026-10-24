; Original address-only main-midboss-invalidate context. No bodies/data/stack.
.386
.model large
MAIN01_BASE equ 0ae10h
SHARED_BASE equ 14ab0h
MAIN03_BASE equ 15270h
DGROUP_BASE equ 209d0h
UNIT_START equ 0109bdh
UNIT_SIZE equ 033h
UNIT_END equ (UNIT_START + UNIT_SIZE)
_TEXT segment word public 'CODE' use16
org MAIN01_BASE
_TEXT ends
MB_INV_TEXT segment byte public 'CODE' use16
assume cs:MB_INV_TEXT
public TILES_INVALIDATE_AROUND
org 0cc2h
TILES_INVALIDATE_AROUND label near
org (UNIT_START - MAIN01_BASE)
MB_INV_TEXT ends
SMALL_EXTRA_MAIN01_TAIL segment byte public 'CODE' use16
org (SHARED_BASE - UNIT_END)
SMALL_EXTRA_MAIN01_TAIL ends
main_01 group MB_INV_TEXT, SMALL_EXTRA_MAIN01_TAIL
SMALL_EXTRA_SHARED segment para public 'CODE' use16
org (MAIN03_BASE - SHARED_BASE)
SMALL_EXTRA_SHARED ends
SMALL_EXTRA_MAIN03_SPACE segment byte public 'CODE' use16
org (DGROUP_BASE - MAIN03_BASE)
SMALL_EXTRA_MAIN03_SPACE ends
_DATA segment word public 'DATA' use16
public _tile_invalidate_box
org 03502h
_tile_invalidate_box label byte
public _midboss
org 05aa4h
_midboss label byte
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end
