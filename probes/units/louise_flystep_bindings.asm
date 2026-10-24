; Symbol-only genuine frames for the complete Louise reflecting movement.
; No instructions, state values, helper bodies or inside-function holes.
.386
.model large
MAIN01_BASE equ 0ae10h
SHARED_BASE equ 14ab0h
MAIN03_BASE equ 15270h
UNIT_START equ 1d8beh
AFTER_BASE equ 1d940h
DGROUP_BASE equ 209d0h

_TEXT segment word public 'CODE' use16
org MAIN01_BASE
_TEXT ends
LOUISE_UPDATE_MAIN01_TEXT segment byte public 'CODE' use16
org (SHARED_BASE - MAIN01_BASE)
LOUISE_UPDATE_MAIN01_TEXT ends
LOUISE_MAIN01_CONTEXT segment byte public 'CODE' use16
LOUISE_MAIN01_CONTEXT ends
GENERIC_BOSS_MAIN01_TEXT segment byte public 'CODE' use16
GENERIC_BOSS_MAIN01_TEXT ends
main_01 group LOUISE_UPDATE_MAIN01_TEXT, LOUISE_MAIN01_CONTEXT, GENERIC_BOSS_MAIN01_TEXT

SHARED segment byte public 'CODE' use16
assume cs:SHARED
public VECTOR2
org 0008h
VECTOR2 label far
org (MAIN03_BASE - SHARED_BASE)
SHARED ends

LASER_SC_TEXT segment byte public 'CODE' use16
assume cs:LASER_SC_TEXT
public @randring2_next16$qv
org (1529ch - MAIN03_BASE)
@randring2_next16$qv label near
org (UNIT_START - MAIN03_BASE)
LASER_SC_TEXT ends
BOSS_TEXT segment byte public 'CODE' use16
BOSS_TEXT ends
B4_UPDATE_TEXT segment byte public 'CODE' use16
B4_UPDATE_TEXT ends

; Original full end1D938 precedes this independent real paragraph1D940.
; Source size and all function bytes remain the compiler's responsibility.
LOUISE_FLYSTEP_AFTER_TEXT segment para public 'CODE' use16
org (DGROUP_BASE - AFTER_BASE)
LOUISE_FLYSTEP_AFTER_TEXT ends
main_03 group LASER_SC_TEXT, BOSS_TEXT, B4_UPDATE_TEXT, LOUISE_FLYSTEP_AFTER_TEXT

_DATA segment word public 'DATA' use16
public _boss
org 5abah
_boss label byte
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end
