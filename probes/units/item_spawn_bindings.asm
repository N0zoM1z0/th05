; Original address-only context; no bodies/data values/stack.
.386
.model large
_TEXT segment word public 'CODE' use16
assume cs:_TEXT
org 0ae10h
_TEXT ends
HUD_OVRL_TEXT segment word public 'CODE' use16
assume cs:HUD_OVRL_TEXT
HUD_OVRL_TEXT ends
ITEM_FOREIGN_MAIN01 segment byte public 'CODE' use16
assume cs:ITEM_FOREIGN_MAIN01
org 09ca0h
ITEM_FOREIGN_MAIN01 ends
main_01 group HUD_OVRL_TEXT, ITEM_FOREIGN_MAIN01
ITEM_FOREIGN_SHARED segment para public 'CODE' use16
assume cs:ITEM_FOREIGN_SHARED
org 07c0h
ITEM_FOREIGN_SHARED ends
ITEM_SPLASH_TEXT segment byte public 'CODE' use16
assume cs:ITEM_SPLASH_TEXT
public @RANDRING2_NEXT16_AND$QUI
org 03ah
@RANDRING2_NEXT16_AND$QUI label near
public @RANDRING2_NEXT16_MOD$QUI
org 050h
@RANDRING2_NEXT16_MOD$QUI label near
public @ITEM_SPLASHES_ADD$Q20%SUBPIXELBASE$TI$TI%T1
org 0110ch
@ITEM_SPLASHES_ADD$Q20%SUBPIXELBASE$TI$TI%T1 label near
org 079bbh
ITEM_SPLASH_TEXT ends
ITEM_SPAWN_TEXT segment byte public 'CODE' use16
assume cs:ITEM_SPAWN_TEXT
ITEM_SPAWN_TEXT ends
ITEM_SPAWN_MAIN03_TAIL segment byte public 'CODE' use16
assume cs:ITEM_SPAWN_MAIN03_TAIL
org 03c24h
ITEM_SPAWN_MAIN03_TAIL ends
main_03 group ITEM_SPLASH_TEXT, ITEM_SPAWN_TEXT, ITEM_SPAWN_MAIN03_TAIL
_DATA segment word public 'DATA' use16
public _ENEMY_DROPS
org 01dc2h
_ENEMY_DROPS label byte
public _ITEM_PATNUM
org 01e04h
_ITEM_PATNUM label byte
public _items_spawned
org 01e7ah
_items_spawned label byte
public _items_pull_to_player
org 01e84h
_items_pull_to_player label byte
public _ITEM_MISS_VELOCITIES
org 01e86h
_ITEM_MISS_VELOCITIES label byte
public _player_pos
org 036d2h
_player_pos label byte
public _lives
org 04ad4h
_lives label byte
public _items
org 0b084h
_items label byte
public _item_drop_cycle
org 0c654h
_item_drop_cycle label byte
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end
