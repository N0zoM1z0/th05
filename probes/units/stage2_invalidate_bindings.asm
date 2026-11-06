; Foreign symbol addresses around the complete stage-two invalidator.
.386
.model large
_TEXT segment word public 'CODE' use16
org 0ae10h
_TEXT ends
STAGE2_TEXT segment byte public 'CODE' use16
STAGE2_TEXT ends
STAGE2_INVALIDATE_TEXT segment byte public 'CODE' use16
assume cs:STAGE2_INVALIDATE_TEXT
public TILES_INVALIDATE_AROUND
org (0bad2h - 0ae10h)
TILES_INVALIDATE_AROUND label near
org (116cdh - 0ae10h)
STAGE2_INVALIDATE_TEXT ends
STAGE2_INVALIDATE_AFTER_TEXT segment byte public 'CODE' use16
org (14ab0h - 11700h)
STAGE2_INVALIDATE_AFTER_TEXT ends
main_01 group STAGE2_TEXT, STAGE2_INVALIDATE_TEXT, STAGE2_INVALIDATE_AFTER_TEXT
SHARED segment byte public 'CODE' use16
org (209d0h - 14ab0h)
SHARED ends
_DATA segment word public 'DATA' use16
public _tile_invalidate_box, _custom_entities
org 03502h
_tile_invalidate_box label word
org 0b3f4h
_custom_entities label byte
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end
