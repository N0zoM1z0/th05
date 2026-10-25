; Genuine foreign frames/provider offsets only; no initialized payload.
.386
.model large
_TEXT segment word public 'CODE' use16
assume cs:_TEXT
public GRC_CLIP_POLYGON_N
org 0139eh
GRC_CLIP_POLYGON_N label far
public GRCG_POLYGON_CX
org 018b4h
GRCG_POLYGON_CX label far
org 0ae10h
_TEXT ends
LASER_RH_TEXT segment word public 'CODE' use16
assume cs:_TEXT
org (0d5c2h-0ae10h)
LASER_RH_TEXT ends
FOREIGN_MAIN01_TAIL segment byte public 'CODE' use16
org (14ab0h-0d71eh)
FOREIGN_MAIN01_TAIL ends
main_01 group LASER_RH_TEXT, FOREIGN_MAIN01_TAIL
SHARED segment para public 'CODE' use16
org (15270h-14ab0h)
SHARED ends
FOREIGN_MAIN03 segment word public 'CODE' use16
org (209d0h-15270h)
FOREIGN_MAIN03 ends
main_03 group FOREIGN_MAIN03
_DATA segment word public 'DATA' use16
public _SinTable8
org 0041ch
_SinTable8 label word
public _CosTable8
org 0049ch
_CosTable8 label word
public _player_pos
org 036d2h
_player_pos label byte
public _player_is_hit
org 036f3h
_player_is_hit label byte
org 0c4c8h
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end
