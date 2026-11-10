; Actual MAIN01 frame and uninitialized tile state, no executable input bytes.
.386
.model large
_TEXT segment word public 'CODE' use16
org 0ae10h
_TEXT ends
TILE_INVALIDATE_RESET_TEXT segment byte public 'CODE' use16
org (0bd24h - 0ae10h)
TILE_INVALIDATE_RESET_TEXT ends
TILE_RESET_FOREIGN_TAIL segment byte public 'CODE' use16
org (014ab0h - 0bd38h)
TILE_RESET_FOREIGN_TAIL ends
main_01 group TILE_INVALIDATE_RESET_TEXT, TILE_RESET_FOREIGN_TAIL
SHARED segment byte public 'CODE' use16
org (015270h - 014ab0h)
SHARED ends
TILE_RESET_MAIN03 segment byte public 'CODE' use16
org (0209d0h - 015270h)
TILE_RESET_MAIN03 ends
main_03 group TILE_RESET_MAIN03
_DATA segment word public 'DATA' use16
public _halftiles_dirty
org 04adah
_halftiles_dirty label byte
org (04adah + (50 * 32))
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end
