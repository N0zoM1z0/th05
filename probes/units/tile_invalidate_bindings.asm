; Complete foreign half-tile map and outside-only native segment frames.
.386
.model large
_TEXT segment word public 'CODE' use16
org 0ae10h
_TEXT ends
TILE_INVALIDATE_TEXT segment byte public 'CODE' use16
org (0bd38h - 0ae10h)
TILE_INVALIDATE_TEXT ends
TILE_INVALIDATE_TAIL segment byte public 'CODE' use16
org (014ab0h - 0bd4eh)
TILE_INVALIDATE_TAIL ends
main_01 group TILE_INVALIDATE_TEXT, TILE_INVALIDATE_TAIL
SHARED segment para public 'CODE' use16
org (0209d0h - 014ab0h)
SHARED ends
_DATA segment word public 'DATA' use16
public _halftiles_dirty
org 04adah
_halftiles_dirty label byte
org (04adah + 1600)
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end
