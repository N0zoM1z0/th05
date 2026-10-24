; Address-only enemy invalidation context; no helper bodies/data/stack.
.386
.model large
_TEXT segment word public 'CODE' use16
assume cs:_TEXT
org 0ae10h
_TEXT ends
HUD_OVRL_TEXT segment word public 'CODE' use16
assume cs:HUD_OVRL_TEXT
HUD_OVRL_TEXT ends
ENEMY_INVALIDATE_TEXT segment byte public 'CODE' use16
assume cs:ENEMY_INVALIDATE_TEXT
public TILES_INVALIDATE_AROUND
org 0cc2h
TILES_INVALIDATE_AROUND label near
org 01370h
ENEMY_INVALIDATE_TEXT ends
ENEMY_INV_MAIN01_TAIL segment byte public 'CODE' use16
assume cs:ENEMY_INV_MAIN01_TAIL
org 08905h
ENEMY_INV_MAIN01_TAIL ends
main_01 group HUD_OVRL_TEXT, ENEMY_INVALIDATE_TEXT, ENEMY_INV_MAIN01_TAIL
ENEMY_INV_SHARED segment para public 'CODE' use16
assume cs:ENEMY_INV_SHARED
org 007c0h
ENEMY_INV_SHARED ends
ENEMY_INV_MAIN03 segment byte public 'CODE' use16
assume cs:ENEMY_INV_MAIN03
org 0b760h
ENEMY_INV_MAIN03 ends
main_03 group ENEMY_INV_MAIN03
_DATA segment word public 'DATA' use16
public _tile_invalidate_box
org 03502h
_tile_invalidate_box label byte
public _enemies
org 093fah
_enemies label byte
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end
