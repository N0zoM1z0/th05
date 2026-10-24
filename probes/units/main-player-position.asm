; Original-address symbols only for main-player-position. No bodies, values or .stack.
.386
.model large
MAIN01_BASE equ 0ae10h
SHARED_BASE equ 14ab0h
MAIN03_BASE equ 15270h
DGROUP_BASE equ 209d0h
UNIT_START equ 0cad2h
UNIT_SIZE equ 038h
UNIT_END equ (UNIT_START + UNIT_SIZE)
_TEXT segment word public 'CODE' use16
org MAIN01_BASE
_TEXT ends
SMALL_MAIN01_CONTEXT segment byte public 'CODE' use16
SMALL_MAIN01_CONTEXT ends
PLAYER_P_TEXT segment byte public 'CODE' use16
assume cs:PLAYER_P_TEXT
public @PlayfieldMotion@update_seg1$qv
org (0be1ah - MAIN01_BASE)
@PlayfieldMotion@update_seg1$qv label near
org (UNIT_START - MAIN01_BASE)
PLAYER_P_TEXT ends
SMALL_MAIN01_TAIL segment byte public 'CODE' use16
assume cs:SMALL_MAIN01_TAIL
org (SHARED_BASE - UNIT_END)
SMALL_MAIN01_TAIL ends
main_01 group SMALL_MAIN01_CONTEXT, PLAYER_P_TEXT, SMALL_MAIN01_TAIL
SMALL_SHARED_SPACE segment para public 'CODE' use16
org (MAIN03_BASE - SHARED_BASE)
SMALL_SHARED_SPACE ends
SMALL_MAIN03_SPACE segment byte public 'CODE' use16
org (DGROUP_BASE - MAIN03_BASE)
SMALL_MAIN03_SPACE ends
main_03 group SMALL_MAIN03_SPACE
_DATA segment word public 'DATA' use16
public _player_pos
org 036d2h
_player_pos label byte
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end
