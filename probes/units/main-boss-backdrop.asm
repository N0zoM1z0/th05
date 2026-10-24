; Original address-only main-boss-backdrop context. No bodies/data/stack.
.386
.model large
MAIN01_BASE equ 0ae10h
SHARED_BASE equ 14ab0h
MAIN03_BASE equ 15270h
DGROUP_BASE equ 209d0h
UNIT_START equ 0109f0h
UNIT_SIZE equ 027h
UNIT_END equ (UNIT_START + UNIT_SIZE)
_TEXT segment word public 'CODE' use16
org MAIN01_BASE
_TEXT ends
BOSS_BD_TEXT segment byte public 'CODE' use16
assume cs:BOSS_BD_TEXT
public @grcg_setmode_tdw$qv
org 013eeh
@grcg_setmode_tdw$qv label near
public @grcg_setcolor_direct_raw$qv
org 013f4h
@grcg_setcolor_direct_raw$qv label near
org (UNIT_START - MAIN01_BASE)
BOSS_BD_TEXT ends
SMALL_EXTRA_MAIN01_TAIL segment byte public 'CODE' use16
org (SHARED_BASE - UNIT_END)
SMALL_EXTRA_MAIN01_TAIL ends
main_01 group BOSS_BD_TEXT, SMALL_EXTRA_MAIN01_TAIL
SMALL_EXTRA_SHARED segment para public 'CODE' use16
assume cs:SMALL_EXTRA_SHARED
public CDG_PUT_NOALPHA_8
org 01c0h
CDG_PUT_NOALPHA_8 label far
org (MAIN03_BASE - SHARED_BASE)
SMALL_EXTRA_SHARED ends
SMALL_EXTRA_MAIN03_SPACE segment byte public 'CODE' use16
org (DGROUP_BASE - MAIN03_BASE)
SMALL_EXTRA_MAIN03_SPACE ends
_DATA segment word public 'DATA' use16
public _boss_backdrop_colorfill
org 04446h
_boss_backdrop_colorfill label word
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end
