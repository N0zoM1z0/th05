; Complete hexagram source owns204 bytes. All foreign extents are symbol-only.
.386
.model large
_TEXT segment word public 'CODE' use16
assume cs:_TEXT
public GRCG_CIRCLE, GRCG_LINE
org 010aeh
GRCG_CIRCLE label far
org 01716h
GRCG_LINE label far
org 0ae10h
_TEXT ends
EXALICE_HEX_PREFIX segment byte public 'CODE' use16
org (114beh - 0ae10h)
EXALICE_HEX_PREFIX ends
EXALICE_HEX_TEXT segment byte public 'CODE' use16
EXALICE_HEX_TEXT ends
EXALICE_HEX_TAIL segment byte public 'CODE' use16
org (14ab0h - 1158ah)
EXALICE_HEX_TAIL ends
main_01 group EXALICE_HEX_PREFIX, EXALICE_HEX_TEXT, EXALICE_HEX_TAIL
SHARED segment byte public 'CODE' use16
assume cs:SHARED
public VECTOR2_AT
org 003b0h
VECTOR2_AT label far
org 007c0h
SHARED ends
EXALICE_HEX_FOREIGN03 segment byte public 'CODE' use16
org (209d0h - 15270h)
EXALICE_HEX_FOREIGN03 ends
_DATA segment word public 'DATA' use16
public _drawpoint, _tri_point_1, _tri_point_2
org 036feh
_drawpoint label byte
org 0443ch
_tri_point_1 label byte
org 04440h
_tri_point_2 label byte
org 04444h
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end
