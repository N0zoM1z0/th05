; Original-address symbols only for main-hud-hp. No bodies, values or .stack.
.386
.model large
MAIN01_BASE equ 0ae10h
SHARED_BASE equ 14ab0h
MAIN03_BASE equ 15270h
DGROUP_BASE equ 209d0h
UNIT_START equ 01c4f6h
UNIT_SIZE equ 058h
UNIT_END equ (UNIT_START + UNIT_SIZE)
_TEXT segment word public 'CODE' use16
org MAIN01_BASE
_TEXT ends
SMALL_MAIN01_CONTEXT segment byte public 'CODE' use16
SMALL_MAIN01_CONTEXT ends
SMALL_MAIN01_SPACE segment byte public 'CODE' use16
assume cs:SMALL_MAIN01_SPACE
public @HUD_HP_PUT$QI
org (0d28bh - MAIN01_BASE)
@HUD_HP_PUT$QI label far
org (SHARED_BASE - MAIN01_BASE)
SMALL_MAIN01_SPACE ends
main_01 group SMALL_MAIN01_CONTEXT, SMALL_MAIN01_SPACE
SMALL_SHARED_SPACE segment para public 'CODE' use16
org (MAIN03_BASE - SHARED_BASE)
SMALL_SHARED_SPACE ends
HUD_HP_TEXT segment byte public 'CODE' use16
org (UNIT_START - MAIN03_BASE)
HUD_HP_TEXT ends
SMALL_MAIN03_TAIL segment byte public 'CODE' use16
org (DGROUP_BASE - UNIT_END)
SMALL_MAIN03_TAIL ends
main_03 group HUD_HP_TEXT, SMALL_MAIN03_TAIL
_DATA segment word public 'DATA' use16
public _hud_hp_bar_value_prev
org 01a5eh
_hud_hp_bar_value_prev label word
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end
